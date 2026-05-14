#!/usr/bin/env python3
"""Generate JT's weekly Spanish evaluation/progress artifact.

This is a local, non-delivery script. It does not send lesson content and it
never marks a week as passed automatically. It creates a structured review file
so the learning loop has an auditable evaluation artifact instead of relying on
ad hoc daily lesson notes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPANISH = ROOT / "spanish"
STATE_PATH = SPANISH / "state.json"
CURRICULUM_PATH = SPANISH / "curriculum.md"
LESSONS_DIR = SPANISH / "lessons"
EVALUATIONS_DIR = SPANISH / "evaluations"

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


@dataclass(frozen=True)
class LessonRecord:
    path: Path
    lesson_date: date
    claimed_week: int | None
    topic: str


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def parse_iso(value: str, field: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{field} must be YYYY-MM-DD, got {value!r}") from exc


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def curriculum_weeks() -> dict[int, str]:
    text = CURRICULUM_PATH.read_text(encoding="utf-8")
    weeks: dict[int, str] = {}
    for match in re.finditer(r"^## Week\s+(\d+)\s+[—-]\s+(.+)$", text, re.MULTILINE):
        weeks[int(match.group(1))] = match.group(2).strip()
    return weeks


def week_window(started: date, week: int) -> tuple[date, date]:
    start = started + timedelta(days=(week - 1) * 7)
    return start, start + timedelta(days=6)


def calendar_week_for(started: date, target: date) -> int:
    return ((target - started).days // 7) + 1


def resolve_week(selector: str, today: date, started: date) -> int:
    current = calendar_week_for(started, today)
    if selector == "current":
        return current
    if selector == "last":
        return max(1, current - 1)
    return int(selector)


def extract_lesson(path: Path) -> LessonRecord | None:
    try:
        lesson_date = parse_iso(path.stem, path.name)
    except ValueError:
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    topic = ""
    patterns = [
        r"\*\*Topic:\*\*\s*([^\n]+)",
        r"Topic:\s*([^\n]+)",
        r"\|\s*Topic:\s*([^\n]+)",
        r"## Topic\s*\n([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            topic = match.group(1).strip().strip("*")
            break
    claimed_week = None
    match = re.search(r"Week\s*(\d+)", text, re.IGNORECASE)
    if match:
        claimed_week = int(match.group(1))
    return LessonRecord(path=path, lesson_date=lesson_date, claimed_week=claimed_week, topic=topic or "(topic not recorded)")


def normalize_topic(topic: str) -> str:
    cleaned = re.sub(r"\([^)]*\)", "", topic.lower())
    cleaned = re.sub(r"week\s*\d+|day\s*\d+|part\s*\d+", "", cleaned)
    cleaned = re.sub(r"[^a-záéíóúñü\s]", " ", cleaned)
    return " ".join(cleaned.split())


def lessons_for_window(start: date, end: date) -> list[LessonRecord]:
    lessons = []
    for path in sorted(LESSONS_DIR.glob("20*.md")):
        rec = extract_lesson(path)
        if rec and start <= rec.lesson_date <= end:
            lessons.append(rec)
    return lessons


def build_report(week: int, today: date) -> tuple[Path, str, bool]:
    state = load_state()
    started = parse_iso(state["started"], "started")
    weeks = curriculum_weeks()
    start, end = week_window(started, week)
    lessons = lessons_for_window(start, end)
    theme = weeks.get(week, "MISSING FROM CURRICULUM")

    drift: list[str] = []
    if week not in weeks:
        drift.append(f"Week {week} is not defined in spanish/curriculum.md.")

    if not lessons:
        drift.append(f"No saved lesson files found for Week {week} ({start} to {end}).")

    seen: dict[str, list[str]] = {}
    for rec in lessons:
        if rec.claimed_week is not None and rec.claimed_week != week:
            drift.append(
                f"{rec.path.name} claims Week {rec.claimed_week}, but calendar/curriculum window is Week {week}."
            )
        key = normalize_topic(rec.topic)
        if key:
            seen.setdefault(key, []).append(rec.path.name)
    for topic, files in seen.items():
        if len(files) > 1:
            drift.append(f"Repeated topic '{topic}' across: {', '.join(files)}.")

    status = "NEEDS_REPAIR" if drift else "READY_FOR_JT_EVAL"
    path = EVALUATIONS_DIR / f"{end.isoformat()}-week-{week}.md"

    lesson_rows = []
    if lessons:
        for rec in lessons:
            lesson_rows.append(
                f"| {rec.lesson_date} | {rec.claimed_week or '—'} | {rec.topic.replace('|', '/')} | `{rec.path.name}` |"
            )
    else:
        lesson_rows.append("| — | — | No lesson files found | — |")

    drift_text = "\n".join(f"- ⚠️ {item}" for item in drift) if drift else "- ✅ No progression drift detected in this week window."

    recommendation = (
        "Do not count this week as passed. Keep the next daily lessons on the current curriculum week and avoid recycled Week 2 topics until JT completes a spoken check."
        if drift
        else "Run the spoken evaluation below with JT. Advance only if score is 6/10 or higher."
    )

    content = f"""# Spanish Weekly Evaluation — Week {week}
**Generated:** {today.isoformat()}  
**Week window:** {start.isoformat()} to {end.isoformat()}  
**Status:** {status}

## State snapshot
- Current state week: {state.get('current_week')}
- Current state day: {state.get('current_day')}
- Last lesson date: {state.get('last_lesson_date')}
- Last lesson complete: {state.get('last_lesson_complete')}
- Total lessons completed: {state.get('total_lessons_completed')}

## Curriculum theme
{theme}

## Lessons reviewed
| Date | Claimed week | Saved topic | File |
|---|---:|---|---|
{chr(10).join(lesson_rows)}

## Progression / drift checks
{drift_text}

## JT spoken evaluation script
Use this as the next evaluation prompt. Do **not** mark the week passed until JT responds.

1. **Role-play, 2 minutes:** Eve plays girlfriend/family member. JT answers only in Spanish.
2. **Recall prompts:** ask 5 quick prompts from this week's actual lesson topics.
3. **Repair prompt:** ask JT to correct one known weak spot: `conocer` vs `saber`, `no hay problema` instead of `no problemo`, or `e/y` before vowel sounds.
4. **Real-world challenge check:** ask whether he used one phrase outside the lesson.

## Scoring rubric
- Meaning conveyed: /4
- Natural phrase choice: /2
- Pronunciation/listening clarity: /2
- Confidence/recovery after mistakes: /2
- **Pass threshold:** 6/10

## Recommendation
{recommendation}
"""
    return path, content, bool(drift)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a weekly Spanish evaluation artifact")
    parser.add_argument("--date", default=date.today().isoformat(), help="Anchor date, YYYY-MM-DD")
    parser.add_argument("--week", default="current", help="Week number, 'current', or 'last'")
    parser.add_argument("--write", action="store_true", help="Write the evaluation file")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing evaluation file")
    args = parser.parse_args()

    today = parse_iso(args.date, "--date")
    state = load_state()
    started = parse_iso(state["started"], "started")
    week = resolve_week(args.week, today, started)
    path, content, drifted = build_report(week, today)

    if not args.write:
        print(content)
        print(f"\nDRY_RUN_PATH={path}")
        return 2 if drifted else 0

    EVALUATIONS_DIR.mkdir(parents=True, exist_ok=True)
    if path.exists() and not args.force:
        return fail(f"evaluation already exists: {path} (use --force to overwrite)")
    path.write_text(content, encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(path), "week": week, "drift_detected": drifted}, indent=2))
    return 2 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())
