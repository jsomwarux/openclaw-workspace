"""Read-only, hash-bound Mission Control task snapshot for LinkedIn Program 0."""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, List, Tuple
from urllib.parse import urlsplit

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp, validate_linkedin_url


SOURCE_URL = "http://127.0.0.1:3000/api/tasks"
SCHEMA_VERSION = "linkedin-mc-snapshot.v1"
SNAPSHOT_TTL = timedelta(hours=2)
MAX_RESPONSE_BYTES = 8 * 1024 * 1024

_HASH = re.compile(r"^[0-9a-f]{64}$")
_RUN_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")
_TERMINAL_STATUSES = {"done", "archived"}
_TASK_STATUSES = {
    "todo",
    "in-progress",
    "done",
    "archived",
    "waiting-external",
    "snoozed",
}


def _utc_now() -> datetime:
    """Clock seam: production always uses actual UTC; tests may patch this helper."""

    return datetime.now(timezone.utc)


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> None:
        return None


def _require_exact_source_url(url: str) -> None:
    if not isinstance(url, str) or url != SOURCE_URL:
        raise ValueError("Mission Control capture URL must be the exact read-only loopback route")
    parsed = urlsplit(url)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.port != 3000
        or parsed.path != "/api/tasks"
        or parsed.query
        or parsed.fragment
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError("Mission Control capture URL must be the exact read-only loopback route")


def capture_tasks(url: str = SOURCE_URL) -> bytes:
    """Perform one exact unauthenticated GET against the local task read route."""

    _require_exact_source_url(url)
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
        method="GET",
    )
    headers = {key.lower() for key, _ in request.header_items()}
    if request.get_method() != "GET" or "authorization" in headers or any(
        "capability" in key for key in headers
    ):
        raise ValueError("capture request must be an unauthenticated GET")

    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        _NoRedirectHandler(),
    )
    with opener.open(request, timeout=5.0) as response:
        if getattr(response, "status", None) != 200:
            raise ValueError("Mission Control task capture returned a non-200 response")
        if response.geturl() != url:
            raise ValueError("Mission Control task capture refused a redirect")
        if response.headers.get_content_type().lower() != "application/json":
            raise ValueError("Mission Control task capture must return JSON")
        payload = response.read(MAX_RESPONSE_BYTES + 1)
    if len(payload) > MAX_RESPONSE_BYTES:
        raise ValueError("Mission Control task capture exceeds the size limit")
    return payload


def _strict_object(pairs: List[Tuple[str, Any]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key {!r}".format(key))
        value[key] = item
    return value


def _decode_json(raw: bytes) -> dict[str, object]:
    if not isinstance(raw, bytes):
        raise ValueError("raw snapshot source must be bytes")

    def reject_constant(value: str) -> None:
        raise ValueError("non-standard JSON constant {}".format(value))

    try:
        decoded = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError("Mission Control task capture is not strict JSON") from error
    if not isinstance(decoded, dict) or set(decoded) != {"tasks"}:
        raise ValueError("Mission Control task capture must contain only a tasks array")
    if not isinstance(decoded["tasks"], list):
        raise ValueError("Mission Control tasks must be an array")
    return decoded


def _require_hash(value: object, label: str) -> str:
    if not isinstance(value, str) or _HASH.fullmatch(value) is None:
        raise ValueError("{} must be a lowercase SHA-256".format(label))
    return value


def _require_run_context(
    run_context: dict[str, object]
) -> tuple[str, str, datetime, datetime]:
    if not isinstance(run_context, dict):
        raise ValueError("run context must be an object")
    if set(run_context) != {"runId", "generatedAt"}:
        raise ValueError("run context fields are not canonical")
    run_id = run_context.get("runId")
    if not isinstance(run_id, str) or _RUN_ID.fullmatch(run_id) is None:
        raise ValueError("runId must be sha256:<64 lowercase hex>")
    generated_at_value = run_context.get("generatedAt")
    if not isinstance(generated_at_value, str):
        raise ValueError("generatedAt must be a string")
    generated_at = parse_timestamp(generated_at_value, "generatedAt")
    consumer_now = _utc_now()
    if consumer_now < generated_at:
        raise ValueError("current time is before capturedAt")
    return run_id, generated_at_value, generated_at, consumer_now


def _iso(value: datetime) -> str:
    return value.isoformat()


def _task_id(task: dict[str, object]) -> str:
    value = task.get("_id", task.get("id"))
    if not isinstance(value, str) or _STABLE_ID.fullmatch(value) is None:
        raise ValueError("every Mission Control task requires a stable task ID")
    return value


def _governed_outcome_pointer(
    value: object, task_id: str, content_id: str
) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    required = {"system", "id", "recordedAt"}
    if set(value) not in (required, required | {"url"}):
        return None
    system = value.get("system")
    outcome_id = value.get("id")
    recorded_at = value.get("recordedAt")
    if (
        system != "linkedin-content-os"
        or not isinstance(outcome_id, str)
        or outcome_id
        != "publication_acknowledged:{}:{}".format(task_id, content_id)
        or not isinstance(recorded_at, int)
        or isinstance(recorded_at, bool)
        or recorded_at < 0
    ):
        return None
    pointer: dict[str, object] = {
        "system": system,
        "id": outcome_id,
        "recordedAt": recorded_at,
    }
    if "url" in value:
        try:
            pointer["url"] = validate_linkedin_url(value["url"])
        except ValueError:
            return None
    return pointer


def _project_task(task: dict[str, object]) -> dict[str, object] | None:
    if not (
        task.get("packetSchema") == "lane-packet-v1"
        and task.get("growthLane") == "linkedin"
        and task.get("approvalState") == "approved"
    ):
        return None
    payload_hash = _require_hash(task.get("payloadHash"), "payloadHash")
    approved_hash = _require_hash(
        task.get("approvedPayloadHash"), "approvedPayloadHash"
    )
    if approved_hash != payload_hash:
        return None

    packet_hash_value = task.get("packetHash")
    if packet_hash_value is None and isinstance(task.get("artifactRef"), dict):
        packet_hash_value = task["artifactRef"].get("sha256")  # type: ignore[index]
    packet_hash = _require_hash(packet_hash_value, "packetHash")
    task_id = _task_id(task)
    status = task.get("status")
    if not isinstance(status, str) or status not in _TASK_STATUSES:
        raise ValueError("lane packet status is unsupported")
    content_id = task.get("contentId")
    if content_id is None and isinstance(task.get("artifactRef"), dict):
        content_id = task["artifactRef"].get("id")  # type: ignore[index]
    if not isinstance(content_id, str) or _STABLE_ID.fullmatch(content_id) is None:
        raise ValueError("LinkedIn lane packet requires a stable contentId")

    projection: dict[str, object] = {
        "taskId": task_id,
        "status": status,
        "approvalState": "approved",
        "packetHash": packet_hash,
        "payloadHash": payload_hash,
        "approvedPayloadHash": approved_hash,
        "contentId": content_id,
    }
    expires_at = task.get("expiresAt")
    if expires_at is not None:
        if not isinstance(expires_at, int) or isinstance(expires_at, bool) or expires_at < 0:
            raise ValueError("expiresAt must be a non-negative integer")
        projection["expiresAt"] = expires_at

    if status not in _TERMINAL_STATUSES:
        projection["projectionType"] = "publication_acknowledgment"
        return projection
    if status != "done":
        return None
    pointer = _governed_outcome_pointer(
        task.get("outcomeRef"), task_id, content_id
    )
    if pointer is None:
        return None
    projection["projectionType"] = "metrics_followup"
    projection["closureType"] = "completed"
    projection["closureOutcomePointer"] = pointer
    return projection


def validate_snapshot(
    raw: bytes, run_context: dict[str, object]
) -> dict[str, object]:
    """Validate exact task bytes and return a minimal canonical wrapper."""

    run_id, captured_at_text, captured_at, consumer_now = _require_run_context(run_context)
    valid_until = captured_at + SNAPSHOT_TTL
    if consumer_now > valid_until:
        raise ValueError("Mission Control snapshot is stale")
    decoded = _decode_json(raw)
    tasks = decoded["tasks"]
    assert isinstance(tasks, list)
    task_ids: set[str] = set()
    packets: list[dict[str, object]] = []
    for raw_task in tasks:
        if not isinstance(raw_task, dict):
            raise ValueError("every Mission Control task must be an object")
        task: dict[str, object] = raw_task
        task_id = _task_id(task)
        if task_id in task_ids:
            raise ValueError("duplicate Mission Control task ID")
        task_ids.add(task_id)
        projected = _project_task(task)
        if projected is not None:
            packets.append(projected)
    packets.sort(key=lambda packet: str(packet["taskId"]))
    snapshot: dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "runId": run_id,
        "capturedAt": captured_at_text,
        "validUntil": _iso(valid_until),
        "sourceUrl": SOURCE_URL,
        "rawSha256": sha256_hex(raw),
        "totalTaskCount": len(tasks),
        "linkedinLanePacketCount": len(packets),
        "packets": packets,
    }
    snapshot["projectionSha256"] = sha256_hex(canonical_bytes(snapshot))
    return snapshot


def approved_linkedin_packets(
    snapshot: dict[str, object], run_context: dict[str, object]
) -> list[dict[str, object]]:
    """Validate a wrapper against the current run before returning projections."""

    if not isinstance(snapshot, dict):
        raise ValueError("snapshot must be an object")
    expected_fields = {
        "schemaVersion",
        "runId",
        "capturedAt",
        "validUntil",
        "sourceUrl",
        "rawSha256",
        "totalTaskCount",
        "linkedinLanePacketCount",
        "packets",
        "projectionSha256",
    }
    if set(snapshot) != expected_fields:
        missing = expected_fields - set(snapshot)
        if "rawSha256" in missing:
            raise ValueError("snapshot missing rawSha256")
        raise ValueError("snapshot wrapper fields are not canonical")
    if snapshot["schemaVersion"] != SCHEMA_VERSION:
        raise ValueError("unsupported snapshot schemaVersion")
    projection_sha256 = _require_hash(
        snapshot["projectionSha256"], "projectionSha256"
    )
    digest_source = {
        key: value for key, value in snapshot.items() if key != "projectionSha256"
    }
    try:
        expected_projection_sha256 = sha256_hex(canonical_bytes(digest_source))
    except (TypeError, ValueError) as error:
        raise ValueError("snapshot cannot be canonically hashed") from error
    if projection_sha256 != expected_projection_sha256:
        raise ValueError("projectionSha256 does not match the persisted projection")
    run_id = snapshot["runId"]
    if not isinstance(run_id, str) or _RUN_ID.fullmatch(run_id) is None:
        raise ValueError("invalid snapshot runId")
    (
        current_run_id,
        generated_at_text,
        generated_at,
        consumer_now,
    ) = _require_run_context(run_context)
    if run_id != current_run_id or snapshot["capturedAt"] != generated_at_text:
        raise ValueError("snapshot does not belong to the current run context")
    if snapshot["sourceUrl"] != SOURCE_URL:
        raise ValueError("invalid snapshot sourceUrl")
    _require_hash(snapshot["rawSha256"], "rawSha256")
    captured_at = parse_timestamp(snapshot["capturedAt"], "capturedAt")
    valid_until = parse_timestamp(snapshot["validUntil"], "validUntil")
    if captured_at != generated_at:
        raise ValueError("snapshot does not belong to the current run context")
    if valid_until != captured_at + SNAPSHOT_TTL:
        raise ValueError("validUntil must be exactly two hours after capturedAt")
    if consumer_now > valid_until:
        raise ValueError("Mission Control snapshot is stale")
    packets = snapshot["packets"]
    if not isinstance(packets, list):
        raise ValueError("snapshot packets must be an array")
    linkedin_count = snapshot["linkedinLanePacketCount"]
    if (
        not isinstance(linkedin_count, int)
        or isinstance(linkedin_count, bool)
        or linkedin_count != len(packets)
    ):
        raise ValueError("LinkedIn packet count mismatch")
    if (
        not isinstance(snapshot["totalTaskCount"], int)
        or isinstance(snapshot["totalTaskCount"], bool)
        or snapshot["totalTaskCount"] < len(packets)
    ):
        raise ValueError("invalid total task count")
    result: list[dict[str, object]] = []
    seen: set[str] = set()
    prior_task_id: str | None = None
    for packet_value in packets:
        if not isinstance(packet_value, dict):
            raise ValueError("projected packet must be an object")
        packet: dict[str, object] = packet_value
        common_fields = {
            "taskId",
            "status",
            "approvalState",
            "packetHash",
            "payloadHash",
            "approvedPayloadHash",
            "contentId",
            "projectionType",
        }
        allowed_fields = common_fields | ({"expiresAt"} if "expiresAt" in packet else set())
        if packet.get("projectionType") == "metrics_followup":
            allowed_fields |= {"closureType", "closureOutcomePointer"}
        if set(packet) != allowed_fields:
            raise ValueError("projected packet does not have canonical fields")
        task_id = packet.get("taskId")
        if (
            not isinstance(task_id, str)
            or _STABLE_ID.fullmatch(task_id) is None
            or task_id in seen
        ):
            raise ValueError("projected packet task IDs must be unique")
        if prior_task_id is not None and task_id <= prior_task_id:
            raise ValueError("projected packets are not in canonical task ID order")
        prior_task_id = task_id
        seen.add(task_id)
        _require_hash(packet.get("packetHash"), "packetHash")
        payload_hash = _require_hash(packet.get("payloadHash"), "payloadHash")
        if _require_hash(packet.get("approvedPayloadHash"), "approvedPayloadHash") != payload_hash:
            raise ValueError("approved payload hash mismatch")
        if packet.get("approvalState") != "approved":
            raise ValueError("projected packet is not approved")
        content_id = packet.get("contentId")
        if (
            not isinstance(content_id, str)
            or _STABLE_ID.fullmatch(content_id) is None
        ):
            raise ValueError("projected packet contentId must be a stable identifier")
        status = packet.get("status")
        if not isinstance(status, str) or status not in _TASK_STATUSES:
            raise ValueError("projected packet status is unsupported")
        if "expiresAt" in packet:
            expires_at = packet["expiresAt"]
            if (
                not isinstance(expires_at, int)
                or isinstance(expires_at, bool)
                or expires_at < 0
            ):
                raise ValueError("projected packet expiresAt is invalid")
        projection_type = packet.get("projectionType")
        if projection_type == "metrics_followup":
            if status != "done" or packet.get("closureType") != "completed":
                raise ValueError("metrics projection is not a completed packet")
            if (
                _governed_outcome_pointer(
                    packet.get("closureOutcomePointer"), task_id, content_id
                )
                is None
            ):
                raise ValueError("metrics projection lacks a governed publication outcome")
        elif projection_type == "publication_acknowledgment":
            if status in _TERMINAL_STATUSES:
                raise ValueError("terminal packet cannot request publication acknowledgment")
        else:
            raise ValueError("unsupported projectionType")
        result.append(dict(packet))
    return result
