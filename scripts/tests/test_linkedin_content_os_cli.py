from __future__ import annotations

import argparse
import copy
import json
import socket
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.historical_audit import audit_legacy_rows, corpus_run_id
from scripts.linkedin_content_os.boundaries import (
    build_authority_consumption_receipt,
    build_boundary_artifact,
    normalize_cron_definitions,
    validate_authority_consumption_receipt,
    validate_boundary_artifact,
)
from scripts.linkedin_content_os.cli import (
    COMMANDS,
    _parser,
    _network_denied,
    _process_guard,
    _primary_checkout_fingerprint,
    _validate_distinct_paths,
    init_run,
    main,
)


GENERATED_AT = "2026-09-28T16:00:00+00:00"


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class LinkedInContentOSCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_exact_command_surface(self) -> None:
        self.assertEqual(
            COMMANDS,
            (
                "init-run",
                "capture-boundaries",
                "audit-history",
                "ingest-human-gate",
                "build-focus",
                "build-corpus",
                "build-fixtures",
                "build-source-policy",
                "audit-voice-rules",
                "preview-checkin",
                "verify",
            ),
        )

    def test_init_run_creates_one_canonical_context_and_preserves_ledger(self) -> None:
        output = self.root / "run-context.json"
        ledger = self.root / "outcomes.jsonl"
        ledger.write_bytes(b'{"preserved":true}\n')

        first = init_run(GENERATED_AT, ledger, output)
        before = ledger.read_bytes()
        second = init_run(GENERATED_AT, ledger, output)

        self.assertEqual(first, second)
        self.assertEqual(ledger.read_bytes(), before)
        self.assertEqual(_read_json(output), first)
        self.assertEqual(set(first), {"schemaVersion", "runId", "generatedAt"})
        self.assertEqual(first["schemaVersion"], "linkedin-program-0-run-context.v1")
        self.assertRegex(str(first["runId"]), r"^sha256:[0-9a-f]{64}$")

    def test_init_run_now_uses_one_clock_read(self) -> None:
        output = self.root / "run-context.json"
        ledger = self.root / "outcomes.jsonl"
        instant = datetime(2026, 9, 28, 16, 0, tzinfo=timezone.utc)
        with mock.patch(
            "scripts.linkedin_content_os.cli._utc_now", return_value=instant
        ) as clock:
            context = init_run("now", ledger, output)
        clock.assert_called_once_with()
        self.assertEqual(context["generatedAt"], instant.isoformat())
        self.assertEqual(ledger.read_bytes(), b"")

    def test_phase_two_transition_uses_distinct_paths_and_preserves_phase_one(self) -> None:
        phase1_context = self.root / "run-context.phase-1.json"
        phase1_outcomes = self.root / "outcomes.phase-1.jsonl"
        phase2_context = self.root / "run-context.json"
        phase2_outcomes = self.root / "outcomes.jsonl"
        phase1_outcomes.write_bytes(b'{"phase":1}\n')
        init_run("2026-09-28T15:00:00+00:00", phase1_outcomes, phase1_context)
        phase1_bytes = (phase1_context.read_bytes(), phase1_outcomes.read_bytes())

        init_run(GENERATED_AT, phase2_outcomes, phase2_context)

        self.assertEqual(
            (phase1_context.read_bytes(), phase1_outcomes.read_bytes()), phase1_bytes
        )
        self.assertNotEqual(_read_json(phase1_context)["runId"], _read_json(phase2_context)["runId"])
        self.assertEqual(phase2_outcomes.read_bytes(), b"")

    def test_cli_emits_json_and_denies_network_for_non_capture_commands(self) -> None:
        output = self.root / "run-context.json"
        ledger = self.root / "outcomes.jsonl"
        with mock.patch("socket.socket.connect") as connect, mock.patch(
            "socket.create_connection"
        ) as create_connection:
            result = main(
                [
                    "init-run",
                    "--generated-at",
                    GENERATED_AT,
                    "--outcomes",
                    str(ledger),
                    "--output",
                    str(output),
                ]
            )
        self.assertEqual(result["schemaVersion"], "linkedin-program-0-run-context.v1")
        connect.assert_not_called()
        create_connection.assert_not_called()

    def test_runtime_guards_deny_network_and_nonallowlisted_children(self) -> None:
        with _network_denied():
            with self.assertRaisesRegex(RuntimeError, "network"):
                socket.create_connection(("example.com", 443))
        with _process_guard("init-run"):
            for call in (
                lambda: subprocess.run(["true"]),
                lambda: subprocess.Popen(["true"]),
                lambda: subprocess.call(["true"]),
                lambda: subprocess.check_call(["true"]),
                lambda: subprocess.check_output(["true"]),
            ):
                with self.assertRaisesRegex(RuntimeError, "prohibited|allowlisted"):
                    call()

    def test_build_fixture_guard_allows_only_pipe_captured_read_only_git_show(self) -> None:
        argv = [
            "git", "--git-dir", str(self.root / "missing.git"), "show",
            "1" * 40 + ":evidence/proof.json",
        ]
        with _process_guard("build-fixtures"):
            result = subprocess.run(
                argv,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertNotEqual(result.returncode, 0)
            with self.assertRaisesRegex(RuntimeError, "options are not allowlisted"):
                subprocess.run(
                    argv,
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                )

    def test_phase_two_exact_argv_parses_without_pre_gate_git_arguments(self) -> None:
        parser = _parser()
        fixtures = parser.parse_args([
            "build-fixtures", "--decagon-packet", "mission-control/lib/mission-control/fixtures/jobs/decagon-agent-development-manager.packet.json",
            "--human-gate-response", "human-gate.json", "--output", "fixtures.jsonl",
        ])
        self.assertEqual(fixtures.human_gate_response, "human-gate.json")
        self.assertIsNone(fixtures.jt_ops_git_dir)
        with self.assertRaises(SystemExit):
            parser.parse_args([
                "build-fixtures", "--decagon-packet", "packet.json",
                "--generated-at", GENERATED_AT, "--output", "fixtures.jsonl",
            ])

    def test_phase_two_handlers_are_real_and_fail_closed_without_gate_artifacts(self) -> None:
        context = self.root / "run-context.json"
        ledger = self.root / "outcomes.jsonl"
        init_run(GENERATED_AT, ledger, context)
        with self.assertRaisesRegex(ValueError, "required artifact"):
            main([
                "build-focus", "--workspace-root", str(self.root), "--outcomes", str(ledger),
                "--run-context", str(context), "--output", str(self.root / "focus.json"),
            ])
        with self.assertRaisesRegex(ValueError, "required artifact"):
            main([
                "build-fixtures", "--decagon-packet", "mission-control/lib/mission-control/fixtures/jobs/decagon-agent-development-manager.packet.json",
                "--human-gate-response", str(self.root / "response.json"),
                "--output", str(self.root / "fixtures.jsonl"),
            ])

    def test_phase_two_exact_argv_dispatches_to_lazy_task_7b_handlers(self) -> None:
        context = self.root / "run-context.json"
        ledger = self.root / "outcomes.jsonl"
        init_run(GENERATED_AT, ledger, context)
        observed: list[tuple[str, argparse.Namespace]] = []

        def handler(name: str):
            def invoke(args: argparse.Namespace) -> dict[str, object]:
                observed.append((name, args))
                return {"handler": name}
            return invoke

        with mock.patch(
            "scripts.linkedin_content_os.recovery.rebuild_focus_files",
            side_effect=handler("focus"),
        ), mock.patch(
            "scripts.linkedin_content_os.recovery.rebuild_fixtures_files",
            side_effect=handler("fixtures"),
        ), mock.patch(
            "scripts.linkedin_content_os.recovery.ingest_human_gate_files",
            side_effect=handler("ingest"),
        ), mock.patch("sys.stdout.write"):
            main([
                "build-focus", "--workspace-root", str(self.root), "--outcomes", str(ledger),
                "--run-context", str(context), "--output", str(self.root / "focus.json"),
            ])
            main([
                "build-fixtures", "--decagon-packet", "mission-control/lib/mission-control/fixtures/jobs/decagon-agent-development-manager.packet.json",
                "--human-gate-response", str(self.root / "response.json"),
                "--output", str(self.root / "fixtures.jsonl"),
            ])
            main([
                "ingest-human-gate", "--response", str(self.root / "response.json"),
                "--recovery-request", str(self.root / "recovery.json"), "--focus", str(self.root / "focus-input.json"),
                "--fixtures", str(self.root / "fixture-input.jsonl"), "--outcomes", str(ledger),
                "--corpus-authority-manifest-output", str(self.root / "manifest.json"),
                "--authority-run-context-output", str(self.root / "authority.json"),
                "--run-context", str(context),
            ])
        self.assertEqual([name for name, _ in observed], ["focus", "fixtures", "ingest"])
        self.assertEqual(observed[0][1].outcomes, str(ledger))
        self.assertEqual(observed[1][1].human_gate_response, str(self.root / "response.json"))

    def test_build_fixtures_rejects_noncanonical_decagon_packet(self) -> None:
        with self.assertRaisesRegex(ValueError, "reviewed Decagon packet"):
            main([
                "build-fixtures", "--decagon-packet", "packet.json",
                "--human-gate-response", str(self.root / "response.json"),
                "--output", str(self.root / "fixtures.jsonl"),
            ])

    def test_build_fixtures_resolves_workspace_root_before_git_extraction(self) -> None:
        context = self.root / "run-context.json"
        outcomes = self.root / "outcomes.jsonl"
        output = self.root / "fixtures.jsonl"
        init_run(GENERATED_AT, outcomes, context)
        relative_root = Path("relative-workspace")
        with mock.patch(
            "scripts.linkedin_content_os.cli.build_evaluation_fixtures",
            return_value=[],
        ) as build, mock.patch("sys.stdout.write"):
            main([
                "build-fixtures",
                "--decagon-packet",
                "mission-control/lib/mission-control/fixtures/jobs/decagon-agent-development-manager.packet.json",
                "--jt-ops-git-dir", str(self.root / "jt-ops.git"),
                "--jt-ops-commit", "cd3e17f5287a64dbfedc27e1d2153d89250ba02c",
                "--jt-ops-path", "evidence/cohort-two.proof-asset.json",
                "--run-context", str(context),
                "--workspace-root", str(relative_root),
                "--output", str(output),
            ])
        self.assertEqual(build.call_args.args[0], relative_root.resolve())

    def test_rejects_input_output_and_receipt_aliases_before_write(self) -> None:
        source = self.root / "source.json"
        alias = self.root / "alias.json"
        source.write_text("source", encoding="utf-8")
        alias.symlink_to(source)
        with self.assertRaisesRegex(ValueError, "alias"):
            _validate_distinct_paths(
                inputs=[source], outputs=[alias], receipts=[], workspace_root=self.root
            )
        self.assertEqual(source.read_text(encoding="utf-8"), "source")

    def test_build_corpus_rejects_receipt_output_alias_before_any_write(self) -> None:
        context = self.root / "run-context.json"
        outcomes = self.root / "outcomes.jsonl"
        audit = self.root / "audit.json"
        gold = self.root / "gold.jsonl"
        pairs = self.root / "pairs.jsonl"
        init_run(GENERATED_AT, outcomes, context)
        audit.write_bytes(canonical_bytes({"corpusAuthorityManifest": {"manifestSha256": "a" * 64}}))
        gold.write_bytes(b"sentinel\n")
        with mock.patch("scripts.linkedin_content_os.cli.load_events", return_value=[]), mock.patch(
            "scripts.linkedin_content_os.cli.build_voice_gold", return_value=[]
        ), mock.patch(
            "scripts.linkedin_content_os.cli.build_contrastive_pairs", return_value=[]
        ):
            with self.assertRaisesRegex(ValueError, "alias"):
                main([
                    "build-corpus", "--audit", str(audit), "--outcomes", str(outcomes),
                    "--run-context", str(context), "--gold-output", str(gold),
                    "--pairs-output", str(pairs), "--receipt-output", str(gold),
                    "--workspace-root", str(self.root),
                ])
        self.assertEqual(gold.read_bytes(), b"sentinel\n")
        self.assertFalse(pairs.exists())

    def test_build_corpus_prevalidates_receipt_before_replacing_any_output(self) -> None:
        context = self.root / "run-context.json"
        outcomes = self.root / "outcomes.jsonl"
        audit = self.root / "audit.json"
        gold = self.root / "gold.jsonl"
        pairs = self.root / "pairs.jsonl"
        receipt = self.root / "receipt.json"
        init_run(GENERATED_AT, outcomes, context)
        audit.write_bytes(canonical_bytes({"corpusAuthorityManifest": {"manifestSha256": "invalid"}}))
        gold.write_bytes(b"gold-sentinel\n")
        pairs.write_bytes(b"pair-sentinel\n")
        with mock.patch("scripts.linkedin_content_os.cli.load_events", return_value=[]), mock.patch(
            "scripts.linkedin_content_os.cli.build_voice_gold", return_value=[]
        ), mock.patch(
            "scripts.linkedin_content_os.cli.build_contrastive_pairs", return_value=[]
        ), mock.patch("sys.stdout.write"):
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                main([
                    "build-corpus", "--audit", str(audit), "--outcomes", str(outcomes),
                    "--run-context", str(context), "--gold-output", str(gold),
                    "--pairs-output", str(pairs), "--receipt-output", str(receipt),
                    "--workspace-root", str(self.root),
                ])
        self.assertEqual(gold.read_bytes(), b"gold-sentinel\n")
        self.assertEqual(pairs.read_bytes(), b"pair-sentinel\n")
        self.assertFalse(receipt.exists())

    def test_build_corpus_passes_audit_and_events_in_each_builder_contract_order(self) -> None:
        context = self.root / "run-context.json"
        outcomes = self.root / "outcomes.jsonl"
        audit = self.root / "audit.json"
        gold = self.root / "gold.jsonl"
        pairs = self.root / "pairs.jsonl"
        receipt = self.root / "receipt.json"
        init_run(GENERATED_AT, outcomes, context)
        audit_value = {
            "corpusAuthorityManifest": {"manifestSha256": "a" * 64},
        }
        audit.write_bytes(canonical_bytes(audit_value))
        events = [{"eventType": "sentinel"}]
        with mock.patch(
            "scripts.linkedin_content_os.cli.load_events", return_value=events
        ), mock.patch(
            "scripts.linkedin_content_os.cli.build_voice_gold", return_value=[]
        ) as build_gold, mock.patch(
            "scripts.linkedin_content_os.cli.build_contrastive_pairs", return_value=[]
        ) as build_pairs, mock.patch(
            "scripts.linkedin_content_os.cli._build_receipt", return_value={"receipt": "ok"}
        ), mock.patch("sys.stdout.write"):
            main([
                "build-corpus", "--audit", str(audit), "--outcomes", str(outcomes),
                "--run-context", str(context), "--gold-output", str(gold),
                "--pairs-output", str(pairs), "--receipt-output", str(receipt),
                "--workspace-root", str(self.root),
            ])
        build_gold.assert_called_once_with(
            audit_value, events, expected_manifest_sha256=None
        )
        build_pairs.assert_called_once_with(
            events, audit_value, expected_manifest_sha256=None
        )

    def test_capture_boundaries_performs_one_scoped_capture_and_writes_artifact(self) -> None:
        context_path = self.root / "run-context.json"
        outcomes = self.root / "outcomes.jsonl"
        init_run(GENERATED_AT, outcomes, context_path)
        for relative in ("memory/content/posted-log.jsonl", "memory/content/edit-deltas.jsonl"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"")
        output = self.root / "boundary.json"
        snapshot = {
            "totalTaskCount": 0, "linkedinLanePacketCount": 0, "packets": [],
            "projectionSha256": "9" * 64,
        }
        with mock.patch("scripts.linkedin_content_os.cli.capture_tasks", return_value=b"raw") as capture, mock.patch(
            "scripts.linkedin_content_os.cli.validate_snapshot", return_value=snapshot
        ) as validate, mock.patch("scripts.linkedin_content_os.cli._cron_list", return_value={"jobs": []}), mock.patch(
            "scripts.linkedin_content_os.cli._launchagent_inventory", return_value=[]
        ), mock.patch(
            "scripts.linkedin_content_os.cli._primary_checkout_fingerprint", return_value="8" * 64
        ), mock.patch("sys.stdout.write"):
            result = main([
                "capture-boundaries", "--phase", "phase-1-before",
                "--run-context", str(context_path), "--workspace-root", str(self.root),
                "--output", str(output),
            ])
        capture.assert_called_once_with("http://127.0.0.1:3000/api/tasks")
        validate.assert_called_once_with(
            b"raw",
            {"runId": _read_json(context_path)["runId"], "generatedAt": GENERATED_AT},
        )
        self.assertEqual(_read_json(output), result)

    def test_primary_checkout_fingerprint_covers_status_without_exposing_paths(self) -> None:
        git_dir = self.root / ".git"
        git_dir.mkdir()
        (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (git_dir / "index").write_bytes(b"index")
        (self.root / "secret-file").write_bytes(b"tracked-content")
        (self.root / "untracked-secret").write_bytes(b"untracked-content")
        completed = subprocess.CompletedProcess(
            ["git"], 0, stdout=b" M secret-file\x00?? untracked-secret\x00", stderr=b""
        )
        fingerprint = _primary_checkout_fingerprint(
            self.root, runner=mock.Mock(return_value=completed)
        )
        self.assertRegex(fingerprint, r"^[0-9a-f]{64}$")
        self.assertNotIn("secret", fingerprint)

    def test_primary_checkout_fingerprint_changes_when_dirty_bytes_change_under_same_status(self) -> None:
        git_dir = self.root / ".git"
        git_dir.mkdir()
        (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (git_dir / "index").write_bytes(b"index")
        dirty = self.root / "tracked.txt"
        dirty.write_bytes(b"version-one")
        completed = subprocess.CompletedProcess(
            ["git"], 0, stdout=b" M tracked.txt\x00", stderr=b""
        )
        runner = mock.Mock(return_value=completed)

        first = _primary_checkout_fingerprint(self.root, runner=runner)
        dirty.write_bytes(b"version-two")
        second = _primary_checkout_fingerprint(self.root, runner=runner)

        self.assertNotEqual(first, second)
        self.assertEqual(runner.call_count, 2)

    def test_capture_guard_allows_one_exact_capture_and_denies_other_network(self) -> None:
        from scripts.linkedin_content_os.cli import _capture_network_guard

        with _capture_network_guard() as exact_get:
            self.assertEqual(exact_get(lambda: b"{}"), b"{}")
            with self.assertRaisesRegex(RuntimeError, "network"):
                socket.create_connection(("example.com", 443))
            with self.assertRaisesRegex(RuntimeError, "exactly one"):
                exact_get(lambda: b"{}")


class AuthorityConsumptionReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.run_context = self.root / "run-context.json"
        self.audit = self.root / "audit.json"
        self.outcomes = self.root / "outcomes.jsonl"
        self.gold = self.root / "gold.jsonl"
        self.pairs = self.root / "pairs.jsonl"
        for path, payload in (
            (
                self.run_context,
                canonical_bytes(
                    {
                        "schemaVersion": "linkedin-program-0-run-context.v1",
                        "runId": "sha256:" + "0" * 64,
                        "generatedAt": GENERATED_AT,
                    }
                ),
            ),
            (self.audit, b'{"audit":1}'),
            (self.outcomes, b""),
            (self.gold, b'{"gold":1}\n'),
            (self.pairs, b'{"pair":1}\n'),
        ):
            path.write_bytes(payload)

    def _bindings(self, *items: tuple[str, Path]) -> list[dict[str, object]]:
        return [
            {
                "role": role,
                "path": path.name,
                "sha256": sha256_hex(path.read_bytes()),
            }
            for role, path in sorted(items)
        ]

    def _receipt(self) -> dict[str, object]:
        return build_authority_consumption_receipt(
            command="build-corpus",
            run_context_sha256=sha256_hex(self.run_context.read_bytes()),
            expected_manifest_sha256=None,
            canonical_manifest_sha256="a" * 64,
            inputs=self._bindings(
                ("audit", self.audit),
                ("outcomes", self.outcomes),
                ("run_context", self.run_context),
            ),
            outputs=self._bindings(
                ("contrastive_pairs", self.pairs),
                ("voice_gold", self.gold),
            ),
            generated_at=GENERATED_AT,
        )

    def test_receipt_is_closed_deterministic_and_hash_bound(self) -> None:
        receipt = self._receipt()
        self.assertEqual(receipt, self._receipt())
        self.assertEqual(
            set(receipt),
            {
                "schemaVersion",
                "command",
                "runContextSha256",
                "expectedManifestSha256",
                "canonicalManifestSha256",
                "inputs",
                "outputs",
                "generatedAt",
                "receiptSha256",
            },
        )
        self.assertIsNone(receipt["expectedManifestSha256"])
        self.assertEqual(validate_authority_consumption_receipt(receipt), receipt)

    def test_rejects_wrong_roles_order_duplicates_paths_hashes_and_tampering(self) -> None:
        receipt = self._receipt()
        cases: list[dict[str, object]] = []
        unknown = copy.deepcopy(receipt)
        unknown["extra"] = True
        cases.append(unknown)
        reordered = copy.deepcopy(receipt)
        reordered["inputs"] = list(reversed(reordered["inputs"]))
        cases.append(reordered)
        duplicate = copy.deepcopy(receipt)
        duplicate["outputs"] = duplicate["outputs"] + [duplicate["outputs"][0]]
        cases.append(duplicate)
        bad_path = copy.deepcopy(receipt)
        bad_path["inputs"][0]["path"] = "../escape"
        cases.append(bad_path)
        bad_hash = copy.deepcopy(receipt)
        bad_hash["inputs"][0]["sha256"] = "A" * 64
        cases.append(bad_hash)
        wrong_role = copy.deepcopy(receipt)
        wrong_role["inputs"][0]["role"] = "posted_log"
        cases.append(wrong_role)
        phase_two_null = copy.deepcopy(receipt)
        phase_two_null["command"] = "audit-history"
        cases.append(phase_two_null)
        tampered = copy.deepcopy(receipt)
        tampered["generatedAt"] = "2026-09-29T16:00:00+00:00"
        cases.append(tampered)
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_authority_consumption_receipt(value)

    def test_bound_byte_change_is_detected(self) -> None:
        receipt = self._receipt()
        self.gold.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "bound.*hash"):
            validate_authority_consumption_receipt(
                receipt, workspace_root=self.root
            )

    def test_receipt_revalidation_rejects_symlink_escape(self) -> None:
        outside = Path(self.temporary.name).parent / (self.root.name + "-outside")
        outside.mkdir(exist_ok=True)
        self.addCleanup(lambda: outside.rmdir() if outside.exists() else None)
        payload = outside / "audit.json"
        payload.write_bytes(self.audit.read_bytes())
        self.addCleanup(lambda: payload.unlink(missing_ok=True))
        (self.root / "escape").symlink_to(outside, target_is_directory=True)
        receipt = self._receipt()
        audit_binding = next(
            item for item in receipt["inputs"] if item["role"] == "audit"
        )
        audit_binding["path"] = "escape/audit.json"
        audit_binding["sha256"] = sha256_hex(payload.read_bytes())
        receipt["inputs"] = sorted(receipt["inputs"], key=lambda item: (item["role"], item["path"]))
        unsigned = {key: value for key, value in receipt.items() if key != "receiptSha256"}
        receipt["receiptSha256"] = sha256_hex(canonical_bytes(unsigned))
        with self.assertRaisesRegex(ValueError, "escapes|symlink"):
            validate_authority_consumption_receipt(receipt, workspace_root=self.root)


class BoundaryArtifactTests(unittest.TestCase):
    def test_cron_normalization_keeps_only_stable_nonsecret_configuration(self) -> None:
        raw = {
            "jobs": [
                {
                    "id": "job-1",
                    "name": "Example",
                    "enabled": True,
                    "schedule": {"kind": "cron", "expr": "0 9 * * *", "tz": "UTC"},
                    "sessionTarget": "isolated",
                    "wakeMode": "now",
                    "payload": {"kind": "agentTurn", "message": "bounded"},
                    "delivery": {"mode": "none"},
                    "lastRunAt": 1,
                    "nextRunAt": 2,
                    "errors": ["transient"],
                }
            ]
        }
        normalized = normalize_cron_definitions(raw)
        job = normalized["jobs"][0]
        self.assertEqual(set(job), {
            "id", "name", "enabled", "schedule", "sessionTarget",
            "wakeMode", "payloadSha256", "deliveryMode", "deliveryTargetSha256",
        })
        self.assertNotIn("lastRunAt", canonical_bytes(normalized).decode())
        webhook = copy.deepcopy(raw)
        webhook["jobs"][0]["delivery"] = {
            "mode": "webhook", "to": "https://hooks.slack.example/secret/path"
        }
        protected = normalize_cron_definitions(webhook)
        serialized = canonical_bytes(protected).decode("utf-8")
        self.assertNotIn("hooks.slack", serialized)
        self.assertRegex(protected["jobs"][0]["deliveryTargetSha256"], r"^[0-9a-f]{64}$")
        secret = copy.deepcopy(raw)
        secret["jobs"][0]["payload"] = {"token": "should-not-be-here"}
        with self.assertRaisesRegex(ValueError, "secret"):
            normalize_cron_definitions(secret)

    def test_boundary_artifact_hashes_minimal_snapshot_and_protected_files(self) -> None:
        snapshot = {
            "schemaVersion": "linkedin-mc-snapshot.v1",
            "totalTaskCount": 4,
            "linkedinLanePacketCount": 1,
            "packets": [{"taskId": "task-1", "payloadHash": "a" * 64}],
            "projectionSha256": "b" * 64,
        }
        cron = {"jobs": []}
        artifact = build_boundary_artifact(
            phase="phase-1-before",
            generated_at=GENERATED_AT,
            run_id="sha256:" + "c" * 64,
            snapshot=snapshot,
            normalized_cron=cron,
            launchagents=[{"path": "Library/LaunchAgents/example.plist", "sha256": "d" * 64}],
            protected_inputs={"memory/content/posted-log.jsonl": "e" * 64},
            primary_checkout_fingerprint="f" * 64,
        )
        self.assertEqual(artifact["missionControl"]["taskIds"], ["task-1"])
        self.assertEqual(artifact["missionControl"]["taskCount"], 4)
        self.assertRegex(str(artifact["boundarySha256"]), r"^[0-9a-f]{64}$")
        self.assertEqual(validate_boundary_artifact(artifact), artifact)
        tampered = copy.deepcopy(artifact)
        tampered["missionControl"]["taskCount"] = 5
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            validate_boundary_artifact(tampered)


class VerificationIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.artifacts = self.root / "memory/content/linkedin-content-os"
        self.artifacts.mkdir(parents=True)

    def _binding(self, role: str, path: Path) -> dict[str, object]:
        return {
            "role": role,
            "path": path.relative_to(self.root).as_posix(),
            "sha256": sha256_hex(path.read_bytes()),
        }

    def _receipt(
        self,
        *,
        command: str,
        context: Path,
        expected: str | None,
        canonical_manifest: str,
        inputs: list[tuple[str, Path]],
        outputs: list[tuple[str, Path]],
        generated_at: str,
        destination: Path,
    ) -> None:
        receipt = build_authority_consumption_receipt(
            command=command,
            run_context_sha256=sha256_hex(context.read_bytes()),
            expected_manifest_sha256=expected,
            canonical_manifest_sha256=canonical_manifest,
            inputs=sorted([self._binding(role, path) for role, path in inputs], key=lambda item: (item["role"], item["path"])),
            outputs=sorted([self._binding(role, path) for role, path in outputs], key=lambda item: (item["role"], item["path"])),
            generated_at=generated_at,
        )
        destination.write_bytes(canonical_bytes(receipt))

    def _boundary(self, phase: str, context: dict[str, object], destination: Path) -> None:
        snapshot = {
            "totalTaskCount": 0,
            "linkedinLanePacketCount": 0,
            "packets": [],
            "projectionSha256": "9" * 64,
        }
        artifact = build_boundary_artifact(
            phase=phase,
            generated_at=str(context["generatedAt"]),
            run_id=str(context["runId"]),
            snapshot=snapshot,
            normalized_cron={"jobs": []},
            launchagents=[],
            protected_inputs={},
            primary_checkout_fingerprint="8" * 64,
        )
        destination.write_bytes(canonical_bytes(artifact))

    def _proof_tree(self) -> dict[str, Path]:
        t1 = "2026-09-28T15:00:00+00:00"
        t2 = GENERATED_AT
        phase1_context_path = self.artifacts / "run-context.phase-1.v1.json"
        phase1_outcomes = self.artifacts / "outcomes.phase-1.v1.jsonl"
        phase1_context = init_run(t1, phase1_outcomes, phase1_context_path)
        posted = self.root / "memory/content/posted-log.jsonl"
        posted.parent.mkdir(parents=True, exist_ok=True)
        posted.write_bytes(b"")
        phase1_audit_value = audit_legacy_rows(posted, phase1_outcomes, t1)
        phase1_audit = self.artifacts / "historical-audit.phase-1.v1.json"
        phase1_audit.write_bytes(canonical_bytes(phase1_audit_value))
        phase1_gold = self.artifacts / "voice-gold.phase-1.v0.jsonl"
        phase1_pairs = self.artifacts / "contrastive-pairs.phase-1.v0.jsonl"
        phase1_gold.write_bytes(b"")
        phase1_pairs.write_bytes(b"")
        phase1_receipt = self.artifacts / "authority-consumption.phase-1-corpus.v1.json"
        phase1_manifest_hash = str(phase1_audit_value["corpusAuthorityManifest"]["manifestSha256"])
        self._receipt(
            command="build-corpus", context=phase1_context_path, expected=None,
            canonical_manifest=phase1_manifest_hash,
            inputs=[("audit", phase1_audit), ("outcomes", phase1_outcomes), ("run_context", phase1_context_path)],
            outputs=[("voice_gold", phase1_gold), ("contrastive_pairs", phase1_pairs)],
            generated_at=t1, destination=phase1_receipt,
        )

        source_sha = sha256_hex(posted.read_bytes())
        manifest: dict[str, object] = {
            "schemaVersion": "linkedin-corpus-authority-manifest.v1",
            "runId": corpus_run_id(source_sha, t2),
            "validatedAt": t2,
            "receiptSha256Allowlist": ["1" * 64],
            "humanGateAuthorityReceiptSha256": "2" * 64,
            "ledgerPrefixSha256": "3" * 64,
            "ledgerPosition": 1,
        }
        manifest["manifestSha256"] = sha256_hex(canonical_bytes(manifest))
        manifest_path = self.artifacts / "corpus-authority-manifest.v1.json"
        manifest_path.write_bytes(canonical_bytes(manifest))
        authority_unsigned = {
            "schemaVersion": "linkedin-program-0-authority-run-context.v1",
            "generatedAt": t2,
            "corpusAuthorityManifestSha256": manifest["manifestSha256"],
        }
        authority_context = {
            **authority_unsigned,
            "runId": "sha256:" + sha256_hex(canonical_bytes(authority_unsigned)),
        }
        authority_path = self.artifacts / "run-context.phase-2-authority.v1.json"
        authority_path.write_bytes(canonical_bytes(authority_context))
        phase2_base_unsigned = {"schemaVersion": "linkedin-program-0-run-context.v1", "generatedAt": t2}
        phase2_context = {**phase2_base_unsigned, "runId": "sha256:" + sha256_hex(canonical_bytes(phase2_base_unsigned))}

        outcomes = self.artifacts / "outcomes.v1.jsonl"
        outcomes.write_bytes(b"")
        recovery = self.artifacts / "historical-recovery-request.v1.json"
        recovery_value = {"schemaVersion": "linkedin-historical-recovery-request.v1", "generatedAt": t2, "sourceSha256": source_sha, "items": []}
        recovery.write_bytes(canonical_bytes(recovery_value))
        audit_value = {
            "schemaVersion": "linkedin-historical-audit.v1", "generatedAt": t2,
            "sourceSha256": source_sha,
            "statusCounts": {"posted_confirmed": 0, "not_posted_confirmed": 0, "status_unknown": 0},
            "missingFieldCounts": {}, "duplicateGroups": [], "records": [],
            "corpusAuthorityManifest": manifest, "recoveryRequest": recovery_value,
        }
        audit = self.artifacts / "historical-audit.v1.json"
        audit.write_bytes(canonical_bytes(audit_value))
        gold = self.artifacts / "voice-gold.v0.jsonl"
        pairs = self.artifacts / "contrastive-pairs.v0.jsonl"
        gold.write_bytes(b"")
        pairs.write_bytes(b"")
        focus = self.artifacts / "focus-snapshot.v1.json"
        focus.write_bytes(canonical_bytes({
            "status": "confirmed",
            "targets": [{"targetId": "consulting-proof"}],
        }))
        fixtures = self.artifacts / "evaluation-fixtures.v0.jsonl"
        fixtures.write_bytes(canonical_bytes({"classification": "negative"}) + b"\n" + canonical_bytes({"classification": "positive"}) + b"\n")
        snapshot_unsigned: dict[str, object] = {
            "schemaVersion": "linkedin-mc-snapshot.v1",
            "runId": phase2_context["runId"],
            "capturedAt": t2,
            "validUntil": "2026-09-28T18:00:00+00:00",
            "sourceUrl": "http://127.0.0.1:3000/api/tasks",
            "rawSha256": "7" * 64,
            "totalTaskCount": 0,
            "linkedinLanePacketCount": 0,
            "packets": [],
        }
        snapshot = {
            **snapshot_unsigned,
            "projectionSha256": sha256_hex(canonical_bytes(snapshot_unsigned)),
        }
        (self.artifacts / "mission-control.snapshot.v1.json").write_bytes(
            canonical_bytes(snapshot)
        )
        checkin = self.artifacts / "checkin.preview.v1.json"
        checkin.write_bytes(canonical_bytes({
            "schemaVersion": "linkedin-checkin-preview.v1",
            "sourceSnapshotSha256": snapshot["projectionSha256"],
            "liveWriteAuthorized": False,
            "task": None,
        }))

        audit_receipt = self.artifacts / "authority-consumption.phase-2-audit.v1.json"
        corpus_receipt = self.artifacts / "authority-consumption.phase-2-corpus.v1.json"
        self._receipt(
            command="audit-history", context=authority_path, expected=str(manifest["manifestSha256"]),
            canonical_manifest=str(manifest["manifestSha256"]),
            inputs=[("posted_log", posted), ("outcomes", outcomes), ("authority_manifest", manifest_path), ("run_context", authority_path)],
            outputs=[("historical_audit", audit), ("recovery_request", recovery)], generated_at=t2,
            destination=audit_receipt,
        )
        self._receipt(
            command="build-corpus", context=authority_path, expected=str(manifest["manifestSha256"]),
            canonical_manifest=str(manifest["manifestSha256"]),
            inputs=[("audit", audit), ("outcomes", outcomes), ("run_context", authority_path)],
            outputs=[("voice_gold", gold), ("contrastive_pairs", pairs)], generated_at=t2,
            destination=corpus_receipt,
        )

        boundaries: list[Path] = []
        for phase, context_value in (
            ("phase-1-before", phase1_context), ("phase-1-after", phase1_context),
            ("phase-2-before", phase2_context), ("phase-2-after", phase2_context),
        ):
            path = self.artifacts / ("boundaries." + phase + ".json")
            self._boundary(phase, context_value, path)
            boundaries.append(path)
        return {
            "authority": authority_path, "manifest": manifest_path,
            "phase1_receipt": phase1_receipt, "audit_receipt": audit_receipt,
            "corpus_receipt": corpus_receipt, "b1": boundaries[0], "a1": boundaries[1],
            "b2": boundaries[2], "a2": boundaries[3], "report": self.root / "report.md",
        }

    def _verify_argv(self, paths: dict[str, Path]) -> list[str]:
        return [
            "verify", "--workspace-root", str(self.root), "--run-context", str(paths["authority"]),
            "--corpus-authority-manifest", str(paths["manifest"]),
            "--phase-1-corpus-receipt", str(paths["phase1_receipt"]),
            "--phase-2-audit-receipt", str(paths["audit_receipt"]),
            "--phase-2-corpus-receipt", str(paths["corpus_receipt"]),
            "--phase-1-before", str(paths["b1"]), "--phase-1-after", str(paths["a1"]),
            "--phase-2-before", str(paths["b2"]), "--phase-2-after", str(paths["a2"]),
            "--report", str(paths["report"]),
        ]

    def test_verify_binds_receipt_order_manifest_context_and_four_boundaries(self) -> None:
        paths = self._proof_tree()
        with mock.patch("scripts.linkedin_content_os.cli.build_voice_gold", return_value=[]), mock.patch(
            "scripts.linkedin_content_os.cli.build_contrastive_pairs", return_value=[]
        ):
            report = main(self._verify_argv(paths))
        self.assertTrue(report["boundaryPairsEqual"])
        self.assertEqual(len(report["boundaryProof"]), 2)
        observed = {
            row[key]
            for row in report["boundaryProof"]
            for key in ("beforeFileSha256", "afterFileSha256")
        }
        self.assertEqual(len(observed), 4)
        self.assertFalse(report["liveOrExternalActionOccurred"])

        swapped = self._verify_argv(paths)
        audit_index = swapped.index("--phase-2-audit-receipt") + 1
        corpus_index = swapped.index("--phase-2-corpus-receipt") + 1
        swapped[audit_index], swapped[corpus_index] = swapped[corpus_index], swapped[audit_index]
        with self.assertRaisesRegex(ValueError, "phase order"):
            main(swapped)

    def test_verify_rejects_boundary_from_wrong_phase_context(self) -> None:
        paths = self._proof_tree()
        boundary = _read_json(paths["a2"])
        boundary["runId"] = "sha256:" + "7" * 64
        unsigned = {key: value for key, value in boundary.items() if key != "boundarySha256"}
        boundary["boundarySha256"] = sha256_hex(canonical_bytes(unsigned))
        paths["a2"].write_bytes(canonical_bytes(boundary))
        with mock.patch("scripts.linkedin_content_os.cli.build_voice_gold", return_value=[]), mock.patch(
            "scripts.linkedin_content_os.cli.build_contrastive_pairs", return_value=[]
        ):
            with self.assertRaisesRegex(ValueError, "run context mismatch"):
                main(self._verify_argv(paths))

    def test_verify_rejects_manifest_and_checkin_tampering(self) -> None:
        paths = self._proof_tree()
        manifest = _read_json(paths["manifest"])
        manifest["ledgerPosition"] = 2
        paths["manifest"].write_bytes(canonical_bytes(manifest))
        with self.assertRaisesRegex(ValueError, "manifest|hash"):
            main(self._verify_argv(paths))

        paths = self._proof_tree()
        checkin = self.artifacts / "checkin.preview.v1.json"
        value = _read_json(checkin)
        value["task"] = {"dedupeKey": "tampered"}
        checkin.write_bytes(canonical_bytes(value))
        with mock.patch("scripts.linkedin_content_os.cli.build_voice_gold", return_value=[]), mock.patch(
            "scripts.linkedin_content_os.cli.build_contrastive_pairs", return_value=[]
        ):
            with self.assertRaisesRegex(ValueError, "check-in preview"):
                main(self._verify_argv(paths))


if __name__ == "__main__":
    unittest.main()
