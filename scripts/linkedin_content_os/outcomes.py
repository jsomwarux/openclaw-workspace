"""Append-only storage for validated LinkedIn Program 0 outcome events."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from scripts.linkedin_content_os.canonical import (
    _exclusive_path_lock,
    append_jsonl_exact_prefix,
    read_jsonl,
)
from scripts.linkedin_content_os.contracts import parse_timestamp, validate_event


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
    return rows


def load_events(path: Path) -> list[dict[str, object]]:
    """Load and validate a complete strict outcome ledger."""

    return _validated_rows(path)


def append_event(
    path: Path, event: dict[str, object]
) -> Literal["appended", "replayed"]:
    """Append one event, or report an exact idempotent replay."""

    validate_event(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    transaction_path = path.with_name("{}.transaction".format(path.name))
    with _exclusive_path_lock(transaction_path):
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

        append_jsonl_exact_prefix(path, event)
        return "appended"


__all__ = ["append_event", "load_events"]
