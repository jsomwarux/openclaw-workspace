"""Source-bound retirement inventory for superseded LinkedIn voice rules."""

from __future__ import annotations

from datetime import date
from typing import Dict, List

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex


SCHEMA_VERSION = "linkedin-voice-rule-retirements.v1"
RECONCILED_AUTHORITY = (
    "Exact JT-final LinkedIn text, evidence safety, and reconciled gates outrank "
    "fixed-day, fixed-format, and quota mechanics."
)
OWNER_SURFACES = (
    "docs/agents/content-rules.md",
    "memory/content-voice.md",
    "skills/wednesday-linkedin/SKILL.md",
)
_RETIRED_PHRASES = (
    "target 5:1 ratio",
    "150-250 words. prose only. no headers, no bullet lists.",
    "wednesday is the most important post of the week",
    "wednesday is jt's most important linkedin post",
    "wednesday is the highest-stakes post of the week",
    "use this skill whenever drafting or reviewing a wednesday linkedin case study post.",
    "four moves, in order:",
)


def _require_effective_date(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("effectiveDate must be a string")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("effectiveDate must be YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise ValueError("effectiveDate must be canonical YYYY-MM-DD")
    return value


def _validate_owners(owner_documents: Dict[str, bytes]) -> Dict[str, bytes]:
    if not isinstance(owner_documents, dict) or set(owner_documents) != set(OWNER_SURFACES):
        raise ValueError("voice-rule owner surfaces do not match the closed contract")
    validated: Dict[str, bytes] = {}
    for path in OWNER_SURFACES:
        payload = owner_documents[path]
        if not isinstance(payload, bytes):
            raise ValueError("owner surface {} must be exact bytes".format(path))
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("owner surface {} must be UTF-8".format(path)) from error
        if RECONCILED_AUTHORITY not in text:
            raise ValueError("owner surface {} lacks reconciled authority".format(path))
        lowered = text.lower()
        if any(phrase in lowered for phrase in _RETIRED_PHRASES):
            raise ValueError("owner surface {} still contains a retired voice rule".format(path))
        validated[path] = payload
    return validated


def _retirements(effective_date: str) -> List[Dict[str, object]]:
    common = {
        "replacementRule": RECONCILED_AUTHORITY,
        "reason": "quality and fit require evidence-bound judgment instead of fixed mechanics",
        "regressionTest": "scripts.tests.test_linkedin_content_os_voice_rules",
        "effectiveDate": effective_date,
    }
    records: List[Dict[str, object]] = [
        {
            **common,
            "oldRule": "pronoun_ratio_5_to_1",
            "ownerSurfaces": ["skills/wednesday-linkedin/SKILL.md"],
        },
        {
            **common,
            "oldRule": "mandatory_wednesday_case_study",
            "ownerSurfaces": list(OWNER_SURFACES),
        },
        {
            **common,
            "oldRule": "universal_150_to_250_prose_only",
            "ownerSurfaces": ["skills/wednesday-linkedin/SKILL.md"],
        },
        {
            **common,
            "oldRule": "fixed_weekly_linkedin_quota",
            "ownerSurfaces": ["memory/content-voice.md"],
        },
    ]
    return sorted(records, key=lambda record: str(record["oldRule"]))


def build_voice_rule_retirements(
    owner_documents: Dict[str, bytes], *, effective_date: str
) -> Dict[str, object]:
    """Build a hash-bound retirement artifact from all canonical owner bytes."""

    effective_date = _require_effective_date(effective_date)
    documents = _validate_owners(owner_documents)
    unsigned: Dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "effectiveDate": effective_date,
        "historicalBottleneck": "quality_fit",
        "legacyPostedFalseAuthority": "status_unknown",
        "ownerSourceSha256": {
            path: sha256_hex(documents[path]) for path in sorted(documents)
        },
        "retirements": _retirements(effective_date),
    }
    return {
        **unsigned,
        "retirementArtifactSha256": sha256_hex(canonical_bytes(unsigned)),
    }
