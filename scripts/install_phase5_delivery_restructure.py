#!/usr/bin/env python3
"""Install Phase 5 delivery restructure cron changes."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime
from pathlib import Path


WORKSPACE = Path("/Users/jtsomwaru/.openclaw/workspace")
JOBS_PATH = Path("/Users/jtsomwaru/.openclaw/cron/jobs.json")
BACKUP_PATH = WORKSPACE / "docs/audits/phase5-prompt-backups.md"
DIGEST_QUEUE = WORKSPACE / "memory/digest-queue.md"

REMINDER_NAMES = {
    "reddit-karma-daily-reminder",
    "Nash Satoshi TikTok Warmup Reminder",
    "TikTok App Account Warm-up Reminder",
    "TikTok App Account Warm-up Reminder (2 PM)",
    "ReelFarm Daily Strategy Intel",
}

BACKUP_NAMES = REMINDER_NAMES | {"Morning Brief"}


def load_jobs() -> tuple[dict, list[dict]]:
    data = json.loads(JOBS_PATH.read_text())
    jobs = data.get("jobs")
    if not isinstance(jobs, list):
        raise SystemExit("jobs.json does not contain a jobs list")
    return data, jobs


def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=str(path.parent), delete=False) as tmp:
        json.dump(data, tmp, indent=2, ensure_ascii=False)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def write_prompt_backup(jobs: list[dict]) -> None:
    BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phase 5 Prompt Backups - 2026-06-11",
        "",
        f"Source: `{JOBS_PATH}`",
        f"Captured: `{datetime.now().isoformat(timespec='seconds')}`",
        "",
        "These are the `payload.message` values backed up before the Phase 5 delivery restructure.",
        "",
    ]
    by_name = {job.get("name"): job for job in jobs}
    for name in sorted(BACKUP_NAMES):
        job = by_name.get(name)
        if not job:
            lines.extend([f"## {name}", "", "MISSING", ""])
            continue
        payload = job.get("payload") or {}
        message = payload.get("message", "")
        lines.extend(
            [
                f"## {name}",
                "",
                f"- Job ID: `{job.get('id')}`",
                f"- Message bytes: `{len(message.encode())}`",
                "",
                "```text",
                message,
                "```",
                "",
            ]
        )
    BACKUP_PATH.write_text("\n".join(lines))


def with_delivery_override(message: str, job_name: str) -> str:
    marker = "## PHASE 5 DELIVERY RESTRUCTURE — 2026-06-11"
    base = message.split(marker)[0].rstrip()
    if job_name == "ReelFarm Daily Strategy Intel":
        body = (
            f"{marker}\n"
            "Do not send a standalone Telegram message for routine FYI output. Always save the report file. "
            "Append a 1-3 line digest entry to `/Users/jtsomwaru/.openclaw/workspace/memory/digest-queue.md` with: "
            "`- [ReelFarm Daily Strategy Intel] [finding/summary] | file: [absolute report path]`. "
            "Use Telegram only for a verified critical finding that needs same-day JT action; otherwise queue it for the Evening Digest."
        )
    elif job_name == "reddit-karma-daily-reminder":
        body = (
            f"{marker}\n"
            "Do not send a standalone Telegram message. Write any generated Reddit reminder/FYI output to the normal local files/logs, "
            "then append a 1-3 line digest entry to `/Users/jtsomwaru/.openclaw/workspace/memory/digest-queue.md` with the draft path, target platform/subreddit, and the one action JT should take. "
            "Use Telegram only for a verified critical finding; otherwise queue it for the Evening Digest."
        )
    elif job_name == "Nash Satoshi TikTok Warmup Reminder":
        body = (
            f"{marker}\n"
            "Do not send a standalone Telegram reminder. Append this 1-3 line FYI to `/Users/jtsomwaru/.openclaw/workspace/memory/digest-queue.md`: "
            "`- [Nash Satoshi TikTok Warmup] Warmup check: scroll crypto/finance FYP naturally, like/comment/save/follow selectively, and post only manually when trust is rebuilt. | reply: skip if done`. "
            "Use Telegram only for a verified critical finding."
        )
    else:
        label = job_name.replace("TikTok App Account Warm-up Reminder", "TikTok App Warmup").strip()
        body = (
            f"{marker}\n"
            "Do not send a standalone Telegram reminder. Append this 1-3 line FYI to `/Users/jtsomwaru/.openclaw/workspace/memory/digest-queue.md`: "
            f"`- [{label}] Spend 15-20 min inside Vista, Nash Satoshi, and Glow Index; scroll niche feeds and interact naturally before one manual re-entry post per account. | reply: skip if done`. "
            "Use Telegram only for a verified critical finding."
        )
    return f"{base}\n\n{body}"


def morning_brief_message(old: str) -> str:
    source_rule = (
        "Run the Morning Brief exactly according to `/Users/jtsomwaru/.openclaw/workspace/HEARTBEAT.md` section `## Morning Brief (7:30 AM, cron)`. "
        "Before composing, read that section fresh from disk."
    )
    send_queue = (
        "SEND QUEUE — mandatory opening section, 2026-06-11 JT override:\n"
        "- Open the brief with `SEND QUEUE` before priorities/news.\n"
        "- Hard cap: 3 items total.\n"
        "- Each item must be a finished artifact with a direct link or absolute file path and exactly one one-word reply keyword: `send`, `post`, or `skip`.\n"
        "- Choose only the day's top 3 JT decisions; do not include FYI reminders here unless they are one of the top 3 actions.\n\n"
    )
    msg = old
    if msg.startswith(source_rule):
        msg = source_rule + "\n\n" + send_queue + msg[len(source_rule):].lstrip()
    else:
        msg = send_queue + msg

    old_contract = (
        "NASH DELIVERY CONTRACT — non-negotiable:\n"
        "- The final Morning Brief must include the FULL Daily X Post text inline.\n"
        "- The final Morning Brief must include the FULL Daily Reddit Draft inline, including `SUBREDDIT`, rationale, `TITLE`, and `BODY`.\n"
        "- Do NOT replace the drafts with only a file path, one-line summary, teaser, or truncated excerpt.\n"
        "- If Telegram length is a concern, shorten lower-priority news sections first; preserve the full Nash X + Reddit drafts."
    )
    new_contract = (
        "NASH DELIVERY CONTRACT — revised by JT on 2026-06-11, explicit override of the prior full-text block:\n"
        "- Include only the first 2 lines of the Nash X post and the first 2 lines of the Reddit draft in the Morning Brief body.\n"
        "- Include the saved local file path and Drive link for the full Nash output.\n"
        "- The full text appears as a `SEND QUEUE` item only when it is among the day's top 3 actions.\n"
        "- Do not paste the full Nash X or Reddit draft inline unless it is selected as one of the capped Send Queue items."
    )
    if old_contract not in msg:
        raise SystemExit("Morning Brief Nash delivery contract block not found")
    return msg.replace(old_contract, new_contract)


def evening_digest_job() -> dict:
    return {
        "name": "Evening Digest",
        "description": "Daily 7PM ET consolidated digest for reminder/FYI jobs queued in memory/digest-queue.md.",
        "enabled": True,
        "schedule": {"kind": "cron", "expr": "0 19 * * *", "tz": "America/New_York"},
        "sessionTarget": "isolated",
        "wakeMode": "now",
        "deleteAfterRun": False,
        "id": "evening-digest-001",
        "delivery": {"mode": "none"},
        "failureAlert": {
            "after": 1,
            "channel": "telegram",
            "to": "6608544825",
            "cooldownMs": 86400000,
            "mode": "announce",
        },
        "state": {},
        "payload": {
            "kind": "agentTurn",
            "timeoutSeconds": 600,
            "message": (
                "You are Eve running the lightweight Evening Digest for JT.\n\n"
                "Rules:\n"
                "1. Read `/Users/jtsomwaru/.openclaw/workspace/memory/digest-queue.md`.\n"
                "2. If the file is empty or only whitespace, send nothing and return `EVENING_DIGEST_EMPTY`.\n"
                "3. If non-empty, send exactly one Telegram message to JT under 2,500 characters summarizing the queued entries. Use concise bullets and preserve any links/file paths.\n"
                "4. After the Telegram send succeeds, clear `/Users/jtsomwaru/.openclaw/workspace/memory/digest-queue.md` to an empty file.\n"
                "5. Lightweight limit: max 5 tool calls total, no web searches, no external browsing.\n\n"
                "Output after completion: `EVENING_DIGEST_SENT` or `EVENING_DIGEST_EMPTY`."
            ),
        },
    }


def main() -> None:
    data, jobs = load_jobs()
    write_prompt_backup(jobs)
    DIGEST_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    DIGEST_QUEUE.touch(exist_ok=True)

    seen = set()
    for job in jobs:
        name = job.get("name")
        if name in REMINDER_NAMES:
            seen.add(name)
            job["payload"]["message"] = with_delivery_override(job["payload"].get("message", ""), name)
            if name in {"TikTok App Account Warm-up Reminder", "TikTok App Account Warm-up Reminder (2 PM)"}:
                job["delivery"] = {"mode": "none"}
            if name == "TikTok App Account Warm-up Reminder":
                # Keep the 2 PM queue-before-digest reminder and retire the redundant 7:45 PM agent turn.
                job["enabled"] = False
        elif name == "Morning Brief":
            seen.add(name)
            job["payload"]["message"] = morning_brief_message(job["payload"].get("message", ""))
        elif name == "content-reminder":
            if "PHASE 5 DELIVERY RESTRUCTURE" in job["payload"].get("message", ""):
                raise SystemExit("content-reminder was unexpectedly modified")

    missing = BACKUP_NAMES - seen
    if missing:
        raise SystemExit(f"Missing jobs: {sorted(missing)}")

    existing = [job for job in jobs if job.get("id") == "evening-digest-001" or job.get("name") == "Evening Digest"]
    if existing:
        for job in existing:
            jobs.remove(job)
    jobs.append(evening_digest_job())

    atomic_write_json(JOBS_PATH, data)
    print(json.dumps({"ok": True, "backup": str(BACKUP_PATH), "digest_queue": str(DIGEST_QUEUE)}, indent=2))


if __name__ == "__main__":
    main()
