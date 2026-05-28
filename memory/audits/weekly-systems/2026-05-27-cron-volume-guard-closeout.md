# Cron Volume Guard Closeout — 2026-05-27

## Decision
Do not disable essential crons to hit the retired blunt `<=20/day` cap. Replace it with an executable guardrail:

- Hard cap: <=35 scheduled invocations/day average
- Hard cap: <=28 agentTurn invocations/day average
- Warning territory: >30 scheduled invocations/day average
- Unknown enabled schedules: max 1

## Verification
Command:

```bash
python3 scripts/cron_volume_guard.py
```

Result:

- ok: true
- enabled jobs: 51
- estimated weekly invocations: 208.46
- estimated daily average: 29.78
- estimated agentTurn daily average: 25.78
- unknown enabled schedules: 0
- warnings: []

## Other Gates
- Gateway LaunchAgent throttle: `ThrottleInterval=10`
- Gateway load sample: ~771MB RSS / 0.3% CPU
- HEARTBEAT.md budget: 3,612 bytes after compaction
- Extended heartbeat rules moved to `docs/agents/heartbeat-extended-rules.md`

## Mission Control
Task `Fix weekly systems review drift: cron cap, gateway load, bootstrap budgets` closed as done. No essential cron was disabled or deleted.
