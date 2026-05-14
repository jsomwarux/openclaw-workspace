# Mission Control Task Hygiene Audit — 2026-05-13

## Grade

**Before: B-**

Mission Control was usable at the top layer but noisy underneath. The board had 320 active tasks, 23 true high-priority tasks after North Star audit rules, 263 active quality gaps, stale outreach chains, and generator drift that could recreate bad tasks.

**After: B+**

The high-priority layer is now controlled and aligned. Safe cleanup reduced active tasks to 307, archived 12 clearly superseded outreach-chain tasks, patched 3 priority/audit-rule items, and added generator guardrails so the same classes of tasks are less likely to reappear. Not A/A+ yet because the backlog still has 251 active task-quality gaps and 307 active tasks.

## Inventory Snapshot

| Metric | Before | After |
|---|---:|---:|
| Visible non-archived tasks | 462 | 451 |
| Active tasks (`todo` + `in-progress`) | 320 | 307 |
| High active tasks | 23 | 23 |
| Uncontrolled high tasks | 2 | 0 |
| Active task quality gaps | 263 | 251 |
| Exact normalized duplicate title groups | 0 | 0 |

## Current Active Counts

- Status: {'todo': 305, 'done': 144, 'in-progress': 2}
- Priority: {'medium': 191, 'low': 93, 'high': 23}
- Top active projects: {'Consulting': 129, 'Skills': 68, 'Job Market': 35, 'passive-income': 23, 'App Marketing': 12, 'Content': 11, 'Operations': 6, 'Apps': 6, 'Vista': 5, 'Crypto': 2}
- Active high-priority layer: 23 tasks
- Archived tasks verified via `GET /api/tasks?include=archived`: 432

## What Changed

### Mission Control records patched

1. `Weekly systems review: prune cron cap + fix gateway throttle` — added explicit North Star audit rule coverage so it no longer appears as uncontrolled high.
2. `Harden cost/cron/security layer to A+ after 2026-05-13 audit` — added explicit North Star audit rule coverage.
3. `Autoresearch: add deterministic cost-cap wrapper` — normalized sortOrder from 320 to 140 under skill/job-market noise rule.
4. Archived 12 stale outreach-chain tasks clearly superseded by current M4 final tasks:
   - FCM/First Class Management: 5 archived
   - ProRealty USA: 4 archived
   - Atlas NYC Property Management: 3 archived

No tasks were deleted.

### Files patched

- `scripts/mission_control_north_star_audit.py`
  - Added explicit operations top rules.
  - Added quality-gate reporting for first action / why / done / owner / priority / status.
  - Added count breakdowns to audit output.
- `scripts/outreach_email_pivot.py`
  - Improved duplicate detection across FCM/First Class title variants.
  - Changed new email-pivot tasks from high to low priority.
  - Changed generated descriptions to include First action / Why it matters / Done looks like.
- `scripts/build_ideas_sync.py`
  - Changed new job-market build-idea descriptions to include First action / Why it matters / Done looks like.
- `reports/mission-control-priority/2026-05-13.md`
  - Live North Star audit report with changes and quality gaps.
- `memory/audits/xhigh-systems/tmp/mc_tasks_before.json`
  - Snapshot before this audit.
- `memory/audits/xhigh-systems/tmp/mc_tasks_after.json`
  - Snapshot after cleanup.

## Validation

- Bootstrap budget check run first:
  - `AGENTS.md` 27,863 bytes (<28k but tight)
  - `MEMORY.md` 19,161 bytes (<20k but tight)
  - `TOOLS.md` 13,581 bytes (<16k)
  - `HEARTBEAT.md` 14,330 bytes (<16k)
- `python3 -m py_compile scripts/mission_control_north_star_audit.py scripts/outreach_email_pivot.py scripts/build_ideas_sync.py` passed.
- `python3 scripts/mission_control_north_star_audit.py --dry-run` after cleanup:
  - changes: 0
  - errors: 0
  - uncontrolled_high: 0
  - active_before/after: 306 before creating this follow-up task, then 307 after follow-up task creation
- Archived records verified through `/api/tasks?include=archived`.
- No destructive deletes were used.

## Remaining Blockers

1. **Backlog size is still too high:** 307 active tasks is not humane. Target should be <200 active, ideally <125 visible active.
2. **Quality gaps remain large:** 251 active tasks still miss at least one of first-action/why/done-state gates. This is mostly older Consulting, Skills, Job Market, and passive-income backlog.
3. **Generator hygiene is partial:** app marketing generator is good; email pivot and job-market build ideas are now patched; older skills/research/outreach generators still need review.
4. **Cold outreach clutter remains:** many low-priority review/send tasks may be stale, but they need evidence from pipeline files before archiving. I only archived chains where a current M4 final clearly superseded earlier steps.
5. **Done/archived visibility is confusing:** default `/api/tasks` returns done tasks but not archived tasks. The UI/API might still feel noisy unless done tasks auto-archive reliably.

## Follow-up Created

Created MC task: `Mission Control hygiene: retire stale backlog + fix task quality gates` (`j576zn0e3pag6dpmxfx99t8k7986mp6x`).

First action: open this report and work the remaining blockers, starting with generators that still create tasks without first-action/why/done-state gates.

## Final Assessment

Honest **B+**. The top layer is now sane and safe to use. The system is not yet A-level because too much stale backlog remains, but the highest-risk failure mode — high-priority drift and generator recontamination — is materially reduced.
