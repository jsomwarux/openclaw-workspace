# XHigh Systems Audit — Cost / Cron / Heartbeat / Security

Date: 2026-05-13
Workspace: `/Users/jtsomwaru/.openclaw/workspace`

## Grades

- **Before grade:** B+
- **After grade:** A-

This is materially stronger after the audit, but not an honest A+. The remaining blockers are structural, not cosmetic.

## Scope Inventory

Audited:
- Bootstrap budgets: `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `HEARTBEAT.md`
- Live cron state via `openclaw cron list --json`
- Recent runs for heartbeat, morning brief, critical-files-integrity, pending-task processor, crypto morning, outreach pipeline, and job-market daily
- Scripts: `scripts/cost-tracker.py`, `scripts/critical-files-integrity.py`, `scripts/backup.sh`, `scripts/cleanup-sessions.py`, `scripts/cron_monitor.py`, `scripts/log-proof.py`
- LaunchAgent visibility for backup/session cleanup/gateway/mission-control
- Backup and session cleanup logs
- Telegram delivery/failure-alert posture for critical user-facing jobs

## Files Changed

- `scripts/cost-tracker.py`
  - Switched cost/reporting day timezone from fixed UTC-5 to DST-aware `America/New_York` via `zoneinfo.ZoneInfo`.
  - Fixed stale monthly alert copy from `exceeds $75 cap` to `exceeds $50 cap`, matching the configured `$50` threshold/goal.

## Crons Changed

Added failure alerts to critical jobs that previously lacked them:

| Cron | Change |
|---|---|
| `eve-heartbeat-2h-002` — Heartbeat (4x/day) | Added Telegram failure alert after 1 error, 6h cooldown |
| `ee357abb-2b58-44b8-8f03-4c152611117d` — critical-files-integrity | Added Telegram failure alert after 1 error, 24h cooldown |
| `babd905a-1098-49dd-8700-772fef14f817` — Spanish Daily Lesson | Added Telegram failure alert after 1 error, 24h cooldown |

Verified final failureAlert values:
```text
[('eve-heartbeat-2h-002', {'after': 1, 'channel': 'telegram', 'to': '6608544825', 'cooldownMs': 21600000, 'mode': 'announce'}), ('ee357abb-2b58-44b8-8f03-4c152611117d', {'after': 1, 'channel': 'telegram', 'to': '6608544825', 'cooldownMs': 86400000, 'mode': 'announce'}), ('babd905a-1098-49dd-8700-772fef14f817', {'after': 1, 'channel': 'telegram', 'to': '6608544825', 'cooldownMs': 86400000, 'mode': 'announce'})]
```

## Validation Results

### Bootstrap budgets

```text
27863 AGENTS.md
19161 MEMORY.md
13581 TOOLS.md
15788 HEARTBEAT.md
76393 total
```

All are under budget, but `AGENTS.md`, `MEMORY.md`, and `HEARTBEAT.md` are close enough that this audit avoided appending to them.

### Cron state

- Enabled cron jobs: **53**
- `deleteAfterRun=true`: **none found**
- Current `lastRunStatus=error` or `consecutiveErrors>=2`: **0 found**
- Failure-alert configured jobs: **34**
- Announce-delivery jobs: **24**

Problem scan output:
```text
[]
```

### Critical recent-run checks

Checked `openclaw cron runs --id <id> --limit 1` for:
- `eve-heartbeat-2h-002`
- `eve-morning-brief-001`
- `ee357abb-2b58-44b8-8f03-4c152611117d`
- `f18cace3-b9e9-4d99-a7a3-625bb121b30c`
- `eve-crypto-morning-008`
- `651fa1da-84d7-44b3-8e10-6a46e1c05cf6`
- `eve-job-market-daily-005`

Findings:
- Morning brief latest run: `ok`, delivered.
- Crypto morning latest run: `ok`; run summary included `telegram_message_sent: true` and generated summary files.
- Critical-files-integrity latest run: `ok`; latest run summary said new refs were added and rerun passed.
- Outreach/job-market latest runs: `ok`; no direct delivery expected.
- Heartbeat latest run: `ok`, but see blocker below — the run lasted 1ms and summary was the payload text, which does not prove HEARTBEAT.md protocol execution.

### Script smoke checks

Passed:
```bash
python3 -m py_compile scripts/cost-tracker.py scripts/critical-files-integrity.py scripts/cleanup-sessions.py scripts/cron_monitor.py scripts/log-proof.py
python3 scripts/cost-tracker.py --check-alerts
python3 scripts/cost-tracker.py --check-runaway
python3 scripts/cost-tracker.py --brief
python3 scripts/critical-files-integrity.py
```

Smoke outputs:
- Cost alerts: `[]`
- Runaway alerts: `[]`
- Cost brief generated successfully.
- Critical files integrity: all critical files intact; no new files detected.

### Backup/session cleanup

- LaunchAgents visible: `com.openclaw.backup`, `com.openclaw.cleanup-sessions`, `ai.openclaw.gateway`, Mission Control services.
- Backup log shows successful local backup + workspace/pipeline pushes on 2026-05-13.
- Backup log also shows **nonfatal n8n-agent push failure** due to remote needing fetch first.
- Session cleanup ran 2026-05-13 03:00 and removed stale sessions safely.

## Remaining Blockers

1. **Heartbeat cron may be a no-op wake.** Latest `eve-heartbeat-2h-002` run completed in `1ms` with the payload itself as summary. That is not proof that HEARTBEAT.md checks ran. Needs proof or conversion from `systemEvent` payload to an agentTurn/protocol that produces observable audit output.
2. **Cron cap mismatch.** `AGENTS.md` says daily cap ≤20 cron invocations/day, but live state has 53 enabled jobs. Some are weekly/monthly, but the posture still needs a formal daily invocation count report and pruning/scheduling reconciliation.
3. **Backup nonfatal failures do not escalate.** `backup.sh` logs failed pushes as nonfatal; n8n-agent push failed on 2026-05-13. Local backup still succeeded, but repo backup drift can silently persist unless this creates an alert or MC task.
4. **Duplicate schedule clusters need review.** Two jobs share `0 3 * * *` and two weekly jobs share `0 18 * * 0`. This may be acceptable, but it conflicts with the “avoid collisions” posture unless documented or staggered.
5. **Telegram empty-message guard is global guidance, not consistently embedded in all announce payloads.** Critical no-new-findings jobs should explicitly skip Telegram sends when output is empty/all-clear. Many announce jobs are content-delivery jobs where this is lower risk, but it is not universally enforceable from live config.

## MC Follow-Up

Created Mission Control task:
- **Harden cost/cron/security layer to A+ after 2026-05-13 audit**
- Priority: high
- First action: prove/fix heartbeat execution, then add backup failure escalation and reconcile cron cap/noise.

## Final Assessment

The layer now catches more failures than before, especially protection-job failures. Cost tracker smoke checks pass, critical integrity passes, latest critical cron runs are mostly healthy, backup/session cleanup are running, and no `deleteAfterRun=true` or current error loops were found.

Do **not** call this A+ until heartbeat execution is proven and backup/cron-cap blockers are closed.
