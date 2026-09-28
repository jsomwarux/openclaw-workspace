"""Read-only, hash-bound Mission Control task snapshot for LinkedIn Program 0."""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, List, Tuple
from urllib.parse import urlsplit

from scripts.linkedin_content_os.canonical import sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp


SOURCE_URL = "http://127.0.0.1:3000/api/tasks"
SCHEMA_VERSION = "linkedin-mc-snapshot.v1"
SNAPSHOT_TTL = timedelta(hours=2)
MAX_RESPONSE_BYTES = 8 * 1024 * 1024

_HASH = re.compile(r"^[0-9a-f]{64}$")
_RUN_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_TERMINAL_STATUSES = {"done", "archived"}


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

    opener = urllib.request.build_opener(_NoRedirectHandler())
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
    run_id = run_context.get("runId")
    if not isinstance(run_id, str) or _RUN_ID.fullmatch(run_id) is None:
        raise ValueError("runId must be sha256:<64 lowercase hex>")
    generated_at_value = run_context.get("generatedAt")
    generated_at = parse_timestamp(generated_at_value, "generatedAt")
    assert isinstance(generated_at_value, str)
    consumer_value = run_context.get("consumerNow")
    consumer_now = (
        parse_timestamp(consumer_value, "consumerNow")
        if consumer_value is not None
        else datetime.now(timezone.utc)
    )
    return run_id, generated_at_value, generated_at, consumer_now


def _iso(value: datetime) -> str:
    return value.isoformat()


def _task_id(task: dict[str, object]) -> str:
    value = task.get("_id", task.get("id"))
    if not isinstance(value, str) or not value:
        raise ValueError("every Mission Control task requires a non-empty task ID")
    return value


def _governed_outcome_pointer(value: object) -> dict[str, str] | None:
    if not isinstance(value, dict):
        return None
    system = value.get("system")
    outcome_id = value.get("id")
    if (
        system != "linkedin-content-os"
        or not isinstance(outcome_id, str)
        or not outcome_id.startswith("publication_acknowledged:")
        or len(outcome_id) == len("publication_acknowledged:")
    ):
        return None
    return {"system": system, "id": outcome_id}


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
    if not isinstance(status, str) or not status:
        raise ValueError("lane packet status must be a non-empty string")
    content_id = task.get("contentId")
    if content_id is None and isinstance(task.get("artifactRef"), dict):
        content_id = task["artifactRef"].get("id")  # type: ignore[index]
    if not isinstance(content_id, str) or not content_id:
        raise ValueError("LinkedIn lane packet requires contentId")

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
    pointer = _governed_outcome_pointer(task.get("outcomeRef"))
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
    return {
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
    }
    if set(snapshot) != expected_fields:
        missing = expected_fields - set(snapshot)
        if "rawSha256" in missing:
            raise ValueError("snapshot missing rawSha256")
        raise ValueError("snapshot wrapper fields are not canonical")
    if snapshot["schemaVersion"] != SCHEMA_VERSION:
        raise ValueError("unsupported snapshot schemaVersion")
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
    if snapshot["linkedinLanePacketCount"] != len(packets):
        raise ValueError("LinkedIn packet count mismatch")
    if (
        not isinstance(snapshot["totalTaskCount"], int)
        or isinstance(snapshot["totalTaskCount"], bool)
        or snapshot["totalTaskCount"] < len(packets)
    ):
        raise ValueError("invalid total task count")
    result: list[dict[str, object]] = []
    seen: set[str] = set()
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
        if not isinstance(task_id, str) or not task_id or task_id in seen:
            raise ValueError("projected packet task IDs must be unique")
        seen.add(task_id)
        _require_hash(packet.get("packetHash"), "packetHash")
        payload_hash = _require_hash(packet.get("payloadHash"), "payloadHash")
        if _require_hash(packet.get("approvedPayloadHash"), "approvedPayloadHash") != payload_hash:
            raise ValueError("approved payload hash mismatch")
        if packet.get("approvalState") != "approved":
            raise ValueError("projected packet is not approved")
        projection_type = packet.get("projectionType")
        if projection_type == "metrics_followup":
            if packet.get("status") != "done" or packet.get("closureType") != "completed":
                raise ValueError("metrics projection is not a completed packet")
            if _governed_outcome_pointer(packet.get("closureOutcomePointer")) is None:
                raise ValueError("metrics projection lacks a governed publication outcome")
        elif projection_type == "publication_acknowledgment":
            if packet.get("status") in _TERMINAL_STATUSES:
                raise ValueError("terminal packet cannot request publication acknowledgment")
        else:
            raise ValueError("unsupported projectionType")
        result.append(dict(packet))
    return result
