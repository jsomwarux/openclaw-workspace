#!/usr/bin/env python3
"""Validate the canonical, machine-readable daily workout source."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
PROGRAM_RE = re.compile(r"```json program\s*(\{.*?\})\s*```", re.DOTALL)
REQUIRED_PHASE_GATES = {
    "1_to_2": ["at least 2 stable weeks", "six completed lifts", "stairs at baseline", "60-minute walk at baseline", "no flare lasting more than 48 hours"],
    "2_to_3": ["four stable weeks", "3x8 controlled 6-inch step-downs", "10 controlled single-leg box squats per side", "load or rep progression in each knee lift", "no next-morning symptom increase"],
    "3_to_4": [
        "complete Phase 3 Week 5: 10:1 run-walk and repeated submaximal jumps 3x5 with stable responses",
        "complete Phase 3 Week 6: 30-minute easy continuous run and sport-specific jumps 3x4/side with stable responses",
        "two stable exposures at each applicable Week 5 and Week 6 stage, repeating the week as needed",
        "two stable 30-minute run-walk sessions", "two stable landing/jump exposures",
        "3x10 controlled step-downs per side", "sports PT or sports-medicine assessment before cutting",
    ],
    "phase_4_to_games": ["two stable exposures at each stage", "baseline the following morning", "stable reactive cuts", "stable non-contact practice", "stable controlled contact practice", "clinician clearance"],
}
TRAINING_KNEE = "before training only if it reduces pain: choose one, Spanish squat OR leg-extension isometric, 4x30-45 sec with 2 min rest; then scheduled tendon resistance; no between-session tendon loading"
REST_KNEE = "none; no between-session tendon loading"
REQUIRED_ISOMETRIC = {
    "frequency": "only when it reduces pain",
    "hard_daily_work": False,
    "one_option_only": True,
    "dose": "4x30-45 sec with 2 min rest",
    "options": ["banded Spanish squat", "mid-range leg-extension quadriceps isometric"],
}
REQUIRED_LOADING = "Finish resistance sets with 2-4 reps in reserve. Add reps before load and change only one variable per week: reps, load, range, or impact contacts."
REQUIRED_RUN = {
    "gate": "7 stable days + 60-minute brisk walk + 3x10 controlled step-downs + 10 single-leg box squats per side, with no next-day increase",
    "start": "1 minute run : 2 minutes walk for 30 minutes",
    "stages": ["run-walk 1:2", "run-walk 2:1", "run-walk 3:1", "run-walk 5:1", "run-walk 10:1", "30 min easy continuous run"],
    "advance": ["2:1", "3:1", "5:1", "10:1", "30 minutes easy continuous"],
    "frequency": "Wednesday primary run; Week 1 Saturday is the second exposure only if Wednesday was stable and at least 72 elapsed hours earlier",
}
REQUIRED_STAIRMASTER = {
    "gate": "7 stable days + pain-free normal stairs + 3x8 controlled 6-inch step-downs",
    "if_not_passed": "45 min swim or easy bike",
    "if_passed": "10 min StairMaster + 35 min swim or easy bike; total 45 min",
    "advance": "add 5 min StairMaster per stable week while reducing swim or easy bike by 5 min; total always 45 min",
}
REQUIRED_IMPACT_SPACING = "Wednesday and Saturday impact sessions require at least 72 elapsed hours; weekday labels alone do not prove spacing"
REQUIRED_JUMP = {
    "gate": "run-walk and strength gates stable",
    "stages": [
        "bilateral landing", "low pogo hops", "jump rope",
        "low countermovement jump and stick", "repeated submaximal jumps", "sport-specific jumps",
    ],
    "spacing": REQUIRED_IMPACT_SPACING,
}
REQUIRED_BASKETBALL = {
    "stages": [
        "shooting with no jumping", "planned acceleration and deceleration",
        "planned 45-degree cuts", "planned 90-degree cuts", "reactive cuts",
        "non-contact practice", "controlled contact practice", "games",
    ],
    "rule": "advance one stage only after two stable exposures and baseline the next morning",
}
REQUIRED_ZONE2 = "Zone 2 = RPE 3-4/10 and the full-sentence talk test (able to speak in full sentences); brisk walks count only when they meet both"
REQUIRED_SPACING_RULE = "Wednesday and Saturday impact sessions require at least 72 elapsed hours; weekday labels alone do not prove spacing. If fewer than 72 elapsed hours, skip impact and do the prescribed low-impact Zone 2 fallback."
REQUIRED_PHASE3_WEEK1_RULE = "No jumps until two stable 30-minute run exposures. If Wednesday was not stable, Saturday does not count as the second stable exposure; do not advance the pointer."
REQUIRED_STAGE_SCHEDULES = {
    "phase3": {
        "1": {"Wed": "run-walk 1:2 — 1 min easy run / 2 min walk for 30 min", "Sat": "second run-walk 1:2 exposure — 30 min"},
        "2": {"Wed": "run-walk 2:1 — 2 min easy run / 1 min walk for 30 min", "Sat": "bilateral landing — 3x5, then 30 min low-impact Zone 2"},
        "3": {"Wed": "run-walk 3:1 — 3 min easy run / 1 min walk for 30 min", "Sat": "low pogo hops — 3x15, then 30 min low-impact Zone 2"},
        "4": {"Wed": "run-walk 5:1 — 5 min easy run / 1 min walk for 30 min", "Sat": "jump rope — 3x30 sec OR low countermovement jump and stick — 3x5, then 30 min low-impact Zone 2"},
        "5": {"Wed": "run-walk 10:1 — 10 min easy run / 1 min walk for 30 min", "Sat": "repeated submaximal jumps — 3x5, then 30 min low-impact Zone 2"},
        "6": {"Wed": "30 min easy continuous run", "Sat": "sport-specific jumps — 3x4/side, then 30 min low-impact Zone 2"},
    },
    "phase4": {
        "1": {"Wed": "planned acceleration and deceleration — 10-20 min", "Sat": "planned acceleration and deceleration — 10-20 min"},
        "2": {"Wed": "planned 45-degree cuts — 10-20 min", "Sat": "planned 45-degree cuts — 10-20 min"},
        "3": {"Wed": "planned 90-degree cuts — 10-20 min", "Sat": "planned 90-degree cuts — 10-20 min"},
        "4": {"Wed": "reactive cuts — 10-20 min", "Sat": "reactive cuts — 10-20 min"},
        "5": {"Wed": "non-contact practice — 10-20 min", "Sat": "non-contact practice — 10-20 min"},
        "6": {"Wed": "controlled contact practice — 10-20 min", "Sat": "controlled contact practice — 10-20 min"},
        "7": {"Wed": "games only after the final phase_4_to_games gate — 10-20 min", "Sat": "games only after the final phase_4_to_games gate — 10-20 min"},
    },
}
REQUIRED_RESPONSE = {
    "during": "pain <=3/10 and non-escalating",
    "next_morning": "baseline",
    "worse_action": "reduce next knee or impact dose 30-50%",
    "flare_over_48h": "regress to the prior tolerated stage",
}
REQUIRED_MOVEMENT_ROLES = {
    "Spanish squat with band": "core",
    "Heel-elevated supported front-knee bend": "later-phase",
    "Single-leg wall sit": "excluded-redundant",
    "Reverse Nordic hold": "later-phase",
    "Backward treadmill walk": "warm-up",
    "Banded TKE": "warm-up",
    "Banded external rotation": "accessory",
    "Hip flexor isometric hold": "accessory",
    "Step-down pulses": "excluded-replace-with-controlled",
    "Tib raises": "accessory",
    "Leg-extension quadriceps isometric": "core",
    "Single-leg box squat": "core",
    "Goblet squat": "core",
    "RFESS isometric hold": "excluded-redundant",
}
REQUIRED_WARMUPS = [
    {"name": "Backward Treadmill Walk", "dose": "5-8 min", "use": "optional before resistance training"},
    {"name": "Banded TKE", "dose": "2x15", "use": "optional before resistance training"},
]
REQUIRED_ACCESSORIES = {
    "maximum": 2,
    "timing": "after main work",
    "options": [
        {"name": "Banded External Rotation", "dose": "2x12/side"},
        {"name": "Hip Flexor Isometric Hold", "dose": "2x20-30 sec/side"},
    ],
}
REQUIRED_LATER_OPTIONS = {
    "heel_elevated_front_knee_bend": {
        "phase": 2,
        "session": "Friday C2 after main work",
        "dose": "2x6/side controlled",
        "tempo": "3-0-2",
        "rule": "replace Single-Leg Box Squat, never add",
        "progression": "increase pain-free range, then add load",
    },
    "reverse_nordic": {
        "phase": 3,
        "session": "Thursday B3 after main work",
        "dose": "2x6-8 controlled",
        "tempo": "3-1-2",
        "rule": "replace Controlled Step-Down, never add",
        "progression": "increase range before adding load",
    },
}
REQUIRED_SUBSTITUTIONS = {
    ("2", "Fri"): {
        "option": "Heel-Elevated Supported Front-Knee Bend",
        "dose": "2x6/side controlled",
        "tempo": "3-0-2",
        "rule": "after main work; replace Single-Leg Box Squat, never add",
    },
    ("3", "Thu"): {
        "option": "Reverse Nordic",
        "dose": "2x6-8 controlled",
        "tempo": "3-1-2",
        "rule": "after main work; replace Controlled Step-Down, never add",
    },
}
REQUIRED_AEROBIC = {
    "1": {
        "Mon": (0, None), "Tue": (45, "freestyle/backstroke swim or easy bike"),
        "Wed": (0, None), "Thu": (45, "freestyle/backstroke swim or easy bike; row only if tolerated"),
        "Fri": (0, None), "Sat": (60, "freestyle/backstroke swim, easy bike, or brisk flat walk"), "Sun": (0, None),
    },
    "2": {
        "Mon": (0, None), "Tue": (45, "swim or easy bike, with the gated StairMaster substitution below"),
        "Wed": (0, None), "Thu": (45, "swim or easy bike"), "Fri": (0, None),
        "Sat": (60, "swim, easy bike, or brisk walk"), "Sun": (0, None),
    },
    "3": {
        "Mon": (0, None), "Tue": (45, "freestyle/backstroke swim, easy bike, or tolerated row"),
        "Wed": (30, "stage-specific easy run-walk"), "Thu": (15, "easy bike after lifting"), "Fri": (0, None),
        "Sat": (30, "stage-specific run or low-impact Zone 2 after landing/jump work"),
        "Sun": (60, "freestyle/backstroke swim, easy bike, tolerated row, or brisk walk meeting Zone 2"),
    },
    "4": {
        "Mon": (0, None), "Tue": (45, "freestyle/backstroke swim, easy bike, or tolerated row"),
        "Wed": (30, "low-impact Zone 2 after athletic work"), "Thu": (15, "easy bike after lifting"),
        "Fri": (45, "freestyle/backstroke swim, easy bike, tolerated row, or brisk walk meeting Zone 2"),
        "Sat": (0, None), "Sun": (60, "freestyle/backstroke swim, easy bike, tolerated row, or brisk walk meeting Zone 2"),
    },
}
REQUIRED_TENDON_DAYS = {"1": ("Mon", "Wed", "Fri"), "2": ("Mon", "Wed", "Fri"), "3": ("Mon", "Thu"), "4": ("Mon", "Thu")}
REQUIRED_STAGE_DAYS = {"1": (), "2": (), "3": ("Wed", "Sat"), "4": ("Wed", "Sat")}
REQUIRED_RED_FLAGS = {
    "swelling", "locking or catching", "instability or giving way", "inability to bear weight",
    "night or rest pain", "worsening symptoms", "chest pain", "faintness",
    "breathlessness disproportionate to effort",
}
REQUIRED_CLINICAL = "sports PT or sports-medicine assessment is recommended and required before cutting or contact basketball"
# Updated only when the approved lift matrix changes. This binds every exercise name, dose, and tempo.
APPROVED_LIFTS_SHA256 = "88ea0cebe2f7074ba6601540a667d0e2b2cb066784f225247274efbd2b3777fb"
# Binds the approved high-low day structure while allowing the JT-owned pointer to advance independently.
APPROVED_PHASES_SHA256 = "28683255a8d7e8e67daf4e5af071017749a752b9c1ffc65e157fb9df134f9dd5"


def load_program(path: Path):
    match = PROGRAM_RE.search(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("missing ```json program block")
    return json.loads(match.group(1))


def validate(data):
    errors = []
    pointer = data.get("pointer", {})
    phase_value = pointer.get("phase")
    week_value = pointer.get("week_in_phase")
    max_weeks = {1: 4, 2: 4, 3: 6, 4: 7}
    max_week = max_weeks.get(phase_value, 0)
    valid_pointer = (
        set(pointer) == {"phase", "week_in_phase", "advanced_by"}
        and type(phase_value) is int
        and phase_value in (1, 2, 3, 4)
        and type(week_value) is int
        and 1 <= week_value <= max_week
        and pointer.get("advanced_by") == "JT_ONLY"
    )
    if not valid_pointer:
        errors.append("pointer must be a valid JT_ONLY phase/week state")

    phases = data.get("phases", {})
    if set(phases) != {"1", "2", "3", "4"}:
        errors.append("exactly four phases are required")
    phase_hash = hashlib.sha256(json.dumps(phases, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if phase_hash != APPROVED_PHASES_SHA256:
        errors.append("approved high-low phase schedule changed")
    for number, phase in phases.items():
        days = phase.get("days", {})
        if set(days) != set(DAYS):
            errors.append(f"phase {number} must define Mon-Sun")
            continue
        total = sum(day.get("aerobic_minutes", 0) for day in days.values())
        if total < 150:
            errors.append(f"phase {number} has only {total} formal aerobic minutes")
        for day_name, day in days.items():
            expected_tendon = day_name in REQUIRED_TENDON_DAYS.get(number, ())
            expected_knee = TRAINING_KNEE if expected_tendon else REST_KNEE
            if day.get("knee_work") != expected_knee:
                errors.append(f"phase {number} {day_name}: conflicting daily knee work")
            if day.get("tendon_resistance") is not expected_tendon:
                errors.append(f"phase {number} {day_name}: tendon resistance flag changed")
            expected_minutes, expected_modality = REQUIRED_AEROBIC.get(number, {}).get(day_name, (None, None))
            if day.get("aerobic_minutes") != expected_minutes or day.get("aerobic") != expected_modality:
                errors.append(f"phase {number} {day_name}: aerobic prescription changed")
            expected_stage = f"phase{number}" if day_name in REQUIRED_STAGE_DAYS.get(number, ()) else None
            if day.get("stage_schedule") != expected_stage:
                errors.append(f"phase {number} {day_name}: stage schedule changed")

    if "1" in phases:
        p1 = json.dumps(phases["1"]["days"]).lower()
        for banned in ("run", "jump", "cut", "basketball", "stairmaster"):
            if banned in p1:
                errors.append(f"phase 1 must exclude {banned}")

    audit = data.get("movement_audit", [])
    names = [row.get("movement") for row in audit]
    actual_roles = {row.get("movement"): row.get("role") for row in audit}
    if len(audit) != 14 or len(names) != len(set(names)) or actual_roles != REQUIRED_MOVEMENT_ROLES:
        errors.append("movement audit must contain the approved 14 unique movements with exact roles")
    if any(set(row) != {"movement", "role", "reason"} for row in audit):
        errors.append("each movement audit row needs movement, one role, and reason")

    knee_rules = data.get("knee_rules", {})
    if knee_rules.get("optional_isometric") != REQUIRED_ISOMETRIC:
        errors.append("optional isometric prescription changed")
    if knee_rules.get("response") != REQUIRED_RESPONSE:
        errors.append("pain response rules changed")
    if knee_rules.get("loading") != REQUIRED_LOADING:
        errors.append("resistance loading or progression rule changed")
    if data.get("optional_warmups") != REQUIRED_WARMUPS:
        errors.append("optional warm-up prescription changed")
    if data.get("accessory_rotation") != REQUIRED_ACCESSORIES:
        errors.append("accessory rotation prescription changed")
    if data.get("later_phase_options") != REQUIRED_LATER_OPTIONS:
        errors.append("later-phase option prescription changed")
    for (phase_number, day_name), substitution in REQUIRED_SUBSTITUTIONS.items():
        if phases.get(phase_number, {}).get("days", {}).get(day_name, {}).get("substitution") != substitution:
            errors.append(f"phase {phase_number} {day_name}: substitution prescription changed")
    if data.get("phase_gates") != REQUIRED_PHASE_GATES:
        errors.append("manual phase gates do not match the approved gates")
    lift_hash = hashlib.sha256(json.dumps(data.get("lifts", {}), sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if lift_hash != APPROVED_LIFTS_SHA256:
        errors.append("approved tendon dose or tempo changed")
    progressions = data.get("progressions", {})
    if progressions.get("run") != REQUIRED_RUN:
        errors.append("run progression changed")
    if progressions.get("stairmaster") != REQUIRED_STAIRMASTER:
        errors.append("StairMaster gate or progression changed")
    if progressions.get("jump") != REQUIRED_JUMP:
        errors.append("jump progression or impact spacing changed")
    if progressions.get("basketball") != REQUIRED_BASKETBALL:
        errors.append("basketball/cut progression changed")
    if data.get("zone2_definition") != REQUIRED_ZONE2:
        errors.append("Zone 2 operational definition changed")
    if data.get("impact_spacing_rule") != REQUIRED_SPACING_RULE:
        errors.append("elapsed-hours impact spacing rule changed")
    if data.get("phase3_week1_rule") != REQUIRED_PHASE3_WEEK1_RULE:
        errors.append("Phase 3 Week 1 stability rule changed")
    if data.get("stage_schedules") != REQUIRED_STAGE_SCHEDULES:
        errors.append("phase/week stage schedule changed")
    phase3_schedule = json.dumps(data.get("stage_schedules", {}).get("phase3", {})).lower()
    for progression_name in ("run", "jump"):
        for stage in progressions.get(progression_name, {}).get("stages", []):
            if stage.lower() not in phase3_schedule:
                errors.append(f"declared pre-cut stage is not scheduled: {stage}")
    for phase_number, phase in phases.items():
        loaded = [
            bool(phase.get("days", {}).get(day, {}).get("tendon_resistance") or phase.get("days", {}).get(day, {}).get("stage_schedule"))
            for day in DAYS
        ]
        if any(all(loaded[index:index + 3]) for index in range(5)):
            errors.append(f"phase {phase_number} has three consecutive tendon-load days")
    safety = data.get("safety", {})
    if set(safety.get("red_flags", [])) != REQUIRED_RED_FLAGS:
        errors.append("red flags changed")
    if safety.get("clinical") != REQUIRED_CLINICAL:
        errors.append("clinician requirement changed")
    if "automatic" in json.dumps(pointer).lower():
        errors.append("automatic pointer advancement is forbidden")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(load_program(args.source))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
