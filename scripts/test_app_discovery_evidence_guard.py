import tempfile
import unittest
from pathlib import Path

import app_discovery_evidence_guard as guard


FAILING = """# Failing Niche OS

## Needs Claims Table

| claim | source_url_or_path | source_snippet | confidence |
|---|---|---|---|
| Users need a faster way to compare skincare routines. | https://example.com/review |  | high |
"""


PASSING = """# Passing Niche OS

## Needs Claims Table

| claim | source_url_or_path | source_snippet | confidence | unverified_reason |
|---|---|---|---|---|
| Users compare products by ingredient conflict. | https://example.com/review | "I need to know what clashes before buying." | high |  |
| Users might share scorecards if they look credible. | UNVERIFIED |  | UNVERIFIED | No direct source yet; must validate in Stage 4 distribution gate. |
"""


class AppDiscoveryEvidenceGuardTests(unittest.TestCase):
    def test_missing_source_snippet_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "niche_os.md"
            path.write_text(FAILING)

            result = guard.check_files([path])

            self.assertFalse(result["ok"])
            self.assertEqual(result["claims_checked"], 1)
            self.assertTrue(any("missing source_snippet" in p for p in result["problems"]))

    def test_all_claims_sourced_or_unverified_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "niche_os.md"
            path.write_text(PASSING)

            result = guard.check_files([path])

            self.assertTrue(result["ok"])
            self.assertEqual(result["claims_checked"], 2)
            self.assertEqual(result["problems"], [])


if __name__ == "__main__":
    unittest.main()
