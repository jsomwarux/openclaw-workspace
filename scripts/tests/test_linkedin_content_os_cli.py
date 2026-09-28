from __future__ import annotations

import copy
import json
import socket
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.boundaries import (
    build_authority_consumption_receipt,
    build_boundary_artifact,
    normalize_cron_definitions,
    validate_authority_consumption_receipt,
    validate_boundary_artifact,
)
from scripts.linkedin_content_os.cli import (
    COMMANDS,
    _network_denied,
    _process_guard,
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
            "wakeMode", "payloadSha256", "deliveryMode", "deliveryTarget",
        })
        self.assertNotIn("lastRunAt", canonical_bytes(normalized).decode())
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


if __name__ == "__main__":
    unittest.main()
