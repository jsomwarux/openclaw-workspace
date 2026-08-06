import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import protocol_ops


class ProtocolOpsTests(unittest.TestCase):
    def test_bookings_parse_reference_section(self):
        text = """# Ref

| # | Appointment | Status | Date |
|---|---|---|---|
| 1 | Prescriber | OUTSTANDING | - |
| 2 | Laryngologist | BOOKED | 2026-08-06 |
| 3 | Therapist | OUTSTANDING | - |

## Next
"""
        self.assertEqual(protocol_ops.bookings(text), [(1, "prescriber"), (3, "therapist")])

    def test_morning_message_is_fixed_shape(self):
        msg = protocol_ops.morning_message()["message"]
        self.assertTrue(msg.startswith("Resting HR?\nBookings outstanding: "))

    def test_log_tracker_appends_json_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "protocol-log.jsonl"
            state = Path(tmp) / "protocol-state.json"
            old = protocol_ops.LOG_PATH
            old_state = protocol_ops.STATE_PATH
            try:
                protocol_ops.LOG_PATH = path
                protocol_ops.STATE_PATH = state
                result = protocol_ops.log_tracker(
                    ["72", "7.5", "N", "Y", "Y", "2", "4", "note"],
                    record_date=date(2026, 8, 5),
                )
            finally:
                protocol_ops.LOG_PATH = old
                protocol_ops.STATE_PATH = old_state

            self.assertEqual(result["status"], "Logged.")
            row = json.loads(path.read_text())
            self.assertEqual(row["date"], "2026-08-05")
            self.assertEqual(row["symptom"], 4)
            self.assertIs(row["alcohol"], False)
            self.assertIs(row["aerobic"], True)

    def test_day7_report_unverified_without_seven_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "protocol-log.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "date": "2026-08-05",
                        "hr_waking": 72,
                        "hours_slept": 7,
                        "alcohol": False,
                        "aerobic": True,
                        "social": True,
                        "symptom": 4,
                    }
                )
                + "\n"
            )
            result = protocol_ops.report(date(2026, 8, 11), path=path)
            self.assertEqual(result["action"], "send")
            self.assertIn("UNVERIFIED", result["message"])

    def test_morning_hr_is_staged_not_appended_to_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "protocol-log.jsonl"
            state = Path(tmp) / "protocol-state.json"
            old_log = protocol_ops.LOG_PATH
            old_state = protocol_ops.STATE_PATH
            try:
                protocol_ops.LOG_PATH = path
                protocol_ops.STATE_PATH = state
                result = protocol_ops.log_morning_hr("68", record_date=date(2026, 8, 5))
            finally:
                protocol_ops.LOG_PATH = old_log
                protocol_ops.STATE_PATH = old_state

            self.assertEqual(result["status"], "Logged.")
            self.assertFalse(path.exists())
            self.assertEqual(json.loads(state.read_text())["morning_hr"]["2026-08-05"], 68)


if __name__ == "__main__":
    unittest.main()
