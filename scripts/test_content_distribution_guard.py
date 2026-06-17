import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_distribution_guard as guard


class ContentDistributionGuardTests(unittest.TestCase):
    def test_ai_ops_teardown_rejects_prior_teardown_company_reference(self):
        text = """# AppFolio Realm-X Claude AI Ops Teardown

That is why AppFolio connecting Realm-X to Claude is the property-management signal I would post after Canals.

AppFolio is the property-management version.
"""

        problems = guard.check_ai_ops_teardown_prior_company_references(
            Path("memory/content/bank/2026-06-16/ai-ops-teardown-appfolio-realm-x-claude.md"),
            text,
        )

        self.assertTrue(any("prior AI Ops Teardown company" in problem for problem in problems))

    def test_ai_ops_teardown_allows_current_company_reference(self):
        text = """# AppFolio Realm-X Claude AI Ops Teardown

That is why AppFolio connecting Realm-X to Claude is the property-management signal worth watching.
"""

        problems = guard.check_ai_ops_teardown_prior_company_references(
            Path("memory/content/bank/2026-06-16/ai-ops-teardown-appfolio-realm-x-claude.md"),
            text,
        )

        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
