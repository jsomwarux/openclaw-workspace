# Weekly Systems Review — 2026-08-09

## North Star Scoreboard
- Cash source conflict: live Mission Control `/api/revenue` reports `metrics.consultingCollected: 0` for August, while `scripts/north_star_pipeline.py summary --json` still reports `current_collected: 5575` and `gap_to_10k_collected: 4425`.
- Friday Scoreboard 2026-08-07 reports CASH collected this week $0, MTD $0, gap to $10K $10,000.
- Do not carry forward `$5,575` as current-month collected cash until a logged payment source reconciles it.
- Weighted forecast: $5,400.
- Forecast gap to $10K using the north-star script's stale collected baseline: $0. Treat as stale until the cash source conflict is resolved.
- Sources: `curl http://localhost:3000/api/revenue`, `memory/audits/friday-scoreboards/2026-08-07.md`, `python3 scripts/north_star_pipeline.py summary --json`.

## Stage Movement / Waiting On
- Altmark rent delinquency remainder: stage `blocked`, waiting on client, value $2,250, last touch 2026-07-16. Older than 7 days.
- DHCR Lease Renewal Phase 1 deposit: stage `pending`, waiting on client, value $1,750, last touch 2026-07-16. Older than 7 days.
- MSI engagement: stage `signed_in_delivery`, waiting on delivery, remaining value $5,400, last touch 2026-07-28. Older than 7 days but active delivery, not client-stale.
- SoberLife and Aya: closed-won/collected; referral asks eligible.

## Phase 7 KPIs
1. Posts delivered vs posted: 1 delivered / 1 posted since 2026-08-02, from `memory/content/posted-log.jsonl`.
2. Engagement per posted item: LinkedIn 2026-08-03 reported 2 likes + 2 comments.
3. Outreach packets completed vs sent vs replied: latest outreach preflight scanned 58 prospects, 57 skip, 1 warm-up-only, 0 copy-review packets, 0 external sends by runner, replies unknown because no reply log source was found in `reports/outreach-pipeline/*`; fix is to add sent/reply counters to the script summary.
4. Consulting pipeline stage movement: no new stage movement in `memory/pipeline.jsonl`; MEMORY says NewCo/job terms email sent Aug 8 and waiting on answers.
5. Cron delivery rate: 12 enabled jobs checked; 12/12 last run ok; user-facing announce jobs with delivery checks were 4/4 delivered on latest run.
6. Dollars spent: weekly AI spend $0.542 from `scripts/cost-tracker.py --weekly-review`; X API spend $0.00 this week because latest `memory/costs/x-api.jsonl` rows are 2026-07-07. OpenRouter-specific weekly spend is unknown because `memory/costs/openrouter-billing.jsonl` stores balance snapshots, not per-call deltas; fix is per-provider cost tagging in cost tracker.

## Cron Health
- Command: `PATH="/opt/homebrew/Cellar/node/26.5.0_1/bin:$PATH" openclaw cron list --json`.
- Total enabled jobs: 12.
- Consecutive errors: 0.
- Last run errors: 0.
- Never-run jobs: 0.
- Timeout pressure: none; no `lastDurationMs` within 10% of timeout.
- Weekday invocation estimate: 5/day normally, 6 on Friday, under the 20/day cap.
- Sunday 10AM: no direct conflict; Sunday lane is staggered at 07:00, 10:00, 13:00, 15:00, 15:20, and 23:00.
- Drift noted: stale diagnostic warnings still mention pseudo-command behavior in Weekly Systems Review, Daily Send Sheet, Friday Scoreboard, and weekly unemployment certification metadata. Latest statuses are ok, so this is not an active failure, but it should be cleaned in the next approved cron-prompt window.

## File Budgets
- `AGENTS.md`: 27,806 / 28,000. Under budget but only 194 bytes of headroom; trim immediately before any append.
- `MEMORY.md`: 6,979 / 20,000.
- `TOOLS.md`: 5,586 / 16,000.
- `HEARTBEAT.md`: 4,189 / 16,000.

## Process Health
- Gateway reachable by `openclaw status`, pid 22648, app 2026.7.1-2.
- Watchdog loaded: `com.openclaw.gateway-watchdog`.
- Node process flag: gateway RSS ~575 MB for 10+ minutes but CPU only 0.4%; watch, no restart.
- Other Node services are normal: n8n ~248 MB, Convex dev ~45 MB, Next dev ~12 MB.

## LaunchAgent Config
- `ai.openclaw.gateway`: `ThrottleInterval` 10. OK.
- `com.openclaw.gateway-watchdog`: `StartInterval` 600. OK.

## Version
- Current: OpenClaw 2026.7.1-2 (`0790d9f`).
- Version check source: GitHub releases API and direct Brave wrapper search.
- Result: current stable matches `v2026.7.1-2`; no stable update needed. Beta `v2026.7.2-beta.7` exists but update remains approval-gated.

## Plugins
- `~/.claude/settings.json`: `context-mode@context-mode` is `false`.
- `~/.openclaw/extensions/`: expected `lossless-claw` extension only.
- Drift: OpenClaw status warns about duplicate `lossless-claw` plugin id and conflicting plugin install metadata for `brave`, `codex`, and `lossless-claw`. Nonfatal, but should be resolved only through approved plugin/config paths.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: present/readable.
- `health/health.sqlite`: present/non-empty.
- `tasks/pending.jsonl`: valid JSONL, 5 non-empty lines.

## Weekly Maintenance
- Autoresearch enrollment: no `skills/` or `agents/` `SKILL.md`/`AGENT.md` files modified in the last 7 days; no new enrollment.
- Future signals: no active signal graduated. Site conversion review date has passed, but the trigger is not met because live Mission Control still waits on ship/loop confirmation and no audit-paid/reply/call signal is recorded.
- Passive-income pruning: Mission Control reachable; query found no active todo tasks with title containing `Build idea:` or `[PI]` and `sortOrder >= 500`.
- Cost review: 7-day spend $0.542; monthly pace $1.82 vs $50 target; Groq/Llama unused this week.
- Mission Control task updated: `Weekly Systems Review 2026-07-27: verify MC recovery and pruning` now carries the 2026-08-09 remaining drift instead of creating a duplicate task.

## Issues Fixed This Run
- Updated existing Mission Control follow-up task with current WSR drift and MC recovery proof.
- Corrected the JSON integrity interpretation for `tasks/pending.jsonl`: it is JSONL and validates line-by-line.
- Post-delivery correction: amended the report to flag the cash source conflict between live Mission Control August cash `$0`, Friday Scoreboard `$0`, and the stale north-star script `$5,575` baseline.

## Needs JT Attention
- Cash source conflict needs cleanup in `scripts/north_star_pipeline.py` or its source inputs before the next scoreboard/review.
- AGENTS.md is effectively full: 194 bytes under cap. Next append requires trimming first.
- Approve or defer the next cron-prompt cleanup window for stale pseudo-command diagnostic text.
- Duplicate plugin metadata warning should be cleaned only through approved plugin/config paths.
- Gateway memory sits slightly above the 500 MB flag threshold but is stable/low CPU.

## Evidence
- Cron list: `openclaw cron list --json`.
- File sizes: `wc -c ~/.openclaw/workspace/AGENTS.md ~/.openclaw/workspace/MEMORY.md ~/.openclaw/workspace/TOOLS.md ~/.openclaw/workspace/HEARTBEAT.md`.
- Process health: `ps aux | grep node | grep -v grep | sort -k4 -rn | head -10`.
- Gateway status: `openclaw status`.
- Version: `openclaw --version`, GitHub releases API, direct Brave wrapper search.
- Cost: `python3 scripts/cost-tracker.py --weekly-review`.
