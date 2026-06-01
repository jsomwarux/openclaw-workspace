# Task Board Rules
> Source: AGENTS.md §Task Board Rules
> Single source of truth for all Mission Control task management.

## Overview
Everything JT needs to do must be on the board. Overnight items, decisions, JT manual steps → pushed as HIGH tasks before logging. De-dupe before pushing. Any build/skill/project recommendation MUST be pushed to MC immediately.

## Priority Bands
- **HIGH** — actionable now: consulting deliverables, job apps with open deadlines, demo builds, alerts → act within 48h
- **MEDIUM** — blocked/speculative: "Build idea:" tasks, blocked/waiting, internal refactors; speculative → sortOrder 500+
- **LOW** — nice-to-have, stalled, far-future

## Standing Priority Order
Consulting first → job apps (2–3/week, 20+/25 threshold, no coding/SE/Python roles) → time-sensitive products → speculative builds → passive habits.

## Dependency Rule
B after A and A not done → B's priority ≤ A's priority.

## Unblocking Rule
When marking done, bump unblocked tasks to HIGH.

## Audit Trigger
Eve adds a task OR JT asks "are my tasks prioritized?" → quick audit + fix same turn.

## Quick Push Template
```bash
curl -s -X POST http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"[TITLE]","description":"[DESCRIPTION]","status":"todo","priority":"[high|medium|low]","assignee":"[eve|JT]","project":"[Job Market|Skills|Consulting|passive-income]","sortOrder":[N]}'
```

## De-dupe Check
Before pushing: `curl -s http://localhost:3000/api/tasks | python3 -c "import sys,json; [print(t['title']) for t in json.load(sys.stdin)]" | grep -i "[keyword]"`

## sortOrder Bands
- HIGH: 10–40 quick wins | 50–90 alerts | 100+ strategic
- MEDIUM: 10, 20, 30…
- Speculative: 500+

## Task Description Requirements
Every MC task must include:
1. Specific first action (URL, command, file path)
2. Why it matters
3. What done looks like

No task that just restates the title. Can't write a concrete first action → flag to JT, don't create it yet.

## Material Delta Routing
Whenever Eve implements a material delta — a new artifact, queue, research finding, proof pack, Drive bundle, automation, or decision-ready output — Mission Control must get the single optimal next-use task.

Rules:
- Add or update exactly the task that helps JT/Eve use the new material, not a generic “review this” placeholder.
- Cite the source artifact/path/link in the task description.
- Assign the real owner: JT only when he must approve, review, post, send, pay, decide, or provide input; Eve when the next action is internal execution.
- Match priority to leverage and readiness. HIGH only for near-term cash, client proof, warm opportunity, urgent risk, app distribution, health/financial stability, or a JT action needed within 48 hours.
- Include first action, why it matters, and done state.
- If no task is justified because the material is already consumed, blocked, or purely archival, log the skip reason in the work summary/daily note.
