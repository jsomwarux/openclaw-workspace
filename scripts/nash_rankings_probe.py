#!/usr/bin/env python3
"""Probe Nash Satoshi live rankings for morning-brief/content gates.

Safe read-only checker: fetches public leaderboard JSON and verifies that live
rank/scores are available and recent enough to use for content drafting.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DEFAULT_URL = "https://nashsatoshi.com/api/leaderboard"


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def fetch_json(url: str, timeout: int) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "OpenClaw Nash rankings probe/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        return json.loads(raw.decode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--max-age-hours", type=float, default=96)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    sep = "&" if "?" in args.url else "?"
    url = f"{args.url}{sep}{urllib.parse.urlencode({'limit': args.limit})}"
    try:
        data = fetch_json(url, args.timeout)
    except Exception as exc:
        result = {"ok": False, "reason": f"fetch_failed: {exc}", "url": url}
        print(json.dumps(result, indent=2) if args.json else f"NASH_RANKINGS_UNAVAILABLE fetch_failed: {exc}")
        return 2

    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        result = {"ok": False, "reason": "no_items", "url": url}
        print(json.dumps(result, indent=2) if args.json else "NASH_RANKINGS_UNAVAILABLE no_items")
        return 2

    valid = []
    newest = None
    for idx, item in enumerate(items, start=1):
        score = item.get("latestScore") or item.get("score7d") or item.get("score30d")
        symbol = item.get("tokenSymbol") or item.get("symbol")
        rank = item.get("overallRank") or idx
        if symbol and isinstance(score, (int, float)) and rank:
            dt = parse_dt(item.get("latestAnalysisDate"))
            if dt and (newest is None or dt > newest):
                newest = dt
            valid.append(
                {
                    "rank": rank,
                    "symbol": symbol,
                    "score": float(score),
                    "trend": item.get("scoreTrend"),
                    "narrative": item.get("latestPrimaryNarrative") or item.get("latestNarrative"),
                    "analysisDate": item.get("latestAnalysisDate"),
                }
            )

    if not valid:
        result = {"ok": False, "reason": "no_rank_scores", "url": url, "itemCount": len(items)}
        print(json.dumps(result, indent=2) if args.json else "NASH_RANKINGS_UNAVAILABLE no_rank_scores")
        return 2

    age_hours = None
    if newest:
        age_hours = (datetime.now(timezone.utc) - newest).total_seconds() / 3600
        if age_hours > args.max_age_hours:
            result = {
                "ok": False,
                "reason": "stale_rankings",
                "ageHours": round(age_hours, 2),
                "newestAnalysisDate": newest.isoformat(),
                "top": valid[:5],
                "url": url,
            }
            print(json.dumps(result, indent=2) if args.json else f"NASH_RANKINGS_STALE age_hours={age_hours:.1f}")
            return 2

    result = {
        "ok": True,
        "url": url,
        "validCount": len(valid),
        "newestAnalysisDate": newest.isoformat() if newest else None,
        "ageHours": round(age_hours, 2) if age_hours is not None else None,
        "top": valid[: args.limit],
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        top = ", ".join(f"#{x['rank']} {x['symbol']} {x['score']:.2f}" for x in valid[:5])
        print(f"NASH_RANKINGS_OK valid={len(valid)} age_hours={result['ageHours']} top={top}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
