# Job State: Job Market Daily Research

- Last completed run: 2026-08-31T05:28:26-04:00
- Cursor: rolling 30-day window 2026-08-02 through 2026-08-31; next run retains a rolling 30-day window and does not exclude still-live roles by cursor
- Open items: none
- Last failure: none; search health passed with 165 unique broad-discovery URLs and 171 unique total URLs checked
- Started marker: clear
- Next expected run: 2026-09-01T05:15:00-04:00
- Legacy definition: `config/cron-snapshots/job-pipeline-legacy-before-reactivation-2026-08-22.json`

## Latest Run

- Run timestamp: 2026-08-31T05:28:26-04:00
- Searches executed: 20 command executions — 12 rolling-month broad searches and 8 targeted validation searches covering the closest candidates and direct-employer paths.
- URLs checked: 171 unique total — 165 unique broad-discovery URLs plus 6 additional unique validation/mirror URLs; every URL and outcome is logged in `daily-brief.md`.
- Surfaced roles: 0. Search health passed, but no role passed the direct named-proof, active-path, location, compensation, seniority, coding, credential, and company-quality gates.
- Artifacts: `/Users/jtsomwaru/projects/job-market-agent/data/daily-brief.md`; `/Users/jtsomwaru/projects/job-market-agent/data/job-opportunities.md` (unchanged); `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/job-market-daily-research.md`
- Failures: none. No role reached the surfacing gate, so no `verify-live-posting.py` surfaced-role check was required.
- Cursor/date: rolling 30-day window 2026-08-02 through 2026-08-31
- Next run: 2026-09-01T05:15:00-04:00

## Recent Runs

- 2026-08-31 05:28 ET: twelve broad rolling-month searches plus eight targeted validations produced 165 unique discovery URLs and 171 unique total URLs checked; no evidence-backed role cleared every gate, and `job-opportunities.md` remained unchanged.
- 2026-08-28 05:23 ET: twelve broad rolling-month searches plus four targeted validations produced 177 unique discovery URLs and 189 unique total URLs checked; no evidence-backed role cleared every gate, and `job-opportunities.md` remained unchanged.
- 2026-08-27 05:23 ET: twelve rolling-month searches produced 174 unique discovery URLs and 175 total URLs checked; no evidence-backed role cleared every gate, and `job-opportunities.md` remained unchanged.
- 2026-08-26 05:23 ET: ten rolling-month searches checked 146 unique discovery URLs; no evidence-backed role cleared every gate, and `job-opportunities.md` remained unchanged.
- 2026-08-25 05:22 ET: ten rolling-month searches checked 147 unique discovery URLs; no evidence-backed role cleared every gate, and `job-opportunities.md` remained unchanged.
- 2026-08-24 13:48 ET: ten rolling-month searches checked 127 unique candidate postings; exact-JD re-review retained Anthropic as a 20/25 stretch application, not a clean fit or automatic rejection.
- 2026-08-24 05:17 ET: seven fresh searches completed; no posting URLs returned and no evidence-backed 20+/25 roles surfaced.
- 2026-08-22: state initialized before approved reactivation; no research run performed in this session.

