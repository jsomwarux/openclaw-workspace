#!/usr/bin/env python3
import json
import os
import tempfile
import time
from pathlib import Path


WORKSPACE = Path("/Users/jtsomwaru/.openclaw/workspace")
JOBS_PATH = Path("/Users/jtsomwaru/.openclaw/cron/jobs.json")
RUNS_DIR = Path("/Users/jtsomwaru/.openclaw/cron/runs")
ARCHIVE_PATH = WORKSPACE / "docs/audits/removed-jobs-2026-06-11.json"
BASELINE_PATH = WORKSPACE / "docs/audits/baseline-delivery-2026-06-11.md"


REMOVE_EXACT = {
    "Review Stalled Projects/Outreach",
    "Reminder: Reevaluate Codex harness config",
    "Altmark rent delinquency tracker follow-up check",
    "reddit-daily-gen-rerun-check-2026-05-24",
}


def is_20260428_catchup(job):
    schedule = job.get("schedule") or {}
    return (
        str(job.get("name", "")).startswith("Catch-up: ")
        and schedule.get("kind") == "at"
        and str(schedule.get("at", "")).startswith("2026-04-28")
    )


def should_remove(job):
    name = job.get("name", "")
    if is_20260428_catchup(job):
        return True
    if name in REMOVE_EXACT:
        return True
    return name.startswith("content-generate (DISABLED")


def is_user_facing(job):
    delivery = job.get("delivery") or {}
    channel = str(delivery.get("channel", ""))
    target = str(delivery.get("to", ""))
    return delivery.get("mode") == "announce" and (
        channel == "telegram" or target.startswith("telegram:")
    )


def read_jsonl(path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def delivered(row):
    if row.get("deliveryStatus") == "delivered":
        return True
    if row.get("delivered") is True:
        return True
    delivery = row.get("delivery") or {}
    return delivery.get("delivered") is True


def baseline(jobs):
    now_ms = int(time.time() * 1000)
    cutoff_ms = now_ms - 7 * 24 * 60 * 60 * 1000
    rows = []
    total_runs = 0
    total_delivered = 0
    for job in jobs:
        if not is_user_facing(job):
            continue
        job_id = job.get("id")
        run_rows = read_jsonl(RUNS_DIR / f"{job_id}.jsonl")
        recent = [
            r for r in run_rows
            if int(r.get("runAtMs") or r.get("ts") or 0) >= cutoff_ms
        ]
        delivered_count = sum(1 for r in recent if delivered(r))
        total_runs += len(recent)
        total_delivered += delivered_count
        rows.append({
            "id": job_id,
            "name": job.get("name", ""),
            "runs": len(recent),
            "delivered": delivered_count,
            "rate": delivered_count / len(recent) if recent else None,
        })
    return total_runs, total_delivered, rows


def write_baseline(jobs):
    total_runs, total_delivered, rows = baseline(jobs)
    rate = total_delivered / total_runs if total_runs else 0
    lines = [
        "# Baseline Delivery - 2026-06-11",
        "",
        "Scope: user-facing cron jobs with `delivery.mode=announce` and Telegram delivery configured.",
        "Source: cron run JSONL records under `/Users/jtsomwaru/.openclaw/cron/runs/`; `jobs.json` contains job definitions but no embedded run records.",
        "Window: last 7 days from script runtime.",
        "",
        f"Delivered runs: {total_delivered}",
        f"Scheduled/executed runs in records: {total_runs}",
        f"Delivery rate: {rate:.1%}",
        "",
        "| Job | Delivered | Runs | Rate |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in sorted(rows, key=lambda r: r["name"].lower()):
        row_rate = "n/a" if row["rate"] is None else f"{row['rate']:.1%}"
        lines.append(f"| {row['name']} | {row['delivered']} | {row['runs']} | {row_rate} |")
    BASELINE_PATH.write_text("\n".join(lines) + "\n")
    return {
        "total_runs": total_runs,
        "total_delivered": total_delivered,
        "rate": rate,
        "user_facing_jobs": len(rows),
    }


def atomic_write_json(path, data):
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    with os.fdopen(fd, "w") as tmp:
        tmp.write(text)
    os.replace(tmp_name, path)


def main():
    data = json.loads(JOBS_PATH.read_text())
    jobs = data["jobs"]
    before_count = len(jobs)
    before_enabled = sum(1 for j in jobs if j.get("enabled", True))
    baseline_result = write_baseline(jobs)

    removed = [job for job in jobs if should_remove(job)]
    kept = [job for job in jobs if not should_remove(job)]

    disabled = []
    moved = []
    for job in kept:
        name = job.get("name", "")
        if name in {"Passive Income Scout", "Passive Income Strategist", "Health Check-in Prompt"}:
            if job.get("enabled", True):
                disabled.append(name)
            job["enabled"] = False
        if name == "Weekly Strategic Gut-Check":
            schedule = job.setdefault("schedule", {})
            if schedule.get("expr") != "30 18 * * 0":
                moved.append({
                    "name": name,
                    "from": schedule.get("expr"),
                    "to": "30 18 * * 0",
                })
            schedule["kind"] = "cron"
            schedule["expr"] = "30 18 * * 0"
            schedule["tz"] = "America/New_York"

    archive = {
        "removed_at": "2026-06-11",
        "source": str(JOBS_PATH),
        "removed_count": len(removed),
        "jobs": removed,
    }
    ARCHIVE_PATH.write_text(json.dumps(archive, indent=2, ensure_ascii=False) + "\n")

    data["jobs"] = kept
    atomic_write_json(JOBS_PATH, data)

    after_count = len(kept)
    after_enabled = sum(1 for j in kept if j.get("enabled", True))
    result = {
        "before_count": before_count,
        "after_count": after_count,
        "before_enabled": before_enabled,
        "after_enabled": after_enabled,
        "removed": [j.get("name") for j in removed],
        "disabled_or_confirmed_disabled": [
            "Passive Income Scout",
            "Passive Income Strategist",
            "Health Check-in Prompt",
        ],
        "moved": moved,
        "archive_path": str(ARCHIVE_PATH),
        "baseline_path": str(BASELINE_PATH),
        "baseline": baseline_result,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
