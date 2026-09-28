"""Append-only storage for validated LinkedIn Program 0 outcome events."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from scripts.linkedin_content_os.canonical import (
    _append_jsonl_exact_prefix_locked as append_jsonl_exact_prefix,
    _exclusive_path_lock,
    read_jsonl,
)
from scripts.linkedin_content_os.contracts import parse_timestamp, validate_event


def validate_event_sequence(rows: list[dict[str, object]]) -> None:
    """Validate cross-event invariants that one event cannot prove alone."""

    by_id = {str(row["outcomeEventId"]): row for row in rows}
    by_hash = {str(row["eventSha256"]): row for row in rows}
    correction_edges: dict[str, str] = {}
    replacement_ids: set[str] = set()
    for correction in rows:
        if correction["eventType"] != "correction":
            continue
        payload = correction["payload"]
        assert isinstance(payload, dict)
        target_id = str(payload["targetOutcomeEventId"])
        replacement = by_hash.get(str(payload["replacementEventSha256"]))
        target = by_id.get(target_id)
        if target is None or replacement is None:
            raise ValueError("correction target and replacement must both be present")
        replacement_id = str(replacement["outcomeEventId"])
        if target_id == replacement_id:
            raise ValueError("correction target and replacement must be distinct")
        if target["eventType"] != replacement["eventType"]:
            raise ValueError("correction target and replacement event types must match")
        if target["eventType"] == "correction":
            raise ValueError("correction chain or cycle is not allowed")
        if (
            target["packetId"] != correction["packetId"]
            or replacement["packetId"] != correction["packetId"]
        ):
            raise ValueError("correction target and replacement must share packetId")
        correction_at = parse_timestamp(correction["recordedAt"], "recordedAt")
        if correction_at <= parse_timestamp(
            target["recordedAt"], "recordedAt"
        ) or correction_at <= parse_timestamp(
            replacement["recordedAt"], "recordedAt"
        ):
            raise ValueError("correction recordedAt must be strictly later")
        prior = correction_edges.get(target_id)
        if prior is not None and prior != replacement_id:
            raise ValueError("conflicting corrections for one outcome event")
        correction_edges[target_id] = replacement_id
        replacement_ids.add(replacement_id)
    if set(correction_edges) & replacement_ids:
        raise ValueError("correction chain or cycle is not allowed")


def _validated_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    rows = read_jsonl(path)
    seen_ids: dict[str, str] = {}
    latest_by_packet: dict[str, object] = {}
    for row in rows:
        validate_event(row)
        event_id = str(row["outcomeEventId"])
        event_hash = str(row["eventSha256"])
        if event_id in seen_ids:
            raise ValueError("duplicate outcomeEventId in ledger")
        seen_ids[event_id] = event_hash
        packet_id = str(row["packetId"])
        recorded_at = parse_timestamp(row["recordedAt"], "recordedAt")
        prior = latest_by_packet.get(packet_id)
        if prior is not None and recorded_at < prior:
            raise ValueError("per-packet timestamp regression in ledger")
        latest_by_packet[packet_id] = recorded_at
    validate_event_sequence(rows)
    return rows


def load_events(path: Path) -> list[dict[str, object]]:
    """Load and validate a complete strict outcome ledger."""

    with _exclusive_path_lock(path):
        return _validated_rows(path)


def append_event(
    path: Path, event: dict[str, object]
) -> Literal["appended", "replayed"]:
    """Append one event, or report an exact idempotent replay."""

    validate_event(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _exclusive_path_lock(path):
        validated_prefix = path.read_bytes() if path.exists() else b""
        existing = _validated_rows(path)
        event_id = str(event["outcomeEventId"])
        event_hash = str(event["eventSha256"])

        for prior in existing:
            if prior["outcomeEventId"] != event_id:
                continue
            if prior["eventSha256"] == event_hash and prior == event:
                return "replayed"
            raise ValueError("outcomeEventId reused with different event bytes")

        recorded_at = parse_timestamp(event["recordedAt"], "recordedAt")
        for prior in reversed(existing):
            if prior["packetId"] == event["packetId"]:
                if recorded_at < parse_timestamp(prior["recordedAt"], "recordedAt"):
                    raise ValueError("per-packet timestamp regression")
                break

        validate_event_sequence(existing + [event])

        append_jsonl_exact_prefix(
            path,
            event,
            expected_prefix=validated_prefix,
        )
        return "appended"


__all__ = ["append_event", "load_events", "validate_event_sequence"]
