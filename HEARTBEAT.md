# HEARTBEAT.md — Periodic Wake Behaviors

## Active Hours
8:00 AM – 11:00 PM EST. Outside these hours: HEARTBEAT_OK immediately.

## Morning Brief (7:30 AM, cron)
Deliver to JT via Telegram:
1. Read memory/tasks.md — top 3 priorities
   **STALENESS CHECK (mandatory before surfacing any task):**
   - Any task referencing a specific content draft, Drive link, or post: check the `| Updated:` date on that task. If > 7 days old → SKIP IT, do not surface it. Stale content tasks create false urgency and JT cannot act on them.
   - Any task referencing a job application: check MEMORY.md Job Market section. If role is marked expired/deprioritized → SKIP IT.
   - Only surface tasks that are actionable TODAY with no staleness risk.
   - "One concrete action" must be derived from CURRENT reality — not from tasks.md entries older than 7 days.
2. Run web searches: AI news, crypto market, tech job market
3. Fetch `https://nashsatoshi.com/rankings` (using Cloudflare /crawl or Firecrawl) to extract the Top Ranked tokens. Draft ONE X post for the Nash Satoshi account. MANDATORY: You must rotate the format based on the current Day of the Week to prevent staleness:
   - Monday: The Leaderboard (Top 3 + game theory scores)
   - Tuesday: Single Asset Spotlight (Focus exclusively on #1, why the 4-model consensus picked it)
   - Wednesday: Anti-Bias Hot Take (Why relying on single-model ChatGPT analysis is dangerous vs Nash Satoshi's ensemble)
   - Thursday: The Methodology (How Claude, GPT, Gemini, and Grok cross-examine each other)
   - Friday: Momentum (Which new token broke into the top rankings recently)
   - Weekends: Aggressive UVP (Short, punchy fact about game-theory edge + no preamble)
   Apply `content-generation/SKILL.md` formatting rules. Include as 🐦 Daily Nash Satoshi X Post section.

4. Read `memory/content/dynasty-strategy.md` — generate ONE elite-tier X post for the @dynastyjig account targeting the "Systems over Symptoms" narrative (Algorithmic Exploits, Roster Construction Economics, or Draft Capital Arbitrage). Apply `skills/content-generation/SKILL.md` formatting. Include as 🏈 Daily Dynasty Strategy X Post section.

3. Read memory/niche-monitor-latest.md — severity-filtered intel
4. Read ~/projects/job-market-agent/data/daily-brief.md — roles (18+/25) + skill gaps + build ideas
5. Run `python3 scripts/cost-tracker.py --brief` — include as 💰 API Costs section

5. Run `python3 health/todays-workout.py` — include as 🏋️ Today's Workout section
5a. Check `~/.openclaw/workspace/agents/vibe-marketing/queue.jsonl` — if any entries with `"posted": false` and `"status": "approved"` exist, include a 📱 Vibe Queue section: "[N] pieces ready to post — [product names]. Check Drive for content."
6. Send: punchy bullets, one concrete action. Title: "🌅 Morning Brief — [date]"

5b. **Weekly outreach count check (every Monday morning brief only):**
   - Read all shortlist files in ~/projects/jt-consulting-pipeline/shortlists/ and count entries with M1 sent in the past 7 days
   - If count < 10: include ⚠️ Outreach Volume alert: "Only [N] DMs sent this week — target is 15. Pipeline needs fuel."
   - If count ≥ 15: include ✅ Outreach on track: "[N] DMs sent this week."

5c. **Relationship check (every Monday morning brief only):**
   - Read memory/networking/contacts.md
   - Apply warmth decay: any Hot contact not touched in 7+ days → flag
   - Any overdue next actions → flag
   - Include 🤝 Relationship section if anything needs attention

5d. **Event scout (first Monday of each month only):**
   - Search Eventbrite NYC for: "construction technology", "property management", "AI business NYC", "real estate tech NYC"
   - Check brooklynchamber.com/events and nycchamber.com/events for that month
   - If any relevant event found: push to MC as HIGH task with date, venue, ICP relevance
   - Append to memory/networking/events.md
   - Include 📅 Events section in morning brief if anything found

Sections: 📋 Top 3 Priorities | 📰 Overnight News | 🔍 Niche Intel | 💼 Job Market | 💰 API Costs | 🏋️ Today.s Workout | 📱 Vibe Queue | 🐦 Daily Nash Satoshi X Post | 🏈 Daily Dynasty Strategy X Post | 💡 One concrete action

## Heartbeat (4x/day: 10AM, 2PM, 6PM, 10PM EST, cron)
1. Check outside active hours → HEARTBEAT_OK
2. Read memory/tasks.md — urgent/overdue items?
3. Run `python3 scripts/cost-tracker.py --check-alerts` — if non-empty array, send each alert to JT via Telegram immediately
3a. **Cron health check (every heartbeat — non-negotiable):**
   - Call `cron list` and scan ALL jobs for `consecutiveErrors >= 2` OR `lastRunStatus: "error"`
   - For any user-facing critical job (morning brief, Spanish lesson, outreach pipeline, cost/security alert), verify latest `openclaw cron runs --id <id> --limit 1` delivery fields when status looks suspicious; `lastRunStatus: ok` is not enough if `deliveryStatus` failed or `deliveryError` exists.
   - For each failing job: diagnose the cause (timeout? bad path? missing file? delivery timeout?) and fix it autonomously — adjust timeout, fix the payload, update the schedule as needed; if delivery failed but content was generated, resend the output manually via Telegram and log it.
   - **Timeout fix rule (mandatory):** ALWAYS run `openclaw cron edit <id> --timeout-seconds X` regardless of what prior session notes say. Never trust "already applied" from a previous session — prior sessions lose context and fixes may not have saved. Verify by checking the returned JSON shows the new value. If last run `durationMs` matches the old timeout, the fix was NOT applied.
   - **Timeout sizing rule:** When a cron consistently times out (2+ runs), do NOT just bump by 50% and wait. Read the job's AGENT.md or payload to estimate full expected runtime (count steps + file reads + API calls + uploads), then set timeout to cover the full runtime + 20% buffer. One correct value, not iterative guesses.
   - If fix is non-obvious or requires JT input: alert JT via Telegram with job name + error + what you tried
   - Log what was fixed in today's daily note under ## Heartbeat HH:MM
   - Never leave a cron with consecutiveErrors >= 2 unaddressed

3b. **Missed cron check (10AM heartbeat only — after 7AM so crypto window has passed):**
   - From `cron list`, check `lastRunAtMs` for these two critical daily jobs:
     - `eve-crypto-morning-008` (should fire at 6AM daily)
     - `651fa1da` outreach-pipeline (should fire at 2AM daily)
   - For crypto: if `lastRunAtMs` is not from today (compare date portion to current date) → fire it immediately via `cron run` with jobId `eve-crypto-morning-008` + alert JT: "⚠️ Crypto cron missed its 6AM slot — fired now."
   - For outreach: if `lastRunAtMs` is not from today AND `lastRunStatus` is not `error` (errors are caught by 3a) → fire it immediately + alert JT.
   - "Not from today" = `lastRunAtMs` date portion ≠ today's date in America/New_York timezone.
   - Log any fires in today's daily note under ## Heartbeat HH:MM.
4. **10AM only — Daily Film Review (non-negotiable, Kobe Protocol):**
   - Read yesterday's `memory/YYYY-MM-DD.md`
   - **Step A — Failure scan:** Find one mistake, one friction point, or one thing that took longer than it should have. Write one concrete fix → appropriate file (AGENTS.md mistake rule, TOOLS.md path update, feedback.md rule, skill SKILL.md update). The fix is incomplete unless it includes a regression check + owner surface in `docs/agents/regression-checks.md` or in the affected skill/cron checklist.
   - **Step A2 — Repeat check:** Scan yesterday's daily note + `docs/agents/mistakes-log-recent.md` for repeat terms (`mistake`, `missed`, `stale`, `timeout`, `hallucinated`, `duplicate`, `failed`, `incorrect`). If a failure pattern appeared twice in the last 14 days, promote it to `docs/agents/regression-checks.md` and update the owner surface.
   - **Step B — Proactive improvement (even when nothing broke):** Ask "what could be sharper?" Pick ONE thing from this priority list and make one targeted improvement:
     1. The most-run skill or cron that hasn't been autoresearched yet → draft or update its checklist in `agents/autoresearch/checklists/`
     2. A rule in AGENTS.md or HEARTBEAT.md that's vague or hard to follow → tighten the language
     3. A prompt in any cron payload that produced mediocre output this week → improve one instruction
     4. A TOOLS.md entry that's stale or missing a key command → update it
     5. A pattern from this week's sessions that should be a rule but isn't yet → write the rule
   - Step B is mandatory even if Step A is "Clear." Kobe watched film after 40-point games too.
   - Append one line to `memory/training/training-log.md`: `[DATE 10AM] Film: [what was reviewed] → Fix: [Step A result] | Improve: [Step B result]`
   - If genuinely nothing to improve after honest review: note "Clear" — but this should be rare.
4a. **10AM only — Spanish lesson delivery check:**
   Run: `openclaw cron runs --id babd905a-1098-49dd-8700-772fef14f817 --limit 1`
   If last run entry has `deliveryError` or `deliveryStatus` != "delivered" → resend lesson from `spanish/lessons/YYYY-MM-DD.md` (use yesterday's date) to JT via Telegram immediately.
   State.json only tracks execution completion, not delivery. This is the only reliable delivery check.
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

## Heartbeat Log Idempotency Rule
Before appending a heartbeat section to `memory/YYYY-MM-DD.md`, check whether the exact `## Heartbeat HH:MM` section already exists.
- If it exists and the new check adds no materially new facts, do not append a duplicate section; update the existing line only if needed.
- If the reminder fires twice within 5 minutes, treat it as a duplicate unless cost/cron/Spanish state changed.
- Regression check: daily film review scans yesterday's note for duplicate `## Heartbeat HH:MM` headings and tightens this rule if duplicates recur.

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
- Weekly synthesis reads content-signals.md → cross-references against what JT is posting → flags gap in Telegram + MC task if gap found
- Main session observes a format clearly getting traction during any research task → proactively recommend adding it to the content system

**The rule:** never sit on a content strategy signal. Intel → gap analysis → recommendation to JT. Don't wait to be asked.

## Content → Consulting Niche Feedback Rule (Sunday synthesis only)
During weekly synthesis, after reading content-signals.md:
- Identify any topic (not just format) that appeared in 3+ high-engagement swipe file entries this week
- Cross-reference: does this topic overlap with JT's consulting niches (construction, wholesale, PM, insurance)?
- If yes AND it's a topic JT hasn't posted about yet → flag as content gap + consulting credibility gap in Telegram
- If yes AND JT has posted about it → note engagement pattern; if it outperformed other posts, recommend adding a related case study to the Wednesday LinkedIn queue
- If the high-engagement topic is a NEW niche not in JT's current matrix → log to memory/niche-fitness-signals.md for monthly niche fitness review
The goal: let content performance data tell you which consulting angles are resonating before you invest more outreach time in them.

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
7a. `docs/agents/regression-checks.md` — **Regression Check Audit (mandatory):** verify each repeatable mistake has a guardrail, owner surface, and check cadence. Scan recent daily notes + mistakes log for repeated failure terms. Any repeated pattern without an Active Check must be promoted before the audit is complete.
8. `memory/future-signals.md` — **Future Signals Review (mandatory):** Read every active signal. For each one, check whether its trigger conditions are now met based on JT's current situation (active clients, project status, outreach volume, hardware). If a signal's trigger is met: (a) push a HIGH task to Mission Control recommending the tool/technique, (b) move it to the Graduated table with date + trigger, (c) notify JT in the weekly synthesis Telegram message. If not triggered: leave as-is. This is how "not now" becomes "now" — it must be reviewed every single week.
9. **Autoresearch enrollment check (mandatory):** Read `agents/autoresearch/targets.md`. Cross-reference against all skills in `skills/` and agents in `agents/` installed or updated this week (check file modification dates via `ls -lt`). For any skill/agent NOT already in targets.md, run the 3-question candidacy check: (1) runs repeatedly? (2) output scoreable with yes/no? (3) clear failure mode? All 3 yes → draft checklist, save to `agents/autoresearch/checklists/[slug].md`, append to targets.md with status `pending`. Log enrollments in the audit output.
10. **Passive income idea queue pruning (mandatory):** Check Mission Control for tasks with title containing "Build idea:" or "[PI]" and sortOrder ≥ 500, status = todo, age > 60 days. For each: (a) does JT's current situation (active clients, skill gaps, hardware, runway) make this more or less viable than when it was created? (b) If clearly less viable or superseded by a better idea: mark as done with note "pruned in weekly synthesis — [reason]." (c) If now viable: bump to sortOrder 400 and flag in Telegram. Goal: never let the idea queue exceed 15 active entries — prune to make room for new ones.

Audit output: append `## Skills Audit — [date]` to `memory/training/training-log.md` with one line per file: `[FILENAME]: [status: current / updated X / flagged Y]`

## Heartbeat vs Cron
- Heartbeat: batch checks, conversational context, timing can drift slightly
- Cron: exact timing, isolation needed, different model, direct channel output
