# Job Application Tracker Agent
*Fires Tue/Thu 10:15 AM EST — monitors open applications, surfaces deadlines, drafts follow-up prompts*
*State source of truth: Mission Control task board (Job Market project)*

---

## Purpose
Squarespace SA was "🔴 urgent" in the morning brief for 2+ weeks without being submitted. The problem isn't awareness — it's accountability. This agent surfaces concrete deadlines, calculates days since posting, and escalates when applications go cold.

---

## Step 0: Load context
Read `~/.openclaw/workspace/MEMORY.md` → Job Market section.
Note: current open applications, their scores, and any known deadlines.

---

## Step 1: Pull open application tasks from Mission Control
```
curl -s "http://localhost:3000/api/tasks" | python3 -c "
import sys, json
tasks = json.load(sys.stdin)
apps = [t for t in tasks if t.get('project') == 'Job Market' and t.get('status') != 'done']
for t in apps:
    print(json.dumps({'id': t['id'], 'title': t['title'], 'status': t['status'], 'createdAt': t.get('createdAt', ''), 'description': t.get('description', '')[:200]}))
"
```

---

## Step 2: Triage each open application

For each open application task, determine:

**Days since created** — if `createdAt` is available, calculate days elapsed.

**Status classification:**
- `todo` + 0-3 days → NEW, no action
- `todo` + 4-7 days → STALE, flag to JT
- `todo` + 7+ days → OVERDUE, escalate with deadline context
- `in_progress` + 3+ days → STUCK, check what's blocking
- `done` → skip

**Deadline detection:** Scan the task description for "DEADLINE", "deadline", "closes", "apply by", "time-sensitive". Extract date if present.

---

## Step 3: Calculate urgency
For each STALE or OVERDUE application:
- Days since posting (job was posted when?)
- Days until deadline (if known)
- Score (from task title — format is usually "score: X/25")
- Doc status (Drive links in description = docs exist; no links = docs needed)

---

## Step 4: Send Telegram alert (only if STALE or OVERDUE items exist)
If everything is NEW or done → **do not message JT**. Silence is the correct output when there's nothing urgent.

If STALE or OVERDUE items exist, send to JT (channel=telegram, target=6608544825):

```
📋 *Application Check-In — [date]*

[For each STALE/OVERDUE item:]
🟠/🔴 *[Company — Role]* (score: X/25)
→ [N] days open | [Deadline: DATE or "no deadline found"]
→ Docs: [Ready ✅ / Needed ❌]
→ Action: [Submit today | Create docs first | Follow up]

[If any docs exist but not submitted:]
Docs are ready. The only step left is submitting.
```

One message. Under 400 chars per application listed. Direct.

---

## Step 5: Follow-up drafting (for cold applications only)
If any application task has status `in_progress` with a note indicating it was submitted more than 10 days ago and no response → draft a follow-up email and include it in the Telegram message.

Format:
```
Subject: Following up — [Role] application
[3-4 sentences: reference original application date, reinforce one concrete value prop, ask for update on timeline]
```

---

## Tone rules
- Direct. Not nagging.
- The goal is a clear next action, not a guilt trip.
- If docs are ready: say "docs are ready, submit today" not "you should apply soon."
- If nothing is urgent: say nothing.
