# Weekly Systems Review - 2026-06-21

## North Star Opening
- Current June collected: about $5,575.
- Weighted forecast: about $4,058.
- Gap to $10K collected: about $4,425.
- Gap to $10K including weighted forecast: about $368, but fragile because forecast is not cash.
- Stage movement: Altmark remains the next-dollar gate; Yair/Altmark rent-delinquency inputs are the unlock for the remaining $2,250 and next workflow.
- Waiting-on items older than 7 days from `memory/pipeline.jsonl`: 0 by status/date scan.

## Phase 7 KPI Numbers
1. Posts delivered vs posted: 6 scheduled/delivered content slots in `memory/content/posted-log.jsonl`; 0 posted confirmations recorded for 2026-06-15 through 2026-06-21.
2. Engagement per posted item: unknown because 0 posted confirmations have URLs/metrics in the posted log. Concrete fix: JT replies with `posted ... <url>` after posting so `scripts/content_posted_reply_handler.py` can attach evidence.
3. Outreach packets completed vs sent vs replied: completed packets exist for the PM COI wave-one sprint; send/reply counts are unknown because JT has not confirmed sends in the outreach log for this wave. Concrete fix: after each send, run `scripts/outreach_update.py` via the send-confirmation handler.
4. Consulting pipeline stage movement: Altmark collected $3,375 in June; next movement is blocked on rent-delinquency inputs/approval, not more research.
5. Cron delivery rate: 45 jobs checked; 25 latest runs had user-facing delivery config; 23/25 had acceptable latest delivery status (`delivered` or `not-requested`), with 2 not-delivered rows tied to errored jobs.
6. Dollars spent: OpenRouter usage delta about $8.017 from 2026-06-15 to 2026-06-21 billing snapshots; X API cost $10.295 for 2,059 tweets across 261 logged calls. Weekly cost-tracker reported total 7-day modeled spend $3.095 and monthly pace $6.57 against $50 target.

## Cron Health Audit
- Jobs checked: 45 live jobs from `openclaw cron list`.
- Red jobs:
  - `922082ee-da62-4b6e-b9e3-909c3446e381` passive-income-strategist: last run error, `consecutiveErrors=1`; Codex stopped before final confirmation. Do not rerun just to clear status.
  - `bb0819d0-8900-4e2a-99a2-28ab950365ab` ReelFarm Weekly Strategy Synthesis: last run error, `consecutiveErrors=1`; failed on pseudo command pattern (`run for f -> run do -> print...`).
  - `870bf3ff-55c9-49c0-9970-361c81a0920b` vibe-marketing-generate: last run error, `consecutiveErrors=2`; Codex stopped before confirmation and delivery was not delivered.
  - `b2357bd5-651d-4151-80df-49e4a928826f` Job Application Auto-Builder: last run error, `consecutiveErrors=1`; audit search pattern against `xplor-ai-transformation-lead-cover-letter.md` failed.
  - `cb8f29dd-0db1-4abd-b87e-3e7168ca4a97` content-generate-x: last run error, `consecutiveErrors=1`; agent could not generate a final response and delivery was not delivered.
  - `eve-niche-monitor-006` Niche Intelligence Monitor: last run error, `consecutiveErrors=1`; `scripts/web_search.py` command failed, likely env sourcing issue.
- User-facing delivery exceptions: vibe-marketing-generate and content-generate-x show `not-delivered` because their runs errored.
- Duration near timeout: none detected from structured job state.
- Never-ran jobs: the local job store has disabled/legacy rows with no `lastRunAtMs`; live list has one future reminder with no last run, expected.
- Invocation cap: local active cron estimate is about 30 Monday invocations and 33 Sunday invocations, above the stricter 20/day target.
- Sunday 10AM conflicts: none at exactly 10:00 besides Weekly Systems Review; nearby Sunday jobs remain staggered.

## File Budget Check
- `AGENTS.md`: 27,516 bytes / 28,000 budget. Close to cap; avoid appending without extracting.
- `MEMORY.md`: 7,965 bytes / 20,000 budget.
- `TOOLS.md`: 5,168 bytes / 16,000 budget.
- `HEARTBEAT.md`: 4,189 bytes / 16,000 budget.
- Action: no compaction required this run. If AGENTS.md needs another rule, extract older long sections before appending.

## Process Health
- Gateway reachable via `openclaw status`, pid 57777, service loaded/running.
- Watchdog loaded: `com.openclaw.gateway-watchdog`.
- High-memory process: OpenClaw gateway node process at about 624 MB RSS, above the 500 MB watch threshold, running since Wed09AM. CPU was low at audit time.
- Other notable process: Codex app-server around 1.9% CPU / 188 MB RSS; n8n around 235 MB RSS.

## LaunchAgent Config
- Gateway plist: `Label=ai.openclaw.gateway`; `ThrottleInterval=10`, acceptable.
- Watchdog plist: `Label=com.openclaw.gateway-watchdog`; `StartInterval=600`, at the maximum acceptable interval.

## Version Check
- Current OpenClaw: `2026.5.28 (e932160)`.
- Fresh direct-Brave search found current OpenClaw release pages and existing MC tasks already reference OpenClaw 2026.6.x upgrade validation. Update available: yes/likely, but OpenClaw updates require JT approval and were not applied.

## Plugin Audit
- `~/.claude/settings.json`: `context-mode@context-mode` is still `false`.
- Extensions directory contains expected `lossless-claw` plus `.openclaw-install-backups`.
- Config warning persists: duplicate `lossless-claw` plugin id; global plugin override is noisy but not breaking this run.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: exists/readable.
- `scripts/gateway-watchdog.sh`: exists.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid line-delimited JSON. Plain `python -m json.tool` is not the right validator for JSONL.

## Maintenance
- Autoresearch enrollment: no new enrollment. Recently modified repeated/scorable targets are already registered or already pending/stable (`cold-email`, `app-marketing/product-content`, `x-research`, `prompt-library`, `content-generation`, `job-application`, `passive-income-scout`, `ai-seo`).
- Future signals: no active signal graduated. Passive-income build queue trigger is not met because consulting revenue is not yet consistent; ViewTrack/PostBridge/Virlo/Remotion triggers are not met because app posting/revenue is not yet consistent.
- Passive-income queue pruning: Mission Control reachable; 9 `[PI]`/`Build idea:` todo items with `sortOrder>=500`; 0 older than 60 days, so nothing pruned/promoted.
- Weekly cost review: total 7-day modeled spend $3.095; monthly pace $6.57; Groq/Llama unused this week.
- Mission Control: updated existing high-priority task `Weekly Systems Review: reduce cron errors and daily agent-turn volume` with this run's evidence and done-state.

## Issues Fixed This Run
- Updated Mission Control repair task with exact red jobs, first action, why it matters, and done-state.
- Corrected pending queue validation from invalid whole-file JSON check to proper JSONL line validation.
- Verified local direct-Brave wrapper use for version search; did not use managed web_search.

## Needs JT Attention
- Approve or defer one current OpenClaw runtime upgrade task; there are multiple stale OpenClaw update tasks in MC that should be consolidated.
- Post confirmations are the KPI bottleneck: 6 scheduled content slots, 0 posted confirmations this week.
- X API spend is high relative to the $10 weekly target: $10.295 already logged for the week.
- Gateway memory is above the watch threshold at about 624 MB RSS. Not an emergency because CPU is low and gateway is reachable, but it deserves a quiet-window restart only via approved restart script if memory keeps climbing.

## Next Review
- 2026-06-28.
