"""Closed, deterministic contracts for LinkedIn Program 0 outcome events."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Dict, List, Set, TypedDict
from urllib.parse import unquote, urlsplit

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex


HISTORICAL_STATUS = {"posted_confirmed", "not_posted_confirmed", "status_unknown"}
OUTCOME_EVENT = {
    "historical_status",
    "publication_acknowledged",
    "publication_deferred",
    "publication_declined",
    "final_text_captured",
    "metric_snapshot",
    "qualified_reply",
    "commercial_outcome",
    "focus_decision",
    "permission_fixture_accepted",
    "corpus_authority_receipt",
    "correction",
}
DECLINE_REASON = {"quality_fit", "stale", "timing", "other"}
EDIT_REASON = {
    "compression",
    "evidence",
    "hook",
    "positioning",
    "specificity",
    "structure",
    "voice",
}
CLAIM_ATTRIBUTION = {
    "public_fact",
    "vendor_assertion",
    "jt_verified_fact",
    "hypothesis",
}
CORPUS_AUTHORITY_SOURCE_TYPE = {
    "jt_authored_text",
    "jt_human_gate_response",
    "linkedin_publication_capture",
}

SCHEMA_VERSION = "linkedin-content-outcome.v1"
_HASH = re.compile(r"^[0-9a-f]{64}$")
_STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_GIT_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_URI = re.compile(r"^[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+$")
_MALFORMED_PERCENT_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")


class SourcePointer(TypedDict):
    sourceType: str
    sourceId: str
    sourceSha256: str


class OutcomeEvent(TypedDict):
    schemaVersion: str
    outcomeEventId: str
    packetId: str
    eventType: str
    recordedAt: str
    sourcePointer: SourcePointer
    payload: Dict[str, object]
    eventSha256: str


_TOP_LEVEL_FIELDS = {
    "schemaVersion",
    "outcomeEventId",
    "packetId",
    "eventType",
    "recordedAt",
    "sourcePointer",
    "payload",
    "eventSha256",
}
_SOURCE_FIELDS = {"sourceType", "sourceId", "sourceSha256"}

# (required fields, optional fields). Each event owns one closed payload shape.
_PAYLOAD_FIELDS = {
    "historical_status": (
        {"legacyRowSha256", "status"},
        set(),
    ),
    "publication_acknowledged": (
        {"publicationUrl"},
        {"publishedAt", "finalText", "finalTextSha256"},
    ),
    "publication_deferred": (
        {"nextCheckAt"},
        set(),
    ),
    "publication_declined": (
        {"declineReason"},
        {"note"},
    ),
    "final_text_captured": (
        {
            "finalText",
            "finalTextSha256",
            "publicationOutcomeEventId",
            "publicationOutcomeEventSha256",
            "publicationUrlSha256",
        },
        {"draftText", "draftTextSha256", "editReason"},
    ),
    "metric_snapshot": (
        {"windowDays", "metrics", "collectionMethod"},
        set(),
    ),
    "qualified_reply": (
        {"evidenceRef", "qualificationReason"},
        {"claimAttribution"},
    ),
    "commercial_outcome": (
        {"outcomeType", "evidenceRef"},
        {"claimAttribution"},
    ),
    "focus_decision": (
        {"decision", "focusSnapshotSha256"},
        {"replacementFocusSnapshotSha256"},
    ),
    "permission_fixture_accepted": (
        {
            "fixtureId",
            "repository",
            "commitSha",
            "path",
            "extractedSha256",
            "permissionEvidenceSha256",
            "permissionExpiresAt",
        },
        set(),
    ),
    "corpus_authority_receipt": (
        {
            "authoritySourceType",
            "authoritySourceId",
            "authoritySourceSha256",
            "rawAuthoritySha256",
            "textOutcomeEventId",
            "textOutcomeEventSha256",
            "ledgerPrefixSha256",
            "ledgerPosition",
            "validatedAt",
            "clientSensitiveMarkers",
        },
        set(),
    ),
    "correction": (
        {"targetOutcomeEventId", "replacementEventSha256", "reason"},
        set(),
    ),
}


def _require_exact_fields(
    value: dict[str, object], required: Set[str], optional: Set[str], label: str
) -> None:
    keys = set(value)
    missing = required - keys
    unknown = keys - required - optional
    if missing:
        raise ValueError("{} missing fields: {}".format(label, sorted(missing)))
    if unknown:
        raise ValueError("{} unknown fields: {}".format(label, sorted(unknown)))


def _require_string(value: object, label: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        raise ValueError("{} must be a string".format(label))
    if nonempty and not value.strip():
        raise ValueError("{} must not be empty".format(label))
    return value


def _require_stable_id(value: object, label: str) -> str:
    text = _require_string(value, label)
    if _STABLE_ID.fullmatch(text) is None:
        raise ValueError("{} must be a stable identifier".format(label))
    return text


def _require_hash(value: object, label: str) -> str:
    text = _require_string(value, label)
    if _HASH.fullmatch(text) is None:
        raise ValueError("{} must be 64 lowercase hexadecimal characters".format(label))
    return text


def parse_timestamp(value: object, label: str = "timestamp") -> datetime:
    """Parse one timezone-aware ISO-8601 timestamp or fail closed."""

    text = _require_string(value, label)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise ValueError("{} must be ISO 8601".format(label)) from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("{} must be timezone-aware".format(label))
    return parsed


def validate_claim_attribution(value: object) -> str:
    text = _require_string(value, "claimAttribution")
    if text not in CLAIM_ATTRIBUTION:
        raise ValueError("unsupported claimAttribution {!r}".format(text))
    return text


def validate_linkedin_url(value: object) -> str:
    text = _require_string(value, "publicationUrl")
    if text != text.strip() or any(
        ord(character) < 32 or ord(character) == 127 for character in text
    ):
        raise ValueError("publicationUrl contains whitespace or control characters")
    if _URI.fullmatch(text) is None:
        raise ValueError("publicationUrl contains a character outside the URI character set")
    if _MALFORMED_PERCENT_ESCAPE.search(text) is not None:
        raise ValueError("publicationUrl contains a malformed percent escape")
    try:
        parsed = urlsplit(text)
        port = parsed.port
    except ValueError as error:
        raise ValueError("publicationUrl is malformed") from error
    host = (parsed.hostname or "").lower()
    if (
        parsed.scheme != "https"
        or port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or not (host == "linkedin.com" or host.endswith(".linkedin.com"))
        or not parsed.path.startswith("/")
    ):
        raise ValueError("publicationUrl must be an HTTPS LinkedIn URL")
    path = unquote(parsed.path)
    if not (
        re.fullmatch(r"/posts/[^/?#]+/?", path)
        or re.fullmatch(r"/feed/update/urn:li:activity:\d+/?", path)
    ):
        raise ValueError("publicationUrl must identify a canonical LinkedIn post")
    decoded_url = unquote(text).lower()
    placeholder_tokens = {
        token for token in re.split(r"[^a-z0-9]+", decoded_url) if token
    }
    if placeholder_tokens & {
        "draft",
        "example",
        "fake",
        "placeholder",
        "sample",
        "temp",
        "test",
        "todo",
        "unknown",
    }:
        raise ValueError("publicationUrl contains a placeholder marker")
    return text


def _validate_payload(event_type: str, payload_value: object) -> None:
    if not isinstance(payload_value, dict):
        raise ValueError("payload must be an object")
    payload: dict[str, object] = payload_value
    required, optional = _PAYLOAD_FIELDS[event_type]
    _require_exact_fields(payload, required, optional, "payload")

    if event_type == "historical_status":
        _require_hash(payload["legacyRowSha256"], "legacyRowSha256")
        if payload["status"] not in HISTORICAL_STATUS:
            raise ValueError("unsupported historical status")
    elif event_type == "publication_acknowledged":
        validate_linkedin_url(payload["publicationUrl"])
        if "publishedAt" in payload:
            parse_timestamp(payload["publishedAt"], "publishedAt")
        if ("finalText" in payload) != ("finalTextSha256" in payload):
            raise ValueError("finalText and finalTextSha256 must appear together")
        if "finalText" in payload:
            final_text = _require_string(payload["finalText"], "finalText")
            expected = sha256_hex(final_text.encode("utf-8"))
            if _require_hash(payload["finalTextSha256"], "finalTextSha256") != expected:
                raise ValueError("finalTextSha256 does not match finalText")
    elif event_type == "publication_deferred":
        parse_timestamp(payload["nextCheckAt"], "nextCheckAt")
    elif event_type == "publication_declined":
        if payload["declineReason"] not in DECLINE_REASON:
            raise ValueError("unsupported declineReason")
        if "note" in payload:
            _require_string(payload["note"], "note")
    elif event_type == "final_text_captured":
        final_text = _require_string(payload["finalText"], "finalText")
        expected = sha256_hex(final_text.encode("utf-8"))
        if _require_hash(payload["finalTextSha256"], "finalTextSha256") != expected:
            raise ValueError("finalTextSha256 does not match finalText")
        _require_stable_id(
            payload["publicationOutcomeEventId"], "publicationOutcomeEventId"
        )
        _require_hash(
            payload["publicationOutcomeEventSha256"],
            "publicationOutcomeEventSha256",
        )
        _require_hash(payload["publicationUrlSha256"], "publicationUrlSha256")
        edit_pair_fields = {"draftText", "draftTextSha256", "editReason"}
        present_edit_pair_fields = edit_pair_fields & set(payload)
        if present_edit_pair_fields and present_edit_pair_fields != edit_pair_fields:
            raise ValueError("edit-pair bundle must be complete")
        if present_edit_pair_fields:
            draft_text = _require_string(payload["draftText"], "draftText")
            draft_expected = sha256_hex(draft_text.encode("utf-8"))
            if (
                _require_hash(payload["draftTextSha256"], "draftTextSha256")
                != draft_expected
            ):
                raise ValueError("draftTextSha256 does not match draftText")
            if draft_text == final_text:
                raise ValueError("draftText and finalText must differ for an edit pair")
            edit_reason = _require_string(payload["editReason"], "editReason")
            if edit_reason not in EDIT_REASON:
                raise ValueError("unsupported editReason {!r}".format(edit_reason))
    elif event_type == "metric_snapshot":
        window = payload["windowDays"]
        if not isinstance(window, int) or isinstance(window, bool) or window <= 0:
            raise ValueError("windowDays must be a positive integer")
        metrics = payload["metrics"]
        if not isinstance(metrics, dict) or not metrics:
            raise ValueError("metrics must be a non-empty object")
        for key, metric in metrics.items():
            _require_stable_id(key, "metric name")
            if not isinstance(metric, int) or isinstance(metric, bool) or metric < 0:
                raise ValueError("metric values must be non-negative integers")
        _require_stable_id(payload["collectionMethod"], "collectionMethod")
    elif event_type == "qualified_reply":
        _require_string(payload["evidenceRef"], "evidenceRef")
        _require_string(payload["qualificationReason"], "qualificationReason")
        if "claimAttribution" in payload:
            validate_claim_attribution(payload["claimAttribution"])
    elif event_type == "commercial_outcome":
        _require_stable_id(payload["outcomeType"], "outcomeType")
        _require_string(payload["evidenceRef"], "evidenceRef")
        if "claimAttribution" in payload:
            validate_claim_attribution(payload["claimAttribution"])
    elif event_type == "focus_decision":
        if payload["decision"] not in {"confirmed", "corrected"}:
            raise ValueError("unsupported focus decision")
        _require_hash(payload["focusSnapshotSha256"], "focusSnapshotSha256")
        replacement = payload.get("replacementFocusSnapshotSha256")
        if payload["decision"] == "corrected":
            _require_hash(replacement, "replacementFocusSnapshotSha256")
        elif replacement is not None:
            raise ValueError("confirmed focus decision cannot include replacement")
    elif event_type == "permission_fixture_accepted":
        _require_stable_id(payload["fixtureId"], "fixtureId")
        _require_string(payload["repository"], "repository")
        commit = _require_string(payload["commitSha"], "commitSha")
        if _GIT_COMMIT.fullmatch(commit) is None:
            raise ValueError("commitSha must be 40 lowercase hexadecimal characters")
        path = _require_string(payload["path"], "path")
        if path.startswith("/") or ".." in path.split("/"):
            raise ValueError("path must be a safe repository-relative path")
        _require_hash(payload["extractedSha256"], "extractedSha256")
        _require_hash(payload["permissionEvidenceSha256"], "permissionEvidenceSha256")
        parse_timestamp(payload["permissionExpiresAt"], "permissionExpiresAt")
    elif event_type == "corpus_authority_receipt":
        authority_type = _require_string(
            payload["authoritySourceType"], "authoritySourceType"
        )
        if authority_type not in CORPUS_AUTHORITY_SOURCE_TYPE:
            raise ValueError(
                "unsupported authoritySourceType {!r}".format(authority_type)
            )
        _require_string(payload["authoritySourceId"], "authoritySourceId")
        _require_hash(payload["authoritySourceSha256"], "authoritySourceSha256")
        _require_hash(payload["rawAuthoritySha256"], "rawAuthoritySha256")
        _require_stable_id(payload["textOutcomeEventId"], "textOutcomeEventId")
        _require_hash(payload["textOutcomeEventSha256"], "textOutcomeEventSha256")
        _require_hash(payload["ledgerPrefixSha256"], "ledgerPrefixSha256")
        position = payload["ledgerPosition"]
        if not isinstance(position, int) or isinstance(position, bool) or position <= 0:
            raise ValueError("ledgerPosition must be a positive integer")
        parse_timestamp(payload["validatedAt"], "validatedAt")
        markers = payload["clientSensitiveMarkers"]
        if not isinstance(markers, list):
            raise ValueError("clientSensitiveMarkers must be a list")
        normalized: list[str] = []
        for marker in markers:
            text = _require_string(marker, "clientSensitiveMarker")
            if text != text.strip():
                raise ValueError("clientSensitiveMarker must be trimmed")
            normalized.append(text)
        if normalized != sorted(set(normalized)):
            raise ValueError("clientSensitiveMarkers must be unique and sorted")
    elif event_type == "correction":
        _require_stable_id(payload["targetOutcomeEventId"], "targetOutcomeEventId")
        _require_hash(payload["replacementEventSha256"], "replacementEventSha256")
        _require_string(payload["reason"], "reason")


def validate_event(event_value: object) -> dict[str, object]:
    """Validate one event and return it unchanged."""

    if not isinstance(event_value, dict):
        raise ValueError("event must be an object")
    event: dict[str, object] = event_value

    def reject_nulls(value: object, label: str) -> None:
        if value is None:
            raise ValueError("{} must not be null".format(label))
        if isinstance(value, dict):
            for key, item in value.items():
                reject_nulls(item, "{}.{}".format(label, key))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                reject_nulls(item, "{}[{}]".format(label, index))

    reject_nulls(event, "event")
    _require_exact_fields(event, _TOP_LEVEL_FIELDS, set(), "event")
    if event["schemaVersion"] != SCHEMA_VERSION:
        raise ValueError("unsupported schemaVersion")
    _require_stable_id(event["outcomeEventId"], "outcomeEventId")
    _require_stable_id(event["packetId"], "packetId")
    event_type = _require_string(event["eventType"], "eventType")
    if event_type not in OUTCOME_EVENT:
        raise ValueError("unsupported eventType {!r}".format(event_type))
    parse_timestamp(event["recordedAt"], "recordedAt")

    source_value = event["sourcePointer"]
    if not isinstance(source_value, dict):
        raise ValueError("sourcePointer must be an object")
    source: dict[str, object] = source_value
    _require_exact_fields(source, _SOURCE_FIELDS, set(), "sourcePointer")
    source_type = _require_stable_id(source["sourceType"], "sourceType")
    _require_string(source["sourceId"], "sourceId")
    _require_hash(source["sourceSha256"], "sourceSha256")
    if (
        event_type == "corpus_authority_receipt"
        and source_type != "corpus_authority_verifier"
    ):
        raise ValueError(
            "corpus_authority_receipt sourceType must be corpus_authority_verifier"
        )

    _validate_payload(event_type, event["payload"])
    if event_type == "corpus_authority_receipt":
        payload = event["payload"]
        assert isinstance(payload, dict)
        if source["sourceSha256"] != payload["rawAuthoritySha256"]:
            raise ValueError(
                "corpus authority verifier source hash must match raw authority bytes"
            )
    provided_hash = _require_hash(event["eventSha256"], "eventSha256")
    unhashed = {key: value for key, value in event.items() if key != "eventSha256"}
    expected_hash = sha256_hex(canonical_bytes(unhashed))
    if provided_hash != expected_hash:
        raise ValueError("eventSha256 does not match canonical event bytes")
    return event


__all__: List[str] = [
    "CLAIM_ATTRIBUTION",
    "CORPUS_AUTHORITY_SOURCE_TYPE",
    "DECLINE_REASON",
    "EDIT_REASON",
    "HISTORICAL_STATUS",
    "OUTCOME_EVENT",
    "OutcomeEvent",
    "SourcePointer",
    "parse_timestamp",
    "validate_claim_attribution",
    "validate_event",
    "validate_linkedin_url",
]
