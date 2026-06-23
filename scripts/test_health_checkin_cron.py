import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

import health_checkin_cron as cron


class HealthCheckinCronTests(unittest.TestCase):
    def test_prepare_skips_when_pending_date_matches_today(self):
        with tempfile.TemporaryDirectory() as tmp:
            pending = Path(tmp) / "pending-checkin.json"
            pending.write_text(json.dumps({"date": "2026-06-22", "sent_at": 123}))

            result = cron.prepare(
                pending,
                now=datetime(2026, 6, 22, 21, 5, tzinfo=ZoneInfo("America/New_York")),
            )

            self.assertEqual(result["action"], "skip")
            self.assertEqual(result["date"], "2026-06-22")
            self.assertEqual(result["status"], "SKIPPED_DUPLICATE_HEALTH_CHECKIN")

    def test_prepare_requests_send_when_pending_is_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            pending = Path(tmp) / "pending-checkin.json"
            pending.write_text(json.dumps({"date": "2026-06-21", "sent_at": 123}))

            result = cron.prepare(
                pending,
                now=datetime(2026, 6, 22, 21, 5, tzinfo=ZoneInfo("America/New_York")),
            )

            self.assertEqual(result["action"], "send")
            self.assertEqual(result["date"], "2026-06-22")
            self.assertIn("Evening Check-in", result["message"])

    def test_mark_sent_writes_compact_pending_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            pending = Path(tmp) / "pending-checkin.json"

            result = cron.mark_sent(pending, "2026-06-22", sent_at=1782177221)

            self.assertEqual(result["status"], "HEALTH_CHECKIN_SENT")
            self.assertEqual(
                json.loads(pending.read_text()),
                {
                    "date": "2026-06-22",
                    "handler": "health_checkin_cron.py",
                    "sent_at": 1782177221,
                    "status": "sent",
                },
            )


if __name__ == "__main__":
    unittest.main()
