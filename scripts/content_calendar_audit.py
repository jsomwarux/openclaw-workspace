#!/usr/bin/env python3
"""Audit JT's content calendar/follow-through system without external writes.

Checks local weekly content, posted-log hygiene, cron guard presence, and optional
Notion calendar state for duplicate same-day/platform entries.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "memory" / "content"
POSTED_LOG = CONTENT_DIR / "posted-log.jsonl"
CRON_JOBS = Path.home() / ".openclaw" / "cron" / "jobs.json"
NOTION_DB_ID = "32516aff-9305-81a7-8659-eac869c71ba8"

CONTENT_CRONS = {
    "content-reminder": ["content_distribution_guard.py", "posted-log.jsonl", "content_pending_reply_state.py", "pending-posted-reply.json"],
    "content-sunday": ["posted-log.jsonl", "reply", "posted", "content_pending_reply_state.py", "pending-posted-reply.json"],
    "content-generate-linkedin": ["content_distribution_guard.py", "Drive", "Notion"],
    "content-generate-x": ["content_distribution_guard.py", "notion-calendar-push.py", "posted-log.jsonl"],
}

POSTED_REPLY_HANDLER = ROOT / "scripts" / "content_posted_reply_handler.py"
PENDING_REPLY_STATE_WRITER = ROOT / "scripts" / "content_pending_reply_state.py"
POSTED_REPLY_DOC = ROOT / "docs" / "agents" / "content-posted-reply-handler.md"


def monday_for(d: date) -> date:
    return d - timedelta(days=d.weekday())


def load_jsonl(path: Path) -> list[tuple[int, dict]]:
    rows: list[tuple[int, dict]] = []
    if not path.exists():
        return rows
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append((i, json.loads(line)))
        except json.JSONDecodeError as exc:
            rows.append((i, {"_parse_error": str(exc), "_raw": line[:160]}))
    return rows


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except Exception:
        return None


def check_weekly(week: date) -> list[str]:
    problems: list[str] = []
    path = CONTENT_DIR / f"weekly-{week:%Y-%m-%d}.md"
    if not path.exists():
        return [f"missing weekly file: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    required = ["Pattern inputs", "Constraint log", "Hook mappings", "## X"]
    for marker in required:
        if marker not in text:
            problems.append(f"{path.relative_to(ROOT)} missing {marker!r}")
    for bad in ["[placeholder]", "[needs current signal]", "TODO:"]:
        if bad.lower() in text.lower():
            problems.append(f"{path.relative_to(ROOT)} contains stale marker {bad}")
    if "SKIP_SLOT" in text and "Do not send" not in text:
        problems.append(f"{path.relative_to(ROOT)} contains SKIP_SLOT without explicit Do not send instruction")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/content_distribution_guard.py",
                "--weekly",
                str(path),
                "--require-reference-map",
                "linkedin",
                "--require-reference-map",
                "x",
                "--check-notion-script",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            problems.append("content_distribution_guard failed: " + (result.stdout + result.stderr).strip().replace("\n", " | "))
    except Exception as exc:
        problems.append(f"content_distribution_guard error: {exc}")
    return problems


def check_posted_log(days: int = 60) -> list[str]:
    problems: list[str] = []
    rows = load_jsonl(POSTED_LOG)
    if not rows:
        return ["posted-log.jsonl missing or empty"]
    cutoff = date.today() - timedelta(days=days)
    key_rows: dict[tuple[str, str, str], list[tuple[int, dict]]] = collections.defaultdict(list)
    for line_no, row in rows:
        if "_parse_error" in row:
            problems.append(f"posted-log line {line_no} JSON parse error: {row['_parse_error']}")
            continue
        d = parse_date(row.get("date"))
        if not d or d < cutoff:
            continue
        key = (row.get("date", ""), str(row.get("platform", "")).lower(), str(row.get("day", "")).lower())
        if row.get("banked") is not True:
            key_rows[key].append((line_no, row))
        if row.get("posted") is True and not row.get("posted_date") and not row.get("url"):
            problems.append(f"posted-log line {line_no} marked posted without posted_date/url")
    for key, vals in sorted(key_rows.items()):
        if len(vals) > 1:
            topics = ", ".join(f"line {n}: {r.get('topic') or r.get('summary')}" for n, r in vals)
            problems.append(f"posted-log duplicate scheduled slot {key}: {topics}")
    return problems


def check_crons() -> list[str]:
    problems: list[str] = []
    if not CRON_JOBS.exists():
        return [f"cron jobs file missing: {CRON_JOBS}"]
    data = json.loads(CRON_JOBS.read_text(encoding="utf-8"))
    jobs = {j.get("name"): j for j in data.get("jobs", [])}
    for name, markers in CONTENT_CRONS.items():
        job = jobs.get(name)
        if not job:
            problems.append(f"missing cron {name}")
            continue
        if not job.get("enabled"):
            problems.append(f"cron disabled: {name}")
        message = job.get("payload", {}).get("message", "")
        for marker in markers:
            if marker not in message:
                problems.append(f"cron {name} missing prompt marker {marker!r}")
        if name == "content-generate-x" and job.get("delivery", {}).get("mode") == "none":
            # Acceptable only if prompt explicitly sends its own Telegram summary.
            if "Telegram" not in message or "send" not in message.lower():
                problems.append("content-generate-x has no runner delivery and no explicit Telegram send instruction")
    if not POSTED_REPLY_HANDLER.exists():
        problems.append(f"missing posted reply handler: {POSTED_REPLY_HANDLER.relative_to(ROOT)}")
    else:
        text = POSTED_REPLY_HANDLER.read_text(encoding="utf-8")
        for marker in ["pending-posted-reply.json", "--dry-run", "NOTION_TOKEN", "posted_log"]:
            if marker not in text:
                problems.append(f"posted reply handler missing marker {marker!r}")
    if not PENDING_REPLY_STATE_WRITER.exists():
        problems.append(f"missing pending reply state writer: {PENDING_REPLY_STATE_WRITER.relative_to(ROOT)}")
    else:
        text = PENDING_REPLY_STATE_WRITER.read_text(encoding="utf-8")
        for marker in ["pending-posted-reply.json", "posted-log.jsonl", "--entries-json", "--dry-run"]:
            if marker not in text:
                problems.append(f"pending reply state writer missing marker {marker!r}")
    if not POSTED_REPLY_DOC.exists():
        problems.append(f"missing posted reply handler docs: {POSTED_REPLY_DOC.relative_to(ROOT)}")
    return problems


def query_notion(start: date, end: date) -> list[dict] | None:
    token = os.getenv("NOTION_TOKEN")
    if not token:
        return None
    payload = {
        "filter": {"and": [
            {"property": "Date", "date": {"on_or_after": f"{start:%Y-%m-%d}"}},
            {"property": "Date", "date": {"on_or_before": f"{end:%Y-%m-%d}"}},
        ]},
        "page_size": 100,
    }
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"},
    )
    data = json.loads(urllib.request.urlopen(req, timeout=20).read())
    rows = []
    for r in data.get("results", []):
        props = r.get("properties", {})
        title = "".join(t.get("plain_text", "") for t in props.get("Post", {}).get("title", []))
        rows.append({
            "id": r.get("id"),
            "date": (props.get("Date", {}).get("date") or {}).get("start"),
            "platform": ((props.get("Platform", {}).get("select") or {}).get("name") or "").lower(),
            "status": ((props.get("Status", {}).get("select") or {}).get("name") or ""),
            "drive": bool(props.get("Drive Link", {}).get("url")),
            "title": title[:120],
        })
    return rows


def check_notion(week: date) -> list[str]:
    problems: list[str] = []
    rows = query_notion(week, week + timedelta(days=6))
    if rows is None:
        return ["Notion check skipped: NOTION_TOKEN not set"]
    by_slot: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for row in rows:
        by_slot[(row.get("date") or "", row.get("platform") or "")].append(row)
        if not row.get("drive"):
            problems.append(f"Notion row missing Drive Link: {row.get('date')} {row.get('platform')} {row.get('title')}")
    for key, vals in sorted(by_slot.items()):
        if len(vals) > 1:
            titles = " | ".join(v.get("title", "") for v in vals)
            problems.append(f"Notion duplicate slot {key}: {len(vals)} rows: {titles}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", help="Monday date YYYY-MM-DD. Defaults to current week.")
    parser.add_argument("--with-notion", action="store_true", help="Query Notion calendar; requires NOTION_TOKEN.")
    args = parser.parse_args()
    week = parse_date(args.week) if args.week else monday_for(date.today())
    if not week:
        raise SystemExit("invalid --week")

    sections = {
        "weekly": check_weekly(week),
        "posted_log": check_posted_log(),
        "crons": check_crons(),
    }
    if args.with_notion:
        sections["notion"] = check_notion(week)

    any_fail = False
    for name, problems in sections.items():
        if problems:
            any_fail = True
            print(f"{name}: FAIL")
            for p in problems:
                print(f"- {p}")
        else:
            print(f"{name}: PASS")
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
