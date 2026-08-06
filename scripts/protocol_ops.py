#!/usr/bin/env python3
"""Deterministic helpers for JT's 14-day protocol ops."""

from __future__ import annotations

import argparse
import json
import re
import statistics
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from zoneinfo import ZoneInfo


WORKSPACE = Path("/Users/jtsomwaru/.openclaw/workspace")
REFERENCE_PATH = WORKSPACE / "health" / "protocol-reference.md"
LOG_PATH = WORKSPACE / "health" / "protocol-log.jsonl"
STATE_PATH = WORKSPACE / "health" / "protocol-state.json"
START_DATE = date(2026, 8, 5)
END_DATE = date(2026, 8, 18)
NY_TZ = ZoneInfo("America/New_York")

DEFAULT_BOOKINGS = [
    (1, "prescriber"),
    (2, "laryngologist"),
    (3, "therapist"),
    (4, "pelvic PT"),
]

MOOD_RE = re.compile(
    r"\b(hopeless|hopelessness|harm myself|kill myself|suicid|can't go on|cant go on)\b",
    re.IGNORECASE,
)


def today() -> date:
    return datetime.now(NY_TZ).date()


def _load_reference(path: Optional[Path] = None) -> str:
    path = path or REFERENCE_PATH
    if not path.exists():
        raise SystemExit(f"REFERENCE_NOT_FOUND: {path}")
    return path.read_text(encoding="utf-8")


def bookings(reference_text: Optional[str] = None) -> List[tuple[int, str]]:
    text = reference_text if reference_text is not None else _load_reference()
    found: List[tuple[int, str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 4 or not parts[0].isdigit():
            continue
        status = parts[2].upper()
        if status != "OUTSTANDING":
            continue
        number = int(parts[0])
        label = {
            1: "prescriber",
            2: "laryngologist",
            3: "therapist",
            4: "pelvic PT",
        }.get(number, parts[1])
        found.append((number, label))
    return found or list(DEFAULT_BOOKINGS)


def _load_state(path: Optional[Path] = None) -> Dict[str, Any]:
    path = path or STATE_PATH
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"STATE_CORRUPT: {path}: {exc}") from exc


def _write_state(data: Dict[str, Any], path: Optional[Path] = None) -> None:
    path = path or STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    tmp.replace(path)


def morning_message() -> Dict[str, Any]:
    day = day_number()
    if day == 15:
        return {"ok": True, "action": "stand_down", "day": day, "message": "14 days complete. Protocol reference archived. Standing down."}
    if day < 1 or day > 14:
        return {"ok": True, "action": "skip", "day": day}
    outstanding_items = bookings()
    outstanding = ", ".join(f"{number} {label}" for number, label in outstanding_items)
    message = f"Resting HR?\nBookings outstanding: {outstanding}"
    if day == 5:
        message += "\n" + "\n".join(f"Booking {number} has been outstanding 5 days." for number, _ in outstanding_items)
    return {
        "ok": True,
        "action": "send",
        "day": day,
        "message": message,
    }


def tracker_message() -> Dict[str, Any]:
    day = day_number()
    if day < 1 or day > 14:
        return {"ok": True, "action": "skip", "day": day}
    return {"ok": True, "action": "send", "day": day, "message": "Tracker."}


def _records(path: Path = LOG_PATH) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for idx, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"LOG_CORRUPT: {path}:{idx}: {exc}") from exc
    return rows


def _append(record: Dict[str, Any], path: Optional[Path] = None) -> Dict[str, Any]:
    path = path or LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    return {"ok": True, "status": "Logged."}


def log_morning_hr(raw: str, *, record_date: Optional[date] = None) -> Dict[str, Any]:
    text = raw.strip()
    if not re.fullmatch(r"\d{2,3}", text):
        raise SystemExit("UNVERIFIED")
    day = (record_date or today()).isoformat()
    state = _load_state()
    state.setdefault("morning_hr", {})[day] = int(text)
    _write_state(state)
    return {"ok": True, "status": "Logged."}


def _yn(value: str) -> str:
    normalized = value.strip().upper()
    if normalized not in {"Y", "N"}:
        raise SystemExit("UNVERIFIED")
    return normalized


def _bool_from_yn(value: str) -> bool:
    return _yn(value) == "Y"


def log_tracker(values: List[str], *, record_date: Optional[date] = None) -> Dict[str, Any]:
    if len(values) < 7:
        raise SystemExit("UNVERIFIED")
    hr, slept, alcohol, aerobic, social, clenching, symptom = values[:7]
    note = " ".join(values[7:]).strip() if len(values) > 7 else ""
    if note and MOOD_RE.search(note):
        print("988 (call or text). And tell someone today.")
        raise SystemExit(0)

    record_day = record_date or today()
    state = _load_state()
    stored_hr = state.get("morning_hr", {}).get(record_day.isoformat())
    hr_value = int(hr) if hr.strip().lower() not in {"null", "none", "-"} else stored_hr
    record = {
        "date": record_day.isoformat(),
        "hr_waking": hr_value,
        "hours_slept": float(slept),
        "alcohol": _bool_from_yn(alcohol),
        "aerobic": _bool_from_yn(aerobic),
        "social": _bool_from_yn(social),
        "clenching": int(clenching),
        "symptom": int(symptom),
        "note": note,
    }
    if record["hr_waking"] is not None:
        record["hr_waking"] = int(record["hr_waking"])
    if not 0 <= record["clenching"] <= 5:
        raise SystemExit("UNVERIFIED")
    if not 0 <= record["symptom"] <= 10:
        raise SystemExit("UNVERIFIED")
    result = _append(record)
    escalation = escalation_check()
    if escalation.get("message"):
        return escalation
    return result


def _tracker_rows(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [row for row in rows if "symptom" in row]


def day_number(current: Optional[date] = None) -> int:
    return ((current or today()) - START_DATE).days + 1


def report_due(current: Optional[date] = None) -> bool:
    return day_number(current) in {7, 14}


def _avg(values: List[Any]) -> str:
    nums = [float(v) for v in values if v is not None]
    if not nums:
        return "UNVERIFIED"
    return f"{statistics.mean(nums):.1f}"


def report(current: Optional[date] = None, *, path: Optional[Path] = None) -> Dict[str, Any]:
    day = day_number(current)
    if day not in {7, 14}:
        return {"ok": True, "action": "skip", "day": day}

    rows = sorted(_tracker_rows(_records(path or LOG_PATH)), key=lambda row: row.get("date", ""))[-7:]
    if len(rows) < 7:
        avg_hr = avg_sleep = avg_symptom = "UNVERIFIED"
        alcohol_free = aerobic = social = "UNVERIFIED"
    else:
        avg_hr = _avg([row.get("hr_waking") for row in rows])
        avg_sleep = _avg([row.get("hours_slept") for row in rows])
        avg_symptom = _avg([row.get("symptom") for row in rows])
        alcohol_free = str(sum(1 for row in rows if row.get("alcohol") is False))
        aerobic = str(sum(1 for row in rows if row.get("aerobic") is True))
        social = str(sum(1 for row in rows if row.get("social") is True))

    outstanding = bookings()
    booked = len(DEFAULT_BOOKINGS) - len(outstanding)
    lines = [
        "7-day averages",
        f"  Resting HR      {avg_hr} bpm",
        f"  Hours slept     {avg_sleep}",
        f"  Symptom score   {avg_symptom}",
        "",
        "Counts (of 7)",
        f"  Alcohol-free    {alcohol_free}",
        f"  Aerobic         {aerobic}",
        f"  Social          {social}",
        "",
        f"Bookings          {booked} of 4 booked",
    ]
    if day == 14:
        lines.extend(
            [
                "",
                "1. How many of 14 days hit all four non-negotiables?",
                "2. What did resting HR do?",
                "3. Did bad days get shorter?",
            ]
        )
    return {"ok": True, "action": "send", "day": day, "message": "\n".join(lines)}


def escalation_check(path: Path = LOG_PATH) -> Dict[str, Any]:
    rows = sorted(_tracker_rows(_records(path)), key=lambda row: row.get("date", ""))[-3:]
    if len(rows) == 3 and all(int(row.get("symptom", -1)) >= 8 for row in rows):
        return {"ok": True, "message": "Three days at 8+. Call your prescriber."}
    return {"ok": True, "message": ""}


def main() -> None:
    parser = argparse.ArgumentParser(description="14-day protocol ops helper")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("morning")
    sub.add_parser("tracker")
    sub.add_parser("report")
    morning_log = sub.add_parser("log-morning-hr")
    morning_log.add_argument("raw")
    tracker_log = sub.add_parser("log-tracker")
    tracker_log.add_argument("values", nargs="+")
    sub.add_parser("escalation-check")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.cmd == "morning":
        result = morning_message()
    elif args.cmd == "tracker":
        result = tracker_message()
    elif args.cmd == "report":
        result = report()
    elif args.cmd == "log-morning-hr":
        result = log_morning_hr(args.raw)
    elif args.cmd == "log-tracker":
        result = log_tracker(args.values)
    else:
        result = escalation_check()

    if args.json:
        print(json.dumps(result, sort_keys=True))
    elif result.get("message"):
        print(result["message"])
    else:
        print(result.get("status") or result.get("action") or "OK")


if __name__ == "__main__":
    main()
