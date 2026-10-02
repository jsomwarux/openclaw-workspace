#!/usr/bin/env python3
"""Deterministic Codex/Claude capacity ledger and task preflight."""

from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
import statistics
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CURRENT = ROOT / "memory/capacity/current.json"
DEFAULT_LEDGER = ROOT / "memory/capacity/usage-ledger.jsonl"
DEFAULT_EXECUTION_LEDGER = ROOT / "memory/capacity/execution-ledger.jsonl"
EXECUTION_SCHEMA = "routing-execution-v1"
PROVIDERS = ("codex", "claude")
TASK_PROVIDERS = {
    "conversation": ("codex",),
    "architecture": ("codex",),
    "prioritization": ("codex",),
    "state": ("codex",),
    "sensitive": ("codex",),
    "verification": ("codex",),
    "buyer_copy": ("codex",),
    "n8n_build": ("claude",),
    "implementation": ("claude",),
    "debugging": ("claude",),
    "adversarial_review": ("claude",),
    "research": ("codex", "claude"),
    "mechanical": ("deterministic",),
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_time(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("recorded_at must be a nonempty ISO 8601 string")
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def capacity_band(remaining: Optional[float]) -> str:
    if remaining is None:
        return "unknown"
    if remaining < 15:
        return "hard_stop"
    if remaining < 25:
        return "reserve"
    if remaining < 40:
        return "critical_only"
    if remaining <= 60:
        return "balance"
    return "normal"


def validate_snapshot(event: Dict[str, Any]) -> Dict[str, Any]:
    provider = event.get("provider")
    if provider not in PROVIDERS:
        raise ValueError(f"provider must be one of {PROVIDERS}")
    remaining = event.get("remaining_percent")
    if remaining is not None:
        remaining = float(remaining)
        if not math.isfinite(remaining) or not 0 <= remaining <= 100:
            raise ValueError("remaining_percent must be finite and between 0 and 100")
        event["remaining_percent"] = remaining
    captured_at = event.get("captured_at")
    if not captured_at:
        raise ValueError("captured_at is required")
    parse_time(captured_at)
    if not event.get("source"):
        raise ValueError("source is required")
    event["band"] = capacity_band(remaining)
    return event


def snapshot_fresh(snapshot: Dict[str, Any], now: datetime, max_age_hours: int = 24) -> bool:
    captured = parse_time(snapshot["captured_at"])
    age_seconds = (now.astimezone(timezone.utc) - captured).total_seconds()
    return 0 <= age_seconds <= max_age_hours * 3600


def route_task(
    snapshots: Dict[str, Dict[str, Any]],
    task_kind: str,
    size: str,
    estimated_burn: float,
    critical: bool = False,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    if task_kind not in TASK_PROVIDERS:
        raise ValueError(f"unknown task_kind: {task_kind}")
    if size not in ("small", "medium", "large"):
        raise ValueError("size must be small, medium, or large")
    if not 0 <= estimated_burn <= 100:
        raise ValueError("estimated_burn must be between 0 and 100")

    candidates = TASK_PROVIDERS[task_kind]
    if candidates == ("deterministic",):
        return {
            "decision": "script",
            "provider": "deterministic",
            "reason": "mechanical work must use deterministic tooling before model capacity",
            "projected_remaining": None,
        }

    check_time = now or utc_now()
    if size == "large":
        for provider in PROVIDERS:
            snap = snapshots.get(provider)
            if not snap or snap.get("remaining_percent") is None:
                return {
                    "decision": "block",
                    "provider": None,
                    "reason": f"{provider} capacity is unknown for a large lane",
                    "projected_remaining": None,
                }
            try:
                remaining = float(snap["remaining_percent"])
                valid_remaining = math.isfinite(remaining) and 0 <= remaining <= 100
                fresh = snapshot_fresh(snap, check_time)
            except (KeyError, TypeError, ValueError, OverflowError):
                valid_remaining = False
                fresh = False
            if not valid_remaining:
                return {
                    "decision": "block",
                    "provider": provider,
                    "reason": f"{provider} capacity snapshot is invalid for a large lane",
                    "projected_remaining": None,
                }
            if not fresh:
                return {
                    "decision": "block",
                    "provider": provider,
                    "reason": f"{provider} capacity snapshot is stale for a large lane",
                    "projected_remaining": None,
                }

    viable = []
    unavailable = []
    for provider in candidates:
        snap = snapshots.get(provider)
        if not snap or snap.get("remaining_percent") is None:
            unavailable.append((provider, "unknown"))
            continue
        try:
            remaining = float(snap["remaining_percent"])
            valid_remaining = math.isfinite(remaining) and 0 <= remaining <= 100
            fresh = snapshot_fresh(snap, check_time)
        except (KeyError, TypeError, ValueError, OverflowError):
            valid_remaining = False
            fresh = False
        if not valid_remaining:
            unavailable.append((provider, "invalid"))
            continue
        if not fresh:
            unavailable.append((provider, "stale"))
            continue
        viable.append((remaining - estimated_burn, remaining, provider))

    if not viable:
        provider = candidates[0]
        state = next((reason for name, reason in unavailable if name == provider), "missing")
        return {
            "decision": "block",
            "provider": provider,
            "reason": f"{provider} capacity snapshot is {state}",
            "projected_remaining": None,
        }

    projected, remaining, provider = max(viable)
    current_band = capacity_band(remaining)
    if remaining < 15 or projected < 15:
        decision = "block"
        reason = f"{provider} is at or would cross the 15% hard stop"
    elif not critical and remaining < 40:
        decision = "block"
        reason = f"{provider} is in {current_band}; only critical work may run"
    elif not critical and projected < 25:
        decision = "block"
        reason = f"{provider} would enter the protected 25% reserve"
    else:
        decision = "route"
        reason = f"route by task fit and projected headroom; {provider} remains at {projected:.1f}%"

    return {
        "decision": decision,
        "provider": provider,
        "reason": reason,
        "remaining_percent": remaining,
        "projected_remaining": projected,
        "band": current_band,
        "critical": critical,
        "size": size,
        "task_kind": task_kind,
    }


def load_current(path: Path = DEFAULT_CURRENT) -> Dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "providers": {}}
    try:
        state = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("current capacity state is not valid JSON") from exc
    if not isinstance(state, dict):
        raise ValueError("current capacity state must be an object")
    providers = state.get("providers", {})
    if not isinstance(providers, dict):
        raise ValueError("current capacity providers must be an object")
    if any(
        not isinstance(provider, str) or not isinstance(snapshot, dict)
        for provider, snapshot in providers.items()
    ):
        raise ValueError("current capacity provider snapshots must be objects")
    return state


def atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temp.replace(path)


def tracking_required(
    task_kind: str,
    batch_items: Optional[int],
    estimated_minutes: Optional[float],
    forced: bool = False,
) -> bool:
    return bool(
        forced
        or task_kind == "buyer_copy"
        or (batch_items is not None and batch_items > 10)
        or (estimated_minutes is not None and estimated_minutes > 10)
    )


def validate_attempt_id(value: str) -> str:
    try:
        return str(uuid.UUID(value))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("attempt_id must be a valid UUID") from exc


def _execution_lock_path(path: Path) -> Path:
    canonical = path.resolve(strict=False)
    if canonical.exists() and canonical.stat().st_nlink > 1:
        raise ValueError("hard-linked execution ledgers are not supported")
    return canonical.with_name(f"{canonical.name}.lock")


def _validate_execution_lifecycle(rows: list[Dict[str, Any]]) -> None:
    preflights: Dict[str, Dict[str, Any]] = {}
    completed: set[str] = set()
    for row in rows:
        attempt_id = row["attempt_id"]
        if row["event_type"] == "preflight":
            if attempt_id in preflights:
                raise ValueError("attempt_id already exists")
            preflights[attempt_id] = row
            continue
        preflight = preflights.get(attempt_id)
        if preflight is None or preflight["task_id"] != row["task_id"]:
            raise ValueError("completion has no matching preflight")
        if preflight["decision"] != "route":
            raise ValueError("blocked preflight cannot have a completion")
        if (
            row["task_kind"] != preflight["task_kind"]
            or row["provider"] != preflight["provider"]
        ):
            raise ValueError("completion routing fields do not match preflight")
        elapsed = (
            parse_time(row["recorded_at"]) - parse_time(preflight["recorded_at"])
        ).total_seconds() / 60
        if elapsed < 0 or not math.isclose(
            row["elapsed_minutes"], elapsed, rel_tol=0, abs_tol=1e-9
        ):
            raise ValueError("completion elapsed time does not match event timestamps")
        if attempt_id in completed:
            raise ValueError("attempt is already complete")
        completed.add(attempt_id)


def _read_execution_rows_unlocked(path: Path) -> list[Dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid execution ledger JSON at line {line_number}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"execution ledger line {line_number} must be an object")
        try:
            _validate_execution_event(row)
        except ValueError as exc:
            raise ValueError(
                f"invalid execution ledger event at line {line_number}: {exc}"
            ) from exc
        rows.append(row)
    _validate_execution_lifecycle(rows)
    return rows


def read_execution_events(path: Path = DEFAULT_EXECUTION_LEDGER) -> list[Dict[str, Any]]:
    lock_path = _execution_lock_path(path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_SH)
        try:
            return _read_execution_rows_unlocked(path)
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def _validate_execution_event(event: Dict[str, Any]) -> None:
    required = ("schema_version", "event_type", "recorded_at", "task_id", "attempt_id")
    missing = [field for field in required if not event.get(field)]
    if missing:
        raise ValueError(f"execution event missing required fields: {', '.join(missing)}")
    if event["schema_version"] != EXECUTION_SCHEMA:
        raise ValueError(f"schema_version must be {EXECUTION_SCHEMA}")
    if event["event_type"] not in ("preflight", "complete"):
        raise ValueError("event_type must be preflight or complete")
    if not isinstance(event["task_id"], str) or not event["task_id"].strip():
        raise ValueError("task_id must be a nonempty string")
    parse_time(event["recorded_at"])
    validate_attempt_id(event["attempt_id"])
    if event["event_type"] == "preflight":
        required_preflight = (
            "task",
            "task_kind",
            "size",
            "estimated_burn",
            "estimated_minutes",
            "batch_items",
            "decision",
            "provider",
            "reason",
            "tracking_required",
        )
        missing_preflight = [field for field in required_preflight if field not in event]
        if missing_preflight:
            raise ValueError(
                "preflight missing required fields: " + ", ".join(missing_preflight)
            )
        if not isinstance(event["task"], str) or not event["task"].strip():
            raise ValueError("task must be a nonempty string")
        task_kind = event["task_kind"]
        if task_kind not in TASK_PROVIDERS:
            raise ValueError("preflight task_kind is invalid")
        if event["size"] not in ("small", "medium", "large"):
            raise ValueError("preflight size is invalid")
        burn = _finite_nonnegative(event["estimated_burn"], "estimated_burn")
        if burn > 100:
            raise ValueError("estimated_burn must be between 0 and 100")
        if event["estimated_minutes"] is not None:
            _finite_nonnegative(event["estimated_minutes"], "estimated_minutes")
        _optional_nonnegative_integer(event["batch_items"], "batch_items")
        decision = event["decision"]
        provider = event["provider"]
        if decision not in ("route", "block", "script"):
            raise ValueError("preflight decision is invalid")
        allowed = TASK_PROVIDERS[task_kind]
        if decision == "route" and provider not in allowed:
            raise ValueError("routed provider does not match task_kind ownership")
        if decision == "script" and (task_kind != "mechanical" or provider != "deterministic"):
            raise ValueError("script decision must use deterministic mechanical routing")
        if decision == "block" and provider is not None and provider not in allowed:
            raise ValueError("blocked provider does not match task_kind ownership")
        if not isinstance(event["reason"], str) or not event["reason"].strip():
            raise ValueError("reason must be a nonempty string")
        if event["tracking_required"] is not True:
            raise ValueError("tracking_required must be true")
        return

    required_completion = (
        "task_kind",
        "provider",
        "elapsed_minutes",
        "tool_calls",
        "provider_delta",
        "avoidable_delay_minutes",
        "delivery_status",
        "sla_verdict",
    )
    missing_completion = [field for field in required_completion if field not in event]
    if missing_completion:
        raise ValueError(
            "completion missing required fields: " + ", ".join(missing_completion)
        )
    task_kind = event["task_kind"]
    if task_kind not in TASK_PROVIDERS or event["provider"] not in PROVIDERS:
        raise ValueError("completion task_kind or provider is invalid")
    if event["provider"] not in TASK_PROVIDERS[task_kind]:
        raise ValueError("completion provider does not match task_kind ownership")
    elapsed = _finite_nonnegative(event["elapsed_minutes"], "elapsed_minutes")
    if isinstance(event["tool_calls"], bool) or not isinstance(event["tool_calls"], int) or event["tool_calls"] < 0:
        raise ValueError("tool_calls must be a nonnegative integer")
    _validated_provider_delta(event["provider_delta"])
    delay = _finite_nonnegative(event["avoidable_delay_minutes"], "avoidable_delay_minutes")
    if delay > elapsed:
        raise ValueError("avoidable_delay_minutes cannot exceed elapsed time")
    if event["delivery_status"] not in ("delivered", "not_delivered"):
        raise ValueError("delivery_status is invalid")
    delivered = event["delivery_status"] == "delivered"
    expected_sla = buyer_copy_sla(task_kind, delivered, elapsed)
    if event["sla_verdict"] != expected_sla:
        raise ValueError("sla_verdict does not match completion telemetry")


def _append_execution_event_unlocked(path: Path, event: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def append_execution_event(path: Path, event: Dict[str, Any]) -> None:
    _validate_execution_event(event)
    lock_path = _execution_lock_path(path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            rows = _read_execution_rows_unlocked(path)
            _validate_execution_lifecycle([*rows, event])
            _append_execution_event_unlocked(path, event)
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def _finite_nonnegative(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be numeric, not boolean")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not math.isfinite(parsed) or parsed < 0:
        raise ValueError(f"{field} must be finite and nonnegative")
    return parsed


def _optional_nonnegative_integer(value: Any, field: str) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")
    return value


def record_preflight(
    *,
    task_id: Optional[str],
    task: str,
    attempt_id: Optional[str],
    task_kind: str,
    size: str,
    estimated_burn: float,
    estimated_minutes: Optional[float],
    batch_items: Optional[int],
    forced: bool,
    result: Dict[str, Any],
    ledger_path: Path,
    recorded_at: datetime,
) -> Optional[Dict[str, Any]]:
    burn = _finite_nonnegative(estimated_burn, "estimated_burn")
    if burn > 100:
        raise ValueError("estimated_burn must be between 0 and 100")
    minutes = None if estimated_minutes is None else _finite_nonnegative(
        estimated_minutes, "estimated_minutes"
    )
    items = _optional_nonnegative_integer(batch_items, "batch_items")
    required = tracking_required(task_kind, items, minutes, forced)
    if not required:
        return None
    if not task_id or not str(task_id).strip():
        raise ValueError("task_id is required for tracked preflight")
    normalized_attempt = validate_attempt_id(attempt_id) if attempt_id else str(uuid.uuid4())
    event = {
        "schema_version": EXECUTION_SCHEMA,
        "event_type": "preflight",
        "recorded_at": recorded_at.astimezone(timezone.utc).isoformat(),
        "task_id": str(task_id),
        "attempt_id": normalized_attempt,
        "task": task,
        "task_kind": task_kind,
        "size": size,
        "estimated_burn": burn,
        "estimated_minutes": minutes,
        "batch_items": items,
        "decision": result.get("decision"),
        "provider": result.get("provider"),
        "reason": result.get("reason"),
        "tracking_required": True,
    }
    append_execution_event(ledger_path, event)
    return event


def buyer_copy_sla(task_kind: str, delivered: bool, elapsed_minutes: float) -> str:
    if task_kind != "buyer_copy":
        return "not_applicable"
    if not delivered:
        return "missed_delivery"
    if elapsed_minutes <= 12:
        return "on_target"
    if elapsed_minutes <= 15:
        return "warning"
    return "breach"


def parse_provider_delta(value: str) -> Optional[float]:
    if value.lower() == "unknown":
        return None
    parsed = _finite_nonnegative(value, "provider_delta")
    if parsed > 100:
        raise ValueError("provider_delta must be between 0 and 100")
    return parsed


def _validated_provider_delta(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    parsed = _finite_nonnegative(value, "provider_delta")
    if parsed > 100:
        raise ValueError("provider_delta must be between 0 and 100")
    return parsed


def record_completion(
    *,
    task_id: str,
    attempt_id: str,
    tool_calls: int,
    provider_delta: Optional[float],
    avoidable_delay_minutes: float,
    delivered: bool,
    ledger_path: Path,
    recorded_at: datetime,
) -> Dict[str, Any]:
    normalized_attempt = validate_attempt_id(attempt_id)
    if not task_id or not str(task_id).strip():
        raise ValueError("task_id is required")
    if isinstance(tool_calls, bool) or not isinstance(tool_calls, int) or tool_calls < 0:
        raise ValueError("tool_calls must be a nonnegative integer")
    delta = _validated_provider_delta(provider_delta)
    delay = _finite_nonnegative(avoidable_delay_minutes, "avoidable_delay_minutes")
    completed_at = recorded_at.astimezone(timezone.utc)

    lock_path = _execution_lock_path(ledger_path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            rows = _read_execution_rows_unlocked(ledger_path)
            matching = [
                row
                for row in rows
                if row.get("event_type") == "preflight"
                and row.get("attempt_id") == normalized_attempt
                and row.get("task_id") == task_id
            ]
            if len(matching) != 1:
                raise ValueError("matching tracked preflight not found")
            preflight = matching[0]
            if preflight.get("decision") != "route":
                raise ValueError("blocked preflight cannot be completed")
            if any(
                row.get("event_type") == "complete"
                and row.get("attempt_id") == normalized_attempt
                for row in rows
            ):
                raise ValueError("attempt is already complete")
            elapsed = (completed_at - parse_time(preflight["recorded_at"])).total_seconds() / 60
            if not math.isfinite(elapsed) or elapsed < 0:
                raise ValueError("completion time must not precede preflight")
            if delay > elapsed:
                raise ValueError("avoidable_delay_minutes cannot exceed elapsed time")
            event = {
                "schema_version": EXECUTION_SCHEMA,
                "event_type": "complete",
                "recorded_at": completed_at.isoformat(),
                "task_id": task_id,
                "attempt_id": normalized_attempt,
                "task_kind": preflight.get("task_kind"),
                "provider": preflight.get("provider"),
                "elapsed_minutes": elapsed,
                "tool_calls": tool_calls,
                "provider_delta": delta,
                "avoidable_delay_minutes": delay,
                "delivery_status": "delivered" if delivered else "not_delivered",
                "sla_verdict": buyer_copy_sla(
                    preflight.get("task_kind"), delivered, elapsed
                ),
            }
            _validate_execution_event(event)
            _validate_execution_lifecycle([*rows, event])
            _append_execution_event_unlocked(ledger_path, event)
            return event
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def summarize_execution(
    ledger_path: Path = DEFAULT_EXECUTION_LEDGER,
    days: int = 7,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
        raise ValueError("days must be a positive integer")
    end = (now or utc_now()).astimezone(timezone.utc)
    cutoff = end - timedelta(days=days)
    completions = [
        row
        for row in read_execution_events(ledger_path)
        if row.get("event_type") == "complete"
        and cutoff <= parse_time(row["recorded_at"]) <= end
    ]
    elapsed = [float(row["elapsed_minutes"]) for row in completions]
    tool_calls = [int(row["tool_calls"]) for row in completions]
    sla_counts = {"on_target": 0, "warning": 0, "breach": 0, "missed_delivery": 0}
    for row in completions:
        verdict = row.get("sla_verdict")
        if row.get("task_kind") == "buyer_copy" and verdict in sla_counts:
            sla_counts[verdict] += 1
    return {
        "window_days": days,
        "completion_count": len(completions),
        "delivered_count": sum(
            row.get("delivery_status") == "delivered" for row in completions
        ),
        "undelivered_count": sum(
            row.get("delivery_status") == "not_delivered" for row in completions
        ),
        "median_elapsed_minutes": statistics.median(elapsed) if elapsed else None,
        "median_tool_calls": statistics.median(tool_calls) if tool_calls else None,
        "avoidable_delay_minutes": sum(
            float(row.get("avoidable_delay_minutes", 0)) for row in completions
        ),
        "buyer_copy_sla": sla_counts,
    }


def record_snapshot(event: Dict[str, Any], current_path: Path, ledger_path: Path) -> None:
    validated = validate_snapshot(dict(event))
    state = load_current(current_path)
    state.setdefault("schema_version", 1)
    state.setdefault("providers", {})[validated["provider"]] = validated
    state["updated_at"] = validated["captured_at"]
    atomic_write_json(current_path, state)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a") as handle:
        handle.write(json.dumps(validated, sort_keys=True) + "\n")


def parse_remaining(value: str) -> Optional[float]:
    if value.lower() == "unknown":
        return None
    return float(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current", type=Path, default=DEFAULT_CURRENT)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--execution-ledger", type=Path, default=DEFAULT_EXECUTION_LEDGER)
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record", help="record a provider capacity snapshot")
    record.add_argument("--provider", choices=PROVIDERS, required=True)
    record.add_argument("--remaining", required=True, help="0-100 or unknown")
    record.add_argument("--reset-at")
    record.add_argument("--captured-at")
    record.add_argument("--source", required=True)
    record.add_argument("--note")

    preflight = sub.add_parser("preflight", help="route or block a proposed task")
    preflight.add_argument("--task", required=True)
    preflight.add_argument("--task-kind", choices=tuple(TASK_PROVIDERS), required=True)
    preflight.add_argument("--size", choices=("small", "medium", "large"), required=True)
    preflight.add_argument("--estimated-burn", type=float, required=True)
    preflight.add_argument("--critical", action="store_true")
    preflight.add_argument("--task-id")
    preflight.add_argument("--attempt-id")
    preflight.add_argument("--estimated-minutes", type=float)
    preflight.add_argument("--batch-items", type=int)
    preflight.add_argument("--track", action="store_true")

    complete = sub.add_parser("complete", help="record completion telemetry")
    complete.add_argument("--task-id", required=True)
    complete.add_argument("--attempt-id", required=True)
    complete.add_argument("--tool-calls", type=int, required=True)
    complete.add_argument("--provider-delta", required=True, help="0-100 or unknown")
    complete.add_argument("--avoidable-delay-minutes", type=float, required=True)
    delivery = complete.add_mutually_exclusive_group(required=True)
    delivery.add_argument("--delivered", action="store_true")
    delivery.add_argument("--not-delivered", action="store_true")

    summary = sub.add_parser("summary", help="summarize execution telemetry")
    summary.add_argument("--days", type=int, default=7)

    sub.add_parser("status", help="show current capacity snapshots")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "record":
        try:
            event = {
                "provider": args.provider,
                "remaining_percent": parse_remaining(args.remaining),
                "reset_at": args.reset_at,
                "captured_at": args.captured_at or utc_now().isoformat(),
                "source": args.source,
                "note": args.note,
            }
            record_snapshot(event, args.current, args.ledger)
            print(json.dumps(validate_snapshot(event), indent=2, sort_keys=True))
        except (TypeError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        return 0
    if args.command == "status":
        try:
            state = load_current(args.current)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(state, indent=2, sort_keys=True))
        return 0
    if args.command == "summary":
        try:
            result = summarize_execution(args.execution_ledger, args.days)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if args.command == "complete":
        try:
            result = record_completion(
                task_id=args.task_id,
                attempt_id=args.attempt_id,
                tool_calls=args.tool_calls,
                provider_delta=parse_provider_delta(args.provider_delta),
                avoidable_delay_minutes=args.avoidable_delay_minutes,
                delivered=args.delivered,
                ledger_path=args.execution_ledger,
                recorded_at=utc_now(),
            )
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    try:
        state = load_current(args.current)
        result = route_task(
            snapshots=state.get("providers", {}),
            task_kind=args.task_kind,
            size=args.size,
            estimated_burn=args.estimated_burn,
            critical=args.critical,
        )
        result["task"] = args.task
        event = record_preflight(
            task_id=args.task_id,
            task=args.task,
            attempt_id=args.attempt_id,
            task_kind=args.task_kind,
            size=args.size,
            estimated_burn=args.estimated_burn,
            estimated_minutes=args.estimated_minutes,
            batch_items=args.batch_items,
            forced=args.track,
            result=result,
            ledger_path=args.execution_ledger,
            recorded_at=utc_now(),
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    result["tracking_required"] = event is not None
    if event is not None:
        result["attempt_id"] = event["attempt_id"]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["decision"] == "block" else 0


if __name__ == "__main__":
    sys.exit(main())
