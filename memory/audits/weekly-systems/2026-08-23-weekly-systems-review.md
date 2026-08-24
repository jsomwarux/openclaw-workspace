# Weekly Systems Review — 2026-08-23

## North Star opening

- **Cash source conflict:** live Mission Control `/api/revenue` reports consulting collected **$0**, while `scripts/north_star_pipeline.py summary --json` reports legacy/current collected **$5,575**. Per the Weekly Systems Review evidence rule, do not treat the older `$5,575` figure as current collected cash until a logged payment source reconciles the two. The current gap to $10K is therefore **unverified**, not `$4,425`.
- Pipeline movement: MSI deliverables accepted/re-verified Aug 17; completion invoice MSI-002 for $5,400 sent Aug 18, due Sep 2. No other verified stage movement this week.
- Waiting-on items older than 7 days: Altmark delinquency inputs, DHCR/Matt approval, Karen expectation-reset handoff, and Maiky cost review. The pipeline summary reports one aging item, but the raw pipeline has four waiting records last touched Aug 10 or earlier; this inconsistency needs repair.

## Six outcome KPIs

1. Posts delivered vs posted: **unknown** — no current unified delivered/posted source exists. Fix: add a deterministic weekly counter over the weekly queue and posted log after the 90-day freeze ends or as part of paid delivery.
2. Engagement per posted item: **unknown** — no current-week engagement ledger exists. Fix: record platform metrics against posted-log IDs.
3. Outreach packets completed vs sent vs replied: **unknown** — no current weekly rollup source exists; outreach-pipeline ran successfully but does not expose these three counters in the cron state. Fix: emit deterministic weekly counters from the outreach state files.
4. Consulting pipeline stage movement: **1 verified movement** — MSI moved to accepted/completion-invoice-sent; no other verified movement.
5. Cron delivery rate: **60% for announce jobs (3 delivered / 5 announce jobs)**; overall latest-run success **88.9% (8/9 jobs)**. Job Market Daily is stale since Jul 8 with `not-requested`; Friday Scoreboard failed delivery.
6. Dollars spent: **$0.273 tracked 7-day model spend**; OpenRouter vs X API split is **unknown** because the weekly report does not expose provider-specific OpenRouter and X API totals.

## Cron health

- 9 enabled jobs checked; well below the 20/day invocation cap (maximum scheduled weekday load is below 20).
- Friday Scoreboard: `lastRunStatus=error`, `consecutiveErrors=4`, delivery `unknown`. Latest run failed before useful output due Codex subscription limit; reset Aug 27 at 12:13 AM EDT. No paid fallback/model-config change was authorized.
- Job Market Daily Research: latest recorded run Jul 8, status ok, output `MARKET_INTEL_ONLY`, delivery not requested. This is stale despite being enabled and needs schedule/state diagnosis.
- No timeout-near-limit conditions. No never-run jobs.
- Sunday 10 AM Weekly Systems Review remains the only 10 AM Sunday job; existing staggering noted.

## File budgets

- AGENTS.md: 27,809 / 28,000 bytes (191 bytes headroom; extract before any append).
- MEMORY.md: 8,992 / 20,000.
- TOOLS.md: 5,586 / 16,000.
- HEARTBEAT.md: 4,189 / 16,000.

## Processes and configuration

- Gateway reachable and LaunchAgent active, PID 41418.
- Gateway RSS 609,872 KB, above the 500 MB review threshold; CPU 1.2%, long-running since Friday.
- Watchdog loaded; interval 600 seconds. Gateway ThrottleInterval 10 seconds. Both settings pass.
- n8n RSS 247,584 KB; no other persistent Node process exceeded thresholds.

## Version and plugins

- Current OpenClaw: 2026.7.1-2 (0790d9f).
- GitHub releases show a release published Aug 16, newer than this Jul-series build; update is available or at minimum requires version confirmation. No update performed.
- `context-mode@context-mode` remains false.
- Extensions present: `lossless-claw` plus install-backup directory. OpenClaw reports duplicate `lossless-claw` plugin metadata and conflicting install-index metadata for brave/codex/lossless-claw. No config changes or restart performed.

## Integrity and maintenance

- mistakes log, gateway watchdog, and health SQLite exist and are readable.
- pending queue: 5 valid JSONL records, 0 corrupt lines.
- Autoresearch: only `skills/job-application/SKILL.md` materially changed in the last 7 days and it is already enrolled/stable; no new target added.
- Future signals: no active trigger verified. All app/passive-income/tooling lanes remain frozen through Nov 17 unless JT explicitly overrides.
- Passive-income pruning: Mission Control reachable; zero matching todo tasks with `Build idea:` or `[PI]` and sortOrder >=500.
- Cost review: $0.273 total tracked 7-day spend; monthly pace $1.80 vs $50 target.

## Issues fixed this run

- Produced a command-safe, evidence-backed audit artifact and line-by-line JSONL integrity result.
- Corrected the opening after heartbeat verification found a cash-source conflict between Mission Control `$0` and the legacy North Star pipeline `$5,575`; the report no longer asserts the older figure as current cash.
- No runtime/config mutations were safe or authorized. The active failures require subscription reset and a quiet plugin/gateway maintenance decision.

## Needs JT attention

1. After the Aug 27 subscription reset, allow Friday Scoreboard to run naturally on Aug 28; do not spend on a fallback just to clear metadata.
2. Diagnose the stale Job Market Daily schedule/state before its next expected run.
3. In a quiet ops window, resolve duplicate plugin install metadata and investigate gateway RSS above 500 MB. OpenClaw update requires explicit approval.

Next review: 2026-08-30.
