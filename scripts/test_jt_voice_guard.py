#!/usr/bin/env python3
"""Regression tests for the JT voice guard."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jt_voice_guard


def score_text(text: str, platform: str = "linkedin") -> tuple[int, list[str], list[str]]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
        handle.write(text)
        path = Path(handle.name)
    try:
        return jt_voice_guard.score(path, platform)
    finally:
        path.unlink(missing_ok=True)


class JTVoiceGuardStopSlopTests(unittest.TestCase):
    def assert_problem_contains(self, text: str, expected: str) -> None:
        _points, problems, _notes = score_text(text)
        self.assertTrue(
            any(expected in problem for problem in problems),
            f"Expected problem containing {expected!r}; got {problems!r}",
        )

    def test_flags_false_agency(self) -> None:
        self.assert_problem_contains(
            """The data tells us the workflow is ready.

The tenant email, owner rule, spreadsheet, approval queue, and maintenance log all point to the same issue.

A manager still needs to review the flagged rows before the record changes.""",
            "false agency",
        )

    def test_flags_narrator_from_distance(self) -> None:
        self.assert_problem_contains(
            """People tend to miss the approval problem.

The tenant email, owner rule, spreadsheet, approval queue, and maintenance log all point to the same issue.

A manager still needs to review the flagged rows before the record changes.""",
            "narrator-from-distance",
        )

    def test_flags_vague_declarative(self) -> None:
        self.assert_problem_contains(
            """The stakes are high.

The tenant email, owner rule, spreadsheet, approval queue, and maintenance log all point to the same issue.

A manager still needs to review the flagged rows before the record changes.""",
            "vague declarative",
        )

    def test_flags_wh_opener_setup(self) -> None:
        self.assert_problem_contains(
            """What makes this hard is the approval path.

The tenant email, owner rule, spreadsheet, approval queue, and maintenance log all point to the same issue.

A manager still needs to review the flagged rows before the record changes.""",
            "Wh-opener setup",
        )

    def test_flags_pull_quote_ending(self) -> None:
        self.assert_problem_contains(
            """A tenant email and owner rule should land in the same queue.

The spreadsheet, approval path, maintenance log, and manager review decide whether the workflow survives.

That's the lesson.""",
            "pull-quote",
        )

    def test_flags_high_confidence_passive_voice(self) -> None:
        self.assert_problem_contains(
            """The tenant approval workflow was created without an owner.

The tenant email, owner rule, spreadsheet, approval queue, and maintenance log all point to the same issue.

A manager still needs to review the flagged rows before the record changes.""",
            "passive voice",
        )

    def test_flags_linkedin_era_framing(self) -> None:
        self.assert_problem_contains(
            """Something shifted on LinkedIn in 2026 and most people missed it.

The tenant email, owner rule, spreadsheet, approval queue, maintenance log, and manager review are still the real proof layer.

Era 3 content wins when the author proves the workflow could only come from them.""",
            "grand era-framing",
        )

    def test_good_jt_proof_sample_still_passes(self) -> None:
        points, problems, notes = score_text(
            """Built the workflow on a local office machine.

It reads tenant emails, checks the lease spreadsheet, flags owner rules, and puts sensitive rows in a manager approval queue.

The local machine matters because the workflow can run near the client's files without creating a new IT problem.""",
        )
        self.assertGreaterEqual(points, 80)
        self.assertEqual(problems, [])
        self.assertTrue(notes)

    def test_jt_selected_yair_proof_sample_passes(self) -> None:
        points, problems, notes = score_text(
            """Built this AI workflow for Yair and his real estate firm.

A dedicated mini PC in their office, connected to their existing systems, running automated workflows 24/7.

11% to 78% compliance jump. $85K saved annually.

Real estate operations is one of the best verticals for this kind of AI automation. @YairsQuest and I are just getting started.""",
            platform="x",
        )
        self.assertGreaterEqual(points, 80)
        self.assertEqual(problems, [])
        self.assertTrue(notes)

    def test_jt_selected_jarvis_linkedin_sample_passes(self) -> None:
        points, problems, notes = score_text(
            """Yesterday I installed a dedicated automation PC for a NYC real estate family office.

They decided to name it Jarvis.

The machine will host 6 automated workflows I built for them, covering insurance expiration tracking, QuickBooks data entry, validation checks, and other back-office tasks that used to require manual follow-up.

The dedicated PC lets the workflows run locally without touching their existing servers, changing their current setup, or introducing unnecessary risk into systems they already depend on.

That is a big part of real AI implementation for established businesses.

The work is not just building the workflow. It is giving the business a safe operating environment where the workflow can run every week without creating a new security headache.

The system handles the repetitive work, and the team only gets notified when something actually needs human attention.

Projected time saved: 10-20 hours per week.""",
        )
        self.assertGreaterEqual(points, 80)
        self.assertEqual(problems, [])
        self.assertTrue(notes)

    def test_live_jts14_x_sample_passes(self) -> None:
        points, problems, _notes = score_text(
            "Lead capturing from NYC ballet family contributors page.",
            platform="x",
        )
        self.assertGreaterEqual(points, 80)
        self.assertEqual(problems, [])

    def test_flags_linkedin_funnel_bro_language_even_with_workflow_nouns(self) -> None:
        points, problems, _notes = score_text(
            """The tenant intake workflow now has an approval queue.

The spreadsheet, email inbox, owner rule, maintenance log, lease record, and manager review make this more than content. It is a proof engine and trust layer for qualified buyers to raise their hand.

That is how content becomes pipeline.""",
        )
        self.assertLess(points, 80)
        self.assertTrue(
            any("funnel" in problem for problem in problems),
            f"Expected funnel problem; got {problems!r}",
        )

    def test_single_family_does_not_trigger_ngl(self) -> None:
        points, problems, _notes = score_text(
            """Built a readiness checklist for single-family rentals and small property teams.

It checks tenant emails, owner rules, maintenance logs, rent roll exports, approval queues, and exception paths before any automation is built.

That keeps the workflow anchored to the record the property manager actually trusts.""",
        )
        self.assertGreaterEqual(points, 80)
        self.assertFalse(
            any("ngl" in problem for problem in problems),
            f"Unexpected casual-language false positive; got {problems!r}",
        )


if __name__ == "__main__":
    unittest.main()
