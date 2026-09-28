"""Derive a strict LinkedIn voice corpus from governed exact-text outcomes."""

from __future__ import annotations

import re
from collections import Counter
from typing import Optional
from urllib.parse import unquote, urlsplit

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import (
    CORPUS_AUTHORITY_SOURCE_TYPE,
    HISTORICAL_STATUS,
    parse_timestamp,
    validate_event,
    validate_linkedin_url,
)
from scripts.linkedin_content_os.historical_audit import (
    corpus_run_id,
    expected_recovery_items,
    validate_corpus_authority_manifest,
)
from scripts.linkedin_content_os.outcomes import validate_event_sequence


_AUDIT_FIELDS = {
    "schemaVersion",
    "generatedAt",
    "sourceSha256",
    "statusCounts",
    "missingFieldCounts",
    "duplicateGroups",
    "records",
    "corpusAuthorityManifest",
    "recoveryRequest",
}
_AUDIT_RECORD_FIELDS = {
    "date",
    "legacyRowSha256",
    "missing",
    "rawPosted",
    "status",
    "topic",
}
_RECOVERY_FIELDS = {"schemaVersion", "generatedAt", "sourceSha256", "items"}
_RECOVERY_ITEM_FIELDS = {
    "allowedAnswers",
    "date",
    "legacyRowSha256",
    "topic",
}
_PLACEHOLDER_MARKERS = {
    "draft",
    "example",
    "fake",
    "placeholder",
    "sample",
    "temp",
    "test",
    "todo",
    "unknown",
}
_HASH_LENGTH = 64
_ALLOWED_RECOVERY_ANSWERS = [
    {"answer": "posted", "required": ["publicUrl"], "optional": ["finalText"]},
    {
        "answer": "not_posted",
        "required": ["declineReason"],
        "allowedDeclineReasons": ["quality_fit", "stale", "timing", "other"],
    },
    {"answer": "still_unknown", "required": []},
]
_EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_PHONE = re.compile(
    r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s])\d{3}[-.\s]\d{4}(?!\d)"
)
_CREDENTIAL = re.compile(
    r"(?i)(?:\bBearer\s+[A-Za-z0-9._~+/-]{12,}|\bsk-[A-Za-z0-9_-]{12,}|"
    r"(?:api[_ -]?key|access[_ -]?token|private[_ -]?key)\s*[:=]\s*\S{8,})"
)
_PRIVATE_MARKER = re.compile(
    r"(?i)(?:\[PRIVATE\]|\bCONFIDENTIAL\b|\bINTERNAL ONLY\b)"
)


def _require_object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("{} must be an object".format(label))
    return value


def _require_hash(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != _HASH_LENGTH
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("{} must be 64 lowercase hexadecimal characters".format(label))
    return value


def _validate_audit(
    audit_value: object,
) -> tuple[dict[str, object], dict[str, str], dict[str, object]]:
    audit = _require_object(audit_value, "audit")
    if set(audit) != _AUDIT_FIELDS:
        raise ValueError("audit fields do not match linkedin-historical-audit.v1")
    if audit["schemaVersion"] != "linkedin-historical-audit.v1":
        raise ValueError("unsupported audit schemaVersion")
    parse_timestamp(audit["generatedAt"], "audit.generatedAt")
    _require_hash(audit["sourceSha256"], "audit.sourceSha256")

    records_value = audit["records"]
    if not isinstance(records_value, list):
        raise ValueError("audit.records must be a list")
    observed: Counter[str] = Counter()
    observed_missing: Counter[str] = Counter()
    observed_hashes: Counter[str] = Counter()
    statuses_by_hash: dict[str, str] = {}
    identity_by_hash: dict[str, tuple[str, str]] = {}
    for index, raw_record in enumerate(records_value):
        record = _require_object(raw_record, "audit record {}".format(index))
        if set(record) != _AUDIT_RECORD_FIELDS:
            raise ValueError("audit record fields are not closed")
        row_hash = _require_hash(
            record["legacyRowSha256"], "audit.records.legacyRowSha256"
        )
        status = record["status"]
        if status not in HISTORICAL_STATUS:
            raise ValueError("audit record has unsupported status")
        if not isinstance(record["missing"], list) or any(
            not isinstance(item, str) for item in record["missing"]
        ):
            raise ValueError("audit record missing must be a string list")
        if not isinstance(record["rawPosted"], bool):
            raise ValueError("audit record rawPosted must be boolean")
        for field in ("date", "topic"):
            if not isinstance(record[field], str) or not record[field].strip():
                raise ValueError("audit record {} must be non-empty text".format(field))
        prior = statuses_by_hash.get(row_hash)
        if prior is not None and prior != status:
            raise ValueError("duplicate audit row hash has conflicting statuses")
        statuses_by_hash[row_hash] = str(status)
        identity = (str(record["date"]), str(record["topic"]))
        prior_identity = identity_by_hash.get(row_hash)
        if prior_identity is not None and prior_identity != identity:
            raise ValueError("duplicate audit row hash has conflicting identity")
        identity_by_hash[row_hash] = identity
        observed[str(status)] += 1
        observed_hashes[row_hash] += 1
        observed_missing.update(str(item) for item in record["missing"])

    status_counts = _require_object(audit["statusCounts"], "audit.statusCounts")
    if set(status_counts) != HISTORICAL_STATUS:
        raise ValueError("audit.statusCounts fields are not closed")
    for status in sorted(HISTORICAL_STATUS):
        count = status_counts[status]
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("audit.statusCounts values must be non-negative integers")
        if count != observed[status]:
            raise ValueError("audit.statusCounts does not match records")

    missing_counts = _require_object(
        audit["missingFieldCounts"], "audit.missingFieldCounts"
    )
    for field, count in missing_counts.items():
        if not isinstance(field, str) or not field:
            raise ValueError("audit.missingFieldCounts keys must be non-empty strings")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError(
                "audit.missingFieldCounts values must be non-negative integers"
            )
    if dict(sorted(missing_counts.items())) != dict(sorted(observed_missing.items())):
        raise ValueError("audit.missingFieldCounts does not match records")

    duplicate_groups = audit["duplicateGroups"]
    if not isinstance(duplicate_groups, list):
        raise ValueError("audit.duplicateGroups must be a list")
    expected_duplicates = [
        {"legacyRowSha256": row_hash, "count": count}
        for row_hash, count in sorted(observed_hashes.items())
        if count > 1
    ]
    if duplicate_groups != expected_duplicates:
        raise ValueError("audit.duplicateGroups does not match records")

    recovery = _require_object(audit["recoveryRequest"], "audit.recoveryRequest")
    if set(recovery) != _RECOVERY_FIELDS:
        raise ValueError("audit.recoveryRequest fields are not closed")
    if recovery["schemaVersion"] != "linkedin-historical-recovery-request.v1":
        raise ValueError("unsupported audit.recoveryRequest schemaVersion")
    if recovery["generatedAt"] != audit["generatedAt"]:
        raise ValueError("audit.recoveryRequest generatedAt mismatch")
    if recovery["sourceSha256"] != audit["sourceSha256"]:
        raise ValueError("audit.recoveryRequest sourceSha256 mismatch")
    recovery_items = recovery["items"]
    if not isinstance(recovery_items, list):
        raise ValueError("audit.recoveryRequest items must be a list")
    seen_recovery: set[str] = set()
    for raw_item in recovery_items:
        item = _require_object(raw_item, "audit.recoveryRequest item")
        if set(item) != _RECOVERY_ITEM_FIELDS:
            raise ValueError("audit.recoveryRequest item fields are not closed")
        row_hash = _require_hash(
            item["legacyRowSha256"], "audit.recoveryRequest legacyRowSha256"
        )
        if row_hash in seen_recovery:
            raise ValueError("audit.recoveryRequest has duplicate row hash")
        seen_recovery.add(row_hash)
        if identity_by_hash.get(row_hash) != (item["date"], item["topic"]):
            raise ValueError("audit.recoveryRequest item is not bound to an audit row")
        answers = item["allowedAnswers"]
        if answers != _ALLOWED_RECOVERY_ANSWERS:
            raise ValueError("audit.recoveryRequest allowedAnswers are not closed")
    expected_items = expected_recovery_items(records_value)
    if recovery_items != expected_items:
        raise ValueError("audit.recoveryRequest is not complete for corpus consumption")
    expected_run_id = corpus_run_id(
        str(audit["sourceSha256"]), str(audit["generatedAt"])
    )
    manifest = validate_corpus_authority_manifest(
        audit["corpusAuthorityManifest"],
        expected_run_id=expected_run_id,
        generated_at=str(audit["generatedAt"]),
    )
    return audit, statuses_by_hash, manifest


def _validated_events(
    events_value: object,
    manifest: Optional[dict[str, object]] = None,
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    if not isinstance(events_value, list):
        raise ValueError("events must be a list")
    events: list[dict[str, object]] = []
    seen_ids: dict[str, str] = {}
    for raw_event in events_value:
        event = validate_event(raw_event)
        event_id = str(event["outcomeEventId"])
        event_hash = str(event["eventSha256"])
        prior = seen_ids.get(event_id)
        if prior is not None:
            raise ValueError("duplicate outcomeEventId in corpus input")
        seen_ids[event_id] = event_hash
        events.append(event)
    validate_event_sequence(events)
    receipt_events = [
        event for event in events if event["eventType"] == "corpus_authority_receipt"
    ]
    if receipt_events and manifest is None:
        raise ValueError("corpus authority receipt requires an independent manifest")
    if manifest is not None:
        allowlist = manifest["receiptSha256Allowlist"]
        assert isinstance(allowlist, list)
        observed_receipts = sorted(str(event["eventSha256"]) for event in receipt_events)
        if observed_receipts != allowlist:
            raise ValueError("corpus authority receipt allowlist mismatch")
        position = int(manifest["ledgerPosition"])
        if position > len(events):
            raise ValueError("corpus authority manifest ledger position is invalid")
        if position:
            prefix = b"".join(
                canonical_bytes(event) + b"\n" for event in events[:position]
            )
            if manifest["ledgerPrefixSha256"] != sha256_hex(prefix):
                raise ValueError("corpus authority manifest ledger prefix mismatch")
            if any(events.index(receipt) + 1 > position for receipt in receipt_events):
                raise ValueError("corpus authority receipt falls outside manifest prefix")
    by_id_in_ledger = {str(event["outcomeEventId"]): event for event in events}
    receipts: dict[str, dict[str, object]] = {}
    for index, receipt in enumerate(events):
        if receipt["eventType"] != "corpus_authority_receipt":
            continue
        payload = _require_object(receipt["payload"], "authority receipt payload")
        assert manifest is not None
        if (
            payload["runId"] != manifest["runId"]
            or payload["rawAuthoritySha256"]
            != manifest["humanGateAuthorityReceiptSha256"]
        ):
            raise ValueError("authority receipt run or human-gate provenance mismatch")
        if parse_timestamp(
            manifest["validatedAt"], "corpusAuthorityManifest.validatedAt"
        ) < parse_timestamp(payload["validatedAt"], "validatedAt"):
            raise ValueError("corpus authority manifest predates receipt validation")
        position = int(payload["ledgerPosition"])
        if position > index or position > len(events):
            raise ValueError("authority receipt ledger position is invalid")
        target = events[position - 1]
        target_id = str(payload["textOutcomeEventId"])
        if by_id_in_ledger.get(target_id) is not target:
            raise ValueError("authority receipt text event position does not match")
        prefix = b"".join(canonical_bytes(event) + b"\n" for event in events[:position])
        if payload["ledgerPrefixSha256"] != sha256_hex(prefix):
            raise ValueError("authority receipt ledger prefix does not match")
        source = _require_object(target["sourcePointer"], "text sourcePointer")
        if (
            payload["textOutcomeEventSha256"] != target["eventSha256"]
            or payload["authoritySourceType"] != source["sourceType"]
            or payload["authoritySourceId"] != source["sourceId"]
            or payload["authoritySourceSha256"] != source["sourceSha256"]
            or receipt["packetId"] != target["packetId"]
        ):
            raise ValueError("authority receipt is not bound to exact text provenance")
        if source["sourceType"] not in CORPUS_AUTHORITY_SOURCE_TYPE:
            raise ValueError("authority receipt source type is not trusted")
        if parse_timestamp(receipt["recordedAt"], "recordedAt") < parse_timestamp(
            target["recordedAt"], "recordedAt"
        ) or parse_timestamp(payload["validatedAt"], "validatedAt") < parse_timestamp(
            target["recordedAt"], "recordedAt"
        ):
            raise ValueError("authority receipt validation predates text event")
        if target_id in receipts:
            raise ValueError("duplicate authority receipt for text event")
        receipts[target_id] = receipt

    ordered = sorted(
        events,
        key=lambda event: (
            parse_timestamp(event["recordedAt"], "recordedAt"),
            str(event["eventSha256"]),
        ),
    )
    by_id = {str(event["outcomeEventId"]): event for event in ordered}
    by_hash = {str(event["eventSha256"]): event for event in ordered}
    superseded: dict[str, str] = {}
    for correction in ordered:
        if correction["eventType"] != "correction":
            continue
        payload = _require_object(correction["payload"], "correction payload")
        target_id = str(payload["targetOutcomeEventId"])
        replacement_hash = str(payload["replacementEventSha256"])
        target = by_id.get(target_id)
        replacement = by_hash.get(replacement_hash)
        if target is None or replacement is None:
            raise ValueError("correction target and replacement must both be present")
        if (
            target["packetId"] != correction["packetId"]
            or replacement["packetId"] != correction["packetId"]
        ):
            raise ValueError("correction target and replacement must share packetId")
        superseded[target_id] = replacement_hash
    active = [
        event
        for event in ordered
        if str(event["outcomeEventId"]) not in superseded
        and event["eventType"] not in {"correction", "corpus_authority_receipt"}
    ]
    active_ids = {str(event["outcomeEventId"]) for event in active}
    return active, {
        event_id: receipt
        for event_id, receipt in receipts.items()
        if event_id in active_ids
    }


def _is_placeholder_url(value: object) -> bool:
    try:
        url = validate_linkedin_url(value)
    except ValueError:
        return True
    lowered = unquote(urlsplit(url).path).lower()
    tokens = {token for token in re.split(r"[^a-z0-9]+", lowered) if token}
    return bool(tokens & _PLACEHOLDER_MARKERS)


def _exact_text(
    event: dict[str, object], receipts: dict[str, dict[str, object]]
) -> Optional[tuple[str, str]]:
    if str(event["outcomeEventId"]) not in receipts:
        return None
    payload = _require_object(event["payload"], "payload")
    text = payload.get("finalText")
    digest = payload.get("finalTextSha256")
    if not isinstance(text, str) or not text.strip() or not isinstance(digest, str):
        return None
    if sha256_hex(text.encode("utf-8")) != digest:
        # validate_event normally catches this. Keep the local invariant explicit.
        raise ValueError("finalTextSha256 does not match exact final text")
    return text, digest


def _privacy_reasons(texts: list[str], receipt: dict[str, object]) -> list[str]:
    payload = _require_object(receipt["payload"], "authority receipt payload")
    markers = payload["clientSensitiveMarkers"]
    assert isinstance(markers, list)
    reasons: set[str] = set()
    combined = "\n".join(texts)
    if _CREDENTIAL.search(combined):
        reasons.add("credential")
    if _EMAIL.search(combined):
        reasons.add("email")
    if _PHONE.search(combined):
        reasons.add("phone")
    if _PRIVATE_MARKER.search(combined):
        reasons.add("private_marker")
    lowered = combined.casefold()
    if any(str(marker).casefold() in lowered for marker in markers):
        reasons.add("client_sensitive_marker")
    return sorted(reasons)


def _quarantine(event: dict[str, object], reasons: list[str]) -> dict[str, object]:
    return {
        "schemaVersion": "linkedin-corpus-quarantine.v0",
        "recordType": "quarantine",
        "packetId": event["packetId"],
        "textOutcomeEventId": event["outcomeEventId"],
        "textOutcomeEventSha256": event["eventSha256"],
        "reasons": reasons,
    }


def _validate_capture_bindings(events: list[dict[str, object]]) -> None:
    by_id = {str(event["outcomeEventId"]): event for event in events}
    for capture in events:
        if capture["eventType"] != "final_text_captured":
            continue
        payload = _require_object(capture["payload"], "final text payload")
        publication = by_id.get(str(payload["publicationOutcomeEventId"]))
        if publication is None or publication["eventType"] != "publication_acknowledged":
            raise ValueError("final text capture publication outcome does not exist")
        if publication["eventSha256"] != payload["publicationOutcomeEventSha256"]:
            raise ValueError("final text capture publication outcome hash does not match")
        if publication["packetId"] != capture["packetId"]:
            raise ValueError("final text capture and publication must share same packet")
        if parse_timestamp(capture["recordedAt"], "recordedAt") < parse_timestamp(
            publication["recordedAt"], "recordedAt"
        ):
            raise ValueError("final text capture recordedAt predates publication")
        publication_payload = _require_object(
            publication["payload"], "publication payload"
        )
        url = str(publication_payload["publicationUrl"])
        if sha256_hex(url.encode("utf-8")) != payload["publicationUrlSha256"]:
            raise ValueError("final text capture publication URL does not match")


def _gap_summary(packet_ids: set[str]) -> dict[str, object]:
    return {
        "schemaVersion": "linkedin-corpus-gap-summary.v0",
        "recordType": "gap_summary",
        "blockingGapCount": len(packet_ids),
        "blockingGapPacketIds": sorted(packet_ids),
    }


def build_voice_gold(
    audit: dict[str, object], events: list[dict[str, object]]
) -> list[dict[str, object]]:
    """Return exact JT-final text records plus one deterministic gap summary.

    Legacy prose is identity/status evidence only. Text can enter the corpus only
    through a validated governed event tied to a confirmed published row.
    """

    _, statuses_by_hash, manifest = _validate_audit(audit)
    ordered_events, receipts = _validated_events(events, manifest)
    _validate_capture_bindings(ordered_events)
    publications: dict[str, list[dict[str, object]]] = {}
    captures: dict[str, list[dict[str, object]]] = {}
    for event in ordered_events:
        packet_id = str(event["packetId"])
        if event["eventType"] == "publication_acknowledged":
            publications.setdefault(packet_id, []).append(event)
        elif event["eventType"] == "final_text_captured":
            captures.setdefault(packet_id, []).append(event)

    candidates: list[tuple[object, str, dict[str, object]]] = []
    gaps: set[str] = set()
    for row_hash, status in sorted(statuses_by_hash.items()):
        if status != "posted_confirmed":
            continue
        packet_id = "legacy:{}".format(row_hash)
        valid_publications = [
            event
            for event in publications.get(packet_id, [])
            if not _is_placeholder_url(
                _require_object(event["payload"], "payload").get("publicationUrl")
            )
        ]
        if not valid_publications:
            gaps.add(packet_id)
            continue
        inline_publications = [
            event
            for event in valid_publications
            if _exact_text(event, receipts) is not None
        ]
        if inline_publications:
            publication = inline_publications[-1]
            text_event = publication
            exact = _exact_text(publication, receipts)
            origin = "jt_published"
        else:
            valid_captures = [
                event for event in captures.get(packet_id, [])
                if _exact_text(event, receipts) is not None
            ]
            if not valid_captures:
                gaps.add(packet_id)
                continue
            text_event = valid_captures[-1]
            capture_payload = _require_object(text_event["payload"], "capture payload")
            publication_id = str(capture_payload["publicationOutcomeEventId"])
            publication = next(
                event for event in valid_publications
                if event["outcomeEventId"] == publication_id
            )
            exact = _exact_text(text_event, receipts)
            assert exact is not None
            source = _require_object(text_event["sourcePointer"], "sourcePointer")
            origin = (
                "jt_authored"
                if source["sourceType"] == "jt_authored_text"
                else "jt_published"
            )
        text, text_hash = exact
        receipt = receipts[str(text_event["outcomeEventId"])]
        privacy = _privacy_reasons([text], receipt)
        if privacy:
            candidates.append(
                (
                    parse_timestamp(text_event["recordedAt"], "recordedAt"),
                    str(text_event["eventSha256"]),
                    _quarantine(text_event, privacy),
                )
            )
            gaps.add(packet_id)
            continue
        source_pointer = _require_object(text_event["sourcePointer"], "sourcePointer")
        record = {
            "schemaVersion": "linkedin-voice-gold.v0",
            "recordType": "voice_gold",
            "origin": origin,
            "packetId": packet_id,
            "legacyRowSha256": row_hash,
            "publicationOutcomeEventId": publication["outcomeEventId"],
            "publicationOutcomeEventSha256": publication["eventSha256"],
            "textOutcomeEventId": text_event["outcomeEventId"],
            "textOutcomeEventSha256": text_event["eventSha256"],
            "text": text,
            "textSha256": text_hash,
            "sourcePointer": dict(source_pointer),
        }
        candidates.append(
            (
                parse_timestamp(text_event["recordedAt"], "recordedAt"),
                str(text_event["eventSha256"]),
                record,
            )
        )

    selected: list[dict[str, object]] = []
    seen_text_hashes: set[str] = set()
    for _, _, record in sorted(candidates, key=lambda item: (item[0], item[1])):
        if record["recordType"] == "quarantine":
            selected.append(record)
            continue
        text_hash = str(record["textSha256"])
        if text_hash in seen_text_hashes:
            continue
        seen_text_hashes.add(text_hash)
        selected.append(record)
    selected.sort(
        key=lambda record: (
            0 if record["recordType"] == "quarantine" else 1,
            str(record.get("textSha256", record.get("textOutcomeEventSha256", ""))),
            str(record["packetId"]),
        )
    )
    selected.append(_gap_summary(gaps))
    return selected


def build_contrastive_pairs(
    events: list[dict[str, object]],
    audit: Optional[dict[str, object]] = None,
) -> list[dict[str, object]]:
    """Return exact governed JT edit pairs plus deterministic blocking gaps."""

    manifest = _validate_audit(audit)[2] if audit is not None else None
    ordered_events, receipts = _validated_events(events, manifest)
    _validate_capture_bindings(ordered_events)
    packets_with_final_text: set[str] = set()
    packets_with_pair: set[str] = set()
    candidates: list[tuple[object, str, dict[str, object]]] = []
    for event in ordered_events:
        if event["eventType"] not in {
            "publication_acknowledged",
            "final_text_captured",
        }:
            continue
        payload = _require_object(event["payload"], "payload")
        if "finalText" in payload:
            packets_with_final_text.add(str(event["packetId"]))
        exact = _exact_text(event, receipts)
        if exact is None:
            continue
        packet_id = str(event["packetId"])
        if event["eventType"] != "final_text_captured":
            continue
        if not {"draftText", "draftTextSha256", "editReason"} <= set(payload):
            continue
        receipt = receipts[str(event["outcomeEventId"])]
        privacy = _privacy_reasons(
            [str(payload["draftText"]), str(payload["finalText"])], receipt
        )
        if privacy:
            candidates.append(
                (
                    parse_timestamp(event["recordedAt"], "recordedAt"),
                    str(event["eventSha256"]),
                    _quarantine(event, privacy),
                )
            )
            continue
        packets_with_pair.add(packet_id)
        source_pointer = _require_object(event["sourcePointer"], "sourcePointer")
        record = {
            "schemaVersion": "linkedin-contrastive-pair.v0",
            "recordType": "contrastive_pair",
            "origin": "jt_edit_pair",
            "packetId": packet_id,
            "outcomeEventId": event["outcomeEventId"],
            "outcomeEventSha256": event["eventSha256"],
            "draftText": payload["draftText"],
            "draftTextSha256": payload["draftTextSha256"],
            "finalText": payload["finalText"],
            "finalTextSha256": payload["finalTextSha256"],
            "editReason": payload["editReason"],
            "sourcePointer": dict(source_pointer),
        }
        candidates.append(
            (
                parse_timestamp(event["recordedAt"], "recordedAt"),
                str(event["eventSha256"]),
                record,
            )
        )

    selected: list[dict[str, object]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for _, _, record in sorted(candidates, key=lambda item: (item[0], item[1])):
        if record["recordType"] == "quarantine":
            selected.append(record)
            continue
        pair_key = (
            str(record["draftTextSha256"]),
            str(record["finalTextSha256"]),
        )
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        selected.append(record)
    selected.sort(
        key=lambda record: (
            0 if record["recordType"] == "quarantine" else 1,
            str(
                record.get(
                    "draftTextSha256", record.get("textOutcomeEventSha256", "")
                )
            ),
            str(record.get("finalTextSha256", "")),
            str(record["packetId"]),
        )
    )
    selected.append(_gap_summary(packets_with_final_text - packets_with_pair))
    return selected


__all__ = ["build_contrastive_pairs", "build_voice_gold"]
