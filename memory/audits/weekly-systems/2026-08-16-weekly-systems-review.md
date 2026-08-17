# Weekly Systems Review - 2026-08-16

## North Star Scoreboard
- Scoreboard source: `memory/north-star.md`; current local summary command: `python3 /Users/jtsomwaru/.openclaw/workspace/scripts/north_star_pipeline.py summary --json`.
- `north_star_pipeline.py` output: `current_collected=$5,575`, `gap_to_10k_collected=$4,425`, `weighted_forecast=$5,400`.
- Current Mission Control revenue API: `/api/revenue` reports `consultingCollected=$0`, `totalCollected=$0`, `openWeighted=$5,400`.
- Latest Friday Scoreboard (`memory/audits/friday-scoreboards/2026-08-14.md`): collected this week `$0`, MTD `$0`, gap to `$10,000`.
- Result: cash-source conflict persists. Treat `/api/revenue` + Friday Scoreboard as current August truth; `north_star_pipeline.py` is carrying stale `$5,575` and needs source reconciliation.

## Phase 7 KPI Snapshot
1. Posts delivered vs posted: `0 delivered / 0 posted` found in `memory/content/posted-log.jsonl` for 2026-08-10 through 2026-08-16. Source gap: no current-week content delivery rows.
2. Engagement per posted item: `unknown`; no posted items or engagement records for the week in `posted-log.jsonl`.
3. Outreach packets completed vs sent vs replied: `0 sent / 0 replies / 0 meetings`; Friday Scoreboard cites daily outreach dry-runs with no external sends and `memory/send-queue.md` says no aging pipeline send items.
4. Consulting pipeline stage movement: 2026-08-10 sync moved/clarified Altmark blocked on client+JT gates, DHCR to Matt delivery-track pending, Maiky on-hold but live, MSI signed/in delivery, Gil referral eligible, Karen referral gated on SEO reset.
5. Cron delivery rate: `12/12` jobs have latest delivery status in `delivered` or `not-requested`; user-facing announce jobs `4/4 delivered`.
6. Dollars spent: OpenRouter/OpenAI-cost tracker last 7 days `$0.426`; monthly pace `$1.85`. X API spend source not found in the weekly cost output; concrete fix is to add X API spend to `scripts/cost-tracker.py --weekly-review` or the KPI scoreboard command.

## Cron Health
- Jobs checked: 12 enabled jobs.
- Current failures: 0 jobs with `consecutiveErrors >= 1`; 0 jobs with `lastRunStatus=error`.
- User-facing delivery: 4 announce jobs, all delivered.
- Timeout pressure: none within 10% of configured timeout.
- Never-run jobs: none.
- Invocation cap: weekdays stay under the 20/day cap. Estimated normal weekday load is 5 runs/day; Friday is 6; Sunday is 9 including weekly review/passive-income/unemployment lanes.
- Notes: Friday Scoreboard and weekly unemployment certification have stale diagnostic warnings containing pseudo-command text, but latest run status is ok and delivery succeeded. Do not rerun just to clear metadata.

## File Budgets
- `AGENTS.md`: 26,573 / 28,000 chars. Under cap, but close; trim before any new rule append.
- `MEMORY.md`: 6,709 / 20,000 chars.
- `TOOLS.md`: 5,586 / 16,000 chars.
- `HEARTBEAT.md`: 4,189 / 16,000 chars.

## Process Health
- Gateway status: reachable in 26ms; LaunchAgent loaded and running, pid 22648.
- Gateway memory: 607 MB, above the 500 MB review flag. CPU was 1.1%, so this is a quiet-window cleanup/watch item, not an emergency.
- Other node processes: n8n about 249 MB; Codex app-server about 169 MB; no CPU runaway found.
- Watchdog: `com.openclaw.gateway-watchdog` loaded.

## LaunchAgent Config
- Gateway plist: `Label=ai.openclaw.gateway`, `ThrottleInterval=10`.
- Watchdog plist: `Label=com.openclaw.gateway-watchdog`, `StartInterval=600`.
- Result: config within expected bounds.

## Version
- Current: `OpenClaw 2026.7.1-2 (0790d9f)`.
- Latest GitHub release: `v2026.7.1-2`, published 2026-08-04.
- Result: current; no update action.

## Plugin Audit
- `~/.claude/settings.json`: `context-mode@context-mode` is `false`.
- `~/.openclaw/extensions/`: only expected `lossless-claw` extension plus install backups.
- OpenClaw status warning persists: duplicate `lossless-claw` plugin id and shared SQLite metadata conflict for `brave`, `codex`, and `lossless-claw`.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: exists/readable.
- `scripts/gateway-watchdog.sh`: exists/readable.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL.

## Weekly Maintenance
- Autoresearch enrollment: no new repeated, scoreable unregistered skill/agent enrolled. Recent modified skill list is broad, but the already-registered targets cover the recurring scoreable surfaces. `app-discovery-loop`, `content-atomizer`, `launch-strategy`, `mcp-builder`, `n8n-blueprint`, `positioning-angles`, `product-build-loop`, `prompt-library`, `proposal-pdf`, `qmd`, and `webapp-testing` are not enrolled from this run because no repeated failure mode was established here.
- Future signals: no signal graduated. `jtsomwaru.com Deferred Conversion Rows` has a stale Aug 2 reconsider date, but the trigger also required homepage + `/property` shipped and enough send/reply/audit signal; local evidence does not prove that full condition.
- Passive-income pruning: Mission Control reachable; no todo tasks titled `Build idea:` or `[PI]` with `sortOrder >= 500`, so nothing pruned/promoted.
- Weekly cost review: 7-day spend `$0.426`; monthly pace `$1.85`; routing note: Groq/Llama unused this week.

## Issues Fixed This Run
- Saved this report artifact.
- Updated the training log with the current WSR drift pattern.
- Updated the existing Mission Control WSR follow-up task instead of creating a duplicate.

## Needs JT Attention
- Cash-source reconciliation: `north_star_pipeline.py` still reports stale `$5,575` collected while `/api/revenue` and Friday Scoreboard report `$0` August collected.
- Quiet ops cleanup: gateway memory is above 500 MB and duplicate plugin metadata warning persists. Do this only through approved plugin/config paths; no raw gateway restart or plugin surgery inside WSR.
- AGENTS.md needs trim before the next rule append.
- Cron prompt cleanup: stale pseudo-command diagnostic warnings remain in old run metadata for Friday Scoreboard and unemployment certification; patch only during approved prompt-maintenance window.

## Next Review
- 2026-08-23
