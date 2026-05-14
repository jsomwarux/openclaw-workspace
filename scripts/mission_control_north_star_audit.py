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
    ("Complete weekly unemployment certification", 1, "Protects current financial stability; keep above optional work."),
    ("Altmark: lock PC handoff + acceptance/payment clarity", 2, "Fastest path to client acceptance, payment clarity, proof, and referrals."),
    ("Altmark: capture proof screenshots", 3, "Turns accepted client work into proof/distribution assets."),
    ("Strategy Jobs Pack: review one clean Drive doc", 4, "Choose the first real send/use from the completed Strategy Jobs Pack."),
    ("Ask Aya for referrals", 5, "Warm referral route from proven client work."),
    ("Aya co-living dashboard", 6, "Pending paid/client expansion opportunity."),
    ("CFS: reply yes to Dan sharing profile", 7, "Selective job-market option with construction/AI fit."),
    ("Vista: run one focused distribution block", 8, "App distribution action; no more stale launch checklist."),
    ("Guyana: ask dad/family network", 9, "Warm-intro gate for Guyana supplier wedge."),
    ("Land first wholesale pilot client", 11, "Credibility and consulting pipeline unlock."),
    ("Run first Consulting Sales Engine audit", 12, "Finds highest-probability next consulting dollar."),
    ("Run first Proof + Distribution audit", 13, "Converts work into visible proof and leads."),
    ("AI Ops Teardown: review/post property insurance", 14, "Proof-led content tied to real implementation work."),
    ("App Marketing OS: connect generated backlog", 30, "Keeps app marketing tasks synced into Mission Control without manual backlog drift."),
    ("App Marketing OS: implement weekly self-improvement", 35, "Forces app marketing continue/rework/measure-first decisions from evidence."),
    ("Vista: submit first durable directory listing", 40, "Durable discovery action for live Vista app."),
    ("Vista: run ASO baseline", 45, "Turns Vista distribution into measured App Store optimization."),
    ("Vista: schedule one clean rating-precision", 50, "Runs the next ReelFarm test with required metrics capture."),
    ("Nash Satoshi: submit first methodology-backed", 55, "Durable discovery action for Nash Satoshi with no return claims."),
    ("Nash Satoshi: create one live-ranking", 60, "Only ships Nash content when current live ranking data exists."),
    ("Glow Index: fix/verify crawler access", 65, "Unblocks durable discovery and AI-search visibility for Glow Index."),
    ("Glow Index: define metrics source", 70, "Prevents Glow social volume before measurement exists."),
    ("Weekly systems review: prune cron cap", 70, "Protects the operating layer from cost/noise/restart drift."),
    ("Harden cost/cron/security layer", 75, "Closes known protection-layer blockers from the xhigh systems audit."),
]

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
