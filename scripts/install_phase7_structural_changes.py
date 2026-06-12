#!/usr/bin/env python3
"""Install Phase 7 cron structural changes with prompt backups."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


WORKSPACE = Path("/Users/jtsomwaru/.openclaw/workspace")
JOBS_PATH = Path("/Users/jtsomwaru/.openclaw/cron/jobs.json")
NIGHT_ARCHIVE = WORKSPACE / "docs/audits/phase7-night-agent-prompts-2026-06-11.md"
PROMPT_BACKUP = WORKSPACE / "docs/audits/phase7-prompt-backups-2026-06-11.md"
FULL_BACKUP = Path("/Users/jtsomwaru/.openclaw/cron/jobs.json.backup-phase7-202606111457")


NIGHTLY_ID = "003191af-45a7-4e3b-a824-f7a6cd52f8c7"
OVERNIGHT_ID = "be59a068-eccd-4a7c-964e-946ab40ace7e"
MERGED_ID = "f146d8b8-94e0-49ff-8e4a-5050a284e894"
WEEKLY_ID = "b2ca53ab-0c07-4a22-8424-9d39bf988405"
MONTHLY_ID = "fdc2cf75-50d8-4466-bbb7-5a8683eb6afd"
INTEGRITY_ID = "ee357abb-2b58-44b8-8f03-4c152611117d"


def load_jobs() -> tuple[dict | list, list[dict]]:
    data = json.loads(JOBS_PATH.read_text())
    if isinstance(data, dict) and isinstance(data.get("jobs"), list):
        return data, data["jobs"]
    if isinstance(data, list):
        return data, data
    raise SystemExit("Unsupported jobs.json shape")


def find_job(jobs: list[dict], job_id: str) -> dict:
    for job in jobs:
        if job.get("id") == job_id:
            return job
    raise SystemExit(f"Missing required cron job {job_id}")


def message(job: dict) -> str:
    return (job.get("payload") or {}).get("message") or ""


def backup_prompt_doc(path: Path, title: str, jobs: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {title}",
        "",
        "Captured before Phase 7 structural cron changes on 2026-06-11.",
        "",
    ]
    for job in jobs:
        lines.extend(
            [
                f"## {job.get('name')} ({job.get('id')})",
                "",
                f"- Enabled before edit: `{job.get('enabled')}`",
                f"- Schedule before edit: `{job.get('schedule')}`",
                f"- Delivery before edit: `{job.get('delivery')}`",
                "",
                "```text",
                message(job),
                "```",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def merged_prompt() -> str:
    return """You are Eve's merged Night Autonomy Agent for JT Somwaru.

## Task Context
Run once nightly at 11:00 PM ET. This job replaces and combines:
- `nightly-autonomous-leverage-agent` / 9:45 PM strategic worker behavior.
- `Overnight Autonomy Agent` / 3:20 AM verification and blocker-removal behavior.

Your job is to complete one full artifact per night inside the sanctioned autonomy lanes, then verify it, log it, and stop. Do not create advisory-only output when a bounded artifact can be finished safely.

## Sanctioned Autonomy Lanes
You have full completion authority, with no asking, only inside these lanes:
1. Content ready state: draft, validate, upload to Drive when required, push/schedule in Notion when required, and queue for JT review.
2. Prospect packet ready state: complete research, verify contact, write hook, save outreach draft to Drive, and return the packet/link for JT to send. Never send outreach.
3. Ops self-healing: safe cron fixes, zombie cleanup, cooldown recovery, bootstrap/file-budget trims, and local guard/script fixes.

Everything outside these lanes is advisory. Never-send-outreach, API key, finance, browser, gateway, model-routing, and all Hard Rules remain binding.

## Phase One - Strategic Worker
1. Read `MEMORY.md`, `HEARTBEAT.md`, `TOOLS.md`, `plans/eve-optimization-2026-06-11.md`, today's daily note, and the current Mission Control priority layer.
2. Ask: what can Eve safely finish tonight that best advances JT's North Star without requiring JT to manage the work?
3. Pick exactly one artifact unless a small prerequisite is required to complete it.
4. Prefer work that creates a reusable asset, closes a known blocker, improves distribution, or reduces operational drag.
5. If the best move is content, produce a review-ready content artifact and route it through the existing content guard/Drive/Notion/queue flow.
6. If the best move is prospecting, produce a complete outreach packet with contact verification and a saved draft. JT presses send.
7. If the best move is ops, fix the root cause, add/adjust the guardrail, and verify the system state.

## Phase Two - Verification And Blocker Removal
After Phase One, verify the artifact instead of assuming it worked.
1. Confirm file paths, Drive/Notion links, cron state, task state, or guard output with real tool/script evidence.
2. Remove one adjacent blocker if it is safe and inside the sanctioned lanes.
3. Update the owner surface: daily note, weekly recap, MEMORY/MEMORY-full when required, proof log, and Mission Control next-use task only when actionable.
4. If no meaningful artifact can be completed, output `NO_ACTION_NEEDED: [specific reason]` and name the checked lane.
5. If blocked by a hard rule or missing external approval, create a concrete next-use task and stop.

## Budget And Stop Rules
- Complete one full artifact per night; do not spread across many partial tasks.
- Keep tool use bounded and purposeful; avoid browsing unless the selected artifact needs fresh public facts.
- Do not run `claude` CLI.
- Do not send outreach or make financial/account changes.
- Do not modify auth/model config or OpenClaw runtime config outside approved rules.
- Stop after the final report; do not keep searching for extra work.

## Output Format
Return exactly:

Night Autonomy Report - YYYY-MM-DD
Lane: content | prospecting | ops | none
Artifact completed: [specific title/path/link or NO_ACTION_NEEDED]
Verification evidence: [commands/files/links checked]
Material delta: [what is better now than before tonight]
Blocker removed or next blocker: [specific]
Files/tasks updated: [paths/task ids or none]
"""


def weekly_addition() -> str:
    return """

## Phase 7 Outcome KPI Reporting - 2026-06-11 JT Override
Every Weekly Systems Review must report these six numbers before recommendations:
1. Posts delivered vs posted.
2. Engagement per posted item.
3. Outreach packets completed vs sent vs replied.
4. Consulting pipeline stage movement.
5. Cron delivery rate.
6. Dollars spent: OpenRouter plus X API.

Use tool/script evidence where available. State `unknown` only with the exact missing source and a concrete fix.

## Phase 7 Monthly Prompt Rewrite Ritual
On the first Sunday of each month:
1. Identify the five longest live `payload.message` prompts in `/Users/jtsomwaru/.openclaw/cron/jobs.json`.
2. Draft clean rewrites under 600 words each.
3. Move tooling command detail into scripts where practical instead of appending more prompt text.
4. Save proposed rewrites under `docs/audits/prompt-rewrites/YYYY-MM-DD/`.
5. Get JT approval per prompt before installing. Do not install rewritten prompts without approval.
"""


def monthly_addition() -> str:
    return """

## Phase 7 KPI-Centered Comparison - 2026-06-11 JT Override
Replace job-description keyword scanning as the comparison target. The monthly gap analysis must compare Eve's current skills, tools, agents, and habits against these six operating KPIs:
1. Posts delivered vs posted.
2. Engagement per posted item.
3. Outreach packets completed vs sent vs replied.
4. Consulting pipeline stage movement.
5. Cron delivery rate.
6. Dollars spent: OpenRouter plus X API.

Recommend skill/tool/prompt changes only when they plausibly improve one of those KPIs.
"""


def integrity_addition() -> str:
    return """

Phase 7 addition: `scripts/critical-files-integrity.py` now also invokes `python3 /Users/jtsomwaru/.openclaw/workspace/scripts/cron_snapshot.py` to snapshot `/Users/jtsomwaru/.openclaw/cron/jobs.json` into `config/cron-snapshots/jobs-YYYY-MM-DD.json` and git-commit that snapshot when changed. Do not create a separate cron for snapshots.
"""


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n" + addition.strip() + "\n"


def main() -> None:
    data, jobs = load_jobs()
    if not FULL_BACKUP.exists():
        shutil.copy2(JOBS_PATH, FULL_BACKUP)

    nightly = find_job(jobs, NIGHTLY_ID)
    overnight = find_job(jobs, OVERNIGHT_ID)
    weekly = find_job(jobs, WEEKLY_ID)
    monthly = find_job(jobs, MONTHLY_ID)
    integrity = find_job(jobs, INTEGRITY_ID)

    backup_prompt_doc(NIGHT_ARCHIVE, "Phase 7 Night Agent Prompt Archive", [nightly, overnight])
    backup_prompt_doc(PROMPT_BACKUP, "Phase 7 Edited Prompt Backups", [weekly, monthly, integrity])

    nightly["enabled"] = False
    nightly["delivery"] = {"mode": "none"}
    overnight["enabled"] = False
    overnight["delivery"] = {"mode": "none"}

    existing = [job for job in jobs if job.get("id") == MERGED_ID]
    merged = existing[0] if existing else {
        "id": MERGED_ID,
        "agentId": "main",
        "sessionKey": nightly.get("sessionKey"),
        "name": "Night Autonomy Agent",
        "createdAtMs": int(datetime(2026, 6, 11, 14, 57).timestamp() * 1000),
        "deleteAfterRun": False,
        "sessionTarget": "isolated",
        "wakeMode": "now",
        "state": {},
    }
    merged.update(
        {
            "name": "Night Autonomy Agent",
            "description": "Merged 11PM strategic worker plus verification/blocker-removal autonomy agent.",
            "enabled": True,
            "schedule": {"kind": "cron", "expr": "0 23 * * *", "tz": "America/New_York"},
            "delivery": {"mode": "announce", "channel": "telegram", "to": "6608544825", "bestEffort": True},
            "failureAlert": {"after": 2, "mode": "announce", "channel": "telegram", "to": "6608544825", "cooldownMs": 21600000},
            "payload": {"kind": "message", "timeoutSeconds": 1800, "message": merged_prompt()},
        }
    )
    if not existing:
        jobs.append(merged)

    weekly["payload"]["message"] = append_once(
        message(weekly),
        "Phase 7 Outcome KPI Reporting",
        weekly_addition(),
    )
    monthly["payload"]["message"] = append_once(
        message(monthly),
        "Phase 7 KPI-Centered Comparison",
        monthly_addition(),
    )
    integrity["payload"]["message"] = append_once(
        message(integrity),
        "Phase 7 addition: `scripts/critical-files-integrity.py`",
        integrity_addition(),
    )

    tmp = JOBS_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(JOBS_PATH)

    print(
        json.dumps(
            {
                "jobs": len(jobs),
                "night_archive": str(NIGHT_ARCHIVE),
                "prompt_backup": str(PROMPT_BACKUP),
                "full_backup": str(FULL_BACKUP),
                "merged_id": MERGED_ID,
                "disabled_originals": [NIGHTLY_ID, OVERNIGHT_ID],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
