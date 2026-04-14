#!/usr/bin/env python3
"""
Fetch rising/market-signal queries using Brave Search.
Replaces pytrends (rate-limited by Google) with reliable Brave API.

Signal sources tuned for PASSIVE INCOME IDEA GENERATION:

1. Brave Web Search: "[keyword] alternative", "[keyword] vs"
   → Top results reveal what people are seeking alternatives TO.
   Community sites (alternativeto.net, reddit, G2, Capterra) = high signal.
   These keywords are DIRECT monetization leads.

2. Brave Web Search: "trending [niche]" + emerging platform searches
   → Surfacing new platform adoption = integration/替代 opportunities.

3. Product Hunt trending page: direct scrape
   → New launches = API/data opportunities.

Each keyword gets exactly 1 Brave API call (1/50th of daily budget).
Results cached for 24h — only refresh if cache is >24h old.
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

import requests

# Load BRAVE_API_KEY from OpenClaw's global.env file directly
# This works when the script runs as a cron (subprocess won't inherit env)
ENV_FILE = Path.home() / ".config" / "env" / "global.env"
if not os.environ.get("BRAVE_API_KEY") and ENV_FILE.exists():
    try:
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

WORKSPACE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = WORKSPACE / "memory" / "passive-income"
OUTPUT_FILE = OUTPUT_DIR / "weekly-trends.md"
CACHE_DIR = OUTPUT_DIR / ".trends-cache"
CACHE_TTL_HOURS = 24

BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
HEADERS = {
    "Accept": "application/json",
    "X-Subscription-Token": BRAVE_API_KEY,
}

# Keywords tuned for IDEA SIGNAL (not vanity volume)
# Each entry: (label, intent_type, list_of_keywords)
KEYWORD_SECTIONS = [
    {
        "label": "🔴 Frustration: Productivity & Workflow Tools",
        "intent": "frustration",
        "keywords": [
            "Notion alternative 2026",
            "Airtable alternative 2026",
            "Asana alternative 2026",
            "Trello alternative 2026",
            "Monday.com alternative 2026",
            "Zapier alternative 2026",
            "ClickUp alternative 2026",
            "Coda alternative 2026",
        ],
    },
    {
        "label": "🔴 Frustration: AI & Dev Tools",
        "intent": "frustration",
        "keywords": [
            "Cursor AI alternative",
            "Copilot alternative",
            "Windsurf alternative",
            "Replit alternative",
            "Vercel alternative",
            "Firebase alternative",
            "Supabase alternative",
            "Railway alternative",
        ],
    },
    {
        "label": "🔴 Frustration: Design & No-Code Tools",
        "intent": "frustration",
        "keywords": [
            "Canva alternative",
            "Figma alternative",
            "Webflow alternative",
            "Framer alternative",
            "Bubble.io alternative",
            "Adalo alternative",
            "Glide apps alternative",
            "Xano alternative",
        ],
    },
    {
        "label": "🔴 Frustration: Business & Freelance Tools",
        "intent": "frustration",
        "keywords": [
            "QuickBooks alternative",
            "FreshBooks alternative",
            "Stripe alternative",
            "PayPal alternative",
            "Upwork alternative",
            "Fiverr alternative",
            "Calendly alternative",
            "Dubsado alternative",
        ],
    },
    {
        "label": "💰 Commercial: Side Income & Monetization",
        "intent": "commercial",
        "keywords": [
            "side hustle ideas 2026",
            "how to make money on side",
            "passive income ideas",
            "ways to earn passive income",
            "how to monetize newsletter",
            "how to monetize blog",
            "AI side hustle ideas",
            " profitable micro SaaS ideas",
        ],
    },
    {
        "label": "✅ Verification: Credentials, Reviews & Trust",
        "intent": "verification",
        "keywords": [
            "verify contractor license online",
            "is contractor licensed check",
            "verify business license online",
            "check if Amazon review is real",
            "how to spot fake reviews",
            "verify professional license",
            "background check service comparison",
            "tenant screening service review",
        ],
    },
    {
        "label": "🛠️ Problem: Trade & Construction Niche",
        "intent": "problem",
        "keywords": [
            "construction project management software small contractor",
            "best estimating software for contractors",
            "contractor invoice app",
            "construction scheduling software",
            "how to track construction costs",
            "roofing estimate software",
        ],
    },
    {
        "label": "🛠️ Problem: Property Management Niche",
        "intent": "problem",
        "keywords": [
            "property management software small landlord",
            "best tenant screening service",
            "rental property management app",
            "how to price rental property",
            "landlord expense tracker",
            "rental property maintenance tracking",
        ],
    },
    {
        "label": "🛠️ Problem: E-commerce & Reseller Niche",
        "intent": "problem",
        "keywords": [
            "product sourcing tool resellers",
            "online arbitrage software",
            "retail arbitrage tool",
            "how to find wholesale suppliers",
            "best price tracking tool",
            "Amazon FBA research tool",
        ],
    },
    {
        "label": "⚖️ Emerging: AI Tool Comparisons & Tutorials",
        "intent": "comparison",
        "keywords": [
            "Claude AI use cases tutorial",
            "ChatGPT alternatives 2026",
            "Perplexity vs ChatGPT",
            "bolt.new tutorial",
            "v0 by Vercel tutorial",
            "Lovable AI app builder review",
            "Mage AI alternative",
            "Cursor vs Copilot",
        ],
    },
]

# URL patterns that indicate community/community信号 = HIGH signal
HIGH_SIGNAL_DOMAINS = [
    "reddit.com", "alternativeto.net", "g2.com", "capterra.com", "producthunt.com",
    "quora.com", "stackexchange.com", "github.com", "hackernews", "lobste.rs",
    "slashdot.org", "news.ycombinator.com",
]

# Keywords in title that indicate frustration = HIGH signal
HIGH_SIGNAL_TITLE_TOKENS = [
    "alternative", "vs", "versus", "replace", "instead of",
    "legit", "scam", "fake", "is it real", "real or fake",
    "verify", "verification", "check if", "how to spot",
    "best", "top", "comparison", "review", "honest review",
    "escape", "migrate from", "moving from", "left because",
]


def is_high_signal_result(url: str, title: str, description: str) -> bool:
    """Return True if result indicates community/frustration signal."""
    url_lower = url.lower()
    title_lower = title.lower()
    desc_lower = description.lower()
    combined = f"{title_lower} {desc_lower}"

    # Community domain signal
    if any(domain in url_lower for domain in HIGH_SIGNAL_DOMAINS):
        return True
    # Title token signal
    if any(token in combined for token in HIGH_SIGNAL_TITLE_TOKENS):
        return True
    return False


def brave_search(query: str, retries=2) -> dict:
    """Call Brave Search API with retry. Returns parsed JSON or {} on failure."""
    params = {"q": query, "count": 10}
    for attempt in range(retries + 1):
        try:
            resp = requests.get(
                BRAVE_ENDPOINT,
                headers=HEADERS,
                params=params,
                timeout=15,
            )
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                if attempt < retries:
                    wait = 30 * (2 ** attempt)
                    print(f"  ⏳ Rate limited, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"  ⚠ Brave 429 on '{query}' after {retries} retries")
                    return {}
            else:
                print(f"  ⚠ Brave {resp.status_code} on '{query}'")
                return {}
        except Exception as e:
            if attempt < retries:
                time.sleep(5 * (attempt + 1))
            else:
                print(f"  ⚠ Network error on '{query}': {e}")
                return {}
    return {}


def get_cache_path(keyword: str) -> Path:
    """Return path for cached result of a keyword."""
    safe = keyword.replace(" ", "-").replace("/", "-")[:60]
    return CACHE_DIR / f"{safe}.json"


def get_cached(keyword: str) -> Optional[dict]:
    """Return cached result if fresh, else None."""
    cache_path = get_cache_path(keyword)
    if not cache_path.exists():
        return None
    try:
        age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        if age < timedelta(hours=CACHE_TTL_HOURS):
            return json.loads(cache_path.read_text())
    except Exception:
        pass
    return None


def save_cache(keyword: str, data: dict):
    """Save result to cache."""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = get_cache_path(keyword)
        cache_path.write_text(json.dumps(data))
    except Exception as e:
        print(f"  ⚠ Cache write error: {e}")


def extract_signal_results(data: dict) -> list:
    """Extract top results that indicate community/frustration signal."""
    results = []
    # Brave API: data["web"]["results"] is a direct list
    raw_results = data.get("web", {}).get("results", [])
    if not isinstance(raw_results, list):
        raw_results = []
    for item in raw_results:
        url = item.get("url", "")
        title = item.get("title", "")
        description = item.get("description", "")
        if is_high_signal_result(url, title, description):
            results.append({
                "title": title,
                "url": url,
                "description": description[:200],
                "domain": url.split("/")[2] if "/" in url else url,
            })
    return results


def main():
    if not BRAVE_API_KEY:
        print("ERROR: BRAVE_API_KEY not set in ~/.config/env/global.env")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Fetching signal queries — {date_str}")
    print(f"Brave API: {BRAVE_API_KEY[:8]}...  |  Cache TTL: {CACHE_TTL_HOURS}h\n")

    all_results = {}
    seen_signals = set()  # deduplicate by normalized title

    total_keywords = sum(len(s["keywords"]) for s in KEYWORD_SECTIONS)
    processed = 0
    cache_hits = 0

    for section in KEYWORD_SECTIONS:
        label = section["label"]
        intent = section["intent"]
        keywords = section["keywords"]
        print(f"[{label}]")

        section_signals = []
        for keyword in keywords:
            processed += 1
            # Check cache first
            cached = get_cached(keyword)
            if cached is not None:
                cache_hits += 1
                print(f"  ✅ {keyword} (cached)")
            else:
                print(f"  🔍 {keyword}...", end=" ", flush=True)
                cached = brave_search(keyword)
                if cached:
                    save_cache(keyword, cached)
                    print("done")
                else:
                    print("no results")
                # Rate limit protection between API calls
                time.sleep(2)

            if cached:
                signals = extract_signal_results(cached)
                for sig in signals:
                    key = sig["title"].lower()[:80]
                    if key not in seen_signals:
                        seen_signals.add(key)
                        sig["query"] = keyword
                        sig["intent"] = intent
                        section_signals.append(sig)

        count = len(section_signals)
        print(f"  → {count} signal results\n")
        all_results[label] = {"intent": intent, "signals": section_signals}

    # ── Write report ────────────────────────────────────────────────────────
    lines = [
        f"# Weekly Google Trends — {date_str}",
        "_Brave Search signal detection — alternatives, comparisons, community discussions_",
        f"Generated: {timestamp}",
        "",
        "## Intent Legend",
        "- 🔴 Frustration: people escaping/replacing a tool → DIRECT monetization lead",
        "- 💰 Commercial: side income/monetization intent → potential customers",
        "- ✅ Verification: checking credentials/reviews/trust → underserved white space",
        "- 🛠️ Problem: specific job-to-be-done in a niche → micro-SaaS opportunity",
        "- ⚖️ Comparison: evaluating alternatives → integration/替代 opportunity",
        "",
    ]

    for label, data in all_results.items():
        intent = data["intent"]
        signals = data["signals"]
        lines.append(f"## {label}")
        if signals:
            for sig in signals:
                lines.append(f"- [{sig['domain']}] {sig['title']}")
                lines.append(f"  _Query: \"{sig['query']}\"_")
        else:
            lines.append("- No strong signal results found")
        lines.append("")

    # Summary
    total = sum(len(v["signals"]) for v in all_results.values())
    by_intent = {}
    for v in all_results.values():
        i = v["intent"]
        by_intent[i] = by_intent.get(i, 0) + len(v["signals"])

    lines.append("## Signal Summary\n")
    lines.append(f"**Total signal results: {total}** (from {total_keywords} queries, {cache_hits} cache hits)")
    lines.append(f"- 🔴 Frustration:     {by_intent.get('frustration', 0)}")
    lines.append(f"- 💰 Commercial:      {by_intent.get('commercial', 0)}")
    lines.append(f"- ✅ Verification:   {by_intent.get('verification', 0)}")
    lines.append(f"- 🛠️ Problem:       {by_intent.get('problem', 0)}")
    lines.append(f"- ⚖️ Comparison:    {by_intent.get('comparison', 0)}")

    lines.append("\n## Scout Guidance")
    lines.append(
        "Community results (Reddit, alternativeto.net, G2, Product Hunt) = strong signal."
        " These represent people actively seeking alternatives — the core monetization lead."
        " Focus scouting energy on categories with 5+ community results."
    )

    OUTPUT_FILE.write_text("\n".join(lines))

    total_signals = sum(len(v["signals"]) for v in all_results.values())
    print(f"\n✅ Done. {total_signals} signal results → {OUTPUT_FILE.relative_to(WORKSPACE)}")
    print(f"   Cache: {cache_hits}/{total_keywords} hits")


if __name__ == "__main__":
    import sys
    main()
