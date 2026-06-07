#!/usr/bin/env python3
"""Score JT content drafts for voice, rhythm, and specificity.

This is a local pre-send guard. It does not decide taste perfectly, but it
catches the repeat failures JT has corrected: generic AI consultant hooks,
thin specificity, stale reveal framing, weak rhythm, and internal-process topics.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BANNED_PATTERNS = [
    (re.compile(r"\bwhat\s+most\s+people\s+miss\b", re.I), "borrowed-creator cliche: what most people miss"),
    (re.compile(r"\bmost\s+people\s+missed\s+it\b", re.I), "borrowed-creator cliche: most people missed it"),
    (re.compile(r"\bsomething\s+(?:shifted|changed)\b", re.I), "grand era-framing: name the concrete signal"),
    (re.compile(r"\bnew\s+era\s+(?:that\s+just\s+began|of\s+[^.\n]{1,80})\b", re.I), "grand era-framing: new era"),
    (re.compile(r"\bera\s+\d+\b", re.I), "grand era-framing: era numbering"),
    (re.compile(r"\bhere'?s\s+(?:the|my)\s+system\b", re.I), "borrowed-creator cliche: here's the system"),
    (re.compile(r"\bhere'?s\s+what\s+you\s+need\s+to\s+do\b", re.I), "borrowed-creator cliche: here's what you need to do"),
    (re.compile(r"\bhere'?s\s+(?:the\s+thing|why|what\s+I\s+find\s+interesting|the\s+problem\s+though)\b", re.I), "throat-clearing opener"),
    (re.compile(r"\bthe\s+results\?", re.I), "borrowed-creator cliche: the results?"),
    (re.compile(r"\b(?:let\s+me\s+be\s+clear|the\s+truth\s+is|I'?ll\s+say\s+it\s+again|I'?m\s+going\s+to\s+be\s+honest|can\s+we\s+talk\s+about)\b", re.I), "throat-clearing opener"),
    (re.compile(r"\b(?:full\s+stop|period|let\s+that\s+sink\s+in|make\s+no\s+mistake|here'?s\s+why\s+that\s+matters)\b", re.I), "performative emphasis"),
    (re.compile(r"\bthis\s+matters\s+because\b", re.I), "performative importance setup"),
    (re.compile(r"\byou'?re\s+a\s+moron\b", re.I), "insult hook"),
    (re.compile(r"\b(?:INSANE|EVERYTHING|DO NOT|PISSED)\b"), "hype caps / manic urgency"),
    (re.compile(r"\bunreal\s+opportunity\b", re.I), "generic opportunity hype"),
    (re.compile(r"\btake\s+action\s+before\s+someone\s+else\s+does\b", re.I), "generic urgency CTA"),
    (re.compile(r"\bgets\s+solved\s+with\s+a\s+hire\b", re.I), "JT-rejected phrase: gets solved with a hire"),
    (re.compile(r"\b\w+(?:\s+\w+){0,5}\s+don'?t\s+[^.\n,]{1,90},?\s+they\s+[^.\n]{1,120}", re.I), "JT-rejected contrast shape: X don't Y, they Z"),
    (re.compile(r"\b(?:the|one)\s+[^.\n:]{3,90}:\s+(?:what|why|how|where|when|who)\b", re.I), "JT-rejected statement-colon hook"),
    (re.compile(r"\bwould\s+you\s+trust\s+an?\s+AI\s+agent\s+with\b", re.I), "too-polished X trust-question hook"),
    (re.compile(r"\bi\s+would\s+trust\s+it\s+with\b", re.I), "too-polished X trust reveal"),
    (re.compile(r"\bis\s+probably\s+a\s+margin\s+leak\b", re.I), "too-polished X margin-leak hook"),
    (re.compile(r"\bthe\s+useful\s+question\s+is\s+uglier\b", re.I), "too-polished X useful-question pivot"),
    (re.compile(r"\bmake\s+stuck\s+work\s+visible\s+before\s+you\s+make\b", re.I), "too-polished X stuck-work line"),
    (re.compile(r"\bwhat\s+did\s+you\s+build\s+in\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\b", re.I), "too-polished X creator-flex CTA"),
    (re.compile(r"\bdifference\s+between\s+[^.\n]{1,120}\s+and\s+[^.\n]{1,120}\s+is\s+the\s+difference\s+between\s+automation\s+and\s+chaos\b", re.I), "too-polished X automation-chaos contrast"),
    (re.compile(r"\bthat'?s\s+not\s+automation\.\s+that'?s\s+leverage\b", re.I), "too-polished X leverage aphorism"),
    (re.compile(r"\bthe\s+better\s+move\s+is\s+building\s+a\s+loop\b", re.I), "too-polished X better-move aphorism"),
    (re.compile(r"\bthe\s+tools\s+exist\.\s+the\s+implementation\s+doesn'?t\b", re.I), "old template slogan: tools/implementation"),
    (re.compile(r"\bagents\s+handle\s+the\s+work\b", re.I), "old template slogan: agents handle the work"),
    (re.compile(r"\bbuild\s+the\s+process\.\s+buy\s+back\s+the\s+time\b", re.I), "old template slogan: build/buy back"),
    (re.compile(r"\bconsultants\s+charge\s+for\s+advice\b", re.I), "old template slogan: consultants charge for advice"),
    (re.compile(r"\bdemo\s+proves\s+it'?s\s+possible\.\s+deploy\s+proves\s+it'?s\s+real\b", re.I), "old template slogan: demo/deploy"),
    (re.compile(r"\bspecs\s+live\s+in\s+decks\.\s+systems\s+live\s+in\s+production\b", re.I), "old template slogan: specs/systems"),
    (re.compile(r"\bchatbots\s+answer\s+questions\.\s+agents\s+close\s+tickets\b", re.I), "old template slogan: chatbots/agents"),
    (re.compile(r"\bthe\s+implementation\s+is\s+always\s+the\s+bottleneck\b", re.I), "old template slogan: implementation bottleneck"),
    (re.compile(r"\bthe\s+best\s+(?:first\s+)?AI\s+project\s+is\b", re.I), "AI-slop best-project hook"),
    (re.compile(r"\b\w+(?:\s+\w+){0,4}\s+AI\s+gets\s+useful\s+at\b", re.I), "AI-slop gets-useful-at hook"),
    (re.compile(r"\bMost\s+(?:AI|SMB|business|businesses|projects)[^.\n]{0,80}\s+do\s+not\s+(?:fail|need)\s+because\b", re.I), "AI-slop most-X-do-not-fail-because hook"),
    (re.compile(r"\bMost\s+(?:SMBs|businesses|teams|operators)[^.\n]{0,100}\s+do\s+not\s+need\s+[^.\n]{1,120}\.\s+They\s+need\b", re.I), "AI-slop most-X-do-not-need-they-need hook"),
    (re.compile(r"\b(the\s+)?blocker\s+is\s+not\b", re.I), "stale blocker reveal"),
    (re.compile(r"\bnot\s+[^.\n]{1,80},?\s+(?:but|it'?s|it is)\b", re.I), "not-X-but-Y reveal"),
    (re.compile(r"\bnot\s+just\s+[^.\n]{1,120}\.\s*(?:it|this|that)\s+is\b", re.I), "not-just-X reveal"),
    (re.compile(r"\bNo\s+[^.\n]{1,80}\.\s*No\s+[^.\n]{1,80}\.\s*Just\s+", re.I), "tricolon negation"),
    (re.compile(r"\bmatters\s+more\s+than\s+people\s+(?:think|realize)\b", re.I), "generic importance phrase"),
    (re.compile(r"\bpeople\s+underestimate\b", re.I), "generic importance phrase"),
    (re.compile(r"\b(?:at\s+its\s+core|it\s+turns\s+out|the\s+real\s+[^.\n]{1,40}\s+is|when\s+it\s+comes\s+to|at\s+the\s+end\s+of\s+the\s+day|it'?s\s+worth\s+noting)\b", re.I), "generic filler phrase"),
    (re.compile(r"—"), "em dash"),
]

VERIFIED_OWNERSHIP_RE = re.compile(r"\b(?:built|shipped|created|launched|installed|deployed)\b", re.I)

PROOF_CONTEXT_MARKERS = [
    "built",
    "installed",
    "deployed",
    "client",
    "firm",
    "office",
    "local",
    "machine",
    "pc",
    "workflow",
    "workflows",
    "saved",
    "system",
    "systems",
]

FALSE_AGENCY_PATTERNS = [
    (re.compile(r"\bthe\s+data\s+(?:tells|shows|says)\s+(?:us\s+)?", re.I), "false agency: data does not speak"),
    (re.compile(r"\bthe\s+decision\s+(?:emerges|was\s+reached)\b", re.I), "false agency: name who decided"),
    (re.compile(r"\bthe\s+market\s+rewards\b", re.I), "false agency: name the buyer behavior"),
    (re.compile(r"\ba\s+complaint\s+becomes\s+a\s+fix\b", re.I), "false agency: name who fixed it"),
    (re.compile(r"\ba\s+bet\s+(?:lives|dies|lives\s+or\s+dies)\b", re.I), "false agency: name who ships or kills it"),
    (re.compile(r"\bthe\s+culture\s+shifts\b", re.I), "false agency: name who changed behavior"),
    (re.compile(r"\bthe\s+conversation\s+moves\s+toward\b", re.I), "false agency: name who steered it"),
    (re.compile(r"\bthe\s+workflow\s+(?:creates|builds)\s+trust\b", re.I), "false agency: name the control or reviewer that creates trust"),
]

NARRATOR_DISTANCE_PATTERNS = [
    (re.compile(r"\bpeople\s+tend\s+to\b", re.I), "narrator-from-distance: put the reader in the scene"),
    (re.compile(r"\bnobody\s+designed\s+this\b", re.I), "narrator-from-distance: name the operating path"),
    (re.compile(r"\bthis\s+happens\s+because\b", re.I), "narrator-from-distance: state the concrete cause"),
    (re.compile(r"\bthis\s+is\s+why\b", re.I), "narrator-from-distance: cut the lecture setup"),
]

VAGUE_DECLARATIVES = [
    (re.compile(r"\bthe\s+stakes\s+are\s+high\b", re.I), "vague declarative: name the actual risk"),
    (re.compile(r"\bthe\s+implications\s+are\s+significant\b", re.I), "vague declarative: name the actual implication"),
    (re.compile(r"\bthe\s+reasons\s+are\s+structural\b", re.I), "vague declarative: name the structure"),
    (re.compile(r"\bthis\s+is\s+the\s+deepest\s+problem\b", re.I), "vague declarative: name the problem"),
    (re.compile(r"\bthe\s+consequences\s+are\s+real\b", re.I), "vague declarative: name the consequence"),
]

WH_OPENER_SETUPS = [
    re.compile(r"(?m)^\s*(?:What\s+makes\s+this\s+hard|Why\s+this\s+matters|How\s+(?:teams|operators|businesses)\s+should\s+think|Where\s+this\s+gets\s+interesting)\b", re.I),
]

PASSIVE_VOICE_PATTERNS = [
    re.compile(r"\b(?:was|were)\s+(?:created|generated|decided|reached|built|designed|implemented|approved|sent|reviewed)\b", re.I),
    re.compile(r"\bmistakes\s+were\s+made\b", re.I),
    re.compile(r"\bit\s+is\s+believed\s+that\b", re.I),
]

GENERIC_AI = [
    "ai is changing",
    "ai-powered future",
    "transformative",
    "streamline",
    "unlock",
    "leverage ai",
    "ai chatbot",
    "cutting-edge",
    "innovative",
    "holistic",
    "robust",
]

POLISHED_GURU = [
    "in today's attention economy",
    "in today's fast-paced",
    "the ultimate competitive advantage",
    "brings to the table",
    "broader policy implications",
    "raise important concerns",
    "centralized source of truth",
    "streamline execution",
    "one thing is clear",
    "the tech is ready. the operations aren't",
    "every business has the data. almost none has the workflow",
    "automating a broken process just breaks it faster",
]

LINKEDIN_FUNNEL_STYLE = [
    "proof engine",
    "trust layer",
    "authority layer",
    "authority engine",
    "raise their hand",
    "qualified buyers raise their hand",
    "content becomes pipeline",
    "content into pipeline",
]

PIPELINE_ASSET_TERMS = [
    "conversion path",
    "lead magnet",
    "diagnostic",
    "reply path",
    "email capture",
    "call-prep",
    "call prep",
    "next-step offer",
]

PIPELINE_ASSET_ANCHORS = [
    "property-management ai workflow readiness checklist",
    "readiness checklist",
    "rent delinquency",
    "maintenance",
    "missed calls",
    "owner approvals",
    "drive",
    "notion",
    "memory/content/assets/",
]

LINKEDIN_TOO_CASUAL = [
    "quick update",
    "small win",
    "built this weekend",
    "been playing with",
    "messing around",
    "not gonna lie",
    "ngl",
    "nothing crazy",
    "pretty cool",
    "kind of cool",
    "vibes",
    "ship it and see",
    "random build",
    "weekend project",
]

INTERNAL_META = [
    "content system",
    "posted log",
    "swipe file",
    "reference ledger",
    "privacy cleanup",
    "client-name removal",
    "proof hygiene",
    "content automation",
]

SPECIFICITY_MARKERS = [
    "workflow",
    "workflows",
    "email",
    "pdf",
    "spreadsheet",
    "voice note",
    "inbox",
    "portal",
    "crm",
    "erp",
    "appfolio",
    "buildium",
    "rent manager",
    "owner",
    "manager",
    "approval",
    "exception",
    "queue",
    "intake",
    "source",
    "record",
    "log",
    "sku",
    "unit",
    "inventory",
    "price",
    "vendor",
    "tenant",
    "lease",
    "maintenance",
    "local",
    "machine",
    "pc",
    "server",
    "servers",
    "quickbooks",
    "compliance",
    "saved",
    "systems",
    "human attention",
    "insurance",
    "validation",
    "lead",
    "capturing",
    "contributors",
    "page",
]

BUYER_SCENE_MARKERS = [
    "tenant",
    "vendor",
    "owner",
    "manager",
    "buyer",
    "customer",
    "rep",
    "foreman",
    "dispatcher",
    "spreadsheet",
    "email",
    "pdf",
    "voicemail",
    "meeting",
    "report",
    "order",
    "invoice",
    "lease",
    "client",
    "firm",
    "office",
    "family office",
    "real estate",
]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def first_content_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue
        return stripped
    return ""


def last_content_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue
        return stripped
    return ""


def count_markers(text: str, markers: list[str]) -> int:
    lower = text.lower()
    return sum(1 for marker in markers if marker in lower)


def has_proof_context(text: str) -> bool:
    lower = text.lower()
    return sum(1 for marker in PROOF_CONTEXT_MARKERS if marker in lower) >= 4


def score(path: Path, platform: str) -> tuple[int, list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    problems: list[str] = []
    notes: list[str] = []
    points = 100

    for regex, label in BANNED_PATTERNS:
        if regex.search(text):
            if label == "not-just-X reveal" and has_proof_context(text):
                continue
            problems.append(label)
            points -= 15

    for regex, label in FALSE_AGENCY_PATTERNS:
        if regex.search(text):
            problems.append(label)
            points -= 15

    for regex, label in NARRATOR_DISTANCE_PATTERNS:
        if regex.search(text):
            problems.append(label)
            points -= 12

    for regex, label in VAGUE_DECLARATIVES:
        if regex.search(text):
            problems.append(label)
            points -= 12

    for regex in WH_OPENER_SETUPS:
        if regex.search(text):
            problems.append("Wh-opener setup: restructure around the actor, object, or constraint")
            points -= 12

    for regex in PASSIVE_VOICE_PATTERNS:
        if regex.search(text):
            problems.append("passive voice: name the actor or approval boundary")
            points -= 12

    generic_hits = [term for term in GENERIC_AI if term in lower]
    if generic_hits:
        problems.append("generic AI phrasing: " + ", ".join(generic_hits[:5]))
        points -= min(20, 5 * len(generic_hits))

    polished_hits = [term for term in POLISHED_GURU if term in lower]
    if polished_hits:
        problems.append("over-polished non-JT phrasing: " + ", ".join(polished_hits[:5]))
        points -= min(20, 5 * len(polished_hits))

    internal_hits = [term for term in INTERNAL_META if term in lower]
    if internal_hits:
        problems.append("internal/process topic surfaced: " + ", ".join(internal_hits[:5]))
        points -= min(25, 8 * len(internal_hits))

    first = first_content_line(text)
    last = last_content_line(text)
    first_lower = first.lower()
    scene_count = count_markers(first, BUYER_SCENE_MARKERS)
    specificity_count = count_markers(text, SPECIFICITY_MARKERS)

    colon_instruction_lists = re.findall(
        r":[^.\n]*(?:,\s*(?:what|who|where|when|why|how)\b[^.\n]*){2,}",
        text,
        flags=re.I,
    )
    if colon_instruction_lists:
        problems.append("robotic colon-list instruction block")
        points -= 15

    numbered_steps = re.findall(r"(?m)^\s*\d+\.\s+\S+", text)
    if len(numbered_steps) >= 4:
        personality_markers = re.findall(
            r"\b(?:built|installed|client|office|local|saved|workflow|operator|owner|approval|exception|metric|risk|system)\b",
            lower,
        )
        if len(personality_markers) < len(numbered_steps):
            problems.append("numbered list with no JT-specific personality")
            points -= 15

    if platform == "linkedin":
        funnel_hits = [term for term in LINKEDIN_FUNNEL_STYLE if term in lower]
        if funnel_hits:
            problems.append("LinkedIn funnel phrasing: " + ", ".join(funnel_hits[:5]))
            points -= min(30, 10 * len(funnel_hits))

        pipeline_hits = [term for term in PIPELINE_ASSET_TERMS if term in lower]
        if pipeline_hits and not any(anchor in lower for anchor in PIPELINE_ASSET_ANCHORS):
            problems.append("pipeline asset named generically: point to a concrete buyer-readable asset/path")
            points -= 15

        casual_hits = [
            term for term in LINKEDIN_TOO_CASUAL
            if re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", lower)
        ]
        if casual_hits:
            problems.append("too-casual LinkedIn phrasing: " + ", ".join(casual_hits[:5]))
            points -= min(25, 7 * len(casual_hits))
        if first and re.match(r"^[a-z]", first):
            problems.append("too-casual LinkedIn lowercase opener")
            points -= 10
        if scene_count == 0 and not VERIFIED_OWNERSHIP_RE.search(first_lower):
            problems.append("LinkedIn first line lacks buyer scene or verified ownership")
            points -= 15
        if VERIFIED_OWNERSHIP_RE.search(first_lower) and specificity_count < 4:
            problems.append("LinkedIn build update lacks client/employer-facing proof")
            points -= 12
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        if len(paragraphs) < 3:
            problems.append("LinkedIn draft has fewer than 3 paragraphs")
            points -= 8
        long_paragraphs = [p for p in paragraphs if len(p) > 520]
        if long_paragraphs:
            problems.append("LinkedIn rhythm too dense: paragraph over 520 chars")
            points -= 7
    elif platform == "x":
        if len(first) > 280:
            problems.append("X lead line exceeds 280 chars")
            points -= 20
        lines = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("```")]
        long_lines = [line for line in lines if len(line) > 240]
        if long_lines:
            problems.append("X rhythm too dense: line over 240 chars")
            points -= 10
        short_fragment_lines = [
            line for line in lines
            if re.fullmatch(r"[A-Za-z0-9$%/+'&-]+(?:\s+[A-Za-z0-9$%/+'&-]+){0,2}\.?", line)
        ]
        if len(short_fragment_lines) >= 5:
            problems.append("too-polished X noun-stack line breaks")
            points -= 15

    if specificity_count < 3:
        problems.append(f"too little operational specificity: {specificity_count} marker(s)")
        points -= 20
    elif specificity_count >= 6:
        notes.append(f"strong specificity markers: {specificity_count}")

    if "ai" in first_lower and scene_count == 0 and "built" not in first_lower:
        problems.append("starts with AI category instead of work scene")
        points -= 12

    if re.search(r"\b\w+[^.\n]{1,100}\s+(?:happened|changed|worked|clicked|shifted)\s+when\s+[^.\n]{1,140}\.?$", last, re.I):
        problems.append("JT-rejected closing shape: X happened/changed/worked when Y")
        points -= 15

    if re.search(r"\b(?:that'?s\s+(?:the\s+)?(?:point|tradeoff|lesson|move)|that'?s\s+how\s+you\s+know|[^.\n]{1,60}\s+is\s+the\s+new\s+[^.\n]{1,60})\.?$", last, re.I):
        problems.append("pull-quote ending: replace the quotable line with a concrete consequence")
        points -= 12

    return max(points, 0), problems, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Score JT content drafts for voice fit.")
    parser.add_argument("draft", help="Draft file to score")
    parser.add_argument("--platform", choices=["linkedin", "x"], required=True)
    parser.add_argument("--min-score", type=int, default=80)
    args = parser.parse_args()

    path = Path(args.draft)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        print(f"JT_VOICE_GUARD_FAIL\n- {rel(path)} does not exist")
        return 1

    points, problems, notes = score(path, args.platform)
    status = "PASS" if points >= args.min_score and not problems else "FAIL"
    print(f"JT_VOICE_GUARD_{status} score={points} min={args.min_score} platform={args.platform} file={rel(path)}")
    for note in notes:
        print(f"- note: {note}")
    for problem in problems:
        print(f"- problem: {problem}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
