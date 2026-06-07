# Weekly Systems Review — 2026-06-07

## Executive Summary
- Overall grade: B. Core services are up and delivery works, but cron metadata still shows three red jobs from prior brittle checks, gateway/Codex load is above watch thresholds, OpenClaw is behind the current release train, and Claude settings contain an MCP bearer token outside the approved secret homes.
- Fixes applied this run: patched `content-generate-x` delivery to Telegram announce + best-effort, manually resent the missed X queue summary to JT, enrolled three autoresearch targets, and created Mission Control follow-up `j5718pb51pq9eftmdeb689f9r98877n5`.
- No jobs were rerun solely to clear stale status.

## Cron Health
- Jobs checked: 54 enabled / 80 total.
- Error metadata:
  - `b2ca53ab-0c07-4a22-8424-9d39bf988405` Weekly Systems Review: prior run red from `verify-live-posting.py` without an explicit URL. Current payload includes the 2026-05-31 soft-exit/live-posting hardening.
  - `be59a068-eccd-4a7c-964e-946ab40ace7e` Overnight Autonomy Agent: latest run failed on pseudo `fetch http://localhost:3000/api/tasks -> run jq`; live payload now contains real `curl | jq '(.tasks // .items // .)'` hardening.
  - `eve-job-market-daily-005` Job Market Daily Research: latest run failed after useful work by executing generated source text/inline script path; live payload now says `Sources:` lines are report content only and forbids pseudo/inline execution.
- Delivery drift:
  - `cb8f29dd-0db1-4abd-b87e-3e7168ca4a97` content-generate-x generated useful output but had delivery `none -> none`. Patched delivery to `announce -> telegram:6608544825` with `bestEffort:true`; missed queue summary sent manually.
- Near timeouts: 0.
- Never ran: 1 future one-shot, `Reminder: YouTube TV midday`, scheduled for 2026-06-25.
- Sunday 10AM conflicts: none at exactly 10AM; existing Sunday 6PM pair remains noted/staggered.
- Cron volume guard: pass with warning. 54 enabled jobs, ~222.46 weekly invocations, ~31.78/day average, ~27.78 agentTurn/day average. Warning: scheduled daily average near cap. The old 20/day target is exceeded, but the executable guard remains under its current thresholds.

## File Budgets
- `AGENTS.md`: 25,875 / 28,000.
- `MEMORY.md`: 19,780 / 20,000.
- `TOOLS.md`: 15,232 / 16,000.
- `HEARTBEAT.md`: 3,795 / 16,000.
- Recommendation: trim MEMORY.md before any strategic append and TOOLS.md before adding more command/tool details.

## Process Health
- Gateway reachable via `openclaw status`, pid 28825.
- Watchdog loaded: `com.openclaw.gateway-watchdog`.
- Flagged processes:
  - Gateway RSS ~754MB, above the 500MB watch threshold, though CPU sample was low.
  - Codex app-server pid 10243 sampled at 6.5% CPU for >10 minutes.
- Mission Control was reachable at `http://localhost:3000/api/tasks`.

## LaunchAgent Config
- Gateway plist: `ThrottleInterval` = 10, OK.
- Watchdog plist: `StartInterval` = 600, OK.

## Version
- Current: OpenClaw 2026.5.28 (`e932160`).
- Fresh version search: GitHub releases show `2026.6.5-beta.1` from 2026-06-04.
- Action: report only. OpenClaw updates require JT approval.

## Plugin / Extension Audit
- `context-mode@context-mode`: false, OK.
- Extensions present: `lossless-claw` plus `.openclaw-install-backups`.
- Warning: OpenClaw reports duplicate `lossless-claw` plugin id where a global plugin overrides another global plugin path.
- Security note: Claude settings contain an MCP bearer token for `n8n-mcp`. I did not copy it into this report. This should be rotated or moved to an approved secret home.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: exists.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL, 4 records.

## Weekly Maintenance
- Autoresearch enrolled:
  - `ui-clone` with checklist `agents/autoresearch/checklists/ui-clone.md`.
  - `workflow-strategist` with checklist `agents/autoresearch/checklists/workflow-strategist.md`.
  - `product-quality-pass` with checklist `agents/autoresearch/checklists/product-quality-pass.md`.
- Future signals reviewed: no active signal trigger met against current MEMORY/project reality.
- Passive-income queue pruning: Mission Control reachable; 11 matching `[PI]` tasks found; 0 older than 60 days; no pruning/promotion applied.
- Weekly cost review: 7-day spend $0.243; monthly pace $0.97 against $50 target; note says Groq/Llama unused this week.

## Mission Control Follow-Up
- Created high-priority Operations task: `Weekly systems review: clear June 7 runtime drift` (`j5718pb51pq9eftmdeb689f9r98877n5`).
- First action: verify next natural Overnight Autonomy + Job Market Daily runs clear stale red status, review gateway/Codex load, decide OpenClaw update timing, and remediate the MCP token location.

## Needs JT Attention
- Approve or defer OpenClaw update path; current runtime is behind the active release train.
- Decide whether to rotate/remove the n8n MCP token found in Claude settings.
- Gateway/Codex process load should be reviewed during a quiet window if it stays above thresholds.
