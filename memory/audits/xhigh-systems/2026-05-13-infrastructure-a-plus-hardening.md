# XHigh A+ Hardening — Autoresearch / Weekly Review / Cost-Cron-Heartbeat-Security
Date: 2026-05-13

## Scope
Hardening pass after xhigh audits returned A- for:
- Autoresearch / self-improvement
- Weekly Intelligence / Weekly Systems Review
- Cost / Cron / Heartbeat / Security

## Fixes Applied

### Autoresearch: deterministic cost cap
- Created `scripts/autoresearch_cost_guard.py`.
- Patched `agents/autoresearch/weekly-sweep-prompt.md` to require the guard before any target selection or model-heavy scoring.
- Patched `Autoresearch Sweep` cron to run the guard first.
- Reduced recurring sweep bounds from 3 inputs / 5 rounds to 2 inputs / 2 rounds so the recurring job fits the $0.50 cap.
- Kept deeper runs available on-demand, but no longer as the recurring default.

Validation:
- `python3 scripts/autoresearch_cost_guard.py --model openai-codex/gpt-5.5 --cap 0.50 --json`
- Result: PASS, estimated $0.375, cap $0.50.

### Heartbeat: no-op fixed
- Converted `eve-heartbeat-2h-002` from `systemEvent` main-session payload to isolated `agentTurn` with observable protocol steps.
- Required mission-control audit, cost alert check, cron health scan, daily-note logging, and final `HEARTBEAT_OK`/blocked/fixed summary.
- Forced proof run completed with model usage and duration 7.389s instead of prior 1–2ms payload echo.

Validation:
- Latest forced run: status ok, summary `HEARTBEAT_OK`, duration 7389ms.

### Backup escalation
- Patched `scripts/backup.sh` to collect nonfatal failures into `FAILURES[]`.
- Nonfatal cost snapshot / GitHub push / Drive token refresh failures now write `reports/backup-alerts/YYYY-MM-DD.md` and exit code 2 instead of silently passing.
- Local backup still completes before escalation.

Validation:
- `bash -n scripts/backup.sh` passed.

### Cron monitor and posture
- Replaced stale infinite-loop `scripts/cron_monitor.py` with a one-shot OpenClaw cron health scan.
- Created `scripts/cron_posture_report.py` to report enabled jobs, estimated daily/weekly invocation posture, dense schedule clusters, missing failure alerts, deleteAfterRun, and announce jobs missing empty-output guard hints.
- Added failure alerts to every enabled cron job that lacked one.

Validation:
- `python3 scripts/cron_monitor.py` → ok true, problem_count 0.
- `python3 scripts/cron_posture_report.py` → enabled jobs 53, estimated weekly invocations 248, estimated daily average 35.43, missing failure alerts [], deleteAfterRun [].
- `openclaw cron list --json` follow-up confirmed missing enabled failure alerts: 0.

## Remaining Structural Issue

### Cron volume/cap mismatch
The system no longer has unprotected enabled jobs, but live cron posture still exceeds the documented ≤20/day cap:
- Enabled jobs: 53
- Estimated weekly invocations: 248
- Estimated daily average: 35.43

This is now deterministically reported in `reports/cron-posture/YYYY-MM-DD.md/json`, not hidden.

Do not randomly disable jobs. Next A+ step is a deliberate cron consolidation/pruning pass by category:
1. Merge or decrowd Sunday 8–9AM clusters.
2. Review daily low-value content/social jobs versus current priorities.
3. Convert pure reminders/low-risk checks to less frequent schedules.
4. Preserve critical revenue/health/security jobs.

## Weekly Systems Review Proof
A focused proof run was spawned after cron history did not immediately show the forced run. Proof report expected at:
- `memory/audits/xhigh-systems/2026-05-13-weekly-systems-review-proof.md`

## Honest Grades After Hardening
- Autoresearch: A+ for recurring sweep cost enforcement and failure alerts. Pending backlog quality still depends on future runs, but the recurring safety/cost blocker is fixed.
- Heartbeat / cost / cron security: A for protections and visibility; not full A+ until cron volume/cap mismatch is pruned or formally rebaselined.
- Weekly Systems Review: pending proof run completion.
