#!/usr/bin/env python3
"""
ExplodingTopics.com scraper — uses the actual internal API.

Found the real endpoint by inspecting network traffic in Playwright:
  GET /api/trends?page=N&size=30&period=24&sort=growth&order=desc
           &type=all&categories={cat}&unverified=null&...

Returns 977 topics for beauty alone, with rich data:
  - keyword, growth['24'], searchHistory[265 monthly pts]
  - keywordDataGlobal{vol, cpc}, categories[], classifications{}
  - briefDescription, path (URL slug)

Run: python3 fetch-exploding-topics.py
Output: memory/passive-income/weekly-exploding-topics.md
Cache: 24h per category
"""

import json
import time as time_module
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

import requests

WORKSPACE = Path(__file__).resolve().parent.parent
CACHE_DIR = WORKSPACE / "memory" / "passive-income" / ".exploding-cache"
OUTPUT_FILE = WORKSPACE / "memory" / "passive-income" / "weekly-exploding-topics.md"
CACHE_TTL_HOURS = 24
PAGE_SIZE = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://explodingtopics.com/",
    "Origin": "https://explodingtopics.com",
}

CATEGORIES = [
    ("beauty",        "Beauty & Personal Care",  "high"),
    ("health",        "Health & Wellness",        "high"),
    ("food",          "Food & Drink",             "high"),
    ("sports",        "Sports & Fitness",         "high"),
    ("lifestyle",     "Lifestyle & Hobbies",      "high"),
    ("entertainment", "Entertainment & Media",  "high"),
    ("education",     "Education",               "medium"),
    ("gaming",        "Gaming",                 "medium"),
    ("science",       "Science & Research",      "medium"),
    ("business",      "Business & Finance",      "low"),
    ("finance",       "Finance",                 "low"),
    ("marketing",     "Marketing",               "low"),
    ("ecommerce",     "E-Commerce",             "low"),
    ("software",      "Software & Tech",         "low"),
]

# Growth thresholds per priority tier (for output filtering)
THRESHOLDS = {"high": 0, "medium": 3, "low": 10}


def _base_url(cat: str, page: int) -> str:
    return (
        f"https://explodingtopics.com/api/trends"
        f"?page={page}&size={PAGE_SIZE}&period=24&sort=growth&order=desc"
        f"&type=all&categories={cat}&unverified=null&proAccess=null"
        f"&proTopicsSelected=false&brandedTopicsSelected=all"
        f"&excludePeaked=true&volatile=stable"
    )


def _cache_path(cat: str) -> Path:
    return CACHE_DIR / (cat + "_all.json")


def _cached(cat: str) -> Optional[Dict]:
    p = _cache_path(cat)
    if not p.exists():
        return None
    try:
        age = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
        if age < timedelta(hours=CACHE_TTL_HOURS):
            return json.loads(p.read_text())
    except Exception:
        pass
    return None


def _save(cat: str, data: Dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _cache_path(cat).write_text(json.dumps(data))
    except Exception:
        pass


def fetch_category(cat: str) -> Dict:
    """Fetch ALL pages for a category. Returns {topics: [...], total: N}."""
    cached = _cached(cat)
    if cached:
        return cached

    first_url = _base_url(cat, 1)
    first_resp = requests.get(first_url, headers=HEADERS, timeout=20)
    if first_resp.status_code != 200:
        return {"cat": cat, "topics": [], "total": 0, "error": first_resp.status_code}

    first_data = first_resp.json()
    total = first_data.get("total", 0)
    all_topics = list(first_data.get("trends", []))
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE

    if total_pages > 1:
        for page in range(2, total_pages + 1):
            url = _base_url(cat, page)
            try:
                r = requests.get(url, headers=HEADERS, timeout=20)
                if r.status_code == 200:
                    page_data = r.json()
                    all_topics.extend(page_data.get("trends", []))
            except Exception:
                pass
            time_module.sleep(0.5)  # Polite rate limiting

    result = {"cat": cat, "topics": all_topics, "total": total}
    _save(cat, result)
    return result


def _format_growth(g: float) -> str:
    """Format growth value: 99 = '99x', 5.67 = '5.67x'."""
    if g >= 99:
        return "99x+"
    return f"{g:.2f}x"


def _clean_item(t: Dict) -> Dict:
    kw = t.get("keyword", "")
    if not kw or len(kw) < 2:
        return None
    g24 = float(t.get("growth", {}).get("24", 0))
    sh = t.get("searchHistory", [])
    current = sh[-1]["value"] if sh else 0
    vol = t.get("keywordDataGlobal", {}).get("vol", 0)
    cpc = t.get("keywordDataGlobal", {}).get("cpc", 0)
    cats = t.get("categories", [])
    path = t.get("path", "")
    classification = t.get("classification", {})
    desc = t.get("briefDescription", "")[:150]
    return {
        "keyword": kw,
        "growth_24m_raw": g24,
        "growth_24m_fmt": _format_growth(g24),
        "current_interest": current,
        "volume": vol,
        "cpc": cpc,
        "categories": cats,
        "url": f"https://explodingtopics.com/topics/{path}",
        "description": desc,
    }


def main():
    print("=== ExplodingTopics.com — Full API Scan ===\n")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    all_data = {}
    total_topics = 0

    for cat, label, priority in CATEGORIES:
        print(f"[{label}] ({priority}) — fetching...", end=" ", flush=True)
        data = fetch_category(cat)
        count = len(data.get("topics", []))
        total = data.get("total", 0)
        print(f"✅ {count}/{total} topics")
        all_data[cat] = {"label": label, "priority": priority, **data}
        total_topics += count
        time_module.sleep(1)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    # ── Build output ─────────────────────────────────────────────────────────
    lines = [
        f"# Exploding Topics — {date_str}",
        f"_14 categories | {total_topics} total topics | real API data_",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "**Priority guide:** 🔴 high (non-tech, highest PI signal) | 🟡 medium | 🔵 low (saturated tech)_",
        "**Growth format:** '99x+' means 99x or greater. '5.67x' means 5.67x growth over 24 months.",
        "",
        "**Key fields:** keyword | growth (24mo) | volume (monthly searches) | CPC ($) | sub-categories",
        "",
    ]

    for cat, label, priority in CATEGORIES:
        data = all_data.get(cat, {})
        raw_topics = data.get("topics", [])
        threshold = THRESHOLDS.get(priority, 0)
        cleaned = [_clean_item(t) for t in raw_topics]
        filtered = [t for t in cleaned if t and t["growth_24m_raw"] >= threshold]

        if not filtered:
            continue

        badge = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🔵"
        lines.append(
            f"## {badge} {label} — {priority.upper()} | "
            f"{len(filtered)}/{data.get('total', 0)} topics"
        )

        for t in filtered[:20]:
            g = t["growth_24m_fmt"]
            vol = f"{t['volume']:,}" if t["volume"] else "?"
            cpc = f"${t['cpc']:.2f}" if t["cpc"] else "?"
            cats = ", ".join(t["categories"][:3])
            lines.append(
                f"- **{t['keyword']}** | growth: {g} | vol: {vol} | cpc: {cpc}"
                f" | {cats} | [link]({t['url']})"
            )
            if t["description"]:
                lines.append(f"  _{t['description']}_")
        lines.append("")

    lines += [
        "## Scout Guidance",
        "",
        "**Non-tech (🔴) = highest PI signal** — real consumer problems, less tech-founder competition",
        "**Growth interpretation:** 99x+ = viral/explosive | 10-99x = strong growth | 3-10x = moderate | <3x = skip",
        "",
        "**What to look for:**",
        "- 🔴 categories with specific product/ingredient names (e.g., 'Pdrn Serum', 'GLP-1 supplement')",
        "- Low competition keywords with decent volume (vol 1000+) and clear monetization path",
        "- Product comparison or ranking opportunities: 'best X for Y', 'X vs Y'",
        "",
        "**What to skip:**",
        "- Generic terms ('skincare routine', 'best moisturizer') — already covered by big players",
        "- Pure tech terms ('AI writing tool', 'developer API') — saturated",
        "- Branded items (branded=true) — trademark risk",
    ]

    OUTPUT_FILE.write_text("\n".join(lines))
    print(f"\n✅ {total_topics} topics → {OUTPUT_FILE.name}")
    print("All 14 categories scraped from the real ExplodingTopics API ✅")


if __name__ == "__main__":
    main()
