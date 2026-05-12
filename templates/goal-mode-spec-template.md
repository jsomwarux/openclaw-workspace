# Goal Mode Spec — [Goal Name]

Use for Codex `/goal`, OpenClaw TaskFlow, or any long-running autonomous/background agent work.

## Objective

[One durable objective. Bigger than one prompt, smaller than a backlog.]

## Why This Matters

[Business/product/user reason.]

## Allowed Scope

- [Files/dirs/projects the agent may edit]
- [Tools allowed]
- [External actions allowed, if any]

## Forbidden Scope

- [Files/dirs/config/auth areas not to touch]
- [External actions not allowed]
- [Behaviors to avoid]

## Required Inputs To Read First

- `[path or URL]`
- `[path or URL]`

## Done State / Stopping Condition

The goal is complete only when all are true:

- [ ] [Specific artifact exists]
- [ ] [Specific test/build/check passes]
- [ ] [Specific output matches expected behavior]
- [ ] [No required item remains unverified]

## Validation Commands / Evidence

```bash
[command]
```

Expected evidence:
- [What command/output proves]

## Checkpoints / Progress Log

1. [Checkpoint 1]
2. [Checkpoint 2]
3. [Checkpoint 3]

At each checkpoint, append a short progress log entry:
- timestamp
- what changed
- what was verified
- what remains
- whether blocked
- next action

Progress log path:
- `[tasks/goal-log.md or project-specific log path]`

## Board / Visibility

Goal work should be visible in Mission Control or the relevant project board.

- Board task: `[link/title/id]`
- Status values: `queued / active / paused / blocked / budget-limited / complete`
- Update cadence: `[after each checkpoint or at least every N minutes]`
- Human review trigger: `[what should make JT review/approve]`

## Budget / Stop Rules

Stop and ask or mark blocked if:
- [time/token/run budget reached]
- [test fails the same way twice]
- [missing credential/auth/input]
- [scope conflict]
- [would require destructive/external action]

## Completion Audit

Before marking complete, verify every requirement against current state:

| Requirement | Evidence | Status |
|---|---|---|
| [req] | [file/test/output] | [proved/incomplete/missing] |

## Mission Control Tracking

- Task title: `[Title]`
- Owner: `eve` or `JT`
- Done state: `[same as stopping condition]`
- Review trigger: `[date/event]`
