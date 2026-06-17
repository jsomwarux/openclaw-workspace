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
        re.compile(r"\b(?:the\s+)?(?P<noun>[A-Za-z][A-Za-z0-9'’/-]{1,40})\s+(?:is|are|was|were)\s+not\s+[^.\n]{1,160}\.\s*(?:the\s+)?(?P=noun)\s+(?:is|are|was|were|becomes|gets)\s+(?:that|when|where|how|[^.\n]{1,80})", re.I),
        "contrarian repeated-noun reveal: 'The risk is not X. The risk is Y.'",
    ),
    (
        re.compile(r"\b(?:it|this|that)\s+(?:is|are|was|were)\s+not\s+[^.\n]{1,160}\.\s*(?:it|this|that)\s+(?:is|are|was|were)\s+[^.\n]{1,160}", re.I),
        "contrarian pronoun reveal: 'That is not X. It is Y.'",
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
    (
        re.compile(r"\bthe\s+best\s+first\s+ai\s+project\s+is\s+usually\s+the\s+least\s+glamorous\s+one\b", re.I),
        "overused generic AI opener: 'best first AI project / least glamorous'",
    ),
    (
        re.compile(r"\bgets\s+risky\s+when\b[^.\n]{0,180}\blive\s+in\s+different\s+places\b", re.I),
        "repeated risk/place pattern: 'gets risky when...live in different places'",
    ),
    (
        re.compile(r"\bexception\s+layer\b", re.I),
        "overused implementation phrase: 'exception layer'",
    ),
    (
        re.compile(r"\bautonomous\s+content\s+systems?\b", re.I),
        "private operating-system reveal: autonomous content systems",
    ),
    (
        re.compile(r"\b(?:content\s+generator|publishing\s+system|content\s+system)\b[^.\n]{0,160}\b(?:current\s+efforts|posted\s+log|swipe\s+references|state\s+file|niche\s+map)\b", re.I),
        "private content-ops reveal: internal publishing machinery",
    ),
    (
        re.compile(r"\bhandoff\s+everyone\s+checks\s+manually\b", re.I),
        "overused generic AI motif: 'handoff everyone checks manually'",
    ),
    (
        re.compile(r"\b(?:content|publishing|post)\b[^.\n]{0,160}\b(?:state\s+file|stop\s+condition)\b", re.I),
        "private content-ops reveal: state file / stop condition",
    ),
    (
        re.compile(r"\b(?:public\s+proof|proof\s+layer|privacy\s+layer|site\s+proof|case-study\s+bait|private\s+client\s+details)\b", re.I),
        "low-value proof hygiene/process-meta angle: public proof/privacy cleanup",
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

WEEKLY_MIN_BYTES = 1500

REFERENCE_REQUIRED_FIELDS = [
    "source url",
    "niche",
    "format",
    "hook mechanic",
    "opening line mechanic",
    "proof mechanism",
    "emotional driver",
    "specificity level",
    "cta type",
    "why it worked",
    "jt translation",
]

CANONICAL_NICHE_LANES = {
    "SMB AI Implementation",
    "Property Management Operations",
    "NYC SMB Operations",
    "Wholesale Distribution Operations",
    "Construction + Skilled Trades Operations",
    "Insurance / Agentforce Operations",
    "AI Operating Systems / Agent Orchestration",
    "AI Enablement / Solutions Architecture Career",
    "Productized Services / Solo Operator Systems",
    "App Growth / App Marketing OS",
    "Vista / Movie Taste Apps",
    "Nash Satoshi / Crypto Ranking",
    "Glow Index / Skincare Ranking",
    "x402 / Agentic Payments",
    "Dynasty Fantasy / Sports GM",
    "Guyana Local Content Operations",
}

POSTED_LOG = ROOT / "memory" / "content" / "posted-log.jsonl"
AI_OPS_TEARDOWN_DIR = ROOT / "memory" / "content" / "bank"
COOLDOWN_DAYS = 45

GENERIC_TEARDOWN_TITLE_WORDS = {
    "AI",
    "Ops",
    "Teardown",
    "Property",
    "Insurance",
    "Expiration",
    "Rent",
    "Delinquency",
    "Readiness",
    "Construction",
    "Field",
    "Note",
    "Family",
    "Office",
    "Cash",
    "Timing",
    "Approval",
    "Queue",
    "Lease",
    "Renewal",
    "Deadline",
    "Wholesale",
    "Order",
    "Intake",
    "Desk",
}

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
    "exception-layer": [
        "exception layer",
        "messy cases",
        "ownership rules",
        "gets approved",
        "gets escalated",
        "stuck orders",
    ],
    "generic-first-ai-project": [
        "best first ai project",
        "least glamorous",
        "handoff everyone checks manually",
        "operating loop",
        "business can trust",
    ],
    "private-content-ops": [
        "autonomous content system",
        "content generator",
        "publishing system",
        "posted log",
        "swipe references",
        "niche map",
        "current efforts",
    ],
    "proof-hygiene-process-meta": [
        "public proof",
        "privacy layer",
        "site proof",
        "case-study bait",
        "private client details",
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


def path_date(path: Path) -> date | None:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", str(path))
    return parse_date(match.group(1)) if match else None


def current_teardown_slug_words(path: Path) -> set[str]:
    name = path.stem
    name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)
    name = re.sub(r"^ai-ops-teardown-", "", name)
    return {part.lower() for part in re.split(r"[^A-Za-z0-9]+", name) if len(part) >= 3}


def extract_prior_teardown_company_names(current_path: Path) -> set[str]:
    """Find named companies from earlier AI Ops Teardowns.

    Previous teardown companies are exclusion-only context. Generic workflow
    titles such as "Property Lease Renewal" are intentionally ignored.
    """
    current_date = path_date(current_path)
    current_slug_words = current_teardown_slug_words(current_path)
    names: set[str] = set()

    for prior_path in AI_OPS_TEARDOWN_DIR.glob("*/ai-ops-teardown-*.md"):
        if prior_path.resolve() == current_path.resolve():
            continue
        prior_date = path_date(prior_path)
        if current_date and prior_date and prior_date >= current_date:
            continue
        try:
            prior_text = read(prior_path)
        except FileNotFoundError:
            continue

        candidates: set[str] = set()
        heading = prior_text.splitlines()[0] if prior_text.splitlines() else ""
        heading_match = re.search(r"^#\s+AI Ops Teardown\s*[-–]\s+([A-Z][A-Za-z0-9&.'-]+)", heading)
        if heading_match:
            candidates.add(heading_match.group(1))
        for signal_match in re.finditer(r"\bCurrent signal:\s*([A-Z][A-Za-z0-9&.'-]+)\b", prior_text):
            candidates.add(signal_match.group(1))

        for candidate in candidates:
            clean = candidate.strip(" .,:;()[]{}")
            if not clean or clean in GENERIC_TEARDOWN_TITLE_WORDS:
                continue
            if clean.lower() in current_slug_words:
                continue
            names.add(clean)
    return names


def check_ai_ops_teardown_prior_company_references(path: Path, text: str) -> list[str]:
    if "ai-ops-teardown" not in path.name and "AI Ops Teardown" not in text:
        return []

    problems: list[str] = []
    for company in sorted(extract_prior_teardown_company_names(path), key=str.lower):
        pattern = re.compile(rf"\b{re.escape(company)}\b", re.I)
        for match in pattern.finditer(text):
            excerpt = " ".join(text[max(0, match.start() - 80): match.end() + 80].split())[:180]
            problems.append(
                f"{rel(path)}: prior AI Ops Teardown company mentioned: {company} -> {excerpt!r}"
            )
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
    if not path.exists():
        return [f"{rel(path)}: weekly artifact missing"]
    text = path.read_text(encoding="utf-8")
    problems = check_common(path, text)
    if len(text.encode("utf-8")) < WEEKLY_MIN_BYTES:
        problems.append(f"{rel(path)}: weekly artifact too small to be a deliverable ({len(text.encode('utf-8'))} bytes)")
    problems.extend(check_linkedin_stale_patterns(path, text))
    problems.extend(check_ai_ops_teardown_prior_company_references(path, text))
    for heading in WEEKLY_REQUIRED:
        if heading not in text:
            problems.append(f"{rel(path)}: missing weekly gate section: {heading}")
    if not re.search(r"^##\s+LinkedIn\b", text, flags=re.I | re.M):
        problems.append(f"{rel(path)}: missing LinkedIn section")
    if not re.search(r"^##\s+X\b", text, flags=re.I | re.M):
        problems.append(f"{rel(path)}: missing X section")
    if not re.search(r"^###+\s+Monday\b", text, flags=re.I | re.M):
        problems.append(f"{rel(path)}: missing Monday post section")
    if "Wednesday Advisory Board" not in text and "Wednesday - Case Study" in text:
        problems.append(f"{rel(path)}: Wednesday case study lacks advisory board")
    if "None - generated from automated sources" in text and "Warning" not in text:
        problems.append(f"{rel(path)}: seedless weekly file lacks explicit warning")
    problems.extend(check_topic_cooldown(path, text))
    return problems


def extract_reference_section(text: str, platform: str) -> str:
    """Return the reference-mechanics section for a platform, if present."""
    platform_re = re.escape(platform)
    patterns = [
        rf"^##+\s+{platform_re}\s+Reference Mechanics\b",
        rf"^##+\s+Reference Mechanics\s*[-:]\s*{platform_re}\b",
        rf"^##+\s+Reference Mechanics\b.*\b{platform_re}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.M)
        if not match:
            continue
        next_heading = re.search(r"^##+\s+", text[match.end():], flags=re.M)
        end = match.end() + next_heading.start() if next_heading else len(text)
        return text[match.start():end]
    return ""


def check_reference_map(path: Path, platform: str) -> list[str]:
    """Ensure saved drafts show platform/niche-specific reference mechanics.

    This is intentionally opt-in so older weekly files do not break daily
    delivery. Generation crons should call it before declaring new queues ready.
    """
    text = read(path)
    section = extract_reference_section(text, platform)
    label = platform.lower()
    if not section:
        return [f"{rel(path)}: missing {label} reference mechanics section"]

    lower = section.lower()
    problems: list[str] = []
    missing = [field for field in REFERENCE_REQUIRED_FIELDS if field not in lower]
    if missing:
        problems.append(f"{rel(path)}: {label} reference mechanics missing fields: {', '.join(missing)}")

    source_count = len(re.findall(r"source\s+url\s*:", section, flags=re.I))
    gap_marked = "recent_swipe_gap" in lower or "adjacent_reference_only" in lower
    if source_count < 2 and not gap_marked:
        problems.append(
            f"{rel(path)}: {label} reference mechanics has {source_count} Source URL rows; need at least 2 or explicit RECENT_SWIPE_GAP/ADJACENT_REFERENCE_ONLY"
        )

    if re.search(r"notion swipe references checked\b", lower) and source_count == 0:
        problems.append(f"{rel(path)}: {label} uses generic swipe assertion without source URLs")
    if "platform: " not in lower and "platform=" not in lower:
        problems.append(f"{rel(path)}: {label} reference mechanics does not name source platform")

    for raw_niche in extract_reference_niches(section):
        normalized = raw_niche.strip().strip("*` ")
        if not normalized:
            continue
        normalized_upper = normalized.upper()
        if normalized_upper in {"ADJACENT_REFERENCE_ONLY", "RECENT_SWIPE_GAP"}:
            continue
        if normalized not in CANONICAL_NICHE_LANES:
            problems.append(
                f"{rel(path)}: {label} reference mechanics uses non-canonical niche {normalized!r}; use memory/content/current-niche-map.md lanes or ADJACENT_REFERENCE_ONLY"
            )

    return problems


def check_required_jts14_ledger(weekly_path: Path, ledger_path: Path) -> list[str]:
    """Require a valid @jts_14 source-to-draft ledger for weekly X delivery."""
    problems: list[str] = []
    if not ledger_path.exists():
        return [f"{rel(weekly_path)}: jts14 X reference ledger missing: {rel(ledger_path)}"]

    try:
        import jts14_x_reference_ledger_guard
    except ImportError as exc:
        return [f"{rel(weekly_path)}: jts14 X reference ledger guard unavailable: {exc}"]

    ledger_problems = jts14_x_reference_ledger_guard.check(ledger_path)
    for problem in ledger_problems:
        problems.append(f"{rel(weekly_path)}: jts14 X reference ledger invalid: {problem}")
    return problems


def extract_reference_niches(section: str) -> list[str]:
    """Pull explicit Niche values from bullet or simple markdown-table rows."""
    niches: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if "niche" not in lower:
            continue
        if "source url" in lower or "why it worked" in lower:
            continue

        if stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            for idx, cell in enumerate(cells[:-1]):
                if cell.lower() == "niche":
                    niches.extend(split_niche_values(cells[idx + 1]))
            continue

        match = re.search(r"\bniche\s*[:=]\s*(.+)$", stripped, flags=re.I)
        if match:
            niches.extend(split_niche_values(match.group(1)))
    return niches


def split_niche_values(value: str) -> list[str]:
    value = re.sub(r"\s+#.*$", "", value).strip().strip("|")
    if not value:
        return []
    return [part.strip() for part in re.split(r"\s*(?:,|;|\band\b)\s*", value) if part.strip()]


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
    parser.add_argument(
        "--require-reference-map",
        action="append",
        default=[],
        choices=["linkedin", "x", "reddit", "tiktok"],
        help="Require a platform-specific Reference Mechanics section in each --weekly file.",
    )
    parser.add_argument(
        "--require-jts14-ledger",
        action="append",
        default=[],
        help="Require a valid @jts_14 X reference ledger path for each --weekly file.",
    )
    parser.add_argument("--check-notion-script", action="store_true", help="Check scripts/notion-calendar-push.py auth/dry-run hygiene")
    args = parser.parse_args()

    problems: list[str] = []
    if args.require_jts14_ledger and len(args.require_jts14_ledger) != len(args.weekly):
        problems.append(
            f"--require-jts14-ledger count ({len(args.require_jts14_ledger)}) must match --weekly count ({len(args.weekly)})"
        )

    for item in args.dynasty_pack:
        problems.extend(check_dynasty_pack(Path(item)))
    for index, item in enumerate(args.weekly):
        weekly_path = Path(item)
        problems.extend(check_weekly(weekly_path))
        for platform in args.require_reference_map:
            canonical = "X" if platform == "x" else platform.title()
            problems.extend(check_reference_map(weekly_path, canonical))
        if index < len(args.require_jts14_ledger):
            problems.extend(check_required_jts14_ledger(weekly_path, Path(args.require_jts14_ledger[index])))
    for item in args.linkedin_draft:
        path = Path(item)
        text = read(path)
        problems.extend(check_common(path, text))
        problems.extend(check_linkedin_stale_patterns(path, text))
        problems.extend(check_ai_ops_teardown_prior_company_references(path, text))
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
