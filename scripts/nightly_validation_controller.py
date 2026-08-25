#!/usr/bin/env python3
"""Two-phase nightly validation admission, reconciliation, and task upsert."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


WORKSPACE = Path(__file__).resolve().parents[1]
APPROVED_EVIDENCE_ROOTS = tuple(
    (WORKSPACE / relative).resolve() for relative in (
        "memory/agent-portfolio/evidence",
    )
)
MC_TASKS_URL = "http://localhost:3000/api/tasks"
FRESHNESS_WINDOW = timedelta(hours=24)
REQUIRED_CANDIDATE_FIELDS = (
    "candidate_id", "lane", "score", "status", "not_before", "source_hash",
    "evidence_path", "evidence_timestamp",
)
REQUIRED_RESULT_FIELDS = (
    "candidateId", "sourceHash", "verdict", "verifierConfirmed", "verifiedAt",
    "score", "evidenceScore", "distributionScore", "fatalConstraint", "question",
    "sourcesChecked", "evidenceFound", "falsificationResult", "artifactPaths",
    "decision", "confidence", "nextTrigger", "title", "firstAction",
    "whyItMatters", "doneState", "workstream",
)
ALLOWED_CANDIDATE_STATUSES = {"pending", "archived", "blocked", "processed"}
ALLOWED_VERDICTS = {"promote", "continue", "archive", "blocked"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_WORKSTREAMS = {"paid-delivery", "career-hedge", "compounding-bet", "administrative", "other"}
PRIVATE_MARKERS = re.compile(
    r"client[-_ ]private|private conversation|confidential|authorization\s*:|bearer\s+|"
    r"\bapi[_ -]?key\b|\bsk-[a-z0-9_-]+",
    re.IGNORECASE,
)


class ControllerError(ValueError):
    pass


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def next_scheduled_run(now: datetime) -> datetime:
    local_zone = ZoneInfo("America/New_York")
    local_now = now.astimezone(local_zone)
    candidate = local_now.replace(hour=23, minute=15, second=0, microsecond=0)
    if candidate <= local_now:
        candidate += timedelta(days=1)
    return candidate.astimezone(timezone.utc)


def parse_timestamp(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ControllerError(f"invalid {field}: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ControllerError(f"invalid {field}: timezone required")
    return parsed.astimezone(timezone.utc)


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def approved_evidence_path(raw_path: str) -> Path | None:
    path = Path(raw_path)
    resolved = (WORKSPACE / path).resolve() if not path.is_absolute() else path.resolve()
    if not resolved.is_file():
        return None
    if not any(resolved == root or root in resolved.parents for root in APPROVED_EVIDENCE_ROOTS):
        return None
    return resolved


def require_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ControllerError(f"invalid {field}: nonempty string required")
    return value


def require_number(value: Any, field: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ControllerError(f"invalid {field}: number required")
    if not minimum <= value <= maximum:
        raise ControllerError(f"invalid {field}: must be between {minimum} and {maximum}")
    return value


def validate_evidence_file(raw_path: str, expected_hash: str | None = None) -> Path:
    path = approved_evidence_path(raw_path)
    if not path:
        raise ControllerError(f"evidence path outside approved public validation root: {raw_path}")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ControllerError(f"evidence must be UTF-8 public text: {raw_path}") from exc
    marker = PRIVATE_MARKERS.search(text)
    if marker:
        raise ControllerError(f"evidence contains private marker: {marker.group(0)}")
    if expected_hash is not None and file_hash(path) != expected_hash:
        raise ControllerError(f"evidence hash mismatch: {raw_path}")
    return path


def validate_candidate_schema(record: dict[str, Any], number: int | None = None,
                              check_evidence: bool = True) -> None:
    prefix = f"invalid candidate on line {number}:" if number is not None else "invalid candidate:"
    fields = set(record)
    required = set(REQUIRED_CANDIDATE_FIELDS)
    missing = [field for field in REQUIRED_CANDIDATE_FIELDS if field not in fields]
    extra = sorted(fields - required)
    if missing:
        raise ControllerError(f"{prefix} missing {missing[0]}")
    if extra:
        raise ControllerError(f"{prefix} unexpected field {extra[0]}")
    for field in ("candidate_id", "lane", "not_before", "source_hash",
                  "evidence_path", "evidence_timestamp", "status"):
        require_nonempty_string(record[field], field)
    require_number(record["score"], "score", 0, 100)
    if record["status"] not in ALLOWED_CANDIDATE_STATUSES:
        raise ControllerError(f"{prefix} invalid status")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", record["source_hash"]):
        raise ControllerError(f"{prefix} invalid source_hash")
    parse_timestamp(record["not_before"], "not_before")
    parse_timestamp(record["evidence_timestamp"], "evidence_timestamp")
    if check_evidence:
        validate_evidence_file(record["evidence_path"], record["source_hash"])


def validate_result_schema(result: dict[str, Any]) -> None:
    fields = set(result)
    required = set(REQUIRED_RESULT_FIELDS)
    missing = sorted(required - fields)
    extra = sorted(fields - required)
    if missing:
        raise ControllerError(f"invalid result: missing {missing[0]}")
    if extra:
        raise ControllerError(f"invalid result: unexpected field {extra[0]}")
    for field in ("candidateId", "sourceHash", "verifiedAt", "question", "evidenceFound",
                  "falsificationResult", "decision", "confidence", "nextTrigger", "title",
                  "firstAction", "whyItMatters", "doneState", "workstream", "verdict"):
        require_nonempty_string(result[field], field)
    if type(result["verifierConfirmed"]) is not bool:
        raise ControllerError("invalid verifierConfirmed: boolean required")
    if type(result["fatalConstraint"]) is not bool:
        raise ControllerError("invalid fatalConstraint: boolean required")
    require_number(result["score"], "score", 0, 40)
    require_number(result["evidenceScore"], "evidenceScore", 0, 5)
    require_number(result["distributionScore"], "distributionScore", 0, 5)
    for field in ("sourcesChecked", "artifactPaths"):
        value = result[field]
        if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
            raise ControllerError(f"invalid {field}: nonempty string list required")
    if result["verdict"] not in ALLOWED_VERDICTS or result["decision"] not in ALLOWED_VERDICTS:
        raise ControllerError("invalid verdict or decision")
    if result["confidence"] not in ALLOWED_CONFIDENCE:
        raise ControllerError("invalid confidence")
    if result["workstream"] not in ALLOWED_WORKSTREAMS:
        raise ControllerError("invalid workstream")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", result["sourceHash"]):
        raise ControllerError("invalid sourceHash")
    parse_timestamp(result["verifiedAt"], "verifiedAt")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise ControllerError(f"input not found: {path}")
    records = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ControllerError(f"invalid JSON on line {number}: {exc.msg}") from exc
        if not isinstance(record, dict):
            raise ControllerError(f"invalid record on line {number}: object required")
        records.append(record)
    return records


def load_candidates(path: Path) -> list[dict[str, Any]]:
    records = load_jsonl(path)
    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    for number, record in enumerate(records, 1):
        validate_candidate_schema(record, number)
        if record["candidate_id"] in seen_ids or record["source_hash"] in seen_hashes:
            raise ControllerError(f"invalid candidate on line {number}: duplicate id or source hash")
        seen_ids.add(record["candidate_id"])
        seen_hashes.add(record["source_hash"])
    return records


def read_state(state_path: Path) -> dict[str, Any]:
    state = {"processedHashes": [], "artifacts": [], "failures": [], "pendingAdmissions": [],
             "lastStatus": "never"}
    if not state_path.exists():
        return state
    for line in state_path.read_text(encoding="utf-8").splitlines():
        for label, key in (
            ("processed_hashes_json:", "processedHashes"),
            ("artifacts_json:", "artifacts"),
            ("failures_json:", "failures"),
            ("pending_admissions_json:", "pendingAdmissions"),
        ):
            if line.startswith(label):
                state[key] = json.loads(line[len(label):].strip())
        if line.startswith("last_status:"):
            state["lastStatus"] = line[len("last_status:"):].strip()
    return state


def read_processed_hashes(state_path: Path) -> set[str]:
    return set(read_state(state_path)["processedHashes"])


def write_state(state_path: Path, state: dict[str, Any], now: datetime) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "# Nightly Validation Controller State\n\n"
        f"last_completed_run: {utc_text(now)}\n"
        f"last_status: {state.get('lastStatus', 'unknown')}\n"
        f"processed_hashes_json: {json.dumps(sorted(set(state['processedHashes'])))}\n"
        f"artifacts_json: {json.dumps(state['artifacts'])}\n"
        f"failures_json: {json.dumps(state['failures'])}\n"
        f"pending_admissions_json: {json.dumps(state['pendingAdmissions'])}\n"
        f"next_run: {utc_text(next_scheduled_run(now))}\n"
    )
    state_path.write_text(text, encoding="utf-8")


def record_failure(state_path: Path, now: datetime, message: str, artifact: str | None) -> None:
    state = read_state(state_path)
    state["failures"].append({"at": utc_text(now), "error": message, "artifact": artifact})
    write_state(state_path, state, now)


def select_candidates(candidates: Iterable[dict[str, Any]], now: datetime,
                      processed_hashes: set[str]) -> list[dict[str, Any]]:
    eligible = [item for item in candidates if item["status"] == "pending"
                and parse_timestamp(item["not_before"], "not_before") <= now
                and item["source_hash"] not in processed_hashes]
    eligible.sort(key=lambda item: (-item["score"], item["candidate_id"]))
    if not eligible:
        return []
    lane = eligible[0]["lane"]
    return [item for item in eligible if item["lane"] == lane][:3]


def build_run_result(selected: list[dict[str, Any]], now: datetime) -> dict[str, Any]:
    return {"status": "ADMISSION_READY" if selected else "NO_QUALIFIED_VALIDATION",
            "runAt": utc_text(now), "lane": selected[0]["lane"] if selected else None,
            "selected": selected}


def unique_run_dir(runs_dir: Path, now: datetime) -> Path:
    stem = now.astimezone(timezone.utc).strftime("%Y-%m-%d/run-%Y%m%dT%H%M%S%fZ")
    candidate = runs_dir / stem
    suffix = 1
    while candidate.exists():
        candidate = runs_dir / f"{stem}-{suffix}"
        suffix += 1
    return candidate


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def admit_candidates(candidates: list[dict[str, Any]], now: datetime, state_path: Path,
                     runs_dir: Path, dry_run: bool) -> dict[str, Any]:
    selected = select_candidates(candidates, now, read_processed_hashes(state_path))
    decision = build_run_result(selected, now)
    if dry_run:
        return decision
    if not selected:
        state = read_state(state_path)
        state["lastStatus"] = "NO_QUALIFIED_VALIDATION"
        write_state(state_path, state, now)
        return decision
    run_dir = unique_run_dir(runs_dir, now)
    admission = {"schema": "nightly-validation-admission-v1",
                 "generatedBy": "nightly-validation-controller", **decision}
    admission["admissionHash"] = canonical_hash(admission)
    path = run_dir / "admission.json"
    write_json(path, admission)
    state = read_state(state_path)
    state["lastStatus"] = "ADMISSION_READY"
    state["artifacts"].append(str(path))
    state["pendingAdmissions"].append(str(path))
    write_state(state_path, state, now)
    return {**decision, "admissionPath": str(path), "admissionHash": admission["admissionHash"]}


def load_admission(path: Path) -> dict[str, Any]:
    try:
        artifact = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ControllerError(f"invalid admission artifact: {exc}") from exc
    claimed_hash = artifact.pop("admissionHash", None)
    if artifact.get("schema") != "nightly-validation-admission-v1" or claimed_hash != canonical_hash(artifact):
        raise ControllerError("invalid or tampered admission artifact")
    artifact["admissionHash"] = claimed_hash
    return artifact


def validate_result(candidate: dict[str, Any], result: dict[str, Any], now: datetime) -> bool:
    validate_candidate_schema(candidate, check_evidence=False)
    validate_result_schema(result)
    evidence = validate_evidence_file(candidate["evidence_path"])
    if file_hash(evidence) != candidate["source_hash"]:
        return False
    try:
        verified_at = parse_timestamp(result["verifiedAt"], "verifiedAt")
        evidence_at = parse_timestamp(candidate["evidence_timestamp"], "evidence_timestamp")
    except ControllerError:
        return False
    artifact_paths = [validate_evidence_file(item) for item in result["artifactPaths"]]
    common = (
        result["candidateId"] == candidate["candidate_id"]
        and result["sourceHash"] == candidate["source_hash"]
        and result["verifierConfirmed"] is True
        and timedelta(0) <= now - verified_at <= FRESHNESS_WINDOW
        and timedelta(0) <= now - evidence_at <= FRESHNESS_WINDOW
        and isinstance(result["sourcesChecked"], list) and bool(result["sourcesChecked"])
        and isinstance(result["artifactPaths"], list) and bool(result["artifactPaths"])
        and all(artifact_paths)
        and result["fatalConstraint"] is False
    )
    if not common:
        return False
    if result["verdict"] == "promote":
        return (result["decision"] == "promote" and result["score"] >= 30
                and result["evidenceScore"] >= 4 and result["distributionScore"] >= 3)
    return result["verdict"] in {"continue", "archive", "blocked"} and result["decision"] == result["verdict"]


def build_strict_promotions(candidates: list[dict[str, Any]], results: list[dict[str, Any]],
                            now: datetime) -> list[dict[str, Any]]:
    by_id = {item["candidate_id"]: item for item in candidates}
    valid = [result for result in results
             if result.get("candidateId") in by_id
             and validate_result(by_id[result["candidateId"]], result, now)
             and result["verdict"] == "promote"]
    valid.sort(key=lambda item: (-item["score"], item["candidateId"], item["sourceHash"]))
    return valid[:1]


def reconcile_results(admission_path: Path, results_path: Path, now: datetime,
                      state_path: Path, dry_run: bool) -> dict[str, Any]:
    admission = load_admission(admission_path)
    candidates = admission["selected"]
    results = load_jsonl(results_path)
    by_id = {item.get("candidateId"): item for item in results}
    if set(by_id) != {item["candidate_id"] for item in candidates}:
        raise ControllerError("result reconciliation incomplete or contains unknown candidates")
    invalid = [item["candidate_id"] for item in candidates
               if not validate_result(item, by_id[item["candidate_id"]], now)]
    if invalid:
        raise ControllerError(f"invalid validation result for: {', '.join(invalid)}")
    promotions = build_strict_promotions(candidates, results, now)
    envelope = {"schema": "nightly-validation-promotion-v1",
                "generatedBy": "nightly-validation-controller", "generatedAt": utc_text(now),
                "admissionPath": str(admission_path), "admissionHash": admission["admissionHash"],
                "promotions": promotions}
    envelope["artifactHash"] = canonical_hash(envelope)
    if dry_run:
        return {"status": "RECONCILED", **envelope}
    promotion_path = admission_path.parent / f"promotions-{now.strftime('%H%M%S%f')}.json"
    write_json(promotion_path, envelope)
    state = read_state(state_path)
    state["processedHashes"] = sorted(set(state["processedHashes"]) |
                                          {item["source_hash"] for item in candidates})
    state["artifacts"].append(str(promotion_path))
    state["pendingAdmissions"] = [item for item in state["pendingAdmissions"]
                                    if item != str(admission_path)]
    write_state(state_path, state, now)
    return {"status": "RECONCILED", "promotionPath": str(promotion_path),
            "promotionCount": len(promotions)}


def load_promotion_artifact(path: Path, now: datetime) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ControllerError(f"invalid promotion artifact: {exc}") from exc
    if not isinstance(envelope, dict) or envelope.get("schema") != "nightly-validation-promotion-v1" \
            or envelope.get("generatedBy") != "nightly-validation-controller":
        raise ControllerError("consume requires a controller-produced promotion artifact")
    claimed_artifact_hash = envelope.get("artifactHash")
    unhashed_envelope = {key: value for key, value in envelope.items() if key != "artifactHash"}
    if claimed_artifact_hash != canonical_hash(unhashed_envelope):
        raise ControllerError("promotion artifact integrity mismatch")
    promotions = envelope.get("promotions")
    if not isinstance(promotions, list) or len(promotions) != 1:
        raise ControllerError("promotion artifact must contain exactly one retryable promotion")
    admission_path = Path(envelope.get("admissionPath", ""))
    admission = load_admission(admission_path)
    if envelope.get("admissionHash") != admission["admissionHash"]:
        raise ControllerError("promotion admission integrity mismatch")
    promotion = promotions[0]
    candidate = next((item for item in admission["selected"]
                      if item["candidate_id"] == promotion.get("candidateId")), None)
    if not candidate or not validate_result(candidate, promotion, now):
        raise ControllerError("promotion failed consume-time gate revalidation")
    return promotion, envelope


def build_admission_payload(promotion: dict[str, Any], promotion_path: str) -> dict[str, Any]:
    return {
        "title": promotion["title"], "description": promotion["evidenceFound"],
        "status": "todo", "assignee": "eve", "priority": "medium",
        "project": "Nightly Validation", "lane": "portfolio-validation",
        "firstAction": promotion["firstAction"], "whyItMatters": promotion["whyItMatters"],
        "doneState": promotion["doneState"], "evidenceLinks": [promotion_path],
        "sourceSystem": "nightly-validation-controller",
        "dedupeKey": f"nightly-validation:{promotion['candidateId']}:{promotion['sourceHash']}",
        "workstream": promotion["workstream"], "promotionScore": promotion["score"],
        "hypothesis": promotion["question"], "nextTest": promotion["firstAction"],
        "revivalTrigger": promotion["nextTrigger"],
        "verdict": promotion["verdict"], "verifierConfirmed": promotion["verifierConfirmed"],
        "verifiedAt": promotion["verifiedAt"], "candidateId": promotion["candidateId"],
        "sourceHash": promotion["sourceHash"], "evidenceScore": promotion["evidenceScore"],
        "distributionScore": promotion["distributionScore"],
        "fatalConstraint": promotion["fatalConstraint"],
    }


def post_task(payload: dict[str, Any], endpoint: str = MC_TASKS_URL) -> dict[str, Any]:
    request = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = json.loads(response.read().decode())
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise ControllerError(f"Mission Control unavailable: {exc}") from exc
    if not body.get("success"):
        raise ControllerError(f"Mission Control rejected task: {body}")
    return body


def consume_artifact(path: Path, now: datetime, receipt_path: Path, dry_run: bool,
                     endpoint: str = MC_TASKS_URL) -> dict[str, Any]:
    promotion, _ = load_promotion_artifact(path, now)
    payload = build_admission_payload(promotion, str(path))
    if receipt_path.exists() and json.loads(receipt_path.read_text()).get("dedupeKey") == payload["dedupeKey"]:
        return {"status": "ALREADY_CONSUMED", "taskPayload": payload}
    if dry_run:
        return {"status": "TASK_PAYLOAD_READY", "taskPayload": payload}
    response = post_task(payload, endpoint)
    write_json(receipt_path, {"dedupeKey": payload["dedupeKey"], "response": response})
    return {"status": "TASK_UPSERTED", "taskPayload": payload, "response": response}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("admit", "reconcile", "consume"), required=True)
    parser.add_argument("--queue", default="memory/agent-portfolio/validation-queue.jsonl")
    parser.add_argument("--state", default="memory/job-state/nightly-validation.md")
    parser.add_argument("--runs-dir", default="memory/agent-portfolio/runs")
    parser.add_argument("--admission")
    parser.add_argument("--results")
    parser.add_argument("--promotion")
    parser.add_argument("--receipt", default="memory/job-state/nightly-validation-consume.json")
    parser.add_argument("--endpoint", default=MC_TASKS_URL)
    parser.add_argument("--now")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def run_controller(args: argparse.Namespace) -> dict[str, Any]:
    now = parse_timestamp(args.now, "now") if args.now else datetime.now(timezone.utc)
    state_path = Path(args.state)
    if args.phase == "admit":
        return admit_candidates(load_candidates(Path(args.queue)), now, state_path,
                                Path(args.runs_dir), args.dry_run)
    if args.phase == "reconcile":
        if not args.admission or not args.results:
            raise ControllerError("reconcile requires --admission and --results")
        return reconcile_results(Path(args.admission), Path(args.results), now, state_path, args.dry_run)
    if not args.promotion:
        raise ControllerError("consume requires --promotion")
    return consume_artifact(Path(args.promotion), now, Path(args.receipt), args.dry_run, args.endpoint)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    now = parse_timestamp(args.now, "now") if args.now else datetime.now(timezone.utc)
    try:
        result = run_controller(args)
    except (ControllerError, OSError, json.JSONDecodeError) as exc:
        record_failure(Path(args.state), now, str(exc), args.promotion or args.admission)
        print(json.dumps({"status": "ERROR", "error": str(exc)}, sort_keys=True)
              if args.json else f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True) if args.json else result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
