"""Read-only, evidence-bound audit of the legacy LinkedIn posted ledger."""

from __future__ import annotations

from collections import Counter
from datetime import date as calendar_date
from pathlib import Path
from typing import Optional

from scripts.linkedin_content_os.canonical import canonical_bytes, read_jsonl_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp, validate_linkedin_url
from scripts.linkedin_content_os.outcomes import load_events


_STATUSES = ("not_posted_confirmed", "posted_confirmed", "status_unknown")
_JT_POSTED_CONFIRMATION = "JT_CONFIRMED_POSTED"


def _legacy_row_hash(row: dict[str, object]) -> str:
    return sha256_hex(canonical_bytes(row))


def _public_url(row: dict[str, object]) -> Optional[str]:
    value = row.get("public_url", row.get("publicUrl"))
    try:
        return validate_linkedin_url(value)
    except ValueError:
        return None


def _final_text(row: dict[str, object]) -> Optional[str]:
    value = row.get("final_text", row.get("finalText"))
    if not isinstance(value, str) or not value.strip():
        return None
    return value


def _has_exact_jt_posted_confirmation(row: dict[str, object]) -> bool:
    return row.get("posted_confirmation") == _JT_POSTED_CONFIRMATION


def _topic(row: dict[str, object], row_hash: str) -> str:
    for key in ("topic", "summary", "text"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "untitled:{}".format(row_hash[:12])


def _canonical_date(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("legacy LinkedIn date must be canonical YYYY-MM-DD")
    try:
        parsed = calendar_date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("legacy LinkedIn date must be canonical YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise ValueError("legacy LinkedIn date must be canonical YYYY-MM-DD")
    return value


def _governed_statuses(outcomes: Optional[Path]) -> dict[str, str]:
    if outcomes is None:
        return {}
    selected: dict[str, tuple[object, str, str]] = {}
    for event in load_events(outcomes):
        if event["eventType"] != "historical_status":
            continue
        payload = event["payload"]
        assert isinstance(payload, dict)
        row_hash = str(payload["legacyRowSha256"])
        status = str(payload["status"])
        timestamp = parse_timestamp(event["recordedAt"], "recordedAt")
        event_hash = str(event["eventSha256"])
        prior = selected.get(row_hash)
        if prior is not None and timestamp == prior[0] and status != prior[1]:
            raise ValueError("conflicting historical statuses at the same timestamp")
        if prior is None or (timestamp, event_hash) > (prior[0], prior[2]):
            selected[row_hash] = (timestamp, status, event_hash)
    return {row_hash: value[1] for row_hash, value in selected.items()}


def _allowed_answers() -> list[dict[str, object]]:
    return [
        {"answer": "posted", "required": ["publicUrl"], "optional": ["finalText"]},
        {
            "answer": "not_posted",
            "required": ["declineReason"],
            "allowedDeclineReasons": ["quality_fit", "stale", "timing", "other"],
        },
        {"answer": "still_unknown", "required": []},
    ]


def audit_legacy_rows(
    posted_log: Path, outcomes: Optional[Path], generated_at: str
) -> dict[str, object]:
    """Classify LinkedIn rows without mutating or over-interpreting legacy data."""

    parse_timestamp(generated_at, "generated_at")
    source_before = posted_log.read_bytes()
    rows = read_jsonl_bytes(source_before, str(posted_log))
    governed = _governed_statuses(outcomes)

    records: list[dict[str, object]] = []
    recovery_candidates: list[tuple[bool, str, str, dict[str, object]]] = []
    row_hashes: list[str] = []
    missing_counts: Counter[str] = Counter()

    for row in rows:
        platform = row.get("platform")
        if not isinstance(platform, str) or platform.lower() != "linkedin":
            continue
        row_hash = _legacy_row_hash(row)
        row_hashes.append(row_hash)
        date = _canonical_date(row.get("date"))
        topic = _topic(row, row_hash)
        public_url = _public_url(row)
        final_text = _final_text(row)
        raw_posted = row.get("posted") is True

        status = governed.get(row_hash)
        if status is None:
            if raw_posted and (
                public_url is not None or _has_exact_jt_posted_confirmation(row)
            ):
                status = "posted_confirmed"
            else:
                status = "status_unknown"

        missing: list[str] = []
        if status == "posted_confirmed" or raw_posted:
            if public_url is None:
                missing.append("public_url")
            if final_text is None:
                missing.append("final_text")
        for field in missing:
            missing_counts[field] += 1

        record = {
            "date": date,
            "legacyRowSha256": row_hash,
            "missing": missing,
            "status": status,
            "topic": topic,
        }
        records.append(record)
        if (raw_posted and bool(missing)) or status == "status_unknown":
            recovery_candidates.append((raw_posted and bool(missing), date, row_hash, record))

    source_after = posted_log.read_bytes()
    if source_after != source_before:
        raise RuntimeError("posted log changed during audit")

    duplicate_groups = [
        {"legacyRowSha256": row_hash, "count": count}
        for row_hash, count in sorted(Counter(row_hashes).items())
        if count > 1
    ]
    status_counts = Counter(str(record["status"]) for record in records)

    required = sorted(
        (candidate for candidate in recovery_candidates if candidate[0]),
        key=lambda item: (item[1], item[2]),
        reverse=True,
    )
    recent_unknown_candidates = sorted(
        (candidate for candidate in recovery_candidates if not candidate[0]),
        key=lambda item: (item[1], item[2]),
        reverse=True,
    )
    recent_unknown: list[tuple[bool, str, str, dict[str, object]]] = []
    recent_unknown_hashes: set[str] = set()
    for candidate in recent_unknown_candidates:
        row_hash = candidate[2]
        if row_hash in recent_unknown_hashes:
            continue
        recent_unknown_hashes.add(row_hash)
        recent_unknown.append(candidate)
        if len(recent_unknown) == 20:
            break
    recovery_items: list[dict[str, object]] = []
    seen_recovery_hashes: set[str] = set()
    for _, _, row_hash, record in required + recent_unknown:
        if row_hash in seen_recovery_hashes:
            continue
        seen_recovery_hashes.add(row_hash)
        recovery_items.append(
            {
                "allowedAnswers": _allowed_answers(),
                "date": record["date"],
                "legacyRowSha256": row_hash,
                "topic": record["topic"],
            }
        )

    return {
        "schemaVersion": "linkedin-historical-audit.v1",
        "generatedAt": generated_at,
        "sourceSha256": sha256_hex(source_before),
        "statusCounts": {status: status_counts.get(status, 0) for status in _STATUSES},
        "missingFieldCounts": dict(sorted(missing_counts.items())),
        "duplicateGroups": duplicate_groups,
        "records": records,
        "recoveryRequest": {
            "schemaVersion": "linkedin-historical-recovery-request.v1",
            "generatedAt": generated_at,
            "sourceSha256": sha256_hex(source_before),
            "items": recovery_items,
        },
    }


__all__ = ["audit_legacy_rows"]
