#!/usr/bin/env python3
"""Cron posture report for OpenClaw operations.

Produces daily invocation estimate, schedule clusters, delivery/failure-alert posture,
and empty-message guard risk. Read-only except for writing the report markdown/json.
"""
from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path.home() / ".openclaw" / "workspace"
OUT_DIR = ROOT / "reports" / "cron-posture"
NY = ZoneInfo("America/New_York")


def cron_runs_per_week(expr: str) -> float | None:
    # Conservative simple parser for common 5-field schedules.
    # Handles day-of-month monthly jobs without overstating them as daily.
    parts = expr.split()
    if len(parts) != 5:
        return None
    minute, hour, dom, month, dow = parts
    if minute == "*" or hour == "*":
        return None
    hours = hour.split(",") if "," in hour else [hour]
    runs_per_fire_day = len(hours)
    if dom != "*" and dow == "*":
        # Monthly day-of-month job. Average month = 4.345 weeks.
        return round(runs_per_fire_day / 4.345, 2)
    if dow == "*":
        days = 7
    elif "," in dow:
        days = len(dow.split(","))
    elif "-" in dow:
        a, b = dow.split("-", 1)
        try:
            days = int(b) - int(a) + 1
        except Exception:
            days = 7
    else:
        days = 1
    return runs_per_fire_day * days


def main() -> int:
    raw = subprocess.check_output(["openclaw", "cron", "list", "--json"], text=True)
    data = json.loads(raw)
    jobs = data.get("jobs", [])
    enabled = [j for j in jobs if j.get("enabled")]
    total_weekly = 0
    unknown = []
    clusters = defaultdict(list)
    missing_alerts = []
    announce_no_guard = []
    delete_after = []
    rows = []
    for j in enabled:
        sched = j.get("schedule") or {}
        expr = sched.get("expr") if sched.get("kind") == "cron" else None
        weekly = cron_runs_per_week(expr or "") if expr else None
        if weekly is None:
            unknown.append(j.get("name") or j.get("id"))
            weekly = 0
        total_weekly += weekly
        if expr:
            parts = expr.split()
            if len(parts) >= 2:
                clusters[f"{parts[1]}:{parts[0]} {sched.get('tz','')}"] .append(j.get("name") or j.get("id"))
        if not j.get("failureAlert"):
            # Only warn; some no-op/local jobs may be intentionally quiet.
            missing_alerts.append(j.get("name") or j.get("id"))
        if j.get("deleteAfterRun"):
            delete_after.append(j.get("name") or j.get("id"))
        delivery = j.get("delivery") or {}
        msg = ((j.get("payload") or {}).get("message") or "").lower()
        if delivery.get("mode") == "announce" and "skip the telegram send" not in msg and "if no new" not in msg and "empty" not in msg:
            announce_no_guard.append(j.get("name") or j.get("id"))
        rows.append({"id": j.get("id"), "name": j.get("name"), "expr": expr, "weekly_estimate": weekly, "failure_alert": bool(j.get("failureAlert")), "delivery": delivery.get("mode")})
    avg_daily = round(total_weekly / 7, 2)
    dense_clusters = {k: v for k, v in clusters.items() if len(v) > 1}
    result = {
        "generated_at": datetime.now(NY).isoformat(),
        "enabled_jobs": len(enabled),
        "estimated_weekly_invocations": total_weekly,
        "estimated_daily_average": avg_daily,
        "unknown_schedule_estimates": unknown,
        "dense_clusters": dense_clusters,
        "missing_failure_alerts": missing_alerts,
        "delete_after_run": delete_after,
        "announce_jobs_without_empty_guard_hint": announce_no_guard,
        "rows": rows,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now(NY).strftime("%Y-%m-%d")
    (OUT_DIR / f"{date}.json").write_text(json.dumps(result, indent=2))
    md = [f"# Cron Posture Report — {date}", "", f"- Enabled jobs: {len(enabled)}", f"- Estimated weekly invocations: {total_weekly}", f"- Estimated daily average: {avg_daily}", f"- Unknown schedule estimates: {len(unknown)}", f"- Dense schedule clusters: {len(dense_clusters)}", f"- Missing failure alerts: {len(missing_alerts)}", f"- deleteAfterRun=true: {len(delete_after)}", f"- Announce jobs without empty-output guard hint: {len(announce_no_guard)}", ""]
    if dense_clusters:
        md.append("## Dense clusters")
        for k, v in sorted(dense_clusters.items()):
            md.append(f"- {k}: {', '.join(v)}")
    if missing_alerts:
        md.append("\n## Missing failure alerts")
        for name in missing_alerts:
            md.append(f"- {name}")
    if announce_no_guard:
        md.append("\n## Announce jobs without explicit empty-output guard")
        for name in announce_no_guard:
            md.append(f"- {name}")
    (OUT_DIR / f"{date}.md").write_text("\n".join(md) + "\n")
    print(json.dumps({k: result[k] for k in ["enabled_jobs", "estimated_weekly_invocations", "estimated_daily_average", "dense_clusters", "missing_failure_alerts", "delete_after_run"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
