#!/usr/bin/env python3
"""
vista-photo-selector.py
------------------------
Selects real photos for Vista TikTok slideshows.
Prioritizes real photos over NB2-generated scenes.
Enforces a 6-week rotation window (no repeats within 6 weeks).

Usage:
  python3 vista-photo-selector.py --count 2
  python3 vista-photo-selector.py --count 4 --vibe cozy,cinematic
  python3 vista-photo-selector.py --count 2 --mark-used --week 2026-04-07
  python3 vista-photo-selector.py --list   # show current availability

Arguments:
  --count N        How many photos to select (default: 2 for hook+CTA)
  --vibe VIBES     Comma-separated preferred vibes (optional: cozy, cinematic, relatable, aspirational, romance, nostalgic, moody, etc.)
  --mark-used      After selection, mark photos as used for --week
  --week DATE      ISO Monday date to mark as used (required with --mark-used)
  --list           Show all photos with availability status and exit

Outputs JSON to stdout:
  {
    "selected": [
      { "id": "photo-23", "file": "photo-23-shrek-projector-fireplace-cabin.jpg", "path": "/absolute/path/...", "vibe": "nostalgic", "energy": "peak-cozy" },
      ...
    ],
    "fallback_nb2": false,
    "available_count": 22,
    "total_count": 25
  }

If not enough real photos are available (all used within rotation window):
  "fallback_nb2": true  -- caller should generate NB2 scenes for missing slides
"""

import json
import argparse
import sys
import os
from datetime import datetime, date, timedelta

LIBRARY_PATH = os.path.join(os.path.dirname(__file__), "../agents/vibe-marketing/real-photos/nash-satoshi/library.json")
PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "../agents/vibe-marketing/real-photos/nash-satoshi/")


def load_library():
    with open(LIBRARY_PATH, "r") as f:
        return json.load(f)


def save_library(library):
    with open(LIBRARY_PATH, "w") as f:
        json.dump(library, f, indent=2)


def is_available(photo, rotation_window_weeks, today):
    """A photo is available if it has never been used, or was last used > rotation_window_weeks ago."""
    if photo["last_used_week"] is None:
        return True
    last_used = date.fromisoformat(photo["last_used_week"])
    cutoff = today - timedelta(weeks=rotation_window_weeks)
    return last_used <= cutoff


def select_photos(library, count, preferred_vibes=None):
    today = date.today()
    rotation_window = library["rotation_window_weeks"]
    photos = library["photos"]

    available = [p for p in photos if is_available(p, rotation_window, today)]

    if not available:
        # Full fallback — all photos used recently
        return [], True, 0

    # Sort: prefer never-used first, then by least recently used, then by use_count ascending
    def sort_key(p):
        if p["last_used_week"] is None:
            return (0, 0, p["use_count"])
        return (1, p["last_used_week"], p["use_count"])

    available_sorted = sorted(available, key=sort_key)

    # If vibes specified, try to weight toward preferred vibes
    selected = []
    if preferred_vibes:
        vibe_set = set(v.strip().lower() for v in preferred_vibes)
        preferred = [p for p in available_sorted if p["vibe"].lower() in vibe_set]
        others = [p for p in available_sorted if p["vibe"].lower() not in vibe_set]
        pool = preferred + others
    else:
        pool = available_sorted

    # Select `count` photos, no duplicates
    selected = pool[:count]

    fallback_nb2 = len(selected) < count
    return selected, fallback_nb2, len(available)


def mark_used(library, photo_ids, week_date):
    for photo in library["photos"]:
        if photo["id"] in photo_ids:
            photo["last_used_week"] = week_date
            photo["use_count"] += 1
    library["last_updated"] = date.today().isoformat()
    save_library(library)


def list_photos(library):
    today = date.today()
    rotation_window = library["rotation_window_weeks"]
    print(f"{'ID':<12} {'Vibe':<20} {'Last Used':<14} {'Uses':<6} {'Available'}")
    print("-" * 70)
    for p in library["photos"]:
        avail = is_available(p, rotation_window, today)
        last = p["last_used_week"] or "never"
        print(f"{p['id']:<12} {p['vibe']:<20} {last:<14} {p['use_count']:<6} {'✅' if avail else '❌'}")


def main():
    parser = argparse.ArgumentParser(description="Vista real photo selector for TikTok slideshows")
    parser.add_argument("--count", type=int, default=2, help="Number of photos to select")
    parser.add_argument("--vibe", type=str, default=None, help="Comma-separated preferred vibes")
    parser.add_argument("--mark-used", action="store_true", help="Mark selected photos as used")
    parser.add_argument("--week", type=str, default=None, help="ISO Monday date to mark as used (YYYY-MM-DD)")
    parser.add_argument("--list", action="store_true", help="List all photos with availability and exit")
    args = parser.parse_args()

    library = load_library()

    if args.list:
        list_photos(library)
        return

    preferred_vibes = args.vibe.split(",") if args.vibe else None
    selected, fallback_nb2, available_count = select_photos(library, args.count, preferred_vibes)

    result = {
        "selected": [
            {
                "id": p["id"],
                "file": p["file"],
                "path": os.path.abspath(os.path.join(PHOTOS_DIR, p["file"])),
                "vibe": p["vibe"],
                "energy": p["energy"],
                "setting": p["setting"],
                "last_used_week": p["last_used_week"],
                "use_count": p["use_count"]
            }
            for p in selected
        ],
        "fallback_nb2": fallback_nb2,
        "available_count": available_count,
        "total_count": len(library["photos"])
    }

    print(json.dumps(result, indent=2))

    if args.mark_used:
        if not args.week:
            print("ERROR: --week required with --mark-used", file=sys.stderr)
            sys.exit(1)
        photo_ids = [p["id"] for p in selected]
        mark_used(library, photo_ids, args.week)
        print(f"\n✅ Marked {len(photo_ids)} photos as used for week {args.week}", file=sys.stderr)


if __name__ == "__main__":
    main()
