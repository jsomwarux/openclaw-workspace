# Job State: Job Market Daily Research

- Last completed run: 2026-09-16T08:47:00-04:00
- Cursor: rolling 30-day window 2026-08-18 through 2026-09-16; next run retains a rolling 30-day window and does not exclude still-live roles by cursor
- Open items: Litmos AI Program Manager surfaced at 22/25 for JT review; Bloomberg and Janus Henderson applications were submitted by JT on 2026-09-08.
- Last failure: no run-level failure; initial unquoted query invocations exited with argparse errors, then all 12 searches were rerun successfully; aggregate search health passed
- Started marker: clear
- Next expected run: 2026-09-17T05:15:00-04:00
- Legacy definition: `config/cron-snapshots/job-pipeline-legacy-before-reactivation-2026-08-22.json`

## Latest Run

- Run timestamp: 2026-09-16T08:39:00-04:00 through 2026-09-16T08:47:00-04:00
- Searches executed: 12 rolling-month broad query families with 15 results requested per query; 11 returned 15 results and the Greenhouse-only query returned 3. Six targeted validation searches plus direct live-posting, ATS API, and verifier checks followed.
- URLs checked: 165 unique discovery URLs from 168 raw search results; every URL and outcome is recorded in the run audit.
- Surfaced roles: 0. No newly discovered role passed every evidence, location, compensation, credential, and live-application gate; Litmos remained live but was a prior surfaced duplicate.
- Artifacts: `/Users/jtsomwaru/projects/job-market-agent/data/daily-brief.md`; `/Users/jtsomwaru/projects/job-market-agent/data/job-opportunities.md` (checked, unchanged); `/Users/jtsomwaru/projects/job-market-agent/data/search-results/2026-09-16-job-market-audit.md`; `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/job-market-daily-research.md`.
- Failures: no run-level failure. Initial search invocations omitted whole-query shell quoting and exited with argparse errors; all 12 required searches were immediately rerun successfully. Several non-qualifying pages were stale, redirected, or blocked and are recorded individually.
- Cursor/date: rolling 30-day window 2026-08-18 through 2026-09-16
- Proof log: `3d01a7cf`
- Next run: 2026-09-17T05:15:00-04:00

## Recent Runs

- 2026-09-16 08:47 ET: twelve broad rolling-month searches produced 168 raw results and 165 unique URLs; no evidence-backed role cleared every gate.
- 2026-09-14 05:22 ET: twelve broad rolling-month searches produced 165 raw results and 163 unique URLs; Litmos AI Program Manager surfaced at 22/25.
- 2026-09-11 05:20 ET: twelve broad rolling-month searches produced 171 raw results and 163 unique URLs; no evidence-backed role cleared every gate.
- 2026-09-10 05:27 ET: twelve broad rolling-month searches produced 180 raw results and 175 unique URLs; no evidence-backed role cleared every gate.
- 2026-09-09 05:24 ET: twelve broad rolling-month searches produced 180 raw results and 175 unique URLs; no evidence-backed role cleared 20/25, with Chime closest at 19/25.
- 2026-09-08 12:42 ET: twelve broad rolling-month searches produced 173 unique raw URLs; 178 candidate or validation URLs were audited and Bloomberg AI Enablement Lead, External Relations surfaced at 22/25.
- 2026-09-08 05:32 ET: twelve broad rolling-month searches produced 177 unique raw URLs and 180 candidate or validation URLs were audited; same-day correction marked Babylist expired, so no role cleared every gate.
- 2026-09-07 05:27 ET: twelve broad rolling-month searches produced 169 unique raw URLs; 134 candidate URLs were audited and Janus Henderson Investors AI Enablement Partner surfaced at 21/25.
- 2026-09-02 05:26 ET: twelve broad rolling-month searches plus eight targeted validations produced 266 unique raw URLs and 139 unique candidate URLs checked; no evidence-backed role cleared every gate.
- 2026-09-01 05:20 ET: twelve broad rolling-month searches plus eight targeted validations produced 166 unique discovery URLs and 187 unique total URLs checked; no evidence-backed role cleared every gate.
- 2026-08-31 05:28 ET: twelve broad rolling-month searches plus eight targeted validations produced 165 unique discovery URLs and 171 unique total URLs checked; no evidence-backed role cleared every gate.
- 2026-08-28 05:23 ET: twelve broad rolling-month searches plus four targeted validations produced 177 unique discovery URLs and 189 unique total URLs checked; no evidence-backed role cleared every gate.
