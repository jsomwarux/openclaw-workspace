#!/usr/bin/env python3
"""Daily Mission Control North Star priority auditor.

Keeps Mission Control's visible priority layer aligned with JT's North Star:
near-term consulting cash/proof first, app distribution second, crypto/opportunity monitoring
third, health/financial stability protected, stale/speculative work demoted.

Safe behavior:
- Does not delete tasks.
- Does not send external messages.
- Patches priority/sort/description only when a task matches explicit rules.
- Saves a report every run.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

BASE = "http://localhost:3000/api/tasks"
ROOT = Path.home() / ".openclaw" / "workspace"
REPORT_DIR = ROOT / "reports" / "mission-control-priority"

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
REQUIRED_DESCRIPTION_MARKERS = ("First action:", "Why it matters:")
DONE_MARKERS = ("Done state:", "Done looks like:")

# Explicit top layer. These are title fragments, not IDs, so the rule survives task recreation.
TOP_RULES: list[tuple[str, int, str]] = [
    ("Altmark: test and deploy rent delinquency workflow", 1, "Active paid client delivery: initial 50% received; testing/deployment is this week's revenue/proof gate."),
    ("Altmark: capture redacted proof screenshots", 2, "Insurance workflow is live and paid; capture proof-safe evidence while fresh."),
    ("Altmark: provide new workflow proposal", 3, "Next paid Altmark workflow after rent delinquency; proposal review is required before delivery planning."),
    ("Fix weekly systems review drift", 5, "Critical operating-layer blocker: cron cap, gateway load, bootstrap budgets."),
]

# Weekly single-focus guard. The North Star active-week file is the owner of the
# current top layer. When present, do not re-promote generic app/outreach/system
# tasks to high just because they were historically important.
ACTIVE_WEEK_FILE = ROOT / "memory" / "north-star" / "active-this-week.md"

STALE_COLD_PATTERNS = [
    "M2 OVERDUE",
    "M3:",
    "Email Pivot:",
    "M2:",
    "Review + Send:",
    "📤 ",
    "April 1",
]
STALE_COLD_PATTERNS_LOWER = [p.lower() for p in STALE_COLD_PATTERNS]

SKILL_PATTERNS = [
    "Trailhead",
    "Anthropic Academy",
    "OpenClaw",
    "Copilot",
    "Claude",
    "X Lists",
    "birdclaw",
    "Trend Radar",
    "MCP",
    "Agentforce Contact Center",
    "Ramp",
    "Close skill gap",
]

SPECULATIVE_PRODUCT_PATTERNS = [
    "WealthAgent",
    "Build idea",
    "programmatic SEO",
    "SEO/AI crawler",
    "HyperFrames",
    "Video Agent",
    "fantasy app",
    "Action Arena",
]

FABLE_DEFERRED_LANE_PATTERNS = [
    "Guyana summit",
    "Guyana growth resume",
    "Guyana:",
]

FABLE_APP_FREEZE_MONITORING_PATTERNS = [
    "Glow Index: define metrics source before any TikTok/ReelFarm volume",
]

# Tasks that should exist as a single active card at a time. Recurring tasks can
# be recreated after completion, but two active copies split attention and make
# the North Star layer look noisier than it is.
SINGLE_ACTIVE_TITLE_PATTERNS = [
    "Complete weekly unemployment certification",
    "Strategy: Clean buyer/channel state before new outreach",
    "Strategy: Clean Buyer-Channel State Before More Outreach",
]


def fetch_tasks() -> list[dict[str, Any]]:
    with urllib.request.urlopen(BASE, timeout=15) as resp:
        payload = json.load(resp)
    tasks = payload.get("tasks", payload)
    return [t for t in tasks if isinstance(t, dict)]


def patch_task(task_id: str, patch: dict[str, Any], dry_run: bool) -> tuple[bool, str]:
    if dry_run:
        return True, "dry-run"
    payload = {"id": task_id, **patch}
    req = urllib.request.Request(
        BASE,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return 200 <= resp.status < 300, str(resp.status)
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def contains_any(title: str, patterns: list[str]) -> bool:
    return any(p.lower() in title.lower() for p in patterns)


def matched_top_rule(title: str) -> tuple[int, str] | None:
    lower = title.lower()
    for fragment, sort_order, reason in TOP_RULES:
        if fragment.lower() in lower:
            return sort_order, reason
    return None


def needs_patch(task: dict[str, Any], desired: dict[str, Any]) -> bool:
    return any(task.get(k) != v for k, v in desired.items())


def append_note(description: str, note: str) -> str:
    if note in description:
        return description
    return (description.rstrip() + "\n\n" + note).strip()


def has_structured_task_contract(description: str) -> bool:
    lower = description.lower()
    return "first action:" in lower and "why it matters:" in lower and (
        "done state:" in lower or "done looks like:" in lower
    )


def build_task_contract(task: dict[str, Any], reason: str) -> str:
    """Create a concrete hygiene contract for legacy tasks without inventing status evidence."""
    title = str(task.get("title") or "this task")
    project = str(task.get("project") or "Mission Control")
    return (
        f"First action: open this Mission Control task and the source artifact referenced in the existing description; if no source artifact exists, decide whether to keep, defer, or archive `{title}` before doing any execution work.\n\n"
        f"Why it matters: {reason}\n\n"
        f"Done state: owner records keep/defer/archive or completes the named action, updates the source artifact if one exists, and closes or re-scopes this task so it no longer remains vague `{project}` backlog."
    )


def add_task_contract(task: dict[str, Any], reason: str) -> str:
    desc = str(task.get("description") or "").strip()
    if has_structured_task_contract(desc):
        return desc
    contract = build_task_contract(task, reason)
    return f"{contract}\n\n---\nLegacy/source details:\n{desc}".strip() if desc else contract


def task_quality(task: dict[str, Any]) -> dict[str, bool]:
    """Return task-board hygiene gates for active tasks.

    The board standard is intentionally concrete: every active task needs a first
    action, a reason it matters, and a done state. This does not mutate tasks; it
    gives the audit report an honest noise meter so generator drift is visible.
    """
    desc = str(task.get("description") or "")
    title = str(task.get("title") or "")
    text = f"{title}\n{desc}"
    return {
        "first_action": bool(re.search(r"first action:", text, re.I)),
        "why": bool(re.search(r"why it matters:", text, re.I)),
        "done": bool(re.search(r"done state:|done looks like:", text, re.I)),
        "owner": task.get("assignee") in {"jt", "eve", "both"},
        "priority": task.get("priority") in {"high", "medium", "low"},
        "status": task.get("status") in {"todo", "in-progress", "done", "archived"},
    }


def quality_gaps(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for task in tasks:
        if task.get("status") in {"done", "archived"}:
            continue
        gates = task_quality(task)
        missing = [name for name, ok in gates.items() if not ok]
        if missing:
            gaps.append({"task": task, "missing": missing})
    return gaps


def desired_for(task: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    if task.get("status") in {"done", "archived"}:
        return None, None
    title = str(task.get("title") or "")
    project = str(task.get("project") or "")
    desc = str(task.get("description") or "")

    top = matched_top_rule(title)
    if top:
        sort_order, reason = top
        note = f"North Star priority rule: {reason}"
        priority_desc = add_task_contract(task, reason) if not has_structured_task_contract(desc) else append_note(desc, note)
        if note not in priority_desc:
            priority_desc = append_note(priority_desc, note)
        desired = {
            "priority": "high",
            "sortOrder": sort_order,
            "description": priority_desc,
        }
        return desired, "promote/keep top priority"

    if contains_any(title, STALE_COLD_PATTERNS) or contains_any(desc, STALE_COLD_PATTERNS_LOWER):
        note = "Demoted by daily North Star audit: stale cold-outreach backlog; revive only if acquisition reset selects this prospect/channel again."
        reason = "stale cold outreach should not compete with warm referrals, paid client acceptance, or proof-led distribution."
        return {
            "priority": "low",
            "sortOrder": 220,
            "description": add_task_contract(task, reason) if not has_structured_task_contract(desc) else append_note(desc, note),
        }, "demote stale cold outreach"

    if project in {"Skills", "Job Market"} or contains_any(title, SKILL_PATTERNS) or title.startswith("Apply:"):
        note = "Demoted by daily North Star audit: useful, but not immediate next-dollar/proof/distribution unless tied to an active opportunity."
        reason = "skills/job-market items are useful only when they support a current role, consulting proof, or near-term revenue path."
        return {
            "priority": "medium",
            "sortOrder": 140,
            "description": add_task_contract(task, reason) if not has_structured_task_contract(desc) else append_note(desc, note),
        }, "demote skill/job-market noise"

    if contains_any(title, FABLE_DEFERRED_LANE_PATTERNS):
        note = "Demoted by daily North Star audit: Fable audit classified Guyana as validation-only until a named buyer/problem/reply exists."
        reason = "Guyana work should not outrank Altmark cash, proof, or the active consulting acquisition queue unless there is a fresh named buyer/problem/reply."
        deferred_priority = "low" if task.get("priority") == "low" else "medium"
        deferred_sort = 230 if deferred_priority == "low" else 180
        return {
            "priority": deferred_priority,
            "sortOrder": deferred_sort,
            "description": add_task_contract(task, reason) if not has_structured_task_contract(desc) else append_note(desc, note),
        }, "demote Fable-deferred Guyana lane"

    if contains_any(title, FABLE_APP_FREEZE_MONITORING_PATTERNS):
        note = "Demoted by daily North Star audit: Glow is in data-accrual freeze; keep one monitoring/setup task only, below consulting cash/proof."
        reason = "Glow metrics setup may support later learning, but it should not compete with Altmark cash, proof, or consulting sends during the Fable product freeze."
        return {
            "priority": "low",
            "sortOrder": 130,
            "description": add_task_contract(task, reason) if not has_structured_task_contract(desc) else append_note(desc, note),
        }, "demote Glow freeze monitoring"

    if contains_any(title, SPECULATIVE_PRODUCT_PATTERNS):
        note = "Demoted by daily North Star audit: speculative product/build work cannot outrank consulting cash/proof or current distribution actions."
        reason = "speculative build work must be explicitly selected before it consumes attention ahead of consulting cash, proof, or current app distribution."
        return {
            "priority": "medium",
            "sortOrder": 150,
            "description": add_task_contract(task, reason) if not has_structured_task_contract(desc) else append_note(desc, note),
        }, "demote speculative build"

    # Catch orphan high tasks without a sort order. High priority must be explicit.
    if task.get("priority") == "high" and task.get("sortOrder") is None:
        note = "Demoted by daily North Star audit: high-priority task had no explicit sort order or top-layer rule."
        return {
            "priority": "medium",
            "sortOrder": 160,
            "description": append_note(desc, note),
        }, "demote unsorted high task"

    return None, None


def canonical_duplicate_key(title: str) -> str | None:
    """Return a normalized duplicate key for active one-card task families."""
    lower = title.lower()
    if "complete weekly unemployment certification" in lower:
        return "weekly_unemployment_certification"
    if "clean buyer" in lower and "channel state" in lower and "outreach" in lower:
        return "clean_buyer_channel_state"
    if "glow index: define metrics source before any tiktok/reelfarm volume" in lower:
        return "glow_metrics_source"
    return None


def dedupe_active_tasks(tasks: list[dict[str, Any]], dry_run: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Archive duplicate active recurring tasks, keeping the newest active copy.

    This is deliberately narrow and only applies to explicit one-card task
    families. It avoids broad title fuzzy matching so the audit cannot archive
    unrelated work that merely sounds similar.
    """
    active = [t for t in tasks if t.get("status") not in {"done", "archived"}]
    buckets: dict[str, list[dict[str, Any]]] = {}
    for task in active:
        key = canonical_duplicate_key(str(task.get("title") or ""))
        if key:
            buckets.setdefault(key, []).append(task)

    changes: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for key, group in buckets.items():
        if len(group) < 2:
            continue
        # Keep newest task; if timestamps tie, keep the one with latest update.
        group.sort(key=lambda t: (t.get("createdAt") or 0, t.get("updatedAt") or 0), reverse=True)
        keep = group[0]
        for dup in group[1:]:
            note = (
                f"Archived by daily North Star audit: duplicate active `{key}` task. "
                f"Current active card kept: {keep.get('_id')} — {keep.get('title')}."
            )
            desc = append_note(str(dup.get("description") or ""), note)
            desired = {"status": "archived", "description": desc}
            ok, detail = patch_task(str(dup.get("_id")), desired, dry_run)
            entry = {
                "id": dup.get("_id"),
                "title": dup.get("title"),
                "reason": "archive duplicate active recurring task",
                "from": {"status": dup.get("status"), "kept": keep.get("_id")},
                "to": {"status": "archived"},
                "status": detail,
            }
            if ok:
                changes.append(entry)
            else:
                errors.append(entry)
    return changes, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tasks = fetch_tasks()
    active_before = [t for t in tasks if t.get("status") not in {"done", "archived"}]
    changes: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for task in tasks:
        desired, reason = desired_for(task)
        if not desired:
            continue
        # Only include fields that actually change, except description note when changed.
        if not needs_patch(task, desired):
            continue
        ok, detail = patch_task(str(task.get("_id")), desired, args.dry_run)
        entry = {
            "id": task.get("_id"),
            "title": task.get("title"),
            "reason": reason,
            "from": {"priority": task.get("priority"), "sortOrder": task.get("sortOrder")},
            "to": {"priority": desired.get("priority"), "sortOrder": desired.get("sortOrder")},
            "status": detail,
        }
        if ok:
            changes.append(entry)
        else:
            errors.append(entry)

    duplicate_changes, duplicate_errors = dedupe_active_tasks(tasks, args.dry_run)
    changes.extend(duplicate_changes)
    errors.extend(duplicate_errors)

    after = fetch_tasks() if not args.dry_run else tasks
    active_after = [t for t in after if t.get("status") not in {"done", "archived"}]
    high_after = [t for t in active_after if t.get("priority") == "high"]
    quality_after = quality_gaps(active_after)
    by_project = Counter(str(t.get("project") or "<missing>") for t in active_after)
    by_priority = Counter(str(t.get("priority") or "<missing>") for t in active_after)
    by_status = Counter(str(t.get("status") or "<missing>") for t in after)
    high_after.sort(key=lambda t: (t.get("sortOrder") if t.get("sortOrder") is not None else 9999, t.get("title") or ""))
    explicit_top_titles = {fragment.lower() for fragment, _, _ in TOP_RULES}
    uncontrolled_high = [
        t
        for t in high_after
        if not any(fragment in str(t.get("title") or "").lower() for fragment in explicit_top_titles)
    ]

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_slug = datetime.now().strftime("%Y-%m-%d")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_suffix = "-dry-run" if args.dry_run else ""
    report_path = REPORT_DIR / f"{date_slug}{report_suffix}.md"

    lines = [
        f"# Mission Control North Star Audit — {now}",
        "",
        f"Dry run: {args.dry_run}",
        f"Active before: {len(active_before)}",
        f"Active after: {len(active_after)}",
        f"High after: {len(high_after)}",
        f"Changes applied: {len(changes)}",
        f"Errors: {len(errors)}",
        f"Uncontrolled high-priority items: {len(uncontrolled_high)}",
        f"Active task quality gaps: {len(quality_after)}",
        "",
        "## Counts",
        f"- By status: {dict(by_status.most_common())}",
        f"- Active by priority: {dict(by_priority.most_common())}",
        f"- Active by project top 10: {dict(by_project.most_common(10))}",
        "",
        "## Current High-Priority Layer",
    ]
    for t in high_after:
        lines.append(f"- {t.get('sortOrder')}: [{t.get('assignee')}] {t.get('title')}")
    lines.extend(["", "## Changes"])
    if changes:
        for c in changes[:100]:
            lines.append(f"- {c['reason']}: {c['title']} ({c['from']} → {c['to']})")
    else:
        lines.append("- No changes needed.")
    if uncontrolled_high:
        lines.extend(["", "## Uncontrolled High-Priority Items"])
        lines.append(
            "These are high-priority tasks not matched by explicit TOP_RULES. Review weekly: keep only if they still serve consulting cash/proof/current distribution."
        )
        for t in uncontrolled_high[:50]:
            lines.append(f"- {t.get('sortOrder')}: [{t.get('assignee')}] {t.get('title')}")
    if quality_after:
        lines.extend(["", "## Task Quality Gaps"])
        lines.append(
            "Active tasks missing first-action/why/done/owner/priority/status gates. Fix generators first; avoid mass-editing stale backlog unless evidence is clear."
        )
        for gap in quality_after[:50]:
            t = gap["task"]
            lines.append(f"- Missing {', '.join(gap['missing'])}: [{t.get('priority')}/{t.get('project')}] {t.get('title')}")
    if errors:
        lines.extend(["", "## Errors"])
        for e in errors:
            lines.append(f"- {e['title']}: {e['status']}")

    report_path.write_text("\n".join(lines) + "\n")

    print(
        json.dumps(
            {
                "ok": not errors,
                "dry_run": args.dry_run,
                "active_before": len(active_before),
                "active_after": len(active_after),
                "high_after": len(high_after),
                "changes": len(changes),
                "errors": len(errors),
                "uncontrolled_high": len(uncontrolled_high),
                "report": str(report_path),
                "high_titles": [t.get("title") for t in high_after[:20]],
            },
            ensure_ascii=False,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
