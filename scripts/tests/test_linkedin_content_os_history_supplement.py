from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.historical_audit import _governed_evidence, corpus_run_id
from scripts.linkedin_content_os.outcomes import load_events
from scripts.linkedin_content_os.recovery import (
    derive_history_supplement,
    ingest_history_supplement_files,
    ingest_human_gate_files,
)


BASE_CONFIRMED_AT = "2026-09-28T17:29:32-04:00"
BASE_GENERATED_AT = "2026-09-28T18:00:00-04:00"
SUPPLEMENT_CONFIRMED_AT = "2026-09-30T09:01:38-04:00"
SUPPLEMENT_GENERATED_AT = "2026-09-30T09:30:00-04:00"
URL = "https://www.linkedin.com/feed/update/urn:li:activity:7490053069380964353/"
FINAL_TEXT = (
    "A delinquency balance should not move without a decision trail.\n\n"
    "• source report or queue\n• final outcome and proof path\n\n"
    "hashtag#AIImplementation"
)
ROW_POSTED = "1" * 64
ROW_DECLINED = "2" * 64
ROW_UNKNOWN = "3" * 64
_ALLOWED = [
    {"answer": "posted", "required": ["publicUrl"], "optional": ["finalText"]},
    {
        "answer": "not_posted",
        "required": ["declineReason"],
        "allowedDeclineReasons": ["quality_fit", "stale", "timing", "other"],
    },
    {"answer": "still_unknown", "required": []},
]


def _context(generated_at: str) -> dict[str, object]:
    unsigned = {"schemaVersion": "linkedin-program-0-run-context.v1", "generatedAt": generated_at}
    return {**unsigned, "runId": "sha256:" + sha256_hex(canonical_bytes(unsigned))}


class HistorySupplementTests(unittest.TestCase):
    """Supplemental human-gate corrections append governed authority without rewriting history."""

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.artifacts = self.root / "memory/content/linkedin-content-os"
        self.artifacts.mkdir(parents=True)
        owner = self.root / "memory/content/current-efforts.md"
        owner.write_text("# Current efforts\n\nPermissioned consulting proof.\n", encoding="utf-8")
        owner_hash = sha256_hex(owner.read_bytes())
        previous_directory = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, previous_directory)
        self.request = {
            "schemaVersion": "linkedin-historical-recovery-request.v1",
            "generatedAt": "2026-09-28T17:00:00-04:00",
            "sourceSha256": "9" * 64,
            "items": [
                {"legacyRowSha256": ROW_POSTED, "date": "2026-06-01", "topic": "posted row", "allowedAnswers": _ALLOWED},
                {"legacyRowSha256": ROW_DECLINED, "date": "2026-05-31", "topic": "declined row", "allowedAnswers": _ALLOWED},
                {"legacyRowSha256": ROW_UNKNOWN, "date": "2026-05-30", "topic": "unknown row", "allowedAnswers": _ALLOWED},
            ],
        }
        self.focus = {
            "schemaVersion": "linkedin-focus-snapshot.v1",
            "snapshotId": "",
            "generatedAt": "2026-09-28T17:00:00-04:00",
            "validUntil": "2026-10-28T17:00:00-04:00",
            "targets": [{
                "targetId": "consulting-proof",
                "kind": "consulting",
                "label": "Permissioned consulting proof",
                "desiredOutcome": "Publish only permissioned proof",
                "sourceRefs": [{"path": "memory/content/current-efforts.md", "sha256": owner_hash}],
            }],
            "prohibitedPremises": ["internal_machinery"],
            "status": "proposed",
        }
        unhashed = {key: value for key, value in self.focus.items() if key != "snapshotId"}
        self.focus["snapshotId"] = "sha256:" + sha256_hex(canonical_bytes(unhashed))
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
        self.permission = {
            "status": "approved-anonymized",
            "evidenceRef": "jt:telegram:28031",
            "expiresAt": "2027-09-28T21:29:32Z",
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
            "permission": self.permission,
            "activeProspectConflict": False,
            "activeEmployerConflict": False,
            "protectedInternalPremise": False,
        }
        self.git_dir, self.commit, self.proof_path, self.proof_bytes = self._git_proof()
        self.ledger = self.artifacts / "outcomes.v1.jsonl"
        self.ledger.write_bytes(b"")
        self.base_paths = self._ingest_base(self._base_response())
        self.base_ledger_bytes = self.ledger.read_bytes()
        self.supplement_context_path = self.artifacts / "run-context.supplement-1.v1.json"
        self.supplement_context_path.write_bytes(canonical_bytes(_context(SUPPLEMENT_GENERATED_AT)))
        self.supplement_path = self.artifacts / "human-gate-supplement-1.v1.json"
        self.manifest_output = self.artifacts / "corpus-authority-manifest.supplement-1.v1.json"
        self.context_output = self.artifacts / "run-context.supplement-1-authority.v1.json"

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

    def _base_response(self, *, posted_final_text: bool = False) -> dict[str, object]:
        posted: dict[str, object] = {"legacyRowSha256": ROW_POSTED, "answer": "posted", "publicUrl": "https://www.linkedin.com/posts/jt-real-activity-123"}
        if posted_final_text:
            posted["finalText"] = "The exact final LinkedIn text."
        return {
            "schemaVersion": "linkedin-human-gate-response.v1",
            "recoveryRequestSha256": sha256_hex(canonical_bytes(self.request)),
            "focusSnapshotSha256": sha256_hex(canonical_bytes(self.focus)),
            "fixtureGapSha256": sha256_hex(canonical_bytes(self.fixture_gap)),
            "focusDecision": {"decision": "confirmed"},
            "historyAnswers": [
                posted,
                {"legacyRowSha256": ROW_DECLINED, "answer": "not_posted", "declineReason": "quality_fit"},
                {"legacyRowSha256": ROW_UNKNOWN, "answer": "still_unknown"},
            ],
            "permissionedFixture": {
                "proofId": "cohort-two-coi-proof-v1",
                "gitDir": str(self.git_dir),
                "commit": self.commit,
                "path": self.proof_path,
                "contentSha256": sha256_hex(self.proof_bytes),
                "permissionEvidenceRef": "/permission",
                "permissionEvidenceSha256": sha256_hex(canonical_bytes(self.permission)),
                "permissionStatus": "approved-anonymized",
            },
            "confirmedAt": BASE_CONFIRMED_AT,
        }

    def _ingest_base(self, response: dict[str, object]) -> dict[str, Path]:
        paths = {
            "response": self.artifacts / "human-gate-response.v1.json",
            "request": self.artifacts / "historical-recovery-request.phase-1.v1.json",
            "focus": self.artifacts / "focus-snapshot.phase-1.v1.json",
            "fixtures": self.artifacts / "evaluation-fixtures.phase-1.v0.jsonl",
            "context": self.artifacts / "run-context.v1.json",
            "manifest": self.artifacts / "corpus-authority-manifest.v1.json",
            "authority": self.artifacts / "run-context.phase-2-authority.v1.json",
        }
        paths["response"].write_bytes(canonical_bytes(response) + b"\n")
        paths["request"].write_bytes(canonical_bytes(self.request))
        paths["focus"].write_bytes(canonical_bytes(self.focus))
        negative = {"schemaVersion": "linkedin-evaluation-fixture.v1", "fixtureId": "negative", "mode": "internal_machinery", "classification": "negative"}
        paths["fixtures"].write_bytes(b"".join(canonical_bytes(row) + b"\n" for row in (negative, self.fixture_gap)))
        paths["context"].write_bytes(canonical_bytes(_context(BASE_GENERATED_AT)))
        ingest_human_gate_files(argparse.Namespace(
            response=str(paths["response"]), recovery_request=str(paths["request"]),
            focus=str(paths["focus"]), fixtures=str(paths["fixtures"]), outcomes=str(self.ledger),
            corpus_authority_manifest_output=str(paths["manifest"]),
            authority_run_context_output=str(paths["authority"]),
            focus_authority_receipt_output=str(self.artifacts / "focus-authority-receipt.v1.json"),
            focus_authority_anchor_output=str(self.artifacts / "focus-authority-anchor.v1.json"),
            run_context=str(paths["context"]), workspace_root=str(self.root),
        ))
        return paths

    def _target(self, row: str) -> dict[str, object]:
        return next(event for event in load_events(self.ledger) if event["outcomeEventId"] == "history:" + row)

    def _supplement(self, **overrides: object) -> dict[str, object]:
        target = self._target(ROW_UNKNOWN)
        value: dict[str, object] = {
            "schemaVersion": "linkedin-human-gate-supplement.v1",
            "supplementId": "supplement-1",
            "baseResponseSha256": sha256_hex(self.base_paths["response"].read_bytes()),
            "baseManifestSha256": json.loads(self.base_paths["manifest"].read_text(encoding="utf-8"))["manifestSha256"],
            "corrections": [{
                "legacyRowSha256": ROW_UNKNOWN,
                "targetOutcomeEventId": "history:" + ROW_UNKNOWN,
                "targetEventSha256": target["eventSha256"],
                "answer": "posted",
                "publicUrl": URL,
                "finalText": FINAL_TEXT,
            }],
            "confirmedAt": SUPPLEMENT_CONFIRMED_AT,
        }
        value.update(overrides)
        return value

    def _args(self, document: dict[str, object] | None = None, **overrides: object) -> argparse.Namespace:
        if document is not None or not self.supplement_path.exists():
            self.supplement_path.write_bytes(canonical_bytes(self._supplement() if document is None else document))
        values: dict[str, object] = {
            "supplement": str(self.supplement_path),
            "base_response": str(self.base_paths["response"]),
            "base_manifest": str(self.base_paths["manifest"]),
            "base_authority_run_context": str(self.base_paths["authority"]),
            "recovery_request": str(self.base_paths["request"]),
            "outcomes": str(self.ledger),
            "run_context": str(self.supplement_context_path),
            "corpus_authority_manifest_output": str(self.manifest_output),
            "authority_run_context_output": str(self.context_output),
            "workspace_root": str(self.root),
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def _assert_unchanged(self) -> None:
        self.assertEqual(self.ledger.read_bytes(), self.base_ledger_bytes)
        self.assertFalse(self.manifest_output.exists())
        self.assertFalse(self.context_output.exists())

    def test_appends_replacement_publication_receipt_and_correction_without_rewriting(self) -> None:
        result = ingest_history_supplement_files(self._args())
        ledger_bytes = self.ledger.read_bytes()
        self.assertTrue(ledger_bytes.startswith(self.base_ledger_bytes))
        events = load_events(self.ledger)
        base_count = len(self.base_ledger_bytes.splitlines())
        block = events[base_count:]
        self.assertEqual(
            [event["outcomeEventId"] for event in block],
            [
                "history-supplement-1:" + ROW_UNKNOWN,
                "publication-supplement-1:" + ROW_UNKNOWN,
                "authority-supplement-1:" + ROW_UNKNOWN,
                "correction-supplement-1:" + ROW_UNKNOWN,
            ],
        )
        target = self._target(ROW_UNKNOWN)
        self.assertEqual(target["payload"]["status"], "status_unknown")
        replacement, publication, receipt, correction = block
        supplement_hash = sha256_hex(self.supplement_path.read_bytes())
        self.assertEqual(replacement["payload"], {"legacyRowSha256": ROW_UNKNOWN, "status": "posted_confirmed"})
        self.assertEqual(replacement["recordedAt"], SUPPLEMENT_CONFIRMED_AT)
        self.assertEqual(replacement["sourcePointer"]["sourceSha256"], supplement_hash)
        self.assertEqual(publication["payload"]["publicationUrl"], URL)
        self.assertEqual(publication["payload"]["finalTextSha256"], sha256_hex(FINAL_TEXT.encode("utf-8")))
        self.assertEqual(correction["eventType"], "correction")
        self.assertEqual(correction["recordedAt"], SUPPLEMENT_GENERATED_AT)
        self.assertEqual(
            correction["payload"],
            {
                "targetOutcomeEventId": "history:" + ROW_UNKNOWN,
                "replacementEventSha256": replacement["eventSha256"],
                "reason": "jt-human-gate-supplement:supplement-1",
            },
        )
        run_id = corpus_run_id(str(self.request["sourceSha256"]), SUPPLEMENT_GENERATED_AT)
        self.assertEqual(receipt["payload"]["runId"], run_id)
        self.assertEqual(receipt["payload"]["rawAuthoritySha256"], supplement_hash)
        self.assertEqual(receipt["payload"]["textOutcomeEventId"], publication["outcomeEventId"])
        self.assertEqual(receipt["payload"]["textOutcomeEventSha256"], publication["eventSha256"])
        self.assertEqual(receipt["payload"]["ledgerPosition"], base_count + 2)
        manifest = json.loads(self.manifest_output.read_text(encoding="utf-8"))
        self.assertEqual(manifest["runId"], run_id)
        self.assertEqual(manifest["validatedAt"], SUPPLEMENT_GENERATED_AT)
        self.assertEqual(manifest["humanGateAuthorityReceiptSha256"], supplement_hash)
        self.assertEqual(manifest["receiptSha256Allowlist"], [receipt["eventSha256"]])
        self.assertEqual(manifest["ledgerPosition"], len(events))
        self.assertEqual(manifest["ledgerPrefixSha256"], sha256_hex(ledger_bytes))
        context = json.loads(self.context_output.read_text(encoding="utf-8"))
        self.assertEqual(context["corpusAuthorityManifestSha256"], manifest["manifestSha256"])
        self.assertEqual(context["generatedAt"], SUPPLEMENT_GENERATED_AT)
        evidence = _governed_evidence(self.ledger)[ROW_UNKNOWN]
        self.assertEqual(evidence["status"], "posted_confirmed")
        self.assertEqual(evidence["publicUrl"], URL)
        self.assertEqual(evidence["finalText"], FINAL_TEXT)
        self.assertEqual(result["appendedEventCount"], 4)
        self.assertEqual(result["replayedEventCount"], 0)

    def test_derivation_is_deterministic_and_pure(self) -> None:
        supplement = self._supplement()
        raw = canonical_bytes(supplement)
        kwargs = dict(
            supplement=supplement,
            supplement_sha256=sha256_hex(raw),
            base_response=json.loads(self.base_paths["response"].read_text(encoding="utf-8")),
            base_response_sha256=sha256_hex(self.base_paths["response"].read_bytes()),
            base_manifest=json.loads(self.base_paths["manifest"].read_text(encoding="utf-8")),
            base_authority_context=json.loads(self.base_paths["authority"].read_text(encoding="utf-8")),
            request=self.request,
            prior_events=load_events(self.ledger),
            run_context=_context(SUPPLEMENT_GENERATED_AT),
        )
        first = derive_history_supplement(**kwargs)
        second = derive_history_supplement(**copy.deepcopy(kwargs))
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        self.assertEqual(self.ledger.read_bytes(), self.base_ledger_bytes)

    def test_exact_replay_is_zero_write(self) -> None:
        ingest_history_supplement_files(self._args())
        snapshots = {
            path: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in (self.ledger, self.manifest_output, self.context_output)
        }
        result = ingest_history_supplement_files(self._args())
        self.assertEqual(result["appendedEventCount"], 0)
        self.assertEqual(result["replayedEventCount"], 4)
        for path, (payload, mtime) in snapshots.items():
            self.assertEqual(path.read_bytes(), payload)
            self.assertEqual(path.stat().st_mtime_ns, mtime)

    def test_conflicting_replay_is_rejected_without_writes(self) -> None:
        ingest_history_supplement_files(self._args())
        before = {path: path.read_bytes() for path in (self.ledger, self.manifest_output, self.context_output)}
        changed = self._supplement()
        changed["corrections"][0]["finalText"] = FINAL_TEXT + " Edited."
        with self.assertRaisesRegex(ValueError, "conflict"):
            ingest_history_supplement_files(self._args(changed))
        self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_partial_prior_state_is_refused(self) -> None:
        ingest_history_supplement_files(self._args())
        self.context_output.unlink()
        with self.assertRaisesRegex(ValueError, "partial"):
            ingest_history_supplement_files(self._args())
        self.assertFalse(self.context_output.exists())

    def test_output_publish_failure_rolls_back_every_byte(self) -> None:
        from scripts.linkedin_content_os import recovery

        original_replace = recovery.os.replace
        calls = {"count": 0}

        def failing_replace(source: str, destination: str) -> None:
            calls["count"] += 1
            if calls["count"] == 2:
                raise OSError("injected supplement publish failure")
            original_replace(source, destination)

        self._args()
        with mock.patch.object(recovery.os, "replace", side_effect=failing_replace):
            with self.assertRaisesRegex(OSError, "injected supplement publish failure"):
                ingest_history_supplement_files(self._args())
        self._assert_unchanged()

    def test_rejects_stale_or_misordered_contexts(self) -> None:
        cases = (
            (_context(SUPPLEMENT_CONFIRMED_AT), None, "run context"),
            (_context("2026-09-30T09:00:00-04:00"), None, "run context"),
            (None, {"confirmedAt": "2026-09-28T17:00:00-04:00"}, "predates|stale"),
        )
        for context, overrides, pattern in cases:
            with self.subTest(pattern=pattern, context=context, overrides=overrides):
                if context is not None:
                    self.supplement_context_path.write_bytes(canonical_bytes(context))
                else:
                    self.supplement_context_path.write_bytes(canonical_bytes(_context(SUPPLEMENT_GENERATED_AT)))
                supplement = self._supplement(**(overrides or {}))
                with self.assertRaisesRegex(ValueError, pattern):
                    ingest_history_supplement_files(self._args(supplement))
                self._assert_unchanged()

    def test_rejects_base_and_target_hash_mismatches(self) -> None:
        mutations = (
            (lambda value: value.__setitem__("baseResponseSha256", "0" * 64), "base response"),
            (lambda value: value.__setitem__("baseManifestSha256", "0" * 64), "base manifest"),
            (lambda value: value["corrections"][0].__setitem__("targetEventSha256", "0" * 64), "target"),
            (lambda value: value["corrections"][0].__setitem__("targetOutcomeEventId", "history:" + ROW_DECLINED), "target"),
            (lambda value: value["corrections"][0].__setitem__("legacyRowSha256", "4" * 64), "request|target"),
        )
        for mutate, pattern in mutations:
            supplement = self._supplement()
            mutate(supplement)
            with self.subTest(pattern=pattern), self.assertRaisesRegex(ValueError, pattern):
                ingest_history_supplement_files(self._args(supplement))
            self._assert_unchanged()

    def test_rejects_wrong_event_type_and_packet(self) -> None:
        publication = next(event for event in load_events(self.ledger) if event["outcomeEventId"] == "publication:" + ROW_POSTED)
        supplement = self._supplement()
        supplement["corrections"][0].update({
            "legacyRowSha256": ROW_POSTED,
            "targetOutcomeEventId": "publication:" + ROW_POSTED,
            "targetEventSha256": publication["eventSha256"],
            "answer": "not_posted",
            "declineReason": "stale",
        })
        for key in ("publicUrl", "finalText"):
            del supplement["corrections"][0][key]
        with self.assertRaisesRegex(ValueError, "target"):
            ingest_history_supplement_files(self._args(supplement))
        self._assert_unchanged()

    def test_rejects_no_op_and_correction_chains(self) -> None:
        no_op = self._supplement()
        no_op["corrections"][0] = {
            "legacyRowSha256": ROW_UNKNOWN,
            "targetOutcomeEventId": "history:" + ROW_UNKNOWN,
            "targetEventSha256": self._target(ROW_UNKNOWN)["eventSha256"],
            "answer": "still_unknown",
        }
        with self.assertRaisesRegex(ValueError, "no-op|unchanged"):
            ingest_history_supplement_files(self._args(no_op))
        self._assert_unchanged()

        ingest_history_supplement_files(self._args(self._supplement()))
        self.manifest_output.unlink()
        self.context_output.unlink()
        after_first = self.ledger.read_bytes()
        second_manifest = self.artifacts / "corpus-authority-manifest.supplement-2.v1.json"
        second_context = self.artifacts / "run-context.supplement-2-authority.v1.json"
        replacement = next(
            event for event in load_events(self.ledger)
            if event["outcomeEventId"] == "history-supplement-1:" + ROW_UNKNOWN
        )
        for target_id, target_hash, pattern in (
            ("history:" + ROW_UNKNOWN, self._target(ROW_UNKNOWN)["eventSha256"], "already corrected|latest"),
            ("history-supplement-1:" + ROW_UNKNOWN, replacement["eventSha256"], "chain|base history"),
        ):
            second = self._supplement(supplementId="supplement-2")
            second["corrections"][0].update({
                "targetOutcomeEventId": target_id,
                "targetEventSha256": target_hash,
                "answer": "not_posted",
                "declineReason": "other",
            })
            for key in ("publicUrl", "finalText"):
                del second["corrections"][0][key]
            with self.subTest(target=target_id), self.assertRaisesRegex(ValueError, pattern):
                ingest_history_supplement_files(self._args(
                    second,
                    corpus_authority_manifest_output=str(second_manifest),
                    authority_run_context_output=str(second_context),
                ))
            self.assertEqual(self.ledger.read_bytes(), after_first)
            self.assertFalse(second_manifest.exists())

    def test_rejects_malformed_partial_null_and_unknown_fields(self) -> None:
        mutations = (
            (lambda value: value.__setitem__("extra", True), "unknown fields"),
            (lambda value: value.pop("confirmedAt"), "missing fields"),
            (lambda value: value.__setitem__("corrections", []), "corrections"),
            (lambda value: value.__setitem__("supplementId", "Supplement One"), "supplementId"),
            (lambda value: value.__setitem__("schemaVersion", "linkedin-human-gate-supplement.v2"), "schemaVersion"),
            (lambda value: value["corrections"][0].__setitem__("declineReason", "stale"), "unknown fields"),
            (lambda value: value["corrections"][0].__setitem__("finalText", None), "null"),
            (lambda value: value["corrections"][0].__setitem__("publicUrl", "https://example.com/post"), "LinkedIn"),
            (lambda value: value["corrections"].append(copy.deepcopy(value["corrections"][0])), "duplicate"),
        )
        for mutate, pattern in mutations:
            supplement = self._supplement()
            mutate(supplement)
            with self.subTest(pattern=pattern), self.assertRaisesRegex(ValueError, pattern):
                ingest_history_supplement_files(self._args(supplement))
            self._assert_unchanged()

    def test_rejects_base_ledgers_that_already_carry_corpus_receipts(self) -> None:
        self.ledger.write_bytes(b"")
        for path in self.base_paths.values():
            if path.name.startswith(("corpus-authority-manifest", "run-context.phase-2")):
                path.unlink()
        (self.artifacts / "focus-authority-receipt.v1.json").unlink()
        (self.artifacts / "focus-authority-anchor.v1.json").unlink()
        self.base_paths = self._ingest_base(self._base_response(posted_final_text=True))
        self.base_ledger_bytes = self.ledger.read_bytes()
        with self.assertRaisesRegex(ValueError, "authority receipt"):
            ingest_history_supplement_files(self._args(self._supplement()))
        self._assert_unchanged()

    def test_rejects_symlinked_escaping_and_aliased_paths(self) -> None:
        link = self.artifacts / "supplement-link.json"
        self._args()
        link.symlink_to(self.supplement_path)
        with self.assertRaisesRegex(ValueError, "symlink"):
            ingest_history_supplement_files(self._args(supplement=str(link)))
        self._assert_unchanged()

        outside_directory = tempfile.TemporaryDirectory()
        self.addCleanup(outside_directory.cleanup)
        outside = Path(outside_directory.name).resolve() / "manifest.json"
        with self.assertRaisesRegex(ValueError, "workspace"):
            ingest_history_supplement_files(self._args(corpus_authority_manifest_output=str(outside)))
        self._assert_unchanged()
        self.assertFalse(outside.exists())

        with self.assertRaisesRegex(ValueError, "alias"):
            ingest_history_supplement_files(
                self._args(corpus_authority_manifest_output=str(self.base_paths["manifest"]))
            )
        self.assertEqual(self.ledger.read_bytes(), self.base_ledger_bytes)


if __name__ == "__main__":
    unittest.main()
