#!/usr/bin/env python3
"""
Outputs today's workout summary for the morning brief.
Usage: python3 health/todays-workout.py
"""
from datetime import datetime

SCHEDULE = {
    0: ("Monday", "Upper Pull + Shoulder Correctives", [
        "Warm-up: Dead hang 3×45-60s | 90/90 hips 2min/side | Chin tucks 2×10 | Band pull-aparts 2×20",
        "Face pulls (cable, ext. rotation) — 4×15",
        "Single-arm cable row — 4×12 each side",
        "Lat pulldown / assisted chin-up — 3×10",
        "Band pull-aparts — 3×20",
        "Dead bug — 3×10 each side",
        "Finisher: Thoracic foam roll 2 min",
    ]),
    1: ("Tuesday", "Lower Body + Pelvic Symmetry", [
        "Warm-up: Dead hang 3×45-60s | 90/90 hips 2min/side | Chin tucks 2×10 | Band pull-aparts 2×20",
        "90/90 hip work (extended) — 4 min each side",
        "Single-leg glute bridge — 4×12 each",
        "Single-leg Romanian deadlift — 3×10 each",
        "Copenhagen adductor hold — 3×30s each",
        "Goblet squat (light, pattern) — 3×10",
        "Bird dog — 3×10 each side",
    ]),
    2: ("Wednesday", "Active Recovery 🚶", [
        "7-min reset protocol (full)",
        "20–30 min walk (easy pace, nasal breathing)",
        "Band pull-aparts — 2×20",
        "Chin tucks — 2×10",
    ]),
    3: ("Thursday", "Upper Push + Thoracic", [
        "Warm-up: Dead hang 3×45-60s | 90/90 hips 2min/side | Chin tucks 2×10 | Band pull-aparts 2×20",
        "Face pulls — 3×15",
        "Landmine press — 4×10 each side",
        "Single-arm cable row — 3×12 each",
        "Band pull-aparts — 3×20",
        "Dead bug — 3×10 each side",
        "Finisher: Dead hang 2×45s + thoracic foam roll",
    ]),
    4: ("Friday", "Lower Body + Core", [
        "Warm-up: Dead hang 3×45-60s | 90/90 hips 2min/side | Chin tucks 2×10 | Band pull-aparts 2×20",
        "Single-leg glute bridge — 3×12 each",
        "Single-leg Romanian deadlift — 4×10 each (add small load vs. Tuesday if Tuesday felt stable)",
        "Copenhagen adductor hold — 2×30s each",
        "Dead bug — 4×10 each side",
        "Bird dog — 3×10 each side",
        "Incline treadmill walk — 20 min, 10-12% grade, nasal breathing",
    ]),
    5: ("Saturday", "Active Recovery 🚶", [
        "7-min reset protocol (full)",
        "20–30 min walk (easy pace, nasal breathing)",
        "Band pull-aparts — 2×20",
        "Chin tucks — 2×10",
    ]),
    6: ("Sunday", "Rest Day 🛌", [
        "7-min reset protocol only",
        "No gym",
    ]),
}

def main():
    today = datetime.now().weekday()  # 0=Mon, 6=Sun
    day_name, session_name, exercises = SCHEDULE[today]

    print(f"🏋️ Today's Workout — {day_name}: {session_name}")
    for ex in exercises:
        print(f"  • {ex}")
    print(f"\n📋 Full routine: ~/.openclaw/workspace/health/exercise-routine.md")

if __name__ == "__main__":
    main()
