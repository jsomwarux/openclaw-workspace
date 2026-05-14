#!/usr/bin/env python3
"""Brave Search fallback for freshness/current-news workflows.

Use when OpenClaw managed web_search cannot support freshness filters.
Reads BRAVE_API_KEY from environment. Does not require the OpenClaw Brave plugin.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

FRESHNESS_MAP = {
    "day": "pd",
    "week": "pw",
    "month": "pm",
    "year": "py",
    "pd": "pd",
    "pw": "pw",
    "pm": "pm",
    "py": "py",
}

def main() -> int:
    parser = argparse.ArgumentParser(description="Brave Search API fallback")
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--freshness", default=None, choices=sorted(FRESHNESS_MAP))
    parser.add_argument("--country", default="US")
    parser.add_argument("--search-lang", default="en")
    parser.add_argument("--json", action="store_true", help="emit raw normalized JSON")
    args = parser.parse_args()

    key = os.environ.get("BRAVE_API_KEY")
    if not key:
        print("ERROR: BRAVE_API_KEY is not set", file=sys.stderr)
        return 2

    params = {
        "q": args.query,
        "count": max(1, min(args.count, 20)),
        "country": args.country,
        "search_lang": args.search_lang,
    }
    if args.freshness:
        params["freshness"] = FRESHNESS_MAP[args.freshness]

    url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "X-Subscription-Token": key,
        "User-Agent": "openclaw-brave-fallback/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: Brave request failed: {exc}", file=sys.stderr)
        return 1

    results = []
    for item in data.get("web", {}).get("results", [])[:params["count"]]:
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
            "age": item.get("age", ""),
            "page_age": item.get("page_age", ""),
        })

    if args.json:
        print(json.dumps({"query": args.query, "provider": "brave-direct", "results": results}, indent=2))
    else:
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['title']}\n   {item['url']}\n   {item['description']}\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
