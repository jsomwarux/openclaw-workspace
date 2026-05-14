#!/usr/bin/env python3
"""Validate JT's Spanish learning state and latest lesson artifact.

Read-only guard for heartbeat/audits. It intentionally does not mark lessons
complete; completion should come from JT practice/evaluation, not from cron
execution metadata.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "spanish" / "state.json"
LESSONS = ROOT / "spanish" / "lessons"
CURRICULUM = ROOT / "spanish" / "curriculum.md"
EVALUATIONS = ROOT / "spanish" / "evaluations"
REQUIRED = {
    "started": str,
    "level": str,
    "goal": str,
    "current_day": int,
    "current_week": int,
    "last_lesson_date": str,
    "last_lesson_complete": bool,
    "lesson_streak": int,
    "longest_streak": int,
    "total_lessons_completed": int,
}


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def parse_iso(value: str, field: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{field} must be YYYY-MM-DD, got {value!r}") from exc


def curriculum_weeks() -> set[int]:
    try:
        text = CURRICULUM.read_text(encoding="utf-8")
    except Exception:
        return set()
    return {int(m.group(1)) for m in re.finditer(r"^## Week\s+(\d+)\s+[—-]", text, re.MULTILINE)}


def calendar_week(started: date, current: date) -> int:
    return ((current - started).days // 7) + 1


def latest_lesson_claimed_week(text: str) -> int | None:
    # Prefer the hardened explicit marker. Older lesson files sometimes mention
    # old weeks inside topic text, which is useful history but not a reliable
    # curriculum-week marker after drift repair.
    for pattern in [r"Curriculum week used:\s*Week\s*(\d+)", r"Progression repair:\s*Week\s*(\d+)"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    match = re.search(r"Week\s*(\d+)", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def normalized_topic(text: str) -> str:
    topic = ""
    for pattern in [r"\*\*Topic:\*\*\s*([^\n]+)", r"Topic:\s*([^\n]+)", r"## Topic\s*\n([^\n]+)"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            topic = match.group(1)
            break
    topic = re.sub(r"\([^)]*\)", "", topic.lower())
    topic = re.sub(r"week\s*\d+|day\s*\d+|part\s*\d+", "", topic)
    topic = re.sub(r"[^a-záéíóúñü\s]", " ", topic)
    return " ".join(topic.split())


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate spanish/state.json and latest lesson file")
    parser.add_argument("--date", default=date.today().isoformat(), help="Expected current date, YYYY-MM-DD")
    parser.add_argument("--max-age-days", type=int, default=2, help="Fail if latest lesson is older than this")
    parser.add_argument("--require-today", action="store_true", help="Require last_lesson_date to equal --date")
    parser.add_argument("--check-progression", action="store_true", help="Validate curriculum week coverage and latest lesson week/topic drift")
    parser.add_argument("--require-evaluation", action="store_true", help="Require a weekly evaluation artifact for the latest completed Sunday window")
    args = parser.parse_args()

    today = parse_iso(args.date, "--date")

    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read/parse {STATE}: {exc}")

    for key, expected_type in REQUIRED.items():
        if key not in state:
            return fail(f"missing required key {key!r}")
        if not isinstance(state[key], expected_type):
            return fail(f"{key!r} must be {expected_type.__name__}, got {type(state[key]).__name__}")

    try:
        started = parse_iso(state["started"], "started")
        last = parse_iso(state["last_lesson_date"], "last_lesson_date")
    except ValueError as exc:
        return fail(str(exc))

    if last < started:
        return fail("last_lesson_date is before started date")
    if last > today:
        return fail("last_lesson_date is in the future")
    if args.require_today and last != today:
        return fail(f"last_lesson_date {last} does not equal expected date {today}")
    if today - last > timedelta(days=args.max_age_days):
        return fail(f"last lesson is stale: {last} ({(today-last).days} days ago)")

    lesson_file = LESSONS / f"{last.isoformat()}.md"
    if not lesson_file.exists():
        return fail(f"missing lesson file {lesson_file}")
    lesson_text = lesson_file.read_text(encoding="utf-8").strip()
    if len(lesson_text) < 80:
        return fail(f"lesson file too short: {lesson_file}")
    if "Topic" not in lesson_text and "Phrases" not in lesson_text and "Spanish Lesson" not in lesson_text:
        return fail(f"lesson file lacks topic/phrase markers: {lesson_file}")

    if args.check_progression:
        weeks = curriculum_weeks()
        expected_week = calendar_week(started, last)
        if expected_week not in weeks:
            return fail(f"calendar week {expected_week} for {last} is missing from curriculum")
        if state["current_week"] != expected_week:
            return fail(f"state.current_week {state['current_week']} does not match calendar/curriculum week {expected_week}")
        claimed_week = latest_lesson_claimed_week(lesson_text)
        if claimed_week is not None and claimed_week != expected_week:
            return fail(f"latest lesson claims Week {claimed_week}, expected Week {expected_week}")
        recent_topics = []
        for path in sorted(LESSONS.glob("20*.md"))[-3:]:
            recent_topics.append((path.name, normalized_topic(path.read_text(encoding="utf-8", errors="replace"))))
        nonempty = [(name, topic) for name, topic in recent_topics if topic]
        if len(nonempty) >= 2 and nonempty[-1][1] == nonempty[-2][1]:
            return fail(f"latest lesson topic repeats previous lesson topic: {nonempty[-1][1]!r}")

    if args.require_evaluation:
        # Require evaluation for the most recent completed Sunday on or before --date.
        sunday = today - timedelta(days=(today.weekday() - 6) % 7)
        if today.weekday() != 6:
            sunday -= timedelta(days=7)
        if sunday >= started:
            eval_week = calendar_week(started, sunday)
            candidates = list(EVALUATIONS.glob(f"{sunday.isoformat()}-week-{eval_week}.md"))
            if not candidates:
                return fail(f"missing weekly evaluation artifact for Week {eval_week}: {EVALUATIONS / f'{sunday.isoformat()}-week-{eval_week}.md'}")

    lesson_count = len(list(LESSONS.glob("20*.md")))
    if state["current_day"] < lesson_count:
        return fail(f"current_day {state['current_day']} is less than saved lesson file count {lesson_count}")
    if state["longest_streak"] < state["lesson_streak"]:
        return fail("longest_streak is lower than lesson_streak")
    if state["total_lessons_completed"] > lesson_count:
        return fail("total_lessons_completed exceeds saved lesson file count")

    status = {
        "ok": True,
        "last_lesson_date": last.isoformat(),
        "last_lesson_complete": state["last_lesson_complete"],
        "current_day": state["current_day"],
        "current_week": state["current_week"],
        "lesson_files": lesson_count,
        "latest_lesson_file": str(lesson_file),
        "progression_checked": args.check_progression,
        "evaluation_checked": args.require_evaluation,
    }
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
