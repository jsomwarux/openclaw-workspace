# Job State: Job Market Daily Research

- Last completed run: 2026-08-26T05:23:07-04:00
- Cursor: rolling 30-day window 2026-07-28 through 2026-08-26; next run retains a rolling 30-day window and does not exclude still-live roles by cursor
- Open items: none
- Last failure: none; search health passed with 146 unique discovery URLs
- Started marker: clear
- Next expected run: 2026-08-27T05:15:00-04:00
- Legacy definition: `config/cron-snapshots/job-pipeline-legacy-before-reactivation-2026-08-22.json`

## Latest Run

- Run timestamp: 2026-08-26T05:23:07-04:00
- Searches executed: 10 rolling-month searches — senior BSA AI/automation; AI operations program management; intelligent automation/workflow transformation; AI adoption/enablement; AI governance/quality operations; Greenhouse AI implementation program management; Lever AI enablement management; Ashby workflow automation leadership; Workday AI adoption management; SmartRecruiters AI transformation management.
- URLs checked: 146 unique discovery URLs; every URL and outcome is logged in `daily-brief.md`.
- Surfaced roles: 0. Search health passed, but no role passed the direct named-proof, location, compensation, seniority, coding, and active-posting gates.
- Artifacts: `/Users/jtsomwaru/projects/job-market-agent/data/daily-brief.md`; `/Users/jtsomwaru/projects/job-market-agent/data/job-opportunities.md` (unchanged); `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/job-market-daily-research.md`
- Failures: none. Search health passed. No role reached the surfacing gate, so no `verify-live-posting.py` surfaced-role check was required.
- Cursor/date: rolling 30-day window 2026-07-28 through 2026-08-26
- Next run: 2026-08-27T05:15:00-04:00

## Recent Runs

- 2026-08-26 05:23 ET: ten rolling-month searches checked 146 unique discovery URLs; no evidence-backed role cleared every gate, and `job-opportunities.md` remained unchanged.
- 2026-08-25 05:22 ET: ten rolling-month searches checked 147 unique discovery URLs; no evidence-backed role cleared every gate, and `job-opportunities.md` remained unchanged.
- 2026-08-24 13:48 ET: ten rolling-month searches checked 127 unique candidate postings; exact-JD re-review retained Anthropic as a 20/25 stretch application, not a clean fit or automatic rejection.
- 2026-08-24 05:17 ET: seven fresh searches completed; no posting URLs returned and no evidence-backed 20+/25 roles surfaced.
- 2026-08-22: state initialized before approved reactivation; no research run performed in this session.
