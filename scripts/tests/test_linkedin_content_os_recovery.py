from __future__ import annotations

import copy
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.outcomes import load_events
from scripts.linkedin_content_os.recovery import (
    ingest_human_gate,
    ingest_human_gate_files,
    rebuild_fixtures_files,
    rebuild_focus_files,
)


CONFIRMED_AT = "2026-09-28T17:29:32-04:00"
GENERATED_AT = "2026-09-28T17:00:00-04:00"


@contextmanager
def _working_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def _event_hash(event: dict[str, object]) -> str:
    return sha256_hex(canonical_bytes(event))


class LinkedInContentOSRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        owner = self.root / "memory/content/current-efforts.md"
        owner.parent.mkdir(parents=True)
        owner.write_text("# Current efforts\n\nPermissioned consulting proof.\n", encoding="utf-8")
        owner_hash = sha256_hex(owner.read_bytes())
        self.focus = {
            "schemaVersion": "linkedin-focus-snapshot.v1",
            "snapshotId": "",
            "generatedAt": GENERATED_AT,
            "validUntil": "2026-10-28T17:00:00-04:00",
            "targets": [{
                "targetId": "consulting-proof",
                "kind": "consulting",
                "label": "Permissioned consulting proof",
                "desiredOutcome": "Publish only permissioned proof",
                "sourceRefs": [{
                    "path": "memory/content/current-efforts.md",
                    "sha256": owner_hash,
                }],
            }],
            "prohibitedPremises": ["internal_machinery"],
            "status": "proposed",
        }
        focus_unhashed = {key: value for key, value in self.focus.items() if key != "snapshotId"}
        self.focus["snapshotId"] = "sha256:" + sha256_hex(canonical_bytes(focus_unhashed))
        self.request = {
            "schemaVersion": "linkedin-historical-recovery-request.v1",
            "generatedAt": GENERATED_AT,
            "sourceSha256": "9" * 64,
            "items": [
                {
                    "legacyRowSha256": "1" * 64,
                    "date": "2026-06-01",
                    "topic": "posted row",
                    "allowedAnswers": [
                        {"answer": "posted", "required": ["publicUrl"], "optional": ["finalText"]},
                        {"answer": "not_posted", "required": ["declineReason"], "allowedDeclineReasons": ["quality_fit", "stale", "timing", "other"]},
                        {"answer": "still_unknown", "required": []},
                    ],
                },
                {
                    "legacyRowSha256": "2" * 64,
                    "date": "2026-05-31",
                    "topic": "declined row",
                    "allowedAnswers": [
                        {"answer": "posted", "required": ["publicUrl"], "optional": ["finalText"]},
                        {"answer": "not_posted", "required": ["declineReason"], "allowedDeclineReasons": ["quality_fit", "stale", "timing", "other"]},
                        {"answer": "still_unknown", "required": []},
                    ],
                },
                {
                    "legacyRowSha256": "3" * 64,
                    "date": "2026-05-30",
                    "topic": "unknown row",
                    "allowedAnswers": [
                        {"answer": "posted", "required": ["publicUrl"], "optional": ["finalText"]},
                        {"answer": "not_posted", "required": ["declineReason"], "allowedDeclineReasons": ["quality_fit", "stale", "timing", "other"]},
                        {"answer": "still_unknown", "required": []},
                    ],
                },
            ],
        }
        self.fixture_gap = {
            "schemaVersion": "linkedin-evaluation-fixture.v1",
            "fixtureId": "cohort-two-coi-proof-v1",
            "mode": "build_proof",
            "classification": "gap",
            "sourceRefs": [],
            "gitObjectId": None,
            "contentSha256": None,
            "permissionState": "missing",
            "expectedGateResult": "block",
            "failureReason": "permission_missing",
            "claimBindings": [],
        }
        self.proof = {
            "schemaVersion": "permissioned-proof.v1",
            "proofId": "cohort-two-coi-proof-v1",
            "status": "verified",
            "verifiedAt": "2026-09-28T16:00:00-04:00",
            "facts": [{
                "factId": "proof-coi-reminder-routing",
                "conceptId": "coi-reminder-routing",
                "outboundText": "Certificate reminders and a staff-status digest.",
            }],
            "permission": {
                "status": "approved-anonymized",
                "evidenceRef": "jt:telegram:28031",
                "expiresAt": "2027-09-28T21:29:32Z",
            },
            "activeProspectConflict": False,
            "activeEmployerConflict": False,
            "protectedInternalPremise": False,
        }
        self.git_dir, self.commit, self.proof_path, self.proof_bytes = self._git_proof()
        self.ledger = self.root / "outcomes.jsonl"
        self.ledger.write_bytes(b"")
        self.run_context = {
            "schemaVersion": "linkedin-program-0-run-context.v1",
            "generatedAt": "2026-09-28T18:00:00-04:00",
        }
        self.run_context["runId"] = "sha256:" + sha256_hex(canonical_bytes(self.run_context))

    def _git_proof(self) -> tuple[Path, str, str, bytes]:
        repository = self.root / "jt-ops"
        subprocess.run(["git", "init", "-q", str(repository)], check=True)
        subprocess.run(["git", "-C", str(repository), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(repository), "config", "user.email", "test@example.com"], check=True)
        proof_path = "evidence/cohort-two.permissioned-proof.json"
        destination = repository / proof_path
        destination.parent.mkdir(parents=True)
        payload = canonical_bytes(self.proof)
        destination.write_bytes(payload)
        subprocess.run(["git", "-C", str(repository), "add", proof_path], check=True)
        subprocess.run(["git", "-C", str(repository), "commit", "-q", "-m", "proof"], check=True)
        commit = subprocess.check_output(["git", "-C", str(repository), "rev-parse", "HEAD"], text=True).strip()
        return repository / ".git", commit, proof_path, payload

    def response(self) -> dict[str, object]:
        permission = self.proof["permission"]
        assert isinstance(permission, dict)
        return {
            "schemaVersion": "linkedin-human-gate-response.v1",
            "recoveryRequestSha256": sha256_hex(canonical_bytes(self.request)),
            "focusSnapshotSha256": sha256_hex(canonical_bytes(self.focus)),
            "fixtureGapSha256": sha256_hex(canonical_bytes(self.fixture_gap)),
            "focusDecision": {"decision": "confirmed"},
            "historyAnswers": [
                {
                    "legacyRowSha256": "1" * 64,
                    "answer": "posted",
                    "publicUrl": "https://www.linkedin.com/posts/jt-real-activity-123",
                    "finalText": "The exact final LinkedIn text.",
                },
                {
                    "legacyRowSha256": "2" * 64,
                    "answer": "not_posted",
                    "declineReason": "quality_fit",
                },
                {"legacyRowSha256": "3" * 64, "answer": "still_unknown"},
            ],
            "permissionedFixture": {
                "proofId": "cohort-two-coi-proof-v1",
                "gitDir": str(self.git_dir),
                "commit": self.commit,
                "path": self.proof_path,
                "contentSha256": sha256_hex(self.proof_bytes),
                "permissionEvidenceRef": "/permission",
                "permissionEvidenceSha256": sha256_hex(canonical_bytes(permission)),
                "permissionStatus": "approved-anonymized",
            },
            "confirmedAt": CONFIRMED_AT,
        }

    def ingest(self, response=None):
        return ingest_human_gate(
            self.response() if response is None else response,
            self.request,
            self.focus,
            self.fixture_gap,
            self.ledger,
            run_context=self.run_context,
            workspace_root=self.root,
        )

    def test_ingests_complete_boundary_and_emits_valid_typed_events(self) -> None:
        result = self.ingest()
        events = load_events(self.ledger)
        self.assertEqual(result["appendedEventCount"], len(events))
        self.assertEqual(result["replayedEventCount"], 0)
        history = [event for event in events if event["eventType"] == "historical_status"]
        self.assertEqual(
            [event["payload"]["status"] for event in history],
            ["posted_confirmed", "not_posted_confirmed", "status_unknown"],
        )
        event_types = [event["eventType"] for event in events]
        self.assertEqual(event_types.count("focus_decision"), 1)
        self.assertEqual(event_types.count("permission_fixture_accepted"), 1)
        self.assertEqual(event_types.count("publication_acknowledged"), 1)
        self.assertEqual(event_types.count("corpus_authority_receipt"), 1)
        manifest = result["corpusAuthorityManifest"]
        self.assertEqual(manifest["receiptSha256Allowlist"], sorted(
            event["eventSha256"] for event in events
            if event["eventType"] == "corpus_authority_receipt"
        ))
        self.assertEqual(manifest["ledgerPosition"], len(events))
        self.assertEqual(manifest["ledgerPrefixSha256"], sha256_hex(self.ledger.read_bytes()))
        unhashed = {key: value for key, value in manifest.items() if key != "manifestSha256"}
        self.assertEqual(manifest["manifestSha256"], sha256_hex(canonical_bytes(unhashed)))
        authority = result["authorityRunContext"]
        self.assertEqual(authority["corpusAuthorityManifestSha256"], manifest["manifestSha256"])

    def test_required_five_argument_api_derives_a_closed_authority_context(self) -> None:
        with _working_directory(self.root):
            result = ingest_human_gate(
                self.response(), self.request, self.focus, self.fixture_gap, self.ledger
            )
        self.assertEqual(
            result["corpusAuthorityManifest"]["validatedAt"], CONFIRMED_AT
        )
        self.assertEqual(
            result["authorityRunContext"]["generatedAt"], CONFIRMED_AT
        )

    def test_requires_exact_complete_history_coverage(self) -> None:
        for mutate, pattern in (
            (lambda value: value["historyAnswers"].pop(), "coverage"),
            (lambda value: value["historyAnswers"].append(copy.deepcopy(value["historyAnswers"][0])), "duplicate"),
            (lambda value: value["historyAnswers"].__setitem__(0, {"legacyRowSha256": "4" * 64, "answer": "still_unknown"}), "coverage"),
        ):
            response = self.response()
            mutate(response)
            with self.subTest(pattern=pattern), self.assertRaisesRegex(ValueError, pattern):
                self.ingest(response)
            self.assertEqual(self.ledger.read_bytes(), b"")

    def test_rejects_hash_drift_nulls_unknown_fields_and_bad_answer_shapes(self) -> None:
        mutations = (
            (lambda value: value.__setitem__("recoveryRequestSha256", "0" * 64), "recovery request"),
            (lambda value: value.__setitem__("focusSnapshotSha256", "0" * 64), "focus snapshot"),
            (lambda value: value.__setitem__("fixtureGapSha256", "0" * 64), "fixture gap"),
            (lambda value: value.__setitem__("extra", True), "unknown fields"),
            (lambda value: value["focusDecision"].__setitem__("extra", None), "null|unknown fields"),
            (lambda value: value["historyAnswers"][2].__setitem__("publicUrl", "https://www.linkedin.com/posts/invalid-extra"), "unknown fields"),
            (lambda value: value["historyAnswers"][1].__setitem__("declineReason", "later"), "declineReason"),
            (lambda value: value["historyAnswers"][0].__setitem__("publicUrl", "https://example.com/post"), "LinkedIn"),
        )
        for mutate, pattern in mutations:
            response = self.response()
            mutate(response)
            with self.subTest(pattern=pattern), self.assertRaisesRegex(ValueError, pattern):
                self.ingest(response)
            self.assertEqual(self.ledger.read_bytes(), b"")

    def test_validates_full_focus_correction_against_owner_bytes(self) -> None:
        response = self.response()
        corrected = copy.deepcopy(self.focus["targets"])
        corrected[0]["label"] = "Corrected consulting proof"
        response["focusDecision"] = {"decision": "corrected", "correctedTargets": corrected}
        result = self.ingest(response)
        focus_event = next(
            event for event in result["events"] if event["eventType"] == "focus_decision"
        )
        self.assertEqual(focus_event["payload"]["decision"], "corrected")
        self.assertIn("replacementFocusSnapshotSha256", focus_event["payload"])

        bad = self.response()
        bad_targets = copy.deepcopy(corrected)
        bad_targets[0]["sourceRefs"][0]["sha256"] = "0" * 64
        bad["focusDecision"] = {"decision": "corrected", "correctedTargets": bad_targets}
        self.ledger.write_bytes(b"")
        with self.assertRaisesRegex(ValueError, "source hash mismatch"):
            self.ingest(bad)

    def test_posted_without_final_text_has_no_text_authority_receipt(self) -> None:
        response = self.response()
        del response["historyAnswers"][0]["finalText"]
        result = self.ingest(response)
        events = result["events"]
        publication = next(event for event in events if event["eventType"] == "publication_acknowledged")
        self.assertNotIn("finalText", publication["payload"])
        self.assertFalse(any(event["eventType"] == "corpus_authority_receipt" for event in events))
        self.assertEqual(result["corpusAuthorityManifest"]["receiptSha256Allowlist"], [])

    def test_permission_fixture_uses_exact_shell_free_git_argv_and_closed_evidence(self) -> None:
        response = self.response()
        real_run = subprocess.run
        calls: list[list[str]] = []

        def recording_run(argv, **kwargs):
            calls.append(list(argv))
            return real_run(argv, **kwargs)

        with mock.patch("scripts.linkedin_content_os.recovery.subprocess.run", side_effect=recording_run):
            self.ingest(response)
        self.assertEqual(calls, [[
            "git", "--git-dir", str(self.git_dir), "show",
            "{}:{}".format(self.commit, self.proof_path),
        ]])

        mutations = (
            (lambda value: value["permissionedFixture"].__setitem__("contentSha256", "0" * 64), "content SHA-256"),
            (lambda value: value["permissionedFixture"].__setitem__("permissionEvidenceRef", "/facts/0"), "permissionEvidenceRef"),
            (lambda value: value["permissionedFixture"].__setitem__("permissionEvidenceSha256", "0" * 64), "permission evidence"),
            (lambda value: value["permissionedFixture"].__setitem__("permissionStatus", "internal-only"), "permissionStatus"),
            (lambda value: value["permissionedFixture"].__setitem__("path", "../proof.json"), "safe"),
        )
        for mutate, pattern in mutations:
            self.ledger.write_bytes(b"")
            value = self.response()
            mutate(value)
            with self.subTest(pattern=pattern), self.assertRaisesRegex(ValueError, pattern):
                self.ingest(value)

        self.ledger.write_bytes(b"")
        expired = self.response()
        document = copy.deepcopy(self.proof)
        document["permission"]["expiresAt"] = CONFIRMED_AT
        # The immutable bytes still contain a later expiry; changing only the response
        # cannot forge expiry or status authority.
        expired["permissionedFixture"]["permissionEvidenceSha256"] = sha256_hex(
            canonical_bytes(document["permission"])
        )
        with self.assertRaisesRegex(ValueError, "permission evidence"):
            self.ingest(expired)

    def test_exact_replay_is_idempotent_and_conflicting_replay_is_refused(self) -> None:
        first = self.ingest()
        prefix = self.ledger.read_bytes()
        second = self.ingest()
        self.assertEqual(self.ledger.read_bytes(), prefix)
        self.assertEqual(second["appendedEventCount"], 0)
        self.assertEqual(second["replayedEventCount"], len(first["events"]))

        conflict = self.response()
        conflict["historyAnswers"][2] = {
            "legacyRowSha256": "3" * 64,
            "answer": "not_posted",
            "declineReason": "stale",
        }
        with self.assertRaisesRegex(ValueError, "conflict|different"):
            self.ingest(conflict)
        self.assertEqual(self.ledger.read_bytes(), prefix)

    def test_append_failure_restores_the_exact_original_prefix(self) -> None:
        sentinel = {
            "schemaVersion": "linkedin-content-outcome.v1",
            "outcomeEventId": "sentinel",
            "packetId": "sentinel",
            "eventType": "historical_status",
            "recordedAt": "2026-09-28T16:00:00-04:00",
            "sourcePointer": {
                "sourceType": "jt_confirmation",
                "sourceId": "sentinel",
                "sourceSha256": "8" * 64,
            },
            "payload": {"legacyRowSha256": "8" * 64, "status": "status_unknown"},
        }
        sentinel["eventSha256"] = _event_hash(sentinel)
        original = canonical_bytes(sentinel) + b"\n"
        self.ledger.write_bytes(original)
        from scripts.linkedin_content_os import recovery
        real_append = recovery._append_jsonl_exact_prefix_locked
        count = 0

        def fail_after_one(path, row, expected_prefix=None):
            nonlocal count
            count += 1
            real_append(path, row, expected_prefix=expected_prefix)
            if count == 2:
                raise RuntimeError("injected append failure")

        with mock.patch.object(recovery, "_append_jsonl_exact_prefix_locked", side_effect=fail_after_one):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                self.ingest()
        self.assertEqual(self.ledger.read_bytes(), original)

    def test_file_handlers_emit_authority_outputs_and_rebuild_deterministically(self) -> None:
        artifacts = self.root / "memory/content/linkedin-content-os"
        artifacts.mkdir(parents=True, exist_ok=True)
        response_path = artifacts / "human-gate-response.v1.json"
        request_path = artifacts / "historical-recovery-request.phase-1.v1.json"
        focus_path = artifacts / "focus-snapshot.phase-1.v1.json"
        fixtures_path = artifacts / "evaluation-fixtures.phase-1.v0.jsonl"
        context_path = artifacts / "run-context.v1.json"
        response_path.write_bytes(canonical_bytes(self.response()))
        request_path.write_bytes(canonical_bytes(self.request))
        focus_path.write_bytes(canonical_bytes(self.focus))
        negative = {"schemaVersion": "linkedin-evaluation-fixture.v1", "fixtureId": "negative", "mode": "internal_machinery", "classification": "negative"}
        teardown = {"schemaVersion": "linkedin-evaluation-fixture.v1", "fixtureId": "teardown-gap", "mode": "company_teardown", "classification": "gap"}
        fixtures_path.write_bytes(b"".join(canonical_bytes(row) + b"\n" for row in (negative, self.fixture_gap, teardown)))
        context_path.write_bytes(canonical_bytes(self.run_context))
        manifest_path = artifacts / "corpus-authority-manifest.v1.json"
        authority_path = artifacts / "run-context.phase-2-authority.v1.json"

        import argparse
        ingest_args = argparse.Namespace(
            response=str(response_path), recovery_request=str(request_path),
            focus=str(focus_path), fixtures=str(fixtures_path), outcomes=str(self.ledger),
            corpus_authority_manifest_output=str(manifest_path),
            authority_run_context_output=str(authority_path), run_context=str(context_path),
            workspace_root=str(self.root),
        )
        result = ingest_human_gate_files(ingest_args)
        self.assertEqual(manifest_path.read_bytes(), canonical_bytes(result["corpusAuthorityManifest"]))
        self.assertEqual(authority_path.read_bytes(), canonical_bytes(result["authorityRunContext"]))

        focus_output = artifacts / "focus-snapshot.v1.json"
        focus_args = argparse.Namespace(
            workspace_root=str(self.root), outcomes=str(self.ledger),
            run_context=str(context_path), output=str(focus_output),
        )
        first_focus = rebuild_focus_files(focus_args)
        second_focus = rebuild_focus_files(focus_args)
        self.assertEqual(first_focus, second_focus)
        self.assertEqual(first_focus["status"], "confirmed")

        fixture_output = artifacts / "evaluation-fixtures.v0.jsonl"
        fixture_args = argparse.Namespace(
            human_gate_response=str(response_path), output=str(fixture_output),
            workspace_root=str(self.root),
        )
        first_fixtures = rebuild_fixtures_files(fixture_args)
        first_bytes = fixture_output.read_bytes()
        second_fixtures = rebuild_fixtures_files(fixture_args)
        self.assertEqual(first_fixtures, second_fixtures)
        self.assertEqual(fixture_output.read_bytes(), first_bytes)
        positive = next(row for row in first_fixtures["fixtures"] if row.get("mode") == "build_proof")
        self.assertEqual(positive["classification"], "positive")
        self.assertEqual(first_fixtures["fixtures"][0], negative)
        self.assertEqual(first_fixtures["fixtures"][-1], teardown)


if __name__ == "__main__":
    unittest.main()
