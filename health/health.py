#!/usr/bin/env python3
"""
Eve's Health Tracking CLI

Usage:
  python3 health.py --log "7, neck, chicken + salad, 30min walk, 8"
  python3 health.py --log-interactive  # guided field-by-field
  python3 health.py --report           # weekly report
  python3 health.py --history [N]      # show last N check-ins (default 7)
  python3 health.py --date YYYY-MM-DD  # show a specific day
  python3 health.py --prompt           # print the check-in prompt template
"""
import sys
import os
import argparse
import json
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(__file__))
from db import init_db, save_checkin, get_recent_checkins, get_checkin, get_all_checkins
from parser import parse_checkin, format_checkin_for_confirm
from report import generate_weekly_report

CHECKIN_PROMPT = """🌙 *Evening Check-in*

Five questions — answer on one line or multiple:

1️⃣ *Activation* — how activated/tense does your nervous system feel right now? (1=fully calm, 10=maximum bracing)
2️⃣ *Bracing scan* — where are you unconsciously holding tension? (jaw / shoulders / glutes / belly / chest / none — all that apply)
3️⃣ *Exhale test* — take a breath now and exhale fully. How complete was it? (full / partial / blocked) + anything notable
4️⃣ *Protocol + movement* — did you do the reset protocol today? (yes / partial / no) + any exercise?
5️⃣ *Sleep* — how was last night? (1–10) + wake up tense or jaw clenching?

_Food note if anything notable (optional)_

_Example: "6, jaw + shoulders, partial, no protocol / 30min walk, 7 woke tense"_"""

PROTOCOL_REMINDER = """
📋 *5-min Reset (if not done today):*
1. Physiological sigh × 2 (double inhale → slow exhale)
2. Extended exhale breathing × 10 (4 in / 8 out)
3. Jaw release: teeth apart, tongue down, soften masseter × 30s
4. Ribcage expansion: breathe into lower ribs outward × 8 cycles
5. Pelvic neutral + shoulder drop lying down × 2 min
Full protocol: ~/.openclaw/workspace/health/protocol.md"""


def cmd_log(raw: str, checkin_date: str = None):
    """Parse and store a check-in from a raw string."""
    init_db()
    target_date = checkin_date or date.today().isoformat()
    parsed = parse_checkin(raw)

    row_id = save_checkin(
        checkin_date=target_date,
        energy=parsed["energy"],
        pain_areas=parsed["pain_areas"],
        food=parsed["food"],
        exercise=parsed["exercise"],
        sleep_quality=parsed["sleep_quality"],
        notes=parsed.get("notes"),
        raw_response=raw,
    )

    confirm = format_checkin_for_confirm(parsed, raw)
    print(confirm)
    return parsed, row_id


def cmd_report():
    """Generate and print the weekly report."""
    init_db()
    report = generate_weekly_report()
    print(report)
    return report


def cmd_history(n: int = 7):
    """Show last N check-ins."""
    init_db()
    checkins = get_recent_checkins(n)
    if not checkins:
        print("No check-ins logged yet.")
        return

    print(f"Last {len(checkins)} check-in(s):\n")
    for c in checkins:
        energy_bar = "●" * (c["energy"] or 0) + "○" * (10 - (c["energy"] or 0))
        sleep_bar  = "●" * (c["sleep_quality"] or 0) + "○" * (10 - (c["sleep_quality"] or 0))
        print(f"📅 {c['date']}")
        print(f"  ⚡ Energy:    {c['energy'] or '?'}/10  {energy_bar}")
        print(f"  😴 Sleep:     {c['sleep_quality'] or '?'}/10  {sleep_bar}")
        print(f"  🤕 Pain:      {c['pain_areas'] or '—'}")
        print(f"  🥗 Food:      {c['food'] or '—'}")
        print(f"  🏃 Exercise:  {c['exercise'] or '—'}")
        print()


def cmd_show_date(target_date: str):
    """Show a specific day's check-in."""
    init_db()
    c = get_checkin(target_date)
    if not c:
        print(f"No check-in for {target_date}.")
        return
    print(f"📅 {c['date']}")
    print(f"  Energy:    {c['energy']}/10")
    print(f"  Sleep:     {c['sleep_quality']}/10")
    print(f"  Pain:      {c['pain_areas'] or 'none'}")
    print(f"  Food:      {c['food'] or 'not logged'}")
    print(f"  Exercise:  {c['exercise'] or 'not logged'}")
    if c.get("notes"):
        print(f"  Notes:     {c['notes']}")
    print(f"\nRaw: {c.get('raw_response', '—')}")


def main():
    parser = argparse.ArgumentParser(description="Eve Health Tracker")
    parser.add_argument("--log",      metavar="RESPONSE", help="Log a check-in from raw text")
    parser.add_argument("--date",     metavar="YYYY-MM-DD", help="Target date for --log or --show")
    parser.add_argument("--report",   action="store_true", help="Generate weekly report")
    parser.add_argument("--history",  nargs="?", const=7, type=int, metavar="N",
                        help="Show last N check-ins (default 7)")
    parser.add_argument("--show",     metavar="YYYY-MM-DD", help="Show a specific date's check-in")
    parser.add_argument("--prompt",   action="store_true", help="Print the check-in prompt")
    parser.add_argument("--json",     action="store_true", help="Output as JSON (for --log)")
    args = parser.parse_args()

    if args.prompt:
        print(CHECKIN_PROMPT)

    elif args.log:
        parsed, row_id = cmd_log(args.log, args.date)
        if args.json:
            print(json.dumps({"id": row_id, **parsed}))

    elif args.report:
        cmd_report()

    elif args.history is not None:
        cmd_history(args.history)

    elif args.show:
        cmd_show_date(args.show)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
