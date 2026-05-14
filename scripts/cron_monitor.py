#!/usr/bin/env python3
"""One-shot cron health monitor.

Legacy version used an infinite `cron list` loop with stale job names. This version
is safe for cron/heartbeat use: one scan, JSON/console output, non-zero only on
actual problematic cron state.
"""
from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    raw = subprocess.check_output(["openclaw", "cron", "list", "--json"], text=True)
    data = json.loads(raw)
    problems = []
    for job in data.get("jobs", []):
        if not job.get("enabled"):
            continue
        state = job.get("state") or {}
        if state.get("lastRunStatus") == "error" or int(state.get("consecutiveErrors") or 0) >= 2:
            problems.append({
                "id": job.get("id"),
                "name": job.get("name"),
                "lastRunStatus": state.get("lastRunStatus"),
                "consecutiveErrors": state.get("consecutiveErrors"),
                "lastDeliveryStatus": state.get("lastDeliveryStatus"),
            })
    print(json.dumps({"ok": not problems, "problem_count": len(problems), "problems": problems}, indent=2))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
