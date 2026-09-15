# Workout Program Redesign Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the active daily-workout source with a phased program balancing strength, aerobic health, athleticism, and conservative patellar-tendon rehabilitation.

**Architecture:** Establish `health/daily-workouts.md` as the stable canonical source and update only the existing automation payload's source path, preserving its 05:00 schedule and manual phase pointer. Add a standard-library validator and renderer so unsafe or internally inconsistent drift fails before delivery. Keep research rationale separate from concise daily cards.

**Tech Stack:** Markdown, Python 3 standard library, unittest, OpenClaw automation payload.

---

## Chunk 1: Stable source, rationale, and deterministic guard

### Task 1: Define source invariants with failing tests

**Files:**
- Create: `health/tests/test_daily_workout_source.py`
- Create: `health/validate_daily_workout_source.py`
- Create: `health/render_daily_workout.py`
- Create: `health/daily-workouts.md`
- Create: `health/workout-program-rationale.md`

- [ ] Test exact unchanged pointer values: `PHASE: 1`, `WEEK_IN_PHASE: 1`, `LIFT_ROTATION: A`, and the rule that only JT advances them.
- [ ] Test every phase for at least 150 formal aerobic minutes, symptom-safe substitutions, nonconsecutive impact sessions, and adequate recovery spacing.
- [ ] Test that Phase 1 excludes running, jumping, cutting, basketball, and StairMaster as training modalities.
- [ ] Test that heavy slow resistance tendon loading occurs Monday/Wednesday/Friday only; impact loading follows the phase-specific schedule and spacing rules; symptom-relief isometrics are optional, not hard daily work.
- [ ] Test explicit gates for StairMaster, run-walk, jumping/landing, deceleration, cutting, non-contact basketball, and full games.
- [ ] Test all 14 requested movements appear in a structured exercise audit with one role each: core, accessory, warm-up, later-phase, or excluded.
- [ ] Test the source says the diagnosis is a working hypothesis and requires sports-PT/sports-medicine assessment before cutting/contact return.
- [ ] Test red flags: swelling, locking/catching, instability/giving way, inability to bear weight, night/rest pain, worsening symptoms, chest pain, faintness, or disproportionate breathlessness.
- [ ] Test no legacy instruction says to continue through incomplete breathing or escalating pain.
- [ ] Write render tests for all seven weekdays and all four phases; assert session, duration, exercises, sets/reps, prescribed tempo for knee/tendon movements, knee work, and safety footer without contradictory evening work.
- [ ] Run the focused suite and confirm RED for missing implementation.

### Task 2: Implement the exact four-phase program

**Files:**
- Create: `health/daily-workouts.md`
- Create: `health/workout-program-rationale.md`
- Create: `health/validate_daily_workout_source.py`
- Create: `health/render_daily_workout.py`

**Phase 1, settle and build baseline capacity:**
- Mon/Wed/Fri: full-body strength A/B/C with one slow quadriceps/tendon movement each day; optional leg-extension isometric or Spanish squat before training only if it reduces pain.
- Tue: 45-minute Zone 2 swim or easy bike. Thu: 45-minute Zone 2 swim/bike; rower only if symptoms stay at baseline. Sat: 60-minute easy swim, bike, or brisk walk. Sun: rest or easy walk, not counted toward the formal target.
- Lift A: goblet squat 3x8 at 3-0-3; DB bench/push-up 3x8-10; chest-supported row 3x10; DB RDL 3x8; standing calf raise 3x12; suitcase carry 3x30-45 sec/side.
- Lift B: supported split squat 3x8/side at 3-0-3; DB overhead press 3x8; pulldown/assisted pull-up 3x8-10; hip thrust 3x10; soleus raise 3x15; Pallof press 3x10/side.
- Lift C: leg extension 3x10 at 3-1-3 in tolerated range; incline DB press 3x8-10; one-arm cable/DB row 3x10/side; hip hinge/back extension 3x10; tib raise 3x15; farmer carry 3x30-45 sec.
- Rotate at most two accessories after main work: band external rotation 2x12/side; hip-flexor iso 2x20-30 sec/side. Backward treadmill 5-8 minutes and TKE 2x15 are optional warm-up only.

**Phase 2, heavy strength and single-leg control:**
- Preserve the 45/45/60 low-impact aerobic schedule.
- Lift A2: goblet squat 4x6-8 at 3-0-2; DB bench 3x6-10; chest-supported row 3x8-10; DB RDL 3x8; standing calf raise 3x12; suitcase carry 3x45 sec/side.
- Lift B2: RFESS 4x6-8/side at 3-0-2; DB overhead press 3x8; pulldown/assisted pull-up 3x8-10; hip thrust 3x8-10; controlled 6-inch step-down 3x6/side; Pallof press 3x10/side.
- Lift C2: leg extension 4x8 at 3-1-2; single-leg box squat 2x6/side as controlled technique work; incline DB press 3x8; one-arm row 3x10/side; back extension 3x10; tib raise 3x15; farmer carry 3x45 sec.
- Reverse Nordic 2x6-8 may appear only as a later-phase accessory when pain remains ≤3/10.
- StairMaster re-enters only after seven stable days, pain-free normal stairs, and 3x8 controlled 6-inch step-downs. Start 10 minutes replacing, not adding to, one Zone 2 session; add 5 minutes per stable week.

**Phase 3, run and energy storage:**
- Use two strength days to protect recovery: Mon Lift A3; Thu Lift B3 plus 15-minute Zone 2 bike. A3 = goblet squat 3x6 at 3-0-2; DB bench 3x8; chest-supported row 3x10; DB RDL 3x8; standing calf raise 3x12; suitcase carry 3x45 sec/side. B3 = RFESS 3x6/side at 3-0-2; DB overhead press 3x8; pulldown 3x8; hip thrust 3x8; leg extension 3x8 at 3-1-2; Pallof press 3x10/side.
- Tue: 45-minute Zone 2 swim/bike. Wed and Sat are the only impact days, separated by a verified 72 hours. Sun: 60-minute Zone 2 swim/bike/brisk walk. Fri: rest/easy mobility.
- Week 1: Wed and Sat each use 30-minute 1:2 run-walk, establishing two stable run exposures before jumping. Week 2: Wed 30-minute run-walk; Sat bilateral landing 3x5 then 30-minute easy bike/swim. Week 3: Wed 30-minute run-walk; Sat pogos 3x15 then 30-minute easy bike/swim. Week 4: Wed 30-minute run-walk; Sat jump rope 3x30 sec or low countermovement jump 3x5, then 30-minute easy bike/swim.
- Formal aerobic minimum is 150 minutes every week: Tue 45 + Wed 30 + Thu 15 + Sat 30 + Sun 60 = 180 minutes. Week 1 also includes the second 30-minute run-walk.
- Running begins only after seven stable days, a 60-minute brisk walk, 3x10 controlled step-downs, and 10 controlled single-leg box squats without next-day increase.
- Run-walk starts 1 minute run/2 minutes walk and progresses running time only after two stable exposures.
- Jumping progresses bilateral landing → pogos → jump rope/low countermovement jump only after two stable run-walk exposures. Wednesday and Saturday sessions must start at least 72 elapsed hours apart; otherwise postpone Saturday's impact work and do only low-impact Zone 2.

**Phase 4, cutting and basketball return:**
- Use two strength days: Mon Lift A4; Thu Lift B4 plus 15-minute Zone 2 bike. A4 = goblet/front squat 3x5-6; DB bench 3x6-8; chest-supported row 3x8; DB RDL 3x6-8; standing calf raise 3x10; suitcase carry 3x45 sec/side. B4 = RFESS 3x6/side; DB overhead press 3x6-8; pulldown 3x8; hip thrust 3x8; leg extension 3x8 at 3-1-2; Pallof press 3x10/side.
- Tue: 45-minute Zone 2 swim/bike. Wed: first 10-20-minute athletic exposure, then 30-minute low-impact Zone 2. Fri: 45-minute Zone 2 swim/bike. Sat: second 10-20-minute exposure at the same athletic stage, at least 72 hours after Wednesday. Sun: 60-minute Zone 2 swim/bike/brisk walk.
- `WEEK_IN_PHASE` selects the exact stage and may run 1-7 in Phase 4: W1 planned deceleration; W2 planned 45-degree cuts; W3 planned 90-degree cuts; W4 reactive cuts; W5 non-contact basketball; W6 controlled-contact practice; W7 games only after the final gate. Each Wednesday/Saturday pair supplies the required two stable exposures before JT advances the week.
- Formal aerobic total is 195 minutes: Tue 45 + Wed 30 + Thu 15 + Fri 45 + Sun 60. Athletic work is not counted as aerobic minutes.
- Progress deceleration → planned 45-degree cuts → planned 90-degree cuts → reactive cuts → non-contact basketball → controlled contact practice → games.
- Sports-PT/sports-medicine assessment is required before cutting/contact progression.
- Each stage requires two stable exposures with pain ≤3/10, baseline next morning, and no flare over 48 hours.

**Manual phase checkpoints:**
- Phase 1 → 2: at least two stable weeks; all six scheduled strength sessions completed; normal stairs and a 60-minute brisk walk at baseline; no flare lasting over 48 hours. If not, repeat Phase 1. JT alone changes the pointer.
- Phase 2 → 3: four stable weeks; 3x8 controlled 6-inch step-downs; 10 controlled single-leg box squats/side; all main knee lifts progressed at least once; no next-morning increase. If not, repeat Phase 2.
- Phase 3 → 4: two stable 30-minute run-walk exposures, two stable landing/jump exposures, 3x10 controlled step-downs, and sports-PT/sports-medicine assessment before any cutting. If not, repeat Phase 3.
- Phase 4 advances one week/stage only after both Wednesday and Saturday exposures are stable and the knee is at baseline the following morning. Games require completed W4-W6 pairs plus clinician clearance. If not, repeat the last stable week.

**Required 14-movement audit and role assignment:**
- Spanish squat with band — core.
- Heel-elevated supported front-knee bend, isometric or kettlebell — later-phase.
- Single-leg wall sit — excluded as redundant.
- Reverse Nordic hold — later-phase.
- Backward treadmill walk — warm-up.
- Banded terminal knee extension — warm-up.
- Banded external rotation — accessory.
- Hip-flexor isometric hold — accessory.
- Step-down pulses — excluded; use controlled step-downs.
- Tibialis raises — accessory.
- Leg-extension quadriceps isometric — core.
- Single-leg box squat — core.
- Goblet squat — core.
- RFESS isometric hold — excluded as redundant; use progressive RFESS reps.

**Global load rules:**
- End strength sets with 2-4 reps in reserve; add reps before load; change only one variable per week.
- Zone 2 means RPE 3-4/10 with full-sentence talk test throughout. Easy walking counts toward formal aerobic minutes only when brisk enough to meet that intensity.
- Pain may reach 3/10 only if non-escalating and back to baseline next morning. If worse next morning, reduce the next knee/impact dose 30-50%; if a flare persists over 48 hours, return to the prior stage.
- Stop the exercise for sharp or escalating pain. Seek clinical care for listed red flags.

- [ ] Implement the minimal validator and renderer that satisfy the tests.
- [ ] Write the rationale with evidence citations and a movement-by-movement role/reasoning audit.
- [ ] Cite the progressive-loading RCT (`https://pmc.ncbi.nlm.nih.gov/articles/PMC8070614/`), clinical management review (`https://pmc.ncbi.nlm.nih.gov/articles/PMC9528703/`), exercise-loading study (`https://pmc.ncbi.nlm.nih.gov/articles/PMC10925836/`), and WHO activity guidance (`https://www.who.int/europe/publications/i/item/9789240014886`).
- [ ] Run focused tests and confirm GREEN.
- [ ] Run the validator and render every weekday for each phase.

## Chunk 2: Delivery integration and independent verification

### Task 3: Point the existing card automation to the stable source

**Files:**
- Modify: Daily Workout Card automation payload only.
- Preserve: schedule `0 5 * * *`, timezone `America/New_York`, enabled state, delivery route, and manual pointer.

- [ ] Save a secret-free before snapshot of the current automation.
- [ ] Change only the source path to `health/daily-workouts.md` and require the validator to pass before rendering.
- [ ] Read back the automation and prove schedule, timezone, enabled state, delivery, and pointer semantics are unchanged.
- [ ] Render today's card without sending it and compare it with the canonical source.

### Task 4: Fresh-context verification

**Files:**
- Create: `health/reports/workout-program-verification-2026-09-14.md`

- [ ] Give a verifier that did not author the program the final paths and SHA-256 hashes.
- [ ] Require a verbatim `CONFIRM` or `FAIL` verdict, including every failure.
- [ ] Require review of medical conservatism, weekly load spacing, 150-minute aerobic totals in all phases, all 14 requested exercises, exact pointer immutability, automation compatibility, and 28 rendered cards.
- [ ] Run the full health test suite, validator, content scan, and automation readback after final bytes are in place.
- [ ] Record the verifier verdict verbatim; do not claim completion on `FAIL`.
