import csv
import json
import os
import tempfile
import unittest
from unittest import mock
from datetime import datetime, timezone
from pathlib import Path

from scripts import growth_os_send_readiness as readiness


NOW = datetime(2026, 10, 2, 19, 0, tzinfo=timezone.utc)


def contact(position=1, email="buyer@example.com", company="Example Builders"):
    return {
        "batch_position": str(position),
        "source_batch": "fixture",
        "company": company,
        "domain": "example.com",
        "employee_count_or_band": "25",
        "buyer_name": "Alex Buyer",
        "buyer_title": "COO",
        "email": email,
        "email_status": "apollo_valid",
        "geography": "New York, NY",
        "evidence_ref": "fixture.csv",
        "suppression_status": "not_requeried_before_send",
        "prior_contact_status": "none",
        "review_verdict": "PASS",
    }


def message(position=1, email="buyer@example.com", company="Example Builders"):
    return readiness.Message(
        position=position,
        buyer_name="Alex Buyer",
        company=company,
        email=email,
        subject="coi renewals",
        body="Alex,\n\nHow do you track COI renewals?\n\nI help contractors find gaps.\n\nWould a short fix list help?",
        signature="JT Somwaru\nNew York City\njtsomwaru.com",
    )


def recipient_check(email="buyer@example.com", **overrides):
    row = {
        "email": email,
        "mailbox_status": "valid",
        "mailbox_verified_at": "2026-10-02T18:30:00Z",
        "identity_status": "verified",
        "identity_checked_at": "2026-10-02T18:00:00Z",
        "suppression_observed": "true",
        "suppression_status": "clear",
        "suppression_checked_at": "2026-10-02T18:55:00Z",
    }
    row.update(overrides)
    return row


def sender(account="alex@safe-outreach.com", **overrides):
    row = {
        "sending_account": account,
        "account_type": "prewarmed",
        "account_status": "active",
        "dns_mx": "pass",
        "dns_spf": "pass",
        "dns_dkim": "pass",
        "dns_dmarc": "pass",
        "warmup_health_score": "95",
        "warmup_days": "0",
        "daily_campaign_limit": "5",
        "sender_checked_at": "2026-10-02T18:30:00Z",
    }
    row.update(overrides)
    return row


class SendReadinessTests(unittest.TestCase):
    def test_bind_rejects_contact_packet_email_drift(self):
        with self.assertRaisesRegex(readiness.ReadinessError, "email mismatch"):
            readiness.bind_contacts([contact()], [message(email="other@example.com")])

    def test_bind_allows_heading_to_omit_only_a_legal_entity_suffix(self):
        bound = readiness.bind_contacts(
            [contact(company="Example Builders Inc.")],
            [message(company="Example Builders")],
        )
        self.assertEqual(1, len(bound))
        with self.assertRaisesRegex(readiness.ReadinessError, "company mismatch"):
            readiness.bind_contacts(
                [contact(company="Example Builders Holdings Inc.")],
                [message(company="Example Builders")],
            )

    def test_bind_rejects_duplicate_recipient(self):
        with self.assertRaisesRegex(readiness.ReadinessError, "duplicate email"):
            readiness.bind_contacts(
                [contact(1), contact(2, company="Other Builders")],
                [message(1), message(2, company="Other Builders")],
            )

    def test_copy_hash_is_deterministic_and_copy_sensitive(self):
        first = readiness.copy_hash(message())
        self.assertEqual(first, readiness.copy_hash(message()))
        changed = message()
        changed = readiness.Message(**{**changed.__dict__, "subject": "different"})
        self.assertNotEqual(first, readiness.copy_hash(changed))

    def test_missing_recipient_check_blocks_without_dropping_row(self):
        result = readiness.compile_batch(
            [contact()], [message()], [], [sender()], now=NOW
        )
        self.assertEqual(1, len(result.rows))
        self.assertFalse(result.ready)
        self.assertIn("recipient_verification_missing", result.rows[0].blockers)

    def test_stale_and_uncleared_recipient_checks_fail_closed(self):
        check = recipient_check(
            mailbox_verified_at="2026-10-01T17:00:00Z",
            suppression_observed="true",
            suppression_status="blocked",
            suppression_checked_at="2026-10-02T18:59:00Z",
        )
        result = readiness.compile_batch(
            [contact()], [message()], [check], [sender()], now=NOW
        )
        self.assertIn("mailbox_verification_stale", result.rows[0].blockers)
        self.assertIn("suppression_blocked", result.rows[0].blockers)

    def test_prohibited_personal_sender_is_rejected(self):
        result = readiness.compile_batch(
            [contact()],
            [message()],
            [recipient_check()],
            [sender("jtsomwaru@gmail.com")],
            now=NOW,
        )
        self.assertFalse(result.ready)
        self.assertIn("no_eligible_sending_mailbox", result.rows[0].blockers)
        self.assertIn("prohibited_sender", result.sender_rejections[0]["reasons"])

    def test_prewarmed_sender_is_capped_at_five_first_batch_rows(self):
        contacts = [contact(i, f"buyer{i}@example.com", f"Builder {i}") for i in range(1, 7)]
        messages = [message(i, f"buyer{i}@example.com", f"Builder {i}") for i in range(1, 7)]
        checks = [recipient_check(f"buyer{i}@example.com") for i in range(1, 7)]
        result = readiness.compile_batch(
            contacts, messages, checks, [sender()], now=NOW
        )
        self.assertFalse(result.ready)
        self.assertEqual(5, sum(row.sending_account != "" for row in result.rows))
        self.assertIn("insufficient_sending_capacity", result.rows[-1].blockers)

    def test_sender_allocation_is_deterministic_round_robin(self):
        contacts = [contact(i, f"buyer{i}@example.com", f"Builder {i}") for i in range(1, 7)]
        messages = [message(i, f"buyer{i}@example.com", f"Builder {i}") for i in range(1, 7)]
        checks = [recipient_check(f"buyer{i}@example.com") for i in range(1, 7)]
        senders = [sender("z@safe-outreach.com"), sender("a@safe-outreach.com")]
        result = readiness.compile_batch(contacts, messages, checks, senders, now=NOW)
        self.assertEqual(
            ["a@safe-outreach.com", "z@safe-outreach.com"] * 3,
            [row.sending_account for row in result.rows],
        )

    def test_unwarmed_standard_sender_is_rejected(self):
        result = readiness.compile_batch(
            [contact()],
            [message()],
            [recipient_check()],
            [sender(account_type="standard", warmup_days="10")],
            now=NOW,
        )
        self.assertIn("warmup_incomplete", result.sender_rejections[0]["reasons"])

    def test_boundary_ages_are_accepted_and_future_attestations_fail(self):
        exact = recipient_check(
            mailbox_verified_at="2026-10-01T19:00:00Z",
            identity_checked_at="2026-09-25T19:00:00Z",
            suppression_checked_at="2026-10-02T18:45:00Z",
        )
        result = readiness.compile_batch(
            [contact()], [message()], [exact],
            [sender(sender_checked_at="2026-10-01T19:00:00Z")], now=NOW,
        )
        self.assertTrue(result.ready)
        with self.assertRaisesRegex(readiness.ReadinessError, "cannot be in the future"):
            readiness.compile_batch(
                [contact()], [message()],
                [recipient_check(mailbox_verified_at="2026-10-02T19:00:01Z")],
                [sender()], now=NOW,
            )

    def test_unobserved_suppression_is_not_clearance(self):
        result = readiness.compile_batch(
            [contact()], [message()],
            [recipient_check(suppression_observed="false")], [sender()], now=NOW,
        )
        self.assertIn("suppression_not_observed", result.rows[0].blockers)

    def test_outputs_withhold_instantly_import_until_every_row_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = readiness.write_outputs(
                readiness.compile_batch([contact()], [message()], [], [sender()], now=NOW),
                Path(tmp),
                "fixture",
            )
            self.assertTrue(paths["readiness_csv"].exists())
            self.assertTrue(paths["summary_json"].exists())
            self.assertTrue(paths["outcome_csv"].exists())
            self.assertIsNone(paths["instantly_csv"])
            with paths["outcome_csv"].open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual("not_sent", rows[0]["send_status"])
            summary = json.loads(paths["summary_json"].read_text(encoding="utf-8"))
            self.assertFalse(summary["ready"])

    def test_ready_batch_emits_instantly_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = readiness.compile_batch(
                [contact()], [message()], [recipient_check()], [sender()], now=NOW
            )
            self.assertTrue(result.ready)
            paths = readiness.write_outputs(result, Path(tmp), "fixture")
            self.assertTrue(paths["instantly_csv"].exists())

    def test_identical_bundle_is_reused_and_blocked_manifest_withholds_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ready = readiness.compile_batch(
                [contact()], [message()], [recipient_check()], [sender()], now=NOW,
                input_hashes={"contactsCsvSha256": "a", "packetMarkdownSha256": "b",
                              "recipientVerificationCsvSha256": "c", "senderInventoryCsvSha256": "d"},
            )
            first = readiness.write_outputs(ready, root)
            second = readiness.write_outputs(ready, root)
            self.assertEqual(first["summary_json"], second["summary_json"])
            blocked = readiness.compile_batch(
                [contact()], [message()], [], [sender()], now=NOW,
                input_hashes={"contactsCsvSha256": "a", "packetMarkdownSha256": "b",
                              "recipientVerificationCsvSha256": None, "senderInventoryCsvSha256": "d"},
            )
            readiness.write_outputs(blocked, root)
            manifest = json.loads((root / "current.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["ready"])
            self.assertIsNone(manifest["instantlyImportPath"])

    def test_reconciliation_is_append_only_idempotent_and_projects_exact_sent_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = readiness.compile_batch(
                [contact()], [message()], [recipient_check()], [sender()], now=NOW
            )
            paths = readiness.write_outputs(result, root, "fixture")
            ledger = root / "reconciliation-events.jsonl"
            event = readiness.build_event(
                batch_id="fixture", row_id_value="fixture:01", vendor_message_id="msg-1",
                evidence_id="jt-final-copy-1", sent_at="2026-10-02T19:10:00Z",
                final_subject="final subject", final_body="Final body\n\nJT Somwaru",
                event_observed_at="2026-10-02T19:12:00Z",
            )
            self.assertTrue(readiness.append_reconciliation_event(ledger, event))
            self.assertFalse(readiness.append_reconciliation_event(ledger, event))
            conflict = dict(event)
            conflict["evidenceId"] = "different-evidence"
            conflict["eventId"] = readiness.sha256_bytes(
                readiness.canonical_json_bytes(readiness._event_core(conflict))
            )
            with self.assertRaisesRegex(readiness.ReadinessError, "conflicts"):
                readiness.append_reconciliation_event(ledger, conflict)
            projected = root / "current-outcomes.csv"
            readiness.project_outcomes(paths["outcome_csv"], ledger, projected)
            with projected.open(newline="", encoding="utf-8") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual("sent", row["send_status"])
            self.assertEqual(event["sentSubjectSha256"], row["sent_subject_sha256"])
            self.assertEqual(event["sentBodySha256"], row["sent_body_sha256"])
            self.assertNotEqual(row["candidate_subject_sha256"], row["sent_subject_sha256"])

    def test_reconciliation_rejects_hardlink_alias_and_projection_revalidates_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = readiness.compile_batch(
                [contact()], [message()], [recipient_check()], [sender()], now=NOW
            )
            paths = readiness.write_outputs(result, root, "fixture")
            ledger = root / "reconciliation-events.jsonl"
            event = readiness.build_event(
                batch_id="fixture", row_id_value="fixture:01", vendor_message_id="msg-1",
                evidence_id="jt-final-copy-1", sent_at="2026-10-02T19:10:00Z",
                final_subject="final subject", final_body="Final body",
                event_observed_at="2026-10-02T19:12:00Z",
            )
            ledger.write_bytes(b"")
            os.link(ledger, root / "ledger-alias.jsonl")
            with self.assertRaisesRegex(readiness.ReadinessError, "unsafe"):
                readiness.append_reconciliation_event(ledger, event)

            ledger.unlink()
            (root / "ledger-alias.jsonl").unlink()
            corrupt = dict(event)
            corrupt["sentBodySha256"] = "0" * 64
            corrupt["eventId"] = readiness.sha256_bytes(
                readiness.canonical_json_bytes(readiness._event_core(corrupt))
            )
            ledger.write_bytes(readiness.canonical_json_bytes(corrupt) + b"\n")
            with self.assertRaisesRegex(readiness.ReadinessError, "sent body hash mismatch"):
                readiness.project_outcomes(paths["outcome_csv"], ledger, root / "current-outcomes.csv")

    def test_reconciliation_retries_partial_os_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "events.jsonl"
            event = readiness.build_event(
                batch_id="fixture", row_id_value="fixture:01", vendor_message_id="msg-1",
                evidence_id="evidence-1", sent_at="2026-10-02T19:10:00Z",
                final_subject="subject", final_body="body",
                event_observed_at="2026-10-02T19:12:00Z",
            )
            original_write = os.write
            calls = []

            def short_write(fd, data):
                calls.append(len(data))
                if len(calls) == 1:
                    data = data[: max(1, len(data) // 2)]
                return original_write(fd, data)

            with mock.patch.object(readiness.os, "write", side_effect=short_write):
                self.assertTrue(readiness.append_reconciliation_event(ledger, event))
            self.assertGreaterEqual(len(calls), 2)
            self.assertEqual(
                readiness.canonical_json_bytes(event) + b"\n",
                ledger.read_bytes(),
            )

    def test_projection_rejects_directly_injected_conflicting_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = readiness.compile_batch(
                [contact()], [message()], [recipient_check()], [sender()], now=NOW
            )
            paths = readiness.write_outputs(result, root, "fixture")
            first = readiness.build_event(
                batch_id="fixture", row_id_value="fixture:01", vendor_message_id="msg-1",
                evidence_id="evidence-1", sent_at="2026-10-02T19:10:00Z",
                final_subject="subject one", final_body="body one",
                event_observed_at="2026-10-02T19:12:00Z",
            )
            conflict = readiness.build_event(
                batch_id="fixture", row_id_value="fixture:01", vendor_message_id="msg-1",
                evidence_id="evidence-2", sent_at="2026-10-02T19:10:00Z",
                final_subject="subject two", final_body="body two",
                event_observed_at="2026-10-02T19:13:00Z",
            )
            ledger = root / "reconciliation-events.jsonl"
            ledger.write_bytes(
                readiness.canonical_json_bytes(first) + b"\n"
                + readiness.canonical_json_bytes(conflict) + b"\n"
            )
            with self.assertRaisesRegex(readiness.ReadinessError, "conflicts"):
                readiness.project_outcomes(paths["outcome_csv"], ledger, root / "current-outcomes.csv")


if __name__ == "__main__":
    unittest.main()
