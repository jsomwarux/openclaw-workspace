#!/usr/bin/env python3
"""Recompute user-facing cron delivery rate without mutating cron config."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


WORKSPACE = Path("/Users/jtsomwaru/.openclaw/workspace")
JOBS_PATH = Path("/Users/jtsomwaru/.openclaw/cron/jobs.json")
RUNS_DIR = Path("/Users/jtsomwaru/.openclaw/cron/runs")


def load_jobs() -> list[dict]:
    data = json.loads(JOBS_PATH.read_text())
    jobs = data.get("jobs", data if isinstance(data, list) else [])
    if not isinstance(jobs, list):
        raise ValueError("jobs.json did not contain a jobs list")
    return jobs


def is_user_facing(job: dict) -> bool:
    delivery = job.get("delivery") or {}
    channel = str(delivery.get("channel", ""))
    target = str(delivery.get("to", ""))
    return delivery.get("mode") == "announce" and (
        channel == "telegram" or target.startswith("telegram:")
    )


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def was_delivered(row: dict) -> bool:
    if row.get("deliveryStatus") == "delivered":
        return True
    if row.get("delivered") is True:
        return True
    delivery = row.get("delivery") or {}
    return delivery.get("delivered") is True


def compute(days: int) -> tuple[int, int, list[dict]]:
    cutoff_ms = int(time.time() * 1000) - days * 24 * 60 * 60 * 1000
    total_runs = 0
    total_delivered = 0
    rows = []
    for job in load_jobs():
        if not is_user_facing(job):
            continue
        job_id = job.get("id")
        recent = [
            row
            for row in read_jsonl(RUNS_DIR / f"{job_id}.jsonl")
            if int(row.get("runAtMs") or row.get("ts") or 0) >= cutoff_ms
        ]
        delivered = sum(1 for row in recent if was_delivered(row))
        total_runs += len(recent)
        total_delivered += delivered
        rows.append(
            {
                "name": job.get("name", ""),
                "delivered": delivered,
                "runs": len(recent),
                "rate": delivered / len(recent) if recent else None,
            }
        )
    return total_runs, total_delivered, rows


def write_report(days: int, output: Path, label: str) -> dict:
    total_runs, total_delivered, rows = compute(days)
    rate = total_delivered / total_runs if total_runs else 0
    lines = [
        f"# Delivery Rate - {label}",
        "",
        "Scope: user-facing cron jobs with `delivery.mode=announce` and Telegram delivery configured.",
        f"Source: `{RUNS_DIR}` plus `{JOBS_PATH}`.",
        f"Window: last {days} days from script runtime.",
        "",
        f"Delivered runs: {total_delivered}",
        f"Scheduled/executed runs in records: {total_runs}",
        f"Delivery rate: {rate:.1%}",
        "",
        "| Job | Delivered | Runs | Rate |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in sorted(rows, key=lambda item: item["name"].lower()):
        row_rate = "n/a" if row["rate"] is None else f"{row['rate']:.1%}"
        lines.append(f"| {row['name']} | {row['delivered']} | {row['runs']} | {row_rate} |")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")
    return {
        "output": str(output),
        "days": days,
        "delivered": total_delivered,
        "runs": total_runs,
        "rate": round(rate, 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--label", default=time.strftime("%Y-%m-%d"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    output = args.output or WORKSPACE / "docs/audits" / f"delivery-rate-{args.label}.md"
    result = write_report(args.days, output, args.label)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"DELIVERY_RATE_REPORT {result['output']} rate={result['rate']:.1%}")


if __name__ == "__main__":
    main()
