"""Read-only, evidence-bound audit of the legacy LinkedIn posted ledger."""

from __future__ import annotations

from collections import Counter
from datetime import date as calendar_date
from pathlib import Path
from typing import Optional

from scripts.linkedin_content_os.canonical import (
    canonical_bytes,
    read_jsonl_bytes,
    sha256_hex,
)
from scripts.linkedin_content_os.contracts import parse_timestamp, validate_linkedin_url
from scripts.linkedin_content_os.outcomes import load_events


_STATUSES = ("not_posted_confirmed", "posted_confirmed", "status_unknown")
_JT_POSTED_CONFIRMATION = "JT_CONFIRMED_POSTED"
_HASH_CHARS = set("0123456789abcdef")
_MANIFEST_FIELDS = {
    "schemaVersion",
    "runId",
    "validatedAt",
    "receiptSha256Allowlist",
    "humanGateAuthorityReceiptSha256",
    "ledgerPrefixSha256",
    "ledgerPosition",
    "manifestSha256",
}


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


def _governed_evidence(outcomes: Optional[Path]) -> dict[str, dict[str, object]]:
    if outcomes is None:
        return {}
    selected: dict[str, tuple[object, str, str]] = {}
    publications: dict[str, tuple[object, dict[str, object], str]] = {}
    for event in load_events(outcomes):
        event_type = event["eventType"]
        if event_type == "publication_acknowledged":
            packet_id = str(event["packetId"])
            if not packet_id.startswith("legacy:"):
                continue
            row_hash = packet_id[len("legacy:"):]
            payload = event["payload"]
            assert isinstance(payload, dict)
            timestamp = parse_timestamp(event["recordedAt"], "recordedAt")
            event_hash = str(event["eventSha256"])
            prior_publication = publications.get(row_hash)
            if (
                prior_publication is not None
                and timestamp == prior_publication[0]
                and payload != prior_publication[1]
            ):
                raise ValueError("conflicting publication fields at the same timestamp")
            if prior_publication is None or (timestamp, event_hash) > (
                prior_publication[0], prior_publication[2]
            ):
                publications[row_hash] = (timestamp, payload, event_hash)
            continue
        if event_type != "historical_status":
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
    evidence: dict[str, dict[str, object]] = {
        row_hash: {"status": value[1]} for row_hash, value in selected.items()
    }
    for row_hash, (_, payload, _) in publications.items():
        governed = evidence.setdefault(row_hash, {})
        governed["publicUrl"] = payload["publicationUrl"]
        if "finalText" in payload:
            governed["finalText"] = payload["finalText"]
    return evidence


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


def _require_hash(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in _HASH_CHARS for character in value)
    ):
        raise ValueError("{} must be 64 lowercase hexadecimal characters".format(label))
    return value


def corpus_run_id(source_sha256: str, generated_at: str) -> str:
    """Derive the immutable audit-run identity shared across the human gate."""

    _require_hash(source_sha256, "sourceSha256")
    parse_timestamp(generated_at, "generatedAt")
    return sha256_hex(
        canonical_bytes(
            {
                "schemaVersion": "linkedin-corpus-run.v1",
                "generatedAt": generated_at,
                "sourceSha256": source_sha256,
            }
        )
    )


def validate_corpus_authority_manifest(
    value: object,
    *,
    expected_run_id: str,
    generated_at: str,
    expected_manifest_sha256: Optional[str] = None,
) -> dict[str, object]:
    """Validate one independently supplied, canonical corpus authority manifest."""

    if not isinstance(value, dict) or set(value) != _MANIFEST_FIELDS:
        raise ValueError("corpusAuthorityManifest fields are not closed")
    manifest: dict[str, object] = value
    if manifest["schemaVersion"] != "linkedin-corpus-authority-manifest.v1":
        raise ValueError("unsupported corpusAuthorityManifest schemaVersion")
    if (
        _require_hash(manifest["runId"], "corpusAuthorityManifest.runId")
        != expected_run_id
    ):
        raise ValueError("corpusAuthorityManifest runId mismatch")
    validated_at = parse_timestamp(
        manifest["validatedAt"], "corpusAuthorityManifest.validatedAt"
    )
    if validated_at < parse_timestamp(generated_at, "generatedAt"):
        raise ValueError("corpusAuthorityManifest validatedAt predates audit")
    allowlist = manifest["receiptSha256Allowlist"]
    if not isinstance(allowlist, list):
        raise ValueError("corpusAuthorityManifest receipt allowlist must be a list")
    checked_allowlist = [
        _require_hash(item, "corpusAuthorityManifest receipt SHA-256")
        for item in allowlist
    ]
    if checked_allowlist != sorted(set(checked_allowlist)):
        raise ValueError(
            "corpusAuthorityManifest receipt allowlist must be sorted and unique"
        )
    authority_hash = _require_hash(
        manifest["humanGateAuthorityReceiptSha256"],
        "humanGateAuthorityReceiptSha256",
    )
    prefix_hash = _require_hash(
        manifest["ledgerPrefixSha256"], "corpusAuthorityManifest.ledgerPrefixSha256"
    )
    position = manifest["ledgerPosition"]
    if not isinstance(position, int) or isinstance(position, bool) or position < 0:
        raise ValueError("corpusAuthorityManifest ledgerPosition must be non-negative")
    zero = "0" * 64
    provenance_present = (
        authority_hash != zero,
        prefix_hash != zero,
        position != 0,
    )
    if checked_allowlist:
        if not all(provenance_present):
            raise ValueError("populated corpusAuthorityManifest has empty provenance")
        if position < len(checked_allowlist):
            raise ValueError("corpusAuthorityManifest ledgerPosition is incomplete")
    elif any(provenance_present) and not all(provenance_present):
        raise ValueError("empty authority allowlist has mixed human-gate provenance")
    has_human_gate_provenance = all(provenance_present)
    provided_hash = _require_hash(
        manifest["manifestSha256"], "corpusAuthorityManifest.manifestSha256"
    )
    unhashed = {
        key: item for key, item in manifest.items() if key != "manifestSha256"
    }
    if provided_hash != sha256_hex(canonical_bytes(unhashed)):
        raise ValueError("corpusAuthorityManifest manifestSha256 mismatch")
    if checked_allowlist or has_human_gate_provenance:
        if expected_manifest_sha256 is None:
            raise ValueError(
                "populated corpusAuthorityManifest requires expected_manifest_sha256"
            )
        expected_hash = _require_hash(
            expected_manifest_sha256, "expected_manifest_sha256"
        )
        if expected_hash != provided_hash:
            raise ValueError("expected manifest digest mismatch")
    elif expected_manifest_sha256 is not None:
        expected_hash = _require_hash(
            expected_manifest_sha256, "expected_manifest_sha256"
        )
        if expected_hash != provided_hash:
            raise ValueError("expected manifest digest mismatch")
    return manifest


def _empty_corpus_authority_manifest(
    *, run_id: str, generated_at: str
) -> dict[str, object]:
    manifest: dict[str, object] = {
        "schemaVersion": "linkedin-corpus-authority-manifest.v1",
        "runId": run_id,
        "validatedAt": generated_at,
        "receiptSha256Allowlist": [],
        "humanGateAuthorityReceiptSha256": "0" * 64,
        "ledgerPrefixSha256": "0" * 64,
        "ledgerPosition": 0,
    }
    manifest["manifestSha256"] = sha256_hex(canonical_bytes(manifest))
    return manifest


def expected_recovery_items(
    records: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return the one canonical bounded recovery queue for Task 3 and consumers."""

    candidates: list[tuple[bool, str, str, dict[str, object]]] = []
    for record in records:
        raw_posted = record.get("rawPosted")
        if not isinstance(raw_posted, bool):
            raise ValueError("audit record rawPosted must be boolean")
        missing = record.get("missing")
        if not isinstance(missing, list):
            raise ValueError("audit record missing must be a list")
        status = record.get("status")
        required = raw_posted and bool(missing)
        if required or status == "status_unknown":
            candidates.append(
                (
                    required,
                    str(record["date"]),
                    str(record["legacyRowSha256"]),
                    record,
                )
            )
    required_rows = sorted(
        (candidate for candidate in candidates if candidate[0]),
        key=lambda item: (item[1], item[2]),
        reverse=True,
    )
    unknown_rows = sorted(
        (candidate for candidate in candidates if not candidate[0]),
        key=lambda item: (item[1], item[2]),
        reverse=True,
    )
    recent_unknown: list[tuple[bool, str, str, dict[str, object]]] = []
    recent_unknown_hashes: set[str] = set()
    for candidate in unknown_rows:
        if candidate[2] in recent_unknown_hashes:
            continue
        recent_unknown_hashes.add(candidate[2])
        recent_unknown.append(candidate)
        if len(recent_unknown) == 20:
            break
    items: list[dict[str, object]] = []
    seen: set[str] = set()
    for _, _, row_hash, record in required_rows + recent_unknown:
        if row_hash in seen:
            continue
        seen.add(row_hash)
        items.append(
            {
                "allowedAnswers": _allowed_answers(),
                "date": record["date"],
                "legacyRowSha256": row_hash,
                "topic": record["topic"],
            }
        )
    return items


def audit_legacy_rows(
    posted_log: Path,
    outcomes: Optional[Path],
    generated_at: str,
    corpus_authority_manifest: Optional[dict[str, object]] = None,
    expected_manifest_sha256: Optional[str] = None,
) -> dict[str, object]:
    """Classify LinkedIn rows without mutating or over-interpreting legacy data."""

    parse_timestamp(generated_at, "generated_at")
    source_before = posted_log.read_bytes()
    rows = read_jsonl_bytes(source_before, str(posted_log))
    governed = _governed_evidence(outcomes)

    records: list[dict[str, object]] = []
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
        governed_row = governed.get(row_hash, {})
        public_url = governed_row.get("publicUrl") or _public_url(row)
        final_text = governed_row.get("finalText") or _final_text(row)
        raw_posted = row.get("posted") is True

        status = governed_row.get("status")
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
            "rawPosted": raw_posted,
            "status": status,
            "topic": topic,
        }
        records.append(record)

    source_after = posted_log.read_bytes()
    if source_after != source_before:
        raise RuntimeError("posted log changed during audit")

    duplicate_groups = [
        {"legacyRowSha256": row_hash, "count": count}
        for row_hash, count in sorted(Counter(row_hashes).items())
        if count > 1
    ]
    status_counts = Counter(str(record["status"]) for record in records)

    recovery_items = expected_recovery_items(records)
    source_sha256 = sha256_hex(source_before)
    run_id = corpus_run_id(source_sha256, generated_at)
    manifest = (
        _empty_corpus_authority_manifest(run_id=run_id, generated_at=generated_at)
        if corpus_authority_manifest is None
        else corpus_authority_manifest
    )
    validate_corpus_authority_manifest(
        manifest,
        expected_run_id=run_id,
        generated_at=generated_at,
        expected_manifest_sha256=expected_manifest_sha256,
    )
    zero = "0" * 64
    if (
        manifest["receiptSha256Allowlist"] == []
        and manifest["humanGateAuthorityReceiptSha256"] != zero
    ):
        governed_statuses = [
            value.get("status") for value in governed.values() if "status" in value
        ]
        if not governed_statuses or any(
            status != "status_unknown" for status in governed_statuses
        ):
            raise ValueError(
                "empty authority allowlist requires all status_unknown "
                "human-gate answers"
            )

    return {
        "schemaVersion": "linkedin-historical-audit.v1",
        "generatedAt": generated_at,
        "sourceSha256": source_sha256,
        "statusCounts": {status: status_counts.get(status, 0) for status in _STATUSES},
        "missingFieldCounts": dict(sorted(missing_counts.items())),
        "duplicateGroups": duplicate_groups,
        "records": records,
        "corpusAuthorityManifest": manifest,
        "recoveryRequest": {
            "schemaVersion": "linkedin-historical-recovery-request.v1",
            "generatedAt": generated_at,
            "sourceSha256": source_sha256,
            "items": recovery_items,
        },
    }


__all__ = [
    "audit_legacy_rows",
    "corpus_run_id",
    "expected_recovery_items",
    "validate_corpus_authority_manifest",
]
