# Mission Control Task Hygiene A+ Hardening — 2026-05-13

## Grade

**Before: B+**

The prior pass controlled the high-priority layer, but Mission Control still had 308 active tasks and 260 strict task-contract gaps when measured against `First action:` / `Why it matters:` / `Done state|Done looks like:` markers.

**After: A-**

The task board is now structurally clean: high-priority drift is zero, strict quality gaps are zero, and the generator/auditor layer now enforces concrete task contracts. It is not A+ yet because active backlog is still 298 tasks; the remaining blocker is volume/noise reduction, not task-description hygiene.

## Inventory Snapshot

| Metric | Before A+ hardening | After hardening |
|---|---:|---:|
| Visible non-archived tasks | 452 | 443 |
| Active tasks (`todo` + `in-progress`) | 308 | 298 |
| High active tasks | 23 | 23 |
| Uncontrolled high tasks | 0 | 0 |
| Strict active quality gaps | 260 | 0 |
| Exact normalized duplicate title groups | 0 | 0 |

## Current Active Counts

- Status: `{'todo': 296, 'done': 145, 'in-progress': 2}`
- Active priority: `{'medium': 192, 'low': 83, 'high': 23}`
- Top active projects: Consulting 119, Skills 68, Job Market 35, passive-income 23, App Marketing 12, Content 11, Apps 7, Operations 6, Vista 5.

## Tasks Changed

Total MC records changed: **126**

Breakdown:
- **10 archived** as clearly superseded stale outreach/batch tasks. No tasks were deleted.
- **6 high-priority tasks** patched with explicit done states.
- **51 passive-income / job-market idea tasks** patched with structured first-action/why/done contracts and parked lower where appropriate.
- **48 older consulting/app/content/misc tasks** patched with structured task contracts.
- **181 additional auditor-driven normalization patches** applied by `scripts/mission_control_north_star_audit.py` after the script fix, mostly adding explicit contracts/notes to legacy Skill/Job Market/Cold Outreach items.
- **1 existing MC blocker task** updated with the remaining A+ blocker and concrete first action.

High-confidence archived examples:
- Superseded April 1 M2 batch confirm task.
- Superseded April 1 batch M2 task.
- Older G-Net / Maxwell M2 tasks superseded by active email-pivot tasks.
- Older Petri, Harlem, Superior Plumbing, and New York Plumbing generic review/send tasks superseded by more specific later tasks.

## Files Changed

- `scripts/mission_control_north_star_audit.py`
  - Fixed PATCH routing to the actual `/api/tasks` endpoint with `{id, ...fields}`.
  - Added strict quality gates for `First action:`, `Why it matters:`, and `Done state:` / `Done looks like:`.
  - Added structured legacy task-contract generation.
  - Kept explicit TOP_RULES for high-priority North Star layer.
  - Reports uncontrolled high tasks, quality gaps, counts by status/priority/project.

- `scripts/outreach_update.py`
  - Uses the working PATCH endpoint instead of stale `/api/tasks/[id]` style.
  - Creates follow-up tasks as low-priority structured tasks, not high-priority clutter.
  - Adds `slug` and `pipelineStage` to follow-up task payloads.
  - Improves closure matching for active Review + Send / Email Pivot tasks.

- `scripts/outreach_email_pivot.py`
  - Already contained the prior pass improvements; revalidated.

- `scripts/build_ideas_sync.py`
  - New generated build-idea tasks now include structured first-action/why/done descriptions.
  - Adds a stable dedupe slug and `pipelineStage: triage`.

## Validation Results

Commands run:

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
python3 -m py_compile scripts/mission_control_north_star_audit.py scripts/outreach_email_pivot.py scripts/build_ideas_sync.py scripts/outreach_update.py scripts/app_marketing_task_generator.py
python3 scripts/app_marketing_task_generator.py --no-fetch --json
python3 scripts/build_ideas_sync.py
python3 scripts/mission_control_north_star_audit.py --dry-run
```

Validation outcomes:
- Bootstrap files within budget at start: AGENTS 26,829; MEMORY 18,570; TOOLS 13,581; HEARTBEAT 14,330.
- Python compile: passed.
- App Marketing generator offline validation: 13 specs, 0 errors.
- Build ideas sync validation: 17 ideas, 0 pushed, 17 skipped; no duplicate creation.
- Final North Star audit dry-run: `changes=0`, `errors=0`, `uncontrolled_high=0`, `active_before=298`, `high_after=23`.
- Final strict quality classifier: `quality_gaps=0`.

## Remaining Blockers

1. **Active backlog volume remains too high:** 298 active tasks is still too much. Target for A+ should be <200, ideally <125 visible active.
2. **Cold outreach backlog remains broad:** 69 active outreach-like tasks remain. Many may be valid, but archiving more needs source-file evidence or an explicit acquisition reset.
3. **Strategic high layer is controlled but large:** 23 high tasks is acceptable for now because all are explicit North Star rules, but weekly review should keep it from expanding.

## Follow-up Blocker Task

Updated existing MC task: `Mission Control hygiene: retire stale backlog + fix task quality gates` (`j576zn0e3pag6dpmxfx99t8k7986mp6x`).

Current first action: open this report, then work the remaining backlog-size blocker by archiving/merging only evidence-backed stale Consulting outreach and old app/content tasks.

## Final Assessment

**A- now.** The structural hygiene problem is fixed: every active task has a concrete first action, reason, and done state; high-priority drift is zero; generator drift is materially reduced. The only reason this is not A+ is the remaining backlog volume.
