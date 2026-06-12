# Heartbeat Extended Rules

Detailed rules extracted from `HEARTBEAT.md` to keep the bootstrap file below budget. `HEARTBEAT.md` remains authoritative for when these rules apply.

## Morning Brief Gates
- **Staleness:** content/Drive/post tasks updated >7 days ago → skip; expired/deprioritized job apps → skip; one concrete action must reflect current Mission Control reality.
- **Fresh search:** use `scripts/web_search.py` with freshness filters; do not use managed `web_search` for freshness/date filters.
- **Daily Nash Satoshi:** fetch `https://nashsatoshi.com/rankings`; if unavailable, skip. Read `docs/x-algorithm.md`, `memory/content-voice.md`, and Nash X optimization rules. Pull Notion swipe refs and X research. Require ≥1 live ranking delta, named token, model disagreement, market context, or methodology proof. Generic hype, copied cadence, proof:none, or repeated ranking-update phrasing → `SKIP_SLOT`. Save output/skip reason to `memory/app-marketing/daily-nash/YYYY-MM-DD.md`. As of JT's 2026-06-11 Phase 5 override, Morning Brief includes only the first 2 lines of the Nash X post and Reddit draft plus file path and Drive link; full text appears only when selected as one of the capped Send Queue items.
- **Daily @dynastyjig:** read sports-gm skill/targets, latest report/snapshot, and fresh sports/X swipe. Include `Native pattern teardown` + `Rejected generic patterns`. Public drafts need current player/news/market specificity or `SKIP_SLOT`; products stay invisible.
- **Monday outreach count:** count shortlist M1 sends in past 7 days; alert if <10, mark on track if ≥15.
- **Monday relationship check:** read `memory/networking/contacts.md` and proof pipeline gates. Flag hot contacts not touched in 7+ days, stale contacts tied to high-priority MC tasks, and overdue next actions. Verify proof/referral gates before surfacing any ask.
- **First Monday event scout:** read `memory/networking/events.md`; search Eventbrite/Brooklyn Chamber/NYC Chamber for ICP-relevant events. Push a HIGH task only with exact date/venue, buyer/operator relevance, and a specific attendance reason.

## Heartbeat Checks
- **Cron health:** scan all jobs for `consecutiveErrors >= 2` or `lastRunStatus=error`. For suspicious user-facing critical jobs, verify latest `openclaw cron runs --id <id> --limit 1` delivery fields; `lastRunStatus=ok` alone is not enough.
- **Cron fixes:** diagnose root cause; fix autonomously when safe. For timeouts, run `openclaw cron edit <id> --timeout-seconds X` and verify returned JSON. Size timeout from actual expected runtime + 20% buffer.
- **Missed 10AM cron check:** verify crypto morning (`eve-crypto-morning-008`) and outreach pipeline (`651fa1da`) ran today; fire/alert if missed. For crypto, confirm the actual recommendation payload was sent, not only metadata.
- **10AM film review:** read yesterday's daily note, find one failure/friction point, write a concrete fix to the owner surface, and add/verify a regression check. If yesterday includes a Nightly Leverage Report, verify it either contains a concrete `Material delta` versus the prior two nightly runs or uses `NO_ACTION_NEEDED`; if it repeats the same client/project/blocker with no new input/evidence, patch `nightly-autonomous-leverage-agent` before accepting the report. If the friction was active-conversation delay, verify `docs/agents/regression-checks.md` includes the active Telegram stall row and treat any live JT message as blocking all heartbeat/proactive work until answered. Also make one targeted proactive improvement unless genuinely clear. Append one line to `memory/training/training-log.md`.
- **Spanish checks:** while Spanish is active, verify daily lesson delivery from cron run history and validate `spanish/state.json`; send completion reminder only when today's lesson was delivered and remains incomplete.

## Content Feedback Loop
- Swipe/content intelligence that shows a repeated high-performing format or topic must become gap analysis + recommendation, not passive notes.
- Sunday synthesis cross-references high-engagement topics with consulting niches and routes gaps to content, Wednesday LinkedIn case studies, or niche-fitness signals.

## Weekly Systems Review
- Systems review owns cron health, file budgets, process/config/plugin checks, cost review, training/regression drift, autoresearch enrollment, `memory/future-signals.md`, and passive-income idea pruning.
- Run `python3 scripts/cron_volume_guard.py`; if it fails, prune/consolidate nonessential schedules or create one explicit Mission Control blocker with the top offending schedules.
- If a future signal triggers, push a HIGH MC task, move it to Graduated with date+trigger, and report it.
- For old `[PI]`/`Build idea:` tasks sortOrder ≥500 and age >60 days, prune stale/superseded ideas or bump newly viable ones to sortOrder 400.
- Append `## Weekly Systems Review — [date]` to `memory/training/training-log.md` covering files checked, fixes, and deferred blockers.
