#!/usr/bin/env python3
"""
Push content posts to the Notion Content Calendar database.
Usage: python3 notion-calendar-push.py --platform "X — Personal" --date 2026-03-23 --post "post text" --type Planned --week 2026-03-23 [--drive-link URL]
"""

import argparse
import json
import subprocess
import sys
import os
import urllib.request

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DB_ID = "32516aff-9305-81a7-8659-eac869c71ba8"

def normalize_platform(platform):
    return "X" if platform == "X — Personal" else platform


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }


def existing_calendar_entries(platform, date):
    """Return existing Notion rows for the same platform/date slot."""
    if not NOTION_TOKEN:
        return []
    payload = {
        "filter": {"and": [
            {"property": "Date", "date": {"equals": date}},
            {"property": "Platform", "select": {"equals": platform}},
        ]},
        "page_size": 20,
    }
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{DB_ID}/query",
        data=json.dumps(payload).encode(),
        headers=notion_headers(),
    )
    data = json.loads(urllib.request.urlopen(req, timeout=20).read())
    return data.get("results", [])


def push_post(platform, date, post_text, post_type="Planned", week=None, drive_link=None, dry_run=False, replace=False):
    from datetime import datetime, timedelta
    # Normalize platform name
    platform = normalize_platform(platform)
    # Auto-compute week label if not provided
    if not week and date:
        try:
            d = datetime.strptime(date, "%Y-%m-%d")
            monday = d - timedelta(days=d.weekday())
            week = f"Week of {monday.strftime('%b %-d')}"
        except Exception:
            pass
    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "Post": {"title": [{"type": "text", "text": {"content": post_text[:500]}}]},
            "Date": {"date": {"start": date}},
            "Platform": {"select": {"name": platform}},
            "Type": {"select": {"name": post_type}},
            "Status": {"select": {"name": "To Post"}},
        }
    }
    if week:
        payload["properties"]["Week"] = {"rich_text": [{"type": "text", "text": {"content": week}}]}
    if drive_link:
        payload["properties"]["Drive Link"] = {"url": drive_link}

    if dry_run:
        print(f"DRY_RUN {date} | {platform} | {post_text[:40]}...")
        return True

    if not NOTION_TOKEN:
        print("❌ Failed: NOTION_TOKEN is not set", file=sys.stderr)
        return False

    existing = existing_calendar_entries(platform, date)
    if existing and not replace:
        print(f"SKIP existing Notion slot: {date} | {platform} ({len(existing)} row(s)). Use --replace to archive/recreate.", file=sys.stderr)
        return True

    result = subprocess.run([
        "curl", "-s", "-X", "POST", "https://api.notion.com/v1/pages",
        "-H", f"Authorization: Bearer {NOTION_TOKEN}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ], capture_output=True, text=True)

    data = json.loads(result.stdout)
    if "id" in data:
        print(f"✅ {date} | {platform} | {post_text[:40]}...")
        return True
    else:
        print(f"❌ Failed: {data.get('message', 'unknown error')}", file=sys.stderr)
        return False

def push_batch(posts_json, dry_run=False, replace=False):
    """Push a batch of posts from a JSON array."""
    posts = json.loads(posts_json)
    seen = set()
    ok = 0
    for p in posts:
        dedupe_key = (p.get("platform"), p.get("date"), p.get("post", "")[:120])
        if dedupe_key in seen:
            print(f"SKIP duplicate in batch: {p.get('date')} | {p.get('platform')} | {p.get('post','')[:40]}...", file=sys.stderr)
            continue
        seen.add(dedupe_key)
        success = push_post(
            platform=p["platform"],
            date=p["date"],
            post_text=p["post"],
            post_type=p.get("type", "Planned"),
            week=p.get("week"),
            drive_link=p.get("drive_link"),
            dry_run=dry_run,
            replace=replace
        )
        if success:
            ok += 1
    print(f"\nPushed {ok}/{len(posts)} posts to Notion Content Calendar.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", help="Platform name (e.g. 'X — Personal')")
    parser.add_argument("--date", help="Post date YYYY-MM-DD")
    parser.add_argument("--post", help="Post text")
    parser.add_argument("--type", default="Planned", help="Type: Planned, News Hook, Vibe")
    parser.add_argument("--week", help="Week anchor date YYYY-MM-DD")
    parser.add_argument("--drive-link", help="Drive URL for the post")
    parser.add_argument("--batch", help="JSON array of post objects")
    parser.add_argument("--dry-run", action="store_true", help="Validate payloads without writing to Notion")
    parser.add_argument("--replace", action="store_true", help="Allow creating a new row even when the date/platform slot already exists")
    args = parser.parse_args()

    if args.batch:
        push_batch(args.batch, dry_run=args.dry_run, replace=args.replace)
    elif args.platform and args.date and args.post:
        push_post(args.platform, args.date, args.post, args.type, args.week, args.drive_link, dry_run=args.dry_run, replace=args.replace)
    else:
        print("Usage: --platform, --date, --post required (or --batch for JSON array)", file=sys.stderr)
        sys.exit(1)
