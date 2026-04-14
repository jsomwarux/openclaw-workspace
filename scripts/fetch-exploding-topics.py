#!/usr/bin/env python3
"""
ExplodingTopics.com scraper — extracts emerging keywords from public category pages.
See script header for full documentation.
Run: python3 fetch-exploding-topics.py
Output: memory/passive-income/weekly-exploding-topics.md
"""
import json
import re
import time as time_module
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict

import requests

WORKSPACE = Path(__file__).resolve().parent.parent
CACHE_DIR = WORKSPACE / "memory" / "passive-income" / ".exploding-cache"
OUTPUT_FILE = WORKSPACE / "memory" / "passive-income" / "weekly-exploding-topics.md"
CACHE_TTL_HOURS = 24

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

WORKING_SLUGS = [
    ("software-topics", "Software & Tech"),
    ("startups", "Startups"),
]


def _cache_path(slug: str) -> Path:
    return CACHE_DIR / (slug + ".json")


def _cached(slug: str) -> Optional[Dict]:
    p = _cache_path(slug)
    if not p.exists():
        return None
    try:
        age = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
        if age < timedelta(hours=CACHE_TTL_HOURS):
            return json.loads(p.read_text())
    except Exception:
        pass
    return None


def _save(slug: str, data: Dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _cache_path(slug).write_text(json.dumps(data))
    except Exception:
        pass


def _extract_json(html: str) -> Optional[Dict]:
    m = re.search(r"__NEXT_DATA__\s*=\s*({.*)", html, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    depth = 0
    for i, c in enumerate(raw):
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(raw[: i + 1])
                except json.JSONDecodeError:
                    pass
    return None


def fetch_page(slug: str) -> Optional[Dict]:
    try:
        resp = requests.get("https://explodingtopics.com/" + slug, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            return None
    except Exception:
        return None

    data = _extract_json(resp.text)
    if not data:
        return None
    try:
        trending = data["props"]["pageProps"]["trendingDesktopData"]
    except (KeyError, TypeError):
        return None

    def clean(item: Dict) -> Optional[Dict]:
        kw = item.get("keyword", "")
        if not kw or len(kw) < 3:
            return None
        growth_pct = float(item.get("growth", {}).get("24", 0))
        sh = item.get("searchHistory", [])
        current = sh[-1]["value"] if sh else 0
        path = item.get("path", "")
        return {
            "keyword": kw,
            "growth_24m": growth_pct,
            "current_interest": current,
            "url": "https://explodingtopics.com/topics/" + path,
        }

    trends = [clean(t) for t in trending.get("trends", [])]
    startups = [clean(t) for t in trending.get("startups", [])]
    all_items = [t for t in trends + startups if t]
    all_items.sort(key=lambda x: x["growth_24m"], reverse=True)
    return {"slug": slug, "topics": all_items, "fetched_at": datetime.now().isoformat()}


def main():
    print("=== ExplodingTopics.com Scraper ===\n")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    all_data = {}
    total = 0

    for slug, label in WORKING_SLUGS:
        print("[" + label + "] " + slug + "...", end=" ", flush=True)
        cached = _cached(slug)
        if cached:
            c = len(cached.get("topics", []))
            print("✅ cached (" + str(c) + " topics)")
            all_data[slug] = cached
            total += c
            continue
        data = fetch_page(slug)
        if data:
            c = len(data["topics"])
            lo = data["topics"][-1]["growth_24m"]
            hi = data["topics"][0]["growth_24m"]
            print("🔍 " + str(c) + " topics (growth: " + str(lo) + "% – " + str(hi) + "%)")
            _save(slug, data)
            all_data[slug] = data
            total += c
        else:
            print("⚠ no data")
            all_data[slug] = {"slug": slug, "topics": [], "fetched_at": datetime.now().isoformat()}
        time_module.sleep(2)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    lines = [
        "# Exploding Topics — " + date_str,
        "_Public scrapes: software-topics + startups | " + str(total) + " total topics_",
        "Generated: " + now.strftime("%Y-%m-%d %H:%M:%S"),
        "**Total topics: " + str(total) + "**",
        "",
    ]
    for slug, label in WORKING_SLUGS:
        data = all_data.get(slug, {})
        topics = data.get("topics", [])
        lines.append("## " + label + " (" + slug + ")")
        if topics:
            for t in topics:
                badge = "🔴" if t["growth_24m"] >= 50 else "🟠" if t["growth_24m"] >= 20 else "🟡"
                lines.append(
                    badge + " **" + t["keyword"] + "** — " + str(t["growth_24m"]) + "% growth, "
                    "interest=" + str(t["current_interest"]) + " | [link](" + t["url"] + ")"
                )
        else:
            lines.append("- No data (auth-gated)")
        lines.append("")

    lines += [
        "## Scout Guidance",
        "- 🔴 ≥50% growth: validate with Brave Search immediately",
        "- 🟠 20–49% growth: cross-ref with X complaints",
        "- 🟡 <20% growth: background — skip",
        "- Note: Crypto/Finance/Health slugs = 404 (paid tier). Software + Startups only.",
    ]

    OUTPUT_FILE.write_text("\n".join(lines))
    print("\n✅ " + str(total) + " topics → " + OUTPUT_FILE.name)


if __name__ == "__main__":
    main()
