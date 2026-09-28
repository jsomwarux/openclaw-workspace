import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.focus import (
    ALLOWED_OWNER_PATHS,
    apply_focus_decision,
    build_focus_snapshot,
    renewal_need,
    validate_focus_snapshot,
)


GENERATED_AT = "2026-09-28T12:00:00-04:00"
VALID_UNTIL = "2026-10-28T12:00:00-04:00"


def _target(path: str, digest: str, *, target_id: str = "consulting-proof") -> dict:
    return {
        "targetId": target_id,
        "kind": "consulting",
        "label": "Consulting proof",
        "desiredOutcome": "Create one permissioned proof-led consulting asset",
        "sourceRefs": [{"path": path, "sha256": digest}],
    }


def _event(snapshot: dict, decision: str = "confirmed", replacement_hash=None) -> dict:
    payload = {
        "decision": decision,
        "focusSnapshotSha256": snapshot["snapshotId"].removeprefix("sha256:"),
    }
    if replacement_hash is not None:
        payload["replacementFocusSnapshotSha256"] = replacement_hash
    event = {
        "schemaVersion": "linkedin-content-outcome.v1",
        "outcomeEventId": "focus-decision-001",
        "packetId": "linkedin-program-0",
        "eventType": "focus_decision",
        "recordedAt": "2026-09-28T12:05:00-04:00",
        "sourcePointer": {
            "sourceType": "jt_response",
            "sourceId": "program-0-gate",
            "sourceSha256": "a" * 64,
        },
        "payload": payload,
    }
    event["eventSha256"] = sha256_hex(canonical_bytes(event))
    return event


class FocusSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.owner_path = "memory/content/current-efforts.md"
        owner = self.root / self.owner_path
        owner.parent.mkdir(parents=True)
        owner.write_text("# Current efforts\n\nConsulting proof is the priority.\n", encoding="utf-8")
        self.digest = sha256_hex(owner.read_bytes())
        self.targets = [_target(self.owner_path, self.digest)]

    def build(self, **kwargs):
        return build_focus_snapshot(
            self.root,
            kwargs.pop("targets", self.targets),
            generated_at=kwargs.pop("generated_at", GENERATED_AT),
            **kwargs,
        )

    def test_builds_deterministic_proposed_snapshot_with_exact_30_day_window(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(first, second)
        self.assertEqual(first["schemaVersion"], "linkedin-focus-snapshot.v1")
        self.assertEqual(first["status"], "proposed")
        self.assertEqual(first["validUntil"], VALID_UNTIL)
        self.assertEqual(first["prohibitedPremises"], ["internal_machinery"])
        self.assertRegex(first["snapshotId"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(validate_focus_snapshot(first, self.root), first)

    def test_rejects_zero_targets_unsupported_kind_duplicate_ids_and_status(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one target"):
            self.build(targets=[])
        unsupported = copy.deepcopy(self.targets)
        unsupported[0]["kind"] = "audience"
        with self.assertRaisesRegex(ValueError, "unsupported target kind"):
            self.build(targets=unsupported)
        duplicate = self.targets + copy.deepcopy(self.targets)
        with self.assertRaisesRegex(ValueError, "duplicate targetId"):
            self.build(targets=duplicate)
        snapshot = self.build()
        snapshot["status"] = "approved"
        with self.assertRaisesRegex(ValueError, "unsupported focus status"):
            validate_focus_snapshot(snapshot, self.root)

    def test_rejects_unallowlisted_missing_and_mismatched_sources(self) -> None:
        outside = copy.deepcopy(self.targets)
        outside[0]["sourceRefs"][0]["path"] = "MEMORY.md"
        with self.assertRaisesRegex(ValueError, "allowlisted"):
            self.build(targets=outside)
        missing = [_target("memory/pipeline.jsonl", "0" * 64)]
        with self.assertRaisesRegex(ValueError, "does not exist"):
            self.build(targets=missing)
        mismatched = [_target(self.owner_path, "0" * 64)]
        with self.assertRaisesRegex(ValueError, "source hash mismatch"):
            self.build(targets=mismatched)

    def test_rejects_conflicting_owner_facts_instead_of_reconciling_them(self) -> None:
        conflict = copy.deepcopy(self.targets)
        second = copy.deepcopy(conflict[0])
        second["label"] = "Different label"
        conflict.append(second)
        with self.assertRaisesRegex(ValueError, "conflicting owner facts"):
            self.build(targets=conflict)

    def test_rejects_invalid_timestamp_window_and_stale_snapshot(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            self.build(generated_at="2026-09-28T12:00:00")
        snapshot = self.build()
        snapshot["validUntil"] = "2026-10-29T12:00:00-04:00"
        with self.assertRaisesRegex(ValueError, "exactly 30 days"):
            validate_focus_snapshot(snapshot, self.root)
        with self.assertRaisesRegex(ValueError, "stale"):
            validate_focus_snapshot(
                self.build(),
                self.root,
                now="2026-10-28T12:00:01-04:00",
            )

    def test_snapshot_id_covers_all_content_and_source_bytes(self) -> None:
        snapshot = self.build()
        changed = copy.deepcopy(snapshot)
        changed["targets"][0]["label"] = "Changed"
        with self.assertRaisesRegex(ValueError, "snapshotId"):
            validate_focus_snapshot(changed, self.root)
        (self.root / self.owner_path).write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source hash mismatch"):
            validate_focus_snapshot(snapshot, self.root)

    def test_pre_gate_build_cannot_be_forced_confirmed(self) -> None:
        with self.assertRaisesRegex(ValueError, "always proposed"):
            self.build(status="confirmed")

    def test_matching_confirmed_decision_derives_confirmed_snapshot(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        confirmed = apply_focus_decision(proposed, event, self.root)
        self.assertEqual(confirmed["status"], "confirmed")
        self.assertNotEqual(confirmed["snapshotId"], proposed["snapshotId"])
        self.assertEqual(
            apply_focus_decision(proposed, event, self.root),
            confirmed,
        )
        self.assertEqual(
            validate_focus_snapshot(confirmed, self.root, focus_decision=event),
            confirmed,
        )

    def test_confirmed_requires_valid_matching_focus_decision(self) -> None:
        proposed = self.build()
        forged = copy.deepcopy(proposed)
        forged["status"] = "confirmed"
        forged["snapshotId"] = "sha256:" + sha256_hex(
            canonical_bytes({k: v for k, v in forged.items() if k != "snapshotId"})
        )
        with self.assertRaisesRegex(ValueError, "focus_decision"):
            validate_focus_snapshot(forged, self.root)
        wrong = _event(proposed)
        wrong["payload"]["focusSnapshotSha256"] = "0" * 64
        wrong["eventSha256"] = sha256_hex(
            canonical_bytes({k: v for k, v in wrong.items() if k != "eventSha256"})
        )
        with self.assertRaisesRegex(ValueError, "does not match"):
            apply_focus_decision(proposed, wrong, self.root)

    def test_confirmed_validation_rejects_decision_bound_to_other_targets(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        confirmed = apply_focus_decision(proposed, event, self.root)
        wrong = copy.deepcopy(event)
        wrong["payload"]["focusSnapshotSha256"] = "0" * 64
        wrong["eventSha256"] = sha256_hex(
            canonical_bytes({k: v for k, v in wrong.items() if k != "eventSha256"})
        )
        rebound = copy.deepcopy(confirmed)
        without_id = {k: v for k, v in rebound.items() if k != "snapshotId"}
        rebound["snapshotId"] = "sha256:" + sha256_hex(
            canonical_bytes(
                {
                    "focusSnapshot": without_id,
                    "focusDecisionEventSha256": wrong["eventSha256"],
                }
            )
        )
        with self.assertRaisesRegex(ValueError, "decision target hash"):
            validate_focus_snapshot(rebound, self.root, focus_decision=wrong)

    def test_corrected_decision_requires_complete_replacement_and_declared_hash(self) -> None:
        proposed = self.build()
        product_path = "memory/pipeline.jsonl"
        product_file = self.root / product_path
        product_file.parent.mkdir(parents=True, exist_ok=True)
        product_file.write_text('{"lane":"product"}\n', encoding="utf-8")
        replacement = [
            {
                "targetId": "product-distribution",
                "kind": "product",
                "label": "Product distribution",
                "desiredOutcome": "Get one existing product to a verified user outcome",
                "sourceRefs": [
                    {"path": product_path, "sha256": sha256_hex(product_file.read_bytes())}
                ],
            }
        ]
        replacement_proposed = self.build(targets=replacement)
        event = _event(
            proposed,
            decision="corrected",
            replacement_hash=replacement_proposed["snapshotId"].removeprefix("sha256:"),
        )
        corrected = apply_focus_decision(
            proposed, event, self.root, corrected_targets=replacement
        )
        self.assertEqual(corrected["targets"], replacement)
        self.assertEqual(corrected["status"], "confirmed")
        self.assertNotEqual(corrected["snapshotId"], proposed["snapshotId"])
        with self.assertRaisesRegex(ValueError, "complete replacement"):
            apply_focus_decision(proposed, event, self.root, corrected_targets=[])
        event["payload"]["replacementFocusSnapshotSha256"] = "f" * 64
        event["eventSha256"] = sha256_hex(
            canonical_bytes({k: v for k, v in event.items() if k != "eventSha256"})
        )
        with self.assertRaisesRegex(ValueError, "replacement snapshot"):
            apply_focus_decision(proposed, event, self.root, corrected_targets=replacement)

    def test_renewal_need_is_single_deterministic_non_mutating_record(self) -> None:
        snapshot = self.build()
        before = canonical_bytes(snapshot)
        self.assertIsNone(renewal_need(snapshot, "2026-10-28T12:00:00-04:00"))
        need = renewal_need(snapshot, "2026-10-28T12:00:01-04:00")
        self.assertEqual(need, renewal_need(snapshot, "2026-10-28T12:00:01-04:00"))
        self.assertEqual(need["needId"], "linkedin-focus-renewal:v1")
        self.assertEqual(need["focusSnapshotId"], snapshot["snapshotId"])
        self.assertEqual(canonical_bytes(snapshot), before)

    def test_fixture_uses_only_allowlisted_exact_owner_hashes(self) -> None:
        fixture_path = Path("scripts/tests/fixtures/linkedin_content_os/focus-sources.json")
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schemaVersion"], "linkedin-focus-sources.v1")
        self.assertGreaterEqual(len(fixture["targets"]), 1)
        for target in fixture["targets"]:
            for source in target["sourceRefs"]:
                self.assertIn(source["path"], ALLOWED_OWNER_PATHS)
                self.assertEqual(
                    source["sha256"], sha256_hex(Path(source["path"]).read_bytes())
                )


if __name__ == "__main__":
    unittest.main()
