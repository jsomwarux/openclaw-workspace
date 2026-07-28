# Weekly Systems Review - 2026-07-27

## North Star Scoreboard
- Current collected: $5,575 per `scripts/north_star_pipeline.py summary --json`.
- Gap to $10K collected: $4,425.
- Weighted forecast: $10,800.
- Pipeline records: 5.
- Waiting-on items older than 7 days:
  - Altmark rent delinquency remainder: waiting_on=client, 11 days, stage=blocked, value=$2,250.
  - DHCR Lease Renewal Phase 1 deposit: waiting_on=client, 11 days, stage=pending, value=$1,750.
  - MSI engagement: waiting_on=jt, 10 days, stage=signed_in_delivery, value=$10,800; next action is kickoff invoice for $5,400.

## Phase 7 KPI Numbers
1. Posts delivered vs posted: 0 delivered rows / 0 posted rows since 2026-07-20 from `memory/content/posted-log.jsonl`.
2. Engagement per posted item: unknown; no posted content rows in the last 7 days to measure.
3. Outreach packets completed vs sent vs replied: 0 eligible copy-review packets completed today; 0 external sends by rule; replies unknown from local source. Outreach preflight scanned 58 prospects, skipped 57, warm-up-only 1 (`HealthPass`).
4. Consulting pipeline stage movement: no new local stage movement since 2026-07-17; current stages are Altmark blocked, DHCR pending, MSI signed_in_delivery, SoberLife/Aya closed_won_collected.
5. Cron delivery rate: 14 enabled jobs; latest stored live rows show 13/14 not-error, with only Weekly Systems Review still carrying the prior 2026-07-19 pseudo-command error. User-facing latest delivery rows with announce delivery are delivered where requested.
6. Dollars spent: OpenRouter/session cost 7-day spend $0.709 from `python3 /Users/jtsomwaru/.openclaw/workspace/scripts/cost-tracker.py --weekly-review`; snapshot today $0.2976 across 15 sessions. X API spend since 2026-07-20: $0 from `memory/costs/x-api.jsonl`.

## Cron Health
- Runtime truth: `openclaw cron list --json` reports 14 live enabled jobs.
- Cron volume: `scripts/cron_volume_guard.py` passed; estimated weekly invocations 50, daily average 7.14, agent-turn daily average 4.14, no same-schedule collisions.
- Error rows: Weekly Systems Review has `lastRunStatus=error`, `consecutiveErrors=5`, duration 373,897ms, timeout 900s. Latest stored run error is the prior pseudo command: `run python3 ~/.openclaw/workspace/scripts/cost-tracker.py (agent)` failed. This run executed the literal cost command successfully and should clear the row when it finishes.
- Running rows: several Sunday/one-time rows appeared `running` around the scheduler wake-up; no duration/timeout breach observed in latest stored completed durations.
- Never-ran note: live CLI row for one-time reminder `74a5b557-084e-4632-b3de-4b8c9cb5ac62` has no lastRunAtMs even though scheduled for 2026-07-24. It is past due and should be cleaned up or verified after the scheduler clears.
- Stale registry note: `/Users/jtsomwaru/.openclaw/cron/jobs.json` contains 74 historical jobs, while CLI runtime truth reports 14. Treat the CLI as authoritative; the stale file is cleanup risk only.

## File Budgets
- AGENTS.md: 27,806 / 28,000 chars. This is under budget but only 194 chars remain; do not append without extracting.
- MEMORY.md: 6,870 / 20,000 chars.
- TOOLS.md: 5,168 / 16,000 chars.
- HEARTBEAT.md: 4,189 / 16,000 chars.

## Process Health
- Gateway reachable via `openclaw status`: local gateway on pid 1331, reachable in 32ms.
- Gateway memory: 481MB, under the 500MB flag threshold but close.
- One Codex app-server process showed 44.9% CPU and 247MB RAM with only 18.96s elapsed, below the 10-minute runaway threshold.
- Two short-lived node processes showed >100% CPU with ~1.5s elapsed, not runaway.
- Watchdog: `com.openclaw.gateway-watchdog` is loaded.

## LaunchAgent Config
- `ai.openclaw.gateway`: Label `ai.openclaw.gateway`, ThrottleInterval `10`.
- `com.openclaw.gateway-watchdog`: Label `com.openclaw.gateway-watchdog`, StartInterval `600`.
- Config posture is acceptable.

## Version
- Current OpenClaw: `2026.5.28 (e932160)`.
- Web search found newer official docs release `v2026.7.1` and GitHub releases updated 2026-07-19.
- Update available: yes. No update applied because OpenClaw updates require JT approval.

## Plugin Audit
- `~/.claude/settings.json`: `context-mode@context-mode` is not enabled; no enabled MCP JSON servers are listed.
- Extensions present: `.openclaw-install-backups`, `lossless-claw`.
- Config warning persists: duplicate `lossless-claw` plugin id; global plugin override path shown by CLI. This is known drift and should be cleaned in a quiet ops window.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: exists.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL, 4 lines. Whole-file JSON parsing fails by design because it is JSONL.

## Maintenance Split
- Autoresearch enrollment: no `SKILL.md` or `AGENT.md` files under workspace `skills/` or `agents/` were modified in the last 7 days; no new target enrolled.
- Future signals: no active signal met its trigger based on current MEMORY/project reality.
- Passive-income idea pruning: Mission Control was unreachable after 3 retries. Ran the approved Mission Control LaunchAgent kickstart, retried 3 more times, still unreachable. Pruning deferred.
- Weekly cost review: complete; final absolute-path check showed 7-day spend $0.709, monthly pace $6.79, $43.21 headroom to $50 target.

## Issues Fixed This Run
- Ran the required literal cost-tracker command successfully.
- Corrected pending queue validation as JSONL during the audit.
- Kickstarted Mission Control Convex + Next LaunchAgents after API unreachability.
- Saved this report artifact.

## Needs JT Attention
- Mission Control still unreachable on `http://localhost:3000/api/tasks` after kickstart; passive-income pruning and the required not-clean follow-up MC task were deferred.
- OpenClaw update is available, but update remains approval-gated.
- AGENTS.md is only 194 chars under budget; next AGENTS append needs extraction first.
- MSI kickoff invoice is JT-owned and 10 days stale in `memory/pipeline.jsonl`.
- Duplicate `lossless-claw` plugin warning persists.

## Evidence Commands
- `python3 scripts/cost-tracker.py --weekly-review`
- `python3 /Users/jtsomwaru/.openclaw/workspace/scripts/cost-tracker.py --weekly-review`
- `PATH=/opt/homebrew/Cellar/node@22/22.22.2_2/bin:$PATH openclaw cron list --json`
- `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md`
- `ps aux | grep node | grep -v grep | sort -k4 -rn | head -10`
- `PATH=/opt/homebrew/Cellar/node@22/22.22.2_2/bin:$PATH openclaw status`
- `launchctl list | grep watchdog`
- `/usr/libexec/PlistBuddy` checks for gateway and watchdog LaunchAgents
- `set -a; source ~/.config/env/global.env; set +a; python3 scripts/web_search.py "OpenClaw changelog latest version site:github.com OR site:docs.openclaw.ai" --freshness month --count 5 --json`
- `python3 scripts/cron_volume_guard.py`
