# Weekly Systems Review — 2026-05-13

## Summary
Grade: B+ / not clean A-level. Core system is up and no cron execution errors are present, but two drift items need follow-up: weekday cron invocation estimate is above the 20/day cap, and gateway LaunchAgent `ThrottleInterval` is `1` instead of the expected >=10.

## Cron Health
- Jobs checked: 53
- Execution errors: none (`consecutiveErrors=0`, no `lastRunStatus:error`)
- Delivery issues: passive-income-strategist last run OK but `lastDeliveryStatus=not-delivered`; run metadata did not expose final content, so no resend was attempted without evidence. AI Ops Teardown Weekly Draft has never run and therefore has no delivery status yet.
- Never ran: Altmark rent delinquency tracker follow-up check (scheduled one-off for 2026-05-15), AI Ops Teardown Weekly Draft (new weekly job, first run pending).
- Timeout margin: none within 10% of configured timeout.
- Daily cap: weekday estimate ≈ 32.07/day, above the 20/day cap. Existing Operations task created to prune/batch.
- Config warning observed: duplicate lossless-claw plugin id; global plugin overrides global plugin path. No immediate breakage observed, but worth cleaning in a future config pass.

## File Budgets
- AGENTS.md: 27,863 / 28,000 — high risk, only 137 chars spare. Avoid appends; extract/compact before any new AGENTS rule.
- MEMORY.md: 19,161 / 20,000 — near budget; compact before substantial updates.
- TOOLS.md: 13,581 / 16,000 — OK.
- HEARTBEAT.md: 14,330 / 16,000 — OK but watch.

## Process Health
- Gateway process: running/reachable on local loopback, PID 29836.
- Gateway node memory: ~1.2GB RSS and 4.6% CPU at snapshot. CPU below >5% threshold; memory above 500MB but appears to be active gateway workload, not proven runaway. Watch if sustained.
- Mission Control/Convex, n8n, Next dev processes running.
- Watchdog: loaded (`com.openclaw.gateway-watchdog`).

## LaunchAgent Config
- `ai.openclaw.gateway` Label OK but `ThrottleInterval=1` — below expected 10+, flagged.
- `com.openclaw.gateway-watchdog` StartInterval=600 — OK, at max allowed threshold.

## Version
- Current: OpenClaw 2026.5.3-1 (2eae30e).
- Update available per `openclaw status`: npm 2026.5.7.
- Web check: GitHub releases page updated ~2026-05-11; docs release policy found. Do not auto-update from cron.

## Plugin Audit
- `~/.claude/settings.json` readable. `context-mode@context-mode=false` ✅
- Extensions: only `lossless-claw` plus install backups observed.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: exists/readable.
- `scripts/gateway-watchdog.sh`: exists/readable.
- `health/health.sqlite`: exists/readable.
- `tasks/pending.jsonl`: valid JSONL.

## Weekly Maintenance Split
- Autoresearch: enrolled `agentguard-positioning`; created `agents/autoresearch/checklists/agentguard-positioning.md` and appended pending target. Skipped `mcp-builder` and `webapp-testing` as general/tooling skills rather than JT-specific repeated failure surfaces. Existing app-marketing checklist present.
- Future signals: no trigger found from current MEMORY/project state. Sports GM Phase 1 active but no evidence of 10+ engaged replies/DMs or 3+ roster audit requests; Vista/Nash revenue triggers not met; no UGC creator trigger; Clay/QuickBooks/Scribe/free-tool triggers not met.
- Passive-income idea pruning: Mission Control reachable; 5 matching PI/build idea tasks found, all <60 days old. No pruning/promotions.
- Cost review:
📊 Weekly Cost Optimization Review
Total 7-day spend: $1.259
- gpt-5.5: $1.154 (92%, 7 sessions)
- deepseek/deepseek-chat-v3-0324: $0.105 (8%, 7 sessions)
- Most expensive: 2026-05-10 prospect-discovery $1.154
- Observation: Groq/Llama unused this week; check heartbeat/simple cron routing.
- Monthly pace: $10.03 vs $50 target ($39.97 headroom).

## Issues Fixed This Run
- Created autoresearch checklist and target for `agentguard-positioning`.
- Created Mission Control task: `Weekly systems review: prune cron cap + fix gateway throttle`.
- Saved this report artifact.

## Needs JT Attention
1. Approve/schedule OpenClaw update from 2026.5.3-1 to 2026.5.7 when convenient.
2. Let Eve prune/batch low-value crons and fix gateway LaunchAgent throttle via safe service path.
3. Decide whether the passive-income-strategist Telegram failure needs a manual rerun/resend; latest run was OK but delivery failed and final content was not visible from cron metadata.

Next review: 2026-05-17
