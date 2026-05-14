#!/usr/bin/env python3
"""Guardrails for JT's content + sports distribution outputs.

This is intentionally lightweight: it checks the artifacts that autonomous
content jobs already save, without posting, uploading, or calling external APIs.
Use it as a pre-delivery smoke test for weekly content, @dynastyjig packs,
news hooks, and Notion calendar script hygiene.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BAD_PLACEHOLDERS = [
    "[placeholder]",
    "[needs current signal]",
    "[source]",
    "lorem ipsum",
    "todo:",
]

DYNASTY_REQUIRED = [
    "Native pattern teardown",
    "Rejected generic patterns",
    "Quality gate applied",
    "Fresh signal used",
    "Recommendation",
]

WEEKLY_REQUIRED = [
    "Constraint log",
    "Hook mappings",
]


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check_common(path: Path, text: str) -> list[str]:
    problems: list[str] = []
    lower = text.lower()
    for marker in BAD_PLACEHOLDERS:
        if marker in lower:
            problems.append(f"{rel(path)}: placeholder/stale marker present: {marker}")
    if "—" in text:
        problems.append(f"{rel(path)}: em dash present")
    if re.search(r"\b(game-changing|revolutionary|unlock the power|seamless)\b", text, re.I):
        problems.append(f"{rel(path)}: generic marketing phrase present")
    return problems


def check_dynasty_pack(path: Path) -> list[str]:
    text = read(path)
    problems = check_common(path, text)
    for heading in DYNASTY_REQUIRED:
        if heading not in text:
            problems.append(f"{rel(path)}: missing dynasty gate section: {heading}")
    if re.search(r"\b(Action Arena|Dynasty Simulator|download|sign up)\b", text) and "Angle:" not in text:
        problems.append(f"{rel(path)}: possible product promo in public draft")
    if "BLOCKED:" in text and "Draft:" in text:
        problems.append(f"{rel(path)}: blocked pack still contains drafts")
    return problems


def check_weekly(path: Path) -> list[str]:
    text = read(path)
    problems = check_common(path, text)
    for heading in WEEKLY_REQUIRED:
        if heading not in text:
            problems.append(f"{rel(path)}: missing weekly gate section: {heading}")
    if "Wednesday Advisory Board" not in text and "Wednesday - Case Study" in text:
        problems.append(f"{rel(path)}: Wednesday case study lacks advisory board")
    if "None - generated from automated sources" in text and "Warning" not in text:
        problems.append(f"{rel(path)}: seedless weekly file lacks explicit warning")
    return problems


def check_news_hook(path: Path) -> list[str]:
    text = read(path)
    problems = check_common(path, text)
    if "SKIP" in text and len(text.strip()) > 500:
        problems.append(f"{rel(path)}: skip note is too long; likely mixed with draft content")
    if "SKIP" not in text and not re.search(r"Tweet 1|Draft|READY", text, re.I):
        problems.append(f"{rel(path)}: neither skip note nor draft marker found")
    return problems


def check_notion_script(path: Path) -> list[str]:
    text = read(path)
    problems: list[str] = []
    if "os.getenv(\"NOTION_TOKEN\")" not in text and "os.environ.get(\"NOTION_TOKEN\")" not in text:
        problems.append(f"{rel(path)}: NOTION_TOKEN is not env-only")
    if re.search(r"ntn_[A-Za-z0-9_\-]{20,}", text):
        problems.append(f"{rel(path)}: hardcoded Notion token pattern found")
    if "--dry-run" not in text:
        problems.append(f"{rel(path)}: missing --dry-run support")
    if "SKIP duplicate in batch" not in text:
        problems.append(f"{rel(path)}: missing batch duplicate guard")
    if "existing_calendar_entries" not in text or "SKIP existing Notion slot" not in text:
        problems.append(f"{rel(path)}: missing existing Notion slot guard")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate content distribution artifacts without external writes.")
    parser.add_argument("--dynasty-pack", action="append", default=[], help="Path to @dynastyjig pack markdown")
    parser.add_argument("--weekly", action="append", default=[], help="Path to weekly content markdown")
    parser.add_argument("--news-hook", action="append", default=[], help="Path to daily news hook markdown")
    parser.add_argument("--check-notion-script", action="store_true", help="Check scripts/notion-calendar-push.py auth/dry-run hygiene")
    args = parser.parse_args()

    problems: list[str] = []
    for item in args.dynasty_pack:
        problems.extend(check_dynasty_pack(Path(item)))
    for item in args.weekly:
        problems.extend(check_weekly(Path(item)))
    for item in args.news_hook:
        problems.extend(check_news_hook(Path(item)))
    if args.check_notion_script:
        problems.extend(check_notion_script(ROOT / "scripts" / "notion-calendar-push.py"))

    if problems:
        print("CONTENT_DISTRIBUTION_GUARD_FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("CONTENT_DISTRIBUTION_GUARD_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
