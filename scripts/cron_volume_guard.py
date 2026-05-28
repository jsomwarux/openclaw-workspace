#!/usr/bin/env python3
"""Audit OpenClaw cron volume against the current operating guardrail."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from typing import Any


MAX_AVG_DAILY = 35.0
MAX_AGENT_TURN_AVG_DAILY = 28.0
WARN_AVG_DAILY = 30.0
MAX_UNKNOWN_ENABLED = 1


@dataclass(frozen=True)
class JobCount:
    job: dict[str, Any]
    weekly: float | None


def cron_weekly_count(expr: str) -> float | None:
    parts = expr.split()
    if len(parts) != 5:
        return None
    minute, hour, dom, month, dow = parts
    if month != "*":
        return None

    def count_field(value: str, maximum: int) -> int | None:
        if value == "*":
            return maximum
        total = 0
        for part in value.split(","):
            if "/" in part:
                return None
            if "-" in part:
                start, end = part.split("-", 1)
                try:
                    total += int(end) - int(start) + 1
                except ValueError:
                    return None
            else:
                try:
                    int(part)
                except ValueError:
                    # Named weekdays/months are intentionally counted in dow only.
                    return None
                total += 1
        return total

    hour_count = count_field(hour, 24)
    minute_count = count_field(minute, 60)
    if hour_count is None or minute_count is None:
        return None
    per_day = hour_count * minute_count

    if dom != "*":
        # Monthly day-of-month schedules average to roughly once per month.
        return per_day * 12 / 52
    if dow == "*":
        day_count = 7
    else:
        names = {
            "SUN": 0,
            "MON": 1,
            "TUE": 2,
            "WED": 3,
            "THU": 4,
            "FRI": 5,
            "SAT": 6,
        }
        normalized = []
        for part in dow.upper().split(","):
            normalized.append(str(names.get(part, part)))
        day_count = count_field(",".join(normalized), 7)
        if day_count is None:
            return None
    return per_day * day_count


def every_weekly_count(schedule: dict[str, Any]) -> float | None:
    every_ms = schedule.get("everyMs")
    if not every_ms:
        return None
    return round(7 * 24 * 60 * 60 * 1000 / every_ms)


def estimate_weekly(job: dict[str, Any]) -> float | None:
    schedule = job.get("schedule") or {}
    kind = schedule.get("kind")
    if kind == "cron":
        expr = schedule.get("expr")
        return cron_weekly_count(expr) if isinstance(expr, str) else None
    if kind == "every":
        return every_weekly_count(schedule)
    return None


def load_jobs() -> list[dict[str, Any]]:
    proc = subprocess.run(
        ["openclaw", "cron", "list", "--all", "--json"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    data = json.loads(proc.stdout)
    jobs = data.get("jobs", data if isinstance(data, list) else [])
    return [j for j in jobs if isinstance(j, dict)]


def main() -> int:
    jobs = load_jobs()
    enabled = [j for j in jobs if j.get("enabled")]
    counted = [JobCount(j, estimate_weekly(j)) for j in enabled]
    unknown = [jc for jc in counted if jc.weekly is None]
    weekly_total = sum(jc.weekly or 0 for jc in counted)
    agent_weekly = sum(
        jc.weekly or 0
        for jc in counted
        if (jc.job.get("payload") or {}).get("kind") == "agentTurn"
    )

    top = sorted(
        (jc for jc in counted if jc.weekly is not None),
        key=lambda jc: jc.weekly or 0,
        reverse=True,
    )[:15]
    schedule_collisions = Counter()
    for jc in counted:
        schedule = jc.job.get("schedule") or {}
        if schedule.get("kind") == "cron":
            schedule_collisions[(schedule.get("expr"), schedule.get("tz"))] += 1

    result = {
        "ok": True,
        "enabled_jobs": len(enabled),
        "estimated_weekly_invocations": weekly_total,
        "estimated_daily_average": round(weekly_total / 7, 2),
        "estimated_agent_turn_daily_average": round(agent_weekly / 7, 2),
        "unknown_enabled_schedules": len(unknown),
        "thresholds": {
            "max_avg_daily": MAX_AVG_DAILY,
            "max_agent_turn_avg_daily": MAX_AGENT_TURN_AVG_DAILY,
            "warn_avg_daily": WARN_AVG_DAILY,
            "max_unknown_enabled": MAX_UNKNOWN_ENABLED,
        },
        "warnings": [],
        "top_jobs": [
            {
                "weekly": round(jc.weekly or 0, 2),
                "daily_average": round((jc.weekly or 0) / 7, 2),
                "id": jc.job.get("id"),
                "name": jc.job.get("name"),
                "schedule": jc.job.get("schedule"),
                "payload_kind": (jc.job.get("payload") or {}).get("kind"),
            }
            for jc in top
        ],
        "same_schedule_collisions": [
            {"expr": expr, "tz": tz, "count": count}
            for (expr, tz), count in schedule_collisions.items()
            if count > 1
        ],
        "unknown_jobs": [
            {"id": jc.job.get("id"), "name": jc.job.get("name"), "schedule": jc.job.get("schedule")}
            for jc in unknown
        ],
    }

    if result["estimated_daily_average"] > MAX_AVG_DAILY:
        result["ok"] = False
        result["warnings"].append("scheduled_daily_average_over_cap")
    elif result["estimated_daily_average"] > WARN_AVG_DAILY:
        result["warnings"].append("scheduled_daily_average_near_cap")
    if result["estimated_agent_turn_daily_average"] > MAX_AGENT_TURN_AVG_DAILY:
        result["ok"] = False
        result["warnings"].append("agent_turn_daily_average_over_cap")
    if len(unknown) > MAX_UNKNOWN_ENABLED:
        result["ok"] = False
        result["warnings"].append("too_many_unknown_enabled_schedules")

    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
