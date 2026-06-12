#!/usr/bin/env python3
"""Snapshot OpenClaw cron jobs.json into git for prompt diffability."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


WORKSPACE = Path("/Users/jtsomwaru/.openclaw/workspace")
JOBS_PATH = Path("/Users/jtsomwaru/.openclaw/cron/jobs.json")
SNAPSHOT_DIR = WORKSPACE / "config/cron-snapshots"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=WORKSPACE, text=True, capture_output=True, timeout=30)


def main() -> int:
    if not JOBS_PATH.exists():
        print(f"CRON_SNAPSHOT_ERROR missing jobs.json: {JOBS_PATH}", file=sys.stderr)
        return 1

    raw = JOBS_PATH.read_text(encoding="utf-8")
    parsed = json.loads(raw)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d")
    target = SNAPSHOT_DIR / f"jobs-{stamp}.json"
    target.write_text(json.dumps(parsed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    rel = target.relative_to(WORKSPACE)
    add = run(["git", "add", str(rel)])
    if add.returncode != 0:
        print(add.stderr.strip() or add.stdout.strip(), file=sys.stderr)
        return add.returncode

    diff = run(["git", "diff", "--cached", "--quiet", "--", str(rel)])
    if diff.returncode == 0:
        print(f"CRON_SNAPSHOT_NO_CHANGE {rel}")
        return 0
    if diff.returncode not in (0, 1):
        print(diff.stderr.strip() or diff.stdout.strip(), file=sys.stderr)
        return diff.returncode

    commit = run(["git", "commit", "-m", f"chore: snapshot cron jobs {stamp}", "--", str(rel)])
    if commit.returncode != 0:
        print(commit.stderr.strip() or commit.stdout.strip(), file=sys.stderr)
        return commit.returncode

    print(f"CRON_SNAPSHOT_COMMITTED {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
