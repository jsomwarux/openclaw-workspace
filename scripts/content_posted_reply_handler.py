#!/usr/bin/env python3
"""Deterministic handler for JT's inbound content "posted" replies.

This script is local and bounded:
- Parses explicit replies like "posted", "posted both", "posted Wednesday LinkedIn", "posted x: <url>".
- Matches pending reminder state when present, otherwise falls back to recent scheduled rows in memory/content/posted-log.jsonl.
- Idempotently marks matched rows posted with posted_date, posted_at, optional URL/evidence.
- Optionally updates the matching Notion Content Calendar row to Status=Posted only when there is exactly one safe date/platform match.
- Prints the confirmation text for Eve to send back to JT.

It never posts externally. JT still presses send on social platforms.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "memory" / "content"
DEFAULT_POSTED_LOG = CONTENT_DIR / "posted-log.jsonl"
DEFAULT_PENDING = CONTENT_DIR / "pending-posted-reply.json"
NOTION_DB_ID = "32516aff-9305-81a7-8659-eac869c71ba8"
URL_RE = re.compile(r"https?://\S+", re.I)

PLATFORM_ALIASES = {
    "x": "x",
    "twitter": "x",
    "tweet": "x",
    "tweets": "x",
    "linkedin": "linkedin",
    "linked in": "linkedin",
    "li": "linkedin",
}
DAYS = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}


@dataclass(frozen=True)
class ParsedReply:
    raw: str
    platforms: set[str]
    day: str | None
    urls: list[str]
    both: bool


def parse_reply(raw: str) -> ParsedReply:
    text = (raw or "").strip()
    if not text:
        raise SystemExit("EMPTY_REPLY")
    lower = re.sub(r"\s+", " ", text.lower()).strip()
    if not re.match(r"^posted\b", lower):
        raise SystemExit("NO_POSTED_SIGNAL: reply must start with 'posted'")

    platforms: set[str] = set()
    for alias, canonical in PLATFORM_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", lower):
            platforms.add(canonical)
    day = next((d for d in DAYS if re.search(rf"\b{d}\b", lower)), None)
    urls = [u.rstrip(").,]") for u in URL_RE.findall(text)]
    both = bool(re.search(r"\b(both|all)\b", lower))
    return ParsedReply(raw=text, platforms=platforms, day=day, urls=urls, both=both)


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def canonical_platform(value: str | None) -> str:
    val = (value or "").strip().lower()
    return PLATFORM_ALIASES.get(val, val)


def display_platform(value: str) -> str:
    return "X" if canonical_platform(value) == "x" else "LinkedIn" if canonical_platform(value) == "linkedin" else value


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
        row["__line_no"] = line_no
        rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    serializable = []
    for row in rows:
        clean = dict(row)
        clean.pop("__line_no", None)
        serializable.append(json.dumps(clean, ensure_ascii=False, separators=(",", ":")))
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("\n".join(serializable) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_pending(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"PENDING_CORRUPT: {path}: {exc}") from exc


def write_pending(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def pending_entries(pending: dict[str, Any], max_age_hours: int) -> list[dict[str, Any]]:
    if not pending:
        return []
    if pending.get("status") in {"logged", "handled", "consumed"}:
        return []
    sent_at = pending.get("sent_at") or pending.get("created_at")
    if isinstance(sent_at, (int, float)):
        age_hours = (time.time() - float(sent_at)) / 3600
        if age_hours > max_age_hours:
            return []
    entries = pending.get("entries") or pending.get("posts") or []
    if not isinstance(entries, list):
        raise SystemExit("PENDING_BAD_SCHEMA: entries/posts must be a list")
    return [e for e in entries if isinstance(e, dict)]


def row_matches_entry(row: dict[str, Any], entry: dict[str, Any]) -> bool:
    if entry.get("line_no") and int(entry["line_no"]) != int(row.get("__line_no", -1)):
        return False
    for key in ("date", "day", "topic", "slug"):
        if entry.get(key) and str(entry.get(key)).lower() != str(row.get(key, "")).lower():
            return False
    if entry.get("platform") and canonical_platform(entry.get("platform")) != canonical_platform(row.get("platform")):
        return False
    return True


def filter_rows_for_reply(rows: list[dict[str, Any]], parsed: ParsedReply, pending: dict[str, Any], *, target_date: date, lookback_hours: int) -> tuple[list[dict[str, Any]], str]:
    entries = pending_entries(pending, lookback_hours)
    candidates: list[dict[str, Any]] = []
    source = "recent posted-log schedule"

    if entries:
        source = "pending reminder state"
        for row in rows:
            if any(row_matches_entry(row, entry) for entry in entries):
                candidates.append(row)
    else:
        min_date = target_date - timedelta(days=max(0, lookback_hours // 24))
        max_date = target_date
        for row in rows:
            d = parse_iso_date(row.get("date"))
            if not d or d < min_date or d > max_date:
                continue
            if row.get("banked") is True or row.get("superseded") is True:
                continue
            candidates.append(row)

    if parsed.platforms:
        candidates = [r for r in candidates if canonical_platform(r.get("platform")) in parsed.platforms]
    if parsed.day:
        candidates = [r for r in candidates if str(r.get("day", "")).lower() == parsed.day]

    # Never mutate intentionally banked/superseded rows from pending state unless the pending entry line_no points to it.
    safe: list[dict[str, Any]] = []
    for row in candidates:
        if row.get("superseded") is True:
            continue
        if row.get("banked") is True and not any(e.get("line_no") for e in entries):
            continue
        safe.append(row)
    return safe, source


def notion_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }


def notion_platform(platform: str) -> str:
    c = canonical_platform(platform)
    return "X" if c == "x" else "LinkedIn" if c == "linkedin" else platform


def query_notion_slot(token: str, row: dict[str, Any]) -> list[dict[str, Any]]:
    payload = {
        "filter": {"and": [
            {"property": "Date", "date": {"equals": row.get("date")}},
            {"property": "Platform", "select": {"equals": notion_platform(str(row.get("platform", ""))) }},
        ]},
        "page_size": 10,
    }
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query",
        data=json.dumps(payload).encode(),
        headers=notion_headers(token),
    )
    data = json.loads(urllib.request.urlopen(req, timeout=20).read())
    return data.get("results", [])


def update_notion_status(token: str, row: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    matches = query_notion_slot(token, row)
    if len(matches) != 1:
        return {"status": "skipped", "reason": f"expected 1 Notion row, found {len(matches)}", "date": row.get("date"), "platform": notion_platform(str(row.get("platform", "")))}
    page = matches[0]
    page_id = page.get("id")
    props = page.get("properties", {})
    current = ((props.get("Status", {}).get("select") or {}).get("name") or "")
    if current == "Posted":
        return {"status": "already", "page_id": page_id}
    if dry_run:
        return {"status": "dry_run", "page_id": page_id, "from": current, "to": "Posted"}
    payload = {"properties": {"Status": {"select": {"name": "Posted"}}}}
    req = urllib.request.Request(
        f"https://api.notion.com/v1/pages/{page_id}",
        data=json.dumps(payload).encode(),
        headers=notion_headers(token),
        method="PATCH",
    )
    json.loads(urllib.request.urlopen(req, timeout=20).read())
    return {"status": "updated", "page_id": page_id, "from": current, "to": "Posted"}


def summarize_row(row: dict[str, Any]) -> str:
    label = row.get("topic") or row.get("summary") or row.get("title") or row.get("text", "")[:50] or f"line {row.get('__line_no')}"
    return f"{row.get('date')} {display_platform(str(row.get('platform', '')))} {row.get('day', '')}: {label}".strip()


def handle_reply(raw: str, *, posted_log: Path = DEFAULT_POSTED_LOG, pending_path: Path = DEFAULT_PENDING,
                 posted_date: str | None = None, dry_run: bool = False, lookback_hours: int = 48,
                 update_notion: bool = True) -> dict[str, Any]:
    parsed = parse_reply(raw)
    target = parse_iso_date(posted_date) or date.today()
    if not target:
        raise SystemExit(f"BAD_DATE: {posted_date}")

    rows = load_jsonl(posted_log)
    pending = load_pending(pending_path)
    targets, source = filter_rows_for_reply(rows, parsed, pending, target_date=target, lookback_hours=lookback_hours)
    if not targets:
        raise SystemExit("NO_MATCHING_CONTENT_SLOT: no unbanked, unsuperseded scheduled row matched this posted reply")

    if parsed.urls and len(targets) > 1 and len(parsed.urls) != len(targets):
        raise SystemExit("AMBIGUOUS_URL: include a platform/day when logging one URL, or provide one URL per matched post")

    now = int(time.time())
    changed: list[dict[str, Any]] = []
    already: list[dict[str, Any]] = []
    for idx, row in enumerate(targets):
        if row.get("posted") is True:
            # Still fill missing URL if this exact reply provides one safely.
            url = parsed.urls[idx] if len(parsed.urls) == len(targets) else parsed.urls[0] if len(parsed.urls) == 1 and len(targets) == 1 else None
            if url and not row.get("url"):
                row["url"] = url
                row["posted_reply_updated_at"] = now
                changed.append(row)
            else:
                already.append(row)
            continue
        row["posted"] = True
        row["posted_date"] = target.isoformat()
        row["posted_at"] = now
        row["posted_source"] = "content_posted_reply_handler.py"
        if parsed.urls:
            if len(parsed.urls) == len(targets):
                row["url"] = parsed.urls[idx]
            elif len(targets) == 1:
                row["url"] = parsed.urls[0]
        changed.append(row)

    notion_results: list[dict[str, Any]] = []
    token = os.getenv("NOTION_TOKEN")
    if update_notion and token:
        for row in targets:
            try:
                notion_results.append(update_notion_status(token, row, dry_run=dry_run))
            except Exception as exc:  # keep local logging from failing because Notion is unavailable
                notion_results.append({"status": "error", "date": row.get("date"), "platform": row.get("platform"), "error": str(exc)})

    if not dry_run:
        if changed:
            write_jsonl(posted_log, rows)
        if pending:
            pending = dict(pending)
            pending.update({
                "status": "logged",
                "logged_at": now,
                "handler": "scripts/content_posted_reply_handler.py",
                "reply": parsed.raw,
                "matched": [summarize_row(r) for r in targets],
            })
            write_pending(pending_path, pending)

    confirmation = "Logged ✅ — " + "; ".join(summarize_row(r) for r in changed or already)
    if already and not changed:
        confirmation = "Already logged ✅ — " + "; ".join(summarize_row(r) for r in already)
    if dry_run:
        confirmation = "DRY_RUN: would mark posted — " + "; ".join(summarize_row(r) for r in targets)

    return {
        "ok": True,
        "dry_run": dry_run,
        "source": source,
        "matched": [summarize_row(r) for r in targets],
        "changed": [summarize_row(r) for r in changed],
        "already": [summarize_row(r) for r in already],
        "notion": notion_results,
        "pending_path": str(pending_path),
        "posted_log": str(posted_log),
        "confirmation": confirmation,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Handle an inbound content posted reply deterministically")
    parser.add_argument("--reply", required=True, help="Raw inbound reply text from JT, e.g. 'posted Wednesday LinkedIn'")
    parser.add_argument("--date", help="Posted date YYYY-MM-DD; defaults to today")
    parser.add_argument("--posted-log", default=str(DEFAULT_POSTED_LOG), help="Path to posted-log.jsonl")
    parser.add_argument("--pending", default=str(DEFAULT_PENDING), help="Path to pending content reminder state")
    parser.add_argument("--lookback-hours", type=int, default=48, help="Fallback match window when no pending state exists")
    parser.add_argument("--dry-run", action="store_true", help="Validate and show target rows without writing")
    parser.add_argument("--skip-notion", action="store_true", help="Do not update Notion Content Calendar status")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    result = handle_reply(
        args.reply,
        posted_log=Path(args.posted_log).expanduser(),
        pending_path=Path(args.pending).expanduser(),
        posted_date=args.date,
        dry_run=args.dry_run,
        lookback_hours=args.lookback_hours,
        update_notion=not args.skip_notion,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["confirmation"])
        if result.get("notion"):
            print("Notion:", json.dumps(result["notion"], ensure_ascii=False))


if __name__ == "__main__":
    main()
