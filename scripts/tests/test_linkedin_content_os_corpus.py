import unittest
from typing import Optional

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.corpus import (
    build_contrastive_pairs,
    build_voice_gold,
)


def _audit(*records: dict[str, object]) -> dict[str, object]:
    statuses = {
        "not_posted_confirmed": 0,
        "posted_confirmed": 0,
        "status_unknown": 0,
    }
    for record in records:
        statuses[str(record["status"])] += 1
    missing_counts: dict[str, int] = {}
    row_counts: dict[str, int] = {}
    for record in records:
        for field in record["missing"]:
            missing_counts[str(field)] = missing_counts.get(str(field), 0) + 1
        row_hash = str(record["legacyRowSha256"])
        row_counts[row_hash] = row_counts.get(row_hash, 0) + 1
    return {
        "schemaVersion": "linkedin-historical-audit.v1",
        "generatedAt": "2026-09-28T12:00:00-04:00",
        "sourceSha256": "a" * 64,
        "statusCounts": statuses,
        "missingFieldCounts": dict(sorted(missing_counts.items())),
        "duplicateGroups": [
            {"legacyRowSha256": row_hash, "count": count}
            for row_hash, count in sorted(row_counts.items())
            if count > 1
        ],
        "records": list(records),
        "recoveryRequest": {
            "schemaVersion": "linkedin-historical-recovery-request.v1",
            "generatedAt": "2026-09-28T12:00:00-04:00",
            "sourceSha256": "a" * 64,
            "items": [
                {
                    "allowedAnswers": [
                        {
                            "answer": "posted",
                            "required": ["publicUrl"],
                            "optional": ["finalText"],
                        },
                        {
                            "answer": "not_posted",
                            "required": ["declineReason"],
                            "allowedDeclineReasons": [
                                "quality_fit",
                                "stale",
                                "timing",
                                "other",
                            ],
                        },
                        {"answer": "still_unknown", "required": []},
                    ],
                    "date": record["date"],
                    "legacyRowSha256": record["legacyRowSha256"],
                    "topic": record["topic"],
                }
                for record in records
                if record["status"] == "posted_confirmed" and record["missing"]
            ],
        },
    }


def _record(row_hash: str, status: str = "posted_confirmed") -> dict[str, object]:
    return {
        "date": "2026-09-01",
        "legacyRowSha256": row_hash,
        "missing": ["final_text"],
        "status": status,
        "topic": "Bound topic",
    }


def _event(
    event_id: str,
    packet_id: str,
    event_type: str,
    payload: dict[str, object],
    *,
    recorded_at: str = "2026-09-28T12:00:00-04:00",
    source_type: str = "jt_human_gate_response",
    source_id: str = "telegram:27993",
    source_sha256: str = "b" * 64,
) -> dict[str, object]:
    event: dict[str, object] = {
        "schemaVersion": "linkedin-content-outcome.v1",
        "outcomeEventId": event_id,
        "packetId": packet_id,
        "eventType": event_type,
        "recordedAt": recorded_at,
        "sourcePointer": {
            "sourceType": source_type,
            "sourceId": source_id,
            "sourceSha256": source_sha256,
        },
        "payload": payload,
    }
    event["eventSha256"] = sha256_hex(canonical_bytes(event))
    return event


def _publication(
    row_hash: str,
    text: str,
    *,
    event_id: str = "published-001",
    url: str = "https://www.linkedin.com/posts/jt_exact-1",
    source_type: str = "jt_human_gate_response",
    recorded_at: str = "2026-09-28T12:00:00-04:00",
) -> dict[str, object]:
    return _event(
        event_id,
        "legacy:{}".format(row_hash),
        "publication_acknowledged",
        {
            "publicationUrl": url,
            "finalText": text,
            "finalTextSha256": sha256_hex(text.encode("utf-8")),
        },
        recorded_at=recorded_at,
        source_type=source_type,
    )


def _publication_without_text(
    row_hash: str,
    *,
    event_id: str = "published-binding",
    recorded_at: str = "2026-09-28T12:00:00-04:00",
    url: str = "https://www.linkedin.com/posts/jt_bound-1",
) -> dict[str, object]:
    return _event(
        event_id,
        "legacy:{}".format(row_hash),
        "publication_acknowledged",
        {"publicationUrl": url},
        recorded_at=recorded_at,
    )


def _capture_payload(
    publication: dict[str, object],
    final: str,
    *,
    draft: Optional[str] = None,
    reason: str = "specificity",
) -> dict[str, object]:
    publication_payload = publication["payload"]
    assert isinstance(publication_payload, dict)
    url = str(publication_payload["publicationUrl"])
    payload: dict[str, object] = {
        "finalText": final,
        "finalTextSha256": sha256_hex(final.encode("utf-8")),
        "publicationOutcomeEventId": publication["outcomeEventId"],
        "publicationOutcomeEventSha256": publication["eventSha256"],
        "publicationUrlSha256": sha256_hex(url.encode("utf-8")),
    }
    if draft is not None:
        payload.update(
            {
                "draftText": draft,
                "draftTextSha256": sha256_hex(draft.encode("utf-8")),
                "editReason": reason,
            }
        )
    return payload


def _authority_receipt(
    ledger_prefix: list[dict[str, object]],
    target: dict[str, object],
    *,
    event_id: str = "authority-receipt-001",
    recorded_at: str = "2026-09-28T12:02:00-04:00",
    markers: Optional[list[str]] = None,
) -> dict[str, object]:
    position = ledger_prefix.index(target) + 1
    prefix = b"".join(canonical_bytes(event) + b"\n" for event in ledger_prefix[:position])
    source = target["sourcePointer"]
    assert isinstance(source, dict)
    return _event(
        event_id,
        str(target["packetId"]),
        "corpus_authority_receipt",
        {
            "authoritySourceType": source["sourceType"],
            "authoritySourceId": source["sourceId"],
            "authoritySourceSha256": source["sourceSha256"],
            "rawAuthoritySha256": "c" * 64,
            "textOutcomeEventId": target["outcomeEventId"],
            "textOutcomeEventSha256": target["eventSha256"],
            "ledgerPrefixSha256": sha256_hex(prefix),
            "ledgerPosition": position,
            "validatedAt": recorded_at,
            "clientSensitiveMarkers": list(markers or []),
        },
        recorded_at=recorded_at,
        source_type="corpus_authority_verifier",
        source_id="authority:program-0",
        source_sha256="c" * 64,
    )


def _edit_pair_event(
    publication: dict[str, object],
    draft: str,
    final: str,
    *,
    event_id: str = "edit-pair-001",
    recorded_at: str = "2026-09-28T12:01:00-04:00",
    reason: str = "specificity",
    source_type: str = "jt_authored_text",
) -> dict[str, object]:
    return _event(
        event_id,
        str(publication["packetId"]),
        "final_text_captured",
        _capture_payload(publication, final, draft=draft, reason=reason),
        recorded_at=recorded_at,
        source_type=source_type,
    )


class VoiceGoldTests(unittest.TestCase):
    def test_accepts_only_exact_hash_bound_final_published_text(self) -> None:
        row_hash = "1" * 64
        text = "The exact final LinkedIn post, including punctuation."
        event = _publication(row_hash, text)
        receipt = _authority_receipt([event], event)

        rows = build_voice_gold(_audit(_record(row_hash)), [event, receipt])

        self.assertEqual(rows[0], {
            "schemaVersion": "linkedin-voice-gold.v0",
            "recordType": "voice_gold",
            "origin": "jt_published",
            "packetId": "legacy:{}".format(row_hash),
            "legacyRowSha256": row_hash,
            "publicationOutcomeEventId": "published-001",
            "publicationOutcomeEventSha256": event["eventSha256"],
            "textOutcomeEventId": "published-001",
            "textOutcomeEventSha256": event["eventSha256"],
            "text": text,
            "textSha256": sha256_hex(text.encode("utf-8")),
            "sourcePointer": event["sourcePointer"],
        })
        self.assertEqual(rows[-1], {
            "schemaVersion": "linkedin-corpus-gap-summary.v0",
            "recordType": "gap_summary",
            "blockingGapCount": 0,
            "blockingGapPacketIds": [],
        })

    def test_self_asserted_text_event_without_independent_receipt_is_a_gap(self) -> None:
        row_hash = "1" * 64
        event = _publication(row_hash, "Self-asserted exact text.")

        self.assertEqual(build_voice_gold(_audit(_record(row_hash)), [event]), [{
            "schemaVersion": "linkedin-corpus-gap-summary.v0",
            "recordType": "gap_summary",
            "blockingGapCount": 1,
            "blockingGapPacketIds": ["legacy:{}".format(row_hash)],
        }])

    def test_authority_receipt_must_match_event_and_ledger_prefix(self) -> None:
        row_hash = "1" * 64
        event = _publication(row_hash, "Anchored exact text.")
        receipt = _authority_receipt([event], event)
        payload = dict(receipt["payload"])
        payload["ledgerPrefixSha256"] = "0" * 64
        forged_receipt = _event(
            "authority-forged",
            str(receipt["packetId"]),
            "corpus_authority_receipt",
            payload,
            recorded_at="2026-09-28T12:03:00-04:00",
            source_type="corpus_authority_verifier",
            source_id="authority:program-0",
            source_sha256="c" * 64,
        )

        with self.assertRaisesRegex(ValueError, "ledger prefix"):
            build_voice_gold(
                _audit(_record(row_hash)), [event, forged_receipt]
            )

    def test_private_or_secret_exact_text_is_quarantined_without_redaction(self) -> None:
        row_hash = "1" * 64
        text = (
            "[PRIVATE] Client Alpha can reach me at jt@example.com or 212-555-0199. "
            "Bearer sk-secretvalue1234567890"
        )
        event = _publication(row_hash, text)
        receipt = _authority_receipt(
            [event], event, markers=["Client Alpha"]
        )

        rows = build_voice_gold(_audit(_record(row_hash)), [event, receipt])

        self.assertEqual(rows[0], {
            "schemaVersion": "linkedin-corpus-quarantine.v0",
            "recordType": "quarantine",
            "packetId": "legacy:{}".format(row_hash),
            "textOutcomeEventId": event["outcomeEventId"],
            "textOutcomeEventSha256": event["eventSha256"],
            "reasons": [
                "client_sensitive_marker",
                "credential",
                "email",
                "phone",
                "private_marker",
            ],
        })
        self.assertNotIn("text", rows[0])
        self.assertEqual(rows[-1]["blockingGapCount"], 1)

    def test_resolves_separate_exact_final_text_capture_to_publication(self) -> None:
        row_hash = "2" * 64
        text = "JT supplied the exact final text later."
        acknowledged = _publication_without_text(
            row_hash,
            event_id="published-002",
            url="https://linkedin.com/posts/jt_exact-2",
        )
        captured = _event(
            "text-002",
            "legacy:{}".format(row_hash),
            "final_text_captured",
            _capture_payload(acknowledged, text),
            recorded_at="2026-09-28T12:01:00-04:00",
            source_type="jt_authored_text",
        )
        receipt = _authority_receipt(
            [acknowledged, captured],
            captured,
            event_id="authority-receipt-002",
        )

        rows = build_voice_gold(
            _audit(_record(row_hash)), [acknowledged, captured, receipt]
        )

        self.assertEqual(rows[0]["origin"], "jt_authored")
        self.assertEqual(rows[0]["publicationOutcomeEventId"], "published-002")
        self.assertEqual(rows[0]["textOutcomeEventId"], "text-002")
        self.assertEqual(rows[0]["text"], text)
        self.assertEqual(rows[-1]["blockingGapCount"], 0)

    def test_final_capture_binding_and_chronology_fail_closed(self) -> None:
        row_hash = "2" * 64
        publication = _publication_without_text(row_hash)
        wrong_packet_publication = _publication_without_text(
            "3" * 64, event_id="wrong-packet-publication"
        )
        bad_binding = _event(
            "capture-bad-binding",
            "legacy:{}".format(row_hash),
            "final_text_captured",
            _capture_payload(wrong_packet_publication, "Exact final text."),
            recorded_at="2026-09-28T12:01:00-04:00",
        )
        bad_time = _event(
            "capture-bad-time",
            "legacy:{}".format(row_hash),
            "final_text_captured",
            _capture_payload(publication, "Exact final text."),
            recorded_at="2026-09-28T11:59:00-04:00",
        )
        for capture, ledger, message in (
            (
                bad_binding,
                [publication, wrong_packet_publication, bad_binding],
                "same packet",
            ),
            (bad_time, [bad_time, publication], "recordedAt"),
        ):
            receipt = _authority_receipt(
                ledger,
                capture,
                event_id="authority-{}".format(capture["outcomeEventId"]),
                recorded_at="2026-09-28T12:03:00-04:00",
            )
            with self.subTest(capture=capture["outcomeEventId"]):
                with self.assertRaisesRegex(ValueError, message):
                    build_voice_gold(
                        _audit(_record(row_hash)), ledger + [receipt]
                    )

    def test_rejects_summary_draft_placeholder_untrusted_and_hashless_sources(self) -> None:
        hashes = ["3" * 64, "4" * 64, "5" * 64, "6" * 64]
        audit = _audit(*[_record(row_hash) for row_hash in hashes])
        summary = _event(
                "summary-only",
                "legacy:{}".format(hashes[0]),
                "publication_acknowledged",
                {"publicationUrl": "https://linkedin.com/posts/jt_summary-only"},
            )
        placeholder = _publication(
                hashes[1],
                "Draft text is not publishable evidence.",
                event_id="placeholder-url",
                url="https://linkedin.com/posts/placeholder",
            )
        model = _publication(
                hashes[2],
                "Model-written mechanics example.",
                event_id="model-example",
                source_type="model_generated",
            )
        declined = _event(
                "declined-draft",
                "legacy:{}".format(hashes[3]),
                "publication_declined",
                {"declineReason": "quality_fit", "note": "Old draft summary"},
            )
        placeholder_receipt = _authority_receipt(
            [summary, placeholder, model, declined],
            placeholder,
            event_id="authority-placeholder",
        )
        events = [summary, placeholder, model, declined, placeholder_receipt]

        with self.assertRaisesRegex(ValueError, "placeholder marker"):
            build_voice_gold(audit, events)

    def test_deduplicates_text_hash_deterministically(self) -> None:
        first_hash = "7" * 64
        second_hash = "8" * 64
        text = "Exact same final post bytes."
        later = _publication(
            second_hash,
            text,
            event_id="published-later",
            recorded_at="2026-09-28T13:00:00-04:00",
        )
        earlier = _publication(
            first_hash,
            text,
            event_id="published-earlier",
            recorded_at="2026-09-28T12:00:00-04:00",
        )

        earlier_receipt = _authority_receipt(
            [earlier, later],
            earlier,
            event_id="authority-earlier",
            recorded_at="2026-09-28T14:00:00-04:00",
        )
        later_receipt = _authority_receipt(
            [earlier, later],
            later,
            event_id="authority-later",
            recorded_at="2026-09-28T14:01:00-04:00",
        )
        rows = build_voice_gold(
            _audit(_record(second_hash), _record(first_hash)),
            [earlier, later, earlier_receipt, later_receipt],
        )

        gold = [row for row in rows if row["recordType"] == "voice_gold"]
        self.assertEqual(len(gold), 1)
        self.assertEqual(gold[0]["publicationOutcomeEventId"], "published-earlier")
        self.assertEqual(rows[-1]["blockingGapCount"], 0)

    def test_does_not_infer_zero_edit_pair_from_equal_or_sequential_text(self) -> None:
        row_hash = "9" * 64
        text = "One exact text."
        acknowledged = _publication(row_hash, text)
        publication_binding = _publication_without_text(
            row_hash,
            event_id="published-binding-009",
            recorded_at="2026-09-28T12:00:30-04:00",
        )
        captured = _event(
            "captured-009",
            "legacy:{}".format(row_hash),
            "final_text_captured",
            _capture_payload(publication_binding, text),
            recorded_at="2026-09-28T12:01:00-04:00",
            source_type="jt_authored_text",
        )
        acknowledged_receipt = _authority_receipt(
            [acknowledged, publication_binding, captured],
            acknowledged,
            event_id="authority-ack-009",
        )
        captured_receipt = _authority_receipt(
            [acknowledged, publication_binding, captured],
            captured,
            event_id="authority-capture-009",
            recorded_at="2026-09-28T12:03:00-04:00",
        )

        self.assertEqual(build_contrastive_pairs([
            acknowledged,
            publication_binding,
            captured,
            acknowledged_receipt,
            captured_receipt,
        ]), [{
            "schemaVersion": "linkedin-corpus-gap-summary.v0",
            "recordType": "gap_summary",
            "blockingGapCount": 1,
            "blockingGapPacketIds": ["legacy:{}".format(row_hash)],
        }])

    def test_builds_exact_typed_contrastive_pair(self) -> None:
        row_hash = "d" * 64
        draft = "AI can help operations teams."
        final = "The useful AI workflow is the one an operator can audit before lunch."
        publication = _publication_without_text(row_hash)
        event = _edit_pair_event(publication, draft, final)
        receipt = _authority_receipt([publication, event], event)

        rows = build_contrastive_pairs([publication, event, receipt])

        self.assertEqual(rows[0], {
            "schemaVersion": "linkedin-contrastive-pair.v0",
            "recordType": "contrastive_pair",
            "origin": "jt_edit_pair",
            "packetId": "legacy:{}".format(row_hash),
            "outcomeEventId": "edit-pair-001",
            "outcomeEventSha256": event["eventSha256"],
            "draftText": draft,
            "draftTextSha256": sha256_hex(draft.encode("utf-8")),
            "finalText": final,
            "finalTextSha256": sha256_hex(final.encode("utf-8")),
            "editReason": "specificity",
            "sourcePointer": event["sourcePointer"],
        })
        self.assertEqual(rows[-1], {
            "schemaVersion": "linkedin-corpus-gap-summary.v0",
            "recordType": "gap_summary",
            "blockingGapCount": 0,
            "blockingGapPacketIds": [],
        })

    def test_single_exact_final_without_pair_is_a_blocking_gap(self) -> None:
        row_hash = "e" * 64
        publication = _publication_without_text(row_hash)
        event = _event(
            "captured-only",
            "legacy:{}".format(row_hash),
            "final_text_captured",
            _capture_payload(
                publication, "Exact final text without the exact draft."
            ),
            source_type="jt_authored_text",
        )
        receipt = _authority_receipt([publication, event], event)

        self.assertEqual(build_contrastive_pairs([publication, event, receipt]), [{
            "schemaVersion": "linkedin-corpus-gap-summary.v0",
            "recordType": "gap_summary",
            "blockingGapCount": 1,
            "blockingGapPacketIds": ["legacy:{}".format(row_hash)],
        }])

    def test_deduplicates_contrastive_pairs_by_exact_hash_pair(self) -> None:
        draft = "Same draft."
        final = "Same final."
        later_publication = _publication_without_text(
            "f" * 64,
            event_id="published-later-binding",
            recorded_at="2026-09-28T12:30:00-04:00",
        )
        later = _edit_pair_event(
            later_publication,
            draft,
            final,
            event_id="pair-later",
            recorded_at="2026-09-28T13:00:00-04:00",
        )
        earlier_publication = _publication_without_text(
            "0" * 64,
            event_id="published-earlier-binding",
            recorded_at="2026-09-28T11:30:00-04:00",
        )
        earlier = _edit_pair_event(
            earlier_publication,
            draft,
            final,
            event_id="pair-earlier",
            recorded_at="2026-09-28T12:00:00-04:00",
        )

        ledger = [earlier_publication, earlier, later_publication, later]
        earlier_receipt = _authority_receipt(
            ledger,
            earlier,
            event_id="authority-pair-earlier",
            recorded_at="2026-09-28T14:00:00-04:00",
        )
        later_receipt = _authority_receipt(
            ledger,
            later,
            event_id="authority-pair-later",
            recorded_at="2026-09-28T14:01:00-04:00",
        )
        rows = build_contrastive_pairs(ledger + [earlier_receipt, later_receipt])
        pairs = [row for row in rows if row["recordType"] == "contrastive_pair"]

        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["outcomeEventId"], "pair-earlier")
        self.assertEqual(rows[-1]["blockingGapCount"], 0)

    def test_untrusted_complete_pair_is_excluded_and_reported_as_gap(self) -> None:
        row_hash = "b" * 64
        publication = _publication_without_text(row_hash)
        event = _edit_pair_event(
            publication,
            "Model draft.",
            "Model final.",
            source_type="model_generated",
        )

        self.assertEqual(build_contrastive_pairs([publication, event]), [{
            "schemaVersion": "linkedin-corpus-gap-summary.v0",
            "recordType": "gap_summary",
            "blockingGapCount": 1,
            "blockingGapPacketIds": ["legacy:{}".format(row_hash)],
        }])

    def test_validates_audit_and_event_contracts(self) -> None:
        row_hash = "a" * 64
        event = _publication(row_hash, "Exact text")
        malformed_event = dict(event)
        malformed_event["eventSha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "eventSha256"):
            build_voice_gold(_audit(_record(row_hash)), [malformed_event])

        malformed_audit = _audit(_record(row_hash))
        malformed_audit["statusCounts"] = {
            "not_posted_confirmed": 0,
            "posted_confirmed": 0,
            "status_unknown": 1,
        }
        with self.assertRaisesRegex(ValueError, "statusCounts"):
            build_voice_gold(malformed_audit, [event])

        malformed_nested_audit = _audit(_record(row_hash))
        malformed_nested_audit["missingFieldCounts"] = {"final_text": 99}
        with self.assertRaisesRegex(ValueError, "missingFieldCounts"):
            build_voice_gold(malformed_nested_audit, [event])

        malformed_recovery_audit = _audit(_record(row_hash))
        malformed_recovery_audit["recoveryRequest"] = {
            "schemaVersion": "linkedin-historical-recovery-request.v1",
            "generatedAt": "2026-09-28T12:00:01-04:00",
            "sourceSha256": "a" * 64,
            "items": [],
        }
        with self.assertRaisesRegex(ValueError, "recoveryRequest"):
            build_voice_gold(malformed_recovery_audit, [event])

        incomplete_recovery = _audit(_record(row_hash))
        recovery = dict(incomplete_recovery["recoveryRequest"])
        recovery["items"] = []
        incomplete_recovery["recoveryRequest"] = recovery
        with self.assertRaisesRegex(ValueError, "recoveryRequest.*complete"):
            build_voice_gold(incomplete_recovery, [event])

        bad_answers = _audit(_record(row_hash))
        recovery = dict(bad_answers["recoveryRequest"])
        item = dict(recovery["items"][0])
        answers = [dict(answer) for answer in item["allowedAnswers"]]
        answers[0]["optional"] = ["summary"]
        item["allowedAnswers"] = answers
        recovery["items"] = [item]
        bad_answers["recoveryRequest"] = recovery
        with self.assertRaisesRegex(ValueError, "allowedAnswers"):
            build_voice_gold(bad_answers, [event])

        with self.assertRaisesRegex(ValueError, "eventSha256"):
            build_contrastive_pairs([malformed_event])

    def test_correction_excludes_superseded_publication_evidence(self) -> None:
        row_hash = "c" * 64
        old = _publication(
            row_hash,
            "Superseded exact text",
            event_id="published-old",
            recorded_at="2026-09-28T12:01:00-04:00",
        )
        replacement = _publication(
            row_hash,
            "Corrected exact text",
            event_id="published-replacement",
            recorded_at="2026-09-28T12:00:00-04:00",
        )
        correction = _event(
            "correction-001",
            "legacy:{}".format(row_hash),
            "correction",
            {
                "targetOutcomeEventId": "published-old",
                "replacementEventSha256": replacement["eventSha256"],
                "reason": "JT corrected the exact published text",
            },
            recorded_at="2026-09-28T12:02:00-04:00",
        )

        ledger = [replacement, old, correction]
        receipt = _authority_receipt(
            ledger,
            replacement,
            event_id="authority-corrected",
            recorded_at="2026-09-28T12:03:00-04:00",
        )
        rows = build_voice_gold(_audit(_record(row_hash)), ledger + [receipt])

        self.assertEqual(rows[0]["text"], "Corrected exact text")
        self.assertEqual(rows[0]["publicationOutcomeEventId"], "published-replacement")


if __name__ == "__main__":
    unittest.main()
