# HEARTBEAT.md — Periodic Wake Behaviors

## Active Hours
8:00 AM – 11:00 PM EST. Outside these hours: HEARTBEAT_OK immediately.

## Morning Brief (7:30 AM, cron)
Deliver to JT via Telegram:
1. Run `python3 scripts/mission_control_north_star_audit.py`, then pull active high-priority tasks from `http://localhost:3000/api/tasks`. Use `memory/tasks.md` only as legacy fallback/context if Mission Control is unreachable.
2. Follow `docs/agents/heartbeat-extended-rules.md` Morning Brief gates for staleness, fresh web search, Nash Satoshi, @dynastyjig, Monday outreach/relationship checks, and first-Monday event scouting.
3. Read `memory/reminders.jsonl` if it exists. Include any reminder whose `date` equals today's America/New_York date; top-priority reminders go at the top of the priorities section.
4. Read `memory/niche-monitor-latest.md`, `~/projects/job-market-agent/data/daily-brief.md`, run `python3 scripts/cost-tracker.py --brief`, run `python3 health/todays-workout.py`, and check approved Vibe queue items.
5. Send punchy bullets with one action. Sections: priorities, news, niche intel, jobs, costs, workout, vibe queue, Nash X+Reddit full drafts when generated, Dynasty X, one action.

## Heartbeat (4x/day: 10AM, 2PM, 6PM, 10PM EST, cron)
1. Check outside active hours → HEARTBEAT_OK
2. Run `python3 scripts/mission_control_north_star_audit.py`, then inspect Mission Control active high/overdue tasks via `http://localhost:3000/api/tasks` (`memory/tasks.md` fallback only).
3. Run `python3 scripts/cost-tracker.py --check-alerts` — if non-empty array, send each alert to JT via Telegram immediately
4. Follow `docs/agents/heartbeat-extended-rules.md` for cron health fixes, 10AM missed-cron checks, 10AM film review, and Spanish checks.
5. If nothing urgent → pick one proactive work item (see below)
6. Log what you did in `memory/YYYY-MM-DD.md` under `## Heartbeat HH:MM`

## Proactive Work Deduplication Rule
Before picking a proactive work item: read today's daily note (`memory/YYYY-MM-DD.md`).
If an item in the priority list was already logged as done today → skip it and move to the next.
Never run the same proactive item twice in one day. Check the note first, every time.

## Heartbeat Log Idempotency Rule
Before appending a heartbeat section to `memory/YYYY-MM-DD.md`, check whether the exact `## Heartbeat HH:MM` section already exists. If it exists and nothing materially changed, do not append a duplicate; update the existing line only if needed. Treat reminders within 5 minutes as duplicates unless cost/cron/Spanish state changed. Regression check: daily film review scans yesterday's note for duplicate headings.

## Proactive Work (priority order when idle)
1. Client/market research → memory/research/
2. AI tool monitoring → memory/ai-tools.md
3. Crypto monitoring → memory/crypto.md
4. Job market pulse → memory/job-market.md
5. Content drafting → memory/drafts/
6. Memory maintenance → distill daily notes to MEMORY.md

## Severity Triage
🔴 Critical = act today | 🟠 High = important today | 🟡 Medium = KB only | 🟢 Low = background

Morning brief + immediate alerts: 🔴🟠 only. 🔴 triggers immediate Telegram.

## Content Feedback Loop
Never sit on a content strategy signal. See `docs/agents/heartbeat-extended-rules.md` for content gap analysis, consulting niche feedback, and Sunday synthesis routing.

## Sunday Weekly Split
**Weekly Intelligence Synthesis (8AM):** intelligence only — niche/job/content signals, strategic recommendation, and `memory/content/weekly-intel-brief.md`. Do NOT run systems maintenance here.

**Weekly Systems Review (10AM):** systems maintenance only. See `docs/agents/heartbeat-extended-rules.md` for exact scope, future-signal handling, PI pruning, and training-log output.
