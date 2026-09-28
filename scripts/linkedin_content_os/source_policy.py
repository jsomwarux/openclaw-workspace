"""Closed, deterministic source-family policy for LinkedIn Program 0."""

from __future__ import annotations

from typing import Dict, List, Set

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp


SCHEMA_VERSION = "linkedin-source-policy.v1"
_TOP_LEVEL_FIELDS = {
    "schemaVersion",
    "generatedAt",
    "families",
    "sourcePolicySha256",
}
_FAMILY_FIELDS = {
    "family",
    "status",
    "owner",
    "requiredEvidence",
    "conflictChecks",
    "permissionRule",
    "freshnessRule",
}
_FAMILY_NAMES = {
    "client_delivery",
    "field_lesson",
    "engineering_recipe",
    "teardown_trigger",
    "ai_event",
    "internal_machinery",
}


def _records() -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = [
        {
            "family": "client_delivery",
            "status": "allowed",
            "owner": "jt-ops immutable proof-asset Git object",
            "requiredEvidence": [
                "immutable_git_object",
                "claim_level_facts",
                "permission_evidence",
            ],
            "conflictChecks": [
                "client_conflict",
                "prospect_conflict",
                "employer_conflict",
            ],
            "permissionRule": "approved_anonymized_or_named_and_non_expired",
            "freshnessRule": "facts_and_permission_reverified_at_admission",
        },
        {
            "family": "field_lesson",
            "status": "allowed",
            "owner": "JT-confirmed field note or append-only outcome event",
            "requiredEvidence": ["jt_confirmation", "source_hash"],
            "conflictChecks": ["protected_purpose_removed", "client_conflict"],
            "permissionRule": "jt_confirmed_and_permission_safe",
            "freshnessRule": "source_state_reverified_at_admission",
        },
        {
            "family": "engineering_recipe",
            "status": "allowed",
            "owner": "accepted verifier claim plus execution artifact",
            "requiredEvidence": ["accepted_verifier_claim", "execution_artifact"],
            "conflictChecks": ["protected_purpose_removed", "public_value_boundary"],
            "permissionRule": "artifact_and_claim_must_be_publication_safe",
            "freshnessRule": "execution_artifact_reverified_at_admission",
        },
        {
            "family": "teardown_trigger",
            "status": "allowed",
            "owner": "primary public source",
            "requiredEvidence": ["primary_public_source", "event_date"],
            "conflictChecks": [
                "consulting_suppression",
                "client_conflict",
                "prospect_conflict",
                "job_conflict",
                "employer_conflict",
            ],
            "permissionRule": "public_facts_only_no_client_implication",
            "freshnessRule": "primary_event_date_controls_freshness",
        },
        {
            "family": "ai_event",
            "status": "allowed",
            "owner": (
                "proven X Intelligence Router, JT-supplied source, or approved primary "
                "public source"
            ),
            "requiredEvidence": {
                "allOf": ["bound_jt_artifact"],
                "oneOf": [
                    ["proven_x_intelligence_router"],
                    ["jt_supplied_source"],
                    ["approved_primary_public_source"],
                ],
            },
            "conflictChecks": ["source_identity", "claim_attribution", "protected_purpose_removed"],
            "permissionRule": "public_or_jt_supplied_source_only",
            "freshnessRule": "primary_event_date_controls_freshness",
        },
        {
            "family": "internal_machinery",
            "status": "prohibited",
            "owner": "no implicit override",
            "requiredEvidence": ["none"],
            "conflictChecks": ["internal_machinery_prohibited"],
            "permissionRule": "prohibited",
            "freshnessRule": "not_applicable",
        },
    ]
    return sorted(records, key=lambda record: str(record["family"]))


def evidence_satisfies(record: Dict[str, object], observed: Set[str]) -> bool:
    """Evaluate the closed all-of/one-of evidence contract for one family."""

    if not isinstance(observed, set) or any(
        not isinstance(item, str) or not item for item in observed
    ):
        raise ValueError("observed evidence must be a set of non-empty strings")
    required = record.get("requiredEvidence")
    if isinstance(required, list):
        if any(not isinstance(item, str) or not item for item in required):
            raise ValueError("requiredEvidence list is invalid")
        return set(required).issubset(observed)
    if not isinstance(required, dict) or set(required) != {"allOf", "oneOf"}:
        raise ValueError("requiredEvidence must be a closed list or branch contract")
    all_of = required.get("allOf")
    one_of = required.get("oneOf")
    if (
        not isinstance(all_of, list)
        or not all_of
        or any(not isinstance(item, str) or not item for item in all_of)
        or not isinstance(one_of, list)
        or not one_of
    ):
        raise ValueError("requiredEvidence branch contract is invalid")
    branches = []
    for branch in one_of:
        if (
            not isinstance(branch, list)
            or not branch
            or any(not isinstance(item, str) or not item for item in branch)
        ):
            raise ValueError("requiredEvidence oneOf branch is invalid")
        branches.append(set(branch))
    return set(all_of).issubset(observed) and any(
        branch.issubset(observed) for branch in branches
    )


def build_source_policy(generated_at: str) -> Dict[str, object]:
    """Build the one closed Program 0 source-family policy artifact."""

    parse_timestamp(generated_at, "generatedAt")
    unsigned: Dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": generated_at,
        "families": _records(),
    }
    return {
        **unsigned,
        "sourcePolicySha256": sha256_hex(canonical_bytes(unsigned)),
    }


def validate_source_policy(value: object) -> Dict[str, object]:
    """Validate exact policy bytes; unknown or changed policy data fail closed."""

    if not isinstance(value, dict) or set(value) != _TOP_LEVEL_FIELDS:
        raise ValueError("source policy has invalid top-level fields")
    generated_at = value.get("generatedAt")
    if not isinstance(generated_at, str):
        raise ValueError("generatedAt must be a string")
    expected = build_source_policy(generated_at)
    if canonical_bytes(value) != canonical_bytes(expected):
        raise ValueError("source policy does not match the closed policy contract")

    families = value.get("families")
    if not isinstance(families, list):
        raise ValueError("families must be a list")
    names = set()
    for record in families:
        if not isinstance(record, dict) or set(record) != _FAMILY_FIELDS:
            raise ValueError("source-family record has invalid fields")
        names.add(record.get("family"))
    if names != _FAMILY_NAMES:
        raise ValueError("source policy has an invalid family set")
    return value
