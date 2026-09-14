#!/usr/bin/env python3
"""Render one concise daily card from the canonical workout source."""

import argparse
from pathlib import Path

from validate_daily_workout_source import DAYS, load_program, validate


def render(data, phase_number, week_number, day_name, preview=False):
    phase = data["phases"][str(phase_number)]
    day = phase["days"][day_name]
    lines = []
    if preview:
        lines.append("PREVIEW — NEVER USED BY AUTOMATION")
    lines.extend([
        f"{day_name.upper()} — PHASE {phase_number}, WEEK {week_number}",
        f"SESSION: {day['session']}",
        f"DURATION: {day['duration']}",
    ])
    lift_name = day.get("lift")
    if lift_name:
        warmups = "; ".join(f"{item['name']} {item['dose']}" for item in data["optional_warmups"])
        lines.append(f"OPTIONAL WARM-UP: {warmups}")
        lines.append(f"KNEE: {day['knee_work']}")
    if day.get("stage_schedule"):
        stage = data["stage_schedules"][day["stage_schedule"]][str(week_number)][day_name]
        lines.append(f"STAGE: {stage}")
        lines.append(f"SPACING: {data['impact_spacing_rule']}")
        if phase_number == 3 and week_number == 1:
            lines.append(f"WEEK 1 GATE: {data['phase3_week1_rule']}")
    if lift_name:
        for exercise in data["lifts"][lift_name]["exercises"]:
            lines.append(f"{exercise['name']} — {exercise['dose']} — TEMPO {exercise['tempo']}")
        if day.get("substitution"):
            substitution = day["substitution"]
            lines.append(
                "SUBSTITUTION (REPLACE, DO NOT ADD): "
                f"{substitution['option']} — {substitution['dose']} — "
                f"TEMPO {substitution['tempo']} — {substitution['rule']}"
            )
        accessories = "; ".join(f"{item['name']} {item['dose']}" for item in data["accessory_rotation"]["options"])
        lines.append(f"OPTIONAL AFTER: choose at most 2 — {accessories}")
    stage_contains_phase3_aerobic = day.get("stage_schedule") == "phase3"
    if day.get("aerobic") and not stage_contains_phase3_aerobic:
        lines.append(f"CARDIO: {day['aerobic']} — {day['aerobic_minutes']} min")
    if phase_number == 2 and day_name == "Tue":
        stairmaster = data["progressions"]["stairmaster"]
        lines.extend([
            f"STAIRMASTER GATE: {stairmaster['gate']}",
            f"IF NOT PASSED: {stairmaster['if_not_passed']}",
            f"IF PASSED: {stairmaster['if_passed']}",
            f"PROGRESSION: {stairmaster['advance']}",
        ])
    if day.get("low_impact_fallback"):
        lines.append(f"FALLBACK: {day['low_impact_fallback']}")
    if day.get("aerobic_minutes") or day.get("low_impact_fallback"):
        lines.append(data["zone2_definition"])
    if not lift_name:
        lines.append(f"KNEE: {day['knee_work']}")
    lines.append("LOAD: pain <=3/10, non-escalating; baseline next morning.")
    lines.append("SAFETY: working hypothesis, not a diagnosis. Stop/seek care for swelling, locking/catching, giving way, inability to bear weight, night/rest pain, worsening symptoms, chest pain, faintness, or disproportionate breathlessness.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--phase", type=int, choices=range(1, 5))
    parser.add_argument("--week", type=int)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--day", choices=DAYS, required=True)
    args = parser.parse_args()
    data = load_program(args.source)
    errors = validate(data)
    if errors:
        parser.error("; ".join(errors))
    pointer = data["pointer"]
    phase = args.phase if args.phase is not None else pointer["phase"]
    week = args.week if args.week is not None else (pointer["week_in_phase"] if phase == pointer["phase"] else 1)
    max_week = {1: 4, 2: 4, 3: 6, 4: 7}[phase]
    if not 1 <= week <= max_week:
        parser.error(f"phase {phase} week must be between 1 and {max_week}")
    if not args.preview and (phase != pointer["phase"] or week != pointer["week_in_phase"]):
        parser.error("noncanonical phase/week requires --preview; automation must render the canonical pointer")
    print(render(data, phase, week, args.day, preview=args.preview), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
