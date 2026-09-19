import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "mission_control_north_star_audit.py"
SPEC = importlib.util.spec_from_file_location("mission_control_north_star_audit", SCRIPT_PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(AUDIT)


class DesiredTaskStateTests(unittest.TestCase):
    def test_immutable_outreach_review_card_is_not_generically_patched(self):
        task = {
            "title": "Review outreach draft: synthetic-no-send / synthetic-capability-123 / cycle 1",
            "project": "AI Workflow Growth OS",
            "description": "Synthetic proof card owned by the outreach review workflow.",
            "priority": "high",
            "sortOrder": None,
            "status": "todo",
        }

        self.assertEqual(AUDIT.desired_for(task), (None, None))

    def test_regular_unsorted_high_task_is_still_demoted(self):
        task = {
            "title": "Uncontrolled high-priority task",
            "project": "Operations",
            "description": "Needs explicit North Star ownership.",
            "priority": "high",
            "sortOrder": None,
            "status": "todo",
        }

        desired, reason = AUDIT.desired_for(task)

        self.assertEqual(reason, "demote unsorted high task")
        self.assertEqual(desired["priority"], "medium")
        self.assertEqual(desired["sortOrder"], 160)


if __name__ == "__main__":
    unittest.main()
