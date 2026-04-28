#!/usr/bin/env python3
"""Fetch dynasty market snapshots for the Sports GM desk.

Sources:
- KeepTradeCut dynasty rankings HTML embedded playersArray
- FantasyCalc public API /values/current
- FantasyPros consensus dynasty rankings embedded ecrData
- DynastyProcess open data values.csv (secondary sanity check; values not directly comparable)

Important: value scales are source-specific. Downstream analysis should compare ranks,
position ranks, percentiles, and source deltas rather than raw values across sources.
"""
import argparse
import csv
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "memory" / "sports-gm" / "market-snapshots"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/json,text/plain,*/*"})
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        cp = subprocess.run(["curl", "-L", "-s", "-A", UA, url], text=True, capture_output=True, timeout=45)
        if cp.returncode != 0 or not cp.stdout:
            raise RuntimeError(f"curl fallback failed for {url}: {cp.stderr[:200]}") from e
        return cp.stdout


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json", "Origin": "https://www.fantasycalc.com", "Referer": "https://www.fantasycalc.com/"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def ktc_rows(today: str):
    html = fetch_text("https://keeptradecut.com/dynasty-rankings")
    m = re.search(r"var playersArray\s*=\s*(\[.*?\]);", html, re.S)
    if not m:
        raise RuntimeError("Could not find KTC playersArray")
    players = json.loads(m.group(1))
    rows = []
    for p in players:
        for fmt, key in [("1QB", "oneQBValues"), ("SF", "superflexValues")]:
            v = p.get(key) or {}
            rows.append({
                "snapshot_date": today,
                "source": "KeepTradeCut",
                "format": fmt,
                "player": p.get("playerName"),
                "position": p.get("position"),
                "team": p.get("team"),
                "age": p.get("age"),
                "value": v.get("value"),
                "overall_rank": v.get("rank"),
                "position_rank": v.get("positionalRank"),
                "trend": v.get("overallTrend"),
                "url": "https://keeptradecut.com/dynasty-rankings",
            })
    return rows


def fantasycalc_rows(today: str):
    rows = []
    for fmt, num_qbs in [("1QB", 1), ("SF", 2)]:
        data = fetch_json(f"https://api.fantasycalc.com/values/current?isDynasty=true&numQbs={num_qbs}")
        pos_counts = {}
        for i, item in enumerate(data, start=1):
            p = item.get("player") or {}
            pos = p.get("position") or ""
            pos_counts[pos] = pos_counts.get(pos, 0) + 1
            rows.append({
                "snapshot_date": today,
                "source": "FantasyCalc",
                "format": fmt,
                "player": p.get("name"),
                "position": pos,
                "team": p.get("team") or "",
                "age": "",
                "value": item.get("value"),
                "overall_rank": i,
                "position_rank": pos_counts[pos],
                "trend": "",
                "url": f"https://api.fantasycalc.com/values/current?isDynasty=true&numQbs={num_qbs}",
            })
    return rows


def fantasypros_rows(today: str):
    html = fetch_text("https://www.fantasypros.com/nfl/rankings/dynasty-overall.php")
    m = re.search(r"var ecrData = (.*?);\n", html, re.S)
    if not m:
        raise RuntimeError("Could not find FantasyPros ecrData")
    payload = json.loads(m.group(1))
    data = payload.get("players", [])
    rows = []
    for r in data:
        pos_rank = r.get("pos_rank") or ""
        pos_rank_num = re.sub(r"^[A-Z]+", "", str(pos_rank))
        rows.append({
            "snapshot_date": today,
            "source": "FantasyPros",
            "format": "1QB",
            "player": r.get("player_name"),
            "position": r.get("player_position_id"),
            "team": r.get("player_team_id"),
            "age": r.get("player_age") or "",
            "value": "",
            "overall_rank": r.get("rank_ecr"),
            "position_rank": pos_rank_num,
            "trend": r.get("player_ecr_delta") or "",
            "url": "https://www.fantasypros.com/nfl/rankings/dynasty-overall.php",
        })
    return rows


def dynastyprocess_rows(today: str):
    text = fetch_text("https://raw.githubusercontent.com/dynastyprocess/data/master/files/values.csv")
    reader = csv.DictReader(text.splitlines())
    rows = []
    for r in reader:
        for fmt, col in [("1QB", "value_1qb"), ("SF", "value_2qb")]:
            rows.append({
                "snapshot_date": today,
                "source": "DynastyProcess",
                "format": fmt,
                "player": r.get("player"),
                "position": r.get("pos"),
                "team": r.get("team"),
                "age": r.get("age"),
                "value": r.get(col),
                "overall_rank": r.get("ecr_1qb" if fmt == "1QB" else "ecr_2qb"),
                "position_rank": r.get("ecr_pos"),
                "trend": "",
                "url": "https://raw.githubusercontent.com/dynastyprocess/data/master/files/values.csv",
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="Output CSV path")
    ap.add_argument("--players", nargs="*", help="Optional player name filters")
    args = ap.parse_args()

    today = dt.datetime.now().strftime("%Y-%m-%d")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else OUT_DIR / f"{today}.csv"

    all_rows = []
    for name, fn in [("KeepTradeCut", ktc_rows), ("FantasyCalc", fantasycalc_rows), ("FantasyPros", fantasypros_rows), ("DynastyProcess", dynastyprocess_rows)]:
        try:
            rows = fn(today)
            print(f"{name}: {len(rows)} rows", file=sys.stderr)
            all_rows.extend(rows)
        except Exception as e:
            print(f"WARN {name}: {e}", file=sys.stderr)

    if args.players:
        needles = [p.lower() for p in args.players]
        all_rows = [r for r in all_rows if r.get("player") and any(n in r["player"].lower() for n in needles)]

    fields = ["snapshot_date", "source", "format", "player", "position", "team", "age", "value", "overall_rank", "position_rank", "trend", "url"]
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(all_rows)
    print(out)


if __name__ == "__main__":
    main()
