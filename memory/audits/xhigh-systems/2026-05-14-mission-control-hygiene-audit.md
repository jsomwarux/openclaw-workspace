# Mission Control Hygiene Audit — 2026-05-14

## Grade

**Before this audit: A-**

The 2026-05-13 hardening materially improved the board: active tasks were already below the stated A+ blocker threshold of 200, exact/fuzzy duplicate groups were zero, and strict task-contract gaps were near zero. The regressions found this morning were mostly guard drift, not board collapse: 7 valid high-priority tasks were not encoded in `TOP_RULES`, and 6 active descriptions missed the exact strict marker wording.

**After this audit: A**

The live board is now structurally clean and below the prior A+ blocker threshold: **196 active tasks**, **25 high-priority tasks**, **0 uncontrolled high**, **0 strict quality gaps**, **0 duplicate groups**. I would not call it A+ yet because the board still has **89 outreach-like active tasks** and **50 stale-like outreach/follow-up tasks**; many may be useful, but they need evidence-backed prune/merge work so the board stays humane.

## A+ Scale Breakdown

| Area | Grade | Evidence |
|---|---:|---|
| Priority correctness | A | 25 high active; 0 uncontrolled high after updating explicit North Star rules. |
| Task description quality | A | 0 strict active gaps for `First action:` / `Why it matters:` / `Done state|Done looks like:` plus owner/priority/status. |
| Duplicate/stale control | B+ | 0 exact/fuzzy duplicate groups, but 50 stale-like outreach/follow-up tasks remain. |
| North Star alignment | A | High layer is explicitly consulting cash/proof, financial stability, app distribution, health/content ops, and protected infra. |
| Backlog volume | A- | 196 active tasks is under the prior <200 blocker threshold, but still above the humane target of <125. |
| Automation/guard coverage | A- | North Star auditor, app marketing generator, outreach update, email pivot, and build ideas sync compile and enforce structured task contracts; remaining weakness is stale outreach pruning requiring source evidence. |

## Current Inventory Snapshot

| Metric | Current |
|---|---:|
| Visible non-archived tasks | 350 |
| Archived tasks | 567 |
| Active tasks (`todo` + `in-progress`) | 196 |
| Active high-priority tasks | 25 |
| Uncontrolled high-priority tasks | 0 |
| Strict active quality gaps | 0 |
| Exact normalized duplicate title groups | 0 |
| Fuzzy duplicate groups | 0 |
| Outreach-like active tasks | 89 |
| Stale-like active tasks | 50 |
| Active tasks older than 90 days | 0 |

Current active counts:
- Status: `{'todo': 195, 'done': 154, 'in-progress': 1}`
- Active priority: `{'medium': 121, 'low': 50, 'high': 25}`
- Top active projects: Consulting 93, Job Market 24, passive-income 15, App Marketing 13, Skills 12, Content 11, Apps 7, Operations 6, Health 2, Vista 2.
- Age buckets: `{'<=7d': 78, '8-14d': 34, '15-30d': 45, '31-60d': 21, '>60d': 18}`

## Files Inspected

- `mission-control/app/api/tasks/route.ts`
- `mission-control/convex/tasks.ts`
- `scripts/mission_control_north_star_audit.py`
- `scripts/outreach_update.py`
- `scripts/outreach_email_pivot.py`
- `scripts/build_ideas_sync.py`
- `scripts/app_marketing_task_generator.py`
- `memory/audits/xhigh-systems/2026-05-13-mission-control-task-hygiene.md`
- `memory/audits/xhigh-systems/2026-05-13-mission-control-a-plus-hardening.md`
- `reports/mission-control-priority/2026-05-14.md`
- `reports/mission-control-priority/2026-05-14-dry-run.md`
- Live Mission Control task API: `http://localhost:3000/api/tasks` and `http://localhost:3000/api/tasks?include=archived`

## Files Changed

- `scripts/mission_control_north_star_audit.py`
  - Updated `TOP_RULES` fragments to match the current high-priority task titles:
    - Altmark redacted proof screenshots
    - Strategy Jobs Pack first real send/use
    - Aya proof-safe evidence before referral ask
    - Relationship stale-contact refresh
    - Vista App Store vendor number
    - Health Telegram inbound wiring
    - Content posted-reply wiring
  - Adjusted Nash directory listing sort order from 55 to 56 to avoid collision with the content posting task.

- Mission Control task records, safe description-only patches:
  - Reworded 5 warm-up comment tasks from `Why this prospect matters:` to strict `Why it matters:`.
  - Reworded `Content posting: wire Telegram posted replies to local handler` to include strict `First action:` and `Why it matters:` markers.

No tasks were deleted. No external messages were sent. No auth/model config was touched.

## Verification Commands / Results

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
# AGENTS 27013, MEMORY 19541, TOOLS 14776, HEARTBEAT 15578 — all under budget.

python3 -m py_compile \
  scripts/mission_control_north_star_audit.py \
  scripts/outreach_update.py \
  scripts/outreach_email_pivot.py \
  scripts/build_ideas_sync.py \
  scripts/app_marketing_task_generator.py
# passed

python3 scripts/app_marketing_task_generator.py --no-fetch --json
# total_specs=13, errors=[]

python3 scripts/build_ideas_sync.py
# ok=true, pushed=0, skipped=17, ideas=17

python3 scripts/mission_control_north_star_audit.py
# ok=true, active_before=196, active_after=196, high_after=25, changes=30, errors=0, uncontrolled_high=0

python3 scripts/mission_control_north_star_audit.py --dry-run
# ok=true, active_before=196, active_after=196, high_after=25, changes=0, errors=0, uncontrolled_high=0
```

Independent live API classifier after patches:

```json
{
  "visible_non_archived": 350,
  "archived": 567,
  "active": 196,
  "active_priority": {"medium": 121, "low": 50, "high": 25},
  "high_active": 25,
  "uncontrolled_high": 0,
  "quality_gaps": 0,
  "exact_duplicate_groups": 0,
  "fuzzy_duplicate_groups": 0,
  "outreach_like_active": 89,
  "stale_like_active": 50,
  "old90_active": 0
}
```

## Remaining Blockers

1. **Outreach/follow-up volume:** 89 outreach-like active tasks and 50 stale-like tasks are still too much cognitive surface area, even though they are low/medium and structured.
2. **Humane backlog target:** 196 active tasks is under the prior A+ blocker threshold, but the board will feel sharper below 125 active.
3. **Report semantics:** `/api/tasks?include=archived` returns archived-only, not all tasks. The name is slightly misleading and should be treated carefully in future scripts.
4. **North Star rule upkeep:** high-priority titles changed after the last pass, which made 7 valid high tasks look uncontrolled until `TOP_RULES` was updated. Weekly review should either keep title fragments stable or update the rule file whenever a high task title changes.

## Recommendation for JT-facing Summary

Mission Control is now **A-level and safe to use**: active backlog is down to 196, high-priority drift is zero, task descriptions pass the strict quality gate, and duplicates are clean. The only thing keeping it from true A+ is outreach backlog volume — next pass should prune/merge evidence-backed stale outreach until active tasks are closer to 125.
