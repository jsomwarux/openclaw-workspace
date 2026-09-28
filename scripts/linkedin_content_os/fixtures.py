"""Build evidence-only LinkedIn Program 0 evaluation fixtures."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Callable, Optional, Sequence

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.contracts import parse_timestamp


DECAGON_PACKET_PATH = (
    "mission-control/lib/mission-control/fixtures/jobs/"
    "decagon-agent-development-manager.packet.json"
)
DECAGON_PAYLOAD_HASH = (
    "cd252d0ca23652adc7a7395ac7dafa97c7e56323dbc92609da3a6eb257644974"
)
DECAGON_SOURCE_COMMIT = "2aae65c4f12ed05831b3c3f577d9fb7d4f16acfd"
DECAGON_BLOB_ID = "da25924bbf874ca128990ad5d694118ea53d546d"
DECAGON_CONTENT_SHA256 = (
    "48448f87b3f5d8dec47bb2ee8113a3c58b5fa63bbfc6883f86c18f4ecdff516d"
)

PRE_GATE_COMMIT = "cd3e17f5287a64dbfedc27e1d2153d89250ba02c"
PRE_GATE_PATH = "evidence/cohort-two.proof-asset.json"
PRE_GATE_BLOB_ID = "02c53107260317f6eb31b2d8cc742b9b357ccadf"
PRE_GATE_CONTENT_SHA256 = (
    "4cca9c69d5430e0d08a16ff9d5ae7141fa2f277ce85196ed4aeb502658c99961"
)

SCHEMA_VERSION = "linkedin-evaluation-fixture.v1"
_HASH40 = re.compile(r"^[0-9a-f]{40}$")
_HASH64 = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_PERMISSION = {"approved-anonymized", "approved-named"}
_PERMISSIONED_FIELDS = {
    "schemaVersion",
    "proofId",
    "status",
    "verifiedAt",
    "facts",
    "permission",
    "activeProspectConflict",
    "activeEmployerConflict",
    "protectedInternalPremise",
}
_PERMISSIONED_FACT_FIELDS = {"factId", "conceptId", "outboundText"}
_PERMISSION_FIELDS = {"status", "evidenceRef", "expiresAt"}
_LEGACY_FIELDS = {
    "schema_version",
    "card_id",
    "status",
    "verified_by",
    "verified_at",
    "system_revision",
    "facts",
}
_LEGACY_FACT_FIELDS = {
    "fact_id",
    "concept_id",
    "sentence_id",
    "outbound_text",
    "claim_values",
}
_Runner = Callable[..., subprocess.CompletedProcess]


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError("{} must be non-empty trimmed text".format(label))
    return value


def _require_hash(value: object, length: int, label: str) -> str:
    text = _require_text(value, label)
    pattern = _HASH40 if length == 40 else _HASH64
    if pattern.fullmatch(text) is None:
        raise ValueError("{} must be {} lowercase hexadecimal characters".format(label, length))
    return text


def _safe_repo_path(value: object) -> str:
    path = _require_text(value, "path")
    parsed = PurePosixPath(path)
    if parsed.is_absolute() or any(part in {"", ".", ".."} for part in parsed.parts):
        raise ValueError("path must be a safe repository-relative path")
    if path == "scripts/tests/fixtures" or path.startswith("scripts/tests/fixtures/"):
        raise ValueError("test fixture paths cannot be authoritative evidence")
    return path


def _git_blob_id(payload: bytes) -> str:
    header = "blob {}\0".format(len(payload)).encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def extract_git_object(
    git_dir: Path,
    commit: str,
    path: str,
    expected_blob_id: str,
    *,
    runner: _Runner = subprocess.run,
) -> bytes:
    """Extract exact Git bytes through one read-only, shell-free argv."""

    git_path = Path(git_dir)
    if not git_path.is_absolute():
        raise ValueError("git_dir must be an absolute path")
    commit_value = _require_hash(commit, 40, "commit")
    object_id = _require_hash(expected_blob_id, 40, "expected Git object ID")
    relative_path = _safe_repo_path(path)
    result = runner(
        [
            "git",
            "--git-dir",
            str(git_path),
            "show",
            "{}:{}".format(commit_value, relative_path),
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ValueError("Git object extraction failed")
    payload = result.stdout
    if not isinstance(payload, bytes):
        raise ValueError("Git object extraction must return exact bytes")
    if _git_blob_id(payload) != object_id:
        raise ValueError("extracted bytes do not match expected Git object ID")
    return payload


def _strict_json(payload: bytes, label: str) -> dict[str, object]:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("{} is not UTF-8".format(label)) from error

    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("{} has duplicate JSON key {}".format(label, key))
            value[key] = item
        return value

    def reject_non_standard_constant(constant: str) -> None:
        raise ValueError("non-standard JSON constant {}".format(constant))

    try:
        value = json.loads(
            text,
            object_pairs_hook=pairs_hook,
            parse_constant=reject_non_standard_constant,
        )
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError("{} is not strict JSON: {}".format(label, error)) from error
    if not isinstance(value, dict):
        raise ValueError("{} must be a JSON object".format(label))
    return value


def _require_exact_fields(
    value: dict[str, object], expected: set[str], label: str
) -> None:
    if set(value) != expected:
        raise ValueError("{} schema fields are not closed".format(label))


def _validate_document_schema(document: dict[str, object]) -> str:
    """Return immutable proof identity after closed schema validation."""

    if document.get("schemaVersion") == "permissioned-proof.v1":
        conflict_fields = {
            "activeProspectConflict",
            "activeEmployerConflict",
            "protectedInternalPremise",
        }
        if not conflict_fields.issubset(document):
            raise ValueError("conflict fields must all exist")
        _require_exact_fields(document, _PERMISSIONED_FIELDS, "permissioned proof")
        identity = _require_text(document["proofId"], "proofId")
        if document["status"] != "verified":
            raise ValueError("permissioned proof status must be verified")
        for field in sorted(conflict_fields):
            if type(document[field]) is not bool:
                raise ValueError("conflict fields must all be exact booleans")
        facts = document["facts"]
        if not isinstance(facts, list):
            raise ValueError("permissioned proof facts must be a list")
        for fact in facts:
            if not isinstance(fact, dict):
                raise ValueError("permissioned proof fact must be an object")
            _require_exact_fields(fact, _PERMISSIONED_FACT_FIELDS, "permissioned fact")
        permission = document["permission"]
        if permission is not None:
            if not isinstance(permission, dict):
                raise ValueError("permission must be an object or null")
            _require_exact_fields(permission, _PERMISSION_FIELDS, "permission")
        return identity

    if document.get("schema_version") == "proof-asset-card-v1":
        _require_exact_fields(document, _LEGACY_FIELDS, "legacy proof")
        identity = _require_text(document["card_id"], "card_id")
        if document["status"] != "verified":
            raise ValueError("legacy proof status must be verified")
        facts = document["facts"]
        if not isinstance(facts, list):
            raise ValueError("legacy proof facts must be a list")
        for fact in facts:
            if not isinstance(fact, dict):
                raise ValueError("legacy proof fact must be an object")
            _require_exact_fields(fact, _LEGACY_FACT_FIELDS, "legacy fact")
            if not isinstance(fact["claim_values"], list):
                raise ValueError("legacy claim_values must be a list")
        return identity

    raise ValueError("unsupported proof schema")


def _source_ref(provenance: dict[str, object], payload: bytes) -> dict[str, object]:
    proof_id = _require_text(provenance.get("proofId"), "proofId")
    repository = _require_text(provenance.get("repository"), "repository")
    commit = _require_hash(provenance.get("commit"), 40, "commit")
    path = _safe_repo_path(provenance.get("path"))
    git_object_id = _require_hash(
        provenance.get("gitObjectId"), 40, "Git object ID"
    )
    content_sha256 = _require_hash(
        provenance.get("contentSha256"), 64, "content SHA-256"
    )
    if _git_blob_id(payload) != git_object_id:
        raise ValueError("payload does not match Git object ID")
    if sha256_hex(payload) != content_sha256:
        raise ValueError("payload does not match content SHA-256")
    return {
        "proofId": proof_id,
        "repository": repository,
        "commit": commit,
        "path": path,
        "gitObjectId": git_object_id,
        "contentSha256": content_sha256,
    }


def _claims(document: dict[str, object]) -> tuple[list[dict[str, object]], int]:
    raw_facts = document.get("facts")
    if not isinstance(raw_facts, list) or not raw_facts:
        return [], 0
    facts: list[dict[str, object]] = []
    specificity = 0
    for raw_fact in raw_facts:
        if not isinstance(raw_fact, dict):
            return [], 0
        normalized = {
            "factId": raw_fact.get("factId", raw_fact.get("fact_id")),
            "conceptId": raw_fact.get("conceptId", raw_fact.get("concept_id")),
            "outboundText": raw_fact.get("outboundText", raw_fact.get("outbound_text")),
        }
        try:
            fact = {
                key: _require_text(value, "fact.{}".format(key))
                for key, value in normalized.items()
            }
        except ValueError:
            return [], 0
        facts.append(fact)
        specificity += len(str(fact["outboundText"]).split())
    return facts, specificity


def _candidate(
    document: dict[str, object], payload: bytes, provenance: dict[str, object], generated_at: str
) -> dict[str, object]:
    source = _source_ref(provenance, payload)
    extracted_document = _strict_json(payload, "proof source")
    if document != extracted_document:
        raise ValueError(
            "caller document does not match the verified exact extracted bytes"
        )
    document = extracted_document
    document_identity = _validate_document_schema(document)
    if source["proofId"] != document_identity:
        raise ValueError("provenance proofId does not match document identity")
    generated = parse_timestamp(generated_at, "generated_at")
    verified_value = document.get("verifiedAt", document.get("verified_at"))
    verified = parse_timestamp(verified_value, "verifiedAt")
    facts, specificity = _claims(document)
    permission = document.get("permission")
    permission_state = "missing"
    reason: Optional[str] = None
    permission_rank = 1
    permission_evidence_ref: Optional[str] = None
    permission_evidence_sha256: Optional[str] = None

    if permission is None:
        reason = "permission_missing"
    elif not isinstance(permission, dict):
        reason = "permission_missing"
    else:
        permission_state = str(permission.get("status", "missing"))
        if permission_state == "internal-only":
            reason = "permission_internal_only"
        elif permission_state not in _ALLOWED_PERMISSION:
            reason = "permission_missing"
        else:
            permission_rank = 0
            evidence_ref = provenance.get("permissionEvidenceRef")
            evidence_sha = provenance.get("permissionEvidenceSha256")
            try:
                permission_evidence_ref = _require_text(
                    evidence_ref, "permission.evidenceRef"
                )
                if permission_evidence_ref != "/permission":
                    raise ValueError(
                        "permission.evidenceRef must point to /permission"
                    )
                permission_evidence_sha256 = _require_hash(
                    evidence_sha, 64, "permission.evidenceSha256"
                )
            except ValueError:
                reason = "permission_missing"
            else:
                if sha256_hex(canonical_bytes(permission)) != permission_evidence_sha256:
                    raise ValueError("permission evidence SHA-256 mismatch")
            expires_value = permission.get("expiresAt")
            try:
                expires = parse_timestamp(expires_value, "permission.expiresAt")
            except ValueError:
                reason = "permission_expired"
            else:
                if expires <= generated:
                    reason = "permission_expired"

    if not facts:
        reason = "claim_bindings_missing"
    elif document.get("activeProspectConflict") is True:
        reason = "active_prospect_conflict"
    elif document.get("activeEmployerConflict") is True:
        reason = "active_employer_conflict"
    elif document.get("protectedInternalPremise") is True:
        reason = "protected_internal_premise"
    if verified > generated:
        reason = "verified_at_future"

    return {
        "document": document,
        "source": source,
        "facts": facts,
        "specificity": specificity,
        "verified": verified,
        "permissionRank": permission_rank,
        "permissionState": permission_state,
        "permissionEvidenceRef": permission_evidence_ref,
        "permissionEvidenceSha256": permission_evidence_sha256,
        "failureReason": reason,
    }


def select_build_proof(
    candidates: Sequence[
        tuple[dict[str, object], bytes, dict[str, object]]
    ],
    *,
    generated_at: str,
) -> dict[str, object]:
    """Select one build-proof source using the closed deterministic order."""

    parse_timestamp(generated_at, "generated_at")
    if not candidates:
        return _missing_mode("build_proof")
    evaluated_raw = [
        _candidate(document, payload, provenance, generated_at)
        for document, payload, provenance in candidates
    ]
    evaluated: list[dict[str, object]] = []
    seen_proof_ids: dict[str, bytes] = {}
    for item in evaluated_raw:
        source = item["source"]
        assert isinstance(source, dict)
        proof_id = str(source["proofId"])
        source_bytes = canonical_bytes(source)
        prior = seen_proof_ids.get(proof_id)
        if prior is not None:
            if prior != source_bytes:
                raise ValueError("duplicate proofId has different immutable source")
            continue
        seen_proof_ids[proof_id] = source_bytes
        evaluated.append(item)
    admissible_or_permission_gap = [
        item
        for item in evaluated
        if item["failureReason"] in {None, "permission_missing"}
    ]
    ranked = admissible_or_permission_gap or evaluated
    ranked.sort(
        key=lambda item: (
            int(item["permissionRank"]),
            -int(item["specificity"]),
            -item["verified"].timestamp(),
            str(item["source"]["proofId"]),
        )
    )
    selected = ranked[0]
    source = selected["source"]
    assert isinstance(source, dict)
    reason = selected["failureReason"]
    result: dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "fixtureId": str(source["proofId"]),
        "mode": "build_proof",
        "classification": "positive" if reason is None else "gap",
        "sourceRefs": [source],
        "gitObjectId": source["gitObjectId"],
        "contentSha256": source["contentSha256"],
        "permissionState": selected["permissionState"],
        "expectedGateResult": "accept" if reason is None else "block",
        "claimBindings": selected["facts"],
    }
    if reason is None:
        result["permissionEvidenceRef"] = selected["permissionEvidenceRef"]
        result["permissionEvidenceSha256"] = selected["permissionEvidenceSha256"]
    else:
        result["failureReason"] = reason
    return result


def _missing_mode(mode: str) -> dict[str, object]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "fixtureId": "{}-evidence-gap".format(mode),
        "mode": mode,
        "classification": "gap",
        "sourceRefs": [],
        "gitObjectId": None,
        "contentSha256": None,
        "permissionState": "not_applicable",
        "expectedGateResult": "block",
        "failureReason": "evidence_missing",
        "claimBindings": [],
    }


def build_decagon_negative_fixture(workspace_root: Path) -> dict[str, object]:
    """Rebuild the canonical negative fixture from the exact reviewed packet."""

    path = Path(workspace_root) / DECAGON_PACKET_PATH
    payload = path.read_bytes()
    if sha256_hex(payload) != DECAGON_CONTENT_SHA256:
        raise ValueError("Decagon packet exact byte SHA-256 mismatch")
    if _git_blob_id(payload) != DECAGON_BLOB_ID:
        raise ValueError("Decagon packet Git object ID mismatch")
    packet = _strict_json(payload, "Decagon packet")
    if packet.get("payloadHash") != DECAGON_PAYLOAD_HASH:
        raise ValueError("Decagon packet payloadHash mismatch")
    source = {
        "proofId": "decagon-approval-is-not-execution",
        "repository": "workspace",
        "commit": DECAGON_SOURCE_COMMIT,
        "path": DECAGON_PACKET_PATH,
        "gitObjectId": DECAGON_BLOB_ID,
        "contentSha256": DECAGON_CONTENT_SHA256,
    }
    return {
        "schemaVersion": SCHEMA_VERSION,
        "fixtureId": "decagon-approval-is-not-execution",
        "mode": "internal_machinery",
        "classification": "negative",
        "sourceRefs": [source],
        "gitObjectId": DECAGON_BLOB_ID,
        "contentSha256": DECAGON_CONTENT_SHA256,
        "payloadHash": DECAGON_PAYLOAD_HASH,
        "permissionState": "prohibited",
        "expectedGateResult": "reject",
        "failureReason": "protected_internal_premise",
        "claimBindings": [],
    }


def _negative_fixture(
    workspace_root: Path, *, runner: _Runner = subprocess.run
) -> dict[str, object]:
    payload = (Path(workspace_root) / DECAGON_PACKET_PATH).read_bytes()
    committed_payload = extract_git_object(
        Path(workspace_root) / ".git",
        DECAGON_SOURCE_COMMIT,
        DECAGON_PACKET_PATH,
        DECAGON_BLOB_ID,
        runner=runner,
    )
    if committed_payload != payload:
        raise ValueError("Decagon working-tree bytes differ from declared Git object")
    return build_decagon_negative_fixture(workspace_root)


def build_evaluation_fixtures(
    workspace_root: Path,
    jt_ops_git_dir: Path,
    *,
    generated_at: str,
    runner: _Runner = subprocess.run,
) -> list[dict[str, object]]:
    """Build the deterministic pre-human-gate Program 0 fixture set."""

    parse_timestamp(generated_at, "generated_at")
    payload = extract_git_object(
        Path(jt_ops_git_dir),
        PRE_GATE_COMMIT,
        PRE_GATE_PATH,
        PRE_GATE_BLOB_ID,
        runner=runner,
    )
    if sha256_hex(payload) != PRE_GATE_CONTENT_SHA256:
        raise ValueError("pre-gate proof exact byte SHA-256 mismatch")
    document = _strict_json(payload, "pre-gate proof")
    proof_id = str(document.get("card_id", "cohort-two-coi-proof-v1"))
    provenance = {
        "proofId": proof_id,
        "repository": "jt-ops",
        "commit": PRE_GATE_COMMIT,
        "path": PRE_GATE_PATH,
        "gitObjectId": PRE_GATE_BLOB_ID,
        "contentSha256": PRE_GATE_CONTENT_SHA256,
    }
    return [
        _negative_fixture(Path(workspace_root), runner=runner),
        select_build_proof(
            [(document, payload, provenance)], generated_at=generated_at
        ),
        _missing_mode("company_teardown"),
        _missing_mode("ai_news"),
    ]
