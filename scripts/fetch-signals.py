#!/usr/bin/env python3
"""
Master signal fetch — runs all three data sources for the passive income pipeline.
Run: python3 fetch-signals.py

Outputs (all to memory/passive-income/):
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
    ("ExplodingTopics", SCRIPTS_DIR / "fetch-exploding-topics.py"),
    ("Google Trends (pytrends)", SCRIPTS_DIR / "fetch-google-trends.py"),
    ("API Discovery", SCRIPTS_DIR / "fetch-new-apis.py"),
    ("TrustMRR Revenue Patterns", SCRIPTS_DIR / "fetch_trustmrr.py"),
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
    for label, script_path in SOURCES:
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
    if failed:
        print("\n⚠ Failed: " + ", ".join(failed))
    else:
        print("\n✅ All sources fetched successfully")


if __name__ == "__main__":
    main()
