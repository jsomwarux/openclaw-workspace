#!/usr/bin/env python3
"""Sync job-market build ideas into Mission Control.

Idempotent local helper for cron dfd92d8d. It avoids agent generation failures by
performing the lightweight file/API diff directly.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

IDEAS_PATH = Path.home() / "projects/job-market-agent/data/agent-ideas.md"
LOG_PATH = Path.home() / "projects/job-market-agent/data/sync-log.md"
TASKS_URL = "http://localhost:3000/api/tasks"


def words(s: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[a-zA-Z0-9]+", s) if len(w) > 2}


def parse_ideas(text: str) -> list[dict[str, str]]:
    ideas: list[dict[str, str]] = []
    # Split on markdown idea headings like **[Skill]: Name**.
    matches = list(re.finditer(r"^\*\*(.+?)\*\*\s*$", text, flags=re.M))
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        if title.lower().startswith("[skill gap]"):
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if not body or "Status:" not in body:
            continue
        ideas.append({"title": title, "body": body})
    return ideas


def get_tasks() -> list[dict]:
    with urlopen(TASKS_URL, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("tasks", data if isinstance(data, list) else [])


def similar_exists(idea_title: str, existing_titles: list[str]) -> bool:
    iw = words(idea_title)
    for title in existing_titles:
        tw = words(title)
        if idea_title.lower() in title.lower() or title.lower() in idea_title.lower():
            return True
        # Require at least 3 meaningful overlapping terms, or all terms for short titles.
        overlap = iw & tw
        if len(overlap) >= min(3, max(1, len(iw))):
            return True
    return False


def dedupe_key(title: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"job-market-build-idea-{key[:100]}"


def post_task(idea: dict[str, str]) -> None:
    task_title = f"Build idea: {idea['title']}"
    body = idea["body"].strip()
    description = (
        "First action: open `~/projects/job-market-agent/data/agent-ideas.md`, find this idea, and validate whether it directly supports a current target role or JT's consulting proof layer before building.\n\n"
        "Why it matters: build ideas are useful only when they improve near-term positioning, consulting proof, or a specific application; otherwise they become task-board clutter.\n\n"
        "Done looks like: decision is recorded as build/defer/kill; if build, a scoped implementation task with exact repo/path and success metric replaces this idea task.\n\n"
        f"Source detail from job-market-agent daily scan:\n{body}"
    )
    payload = {
        "title": task_title[:240],
        "description": description,
        "status": "todo",
        "priority": "medium",
        "assignee": "eve",
        "project": "Job Market",
        "sortOrder": 500,
        "slug": dedupe_key(task_title),
        "pipelineStage": "triage",
    }
    req = Request(
        TASKS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=20) as resp:
        resp.read()


def main() -> int:
    if not IDEAS_PATH.exists():
        raise SystemExit(f"missing ideas file: {IDEAS_PATH}")
    ideas = parse_ideas(IDEAS_PATH.read_text())
    tasks = get_tasks()
    existing_titles = [str(t.get("title", "")) for t in tasks]
    pushed = skipped = 0
    for idea in ideas:
        if similar_exists(idea["title"], existing_titles):
            skipped += 1
            continue
        post_task(idea)
        existing_titles.append(f"Build idea: {idea['title']}")
        pushed += 1
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    LOG_PATH.open("a").write(f"[{stamp}] build-ideas-sync | pushed: {pushed} | skipped: {skipped}\n")
    print(json.dumps({"ok": True, "pushed": pushed, "skipped": skipped, "ideas": len(ideas)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
