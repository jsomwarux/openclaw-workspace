import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.focus import (
    ALLOWED_OWNER_PATHS,
    AUTHORITY_RECEIPT_SCHEMA_VERSION,
    HUMAN_GATE_PACKET_ID,
    HUMAN_GATE_SOURCE_TYPE,
    apply_focus_decision,
    build_focus_snapshot,
    renewal_need,
    validate_focus_snapshot,
)


GENERATED_AT = "2026-09-28T12:00:00-04:00"
VALID_UNTIL = "2026-10-28T12:00:00-04:00"
NOW = datetime(2026, 9, 28, 17, 0, tzinfo=timezone.utc)


def _target(path: str, digest: str, *, target_id: str = "consulting-proof") -> dict:
    return {
        "targetId": target_id,
        "kind": "consulting",
        "label": "Consulting proof",
        "desiredOutcome": "Create one permissioned proof-led consulting asset",
        "sourceRefs": [{"path": path, "sha256": digest}],
    }


def _event(snapshot: dict, decision: str = "confirmed", replacement_hash=None) -> dict:
    response_hash = "a" * 64
    payload = {
        "decision": decision,
        "focusSnapshotSha256": snapshot["snapshotId"].removeprefix("sha256:"),
    }
    if replacement_hash is not None:
        payload["replacementFocusSnapshotSha256"] = replacement_hash
    event = {
        "schemaVersion": "linkedin-content-outcome.v1",
        "outcomeEventId": "focus-decision-001",
        "packetId": HUMAN_GATE_PACKET_ID,
        "eventType": "focus_decision",
        "recordedAt": "2026-09-28T12:05:00-04:00",
        "sourcePointer": {
            "sourceType": HUMAN_GATE_SOURCE_TYPE,
            "sourceId": "sha256:" + response_hash,
            "sourceSha256": response_hash,
        },
        "payload": payload,
    }
    event["eventSha256"] = sha256_hex(canonical_bytes(event))
    return event


def _receipt(
    snapshot: dict, event: dict, *, decision: str = "confirmed",
    corrected_targets=None, replacement_hash=None,
) -> dict:
    focus_decision = {"decision": decision}
    if corrected_targets is not None:
        focus_decision["correctedTargets"] = corrected_targets
    receipt = {
        "schemaVersion": AUTHORITY_RECEIPT_SCHEMA_VERSION,
        "rawResponseSha256": event["sourcePointer"]["sourceSha256"],
        "recoveryRequestSha256": "1" * 64,
        "fixtureGapSha256": "2" * 64,
        "focusDecisionEventSha256": event["eventSha256"],
        "ledgerPrefixSha256": "3" * 64,
        "ledgerPosition": 1,
        "validatedAt": "2026-09-28T12:06:00-04:00",
        "originalProposalSha256": snapshot["snapshotId"].removeprefix("sha256:"),
        "focusDecision": focus_decision,
    }
    if replacement_hash is not None:
        receipt["replacementProposalSha256"] = replacement_hash
    receipt["receiptSha256"] = sha256_hex(canonical_bytes(receipt))
    return receipt


class FocusSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        clock = mock.patch(
            "scripts.linkedin_content_os.focus._utc_now", return_value=NOW
        )
        clock.start()
        self.addCleanup(clock.stop)
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
        with mock.patch(
            "scripts.linkedin_content_os.focus._utc_now",
            return_value=datetime(2026, 10, 28, 16, 0, 1, tzinfo=timezone.utc),
        ):
            with self.assertRaisesRegex(ValueError, "stale"):
                validate_focus_snapshot(self.build(), self.root)

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
        receipt = _receipt(proposed, event)
        confirmed = apply_focus_decision(
            proposed, event, self.root, authority_receipt=receipt,
            expected_authority_receipt_sha256=receipt["receiptSha256"],
        )
        self.assertEqual(confirmed["status"], "confirmed")
        self.assertNotEqual(confirmed["snapshotId"], proposed["snapshotId"])
        self.assertEqual(
            apply_focus_decision(
                proposed, event, self.root, authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
            ),
            confirmed,
        )
        self.assertEqual(
            validate_focus_snapshot(
                confirmed,
                self.root,
                focus_decision=event,
                authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
                original_proposed_snapshot=proposed,
            ),
            confirmed,
        )

    def test_confirmed_requires_valid_matching_focus_decision(self) -> None:
        proposed = self.build()
        forged = copy.deepcopy(proposed)
        forged["status"] = "confirmed"
        forged["snapshotId"] = "sha256:" + sha256_hex(
            canonical_bytes({k: v for k, v in forged.items() if k != "snapshotId"})
        )
        with self.assertRaisesRegex(ValueError, "decisionBinding"):
            validate_focus_snapshot(forged, self.root)
        event = _event(proposed)
        receipt = _receipt(proposed, event)
        wrong = copy.deepcopy(event)
        wrong["payload"]["focusSnapshotSha256"] = "0" * 64
        wrong["eventSha256"] = sha256_hex(
            canonical_bytes({k: v for k, v in wrong.items() if k != "eventSha256"})
        )
        with self.assertRaisesRegex(ValueError, "event|payload"):
            apply_focus_decision(
                proposed, wrong, self.root, authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
            )

    def test_confirmed_validation_rejects_decision_bound_to_other_targets(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        receipt = _receipt(proposed, event)
        confirmed = apply_focus_decision(
            proposed, event, self.root, authority_receipt=receipt,
            expected_authority_receipt_sha256=receipt["receiptSha256"],
        )
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
        with self.assertRaisesRegex(ValueError, "event|payload"):
            validate_focus_snapshot(
                rebound,
                self.root,
                focus_decision=wrong,
                authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
                original_proposed_snapshot=proposed,
            )

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
            proposed, decision="corrected",
            replacement_hash=replacement_proposed["snapshotId"].removeprefix("sha256:"),
        )
        receipt = _receipt(
            proposed, event, decision="corrected", corrected_targets=replacement,
            replacement_hash=replacement_proposed["snapshotId"].removeprefix("sha256:"),
        )
        corrected = apply_focus_decision(
            proposed, event, self.root, authority_receipt=receipt,
            expected_authority_receipt_sha256=receipt["receiptSha256"],
        )
        self.assertEqual(corrected["targets"], replacement)
        self.assertEqual(corrected["status"], "confirmed")
        self.assertNotEqual(corrected["snapshotId"], proposed["snapshotId"])
        self.assertEqual(
            validate_focus_snapshot(
                corrected,
                self.root,
                focus_decision=event,
                authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
                original_proposed_snapshot=proposed,
            ),
            corrected,
        )
        with self.assertRaisesRegex(ValueError, "correctedTargets|complete replacement"):
            missing = copy.deepcopy(receipt)
            del missing["focusDecision"]["correctedTargets"]
            missing["receiptSha256"] = sha256_hex(canonical_bytes(
                {k: v for k, v in missing.items() if k != "receiptSha256"}
            ))
            apply_focus_decision(
                proposed, event, self.root, authority_receipt=missing,
                expected_authority_receipt_sha256=missing["receiptSha256"],
            )
        event["payload"]["replacementFocusSnapshotSha256"] = "f" * 64
        event["eventSha256"] = sha256_hex(
            canonical_bytes({k: v for k, v in event.items() if k != "eventSha256"})
        )
        with self.assertRaisesRegex(ValueError, "event|payload"):
            apply_focus_decision(
                proposed, event, self.root, authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
            )

        other = copy.deepcopy(corrected)
        other["targets"] = self.targets
        without_id = {k: v for k, v in other.items() if k != "snapshotId"}
        other["snapshotId"] = "sha256:" + sha256_hex(canonical_bytes(without_id))
        with self.assertRaisesRegex(ValueError, "corrected targets"):
            validate_focus_snapshot(
                other,
                self.root,
                focus_decision=_event(
                    proposed, decision="corrected",
                    replacement_hash=replacement_proposed["snapshotId"].removeprefix("sha256:"),
                ),
                authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
                original_proposed_snapshot=proposed,
            )

    def test_renewal_need_is_single_deterministic_non_mutating_record(self) -> None:
        snapshot = self.build()
        before = canonical_bytes(snapshot)
        with mock.patch(
            "scripts.linkedin_content_os.focus._utc_now",
            return_value=datetime(2026, 10, 28, 16, 0, tzinfo=timezone.utc),
        ):
            self.assertIsNone(renewal_need(snapshot, self.root))
        with mock.patch(
            "scripts.linkedin_content_os.focus._utc_now",
            return_value=datetime(2026, 10, 28, 16, 0, 1, tzinfo=timezone.utc),
        ):
            need = renewal_need(snapshot, self.root)
            self.assertEqual(need, renewal_need(snapshot, self.root))
        self.assertEqual(need["needId"], "linkedin-focus-renewal:v1")
        self.assertEqual(need["focusSnapshotId"], snapshot["snapshotId"])
        self.assertEqual(canonical_bytes(snapshot), before)

    def test_arbitrary_self_hashed_event_is_not_human_authority(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        forged_response = {
            "schemaVersion": "linkedin-human-gate-response.v1",
            "focusDecision": {"decision": "confirmed"},
        }
        with self.assertRaisesRegex(ValueError, "authority receipt"):
            apply_focus_decision(
                proposed, event, self.root, authority_receipt=forged_response,
                expected_authority_receipt_sha256="f" * 64,
            )

    def test_authority_receipt_requires_independent_anchor_and_ledger_provenance(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        receipt = _receipt(proposed, event)
        with self.assertRaisesRegex(ValueError, "expected authority receipt"):
            apply_focus_decision(
                proposed, event, self.root, authority_receipt=receipt,
                expected_authority_receipt_sha256="f" * 64,
            )
        for field, value in (("ledgerPrefixSha256", "f" * 64), ("ledgerPosition", 2)):
            tampered = copy.deepcopy(receipt)
            tampered[field] = value
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "receiptSha256"):
                    apply_focus_decision(
                        proposed, event, self.root, authority_receipt=tampered,
                        expected_authority_receipt_sha256=receipt["receiptSha256"],
                    )
        malformed = copy.deepcopy(receipt)
        malformed["ledgerPosition"] = 0
        malformed["receiptSha256"] = sha256_hex(canonical_bytes(
            {k: v for k, v in malformed.items() if k != "receiptSha256"}
        ))
        with self.assertRaisesRegex(ValueError, "ledgerPosition"):
            apply_focus_decision(
                proposed, event, self.root, authority_receipt=malformed,
                expected_authority_receipt_sha256=malformed["receiptSha256"],
            )

    def test_focus_rejects_raw_human_response_bytes(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        with self.assertRaisesRegex(ValueError, "authority receipt"):
            apply_focus_decision(
                proposed, event, self.root,
                authority_receipt=canonical_bytes({"focusDecision": {"decision": "confirmed"}}),
                expected_authority_receipt_sha256="f" * 64,
            )

    def test_decision_time_and_freshness_are_mandatory(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        receipt = _receipt(proposed, event)
        with mock.patch(
            "scripts.linkedin_content_os.focus._utc_now",
            return_value=datetime(2026, 10, 28, 16, 0, 1, tzinfo=timezone.utc),
        ):
            with self.assertRaisesRegex(ValueError, "stale"):
                apply_focus_decision(
                    proposed, event, self.root, authority_receipt=receipt,
                    expected_authority_receipt_sha256=receipt["receiptSha256"],
                )

        for recorded_at in (
            "2026-09-28T11:59:59-04:00",
            "2026-10-28T12:00:01-04:00",
            "2026-09-28T14:00:00-04:00",
        ):
            timed_event = copy.deepcopy(event)
            timed_event["recordedAt"] = recorded_at
            timed_event["eventSha256"] = sha256_hex(canonical_bytes(
                {k: v for k, v in timed_event.items() if k != "eventSha256"}
            ))
            timed_receipt = _receipt(proposed, timed_event)
            with self.subTest(recorded_at=recorded_at):
                with self.assertRaises(ValueError):
                    apply_focus_decision(
                        proposed,
                        timed_event,
                        self.root,
                        authority_receipt=timed_receipt,
                        expected_authority_receipt_sha256=timed_receipt["receiptSha256"],
                    )

        with self.assertRaisesRegex(ValueError, "future"):
            self.build(generated_at="2026-09-28T14:00:00-04:00")

    def test_rejects_symlinked_owner_file_and_path_component(self) -> None:
        real = self.root / "real.md"
        real.write_text("real", encoding="utf-8")
        owner = self.root / self.owner_path
        owner.unlink()
        owner.symlink_to(real)
        targets = [_target(self.owner_path, sha256_hex(real.read_bytes()))]
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.build(targets=targets)

        owner.unlink()
        content_dir = self.root / "memory/content"
        content_dir.rmdir()
        real_dir = self.root / "real-content"
        real_dir.mkdir()
        (real_dir / "current-efforts.md").write_text("real", encoding="utf-8")
        content_dir.symlink_to(real_dir, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.build(targets=targets)

    def test_rejects_owner_path_swap_during_descriptor_read(self) -> None:
        owner = self.root / self.owner_path
        original_stat = owner.stat()
        replacement = owner.with_name("replacement.md")
        replacement.write_bytes(owner.read_bytes())
        real_stat = __import__("os").stat

        calls = 0

        def swapping_stat(path, *args, **kwargs):
            nonlocal calls
            result = real_stat(path, *args, **kwargs)
            if kwargs.get("dir_fd") is not None and path == "current-efforts.md":
                calls += 1
                if calls == 1:
                    replacement.replace(owner)
            return result

        with mock.patch("scripts.linkedin_content_os.focus.os.stat", side_effect=swapping_stat):
            with self.assertRaisesRegex(ValueError, "changed during read"):
                self.build()
        self.assertNotEqual(owner.stat().st_ino, original_stat.st_ino)

    def test_confirmed_snapshot_standalone_binding_rejects_original_authority_and_event_changes(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        receipt = _receipt(proposed, event)
        confirmed = apply_focus_decision(
            proposed, event, self.root, authority_receipt=receipt,
            expected_authority_receipt_sha256=receipt["receiptSha256"],
        )
        binding = confirmed["decisionBinding"]
        self.assertEqual(
            binding["originalProposalSha256"],
            proposed["snapshotId"].removeprefix("sha256:"),
        )
        self.assertEqual(binding["authorityReceiptSha256"], receipt["receiptSha256"])
        self.assertEqual(binding["focusDecisionEventSha256"], event["eventSha256"])

        for field in (
            "originalProposalSha256",
            "authorityReceiptSha256",
            "focusDecisionEventSha256",
        ):
            forged = copy.deepcopy(confirmed)
            forged["decisionBinding"][field] = "0" * 64
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    validate_focus_snapshot(
                        forged,
                        self.root,
                        focus_decision=event,
                        authority_receipt=receipt,
                        expected_authority_receipt_sha256=receipt["receiptSha256"],
                        original_proposed_snapshot=proposed,
                    )

        other_targets = copy.deepcopy(self.targets)
        other_targets[0]["label"] = "Different original"
        other = self.build(targets=other_targets)
        with self.assertRaisesRegex(ValueError, "original proposed"):
            validate_focus_snapshot(
                confirmed, self.root, focus_decision=event,
                authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
                original_proposed_snapshot=other,
            )

    def test_confirmed_and_corrected_snapshots_cannot_shift_original_window(self) -> None:
        proposed = self.build()
        cases = []

        confirmed_event = _event(proposed)
        confirmed_receipt = _receipt(proposed, confirmed_event)
        confirmed = apply_focus_decision(
            proposed, confirmed_event, self.root,
            authority_receipt=confirmed_receipt,
            expected_authority_receipt_sha256=confirmed_receipt["receiptSha256"],
        )
        cases.append((confirmed, confirmed_event, confirmed_receipt))

        product_path = "memory/pipeline.jsonl"
        product_file = self.root / product_path
        product_file.parent.mkdir(parents=True, exist_ok=True)
        product_file.write_text('{"lane":"product"}\n', encoding="utf-8")
        replacement = [_target(
            product_path, sha256_hex(product_file.read_bytes()),
            target_id="product-distribution",
        )]
        replacement[0]["kind"] = "product"
        replacement_proposed = self.build(targets=replacement)
        replacement_hash = replacement_proposed["snapshotId"].removeprefix("sha256:")
        corrected_event = _event(
            proposed, decision="corrected", replacement_hash=replacement_hash
        )
        corrected_receipt = _receipt(
            proposed, corrected_event, decision="corrected",
            corrected_targets=replacement, replacement_hash=replacement_hash,
        )
        corrected = apply_focus_decision(
            proposed, corrected_event, self.root,
            authority_receipt=corrected_receipt,
            expected_authority_receipt_sha256=corrected_receipt["receiptSha256"],
        )
        cases.append((corrected, corrected_event, corrected_receipt))

        for snapshot, event, receipt in cases:
            shifted = copy.deepcopy(snapshot)
            shifted["generatedAt"] = "2026-09-28T12:01:00-04:00"
            shifted["validUntil"] = "2026-10-28T12:01:00-04:00"
            shifted["snapshotId"] = "sha256:" + sha256_hex(canonical_bytes(
                {key: value for key, value in shifted.items() if key != "snapshotId"}
            ))
            with self.subTest(decision=receipt["focusDecision"]["decision"]):
                with self.assertRaisesRegex(ValueError, "window.*original proposed"):
                    validate_focus_snapshot(
                        shifted, self.root, focus_decision=event,
                        authority_receipt=receipt,
                        expected_authority_receipt_sha256=receipt["receiptSha256"],
                        original_proposed_snapshot=proposed,
                    )

    def test_renewal_need_fully_validates_snapshot(self) -> None:
        forged = self.build()
        forged["targets"][0]["label"] = "tampered"
        with mock.patch(
            "scripts.linkedin_content_os.focus._utc_now",
            return_value=datetime(2026, 10, 28, 16, 0, 1, tzinfo=timezone.utc),
        ):
            with self.assertRaisesRegex(ValueError, "snapshotId"):
                renewal_need(forged, self.root)

    def test_stale_confirmed_renewal_requires_and_verifies_authority(self) -> None:
        proposed = self.build()
        event = _event(proposed)
        receipt = _receipt(proposed, event)
        confirmed = apply_focus_decision(
            proposed, event, self.root, authority_receipt=receipt,
            expected_authority_receipt_sha256=receipt["receiptSha256"],
        )
        with mock.patch(
            "scripts.linkedin_content_os.focus._utc_now",
            return_value=datetime(2026, 10, 28, 16, 0, 1, tzinfo=timezone.utc),
        ):
            with self.assertRaisesRegex(ValueError, "authority"):
                renewal_need(confirmed, self.root)
            need = renewal_need(
                confirmed,
                self.root,
                focus_decision=event,
                authority_receipt=receipt,
                expected_authority_receipt_sha256=receipt["receiptSha256"],
                original_proposed_snapshot=proposed,
            )
        self.assertEqual(need["focusSnapshotId"], confirmed["snapshotId"])

    def test_malformed_status_and_containers_raise_value_error(self) -> None:
        for field, value in (
            ("status", []),
            ("targets", {}),
            ("prohibitedPremises", {}),
        ):
            snapshot = self.build()
            snapshot[field] = value
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    validate_focus_snapshot(snapshot, self.root)

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
