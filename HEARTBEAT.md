# HEARTBEAT.md — Periodic Wake Behaviors

## Active Hours
8:00 AM – 11:00 PM EST. Outside these hours: HEARTBEAT_OK immediately.

## Morning Brief (7:30 AM, cron)
Deliver to JT via Telegram:
1. Read memory/tasks.md — top 3 priorities
2. Run web searches: AI news, crypto market, tech job market
3. Read memory/niche-monitor-latest.md — severity-filtered intel
4. Read ~/projects/job-market-agent/data/daily-brief.md — roles (18+/25) + skill gaps + build ideas
5. Run `python3 scripts/cost-tracker.py --brief` — include as 💰 API Costs section
6. Send: punchy bullets, one concrete action. Title: "🌅 Morning Brief — [date]"

Sections: 📋 Top 3 Priorities | 📰 Overnight News (🔴🟠 only) | 🔍 Niche Intel (🔴🟠 only) | 💼 Job Market | 💰 API Costs | 💡 One concrete action

## Heartbeat (4x/day: 10AM, 2PM, 6PM, 10PM EST, cron)
1. Check outside active hours → HEARTBEAT_OK
2. Read memory/tasks.md — urgent/overdue items?
3. Run `python3 scripts/cost-tracker.py --check-alerts` — if non-empty array, send each alert to JT via Telegram immediately
4. **10AM only — Daily Film Review (non-negotiable):**
   - Read yesterday's `memory/YYYY-MM-DD.md`
   - Find: one mistake, one friction point, or one thing that took longer than it should have
   - Write one concrete fix → appropriate file (AGENTS.md mistake rule, TOOLS.md path update, feedback.md rule, skill SKILL.md update)
   - Append one line to `memory/training/training-log.md`: `[DATE 10AM] Film: [what was reviewed] → Fix: [what was updated]`
   - If nothing to fix: note "Clear" and move on — don't skip the step
5. **10PM only — Spanish accountability check:**
   Read `~/.openclaw/workspace/spanish/state.json`.
   If `last_lesson_date` == today AND `last_lesson_complete` == false:
   → Send JT: "🇪🇸 Still need to finish tonight's Spanish lesson! 10 minutes. Reply 'lesson' to jump in now."
   Skip if lesson wasn't delivered today (cron handles that) or already complete.
6. If nothing urgent → pick one proactive work item (see below)
7. Log what you did in memory/YYYY-MM-DD.md under ## Heartbeat HH:MM

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

## Weekly Skills Audit (Sunday only — runs inside weekly-synthesis cron)
Go through every operational file, one by one. For each: is it accurate? Is anything stale, missing, or wrong?
Files to audit in order:
1. `TOOLS.md` — paths, commands, API keys. Update anything that drifted.
2. `AGENTS.md` — rules still valid? Any new patterns to add from the week?
3. `MEMORY.md` — distill week's daily notes. Remove noise. Sharpen what matters.
4. `HEARTBEAT.md` — are the proactive work priorities still right for JT's current goals?
5. All `skills/*/SKILL.md` files — are the instructions still accurate? Any new commands?
6. All `agents/*/AGENT.md` files — are the agents configured correctly? Any drift?
7. `memory/training/training-log.md` — review the week's film review entries. Are patterns emerging? Write a weekly summary line.

Audit output: append `## Skills Audit — [date]` to `memory/training/training-log.md` with one line per file: `[FILENAME]: [status: current / updated X / flagged Y]`

## Heartbeat vs Cron
- Heartbeat: batch checks, conversational context, timing can drift slightly
- Cron: exact timing, isolation needed, different model, direct channel output
