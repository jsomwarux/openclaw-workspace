# HEARTBEAT.md — Periodic Wake Behaviors

## Active Hours
8:00 AM – 11:00 PM EST. Outside these hours: HEARTBEAT_OK immediately.

## Morning Brief (7:30 AM, cron)
Deliver to JT via Telegram:
1. Run `python3 scripts/mission_control_north_star_audit.py`, then pull active high-priority tasks from `http://localhost:3000/api/tasks`. Use `memory/tasks.md` only as legacy fallback/context if Mission Control is unreachable.
   **STALENESS CHECK:** content/Drive/post tasks updated >7 days ago → SKIP; expired/deprioritized job apps → SKIP; one concrete action must reflect current Mission Control reality.
2. Run web searches: AI news, crypto market, tech job market. For current/fresh searches, use canonical local search: `set -a; source ~/.config/env/global.env; set +a; python3 /Users/jtsomwaru/.openclaw/workspace/scripts/web_search.py "QUERY" --freshness day --count 5 --json`. Do not use managed `web_search` with freshness/date filters.
3. **Daily Nash Satoshi gate:** fetch `https://nashsatoshi.com/rankings` live. If ranks/scores unavailable, SKIP. Pull pattern inputs before drafting:
   - Notion: `set -a; source ~/.config/env/global.env; set +a; python3 scripts/notion-swipe-fetch.py --platform X --niche "Crypto" --niche "AI Agents" --niche "x402" --niche "Nash Satoshi" --limit 12 --min-engagement 0 --since-days 14`
   - X: `cd ~/.openclaw/workspace/skills/x-research && source ~/.config/env/global.env && bun run x-search.ts search "(AI agent tokens OR crypto AI agents OR x402 OR DeFAI OR verifiable inference) -airdrop -giveaway -whitelist" --quick --sort likes --since 7d --limit 10`
   - <3 usable current inputs → label `RECENT_NASH_SWIPE_GAP`; use archived examples only as mechanics, not trend proof.
   X must be token-specific, reply-hook first, dwell-friendly, repost-worthy, no links/hashtags/hype. Reddit: community-native, discussion-first, non-promo, different from X, with `SUBREDDIT:` + rationale or `SUBREDDIT: SKIP — [reason]`. Include Nash only when non-generic. Save output/skip reason to `memory/app-marketing/daily-nash/YYYY-MM-DD.md`. **Delivery requirement:** the Morning Brief must include the FULL Daily X Post text and FULL Daily Reddit Draft inline (subreddit/rationale, title, and body). Do not replace drafts with a file path, summary, teaser, or “saved to” line only.

4. **Daily @dynastyjig gate:** read sports-gm skill/targets + latest report/snapshot + fresh X/sports swipe. Include `Native pattern teardown` + `Rejected generic patterns`; draft from native syntax, not topics. Public draft needs current player/news/market specificity (player, rookie tier, team, pick range, betting market, rank gap, card/unit/leg) or `SKIP_SLOT`. Products invisible; no broad rebuild/parlay aphorisms.

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
   - Read `memory/networking/contacts.md` and `memory/clients/proof-pipeline-gates.md`.
   - Apply warmth decay: any `🔥 Hot` contact not touched in 7+ days → flag; any `🧊 Stale` contact with a current high-priority MC task → flag as “refresh before ask.”
   - Flag overdue next actions, but label the action type: `relationship refresh`, `validation-only`, or `referral/proof ask`.
   - Before surfacing any referral/proof ask, verify the relevant gate allows it. If blocked, surface the blocker instead of the draft ask.
   - Include 🤝 Relationship section only when there is one concrete next action or blocker; do not create duplicate strategy tasks.

5d. **Event scout (first Monday of each month only):**
   - Read `memory/networking/events.md` first and use its Event Scouting Checklist.
   - Search Eventbrite NYC for: "construction technology", "property management", "AI business NYC", "real estate tech NYC".
   - Check brooklynchamber.com/events and nycchamber.com/events for that month.
   - Push a HIGH MC task only when the event has exact date/venue, clear buyer/operator ICP relevance, and a specific reason JT should attend.
   - Append researched results or “no strong event found” to `memory/networking/events.md`, and include 📅 Events section only for actionable events.

Sections: priorities, news, niche intel, jobs, costs, workout, vibe queue, Nash X+Reddit full drafts, Dynasty X, one action

## Heartbeat (4x/day: 10AM, 2PM, 6PM, 10PM EST, cron)
1. Check outside active hours → HEARTBEAT_OK
2. Run `python3 scripts/mission_control_north_star_audit.py`, then inspect Mission Control active high/overdue tasks via `http://localhost:3000/api/tasks` (`memory/tasks.md` fallback only).
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
   - From `cron list`, check `lastRunAtMs` for critical dailies: `eve-crypto-morning-008` (6AM) and `651fa1da` outreach-pipeline (2AM).
   - For crypto: if `lastRunAtMs` is not from today (compare date portion to current date) → fire it immediately via `cron run` with jobId `eve-crypto-morning-008` + alert JT: "⚠️ Crypto cron missed its 6AM slot — fired now."
   - For crypto even when `lastRunStatus=ok` / `deliveryStatus=delivered`: verify the latest run explicitly sent the recommendation payload (`telegram_message_sent=true` + summary text), or manually read `/Users/jtsomwaru/projects/crypto-agent/data/telegram-summary.txt` and resend it via Telegram. Do not trust cron delivery metadata alone for this job.
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
   Then run `python3 /Users/jtsomwaru/.openclaw/workspace/scripts/spanish_state_check.py --max-age-days 2`. If it fails, fix the state/lesson artifact or alert JT with the exact failure.
   State.json only tracks execution completion, not delivery. Cron run delivery history is the reliable delivery check; `spanish_state_check.py` is the persistence/freshness check.
5. **10PM only — Spanish accountability check:**
   Read `~/.openclaw/workspace/spanish/state.json` and run `python3 /Users/jtsomwaru/.openclaw/workspace/scripts/spanish_state_check.py --date $(date +%F) --require-today`.
   If the validation fails, alert JT: "⚠️ Spanish lesson state check failed: [exact failure]." Do not send a completion reminder off stale/broken state.
   If validation passes AND `last_lesson_date` == today AND `last_lesson_complete` == false:
   → Send JT: "🇪🇸 Still need to finish tonight's Spanish lesson! 10 minutes. Reply 'lesson' to jump in now."
   Skip if lesson wasn't delivered today (cron handles that) or already complete.
6. If nothing urgent → pick one proactive work item (see below)
7. Log what you did in memory/YYYY-MM-DD.md under ## Heartbeat HH:MM

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

## Sunday Weekly Split
**Weekly Intelligence Synthesis (8AM):** intelligence only — niche/job/content signals, strategic recommendation, and `memory/content/weekly-intel-brief.md`. Do NOT run systems maintenance here.

**Weekly Systems Review (10AM):** owns maintenance — cron health, file budgets, process/config/plugin checks, cost review, training/regression drift, autoresearch enrollment, `memory/future-signals.md`, and passive-income idea pruning. If a future signal triggers: push HIGH MC task, move it to Graduated with date+trigger, and report it in the systems review. For old `[PI]`/`Build idea:` tasks sortOrder ≥500 and age >60 days: prune stale/superseded ideas or bump newly viable ones to sortOrder 400.

Audit output: append a concise `## Weekly Systems Review — [date]` line to `memory/training/training-log.md` covering files checked, fixes, and deferred blockers.

