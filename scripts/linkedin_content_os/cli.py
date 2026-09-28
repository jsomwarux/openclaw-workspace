"""One local, deterministic command surface for LinkedIn Program 0."""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import urllib.request
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple

from scripts.linkedin_content_os.boundaries import (
    build_authority_consumption_receipt,
    build_boundary_artifact,
    normalize_cron_definitions,
    validate_authority_consumption_receipt,
    validate_boundary_artifact,
)
from scripts.linkedin_content_os.canonical import (
    canonical_bytes,
    read_jsonl,
    sha256_hex,
    write_json_atomic,
)
from scripts.linkedin_content_os.checkin import project_checkin
from scripts.linkedin_content_os.contracts import parse_timestamp
from scripts.linkedin_content_os.corpus import (
    build_contrastive_pairs,
    build_voice_gold,
)
from scripts.linkedin_content_os.fixtures import (
    PRE_GATE_COMMIT,
    PRE_GATE_PATH,
    build_evaluation_fixtures,
)
from scripts.linkedin_content_os.focus import build_focus_snapshot
from scripts.linkedin_content_os.historical_audit import audit_legacy_rows
from scripts.linkedin_content_os.mc_snapshot import (
    SOURCE_URL,
    capture_tasks,
    validate_snapshot,
)
from scripts.linkedin_content_os.outcomes import load_events
from scripts.linkedin_content_os.source_policy import build_source_policy
from scripts.linkedin_content_os.voice_rules import (
    OWNER_SURFACES,
    build_voice_rule_retirements,
)


COMMANDS = (
    "init-run",
    "capture-boundaries",
    "audit-history",
    "ingest-human-gate",
    "build-focus",
    "build-corpus",
    "build-fixtures",
    "build-source-policy",
    "audit-voice-rules",
    "preview-checkin",
    "verify",
)
RUN_CONTEXT_SCHEMA = "linkedin-program-0-run-context.v1"
AUTHORITY_CONTEXT_SCHEMA = "linkedin-program-0-authority-run-context.v1"
_HASH_CHARS = set("0123456789abcdef")
_PROTECTED_INPUTS = (
    "memory/content/posted-log.jsonl",
    "memory/content/edit-deltas.jsonl",
)
_GIT_COMMIT = re.compile(r"^[0-9a-f]{40}$")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _strict_object(pairs: List[Tuple[str, object]]) -> Dict[str, object]:
    result: Dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key {!r}".format(key))
        result[key] = value
    return result


def _read_json(path: Path) -> Dict[str, object]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError("non-standard JSON constant {}".format(value))
            ),
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("invalid JSON file {}".format(path)) from error
    if not isinstance(value, dict):
        raise ValueError("{} must contain a JSON object".format(path))
    return value


def _write_jsonl(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    payload = b"".join(canonical_bytes(row) + b"\n" for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(".{}.{}.tmp".format(path.name, os.getpid()))
    try:
        with temporary.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temporary), str(path))
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _read_jsonl_optional(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        raise ValueError("required Program 0 artifact is missing: {}".format(path))
    return read_jsonl(path)


def _require_hash(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in _HASH_CHARS for character in value)
    ):
        raise ValueError("{} must be a lowercase SHA-256".format(label))
    return value


def _run_context(path: Path, *, authority: bool = False) -> Dict[str, object]:
    value = _read_json(path)
    base = {"schemaVersion", "runId", "generatedAt"}
    expected = base | ({"corpusAuthorityManifestSha256"} if authority else set())
    if set(value) != expected:
        raise ValueError("run context fields are not closed")
    schema = AUTHORITY_CONTEXT_SCHEMA if authority else RUN_CONTEXT_SCHEMA
    if value["schemaVersion"] != schema:
        raise ValueError("unsupported run context schema")
    generated_at = value["generatedAt"]
    parse_timestamp(generated_at, "runContext.generatedAt")
    unsigned = {
        "schemaVersion": value["schemaVersion"],
        "generatedAt": generated_at,
    }
    if authority:
        manifest_digest = _require_hash(
            value["corpusAuthorityManifestSha256"],
            "corpusAuthorityManifestSha256",
        )
        unsigned["corpusAuthorityManifestSha256"] = manifest_digest
    expected_run_id = "sha256:" + sha256_hex(canonical_bytes(unsigned))
    if value["runId"] != expected_run_id:
        raise ValueError("runId does not match canonical run context")
    return value


def init_run(
    generated_at: str, outcomes: Path, output: Path
) -> Dict[str, object]:
    """Create one run context while preserving any existing outcome ledger."""

    instant = _utc_now().isoformat() if generated_at == "now" else generated_at
    parse_timestamp(instant, "generatedAt")
    unsigned: Dict[str, object] = {
        "schemaVersion": RUN_CONTEXT_SCHEMA,
        "generatedAt": instant,
    }
    context = {**unsigned, "runId": "sha256:" + sha256_hex(canonical_bytes(unsigned))}
    outcomes.parent.mkdir(parents=True, exist_ok=True)
    if not outcomes.exists():
        descriptor = os.open(str(outcomes), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(descriptor)
    before = outcomes.read_bytes()
    if output.exists():
        existing = _read_json(output)
        if canonical_bytes(existing) != canonical_bytes(context):
            raise ValueError("existing run context differs from requested run")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        write_json_atomic(output, context)
    if outcomes.read_bytes() != before:
        raise RuntimeError("init-run changed an existing outcome ledger")
    return context


@contextmanager
def _network_denied() -> Iterator[None]:
    original_connect = socket.socket.connect
    original_create = socket.create_connection
    original_urlopen = urllib.request.urlopen

    def blocked(*args: object, **kwargs: object) -> object:
        raise RuntimeError("network access is prohibited for this command")

    socket.socket.connect = blocked  # type: ignore[assignment]
    socket.create_connection = blocked  # type: ignore[assignment]
    urllib.request.urlopen = blocked  # type: ignore[assignment]
    try:
        yield
    finally:
        socket.socket.connect = original_connect  # type: ignore[assignment]
        socket.create_connection = original_create  # type: ignore[assignment]
        urllib.request.urlopen = original_urlopen  # type: ignore[assignment]


def _allowed_process_argv(command: str, argv: object) -> bool:
    if not isinstance(argv, (list, tuple)) or any(
        not isinstance(item, str) for item in argv
    ):
        return False
    values = list(argv)
    if command == "capture-boundaries":
        return values == ["openclaw", "cron", "list", "--json"]
    if command in {"build-fixtures", "ingest-human-gate"}:
        return (
            len(values) == 5
            and values[0] == "git"
            and values[1] == "--git-dir"
            and Path(values[2]).is_absolute()
            and values[3] == "show"
            and ":" in values[4]
            and _GIT_COMMIT.fullmatch(values[4].split(":", 1)[0]) is not None
            and not values[4].split(":", 1)[1].startswith("/")
            and ".." not in Path(values[4].split(":", 1)[1]).parts
        )
    return False


@contextmanager
def _process_guard(command: str) -> Iterator[None]:
    originals = {
        "Popen": subprocess.Popen,
        "run": subprocess.run,
        "call": subprocess.call,
        "check_call": subprocess.check_call,
        "check_output": subprocess.check_output,
    }

    def blocked(*args: object, **kwargs: object) -> object:
        raise RuntimeError("child process is prohibited for {}".format(command))

    def guarded_run(argv: object, *args: object, **kwargs: object) -> object:
        if not _allowed_process_argv(command, argv):
            raise RuntimeError("child process argv is not allowlisted")
        if args or kwargs.get("shell") or kwargs.get("env") is not None or kwargs.get("cwd") is not None:
            raise RuntimeError("child process options are not allowlisted")
        unknown = set(kwargs) - {"check", "capture_output", "text"}
        if unknown:
            raise RuntimeError("child process options are not allowlisted")
        subprocess.Popen = originals["Popen"]  # type: ignore[assignment]
        try:
            return originals["run"](argv, **kwargs)
        finally:
            subprocess.Popen = blocked  # type: ignore[assignment]

    subprocess.Popen = blocked  # type: ignore[assignment]
    subprocess.run = guarded_run  # type: ignore[assignment]
    subprocess.call = blocked  # type: ignore[assignment]
    subprocess.check_call = blocked  # type: ignore[assignment]
    subprocess.check_output = blocked  # type: ignore[assignment]
    try:
        yield
    finally:
        for name, value in originals.items():
            setattr(subprocess, name, value)


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError("artifact path must stay under workspace root") from error


def _binding(role: str, path: Path, root: Path) -> Dict[str, object]:
    return {
        "role": role,
        "path": _relative(path, root),
        "sha256": sha256_hex(path.read_bytes()),
    }


def _write_receipt(
    *,
    command: str,
    run_context_path: Path,
    run_context: Dict[str, object],
    manifest: Dict[str, object],
    expected_manifest_sha256: Optional[str],
    inputs: Sequence[Tuple[str, Path]],
    outputs: Sequence[Tuple[str, Path]],
    receipt_output: Path,
    workspace_root: Path,
) -> Dict[str, object]:
    canonical_manifest_sha256 = _require_hash(
        manifest.get("manifestSha256"), "manifest.manifestSha256"
    )
    receipt = build_authority_consumption_receipt(
        command=command,
        run_context_sha256=sha256_hex(run_context_path.read_bytes()),
        expected_manifest_sha256=expected_manifest_sha256,
        canonical_manifest_sha256=canonical_manifest_sha256,
        inputs=sorted(
            [_binding(role, path, workspace_root) for role, path in inputs],
            key=lambda item: (str(item["role"]), str(item["path"])),
        ),
        outputs=sorted(
            [_binding(role, path, workspace_root) for role, path in outputs],
            key=lambda item: (str(item["role"]), str(item["path"])),
        ),
        generated_at=str(run_context["generatedAt"]),
    )
    receipt_output.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(receipt_output, receipt)
    return receipt


def _default_focus_targets(root: Path) -> List[Dict[str, object]]:
    definitions = (
        (
            "consulting-proof",
            "consulting",
            "Permissioned consulting proof",
            "Publish only proof-led consulting content that clears evidence and permission gates",
            "memory/content/current-efforts.md",
        ),
        (
            "career-authority",
            "career",
            "Enterprise AI operator authority",
            "Show evidence-backed enterprise AI execution without exposing internal machinery",
            "memory/job-state/job-market-daily-research.md",
        ),
        (
            "product-distribution",
            "product",
            "Shipped product distribution",
            "Turn verified shipped outcomes into commercially relevant public lessons",
            "memory/north-star/active-this-week.md",
        ),
    )
    targets: List[Dict[str, object]] = []
    for target_id, kind, label, desired, relative in definitions:
        path = root / relative
        targets.append(
            {
                "targetId": target_id,
                "kind": kind,
                "label": label,
                "desiredOutcome": desired,
                "sourceRefs": [
                    {"path": relative, "sha256": sha256_hex(path.read_bytes())}
                ],
            }
        )
    return targets


def _cron_list() -> Dict[str, object]:
    completed = subprocess.run(
        ["openclaw", "cron", "list", "--json"],
        check=True,
        capture_output=True,
        text=False,
    )
    try:
        value = json.loads(completed.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("openclaw cron list returned invalid JSON") from error
    if not isinstance(value, dict):
        raise ValueError("openclaw cron list must return an object")
    return value


def _launchagent_inventory() -> List[Dict[str, object]]:
    root = Path.home()
    directory = root / "Library" / "LaunchAgents"
    if not directory.exists():
        return []
    result = [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256_hex(path.read_bytes()),
        }
        for path in sorted(directory.glob("*.plist"))
        if path.is_file() and not path.is_symlink()
    ]
    return result


def _primary_checkout_fingerprint() -> str:
    root = Path("/Users/jtsomwaru/.openclaw/workspace")
    entries: List[Dict[str, object]] = []
    for relative in (".git/HEAD", ".git/index"):
        path = root / relative
        if path.is_file():
            entries.append({"path": relative, "sha256": sha256_hex(path.read_bytes())})
    return sha256_hex(canonical_bytes(entries))


def _capture_boundaries(args: argparse.Namespace) -> Dict[str, object]:
    run_context = _run_context(Path(args.run_context))
    raw = capture_tasks(SOURCE_URL)
    snapshot = validate_snapshot(raw, run_context)
    if args.mc_output:
        write_json_atomic(Path(args.mc_output), snapshot)
    cron = normalize_cron_definitions(_cron_list())
    protected: Dict[str, str] = {}
    root = Path(args.workspace_root).resolve()
    for relative in _PROTECTED_INPUTS:
        path = root / relative
        protected[relative] = sha256_hex(path.read_bytes())
    artifact = build_boundary_artifact(
        phase=args.phase,
        generated_at=str(run_context["generatedAt"]),
        run_id=str(run_context["runId"]),
        snapshot=snapshot,
        normalized_cron=cron,
        launchagents=_launchagent_inventory(),
        protected_inputs=protected,
        primary_checkout_fingerprint=_primary_checkout_fingerprint(),
    )
    write_json_atomic(Path(args.output), artifact)
    return artifact


def _audit_history(args: argparse.Namespace) -> Dict[str, object]:
    context_path = Path(args.run_context)
    authority = args.corpus_authority_manifest is not None
    context = _run_context(context_path, authority=authority)
    manifest = (
        _read_json(Path(args.corpus_authority_manifest)) if authority else None
    )
    expected = (
        str(context["corpusAuthorityManifestSha256"]) if authority else None
    )
    audit = audit_legacy_rows(
        Path(args.posted_log),
        Path(args.outcomes),
        str(context["generatedAt"]),
        corpus_authority_manifest=manifest,
        expected_manifest_sha256=expected,
    )
    write_json_atomic(Path(args.output), audit)
    recovery = audit["recoveryRequest"]
    assert isinstance(recovery, dict)
    write_json_atomic(Path(args.recovery_output), recovery)
    result: Dict[str, object] = {"audit": audit, "recoveryRequest": recovery}
    if authority:
        if args.receipt_output is None:
            raise ValueError("phase-2 audit requires --receipt-output")
        assert manifest is not None
        receipt = _write_receipt(
            command="audit-history",
            run_context_path=context_path,
            run_context=context,
            manifest=manifest,
            expected_manifest_sha256=expected,
            inputs=(
                ("posted_log", Path(args.posted_log)),
                ("outcomes", Path(args.outcomes)),
                ("authority_manifest", Path(args.corpus_authority_manifest)),
                ("run_context", context_path),
            ),
            outputs=(
                ("historical_audit", Path(args.output)),
                ("recovery_request", Path(args.recovery_output)),
            ),
            receipt_output=Path(args.receipt_output),
            workspace_root=Path(args.workspace_root),
        )
        result["authorityConsumptionReceipt"] = receipt
    return result


def _build_focus(args: argparse.Namespace) -> Dict[str, object]:
    context = _run_context(Path(args.run_context))
    root = Path(args.workspace_root)
    if args.outcomes is not None:
        raise ValueError(
            "phase-2 focus rebuild requires Task 7B recovery authority and is unavailable before the human gate"
        )
    snapshot = build_focus_snapshot(
        root,
        _default_focus_targets(root),
        generated_at=str(context["generatedAt"]),
    )
    write_json_atomic(Path(args.output), snapshot)
    return snapshot


def _build_corpus(args: argparse.Namespace) -> Dict[str, object]:
    context_path = Path(args.run_context)
    raw_context = _read_json(context_path)
    authority = "corpusAuthorityManifestSha256" in raw_context
    context = _run_context(context_path, authority=authority)
    audit = _read_json(Path(args.audit))
    events = load_events(Path(args.outcomes))
    expected = (
        str(context["corpusAuthorityManifestSha256"]) if authority else None
    )
    gold = build_voice_gold(events, audit, expected_manifest_sha256=expected)
    pairs = build_contrastive_pairs(events, audit, expected_manifest_sha256=expected)
    _write_jsonl(Path(args.gold_output), gold)
    _write_jsonl(Path(args.pairs_output), pairs)
    manifest = audit.get("corpusAuthorityManifest")
    if not isinstance(manifest, dict):
        raise ValueError("audit lacks corpus authority manifest")
    receipt = _write_receipt(
        command="build-corpus",
        run_context_path=context_path,
        run_context=context,
        manifest=manifest,
        expected_manifest_sha256=expected,
        inputs=(
            ("audit", Path(args.audit)),
            ("outcomes", Path(args.outcomes)),
            ("run_context", context_path),
        ),
        outputs=(
            ("voice_gold", Path(args.gold_output)),
            ("contrastive_pairs", Path(args.pairs_output)),
        ),
        receipt_output=Path(args.receipt_output),
        workspace_root=Path(args.workspace_root),
    )
    return {"voiceGoldCount": len(gold), "contrastivePairCount": len(pairs), "receipt": receipt}


def _build_fixtures(args: argparse.Namespace) -> Dict[str, object]:
    context_path = Path(args.run_context) if args.run_context else Path(
        args.workspace_root
    ) / "memory/content/linkedin-content-os/run-context.v1.json"
    context = _run_context(context_path)
    generated_at = str(context["generatedAt"])
    parse_timestamp(generated_at, "generatedAt")
    if args.jt_ops_commit != PRE_GATE_COMMIT or args.jt_ops_path != PRE_GATE_PATH:
        raise ValueError("build-fixtures source does not match the reviewed Git object")
    rows = build_evaluation_fixtures(
        Path(args.workspace_root),
        Path(args.jt_ops_git_dir),
        generated_at=generated_at,
        runner=subprocess.run,
    )
    _write_jsonl(Path(args.output), rows)
    return {"schemaVersion": "linkedin-evaluation-fixtures-result.v1", "count": len(rows), "outputSha256": sha256_hex(Path(args.output).read_bytes())}


def _build_source_policy_command(args: argparse.Namespace) -> Dict[str, object]:
    context = _run_context(Path(args.run_context))
    artifact = build_source_policy(str(context["generatedAt"]))
    write_json_atomic(Path(args.output), artifact)
    return artifact


def _audit_voice_rules(args: argparse.Namespace) -> Dict[str, object]:
    context = _run_context(Path(args.run_context))
    documents = {
        path: (Path(args.workspace_root) / path).read_bytes() for path in OWNER_SURFACES
    }
    effective_date = parse_timestamp(
        context["generatedAt"], "generatedAt"
    ).date().isoformat()
    artifact = build_voice_rule_retirements(documents, effective_date=effective_date)
    write_json_atomic(Path(args.output), artifact)
    return artifact


def _preview_checkin(args: argparse.Namespace) -> Dict[str, object]:
    context = _run_context(Path(args.run_context))
    snapshot = _read_json(Path(args.mc_snapshot))
    events = load_events(Path(args.outcomes))
    now = parse_timestamp(context["generatedAt"], "generatedAt")
    preview = project_checkin(snapshot, events, now)
    result: Dict[str, object] = (
        preview
        if preview is not None
        else {
            "schemaVersion": "linkedin-checkin-preview.v1",
            "sourceSnapshotSha256": snapshot.get("projectionSha256"),
            "liveWriteAuthorized": False,
            "task": None,
        }
    )
    write_json_atomic(Path(args.output), result)
    return result


def _verify(args: argparse.Namespace) -> Dict[str, object]:
    context = _run_context(Path(args.run_context), authority=True)
    manifest = _read_json(Path(args.corpus_authority_manifest))
    canonical_manifest = _require_hash(manifest.get("manifestSha256"), "manifestSha256")
    expected = str(context["corpusAuthorityManifestSha256"])
    if canonical_manifest != expected:
        raise ValueError("authority context and canonical manifest hashes differ")
    receipts = []
    for path_value in (
        args.phase_1_corpus_receipt,
        args.phase_2_audit_receipt,
        args.phase_2_corpus_receipt,
    ):
        path = Path(path_value)
        receipt = validate_authority_consumption_receipt(
            _read_json(path), workspace_root=Path(args.workspace_root)
        )
        receipts.append({"path": _relative(path, Path(args.workspace_root)), "sha256": sha256_hex(path.read_bytes()), "receipt": receipt})
    if receipts[0]["receipt"]["expectedManifestSha256"] is not None:
        raise ValueError("phase-1 corpus receipt must use the fixed-empty authority")
    for item in receipts[1:]:
        if item["receipt"]["expectedManifestSha256"] != expected:
            raise ValueError("phase-2 receipt authority digest mismatch")
    boundaries = [validate_boundary_artifact(_read_json(Path(value))) for value in (
        args.phase_1_before, args.phase_1_after, args.phase_2_before, args.phase_2_after
    )]
    expected_phases = [
        "phase-1-before", "phase-1-after", "phase-2-before", "phase-2-after"
    ]
    if [item["phase"] for item in boundaries] != expected_phases:
        raise ValueError("boundary artifacts are not in the required phase order")
    for before, after in ((boundaries[0], boundaries[1]), (boundaries[2], boundaries[3])):
        for key in (
            "missionControl", "cronDefinitionSha256", "launchAgents",
            "protectedInputs", "primaryCheckoutFingerprint",
        ):
            if before.get(key) != after.get(key):
                raise ValueError("boundary changed for {}".format(key))
    root = Path(args.workspace_root)
    artifact_root = root / "memory/content/linkedin-content-os"
    audit = _read_json(artifact_root / "historical-audit.v1.json")
    focus = _read_json(artifact_root / "focus-snapshot.v1.json")
    fixtures = _read_jsonl_optional(artifact_root / "evaluation-fixtures.v0.jsonl")
    gold = _read_jsonl_optional(artifact_root / "voice-gold.v0.jsonl")
    pairs = _read_jsonl_optional(artifact_root / "contrastive-pairs.v0.jsonl")
    checkin = _read_json(artifact_root / "checkin.preview.v1.json")
    status_counts = audit.get("statusCounts")
    missing_counts = audit.get("missingFieldCounts")
    recovery = audit.get("recoveryRequest")
    if not isinstance(status_counts, dict) or set(status_counts) != {
        "posted_confirmed", "not_posted_confirmed", "status_unknown"
    }:
        raise ValueError("historical audit status counts are not closed")
    if not isinstance(missing_counts, dict):
        raise ValueError("historical audit missing-field counts are invalid")
    if not isinstance(recovery, dict) or not isinstance(recovery.get("items"), list):
        raise ValueError("historical recovery request is invalid")
    if recovery["items"]:
        raise ValueError("human gate has unanswered bounded recovery rows")
    if focus.get("status") != "confirmed":
        raise ValueError("focus snapshot is not confirmed")
    classifications: Dict[str, int] = {"positive": 0, "negative": 0, "gap": 0}
    for fixture in fixtures:
        classification = fixture.get("classification")
        if classification not in classifications:
            raise ValueError("fixture classification is invalid")
        classifications[str(classification)] += 1
    if classifications["positive"] < 1 or classifications["negative"] < 1:
        raise ValueError("fixture set lacks the required positive and negative evidence")
    voice_gold_count = sum(row.get("recordType") == "voice_gold" for row in gold)
    pair_count = sum(row.get("recordType") == "contrastive_pair" for row in pairs)
    task_value = checkin.get("task")
    if task_value is not None and not isinstance(task_value, dict):
        raise ValueError("check-in preview task must be null or an object")
    targets = focus.get("targets")
    if not isinstance(targets, list):
        raise ValueError("focus targets must be a list")
    report = {
        "schemaVersion": "linkedin-program-0-verification.v1",
        "authorityContextDigest": sha256_hex(Path(args.run_context).read_bytes()),
        "canonicalManifestSha256": canonical_manifest,
        "receipts": [{"path": item["path"], "sha256": item["sha256"]} for item in receipts],
        "authorityConsumptionBindings": {
            "phase1Corpus": receipts[0]["receipt"],
            "phase2Audit": receipts[1]["receipt"],
            "phase2Corpus": receipts[2]["receipt"],
        },
        "boundaryPairsEqual": True,
        "statusCounts": status_counts,
        "missingUrlCount": int(missing_counts.get("public_url", 0)),
        "missingFinalTextCount": int(missing_counts.get("final_text", 0)),
        "focusTargets": targets,
        "voiceGoldCount": voice_gold_count,
        "contrastivePairCount": pair_count,
        "fixtureClassifications": classifications,
        "checkinPreviewCount": 0 if task_value is None else 1,
        "humanGateResolved": True,
        "liveOrExternalActionOccurred": False,
        "verdict": "program-0-local-proof-ready-for-independent-verification",
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "# LinkedIn Content OS Program 0\n\n```json\n{}\n```\n".format(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
        ),
        encoding="utf-8",
    )
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="linkedin-content-os-program-0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init-run")
    init.add_argument("--generated-at", required=True)
    init.add_argument("--outcomes", required=True)
    init.add_argument("--output", required=True)

    capture = subparsers.add_parser("capture-boundaries")
    capture.add_argument("--phase", required=True)
    capture.add_argument("--run-context", required=True)
    capture.add_argument("--mc-output")
    capture.add_argument("--output", required=True)
    capture.add_argument("--workspace-root", default=".")

    audit = subparsers.add_parser("audit-history")
    audit.add_argument("--posted-log", required=True)
    audit.add_argument("--outcomes", required=True)
    audit.add_argument("--corpus-authority-manifest")
    audit.add_argument("--run-context", required=True)
    audit.add_argument("--output", required=True)
    audit.add_argument("--recovery-output", required=True)
    audit.add_argument("--receipt-output")
    audit.add_argument("--workspace-root", default=".")

    ingest = subparsers.add_parser("ingest-human-gate")
    for name in (
        "response", "recovery-request", "focus", "fixtures", "outcomes",
        "corpus-authority-manifest-output", "authority-run-context-output", "run-context",
    ):
        ingest.add_argument("--" + name, required=True)

    focus = subparsers.add_parser("build-focus")
    focus.add_argument("--workspace-root", required=True)
    focus.add_argument("--outcomes")
    focus.add_argument("--run-context", required=True)
    focus.add_argument("--output", required=True)

    corpus = subparsers.add_parser("build-corpus")
    corpus.add_argument("--audit", required=True)
    corpus.add_argument("--outcomes", required=True)
    corpus.add_argument("--run-context", required=True)
    corpus.add_argument("--gold-output", required=True)
    corpus.add_argument("--pairs-output", required=True)
    corpus.add_argument("--receipt-output", required=True)
    corpus.add_argument("--workspace-root", default=".")

    fixtures = subparsers.add_parser("build-fixtures")
    fixtures.add_argument("--decagon-packet", required=True)
    fixtures.add_argument("--jt-ops-git-dir", required=True)
    fixtures.add_argument("--jt-ops-commit", required=True)
    fixtures.add_argument("--jt-ops-path", required=True)
    fixtures.add_argument("--output", required=True)
    fixtures.add_argument("--run-context")
    fixtures.add_argument("--generated-at")
    fixtures.add_argument("--workspace-root", default=".")
    fixtures.add_argument("--human-gate-response")

    policy = subparsers.add_parser("build-source-policy")
    policy.add_argument("--run-context", required=True)
    policy.add_argument("--output", required=True)

    voice = subparsers.add_parser("audit-voice-rules")
    voice.add_argument("--run-context", required=True)
    voice.add_argument("--output", required=True)
    voice.add_argument("--workspace-root", default=".")

    preview = subparsers.add_parser("preview-checkin")
    preview.add_argument("--mc-snapshot", required=True)
    preview.add_argument("--outcomes", required=True)
    preview.add_argument("--run-context", required=True)
    preview.add_argument("--output", required=True)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--workspace-root", required=True)
    verify.add_argument("--run-context", required=True)
    verify.add_argument("--corpus-authority-manifest", required=True)
    verify.add_argument("--phase-1-corpus-receipt", required=True)
    verify.add_argument("--phase-2-audit-receipt", required=True)
    verify.add_argument("--phase-2-corpus-receipt", required=True)
    verify.add_argument("--phase-1-before", required=True)
    verify.add_argument("--phase-1-after", required=True)
    verify.add_argument("--phase-2-before", required=True)
    verify.add_argument("--phase-2-after", required=True)
    verify.add_argument("--report", required=True)
    return parser


def _ingest_human_gate(args: argparse.Namespace) -> Dict[str, object]:
    try:
        from scripts.linkedin_content_os.recovery import ingest_human_gate_files
    except ImportError as error:
        raise RuntimeError(
            "Task 7B recovery implementation is required before ingest-human-gate"
        ) from error
    return ingest_human_gate_files(args)


def main(argv: Optional[Sequence[str]] = None) -> Dict[str, object]:
    args = _parser().parse_args(argv)
    dispatch: Dict[str, Callable[[argparse.Namespace], Dict[str, object]]] = {
        "init-run": lambda value: init_run(
            value.generated_at, Path(value.outcomes), Path(value.output)
        ),
        "capture-boundaries": _capture_boundaries,
        "audit-history": _audit_history,
        "ingest-human-gate": _ingest_human_gate,
        "build-focus": _build_focus,
        "build-corpus": _build_corpus,
        "build-fixtures": _build_fixtures,
        "build-source-policy": _build_source_policy_command,
        "audit-voice-rules": _audit_voice_rules,
        "preview-checkin": _preview_checkin,
        "verify": _verify,
    }
    with _process_guard(args.command):
        if args.command == "capture-boundaries":
            result = dispatch[args.command](args)
        else:
            with _network_denied():
                result = dispatch[args.command](args)
    sys.stdout.write(canonical_bytes(result).decode("utf-8") + "\n")
    return result


if __name__ == "__main__":
    main()
