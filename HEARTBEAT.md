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

5. Run `python3 health/todays-workout.py` — include as 🏋️ Today's Workout section
5a. Check `~/.openclaw/workspace/agents/vibe-marketing/queue.jsonl` — if any entries with `"posted": false` and `"status": "approved"` exist, include a 📱 Vibe Queue section: "[N] pieces ready to post — [product names]. Check Drive for content."
6. Send: punchy bullets, one concrete action. Title: "🌅 Morning Brief — [date]"

Sections: 📋 Top 3 Priorities | 📰 Overnight News (🔴🟠 only) | 🔍 Niche Intel (🔴🟠 only) | 💼 Job Market | 💰 API Costs | 🏋️ Today's Workout | 📱 Vibe Queue (if items waiting) | 💡 One concrete action

## Heartbeat (4x/day: 10AM, 2PM, 6PM, 10PM EST, cron)
1. Check outside active hours → HEARTBEAT_OK
2. Read memory/tasks.md — urgent/overdue items?
3. Run `python3 scripts/cost-tracker.py --check-alerts` — if non-empty array, send each alert to JT via Telegram immediately
3a. **Cron health check (every heartbeat — non-negotiable):**
   - Call `cron list` and scan ALL jobs for `consecutiveErrors >= 2` OR `lastRunStatus: "error"`
   - For each failing job: diagnose the cause (timeout? bad path? missing file?) and fix it autonomously — adjust timeout, fix the payload, update the schedule as needed
   - **Timeout fix rule (mandatory):** ALWAYS run `openclaw cron edit <id> --timeout-seconds X` regardless of what prior session notes say. Never trust "already applied" from a previous session — prior sessions lose context and fixes may not have saved. Verify by checking the returned JSON shows the new value. If last run `durationMs` matches the old timeout, the fix was NOT applied.
   - If fix is non-obvious or requires JT input: alert JT via Telegram with job name + error + what you tried
   - Log what was fixed in today's daily note under ## Heartbeat HH:MM
   - Never leave a cron with consecutiveErrors >= 2 unaddressed
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

## Proactive Work Deduplication Rule
Before picking a proactive work item: read today's daily note (`memory/YYYY-MM-DD.md`).
If an item in the priority list was already logged as done today → skip it and move to the next.
Never run the same proactive item twice in one day. Check the note first, every time.

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

## Proactive Content Strategy Rule (standing — applies always, not just Sunday)
When ANY intelligence system surfaces a content format performing well in JT's community:
- Swipe cron detects trending formats (3+ appearances) or topics (1000+ combined engagement) → writes to content-signals.md
- Weekly synthesis reads format-signals.md → cross-references against what JT is posting → flags gap in Telegram + MC task if gap found
- Main session observes a format clearly getting traction during any research task → proactively recommend adding it to the content system

**The rule:** never sit on a content strategy signal. Intel → gap analysis → recommendation to JT. Don't wait to be asked.

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
8. `memory/future-signals.md` — **Future Signals Review (mandatory):** Read every active signal. For each one, check whether its trigger conditions are now met based on JT's current situation (active clients, project status, outreach volume, hardware). If a signal's trigger is met: (a) push a HIGH task to Mission Control recommending the tool/technique, (b) move it to the Graduated table with date + trigger, (c) notify JT in the weekly synthesis Telegram message. If not triggered: leave as-is. This is how "not now" becomes "now" — it must be reviewed every single week.

Audit output: append `## Skills Audit — [date]` to `memory/training/training-log.md` with one line per file: `[FILENAME]: [status: current / updated X / flagged Y]`

## Heartbeat vs Cron
- Heartbeat: batch checks, conversational context, timing can drift slightly
- Cron: exact timing, isolation needed, different model, direct channel output
