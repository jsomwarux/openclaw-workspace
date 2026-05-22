#!/usr/bin/env python3
"""Guardrails for JT's content + sports distribution outputs.

This is intentionally lightweight: it checks the artifacts that autonomous
content jobs already save, without posting, uploading, or calling external APIs.
Use it as a pre-delivery smoke test for weekly content, @dynastyjig packs,
news hooks, and Notion calendar script hygiene.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BAD_PLACEHOLDERS = [
    "[placeholder]",
    "[needs current signal]",
    "[source]",
    "lorem ipsum",
    "todo:",
]

LINKEDIN_STALE_PATTERNS = [
    (
        re.compile(r"\b(?:the\s+)?(?:biggest|real|main)\s+blocker\s+(?:to\s+[^.\n]{0,120}\s+)?(?:is|was)\s+not\s+(?:whether|if)\b", re.I),
        "contrarian blocker reveal: 'the blocker is not whether X...'",
    ),
    (
        re.compile(r"\b(?:it|this|that)\s+(?:is|was|isn['’]t|wasn['’]t)\s+not\s+[^.\n]{0,120}\b(?:it\s+is|it['’]s|but|more\s+like)\b", re.I),
        "contrarian reveal: 'it is not X, it is Y'",
    ),
    (
        re.compile(r"\b(?:a|an|the|this|that|your|my|our|[A-Z][A-Za-z0-9'’/-]{1,40})\s+[^.\n]{0,80}\s+(?:is|are|was|were)\s+not\s+just\s+[^.\n]{1,120}\.\s*(?:it|this|that|they|those|these|he|she)\s+(?:is|are|was|were)\s+[^.\n]{1,120}\.", re.I),
        "banned Not-Y-X variant: 'X is not just Y. It is Z.'",
    ),
    (
        re.compile(r"\bnot\s+[\"'“”‘’]?look\s+what\s+[^.\n]{0,120}\b(?:more\s+like|it\s+is|it['’]s|but)\b", re.I),
        "stale demo contrast: 'not look what this tool can do...'",
    ),
    (
        re.compile(r"\bmore\s+like\s*[:\"'“”‘’]", re.I),
        "stale reveal phrase: 'more like...'",
    ),
    (
        re.compile(r"\b(?:matters\s+more\s+than\s+people\s+(?:think|realize)|people\s+underestimate|that\s+part\s+matters)\b", re.I),
        "generic importance phrase",
    ),
    (
        re.compile(r"\bNo\s+[^.\n]{1,80}\.\s*No\s+[^.\n]{1,80}\.\s*Just\s+[^.\n]{1,80}\.", re.I),
        "tricolon negation: 'No X. No Y. Just Z.'",
    ),
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

POSTED_LOG = ROOT / "memory" / "content" / "posted-log.jsonl"
COOLDOWN_DAYS = 45

TOPIC_CLUSTERS = {
    "agentforce-boundary-escalation": [
        "agentforce",
        "allowed to decide",
        "where the agent stops",
        "knows when not to",
        "unofficial rules",
        "topic boundaries",
        "escalation rules",
        "handoff conditions",
        "stopping point",
        "refuses the right work",
    ],
    "agentforce-activation-not-implementation": [
        "agentforce",
        "activation",
        "not implementation",
        "800m arr",
        "feature is not adoption",
    ],
    "streeteasy-scraper": [
        "streeteasy",
        "runs every 14 days",
        "manual search work",
        "matching listings",
    ],
}


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


def check_linkedin_stale_patterns(path: Path, text: str) -> list[str]:
    problems: list[str] = []
    for pattern, label in LINKEDIN_STALE_PATTERNS:
        for match in pattern.finditer(text):
            excerpt = " ".join(match.group(0).split())[:160]
            problems.append(f"{rel(path)}: LinkedIn stale pattern: {label} -> {excerpt!r}")
    return problems



def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except Exception:
        return None


def load_recent_log(days: int = COOLDOWN_DAYS) -> list[dict]:
    rows: list[dict] = []
    if not POSTED_LOG.exists():
        return rows
    cutoff = date.today() - timedelta(days=days)
    for line in POSTED_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        d = parse_date(row.get("date") or row.get("posted_date"))
        if d and d >= cutoff:
            rows.append(row)
    return rows


def cluster_hits(text: str) -> dict[str, int]:
    lower = text.lower()
    return {name: sum(1 for term in terms if term in lower) for name, terms in TOPIC_CLUSTERS.items()}


def iter_weekly_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^##+\s+", text, flags=re.M))
    if not matches:
        return [("full file", text)]
    sections: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk = text[m.start():end]
        heading = chunk.splitlines()[0].strip("# ").strip()
        sections.append((heading, chunk))
    return sections


def section_is_past(chunk: str) -> bool:
    # Delivery guard runs daily against the weekly file. Do not let already-passed
    # slots block today's delivery, but future/current sections still get checked.
    m = re.search(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", chunk)
    if not m:
        return False
    d = parse_date(m.group(1))
    return bool(d and d < date.today())


def check_topic_cooldown(path: Path, text: str) -> list[str]:
    problems: list[str] = []
    recent_rows = load_recent_log()
    for heading, chunk in iter_weekly_sections(text):
        if section_is_past(chunk):
            continue
        current = cluster_hits(chunk)
        for cluster, score in current.items():
            # 3+ markers means the actual draft is using the cluster, not merely naming it in metadata.
            if score < 3:
                continue
            terms = TOPIC_CLUSTERS[cluster]
            for row in recent_rows:
                if str(row.get("platform", "")).lower() != "linkedin":
                    continue
                blob = " ".join(str(row.get(k, "")) for k in ["topic", "pillar", "summary", "title", "day"]).lower()
                if cluster.replace("-", " ") in blob or sum(1 for term in terms if term in blob) >= 1:
                    problems.append(
                        f"{rel(path)}: topic cooldown breach in {heading} for {cluster}; recent log row {row.get('date')} {row.get('topic') or row.get('title')}"
                    )
                    break
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
    problems.extend(check_linkedin_stale_patterns(path, text))
    for heading in WEEKLY_REQUIRED:
        if heading not in text:
            problems.append(f"{rel(path)}: missing weekly gate section: {heading}")
    if "Wednesday Advisory Board" not in text and "Wednesday - Case Study" in text:
        problems.append(f"{rel(path)}: Wednesday case study lacks advisory board")
    if "None - generated from automated sources" in text and "Warning" not in text:
        problems.append(f"{rel(path)}: seedless weekly file lacks explicit warning")
    problems.extend(check_topic_cooldown(path, text))
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
    parser.add_argument("--linkedin-draft", action="append", default=[], help="Path to LinkedIn draft markdown/text to scan for stale AI-copy patterns")
    parser.add_argument("--news-hook", action="append", default=[], help="Path to daily news hook markdown")
    parser.add_argument("--check-notion-script", action="store_true", help="Check scripts/notion-calendar-push.py auth/dry-run hygiene")
    args = parser.parse_args()

    problems: list[str] = []
    for item in args.dynasty_pack:
        problems.extend(check_dynasty_pack(Path(item)))
    for item in args.weekly:
        problems.extend(check_weekly(Path(item)))
    for item in args.linkedin_draft:
        path = Path(item)
        text = read(path)
        problems.extend(check_common(path, text))
        problems.extend(check_linkedin_stale_patterns(path, text))
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
