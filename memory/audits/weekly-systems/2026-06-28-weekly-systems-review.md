# Weekly Systems Review - 2026-06-28

## North Star
- Current June collected: about $5,575.
- Pipeline-weighted forecast: about $4,058.
- Gap to $10K collected: about $4,425; gap including weighted forecast: about $368, but fragile because weighted pipeline is not cash.
- Aging pipeline items: 6.
- Waiting-on older than 7 days: Altmark rent delinquency inputs from Yair, Altmark DHCR lease renewal, Altmark support retainer, Altmark remaining workflow buildout, Petri follow-up, HPM/Superior/Guyana/Aya revival lanes.

## Phase 7 KPI Scoreboard
- Posts delivered vs posted: 6 scheduled/delivered content rows for 2026-06-22 through 2026-06-28; 0 marked posted in `memory/content/posted-log.jsonl`.
- Engagement per posted item: unknown; missing source is current post-performance replies/posted URLs with likes/replies/views. Fix: log posted URLs and metrics through the posted-reply/performance handlers.
- Outreach packets completed vs sent vs replied: 0 eligible copy-review items and no external outreach in latest outreach pipeline evidence; no dedicated weekly send/reply JSONL source exists. Fix: add a weekly outreach KPI writer keyed from `reports/outreach-pipeline/` and send confirmations.
- Consulting pipeline stage movement: no clear stage movement; current active counts are active 1, proposal 2, lead 5, contacted 3.
- Cron delivery rate: 16/17 latest announce jobs delivered, 94.1%; failure is `content-generate-x`.
- Dollars spent: OpenRouter billing source shows $0.00 for 2026-06-22 through 2026-06-28; X API log shows $9.715 for 257 rows; cost tracker 7-day total LLM spend is $4.553 across local session accounting.

## Cron Health
- Total enabled jobs checked: 44.
- Error rows: 2.
- `Weekly Systems Review` had prior `consecutiveErrors=1` from the 2026-06-21 pseudo-command finalization failure; this run used real shell commands and saved this artifact.
- `content-generate-x` has `consecutiveErrors=2`, `lastRunStatus=error`, `lastDeliveryStatus=not-delivered`; latest run ended with `Agent couldn't generate a response` and no useful output in the run record.
- Near-timeout jobs: none.
- Never-run jobs: none.
- Sunday 10AM conflict: none material; Sunday morning jobs remain staggered.
- Cron volume: `scripts/cron_volume_guard.py` passed, but estimated agent-turn average is 20.21/day against the stricter <=20 Phase 7 target.

## File Budgets
- `AGENTS.md`: 27,516 / 28,000, under cap but tight. Extract before any new rule append.
- `MEMORY.md`: 7,306 / 20,000, healthy.
- `TOOLS.md`: 5,168 / 16,000, healthy.
- `HEARTBEAT.md`: 4,189 / 16,000, healthy.

## Process Health
- Gateway reachable at pid 40432; `openclaw status` reports gateway LaunchAgent loaded/running.
- Gateway node process memory: 586,864 KB, over the 500 MB review threshold, CPU low at 0.3%.
- Codex app-server memory: 180,752 KB, CPU 1.0%.
- Watchdog running: `com.openclaw.gateway-watchdog`.

## LaunchAgent Config
- Gateway plist: `ThrottleInterval=10`, OK.
- Watchdog plist: `StartInterval=600`, OK at the maximum allowed interval.

## Version
- Current OpenClaw: 2026.5.28 (e932160).
- Version search found GitHub releases updated 2026-06-04 and repo activity on 2026-06-26, so an update may exist. Do not update without JT approval.

## Plugin Audit
- `~/.claude/settings.json`: `context-mode@context-mode=false`, OK.
- Extensions: only `lossless-claw` found.
- Config warning persists: duplicate `lossless-claw` plugin id; global plugin overrides global plugin path. This should be cleaned during a quiet ops window, not inside this cron.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: exists.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL line-by-line. Whole-file JSON parsing correctly fails because JSONL is not a single JSON document.

## Weekly Maintenance
- Autoresearch enrollment: no new scoreable repeated skill/agent needed enrollment. Recently modified candidates are already registered or one-off/log-only.
- Future signals: no triggers met. Altmark proof is not accepted, apps lack revenue/distribution signal, no creator hired, no client custom-model/RAG trigger, no Cloudflare/DGX/Clay/PostBridge/ViewTrack trigger.
- Passive-income pruning: Mission Control reachable; 9 `[PI]` candidates found, none older than 60 days, no prune/promote action.
- Cost review: 7-day LLM spend $4.553; monthly pace $10.12 vs $50 target; Groq/Llama unused.

## Fixes Applied
- Updated existing high-priority Mission Control task `Weekly Systems Review: reduce cron errors and daily agent-turn volume` with 2026-06-28 evidence and next action.
- Saved this local report artifact.
- Appended weekly systems entry to `memory/training/training-log.md`.

## Needs JT Attention
- Approve or defer OpenClaw update review; no auto-update was performed.
- Let Eve repair `content-generate-x` before Monday content if possible.
- During a quiet window, review duplicate `lossless-claw` plugin warning and gateway memory if it remains above 500 MB.
