# Weekly Systems Review — 2026-05-31

## Executive Summary
- Overall grade: B. Core gateway/process/config/file integrity is healthy, but cron hygiene is not clean.
- Jobs checked: 51.
- Current cron issues: 7 errored jobs, 1 never-run job, no near-timeout jobs, no bad delivery statuses on announce jobs.
- Fixes applied this run: patched `t3-cold-hook` and `prospect-discovery` cron payload guardrails, hardened Weekly Systems Review live-posting verifier handling, enrolled `reelfarm-intel` in autoresearch, created MC follow-up task `j574ab89vdkq4t8vmfbs8m446s87rxm6`.

## Cron Health
Errored jobs:
- `fe575759-c8b1-4715-ae5a-0dbe034b3c9b` — `reddit-karma-daily-reminder`, consecutiveErrors=1. Latest error: bare `python3 scripts/web_search.py` failed. Current payload already contains env-sourced web-search hardening.
- `eve-job-market-daily-005` — `Job Market Daily Research`, consecutiveErrors=3. Latest error: `verify-live-posting.py` run without required URL. Current payload already requires URL + `--soft-exit`; needs next run or targeted debug to clear.
- `33b8b0a2-e86c-4f51-aa4f-b8537def3107` — `Viral Post Swipe File — X Research`, consecutiveErrors=1. Latest error: inline Python/heredoc tool failure. Current payload already bans inline Python/heredocs.
- `4c437ff5-02cd-4288-8e6e-6e6fc07203ce` — `Skills & API Researcher — Daily Scan`, consecutiveErrors=2. Latest error: bare `bun kb.ts` cwd failure. Current payload already requires `cd ~/.openclaw/workspace/knowledge && bun kb.ts ...`.
- `3ed01a8a-c3fb-4673-9ae0-993611e94c5a` — `t3-cold-hook`, consecutiveErrors=1. Latest error: proof-log/memory guard chained command failure. Patched this run to run proof commands separately and report partial success when drafts deliver but proof logging fails.
- `ebb843af-e752-4c65-923d-540d5ff5ad3f` — `prospect-discovery`, consecutiveErrors=1. Latest error: duplicate check treated no-match search as failure. Patched this run to use `rg ... || true` and interpret empty output as no duplicate.
- `b2ca53ab-0c07-4a22-8424-9d39bf988405` — `Weekly Systems Review`, consecutiveErrors=1. Latest error: strict job-market live-posting verifier exited nonzero during systems audit. Patched after the run so systems-review audits use `verify-live-posting.py "[POSTING_URL]" --json --soft-exit` for classification/expiry checks, reserve strict exit behavior for apply/package gates, and never run the verifier without a URL.

Never-run job:
- `e7d45070-1443-4cca-9776-8b016d97e225` — `passive-income-strategist-delivery-guard`. Flagged for JT/Eve follow-up; it is scheduled after the strategist run and has not fired yet.

Timing and delivery:
- Near-timeout jobs: none.
- Announce jobs with bad `lastDeliveryStatus`: none.
- Sunday 10AM conflict: only Weekly Systems Review runs in the Sunday 10AM hour.
- Invocation volume: 51 jobs total. Rough weekday scheduled invocations from cron expressions: 36/day, above the old 20/day cap. `scripts/cron_volume_guard.py` passes under the newer executable thresholds: 208.46 weekly invocations, 29.78/day average, 25.78 agentTurn/day average, 0 unknown schedules, no warnings.

## File Budgets
- `AGENTS.md`: 24,488 / 28,000 bytes (87.5%).
- `MEMORY.md`: 19,578 / 20,000 bytes (97.9%). Near cap; trim before major appends.
- `TOOLS.md`: 14,963 / 16,000 bytes (93.5%). Near cap; archive old/tool-detail sections before major appends.
- `HEARTBEAT.md`: 3,612 / 16,000 bytes (22.6%).

## Process Health
- Gateway process: healthy and reachable via `openclaw status`, pid 1365.
- Gateway RSS: ~818 MB, CPU sample 3.0%. Memory is above the 500 MB flag threshold, but CPU is not runaway.
- Transient node processes at ~130% CPU were current cron/tool workers under 10 minutes, not flagged as sustained runaway.
- Watchdog: `com.openclaw.gateway-watchdog` loaded.

## LaunchAgent Config
- `ai.openclaw.gateway` ThrottleInterval: 10. OK.
- `com.openclaw.gateway-watchdog` StartInterval: 600. OK, at max allowed interval.

## Version
- Current: OpenClaw 2026.5.22 (`a374c3a`).
- Local `openclaw status`: update available, npm 2026.5.28.
- Web check: GitHub releases result shows `2026.5.28-beta.1` published recently.
- Action: note only. No update performed because OpenClaw updates require JT approval.

## Plugin Audit
- `~/.claude/settings.json`: `enabledPlugins.context-mode@context-mode` is `false`.
- Other enabled Claude plugin: `claude-warden@claude-warden-marketplace`.
- `~/.openclaw/extensions/`: expected `lossless-claw` plus `.openclaw-install-backups`.
- Recurring warning: duplicate lossless-claw plugin id is still emitted by OpenClaw CLI.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: exists/readable, 28,598 bytes.
- `scripts/gateway-watchdog.sh`: exists/readable, 7,038 bytes.
- `health/health.sqlite`: exists/readable, 32,768 bytes.
- `tasks/pending.jsonl`: valid JSONL, 3,870 bytes.

## Weekly Maintenance Split
Autoresearch:
- Modified repeated/scorable files already registered: `portfolio-card`, `t3-cold-hook`, `skills-researcher`, `app-marketing/product-content`, `content-scheduler`, `cold-email`.
- New enrollment: `reelfarm-intel`, because daily/weekly prompts are recurring, scoreable, and recently changed. Added `agents/autoresearch/checklists/reelfarm-intel.md` and registry row in `agents/autoresearch/targets.md`.

Future signals:
- Reviewed active trigger conditions against current project reality. No signal graduated this run.

Passive-income queue:
- Mission Control reachable.
- Found 10 `[PI]` todo tasks with `sortOrder >= 500`.
- None are older than 60 days, so nothing pruned.
- No newly viable idea promoted; current future-signal trigger still requires Altmark proof acceptance plus consulting/revenue/distribution pull.

Cost review:
- 7-day spend: $2.356.
- Largest cost: `Cron: prospect-discovery` on 2026-05-27 at $2.132.
- Monthly pace: $10.02 against $50 target, $39.98 headroom.
- Routing note: Groq/Llama unused this week; simple cron routing can be reviewed separately.

Training / regression:
- Added `## Weekly Systems Review — 2026-05-31` entry to `memory/training/training-log.md`.
- Current repeat failure class remains useful-work-before-tool-failure: inline scripts, no-match searches, wrong cwd, strict verifier exits, or missing verifier arguments making cron status red after useful output.

## Follow-Up
- Created high-priority MC task: `Fix current errored crons from 2026-05-31 systems review` (`j574ab89vdkq4t8vmfbs8m446s87rxm6`).
- Needs JT attention: approve/schedule OpenClaw update when ready; decide whether to keep the never-run passive-income strategist guard or fire it manually after today's 3PM strategist run. Current errored cron statuses should clear on next scheduled safe runs or targeted debug, not via duplicate content reruns.
