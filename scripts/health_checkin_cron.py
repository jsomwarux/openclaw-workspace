#!/usr/bin/env python3
"""Deterministic helper for the 9PM Health Check-in cron."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo


WORKSPACE = Path("/Users/jtsomwaru/.openclaw/workspace")
PENDING_PATH = WORKSPACE / "health" / "pending-checkin.json"
NY_TZ = ZoneInfo("America/New_York")

CHECKIN_MESSAGE = """🌙 *Evening Check-in*

Five questions — answer on one line or multiple:

1️⃣ *Activation* — how activated/tense does your nervous system feel right now? (1=fully calm, 10=maximum bracing)
2️⃣ *Bracing scan* — where are you unconsciously holding tension? (jaw / shoulders / glutes / belly / chest / none — all that apply)
3️⃣ *Exhale test* — take a breath now and exhale fully. How complete was it? (full / partial / blocked) + anything notable
4️⃣ *Protocol + movement* — did you do the reset protocol today? (yes / partial / no) + any exercise?
5️⃣ *Sleep* — how was last night? (1–10) + wake up tense or jaw clenching?

_Food note if anything notable (optional)_

_Example: "6, jaw + shoulders, partial, no protocol / 30min walk, 7 woke tense"_

📋 *5-min Reset (if not done today):*
1. Physiological sigh × 2 (double inhale → long exhale)
2. Extended exhale × 10 (4 in / 8 out)
3. Jaw release: teeth apart, tongue down, soften masseter × 30s
4. Ribcage expansion: breathe into lower ribs outward × 8 cycles
5. Pelvic neutral + shoulder drop lying down × 2 min
_Protocol: ~/.openclaw/workspace/health/protocol.md_"""


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"PENDING_CORRUPT: {path}: {exc}") from exc


def _today(now: Optional[datetime] = None) -> str:
    current = now or datetime.now(NY_TZ)
    if current.tzinfo is None:
        current = current.replace(tzinfo=NY_TZ)
    return current.astimezone(NY_TZ).date().isoformat()


def prepare(pending_path: Path = PENDING_PATH, *, now: Optional[datetime] = None) -> Dict[str, Any]:
    target_date = _today(now)
    pending = _load_json(pending_path)
    if pending.get("date") == target_date and pending.get("status") != "failed":
        return {
            "ok": True,
            "action": "skip",
            "date": target_date,
            "status": "SKIPPED_DUPLICATE_HEALTH_CHECKIN",
        }
    return {
        "ok": True,
        "action": "send",
        "date": target_date,
        "message": CHECKIN_MESSAGE,
    }


def mark_sent(pending_path: Path = PENDING_PATH, checkin_date: Optional[str] = None,
              *, sent_at: Optional[int] = None) -> Dict[str, Any]:
    target_date = checkin_date or _today()
    data = {
        "date": target_date,
        "handler": "health_checkin_cron.py",
        "sent_at": int(sent_at if sent_at is not None else time.time()),
        "status": "sent",
    }
    pending_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = pending_path.with_suffix(pending_path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    tmp.replace(pending_path)
    return {"ok": True, "date": target_date, "status": "HEALTH_CHECKIN_SENT"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or mark the evening health check-in.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true", help="Return send/skip decision and prompt text")
    mode.add_argument("--mark-sent", action="store_true", help="Write pending-checkin sent state")
    parser.add_argument("--date", help="YYYY-MM-DD date for --mark-sent; defaults to today in America/New_York")
    parser.add_argument("--pending-path", default=str(PENDING_PATH), help="Path to pending-checkin.json")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    pending_path = Path(args.pending_path)
    if args.prepare:
        result = prepare(pending_path)
    else:
        result = mark_sent(pending_path, args.date)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    elif result.get("action") == "send":
        print(result["message"])
    else:
        print(result["status"])


if __name__ == "__main__":
    main()
