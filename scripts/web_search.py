#!/usr/bin/env python3
"""Canonical local web search for OpenClaw agents/crons.

Why this exists:
- Gateway-managed web_search can misroute freshness/date-filtered searches.
- The Brave OpenClaw plugin has been unstable in this environment.
- Direct Brave API works reliably and does not require gateway plugin config/restarts.

Usage:
  set -a; source ~/.config/env/global.env; set +a
  python3 scripts/web_search.py "AI agents news" --freshness day --count 5 --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date

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


def brave_search(query: str, count: int, freshness: str | None, country: str, search_lang: str) -> dict:
    key = os.environ.get("BRAVE_API_KEY")
    if not key:
        raise RuntimeError("BRAVE_API_KEY is not set; source ~/.config/env/global.env first")

    params = {
        "q": query,
        "count": max(1, min(count, 20)),
        "country": country,
        "search_lang": search_lang,
    }
    if freshness:
        params["freshness"] = FRESHNESS_MAP[freshness]

    url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": key,
            "User-Agent": "openclaw-local-web-search/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = json.load(resp)

    results = []
    for item in raw.get("web", {}).get("results", [])[: params["count"]]:
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "age": item.get("age", ""),
                "page_age": item.get("page_age", ""),
                "source": item.get("profile", {}).get("name", ""),
            }
        )

    return {
        "provider": "brave-direct",
        "query": query,
        "freshness": freshness,
        "country": country,
        "search_lang": search_lang,
        "retrieved_at_date": date.today().isoformat(),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Stable local web search for OpenClaw jobs")
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--freshness", choices=sorted(FRESHNESS_MAP), default=None)
    parser.add_argument("--country", default="US")
    parser.add_argument("--search-lang", default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        data = brave_search(args.query, args.count, args.freshness, args.country, args.search_lang)
    except Exception as exc:
        print(f"WEB_SEARCH_ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    if not data["results"]:
        print(f"No results for: {args.query}")
        return 0

    print(f"Provider: {data['provider']} | Query: {data['query']} | Freshness: {data['freshness'] or 'none'}")
    for i, item in enumerate(data["results"], 1):
        print(f"\n{i}. {item['title']}\n   {item['url']}")
        if item.get("age") or item.get("page_age"):
            print(f"   age={item.get('age','')} page_age={item.get('page_age','')}")
        if item.get("description"):
            print(f"   {item['description']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
