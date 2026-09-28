import unittest

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
            "items": [],
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
    source_type: str = "jt_confirmation",
    source_id: str = "telegram:27993",
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
            "sourceSha256": "b" * 64,
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
    source_type: str = "jt_confirmation",
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


class VoiceGoldTests(unittest.TestCase):
    def test_accepts_only_exact_hash_bound_final_published_text(self) -> None:
        row_hash = "1" * 64
        text = "The exact final LinkedIn post, including punctuation."
        event = _publication(row_hash, text)

        rows = build_voice_gold(_audit(_record(row_hash)), [event])

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

    def test_resolves_separate_exact_final_text_capture_to_publication(self) -> None:
        row_hash = "2" * 64
        text = "JT supplied the exact final text later."
        acknowledged = _event(
            "published-002",
            "legacy:{}".format(row_hash),
            "publication_acknowledged",
            {"publicationUrl": "https://linkedin.com/posts/jt_exact-2"},
        )
        captured = _event(
            "text-002",
            "legacy:{}".format(row_hash),
            "final_text_captured",
            {
                "finalText": text,
                "finalTextSha256": sha256_hex(text.encode("utf-8")),
            },
            recorded_at="2026-09-28T12:01:00-04:00",
            source_type="jt_authored_text",
        )

        rows = build_voice_gold(_audit(_record(row_hash)), [captured, acknowledged])

        self.assertEqual(rows[0]["origin"], "jt_authored")
        self.assertEqual(rows[0]["publicationOutcomeEventId"], "published-002")
        self.assertEqual(rows[0]["textOutcomeEventId"], "text-002")
        self.assertEqual(rows[0]["text"], text)
        self.assertEqual(rows[-1]["blockingGapCount"], 0)

    def test_rejects_summary_draft_placeholder_untrusted_and_hashless_sources(self) -> None:
        hashes = ["3" * 64, "4" * 64, "5" * 64, "6" * 64]
        audit = _audit(*[_record(row_hash) for row_hash in hashes])
        events = [
            _event(
                "summary-only",
                "legacy:{}".format(hashes[0]),
                "publication_acknowledged",
                {"publicationUrl": "https://linkedin.com/posts/jt_summary-only"},
            ),
            _publication(
                hashes[1],
                "Draft text is not publishable evidence.",
                event_id="placeholder-url",
                url="https://linkedin.com/posts/placeholder",
            ),
            _publication(
                hashes[2],
                "Model-written mechanics example.",
                event_id="model-example",
                source_type="model_generated",
            ),
            _event(
                "declined-draft",
                "legacy:{}".format(hashes[3]),
                "publication_declined",
                {"declineReason": "quality_fit", "note": "Old draft summary"},
            ),
        ]

        rows = build_voice_gold(audit, events)

        self.assertEqual(rows, [{
            "schemaVersion": "linkedin-corpus-gap-summary.v0",
            "recordType": "gap_summary",
            "blockingGapCount": 4,
            "blockingGapPacketIds": ["legacy:{}".format(value) for value in sorted(hashes)],
        }])

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

        rows = build_voice_gold(
            _audit(_record(second_hash), _record(first_hash)),
            [later, earlier],
        )

        gold = [row for row in rows if row["recordType"] == "voice_gold"]
        self.assertEqual(len(gold), 1)
        self.assertEqual(gold[0]["publicationOutcomeEventId"], "published-earlier")
        self.assertEqual(rows[-1]["blockingGapCount"], 0)

    def test_does_not_infer_zero_edit_pair_from_equal_or_sequential_text(self) -> None:
        row_hash = "9" * 64
        text = "One exact text."
        acknowledged = _publication(row_hash, text)
        captured = _event(
            "captured-009",
            "legacy:{}".format(row_hash),
            "final_text_captured",
            {"finalText": text, "finalTextSha256": sha256_hex(text.encode("utf-8"))},
            recorded_at="2026-09-28T12:01:00-04:00",
            source_type="jt_authored_text",
        )

        self.assertEqual(build_contrastive_pairs([acknowledged, captured]), [{
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

        rows = build_voice_gold(
            _audit(_record(row_hash)),
            [correction, old, replacement],
        )

        self.assertEqual(rows[0]["text"], "Corrected exact text")
        self.assertEqual(rows[0]["publicationOutcomeEventId"], "published-replacement")


if __name__ == "__main__":
    unittest.main()
