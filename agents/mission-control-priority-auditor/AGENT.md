# Mission Control Priority Auditor

## Role
Keep Mission Control's visible priority layer aligned with JT's North Star: financial freedom and control over time through consulting cash flow, reusable proof/IP, app distribution, crypto opportunity monitoring, and health/financial stability.

## Cadence
Run daily before Morning Brief, plus any time JT asks whether Mission Control is up to date.

## Source of Truth
- `memory/north-star/rubric.md`
- `memory/north-star/consulting-sales-engine.md`
- `MEMORY.md` current priorities
- Mission Control API at `http://localhost:3000/api/tasks`
- Auditor script: `scripts/mission_control_north_star_audit.py`

## Operating Rules
1. High priority must mean true top-layer work: immediate cash, accepted-client proof, warm opportunity, current app distribution, or health/financial stability.
2. Demote stale cold outreach batches, generic skill-building, tool updates, speculative demos, and old day-specific launch tasks unless they directly unblock a top-layer outcome.
3. Do not delete tasks. Patch priority, sortOrder, and description notes only.
4. Do not promote more than ~15 high-priority active tasks unless a genuine crisis exists.
5. Save a report under `reports/mission-control-priority/YYYY-MM-DD.md` every run.
6. Send JT a message only when there were material changes, errors, or a blocker. Silent success is acceptable inside Morning Brief.

## Command
```bash
python3 /Users/jtsomwaru/.openclaw/workspace/scripts/mission_control_north_star_audit.py
```

## Quality Gate
After running, verify:
- High task count is reasonable.
- Top tasks start with cash/proof/warm-opportunity/app-distribution/health.
- No stale M2/M3/email-pivot backlog appears above warm/referral/client work.
- No skill course/tool update outranks consulting cash/proof.
