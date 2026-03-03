#!/usr/bin/env python3
"""
notion-swipe-push.py — Push a viral post to the Notion Swipe File database.

Usage:
  python3 notion-swipe-push.py \
    --text "Full post text here" \
    --author "@handle" \
    --url "https://x.com/..." \
    --niche "AI Agents" \
    --format "Hot Take" \
    --why "Why this worked — 1-2 sentences" \
    --engagement 1200 \
    --hook "Contrarian claim" \
    [--tier "⚡ High (1K–10K)"]  # auto-calculated if omitted
"""

import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

NOTION_TOKEN = "ntn_I6090101509856iOb9JOeecrHaqzwG24r7PCjud0PE49iU"
DATABASE_ID = "31316aff930580f6a195ca179793eb0e"
NOTION_VERSION = "2022-06-28"
API_URL = "https://api.notion.com/v1/pages"

VALID_NICHES = ["AI Consulting", "Crypto", "AI Agents", "Job Market", "Personal Brand", "x402"]
VALID_FORMATS = ["Hot Take", "Thread Opener", "Story", "List", "Question", "Contrarian", "Behind-the-scenes", "Data Drop", "Analogy"]
VALID_HOOKS = ["Curiosity gap", "Contrarian claim", "Personal story", "Provocative question", "Bold prediction", "Data surprise"]


def auto_tier(engagement: int) -> str:
    if engagement >= 10000:
        return "🔥 Mega (10K+)"
    elif engagement >= 1000:
        return "⚡ High (1K–10K)"
    else:
        return "✅ Solid (100–1K)"


def push_to_notion(args) -> dict:
    tier = args.tier if args.tier else auto_tier(args.engagement)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    niches = [n.strip() for n in args.niche.split(",")]
    for n in niches:
        if n not in VALID_NICHES:
            print(f"⚠️  Warning: '{n}' not a recognized niche. Valid: {VALID_NICHES}")

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Post Text": {
                "title": [{"text": {"content": args.text[:2000]}}]
            },
            "Author Handle": {
                "rich_text": [{"text": {"content": args.author}}]
            },
            "URL": {
                "url": args.url
            },
            "Niche": {
                "multi_select": [{"name": n} for n in niches]
            },
            "Format": {
                "select": {"name": args.format}
            },
            "Why It Works": {
                "rich_text": [{"text": {"content": args.why}}]
            },
            "Engagement": {
                "number": args.engagement
            },
            "Engagement Tier": {
                "select": {"name": tier}
            },
            "Hook Type": {
                "select": {"name": args.hook}
            },
            "Date Captured": {
                "date": {"start": today}
            },
            "Used As Reference": {
                "checkbox": False
            }
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            page_id = result.get("id", "unknown")
            print(f"✅ Pushed to Notion: {args.author} | {args.format} | {tier} | page_id={page_id}")
            return {"success": True, "page_id": page_id}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ Notion API error {e.code}: {body}")
        return {"success": False, "error": body}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Push a viral post to Notion Swipe File")
    parser.add_argument("--text", required=True, help="Full post text")
    parser.add_argument("--author", required=True, help="@handle of author")
    parser.add_argument("--url", required=True, help="X post URL")
    parser.add_argument("--niche", required=True, help="Niche(s), comma-separated")
    parser.add_argument("--format", required=True, help="Post format")
    parser.add_argument("--why", required=True, help="Why this post worked (1-2 sentences)")
    parser.add_argument("--engagement", required=True, type=int, help="Total engagement count")
    parser.add_argument("--hook", required=True, help="Hook type")
    parser.add_argument("--tier", help="Engagement tier (auto-calculated if omitted)")
    args = parser.parse_args()
    push_to_notion(args)


if __name__ == "__main__":
    main()
