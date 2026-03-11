#!/usr/bin/env python3
"""
notion-swipe-fetch.py — Fetch recent viral posts from JT's Notion swipe file.
Outputs JSON array of posts for content generation agents.

Usage:
  python3 notion-swipe-fetch.py [--limit 5] [--min-engagement 500]
"""

import argparse
import json
import sys
import warnings
warnings.filterwarnings("ignore")
import requests

NOTION_TOKEN = "ntn_I6090101509856iOb9JOeecrHaqzwG24r7PCjud0PE49iU"
DB_ID = "31316aff930580f6a195ca179793eb0e"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def get_rich_text(prop):
    return "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))


def get_title(prop):
    return "".join(t.get("plain_text", "") for t in prop.get("title", []))


def get_select(prop):
    sel = prop.get("select")
    return sel.get("name", "") if sel else ""


def get_multi_select(prop):
    return [s.get("name", "") for s in prop.get("multi_select", [])]


def get_number(prop):
    return prop.get("number") or 0


def get_url(prop):
    return prop.get("url") or ""


def fetch_swipe_posts(limit=8, min_engagement=0):
    payload = {
        "page_size": limit * 2,  # fetch extra since we'll filter
        "sorts": [{"property": "Engagement", "direction": "descending"}]
    }

    r = requests.post(
        f"https://api.notion.com/v1/databases/{DB_ID}/query",
        headers=HEADERS,
        json=payload,
        timeout=15
    )

    if r.status_code != 200:
        print(json.dumps({"error": f"Notion API error {r.status_code}: {r.text[:200]}"}))
        sys.exit(1)

    posts = []
    for page in r.json().get("results", []):
        props = page.get("properties", {})
        engagement = get_number(props.get("Engagement", {}))
        if engagement < min_engagement:
            continue

        posts.append({
            "text": get_title(props.get("Post Text", {}))[:600],
            "author": get_rich_text(props.get("Author Handle", {})),
            "url": get_url(props.get("URL", {})),
            "niche": get_multi_select(props.get("Niche", {})),
            "format": get_select(props.get("Format", {})),
            "hook_type": get_select(props.get("Hook Type", {})),
            "why_it_works": get_rich_text(props.get("Why It Works", {})),
            "engagement": engagement,
            "engagement_tier": get_select(props.get("Engagement Tier", {}))
        })

        if len(posts) >= limit:
            break

    return posts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--min-engagement", type=int, default=0)
    args = parser.parse_args()

    posts = fetch_swipe_posts(limit=args.limit, min_engagement=args.min_engagement)
    print(json.dumps(posts, indent=2))


if __name__ == "__main__":
    main()
