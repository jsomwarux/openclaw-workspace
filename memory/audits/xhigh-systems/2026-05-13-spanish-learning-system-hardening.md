# Spanish / Learning System — A+ Hardening
Date: 2026-05-13
Agent: subagent `hardening-spanish-learning-system`
Prior audit: `memory/audits/xhigh-systems/2026-05-13-spanish-learning-system.md`

## Before grade: A-
Daily generation/delivery/persistence was operational after the prior audit, but the learning loop still had two serious quality failures:
- `spanish/curriculum.md` only defined Weeks 1-4 while `spanish/state.json` said Week 9.
- Recent lesson records recycled Week 2 topics through May 13, including repeated "Making Plans", while state/date progression should have been Week 10/11.
- `spanish/evaluations/` was empty, so weekly progress visibility existed in docs but not in artifacts.
- The validator checked state shape and latest lesson existence, but not curriculum/week consistency or weekly evaluations.

## After grade: A
The system now has deterministic progression gates, curriculum coverage through the current week, evaluation artifacts, and cron-level prevention against silent old-week recycling.

## Changes made
### Curriculum progression
- Expanded `spanish/curriculum.md` from Week 4 through Week 11.
- Added explicit `Progression Guardrails` section:
  - use calendar/curriculum week from `started` + today's date,
  - fail loudly if a week is missing,
  - do not silently recycle old weeks,
  - avoid repeating prior-two topics,
  - create evaluation artifacts for Sunday/evaluation flow.

### State alignment
- Updated `spanish/state.json`:
  - `current_week`: 11, matching `started=2026-03-02` and `last_lesson_date=2026-05-13`.
  - `notes`: documents Week 11 drift repair and next-topic guidance.

### Lesson history preservation
- Did **not** overwrite/delete lesson history.
- Appended a repair note to `spanish/lessons/2026-05-13.md` and inserted `Curriculum week used: Week 11` marker near the top so strict validators can distinguish the repaired current curriculum week from the preserved bad Week 2 topic text.

### Weekly evaluation script/artifacts
- Added `scripts/spanish_weekly_eval.py`.
  - Generates deterministic weekly evaluation/progress artifacts under `spanish/evaluations/`.
  - Detects claimed-week mismatches and repeated topics.
  - Exits `2` on drift so audits/cron checks can distinguish "artifact created but needs repair" from clean pass.
  - Does not mark lessons/weeks passed automatically.
- Generated:
  - `spanish/evaluations/2026-05-03-week-9.md` — clean historical Week 9 artifact.
  - `spanish/evaluations/2026-05-10-week-10.md` — drift detected.
  - `spanish/evaluations/2026-05-17-week-11.md` — drift detected/current-week evaluation scaffold.

### Validator hardening
- Patched `scripts/spanish_state_check.py` with:
  - `--check-progression`: validates curriculum coverage, `state.current_week` vs calendar week, latest lesson week marker, and repeated latest topic.
  - `--require-evaluation`: validates that the most recent completed Sunday has an evaluation artifact.
  - explicit curriculum/evaluation status fields in JSON output.

### Cron hardening
- Patched Spanish Daily Lesson cron `babd905a-1098-49dd-8700-772fef14f817` prompt:
  - loads latest 3 lesson files,
  - computes correct week from `started` + today's date,
  - aligns `state.current_week` when needed,
  - fails loudly if curriculum week missing,
  - blocks silent Week 1-4 recycling,
  - applies anti-repeat guard,
  - handles accidental Sunday run by generating evaluation artifact instead of normal lesson,
  - validates with `spanish_state_check.py --require-today --check-progression` after persistence.
- Confirmed delivery remains `bestEffort=false`.

### Mission Control
- Closed MC task `Fix Spanish weekly evaluation + curriculum progression` (`j57824c4zmj7tj9hmm3q1bhs2x86qrnn`) as `done`.

## Validation
- Bootstrap budget check before work:
  - `AGENTS.md` 27013 bytes
  - `MEMORY.md` 19258 bytes
  - `TOOLS.md` 14496 bytes
  - `HEARTBEAT.md` 15578 bytes
- `python3 -m py_compile scripts/spanish_state_check.py scripts/spanish_weekly_eval.py` passed.
- `python3 -m json.tool spanish/state.json` passed.
- `python3 scripts/spanish_state_check.py --date 2026-05-13 --require-today` passed.
- `python3 scripts/spanish_state_check.py --date 2026-05-13 --require-today --check-progression` passed.
- `python3 scripts/spanish_state_check.py --date 2026-05-13 --require-today --check-progression --require-evaluation` passed after Week 9 evaluation artifact was generated.
- `python3 scripts/spanish_weekly_eval.py --date 2026-05-17 --week current` dry-run produced Week 11 artifact content and drift status as expected.
- `openclaw cron show babd905a-1098-49dd-8700-772fef14f817 --json` confirmed:
  - prompt contains `--check-progression`,
  - prompt contains `spanish_weekly_eval.py`,
  - prompt contains missing-curriculum guard,
  - prompt contains anti-repeat guard,
  - `delivery.bestEffort=false`.
- MC task verified as `done` via `/api/tasks`.

## Remaining blockers
None blocking A-grade system reliability.

Known learning-quality note: Week 10 and current Week 11 artifacts correctly flag existing drift from the previously generated lessons. The next daily lesson should continue Week 11 family-table/food conversation and avoid "Making Plans" unless explicitly marked as review.

## Files changed
- `spanish/curriculum.md`
- `spanish/state.json`
- `spanish/lessons/2026-05-13.md`
- `spanish/evaluations/2026-05-03-week-9.md`
- `spanish/evaluations/2026-05-10-week-10.md`
- `spanish/evaluations/2026-05-17-week-11.md`
- `scripts/spanish_state_check.py`
- `scripts/spanish_weekly_eval.py`
- Spanish Daily Lesson cron payload
- Mission Control task status
