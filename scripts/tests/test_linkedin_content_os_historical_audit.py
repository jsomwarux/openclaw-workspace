import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.historical_audit import audit_legacy_rows


FIXTURE = Path("scripts/tests/fixtures/linkedin_content_os/legacy-posted-log.jsonl")
GENERATED_AT = "2026-09-28T12:00:00-04:00"


def _event(
    row_hash: str,
    status: str,
    *,
    event_id: str,
    recorded_at: str = "2026-09-28T12:00:00-04:00",
) -> dict[str, object]:
    event: dict[str, object] = {
        "schemaVersion": "linkedin-content-outcome.v1",
        "outcomeEventId": event_id,
        "packetId": "legacy:{}".format(row_hash),
        "eventType": "historical_status",
        "recordedAt": recorded_at,
        "sourcePointer": {
            "sourceType": "jt_confirmation",
            "sourceId": "telegram:27993",
            "sourceSha256": "2" * 64,
        },
        "payload": {"legacyRowSha256": row_hash, "status": status},
    }
    event["eventSha256"] = sha256_hex(canonical_bytes(event))
    return event


def _fixture_rows() -> list[dict[str, object]]:
    import json

    return [json.loads(line) for line in FIXTURE.read_text(encoding="utf-8").splitlines()]


def _row_hash(topic: str) -> str:
    row = next(row for row in _fixture_rows() if row.get("topic") == topic)
    return sha256_hex(canonical_bytes(row))


def _write_outcomes(path: Path) -> None:
    events = [
        _event(
            _row_hash("jt-confirmed-no-url"),
            "posted_confirmed",
            event_id="history-confirmed-001",
        ),
        _event(
            _row_hash("governed-decline"),
            "not_posted_confirmed",
            event_id="history-declined-001",
        ),
    ]
    path.write_bytes(b"".join(canonical_bytes(event) + b"\n" for event in events))


class HistoricalAuditTests(unittest.TestCase):
    def _audit(self) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            outcomes = Path(directory) / "outcomes.jsonl"
            _write_outcomes(outcomes)
            return audit_legacy_rows(FIXTURE, outcomes, GENERATED_AT)

    def test_classifies_only_evidence_backed_linkedin_history(self) -> None:
        audit = self._audit()
        records = audit["records"]
        self.assertEqual(len(records), 6)
        self.assertNotIn("exclude-x", {record["topic"] for record in records})
        by_topic = {record["topic"]: record for record in records}

        self.assertEqual(by_topic["public-url-proof"]["status"], "posted_confirmed")
        self.assertEqual(by_topic["public-url-proof"]["missing"], [])
        self.assertEqual(by_topic["jt-confirmed-no-url"]["status"], "posted_confirmed")
        self.assertEqual(
            by_topic["jt-confirmed-no-url"]["missing"],
            ["public_url", "final_text"],
        )
        self.assertEqual(
            by_topic["raw-false-remains-unknown"]["status"], "status_unknown"
        )
        self.assertEqual(
            by_topic["governed-decline"]["status"], "not_posted_confirmed"
        )

        self.assertEqual(
            audit["statusCounts"],
            {
                "not_posted_confirmed": 1,
                "posted_confirmed": 2,
                "status_unknown": 3,
            },
        )

    def test_raw_false_cannot_become_not_posted_without_governed_event(self) -> None:
        audit = audit_legacy_rows(FIXTURE, None, GENERATED_AT)
        false_records = [
            record
            for record in audit["records"]
            if record["topic"] in {
                "raw-false-remains-unknown",
                "governed-decline",
                "duplicate-row",
            }
        ]
        self.assertTrue(false_records)
        self.assertEqual({record["status"] for record in false_records}, {"status_unknown"})

    def test_raw_false_stays_unknown_even_with_a_valid_linkedin_url(self) -> None:
        audit = audit_legacy_rows(FIXTURE, None, GENERATED_AT)
        record = next(
            item
            for item in audit["records"]
            if item["topic"] == "raw-false-remains-unknown"
        )
        self.assertEqual(record["status"], "status_unknown")

    def test_exact_legacy_jt_confirmation_marker_confirms_post_without_url(self) -> None:
        audit = audit_legacy_rows(FIXTURE, None, GENERATED_AT)
        record = next(
            item
            for item in audit["records"]
            if item["topic"] == "jt-confirmed-no-url"
        )
        self.assertEqual(record["status"], "posted_confirmed")
        self.assertEqual(record["missing"], ["public_url", "final_text"])

    def test_free_form_confirmation_and_workflow_metadata_do_not_confirm(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.jsonl"
            path.write_text(
                '{"date":"2026-09-07","platform":"linkedin","topic":"free-form",'
                '"posted":true,"posted_confirmation":"JT probably posted this",'
                '"scheduled_in_notion":true,"drive_link":"https://example.com"}\n',
                encoding="utf-8",
            )
            audit = audit_legacy_rows(path, None, GENERATED_AT)
        self.assertEqual(audit["records"][0]["status"], "status_unknown")

    def test_reports_duplicates_without_line_number_identity_or_merging(self) -> None:
        audit = self._audit()
        duplicate_hash = _row_hash("duplicate-row")
        duplicate_records = [
            record for record in audit["records"] if record["legacyRowSha256"] == duplicate_hash
        ]
        self.assertEqual(len(duplicate_records), 2)
        self.assertEqual(
            audit["duplicateGroups"],
            [{"legacyRowSha256": duplicate_hash, "count": 2}],
        )
        for record in audit["records"]:
            self.assertEqual(set(record), {"date", "legacyRowSha256", "missing", "status", "topic"})
            self.assertNotIn("line", record)

    def test_builds_bounded_hash_bound_recovery_request(self) -> None:
        audit = self._audit()
        request = audit["recoveryRequest"]
        items = request["items"]
        hashes = [item["legacyRowSha256"] for item in items]
        self.assertEqual(len(hashes), len(set(hashes)))
        self.assertIn(_row_hash("jt-confirmed-no-url"), hashes)
        self.assertIn(_row_hash("raw-false-remains-unknown"), hashes)
        self.assertNotIn(_row_hash("governed-decline"), hashes)
        for item in items:
            self.assertEqual(set(item), {"allowedAnswers", "date", "legacyRowSha256", "topic"})
            self.assertEqual(
                [answer["answer"] for answer in item["allowedAnswers"]],
                ["posted", "not_posted", "still_unknown"],
            )
            self.assertEqual(item["allowedAnswers"][0]["required"], ["publicUrl"])
            self.assertEqual(item["allowedAnswers"][0]["optional"], ["finalText"])

    def test_is_reproducible_and_never_mutates_the_source(self) -> None:
        before = FIXTURE.read_bytes()
        first = self._audit()
        second = self._audit()
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        self.assertEqual(FIXTURE.read_bytes(), before)
        self.assertEqual(first["sourceSha256"], sha256_hex(before))

    def test_fails_if_source_changes_during_audit(self) -> None:
        before = FIXTURE.read_bytes()
        original = Path.read_bytes

        def changing_read(path: Path) -> bytes:
            if path == FIXTURE:
                calls.append(path)
                return before if len(calls) == 1 else before + b" "
            return original(path)

        calls: list[Path] = []
        with mock.patch.object(Path, "read_bytes", changing_read):
            with self.assertRaisesRegex(RuntimeError, "changed during audit"):
                audit_legacy_rows(FIXTURE, None, GENERATED_AT)

    def test_parses_the_exact_bytes_bound_to_source_hash(self) -> None:
        injected = (
            FIXTURE.read_text(encoding="utf-8")
            + '{"date":"2026-09-30","platform":"linkedin","topic":"injected",'
            '"posted":true,"posted_confirmation":"JT_CONFIRMED_POSTED"}\n'
        )
        with mock.patch.object(Path, "read_text", return_value=injected):
            audit = audit_legacy_rows(FIXTURE, None, GENERATED_AT)
        self.assertNotIn("injected", {record["topic"] for record in audit["records"]})
        self.assertEqual(audit["sourceSha256"], sha256_hex(FIXTURE.read_bytes()))

    def test_legacy_urls_use_the_governed_strict_validator(self) -> None:
        invalid_urls = (
            "https://www.linkedin.com/posts/jt_bad\x00url",
            "https://www.linkedin.com/posts/jt bad",
            "https://www.linkedin.com/posts/jt\u00a0bad",
            "https://www.linkedin.com/posts/jt%post",
            "https://www.linkedin.com/posts/jt%2post",
            "https://www.linkedin.com/posts/jt%GGbad",
            "https://user@www.linkedin.com/posts/jt_bad",
            "https://www.linkedin.com:444/posts/jt_bad",
            "https://www.linkedin.com:99999/posts/jt_bad",
            "https://www.linkedin.com:notaport/posts/jt_bad",
            "https://linkedin.com.evil.example/posts/jt_bad",
            "https://evil-linkedin.com/posts/jt_bad",
            "https://www.linkedin.com/posts/jt_bad\n",
        )
        import json

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.jsonl"
            for index, url in enumerate(invalid_urls):
                row = {
                    "date": "2026-09-{:02d}".format(index + 1),
                    "platform": "linkedin",
                    "topic": "bad-url-{}".format(index),
                    "posted": True,
                    "public_url": url,
                }
                path.write_text(json.dumps(row) + "\n", encoding="utf-8")
                with self.subTest(url=repr(url)):
                    audit = audit_legacy_rows(path, None, GENERATED_AT)
                    self.assertEqual(audit["records"][0]["status"], "status_unknown")

    def test_invalid_or_noncanonical_dates_fail_closed(self) -> None:
        invalid_dates = ("2026-02-30", "2026-9-01", "09/01/2026", "")
        import json

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.jsonl"
            for date in invalid_dates:
                row = {
                    "date": date,
                    "platform": "linkedin",
                    "topic": "invalid-date",
                    "posted": False,
                }
                path.write_text(json.dumps(row) + "\n", encoding="utf-8")
                with self.subTest(date=date):
                    with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                        audit_legacy_rows(path, None, GENERATED_AT)

    def test_unknown_cap_counts_unique_hashes_before_slicing(self) -> None:
        import json

        rows = []
        for day in range(1, 22):
            rows.append(
                {
                    "date": "2026-09-{:02d}".format(day),
                    "platform": "linkedin",
                    "topic": "unknown-{:02d}".format(day),
                    "posted": False,
                }
            )
        rows.append(dict(rows[-1]))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.jsonl"
            path.write_text(
                "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )
            audit = audit_legacy_rows(path, None, GENERATED_AT)

        items = audit["recoveryRequest"]["items"]
        self.assertEqual(len(items), 20)
        self.assertEqual(len({item["legacyRowSha256"] for item in items}), 20)
        self.assertNotIn("unknown-01", {item["topic"] for item in items})
        self.assertEqual(audit["duplicateGroups"][0]["count"], 2)


if __name__ == "__main__":
    unittest.main()
