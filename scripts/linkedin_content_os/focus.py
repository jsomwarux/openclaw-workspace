"""Deterministic, hash-bound current-focus snapshots for LinkedIn Program 0."""

from __future__ import annotations

import re
from datetime import timedelta
from pathlib import Path
from typing import Optional

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp, validate_event


SCHEMA_VERSION = "linkedin-focus-snapshot.v1"
SOURCE_SCHEMA_VERSION = "linkedin-focus-sources.v1"
ALLOWED_KINDS = {"consulting", "career", "product"}
ALLOWED_STATUSES = {"proposed", "confirmed"}
ALLOWED_OWNER_PATHS = {
    "memory/content/current-efforts.md",
    "memory/north-star/active-this-week.md",
    "memory/north-star/revenue-command-center.md",
    "memory/pipeline.jsonl",
    "memory/job-state/job-market-daily-research.md",
}

_HASH = re.compile(r"^[0-9a-f]{64}$")
_SNAPSHOT_ID = re.compile(r"^sha256:([0-9a-f]{64})$")
_STABLE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SNAPSHOT_FIELDS = {
    "schemaVersion",
    "snapshotId",
    "generatedAt",
    "validUntil",
    "targets",
    "prohibitedPremises",
    "status",
}
_TARGET_FIELDS = {
    "targetId",
    "kind",
    "label",
    "desiredOutcome",
    "sourceRefs",
}
_SOURCE_FIELDS = {"path", "sha256"}


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError("{} must be a non-empty trimmed string".format(label))
    return value


def _require_exact_fields(value: dict[str, object], expected: set[str], label: str) -> None:
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing:
        raise ValueError("{} missing fields: {}".format(label, sorted(missing)))
    if unknown:
        raise ValueError("{} unknown fields: {}".format(label, sorted(unknown)))


def _owner_bytes(workspace_root: Path, relative_path: str) -> bytes:
    if relative_path not in ALLOWED_OWNER_PATHS:
        raise ValueError("source path is not allowlisted: {}".format(relative_path))
    root = workspace_root.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError("source path escapes workspace root") from error
    if not candidate.is_file():
        raise ValueError("owner source does not exist: {}".format(relative_path))
    return candidate.read_bytes()


def _validate_targets(
    targets_value: object, workspace_root: Path
) -> list[dict[str, object]]:
    if not isinstance(targets_value, list) or not targets_value:
        raise ValueError("focus snapshot requires at least one target")
    targets: list[dict[str, object]] = []
    seen: dict[str, bytes] = {}
    for index, raw_target in enumerate(targets_value):
        if not isinstance(raw_target, dict):
            raise ValueError("target {} must be an object".format(index))
        target: dict[str, object] = raw_target
        _require_exact_fields(target, _TARGET_FIELDS, "target")
        target_id = _require_text(target["targetId"], "targetId")
        if _STABLE_SLUG.fullmatch(target_id) is None:
            raise ValueError("targetId must be a stable lowercase slug")
        kind = _require_text(target["kind"], "kind")
        if kind not in ALLOWED_KINDS:
            raise ValueError("unsupported target kind {!r}".format(kind))
        _require_text(target["label"], "label")
        _require_text(target["desiredOutcome"], "desiredOutcome")
        source_refs = target["sourceRefs"]
        if not isinstance(source_refs, list) or not source_refs:
            raise ValueError("sourceRefs must be a non-empty list")
        seen_paths: set[str] = set()
        for raw_source in source_refs:
            if not isinstance(raw_source, dict):
                raise ValueError("sourceRef must be an object")
            source: dict[str, object] = raw_source
            _require_exact_fields(source, _SOURCE_FIELDS, "sourceRef")
            path = _require_text(source["path"], "sourceRef.path")
            if path in seen_paths:
                raise ValueError("duplicate source path in target")
            seen_paths.add(path)
            digest = _require_text(source["sha256"], "sourceRef.sha256")
            if _HASH.fullmatch(digest) is None:
                raise ValueError("source sha256 must be 64 lowercase hexadecimal characters")
            actual = sha256_hex(_owner_bytes(workspace_root, path))
            if actual != digest:
                raise ValueError("source hash mismatch for {}".format(path))

        target_bytes = canonical_bytes(target)
        prior = seen.get(target_id)
        if prior is not None:
            if prior != target_bytes:
                raise ValueError("conflicting owner facts for targetId {}".format(target_id))
            raise ValueError("duplicate targetId {}".format(target_id))
        seen[target_id] = target_bytes
        targets.append(target)
    return targets


def _snapshot_id(snapshot_without_id: dict[str, object], decision_hash: Optional[str] = None) -> str:
    preimage: object = snapshot_without_id
    if decision_hash is not None:
        preimage = {
            "focusSnapshot": snapshot_without_id,
            "focusDecisionEventSha256": decision_hash,
        }
    return "sha256:" + sha256_hex(canonical_bytes(preimage))


def _base_snapshot(
    workspace_root: Path,
    targets: object,
    generated_at: str,
    *,
    status: str,
    decision_hash: Optional[str] = None,
) -> dict[str, object]:
    generated = parse_timestamp(generated_at, "generatedAt")
    validated_targets = _validate_targets(targets, workspace_root)
    without_id: dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": generated_at,
        "validUntil": (generated + timedelta(days=30)).isoformat(),
        "targets": validated_targets,
        "prohibitedPremises": ["internal_machinery"],
        "status": status,
    }
    return {
        "schemaVersion": SCHEMA_VERSION,
        "snapshotId": _snapshot_id(without_id, decision_hash),
        "generatedAt": generated_at,
        "validUntil": without_id["validUntil"],
        "targets": validated_targets,
        "prohibitedPremises": ["internal_machinery"],
        "status": status,
    }


def build_focus_snapshot(
    workspace_root: Path,
    targets: object,
    *,
    generated_at: str,
    status: str = "proposed",
) -> dict[str, object]:
    """Build a pre-gate focus snapshot from exact allowlisted owner bytes."""

    if status != "proposed":
        raise ValueError("pre-gate focus snapshot is always proposed")
    return _base_snapshot(
        Path(workspace_root), targets, generated_at, status="proposed"
    )


def _validate_decision(event: object) -> dict[str, object]:
    validated = validate_event(event)
    if validated["eventType"] != "focus_decision":
        raise ValueError("confirmed focus requires a focus_decision event")
    return validated


def apply_focus_decision(
    proposed_snapshot: dict[str, object],
    focus_decision: dict[str, object],
    workspace_root: Path,
    *,
    corrected_targets: Optional[object] = None,
) -> dict[str, object]:
    """Derive a confirmed snapshot from one matching JT focus decision."""

    validate_focus_snapshot(proposed_snapshot, workspace_root)
    if proposed_snapshot["status"] != "proposed":
        raise ValueError("focus decision must bind a proposed snapshot")
    event = _validate_decision(focus_decision)
    payload: dict[str, object] = event["payload"]  # type: ignore[assignment]
    proposed_hash = str(proposed_snapshot["snapshotId"])[len("sha256:") :]
    if payload["focusSnapshotSha256"] != proposed_hash:
        raise ValueError("focus decision does not match proposed snapshot")

    targets: object = proposed_snapshot["targets"]
    if payload["decision"] == "confirmed":
        if corrected_targets is not None:
            raise ValueError("confirmed decision cannot carry corrected targets")
    else:
        if not isinstance(corrected_targets, list) or not corrected_targets:
            raise ValueError("corrected decision requires a complete replacement target list")
        replacement = build_focus_snapshot(
            workspace_root,
            corrected_targets,
            generated_at=str(proposed_snapshot["generatedAt"]),
        )
        declared = payload["replacementFocusSnapshotSha256"]
        actual = str(replacement["snapshotId"])[len("sha256:") :]
        if declared != actual:
            raise ValueError("focus decision replacement snapshot hash does not match")
        targets = corrected_targets

    return _base_snapshot(
        Path(workspace_root),
        targets,
        str(proposed_snapshot["generatedAt"]),
        status="confirmed",
        decision_hash=str(event["eventSha256"]),
    )


def validate_focus_snapshot(
    snapshot_value: object,
    workspace_root: Path,
    *,
    now: Optional[str] = None,
    focus_decision: Optional[dict[str, object]] = None,
) -> dict[str, object]:
    """Validate structure, owner hashes, freshness, and confirmation authority."""

    if not isinstance(snapshot_value, dict):
        raise ValueError("focus snapshot must be an object")
    snapshot: dict[str, object] = snapshot_value
    _require_exact_fields(snapshot, _SNAPSHOT_FIELDS, "focus snapshot")
    if snapshot["schemaVersion"] != SCHEMA_VERSION:
        raise ValueError("unsupported focus schemaVersion")
    status = snapshot["status"]
    if status not in ALLOWED_STATUSES:
        raise ValueError("unsupported focus status")
    generated = parse_timestamp(snapshot["generatedAt"], "generatedAt")
    valid_until = parse_timestamp(snapshot["validUntil"], "validUntil")
    if valid_until != generated + timedelta(days=30):
        raise ValueError("validUntil must be exactly 30 days after generatedAt")
    if snapshot["prohibitedPremises"] != ["internal_machinery"]:
        raise ValueError("prohibitedPremises must contain only internal_machinery")
    _validate_targets(snapshot["targets"], Path(workspace_root))
    if now is not None and parse_timestamp(now, "now") > valid_until:
        raise ValueError("focus snapshot is stale")

    decision_hash: Optional[str] = None
    if status == "confirmed":
        if focus_decision is None:
            raise ValueError("confirmed focus requires a matching focus_decision event")
        event = _validate_decision(focus_decision)
        event_payload: dict[str, object] = event["payload"]  # type: ignore[assignment]
        target_proposal = build_focus_snapshot(
            Path(workspace_root),
            snapshot["targets"],
            generated_at=str(snapshot["generatedAt"]),
        )
        target_hash = str(target_proposal["snapshotId"])[len("sha256:") :]
        if event_payload["decision"] == "confirmed":
            declared_target_hash = event_payload["focusSnapshotSha256"]
        else:
            declared_target_hash = event_payload["replacementFocusSnapshotSha256"]
        if declared_target_hash != target_hash:
            raise ValueError("focus decision target hash does not match snapshot targets")
        decision_hash = str(event["eventSha256"])
    without_id = {key: value for key, value in snapshot.items() if key != "snapshotId"}
    expected = _snapshot_id(without_id, decision_hash)
    provided = snapshot["snapshotId"]
    if not isinstance(provided, str) or _SNAPSHOT_ID.fullmatch(provided) is None:
        raise ValueError("snapshotId must be sha256:<64 lowercase hex>")
    if provided != expected:
        raise ValueError("snapshotId does not match canonical snapshot content")
    return snapshot


def renewal_need(snapshot: dict[str, object], now: str) -> Optional[dict[str, object]]:
    """Return one stable renewal need for a stale snapshot without rewriting it."""

    valid_until = parse_timestamp(snapshot.get("validUntil"), "validUntil")
    current = parse_timestamp(now, "now")
    if current <= valid_until:
        return None
    snapshot_id = snapshot.get("snapshotId")
    if not isinstance(snapshot_id, str) or _SNAPSHOT_ID.fullmatch(snapshot_id) is None:
        raise ValueError("snapshotId must be valid before projecting renewal")
    return {
        "schemaVersion": "linkedin-focus-renewal-need.v1",
        "needId": "linkedin-focus-renewal:v1",
        "focusSnapshotId": snapshot_id,
        "reason": "focus_snapshot_stale",
        "detectedAt": now,
    }


__all__ = [
    "ALLOWED_KINDS",
    "ALLOWED_OWNER_PATHS",
    "ALLOWED_STATUSES",
    "SCHEMA_VERSION",
    "apply_focus_decision",
    "build_focus_snapshot",
    "renewal_need",
    "validate_focus_snapshot",
]
