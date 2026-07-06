# Weekly Systems Review - 2026-07-05

## North Star Scoreboard
- Current collected: $5,575.
- Weighted forecast: $4,057.50.
- Gap to $10K collected: $4,425.
- Gap to $10K with weighted forecast: $367.50.
- Aging pipeline items: 6.

## Stage Movement / Waiting On
- Altmark rent delinquency remaining: active, $2,250, 55% weight, waiting on client since 2026-06-11.
- Altmark DHCR phase 1: proposal, waiting on client since 2026-05-27, intentionally behind rent delinquency.
- Petri Plumbing follow-up: contacted, waiting on JT since 2026-06-01.
- HPM and Superior Plumbing follow-ups: contacted, waiting on prospect since 2026-06-01.
- Marketsmith: live MC task says wait for July 6-7 leadership plan, then convert to proposal if they reply.

## Phase 7 KPI Scoreboard
1. Posts delivered vs posted: 5 logged/delivered to content system for 2026-06-29 through 2026-07-05; 0 marked posted in `memory/content/posted-log.jsonl`.
2. Engagement per posted item: 0/unknown because no item is marked posted; missing source is a post-confirmed engagement capture path for X/LinkedIn.
3. Outreach packets completed vs sent vs replied: completed packets exist in MC send queue, but no outreach log files were modified in the last 14 days; sent = 0 confirmed this week; replies = unknown from local logs. Fix: require `scripts/outreach_update.py` confirmation after every JT send.
4. Consulting pipeline stage movement: no stage movement in `memory/pipeline.jsonl`; top movement gate is still Altmark acceptance/payment and Marketsmith July 6-7 reply.
5. Cron delivery rate: current-state posture is 42/44 enabled jobs ok by `openclaw cron list`; exact 7-day delivery rate unavailable because `openclaw cron runs` requires a job id and `/Users/jtsomwaru/.openclaw/cron.db` is empty. Fix: add/export a run-log aggregator.
6. Dollars spent: OpenRouter delta $3.077468 from `memory/costs/openrouter-billing.jsonl`; X API $9.36 from `memory/costs/x-api.jsonl`; cost tracker 7-day LLM spend $1.906 excluding X API/OpenRouter billing delta.

## Cron Health
- Jobs checked: 44 enabled.
- Cron volume guard: PASS, 176.46 weekly invocations, 25.21/day average, 20.21 agent-turn/day average, no warnings.
- Error rows:
  - `eve-morning-brief-001` Morning Brief: latest run failed after pseudo command `run python3 ~/.openclaw/workspace/scripts/nash_rankings_probe.py (agent)`. Current live payload already has 2026-07-05 command-only hardening and Nash non-abort instructions. No rerun; verify next natural run.
  - `4c437ff5-02cd-4288-8e6e-6e6fc07203ce` Skills & API Researcher Daily Scan: latest run failed after pseudo file-read command `print lines ... -> ... (agent)`. Current live payload already has 2026-07-04 file-read command hardening. No rerun; verify next natural run.
- Delivery: Morning Brief failure notification not delivered because the run itself stopped before final confirmation. Prior day Morning Brief delivered correctly with fallback.
- Sunday 10AM conflict: Weekly Systems Review runs at 10:00; Weekly Health Report runs 09:20 and content-sunday runs 09:00, so no direct 10AM conflict.
- Never-ran jobs: none visible in human `openclaw cron list`; `jobs.json` does not store run state and should not be used for that classification.

## File Budgets
- `AGENTS.md`: 27,614 / 28,000 chars. Close to cap; do not append without extracting.
- `MEMORY.md`: 6,973 / 20,000 chars.
- `TOOLS.md`: 5,168 / 16,000 chars.
- `HEARTBEAT.md`: 4,189 / 16,000 chars.
- Recommendation: next AGENTS.md correction should extract older operating rules or mistakes pointers before appending.

## Process / Gateway Health
- Gateway reachable via `openclaw status`; LaunchAgent loaded and running, PID 68142.
- Node process sample: gateway ~720MB RSS, 0.6% CPU; above 500MB RAM but low CPU and long-running. Review during quiet window, no restart from cron.
- Watchdog loaded: `com.openclaw.gateway-watchdog`.
- Other notable node processes: n8n ~105MB, Convex ~76MB, Next dev ~34MB.

## LaunchAgent Config
- `ai.openclaw.gateway`: ThrottleInterval 10, OK.
- `com.openclaw.gateway-watchdog`: StartInterval 600, OK.

## OpenClaw Version
- Current: OpenClaw 2026.5.28 (e932160).
- Latest found via local direct-Brave wrapper: v2026.6.11 on docs/GitHub.
- Action: update available; do not auto-update without JT approval.

## Plugin / Settings Audit
- `~/.claude/settings.json`: `context-mode@context-mode` is false.
- Extensions found: `lossless-claw` only.
- Config warning persists: duplicate plugin id for `lossless-claw`; global plugin overrides global plugin path. Needs quiet-window cleanup/documentation.
- Security note: `~/.claude/settings.json` contains a bearer-style MCP token. It was not copied into this report. Review whether Claude settings is an approved home for that token or move to env/keychain-compatible config.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: executable.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL.

## Weekly Maintenance Split
- Autoresearch: modified in last 7 days: `skills/cold-email/SKILL.md`, `skills/opticfy-pipeline/SKILL.md`, `agents/passive-income-scout/AGENT.md`. All are already registered; no new enrollment.
- Future signals: no active signal trigger met against current MEMORY/project state.
- Passive-income idea pruning: 9 `[PI]` tasks found with sortOrder >=500; none older than 60 days, so none pruned/promoted.
- Mission Control follow-up: updated existing high-priority task `Weekly Systems Review: reduce cron errors and daily agent-turn volume` with 2026-07-05 evidence.
- Weekly cost review: total 7-day LLM spend $1.906; gpt-5.5 $1.585; unknown $0.322; monthly pace $3.13 against $50 target.

## First-Sunday Prompt Rewrite Ritual
- Five longest live prompts identified:
  1. Viral Post Swipe File - X Research, 14,990 chars.
  2. Job Market Daily Research, 14,166 chars.
  3. prospect-discovery, 11,141 chars.
  4. Weekly Systems Review, 10,671 chars.
  5. Weekly Intelligence Synthesis, 9,520 chars.
- Proposed rewrites saved under `docs/audits/prompt-rewrites/2026-07-05/`.
- Convex finding: current local docs/scripts use `convex dev` / `npx convex dev`; no live `--instance-secret` argv found outside the audit redaction script. Do not change runtime config without JT approval.

## Issues Fixed This Run
- Updated the existing high-priority Mission Control systems-review task with current red cron rows, next action, and done-state.
- Saved this local audit artifact.

## Needs JT Attention
- Approve/defer OpenClaw v2026.6.11 update path. Current machine is behind stable runtime fixes.
- Decide whether the bearer-style MCP token in Claude settings should remain there or move to approved secret storage.
- Confirm whether duplicate OpenClaw update tasks should be collapsed into the current v2026.6.11 task.
- Do not append to AGENTS.md until it is trimmed or content is extracted.

## Next Review
- 2026-07-12.
