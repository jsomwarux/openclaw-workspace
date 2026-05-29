#!/usr/bin/env python3
"""Check Mission Control for stale or urgent active job applications."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from typing import Any


MISSION_CONTROL_URL = "http://localhost:3000/api/tasks"

APPLICATION_TITLE_RE = re.compile(
    r"^(apply:|apply to |review \+ submit:|dual-track )", re.IGNORECASE
)
SKIP_TITLE_RE = re.compile(
    r"^(build idea:|consulting lead from job post|verify job signal)", re.IGNORECASE
)
DEPRIORITIZED_RE = re.compile(
    r"\b(deprioriti[sz]ed|demoted|archived|no deadline|do not apply|passed on)\b",
    re.IGNORECASE,
)
DEADLINE_RE = re.compile(
    r"\b(deadline|due|apply by)\b[^.\n]*(\d{4}-\d{2}-\d{2}|[A-Z][a-z]+ \d{1,2})",
    re.IGNORECASE,
)
DRIVE_RE = re.compile(r"https://(?:docs|drive)\.google\.com/\S+")
URL_RE = re.compile(r"https?://\S+")


def task_created_at(task: dict[str, Any]) -> dt.datetime | None:
    value = task.get("createdAt") or task.get("_creationTime")
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number > 10_000_000_000:
        number /= 1000
    return dt.datetime.fromtimestamp(number, tz=dt.timezone.utc)


def parse_tasks(raw: bytes) -> list[dict[str, Any]]:
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("tasks", data.get("data", []))
    if not isinstance(data, list):
        raise ValueError("Mission Control response did not contain a task list")
    return [task for task in data if isinstance(task, dict)]


def is_open_application(task: dict[str, Any]) -> bool:
    title = task.get("title") or ""
    status = (task.get("status") or "").lower()
    if status in {"done", "completed", "cancelled", "canceled", "archived"}:
        return False
    if SKIP_TITLE_RE.search(title):
        return False
    return bool(APPLICATION_TITLE_RE.search(title))


def deadline_hint(description: str) -> str | None:
    match = DEADLINE_RE.search(description)
    if not match:
        return None
    return match.group(0).strip()


def link_for(description: str, label: str) -> str | None:
    lines = description.splitlines()
    for line in lines:
        if label.lower() in line.lower():
            match = URL_RE.search(line)
            if match:
                return match.group(0).rstrip(").,")
    if label == "Drive":
        match = DRIVE_RE.search(description)
        if match:
            return match.group(0).rstrip(").,")
    return None


def build_report(tasks: list[dict[str, Any]], now: dt.datetime) -> dict[str, Any]:
    apps = [task for task in tasks if is_open_application(task)]
    flagged: list[dict[str, Any]] = []
    for task in apps:
        description = task.get("description") or ""
        created = task_created_at(task)
        age_days = (now - created).days if created else None
        deadline = deadline_hint(description)
        stale = age_days is not None and age_days > 3 and not DEPRIORITIZED_RE.search(description)
        urgent = bool(deadline)
        if not (stale or urgent):
            continue
        flagged.append(
            {
                "id": task.get("_id") or task.get("id"),
                "title": task.get("title"),
                "age_days": age_days,
                "issue": "urgent deadline" if urgent else f"stale {age_days} days",
                "deadline": deadline,
                "resume": link_for(description, "Resume"),
                "cover_letter": link_for(description, "Cover"),
                "apply": link_for(description, "Apply"),
                "drive": link_for(description, "Drive"),
            }
        )

    alert_lines: list[str] = []
    if flagged:
        alert_lines.append(f"Job Application Check - {now.date().isoformat()}")
        alert_lines.append("")
        for item in flagged[:8]:
            alert_lines.append(f"- {item['title']} - {item['issue']}")
            if item.get("resume"):
                alert_lines.append(f"  Resume: {item['resume']}")
            if item.get("cover_letter"):
                alert_lines.append(f"  Cover Letter: {item['cover_letter']}")
            if item.get("apply"):
                alert_lines.append(f"  Apply: {item['apply']}")
        if len(flagged) > 8:
            alert_lines.append(f"- Plus {len(flagged) - 8} more flagged applications.")

    return {
        "ok": True,
        "active_applications": len(apps),
        "flagged_count": len(flagged),
        "flagged": flagged,
        "alert_text": "\n".join(alert_lines),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print machine-readable report")
    args = parser.parse_args()

    try:
        raw = urllib.request.urlopen(MISSION_CONTROL_URL, timeout=20).read()
        report = build_report(parse_tasks(raw), dt.datetime.now(tz=dt.timezone.utc))
    except Exception as exc:  # noqa: BLE001 - cron should see a clear failure.
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    elif report["alert_text"]:
        print(report["alert_text"])
    else:
        print("No stale or urgent active applications.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
