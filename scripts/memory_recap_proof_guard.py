#!/usr/bin/env python3
"""
Memory / recap / proof guard.

Read-only validation for continuity surfaces:
- bootstrap file budgets
- today's daily note exists and has substantive sections
- weekly recap header/currentness and stale carried-forward risk
- proof log recency and JSON validity
- recent builds freshness/size
- content proof points presence
- LCM recall guidance in MEMORY.md

Exit codes:
  0 = pass
  1 = warnings/failures found
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[1]
BUDGETS = {
    "AGENTS.md": 28_000,
    "MEMORY.md": 20_000,
    "TOOLS.md": 16_000,
    "HEARTBEAT.md": 16_000,
}
# Bootstrap budgets are hard caps, but this guard should not fail solely
# because a file is close to budget; it should fail when the layer is broken.
# Near-budget files are surfaced as notes so audits can still pass after safe
# compaction without forcing risky edits.
WARN_RATIO = 0.95
SUBSTANTIVE_DAILY_HEADING_RE = re.compile(
    r"^##\s+.*(audit|xhigh|build|built|ship|shipped|deploy|deployment|"
    r"portfolio|proof|content generation|app marketing|strategy jobs|mission control|"
    r"client|outreach|automation|cron wiring)",
    flags=re.I | re.M,
)
PUBLIC_PROOF_HINT_RE = re.compile(
    r"(production|live|public|commit|pushed|build \+ lint|build/lint|sitemap|"
    r"llms\.txt|homepage|jtsomwaru\.com|vista|nash|streeteasy)",
    flags=re.I,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def file_age_days(path: Path, now: datetime) -> float | None:
    if not path.exists():
        return None
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return (now - mtime).total_seconds() / 86400


def parse_jsonl(path: Path) -> tuple[int, list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    entries: list[dict[str, Any]] = []
    count = 0
    if not path.exists():
        return count, ["missing"], entries
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        try:
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                entries.append(parsed)
            else:
                errors.append(f"line {lineno}: JSON value is not an object")
        except json.JSONDecodeError as exc:
            errors.append(f"line {lineno}: {exc}")
    return count, errors, entries


def normalize_title(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = value.replace("–", "-").replace("—", "-")
    value = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return re.sub(r"\s+", " ", value).strip()


def parse_recent_build_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    headings = list(re.finditer(r"^##\s+(.+)$", text, flags=re.M))
    for idx, match in enumerate(headings):
        block_start = match.start()
        block_end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
        block = text[block_start:block_end].strip()
        title_line = match.group(1).strip()
        if title_line.startswith("[") or title_line.lower() == "format":
            continue
        date_match = re.search(r"[—-]\s*(20\d\d-\d\d-\d\d)\s*$", title_line)
        clean_title = re.sub(r"\s+[—-]\s*20\d\d-\d\d-\d\d\s*$", "", title_line).strip()
        fields: dict[str, str] = {"title": clean_title, "raw_title": title_line, "date": date_match.group(1) if date_match else ""}
        for field in ["What", "For", "Outcome", "Demonstrates", "Content angle", "Status"]:
            field_match = re.search(rf"^[-\s]*\*\*{re.escape(field)}:\*\*\s*(.+)$", block, flags=re.M)
            fields[field.lower().replace(" ", "_")] = field_match.group(1).strip() if field_match else ""
        entries.append(fields)
    return entries


def parse_content_voice_proof_titles(text: str) -> set[str]:
    section_match = re.search(r"^##\s+Proof Points\s*$([\s\S]*?)(?:^##\s+|\Z)", text, flags=re.M)
    section = section_match.group(1) if section_match else ""
    titles: set[str] = set()
    for line in section.splitlines():
        if not line.strip().startswith("|") or re.match(r"^\|\s*-+", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].lower() != "date" and re.match(r"20\d\d-\d\d-\d\d", cells[0]):
            titles.add(normalize_title(cells[1]))
    # Backward-compatible with older bullet-style proof points while the table is being normalized.
    for bullet in re.findall(r"^-\s+\*\*(.+?)\s*\(20\d\d-\d\d-\d\d\):", section, flags=re.M):
        titles.add(normalize_title(bullet))
    return titles


def proof_worthy_recent_build(entry: dict[str, str], now: datetime) -> bool:
    date_value = entry.get("date", "")
    if not date_value:
        return False
    try:
        entry_date = datetime.fromisoformat(date_value).date()
    except ValueError:
        return False
    if (now.date() - entry_date).days > 30:
        return False
    status = entry.get("status", "").lower()
    if status and "complete" not in status and "live" not in status and "pushed" not in status:
        return False
    text = " | ".join([entry.get("title", ""), entry.get("for", ""), entry.get("outcome", ""), entry.get("status", "")])
    if "internal content system" in text.lower():
        return False
    return bool(PUBLIC_PROOF_HINT_RE.search(text))


def first_monday_of_week(now: datetime) -> str:
    local = now.astimezone()
    monday = local.date() - timedelta(days=local.weekday())
    return monday.isoformat()


def check(today: str | None = None) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    local_today = today or datetime.now().strftime("%Y-%m-%d")
    results: dict[str, Any] = {"ok": True, "warnings": [], "checks": {}}

    def warn(msg: str) -> None:
        results["ok"] = False
        results["warnings"].append(msg)

    # Bootstrap budgets
    budget_rows = {}
    for rel, limit in BUDGETS.items():
        path = WORKSPACE / rel
        size = path.stat().st_size if path.exists() else None
        budget_rows[rel] = {"bytes": size, "limit": limit}
        if size is None:
            warn(f"missing bootstrap file: {rel}")
        elif size >= limit:
            warn(f"bootstrap over budget: {rel} {size}/{limit}")
        elif size >= int(limit * WARN_RATIO):
            budget_rows[rel]["near_budget"] = True
    results["checks"]["bootstrap_budgets"] = budget_rows

    # Daily note
    daily = WORKSPACE / "memory" / f"{local_today}.md"
    daily_info: dict[str, Any] = {"path": str(daily.relative_to(WORKSPACE)), "exists": daily.exists()}
    if not daily.exists():
        warn(f"today daily note missing: {daily.relative_to(WORKSPACE)}")
    else:
        daily_text = read_text(daily)
        headings = re.findall(r"^##\s+", daily_text, flags=re.M)
        substantive_sections = [m.group(0).replace("##", "").strip() for m in SUBSTANTIVE_DAILY_HEADING_RE.finditer(daily_text)]
        daily_info.update({
            "bytes": daily.stat().st_size,
            "section_count": len(headings),
            "has_heartbeat_or_ops": bool(re.search(r"^##\s+(Heartbeat|Session Cleanup|Overnight|XHigh|Strategy)", daily_text, flags=re.M)),
            "substantive_sections_requiring_proof": substantive_sections,
        })
        if daily.stat().st_size < 200 or len(headings) == 0:
            warn(f"today daily note looks too thin: {daily.relative_to(WORKSPACE)}")
    results["checks"]["daily_note"] = daily_info

    # Weekly recap
    weekly = WORKSPACE / "memory" / "weekly-recaps" / "current-week.md"
    weekly_info: dict[str, Any] = {"path": str(weekly.relative_to(WORKSPACE)), "exists": weekly.exists()}
    if not weekly.exists():
        warn("weekly recap missing: memory/weekly-recaps/current-week.md")
    else:
        weekly_text = read_text(weekly)
        first_line = weekly_text.splitlines()[0] if weekly_text.splitlines() else ""
        current_week = first_monday_of_week(now)
        old_date_lines = len(re.findall(r"^[-\s]*\[?2026-0[234]-", weekly_text, flags=re.M))
        weekly_info.update({
            "bytes": weekly.stat().st_size,
            "first_line": first_line,
            "expected_week_start": current_week,
            "age_days": round(file_age_days(weekly, now) or 0, 2),
            "older_carried_forward_lines": old_date_lines,
        })
        if current_week not in first_line:
            warn(f"weekly recap header not current-week: {first_line!r} expected {current_week}")
        if (file_age_days(weekly, now) or 999) > 7:
            warn("weekly recap has not been touched in >7 days")
        if old_date_lines > 25:
            warn(f"weekly recap contains {old_date_lines} older carried-forward dated lines; archive/compact to prevent stale recall")
    results["checks"]["weekly_recap"] = weekly_info

    # Proof logs
    proofs_dir = WORKSPACE / "proofs"
    proof_files = sorted(proofs_dir.glob("20*/actions.jsonl")) if proofs_dir.exists() else []
    proof_info: dict[str, Any] = {"proof_file_count": len(proof_files), "latest": None}
    if not proof_files:
        warn("no proof logs found")
    else:
        latest = max(proof_files, key=lambda p: p.stat().st_mtime)
        count, errors, entries = parse_jsonl(latest)
        proof_info["latest"] = {
            "path": str(latest.relative_to(WORKSPACE)),
            "entries": count,
            "age_days": round(file_age_days(latest, now) or 0, 2),
            "json_errors": errors,
            "entries_with_files": sum(1 for e in entries if e.get("files_affected")),
        }
        if errors:
            warn(f"latest proof log has JSON errors: {latest.relative_to(WORKSPACE)}")
        if count == 0:
            warn(f"latest proof log is empty: {latest.relative_to(WORKSPACE)}")
        if (file_age_days(latest, now) or 999) > 14:
            warn("no proof log updated in >14 days")
    results["checks"]["proof_logs"] = proof_info

    # Today's substantive daily-note sections should have a same-day proof log.
    today_proof = proofs_dir / local_today / "actions.jsonl"
    today_count, today_errors, today_entries = parse_jsonl(today_proof)
    substantive_sections = daily_info.get("substantive_sections_requiring_proof", []) if daily_info.get("exists") else []
    proof_required_info = {
        "date": local_today,
        "path": str(today_proof.relative_to(WORKSPACE)),
        "substantive_sections": substantive_sections,
        "proof_entries": today_count,
        "json_errors": today_errors,
        "entries_with_files": sum(1 for e in today_entries if e.get("files_affected")),
    }
    if substantive_sections and today_count == 0:
        warn(f"daily note has substantive sections but no same-day proof entries: {local_today}")
    if today_errors and today_errors != ["missing"]:
        warn(f"today proof log has JSON errors: {today_proof.relative_to(WORKSPACE)}")
    if substantive_sections and today_count > 0 and proof_required_info["entries_with_files"] == 0:
        warn("same-day proof entries exist but none list files_affected for substantive work")
    results["checks"]["same_day_proof_required"] = proof_required_info

    # Recent builds and proof points
    recent = WORKSPACE / "memory" / "content" / "recent-builds.md"
    recent_info: dict[str, Any] = {"exists": recent.exists()}
    if not recent.exists():
        warn("missing memory/content/recent-builds.md")
    else:
        recent_text = read_text(recent)
        headers = re.findall(r"^##\s+(.+)$", recent_text, flags=re.M)
        build_entries = parse_recent_build_entries(recent_text)
        recent_info.update({"bytes": recent.stat().st_size, "entry_headers": len(headers), "parsed_entries": len(build_entries), "age_days": round(file_age_days(recent, now) or 0, 2)})
        if recent.stat().st_size > 20_000:
            warn(f"recent-builds exceeds 20k target ({recent.stat().st_size} bytes); archive stale entries")
        if (file_age_days(recent, now) or 999) > 14:
            warn("recent-builds not updated in >14 days")
    results["checks"]["recent_builds"] = recent_info

    voice = WORKSPACE / "memory" / "content-voice.md"
    voice_info: dict[str, Any] = {"exists": voice.exists()}
    if not voice.exists():
        warn("missing memory/content-voice.md")
    else:
        voice_text = read_text(voice)
        proof_section = "## Proof Points" in voice_text
        proof_rows = len(re.findall(r"^\|\s*20\d\d-", voice_text, flags=re.M))
        proof_titles = parse_content_voice_proof_titles(voice_text)
        proof_worthy_builds = []
        missing_proof_points = []
        if recent.exists():
            for entry in parse_recent_build_entries(read_text(recent)):
                if proof_worthy_recent_build(entry, now):
                    proof_worthy_builds.append(entry["title"])
                    if normalize_title(entry["title"]) not in proof_titles:
                        missing_proof_points.append(entry["title"])
        voice_info.update({
            "has_proof_points_section": proof_section,
            "proof_point_rows": proof_rows,
            "proof_point_titles": len(proof_titles),
            "recent_proof_worthy_builds": proof_worthy_builds,
            "missing_recent_build_proof_points": missing_proof_points,
        })
        if not proof_section or proof_rows == 0:
            warn("content-voice proof points section missing or empty")
        if missing_proof_points:
            warn("recent-builds entries missing from content-voice Proof Points: " + "; ".join(missing_proof_points))
    results["checks"]["content_voice_proof_points"] = voice_info

    memory = WORKSPACE / "MEMORY.md"
    if memory.exists():
        memory_text = read_text(memory)
        lcm_ok = all(term in memory_text for term in ["lcm_grep", "lcm_describe", "lcm_expand_query"])
        fabrication_ok = "Never fabricate" in memory_text and "tool/script evidence" in memory_text
        results["checks"]["memory_recall_integrity"] = {"lcm_guidance": lcm_ok, "fabrication_guard": fabrication_ok}
        if not lcm_ok:
            warn("MEMORY.md missing complete LCM recall guidance")
        if not fabrication_ok:
            warn("MEMORY.md missing explicit fabrication/evidence guard")

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate memory/recap/proof continuity surfaces.")
    parser.add_argument("--date", help="Date to check daily note for (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()

    result = check(args.date)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        status = "PASS" if result["ok"] else "WARN"
        print(f"Memory/recap/proof guard: {status}")
        for warning in result["warnings"]:
            print(f"- {warning}")
        print(json.dumps(result["checks"], indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
