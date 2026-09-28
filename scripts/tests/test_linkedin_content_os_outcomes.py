import json
import multiprocessing
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import (
    CLAIM_ATTRIBUTION,
    DECLINE_REASON,
    HISTORICAL_STATUS,
    OUTCOME_EVENT,
    validate_claim_attribution,
    validate_event,
)
from scripts.linkedin_content_os.outcomes import append_event, load_events


def _hold_ledger_lock(path_text: str, acquired: object, release: object) -> None:
    from scripts.linkedin_content_os.canonical import _exclusive_path_lock

    with _exclusive_path_lock(Path(path_text)):
        acquired.set()
        release.wait(timeout=5)


def _event(
    *,
    event_id: str = "outcome-001",
    packet_id: str = "packet-001",
    event_type: str = "historical_status",
    recorded_at: str = "2026-09-28T12:00:00-04:00",
    payload: object = None,
) -> dict[str, object]:
    if payload is None:
        payload = {
            "legacyRowSha256": "1" * 64,
            "status": "status_unknown",
        }
    event: dict[str, object] = {
        "schemaVersion": "linkedin-content-outcome.v1",
        "outcomeEventId": event_id,
        "packetId": packet_id,
        "eventType": event_type,
        "recordedAt": recorded_at,
        "sourcePointer": {
            "sourceType": "fixture",
            "sourceId": "fixture:outcomes",
            "sourceSha256": "2" * 64,
        },
        "payload": payload,
    }
    event["eventSha256"] = sha256_hex(canonical_bytes(event))
    return event


class ClosedContractTests(unittest.TestCase):
    def test_closed_enums_are_exact(self) -> None:
        self.assertEqual(
            HISTORICAL_STATUS,
            {"posted_confirmed", "not_posted_confirmed", "status_unknown"},
        )
        self.assertEqual(
            OUTCOME_EVENT,
            {
                "historical_status",
                "publication_acknowledged",
                "publication_deferred",
                "publication_declined",
                "final_text_captured",
                "metric_snapshot",
                "qualified_reply",
                "commercial_outcome",
                "focus_decision",
                "permission_fixture_accepted",
                "correction",
            },
        )
        self.assertEqual(DECLINE_REASON, {"quality_fit", "stale", "timing", "other"})
        self.assertEqual(
            CLAIM_ATTRIBUTION,
            {"public_fact", "vendor_assertion", "jt_verified_fact", "hypothesis"},
        )

    def test_accepts_valid_historical_event(self) -> None:
        event = _event()
        self.assertEqual(validate_event(event), event)

    def test_rejects_unknown_top_level_source_and_payload_fields(self) -> None:
        cases = []
        top_level = _event()
        top_level["surprise"] = True
        cases.append(top_level)

        source = _event()
        source_pointer = dict(source["sourcePointer"])
        source_pointer["url"] = "https://example.com"
        source["sourcePointer"] = source_pointer
        source["eventSha256"] = sha256_hex(
            canonical_bytes({key: value for key, value in source.items() if key != "eventSha256"})
        )
        cases.append(source)

        payload = _event(payload={
            "legacyRowSha256": "1" * 64,
            "status": "status_unknown",
            "unknown": True,
        })
        cases.append(payload)

        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    validate_event(case)

    def test_rejects_invalid_enum_hash_timestamp_and_id(self) -> None:
        mutations = [
            ("eventType", "invented"),
            ("eventSha256", "A" * 64),
            ("recordedAt", "2026-09-28T12:00:00"),
            ("outcomeEventId", "contains spaces"),
        ]
        for field, value in mutations:
            event = _event()
            event[field] = value
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    validate_event(event)

    def test_rejects_noncanonical_event_hash(self) -> None:
        event = _event()
        event["eventSha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "eventSha256"):
            validate_event(event)

    def test_rejects_null_anywhere(self) -> None:
        event = _event(
            event_type="publication_declined",
            payload={"declineReason": "quality_fit", "note": None},
        )
        with self.assertRaisesRegex(ValueError, "must not be null"):
            validate_event(event)

    def test_each_closed_event_type_has_a_strict_valid_payload(self) -> None:
        final_text = "Exact final text"
        payloads = {
            "historical_status": {
                "legacyRowSha256": "1" * 64,
                "status": "posted_confirmed",
            },
            "publication_acknowledged": {
                "publicationUrl": "https://linkedin.com/posts/jt_valid-1"
            },
            "publication_deferred": {"nextCheckAt": "2026-09-29T12:00:00Z"},
            "publication_declined": {"declineReason": "quality_fit"},
            "final_text_captured": {
                "finalText": final_text,
                "finalTextSha256": sha256_hex(final_text.encode("utf-8")),
            },
            "metric_snapshot": {
                "windowDays": 7,
                "metrics": {"impressions": 12},
                "collectionMethod": "jt_manual",
            },
            "qualified_reply": {
                "evidenceRef": "proof:reply-1",
                "qualificationReason": "buyer asked for a call",
                "claimAttribution": "jt_verified_fact",
            },
            "commercial_outcome": {
                "outcomeType": "buyer_conversation",
                "evidenceRef": "proof:conversation-1",
            },
            "focus_decision": {
                "decision": "confirmed",
                "focusSnapshotSha256": "3" * 64,
            },
            "permission_fixture_accepted": {
                "fixtureId": "fixture-001",
                "repository": "git@github.com:example/repo.git",
                "commitSha": "4" * 40,
                "path": "evidence/proof.json",
                "extractedSha256": "5" * 64,
                "permissionEvidenceSha256": "6" * 64,
                "permissionExpiresAt": "2027-09-28T12:00:00Z",
            },
            "correction": {
                "targetOutcomeEventId": "outcome-previous",
                "replacementEventSha256": "7" * 64,
                "reason": "JT corrected the source fact",
            },
        }
        self.assertEqual(set(payloads), OUTCOME_EVENT)
        for index, (event_type, payload) in enumerate(payloads.items()):
            event = _event(
                event_id="outcome-{:03d}".format(index + 10),
                event_type=event_type,
                payload=payload,
            )
            with self.subTest(event_type=event_type):
                self.assertEqual(validate_event(event), event)

    def test_publication_acknowledgment_requires_https_linkedin_url(self) -> None:
        for url in (
            "http://www.linkedin.com/posts/jt_post-1",
            "https://example.com/posts/1",
            "https://linkedin.evil.example/posts/1",
            " https://www.linkedin.com/posts/jt_post-1",
            "https://www.linkedin.com/posts/jt_post-1\n",
            "https://www.linkedin.com:444/posts/jt_post-1",
            "https://www.linkedin.com:99999/posts/jt_post-1",
            "https://www.linkedin.com:notaport/posts/jt_post-1",
            "https://www.linkedin.com/posts/jt_post-1\x00",
            "https://www.linkedin.com/posts/jt post-1",
            "https://www.linkedin.com/posts\\jt_post-1",
            "https://www.linkedin.com/posts/jt\u00a0post-1",
            "https://www.linkedin.com/posts/jt|post-1",
            "https://www.linkedin.com/posts/jt%post-1",
            "https://www.linkedin.com/posts/jt%2post-1",
            "https://www.linkedin.com/posts/jt%GGpost-1",
        ):
            event = _event(
                event_type="publication_acknowledged",
                payload={"publicationUrl": url},
            )
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validate_event(event)

        valid = _event(
            event_type="publication_acknowledged",
            payload={
                "publicationUrl": "https://www.linkedin.com:443/posts/jt_post-1%20proof?trk=public_post"
            },
        )
        self.assertEqual(validate_event(valid), valid)

    def test_decline_reason_historical_status_and_claim_attribution_are_closed(self) -> None:
        declined = _event(
            event_type="publication_declined",
            payload={"declineReason": "not_good_enough"},
        )
        status = _event(payload={"legacyRowSha256": "1" * 64, "status": "posted_maybe"})
        with self.assertRaises(ValueError):
            validate_event(declined)
        with self.assertRaises(ValueError):
            validate_event(status)
        with self.assertRaises(ValueError):
            validate_claim_attribution("model_guess")

    def test_fixture_contains_strict_valid_rows(self) -> None:
        fixture = Path("scripts/tests/fixtures/linkedin_content_os/outcomes.jsonl")
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "outcomes.jsonl"
            copy.write_bytes(fixture.read_bytes())
            events = load_events(copy)
            self.assertGreaterEqual(len(events), 2)
            self.assertEqual([validate_event(event) for event in events], events)


class OutcomeLedgerTests(unittest.TestCase):
    def test_appends_and_exact_replay_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.jsonl"
            event = _event()
            self.assertEqual(append_event(path, event), "appended")
            original = path.read_bytes()
            self.assertEqual(append_event(path, event), "replayed")
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(load_events(path), [event])

    def test_reusing_id_with_different_event_fails_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.jsonl"
            first = _event()
            append_event(path, first)
            original = path.read_bytes()
            conflict = _event(payload={
                "legacyRowSha256": "1" * 64,
                "status": "posted_confirmed",
            })
            with self.assertRaisesRegex(ValueError, "outcomeEventId"):
                append_event(path, conflict)
            self.assertEqual(path.read_bytes(), original)

    def test_rejects_per_packet_timestamp_regression_but_allows_other_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.jsonl"
            append_event(path, _event(recorded_at="2026-09-28T13:00:00-04:00"))
            with self.assertRaisesRegex(ValueError, "timestamp regression"):
                append_event(
                    path,
                    _event(event_id="outcome-002", recorded_at="2026-09-28T12:59:59-04:00"),
                )
            self.assertEqual(
                append_event(
                    path,
                    _event(
                        event_id="outcome-003",
                        packet_id="packet-002",
                        recorded_at="2026-09-28T12:59:59-04:00",
                    ),
                ),
                "appended",
            )

    def test_preserves_noncanonical_earlier_prefix_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.jsonl"
            first = _event()
            prefix = json.dumps(first, ensure_ascii=False, sort_keys=False).encode("utf-8") + b"\n"
            path.write_bytes(prefix)

            second = _event(
                event_id="outcome-002",
                recorded_at="2026-09-28T12:01:00-04:00",
            )
            self.assertEqual(append_event(path, second), "appended")
            self.assertTrue(path.read_bytes().startswith(prefix))

    def test_fails_closed_if_ledger_mutates_between_validation_and_append(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.jsonl"
            append_event(path, _event())
            corrupt = b'{"corrupt":true}\n'
            second = _event(
                event_id="outcome-002",
                recorded_at="2026-09-28T12:01:00-04:00",
            )

            from scripts.linkedin_content_os import outcomes

            real_append = outcomes.append_jsonl_exact_prefix

            def mutate_then_append(*args: object, **kwargs: object) -> None:
                path.write_bytes(corrupt)
                real_append(*args, **kwargs)

            with mock.patch.object(
                outcomes,
                "append_jsonl_exact_prefix",
                side_effect=mutate_then_append,
            ):
                with self.assertRaisesRegex(RuntimeError, "validated prefix"):
                    append_event(path, second)

            self.assertEqual(path.read_bytes(), corrupt)

    def test_load_fails_closed_on_invalid_prior_row(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.jsonl"
            path.write_text('{"not":"an outcome"}\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_events(path)

    def test_reader_waits_for_writer_ledger_lock(self) -> None:
        context = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.jsonl"
            append_event(path, _event())
            acquired = context.Event()
            release = context.Event()
            holder = context.Process(
                target=_hold_ledger_lock,
                args=(str(path), acquired, release),
            )
            holder.start()
            self.assertTrue(acquired.wait(timeout=2))

            completed = threading.Event()
            errors = []

            def read_ledger() -> None:
                try:
                    load_events(path)
                except Exception as error:
                    errors.append(error)
                finally:
                    completed.set()

            reader = threading.Thread(target=read_ledger)
            reader.start()
            self.assertFalse(completed.wait(timeout=0.1))
            release.set()
            self.assertTrue(completed.wait(timeout=2))
            reader.join(timeout=1)
            holder.join(timeout=2)
            self.assertEqual(holder.exitcode, 0)
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
