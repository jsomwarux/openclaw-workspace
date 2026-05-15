#!/usr/bin/env python3
"""Write pending state for content posted-reply handling.

Used after a content reminder sends JT one or more posts. The file lets
scripts/content_posted_reply_handler.py map a later `posted` reply to exact
posted-log rows instead of guessing from recent scheduled rows.
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "memory" / "content"
POSTED_LOG = CONTENT_DIR / "posted-log.jsonl"
PENDING = CONTENT_DIR / "pending-posted-reply.json"

PLATFORM_ALIASES = {
    "x": "x",
    "twitter": "x",
    "tweet": "x",
    "linkedin": "linkedin",
    "linked in": "linkedin",
    "li": "linkedin",
}


def canonical_platform(value: str | None) -> str:
    val = (value or "").strip().lower()
    return PLATFORM_ALIASES.get(val, val)


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        raise SystemExit(f"POSTED_LOG_MISSING: {path}")
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"POSTED_LOG_CORRUPT line {line_no}: {exc}") from exc
        row["line_no"] = line_no
        rows.append(row)
    return rows


def load_entries_arg(raw: str | None) -> list[dict[str, Any]]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"BAD_ENTRIES_JSON: {exc}") from exc
    if not isinstance(data, list) or not all(isinstance(e, dict) for e in data):
        raise SystemExit("BAD_ENTRIES_JSON: expected a JSON array of objects")
    return data


def match_rows(rows: list[dict[str, Any]], *, target_date: str, platforms: set[str], day: str | None) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("date", ""))[:10] != target_date:
            continue
        if row.get("banked") is True or row.get("superseded") is True:
            continue
        if row.get("posted") is True:
            continue
        if platforms and canonical_platform(row.get("platform")) not in platforms:
            continue
        if day and str(row.get("day", "")).strip().lower() != day:
            continue
        matches.append(row)
    return matches


def normalize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key in ("line_no", "date", "platform", "day", "topic", "slug", "summary"):
        if entry.get(key) not in (None, ""):
            clean[key] = entry[key]
    if "platform" in clean:
        clean["platform"] = canonical_platform(str(clean["platform"]))
    if "day" in clean:
        clean["day"] = str(clean["day"]).strip().lower()
    return clean


def build_pending(*, source: str, entries: list[dict[str, Any]], note: str | None) -> dict[str, Any]:
    now = int(time.time())
    return {
        "sent_at": now,
        "status": "pending",
        "source": source,
        "note": note or "",
        "entries": [normalize_entry(e) for e in entries],
    }


def write_pending(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write pending state for content posted-reply handler")
    parser.add_argument("--date", help="Scheduled content date YYYY-MM-DD; defaults to today")
    parser.add_argument("--platform", action="append", choices=["x", "twitter", "linkedin", "li"], help="Platform to include; repeatable")
    parser.add_argument("--day", help="Day name filter, e.g. sunday")
    parser.add_argument("--source", default="content-reminder", help="Source label stored in pending state")
    parser.add_argument("--entries-json", help="Exact entries JSON array. If omitted, rows are matched from posted-log by date/platform/day")
    parser.add_argument("--posted-log", default=str(POSTED_LOG), help="Path to posted-log.jsonl")
    parser.add_argument("--pending", default=str(PENDING), help="Path to pending-posted-reply.json")
    parser.add_argument("--note", help="Optional note about the reminder message")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    target = parse_date(args.date) or date.today()
    target_s = target.isoformat()
    day = args.day.strip().lower() if args.day else None
    platforms = {canonical_platform(p) for p in (args.platform or [])}

    entries = load_entries_arg(args.entries_json)
    if not entries:
        rows = load_jsonl(Path(args.posted_log).expanduser())
        entries = match_rows(rows, target_date=target_s, platforms=platforms, day=day)
    if not entries:
        raise SystemExit("NO_PENDING_ENTRIES: no unposted scheduled rows matched")

    pending = build_pending(source=args.source, entries=entries, note=args.note)
    if not args.dry_run:
        write_pending(Path(args.pending).expanduser(), pending)

    result = {
        "ok": True,
        "dry_run": args.dry_run,
        "pending_path": str(Path(args.pending).expanduser()),
        "entries_count": len(pending["entries"]),
        "entries": pending["entries"],
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Pending posted-reply state {'would be written' if args.dry_run else 'written'} ✅ — {len(pending['entries'])} entr{'y' if len(pending['entries']) == 1 else 'ies'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
