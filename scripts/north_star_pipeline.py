#!/usr/bin/env python3
"""Deterministic North Star pipeline utilities.

This keeps the scoreboard and Send Queue grounded in local JSONL instead of
asking a cron prompt to infer pipeline math from scattered notes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
PIPELINE_PATH = WORKSPACE / "memory" / "pipeline.jsonl"
SCOREBOARD_PATH = WORKSPACE / "memory" / "north-star.md"
SEND_QUEUE_PATH = WORKSPACE / "memory" / "send-queue.md"

TARGETS = (10000, 30000, 100000)
CURRENT_COLLECTED = 5575


def load_records(path: Path = PIPELINE_PATH) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        records.append(record)
    return records


def write_records(records: list[dict[str, Any]], path: Path = PIPELINE_PATH) -> None:
    text = "\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n"
    path.write_text(text, encoding="utf-8")


def weighted_forecast(records: list[dict[str, Any]]) -> float:
    total = 0.0
    for record in records:
        if record.get("stage") in {"closed", "paid"}:
            continue
        value = float(record.get("value", 0) or 0)
        weight = float(record.get("weight", 0) or 0)
        total += value * weight / 100
    return total


def aging_items(records: list[dict[str, Any]], today: date) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for record in records:
        if record.get("waiting_on") not in {"client", "prospect", "jt"}:
            continue
        if record.get("stage") in {"closed", "paid"}:
            continue
        name = str(record.get("name", "")).lower()
        next_action = str(record.get("next_action", "")).lower()
        if "rent delinquency" not in name and (
            next_action.startswith("keep ready")
            or next_action.startswith("do not")
            or next_action.startswith("blocked until")
            or next_action.startswith("only revive")
        ):
            continue
        last_touch = str(record.get("last_touch", ""))
        try:
            touched = date.fromisoformat(last_touch)
        except ValueError:
            continue
        age_days = (today - touched).days
        if "rent delinquency" in name or record.get("waiting_on") == "jt" or age_days >= 7:
            item = dict(record)
            item["age_days"] = age_days
            items.append(item)
    return sorted(
        items,
        key=lambda r: (
            "rent delinquency" not in str(r.get("name", "")).lower(),
            r.get("waiting_on") != "client",
            -int(r.get("value", 0) or 0),
        ),
    )


def summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    forecast = weighted_forecast(records)
    return {
        "targets": TARGETS,
        "current_collected": CURRENT_COLLECTED,
        "weighted_forecast": round(forecast, 2),
        "gap_to_10k_collected": max(0, TARGETS[0] - CURRENT_COLLECTED),
        "gap_to_10k_with_forecast": max(0, round(TARGETS[0] - CURRENT_COLLECTED - forecast, 2)),
        "records": len(records),
        "aging_items": len(aging_items(records, date.today())),
    }


def print_summary(records: list[dict[str, Any]], as_json: bool) -> None:
    payload = summary(records)
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(f"Current collected: ${payload['current_collected']:,.0f}")
    print(f"Pipeline weighted forecast: ${payload['weighted_forecast']:,.0f}")
    print(f"Gap to $10K collected: ${payload['gap_to_10k_collected']:,.0f}")
    print(f"Gap to $10K with forecast: ${payload['gap_to_10k_with_forecast']:,.0f}")
    print(f"Pipeline records: {payload['records']}")
    print(f"Aging send-queue candidates: {payload['aging_items']}")


def build_queue(records: list[dict[str, Any]], limit: int) -> str:
    items = aging_items(records, date.today())[:limit]
    lines = [
        f"# Send Queue - Generated {date.today().isoformat()}",
        "",
        "Generated from `memory/pipeline.jsonl`. JT sends; Eve never sends outreach.",
        "",
    ]
    for idx, record in enumerate(items, start=1):
        keyword = "send"
        lines.append(f"{idx}. {keyword} - {record['name']}")
        lines.append(f"   Source: `{record.get('source', 'unknown')}`")
        lines.append(f"   Next action: {record.get('next_action', '')}")
        lines.append(f"   Waiting on: {record.get('waiting_on')} | age: {record.get('age_days')} days")
        lines.append("")
    if not items:
        lines.append("No aging pipeline send items.")
    return "\n".join(lines).rstrip() + "\n"


ASSIGNMENT_RE = re.compile(r"(\w+)=('([^']*)'|\"([^\"]*)\"|([^\s]+))")


def apply_update(text: str) -> dict[str, Any]:
    if not text.lower().startswith("pipeline:"):
        raise SystemExit("Update must start with 'pipeline:'")
    body = text.split(":", 1)[1].strip()
    match = re.match(r"(.+?)(?:\s+\w+=|$)", body)
    if not match:
        raise SystemExit("Missing pipeline record name")
    raw_name = match.group(1).strip()
    assignments = {
        m.group(1): next(group for group in m.groups()[2:] if group is not None)
        for m in ASSIGNMENT_RE.finditer(body)
    }
    records = load_records()
    matches = [record for record in records if raw_name.lower() in str(record.get("name", "")).lower()]
    if len(matches) != 1:
        raise SystemExit(f"Expected one record match for {raw_name!r}, found {len(matches)}")
    record = matches[0]
    for key in ("stage", "waiting_on", "next_action", "source"):
        if key in assignments:
            record[key] = assignments[key]
    if "value" in assignments:
        record["value"] = float(assignments["value"])
    if "weight" in assignments:
        record["weight"] = float(assignments["weight"])
    record["last_touch"] = assignments.get("last_touch", date.today().isoformat())
    write_records(records)
    return {"updated": record["name"], "record": record, "summary": summary(records)}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("summary")
    s.add_argument("--json", action="store_true")
    q = sub.add_parser("queue")
    q.add_argument("--limit", type=int, default=4)
    q.add_argument("--write", action="store_true")
    u = sub.add_parser("update")
    u.add_argument("text")
    args = parser.parse_args()

    records = load_records()
    if args.cmd == "summary":
        print_summary(records, args.json)
    elif args.cmd == "queue":
        text = build_queue(records, args.limit)
        if args.write:
            SEND_QUEUE_PATH.write_text(text, encoding="utf-8")
            print(SEND_QUEUE_PATH)
        else:
            print(text, end="")
    elif args.cmd == "update":
        print(json.dumps(apply_update(args.text), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
