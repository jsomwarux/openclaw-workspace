# Daily Workouts — Strength, Heart Health, and Return to Basketball

This is the canonical source for the daily workout card. The knee plan treats left patellar tendon pain as a **working hypothesis, not a diagnosis**. Only JT changes the pointer after passing the manual gate.

```json program
{
  "pointer": {"phase": 1, "week_in_phase": 1, "advanced_by": "JT_ONLY"},
  "zone2_definition": "Zone 2 = RPE 3-4/10 and the full-sentence talk test (able to speak in full sentences); brisk walks count only when they meet both",
  "impact_spacing_rule": "Wednesday and Saturday impact sessions require at least 72 elapsed hours; weekday labels alone do not prove spacing. If fewer than 72 elapsed hours, skip impact and do the prescribed low-impact Zone 2 fallback.",
  "phase3_week1_rule": "No jumps until two stable 30-minute run exposures. If Wednesday was not stable, Saturday does not count as the second stable exposure; do not advance the pointer.",
  "phases": {
    "1": {
      "name": "Settle symptoms and build capacity",
      "days": {
        "Mon": {"session": "Full-body A + tendon resistance", "duration": "60 min", "lift": "A", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Tue": {"session": "Low-impact Zone 2", "duration": "45 min", "aerobic": "freestyle/backstroke swim or easy bike", "aerobic_minutes": 45, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Wed": {"session": "Full-body B + tendon resistance", "duration": "60 min", "lift": "B", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Thu": {"session": "Low-impact Zone 2", "duration": "45 min", "aerobic": "freestyle/backstroke swim or easy bike; row only if tolerated", "aerobic_minutes": 45, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Fri": {"session": "Full-body C + tendon resistance", "duration": "60 min", "lift": "C", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Sat": {"session": "Long easy aerobic", "duration": "60 min", "aerobic": "freestyle/backstroke swim, easy bike, or brisk flat walk", "aerobic_minutes": 60, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Sun": {"session": "Recovery", "duration": "rest or easy walk", "aerobic_minutes": 0, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"}
      }
    },
    "2": {
      "name": "Heavy slow resistance and single-leg control",
      "days": {
        "Mon": {"session": "Full-body A2 + tendon resistance", "duration": "65 min", "lift": "A2", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Tue": {"session": "Low-impact Zone 2 or gated StairMaster substitution", "duration": "45 min", "aerobic": "swim or easy bike, with the gated StairMaster substitution below", "aerobic_minutes": 45, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Wed": {"session": "Full-body B2 + tendon resistance", "duration": "65 min", "lift": "B2", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Thu": {"session": "Low-impact Zone 2", "duration": "45 min", "aerobic": "swim or easy bike", "aerobic_minutes": 45, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Fri": {"session": "Full-body C2 + tendon resistance", "duration": "65 min", "lift": "C2", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading", "substitution": {"option": "Heel-Elevated Supported Front-Knee Bend", "dose": "2x6/side controlled", "tempo": "3-0-2", "rule": "after main work; replace Single-Leg Box Squat, never add"}},
        "Sat": {"session": "Long easy aerobic", "duration": "60 min", "aerobic": "swim, easy bike, or brisk walk", "aerobic_minutes": 60, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Sun": {"session": "Recovery", "duration": "rest or easy walk", "aerobic_minutes": 0, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"}
      }
    },
    "3": {
      "name": "Run-walk and energy storage",
      "days": {
        "Mon": {"session": "Full-body A3 strength", "duration": "60 min", "lift": "A3", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Tue": {"session": "Low-impact Zone 2", "duration": "45 min", "aerobic": "freestyle/backstroke swim, easy bike, or tolerated row", "aerobic_minutes": 45, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Wed": {"session": "Stage-specific run", "duration": "30 min", "aerobic": "stage-specific easy run-walk", "aerobic_minutes": 30, "tendon_resistance": false, "stage_schedule": "phase3", "low_impact_fallback": "If fewer than 72 elapsed hours since the prior impact exposure or symptoms are not stable, skip the run and do 30 min low-impact Zone 2 only", "knee_work": "none; no between-session tendon loading"},
        "Thu": {"session": "Full-body B3 strength + easy bike", "duration": "75 min", "lift": "B3", "aerobic": "easy bike after lifting", "aerobic_minutes": 15, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading", "substitution": {"option": "Reverse Nordic", "dose": "2x6-8 controlled", "tempo": "3-1-2", "rule": "after main work; replace Controlled Step-Down, never add"}},
        "Fri": {"session": "Rest", "duration": "rest", "aerobic_minutes": 0, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Sat": {"session": "Stage-specific second impact exposure", "duration": "30-45 min", "aerobic": "stage-specific run or low-impact Zone 2 after landing/jump work", "aerobic_minutes": 30, "tendon_resistance": false, "stage_schedule": "phase3", "low_impact_fallback": "If fewer than 72 elapsed hours since Wednesday or symptoms are not stable, skip impact and do 30 min low-impact Zone 2 only", "knee_work": "none; no between-session tendon loading"},
        "Sun": {"session": "Long Zone 2", "duration": "60 min", "aerobic": "freestyle/backstroke swim, easy bike, tolerated row, or brisk walk meeting Zone 2", "aerobic_minutes": 60, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"}
      }
    },
    "4": {
      "name": "Return to cutting and basketball",
      "days": {
        "Mon": {"session": "Full-body A4 strength", "duration": "60 min", "lift": "A4", "aerobic_minutes": 0, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Tue": {"session": "Low-impact Zone 2", "duration": "45 min", "aerobic": "freestyle/backstroke swim, easy bike, or tolerated row", "aerobic_minutes": 45, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Wed": {"session": "Athletic stage + low-impact Zone 2", "duration": "40-50 min", "aerobic": "low-impact Zone 2 after athletic work", "aerobic_minutes": 30, "tendon_resistance": false, "stage_schedule": "phase4", "low_impact_fallback": "If fewer than 72 elapsed hours since the prior impact exposure or symptoms are not stable, skip athletic work and do 30 min low-impact Zone 2 only", "knee_work": "none; no between-session tendon loading"},
        "Thu": {"session": "Full-body B4 strength + easy bike", "duration": "75 min", "lift": "B4", "aerobic": "easy bike after lifting", "aerobic_minutes": 15, "tendon_resistance": true, "knee_work": "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"},
        "Fri": {"session": "Low-impact Zone 2", "duration": "45 min", "aerobic": "freestyle/backstroke swim, easy bike, tolerated row, or brisk walk meeting Zone 2", "aerobic_minutes": 45, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"},
        "Sat": {"session": "Same-stage second athletic exposure", "duration": "10-20 min", "aerobic_minutes": 0, "tendon_resistance": false, "stage_schedule": "phase4", "low_impact_fallback": "If fewer than 72 elapsed hours since Wednesday or symptoms are not stable, postpone the athletic exposure and do 30 min low-impact Zone 2 only", "knee_work": "none; no between-session tendon loading"},
        "Sun": {"session": "Long Zone 2", "duration": "60 min", "aerobic": "freestyle/backstroke swim, easy bike, tolerated row, or brisk walk meeting Zone 2", "aerobic_minutes": 60, "tendon_resistance": false, "knee_work": "none; no between-session tendon loading"}
      }
    }
  },
  "stage_schedules": {
    "phase3": {
      "1": {"Wed": "run-walk 1:2 — 1 min easy run / 2 min walk for 30 min", "Sat": "second run-walk 1:2 exposure — 30 min"},
      "2": {"Wed": "run-walk 2:1 — 2 min easy run / 1 min walk for 30 min", "Sat": "bilateral landing — 3x5, then 30 min low-impact Zone 2"},
      "3": {"Wed": "run-walk 3:1 — 3 min easy run / 1 min walk for 30 min", "Sat": "low pogo hops — 3x15, then 30 min low-impact Zone 2"},
      "4": {"Wed": "run-walk 5:1 — 5 min easy run / 1 min walk for 30 min", "Sat": "jump rope — 3x30 sec OR low countermovement jump and stick — 3x5, then 30 min low-impact Zone 2"},
      "5": {"Wed": "run-walk 10:1 — 10 min easy run / 1 min walk for 30 min", "Sat": "repeated submaximal jumps — 3x5, then 30 min low-impact Zone 2"},
      "6": {"Wed": "30 min easy continuous run", "Sat": "sport-specific jumps — 3x4/side, then 30 min low-impact Zone 2"}
    },
    "phase4": {
      "1": {"Wed": "planned acceleration and deceleration — 10-20 min", "Sat": "planned acceleration and deceleration — 10-20 min"},
      "2": {"Wed": "planned 45-degree cuts — 10-20 min", "Sat": "planned 45-degree cuts — 10-20 min"},
      "3": {"Wed": "planned 90-degree cuts — 10-20 min", "Sat": "planned 90-degree cuts — 10-20 min"},
      "4": {"Wed": "reactive cuts — 10-20 min", "Sat": "reactive cuts — 10-20 min"},
      "5": {"Wed": "non-contact practice — 10-20 min", "Sat": "non-contact practice — 10-20 min"},
      "6": {"Wed": "controlled contact practice — 10-20 min", "Sat": "controlled contact practice — 10-20 min"},
      "7": {"Wed": "games only after the final phase_4_to_games gate — 10-20 min", "Sat": "games only after the final phase_4_to_games gate — 10-20 min"}
    }
  },
  "lifts": {
    "A": {"exercises": [
      {"name": "Goblet Squat", "dose": "3x8", "tempo": "3-0-3"}, {"name": "DB Bench Press or Push-up", "dose": "3x8-10", "tempo": "2-0-2"}, {"name": "Chest-Supported DB Row", "dose": "3x10", "tempo": "2-1-2"}, {"name": "DB Romanian Deadlift", "dose": "3x8", "tempo": "3-0-2"}, {"name": "Standing Calf Raise", "dose": "3x12", "tempo": "2-1-3"}, {"name": "Suitcase Carry", "dose": "3x30-45 sec/side", "tempo": "controlled"}
    ]},
    "B": {"exercises": [
      {"name": "Supported Split Squat", "dose": "3x8/side", "tempo": "3-0-3"}, {"name": "Seated DB Overhead Press", "dose": "3x8", "tempo": "2-0-2"}, {"name": "Lat Pulldown", "dose": "3x8-10", "tempo": "2-1-2"}, {"name": "Hip Thrust", "dose": "3x10", "tempo": "2-1-2"}, {"name": "Seated Soleus Raise", "dose": "3x15", "tempo": "2-1-3"}, {"name": "Pallof Press", "dose": "3x10/side", "tempo": "controlled"}
    ]},
    "C": {"exercises": [
      {"name": "Leg Extension", "dose": "3x10", "tempo": "3-1-3"}, {"name": "Incline DB Press", "dose": "3x8-10", "tempo": "2-0-2"}, {"name": "One-Arm Row", "dose": "3x10/side", "tempo": "2-1-2"}, {"name": "Back Extension or Hinge", "dose": "3x10", "tempo": "3-1-2"}, {"name": "Tib Raise", "dose": "3x15", "tempo": "2-1-2"}, {"name": "Farmer Carry", "dose": "3x30-45 sec", "tempo": "controlled"}
    ]},
    "A2": {"exercises": [
      {"name": "Goblet Squat", "dose": "4x6-8", "tempo": "3-0-2"}, {"name": "DB Bench Press", "dose": "3x6-10", "tempo": "2-0-2"}, {"name": "Chest-Supported Row", "dose": "3x8-10", "tempo": "2-1-2"}, {"name": "DB Romanian Deadlift", "dose": "3x8", "tempo": "3-0-2"}, {"name": "Standing Calf Raise", "dose": "3x12", "tempo": "2-1-3"}, {"name": "Suitcase Carry", "dose": "3x45 sec/side", "tempo": "controlled"}
    ]},
    "B2": {"exercises": [
      {"name": "Rear-Foot-Elevated Split Squat", "dose": "4x6-8/side", "tempo": "3-0-2"}, {"name": "DB Overhead Press", "dose": "3x8", "tempo": "2-0-2"}, {"name": "Lat Pulldown", "dose": "3x8-10", "tempo": "2-1-2"}, {"name": "Hip Thrust", "dose": "3x8-10", "tempo": "2-1-2"}, {"name": "Controlled 6-inch Step-Down", "dose": "3x6/side", "tempo": "3-1-2"}, {"name": "Pallof Press", "dose": "3x10/side", "tempo": "controlled"}
    ]},
    "C2": {"exercises": [
      {"name": "Leg Extension", "dose": "4x8", "tempo": "3-1-2"}, {"name": "Single-Leg Box Squat", "dose": "2x6/side technique", "tempo": "3-1-2"}, {"name": "Incline DB Press", "dose": "3x8", "tempo": "2-0-2"}, {"name": "One-Arm Row", "dose": "3x10/side", "tempo": "2-1-2"}, {"name": "Back Extension", "dose": "3x10", "tempo": "2-1-2"}, {"name": "Tib Raise", "dose": "3x15", "tempo": "2-1-2"}, {"name": "Farmer Carry", "dose": "3x45 sec", "tempo": "controlled"}
    ]},
    "A3": {"exercises": [
      {"name": "Goblet Squat", "dose": "3x6", "tempo": "3-0-2"}, {"name": "DB Bench Press", "dose": "3x8", "tempo": "2-0-2"}, {"name": "Chest-Supported Row", "dose": "3x10", "tempo": "2-1-2"}, {"name": "DB Romanian Deadlift", "dose": "3x8", "tempo": "3-0-2"}, {"name": "Standing Calf Raise", "dose": "3x12", "tempo": "2-1-3"}, {"name": "Suitcase Carry", "dose": "3x45 sec/side", "tempo": "controlled"}
    ]},
    "B3": {"exercises": [
      {"name": "Rear-Foot-Elevated Split Squat", "dose": "3x6/side", "tempo": "3-0-2"}, {"name": "DB Overhead Press", "dose": "3x8", "tempo": "2-0-2"}, {"name": "Lat Pulldown", "dose": "3x8", "tempo": "2-1-2"}, {"name": "Hip Thrust", "dose": "3x8", "tempo": "2-1-2"}, {"name": "Controlled Step-Down", "dose": "2x8/side", "tempo": "3-1-2"}, {"name": "Pallof Press", "dose": "3x10/side", "tempo": "controlled"}
    ]},
    "A4": {"exercises": [
      {"name": "Goblet or Front Squat", "dose": "3x5-6", "tempo": "3-0-2"}, {"name": "DB Bench Press", "dose": "3x6-8", "tempo": "2-0-2"}, {"name": "Chest-Supported Row", "dose": "3x8", "tempo": "2-1-2"}, {"name": "DB Romanian Deadlift", "dose": "3x6-8", "tempo": "3-0-2"}, {"name": "Standing Calf Raise", "dose": "3x10", "tempo": "2-1-3"}, {"name": "Suitcase Carry", "dose": "3x45 sec/side", "tempo": "controlled"}
    ]},
    "B4": {"exercises": [
      {"name": "Rear-Foot-Elevated Split Squat", "dose": "3x6/side", "tempo": "3-0-2"}, {"name": "DB Overhead Press", "dose": "3x6-8", "tempo": "2-0-2"}, {"name": "Lat Pulldown", "dose": "3x8", "tempo": "2-1-2"}, {"name": "Hip Thrust", "dose": "3x8", "tempo": "2-1-2"}, {"name": "Leg Extension", "dose": "3x8", "tempo": "3-1-2"}, {"name": "Pallof Press", "dose": "3x10/side", "tempo": "controlled"}
    ]}
  },
  "optional_warmups": [
    {"name": "Backward Treadmill Walk", "dose": "5-8 min", "use": "optional before resistance training"},
    {"name": "Banded TKE", "dose": "2x15", "use": "optional before resistance training"}
  ],
  "accessory_rotation": {"maximum": 2, "timing": "after main work", "options": [
    {"name": "Banded External Rotation", "dose": "2x12/side"},
    {"name": "Hip Flexor Isometric Hold", "dose": "2x20-30 sec/side"}
  ]},
  "later_phase_options": {
    "heel_elevated_front_knee_bend": {"phase": 2, "session": "Friday C2 after main work", "dose": "2x6/side controlled", "tempo": "3-0-2", "rule": "replace Single-Leg Box Squat, never add", "progression": "increase pain-free range, then add load"},
    "reverse_nordic": {"phase": 3, "session": "Thursday B3 after main work", "dose": "2x6-8 controlled", "tempo": "3-1-2", "rule": "replace Controlled Step-Down, never add", "progression": "increase range before adding load"}
  },
  "knee_rules": {
    "optional_isometric": {"frequency": "only when it reduces pain", "hard_daily_work": false, "one_option_only": true, "dose": "4x30-45 sec with 2 min rest", "options": ["banded Spanish squat", "mid-range leg-extension quadriceps isometric"]},
    "response": {"during": "pain <=3/10 and non-escalating", "next_morning": "baseline", "worse_action": "reduce next knee or impact dose 30-50%", "flare_over_48h": "regress to the prior tolerated stage"},
    "loading": "Finish resistance sets with 2-4 reps in reserve. Add reps before load and change only one variable per week: reps, load, range, or impact contacts."
  },
  "phase_gates": {
    "1_to_2": ["at least 2 stable weeks", "six completed lifts", "stairs at baseline", "60-minute walk at baseline", "no flare lasting more than 48 hours"],
    "2_to_3": ["four stable weeks", "3x8 controlled 6-inch step-downs", "10 controlled single-leg box squats per side", "load or rep progression in each knee lift", "no next-morning symptom increase"],
    "3_to_4": ["complete Phase 3 Week 5: 10:1 run-walk and repeated submaximal jumps 3x5 with stable responses", "complete Phase 3 Week 6: 30-minute easy continuous run and sport-specific jumps 3x4/side with stable responses", "two stable exposures at each applicable Week 5 and Week 6 stage, repeating the week as needed", "two stable 30-minute run-walk sessions", "two stable landing/jump exposures", "3x10 controlled step-downs per side", "sports PT or sports-medicine assessment before cutting"],
    "phase_4_to_games": ["two stable exposures at each stage", "baseline the following morning", "stable reactive cuts", "stable non-contact practice", "stable controlled contact practice", "clinician clearance"]
  },
  "progressions": {
    "stairmaster": {"gate": "7 stable days + pain-free normal stairs + 3x8 controlled 6-inch step-downs", "if_not_passed": "45 min swim or easy bike", "if_passed": "10 min StairMaster + 35 min swim or easy bike; total 45 min", "advance": "add 5 min StairMaster per stable week while reducing swim or easy bike by 5 min; total always 45 min"},
    "run": {"gate": "7 stable days + 60-minute brisk walk + 3x10 controlled step-downs + 10 single-leg box squats per side, with no next-day increase", "start": "1 minute run : 2 minutes walk for 30 minutes", "stages": ["run-walk 1:2", "run-walk 2:1", "run-walk 3:1", "run-walk 5:1", "run-walk 10:1", "30 min easy continuous run"], "advance": ["2:1", "3:1", "5:1", "10:1", "30 minutes easy continuous"], "frequency": "Wednesday primary run; Week 1 Saturday is the second exposure only if Wednesday was stable and at least 72 elapsed hours earlier"},
    "jump": {"gate": "run-walk and strength gates stable", "stages": ["bilateral landing", "low pogo hops", "jump rope", "low countermovement jump and stick", "repeated submaximal jumps", "sport-specific jumps"], "spacing": "Wednesday and Saturday impact sessions require at least 72 elapsed hours; weekday labels alone do not prove spacing"},
    "basketball": {"stages": ["shooting with no jumping", "planned acceleration and deceleration", "planned 45-degree cuts", "planned 90-degree cuts", "reactive cuts", "non-contact practice", "controlled contact practice", "games"], "rule": "advance one stage only after two stable exposures and baseline the next morning"}
  },
  "movement_audit": [
    {"movement": "Spanish squat with band", "role": "core", "reason": "optional pain-modulating isometric and early quadriceps load"},
    {"movement": "Heel-elevated supported front-knee bend", "role": "later-phase", "reason": "progressive knee-dominant loading after early tolerance"},
    {"movement": "Single-leg wall sit", "role": "excluded-redundant", "reason": "duplicates better-standardized isometric options"},
    {"movement": "Reverse Nordic hold", "role": "later-phase", "reason": "quad accessory after primary loading is established"},
    {"movement": "Backward treadmill walk", "role": "warm-up", "reason": "optional low-load preparation, not primary treatment"},
    {"movement": "Banded TKE", "role": "warm-up", "reason": "optional activation, not progressive tendon resistance"},
    {"movement": "Banded external rotation", "role": "accessory", "reason": "hip capacity support, not direct tendon treatment"},
    {"movement": "Hip flexor isometric hold", "role": "accessory", "reason": "trunk and hip support"},
    {"movement": "Step-down pulses", "role": "excluded-replace-with-controlled", "reason": "replace bouncing pulses with slow controlled step-downs"},
    {"movement": "Tib raises", "role": "accessory", "reason": "lower-leg capacity for running and landing"},
    {"movement": "Leg-extension quadriceps isometric", "role": "core", "reason": "standardized optional pain modulation and quadriceps loading entry"},
    {"movement": "Single-leg box squat", "role": "core", "reason": "single-leg capacity and gate exercise"},
    {"movement": "Goblet squat", "role": "core", "reason": "primary bilateral heavy slow resistance pattern"},
    {"movement": "RFESS isometric hold", "role": "excluded-redundant", "reason": "dynamic RFESS supplies more progressive loading"}
  ],
  "safety": {
    "status": "working hypothesis, not a diagnosis",
    "clinical": "sports PT or sports-medicine assessment is recommended and required before cutting or contact basketball",
    "red_flags": ["swelling", "locking or catching", "instability or giving way", "inability to bear weight", "night or rest pain", "worsening symptoms", "chest pain", "faintness", "breathlessness disproportionate to effort"],
    "breathing_rule": "Stop the session for chest pain, faintness, or breathlessness disproportionate to effort; do not push through it."
  }
}
```

## Operator rules

- The card renderer reads this source; it never edits it.
- Only JT advances `PHASE` or `WEEK_IN_PHASE` after passing the written gate. Lifts are fixed by weekday.
- Phase 1 contains no running, jumping, cutting, basketball, or StairMaster.
- Formal aerobic work is at least 150 minutes in every phase. Daily walking is useful background activity, not counted toward that minimum.
- Isometrics are optional symptom tools only when they reduce pain. They are not mandatory evening work and never stack as hard knee work on a resistance day.
