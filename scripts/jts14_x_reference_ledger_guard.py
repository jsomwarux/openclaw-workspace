#!/usr/bin/env python3
"""Validate @jts_14 X reference ledgers.

This catches the failure mode where X research exists but is scattered across
weekly queues, raw JSON, and swipe reports without a clear source-to-draft map.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_HEADERS = [
    "Source",
    "URL",
    "Lane",
    "Why selected",
    "Analyzed",
    "Influence type",
    "Applied to",
]
VALID_INFLUENCE = {
    "Topic selection",
    "Structure",
    "Credibility/proof",
    "Niche signal only",
    "Rejected",
    "Constraint",
}
FORBIDDEN_CROSS_NICHE = [
    "Dynasty Fantasy / Sports GM",
    "betting",
    "parlay",
    "prop bet",
    "player prop",
]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_tables(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = split_cells(line)
        if REQUIRED_HEADERS[0] not in cells:
            continue
        headers = cells
        if idx + 1 >= len(lines) or not re.match(r"^\s*\|?\s*:?-{3,}", lines[idx + 1]):
            continue
        for row_line in lines[idx + 2 :]:
            if not row_line.strip().startswith("|"):
                break
            row_cells = split_cells(row_line)
            if len(row_cells) != len(headers):
                continue
            rows.append(dict(zip(headers, row_cells)))
    return rows


def influence_values(raw: str) -> set[str]:
    return {part.strip() for part in re.split(r"\s*\+\s*|\s*,\s*", raw) if part.strip()}


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    problems: list[str] = []

    for header in REQUIRED_HEADERS:
        if header.lower() not in lower:
            problems.append(f"{rel(path)}: missing required ledger field {header!r}")

    rows = parse_tables(text)
    applied_rows = [row for row in rows if "Applied to" in row]
    if len(applied_rows) < 8:
        problems.append(f"{rel(path)}: only {len(applied_rows)} rows; need at least 8 for a weekly @jts_14 ledger")

    for index, row in enumerate(applied_rows, start=1):
        for field in REQUIRED_HEADERS:
            if not row.get(field, "").strip():
                problems.append(f"{rel(path)}: row {index} has empty {field!r}")
        url = row.get("URL", "")
        if not re.search(r"https://(?:x\.com|twitter\.com)/|saved in `", url):
            problems.append(f"{rel(path)}: row {index} URL is not an X URL or saved-artifact pointer")
        influences = influence_values(row.get("Influence type", ""))
        unknown = influences - VALID_INFLUENCE
        if unknown:
            problems.append(f"{rel(path)}: row {index} has unknown influence type(s): {', '.join(sorted(unknown))}")
        applied_to = row.get("Applied to", "").lower()
        if "Niche signal only" in influences and not any(marker in applied_to for marker in ["not", "future", "validated", "reinforced", "support"]):
            problems.append(f"{rel(path)}: row {index} marks niche signal only but overclaims application")

    for phrase in FORBIDDEN_CROSS_NICHE:
        if phrase.lower() in lower:
            problems.append(f"{rel(path)}: contains cross-niche/dynasty-betting reference {phrase!r}")

    if "topic selection" not in lower or "structure" not in lower or "rejected" not in lower:
        problems.append(f"{rel(path)}: must explicitly separate topic selection, structure, and rejected sources")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate @jts_14 X reference ledger files.")
    parser.add_argument("ledger", nargs="+", help="Ledger markdown path(s)")
    args = parser.parse_args()

    problems: list[str] = []
    for item in args.ledger:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            problems.append(f"{rel(path)}: file does not exist")
            continue
        problems.extend(check(path))

    if problems:
        print("JTS14_X_REFERENCE_LEDGER_GUARD_FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("JTS14_X_REFERENCE_LEDGER_GUARD_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
