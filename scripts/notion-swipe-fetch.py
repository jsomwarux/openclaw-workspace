#!/usr/bin/env python3
"""
notion-swipe-fetch.py — Fetch viral posts from JT's Notion swipe file.
Outputs a format-stratified JSON array for content generation agents.

Stratification ensures format diversity:
- At least 1 post per format present in DB (up to limit)
- Remaining slots filled by highest engagement not yet included
- Result: generation agents see diverse hook structures, not just top Hot Takes

Usage:
  python3 notion-swipe-fetch.py [--limit 8] [--min-engagement 500] [--raw]
  python3 notion-swipe-fetch.py --platform X --niche "Dynasty Fantasy" --niche "Sports Betting" --limit 12
  python3 notion-swipe-fetch.py --platform LinkedIn --niche "AI Consulting" --format "Case Study" --limit 8

  --raw: skip stratification, return top N by engagement (legacy behavior)
"""

import argparse
import json
import os
import sys
import warnings
warnings.filterwarnings("ignore")
import requests
from pathlib import Path


def env_from_global_env(*names):
    for name in names:
        if os.environ.get(name):
            return os.environ[name]
    env_path = Path.home() / ".config/env/global.env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if not line or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().removeprefix("export ")
            if key in names:
                value = value.strip().strip('"').strip("'")
                if value:
                    return value
    return None


NOTION_TOKEN = env_from_global_env("NOTION_TOKEN", "NOTION_API_KEY")
DB_ID = os.environ.get("NOTION_VIRAL_SWIPE_DB_ID", "31316aff930580f6a195ca179793eb0e")
if not NOTION_TOKEN:
    print("❌ Missing NOTION_TOKEN or NOTION_API_KEY environment variable", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Priority format order for stratification
# Ensures case studies, threads, stories make it in even if lower engagement
FORMAT_PRIORITY = [
    "Case study / proof of work",
    "Thread Opener",
    "Behind-the-scenes",
    "Story",
    "Build-in-public",
    "Data Drop",
    "Contrarian",
    "Hot Take",
    "List",
    "Question",
    "Analogy",
]


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


def infer_platform(url: str, explicit_platform: str = "") -> str:
    if explicit_platform:
        return explicit_platform
    url = (url or "").lower()
    if "linkedin.com" in url:
        return "LinkedIn"
    if "reddit.com" in url:
        return "Reddit"
    if "x.com" in url or "twitter.com" in url:
        return "X"
    return "Unknown"


def fetch_all_posts(min_engagement=0, fetch_limit=100, niches=None, platforms=None, formats=None):
    """Fetch up to fetch_limit posts from Notion, sorted by engagement desc.

    Optional filters:
    - niches: posts whose Niche multi_select includes any requested niche
    - platforms: inferred from URL unless a Platform property exists later
    - formats: posts whose Format select matches any requested format
    """
    payload = {
        "page_size": fetch_limit,
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

        post_niches = get_multi_select(props.get("Niche", {}))
        post_format = get_select(props.get("Format", {}))
        post_url = get_url(props.get("URL", {}))
        post_platform = infer_platform(post_url, get_select(props.get("Platform", {})))

        if niches and not any(n in post_niches for n in niches):
            continue
        if platforms and post_platform not in platforms:
            continue
        if formats and post_format not in formats:
            continue

        posts.append({
            "text": get_title(props.get("Post Text", {}))[:600],
            "author": get_rich_text(props.get("Author Handle", {})),
            "url": post_url,
            "platform": post_platform,
            "niche": post_niches,
            "format": post_format,
            "hook_type": get_select(props.get("Hook Type", {})),
            "why_it_works": get_rich_text(props.get("Why It Works", {})),
            "engagement": engagement,
            "engagement_tier": get_select(props.get("Engagement Tier", {}))
        })

    return posts


def stratify_posts(all_posts: list, limit: int) -> list:
    """
    Return up to `limit` posts with format diversity.

    Strategy:
    1. For each format in FORMAT_PRIORITY, include the highest-engagement post
       of that format not yet selected (up to limit).
    2. Fill remaining slots with highest-engagement posts not yet selected.
    3. Sort final selection by engagement descending so agents see best first.
    """
    selected = []
    selected_texts = set()

    def add(post):
        key = post["text"][:80].lower().strip()
        if key not in selected_texts:
            selected.append(post)
            selected_texts.add(key)

    # Group by format
    by_format = {}
    for post in all_posts:
        fmt = post["format"]
        # Normalize variant format names to canonical
        canonical = fmt
        for pf in FORMAT_PRIORITY:
            if pf.lower() in fmt.lower() or fmt.lower() in pf.lower():
                canonical = pf
                break
        by_format.setdefault(canonical, []).append(post)

    # Phase 1: one best post per priority format
    for fmt in FORMAT_PRIORITY:
        if len(selected) >= limit:
            break
        candidates = by_format.get(fmt, [])
        if candidates:
            # Already sorted by engagement desc from Notion
            add(candidates[0])

    # Phase 2: fill remaining slots with highest engagement overall
    for post in all_posts:
        if len(selected) >= limit:
            break
        add(post)

    # Sort final result by engagement desc
    selected.sort(key=lambda p: p["engagement"], reverse=True)
    return selected[:limit]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--min-engagement", type=int, default=0)
    parser.add_argument("--niche", action="append", default=[], help="Filter to one or more Notion Niche values. Repeatable.")
    parser.add_argument("--platform", action="append", default=[], help="Filter to inferred platform: X, LinkedIn, Reddit, Unknown. Repeatable.")
    parser.add_argument("--format", action="append", default=[], help="Filter to one or more Notion Format values. Repeatable.")
    parser.add_argument("--raw", action="store_true", help="Skip stratification, return top N by engagement")
    args = parser.parse_args()

    all_posts = fetch_all_posts(
        min_engagement=args.min_engagement,
        fetch_limit=100,
        niches=args.niche,
        platforms=args.platform,
        formats=args.format,
    )

    if args.raw or len(all_posts) <= args.limit:
        result = all_posts[:args.limit]
    else:
        result = stratify_posts(all_posts, args.limit)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
