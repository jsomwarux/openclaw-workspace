#!/usr/bin/env python3
"""
Deterministic handler for JT's inbound health check-in replies.

This script is intentionally local and side-effect-bounded:
- Reads health/pending-checkin.json to determine the expected check-in date.
- Parses/logs one reply into health.sqlite through the existing parser/db layer.
- Idempotently refuses to overwrite an existing same-date check-in unless --force.
- Marks the pending file as logged after success.
- Prints the confirmation text for Eve to send back to JT.

It does not send Telegram by itself; the main agent/message layer owns external sends.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional

HEALTH_DIR = Path(__file__).resolve().parent
WORKSPACE = HEALTH_DIR.parent
PENDING_PATH = HEALTH_DIR / "pending-checkin.json"

sys.path.insert(0, str(HEALTH_DIR))
from db import init_db, get_checkin, save_checkin  # noqa: E402
from parser import parse_checkin, format_checkin_for_confirm  # noqa: E402


def _load_pending(path: Path = PENDING_PATH) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"PENDING_CORRUPT: {path}: {exc}") from exc


def _write_pending(data: Dict[str, Any], path: Path = PENDING_PATH) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def _target_date(pending: Dict[str, Any], explicit_date: Optional[str]) -> str:
    target = explicit_date or pending.get("date") or date.today().isoformat()
    try:
        datetime.strptime(target, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit(f"BAD_DATE: {target} must be YYYY-MM-DD") from exc
    return target


def _pending_allows_log(pending: Dict[str, Any], target_date: str, allow_no_pending: bool) -> None:
    if allow_no_pending:
        return
    if not pending:
        raise SystemExit("NO_PENDING_CHECKIN: health/pending-checkin.json is missing or empty")
    pending_date = pending.get("date")
    if pending_date != target_date:
        raise SystemExit(f"PENDING_DATE_MISMATCH: pending={pending_date!r} target={target_date!r}")
    if pending.get("status") == "logged":
        raise SystemExit(f"ALREADY_HANDLED: pending check-in for {target_date} is already marked logged")


def handle_reply(raw: str, *, checkin_date: Optional[str] = None, force: bool = False,
                 dry_run: bool = False, allow_no_pending: bool = False) -> Dict[str, Any]:
    raw = (raw or "").strip()
    if not raw:
        raise SystemExit("EMPTY_REPLY")

    pending = _load_pending()
    target = _target_date(pending, checkin_date)
    _pending_allows_log(pending, target, allow_no_pending)

    init_db()
    existing = get_checkin(target)
    if existing and not force:
        raise SystemExit(f"DUPLICATE_CHECKIN: {target} already logged; use --force to overwrite")

    parsed = parse_checkin(raw)
    confirm = format_checkin_for_confirm(parsed, raw)

    row_id = None
    if not dry_run:
        row_id = save_checkin(
            checkin_date=target,
            energy=parsed["energy"],
            pain_areas=parsed["pain_areas"],
            food=parsed["food"],
            exercise=parsed["exercise"],
            sleep_quality=parsed["sleep_quality"],
            notes=parsed.get("notes"),
            raw_response=raw,
        )
        updated_pending = dict(pending)
        updated_pending.update({
            "date": target,
            "status": "logged",
            "logged_at": int(time.time()),
            "handler": "health/inbound_handler.py",
        })
        _write_pending(updated_pending)

    return {
        "ok": True,
        "date": target,
        "dry_run": dry_run,
        "row_id": row_id,
        "parsed": parsed,
        "confirmation": confirm,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Handle an inbound health check-in reply deterministically")
    ap.add_argument("--reply", required=True, help="Raw inbound reply text from JT")
    ap.add_argument("--date", help="Override check-in date (YYYY-MM-DD); defaults to pending-checkin date")
    ap.add_argument("--force", action="store_true", help="Overwrite existing check-in for the date")
    ap.add_argument("--dry-run", action="store_true", help="Parse and validate without writing DB/pending state")
    ap.add_argument("--allow-no-pending", action="store_true", help="Allow logging without pending-checkin.json match")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args()

    result = handle_reply(
        args.reply,
        checkin_date=args.date,
        force=args.force,
        dry_run=args.dry_run,
        allow_no_pending=args.allow_no_pending,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["confirmation"])
        if args.dry_run:
            print(f"\nDRY_RUN: would log health check-in for {result['date']}")
        else:
            print(f"\nHEALTH_CHECKIN_LOGGED: {result['date']}")


if __name__ == "__main__":
    main()
