#!/usr/bin/env python3
"""Compile Growth OS first-25 send readiness without network or send authority."""

from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import math
import os
import re
import shutil
import stat
import tempfile
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


SCHEMA_VERSION = "growth-os-send-readiness-v1"
DEFAULT_BATCH_ID = "growth-os-first25-m1-v2-2026-10-02"
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")
SECTION_RE = re.compile(r"^## (\d+)\. (.+), (.+)$", re.MULTILINE)
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

CONTACT_FIELDS = (
    "batch_position", "source_batch", "company", "domain",
    "employee_count_or_band", "buyer_name", "buyer_title", "email",
    "email_status", "geography", "evidence_ref", "suppression_status",
    "prior_contact_status", "review_verdict",
)
RECIPIENT_FIELDS = (
    "email", "mailbox_status", "mailbox_verified_at", "identity_status",
    "identity_checked_at", "suppression_observed", "suppression_status",
    "suppression_checked_at",
)
SENDER_FIELDS = (
    "sending_account", "account_type", "account_status", "dns_mx",
    "dns_spf", "dns_dkim", "dns_dmarc", "warmup_health_score",
    "warmup_days", "daily_campaign_limit", "sender_checked_at",
)
READINESS_FIELDS = (
    "schema_version", "batch_id", "row_id", "batch_position", "company",
    "buyer_name", "email", "copy_subject_sha256", "copy_body_sha256",
    "sending_account", "ready", "blocker_codes",
)
INSTANTLY_FIELDS = (
    "email", "first_name", "last_name", "company_name", "subject", "body",
    "sending_account", "row_id", "row_hash",
)
OUTCOME_FIELDS = (
    "schema_version", "batch_id", "row_id", "batch_position", "prospect_id",
    "company", "email_fingerprint", "candidate_subject_sha256",
    "candidate_body_sha256", "sending_account", "send_status", "sent_at",
    "vendor_message_id", "sent_subject_sha256", "sent_body_sha256",
    "delivery_status", "delivery_observed_at", "reply_classification",
    "reply_observed_at", "outcome_evidence_id", "next_action",
    "next_action_due_at",
)
EVENT_FIELDS = frozenset({
    "schemaVersion", "eventId", "batchId", "rowId", "vendorMessageId",
    "evidenceId", "sentAt", "finalSubject", "finalBody",
    "sentSubjectSha256", "sentBodySha256", "eventObservedAt",
})
PLATFORM_MAX = {"prewarmed": 25, "standard": 30, "airmail": 20}


class ReadinessError(ValueError):
    pass


@dataclass(frozen=True)
class Message:
    position: int
    buyer_name: str
    company: str
    email: str
    subject: str
    body: str
    signature: str


@dataclass
class ReadinessRow:
    contact: dict
    message: Message
    row_id: str
    blockers: List[str]
    sending_account: str = ""


@dataclass
class BatchResult:
    rows: List[ReadinessRow]
    sender_rejections: List[dict]
    eligible_senders: List[dict]
    batch_id: str
    as_of: datetime
    input_hashes: dict

    @property
    def ready(self) -> bool:
        return bool(self.rows) and all(not row.blockers for row in self.rows)


def canonical_json_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise ReadinessError("value is not canonical JSON") from exc


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _normalized_text(value: str) -> str:
    if not isinstance(value, str):
        raise ReadinessError("text value must be text")
    return " ".join(unicodedata.normalize("NFC", value).strip().split())


def normalized_email(value: str) -> str:
    result = _normalized_text(value).lower()
    if not EMAIL_RE.fullmatch(result):
        raise ReadinessError("email is invalid")
    return result


def canonical_company_name(value: str) -> str:
    """Normalize only punctuation and a terminal legal-entity suffix."""
    normalized = _normalized_text(value).casefold()
    normalized = re.sub(r"[,.]", "", normalized)
    normalized = re.sub(
        r"\s+(?:incorporated|inc|corporation|corp|limited|ltd|llc|l\.l\.c)$",
        "",
        normalized,
    )
    return _normalized_text(normalized)


def canonical_subject(value: str) -> str:
    return unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n").strip()


def canonical_body(message: Message) -> str:
    value = message.body + "\n\n" + message.signature
    value = unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in value.split("\n")).strip()


def subject_hash(message: Message) -> str:
    return sha256_bytes(canonical_subject(message.subject).encode("utf-8"))


def body_hash(message: Message) -> str:
    return sha256_bytes(canonical_body(message).encode("utf-8"))


def copy_hash(message: Message) -> str:
    return sha256_bytes(canonical_json_bytes({
        "body": canonical_body(message),
        "subject": canonical_subject(message.subject),
    }))


def parse_utc(value: str, label: str) -> datetime:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        raise ReadinessError(f"{label} must be RFC3339 UTC with Z")
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00").astimezone(timezone.utc)
    except ValueError as exc:
        raise ReadinessError(f"{label} is invalid") from exc


def format_utc(value: datetime) -> str:
    if value.tzinfo is None:
        raise ReadinessError("as-of must be timezone aware")
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _age_ok(raw: str, as_of: datetime, maximum: timedelta, label: str) -> bool:
    observed = parse_utc(raw, label)
    age = as_of - observed
    if age < timedelta(0):
        raise ReadinessError(f"{label} cannot be in the future")
    return age <= maximum


def parse_packet_text(text: str) -> List[Message]:
    matches = list(SECTION_RE.finditer(text))
    messages: List[Message] = []
    for index, match in enumerate(matches):
        block = text[match.end():matches[index + 1].start() if index + 1 < len(matches) else len(text)]
        to_match = re.search(r"^\*\*To:\*\* (.+)$", block, re.MULTILINE)
        subject_match = re.search(r"^\*\*Subject:\*\* (.+)$", block, re.MULTILINE)
        if to_match is None or subject_match is None:
            raise ReadinessError(f"packet message {match.group(1)} is incomplete")
        subject_end = subject_match.end()
        payload = block[subject_end:].lstrip("\n")
        signature = "JT Somwaru\nNew York City\njtsomwaru.com"
        marker = "\n\n" + signature
        if marker not in payload:
            raise ReadinessError(f"packet message {match.group(1)} signature is missing")
        body, _remainder = payload.split(marker, 1)
        messages.append(Message(
            position=int(match.group(1)),
            buyer_name=_normalized_text(match.group(2)),
            company=_normalized_text(match.group(3)),
            email=to_match.group(1).strip(),
            subject=subject_match.group(1).strip(),
            body=body.strip(),
            signature=signature,
        ))
    if not messages:
        raise ReadinessError("packet contains no messages")
    return messages


def parse_packet(path: Path) -> List[Message]:
    return parse_packet_text(path.read_text(encoding="utf-8"))


def read_csv(path: Path, expected_fields: Sequence[str]) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != tuple(expected_fields):
            raise ReadinessError(f"{path.name} fields are not exact")
        return [dict(row) for row in reader]


def row_id(batch_id: str, position: int) -> str:
    return f"{batch_id}:{position:02d}"


def prospect_id(email: str, company: str) -> str:
    raw = (
        b"growth-os-prospect-v1\0" + normalized_email(email).encode("utf-8")
        + b"\0" + _normalized_text(company).casefold().encode("utf-8")
    )
    return "prospect." + sha256_bytes(raw)[:20]


def email_fingerprint(email: str) -> str:
    return sha256_bytes(
        b"outreach-channel-v1\0direct_email\0" + normalized_email(email).encode("utf-8")
    )


def split_name(value: str) -> Tuple[str, str]:
    parts = _normalized_text(value).split(" ")
    return parts[0], " ".join(parts[1:])


def bind_contacts(contacts: Sequence[dict], messages: Sequence[Message], batch_id: str = DEFAULT_BATCH_ID) -> List[ReadinessRow]:
    if len(contacts) != len(messages):
        raise ReadinessError("contact and packet row counts differ")
    positions = [int(row["batch_position"]) for row in contacts]
    if sorted(positions) != list(range(1, len(contacts) + 1)) or len(set(positions)) != len(positions):
        raise ReadinessError("batch positions must be contiguous and unique")
    message_positions = [message.position for message in messages]
    if sorted(message_positions) != list(range(1, len(messages) + 1)) or len(set(message_positions)) != len(message_positions):
        raise ReadinessError("packet positions must be contiguous and unique")
    emails = [normalized_email(row["email"]) for row in contacts]
    if len(set(emails)) != len(emails):
        raise ReadinessError("duplicate email")
    companies = [_normalized_text(row["company"]).casefold() for row in contacts]
    if len(set(companies)) != len(companies):
        raise ReadinessError("duplicate company")
    by_position = {int(row["batch_position"]): row for row in contacts}
    message_by_position = {message.position: message for message in messages}
    bound: List[ReadinessRow] = []
    for position in sorted(by_position):
        contact = by_position[position]
        message = message_by_position[position]
        if normalized_email(contact["email"]) != normalized_email(message.email):
            raise ReadinessError(f"email mismatch at position {position}")
        if _normalized_text(contact["buyer_name"]).casefold() != _normalized_text(message.buyer_name).casefold():
            raise ReadinessError(f"buyer mismatch at position {position}")
        if canonical_company_name(contact["company"]) != canonical_company_name(message.company):
            raise ReadinessError(f"company mismatch at position {position}")
        bound.append(ReadinessRow(contact=dict(contact), message=message, row_id=row_id(batch_id, position), blockers=[]))
    return bound


def _validate_exact_keys(rows: Sequence[dict], fields: Sequence[str], label: str) -> None:
    expected = set(fields)
    for row in rows:
        if set(row) != expected:
            raise ReadinessError(f"{label} fields are not exact")


def _recipient_blockers(check: dict, as_of: datetime) -> List[str]:
    blockers: List[str] = []
    mailbox = check["mailbox_status"]
    if mailbox not in {"valid", "invalid", "unknown"}:
        raise ReadinessError("mailbox_status is invalid")
    if mailbox == "invalid": blockers.append("mailbox_invalid")
    if mailbox == "unknown": blockers.append("mailbox_unknown")
    if not _age_ok(check["mailbox_verified_at"], as_of, timedelta(hours=24), "mailbox_verified_at"):
        blockers.append("mailbox_verification_stale")
    identity = check["identity_status"]
    if identity not in {"verified", "mismatch", "unknown"}:
        raise ReadinessError("identity_status is invalid")
    if identity == "mismatch": blockers.append("identity_mismatch")
    if identity == "unknown": blockers.append("identity_unknown")
    if not _age_ok(check["identity_checked_at"], as_of, timedelta(days=7), "identity_checked_at"):
        blockers.append("identity_check_stale")
    observed = check["suppression_observed"]
    if observed not in {"true", "false"}:
        raise ReadinessError("suppression_observed is invalid")
    status = check["suppression_status"]
    if status not in {"clear", "blocked", "unknown"}:
        raise ReadinessError("suppression_status is invalid")
    if observed == "false": blockers.append("suppression_not_observed")
    if status == "blocked": blockers.append("suppression_blocked")
    if status == "unknown": blockers.append("suppression_unknown")
    if not _age_ok(check["suppression_checked_at"], as_of, timedelta(minutes=15), "suppression_checked_at"):
        blockers.append("suppression_check_stale")
    return sorted(set(blockers))


def _sender_reasons(sender: dict, as_of: datetime) -> List[str]:
    reasons: List[str] = []
    account = normalized_email(sender["sending_account"])
    if account == "jtsomwaru@gmail.com" or account.endswith("@jtsomwaru.com"):
        reasons.append("prohibited_sender")
    account_type = sender["account_type"]
    if account_type not in PLATFORM_MAX:
        raise ReadinessError("account_type is invalid")
    if sender["account_status"] not in {"active", "paused", "error"}:
        raise ReadinessError("account_status is invalid")
    if sender["account_status"] != "active": reasons.append("sender_inactive")
    for field in ("dns_mx", "dns_spf", "dns_dkim", "dns_dmarc"):
        value = sender[field]
        if value not in {"pass", "fail", "unknown"}:
            raise ReadinessError(f"{field} is invalid")
        if value != "pass": reasons.append(f"{field}_{value}")
    try:
        score = float(sender["warmup_health_score"])
        days = int(sender["warmup_days"])
        limit = int(sender["daily_campaign_limit"])
    except (TypeError, ValueError) as exc:
        raise ReadinessError("sender numeric field is invalid") from exc
    if not math.isfinite(score) or score < 0 or days < 0 or limit < 0:
        raise ReadinessError("sender numeric field is invalid")
    if score < 90: reasons.append("health_below_90")
    if account_type != "prewarmed" and days < 14: reasons.append("warmup_incomplete")
    if limit > PLATFORM_MAX[account_type]: reasons.append("limit_exceeds_policy")
    if not sender["sender_checked_at"]:
        reasons.append("sender_attestation_missing")
    elif not _age_ok(sender["sender_checked_at"], as_of, timedelta(hours=24), "sender_checked_at"):
        reasons.append("sender_attestation_stale")
    return sorted(set(reasons))


def compile_batch(
    contacts: Sequence[dict],
    messages: Sequence[Message],
    recipient_checks: Sequence[dict],
    senders: Sequence[dict],
    *,
    now: datetime,
    batch_id: str = DEFAULT_BATCH_ID,
    input_hashes: Optional[dict] = None,
) -> BatchResult:
    if now.tzinfo is None:
        raise ReadinessError("as-of must be timezone aware")
    _validate_exact_keys(recipient_checks, RECIPIENT_FIELDS, "recipient verification")
    _validate_exact_keys(senders, SENDER_FIELDS, "sender inventory")
    rows = bind_contacts(contacts, messages, batch_id=batch_id)
    checks: Dict[str, dict] = {}
    for check in recipient_checks:
        key = normalized_email(check["email"])
        if key in checks: raise ReadinessError("duplicate recipient verification")
        checks[key] = check
    for row in rows:
        check = checks.get(normalized_email(row.contact["email"]))
        if check is None:
            row.blockers.append("recipient_verification_missing")
        else:
            row.blockers.extend(_recipient_blockers(check, now))
    seen_senders = set()
    eligible: List[dict] = []
    rejections: List[dict] = []
    for sender in senders:
        key = normalized_email(sender["sending_account"])
        if key in seen_senders: raise ReadinessError("duplicate sending account")
        seen_senders.add(key)
        reasons = _sender_reasons(sender, now)
        if reasons:
            rejections.append({"sending_account": sender["sending_account"], "reasons": reasons})
        else:
            eligible.append(dict(sender))
    eligible.sort(key=lambda row: normalized_email(row["sending_account"]))
    remaining = {normalized_email(s["sending_account"]): min(int(s["daily_campaign_limit"]), 5) for s in eligible}
    candidates = [row for row in rows if not row.blockers]
    cursor = 0
    while candidates and any(value > 0 for value in remaining.values()):
        sender = eligible[cursor % len(eligible)] if eligible else None
        cursor += 1
        if sender is None: break
        key = normalized_email(sender["sending_account"])
        if remaining[key] <= 0: continue
        row = candidates.pop(0)
        row.sending_account = sender["sending_account"]
        remaining[key] -= 1
    for row in rows:
        if row.sending_account:
            continue
        if not eligible:
            row.blockers.append("no_eligible_sending_mailbox")
        elif not row.blockers:
            row.blockers.append("insufficient_sending_capacity")
        row.blockers = sorted(set(row.blockers))
    hashes = input_hashes or {
        "contactsCsvSha256": None,
        "packetMarkdownSha256": None,
        "recipientVerificationCsvSha256": None,
        "senderInventoryCsvSha256": None,
    }
    return BatchResult(rows, rejections, eligible, batch_id, now.astimezone(timezone.utc), hashes)


def _csv_bytes(fields: Sequence[str], rows: Iterable[Mapping[str, object]]) -> bytes:
    import io
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buffer.getvalue().encode("utf-8")


def _readiness_rows(result: BatchResult) -> List[dict]:
    output = []
    for row in result.rows:
        output.append({
            "schema_version": SCHEMA_VERSION,
            "batch_id": result.batch_id,
            "row_id": row.row_id,
            "batch_position": row.contact["batch_position"],
            "company": row.contact["company"],
            "buyer_name": row.contact["buyer_name"],
            "email": row.contact["email"],
            "copy_subject_sha256": subject_hash(row.message),
            "copy_body_sha256": body_hash(row.message),
            "sending_account": row.sending_account,
            "ready": "true" if not row.blockers else "false",
            "blocker_codes": ";".join(sorted(set(row.blockers))),
        })
    return output


def _outcome_rows(result: BatchResult) -> List[dict]:
    output = []
    for row in result.rows:
        output.append({
            "schema_version": SCHEMA_VERSION,
            "batch_id": result.batch_id,
            "row_id": row.row_id,
            "batch_position": row.contact["batch_position"],
            "prospect_id": prospect_id(row.contact["email"], row.contact["company"]),
            "company": row.contact["company"],
            "email_fingerprint": email_fingerprint(row.contact["email"]),
            "candidate_subject_sha256": subject_hash(row.message),
            "candidate_body_sha256": body_hash(row.message),
            "sending_account": row.sending_account,
            "send_status": "not_sent",
        })
    return output


def _instantly_rows(result: BatchResult) -> List[dict]:
    output = []
    for row in result.rows:
        first, last = split_name(row.contact["buyer_name"])
        core = {
            "schemaVersion": SCHEMA_VERSION,
            "row_id": row.row_id,
            "email": normalized_email(row.contact["email"]),
            "subject": canonical_subject(row.message.subject),
            "body": canonical_body(row.message),
            "sending_account": normalized_email(row.sending_account),
        }
        output.append({
            "email": row.contact["email"], "first_name": first, "last_name": last,
            "company_name": row.contact["company"], "subject": core["subject"],
            "body": core["body"], "sending_account": row.sending_account,
            "row_id": row.row_id, "row_hash": sha256_bytes(canonical_json_bytes(core)),
        })
    return output


def _fsync_write(path: Path, data: bytes) -> None:
    with path.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    written = 0
    while written < len(view):
        count = os.write(fd, view[written:])
        if count <= 0:
            raise ReadinessError("short write to reconciliation ledger")
        written += count


def _read_all(fd: int) -> bytes:
    chunks = []
    while True:
        chunk = os.read(fd, 65536)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    fd = os.open(str(path), flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _same_tree(left: Path, right: Path) -> bool:
    left_files = sorted(p.relative_to(left) for p in left.iterdir() if p.is_file())
    right_files = sorted(p.relative_to(right) for p in right.iterdir() if p.is_file())
    if left_files != right_files: return False
    return all((left / name).read_bytes() == (right / name).read_bytes() for name in left_files)


def write_outputs(result: BatchResult, output_root: Path, batch_id: Optional[str] = None) -> dict:
    if batch_id and batch_id != result.batch_id:
        result.batch_id = batch_id
        for row in result.rows:
            row.row_id = row_id(batch_id, int(row.contact["batch_position"]))
    root = output_root
    bundles = root / "bundles"
    bundles.mkdir(parents=True, exist_ok=True)
    as_of = format_utc(result.as_of)
    bundle_core = {"schemaVersion": SCHEMA_VERSION, "batchId": result.batch_id, "asOf": as_of, "inputHashes": result.input_hashes}
    bundle_id = sha256_bytes(canonical_json_bytes(bundle_core))
    staged = Path(tempfile.mkdtemp(prefix=".bundle-", dir=str(root)))
    readiness_data = _csv_bytes(READINESS_FIELDS, _readiness_rows(result))
    outcome_data = _csv_bytes(OUTCOME_FIELDS, _outcome_rows(result))
    counts = Counter(code for row in result.rows for code in row.blockers)
    summary = {
        "schemaVersion": SCHEMA_VERSION, "batchId": result.batch_id,
        "asOf": as_of, "generatedAt": as_of, "inputHashes": result.input_hashes,
        "rowCount": len(result.rows), "readyCount": sum(not row.blockers for row in result.rows),
        "blockedCount": sum(bool(row.blockers) for row in result.rows),
        "eligibleSenderCount": len(result.eligible_senders),
        "assignedCount": sum(bool(row.sending_account) for row in result.rows),
        "blockerCounts": dict(sorted(counts.items())), "ready": result.ready,
        "currentBundle": bundle_id,
    }
    _fsync_write(staged / "readiness.csv", readiness_data)
    _fsync_write(staged / "outcome-spine.csv", outcome_data)
    _fsync_write(staged / "summary.json", canonical_json_bytes(summary) + b"\n")
    instantly_path = None
    if result.ready:
        _fsync_write(staged / "instantly-import.csv", _csv_bytes(INSTANTLY_FIELDS, _instantly_rows(result)))
        instantly_path = f"bundles/{bundle_id}/instantly-import.csv"
    destination = bundles / bundle_id
    if destination.exists():
        if not _same_tree(staged, destination):
            shutil.rmtree(staged)
            raise ReadinessError("immutable bundle content mismatch")
        shutil.rmtree(staged)
    else:
        os.rename(staged, destination)
        _fsync_directory(destination)
        _fsync_directory(bundles)
    manifest = {
        "schemaVersion": SCHEMA_VERSION, "batchId": result.batch_id,
        "bundleId": bundle_id, "ready": result.ready,
        "summaryPath": f"bundles/{bundle_id}/summary.json",
        "readinessPath": f"bundles/{bundle_id}/readiness.csv",
        "outcomePath": f"bundles/{bundle_id}/outcome-spine.csv",
        "instantlyImportPath": instantly_path,
    }
    manifest_tmp = root / ".current.json.tmp"
    _fsync_write(manifest_tmp, canonical_json_bytes(manifest) + b"\n")
    os.replace(manifest_tmp, root / "current.json")
    _fsync_directory(root)
    return {
        "readiness_csv": destination / "readiness.csv",
        "summary_json": destination / "summary.json",
        "outcome_csv": destination / "outcome-spine.csv",
        "instantly_csv": destination / "instantly-import.csv" if result.ready else None,
        "manifest": root / "current.json",
    }


def _raw_hash(path: Optional[Path]) -> Optional[str]:
    return None if path is None else sha256_bytes(path.read_bytes())


def _event_core(event: dict) -> dict:
    return {key: value for key, value in event.items() if key != "eventId"}


def _validate_reconciliation_event(event: dict) -> None:
    if set(event) != EVENT_FIELDS:
        raise ReadinessError("reconciliation event fields are not exact")
    if event["schemaVersion"] != SCHEMA_VERSION:
        raise ReadinessError("reconciliation event schema is invalid")
    expected_id = sha256_bytes(canonical_json_bytes(_event_core(event)))
    if event["eventId"] != expected_id:
        raise ReadinessError("reconciliation event ID is invalid")
    if not event["vendorMessageId"] or not event["evidenceId"] or not event["finalSubject"] or not event["finalBody"]:
        raise ReadinessError("reconciliation event is incomplete")
    parse_utc(event["sentAt"], "sentAt")
    parse_utc(event["eventObservedAt"], "eventObservedAt")
    if event["sentSubjectSha256"] != sha256_bytes(canonical_subject(event["finalSubject"]).encode("utf-8")):
        raise ReadinessError("sent subject hash mismatch")
    final_body = "\n".join(line.rstrip() for line in event["finalBody"].replace("\r\n", "\n").replace("\r", "\n").split("\n")).strip()
    if event["sentBodySha256"] != sha256_bytes(final_body.encode("utf-8")):
        raise ReadinessError("sent body hash mismatch")


def _decode_reconciliation_events(raw: bytes) -> List[dict]:
    if raw and not raw.endswith(b"\n"):
        raise ReadinessError("reconciliation ledger has incomplete trailing bytes")
    events = []
    for line in raw.splitlines():
        try:
            event = json.loads(line.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ReadinessError("reconciliation ledger is malformed") from exc
        _validate_reconciliation_event(event)
        events.append(event)
    return events


def _read_reconciliation_ledger(ledger: Path) -> List[dict]:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(str(ledger), flags)
    except FileNotFoundError:
        return []
    try:
        fcntl.flock(fd, fcntl.LOCK_SH)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ReadinessError("reconciliation ledger path is unsafe")
        os.lseek(fd, 0, os.SEEK_SET)
        return _decode_reconciliation_events(_read_all(fd))
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def append_reconciliation_event(ledger: Path, event: dict) -> bool:
    _validate_reconciliation_event(event)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"): flags |= os.O_NOFOLLOW
    fd = os.open(str(ledger), flags, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ReadinessError("reconciliation ledger path is unsafe")
        os.lseek(fd, 0, os.SEEK_SET)
        existing = _decode_reconciliation_events(_read_all(fd))
        key = (event["batchId"], event["rowId"], event["vendorMessageId"])
        for prior in existing:
            prior_key = (prior["batchId"], prior["rowId"], prior["vendorMessageId"])
            if prior_key == key:
                if prior == event: return False
                raise ReadinessError("reconciliation event conflicts with existing event")
        os.lseek(fd, 0, os.SEEK_END)
        _write_all(fd, canonical_json_bytes(event) + b"\n")
        os.fsync(fd)
        return True
    finally:
        try: fcntl.flock(fd, fcntl.LOCK_UN)
        finally: os.close(fd)


def build_event(*, batch_id: str, row_id_value: str, vendor_message_id: str, evidence_id: str, sent_at: str, final_subject: str, final_body: str, event_observed_at: str) -> dict:
    body = "\n".join(line.rstrip() for line in final_body.replace("\r\n", "\n").replace("\r", "\n").split("\n")).strip()
    core = {
        "schemaVersion": SCHEMA_VERSION, "batchId": batch_id, "rowId": row_id_value,
        "vendorMessageId": vendor_message_id, "evidenceId": evidence_id,
        "sentAt": sent_at, "finalSubject": canonical_subject(final_subject),
        "finalBody": body,
        "sentSubjectSha256": sha256_bytes(canonical_subject(final_subject).encode("utf-8")),
        "sentBodySha256": sha256_bytes(body.encode("utf-8")),
        "eventObservedAt": event_observed_at,
    }
    return {**core, "eventId": sha256_bytes(canonical_json_bytes(core))}


def project_outcomes(seed_csv: Path, ledger: Path, output_csv: Path) -> None:
    seed = read_csv(seed_csv, OUTCOME_FIELDS)
    by_row = {row["row_id"]: dict(row) for row in seed}
    seen_events = {}
    for event in _read_reconciliation_ledger(ledger):
        key = (event["batchId"], event["rowId"], event["vendorMessageId"])
        prior = seen_events.get(key)
        if prior is not None:
            if prior == event:
                continue
            raise ReadinessError("reconciliation event conflicts with existing event")
        seen_events[key] = event
        row = by_row.get(event["rowId"])
        if row is None or row["batch_id"] != event["batchId"]:
            raise ReadinessError("reconciliation event does not bind to seed")
        if row["send_status"] == "sent" and row["vendor_message_id"] != event["vendorMessageId"]:
            raise ReadinessError("multiple sends for one row are unsupported in V1")
        row.update({
            "send_status": "sent", "sent_at": event["sentAt"],
            "vendor_message_id": event["vendorMessageId"],
            "sent_subject_sha256": event["sentSubjectSha256"],
            "sent_body_sha256": event["sentBodySha256"],
            "outcome_evidence_id": event["evidenceId"],
        })
    data = _csv_bytes(OUTCOME_FIELDS, sorted(by_row.values(), key=lambda row: int(row["batch_position"])))
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_csv.with_name("." + output_csv.name + ".tmp")
    _fsync_write(tmp, data)
    os.replace(tmp, output_csv)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contacts", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--recipient-verifications", type=Path)
    parser.add_argument("--senders", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--batch-id", default=DEFAULT_BATCH_ID)
    parser.add_argument("--expected-count", type=int, default=25)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    contacts = read_csv(args.contacts, CONTACT_FIELDS)
    messages = parse_packet(args.packet)
    if len(contacts) != args.expected_count or len(messages) != args.expected_count:
        raise ReadinessError("input count does not match expected count")
    recipient = [] if args.recipient_verifications is None else read_csv(args.recipient_verifications, RECIPIENT_FIELDS)
    senders = [] if args.senders is None else read_csv(args.senders, SENDER_FIELDS)
    hashes = {
        "contactsCsvSha256": _raw_hash(args.contacts),
        "packetMarkdownSha256": _raw_hash(args.packet),
        "recipientVerificationCsvSha256": _raw_hash(args.recipient_verifications),
        "senderInventoryCsvSha256": _raw_hash(args.senders),
    }
    result = compile_batch(
        contacts, messages, recipient, senders, now=parse_utc(args.as_of, "as-of"),
        batch_id=args.batch_id, input_hashes=hashes,
    )
    paths = write_outputs(result, args.output_root)
    print(canonical_json_bytes({
        "ready": result.ready, "rows": len(result.rows),
        "blocked": sum(bool(row.blockers) for row in result.rows),
        "manifest": str(paths["manifest"]),
    }).decode("utf-8"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ReadinessError, OSError, UnicodeError) as exc:
        print(f"send readiness failed: {exc}", file=os.sys.stderr)
        raise SystemExit(1)
