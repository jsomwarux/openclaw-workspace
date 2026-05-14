#!/usr/bin/env python3
"""Validate Passive Income Scout -> Strategist handoff.

This catches the failure mode where cron reports ok but the expected strategist
artifact was never created for the scout report being evaluated.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
PI_DIR = ROOT / "memory" / "passive-income"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="YYYY-MM-DD; defaults to today")
    p.add_argument("--mode", choices=["pre-scout", "pre-strategist", "post-strategist"], default="post-strategist")
    p.add_argument("--json", action="store_true")
    return p.parse_args()


def file_state(path: Path) -> dict:
    exists = path.exists()
    size = path.stat().st_size if exists else 0
    mtime = path.stat().st_mtime if exists else None
    text_head = path.read_text(errors="ignore")[:2000] if exists and size else ""
    return {
        "path": str(path),
        "exists": exists,
        "size": size,
        "mtime": datetime.fromtimestamp(mtime, timezone.utc).isoformat() if mtime else None,
        "incomplete": "INCOMPLETE" in text_head,
    }


def main() -> int:
    args = parse_args()
    scout = PI_DIR / f"{args.date}-scout.md"
    strategist = PI_DIR / f"{args.date}-strategist.md"
    scout_state = file_state(scout)
    strategist_state = file_state(strategist)
    required_signal_files = [
        PI_DIR / "weekly-trends.md",
        PI_DIR / "weekly-apis.md",
        PI_DIR / "weekly-exploding-topics.md",
        PI_DIR / "weekly-google-trends.md",
    ]
    signal_states = {p.name: file_state(p) for p in required_signal_files}

    problems: list[str] = []
    if args.mode == "pre-scout":
        now = datetime.now(timezone.utc).timestamp()
        for p in required_signal_files:
            state = signal_states[p.name]
            if not state["exists"]:
                problems.append(f"missing signal file: {p}")
                continue
            if state["size"] < 100:
                problems.append(f"signal file too small: {p} ({state['size']} bytes)")
            age_days = (now - p.stat().st_mtime) / 86400
            if age_days > 8:
                problems.append(f"signal file stale >8 days: {p} ({age_days:.1f}d)")

    if args.mode in {"pre-strategist", "post-strategist"}:
        if not scout_state["exists"]:
            problems.append(f"missing scout report: {scout}")
        elif scout_state["size"] < 500:
            problems.append(f"scout report too small: {scout_state['size']} bytes")
        if scout_state["incomplete"]:
            problems.append("scout report marked INCOMPLETE")

    if args.mode == "post-strategist":
        if not strategist_state["exists"]:
            problems.append(f"missing strategist report: {strategist}")
        elif strategist_state["size"] < 500:
            problems.append(f"strategist report too small: {strategist_state['size']} bytes")
        if strategist_state["exists"] and scout_state["exists"]:
            if strategist.stat().st_mtime < scout.stat().st_mtime:
                problems.append("strategist report is older than scout report")

    result = {
        "ok": not problems,
        "date": args.date,
        "mode": args.mode,
        "signals": signal_states,
        "scout": scout_state,
        "strategist": strategist_state,
        "problems": problems,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["ok"]:
            print(f"PASSIVE_INCOME_HANDOFF_OK date={args.date} mode={args.mode}")
        else:
            print(f"PASSIVE_INCOME_HANDOFF_FAIL date={args.date} mode={args.mode}")
            for prob in problems:
                print(f"- {prob}")
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
