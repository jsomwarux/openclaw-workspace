#!/usr/bin/env python3
"""
Fetch rising Google Trends queries across passive-income-relevant categories.
Writes deduplicated results to memory/passive-income/weekly-trends.md.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

from pytrends.request import TrendReq

WORKSPACE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = WORKSPACE / "memory" / "passive-income"
OUTPUT_FILE = OUTPUT_DIR / "weekly-trends.md"

# Category seed keywords — one representative keyword per category
CATEGORIES = {
    "Hobbies & Leisure": "hobbies",
    "Health": "health",
    "Food & Drink": "food",
    "Sports": "sports",
    "Shopping": "shopping",
}

MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds


def fetch_rising_queries(pytrends, keyword, retries=0):
    """Fetch rising related queries for a keyword with retry on 429."""
    try:
        pytrends.build_payload([keyword], timeframe="now 7-d")
        related = pytrends.related_queries()
        rising = related.get(keyword, {}).get("rising")
        if rising is not None and not rising.empty:
            rows = []
            for _, row in rising.head(10).iterrows():
                query = row["query"]
                value = row["value"]
                label = "Breakout" if value >= 5000 else str(value)
                rows.append((query, label))
            return rows
        return []
    except Exception as e:
        status = getattr(e, "response", None)
        status_code = getattr(status, "status_code", None) if status else None
        if status_code == 429 and retries < MAX_RETRIES:
            print(f"  Rate limited on '{keyword}', retrying in {RETRY_DELAY}s (attempt {retries + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
            return fetch_rising_queries(pytrends, keyword, retries + 1)
        if "429" in str(e) and retries < MAX_RETRIES:
            print(f"  Rate limited on '{keyword}', retrying in {RETRY_DELAY}s (attempt {retries + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
            return fetch_rising_queries(pytrends, keyword, retries + 1)
        print(f"  Error fetching '{keyword}': {e}")
        return []


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pytrends = TrendReq(hl="en-US", tz=300)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    results = {}
    seen_queries = set()

    for category, keyword in CATEGORIES.items():
        print(f"Fetching: {category} (keyword: '{keyword}')...")
        rows = fetch_rising_queries(pytrends, keyword)

        # Deduplicate across categories
        deduped = []
        for query, value in rows:
            key = query.lower().strip()
            if key not in seen_queries:
                seen_queries.add(key)
                deduped.append((query, value))

        results[category] = deduped
        print(f"  -> {len(deduped)} unique rising queries")

        # Small delay between categories to avoid rate limiting
        time.sleep(2)

    # Write markdown
    lines = [
        f"# Weekly Google Trends — {date_str}",
        f"Generated: {timestamp}",
        "",
    ]

    total = 0
    for category in CATEGORIES:
        lines.append(f"## {category}")
        entries = results.get(category, [])
        if entries:
            for query, value in entries:
                lines.append(f"- {query} (rising: {value})")
                total += 1
        else:
            lines.append("- No rising queries found this week")
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines))

    print(f"\nDone. {total} total trends written to {OUTPUT_FILE.relative_to(WORKSPACE)}")


if __name__ == "__main__":
    main()
