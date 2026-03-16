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

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "ntn_I6090101509856iOb9JOeecrHaqzwG24r7PCjud0PE49iU")
DB_ID = "32516aff-9305-81a7-8659-eac869c71ba8"

def push_post(platform, date, post_text, post_type="Planned", week=None, drive_link=None):
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

def push_batch(posts_json):
    """Push a batch of posts from a JSON array."""
    posts = json.loads(posts_json)
    ok = 0
    for p in posts:
        success = push_post(
            platform=p["platform"],
            date=p["date"],
            post_text=p["post"],
            post_type=p.get("type", "Planned"),
            week=p.get("week"),
            drive_link=p.get("drive_link")
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
    args = parser.parse_args()

    if args.batch:
        push_batch(args.batch)
    elif args.platform and args.date and args.post:
        push_post(args.platform, args.date, args.post, args.type, args.week, args.drive_link)
    else:
        print("Usage: --platform, --date, --post required (or --batch for JSON array)", file=sys.stderr)
        sys.exit(1)
