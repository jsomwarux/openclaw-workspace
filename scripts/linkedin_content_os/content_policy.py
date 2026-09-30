"""Deterministic public-copy policy for every LinkedIn content surface.

One authority for the governed hard bans in `docs/agents/content-rules.md` and
`memory/content-voice.md`. Every public surface (post, eyebrow, title, subtitle,
stage, footer, attribution, alt text) is checked by the same rules. Heuristic
voice scoring (first-line scene, pull-quote tone, rhythm) stays with
`scripts/jt_voice_guard.py`, which remains a required post-text gate.
"""

from __future__ import annotations

import re
from typing import Pattern, Tuple

PUBLIC_SURFACES = ("post", "eyebrow", "title", "subtitle", "stage", "footer", "attribution", "alt")

_I = re.IGNORECASE


def _words(rule: str, *patterns: str) -> Tuple[Tuple[str, Pattern[str]], ...]:
    return tuple((rule, re.compile(r"(?<![\w-])(?:{})(?![\w-])".format(pattern), _I)) for pattern in patterns)


# content-voice.md "Forbidden Words (zero exceptions across all platforms)".
_FORBIDDEN_WORDS = _words(
    "forbidden_word",
    r"utiliz(?:e|es|ed|ing|ation)",
    r"synerg(?:y|ies|istic)",
    r"ecosystems?",
    r"scalab(?:le|ility)",
    r"streamlin(?:e|es|ed|ing)",
    r"actionable",
    r"bandwidth",
    r"holistic(?:ally)?",
    r"innovative",
    r"robust(?:ly|ness)?",
    r"cutting[- ]edge",
    r"best[- ]in[- ]class",
    r"thought[- ]leaders?(?:ship)?",
    r"value[- ]adds?",
    r"paradigms?",
    r"granular(?:ity)?",
    r"deliverables?",
    r"upskill(?:s|ed|ing)?",
    r"touchpoints?",
    r"disruptive",
    r"implementation excellence",
    r"transformative",
    r"leverag(?:e|es|ed|ing)",
    r"solutions?",
    r"optimi[sz](?:e|es|ed|ing|ation|ations)",
    r"strategiz(?:e|es|ed|ing)",
    r"proactive(?:ly)?",
    r"learnings",
    r"unpack(?:s|ed|ing)?",
    r"unlock(?:s|ed|ing)?",
    r"at the end of the day",
    r"in terms of",
    r"it is important to note",
    r"that being said",
    r"in order to",
    r"here[’']?s the thing",
)

_PATTERNS: Tuple[Tuple[str, Pattern[str]], ...] = (
    # content-voice.md and content-rules.md "Never use" punctuation.
    ("em_dash", re.compile("—")),
    ("exclamation", re.compile(r"!")),
    ("question_marks", re.compile(r"\?\s*\?")),
    ("hashtag", re.compile(r"(?<![\w&])#[A-Za-z]\w*")),
    # content-voice.md global punctuation rule: no colon introduces a list,
    # sequence, explanation, statement hook, or reveal. Clock times and URLs
    # keep their colons because no whitespace follows them.
    ("prose_colon", re.compile(r":(?=\s|$)")),
    ("numbered_list", re.compile(r"(?m)^\s*\d+[.)]\s")),
    ("tricolon_negation", re.compile(r"\bno\s[^.!?\n]{1,80}[.!?]\s*no\s[^.!?\n]{1,80}[.!?]\s*just\b", _I)),
    # content-voice.md hard-banned hooks (Questions 2, 3, 5, 7).
    ("banned_hook", re.compile(r"\bthe\s+best\s+(?:first\s+)?ai\s+project\b", _I)),
    ("banned_hook", re.compile(r"\bai\s+gets\s+useful\s+at\b", _I)),
    ("banned_hook", re.compile(r"\bmost\b[^.!?\n]{0,80}\b(?:do|does)\s+not\s+(?:fail\s+because|need)\b", _I)),
    ("banned_hook", re.compile(r"\bwhat\s+most\s+people\s+miss\b", _I)),
    ("banned_hook", re.compile(r"\bhere[’']?s\s+(?:the|my)\s+system\b", _I)),
    ("banned_hook", re.compile(r"\bhere[’']?s\s+what\s+you\s+need\s+to\s+do\b", _I)),
    ("banned_hook", re.compile(r"\bthe\s+results\?", _I)),
    ("banned_hook", re.compile(r"\bmoron\b", _I)),
    ("banned_hook", re.compile(r"\b(?:INSANE|EVERYTHING|DO NOT|PISSED)\b")),
    ("banned_hook", re.compile(r"\binsane\s+opportunity\b", _I)),
    ("banned_hook", re.compile(r"\btake\s+action\s+before\s+someone\s+else\s+does\b", _I)),
    ("banned_hook", re.compile(r"\bgets\s+solved\s+with\s+a\s+hire\b", _I)),
    ("banned_hook", re.compile(r"\b(?:do|does)\s+not\s+[^.!?\n]{1,90},\s*(?:they|it)\s", _I)),
    ("banned_hook", re.compile(r"\bwould\s+you\s+trust\s+an?\s+ai\s+agent\s+with\b", _I)),
    ("banned_hook", re.compile(r"\bi\s+would\s+trust\s+it\s+with\b", _I)),
    ("banned_hook", re.compile(r"\bis\s+probably\s+a\s+margin\s+leak\b", _I)),
    ("banned_hook", re.compile(r"\bthe\s+useful\s+question\s+is\s+uglier\b", _I)),
    ("banned_hook", re.compile(r"\bmake\s+stuck\s+work\s+visible\s+before\s+you\s+make\b", _I)),
    ("banned_hook", re.compile(r"\bwhat\s+did\s+you\s+build\s+in\b", _I)),
    # content-voice.md slogan pairs named as too polished.
    ("slogan_pair", re.compile(r"\bagents\s+handle\s+the\s+work\b", _I)),
    ("slogan_pair", re.compile(r"\byou\s+keep\s+the\s+margin\b", _I)),
    ("slogan_pair", re.compile(r"\bbuild\s+the\s+process\.\s+buy\s+back\s+the\s+time\b", _I)),
    ("slogan_pair", re.compile(r"\bconsultants\s+charge\s+for\s+advice\b", _I)),
    ("slogan_pair", re.compile(r"\bi\s+charge\s+for\s+the\s+thing\s+that\s+works\b", _I)),
    ("slogan_pair", re.compile(r"\bdemo\s+proves\s+it[’']?s\s+possible\b", _I)),
    ("slogan_pair", re.compile(r"\bspecs\s+live\s+in\s+decks\b", _I)),
    # content-rules.md and content-voice.md contrarian-setup bans.
    ("contrast_shape", re.compile(r"\b\w+n[’']t\b", _I)),
    ("contrast_shape", re.compile(r"\b(?:is|are)\s+not\b", _I)),
    ("contrast_shape", re.compile(r",\s*not\b", _I)),
    ("contrast_shape", re.compile(r"\bnot\b[^.!?\n]{0,80}\b(?:but|more\s+like)\b", _I)),
    ("contrast_shape", re.compile(r"\bshould\s+become\b[^.!?\n]{0,80}\binstead\s+of\b", _I)),
    ("importance_phrase", re.compile(r"\bmatters\s+more\s+than\s+people\s+(?:think|realize)\b", _I)),
    ("importance_phrase", re.compile(r"\bpeople\s+underestimate\b", _I)),
    ("importance_phrase", re.compile(r"\bthat\s+part\s+matters\b", _I)),
    # content-rules.md LinkedIn originality hard blocks.
    ("originality_block", re.compile(r"\bleast\s+glamorous\b", _I)),
    ("originality_block", re.compile(r"\bhandoff\s+everyone\s+checks\s+manually\b", _I)),
    ("originality_block", re.compile(r"\bgets\s+risky\s+when\b", _I)),
    ("originality_block", re.compile(r"\blive\s+in\s+different\s+places\b", _I)),
    ("originality_block", re.compile(r"\bexception\s+layer\b", _I)),
    ("originality_block", re.compile(r"\bwhere\s+the\s+risk\s+lives\b", _I)),
    # content-rules.md internal-machinery prohibition and originality blocks.
    ("internal_machinery", re.compile(r"\bautonomous\s+content\s+system\b", _I)),
    ("internal_machinery", re.compile(r"\bstate\s+file\b", _I)),
    ("internal_machinery", re.compile(r"\bstop\s+condition\b", _I)),
    ("internal_machinery", re.compile(r"\bmission\s+control\b", _I)),
    ("internal_machinery", re.compile(r"\bopenclaw\b", _I)),
    ("internal_machinery", re.compile(r"\beve\b", _I)),
    ("internal_machinery", re.compile(r"\b(?:content|growth)\s+os\b", _I)),
    ("internal_machinery", re.compile(r"\b(?:outreach|prospecting|job[- ]search)\s+(?:automation|operations|pipeline)\b", _I)),
    ("internal_machinery", re.compile(r"\bjob\s+search\b", _I)),
    ("internal_machinery", re.compile(r"\bproof\s+hygiene\b", _I)),
    ("internal_machinery", re.compile(r"\b(?:publishing|content)\s+machinery\b", _I)),
    ("internal_machinery", re.compile(r"\bcontent[- ]generation\b", _I)),
    ("internal_machinery", re.compile(r"\bdecagon\b", _I)),
    # content-voice.md "Stop Slop delta adopted 2026-06-07".
    ("false_agency", re.compile(r"\bthe\s+data\s+(?:tells|shows|says)\b", _I)),
    ("false_agency", re.compile(r"\bthe\s+decision\s+(?:emerges|was\s+reached)\b", _I)),
    ("false_agency", re.compile(r"\bthe\s+market\s+rewards\b", _I)),
    ("false_agency", re.compile(r"\ba\s+complaint\s+becomes\s+a\s+fix\b", _I)),
    ("false_agency", re.compile(r"\ba\s+bet\s+(?:lives|dies)\b", _I)),
    ("false_agency", re.compile(r"\bthe\s+culture\s+shifts\b", _I)),
    ("false_agency", re.compile(r"\bthe\s+conversation\s+moves\s+toward\b", _I)),
    ("false_agency", re.compile(r"\bthe\s+workflow\s+(?:creates|builds)\s+trust\b", _I)),
    ("narrator_distance", re.compile(r"\bpeople\s+tend\s+to\b", _I)),
    ("narrator_distance", re.compile(r"\bnobody\s+designed\s+this\b", _I)),
    ("narrator_distance", re.compile(r"\bthis\s+happens\s+because\b", _I)),
    ("narrator_distance", re.compile(r"\bthis\s+is\s+why\b", _I)),
    ("vague_declarative", re.compile(r"\bthe\s+stakes\s+are\s+high\b", _I)),
    ("vague_declarative", re.compile(r"\bthe\s+implications\s+are\s+significant\b", _I)),
    ("vague_declarative", re.compile(r"\bthe\s+reasons\s+are\s+structural\b", _I)),
    ("vague_declarative", re.compile(r"\bthe\s+consequences\s+are\s+real\b", _I)),
    ("wh_opener", re.compile(r"(?m)^\s*(?:what\s+makes\s+this\s+hard|why\s+this\s+matters|how\s+(?:teams|operators|businesses)\s+should\s+think)\b", _I)),
    ("pull_quote_ending", re.compile(r"\bthat(?:[’']s|\s+is)\s+the\s+(?:lesson|tradeoff)\b", _I)),
    ("pull_quote_ending", re.compile(r"\bis\s+the\s+new\s+\w+", _I)),
    ("passive_voice", re.compile(r"\b(?:was|were)\s+(?:created|generated|decided|reached)\b", _I)),
    ("passive_voice", re.compile(r"\bmistakes\s+were\s+made\b", _I)),
    ("possible_secret", re.compile(r"(?:\bsk-|\bbearer\s+|\btoken[=:]|[0-9a-f]{40,})", _I)),
)

_SENTENCE = re.compile(r"[^.!?\n]+[.!?]?")


def _noun_stack(text: str) -> bool:
    """Three or more consecutive one- or two-word sentences (content-voice.md Q7)."""

    run = 0
    for sentence in _SENTENCE.findall(text):
        words = sentence.strip().rstrip(".!?").split()
        if not words:
            continue
        run = run + 1 if len(words) <= 2 else 0
        if run >= 3:
            return True
    return False


def _closing_when(text: str) -> bool:
    """The final sentence may not be an "X happened/changed/worked when Y" close."""

    sentences = [sentence.strip() for sentence in _SENTENCE.findall(text) if sentence.strip()]
    return bool(sentences) and re.search(
        r"\b(?:happened|changed|worked)\s+when\b", sentences[-1], _I
    ) is not None


def violations(text: str) -> list[str]:
    """Return every governed rule the text breaks, as `rule:matched-text` entries."""

    found: list[str] = []
    for rule, pattern in _FORBIDDEN_WORDS + _PATTERNS:
        match = pattern.search(text)
        if match is not None:
            found.append("{}:{}".format(rule, match.group(0).strip()))
    if text.count("?") > 2:
        found.append("question_marks:{} question marks".format(text.count("?")))
    if _noun_stack(text):
        found.append("noun_stack:consecutive one- or two-word sentences")
    if _closing_when(text):
        found.append("closing_when:final happened/changed/worked-when sentence")
    return found


def require_public_copy(text: str, surface: str) -> str:
    """Return the text unchanged, or fail closed on the first governed violation."""

    if surface not in PUBLIC_SURFACES:
        raise ValueError("unknown public copy surface {!r}".format(surface))
    found = violations(text)
    if found:
        raise ValueError("{} uses prohibited public copy [{}]".format(surface, found[0]))
    return text


__all__ = ["PUBLIC_SURFACES", "require_public_copy", "violations"]
