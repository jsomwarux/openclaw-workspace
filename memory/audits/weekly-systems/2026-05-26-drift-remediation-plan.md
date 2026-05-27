# Systems Drift Remediation Plan — 2026-05-26

Source task: `Fix weekly systems review drift: cron cap, gateway load, bootstrap budgets`.

## Current snapshot
- Mission Control after audit: 304 active tasks, 4 high-priority tasks.
- Cron health: 52 jobs checked; no jobs with `consecutiveErrors >= 2`, no `lastRunStatus=error`, no suspicious delivery statuses.
- Config warning during cron list: duplicate `lossless-claw` plugin id; global plugin overrides global plugin path. Non-blocking but noisy.
- File sizes:
  - `AGENTS.md`: 27,013 / 28,000 chars
  - `MEMORY.md`: 19,940 / 20,000 chars
  - `TOOLS.md`: 15,139 / 16,000 chars
  - `HEARTBEAT.md`: 15,997 / 16,000 chars
- Gateway LaunchAgent: `ai.openclaw.gateway`; `ThrottleInterval` key present, value still needs direct plist value confirmation before edit.
- Gateway process: PID 29836 around 2.49 GB RSS and 5.4% CPU at sample time. Still above weekly systems review threshold.

## Remediation order
1. **Bootstrap budget first**
   - Compact `HEARTBEAT.md` below 15,000 chars before any future append.
   - Distill/archive old `MEMORY.md` details before it crosses 20,000 chars.
   - Regression check: `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md` must show `HEARTBEAT.md < 15000` and `MEMORY.md < 19500` after compaction.

2. **Gateway throttle second**
   - Confirm exact value with `plutil -p ~/Library/LaunchAgents/ai.openclaw.gateway.plist | grep ThrottleInterval`.
   - Set `ThrottleInterval` to `10` during a planned maintenance window, then restart via the approved gateway restart path.
   - Regression check: `plutil -p ...` returns `ThrottleInterval => 10` or higher, and gateway returns healthy status after restart.

3. **Gateway load third**
   - Re-sample gateway RSS/CPU after cleanup/restart.
   - If still >500 MB RSS or >5% CPU for 10+ minutes, inspect plugin/session load before changing cron volume.
   - Regression check: append before/after process sample to the weekly systems audit.

4. **Cron cap last**
   - Keep current jobs running while no errors exist.
   - Do not disable revenue/health/content/security jobs blindly.
   - Build a ranked consolidation list: duplicate Sunday reports, low-value announce jobs, and jobs that can fold into weekly systems review or command center.
   - Regression check: daily invocation estimate documented; either <=20 or the cap is explicitly revised with rationale.

## Blockers / caution
- `HEARTBEAT.md` compaction is the highest risk because it contains active cron behavior rules. It should be done as a focused edit with a before/after diff, not opportunistic deletion.
- LaunchAgent changes are stateful. Apply during a deliberate maintenance window, not during a random heartbeat unless gateway instability becomes urgent.
