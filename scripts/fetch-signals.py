#!/usr/bin/env python3
"""
Master signal fetch — runs all three data sources for the passive income pipeline.
Run: python3 fetch-signals.py

Outputs (all to memory/passive-income/):
  weekly-trends.md            — Brave Search signal data
  weekly-exploding-topics.md   — ExplodingTopics public scrapes
  weekly-google-trends.md      — pytrends keyword momentum
  weekly-apis.md               — API discovery (4 sources)
  weekly-trustmrr.json/md       — TrustMRR revenue-pattern comps

Runtime: ~15 minutes (pytrends = slow, rate-limited)
Recommended schedule: Saturday 5:30 AM ET (before Scout runs Sun 6 AM)
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = WORKSPACE / "scripts"

SOURCES = [
    ("Brave Search Trends", SCRIPTS_DIR / "fetch-trends.py", True),
    ("ExplodingTopics", SCRIPTS_DIR / "fetch-exploding-topics.py"),
    ("Google Trends (pytrends)", SCRIPTS_DIR / "fetch-google-trends.py", False),
    ("API Discovery", SCRIPTS_DIR / "fetch-new-apis.py"),
    ("TrustMRR Revenue Patterns", SCRIPTS_DIR / "fetch_trustmrr.py", False),
]


def run(path: Path, label: str) -> bool:
    print("=" * 50)
    print("RUNNING: " + label)
    print("=" * 50)
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        timeout=900,  # 15 min max per script
    )
    if result.returncode == 0:
        print("✅ " + label + " — done")
        return True
    else:
        print("⚠ " + label + " — FAILED (exit " + str(result.returncode) + ")")
        print("STDERR: " + result.stderr[-500:])
        return False


def main():
    print("=== Passive Income: Signal Fetch ===\n")
    print("Started: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()

    results = {}
    required = {}
    for item in SOURCES:
        label, script_path = item[0], item[1]
        is_required = item[2] if len(item) > 2 else True
        required[label] = is_required
        if not script_path.exists():
            print("⚠ SKIP — " + str(script_path) + " not found")
            results[label] = False
            continue
        results[label] = run(script_path, label)
        print()

    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    for label, ok in results.items():
        print("  " + ("✅" if ok else "❌") + " " + label)

    failed = [k for k, v in results.items() if not v]
    hard_failed = [k for k in failed if required.get(k, True)]
    if failed:
        print("\n⚠ Failed: " + ", ".join(failed))
    else:
        print("\n✅ All sources fetched successfully")

    gate = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "passive_income_handoff_check.py"), "--mode", "pre-scout"],
        cwd=WORKSPACE,
        text=True,
        capture_output=True,
        timeout=60,
    )
    print("\n" + "=" * 50)
    print("PRE-SCOUT GATE")
    print("=" * 50)
    print(gate.stdout.strip())
    if gate.stderr.strip():
        print("STDERR: " + gate.stderr.strip())

    if hard_failed or gate.returncode != 0:
        if hard_failed:
            print("\n❌ Required sources failed: " + ", ".join(hard_failed))
        if gate.returncode != 0:
            print("❌ Pre-scout gate failed")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
