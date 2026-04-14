#!/usr/bin/env python3
"""
Google Trends fetcher — validates keyword momentum via pytrends.

Uses interest_over_time (only endpoint still working as of 2026-04).
Checks curated keyword lists across 6 channels, computes 90-day trend slope.

Breakout: +10% 30d change | Rising: 0–10% | Declining: <0%

Output: memory/passive-income/weekly-google-trends.md
Runtime: ~12 minutes (1 req / 12s rate limit)
"""

import time as time_module
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

import pandas as pd
from pytrends.request import TrendReq

WORKSPACE = Path(__file__).resolve().parent.parent
CACHE_DIR = WORKSPACE / "memory" / "passive-income" / ".trends-cache"
OUTPUT_FILE = WORKSPACE / "memory" / "passive-income" / "weekly-google-trends.md"
CACHE_TTL_HOURS = 24

KEYWORD_SETS = {
    "Monetization & Side Income": [
        "side hustle ideas", "make money online", "passive income ideas",
        "how to monetize skills", "freelance side gig", "online business ideas",
        "sell digital products", "affiliate marketing for beginners",
    ],
    "AI & Productivity Tools": [
        "AI tools for business", "best AI assistant", "automation tools",
        "AI productivity app", "best AI writing tool", "ChatGPT alternatives",
    ],
    "Crypto & Web3": [
        "crypto portfolio tracker", "best DeFi wallet", "crypto tax tool",
        "Web3 portfolio management", "crypto analytics",
    ],
    "Finance & Investing": [
        "investment tracker app", "personal finance tool", "budget app comparison",
        "robo advisor alternatives", "financial planning software",
    ],
    "Content Creation": [
        "content creator tools", "TikTok analytics", "creator economy platform",
        "best video editing app", "content scheduling tool",
    ],
    "Niche Marketplaces": [
        "vertical SaaS", "marketplace builder", "micro-SaaS ideas",
        "B2B marketplace software", "niche job board platform",
    ],
}


def _cache_path(key: str) -> Path:
    return CACHE_DIR / (key.replace(" ", "_") + ".json")


def _cached(key: str) -> Optional[Dict]:
    p = _cache_path(key)
    if not p.exists():
        return None
    try:
        age = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
        if age < timedelta(hours=CACHE_TTL_HOURS):
            return json.loads(p.read_text())
    except Exception:
        pass
    return None


def _save(key: str, data: Dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _cache_path(key).write_text(json.dumps(data))
    except Exception:
        pass


def _slope(series: pd.Series, n: int) -> float:
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


def fetch_keyword_trend(pt: TrendReq, keyword: str) -> Dict:
    """Fetch 90-day trend. Returns change_pct and slope."""
    import json as _json
    cache_key = keyword.replace(" ", "_")
    cached = _cached(cache_key)
    if cached:
        return cached

    try:
        pt.build_payload(kw_list=[keyword], timeframe="today 3-m", geo="US")
        df = pt.interest_over_time()
        if df.empty or keyword not in df.columns:
            return {"keyword": keyword, "error": "no data"}

        s = df[keyword]
        if len(s) < 30:
            return {"keyword": keyword, "error": "too few data points"}

        recent = float(s[-30:].mean())
        prior = float(s[-60:-30].mean())
        change_pct = round(((recent - prior) / max(prior, 1)) * 100, 1) if prior > 0 else 0.0
        slope = round(_slope(s, 60), 3)

        result = {
            "keyword": keyword,
            "current": round(recent, 1),
            "prior_30d": round(prior, 1),
            "change_pct": change_pct,
            "slope_60d": slope,
            "data_points": len(s),
        }
        _save(cache_key, result)
        return result
    except Exception as e:
        return {"keyword": keyword, "error": str(e)}


def main():
    print("=== Google Trends Fetcher (pytrends) ===\n")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    from datetime import timedelta
    import json

    pt = TrendReq(hl="en-US", tz=240, timeout=15)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    all_results = {}
    breakout_total = 0

    for channel, keywords in KEYWORD_SETS.items():
        print("[" + channel + "]")
        channel_results = []

        for kw in keywords:
            result = fetch_keyword_trend(pt, kw)
            if "error" in result:
                print("  ⚠ " + kw + ": " + result["error"])
            else:
                badge = "🔥" if result["change_pct"] >= 10 else "📈" if result["change_pct"] >= 0 else "📉"
                print("  " + badge + " " + kw + ": " + str(result["change_pct"]) + "%")
            channel_results.append(result)
            time_module.sleep(12)

        all_results[channel] = channel_results
        print()

    lines = [
        "# Google Trends (pytrends) — " + date_str,
        "_interest_over_time: 90-day window, US | breakout = +10% 30d change_",
        "Generated: " + now.strftime("%Y-%m-%d %H:%M:%S"),
        "",
    ]

    for channel, results in all_results.items():
        breakout = [r for r in results if r.get("change_pct", 0) >= 10]
        rising = [r for r in results if 0 < r.get("change_pct", 0) < 10]
        declining = [r for r in results if r.get("change_pct", 0) < 0]
        breakout_total += len(breakout)

        lines.append("## " + channel)
        lines.append(
            "**Total: " + str(len(results)) + " | 🔥 Breakout: " + str(len(breakout))
            + " | 📈 Rising: " + str(len(rising)) + " | 📉 Declining: " + str(len(declining)) + "**"
        )
        lines.append("")

        for r in sorted(breakout, key=lambda x: x["change_pct"], reverse=True):
            lines.append(
                "- 🔴 **" + r["keyword"] + "** — +" + str(r["change_pct"])
                + "% (30d), current=" + str(r["current"]) + " slope=" + str(r["slope_60d"])
            )
        for r in sorted(rising, key=lambda x: x["change_pct"], reverse=True):
            lines.append(
                "- 🟡 " + r["keyword"] + " — +" + str(r["change_pct"]) + "% (30d)"
            )
        for r in sorted(declining, key=lambda x: x["change_pct"]):
            lines.append(
                "- 🔵 " + r["keyword"] + " — " + str(r["change_pct"]) + "% (30d)"
            )
        lines.append("")

    lines += [
        "## Scout Guidance",
        "- 🔴 Breakout keywords = validate with ExplodingTopics + Brave Search",
        "- 🟡 Rising keywords = cross-ref with X complaints",
        "- 🔵 Declining keywords = drop from consideration",
    ]

    OUTPUT_FILE.write_text("\n".join(lines))
    print("✅ Done — " + str(breakout_total) + " breakout keywords → " + OUTPUT_FILE.name)


if __name__ == "__main__":
    main()
