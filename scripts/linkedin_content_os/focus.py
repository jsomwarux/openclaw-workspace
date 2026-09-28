"""Deterministic, hash-bound current-focus snapshots for LinkedIn Program 0."""

from __future__ import annotations

import os
import re
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp, validate_event


SCHEMA_VERSION = "linkedin-focus-snapshot.v1"
SOURCE_SCHEMA_VERSION = "linkedin-focus-sources.v1"
AUTHORITY_RECEIPT_SCHEMA_VERSION = "linkedin-human-gate-authority-receipt.v1"
HUMAN_GATE_PACKET_ID = "linkedin-program-0-human-gate"
HUMAN_GATE_SOURCE_TYPE = "jt_human_gate_response"
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
_SNAPSHOT_BASE_FIELDS = {
    "schemaVersion", "snapshotId", "generatedAt", "validUntil", "targets",
    "prohibitedPremises", "status",
}
_TARGET_FIELDS = {"targetId", "kind", "label", "desiredOutcome", "sourceRefs"}
_SOURCE_FIELDS = {"path", "sha256"}
_BINDING_REQUIRED_FIELDS = {
    "originalProposalSha256", "authorityReceiptSha256", "focusDecisionEventSha256",
}
_RECEIPT_REQUIRED_FIELDS = {
    "schemaVersion", "rawResponseSha256", "recoveryRequestSha256",
    "fixtureGapSha256", "focusDecisionEventSha256", "ledgerPrefixSha256",
    "ledgerPosition", "validatedAt", "originalProposalSha256",
    "focusDecision", "receiptSha256",
}


def _utc_now() -> datetime:
    """Private clock seam; production always resolves current UTC here."""
    return datetime.now(timezone.utc)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError("{} must be a non-empty trimmed string".format(label))
    return value


def _require_hash(value: object, label: str) -> str:
    text = _require_text(value, label)
    if _HASH.fullmatch(text) is None:
        raise ValueError("{} must be 64 lowercase hexadecimal characters".format(label))
    return text


def _require_exact_fields(value: object, expected: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("{} must be an object".format(label))
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing:
        raise ValueError("{} missing fields: {}".format(label, sorted(missing)))
    if unknown:
        raise ValueError("{} unknown fields: {}".format(label, sorted(unknown)))
    return value


def _reject_nulls(value: object, label: str) -> None:
    if value is None:
        raise ValueError("{} must not be null".format(label))
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_nulls(item, "{}.{}".format(label, key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nulls(item, "{}[{}]".format(label, index))


def _stat_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns,
    )


def _owner_bytes(workspace_root: Path, relative_path: str) -> bytes:
    """Read one allowlisted regular file without following links or path swaps."""
    if relative_path not in ALLOWED_OWNER_PATHS:
        raise ValueError("source path is not allowlisted: {}".format(relative_path))
    root = Path(workspace_root).absolute()
    try:
        root_lstat = root.lstat()
    except OSError as error:
        raise ValueError("workspace root is unavailable") from error
    if stat.S_ISLNK(root_lstat.st_mode):
        raise ValueError("workspace root must not be a symlink")
    if not stat.S_ISDIR(root_lstat.st_mode):
        raise ValueError("workspace root must be a directory")
    parts = Path(relative_path).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise ValueError("source path must be a safe workspace-relative path")
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    directory_flag = getattr(os, "O_DIRECTORY", 0)
    descriptors: list[int] = []
    opened_components: list[tuple[int, str, int, tuple[int, int, int, int, int, int]]] = []
    try:
        current_fd = os.open(str(root), os.O_RDONLY | directory_flag | nofollow)
        descriptors.append(current_fd)
        root_identity = _stat_identity(os.fstat(current_fd))
        if root_identity != _stat_identity(root_lstat):
            raise ValueError("workspace root changed during read")
        for component in parts[:-1]:
            before = os.stat(component, dir_fd=current_fd, follow_symlinks=False)
            if stat.S_ISLNK(before.st_mode):
                raise ValueError("source path component must not be a symlink")
            if not stat.S_ISDIR(before.st_mode):
                raise ValueError("source path component must be a directory")
            child_fd = os.open(
                component, os.O_RDONLY | directory_flag | nofollow, dir_fd=current_fd
            )
            opened = os.fstat(child_fd)
            if _stat_identity(before) != _stat_identity(opened):
                os.close(child_fd)
                raise ValueError("source path changed during read")
            opened_components.append(
                (current_fd, component, child_fd, _stat_identity(opened))
            )
            descriptors.append(child_fd)
            current_fd = child_fd
        filename = parts[-1]
        try:
            before_file = os.stat(filename, dir_fd=current_fd, follow_symlinks=False)
        except FileNotFoundError as error:
            raise ValueError("owner source does not exist: {}".format(relative_path)) from error
        if stat.S_ISLNK(before_file.st_mode):
            raise ValueError("owner source must not be a symlink")
        if not stat.S_ISREG(before_file.st_mode):
            raise ValueError("owner source must be a regular file")
        file_fd = os.open(filename, os.O_RDONLY | nofollow, dir_fd=current_fd)
        descriptors.append(file_fd)
        opened_file = os.fstat(file_fd)
        if _stat_identity(before_file) != _stat_identity(opened_file):
            raise ValueError("owner source changed during read")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(file_fd, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        after_fd = os.fstat(file_fd)
        after_path = os.stat(filename, dir_fd=current_fd, follow_symlinks=False)
        if (_stat_identity(opened_file) != _stat_identity(after_fd)
                or _stat_identity(opened_file) != _stat_identity(after_path)):
            raise ValueError("owner source changed during read")
        if _stat_identity(os.stat(str(root), follow_symlinks=False)) != root_identity:
            raise ValueError("workspace root changed during read")
        for parent_fd, component, child_fd, identity in opened_components:
            if (_stat_identity(os.fstat(child_fd)) != identity
                    or _stat_identity(os.stat(
                        component, dir_fd=parent_fd, follow_symlinks=False
                    )) != identity):
                raise ValueError("source path changed during read")
        return b"".join(chunks)
    except OSError as error:
        raise ValueError("owner source could not be read safely") from error
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _validate_targets(targets_value: object, workspace_root: Path) -> list[dict[str, object]]:
    if not isinstance(targets_value, list) or not targets_value:
        raise ValueError("focus snapshot requires at least one target")
    targets: list[dict[str, object]] = []
    seen: dict[str, bytes] = {}
    for index, raw_target in enumerate(targets_value):
        target = _require_exact_fields(raw_target, _TARGET_FIELDS, "target {}".format(index))
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
            source = _require_exact_fields(raw_source, _SOURCE_FIELDS, "sourceRef")
            path = _require_text(source["path"], "sourceRef.path")
            if path in seen_paths:
                raise ValueError("duplicate source path in target")
            seen_paths.add(path)
            digest = _require_hash(source["sha256"], "sourceRef.sha256")
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


def _snapshot_id(snapshot_without_id: dict[str, object]) -> str:
    return "sha256:" + sha256_hex(canonical_bytes(snapshot_without_id))


def _base_snapshot(
    workspace_root: Path, targets: object, generated_at: str, *, status: str,
    decision_binding: Optional[dict[str, object]] = None,
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
    if decision_binding is not None:
        without_id["decisionBinding"] = decision_binding
    return {
        "schemaVersion": SCHEMA_VERSION,
        "snapshotId": _snapshot_id(without_id),
        "generatedAt": generated_at,
        "validUntil": without_id["validUntil"],
        "targets": validated_targets,
        "prohibitedPremises": ["internal_machinery"],
        "status": status,
        **({"decisionBinding": decision_binding} if decision_binding is not None else {}),
    }


def build_focus_snapshot(
    workspace_root: Path, targets: object, *, generated_at: str,
    status: str = "proposed",
) -> dict[str, object]:
    """Build a pre-gate focus snapshot from exact allowlisted owner bytes."""
    if status != "proposed":
        raise ValueError("pre-gate focus snapshot is always proposed")
    snapshot = _base_snapshot(Path(workspace_root), targets, generated_at, status="proposed")
    _validate_focus_snapshot(snapshot, Path(workspace_root), allow_stale=False)
    return snapshot


def _validate_authority(
    event_value: object, receipt_value: object, expected_receipt_sha256: object,
    proposed_hash: str,
    workspace_root: Path, generated_at: str, valid_until: str,
) -> tuple[dict[str, object], str, object, Optional[str]]:
    """Verify Task 7B's receipt against an independently supplied trust anchor.

    The expected digest is established by recovery ingestion.  It must not be
    computed from the event or receipt at this boundary.
    """
    if not isinstance(receipt_value, dict):
        raise ValueError("authority receipt must be an object")
    expected_anchor = _require_hash(
        expected_receipt_sha256, "expected authority receipt digest"
    )
    expected_fields = set(_RECEIPT_REQUIRED_FIELDS)
    if "replacementProposalSha256" in receipt_value:
        expected_fields.add("replacementProposalSha256")
    receipt = _require_exact_fields(receipt_value, expected_fields, "authority receipt")
    _reject_nulls(receipt, "authority receipt")
    if receipt["schemaVersion"] != AUTHORITY_RECEIPT_SCHEMA_VERSION:
        raise ValueError("unsupported authority receipt schemaVersion")
    for field in (
        "rawResponseSha256", "recoveryRequestSha256", "fixtureGapSha256",
        "focusDecisionEventSha256", "ledgerPrefixSha256",
        "originalProposalSha256", "receiptSha256",
    ):
        _require_hash(receipt[field], field)
    if "replacementProposalSha256" in receipt:
        _require_hash(receipt["replacementProposalSha256"], "replacementProposalSha256")
    position = receipt["ledgerPosition"]
    if isinstance(position, bool) or not isinstance(position, int) or position < 1:
        raise ValueError("ledgerPosition must be a positive integer")
    validated_at = parse_timestamp(receipt["validatedAt"], "validatedAt")
    receipt_without_hash = {
        key: value for key, value in receipt.items() if key != "receiptSha256"
    }
    computed_receipt_hash = sha256_hex(canonical_bytes(receipt_without_hash))
    if receipt["receiptSha256"] != computed_receipt_hash:
        raise ValueError("authority receipt receiptSha256 mismatch")
    if computed_receipt_hash != expected_anchor:
        raise ValueError("expected authority receipt digest mismatch")
    if receipt["originalProposalSha256"] != proposed_hash:
        raise ValueError("authority receipt does not bind the original proposal")

    event = validate_event(event_value)
    if event["eventType"] != "focus_decision":
        raise ValueError("confirmed focus requires a focus_decision event")
    if event["packetId"] != HUMAN_GATE_PACKET_ID:
        raise ValueError("focus decision packetId is not the human-gate packet")
    source: dict[str, object] = event["sourcePointer"]  # type: ignore[assignment]
    if source["sourceType"] != HUMAN_GATE_SOURCE_TYPE:
        raise ValueError("focus decision sourceType is not JT human-gate authority")
    raw_response_hash = receipt["rawResponseSha256"]
    if (source["sourceSha256"] != raw_response_hash
            or source["sourceId"] != "sha256:" + str(raw_response_hash)):
        raise ValueError("focus decision source does not match authority receipt")
    if event["eventSha256"] != receipt["focusDecisionEventSha256"]:
        raise ValueError("focus decision event does not match authority receipt")
    recorded = parse_timestamp(event["recordedAt"], "recordedAt")
    generated = parse_timestamp(generated_at, "generatedAt")
    expires = parse_timestamp(valid_until, "validUntil")
    current = _utc_now()
    if recorded < generated or recorded > expires:
        raise ValueError("focus decision recordedAt is outside the proposal validity window")
    if recorded > current:
        raise ValueError("focus decision recordedAt is in the future")
    if validated_at < recorded or validated_at > expires or validated_at > current:
        raise ValueError("authority receipt validatedAt is outside the trusted time window")
    decision_value = receipt["focusDecision"]
    if not isinstance(decision_value, dict):
        raise ValueError("focusDecision must be an object")
    decision: dict[str, object] = decision_value
    targets: object = None
    replacement_hash: Optional[str] = None
    expected_payload: dict[str, object] = {
        "decision": decision["decision"], "focusSnapshotSha256": proposed_hash,
    }
    if decision.get("decision") == "confirmed":
        _require_exact_fields(decision, {"decision"}, "focusDecision")
        if "replacementProposalSha256" in receipt:
            raise ValueError("confirmed authority receipt cannot include replacement hash")
    elif decision.get("decision") == "corrected":
        _require_exact_fields(decision, {"decision", "correctedTargets"}, "focusDecision")
        if not isinstance(decision.get("correctedTargets"), list) or not decision["correctedTargets"]:
            raise ValueError("corrected decision requires a complete replacement target list")
        targets = decision["correctedTargets"]
        replacement = _base_snapshot(
            workspace_root, targets, generated_at, status="proposed"
        )
        replacement_hash = str(replacement["snapshotId"])[len("sha256:"):]
        if receipt.get("replacementProposalSha256") != replacement_hash:
            raise ValueError("authority receipt replacement hash mismatch")
        expected_payload["replacementFocusSnapshotSha256"] = replacement_hash
    else:
        raise ValueError("unsupported focusDecision")
    if event["payload"] != expected_payload:
        raise ValueError("focus decision payload does not equal authority receipt decision")
    return event, computed_receipt_hash, targets, replacement_hash


def apply_focus_decision(
    proposed_snapshot: dict[str, object], focus_decision: dict[str, object],
    workspace_root: Path, *, authority_receipt: object,
    expected_authority_receipt_sha256: object,
) -> dict[str, object]:
    """Derive confirmed focus only from Task 7B's independently anchored receipt."""
    proposed = _validate_focus_snapshot(proposed_snapshot, Path(workspace_root), allow_stale=False)
    if proposed["status"] != "proposed":
        raise ValueError("focus decision must bind a proposed snapshot")
    proposed_hash = str(proposed["snapshotId"])[len("sha256:"):]
    event, receipt_hash, corrected_targets, replacement_hash = _validate_authority(
        focus_decision, authority_receipt, expected_authority_receipt_sha256,
        proposed_hash, Path(workspace_root),
        str(proposed["generatedAt"]), str(proposed["validUntil"]),
    )
    targets = proposed["targets"] if corrected_targets is None else corrected_targets
    binding: dict[str, object] = {
        "originalProposalSha256": proposed_hash,
        "authorityReceiptSha256": receipt_hash,
        "focusDecisionEventSha256": event["eventSha256"],
    }
    if replacement_hash is not None:
        binding["replacementProposalSha256"] = replacement_hash
    return _base_snapshot(
        Path(workspace_root), targets, str(proposed["generatedAt"]),
        status="confirmed", decision_binding=binding,
    )


def _validate_binding(binding_value: object) -> dict[str, object]:
    if not isinstance(binding_value, dict):
        raise ValueError("decisionBinding must be an object")
    expected = set(_BINDING_REQUIRED_FIELDS)
    if "replacementProposalSha256" in binding_value:
        expected.add("replacementProposalSha256")
    binding = _require_exact_fields(binding_value, expected, "decisionBinding")
    for field in expected:
        _require_hash(binding[field], "decisionBinding.{}".format(field))
    return binding


def _validate_focus_snapshot(
    snapshot_value: object, workspace_root: Path, *, allow_stale: bool,
    focus_decision: Optional[dict[str, object]] = None,
    authority_receipt: object = None,
    expected_authority_receipt_sha256: object = None,
    original_proposed_snapshot: object = None,
) -> dict[str, object]:
    if not isinstance(snapshot_value, dict):
        raise ValueError("focus snapshot must be an object")
    snapshot: dict[str, object] = snapshot_value
    status = snapshot.get("status")
    if not isinstance(status, str) or status not in ALLOWED_STATUSES:
        raise ValueError("unsupported focus status")
    expected_fields = set(_SNAPSHOT_BASE_FIELDS)
    if status == "confirmed":
        expected_fields.add("decisionBinding")
    _require_exact_fields(snapshot, expected_fields, "focus snapshot")
    if snapshot["schemaVersion"] != SCHEMA_VERSION:
        raise ValueError("unsupported focus schemaVersion")
    generated = parse_timestamp(snapshot["generatedAt"], "generatedAt")
    valid_until = parse_timestamp(snapshot["validUntil"], "validUntil")
    if valid_until != generated + timedelta(days=30):
        raise ValueError("validUntil must be exactly 30 days after generatedAt")
    if snapshot["prohibitedPremises"] != ["internal_machinery"]:
        raise ValueError("prohibitedPremises must contain only internal_machinery")
    _validate_targets(snapshot["targets"], Path(workspace_root))
    current = _utc_now()
    if generated > current:
        raise ValueError("focus snapshot generatedAt is in the future")
    if not allow_stale and current > valid_until:
        raise ValueError("focus snapshot is stale")
    if status == "confirmed":
        if (focus_decision is None or authority_receipt is None
                or expected_authority_receipt_sha256 is None
                or original_proposed_snapshot is None):
            raise ValueError("confirmed focus requires immutable decision authority")
        binding = _validate_binding(snapshot["decisionBinding"])
        original = _validate_focus_snapshot(
            original_proposed_snapshot, Path(workspace_root), allow_stale=allow_stale
        )
        if original["status"] != "proposed":
            raise ValueError("original proposed snapshot artifact must be proposed")
        original_hash = str(original["snapshotId"])[len("sha256:"):]
        if binding["originalProposalSha256"] != original_hash:
            raise ValueError("decisionBinding does not match original proposed snapshot")
        event, receipt_hash, corrected_targets, replacement_hash = _validate_authority(
            focus_decision, authority_receipt, expected_authority_receipt_sha256,
            original_hash, Path(workspace_root),
            str(snapshot["generatedAt"]), str(snapshot["validUntil"]),
        )
        if binding["authorityReceiptSha256"] != receipt_hash:
            raise ValueError("decisionBinding authority receipt hash mismatch")
        if binding["focusDecisionEventSha256"] != event["eventSha256"]:
            raise ValueError("decisionBinding event hash mismatch")
        corrected = corrected_targets is not None
        if corrected:
            if "replacementProposalSha256" not in binding:
                raise ValueError("corrected decisionBinding is missing replacement hash")
            if binding["replacementProposalSha256"] != replacement_hash:
                raise ValueError("decisionBinding replacement hash mismatch")
            if canonical_bytes(snapshot["targets"]) != canonical_bytes(corrected_targets):
                raise ValueError("confirmed snapshot does not equal corrected targets")
        else:
            if "replacementProposalSha256" in binding:
                raise ValueError("confirmed decisionBinding cannot include replacement hash")
            if canonical_bytes(snapshot["targets"]) != canonical_bytes(original["targets"]):
                raise ValueError("confirmed snapshot does not equal original proposed targets")
    without_id = {key: value for key, value in snapshot.items() if key != "snapshotId"}
    expected_id = _snapshot_id(without_id)
    provided = snapshot["snapshotId"]
    if not isinstance(provided, str) or _SNAPSHOT_ID.fullmatch(provided) is None:
        raise ValueError("snapshotId must be sha256:<64 lowercase hex>")
    if provided != expected_id:
        raise ValueError("snapshotId does not match canonical snapshot content")
    return snapshot


def validate_focus_snapshot(
    snapshot_value: object, workspace_root: Path, *,
    focus_decision: Optional[dict[str, object]] = None,
    authority_receipt: object = None,
    expected_authority_receipt_sha256: object = None,
    original_proposed_snapshot: object = None,
) -> dict[str, object]:
    """Validate owner hashes, current freshness, and immutable JT authority."""
    return _validate_focus_snapshot(
        snapshot_value, Path(workspace_root), allow_stale=False,
        focus_decision=focus_decision, authority_receipt=authority_receipt,
        expected_authority_receipt_sha256=expected_authority_receipt_sha256,
        original_proposed_snapshot=original_proposed_snapshot,
    )


def renewal_need(
    snapshot: dict[str, object], workspace_root: Path, *,
    focus_decision: Optional[dict[str, object]] = None,
    authority_receipt: object = None,
    expected_authority_receipt_sha256: object = None,
    original_proposed_snapshot: object = None,
) -> Optional[dict[str, object]]:
    """Validate fully, then return one stable renewal need for a stale snapshot."""
    validated = _validate_focus_snapshot(
        snapshot, Path(workspace_root), allow_stale=True,
        focus_decision=focus_decision, authority_receipt=authority_receipt,
        expected_authority_receipt_sha256=expected_authority_receipt_sha256,
        original_proposed_snapshot=original_proposed_snapshot,
    )
    current = _utc_now()
    valid_until = parse_timestamp(validated["validUntil"], "validUntil")
    if current <= valid_until:
        return None
    return {
        "schemaVersion": "linkedin-focus-renewal-need.v1",
        "needId": "linkedin-focus-renewal:v1",
        "focusSnapshotId": validated["snapshotId"],
        "reason": "focus_snapshot_stale",
        "detectedAt": current.isoformat(),
    }


__all__ = [
    "ALLOWED_KINDS", "ALLOWED_OWNER_PATHS", "ALLOWED_STATUSES",
    "AUTHORITY_RECEIPT_SCHEMA_VERSION", "HUMAN_GATE_PACKET_ID",
    "HUMAN_GATE_SOURCE_TYPE", "SCHEMA_VERSION", "apply_focus_decision",
    "build_focus_snapshot", "renewal_need", "validate_focus_snapshot",
]
