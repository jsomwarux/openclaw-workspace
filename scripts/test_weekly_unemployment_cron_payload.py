#!/usr/bin/env python3
"""Regression test for the weekly unemployment Mission Control task gate."""

import json
import os
import subprocess
import unittest


JOB_ID = "ac53b979-44c6-481b-b2aa-7cb9203e6476"
NODE_BIN = "/opt/homebrew/Cellar/node/26.5.0_1/bin"


class WeeklyUnemploymentCronPayloadTest(unittest.TestCase):
    def test_uses_shared_task_gate_instead_of_raw_id_lookup(self) -> None:
        env = os.environ.copy()
        env["PATH"] = f"{NODE_BIN}:{env.get('PATH', '')}"
        completed = subprocess.run(
            ["openclaw", "cron", "get", JOB_ID],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        job = json.loads(completed.stdout)
        message = job["payload"]["message"]

        self.assertIn("scripts/mission_control_task_gate.py", message)
        self.assertNotIn("matches[0]['id']", message)


if __name__ == "__main__":
    unittest.main()
