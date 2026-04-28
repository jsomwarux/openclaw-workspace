#!/usr/bin/env python3
"""Generate Sports GM candidates/report/posts from comparable rank signals.

Do NOT compare raw trade values across sources. KTC/FantasyCalc/DynastyProcess
use different value scales. This script compares overall ranks and positional
ranks, then treats raw values as source-local metadata only.
"""
import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPORTS_DIR = ROOT / "memory" / "sports-gm"
SNAP_DIR = SPORTS_DIR / "market-snapshots"
REPORT_DIR = SPORTS_DIR / "reports"
CAND_DIR = SPORTS_DIR / "candidates"
POST_DIR = ROOT / "memory" / "content" / "bank"

PRIMARY_SOURCES = {"KeepTradeCut", "FantasyCalc", "FantasyPros"}
SECONDARY_SOURCES = {"DynastyProcess"}


def latest_snapshot():
    files = sorted(SNAP_DIR.glob("*.csv"))
    if not files:
        raise SystemExit("No market snapshot found. Run scripts/sports_gm_fetch_prices.py first.")
    return files[-1]


def num(x):
    try:
        if x in (None, ""):
            return None
        return float(x)
    except Exception:
        return None


def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def aggregate(rows):
    grouped = defaultdict(list)
    for r in rows:
        overall = num(r.get("overall_rank"))
        pos_rank = num(r.get("position_rank"))
        if overall is None and pos_rank is None:
            continue
        key = (r.get("format") or "", r.get("player") or "")
        grouped[key].append({**r, "overall_num": overall, "pos_num": pos_rank, "value_num": num(r.get("value"))})

    candidates = []
    for (fmt, player), vals in grouped.items():
        sources = {v["source"] for v in vals}
        primary_vals = [v for v in vals if v["source"] in PRIMARY_SOURCES]
        if len({v["source"] for v in primary_vals}) < 2:
            continue
        overall_nums = [v["overall_num"] for v in primary_vals if v["overall_num"] is not None]
        pos_nums = [v["pos_num"] for v in primary_vals if v["pos_num"] is not None]
        if len(overall_nums) < 2:
            continue
        overall_delta = max(overall_nums) - min(overall_nums)
        pos_delta = max(pos_nums) - min(pos_nums) if len(pos_nums) >= 2 else None
        best = min(overall_nums)
        worst = max(overall_nums)
        # Actionable assets only: avoid tail-only noise.
        if best > 260 and worst > 420:
            continue
        if overall_delta < 45 and (pos_delta is None or pos_delta < 10):
            continue
        pos = next((v.get("position") for v in vals if v.get("position")), "")
        team = next((v.get("team") for v in vals if v.get("team")), "")
        age = next((v.get("age") for v in vals if v.get("age")), "")
        rank_summary = ";".join(
            f"{v['source']} OVR={clean(v['overall_rank'])} POS={clean(v['position_rank'])} VAL={clean(v['value'])}"
            for v in sorted(vals, key=lambda x: (x["source"] not in PRIMARY_SOURCES, x["source"]))
        )
        candidates.append({
            "format": fmt,
            "player": player,
            "position": pos,
            "team": team,
            "age": age,
            "sources": ";".join(sorted(sources)),
            "rank_summary": rank_summary,
            "best_primary_overall_rank": int(best),
            "worst_primary_overall_rank": int(worst),
            "overall_rank_delta": round(overall_delta, 1),
            "position_rank_delta": round(pos_delta, 1) if pos_delta is not None else "",
            "candidate_type": classify(overall_delta, pos_delta),
        })
    return sorted(candidates, key=lambda c: (c["overall_rank_delta"], c["position_rank_delta"] or 0), reverse=True)


def clean(x):
    return "" if x in (None, "") else str(x)


def classify(overall_delta, pos_delta):
    if overall_delta >= 100 or (pos_delta is not None and pos_delta >= 25):
        return "major_rank_disagreement"
    if overall_delta >= 60 or (pos_delta is not None and pos_delta >= 15):
        return "rank_dislocation_watchlist"
    return "minor_rank_gap"


def write_candidates(candidates, date):
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    out = CAND_DIR / f"{date}.csv"
    fields = ["format", "player", "position", "team", "age", "sources", "rank_summary", "best_primary_overall_rank", "worst_primary_overall_rank", "overall_rank_delta", "position_rank_delta", "candidate_type"]
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(candidates)
    return out


def top_by_format(candidates, fmt, n=12):
    return [c for c in candidates if c["format"] == fmt and c["candidate_type"] != "minor_rank_gap"][:n]


def md_table(rows):
    if not rows:
        return "No major multi-source rank dislocations found.\n"
    lines = ["| Player | Pos | Team | Format | Rank Summary | OVR Δ | Pos Δ | Research Lane |", "|---|---|---|---|---|---:|---:|---|"]
    for c in rows:
        lane = "Rank disagreement only. Needs usage/context check before public call."
        lines.append(f"| {c['player']} | {c['position']} | {c['team']} | {c['format']} | {c['rank_summary']} | {c['overall_rank_delta']} | {c['position_rank_delta']} | {lane} |")
    return "\n".join(lines) + "\n"


def write_report(candidates, date, snapshot_path, candidate_path):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"weekly-gm-report-{date}.md"
    content = f"""# Weekly Dynasty GM Report — {date}

## Automation Status
Generated from market snapshot: `{snapshot_path}`
Candidate file: `{candidate_path}`

**Method fix:** raw values across KTC, FantasyCalc, FantasyPros, and DynastyProcess are not directly comparable. This report uses comparable overall/position rank deltas. Raw values are source-local metadata only.

Primary sources: KeepTradeCut, FantasyCalc, FantasyPros.
Secondary sanity check: DynastyProcess.

## Market Thesis
The exploitable layer is not raw value disagreement. It is **rank disagreement across trusted market/ranking sources**.

If KTC likes a player materially more than FantasyCalc/FantasyPros, that may mean sentiment is sticky. If FantasyPros is higher than the market tools, that may mean expert consensus sees role/talent that crowds are discounting. Either way, it is a research candidate, not a take.

## Superflex Rank Dislocation Watchlist
{md_table(top_by_format(candidates, "SF", 10))}
## 1QB Rank Dislocation Watchlist
{md_table(top_by_format(candidates, "1QB", 10))}
## What Happens Next
For the top 3-5 candidates, complete the player thesis standard:
- rank/value references from primary sources
- football/usage/context research
- thesis
- confidence
- risk case
- receipt row only if JT posts it publicly

## Content Hooks Generated
1. Raw trade values are source-specific. Ranks are where the comparison starts.
2. KTC is crowd sentiment. FantasyPros is expert consensus. FantasyCalc is trade behavior. The edge is knowing which one is lying today.
3. A rank gap is not a take. It is a work queue.
"""
    out.write_text(content)
    return out


def write_posts(date):
    week_dir = POST_DIR / date
    week_dir.mkdir(parents=True, exist_ok=True)
    out = week_dir / "dynasty-gm-automated-market-posts.md"
    out.write_text(f"""# Dynasty GM Automated Market Posts — {date}

## Correction
Do not compare raw trade values across sources. KTC, FantasyCalc, FantasyPros, and DynastyProcess use different scales.

## Standalone Posts

1. Raw trade values are source-specific.

Ranks are where the comparison starts.

2. KTC is crowd sentiment.
FantasyCalc is trade behavior.
FantasyPros is expert consensus.

The edge is knowing which one is lying today.

3. A rank gap is not a take.

It is a work queue.

4. Dynasty managers overpay when they treat every calculator like it is measuring the same thing.

5. The question is not “what is his value?”

The question is “which market is mispricing the role?”
""")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default=None)
    args = ap.parse_args()
    snapshot = Path(args.snapshot) if args.snapshot else latest_snapshot()
    date = snapshot.stem
    rows = load_rows(snapshot)
    candidates = aggregate(rows)
    candidate_path = write_candidates(candidates, date)
    report_path = write_report(candidates, date, snapshot, candidate_path)
    posts_path = write_posts(date)
    print(report_path)
    print(candidate_path)
    print(posts_path)
    print(f"candidates={len(candidates)}")

if __name__ == "__main__":
    main()
