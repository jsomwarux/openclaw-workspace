import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


spec = importlib.util.spec_from_file_location(
    "model_routing_guard",
    Path(__file__).resolve().with_name("model_routing_guard.py"),
)
model_routing_guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_routing_guard)


class ModelRoutingGuardTests(unittest.TestCase):
    def test_main_uses_live_cron_list_when_legacy_jobs_json_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config_path = tmp_path / "openclaw.json"
            missing_jobs_path = tmp_path / "missing-jobs.json"
            config_path.write_text(
                json.dumps(
                    {
                        "agents": {
                            "defaults": {
                                "model": {"primary": "openai/gpt-5.5", "fallbacks": []},
                                "models": {"openai/gpt-5.5": {}},
                            }
                        },
                        "models": {"providers": {}},
                    }
                )
            )

            cli_payload = {
                "jobs": [
                    {
                        "id": "safe-job",
                        "name": "Safe Job",
                        "enabled": True,
                        "payload": {"model": "openai/gpt-5.5"},
                    }
                ]
            }

            completed = subprocess.CompletedProcess(
                ["openclaw", "cron", "list", "--json"],
                0,
                stdout="Config warnings:\n" + json.dumps(cli_payload),
                stderr="",
            )

            with mock.patch.object(model_routing_guard, "OPENCLAW_CONFIG", config_path), \
                mock.patch.object(model_routing_guard, "CRON_JOBS", missing_jobs_path), \
                mock.patch.object(sys, "argv", ["model_routing_guard.py"]), \
                mock.patch("subprocess.run", return_value=completed):
                self.assertEqual(model_routing_guard.main(), 0)


if __name__ == "__main__":
    unittest.main()
