"""Pure, read-only projection of one LinkedIn outcome check-in preview."""

from __future__ import annotations

import re
from datetime import datetime, timedelta

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import (
    parse_timestamp,
    validate_event,
    validate_linkedin_url,
)
from scripts.linkedin_content_os.outcomes import validate_event_sequence


SCHEMA_VERSION = "linkedin-checkin-preview.v1"
DEDUPE_KEY = "linkedin-checkin:v1"
SNAPSHOT_SCHEMA_VERSION = "linkedin-mc-snapshot.v1"
SNAPSHOT_SOURCE_URL = "http://127.0.0.1:3000/api/tasks"
SNAPSHOT_TTL = timedelta(hours=2)
METRICS_WINDOW = timedelta(days=7)

_HASH = re.compile(r"^[0-9a-f]{64}$")
_RUN_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")
_EVENT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_PUBLICATION_EVENTS = {
    "publication_acknowledged",
    "publication_deferred",
    "publication_declined",
    "metric_snapshot",
}
_NONTERMINAL_STATUSES = {"todo", "in-progress", "waiting-external", "snoozed"}


def _require_hash(value: object, label: str) -> str:
    if not isinstance(value, str) or _HASH.fullmatch(value) is None:
        raise ValueError("{} must be a lowercase SHA-256".format(label))
    return value


def _require_stable_id(value: object, label: str) -> str:
    if not isinstance(value, str) or _STABLE_ID.fullmatch(value) is None:
        raise ValueError("{} must be a stable identifier".format(label))
    return value


def _require_aware(now: datetime) -> None:
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be a timezone-aware datetime")


def _validate_snapshot(
    snapshot: dict[str, object], now: datetime
) -> list[dict[str, object]]:
    if not isinstance(snapshot, dict):
        raise ValueError("Mission Control snapshot must be an object")
    fields = {
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
    if set(snapshot) != fields:
        raise ValueError("Mission Control snapshot fields are not canonical")
    if snapshot["schemaVersion"] != SNAPSHOT_SCHEMA_VERSION:
        raise ValueError("unsupported Mission Control snapshot schema")
    run_id = snapshot["runId"]
    if not isinstance(run_id, str) or _RUN_ID.fullmatch(run_id) is None:
        raise ValueError("Mission Control snapshot runId is invalid")
    if snapshot["sourceUrl"] != SNAPSHOT_SOURCE_URL:
        raise ValueError("Mission Control snapshot source URL is invalid")
    _require_hash(snapshot["rawSha256"], "rawSha256")
    provided_digest = _require_hash(
        snapshot["projectionSha256"], "projectionSha256"
    )
    digest_source = {
        key: value for key, value in snapshot.items() if key != "projectionSha256"
    }
    try:
        expected_digest = sha256_hex(canonical_bytes(digest_source))
    except (TypeError, ValueError) as error:
        raise ValueError("Mission Control snapshot cannot be canonically hashed") from error
    if provided_digest != expected_digest:
        raise ValueError("projectionSha256 does not match the Mission Control snapshot")

    captured_at = parse_timestamp(snapshot["capturedAt"], "capturedAt")
    valid_until = parse_timestamp(snapshot["validUntil"], "validUntil")
    if valid_until != captured_at + SNAPSHOT_TTL:
        raise ValueError("Mission Control snapshot validity window is not canonical")
    if now < captured_at:
        raise ValueError("now precedes the Mission Control snapshot")
    if now > valid_until:
        raise ValueError("Mission Control snapshot is stale")

    packets_value = snapshot["packets"]
    if not isinstance(packets_value, list):
        raise ValueError("Mission Control snapshot packets must be an array")
    packet_count = snapshot["linkedinLanePacketCount"]
    total_count = snapshot["totalTaskCount"]
    if (
        not isinstance(packet_count, int)
        or isinstance(packet_count, bool)
        or packet_count != len(packets_value)
        or not isinstance(total_count, int)
        or isinstance(total_count, bool)
        or total_count < packet_count
    ):
        raise ValueError("Mission Control snapshot counts are invalid")

    packets: list[dict[str, object]] = []
    seen: set[str] = set()
    seen_content_ids: set[str] = set()
    prior_task_id: str | None = None
    for value in packets_value:
        if not isinstance(value, dict):
            raise ValueError("projected packet must be an object")
        packet: dict[str, object] = value
        common = {
            "taskId",
            "status",
            "approvalState",
            "packetHash",
            "payloadHash",
            "approvedPayloadHash",
            "contentId",
            "projectionType",
        }
        allowed = common | ({"expiresAt"} if "expiresAt" in packet else set())
        projection_type = packet.get("projectionType")
        if projection_type == "metrics_followup":
            allowed |= {
                "closureType",
                "doneEvidenceType",
                "doneEvidence",
                "closureOutcomePointer",
            }
        if set(packet) != allowed:
            raise ValueError("projected packet fields are not canonical")
        task_id = _require_stable_id(packet.get("taskId"), "taskId")
        if task_id in seen or (prior_task_id is not None and task_id <= prior_task_id):
            raise ValueError("projected packet task IDs must be unique and sorted")
        seen.add(task_id)
        prior_task_id = task_id
        _require_hash(packet.get("packetHash"), "packetHash")
        payload_hash = _require_hash(packet.get("payloadHash"), "payloadHash")
        if (
            _require_hash(packet.get("approvedPayloadHash"), "approvedPayloadHash")
            != payload_hash
        ):
            raise ValueError("approved payload hash mismatch")
        if packet.get("approvalState") != "approved":
            raise ValueError("projected packet is not approved")
        content_id = _require_stable_id(packet.get("contentId"), "contentId")
        if content_id in seen_content_ids:
            raise ValueError("projected packet contentId values must be unique")
        seen_content_ids.add(content_id)
        expires_at = packet.get("expiresAt")
        if expires_at is not None and (
            not isinstance(expires_at, int)
            or isinstance(expires_at, bool)
            or expires_at < 0
        ):
            raise ValueError("expiresAt must be a non-negative integer")
        if projection_type == "publication_acknowledgment":
            if packet.get("status") not in _NONTERMINAL_STATUSES:
                raise ValueError("publication packet status is unsupported")
        elif projection_type == "metrics_followup":
            _validate_terminal_projection(packet)
        else:
            raise ValueError("unsupported packet projectionType")
        packets.append(packet)
    return packets


def _validate_terminal_projection(packet: dict[str, object]) -> None:
    if (
        packet.get("status") != "done"
        or packet.get("closureType") != "completed"
        or packet.get("doneEvidenceType") != "post-url"
    ):
        raise ValueError("terminal packet lacks a governed publication closure")
    evidence = packet.get("doneEvidence")
    pointer = packet.get("closureOutcomePointer")
    if not isinstance(evidence, dict) or set(evidence) != {
        "type",
        "ref",
        "recordedAt",
        "recordedBy",
    }:
        raise ValueError("terminal packet lacks canonical publication evidence")
    if evidence.get("type") != "post-url" or evidence.get("recordedBy") != "jt":
        raise ValueError("terminal packet lacks canonical publication evidence")
    validate_linkedin_url(evidence.get("ref"))
    if not isinstance(pointer, dict) or set(pointer) not in (
        {"system", "id", "recordedAt"},
        {"system", "id", "recordedAt", "url"},
    ):
        raise ValueError("terminal packet lacks a governed publication closure")
    if pointer.get("system") != "linkedin-content-os":
        raise ValueError("terminal packet lacks a governed publication closure")
    if "url" in pointer:
        validate_linkedin_url(pointer.get("url"))
    outcome_id = pointer.get("id")
    if not isinstance(outcome_id, str) or _EVENT_ID.fullmatch(outcome_id) is None:
        raise ValueError("terminal packet publication outcome ID is invalid")
    for value, label in (
        (evidence.get("recordedAt"), "doneEvidence.recordedAt"),
        (pointer.get("recordedAt"), "closureOutcomePointer.recordedAt"),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("{} must be a non-negative integer".format(label))


def _effective_events(events: list[dict[str, object]]) -> list[dict[str, object]]:
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    copied: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    for event in events:
        validated = validate_event(event)
        event_id = str(validated["outcomeEventId"])
        event_hash = str(validated["eventSha256"])
        if event_id in seen_ids:
            raise ValueError("duplicate outcomeEventId in events")
        if event_hash in seen_hashes:
            raise ValueError("duplicate eventSha256 in events")
        seen_ids.add(event_id)
        seen_hashes.add(event_hash)
        copied.append(validated)
    validate_event_sequence(copied)
    by_hash = {str(event["eventSha256"]): event for event in copied}
    superseded: set[str] = set()
    for event in copied:
        if event["eventType"] != "correction":
            continue
        payload = event["payload"]
        assert isinstance(payload, dict)
        superseded.add(str(payload["targetOutcomeEventId"]))
        replacement = by_hash[str(payload["replacementEventSha256"])]
        if replacement["outcomeEventId"] in superseded:
            raise ValueError("replacement event is superseded")
    return [
        event
        for event in copied
        if event["eventType"] != "correction"
        and event["outcomeEventId"] not in superseded
    ]


def _events_for_packet(
    packet: dict[str, object], events: list[dict[str, object]]
) -> list[dict[str, object]]:
    packet_events = [
        event
        for event in events
        if event["packetId"] == packet["contentId"]
        and event["eventType"] in _PUBLICATION_EVENTS
    ]
    packet_events.sort(
        key=lambda event: (
            parse_timestamp(event["recordedAt"], "recordedAt"),
            str(event["outcomeEventId"]),
        )
    )
    for event in packet_events:
        source = event["sourcePointer"]
        assert isinstance(source, dict)
        if (
            source.get("sourceType") != "mission_control_packet"
            or source.get("sourceId") != packet["taskId"]
            or source.get("sourceSha256") != packet["payloadHash"]
        ):
            raise ValueError("outcome event is not bound to the approved packet")
    return packet_events


def _publication_state(
    packet: dict[str, object], events: list[dict[str, object]]
) -> tuple[dict[str, object] | None, dict[str, object] | None, datetime | None]:
    terminal: dict[str, object] | None = None
    deferred: dict[str, object] | None = None
    metric_events: list[dict[str, object]] = []
    for event in events:
        event_type = event["eventType"]
        if event_type == "publication_deferred":
            if terminal is not None:
                raise ValueError("publication deferral cannot follow a terminal decision")
            deferred = event
        elif event_type in {"publication_acknowledged", "publication_declined"}:
            if terminal is not None:
                raise ValueError("packet has conflicting publication decisions")
            terminal = event
        elif event_type == "metric_snapshot":
            payload = event["payload"]
            assert isinstance(payload, dict)
            if payload["windowDays"] == 7:
                metric_events.append(event)

    if terminal is not None and terminal["eventType"] == "publication_declined":
        if metric_events:
            raise ValueError("declined publication cannot have metrics")
        return terminal, None, None
    if terminal is None:
        if metric_events:
            raise ValueError("metrics require a publication acknowledgment")
        next_check = None
        if deferred is not None:
            payload = deferred["payload"]
            assert isinstance(payload, dict)
            next_check = parse_timestamp(payload["nextCheckAt"], "nextCheckAt")
        return None, None, next_check

    payload = terminal["payload"]
    assert isinstance(payload, dict)
    published_at = parse_timestamp(
        payload.get("publishedAt", terminal["recordedAt"]), "publishedAt"
    )
    metrics_due = published_at + METRICS_WINDOW
    eligible_metrics = [
        event
        for event in metric_events
        if parse_timestamp(event["recordedAt"], "recordedAt") >= metrics_due
    ]
    if len(eligible_metrics) > 1:
        raise ValueError("packet has duplicate seven-day metric snapshots")
    return terminal, eligible_metrics[0] if eligible_metrics else None, metrics_due


def _validate_terminal_binding(
    packet: dict[str, object], publication: dict[str, object] | None
) -> None:
    if packet["projectionType"] != "metrics_followup":
        return
    if publication is None or publication["eventType"] != "publication_acknowledged":
        raise ValueError("terminal packet is missing its matching publication closure")
    pointer = packet["closureOutcomePointer"]
    evidence = packet["doneEvidence"]
    assert isinstance(pointer, dict) and isinstance(evidence, dict)
    payload = publication["payload"]
    assert isinstance(payload, dict)
    if (
        pointer["id"] != publication["outcomeEventId"]
        or evidence["ref"] != payload["publicationUrl"]
        or ("url" in pointer and pointer["url"] != payload["publicationUrl"])
    ):
        raise ValueError("terminal packet is missing its matching publication closure")
    published_at = parse_timestamp(
        payload.get("publishedAt", publication["recordedAt"]), "publishedAt"
    )
    published_millis = _milliseconds(published_at)
    if (
        evidence["recordedAt"] < published_millis
        or pointer["recordedAt"] < published_millis
    ):
        raise ValueError("terminal publication closure predates publication")


def _milliseconds(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def project_checkin(
    mc_snapshot: dict[str, object],
    events: list[dict[str, object]],
    now: datetime,
) -> dict[str, object] | None:
    """Return zero or one deterministic, non-writable universal-task preview."""

    _require_aware(now)
    packets = _validate_snapshot(mc_snapshot, now)
    effective_events = _effective_events(events)
    publication_steps: list[tuple[datetime, str]] = []
    metrics_steps: list[tuple[datetime, str]] = []

    for packet in packets:
        packet_events = _events_for_packet(packet, effective_events)
        publication, metrics, next_due = _publication_state(packet, packet_events)
        _validate_terminal_binding(packet, publication)
        task_id = str(packet["taskId"])
        content_id = str(packet["contentId"])

        if packet["projectionType"] == "publication_acknowledgment":
            expires_at = packet.get("expiresAt")
            if isinstance(expires_at, int) and _milliseconds(now) > expires_at:
                raise ValueError("approved packet expired before acknowledgment")
            if (
                isinstance(expires_at, int)
                and publication is None
                and next_due is not None
                and _milliseconds(next_due) > expires_at
            ):
                raise ValueError("publication deferral exceeds packet expiry")
            if publication is None and (next_due is None or now >= next_due):
                publication_steps.append(
                    (
                        next_due or now,
                        "For {} ({}), choose posted / not yet / won't post. "
                        "Posted requires the LinkedIn URL; not yet requires the next check date; "
                        "won't post records a closed reason and governed no-action closure.".format(
                            task_id, content_id
                        ),
                    )
                )

        if publication is not None and publication["eventType"] == "publication_acknowledged":
            assert next_due is not None
            if metrics is None and now >= next_due:
                metrics_steps.append(
                    (
                        next_due,
                        "For {} ({}), record the one seven-day performance snapshot. "
                        "Any unavailable metric stays metrics_unknown; never enter zero for missing data.".format(
                            task_id, content_id
                        ),
                    )
                )

    unresolved = publication_steps + metrics_steps
    if not unresolved:
        return None
    publication_steps.sort(key=lambda item: (item[0], item[1]))
    metrics_steps.sort(key=lambda item: (item[0], item[1]))
    exact_steps = [text for _, text in publication_steps + metrics_steps]
    due_at = min(item[0] for item in unresolved)
    task: dict[str, object] = {
        "title": "Update LinkedIn publication and performance truth",
        "whyItMatters": (
            "The Content OS cannot improve quality or fit while publication decisions and "
            "seven-day outcomes are missing."
        ),
        "exactSteps": exact_steps,
        "doneState": "Every listed publication or seven-day metrics gap is recorded once.",
        "dueDate": _milliseconds(due_at),
        "dueDateSource": "self",
        "project": "LinkedIn Content OS",
        "assignee": "jt",
        "dedupeKey": DEDUPE_KEY,
    }
    return {
        "schemaVersion": SCHEMA_VERSION,
        "sourceSnapshotSha256": mc_snapshot["projectionSha256"],
        "liveWriteAuthorized": False,
        "task": task,
    }


__all__ = ["DEDUPE_KEY", "SCHEMA_VERSION", "project_checkin"]
