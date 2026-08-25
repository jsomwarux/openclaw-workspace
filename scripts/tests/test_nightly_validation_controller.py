import importlib.util
import json
import tempfile
import unittest
import hashlib
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "nightly_validation_controller.py"
WORKSPACE = Path(__file__).resolve().parents[2]


def load_controller():
    if not MODULE_PATH.exists():
        return None
    spec = importlib.util.spec_from_file_location("nightly_validation_controller", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class NightlyValidationControllerTests(unittest.TestCase):
    def setUp(self):
        self.controller = load_controller()
        self.assertIsNotNone(
            self.controller,
            "nightly_validation_controller.py must implement the tested contract",
        )
        self.now = datetime(2026, 8, 24, 23, 15, tzinfo=timezone.utc)

    def candidate(self, **overrides):
        evidence_path = WORKSPACE / "memory/agent-portfolio/evidence/fixtures/evidence-a.json"
        record = {
            "candidate_id": "candidate-a",
            "lane": "workflow",
            "score": 80,
            "status": "pending",
            "not_before": "2026-08-24T20:00:00Z",
            "source_hash": "sha256:" + hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
            "evidence_path": str(evidence_path),
            "evidence_timestamp": "2026-08-24T22:00:00Z",
        }
        record.update(overrides)
        return record

    def validation_result(self, candidate=None, **overrides):
        candidate = candidate or self.candidate()
        record = {
            "candidateId": candidate["candidate_id"],
            "sourceHash": candidate["source_hash"],
            "verdict": "promote",
            "verifierConfirmed": True,
            "verifiedAt": "2026-08-24T23:00:00Z",
            "score": 34,
            "evidenceScore": 4,
            "distributionScore": 3,
            "fatalConstraint": False,
            "question": "Will this produce a priced conversation?",
            "sourcesChecked": ["fixture-source"],
            "evidenceFound": "A bounded buyer signal exists.",
            "falsificationResult": "No disqualifying evidence found.",
            "artifactPaths": [candidate["evidence_path"]],
            "decision": "promote",
            "confidence": "medium",
            "nextTrigger": "JT reviews the evidence.",
            "title": "Validate workflow offer",
            "firstAction": "Open the validation artifact.",
            "whyItMatters": "A buyer signal passed deterministic gates.",
            "doneState": "JT records a go/no-go decision.",
            "workstream": "compounding-bet",
        }
        record.update(overrides)
        return record

    def test_load_jsonl_rejects_malformed_line_with_line_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "queue.jsonl"
            queue.write_text('{"candidate_id":"ok"}\n{bad json}\n', encoding="utf-8")
            with self.assertRaisesRegex(self.controller.ControllerError, r"line 2"):
                self.controller.load_candidates(queue)

    def test_load_jsonl_rejects_missing_required_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "queue.jsonl"
            queue.write_text(json.dumps({"candidate_id": "incomplete"}) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(self.controller.ControllerError, r"line 1.*lane"):
                self.controller.load_candidates(queue)

    def test_selection_uses_highest_candidate_lane_and_caps_at_three(self):
        candidates = [
            self.candidate(candidate_id="a", source_hash="sha256:a", score=90, lane="workflow"),
            self.candidate(candidate_id="b", source_hash="sha256:b", score=85, lane="workflow"),
            self.candidate(candidate_id="c", source_hash="sha256:c", score=80, lane="workflow"),
            self.candidate(candidate_id="d", source_hash="sha256:d", score=75, lane="workflow"),
            self.candidate(candidate_id="other", source_hash="sha256:e", score=89, lane="content"),
        ]
        selected = self.controller.select_candidates(candidates, self.now, set())
        self.assertEqual([item["candidate_id"] for item in selected], ["a", "b", "c"])

    def test_selection_skips_future_nonpending_and_processed_hashes(self):
        candidates = [
            self.candidate(candidate_id="processed", source_hash="sha256:done", score=99),
            self.candidate(candidate_id="future", source_hash="sha256:future", score=98,
                           not_before="2026-08-25T00:00:00Z"),
            self.candidate(candidate_id="archived", source_hash="sha256:archived", score=97,
                           status="archived"),
            self.candidate(candidate_id="eligible", source_hash="sha256:new", score=70),
        ]
        selected = self.controller.select_candidates(candidates, self.now, {"sha256:done"})
        self.assertEqual([item["candidate_id"] for item in selected], ["eligible"])

    def test_empty_eligible_set_returns_no_qualified_validation(self):
        result = self.controller.build_run_result([], self.now)
        self.assertEqual(result["status"], "NO_QUALIFIED_VALIDATION")
        self.assertEqual(result["selected"], [])

    def test_non_dry_no_work_records_completed_state_without_run_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_path = root / "state.md"
            runs_dir = root / "runs"
            result = self.controller.admit_candidates([], self.now, state_path, runs_dir, False)
            self.assertEqual(result["status"], "NO_QUALIFIED_VALIDATION")
            self.assertTrue(state_path.exists())
            text = state_path.read_text(encoding="utf-8")
            self.assertIn("last_status: NO_QUALIFIED_VALIDATION", text)
            self.assertIn("last_completed_run: 2026-08-24T23:15:00Z", text)
            self.assertIn("next_run: 2026-08-25T03:15:00Z", text)
            self.assertFalse(runs_dir.exists())

    def test_strict_result_gate_requires_scores_confirmation_and_full_schema(self):
        candidate = self.candidate()
        valid = self.validation_result(candidate)
        self.assertTrue(self.controller.validate_result(candidate, valid, self.now))
        for change in (
            {"verifierConfirmed": False}, {"verdict": "continue"}, {"score": 29},
            {"evidenceScore": 3}, {"distributionScore": 2}, {"fatalConstraint": True},
            {"verifiedAt": "2026-08-20T00:00:00Z"},
        ):
            invalid = dict(valid)
            invalid.update(change)
            with self.subTest(change=change):
                self.assertFalse(self.controller.validate_result(candidate, invalid, self.now))

    def test_result_gate_rejects_hash_mismatch_and_unapproved_evidence_root(self):
        candidate = self.candidate(source_hash="sha256:" + "0" * 64)
        self.assertFalse(self.controller.validate_result(candidate, self.validation_result(candidate), self.now))
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "evidence.json"
            outside.write_text("{}", encoding="utf-8")
            digest = hashlib.sha256(outside.read_bytes()).hexdigest()
            candidate = self.candidate(evidence_path=str(outside), source_hash=f"sha256:{digest}")
            with self.assertRaisesRegex(self.controller.ControllerError, "approved public"):
                self.controller.validate_result(candidate, self.validation_result(candidate), self.now)

    def test_strict_promotions_are_deterministic_and_capped_at_one(self):
        first = self.candidate(candidate_id="a")
        second = self.candidate(candidate_id="b")
        promotions = self.controller.build_strict_promotions(
            [first, second],
            [self.validation_result(second, score=31), self.validation_result(first, score=39)],
            self.now,
        )
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0]["candidateId"], "a")

    def test_task_payload_uses_full_camel_case_admission_contract(self):
        payload = self.controller.build_admission_payload(
            self.validation_result(), "memory/agent-portfolio/runs/run/promotions.json"
        )
        self.assertEqual(payload["sourceSystem"], "nightly-validation-controller")
        self.assertEqual(payload["dedupeKey"].split(":", 1)[0], "nightly-validation")
        self.assertEqual(payload["promotionScore"], 34)
        self.assertEqual(payload["firstAction"], "Open the validation artifact.")
        self.assertEqual(payload["whyItMatters"], "A buyer signal passed deterministic gates.")
        self.assertEqual(payload["doneState"], "JT records a go/no-go decision.")
        self.assertEqual(payload["evidenceLinks"], ["memory/agent-portfolio/runs/run/promotions.json"])
        for field in ("verdict", "verifierConfirmed", "verifiedAt", "candidateId",
                      "sourceHash", "evidenceScore", "distributionScore", "fatalConstraint"):
            self.assertEqual(payload[field], self.validation_result()[field])
        self.assertNotIn("dedupe_key", payload)

    def test_consume_rejects_raw_or_tampered_promotion_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw.json"
            raw.write_text(json.dumps([self.validation_result()]), encoding="utf-8")
            with self.assertRaisesRegex(self.controller.ControllerError, "controller-produced"):
                self.controller.load_promotion_artifact(raw, self.now)

    def test_admission_does_not_process_hash_until_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.md"
            artifact = self.controller.admit_candidates(
                [self.candidate()], self.now, state, root / "runs", dry_run=False
            )
            self.assertEqual(self.controller.read_processed_hashes(state), set())
            self.assertTrue(Path(artifact["admissionPath"]).exists())

    def test_unique_admissions_preserve_artifact_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.md"
            first = self.controller.admit_candidates([self.candidate()], self.now, state, root / "runs", False)
            second = self.controller.admit_candidates([self.candidate()], self.now, state, root / "runs", False)
            self.assertNotEqual(first["admissionPath"], second["admissionPath"])
            self.assertEqual(len(self.controller.read_state(state)["artifacts"]), 2)

    def test_post_task_uses_json_post_and_returns_upsert_response(self):
        received = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received["path"] = self.path
                received["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                body = json.dumps({"success": True, "created": True, "id": "task-1"}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            payload = self.controller.build_admission_payload(self.validation_result(), "artifact.json")
            result = self.controller.post_task(payload, f"http://127.0.0.1:{server.server_port}/api/tasks")
        finally:
            server.shutdown()
            thread.join()
            server.server_close()
        self.assertTrue(result["success"])
        self.assertEqual(received["path"], "/api/tasks")
        self.assertEqual(received["body"]["dedupeKey"], payload["dedupeKey"])

    def test_record_failure_preserves_retryable_artifact_and_appends_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.md"
            promotion = root / "promotion.json"
            promotion.write_text("{}", encoding="utf-8")
            self.controller.record_failure(state, self.now, "Mission Control unavailable", str(promotion))
            self.assertTrue(promotion.exists())
            saved = self.controller.read_state(state)
            self.assertEqual(saved["failures"][0]["artifact"], str(promotion))

    def test_promotion_artifact_detects_post_reconciliation_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.md"
            admission_result = self.controller.admit_candidates(
                [self.candidate()], self.now, state, root / "runs", False
            )
            results = root / "results.jsonl"
            results.write_text(json.dumps(self.validation_result()) + "\n", encoding="utf-8")
            reconciled = self.controller.reconcile_results(
                Path(admission_result["admissionPath"]), results, self.now, state, False
            )
            promotion_path = Path(reconciled["promotionPath"])
            artifact = json.loads(promotion_path.read_text(encoding="utf-8"))
            artifact["promotions"][0]["score"] = 40
            promotion_path.write_text(json.dumps(artifact), encoding="utf-8")
            with self.assertRaisesRegex(self.controller.ControllerError, "integrity"):
                self.controller.load_promotion_artifact(promotion_path, self.now)

    def test_incomplete_reconciliation_leaves_selected_hash_unprocessed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.md"
            admission_result = self.controller.admit_candidates(
                [self.candidate()], self.now, state, root / "runs", False
            )
            empty_results = root / "results.jsonl"
            empty_results.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(self.controller.ControllerError, "incomplete"):
                self.controller.reconcile_results(
                    Path(admission_result["admissionPath"]), empty_results, self.now, state, False
                )
            self.assertEqual(self.controller.read_processed_hashes(state), set())

    def test_malformed_result_types_raise_before_gate_comparisons(self):
        candidate = self.candidate()
        for change in (
            {"score": "34"}, {"verifierConfirmed": 1}, {"sourcesChecked": "source"},
            {"artifactPaths": [3]}, {"fatalConstraint": "false"},
            {"confidence": "certain"},
        ):
            malformed = self.validation_result(candidate, **change)
            with self.subTest(change=change), self.assertRaises(self.controller.ControllerError):
                self.controller.validate_result(candidate, malformed, self.now)

    def test_unknown_fields_are_rejected_for_candidates_and_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "queue.jsonl"
            queue.write_text(json.dumps(self.candidate(privateNotes="secret")) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(self.controller.ControllerError, "unexpected field"):
                self.controller.load_candidates(queue)
        with self.assertRaisesRegex(self.controller.ControllerError, "unexpected field"):
            self.controller.validate_result(
                self.candidate(), self.validation_result(privateNotes="secret"), self.now
            )

    def test_private_markers_in_evidence_prevent_promotion(self):
        private_path = WORKSPACE / "memory/agent-portfolio/evidence/fixtures/private-marker.json"
        candidate = self.candidate(
            evidence_path=str(private_path),
            source_hash="sha256:" + hashlib.sha256(private_path.read_bytes()).hexdigest(),
        )
        with self.assertRaisesRegex(self.controller.ControllerError, "private marker"):
            self.controller.validate_result(candidate, self.validation_result(candidate), self.now)


if __name__ == "__main__":
    unittest.main()
