import contextlib
import io
import json
import math
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

from scripts import model_capacity_controller as controller


NOW = datetime(2026, 10, 2, 14, 0, tzinfo=timezone.utc)


def snapshot(provider: str, remaining, hours_old: int = 0):
    captured = NOW.timestamp() - (hours_old * 3600)
    return {
        "provider": provider,
        "remaining_percent": remaining,
        "reset_at": None,
        "captured_at": datetime.fromtimestamp(captured, timezone.utc).isoformat(),
        "source": "test",
    }


class ThresholdTests(unittest.TestCase):
    def test_threshold_bands_preserve_reserve_and_hard_stop(self):
        self.assertEqual(controller.capacity_band(61), "normal")
        self.assertEqual(controller.capacity_band(60), "balance")
        self.assertEqual(controller.capacity_band(40), "balance")
        self.assertEqual(controller.capacity_band(39), "critical_only")
        self.assertEqual(controller.capacity_band(25), "critical_only")
        self.assertEqual(controller.capacity_band(24), "reserve")
        self.assertEqual(controller.capacity_band(15), "reserve")
        self.assertEqual(controller.capacity_band(14), "hard_stop")


class RoutingTests(unittest.TestCase):
    def test_nonfinite_capacity_snapshot_fails_closed(self):
        for value in (math.nan, math.inf, -math.inf, "NaN"):
            with self.subTest(value=value):
                result = controller.route_task(
                    snapshots={
                        "codex": snapshot("codex", value),
                        "claude": snapshot("claude", 99),
                    },
                    task_kind="buyer_copy",
                    size="medium",
                    estimated_burn=8,
                    now=NOW,
                )
                self.assertEqual(result["decision"], "block")
                self.assertEqual(result["provider"], "codex")
                self.assertIn("invalid", result["reason"])

    def test_buyer_copy_routes_to_codex(self):
        result = controller.route_task(
            snapshots={"codex": snapshot("codex", 99), "claude": snapshot("claude", 99)},
            task_kind="buyer_copy",
            size="medium",
            estimated_burn=8,
            now=NOW,
        )
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["provider"], "codex")

    def test_mechanical_work_never_consumes_model_capacity(self):
        result = controller.route_task(
            snapshots={}, task_kind="mechanical", size="large", estimated_burn=30, now=NOW
        )
        self.assertEqual(result["decision"], "script")
        self.assertEqual(result["provider"], "deterministic")

    def test_research_routes_to_provider_with_more_projected_headroom(self):
        result = controller.route_task(
            snapshots={"codex": snapshot("codex", 72), "claude": snapshot("claude", 88)},
            task_kind="research",
            size="medium",
            estimated_burn=8,
            now=NOW,
        )
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["provider"], "claude")
        self.assertEqual(result["projected_remaining"], 80)

    def test_large_lane_fails_closed_when_either_capacity_is_unknown(self):
        result = controller.route_task(
            snapshots={"codex": snapshot("codex", 100), "claude": snapshot("claude", None)},
            task_kind="research",
            size="large",
            estimated_burn=12,
            now=NOW,
        )
        self.assertEqual(result["decision"], "block")
        self.assertIn("unknown", result["reason"])

    def test_stale_selected_snapshot_blocks_lane(self):
        result = controller.route_task(
            snapshots={"codex": snapshot("codex", 90, hours_old=25), "claude": snapshot("claude", 80)},
            task_kind="architecture",
            size="medium",
            estimated_burn=5,
            now=NOW,
        )
        self.assertEqual(result["decision"], "block")
        self.assertIn("stale", result["reason"])

    def test_noncritical_lane_cannot_spend_into_reserve(self):
        result = controller.route_task(
            snapshots={"codex": snapshot("codex", 31), "claude": snapshot("claude", 90)},
            task_kind="architecture",
            size="medium",
            estimated_burn=8,
            now=NOW,
        )
        self.assertEqual(result["decision"], "block")
        self.assertEqual(result["provider"], "codex")
        self.assertEqual(result["projected_remaining"], 23)

    def test_critical_lane_may_use_reserve_but_not_hard_stop(self):
        allowed = controller.route_task(
            snapshots={"codex": snapshot("codex", 24), "claude": snapshot("claude", 90)},
            task_kind="sensitive",
            size="small",
            estimated_burn=5,
            critical=True,
            now=NOW,
        )
        blocked = controller.route_task(
            snapshots={"codex": snapshot("codex", 18), "claude": snapshot("claude", 90)},
            task_kind="sensitive",
            size="small",
            estimated_burn=5,
            critical=True,
            now=NOW,
        )
        self.assertEqual(allowed["decision"], "route")
        self.assertEqual(blocked["decision"], "block")

    def test_n8n_build_never_reroutes_away_from_manual_claude_lane(self):
        result = controller.route_task(
            snapshots={"codex": snapshot("codex", 95), "claude": snapshot("claude", 30)},
            task_kind="n8n_build",
            size="medium",
            estimated_burn=10,
            now=NOW,
        )
        self.assertEqual(result["decision"], "block")
        self.assertEqual(result["provider"], "claude")


class PersistenceTests(unittest.TestCase):
    def test_record_snapshot_updates_current_and_appends_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "current.json"
            ledger = Path(tmp) / "ledger.jsonl"
            event = snapshot("codex", 87)
            controller.record_snapshot(event, current, ledger)
            controller.record_snapshot(snapshot("claude", None), current, ledger)

            state = json.loads(current.read_text())
            rows = [json.loads(line) for line in ledger.read_text().splitlines()]
            self.assertEqual(state["providers"]["codex"]["remaining_percent"], 87)
            self.assertIsNone(state["providers"]["claude"]["remaining_percent"])
            self.assertEqual(len(rows), 2)


class ExecutionTrackingTests(unittest.TestCase):
    def _route(self, decision="route"):
        return {
            "decision": decision,
            "provider": "codex" if decision == "route" else None,
            "reason": "test route",
            "remaining_percent": 99.0,
            "projected_remaining": 91.0,
            "band": "normal",
            "critical": False,
            "size": "medium",
            "task_kind": "buyer_copy",
        }

    def test_buyer_copy_preflight_is_tracked_with_stable_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            event = controller.record_preflight(
                task_id="copy-25",
                task="Draft 25 emails",
                attempt_id="00000000-0000-4000-8000-000000000001",
                task_kind="buyer_copy",
                size="medium",
                estimated_burn=8,
                estimated_minutes=12,
                batch_items=25,
                forced=False,
                result=self._route(),
                ledger_path=ledger,
                recorded_at=NOW,
            )
            self.assertEqual(event["schema_version"], "routing-execution-v1")
            self.assertEqual(event["event_type"], "preflight")
            self.assertTrue(event["tracking_required"])
            self.assertEqual(event["attempt_id"], "00000000-0000-4000-8000-000000000001")
            self.assertEqual(controller.read_execution_events(ledger), [event])

    def test_tracking_threshold_is_strictly_above_ten(self):
        self.assertFalse(controller.tracking_required("research", 10, 10, False))
        self.assertTrue(controller.tracking_required("research", 11, 10, False))
        self.assertTrue(controller.tracking_required("research", 10, 10.1, False))
        self.assertTrue(controller.tracking_required("buyer_copy", 1, 1, False))

    def test_small_legacy_preflight_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            event = controller.record_preflight(
                task_id=None,
                task="Small check",
                attempt_id=None,
                task_kind="research",
                size="small",
                estimated_burn=3,
                estimated_minutes=None,
                batch_items=None,
                forced=False,
                result={**self._route(), "task_kind": "research", "size": "small"},
                ledger_path=ledger,
                recorded_at=NOW,
            )
            self.assertIsNone(event)
            self.assertFalse(ledger.exists())

    def test_tracked_preflight_requires_task_id_and_valid_inputs_without_write(self):
        bad_values = [
            {"task_id": None},
            {"attempt_id": "bad-uuid"},
            {"batch_items": -1},
            {"estimated_minutes": math.inf},
            {"estimated_burn": math.nan},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            base = dict(
                task_id="copy-25",
                task="Draft 25 emails",
                attempt_id="00000000-0000-4000-8000-000000000001",
                task_kind="buyer_copy",
                size="medium",
                estimated_burn=8,
                estimated_minutes=12,
                batch_items=25,
                forced=False,
                result=self._route(),
                ledger_path=ledger,
                recorded_at=NOW,
            )
            for change in bad_values:
                with self.subTest(change=change), self.assertRaises(ValueError):
                    controller.record_preflight(**{**base, **change})
                self.assertFalse(ledger.exists())

    def test_blocked_preflight_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            event = controller.record_preflight(
                task_id="blocked",
                task="Blocked copy",
                attempt_id=None,
                task_kind="buyer_copy",
                size="medium",
                estimated_burn=8,
                estimated_minutes=12,
                batch_items=25,
                forced=False,
                result=self._route("block"),
                ledger_path=ledger,
                recorded_at=NOW,
            )
            UUID(event["attempt_id"])
            self.assertEqual(event["decision"], "block")

    def test_malformed_row_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            ledger.write_text("{not-json}\n")
            with self.assertRaises(ValueError):
                controller.read_execution_events(ledger)

    def test_structurally_incomplete_rows_fail_loudly(self):
        partial_rows = [
            {
                "schema_version": "routing-execution-v1",
                "event_type": "preflight",
                "recorded_at": NOW.isoformat(),
                "task_id": "partial",
                "attempt_id": "00000000-0000-4000-8000-000000000050",
                "decision": "route",
            },
            {
                "schema_version": "routing-execution-v1",
                "event_type": "complete",
                "recorded_at": NOW.isoformat(),
                "task_id": "partial",
                "attempt_id": "00000000-0000-4000-8000-000000000051",
            },
        ]
        for row in partial_rows:
            with self.subTest(event_type=row["event_type"]), tempfile.TemporaryDirectory() as tmp:
                ledger = Path(tmp) / "execution.jsonl"
                ledger.write_text(json.dumps(row) + "\n")
                with self.assertRaises(ValueError):
                    controller.read_execution_events(ledger)

    def test_duplicate_attempt_id_is_rejected_under_concurrent_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            attempt = "00000000-0000-4000-8000-000000000060"
            errors = []
            successes = []

            def write_preflight(task_id):
                try:
                    successes.append(
                        controller.record_preflight(
                            task_id=task_id,
                            task="Concurrent draft",
                            attempt_id=attempt,
                            task_kind="buyer_copy",
                            size="medium",
                            estimated_burn=8,
                            estimated_minutes=12,
                            batch_items=25,
                            forced=False,
                            result=self._route(),
                            ledger_path=ledger,
                            recorded_at=NOW,
                        )
                    )
                except Exception as exc:  # pragma: no cover - assertions inspect it
                    errors.append(exc)

            threads = [threading.Thread(target=write_preflight, args=(f"task-{i}",)) for i in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.assertEqual(len(successes), 1)
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], ValueError)
            self.assertIn("attempt_id already exists", str(errors[0]))
            self.assertEqual(len(controller.read_execution_events(ledger)), 1)

    def test_symlink_alias_uses_same_lock_and_attempt_namespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            alias = Path(tmp) / "alias.jsonl"
            alias.symlink_to(ledger)
            attempt = "00000000-0000-4000-8000-000000000061"
            errors = []
            successes = []

            def write_preflight(path, task_id):
                try:
                    successes.append(
                        controller.record_preflight(
                            task_id=task_id,
                            task="Alias draft",
                            attempt_id=attempt,
                            task_kind="buyer_copy",
                            size="medium",
                            estimated_burn=8,
                            estimated_minutes=12,
                            batch_items=25,
                            forced=False,
                            result=self._route(),
                            ledger_path=path,
                            recorded_at=NOW,
                        )
                    )
                except Exception as exc:  # pragma: no cover - assertions inspect it
                    errors.append(exc)

            threads = [
                threading.Thread(target=write_preflight, args=(ledger, "real")),
                threading.Thread(target=write_preflight, args=(alias, "alias")),
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.assertEqual(len(successes), 1)
            self.assertEqual(len(errors), 1)
            self.assertEqual(len(controller.read_execution_events(ledger)), 1)
            self.assertEqual(len(list(Path(tmp).glob("*.lock"))), 1)

    def test_hard_linked_execution_ledger_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            alias = Path(tmp) / "hardlink.jsonl"
            ledger.write_text("")
            os.link(ledger, alias)
            with self.assertRaisesRegex(ValueError, "hard-linked"):
                controller.read_execution_events(alias)

    def test_orphan_and_duplicate_completions_are_rejected(self):
        completion = {
            "schema_version": "routing-execution-v1",
            "event_type": "complete",
            "recorded_at": (NOW + timedelta(minutes=5)).isoformat(),
            "task_id": "copy-25",
            "attempt_id": "00000000-0000-4000-8000-000000000062",
            "task_kind": "buyer_copy",
            "provider": "codex",
            "elapsed_minutes": 5.0,
            "tool_calls": 2,
            "provider_delta": None,
            "avoidable_delay_minutes": 0.0,
            "delivery_status": "delivered",
            "sla_verdict": "on_target",
        }
        with tempfile.TemporaryDirectory() as tmp:
            orphan = Path(tmp) / "orphan.jsonl"
            orphan.write_text(json.dumps(completion) + "\n")
            with self.assertRaisesRegex(ValueError, "matching preflight"):
                controller.read_execution_events(orphan)

            ledger = Path(tmp) / "duplicate.jsonl"
            preflight = {
                "schema_version": "routing-execution-v1",
                "event_type": "preflight",
                "recorded_at": NOW.isoformat(),
                "task_id": "copy-25",
                "attempt_id": completion["attempt_id"],
                "task": "Draft copy",
                "task_kind": "buyer_copy",
                "size": "medium",
                "estimated_burn": 8.0,
                "estimated_minutes": 12.0,
                "batch_items": 25,
                "decision": "route",
                "provider": "codex",
                "reason": "test",
                "tracking_required": True,
            }
            ledger.write_text("\n".join(map(json.dumps, [preflight, completion, completion])) + "\n")
            with self.assertRaisesRegex(ValueError, "already complete"):
                controller.read_execution_events(ledger)

    def test_completion_must_match_preflight_semantics_and_elapsed_time(self):
        base_preflight = {
            "schema_version": "routing-execution-v1",
            "event_type": "preflight",
            "recorded_at": NOW.isoformat(),
            "task_id": "research-1",
            "attempt_id": "00000000-0000-4000-8000-000000000065",
            "task": "Research",
            "task_kind": "research",
            "size": "medium",
            "estimated_burn": 8.0,
            "estimated_minutes": 12.0,
            "batch_items": 25,
            "decision": "route",
            "provider": "claude",
            "reason": "test",
            "tracking_required": True,
        }
        base_completion = {
            "schema_version": "routing-execution-v1",
            "event_type": "complete",
            "recorded_at": (NOW + timedelta(minutes=5)).isoformat(),
            "task_id": "research-1",
            "attempt_id": base_preflight["attempt_id"],
            "task_kind": "research",
            "provider": "claude",
            "elapsed_minutes": 5.0,
            "tool_calls": 2,
            "provider_delta": None,
            "avoidable_delay_minutes": 0.0,
            "delivery_status": "delivered",
            "sla_verdict": "not_applicable",
        }
        bad_completions = [
            {**base_completion, "task_kind": "buyer_copy", "provider": "codex", "sla_verdict": "on_target"},
            {**base_completion, "elapsed_minutes": 4.0},
            {**base_completion, "recorded_at": (NOW - timedelta(minutes=1)).isoformat(), "elapsed_minutes": 1.0},
        ]
        for completion in bad_completions:
            with self.subTest(completion=completion), tempfile.TemporaryDirectory() as tmp:
                ledger = Path(tmp) / "execution.jsonl"
                ledger.write_text("\n".join(map(json.dumps, [base_preflight, completion])) + "\n")
                with self.assertRaises(ValueError):
                    controller.read_execution_events(ledger)

    def test_json_booleans_are_not_accepted_as_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            row = {
                "schema_version": "routing-execution-v1",
                "event_type": "preflight",
                "recorded_at": NOW.isoformat(),
                "task_id": "boolean",
                "attempt_id": "00000000-0000-4000-8000-000000000063",
                "task": "Boolean draft",
                "task_kind": "buyer_copy",
                "size": "medium",
                "estimated_burn": True,
                "estimated_minutes": False,
                "batch_items": 25,
                "decision": "route",
                "provider": "codex",
                "reason": "test",
                "tracking_required": True,
            }
            ledger.write_text(json.dumps(row) + "\n")
            with self.assertRaises(ValueError):
                controller.read_execution_events(ledger)

    def test_nonstring_timestamp_is_controlled_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            row = {
                "schema_version": "routing-execution-v1",
                "event_type": "preflight",
                "recorded_at": 123,
                "task_id": "timestamp",
                "attempt_id": "00000000-0000-4000-8000-000000000064",
            }
            ledger.write_text(json.dumps(row) + "\n")
            with self.assertRaisesRegex(ValueError, "recorded_at"):
                controller.read_execution_events(ledger)

    def test_concurrent_appends_preserve_complete_json_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            errors = []

            def write_row(index):
                try:
                    controller.append_execution_event(
                        ledger,
                        {
                            "schema_version": "routing-execution-v1",
                            "event_type": "preflight",
                            "recorded_at": NOW.isoformat(),
                            "task_id": f"task-{index}",
                            "attempt_id": f"00000000-0000-4000-8000-{index:012d}",
                            "task": "Concurrent write",
                            "task_kind": "buyer_copy",
                            "size": "medium",
                            "estimated_burn": 8.0,
                            "estimated_minutes": 12.0,
                            "batch_items": 25,
                            "decision": "route",
                            "provider": "codex",
                            "reason": "test",
                            "tracking_required": True,
                        },
                    )
                except Exception as exc:  # pragma: no cover - assertion captures details
                    errors.append(exc)

            threads = [threading.Thread(target=write_row, args=(index,)) for index in range(20)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(errors, [])
            rows = controller.read_execution_events(ledger)
            self.assertEqual(len(rows), 20)
            self.assertEqual({row["task_id"] for row in rows}, {f"task-{i}" for i in range(20)})


class CompletionTelemetryTests(unittest.TestCase):
    ATTEMPT = "00000000-0000-4000-8000-000000000101"

    def _preflight(self, ledger, decision="route", task_id="copy-25", task_kind="buyer_copy"):
        return controller.record_preflight(
            task_id=task_id,
            task="Draft copy",
            attempt_id=self.ATTEMPT,
            task_kind=task_kind,
            size="medium",
            estimated_burn=8,
            estimated_minutes=12,
            batch_items=25,
            forced=False,
            result={
                "decision": decision,
                "provider": "codex" if decision == "route" else None,
                "reason": "test",
            },
            ledger_path=ledger,
            recorded_at=NOW,
        )

    def _complete(self, ledger, minutes=12, delivered=True, task_id="copy-25", **changes):
        values = dict(
            task_id=task_id,
            attempt_id=self.ATTEMPT,
            tool_calls=8,
            provider_delta=None,
            avoidable_delay_minutes=0,
            delivered=delivered,
            ledger_path=ledger,
            recorded_at=NOW + timedelta(minutes=minutes),
        )
        values.update(changes)
        return controller.record_completion(**values)

    def test_completion_requires_matching_routed_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            with self.assertRaises(ValueError):
                self._complete(ledger)
            self._preflight(ledger)
            with self.assertRaises(ValueError):
                self._complete(ledger, task_id="wrong-task")
            self.assertEqual(len(controller.read_execution_events(ledger)), 1)

    def test_blocked_and_duplicate_completion_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocked = Path(tmp) / "blocked.jsonl"
            self._preflight(blocked, decision="block")
            with self.assertRaises(ValueError):
                self._complete(blocked)
            live = Path(tmp) / "live.jsonl"
            self._preflight(live)
            self._complete(live)
            with self.assertRaises(ValueError):
                self._complete(live, minutes=13)
            self.assertEqual(len(controller.read_execution_events(live)), 2)

    def test_buyer_copy_sla_boundaries_and_elapsed_calculation(self):
        cases = [
            (12, True, "on_target"),
            (12.01, True, "warning"),
            (15, True, "warning"),
            (15.01, True, "breach"),
            (5, False, "missed_delivery"),
        ]
        for index, (minutes, delivered, expected) in enumerate(cases):
            with self.subTest(minutes=minutes, delivered=delivered), tempfile.TemporaryDirectory() as tmp:
                ledger = Path(tmp) / "execution.jsonl"
                self._preflight(ledger)
                event = self._complete(ledger, minutes=minutes, delivered=delivered)
                self.assertAlmostEqual(event["elapsed_minutes"], minutes)
                self.assertEqual(event["sla_verdict"], expected)

    def test_non_buyer_copy_sla_is_not_applicable(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            self._preflight(ledger, task_kind="research")
            event = self._complete(ledger)
            self.assertEqual(event["sla_verdict"], "not_applicable")

    def test_unknown_provider_delta_is_json_null(self):
        self.assertIsNone(controller.parse_provider_delta("unknown"))
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            self._preflight(ledger)
            event = self._complete(ledger, provider_delta=controller.parse_provider_delta("unknown"))
            self.assertIsNone(event["provider_delta"])

    def test_invalid_completion_telemetry_does_not_mutate_ledger(self):
        bad_values = [
            {"tool_calls": -1},
            {"tool_calls": 1.5},
            {"provider_delta": -1},
            {"provider_delta": 101},
            {"provider_delta": math.nan},
            {"avoidable_delay_minutes": -1},
            {"avoidable_delay_minutes": math.inf},
            {"avoidable_delay_minutes": 13},
        ]
        for change in bad_values:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                ledger = Path(tmp) / "execution.jsonl"
                self._preflight(ledger)
                with self.assertRaises(ValueError):
                    self._complete(ledger, minutes=12, **change)
                self.assertEqual(len(controller.read_execution_events(ledger)), 1)


class ExecutionSummaryTests(unittest.TestCase):
    def _completion(self, recorded_at, task_id, delivered, elapsed, tool_calls, delay, sla):
        return {
            "schema_version": "routing-execution-v1",
            "event_type": "complete",
            "recorded_at": recorded_at.isoformat(),
            "task_id": task_id,
            "attempt_id": f"00000000-0000-4000-8000-{int(task_id.split('-')[-1]):012d}",
            "task_kind": "buyer_copy",
            "provider": "codex",
            "elapsed_minutes": elapsed,
            "tool_calls": tool_calls,
            "provider_delta": None,
            "avoidable_delay_minutes": delay,
            "delivery_status": "delivered" if delivered else "not_delivered",
            "sla_verdict": sla,
        }

    def _preflight(self, completion):
        return {
            "schema_version": "routing-execution-v1",
            "event_type": "preflight",
            "recorded_at": (
                datetime.fromisoformat(completion["recorded_at"])
                - timedelta(minutes=completion["elapsed_minutes"])
            ).isoformat(),
            "task_id": completion["task_id"],
            "attempt_id": completion["attempt_id"],
            "task": "Summary fixture",
            "task_kind": completion["task_kind"],
            "size": "medium",
            "estimated_burn": 8.0,
            "estimated_minutes": 12.0,
            "batch_items": 25,
            "decision": "route",
            "provider": completion["provider"],
            "reason": "test",
            "tracking_required": True,
        }

    def test_empty_summary_has_stable_zero_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = controller.summarize_execution(Path(tmp) / "missing.jsonl", 7, NOW)
            self.assertEqual(result["completion_count"], 0)
            self.assertIsNone(result["median_elapsed_minutes"])
            self.assertIsNone(result["median_tool_calls"])
            self.assertEqual(
                result["buyer_copy_sla"],
                {"on_target": 0, "warning": 0, "breach": 0, "missed_delivery": 0},
            )

    def test_summary_uses_inclusive_utc_window_and_attempt_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            cutoff = NOW - timedelta(days=7)
            rows = [
                self._completion(cutoff, "task-1", True, 10, 6, 0, "on_target"),
                self._completion(NOW, "task-2", True, 14, 10, 2, "warning"),
                self._completion(NOW - timedelta(days=1), "task-3", True, 18, 8, 3, "breach"),
                self._completion(NOW - timedelta(days=2), "task-4", False, 5, 4, 1, "missed_delivery"),
                self._completion(cutoff - timedelta(microseconds=1), "task-5", True, 1, 1, 0, "on_target"),
            ]
            for row in rows:
                controller.append_execution_event(ledger, self._preflight(row))
                controller.append_execution_event(ledger, row)
            result = controller.summarize_execution(ledger, 7, NOW)
            self.assertEqual(result["completion_count"], 4)
            self.assertEqual(result["delivered_count"], 3)
            self.assertEqual(result["undelivered_count"], 1)
            self.assertEqual(result["median_elapsed_minutes"], 12)
            self.assertEqual(result["median_tool_calls"], 7)
            self.assertEqual(result["avoidable_delay_minutes"], 6)
            self.assertEqual(
                result["buyer_copy_sla"],
                {"on_target": 1, "warning": 1, "breach": 1, "missed_delivery": 1},
            )

    def test_repeated_task_ids_count_as_distinct_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "execution.jsonl"
            first = self._completion(NOW, "task-10", True, 10, 3, 0, "on_target")
            second = self._completion(NOW, "task-11", True, 11, 4, 0, "on_target")
            second["task_id"] = first["task_id"]
            controller.append_execution_event(ledger, self._preflight(first))
            controller.append_execution_event(ledger, first)
            controller.append_execution_event(ledger, self._preflight(second))
            controller.append_execution_event(ledger, second)
            result = controller.summarize_execution(ledger, 7, NOW)
            self.assertEqual(result["completion_count"], 2)


class CliCompatibilityTests(unittest.TestCase):
    def _current(self, path):
        payload = {
            "schema_version": 1,
            "providers": {
                "codex": snapshot("codex", 99),
                "claude": snapshot("claude", 99),
            },
        }
        for provider in payload["providers"].values():
            provider["captured_at"] = controller.utc_now().isoformat()
        path.write_text(json.dumps(payload))

    def _main(self, args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = controller.main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_legacy_preflight_keeps_exit_semantics_without_ledger_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "current.json"
            execution = Path(tmp) / "execution.jsonl"
            self._current(current)
            code, output, _ = self._main(
                [
                    "--current", str(current),
                    "--execution-ledger", str(execution),
                    "preflight", "--task", "legacy", "--task-kind", "research",
                    "--size", "small", "--estimated-burn", "3",
                ]
            )
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output)["decision"], "route")
            self.assertFalse(json.loads(output)["tracking_required"])
            self.assertFalse(execution.exists())

    def test_tracked_preflight_prints_attempt_and_completion_prints_sla(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "current.json"
            execution = Path(tmp) / "execution.jsonl"
            self._current(current)
            preflight_args = [
                "--current", str(current), "--execution-ledger", str(execution),
                "preflight", "--task-id", "copy-25", "--task", "Draft copy",
                "--task-kind", "buyer_copy", "--size", "medium",
                "--estimated-burn", "8", "--estimated-minutes", "12", "--batch-items", "25",
            ]
            code, output, _ = self._main(preflight_args)
            payload = json.loads(output)
            self.assertEqual(code, 0)
            self.assertTrue(payload["tracking_required"])
            UUID(payload["attempt_id"])
            code, output, _ = self._main(
                [
                    "--execution-ledger", str(execution), "complete",
                    "--task-id", "copy-25", "--attempt-id", payload["attempt_id"],
                    "--tool-calls", "8", "--provider-delta", "unknown",
                    "--avoidable-delay-minutes", "0", "--delivered",
                ]
            )
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output)["sla_verdict"], "on_target")

    def test_mandatory_tracking_without_task_id_fails_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "current.json"
            execution = Path(tmp) / "execution.jsonl"
            self._current(current)
            code, _, error = self._main(
                [
                    "--current", str(current), "--execution-ledger", str(execution),
                    "preflight", "--task", "Draft copy", "--task-kind", "buyer_copy",
                    "--size", "medium", "--estimated-burn", "8",
                ]
            )
            self.assertEqual(code, 2)
            self.assertIn("task_id", error)
            self.assertFalse(execution.exists())

    def test_summary_cli_prints_stable_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            execution = Path(tmp) / "execution.jsonl"
            code, output, _ = self._main(
                ["--execution-ledger", str(execution), "summary", "--days", "7"]
            )
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output)["completion_count"], 0)

    def test_nonfinite_estimated_burn_returns_controlled_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "current.json"
            execution = Path(tmp) / "execution.jsonl"
            self._current(current)
            code, output, error = self._main(
                [
                    "--current", str(current), "--execution-ledger", str(execution),
                    "preflight", "--task-id", "nan", "--task", "Bad burn",
                    "--task-kind", "buyer_copy", "--size", "medium",
                    "--estimated-burn", "nan",
                ]
            )
            self.assertEqual(code, 2)
            self.assertEqual(output, "")
            self.assertIn("estimated_burn", error)
            self.assertFalse(execution.exists())

    def test_malformed_record_inputs_return_controlled_exit(self):
        cases = [
            ["record", "--provider", "codex", "--remaining", "nan", "--source", "test"],
            [
                "record", "--provider", "codex", "--remaining", "50",
                "--captured-at", "not-a-time", "--source", "test",
            ],
        ]
        for command in cases:
            with self.subTest(command=command), tempfile.TemporaryDirectory() as tmp:
                current = Path(tmp) / "current.json"
                ledger = Path(tmp) / "usage.jsonl"
                code, output, error = self._main(
                    ["--current", str(current), "--ledger", str(ledger), *command]
                )
                self.assertEqual(code, 2)
                self.assertEqual(output, "")
                self.assertTrue(error.strip())
                self.assertFalse(current.exists())
                self.assertFalse(ledger.exists())

    def test_malformed_current_state_returns_controlled_exit_only_when_needed(self):
        malformed_payloads = ["{not-json}", "[]", "null", '"text"', '{"providers": []}']
        for payload in malformed_payloads:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as tmp:
                current = Path(tmp) / "current.json"
                execution = Path(tmp) / "execution.jsonl"
                current.write_text(payload)
                code, output, error = self._main(
                    [
                        "--current", str(current), "--execution-ledger", str(execution),
                        "preflight", "--task-id", "state-check", "--task", "State check",
                        "--task-kind", "buyer_copy", "--size", "medium",
                        "--estimated-burn", "8",
                    ]
                )
                self.assertEqual(code, 2)
                self.assertEqual(output, "")
                self.assertTrue(error.strip())
                self.assertFalse(execution.exists())

                code, output, error = self._main(
                    [
                        "--current", str(current), "--execution-ledger", str(execution),
                        "summary", "--days", "7",
                    ]
                )
                self.assertEqual(code, 0)
                self.assertEqual(json.loads(output)["completion_count"], 0)
                self.assertEqual(error, "")


class RoutingV2AcceptanceHarnessTests(unittest.TestCase):
    def test_acceptance_writes_named_report_without_touching_production_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "acceptance.json"
            process = subprocess.run(
                [sys.executable, "scripts/routing_v2_acceptance.py", "--report", str(report)],
                cwd=controller.ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertIn("ROUTING_V2_ACCEPTANCE_OK", process.stdout)
            payload = json.loads(report.read_text())
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["events"], 2)
            self.assertEqual(payload["sla_verdict"], "on_target")
            self.assertIsNone(payload["provider_delta"])
            self.assertTrue(payload["production_ledger_unchanged"])

    def test_acceptance_rejects_report_aliasing_production_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            production = Path(tmp) / "execution.jsonl"
            process = subprocess.run(
                [
                    sys.executable,
                    "scripts/routing_v2_acceptance.py",
                    "--production-ledger", str(production),
                    "--report", str(production),
                ],
                cwd=controller.ROOT,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(process.returncode, 0)
            self.assertIn("must not resolve to the production ledger", process.stderr)
            self.assertFalse(production.exists())

    def test_acceptance_rejects_hard_link_alias_of_production_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            production = Path(tmp) / "execution.jsonl"
            report = Path(tmp) / "report.json"
            production.write_text("sentinel\n")
            os.link(production, report)
            before = production.read_bytes()
            process = subprocess.run(
                [
                    sys.executable,
                    "scripts/routing_v2_acceptance.py",
                    "--production-ledger", str(production),
                    "--report", str(report),
                ],
                cwd=controller.ROOT,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(process.returncode, 0)
            self.assertIn("must not alias the production ledger", process.stderr)
            self.assertEqual(production.read_bytes(), before)

    def test_acceptance_checks_survive_optimized_python(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "optimized.json"
            production = Path(tmp) / "production.jsonl"
            process = subprocess.run(
                [
                    sys.executable,
                    "-O",
                    "scripts/routing_v2_acceptance.py",
                    "--production-ledger", str(production),
                    "--report", str(report),
                ],
                cwd=controller.ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertIn("ROUTING_V2_ACCEPTANCE_OK", process.stdout)
            self.assertTrue(json.loads(report.read_text())["production_ledger_unchanged"])


if __name__ == "__main__":
    unittest.main()
