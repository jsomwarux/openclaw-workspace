#!/usr/bin/env python3
"""Deduped Mission Control task gate for research crons.

This gives agent prompts a script-file path for task checks/creation so they do
not use inline Python or heredocs after fetching Mission Control JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any


MC_URL = "http://localhost:3000/api/tasks"
CLOSED_STATUSES = {"done", "completed", "archived", "cancelled", "canceled"}


def fetch_tasks() -> list[dict[str, Any]]:
    with urllib.request.urlopen(MC_URL, timeout=15) as resp:
        payload = json.load(resp)
    tasks = payload.get("tasks", payload) if isinstance(payload, dict) else payload
    if not isinstance(tasks, list):
        raise RuntimeError("Mission Control response did not contain a task list")
    return [task for task in tasks if isinstance(task, dict)]


def active_tasks(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        task
        for task in tasks
        if str(task.get("status") or "").lower() not in CLOSED_STATUSES
    ]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def matching_tasks(tasks: list[dict[str, Any]], title: str) -> list[dict[str, Any]]:
    needle = normalize(title)
    if not needle:
        return []
    return [
        task
        for task in active_tasks(tasks)
        if needle in normalize(str(task.get("title") or ""))
        or normalize(str(task.get("title") or "")) in needle
    ]


def load_task(path: Path) -> dict[str, Any]:
    task = json.loads(path.read_text())
    if not isinstance(task, dict):
        raise RuntimeError("Task file must contain a JSON object")
    required = ["title", "description", "status", "priority", "assignee", "project"]
    missing = [key for key in required if not task.get(key)]
    if missing:
        raise RuntimeError(f"Task file missing required fields: {', '.join(missing)}")
    return task


def post_task(task: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        MC_URL,
        data=json.dumps(task).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True, help="Finding/task title to dedupe")
    parser.add_argument("--create-file", help="JSON task payload to POST if no match exists")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    tasks = fetch_tasks()
    matches = matching_tasks(tasks, args.title)
    result: dict[str, Any] = {
        "duplicate": bool(matches),
        "matches": [
            {
                "id": task.get("_id") or task.get("id"),
                "title": task.get("title"),
                "status": task.get("status"),
                "priority": task.get("priority"),
                "project": task.get("project"),
            }
            for task in matches[:10]
        ],
        "created": False,
        "created_task": None,
    }

    if args.create_file and not matches:
        task = load_task(Path(args.create_file))
        created = post_task(task)
        result["created"] = True
        result["created_task"] = created

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif matches:
        print(f"SKIP duplicate: {args.title}")
    elif result["created"]:
        print(f"CREATED: {args.title}")
    else:
        print(f"NO_MATCH: {args.title}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
