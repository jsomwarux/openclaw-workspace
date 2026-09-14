import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

HEALTH = Path(__file__).resolve().parents[1]
SOURCE = HEALTH / "daily-workouts.md"
VALIDATOR = HEALTH / "validate_daily_workout_source.py"
RENDERER = HEALTH / "render_daily_workout.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def program():
    return load_module(VALIDATOR, "workout_validator").load_program(SOURCE)


class WorkoutSourceTests(unittest.TestCase):

 def test_pointer_is_manual_and_unchanged(self):
    data = program()
    assert data["pointer"] == {
        "phase": 1,
        "week_in_phase": 1,
        "advanced_by": "JT_ONLY",
    }
    assert "automatic" not in json.dumps(data["pointer"]).lower()

 def test_validator_allows_valid_jt_pointer_states_and_rejects_invalid_ones(self):
    validator = load_module(VALIDATOR, "workout_validator_pointer_states")
    for phase, week in ((1, 4), (2, 3), (3, 6), (4, 7)):
        with self.subTest(phase=phase, week=week):
            candidate = copy.deepcopy(program())
            candidate["pointer"] = {"phase": phase, "week_in_phase": week, "advanced_by": "JT_ONLY"}
            self.assertEqual(validator.validate(candidate), [])
    for phase, week in ((0, 1), (True, 1), (2, 5), (3, 7), (4, 8)):
        with self.subTest(phase=phase, week=week):
            candidate = copy.deepcopy(program())
            candidate["pointer"] = {"phase": phase, "week_in_phase": week, "advanced_by": "JT_ONLY"}
            self.assertTrue(validator.validate(candidate))

 def test_renderer_defaults_to_pointer_and_requires_preview_for_other_phase_or_week(self):
    default = subprocess.run(
        [sys.executable, str(RENDERER), "--source", str(SOURCE), "--day", "Mon"],
        text=True, capture_output=True,
    )
    self.assertEqual(default.returncode, 0, default.stderr)
    self.assertIn("PHASE 1, WEEK 1", default.stdout)
    self.assertNotIn("PREVIEW", default.stdout)
    blocked = subprocess.run(
        [sys.executable, str(RENDERER), "--source", str(SOURCE), "--phase", "4", "--week", "7", "--day", "Sat"],
        text=True, capture_output=True,
    )
    self.assertNotEqual(blocked.returncode, 0)
    preview = subprocess.run(
        [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", "4", "--week", "7", "--day", "Sat"],
        text=True, capture_output=True,
    )
    self.assertEqual(preview.returncode, 0, preview.stderr)
    self.assertIn("PREVIEW — NEVER USED BY AUTOMATION", preview.stdout)
    self.assertIn("games only after the final phase_4_to_games gate", preview.stdout)


 def test_all_phases_meet_formal_aerobic_minimum_and_phase_one_is_low_impact(self):
    data = program()
    assert {str(n) for n in range(1, 5)} == set(data["phases"])
    for phase in data["phases"].values():
        assert sum(day["aerobic_minutes"] for day in phase["days"].values()) >= 150

    p1 = data["phases"]["1"]["days"]
    assert p1["Tue"]["aerobic_minutes"] == 45
    assert p1["Thu"]["aerobic_minutes"] == 45
    assert p1["Sat"]["aerobic_minutes"] == 60
    p1_text = json.dumps(p1).lower()
    for banned in ("run", "jump", "cut", "basketball", "stairmaster"):
        assert banned not in p1_text

    p2 = data["phases"]["2"]["days"]
    assert [p2[d]["aerobic_minutes"] for d in ("Tue", "Thu", "Sat")] == [45, 45, 60]
    p3 = data["phases"]["3"]["days"]
    self.assertEqual([p3[d]["aerobic_minutes"] for d in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")], [0, 45, 30, 15, 0, 30, 60])
    p4 = data["phases"]["4"]["days"]
    self.assertEqual([p4[d]["aerobic_minutes"] for d in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")], [0, 45, 30, 15, 45, 0, 60])


 def test_hsr_schedule_and_named_lift_progressions(self):
    data = program()
    expected_tendon_days = {"1": ("Mon", "Wed", "Fri"), "2": ("Mon", "Wed", "Fri"), "3": ("Mon", "Thu"), "4": ("Mon", "Thu")}
    for phase_number, phase in data["phases"].items():
        actual = tuple(day for day, spec in phase["days"].items() if spec["tendon_resistance"])
        self.assertEqual(actual, expected_tendon_days[phase_number])

    expected = {
        "1": {"Mon": "A", "Wed": "B", "Fri": "C"},
        "2": {"Mon": "A2", "Wed": "B2", "Fri": "C2"},
        "3": {"Mon": "A3", "Thu": "B3"},
        "4": {"Mon": "A4", "Thu": "B4"},
    }
    for phase_num, days in expected.items():
        for day, lift in days.items():
            assert data["phases"][phase_num]["days"][day]["lift"] == lift

    assert data["lifts"]["A"]["exercises"][0]["name"] == "Goblet Squat"
    assert data["lifts"]["B"]["exercises"][0]["name"] == "Supported Split Squat"
    assert data["lifts"]["C"]["exercises"][0]["name"] == "Leg Extension"
    assert tuple(day for day, spec in data["phases"]["3"]["days"].items() if spec.get("stage_schedule")) == ("Wed", "Sat")
    assert tuple(day for day, spec in data["phases"]["4"]["days"].items() if spec.get("stage_schedule")) == ("Wed", "Sat")

 def test_all_lift_definitions_are_referenced_by_the_approved_schedule(self):
    data = program()
    referenced = {
        day["lift"]
        for phase in data["phases"].values()
        for day in phase["days"].values()
        if day.get("lift")
    }
    self.assertEqual(set(data["lifts"]), referenced)

 def test_later_phase_sessions_match_approved_doses(self):
    data = program()
    expected = {
        "A2": [("Goblet Squat", "4x6-8", "3-0-2"), ("DB Bench Press", "3x6-10", "2-0-2"), ("Chest-Supported Row", "3x8-10", "2-1-2"), ("DB Romanian Deadlift", "3x8", "3-0-2"), ("Standing Calf Raise", "3x12", "2-1-3"), ("Suitcase Carry", "3x45 sec/side", "controlled")],
        "B2": [("Rear-Foot-Elevated Split Squat", "4x6-8/side", "3-0-2"), ("DB Overhead Press", "3x8", "2-0-2"), ("Lat Pulldown", "3x8-10", "2-1-2"), ("Hip Thrust", "3x8-10", "2-1-2"), ("Controlled 6-inch Step-Down", "3x6/side", "3-1-2"), ("Pallof Press", "3x10/side", "controlled")],
        "C2": [("Leg Extension", "4x8", "3-1-2"), ("Single-Leg Box Squat", "2x6/side technique", "3-1-2"), ("Incline DB Press", "3x8", "2-0-2"), ("One-Arm Row", "3x10/side", "2-1-2"), ("Back Extension", "3x10", "2-1-2"), ("Tib Raise", "3x15", "2-1-2"), ("Farmer Carry", "3x45 sec", "controlled")],
        "A3": [("Goblet Squat", "3x6", "3-0-2"), ("DB Bench Press", "3x8", "2-0-2"), ("Chest-Supported Row", "3x10", "2-1-2"), ("DB Romanian Deadlift", "3x8", "3-0-2"), ("Standing Calf Raise", "3x12", "2-1-3"), ("Suitcase Carry", "3x45 sec/side", "controlled")],
        "B3": [("Rear-Foot-Elevated Split Squat", "3x6/side", "3-0-2"), ("DB Overhead Press", "3x8", "2-0-2"), ("Lat Pulldown", "3x8", "2-1-2"), ("Hip Thrust", "3x8", "2-1-2"), ("Controlled Step-Down", "2x8/side", "3-1-2"), ("Pallof Press", "3x10/side", "controlled")],
        "A4": [("Goblet or Front Squat", "3x5-6", "3-0-2"), ("DB Bench Press", "3x6-8", "2-0-2"), ("Chest-Supported Row", "3x8", "2-1-2"), ("DB Romanian Deadlift", "3x6-8", "3-0-2"), ("Standing Calf Raise", "3x10", "2-1-3"), ("Suitcase Carry", "3x45 sec/side", "controlled")],
        "B4": [("Rear-Foot-Elevated Split Squat", "3x6/side", "3-0-2"), ("DB Overhead Press", "3x6-8", "2-0-2"), ("Lat Pulldown", "3x8", "2-1-2"), ("Hip Thrust", "3x8", "2-1-2"), ("Leg Extension", "3x8", "3-1-2"), ("Pallof Press", "3x10/side", "controlled")],
    }
    for lift_name, rows in expected.items():
        actual = [(e["name"], e["dose"], e["tempo"]) for e in data["lifts"][lift_name]["exercises"]]
        self.assertEqual(actual, rows, lift_name)

 def test_phase_one_sessions_match_approved_doses_and_substitutions(self):
    data = program()
    expected = {
        "A": [("Goblet Squat", "3x8", "3-0-3"), ("DB Bench Press or Push-up", "3x8-10", "2-0-2"), ("Chest-Supported DB Row", "3x10", "2-1-2"), ("DB Romanian Deadlift", "3x8", "3-0-2"), ("Standing Calf Raise", "3x12", "2-1-3"), ("Suitcase Carry", "3x30-45 sec/side", "controlled")],
        "B": [("Supported Split Squat", "3x8/side", "3-0-3"), ("Seated DB Overhead Press", "3x8", "2-0-2"), ("Lat Pulldown", "3x8-10", "2-1-2"), ("Hip Thrust", "3x10", "2-1-2"), ("Seated Soleus Raise", "3x15", "2-1-3"), ("Pallof Press", "3x10/side", "controlled")],
        "C": [("Leg Extension", "3x10", "3-1-3"), ("Incline DB Press", "3x8-10", "2-0-2"), ("One-Arm Row", "3x10/side", "2-1-2"), ("Back Extension or Hinge", "3x10", "3-1-2"), ("Tib Raise", "3x15", "2-1-2"), ("Farmer Carry", "3x30-45 sec", "controlled")],
    }
    for lift_name, rows in expected.items():
        actual = [(e["name"], e["dose"], e["tempo"]) for e in data["lifts"][lift_name]["exercises"]]
        self.assertEqual(actual, rows, lift_name)

 def test_optional_knee_tools_are_operational_and_not_between_session_loading(self):
    data = program()
    days = data["phases"]["1"]["days"]
    for day in ("Mon", "Wed", "Fri"):
        self.assertIn("before training only if it reduces pain", days[day]["knee_work"].lower())
        self.assertIn("OR", days[day]["knee_work"])
        self.assertIn("no between-session tendon loading", days[day]["knee_work"])
    for day in ("Tue", "Thu", "Sat", "Sun"):
        self.assertEqual(days[day]["knee_work"], "none; no between-session tendon loading")

    self.assertEqual(data["optional_warmups"], [
        {"name": "Backward Treadmill Walk", "dose": "5-8 min", "use": "optional before resistance training"},
        {"name": "Banded TKE", "dose": "2x15", "use": "optional before resistance training"},
    ])
    self.assertEqual(data["accessory_rotation"]["maximum"], 2)
    self.assertEqual(data["accessory_rotation"]["timing"], "after main work")
    self.assertEqual(data["accessory_rotation"]["options"], [
        {"name": "Banded External Rotation", "dose": "2x12/side"},
        {"name": "Hip Flexor Isometric Hold", "dose": "2x20-30 sec/side"},
    ])
    self.assertEqual(data["later_phase_options"]["heel_elevated_front_knee_bend"], {
        "phase": 2,
        "session": "Friday C2 after main work",
        "dose": "2x6/side controlled",
        "tempo": "3-0-2",
        "rule": "replace Single-Leg Box Squat, never add",
        "progression": "increase pain-free range, then add load",
    })
    self.assertEqual(data["later_phase_options"]["reverse_nordic"], {
        "phase": 3,
        "session": "Thursday B3 after main work",
        "dose": "2x6-8 controlled",
        "tempo": "3-1-2",
        "rule": "replace Controlled Step-Down, never add",
        "progression": "increase range before adding load",
    })


 def test_isometrics_are_optional_and_load_rules_are_exact(self):
    data = program()
    iso = data["knee_rules"]["optional_isometric"]
    assert iso["frequency"] == "only when it reduces pain"
    assert iso["hard_daily_work"] is False
    rules = data["knee_rules"]["response"]
    assert rules["during"] == "pain <=3/10 and non-escalating"
    assert rules["next_morning"] == "baseline"
    assert rules["worse_action"] == "reduce next knee or impact dose 30-50%"
    assert rules["flare_over_48h"] == "regress to the prior tolerated stage"


 def test_manual_phase_gates_and_return_progressions_are_explicit(self):
    data = program()
    gates = data["phase_gates"]
    assert gates["1_to_2"] == [
        "at least 2 stable weeks",
        "six completed lifts",
        "stairs at baseline",
        "60-minute walk at baseline",
        "no flare lasting more than 48 hours",
    ]
    assert gates["2_to_3"] == [
        "four stable weeks",
        "3x8 controlled 6-inch step-downs",
        "10 controlled single-leg box squats per side",
        "load or rep progression in each knee lift",
        "no next-morning symptom increase",
    ]
    assert gates["3_to_4"] == [
        "complete Phase 3 Week 5: 10:1 run-walk and repeated submaximal jumps 3x5 with stable responses",
        "complete Phase 3 Week 6: 30-minute easy continuous run and sport-specific jumps 3x4/side with stable responses",
        "two stable exposures at each applicable Week 5 and Week 6 stage, repeating the week as needed",
        "two stable 30-minute run-walk sessions",
        "two stable landing/jump exposures",
        "3x10 controlled step-downs per side",
        "sports PT or sports-medicine assessment before cutting",
    ]
    assert "clinician clearance" in gates["phase_4_to_games"]

    assert data["progressions"]["run"]["gate"] == "7 stable days + 60-minute brisk walk + 3x10 controlled step-downs + 10 single-leg box squats per side, with no next-day increase"
    assert data["progressions"]["run"]["start"] == "1 minute run : 2 minutes walk for 30 minutes"
    assert data["progressions"]["jump"]["spacing"] == "Wednesday and Saturday impact sessions require at least 72 elapsed hours; weekday labels alone do not prove spacing"
    assert data["progressions"]["stairmaster"] == {
        "gate": "7 stable days + pain-free normal stairs + 3x8 controlled 6-inch step-downs",
        "if_not_passed": "45 min swim or easy bike",
        "if_passed": "10 min StairMaster + 35 min swim or easy bike; total 45 min",
        "advance": "add 5 min StairMaster per stable week while reducing swim or easy bike by 5 min; total always 45 min",
    }
    assert "two stable exposures at each stage" in data["phase_gates"]["phase_4_to_games"]
    assert "baseline the following morning" in data["phase_gates"]["phase_4_to_games"]
    assert data["progressions"]["basketball"]["stages"] == [
        "shooting with no jumping",
        "planned acceleration and deceleration",
        "planned 45-degree cuts",
        "planned 90-degree cuts",
        "reactive cuts",
        "non-contact practice",
        "controlled contact practice",
        "games",
    ]


 def test_working_hypothesis_clinician_gate_and_red_flags(self):
    data = program()
    safety = data["safety"]
    assert safety["status"] == "working hypothesis, not a diagnosis"
    assert "sports PT or sports-medicine assessment is recommended" in safety["clinical"]
    assert "required before cutting or contact basketball" in safety["clinical"]
    required = {
        "swelling",
        "locking or catching",
        "instability or giving way",
        "inability to bear weight",
        "night or rest pain",
        "worsening symptoms",
        "chest pain",
        "faintness",
        "breathlessness disproportionate to effort",
    }
    assert required <= set(safety["red_flags"])
    assert "continue" not in safety["breathing_rule"].lower()


 def test_all_requested_movements_have_exactly_one_audited_role(self):
    data = program()
    expected = {
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
    audit = data["movement_audit"]
    assert len(audit) == 14
    assert {row["movement"] for row in audit} == set(expected)
    for row in audit:
        assert row["role"] == expected[row["movement"]]


 def test_rationale_has_required_sources(self):
    rationale = (HEALTH / "workout-program-rationale.md").read_text()
    for url in (
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC8070614/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC9528703/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10925836/",
        "https://www.who.int/europe/publications/i/item/9789240014886",
    ):
        assert url in rationale


 def test_renderer_covers_every_valid_phase_week_day_preview(self):
    data = program()
    rendered = 0
    for phase, max_week in {1: 4, 2: 4, 3: 6, 4: 7}.items():
        for week in range(1, max_week + 1):
            for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                with self.subTest(phase=phase, week=week, day=day):
                    result = subprocess.run(
                        [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", str(phase), "--week", str(week), "--day", day],
                        text=True,
                        capture_output=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(f"PHASE {phase}, WEEK {week}", result.stdout)
                    self.assertIn("PREVIEW — NEVER USED BY AUTOMATION", result.stdout)
                    self.assertIn("SESSION:", result.stdout)
                    self.assertIn("DURATION:", result.stdout)
                    self.assertIn("KNEE:", result.stdout)
                    self.assertIn("SAFETY:", result.stdout)
                    self.assertIn("swelling", result.stdout)
                    self.assertIn("chest pain", result.stdout)
                    if data["phases"][str(phase)]["days"][day].get("lift"):
                        self.assertIn("TEMPO", result.stdout)
                    lift_name = data["phases"][str(phase)]["days"][day].get("lift")
                    if lift_name:
                        positions = [result.stdout.index(exercise["name"]) for exercise in data["lifts"][lift_name]["exercises"]]
                        self.assertEqual(positions, sorted(positions), f"phase {phase} week {week} {day} exercise order")
                        self.assertLess(result.stdout.index("KNEE:"), positions[0], f"phase {phase} week {week} {day} pre-training isometric order")
                    rendered += 1
    self.assertEqual(rendered, 147)

 def test_renderer_resolves_all_phase_three_and_four_week_stages(self):
    expected_phase3_wed = {
        1: "run-walk 1:2",
        2: "run-walk 2:1",
        3: "run-walk 3:1",
        4: "run-walk 5:1",
        5: "run-walk 10:1",
        6: "30 min easy continuous run",
    }
    expected_phase3_sat = {
        1: "second run-walk 1:2 exposure",
        2: "bilateral landing — 3x5",
        3: "low pogo hops — 3x15",
        4: "jump rope — 3x30 sec OR low countermovement jump and stick — 3x5",
        5: "repeated submaximal jumps — 3x5",
        6: "sport-specific jumps — 3x4/side",
    }
    for week, marker in expected_phase3_sat.items():
        with self.subTest(phase=3, week=week):
            wed_output = subprocess.run(
                [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", "3", "--week", str(week), "--day", "Wed"],
                text=True, capture_output=True, check=True,
            ).stdout
            output = subprocess.run(
                [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", "3", "--week", str(week), "--day", "Sat"],
                text=True, capture_output=True, check=True,
            ).stdout
            self.assertIn(expected_phase3_wed[week], wed_output)
            self.assertIn(marker, output)
            self.assertNotIn("current stage", output.lower())
            self.assertIn("72 elapsed hours", output)
    expected_phase4 = {
        1: "planned acceleration and deceleration",
        2: "planned 45-degree cuts",
        3: "planned 90-degree cuts",
        4: "reactive cuts",
        5: "non-contact practice",
        6: "controlled contact practice",
        7: "games only after the final phase_4_to_games gate",
    }
    for week, marker in expected_phase4.items():
        for day in ("Wed", "Sat"):
            with self.subTest(phase=4, week=week, day=day):
                output = subprocess.run(
                    [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", "4", "--week", str(week), "--day", day],
                    text=True, capture_output=True, check=True,
                ).stdout
                self.assertIn(marker, output)
                self.assertIn("10-20 min", output)
                self.assertNotIn("current stage", output.lower())
                self.assertIn("72 elapsed hours", output)

 def test_phase_one_aerobic_modalities_are_day_specific(self):
    days = program()["phases"]["1"]["days"]
    self.assertEqual(days["Tue"]["aerobic"], "freestyle/backstroke swim or easy bike")
    self.assertEqual(days["Thu"]["aerobic"], "freestyle/backstroke swim or easy bike; row only if tolerated")
    self.assertNotIn("row", days["Tue"]["aerobic"].lower())

 def test_phase_two_tuesday_renders_exact_gated_stairmaster_substitution(self):
    expected = {
        "gate": "7 stable days + pain-free normal stairs + 3x8 controlled 6-inch step-downs",
        "if_not_passed": "45 min swim or easy bike",
        "if_passed": "10 min StairMaster + 35 min swim or easy bike; total 45 min",
        "advance": "add 5 min StairMaster per stable week while reducing swim or easy bike by 5 min; total always 45 min",
    }
    self.assertEqual(program()["progressions"]["stairmaster"], expected)
    output = subprocess.run(
        [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", "2", "--week", "1", "--day", "Tue"],
        text=True, capture_output=True, check=True,
    ).stdout
    self.assertIn(f"STAIRMASTER GATE: {expected['gate']}", output)
    self.assertIn(f"IF NOT PASSED: {expected['if_not_passed']}", output)
    self.assertIn(f"IF PASSED: {expected['if_passed']}", output)
    self.assertIn(f"PROGRESSION: {expected['advance']}", output)
    self.assertEqual(output.count("total 45 min"), 1)
    self.assertEqual(output.count("total always 45 min"), 1)

 def test_validator_rejects_any_stairmaster_contract_mutation(self):
    validator = load_module(VALIDATOR, "workout_validator_stairmaster_exact")
    mutations = {
        "gate": "stairs feel okay",
        "if_not_passed": "20 min StairMaster",
        "if_passed": "45 min StairMaster",
        "advance": "add 5 min without reducing low impact",
    }
    for field, value in mutations.items():
        with self.subTest(field=field):
            bad = copy.deepcopy(program())
            bad["progressions"]["stairmaster"][field] = value
            self.assertTrue(any("stairmaster" in error.lower() for error in validator.validate(bad)))

 def test_later_options_are_explicit_session_substitutions_not_added_volume(self):
    data = program()
    self.assertEqual(data["phases"]["2"]["days"]["Fri"]["substitution"], {
        "option": "Heel-Elevated Supported Front-Knee Bend",
        "dose": "2x6/side controlled",
        "tempo": "3-0-2",
        "rule": "after main work; replace Single-Leg Box Squat, never add",
    })
    self.assertEqual(data["phases"]["3"]["days"]["Thu"]["substitution"], {
        "option": "Reverse Nordic",
        "dose": "2x6-8 controlled",
        "tempo": "3-1-2",
        "rule": "after main work; replace Controlled Step-Down, never add",
    })
    for phase, day, option, replaced in (
        (2, "Fri", "Heel-Elevated Supported Front-Knee Bend", "Single-Leg Box Squat"),
        (3, "Thu", "Reverse Nordic", "Controlled Step-Down"),
    ):
        rendered = subprocess.run(
            [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", str(phase), "--week", "1", "--day", day],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertIn("SUBSTITUTION (REPLACE, DO NOT ADD):", rendered)
        self.assertIn(option, rendered)
        self.assertIn(replaced, rendered)

 def test_impact_days_require_elapsed_72_hours_and_no_three_consecutive_load_days(self):
    data = program()
    for phase_number in ("3", "4"):
        impact_days = [day for day, spec in data["phases"][phase_number]["days"].items() if spec.get("stage_schedule")]
        self.assertEqual(impact_days, ["Wed", "Sat"])
    spacing = data["impact_spacing_rule"]
    self.assertIn("72 elapsed hours", spacing)
    self.assertIn("weekday labels alone do not prove spacing", spacing)
    self.assertIn("skip impact", spacing)
    ordered = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for phase_number, phase in data["phases"].items():
        loaded = [bool(phase["days"][day].get("tendon_resistance") or phase["days"][day].get("stage_schedule")) for day in ordered]
        self.assertFalse(any(all(loaded[index:index + 3]) for index in range(5)), f"phase {phase_number} has 3 consecutive load days")

 def test_zone_two_definition_is_bound_and_rendered_on_every_aerobic_card(self):
    data = program()
    definition = "Zone 2 = RPE 3-4/10 and the full-sentence talk test (able to speak in full sentences); brisk walks count only when they meet both"
    self.assertEqual(data["zone2_definition"], definition)
    max_weeks = {1: 4, 2: 4, 3: 6, 4: 7}
    for phase in range(1, 5):
        for week in range(1, max_weeks[phase] + 1):
            for day, spec in data["phases"][str(phase)]["days"].items():
                if not spec["aerobic_minutes"] and not spec.get("low_impact_fallback"):
                    continue
                output = subprocess.run(
                    [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", str(phase), "--week", str(week), "--day", day],
                    text=True, capture_output=True, check=True,
                ).stdout
                self.assertIn(definition, output, f"missing Zone 2 definition phase {phase} week {week} {day}")

 def test_phase_three_week_one_blocks_jumps_and_false_advancement(self):
    output = subprocess.run(
        [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", "3", "--week", "1", "--day", "Sat"],
        text=True, capture_output=True, check=True,
    ).stdout
    self.assertIn("No jumps until two stable 30-minute run exposures", output)
    self.assertIn("If Wednesday was not stable, Saturday does not count as the second stable exposure", output)
    self.assertIn("do not advance", output.lower())
    self.assertNotIn("after landing/jump work", output)


 def test_validator_exits_nonzero_for_conflicting_daily_knee_work(self):
    import tempfile
    data = program()
    bad = copy.deepcopy(data)
    bad["phases"]["1"]["days"]["Mon"]["knee_work"] = "hard Spanish squat isometrics"
    bad["phases"]["1"]["days"]["Mon"]["tendon_resistance"] = True
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "bad.md"
        source.write_text("# bad\n\n```json program\n" + json.dumps(bad) + "\n```\n")
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(source)], text=True, capture_output=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("conflicting daily knee work", result.stderr.lower())

 def test_validator_rejects_manual_gate_drift(self):
    validator = load_module(VALIDATOR, "workout_validator_gate")
    bad = copy.deepcopy(program())
    bad["phase_gates"]["3_to_4"].remove("sports PT or sports-medicine assessment before cutting")
    self.assertTrue(any("phase gates" in error.lower() for error in validator.validate(bad)))

 def test_validator_rejects_safety_dose_and_progression_mutations(self):
    validator = load_module(VALIDATOR, "workout_validator_mutations")
    mutations = {
        "tendon dose": lambda d: d["lifts"]["A"]["exercises"][0].update(dose="9x99"),
        "tendon tempo": lambda d: d["lifts"]["C"]["exercises"][0].update(tempo="fast"),
        "run progression": lambda d: d["progressions"]["run"].update(start="continuous sprint"),
        "StairMaster gate": lambda d: d["progressions"]["stairmaster"].update(gate="whenever"),
        "red flags": lambda d: d["safety"]["red_flags"].remove("chest pain"),
        "clinician requirement": lambda d: d["safety"].update(clinical="optional"),
        "impact spacing": lambda d: d["progressions"]["jump"].update(spacing="consecutive days"),
    }
    for label, mutate in mutations.items():
        with self.subTest(label=label):
            bad = copy.deepcopy(program())
            mutate(bad)
            self.assertTrue(validator.validate(bad), f"validator accepted mutated {label}")

 def test_validator_rejects_tendon_resistance_flag_drift(self):
    validator = load_module(VALIDATOR, "workout_validator_tendon_flags")
    expected = {"1": ("Mon", "Wed", "Fri"), "2": ("Mon", "Wed", "Fri"), "3": ("Mon", "Thu"), "4": ("Mon", "Thu")}
    for phase, days in expected.items():
        for day in days:
            with self.subTest(phase=phase, day=day):
                bad = copy.deepcopy(program())
                bad["phases"][phase]["days"][day]["tendon_resistance"] = False
                self.assertTrue(validator.validate(bad), f"accepted missing tendon resistance on phase {phase} {day}")

 def test_validator_rejects_pain_response_drift(self):
    validator = load_module(VALIDATOR, "workout_validator_pain_response")
    for field in ("during", "next_morning", "worse_action", "flare_over_48h"):
        with self.subTest(field=field):
            bad = copy.deepcopy(program())
            bad["knee_rules"]["response"][field] = "continue anyway"
            self.assertTrue(validator.validate(bad), f"accepted changed pain rule {field}")

 def test_validator_rejects_movement_and_operational_dose_drift(self):
    validator = load_module(VALIDATOR, "workout_validator_movement_contract")
    mutations = {
        "movement name": lambda d: d["movement_audit"][0].update(movement="Other squat"),
        "movement role": lambda d: d["movement_audit"][0].update(role="optional"),
        "warm-up dose": lambda d: d["optional_warmups"][0].update(dose="20 min"),
        "accessory dose": lambda d: d["accessory_rotation"]["options"][0].update(dose="5x20"),
        "accessory cap": lambda d: d["accessory_rotation"].update(maximum=4),
        "later option dose": lambda d: d["later_phase_options"]["reverse_nordic"].update(dose="5x20"),
        "session substitution": lambda d: d["phases"]["2"]["days"]["Fri"].pop("substitution", None),
    }
    for label, mutate in mutations.items():
        with self.subTest(label=label):
            bad = copy.deepcopy(program())
            mutate(bad)
            self.assertTrue(validator.validate(bad), f"accepted changed {label}")

 def test_validator_rejects_aerobic_distribution_modality_and_sprints(self):
    validator = load_module(VALIDATOR, "workout_validator_aerobic_contract")
    for phase in ("1", "2", "3", "4"):
        with self.subTest(phase=phase, mutation="redistribution"):
            bad = copy.deepcopy(program())
            bad["phases"][phase]["days"]["Sun"]["aerobic_minutes"] += 1
            self.assertTrue(validator.validate(bad), f"accepted redistributed phase {phase} aerobic minutes")
        active = next(day for day in ("Mon", "Tue", "Thu", "Sat") if program()["phases"][phase]["days"][day].get("aerobic"))
        with self.subTest(phase=phase, mutation="modality"):
            bad = copy.deepcopy(program())
            bad["phases"][phase]["days"][active]["aerobic"] = "all-out sprints"
            self.assertTrue(validator.validate(bad), f"accepted all-out sprints in phase {phase}")

 def test_validator_binds_revised_stage_schedules_and_elapsed_spacing(self):
    validator = load_module(VALIDATOR, "workout_validator_stage_schedule")
    mutations = {
        "phase 3 stage": lambda d: d["stage_schedules"]["phase3"]["2"].update(Sat="reactive cuts"),
        "phase 4 stage": lambda d: d["stage_schedules"]["phase4"]["3"].update(Wed="maximal cuts"),
        "phase 4 games gate": lambda d: d["stage_schedules"]["phase4"]["7"].update(Wed="games"),
        "spacing": lambda d: d.update(impact_spacing_rule="Wednesday and Saturday are enough"),
        "week 1 stability": lambda d: d.update(phase3_week1_rule="advance after Saturday"),
    }
    for label, mutate in mutations.items():
        with self.subTest(label=label):
            bad = copy.deepcopy(program())
            mutate(bad)
            self.assertTrue(validator.validate(bad), f"accepted changed {label}")

 def test_validator_rejects_revised_high_low_schedule_shape_drift(self):
    validator = load_module(VALIDATOR, "workout_validator_high_low_shape")
    mutations = {
        "phase 3 Monday lift": lambda d: d["phases"]["3"]["days"]["Mon"].update(lift="C3"),
        "phase 3 Friday rest": lambda d: d["phases"]["3"]["days"]["Fri"].update(session="Plyometrics"),
        "phase 4 Wednesday duration": lambda d: d["phases"]["4"]["days"]["Wed"].update(duration="90 min"),
        "phase 4 Saturday fallback": lambda d: d["phases"]["4"]["days"]["Sat"].update(low_impact_fallback="ignore elapsed time"),
    }
    for label, mutate in mutations.items():
        with self.subTest(label=label):
            bad = copy.deepcopy(program())
            mutate(bad)
            self.assertTrue(validator.validate(bad), f"accepted changed {label}")

 def test_validator_binds_jump_and_basketball_stage_lists(self):
    data = program()
    self.assertEqual(data["progressions"]["jump"]["stages"], [
        "bilateral landing",
        "low pogo hops",
        "jump rope",
        "low countermovement jump and stick",
        "repeated submaximal jumps",
        "sport-specific jumps",
    ])
    self.assertEqual(data["progressions"]["basketball"]["stages"], [
        "shooting with no jumping",
        "planned acceleration and deceleration",
        "planned 45-degree cuts",
        "planned 90-degree cuts",
        "reactive cuts",
        "non-contact practice",
        "controlled contact practice",
        "games",
    ])
    validator = load_module(VALIDATOR, "workout_validator_stage_lists")
    for progression in ("jump", "basketball"):
        for mutation in ("empty", "changed"):
            with self.subTest(progression=progression, mutation=mutation):
                bad = copy.deepcopy(data)
                if mutation == "empty":
                    bad["progressions"][progression]["stages"] = []
                else:
                    bad["progressions"][progression]["stages"][0] = "maximal competition"
                self.assertTrue(validator.validate(bad), f"accepted {mutation} {progression} stages")

 def test_all_declared_pre_cut_stages_are_reachable_before_phase_four(self):
    data = program()
    scheduled = json.dumps(data["stage_schedules"]["phase3"]).lower()
    for stage in data["progressions"]["run"]["stages"] + data["progressions"]["jump"]["stages"]:
        with self.subTest(stage=stage):
            self.assertIn(stage.lower(), scheduled)

    validator = load_module(VALIDATOR, "workout_validator_reachability")
    for progression in ("run", "jump"):
        with self.subTest(progression=progression):
            bad = copy.deepcopy(data)
            bad["progressions"][progression]["stages"].append("declared but unscheduled stage")
            errors = validator.validate(bad)
            self.assertTrue(any("not scheduled" in error.lower() for error in errors), errors)

 def test_validator_binds_rir_and_weekly_progression_rule(self):
    validator = load_module(VALIDATOR, "workout_validator_loading_rule")
    expected = "Finish resistance sets with 2-4 reps in reserve. Add reps before load and change only one variable per week: reps, load, range, or impact contacts."
    self.assertEqual(program()["knee_rules"]["loading"], expected)
    for replacement in ("Train every set to failure.", "Add load before reps.", "Change load and impact together every day."):
        with self.subTest(replacement=replacement):
            bad = copy.deepcopy(program())
            bad["knee_rules"]["loading"] = replacement
            self.assertTrue(validator.validate(bad), "accepted changed resistance progression rule")

 def test_validator_binds_structured_optional_isometric_prescription(self):
    expected = {
        "frequency": "only when it reduces pain",
        "hard_daily_work": False,
        "one_option_only": True,
        "dose": "4x30-45 sec with 2 min rest",
        "options": ["banded Spanish squat", "mid-range leg-extension quadriceps isometric"],
    }
    self.assertEqual(program()["knee_rules"]["optional_isometric"], expected)
    validator = load_module(VALIDATOR, "workout_validator_isometric_contract")
    mutations = {
        "dose": lambda d: d["knee_rules"]["optional_isometric"].update(dose="10x60 sec"),
        "rest": lambda d: d["knee_rules"]["optional_isometric"].update(dose="4x30-45 sec with no rest"),
        "one option": lambda d: d["knee_rules"]["optional_isometric"].update(one_option_only=False),
        "pain response": lambda d: d["knee_rules"]["optional_isometric"].update(frequency="every day"),
    }
    for label, mutate in mutations.items():
        with self.subTest(label=label):
            bad = copy.deepcopy(program())
            mutate(bad)
            self.assertTrue(validator.validate(bad), f"accepted changed isometric {label}")

 def test_substitution_cards_render_numeric_tendon_tempos(self):
    expected = {
        (2, "Fri"): ("Heel-Elevated Supported Front-Knee Bend", "3-0-2"),
        (3, "Thu"): ("Reverse Nordic", "3-1-2"),
    }
    for (phase, day), (name, tempo) in expected.items():
        with self.subTest(phase=phase, day=day):
            substitution = program()["phases"][str(phase)]["days"][day]["substitution"]
            self.assertEqual(substitution["tempo"], tempo)
            rendered = subprocess.run(
                [sys.executable, str(RENDERER), "--source", str(SOURCE), "--preview", "--phase", str(phase), "--week", "1", "--day", day],
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            line = next(row for row in rendered.splitlines() if row.startswith("SUBSTITUTION"))
            self.assertIn(name, line)
            self.assertIn(f"TEMPO {tempo}", line)


 def test_validator_accepts_canonical_source(self):
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(SOURCE)], text=True, capture_output=True
    )
    assert result.returncode == 0, result.stderr
    assert "VALID" in result.stdout


if __name__ == "__main__":
    unittest.main()
