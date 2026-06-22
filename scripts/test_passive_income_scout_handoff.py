import tempfile
import unittest
from pathlib import Path

import passive_income_scout_handoff as handoff
import passive_income_strategist_delivery_guard as strategist_guard


class PassiveIncomeScoutHandoffTests(unittest.TestCase):
    def test_creates_same_day_scout_report_from_local_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pi_dir = root / "memory" / "passive-income"
            pi_dir.mkdir(parents=True)
            (root / "agents" / "passive-income-scout").mkdir(parents=True)
            (root / "agents" / "passive-income-scout" / "state.json").write_text(
                '{"run_dates":["2026-06-14"]}\n'
            )
            (pi_dir / "weekly-trends.md").write_text("# Weekly Trends\nAI invoice audits\nPermit tracker demand\n" * 10)
            (pi_dir / "weekly-exploding-topics.md").write_text("# Exploding\nMicro compliance tools\n" * 10)
            (pi_dir / "weekly-google-trends.md").write_text("# Google Trends\nlocal AI SEO breakout\n" * 5)
            (pi_dir / "weekly-apis.md").write_text("# APIs\nOpen permits API\n")
            (pi_dir / "weekly-trustmrr.json").write_text('{"items":[{"name":"Tiny AI CRM","mrr":1200}]}\n')

            report = handoff.generate_handoff(root=root, date="2026-06-21")

            report_path = pi_dir / "2026-06-21-scout.md"
            self.assertEqual(report_path, report.path)
            text = report_path.read_text()
            self.assertGreater(len(text), 500)
            self.assertIn("# Passive Income Scout - 2026-06-21", text)
            self.assertIn("DETERMINISTIC HANDOFF", text)
            self.assertIn("## Raw Ideas", text)
            self.assertNotIn("INCOMPLETE", text)
            self.assertGreaterEqual(text.count("### Idea"), 4)

    def test_delivery_guard_creates_degraded_strategist_report_from_scout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pi_dir = root / "memory" / "passive-income"
            pi_dir.mkdir(parents=True)
            scout = pi_dir / "2026-06-21-scout.md"
            scout.write_text(
                "# Passive Income Scout - 2026-06-21\n\n"
                "Status: DETERMINISTIC HANDOFF\n\n"
                "## Raw Ideas\n\n"
                "### Idea 1: OpsProof Radar\n"
                "- **Concept:** source-backed exception packets.\n\n"
                "### Idea 2: NicheRank Pages\n"
                "- **Concept:** AI comparison pages.\n"
            )

            report = strategist_guard.create_degraded_report(root=root, date="2026-06-21")

            text = report.read_text()
            self.assertIn("# Passive Income Strategist - 2026-06-21", text)
            self.assertIn("Status: DEGRADED FALLBACK", text)
            self.assertIn("OpsProof Radar", text)
            self.assertIn("No BUILD recommendation", text)
            self.assertGreater(len(text), 500)

    def test_delivery_marker_must_be_newer_than_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pi_dir = root / "memory" / "passive-income"
            pi_dir.mkdir(parents=True)
            report = pi_dir / "2026-06-21-strategist.md"
            marker = pi_dir / "2026-06-21-strategist-delivery.json"
            marker.write_text(
                '{"ok":true,"channel":"telegram","target":"6608544825","messageId":"old","report":"'
                + str(report)
                + '"}\n'
            )
            report.write_text("# Passive Income Strategist - 2026-06-21\n\nStatus: DEGRADED FALLBACK\n")

            self.assertFalse(strategist_guard.marker_confirms_report(marker, report))


if __name__ == "__main__":
    unittest.main()
