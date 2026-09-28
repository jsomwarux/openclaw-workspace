"""Governed Task 7B ingestion and deterministic phase-two rebuild helpers."""

from __future__ import annotations

import argparse
import json
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath
from typing import Optional, Sequence

from scripts.linkedin_content_os.canonical import (
    _append_jsonl_exact_prefix_locked,
    _exclusive_path_lock,
    _write_bytes_atomic,
    canonical_bytes,
    read_jsonl,
    sha256_hex,
    write_json_atomic,
)
from scripts.linkedin_content_os.contracts import (
    DECLINE_REASON,
    parse_timestamp,
    validate_event,
    validate_linkedin_url,
)
from scripts.linkedin_content_os.fixtures import (
    _git_blob_id,
    _strict_json,
    _validate_document_schema,
    select_build_proof,
)
from scripts.linkedin_content_os.focus import (
    AUTHORITY_RECEIPT_SCHEMA_VERSION,
    HUMAN_GATE_PACKET_ID,
    apply_focus_decision,
    build_focus_snapshot,
    validate_focus_snapshot,
)
from scripts.linkedin_content_os.historical_audit import corpus_run_id
from scripts.linkedin_content_os.outcomes import load_events, validate_event_sequence


_HASH = re.compile(r"^[0-9a-f]{64}$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_RESPONSE_FIELDS = {
    "schemaVersion", "recoveryRequestSha256", "focusSnapshotSha256",
    "fixtureGapSha256", "focusDecision", "historyAnswers",
    "permissionedFixture", "confirmedAt",
}
_PERMISSION_FIXTURE_FIELDS = {
    "proofId", "gitDir", "commit", "path", "contentSha256",
    "permissionEvidenceRef", "permissionEvidenceSha256", "permissionStatus",
}
_REQUEST_FIELDS = {"schemaVersion", "generatedAt", "sourceSha256", "items"}
_REQUEST_ITEM_FIELDS = {
    "legacyRowSha256", "date", "topic", "allowedAnswers",
}
_ALLOWED_ANSWERS = [
    {"answer": "posted", "required": ["publicUrl"], "optional": ["finalText"]},
    {
        "answer": "not_posted", "required": ["declineReason"],
        "allowedDeclineReasons": ["quality_fit", "stale", "timing", "other"],
    },
    {"answer": "still_unknown", "required": []},
]
_PERMISSION_STATUS = {"approved-anonymized", "approved-named"}
_RUN_CONTEXT_FIELDS = {"schemaVersion", "runId", "generatedAt"}


def _require_object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("{} must be an object".format(label))
    return value


def _exact_fields(value: object, expected: set[str], label: str) -> dict[str, object]:
    result = _require_object(value, label)
    missing = expected - set(result)
    unknown = set(result) - expected
    if missing:
        raise ValueError("{} missing fields: {}".format(label, sorted(missing)))
    if unknown:
        raise ValueError("{} unknown fields: {}".format(label, sorted(unknown)))
    return result


def _reject_nulls(value: object, label: str) -> None:
    if value is None:
        raise ValueError("{} must not be null".format(label))
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_nulls(item, "{}.{}".format(label, key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nulls(item, "{}[{}]".format(label, index))


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError("{} must be non-empty trimmed text".format(label))
    return value


def _require_hash(value: object, label: str) -> str:
    text = _require_text(value, label)
    if _HASH.fullmatch(text) is None:
        raise ValueError("{} must be 64 lowercase hexadecimal characters".format(label))
    return text


def _hash_object(value: object) -> str:
    return sha256_hex(canonical_bytes(value))


def _event(
    event_id: str,
    packet_id: str,
    event_type: str,
    recorded_at: str,
    response_hash: str,
    payload: dict[str, object],
) -> dict[str, object]:
    source_type = (
        "corpus_authority_verifier"
        if event_type == "corpus_authority_receipt"
        else "jt_human_gate_response"
    )
    value: dict[str, object] = {
        "schemaVersion": "linkedin-content-outcome.v1",
        "outcomeEventId": event_id,
        "packetId": packet_id,
        "eventType": event_type,
        "recordedAt": recorded_at,
        "sourcePointer": {
            "sourceType": source_type,
            "sourceId": "sha256:" + response_hash,
            "sourceSha256": response_hash,
        },
        "payload": payload,
    }
    value["eventSha256"] = _hash_object(value)
    return validate_event(value)


def _validate_request(request_value: object) -> dict[str, object]:
    request = _exact_fields(request_value, _REQUEST_FIELDS, "recovery request")
    if request["schemaVersion"] != "linkedin-historical-recovery-request.v1":
        raise ValueError("unsupported recovery request schemaVersion")
    parse_timestamp(request["generatedAt"], "recoveryRequest.generatedAt")
    _require_hash(request["sourceSha256"], "recoveryRequest.sourceSha256")
    items = request["items"]
    if not isinstance(items, list) or not items:
        raise ValueError("recovery request items must be a non-empty list")
    seen: set[str] = set()
    for index, raw in enumerate(items):
        item = _exact_fields(raw, _REQUEST_ITEM_FIELDS, "recovery request item")
        row_hash = _require_hash(item["legacyRowSha256"], "legacyRowSha256")
        if row_hash in seen:
            raise ValueError("recovery request has duplicate legacy row")
        seen.add(row_hash)
        _require_text(item["date"], "recovery request date")
        _require_text(item["topic"], "recovery request topic")
        if item["allowedAnswers"] != _ALLOWED_ANSWERS:
            raise ValueError("recovery request allowed answers are not closed")
    return request


def _validate_run_context(value: object) -> dict[str, object]:
    context = _exact_fields(value, _RUN_CONTEXT_FIELDS, "run context")
    if context["schemaVersion"] != "linkedin-program-0-run-context.v1":
        raise ValueError("unsupported run context schemaVersion")
    parse_timestamp(context["generatedAt"], "runContext.generatedAt")
    unsigned = {
        "schemaVersion": context["schemaVersion"],
        "generatedAt": context["generatedAt"],
    }
    if context["runId"] != "sha256:" + _hash_object(unsigned):
        raise ValueError("run context runId mismatch")
    return context


def _validate_focus_decision(
    response: dict[str, object],
    focus: dict[str, object],
    workspace_root: Path,
) -> tuple[dict[str, object], Optional[str]]:
    validate_focus_snapshot(focus, workspace_root)
    decision = _require_object(response["focusDecision"], "focusDecision")
    proposal_hash = str(focus["snapshotId"])
    if not proposal_hash.startswith("sha256:"):
        raise ValueError("focus snapshotId is malformed")
    payload: dict[str, object] = {
        "decision": decision.get("decision"),
        "focusSnapshotSha256": proposal_hash[len("sha256:"):],
    }
    replacement_hash: Optional[str] = None
    if decision.get("decision") == "confirmed":
        _exact_fields(decision, {"decision"}, "focusDecision")
    elif decision.get("decision") == "corrected":
        _exact_fields(decision, {"decision", "correctedTargets"}, "focusDecision")
        targets = decision["correctedTargets"]
        if not isinstance(targets, list) or not targets:
            raise ValueError("corrected focus requires a full non-empty target list")
        replacement = build_focus_snapshot(
            workspace_root,
            targets,
            generated_at=str(focus["generatedAt"]),
        )
        replacement_hash = str(replacement["snapshotId"])[len("sha256:"):]
        payload["replacementFocusSnapshotSha256"] = replacement_hash
    else:
        raise ValueError("unsupported focusDecision")
    return payload, replacement_hash


def _safe_repo_path(value: object) -> str:
    text = _require_text(value, "permissionedFixture.path")
    path = PurePosixPath(text)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("permissionedFixture.path must be a safe repository-relative path")
    return text


def _validated_git_dir(value: object) -> Path:
    text = _require_text(value, "permissionedFixture.gitDir")
    path = Path(text)
    if not path.is_absolute():
        raise ValueError("permissionedFixture.gitDir must be absolute")
    try:
        current = Path(path.anchor)
        for part in path.parts[1:]:
            current = current / part
            item = current.lstat()
            if stat.S_ISLNK(item.st_mode):
                raise ValueError("permissionedFixture.gitDir must not traverse symlinks")
        if not stat.S_ISDIR(path.stat().st_mode):
            raise ValueError("permissionedFixture.gitDir must be a directory")
    except OSError as error:
        raise ValueError("permissionedFixture.gitDir is unavailable") from error
    if ".git" not in path.parts:
        raise ValueError("permissionedFixture.gitDir must identify Git metadata")
    return path


def _extract_permission_fixture(
    raw_fixture: object,
    confirmed_at: str,
) -> tuple[dict[str, object], bytes, dict[str, object], str]:
    fixture = _exact_fields(
        raw_fixture, _PERMISSION_FIXTURE_FIELDS, "permissionedFixture"
    )
    proof_id = _require_text(fixture["proofId"], "permissionedFixture.proofId")
    git_dir = _validated_git_dir(fixture["gitDir"])
    commit = _require_text(fixture["commit"], "permissionedFixture.commit")
    if _COMMIT.fullmatch(commit) is None:
        raise ValueError("permissionedFixture.commit must be 40 lowercase hexadecimal characters")
    path = _safe_repo_path(fixture["path"])
    content_hash = _require_hash(
        fixture["contentSha256"], "permissionedFixture content SHA-256"
    )
    pointer = _require_text(
        fixture["permissionEvidenceRef"], "permissionEvidenceRef"
    )
    if pointer != "/permission":
        raise ValueError("permissionEvidenceRef must be /permission")
    permission_hash = _require_hash(
        fixture["permissionEvidenceSha256"], "permission evidence SHA-256"
    )
    status = _require_text(fixture["permissionStatus"], "permissionStatus")
    if status not in _PERMISSION_STATUS:
        raise ValueError("unsupported permissionStatus")
    result = subprocess.run(
        ["git", "--git-dir", str(git_dir), "show", "{}:{}".format(commit, path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0 or not isinstance(result.stdout, bytes):
        raise ValueError("Git permission evidence extraction failed")
    payload = result.stdout
    if sha256_hex(payload) != content_hash:
        raise ValueError("extracted bytes do not match content SHA-256")
    document = _strict_json(payload, "permissioned proof")
    if _validate_document_schema(document) != proof_id:
        raise ValueError("permissioned proof identity mismatch")
    permission = _require_object(document.get("permission"), "permission evidence")
    if _hash_object(permission) != permission_hash:
        raise ValueError("permission evidence SHA-256 mismatch")
    if permission.get("status") != status:
        raise ValueError("permissionStatus does not match immutable evidence")
    expires_at = _require_text(permission.get("expiresAt"), "permission.expiresAt")
    if parse_timestamp(expires_at, "permission.expiresAt") <= parse_timestamp(
        confirmed_at, "confirmedAt"
    ):
        raise ValueError("permission expiry must be strictly after confirmedAt")
    provenance = {
        "proofId": proof_id,
        "repository": str(git_dir),
        "commit": commit,
        "path": path,
        "gitObjectId": _git_blob_id(payload),
        "contentSha256": content_hash,
        "permissionEvidenceRef": pointer,
        "permissionEvidenceSha256": permission_hash,
    }
    return document, payload, provenance, expires_at


def _validate_answers(
    response: dict[str, object], request: dict[str, object]
) -> list[dict[str, object]]:
    answers = response["historyAnswers"]
    if not isinstance(answers, list) or not answers:
        raise ValueError("history answer coverage is empty")
    requested = [str(item["legacyRowSha256"]) for item in request["items"]]  # type: ignore[index]
    seen: set[str] = set()
    validated: dict[str, dict[str, object]] = {}
    for raw in answers:
        answer = _require_object(raw, "history answer")
        row_hash = _require_hash(answer.get("legacyRowSha256"), "legacyRowSha256")
        if row_hash in seen:
            raise ValueError("duplicate history answer")
        seen.add(row_hash)
        kind = answer.get("answer")
        if kind == "posted":
            expected = {"legacyRowSha256", "answer", "publicUrl"}
            if "finalText" in answer:
                expected.add("finalText")
            _exact_fields(answer, expected, "posted history answer")
            validate_linkedin_url(answer["publicUrl"])
            if "finalText" in answer:
                _require_text(answer["finalText"], "finalText")
        elif kind == "not_posted":
            _exact_fields(
                answer,
                {"legacyRowSha256", "answer", "declineReason"},
                "not_posted history answer",
            )
            if answer["declineReason"] not in DECLINE_REASON:
                raise ValueError("unsupported declineReason")
        elif kind == "still_unknown":
            _exact_fields(
                answer, {"legacyRowSha256", "answer"}, "still_unknown history answer"
            )
        else:
            raise ValueError("unsupported history answer")
        validated[row_hash] = answer
    if seen != set(requested) or len(answers) != len(requested):
        raise ValueError("history answer coverage does not exactly match request")
    return [validated[row_hash] for row_hash in requested]


def _canonical_ledger_rows(path: Path) -> tuple[list[dict[str, object]], bytes]:
    if not path.exists():
        return [], b""
    rows = read_jsonl(path)
    canonical = b"".join(canonical_bytes(row) + b"\n" for row in rows)
    exact = path.read_bytes()
    if exact != canonical:
        raise ValueError("outcome ledger must be strict canonical JSONL")
    for row in rows:
        validate_event(row)
    validate_event_sequence(rows)
    return rows, exact


def _append_batch(
    path: Path, new_events: Sequence[dict[str, object]]
) -> tuple[int, int, bytes, list[dict[str, object]]]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _exclusive_path_lock(path):
        existing, original = _canonical_ledger_rows(path)
        by_id = {str(event["outcomeEventId"]): event for event in existing}
        appended: list[dict[str, object]] = []
        replayed = 0
        for event in new_events:
            prior = by_id.get(str(event["outcomeEventId"]))
            if prior is not None:
                if prior != event or prior["eventSha256"] != event["eventSha256"]:
                    raise ValueError("outcome event conflict: ID reused with different bytes")
                replayed += 1
                continue
            by_id[str(event["outcomeEventId"])] = event
            appended.append(event)
        combined = existing + appended
        validate_event_sequence(combined)
        latest_by_packet: dict[str, object] = {}
        for event in combined:
            timestamp = parse_timestamp(event["recordedAt"], "recordedAt")
            packet = str(event["packetId"])
            prior = latest_by_packet.get(packet)
            if prior is not None and timestamp < prior:
                raise ValueError("per-packet timestamp regression")
            latest_by_packet[packet] = timestamp
        expected = original
        try:
            for event in appended:
                _append_jsonl_exact_prefix_locked(path, event, expected_prefix=expected)
                expected += canonical_bytes(event) + b"\n"
        except Exception:
            if original:
                _write_bytes_atomic(path, original)
            else:
                path.unlink(missing_ok=True)
            raise
        return len(appended), replayed, expected, combined


def _focus_receipt(
    response: dict[str, object], focus: dict[str, object], focus_event: dict[str, object],
    ledger_bytes: bytes, ledger_position: int, replacement_hash: Optional[str],
) -> dict[str, object]:
    receipt: dict[str, object] = {
        "schemaVersion": AUTHORITY_RECEIPT_SCHEMA_VERSION,
        "rawResponseSha256": _hash_object(response),
        "recoveryRequestSha256": response["recoveryRequestSha256"],
        "fixtureGapSha256": response["fixtureGapSha256"],
        "focusDecisionEventSha256": focus_event["eventSha256"],
        "ledgerPrefixSha256": sha256_hex(ledger_bytes),
        "ledgerPosition": ledger_position,
        "validatedAt": response["confirmedAt"],
        "originalProposalSha256": str(focus["snapshotId"])[len("sha256:"):],
        "focusDecision": response["focusDecision"],
    }
    if replacement_hash is not None:
        receipt["replacementProposalSha256"] = replacement_hash
    receipt["receiptSha256"] = _hash_object(receipt)
    return receipt


def ingest_human_gate(
    response: object,
    request: object,
    focus: object,
    fixture_gap: object,
    ledger: Path,
    *,
    run_context: Optional[object] = None,
    workspace_root: Path = Path("."),
) -> dict[str, object]:
    """Validate and append one complete human-gate boundary deterministically."""

    response_value = _exact_fields(response, _RESPONSE_FIELDS, "human-gate response")
    _reject_nulls(response_value, "human-gate response")
    if response_value["schemaVersion"] != "linkedin-human-gate-response.v1":
        raise ValueError("unsupported human-gate response schemaVersion")
    confirmed_at = _require_text(response_value["confirmedAt"], "confirmedAt")
    parse_timestamp(confirmed_at, "confirmedAt")
    request_value = _validate_request(request)
    focus_value = _require_object(focus, "focus snapshot")
    gap_value = _require_object(fixture_gap, "fixture gap")
    expected_hashes = (
        ("recovery request", response_value["recoveryRequestSha256"], request_value),
        ("focus snapshot", response_value["focusSnapshotSha256"], focus_value),
        ("fixture gap", response_value["fixtureGapSha256"], gap_value),
    )
    for label, supplied, value in expected_hashes:
        if _require_hash(supplied, label + " SHA-256") != _hash_object(value):
            raise ValueError("{} SHA-256 mismatch".format(label))
    if (
        gap_value.get("classification") != "gap"
        or gap_value.get("mode") != "build_proof"
        or gap_value.get("failureReason") != "permission_missing"
    ):
        raise ValueError("fixture gap is not the permission-missing build proof")
    context = _validate_run_context(
        run_context
        if run_context is not None
        else {
            "schemaVersion": "linkedin-program-0-run-context.v1",
            "generatedAt": confirmed_at,
            "runId": "sha256:" + _hash_object({
                "schemaVersion": "linkedin-program-0-run-context.v1",
                "generatedAt": confirmed_at,
            }),
        }
    )
    confirmed_instant = parse_timestamp(confirmed_at, "confirmedAt")
    if confirmed_instant < parse_timestamp(
        focus_value.get("generatedAt"), "focus.generatedAt"
    ):
        raise ValueError("confirmedAt predates the focus proposal")
    if parse_timestamp(context["generatedAt"], "runContext.generatedAt") < confirmed_instant:
        raise ValueError("phase-two run context predates confirmedAt")
    focus_payload, replacement_hash = _validate_focus_decision(
        response_value, focus_value, Path(workspace_root)
    )
    answers = _validate_answers(response_value, request_value)
    document, proof_bytes, provenance, expires_at = _extract_permission_fixture(
        response_value["permissionedFixture"], confirmed_at
    )
    del document, proof_bytes
    response_hash = _hash_object(response_value)
    existing, existing_bytes = _canonical_ledger_rows(Path(ledger))
    planned_ids = {
        "history:" + str(answer["legacyRowSha256"])
        for answer in answers
    }
    planned_ids.update(
        "publication:" + str(answer["legacyRowSha256"])
        for answer in answers if answer["answer"] == "posted"
    )
    planned_ids.update(
        "authority:" + str(answer["legacyRowSha256"])
        for answer in answers
        if answer["answer"] == "posted" and "finalText" in answer
    )
    planned_ids.update({
        "focus:linkedin-program-0",
        "permission:" + str(provenance["proofId"]),
    })
    owned_positions = [
        index for index, event in enumerate(existing)
        if str(event["outcomeEventId"]) in planned_ids
    ]
    if owned_positions:
        first_owned = owned_positions[0]
        if owned_positions != list(range(first_owned, len(existing))):
            raise ValueError("human-gate replay events must be one exact ledger suffix")
        prefix_events = list(existing[:first_owned])
        prefix_bytes = b"".join(
            canonical_bytes(event) + b"\n" for event in prefix_events
        )
    else:
        prefix_events = list(existing)
        prefix_bytes = existing_bytes
    events: list[dict[str, object]] = []
    run_id = corpus_run_id(
        str(request_value["sourceSha256"]), str(context["generatedAt"])
    )

    for answer in answers:
        row_hash = str(answer["legacyRowSha256"])
        packet_id = "legacy:" + row_hash
        status = {
            "posted": "posted_confirmed",
            "not_posted": "not_posted_confirmed",
            "still_unknown": "status_unknown",
        }[str(answer["answer"])]
        history = _event(
            "history:" + row_hash, packet_id, "historical_status", confirmed_at,
            response_hash, {"legacyRowSha256": row_hash, "status": status},
        )
        events.append(history)
        prefix_events.append(history)
        prefix_bytes += canonical_bytes(history) + b"\n"
        if answer["answer"] != "posted":
            continue
        publication_payload: dict[str, object] = {"publicationUrl": answer["publicUrl"]}
        if "finalText" in answer:
            final_text = str(answer["finalText"])
            publication_payload.update({
                "finalText": final_text,
                "finalTextSha256": sha256_hex(final_text.encode("utf-8")),
            })
        publication = _event(
            "publication:" + row_hash, packet_id, "publication_acknowledged",
            confirmed_at, response_hash, publication_payload,
        )
        events.append(publication)
        prefix_events.append(publication)
        prefix_bytes += canonical_bytes(publication) + b"\n"
        if "finalText" not in answer:
            continue
        receipt_payload = {
            "authoritySourceType": "jt_human_gate_response",
            "authoritySourceId": "sha256:" + response_hash,
            "authoritySourceSha256": response_hash,
            "rawAuthoritySha256": response_hash,
            "runId": run_id,
            "textOutcomeEventId": publication["outcomeEventId"],
            "textOutcomeEventSha256": publication["eventSha256"],
            "ledgerPrefixSha256": sha256_hex(prefix_bytes),
            "ledgerPosition": len(prefix_events),
            "validatedAt": confirmed_at,
            "clientSensitiveMarkers": [],
        }
        authority = _event(
            "authority:" + row_hash, packet_id, "corpus_authority_receipt",
            confirmed_at, response_hash, receipt_payload,
        )
        events.append(authority)
        prefix_events.append(authority)
        prefix_bytes += canonical_bytes(authority) + b"\n"

    focus_event = _event(
        "focus:linkedin-program-0", HUMAN_GATE_PACKET_ID, "focus_decision",
        confirmed_at, response_hash, focus_payload,
    )
    events.append(focus_event)
    permission_event = _event(
        "permission:" + str(provenance["proofId"]),
        "proof:" + str(provenance["proofId"]),
        "permission_fixture_accepted",
        confirmed_at,
        response_hash,
        {
            "fixtureId": provenance["proofId"],
            "repository": provenance["repository"],
            "commitSha": provenance["commit"],
            "path": provenance["path"],
            "extractedSha256": provenance["contentSha256"],
            "permissionEvidenceSha256": provenance["permissionEvidenceSha256"],
            "permissionExpiresAt": expires_at,
        },
    )
    events.append(permission_event)
    appended, replayed, ledger_bytes, all_events = _append_batch(Path(ledger), events)
    by_id = {str(item["outcomeEventId"]): item for item in all_events}
    focus_event = by_id[str(focus_event["outcomeEventId"])]
    focus_receipt = _focus_receipt(
        response_value, focus_value, focus_event, ledger_bytes, len(all_events),
        replacement_hash,
    )
    authority_hashes = sorted(
        str(by_id[str(event["outcomeEventId"])]["eventSha256"])
        for event in events if event["eventType"] == "corpus_authority_receipt"
    )
    manifest: dict[str, object] = {
        "schemaVersion": "linkedin-corpus-authority-manifest.v1",
        "runId": run_id,
        "validatedAt": context["generatedAt"],
        "receiptSha256Allowlist": authority_hashes,
        "humanGateAuthorityReceiptSha256": response_hash,
        "ledgerPrefixSha256": sha256_hex(ledger_bytes),
        "ledgerPosition": len(all_events),
    }
    manifest["manifestSha256"] = _hash_object(manifest)
    authority_unsigned: dict[str, object] = {
        "schemaVersion": "linkedin-program-0-authority-run-context.v1",
        "generatedAt": context["generatedAt"],
        "corpusAuthorityManifestSha256": manifest["manifestSha256"],
    }
    authority_context = {
        **authority_unsigned,
        "runId": "sha256:" + _hash_object(authority_unsigned),
    }
    return {
        "schemaVersion": "linkedin-human-gate-ingestion.v1",
        "responseSha256": response_hash,
        "appendedEventCount": appended,
        "replayedEventCount": replayed,
        "events": [by_id[str(event["outcomeEventId"])] for event in events],
        "focusAuthorityReceipt": focus_receipt,
        "corpusAuthorityManifest": manifest,
        "authorityRunContext": authority_context,
    }


def _strict_json_file(path: Path) -> dict[str, object]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise ValueError("required artifact is unavailable: {}".format(path)) from error
    return _strict_json(payload, str(path))


def _phase1_fixture_rows(path: Path) -> list[dict[str, object]]:
    rows = read_jsonl(path)
    gaps = [
        row for row in rows
        if row.get("mode") == "build_proof"
        and row.get("classification") == "gap"
        and row.get("failureReason") == "permission_missing"
    ]
    if len(gaps) != 1:
        raise ValueError("phase-1 fixtures require exactly one permission gap")
    return rows


def ingest_human_gate_files(args: argparse.Namespace) -> dict[str, object]:
    response = _strict_json_file(Path(args.response))
    request = _strict_json_file(Path(args.recovery_request))
    focus = _strict_json_file(Path(args.focus))
    fixtures = _phase1_fixture_rows(Path(args.fixtures))
    fixture_gap = next(row for row in fixtures if row.get("mode") == "build_proof")
    context = _strict_json_file(Path(args.run_context))
    result = ingest_human_gate(
        response, request, focus, fixture_gap, Path(args.outcomes),
        run_context=context,
        workspace_root=Path(getattr(args, "workspace_root", ".")),
    )
    write_json_atomic(
        Path(args.corpus_authority_manifest_output),
        result["corpusAuthorityManifest"],
    )
    write_json_atomic(
        Path(args.authority_run_context_output), result["authorityRunContext"]
    )
    return result


def _phase1_paths(directory: Path) -> tuple[Path, Path, Path, Path]:
    return (
        directory / "human-gate-response.v1.json",
        directory / "historical-recovery-request.phase-1.v1.json",
        directory / "focus-snapshot.phase-1.v1.json",
        directory / "evaluation-fixtures.phase-1.v0.jsonl",
    )


def rebuild_focus_files(args: argparse.Namespace) -> dict[str, object]:
    output = Path(args.output)
    response_path, request_path, proposed_path, fixtures_path = _phase1_paths(output.parent)
    response = _strict_json_file(response_path)
    request = _strict_json_file(request_path)
    proposed = _strict_json_file(proposed_path)
    fixtures = _phase1_fixture_rows(fixtures_path)
    gap = next(row for row in fixtures if row.get("mode") == "build_proof")
    if response["recoveryRequestSha256"] != _hash_object(request):
        raise ValueError("recovery request SHA-256 mismatch")
    if response["focusSnapshotSha256"] != _hash_object(proposed):
        raise ValueError("focus snapshot SHA-256 mismatch")
    if response["fixtureGapSha256"] != _hash_object(gap):
        raise ValueError("fixture gap SHA-256 mismatch")
    events = load_events(Path(args.outcomes))
    response_hash = _hash_object(response)
    focus_events = [
        event for event in events
        if event["eventType"] == "focus_decision"
        and event["packetId"] == HUMAN_GATE_PACKET_ID
        and event["sourcePointer"]["sourceSha256"] == response_hash
    ]
    if len(focus_events) != 1:
        raise ValueError("ledger requires exactly one matching focus decision")
    focus_event = focus_events[0]
    response_positions = [
        index
        for index, event in enumerate(events)
        if event["sourcePointer"]["sourceSha256"] == response_hash
    ]
    if not response_positions:
        raise ValueError("ledger lacks the human-gate response event batch")
    ledger_position = max(response_positions) + 1
    ledger_prefix = b"".join(
        canonical_bytes(event) + b"\n" for event in events[:ledger_position]
    )
    replacement_hash = _require_object(focus_event["payload"], "focus payload").get(
        "replacementFocusSnapshotSha256"
    )
    receipt = _focus_receipt(
        response, proposed, focus_event, ledger_prefix, ledger_position,
        str(replacement_hash) if replacement_hash is not None else None,
    )
    confirmed = apply_focus_decision(
        proposed,
        focus_event,
        Path(args.workspace_root),
        authority_receipt=receipt,
        expected_authority_receipt_sha256=receipt["receiptSha256"],
    )
    write_json_atomic(output, confirmed)
    return confirmed


def rebuild_fixtures_files(args: argparse.Namespace) -> dict[str, object]:
    output = Path(args.output)
    response_path = Path(args.human_gate_response)
    response = _strict_json_file(response_path)
    phase1_path = response_path.parent / "evaluation-fixtures.phase-1.v0.jsonl"
    rows = _phase1_fixture_rows(phase1_path)
    confirmed_at = _require_text(response.get("confirmedAt"), "confirmedAt")
    document, payload, provenance, _ = _extract_permission_fixture(
        response.get("permissionedFixture"), confirmed_at
    )
    positive = select_build_proof(
        [(document, payload, provenance)], generated_at=confirmed_at
    )
    if positive.get("classification") != "positive":
        raise ValueError("permissioned fixture did not produce a positive fixture")
    rebuilt = [positive if row.get("mode") == "build_proof" else row for row in rows]
    payload_bytes = b"".join(canonical_bytes(row) + b"\n" for row in rebuilt)
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_bytes_atomic(output, payload_bytes)
    return {"schemaVersion": "linkedin-evaluation-fixture-set.v1", "fixtures": rebuilt}


__all__ = [
    "ingest_human_gate", "ingest_human_gate_files", "rebuild_fixtures_files",
    "rebuild_focus_files",
]
