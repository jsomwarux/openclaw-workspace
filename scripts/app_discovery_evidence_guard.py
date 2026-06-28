#!/usr/bin/env python3
"""Validate app-discovery evidence claims in Markdown artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_HEADERS = {"claim", "source_url_or_path", "source_snippet", "confidence"}
PLACEHOLDERS = {"", "todo", "tbd", "[todo]", "[source]", "[snippet]", "placeholder"}


def normalize_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("**") and value.endswith("**") and len(value) > 4:
        value = value[2:-2].strip()
    return value.replace("`", "").strip()


def split_row(line: str) -> list[str]:
    return [normalize_cell(cell) for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_claim_tables(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    tables: list[dict[str, object]] = []
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        next_line = lines[i + 1].strip()
        if not (line.startswith("|") and next_line.startswith("|")):
            i += 1
            continue

        headers = [header.lower() for header in split_row(line)]
        separator = split_row(next_line)
        if not REQUIRED_HEADERS.issubset(set(headers)) or not is_separator(separator):
            i += 1
            continue

        rows: list[dict[str, str]] = []
        i += 2
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = split_row(lines[i])
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))
            rows.append(dict(zip(headers, cells)))
            i += 1
        tables.append({"headers": headers, "rows": rows})
    return tables


def is_blank_or_placeholder(value: str) -> bool:
    return normalize_cell(value).strip().lower() in PLACEHOLDERS


def row_is_unverified(row: dict[str, str]) -> bool:
    fields = [
        row.get("status", ""),
        row.get("confidence", ""),
        row.get("source_url_or_path", ""),
    ]
    return any(normalize_cell(field).upper() == "UNVERIFIED" for field in fields)


def row_is_blank(row: dict[str, str]) -> bool:
    return all(is_blank_or_placeholder(value) for value in row.values())


def check_row(path: Path, row: dict[str, str], row_number: int) -> list[str]:
    problems: list[str] = []
    prefix = f"{path}: claim row {row_number}"

    if is_blank_or_placeholder(row.get("claim", "")):
        problems.append(f"{prefix}: missing claim")

    if row_is_unverified(row):
        reason = row.get("unverified_reason", "") or row.get("reason", "")
        if is_blank_or_placeholder(reason):
            problems.append(f"{prefix}: UNVERIFIED claim missing unverified_reason")
        return problems

    for field in ("source_url_or_path", "source_snippet", "confidence"):
        if is_blank_or_placeholder(row.get(field, "")):
            problems.append(f"{prefix}: missing {field}")
    return problems


def check_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    tables = parse_claim_tables(text)
    problems: list[str] = []
    claims_checked = 0

    for table in tables:
        rows = table["rows"]
        for index, row in enumerate(rows, start=1):
            if row_is_blank(row):
                continue
            claims_checked += 1
            problems.extend(check_row(path, row, index))

    return {
        "path": str(path),
        "claim_tables": len(tables),
        "claims_checked": claims_checked,
        "problems": problems,
    }


def check_files(paths: list[Path]) -> dict[str, object]:
    file_results = [check_file(path) for path in paths]
    problems = [problem for result in file_results for problem in result["problems"]]
    return {
        "ok": not problems,
        "files_checked": len(file_results),
        "claim_tables": sum(int(result["claim_tables"]) for result in file_results),
        "claims_checked": sum(int(result["claims_checked"]) for result in file_results),
        "problems": problems,
        "files": file_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Markdown artifacts to validate")
    args = parser.parse_args()

    paths = [Path(path) for path in args.paths]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        result = {
            "ok": False,
            "files_checked": 0,
            "claim_tables": 0,
            "claims_checked": 0,
            "problems": [f"missing file: {path}" for path in missing],
            "files": [],
        }
    else:
        result = check_files(paths)

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
