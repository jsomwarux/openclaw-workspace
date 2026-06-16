#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

import build_jts14_x_reference_ledger as builder
import content_distribution_guard as distribution_guard
import jts14_x_reference_ledger_guard as ledger_guard


class Jts14XReferenceLedgerTests(unittest.TestCase):
    def test_build_ledger_creates_valid_rows_from_saved_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            report = workspace / "report.md"
            replies = workspace / "reply-targets.md"
            weekly = workspace / "weekly.md"
            output = workspace / "ledger.md"

            report.write_text(
                """# Viral Post Swipe File — X Research — 2026-06-15

## Usable Posts
- @jasonlk — 21+ AI agents in production. Relevant because it turns agent discourse into production metrics JT can translate into review queues and approval logs. https://x.com/jasonlk/status/1
- @SalesforceDevs — Agentforce Builder / Agent Script event post. Relevant for reply targeting, not strong enough for swipe by engagement. https://x.com/SalesforceDevs/status/2

## Low Signal / Rejected
- AI consulting query was mostly generic money-making list content.
- n8n query was mostly low-impression promos.
""",
                encoding="utf-8",
            )
            replies.write_text(
                """# X Reply Targets — 2026-06-15

## @jasonlk (242k)
Link: https://x.com/jasonlk/status/1
Draft reply: I would want to see the queue, stops, reviews, and logging.

## @VannDough (1.9k)
Link: https://x.com/VannDough/status/3
Draft reply: Wallet access needs budgets, receipts, and shutdown rules.
""",
                encoding="utf-8",
            )
            weekly.write_text(
                """## X Reference Mechanics
Reference row 1:
Source URL: https://x.com/dimoflexx/status/4
Niche: AI Operating Systems / Agent Orchestration
Hook mechanic: Concrete spend before technical claim.
JT translation: Local only matters with memory, logs, and review rules.
""",
                encoding="utf-8",
            )

            rows = builder.build_ledger(report=report, replies=replies, weekly=weekly, output=output)

            self.assertGreaterEqual(len(rows), 5)
            self.assertTrue(output.exists())
            self.assertEqual([], ledger_guard.check(output))

    def test_distribution_guard_requires_valid_jts14_ledger_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            weekly = workspace / "weekly.md"
            missing_ledger = workspace / "missing-ledger.md"
            weekly.write_text(
                """# Weekly Content - 2026-06-15

## Seeds used this week
Recovered.

## Hook mappings
- Monday LinkedIn: approval queue.

## LinkedIn
### Monday
**Date:** 2026-06-15
Approval queue proof.

## X
### Monday
**Date:** 2026-06-15
Approval queue proof.

## Constraint log
- No private data.
"""
                + ("x" * 1600),
                encoding="utf-8",
            )

            problems = distribution_guard.check_required_jts14_ledger(
                weekly_path=weekly,
                ledger_path=missing_ledger,
            )

            self.assertIn("jts14 X reference ledger missing", "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
