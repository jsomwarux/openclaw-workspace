# Weekly Systems Review - 2026-07-19

## North Star Scoreboard
- July collected consulting cash: $5,575.
- Gap to $10K collected: $4,425.
- Weighted forecast: $10,800.
- Gap to $10K with forecast: $0.
- Active pipeline records: 5.
- Waiting-on items older than 7 days: 0 from `memory/pipeline.jsonl`; several records have no dated update field, so the aging check used available dated fields only.

## Stage Movement
- MSI / Marketsmith: signed and active delivery. Next action is JT-gated kickoff invoice for $5,400.
- Altmark rent delinquency: still blocked on client inputs.
- DHCR Lease Renewal Phase 1: pending Matt approval + deposit.
- SoberLife and Aya: closed-won/collected; referral asks eligible.

## Outcome KPIs
1. Posts delivered vs posted: 0 delivered / 0 posted in `memory/content/posted-log.jsonl` for 2026-07-12..2026-07-19.
2. Engagement per posted item: no posted items in the local posted-log window, so engagement per item is 0 / not applicable.
3. Outreach packets completed vs sent vs replied: 0 completed / 0 sent / 0 replied from local outreach files in the 2026-07-12..2026-07-19 window; Friday Scoreboard also reports 0 sends and 0 replies.
4. Consulting pipeline stage movement: MSI moved to signed active delivery; Aya and SoberLife closed-won/collected; Altmark still blocked; DHCR still pending.
5. Cron delivery rate: 9 delivered or non-delivery-required runs / 9 recent user-facing runs = 100%. Evidence: `docs/audits/delivery-rate-2026-07-19.md`.
6. Dollars spent: OpenRouter actual billing delta $0.00; X API $0.00 from `memory/costs/x-api.jsonl`. Cost tracker estimated 7-day session spend at $1.528.

## Cron Health
- Enabled jobs checked: 12.
- Current enabled red row: `Weekly Systems Review` had `lastRunStatus=error`, `consecutiveErrors=4`, last failure `run openclaw status (agent)` from 2026-07-12. This run is executing the hardened real-command path; final cron row will clear only after the current run exits.
- User-facing delivery statuses: delivered or not-requested for enabled jobs. Daily Send Sheet, Friday Scoreboard, and weekly unemployment cert delivered.
- Near-timeout enabled jobs: none. Largest duration was passive-income-fetch-signals at 960,607 ms against 3,600 seconds.
- Cron volume: 12 enabled recurring jobs. Estimated runs/day: Mon 11, Tue 5, Wed 5, Thu 5, Fri 5, Sat 6, Sun 6; weekdays stay under the 20/day invocation cap.
- Sunday 10AM conflict: none requiring action.
- Never-ran enabled jobs: none from live `openclaw cron list`; stale nulls in `jobs.json` are inactive/static config and not live state.

## File Budgets
- `AGENTS.md`: 27,806 / 28,000 chars. Critical near-cap: only 194 chars left. Do not append; extract before any future rule addition.
- `MEMORY.md`: 6,991 / 20,000 chars.
- `TOOLS.md`: 5,168 / 16,000 chars.
- `HEARTBEAT.md`: 4,189 / 16,000 chars.

## Process Health
- Gateway reachable via `openclaw status`, running pid 68142.
- Gateway process: `/opt/homebrew/opt/node/bin/node /opt/homebrew/lib/node_modules/openclaw/dist/index.js gateway --port 18789`, about 31.5% CPU and 788 MB RSS in the sample. This exceeds the >500 MB review flag; no restart performed because gateway changes/restarts are red/yellow-gated unless explicitly approved or recovery-required.
- Codex app-server sample: about 11% CPU and 186 MB RSS.
- Watchdog: `com.openclaw.gateway-watchdog` loaded.

## LaunchAgent Config
- Gateway LaunchAgent label: `ai.openclaw.gateway`.
- Gateway `ThrottleInterval`: 10. OK.
- Watchdog label: `com.openclaw.gateway-watchdog`.
- Watchdog `StartInterval`: 600. OK at the upper allowed bound.

## Version
- Current OpenClaw: `2026.5.28 (e932160)`.
- Latest found by direct Brave wrapper: docs release `v2026.7.1` and GitHub releases updated 2026-07-18.
- Update available: yes. No update performed; OpenClaw updates require JT approval.
- Sources: https://docs.openclaw.ai/releases/2026.7.1 and https://github.com/openclaw/openclaw/releases.

## Plugin Audit
- `~/.claude/settings.json`: `enabledPlugins.context-mode@context-mode` is `false`.
- `~/.openclaw/extensions/`: expected `lossless-claw` extension plus `.openclaw-install-backups`.
- Drift: OpenClaw emits duplicate `lossless-claw` plugin warning on CLI commands. Existing high-priority Mission Control task already owns this.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: exists.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL, 4 entries.

## Maintenance
- Autoresearch enrollment: no new target enrolled. Recently modified repeated/scorable targets are already registered; unregistered modified skills are not active recurring score targets or lack a clear repeated failure mode.
- Future signals: no active trigger graduated. Consulting cash is $5,575 collected but the relevant passive-income trigger requires Altmark proof accepted plus consulting or buyer-pull conditions; sports/app/product triggers remain unmet.
- Passive-income queue pruning: 8 stale `[PI]` Mission Control tasks with `sortOrder >= 500` were marked done with a 2026-07-19 pruning note. No ideas promoted.
- Weekly cost review: 7-day estimated spend $1.528; monthly pace $7.01 against $50 target; headroom $42.99. Routing note: Groq/Llama unused this week.

## Issues Fixed This Run
- Pruned 8 stale/superseded passive-income idea tasks from Mission Control.
- Avoided creating a duplicate systems-drift task; existing high-priority task `Weekly Systems Review: reduce cron errors and daily agent-turn volume` remains the owner.

## Needs JT Attention
- Approve/timing decision for OpenClaw update from 2026.5.28 to current release line.
- Quiet-window ops task still needed: fix clean-shell OpenClaw Node path, resolve duplicate `lossless-claw` warning, and review gateway RSS/CPU.
- `AGENTS.md` is too close to cap for future appends; next rule addition must extract/archive first.
- Business outcome pressure: local evidence shows 0 posts, 0 sends, 0 replies this week even though MSI moved to signed delivery.

## Evidence Commands
- `PATH=/opt/homebrew/Cellar/node@22/22.22.2_2/bin:$PATH openclaw cron list`
- `PATH=/opt/homebrew/Cellar/node@22/22.22.2_2/bin:$PATH openclaw cron list --json`
- `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md`
- `ps aux | grep node | grep -v grep | sort -k4 -rn | head -10`
- `PATH=/opt/homebrew/Cellar/node@22/22.22.2_2/bin:$PATH openclaw status`
- `launchctl list | grep watchdog`
- `plutil -extract ThrottleInterval raw ~/Library/LaunchAgents/ai.openclaw.gateway.plist`
- `plutil -extract StartInterval raw ~/Library/LaunchAgents/com.openclaw.gateway-watchdog.plist`
- `PATH=/opt/homebrew/Cellar/node@22/22.22.2_2/bin:$PATH openclaw --version`
- `python3 scripts/web_search.py "OpenClaw changelog latest version site:github.com OR site:docs.openclaw.ai" --freshness month --count 5 --json`
- `python3 scripts/north_star_pipeline.py summary --json`
- `python3 scripts/recompute_delivery_rate.py --days 7 --json`
- `python3 scripts/cost-tracker.py --weekly-review`

