"""Closed proof receipts and stable external-boundary snapshots for Program 0."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import Dict, List, Optional, Sequence

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp


RECEIPT_SCHEMA_VERSION = "linkedin-authority-consumption-receipt.v1"
BOUNDARY_SCHEMA_VERSION = "linkedin-program-0-boundary.v1"
_HASH = re.compile(r"^[0-9a-f]{64}$")
_RUN_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_SECRET_KEY = re.compile(
    r"(?i)(?:authorization|bearer|credential|password|private[_-]?key|secret|token)"
)
_SECRET_VALUE = re.compile(r"(?i)(?:\bBearer\s+\S+|\bsk-[A-Za-z0-9_-]{8,})")
_RECEIPT_FIELDS = {
    "schemaVersion",
    "command",
    "runContextSha256",
    "expectedManifestSha256",
    "canonicalManifestSha256",
    "inputs",
    "outputs",
    "generatedAt",
    "receiptSha256",
}
_BINDING_FIELDS = {"role", "path", "sha256"}
BOUNDARY_PHASES = frozenset({
    "phase-1-before",
    "phase-1-after",
    "phase-2-before",
    "phase-2-after",
    "supplement-before",
    "supplement-after",
})
_ROLE_SETS = {
    "build-corpus": (
        {"audit", "outcomes", "run_context"},
        {"contrastive_pairs", "voice_gold"},
    ),
    "audit-history": (
        {"authority_manifest", "outcomes", "posted_log", "run_context"},
        {"historical_audit", "recovery_request"},
    ),
}


def _require_hash(value: object, label: str) -> str:
    if not isinstance(value, str) or _HASH.fullmatch(value) is None:
        raise ValueError("{} must be a lowercase SHA-256".format(label))
    return value


def _safe_relative_path(value: object) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("receipt binding path must be workspace-relative")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError("receipt binding path must be canonical workspace-relative")
    if pure.as_posix() != value:
        raise ValueError("receipt binding path must be canonical workspace-relative")
    return value


def _validate_bindings(
    value: object, *, label: str, expected_roles: set[str]
) -> List[Dict[str, object]]:
    if not isinstance(value, list):
        raise ValueError("{} must be a list".format(label))
    result: List[Dict[str, object]] = []
    prior: Optional[tuple[str, str]] = None
    roles: set[str] = set()
    paths: set[str] = set()
    for raw in value:
        if not isinstance(raw, dict) or set(raw) != _BINDING_FIELDS:
            raise ValueError("{} binding fields are not closed".format(label))
        role = raw.get("role")
        if not isinstance(role, str) or role not in expected_roles:
            raise ValueError("{} binding role is not allowed".format(label))
        path = _safe_relative_path(raw.get("path"))
        digest = _require_hash(raw.get("sha256"), "{}.sha256".format(label))
        key = (role, path)
        if prior is not None and key <= prior:
            raise ValueError("{} bindings must be sorted and duplicate-free".format(label))
        if role in roles or path in paths:
            raise ValueError("{} bindings must have unique roles and paths".format(label))
        prior = key
        roles.add(role)
        paths.add(path)
        result.append({"role": role, "path": path, "sha256": digest})
    if roles != expected_roles:
        raise ValueError("{} binding roles do not match the closed contract".format(label))
    return result


def validate_authority_consumption_receipt(
    value: object, *, workspace_root: Optional[Path] = None
) -> Dict[str, object]:
    """Validate a closed receipt and optionally rehash every bound byte."""

    if not isinstance(value, dict) or set(value) != _RECEIPT_FIELDS:
        raise ValueError("authority consumption receipt fields are not closed")
    receipt: Dict[str, object] = value
    if receipt.get("schemaVersion") != RECEIPT_SCHEMA_VERSION:
        raise ValueError("unsupported authority consumption receipt schema")
    command = receipt.get("command")
    if command not in _ROLE_SETS:
        raise ValueError("authority consumption receipt command is not allowed")
    input_roles, output_roles = _ROLE_SETS[str(command)]
    inputs = _validate_bindings(
        receipt.get("inputs"), label="inputs", expected_roles=input_roles
    )
    outputs = _validate_bindings(
        receipt.get("outputs"), label="outputs", expected_roles=output_roles
    )
    run_context_sha256 = _require_hash(
        receipt.get("runContextSha256"), "runContextSha256"
    )
    run_binding = next(item for item in inputs if item["role"] == "run_context")
    if run_binding["sha256"] != run_context_sha256:
        raise ValueError("runContextSha256 does not match the run_context binding")
    expected = receipt.get("expectedManifestSha256")
    if command == "audit-history" and expected is None:
        raise ValueError("phase-2 audit receipt requires expected manifest digest")
    if expected is not None:
        expected = _require_hash(expected, "expectedManifestSha256")
    canonical_manifest = _require_hash(
        receipt.get("canonicalManifestSha256"), "canonicalManifestSha256"
    )
    if expected is not None and expected != canonical_manifest:
        raise ValueError("expected and canonical manifest digests differ")
    generated_at = receipt.get("generatedAt")
    parse_timestamp(generated_at, "generatedAt")
    provided = _require_hash(receipt.get("receiptSha256"), "receiptSha256")
    unsigned = {key: item for key, item in receipt.items() if key != "receiptSha256"}
    if provided != sha256_hex(canonical_bytes(unsigned)):
        raise ValueError("authority consumption receipt hash mismatch")
    if workspace_root is not None:
        root = Path(workspace_root).resolve()
        for binding in inputs + outputs:
            unresolved = root / str(binding["path"])
            try:
                path = unresolved.resolve(strict=True)
                path.relative_to(root)
            except (OSError, ValueError) as error:
                raise ValueError("bound receipt path escapes workspace or is unavailable") from error
            try:
                payload = path.read_bytes()
            except OSError as error:
                raise ValueError("bound receipt path is unavailable") from error
            if sha256_hex(payload) != binding["sha256"]:
                raise ValueError("bound receipt byte hash mismatch")
        run_path = (root / str(run_binding["path"])).resolve(strict=True)
        try:
            run_value = __import__("json").loads(run_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as error:
            raise ValueError("bound run context is not valid JSON") from error
        if not isinstance(run_value, dict) or run_value.get("generatedAt") != generated_at:
            raise ValueError("receipt generatedAt does not match bound run context")
    return receipt


def build_authority_consumption_receipt(
    *,
    command: str,
    run_context_sha256: str,
    expected_manifest_sha256: Optional[str],
    canonical_manifest_sha256: str,
    inputs: Sequence[Dict[str, object]],
    outputs: Sequence[Dict[str, object]],
    generated_at: str,
) -> Dict[str, object]:
    """Create one canonical receipt for an authority-consuming command."""

    unsigned: Dict[str, object] = {
        "schemaVersion": RECEIPT_SCHEMA_VERSION,
        "command": command,
        "runContextSha256": run_context_sha256,
        "expectedManifestSha256": expected_manifest_sha256,
        "canonicalManifestSha256": canonical_manifest_sha256,
        "inputs": list(inputs),
        "outputs": list(outputs),
        "generatedAt": generated_at,
    }
    receipt = {**unsigned, "receiptSha256": sha256_hex(canonical_bytes(unsigned))}
    return validate_authority_consumption_receipt(receipt)


def _reject_secret_material(value: object, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("cron definitions require string keys")
            if _SECRET_KEY.search(key):
                raise ValueError("secret-bearing cron key at {}".format(path))
            _reject_secret_material(item, "{}.{}".format(path, key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_secret_material(item, "{}[{}]".format(path, index))
    elif isinstance(value, str) and _SECRET_VALUE.search(value):
        raise ValueError("secret-bearing cron value at {}".format(path))


def normalize_cron_definitions(value: object) -> Dict[str, object]:
    """Project OpenClaw cron output to stable, non-runtime configuration only."""

    _reject_secret_material(value)
    if not isinstance(value, dict) or not isinstance(value.get("jobs"), list):
        raise ValueError("cron list must contain a jobs array")
    jobs: List[Dict[str, object]] = []
    seen: set[str] = set()
    for raw in value["jobs"]:
        if not isinstance(raw, dict):
            raise ValueError("cron job must be an object")
        job_id = raw.get("id")
        name = raw.get("name")
        enabled = raw.get("enabled")
        if (
            not isinstance(job_id, str)
            or not job_id
            or job_id in seen
            or not isinstance(name, str)
            or not name
            or not isinstance(enabled, bool)
        ):
            raise ValueError("cron job identity is invalid")
        seen.add(job_id)
        payload = raw.get("payload", {})
        delivery = raw.get("delivery", {})
        if not isinstance(delivery, dict):
            raise ValueError("cron delivery must be an object")
        target = delivery.get("to", delivery.get("target"))
        if target is not None and not isinstance(target, str):
            raise ValueError("cron delivery target must be text")
        target_digest = (
            sha256_hex(target.encode("utf-8")) if isinstance(target, str) else None
        )
        jobs.append(
            {
                "id": job_id,
                "name": name,
                "enabled": enabled,
                "schedule": raw.get("schedule"),
                "sessionTarget": raw.get("sessionTarget"),
                "wakeMode": raw.get("wakeMode"),
                "payloadSha256": sha256_hex(canonical_bytes(payload)),
                "deliveryMode": delivery.get("mode"),
                "deliveryTargetSha256": target_digest,
            }
        )
    jobs.sort(key=lambda item: str(item["id"]))
    return {"jobs": jobs}


def build_boundary_artifact(
    *,
    phase: str,
    generated_at: str,
    run_id: str,
    snapshot: Dict[str, object],
    normalized_cron: Dict[str, object],
    launchagents: Sequence[Dict[str, object]],
    protected_inputs: Dict[str, str],
    primary_checkout_fingerprint: str,
) -> Dict[str, object]:
    """Build one deterministic boundary artifact from already captured inputs."""

    if phase not in BOUNDARY_PHASES:
        raise ValueError("unsupported boundary phase")
    parse_timestamp(generated_at, "generatedAt")
    if not isinstance(run_id, str) or _RUN_ID.fullmatch(run_id) is None:
        raise ValueError("runId is invalid")
    _require_hash(primary_checkout_fingerprint, "primaryCheckoutFingerprint")
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot must be an object")
    packets = snapshot.get("packets")
    if not isinstance(packets, list):
        raise ValueError("snapshot packets must be a list")
    task_ids = sorted(
        str(packet["taskId"])
        for packet in packets
        if isinstance(packet, dict) and isinstance(packet.get("taskId"), str)
    )
    if len(task_ids) != len(packets) or len(set(task_ids)) != len(task_ids):
        raise ValueError("snapshot packet task IDs are invalid")
    lane_rows_sha256 = sha256_hex(canonical_bytes(packets))
    launchagent_rows = list(launchagents)
    if launchagent_rows != sorted(launchagent_rows, key=lambda item: str(item.get("path"))):
        raise ValueError("LaunchAgent inventory must be sorted")
    for item in launchagent_rows:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ValueError("LaunchAgent inventory fields are not closed")
        _safe_relative_path(item["path"])
        _require_hash(item["sha256"], "LaunchAgent sha256")
    protected = []
    for path, digest in sorted(protected_inputs.items()):
        protected.append(
            {"path": _safe_relative_path(path), "sha256": _require_hash(digest, path)}
        )
    unsigned: Dict[str, object] = {
        "schemaVersion": BOUNDARY_SCHEMA_VERSION,
        "phase": phase,
        "generatedAt": generated_at,
        "runId": run_id,
        "missionControl": {
            "taskCount": snapshot.get("totalTaskCount"),
            "linkedinLanePacketCount": snapshot.get("linkedinLanePacketCount"),
            "taskIds": task_ids,
            "laneRowsSha256": lane_rows_sha256,
            "projectionSha256": snapshot.get("projectionSha256"),
        },
        "cronDefinitionSha256": sha256_hex(canonical_bytes(normalized_cron)),
        "launchAgents": launchagent_rows,
        "protectedInputs": protected,
        "primaryCheckoutFingerprint": primary_checkout_fingerprint,
    }
    return {**unsigned, "boundarySha256": sha256_hex(canonical_bytes(unsigned))}


def validate_boundary_artifact(value: object) -> Dict[str, object]:
    """Validate the canonical boundary digest and its closed top-level contract."""

    expected_fields = {
        "schemaVersion",
        "phase",
        "generatedAt",
        "runId",
        "missionControl",
        "cronDefinitionSha256",
        "launchAgents",
        "protectedInputs",
        "primaryCheckoutFingerprint",
        "boundarySha256",
    }
    if not isinstance(value, dict) or set(value) != expected_fields:
        raise ValueError("boundary artifact fields are not closed")
    artifact: Dict[str, object] = value
    if artifact["schemaVersion"] != BOUNDARY_SCHEMA_VERSION:
        raise ValueError("unsupported boundary artifact schema")
    if artifact["phase"] not in BOUNDARY_PHASES:
        raise ValueError("unsupported boundary phase")
    parse_timestamp(artifact["generatedAt"], "generatedAt")
    if not isinstance(artifact["runId"], str) or _RUN_ID.fullmatch(artifact["runId"]) is None:
        raise ValueError("boundary runId is invalid")
    for field in (
        "cronDefinitionSha256", "primaryCheckoutFingerprint", "boundarySha256"
    ):
        _require_hash(artifact[field], field)
    mission_control = artifact["missionControl"]
    if not isinstance(mission_control, dict) or set(mission_control) != {
        "taskCount",
        "linkedinLanePacketCount",
        "taskIds",
        "laneRowsSha256",
        "projectionSha256",
    }:
        raise ValueError("boundary Mission Control projection is not closed")
    _require_hash(mission_control["laneRowsSha256"], "laneRowsSha256")
    _require_hash(mission_control["projectionSha256"], "projectionSha256")
    task_ids = mission_control["taskIds"]
    if not isinstance(task_ids, list) or task_ids != sorted(set(task_ids)):
        raise ValueError("boundary task IDs must be sorted and unique")
    for field in ("taskCount", "linkedinLanePacketCount"):
        count = mission_control[field]
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("boundary Mission Control counts are invalid")
    if mission_control["linkedinLanePacketCount"] != len(task_ids):
        raise ValueError("boundary LinkedIn packet count does not match task IDs")
    if mission_control["taskCount"] < len(task_ids):
        raise ValueError("boundary task count is smaller than packet count")
    for label in ("launchAgents", "protectedInputs"):
        bindings = artifact[label]
        if not isinstance(bindings, list):
            raise ValueError("{} must be a list".format(label))
        prior: Optional[str] = None
        for item in bindings:
            if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
                raise ValueError("{} binding fields are not closed".format(label))
            path = _safe_relative_path(item["path"])
            _require_hash(item["sha256"], "{}.sha256".format(label))
            if prior is not None and path <= prior:
                raise ValueError("{} must be sorted and duplicate-free".format(label))
            prior = path
    provided = str(artifact["boundarySha256"])
    unsigned = {key: item for key, item in artifact.items() if key != "boundarySha256"}
    if provided != sha256_hex(canonical_bytes(unsigned)):
        raise ValueError("boundary artifact hash mismatch")
    return artifact


__all__ = [
    "BOUNDARY_PHASES",
    "BOUNDARY_SCHEMA_VERSION",
    "RECEIPT_SCHEMA_VERSION",
    "build_authority_consumption_receipt",
    "build_boundary_artifact",
    "normalize_cron_definitions",
    "validate_authority_consumption_receipt",
    "validate_boundary_artifact",
]
