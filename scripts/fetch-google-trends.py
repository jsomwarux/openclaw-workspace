#!/usr/bin/env python3
"""
Google Trends fetcher — dual mode for passive income intelligence.

Mode 1 — Scout Idea Validation: checks trend for specific keywords passed on
  command line. Used by fetch-signals.py after reading Brave/exploding signals.

Mode 2 — Category Momentum Scan: scans 48 curated keywords across 6 channels
  to surface BREAKOUT keywords for passive income research.
  Computes 30-day change (% growth) + 60-day slope.
  Breakout: +10% 30d change | Rising: 0–10% | Declining: <0%

Run:
  python3 fetch-google-trends.py                    # Category scan (all 48 keywords)
  python3 fetch-google-trends.py --check "side hustle ideas"  # Single keyword check
  python3 fetch-google-trends.py --check "keyword 1" "keyword 2"  # Multiple keywords

Output: memory/passive-income/weekly-google-trends.md
Runtime: ~12 minutes for category scan (1 req / 12s rate limit)
"""

import argparse
import json
import sys
import time as time_module
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

import pandas as pd
from pytrends.request import TrendReq

WORKSPACE = Path(__file__).resolve().parent.parent
CACHE_DIR = WORKSPACE / "memory" / "passive-income" / ".trends-cache"
OUTPUT_FILE = WORKSPACE / "memory" / "passive-income" / "weekly-google-trends.md"
CACHE_TTL_HOURS = 24

# Category scan keyword sets — used for passive income discovery
# Non-tech categories weighted higher to match ExplodingTopics high-priority categories
KEYWORD_SETS = {
    "Monetization & Side Income": [
        "side hustle ideas", "passive income ideas", "make money online",
        "how to monetize skills", "online business ideas", "freelance pricing guide",
        "digital product ideas", "affiliate marketing beginners",
    ],
    "Health & Wellness": [  # Matches ExplodingTopics health-topics
        "home workout plan", "meal prep delivery", "supplement stack",
        "calorie counter app", "meditation app comparison", "personal training app",
        "sleep tracking app", "fitness challenge creator",
    ],
    "Beauty & Personal Care": [  # Matches ExplodingTopics beauty-topics
        "skincare routine builder", "beauty product comparison", "cosmetic ingredients guide",
        "hair care app", "makeup lookup", "beauty subscription box",
        "nail care tutorial", "perfume finder",
    ],
    "Food & Drink": [  # Matches ExplodingTopics food-topics
        "meal planning app", "recipe organized", "wine pairing guide",
        "coffee subscription", "food delivery comparison", "ingredient substitution",
        "restaurant calorie lookup", "kitchen timer app",
    ],
    "Sports & Fitness": [  # Matches ExplodingTopics sports-topics
        "fantasy sports tools", "gym workout tracker", "sports betting odds",
        "running route planner", "cycling training plan", "yoga class finder",
        "sports equipment review", "personal best tracker",
    ],
    "Entertainment & Lifestyle": [  # Matches ExplodingTopics lifestyle/entertainment
        "book tracking app", "movie recommendation engine", "tv show tracker",
        "gaming achievement tracker", "hobby app", "collection organizer",
        "date night ideas generator", "gift recommendation engine",
    ],
}


def _slope(series: pd.Series, n: int = 60) -> float:
    """Simple linear regression slope on last n points."""
    n = min(n, len(series))
    subset = series[-n:]
    x = list(range(n))
    y = list(subset.values)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    num = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean) ** 2 for i in range(n))
    return float(num / den) if den != 0 else 0.0


def _cache_get(key: str) -> Optional[Dict]:
    p = CACHE_DIR / (key.replace(" ", "_") + ".json")
    if not p.exists():
        return None
    try:
        age = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
        if age < timedelta(hours=CACHE_TTL_HOURS):
            return json.loads(p.read_text())
    except Exception:
        pass
    return None


def _cache_set(key: str, data: Dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        (CACHE_DIR / (key.replace(" ", "_") + ".json")).write_text(json.dumps(data))
    except Exception:
        pass


def check_keyword(pt: TrendReq, keyword: str) -> Dict:
    """Fetch 90-day trend for a single keyword. Returns momentum signal."""
    cache_key = "kw_" + keyword.replace(" ", "_")
    cached = _cache_get(cache_key)
    if cached:
        return cached

    try:
        pt.build_payload(kw_list=[keyword], timeframe="today 3-m", geo="US")
        df = pt.interest_over_time()
        if df.empty or keyword not in df.columns:
            return {"keyword": keyword, "error": "no_data"}

        s = df[keyword]
        if len(s) < 30:
            return {"keyword": keyword, "error": "too_few_points"}

        recent = float(s[-30:].mean())
        prior = float(s[-60:-30].mean()) if len(s) >= 60 else float(s[:30].mean())
        change_pct = round(((recent - prior) / max(prior, 1)) * 100, 1)
        slope = round(_slope(s, 60), 3)

        result = {
            "keyword": keyword,
            "current": round(recent, 1),
            "prior_30d": round(prior, 1),
            "change_pct": change_pct,
            "slope_60d": slope,
            "data_points": len(s),
        }
        _cache_set(cache_key, result)
        return result

    except Exception as e:
        return {"keyword": keyword, "error": str(e)}


def run_category_scan() -> None:
    """Scan curated keywords across 6 channels. Outputs to weekly-google-trends.md."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    pt = TrendReq(hl="en-US", tz=240, timeout=15)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    all_results = {}
    breakout_total = 0

    for channel, keywords in KEYWORD_SETS.items():
        print("[" + channel + "]")
        channel_results = []
        for kw in keywords:
            result = check_keyword(pt, kw)
            if "error" in result:
                print("  ⚠ " + kw + ": " + result["error"])
            else:
                badge = "🔥" if result["change_pct"] >= 10 else "📈" if result["change_pct"] >= 0 else "📉"
                print("  " + badge + " " + kw + ": " + str(result["change_pct"]) + "%")
            channel_results.append(result)
            time_module.sleep(12)  # pytrends rate limit

        all_results[channel] = channel_results
        print()

    # Write report
    lines = [
        "# Google Trends — " + date_str,
        "_90-day window, US geo | breakout = +10% 30-day change | channels matched to ExplodingTopics_",
        "Generated: " + now.strftime("%Y-%m-%d %H:%M:%S"),
        "",
    ]

    for channel, results in all_results.items():
        breakout = [r for r in results if r.get("change_pct", 0) >= 10]
        rising = [r for r in results if 0 <= r.get("change_pct", 0) < 10]
        declining = [r for r in results if r.get("change_pct", 0) < 0]
        breakout_total += len(breakout)

        lines.append("## " + channel)
        lines.append(
            "Breakout 🔥: " + str(len(breakout)) + " | Rising 📈: " + str(len(rising))
            + " | Declining 📉: " + str(len(declining))
        )
        lines.append("")

        for r in sorted(breakout, key=lambda x: x["change_pct"], reverse=True):
            lines.append(
                "🔥 **" + r["keyword"] + "** — +" + str(r["change_pct"])
                + "% (30d) | current=" + str(r["current"]) + " | slope=" + str(r["slope_60d"])
            )
        for r in sorted(rising, key=lambda x: x["change_pct"], reverse=True):
            lines.append(
                "📈 " + r["keyword"] + " — +" + str(r["change_pct"]) + "% (30d)"
            )
        for r in sorted(declining, key=lambda x: x["change_pct"]):
            lines.append(
                "📉 " + r["keyword"] + " — " + str(r["change_pct"]) + "% (30d)"
            )
        lines.append("")

    lines += [
        "## Scout Guidance",
        "- 🔥 Breakout keywords = strong demand signal, validate with Brave Search",
        "- 📈 Rising keywords = moderate signal, check for underserved audience",
        "- 📉 Declining keywords = drop from PI consideration",
        "- Non-tech channels (Health, Beauty, Food, Sports, Entertainment) = highest PI signal",
    ]

    OUTPUT_FILE.write_text("\n".join(lines))
    print("✅ " + str(breakout_total) + " breakout keywords → " + OUTPUT_FILE.name)


def run_keyword_check(keywords: List[str]) -> None:
    """Check specific keywords (used by fetch-signals.py for Scout-idea validation)."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    pt = TrendReq(hl="en-US", tz=240, timeout=15)
    now = datetime.now()

    results = []
    for kw in keywords:
        print("Checking: " + kw + "...", end=" ", flush=True)
        result = check_keyword(pt, kw)
        if "error" in result:
            print("⚠ " + result["error"])
        else:
            badge = "🔥" if result["change_pct"] >= 10 else "📈" if result["change_pct"] >= 0 else "📉"
            print(badge + " " + str(result["change_pct"]) + "% (" + str(result["current"]) + ")")
        results.append(result)
        time_module.sleep(12)

    # Print compact results
    print("\n=== Trend Check Results ===")
    for r in results:
        if "error" in r:
            print("  ⚠ " + r["keyword"] + ": " + r["error"])
        else:
            badge = "🔥" if r["change_pct"] >= 10 else "📈" if r["change_pct"] >= 0 else "📉"
            print("  " + badge + " " + r["keyword"] + ": " + str(r["change_pct"]) + "% change | current="
                  + str(r["current"]) + " | slope=" + str(r["slope_60d"]))


def main():
    parser = argparse.ArgumentParser(description="Google Trends fetcher")
    parser.add_argument("--check", nargs="+", help="Check specific keyword(s) and exit")
    args = parser.parse_args()

    if args.check:
        run_keyword_check(args.check)
    else:
        run_category_scan()


if __name__ == "__main__":
    main()
