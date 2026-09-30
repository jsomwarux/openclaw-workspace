"""One local, deterministic command surface for LinkedIn Program 0."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import stat
import subprocess
import sys
import unicodedata
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
    read_jsonl_bytes,
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
    DECAGON_PACKET_PATH,
    PRE_GATE_COMMIT,
    PRE_GATE_PATH,
    build_evaluation_fixtures,
)
from scripts.linkedin_content_os.focus import build_focus_snapshot
from scripts.linkedin_content_os.historical_audit import (
    audit_legacy_rows,
    corpus_run_id,
    validate_corpus_authority_manifest,
)
from scripts.linkedin_content_os.mc_snapshot import (
    SOURCE_URL,
    capture_tasks,
    validate_snapshot,
)
from scripts.linkedin_content_os.outcomes import load_events, validate_events
from scripts.linkedin_content_os.source_policy import build_source_policy, validate_source_policy
from scripts.linkedin_content_os.voice_rules import (
    OWNER_SURFACES,
    build_voice_rule_retirements,
)


COMMANDS = (
    "init-run",
    "capture-boundaries",
    "audit-history",
    "ingest-human-gate",
    "ingest-history-correction",
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


def _read_json_bytes(payload: bytes, source: object) -> Dict[str, object]:
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError("non-standard JSON constant {}".format(value))
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("invalid JSON file {}".format(source)) from error
    if not isinstance(value, dict):
        raise ValueError("{} must contain a JSON object".format(source))
    return value


def _read_json(path: Path) -> Dict[str, object]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise ValueError("invalid JSON file {}".format(path)) from error
    return _read_json_bytes(payload, path)


class _VerifierSnapshots:
    """Read every verifier input once and reuse that exact immutable snapshot."""

    def __init__(self) -> None:
        self._payloads: Dict[Path, bytes] = {}
        self._targets: Dict[Path, Path] = {}

    def _path(self, path: Path) -> Path:
        logical = Path(os.path.abspath(os.fspath(Path(path))))
        if logical in self._targets:
            return self._targets[logical]
        try:
            target = logical.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise ValueError("verifier input is unavailable: {}".format(path)) from error
        self._targets[logical] = target
        return target

    def resolved(self, path: Path) -> Path:
        """Return the immutable first resolution for one logical verifier input."""

        return self._path(path)

    def bytes(self, path: Path) -> bytes:
        canonical = self._path(path)
        if canonical not in self._payloads:
            try:
                self._payloads[canonical] = canonical.read_bytes()
            except OSError as error:
                raise ValueError(
                    "verifier input is unavailable: {}".format(path)
                ) from error
        return self._payloads[canonical]

    def sha256(self, path: Path) -> str:
        return sha256_hex(self.bytes(path))

    def json(self, path: Path) -> Dict[str, object]:
        return _read_json_bytes(self.bytes(path), path)

    def jsonl(self, path: Path) -> List[Dict[str, object]]:
        return read_jsonl_bytes(self.bytes(path), str(path))


def _write_jsonl(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    payload = _jsonl_bytes(rows)
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


def _jsonl_bytes(rows: Sequence[Dict[str, object]]) -> bytes:
    return b"".join(canonical_bytes(row) + b"\n" for row in rows)


def _write_bytes_atomic(path: Path, payload: bytes) -> None:
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


def _validate_distinct_paths(
    *,
    inputs: Sequence[Path],
    outputs: Sequence[Path],
    receipts: Sequence[Path],
    workspace_root: Path,
) -> None:
    """Reject every input/output/receipt alias before a command can write."""

    del workspace_root  # Paths may intentionally include an external read-only Git dir.
    labeled: List[Tuple[str, Path, str]] = []
    for label, paths in (("input", inputs), ("output", outputs), ("receipt", receipts)):
        for path in paths:
            resolved = Path(path).resolve(strict=False)
            case_key = os.path.normcase(
                unicodedata.normalize("NFC", str(resolved))
            ).casefold()
            labeled.append((label, resolved, case_key))
    for index, (left_label, left, left_case_key) in enumerate(labeled):
        for right_label, right, right_case_key in labeled[index + 1:]:
            aliased = left == right or left_case_key == right_case_key
            if not aliased and left.exists() and right.exists():
                try:
                    aliased = os.path.samefile(left, right)
                except OSError:
                    aliased = False
            if aliased:
                raise ValueError(
                    "path alias between {} and {}: {}".format(
                        left_label, right_label, right
                    )
                )


def _require_hash(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in _HASH_CHARS for character in value)
    ):
        raise ValueError("{} must be a lowercase SHA-256".format(label))
    return value


def _validate_run_context(
    value: Dict[str, object], *, authority: bool = False
) -> Dict[str, object]:
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


def _run_context(path: Path, *, authority: bool = False) -> Dict[str, object]:
    return _validate_run_context(_read_json(path), authority=authority)


def init_run(
    generated_at: str, outcomes: Path, output: Path
) -> Dict[str, object]:
    """Create one run context while preserving any existing outcome ledger."""

    _validate_distinct_paths(
        inputs=[], outputs=[Path(outcomes), Path(output)], receipts=[], workspace_root=Path(".")
    )
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


@contextmanager
def _capture_network_guard() -> Iterator[Callable[[Callable[[], bytes]], bytes]]:
    """Deny all network except one explicitly scoped capture_tasks invocation."""

    original_connect = socket.socket.connect
    original_create = socket.create_connection
    original_urlopen = urllib.request.urlopen
    calls = 0

    def blocked(*args: object, **kwargs: object) -> object:
        raise RuntimeError("network access is prohibited outside the exact loopback GET")

    def exact_get(operation: Callable[[], bytes]) -> bytes:
        nonlocal calls
        if calls != 0:
            raise RuntimeError("capture-boundaries permits exactly one loopback GET")
        calls += 1
        socket.socket.connect = original_connect  # type: ignore[assignment]
        socket.create_connection = original_create  # type: ignore[assignment]
        urllib.request.urlopen = original_urlopen  # type: ignore[assignment]
        try:
            return operation()
        finally:
            socket.socket.connect = blocked  # type: ignore[assignment]
            socket.create_connection = blocked  # type: ignore[assignment]
            urllib.request.urlopen = blocked  # type: ignore[assignment]

    socket.socket.connect = blocked  # type: ignore[assignment]
    socket.create_connection = blocked  # type: ignore[assignment]
    urllib.request.urlopen = blocked  # type: ignore[assignment]
    try:
        yield exact_get
        if calls != 1:
            raise RuntimeError("capture-boundaries requires exactly one loopback GET")
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
        if values == ["openclaw", "cron", "list", "--json"]:
            return True
        return (
            len(values) == 7
            and values[0] == "git"
            and values[1] == "-C"
            and Path(values[2]).is_absolute()
            and values[3:] == [
                "status", "--porcelain=v1", "-z", "--untracked-files=all"
            ]
        )
    if command in {"build-fixtures", "ingest-human-gate", "verify"}:
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
        unknown = set(kwargs) - {"check", "capture_output", "text", "stdout", "stderr"}
        if unknown:
            raise RuntimeError("child process options are not allowlisted")
        if kwargs.get("stdout") not in {None, subprocess.PIPE} or kwargs.get(
            "stderr"
        ) not in {None, subprocess.PIPE}:
            raise RuntimeError("child process options are not allowlisted")
        if kwargs.get("capture_output") and (
            "stdout" in kwargs or "stderr" in kwargs
        ):
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


def _payload_binding(
    role: str, path: Path, payload: bytes, root: Path
) -> Dict[str, object]:
    return {
        "role": role,
        "path": _relative(path, root),
        "sha256": sha256_hex(payload),
    }


def _build_receipt(
    *,
    command: str,
    run_context_path: Path,
    run_context: Dict[str, object],
    manifest: Dict[str, object],
    expected_manifest_sha256: Optional[str],
    inputs: Sequence[Tuple[str, Path]],
    outputs: Sequence[Tuple[str, Path, bytes]],
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
            [
                _payload_binding(role, path, payload, workspace_root)
                for role, path, payload in outputs
            ],
            key=lambda item: (str(item["role"]), str(item["path"])),
        ),
        generated_at=str(run_context["generatedAt"]),
    )
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


def _stable_stat_identity(value: os.stat_result) -> Tuple[int, int, int, int, int]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_size,
        value.st_mtime_ns,
    )


def _hash_worktree_node(path: Path) -> Tuple[str, str]:
    """Hash one working-tree node without following symlinks or exposing bytes."""

    before = os.lstat(str(path))
    if stat.S_ISREG(before.st_mode):
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(str(path), flags)
        digest = hashlib.sha256()
        try:
            opened = os.fstat(descriptor)
            if _stable_stat_identity(opened) != _stable_stat_identity(before):
                raise RuntimeError("working-tree file changed before fingerprinting")
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        if _stable_stat_identity(after) != _stable_stat_identity(before):
            raise RuntimeError("working-tree file changed while fingerprinting")
        return "file", digest.hexdigest()
    if stat.S_ISLNK(before.st_mode):
        target = os.readlink(os.fsencode(str(path)))
        after = os.lstat(str(path))
        if _stable_stat_identity(after) != _stable_stat_identity(before):
            raise RuntimeError("working-tree symlink changed while fingerprinting")
        if isinstance(target, str):
            target_bytes = os.fsencode(target)
        else:
            target_bytes = target
        return "symlink", sha256_hex(target_bytes)
    if stat.S_ISDIR(before.st_mode):
        children: List[Dict[str, object]] = []
        with os.scandir(str(path)) as iterator:
            names = sorted((entry.name for entry in iterator), key=os.fsencode)
        for name in names:
            kind, digest = _hash_worktree_node(path / name)
            children.append(
                {
                    "nameSha256": sha256_hex(os.fsencode(name)),
                    "kind": kind,
                    "contentSha256": digest,
                }
            )
        after = os.lstat(str(path))
        if _stable_stat_identity(after) != _stable_stat_identity(before):
            raise RuntimeError("working-tree directory changed while fingerprinting")
        return "directory", sha256_hex(canonical_bytes(children))
    raise ValueError("working-tree fingerprint refuses special filesystem nodes")


def _status_content_entries(root: Path, status: bytes) -> List[Dict[str, object]]:
    """Parse porcelain-v1-z and bind every dirty path to exact current content."""

    tokens = status.split(b"\0")
    entries: List[Dict[str, object]] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if not token:
            continue
        if len(token) < 4 or token[2:3] != b" ":
            raise ValueError("git status porcelain record is malformed")
        try:
            code = token[:2].decode("ascii")
        except UnicodeDecodeError as error:
            raise ValueError("git status code must be ASCII") from error
        raw_path = token[3:]
        relative = Path(os.fsdecode(raw_path))
        if (
            not raw_path
            or relative.is_absolute()
            or any(part in {"", ".", ".."} for part in relative.parts)
        ):
            raise ValueError("git status path is not canonical workspace-relative")
        cursor = root
        for part in relative.parts[:-1]:
            cursor = cursor / part
            parent = os.lstat(str(cursor))
            if stat.S_ISLNK(parent.st_mode) or not stat.S_ISDIR(parent.st_mode):
                raise ValueError("git status path traverses a non-directory or symlink")
        path = root / relative
        try:
            kind, content_digest = _hash_worktree_node(path)
        except FileNotFoundError:
            if "D" not in code:
                raise RuntimeError("working-tree path disappeared while fingerprinting")
            kind, content_digest = "missing", sha256_hex(b"")
        entry: Dict[str, object] = {
            "status": code,
            "pathSha256": sha256_hex(raw_path),
            "kind": kind,
            "contentSha256": content_digest,
        }
        if "R" in code or "C" in code:
            if index >= len(tokens) or not tokens[index]:
                raise ValueError("git rename/copy status lacks its source path")
            entry["sourcePathSha256"] = sha256_hex(tokens[index])
            index += 1
        entries.append(entry)
    return entries


def _primary_checkout_fingerprint(
    root: Path = Path("/Users/jtsomwaru/.openclaw/workspace"),
    *,
    runner: Optional[Callable[..., subprocess.CompletedProcess]] = None,
) -> str:
    root = Path(root).resolve()
    entries: List[Dict[str, object]] = []
    for relative in (".git/HEAD", ".git/index"):
        path = root / relative
        if path.is_file():
            entries.append({"path": relative, "sha256": sha256_hex(path.read_bytes())})
    active_runner = subprocess.run if runner is None else runner
    completed = active_runner(
        [
            "git", "-C", str(root), "status", "--porcelain=v1", "-z",
            "--untracked-files=all",
        ],
        check=True,
        capture_output=True,
        text=False,
    )
    status = completed.stdout
    if not isinstance(status, bytes):
        raise ValueError("git status fingerprint requires byte output")
    entries.append({"path": ".git/status-porcelain-v1-z", "sha256": sha256_hex(status)})
    entries.append(
        {
            "path": ".git/dirty-content",
            "sha256": sha256_hex(canonical_bytes(_status_content_entries(root, status))),
        }
    )
    return sha256_hex(canonical_bytes(entries))


def _capture_boundaries(args: argparse.Namespace) -> Dict[str, object]:
    run_context = _run_context(Path(args.run_context))
    with _capture_network_guard() as exact_get:
        raw = exact_get(lambda: capture_tasks(SOURCE_URL))
    snapshot = validate_snapshot(
        raw,
        {
            "runId": run_context["runId"],
            "generatedAt": run_context["generatedAt"],
        },
    )
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
    if args.mc_output:
        write_json_atomic(Path(args.mc_output), snapshot)
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
    recovery = audit["recoveryRequest"]
    assert isinstance(recovery, dict)
    audit_payload = canonical_bytes(audit)
    recovery_payload = canonical_bytes(recovery)
    result: Dict[str, object] = {"audit": audit, "recoveryRequest": recovery}
    receipt: Optional[Dict[str, object]] = None
    if authority:
        if args.receipt_output is None:
            raise ValueError("phase-2 audit requires --receipt-output")
        assert manifest is not None
        receipt = _build_receipt(
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
                ("historical_audit", Path(args.output), audit_payload),
                ("recovery_request", Path(args.recovery_output), recovery_payload),
            ),
            workspace_root=Path(args.workspace_root),
        )
        result["authorityConsumptionReceipt"] = receipt
    _write_bytes_atomic(Path(args.output), audit_payload)
    _write_bytes_atomic(Path(args.recovery_output), recovery_payload)
    if receipt is not None:
        _write_bytes_atomic(Path(args.receipt_output), canonical_bytes(receipt))
    return result


def _build_focus(args: argparse.Namespace) -> Dict[str, object]:
    context = _run_context(Path(args.run_context))
    root = Path(args.workspace_root)
    if args.outcomes is not None:
        return _task7b_handler("rebuild_focus_files", args)
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
    gold = build_voice_gold(audit, events, expected_manifest_sha256=expected)
    pairs = build_contrastive_pairs(events, audit, expected_manifest_sha256=expected)
    gold_payload = _jsonl_bytes(gold)
    pairs_payload = _jsonl_bytes(pairs)
    manifest = audit.get("corpusAuthorityManifest")
    if not isinstance(manifest, dict):
        raise ValueError("audit lacks corpus authority manifest")
    receipt = _build_receipt(
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
            ("voice_gold", Path(args.gold_output), gold_payload),
            ("contrastive_pairs", Path(args.pairs_output), pairs_payload),
        ),
        workspace_root=Path(args.workspace_root),
    )
    _write_bytes_atomic(Path(args.gold_output), gold_payload)
    _write_bytes_atomic(Path(args.pairs_output), pairs_payload)
    _write_bytes_atomic(Path(args.receipt_output), canonical_bytes(receipt))
    return {"voiceGoldCount": len(gold), "contrastivePairCount": len(pairs), "receipt": receipt}


def _build_fixtures(args: argparse.Namespace) -> Dict[str, object]:
    if args.decagon_packet != DECAGON_PACKET_PATH:
        raise ValueError("--decagon-packet must be the reviewed Decagon packet path")
    if args.human_gate_response is not None:
        if any(
            value is not None
            for value in (args.jt_ops_git_dir, args.jt_ops_commit, args.jt_ops_path)
        ):
            raise ValueError("phase-2 build-fixtures rejects pre-gate Git arguments")
        return _task7b_handler("rebuild_fixtures_files", args)
    if any(
        value is None
        for value in (args.jt_ops_git_dir, args.jt_ops_commit, args.jt_ops_path)
    ):
        raise ValueError("pre-gate build-fixtures requires the reviewed Git object")
    context_path = Path(args.run_context) if args.run_context else Path(
        args.workspace_root
    ) / "memory/content/linkedin-content-os/run-context.v1.json"
    context = _run_context(context_path)
    generated_at = str(context["generatedAt"])
    parse_timestamp(generated_at, "generatedAt")
    if args.jt_ops_commit != PRE_GATE_COMMIT or args.jt_ops_path != PRE_GATE_PATH:
        raise ValueError("build-fixtures source does not match the reviewed Git object")
    rows = build_evaluation_fixtures(
        Path(args.workspace_root).resolve(),
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


def _validate_receipt_snapshot_bindings(
    receipt: Dict[str, object],
    *,
    root: Path,
    snapshots: _VerifierSnapshots,
) -> None:
    bindings = list(receipt["inputs"]) + list(receipt["outputs"])
    for binding in bindings:
        assert isinstance(binding, dict)
        unresolved = root / str(binding["path"])
        try:
            path = snapshots.resolved(unresolved)
            path.relative_to(root)
        except (OSError, ValueError) as error:
            raise ValueError(
                "bound receipt path escapes workspace or is unavailable"
            ) from error
        if snapshots.sha256(path) != binding["sha256"]:
            raise ValueError("bound receipt byte hash mismatch")
    run_binding = next(
        item for item in receipt["inputs"] if item["role"] == "run_context"
    )
    run_path = snapshots.resolved(root / str(run_binding["path"]))
    run_context = snapshots.json(run_path)
    if run_context.get("generatedAt") != receipt["generatedAt"]:
        raise ValueError("receipt generatedAt differs from bound run context")


def _verifier_relative(target: Path, root: Path) -> str:
    """Render an already-bound target without consulting the filesystem again."""

    try:
        return target.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError("artifact path must stay under workspace root") from error


_SUPPLEMENT_ARGUMENTS = (
    "supplement",
    "supplement_run_context",
    "supplement_authority_run_context",
    "supplement_manifest",
    "supplement_before",
    "supplement_after",
)
_AUTHORITY_EVENT_TYPES = {"historical_status", "correction", "corpus_authority_receipt"}
_GOVERNED_BOUNDARY_KEYS = (
    "missionControl", "cronDefinitionSha256", "launchAgents",
    "protectedInputs", "primaryCheckoutFingerprint",
)


def _verify_supplement(
    args: argparse.Namespace,
    *,
    snapshots: "_VerifierSnapshots",
    root: Path,
    artifact_root: Path,
    base_context: Dict[str, object],
    events: List[Dict[str, object]],
) -> Dict[str, object]:
    """Re-derive one supplemental human-gate authority and prove its equal boundary pair."""

    from scripts.linkedin_content_os.recovery import (
        _supplement_block_positions,
        _validate_supplement_document,
        derive_history_supplement,
    )

    supplement_path = Path(args.supplement)
    supplement_value = snapshots.json(supplement_path)
    document = _validate_supplement_document(supplement_value)
    supplement_context = _validate_run_context(
        snapshots.json(Path(args.supplement_run_context))
    )
    supplement_authority_path = Path(args.supplement_authority_run_context)
    supplement_authority = _validate_run_context(
        snapshots.json(supplement_authority_path), authority=True
    )
    if supplement_authority["generatedAt"] != supplement_context["generatedAt"]:
        raise ValueError("supplement authority context is not bound to the supplement run context")
    response_path = artifact_root / "human-gate-response.v1.json"
    request_path = artifact_root / "historical-recovery-request.phase-1.v1.json"
    owned = _supplement_block_positions(events, str(document["supplementId"]))
    if not owned:
        raise ValueError("supplement block is missing from the canonical ledger")
    first = owned[0]
    derived = derive_history_supplement(
        supplement=supplement_value,
        supplement_sha256=snapshots.sha256(supplement_path),
        base_response=snapshots.json(response_path),
        base_response_sha256=snapshots.sha256(response_path),
        base_manifest=snapshots.json(Path(args.corpus_authority_manifest)),
        base_authority_context=base_context,
        request=snapshots.json(request_path),
        prior_events=events[:first],
        run_context=supplement_context,
    )
    block = list(derived["events"])  # type: ignore[arg-type]
    if (
        owned != list(range(first, first + len(block)))
        or canonical_bytes(events[first:first + len(block)]) != canonical_bytes(block)
    ):
        raise ValueError("supplement ledger block does not match its governed derivation")
    if any(
        event["eventType"] in _AUTHORITY_EVENT_TYPES
        for event in events[first + len(block):]
    ):
        raise ValueError("ledger carries authority beyond the verified supplement")
    manifest_path = Path(args.supplement_manifest)
    if snapshots.bytes(manifest_path) != canonical_bytes(derived["corpusAuthorityManifest"]):
        raise ValueError("supplement manifest does not match its governed derivation")
    if snapshots.bytes(supplement_authority_path) != canonical_bytes(derived["authorityRunContext"]):
        raise ValueError("supplement authority context does not match its governed derivation")
    boundary_paths = (Path(args.supplement_before), Path(args.supplement_after))
    before, after = (validate_boundary_artifact(snapshots.json(path)) for path in boundary_paths)
    if [before["phase"], after["phase"]] != ["supplement-before", "supplement-after"]:
        raise ValueError("supplement boundary artifacts are not in the required phase order")
    for artifact in (before, after):
        if (
            artifact["runId"] != supplement_context["runId"]
            or artifact["generatedAt"] != supplement_context["generatedAt"]
        ):
            raise ValueError("boundary pair is bound to the wrong phase context")
    for key in _GOVERNED_BOUNDARY_KEYS:
        if before.get(key) != after.get(key):
            raise ValueError("boundary changed for {}".format(key))
    equality_row = {
        "beforePath": _verifier_relative(snapshots.resolved(boundary_paths[0]), root),
        "afterPath": _verifier_relative(snapshots.resolved(boundary_paths[1]), root),
        "beforeFileSha256": snapshots.sha256(boundary_paths[0]),
        "afterFileSha256": snapshots.sha256(boundary_paths[1]),
        "beforeSha256": before["boundarySha256"],
        "afterSha256": after["boundarySha256"],
        "governedKeys": list(_GOVERNED_BOUNDARY_KEYS),
        "governedValuesEqual": True,
        "runId": supplement_context["runId"],
        "generatedAt": supplement_context["generatedAt"],
    }
    return {
        "context": supplement_authority,
        "contextPath": supplement_authority_path,
        "manifestPath": manifest_path,
        "requestPath": request_path,
        "equalityRow": equality_row,
        "report": {
            "supplementPath": _verifier_relative(snapshots.resolved(supplement_path), root),
            "supplementId": derived["supplementId"],
            "supplementSha256": derived["supplementSha256"],
            "runContextSha256": snapshots.sha256(Path(args.supplement_run_context)),
            "authorityContextDigest": snapshots.sha256(supplement_authority_path),
            "manifestPath": _verifier_relative(snapshots.resolved(manifest_path), root),
            "manifestSha256": derived["corpusAuthorityManifest"]["manifestSha256"],  # type: ignore[index]
            "runId": derived["runId"],
            "priorEventCount": derived["priorEventCount"],
            "blockEventCount": len(block),
            "corrections": derived["corrections"],
        },
    }


def _verify(args: argparse.Namespace) -> Dict[str, object]:
    snapshots = _VerifierSnapshots()
    base_context_path = Path(args.run_context)
    base_context = _validate_run_context(
        snapshots.json(base_context_path), authority=True
    )
    root = Path(args.workspace_root).resolve()
    artifact_root = root / "memory/content/linkedin-content-os"
    audit = snapshots.json(artifact_root / "historical-audit.v1.json")
    source_sha = _require_hash(audit.get("sourceSha256"), "audit.sourceSha256")
    audit_generated_at = str(audit.get("generatedAt"))
    base_manifest_value = validate_corpus_authority_manifest(
        snapshots.json(Path(args.corpus_authority_manifest)),
        expected_run_id=corpus_run_id(source_sha, str(base_context["generatedAt"])),
        generated_at=str(base_context["generatedAt"]),
        expected_manifest_sha256=str(base_context["corpusAuthorityManifestSha256"]),
    )
    events = validate_events(snapshots.jsonl(artifact_root / "outcomes.v1.jsonl"))
    supplied = [getattr(args, name, None) is not None for name in _SUPPLEMENT_ARGUMENTS]
    if any(supplied) and not all(supplied):
        raise ValueError("supplement arguments must be supplied all together")
    supplement: Optional[Dict[str, object]] = None
    if all(supplied):
        supplement = _verify_supplement(
            args,
            snapshots=snapshots,
            root=root,
            artifact_root=artifact_root,
            base_context=base_context,
            events=events,
        )
        context = supplement["context"]
        assert isinstance(context, dict)
        context_path = Path(str(supplement["contextPath"]))
        effective_manifest_path = Path(str(supplement["manifestPath"]))
    else:
        base_position = int(base_manifest_value["ledgerPosition"])
        if any(event["eventType"] in _AUTHORITY_EVENT_TYPES for event in events[base_position:]):
            raise ValueError(
                "ledger carries supplemental human-gate authority; "
                "supplement verification arguments are required"
            )
        context = base_context
        context_path = base_context_path
        effective_manifest_path = Path(args.corpus_authority_manifest)
    if audit_generated_at != context["generatedAt"]:
        raise ValueError("historical audit is not bound to the effective authority context")
    expected = str(context["corpusAuthorityManifestSha256"])
    canonical_manifest_value = validate_corpus_authority_manifest(
        snapshots.json(effective_manifest_path),
        expected_run_id=corpus_run_id(source_sha, audit_generated_at),
        generated_at=audit_generated_at,
        expected_manifest_sha256=expected,
    )
    canonical_manifest = str(canonical_manifest_value["manifestSha256"])
    authority_context_sha256 = snapshots.sha256(context_path)
    receipts = []
    for path_value in (
        args.phase_1_corpus_receipt,
        args.phase_2_audit_receipt,
        args.phase_2_corpus_receipt,
    ):
        path = Path(path_value)
        receipt = validate_authority_consumption_receipt(snapshots.json(path))
        _validate_receipt_snapshot_bindings(
            receipt, root=root, snapshots=snapshots
        )
        receipts.append({
            "path": _verifier_relative(snapshots.resolved(path), root),
            "sha256": snapshots.sha256(path),
            "receipt": receipt,
        })
    receipt_commands = [item["receipt"]["command"] for item in receipts]
    if receipt_commands != ["build-corpus", "audit-history", "build-corpus"]:
        raise ValueError("authority consumption receipts are not in the required phase order")
    if receipts[0]["receipt"]["expectedManifestSha256"] is not None:
        raise ValueError("phase-1 corpus receipt must use the fixed-empty authority")
    for item in receipts[1:]:
        if item["receipt"]["expectedManifestSha256"] != expected:
            raise ValueError("phase-2 receipt authority digest mismatch")
        if item["receipt"]["runContextSha256"] != authority_context_sha256:
            raise ValueError("phase-2 receipt is not bound to the authority context")
        if item["receipt"]["canonicalManifestSha256"] != canonical_manifest:
            raise ValueError("phase-2 receipt canonical manifest digest mismatch")
    phase2_audit_inputs = {
        item["role"]: item for item in receipts[1]["receipt"]["inputs"]
    }
    manifest_binding = phase2_audit_inputs["authority_manifest"]
    manifest_path = snapshots.resolved(effective_manifest_path)
    if (
        snapshots.resolved(root / str(manifest_binding["path"])) != manifest_path
        or manifest_binding["sha256"] != snapshots.sha256(manifest_path)
    ):
        raise ValueError("phase-2 audit receipt is not bound to the supplied authority manifest")
    expected_phase2_paths = (
        {
            "authority_manifest": effective_manifest_path,
            "outcomes": artifact_root / "outcomes.v1.jsonl",
            "posted_log": root / "memory/content/posted-log.jsonl",
            "run_context": context_path,
        },
        {
            "historical_audit": artifact_root / "historical-audit.v1.json",
            "recovery_request": artifact_root / "historical-recovery-request.v1.json",
        },
        {
            "audit": artifact_root / "historical-audit.v1.json",
            "outcomes": artifact_root / "outcomes.v1.jsonl",
            "run_context": context_path,
        },
        {
            "contrastive_pairs": artifact_root / "contrastive-pairs.v0.jsonl",
            "voice_gold": artifact_root / "voice-gold.v0.jsonl",
        },
    )
    for receipt_index, expected_inputs, expected_outputs in (
        (1, expected_phase2_paths[0], expected_phase2_paths[1]),
        (2, expected_phase2_paths[2], expected_phase2_paths[3]),
    ):
        for collection, expected_paths in (
            (receipts[receipt_index]["receipt"]["inputs"], expected_inputs),
            (receipts[receipt_index]["receipt"]["outputs"], expected_outputs),
        ):
            observed = {
                item["role"]: snapshots.resolved(root / str(item["path"]))
                for item in collection
            }
            canonical_expected = {
                role: snapshots.resolved(path) for role, path in expected_paths.items()
            }
            if observed != canonical_expected:
                raise ValueError("phase-2 receipt paths do not match canonical artifacts")

    phase1_receipt = receipts[0]["receipt"]
    phase1_run_binding = next(
        item for item in phase1_receipt["inputs"] if item["role"] == "run_context"
    )
    phase1_context_path = snapshots.resolved(root / str(phase1_run_binding["path"]))
    phase1_context = _validate_run_context(snapshots.json(phase1_context_path))
    phase1_audit_binding = next(
        item for item in phase1_receipt["inputs"] if item["role"] == "audit"
    )
    phase1_audit = snapshots.json(
        snapshots.resolved(root / str(phase1_audit_binding["path"]))
    )
    phase1_manifest = phase1_audit.get("corpusAuthorityManifest")
    if not isinstance(phase1_manifest, dict):
        raise ValueError("phase-1 audit lacks its fixed-empty authority manifest")
    validated_phase1_manifest = validate_corpus_authority_manifest(
        phase1_manifest,
        expected_run_id=corpus_run_id(
            _require_hash(phase1_audit.get("sourceSha256"), "phase1Audit.sourceSha256"),
            str(phase1_audit.get("generatedAt")),
        ),
        generated_at=str(phase1_audit.get("generatedAt")),
        expected_manifest_sha256=None,
    )
    if phase1_receipt["canonicalManifestSha256"] != validated_phase1_manifest["manifestSha256"]:
        raise ValueError("phase-1 receipt fixed-empty manifest digest mismatch")
    boundary_paths = [Path(value) for value in (
        args.phase_1_before, args.phase_1_after, args.phase_2_before, args.phase_2_after
    )]
    boundaries = [
        validate_boundary_artifact(snapshots.json(path)) for path in boundary_paths
    ]
    expected_phases = [
        "phase-1-before", "phase-1-after", "phase-2-before", "phase-2-after"
    ]
    if [item["phase"] for item in boundaries] != expected_phases:
        raise ValueError("boundary artifacts are not in the required phase order")
    phase2_base_unsigned = {
        "schemaVersion": RUN_CONTEXT_SCHEMA,
        "generatedAt": base_context["generatedAt"],
    }
    phase2_base_run_id = "sha256:" + sha256_hex(canonical_bytes(phase2_base_unsigned))
    expected_boundary_contexts = (
        (str(phase1_context["runId"]), str(phase1_context["generatedAt"])),
        (phase2_base_run_id, str(base_context["generatedAt"])),
    )
    equality_rows: List[Dict[str, object]] = []
    governed_keys = _GOVERNED_BOUNDARY_KEYS
    for pair_index, (before, after) in enumerate(
        ((boundaries[0], boundaries[1]), (boundaries[2], boundaries[3]))
    ):
        expected_run_id, expected_generated_at = expected_boundary_contexts[pair_index]
        if before["runId"] != after["runId"] or before["generatedAt"] != after["generatedAt"]:
            raise ValueError("boundary pair run context mismatch")
        if before["runId"] != expected_run_id or before["generatedAt"] != expected_generated_at:
            raise ValueError("boundary pair is bound to the wrong phase context")
        equal = True
        for key in governed_keys:
            if before.get(key) != after.get(key):
                raise ValueError("boundary changed for {}".format(key))
        equality_rows.append({
            "beforePath": _verifier_relative(
                snapshots.resolved(boundary_paths[pair_index * 2]), root
            ),
            "afterPath": _verifier_relative(
                snapshots.resolved(boundary_paths[pair_index * 2 + 1]), root
            ),
            "beforeFileSha256": snapshots.sha256(
                boundary_paths[pair_index * 2]
            ),
            "afterFileSha256": snapshots.sha256(
                boundary_paths[pair_index * 2 + 1]
            ),
            "beforeSha256": before["boundarySha256"],
            "afterSha256": after["boundarySha256"],
            "governedKeys": list(governed_keys),
            "governedValuesEqual": equal,
            "runId": expected_run_id,
            "generatedAt": expected_generated_at,
        })
    if supplement is not None:
        equality_rows.append(dict(supplement["equalityRow"]))  # type: ignore[arg-type]
    focus = snapshots.json(artifact_root / "focus-snapshot.v1.json")
    fixture_path = artifact_root / "evaluation-fixtures.v0.jsonl"
    fixture_bytes = snapshots.bytes(fixture_path)
    fixtures = read_jsonl_bytes(fixture_bytes, str(fixture_path))
    gold = snapshots.jsonl(artifact_root / "voice-gold.v0.jsonl")
    pairs = snapshots.jsonl(artifact_root / "contrastive-pairs.v0.jsonl")
    checkin = snapshots.json(artifact_root / "checkin.preview.v1.json")
    from scripts.linkedin_content_os.recovery import (
        derive_authorized_fixture_rows,
        validate_human_gate_history_authority,
        validate_permission_fixture_authority,
    )
    response_path = artifact_root / "human-gate-response.v1.json"
    response_value = snapshots.json(response_path)
    response_bytes = snapshots.bytes(response_path)
    permission_authority = validate_permission_fixture_authority(
        response_value,
        response_bytes,
        snapshots.json(artifact_root / "focus-authority-receipt.v1.json"),
        snapshots.json(artifact_root / "focus-authority-anchor.v1.json"),
        events,
    )
    permission_receipt = permission_authority["authorityReceipt"]
    assert isinstance(permission_receipt, dict)
    if (
        base_manifest_value["humanGateAuthorityReceiptSha256"]
            != permission_authority["responseSha256"]
        or base_manifest_value["ledgerPrefixSha256"]
            != permission_receipt["ledgerPrefixSha256"]
        or base_manifest_value["ledgerPosition"]
            != permission_receipt["ledgerPosition"]
    ):
        raise ValueError("authority manifest does not bind the accepted permission response")
    permission_response = permission_authority["response"]
    assert isinstance(permission_response, dict)
    phase1_recovery_request = phase1_audit.get("recoveryRequest")
    if not isinstance(phase1_recovery_request, dict):
        raise ValueError("phase-1 audit lacks the original bounded recovery request")
    if supplement is not None and snapshots.bytes(
        Path(str(supplement["requestPath"]))
    ) != canonical_bytes(phase1_recovery_request):
        raise ValueError("supplement recovery request is not the phase-1 bounded request")
    history_authority = validate_human_gate_history_authority(
        response_value,
        response_bytes,
        phase1_recovery_request,
        events,
        permission_receipt,
        run_id=str(base_manifest_value["runId"]),
    )
    expected_fixture_rows = derive_authorized_fixture_rows(
        permission_response, root
    )
    expected_fixture_bytes = b"".join(
        canonical_bytes(row) + b"\n" for row in expected_fixture_rows
    )
    if fixture_bytes != expected_fixture_bytes:
        raise ValueError(
            "evaluation fixture artifact does not match canonical authority derivation"
        )
    derived_gold = build_voice_gold(audit, events, expected_manifest_sha256=expected)
    derived_pairs = build_contrastive_pairs(events, audit, expected_manifest_sha256=expected)
    if canonical_bytes(gold) != canonical_bytes(derived_gold):
        raise ValueError("voice-gold artifact does not match canonical derivation")
    if canonical_bytes(pairs) != canonical_bytes(derived_pairs):
        raise ValueError("contrastive-pair artifact does not match canonical derivation")
    snapshot = snapshots.json(artifact_root / "mission-control.snapshot.v1.json")
    derived_checkin = project_checkin(
        snapshot, events, parse_timestamp(base_context["generatedAt"], "generatedAt")
    )
    expected_checkin: Dict[str, object] = (
        derived_checkin
        if derived_checkin is not None
        else {
            "schemaVersion": "linkedin-checkin-preview.v1",
            "sourceSnapshotSha256": snapshot.get("projectionSha256"),
            "liveWriteAuthorized": False,
            "task": None,
        }
    )
    if canonical_bytes(checkin) != canonical_bytes(expected_checkin):
        raise ValueError("check-in preview does not match canonical derivation")
    policy_path = artifact_root / "source-policy.v1.json"
    if policy_path.exists():
        validate_source_policy(snapshots.json(policy_path))
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
    if not isinstance(targets, list) or not targets:
        raise ValueError("focus targets must be a non-empty list")
    human_gate_resolved = not recovery["items"] and focus.get("status") == "confirmed" and classifications["positive"] >= 1
    governed_boundaries_equal = all(
        bool(item["governedValuesEqual"]) for item in equality_rows
    )
    report = {
        "schemaVersion": "linkedin-program-0-verification.v1",
        "authorityContextDigest": authority_context_sha256,
        "canonicalManifestSha256": canonical_manifest,
        "receipts": [{"path": item["path"], "sha256": item["sha256"]} for item in receipts],
        "authorityConsumptionBindings": {
            "phase1Corpus": receipts[0]["receipt"],
            "phase2Audit": receipts[1]["receipt"],
            "phase2Corpus": receipts[2]["receipt"],
        },
        "boundaryProof": equality_rows,
        "boundaryPairsEqual": governed_boundaries_equal,
        "statusCounts": status_counts,
        "missingUrlCount": int(missing_counts.get("public_url", 0)),
        "missingFinalTextCount": int(missing_counts.get("final_text", 0)),
        "focusTargets": targets,
        "voiceGoldCount": voice_gold_count,
        "contrastivePairCount": pair_count,
        "fixtureClassifications": classifications,
        "checkinPreviewCount": 0 if task_value is None else 1,
        "humanGateAnswerCount": history_authority["answerCount"],
        "humanGateResolved": human_gate_resolved,
        "liveOrExternalActionOccurred": not governed_boundaries_equal,
        "verdict": "program-0-local-proof-ready-for-independent-verification",
    }
    if supplement is not None:
        report["baseAuthority"] = {
            "authorityContextDigest": snapshots.sha256(base_context_path),
            "manifestSha256": base_manifest_value["manifestSha256"],
            "ledgerPosition": base_manifest_value["ledgerPosition"],
        }
        report["supplementalAuthority"] = supplement["report"]
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
    ingest.add_argument("--focus-authority-receipt-output")
    ingest.add_argument("--focus-authority-anchor-output")

    correction = subparsers.add_parser("ingest-history-correction")
    for name in (
        "supplement", "base-response", "base-manifest", "base-authority-run-context",
        "recovery-request", "outcomes", "run-context",
        "corpus-authority-manifest-output", "authority-run-context-output",
    ):
        correction.add_argument("--" + name, required=True)
    correction.add_argument("--workspace-root", default=".")

    focus = subparsers.add_parser("build-focus")
    focus.add_argument("--workspace-root", required=True)
    focus.add_argument("--outcomes")
    focus.add_argument("--run-context", required=True)
    focus.add_argument("--focus-authority-receipt")
    focus.add_argument("--focus-authority-anchor")
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
    fixtures.add_argument("--jt-ops-git-dir")
    fixtures.add_argument("--jt-ops-commit")
    fixtures.add_argument("--jt-ops-path")
    fixtures.add_argument("--output", required=True)
    fixtures.add_argument("--run-context")
    fixtures.add_argument("--workspace-root", default=".")
    fixtures.add_argument("--human-gate-response")
    fixtures.add_argument("--outcomes")
    fixtures.add_argument("--focus-authority-receipt")
    fixtures.add_argument("--focus-authority-anchor")

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
    for name in _SUPPLEMENT_ARGUMENTS:
        verify.add_argument("--" + name.replace("_", "-"))
    return parser


def _task7b_handler(name: str, args: argparse.Namespace) -> Dict[str, object]:
    try:
        from scripts.linkedin_content_os import recovery
    except ImportError as error:
        raise RuntimeError(
            "Task 7B recovery module unavailable until the governed human response"
        ) from error
    handler = getattr(recovery, name, None)
    if not callable(handler):
        raise RuntimeError("Task 7B recovery module lacks {}".format(name))
    result = handler(args)
    if not isinstance(result, dict):
        raise ValueError("Task 7B handler must return an object")
    return result


def _ingest_human_gate(args: argparse.Namespace) -> Dict[str, object]:
    return _task7b_handler("ingest_human_gate_files", args)


def _ingest_history_correction(args: argparse.Namespace) -> Dict[str, object]:
    return _task7b_handler("ingest_history_supplement_files", args)


def _present_paths(args: argparse.Namespace, names: Sequence[str]) -> List[Path]:
    result: List[Path] = []
    for name in names:
        value = getattr(args, name, None)
        if value is not None:
            result.append(Path(value))
    return result


def _validate_command_paths(args: argparse.Namespace) -> None:
    """Apply each command's closed read/write path partition before dispatch."""

    if args.command == "ingest-human-gate":
        directory = Path(args.response).parent
        if args.focus_authority_receipt_output is None:
            args.focus_authority_receipt_output = str(
                directory / "focus-authority-receipt.v1.json"
            )
        if args.focus_authority_anchor_output is None:
            args.focus_authority_anchor_output = str(
                directory / "focus-authority-anchor.v1.json"
            )
    elif args.command == "build-focus" and args.outcomes is not None:
        directory = Path(args.output).parent
        if args.focus_authority_receipt is None:
            args.focus_authority_receipt = str(
                directory / "focus-authority-receipt.v1.json"
            )
        if args.focus_authority_anchor is None:
            args.focus_authority_anchor = str(
                directory / "focus-authority-anchor.v1.json"
            )
    elif args.command == "build-fixtures" and args.human_gate_response is not None:
        directory = Path(args.human_gate_response).parent
        if args.outcomes is None:
            args.outcomes = str(directory / "outcomes.v1.jsonl")
        if args.focus_authority_receipt is None:
            args.focus_authority_receipt = str(
                directory / "focus-authority-receipt.v1.json"
            )
        if args.focus_authority_anchor is None:
            args.focus_authority_anchor = str(
                directory / "focus-authority-anchor.v1.json"
            )

    contracts: Dict[str, Tuple[Sequence[str], Sequence[str], Sequence[str]]] = {
        "capture-boundaries": (("run_context",), ("mc_output", "output"), ()),
        "audit-history": (
            ("posted_log", "outcomes", "corpus_authority_manifest", "run_context"),
            ("output", "recovery_output"), ("receipt_output",),
        ),
        "ingest-human-gate": (
            ("response", "recovery_request", "focus", "fixtures", "outcomes", "run_context"),
            (
                "corpus_authority_manifest_output", "authority_run_context_output",
                "focus_authority_receipt_output", "focus_authority_anchor_output",
            ), (),
        ),
        "ingest-history-correction": (
            (
                "supplement", "base_response", "base_manifest",
                "base_authority_run_context", "recovery_request", "outcomes", "run_context",
            ),
            ("corpus_authority_manifest_output", "authority_run_context_output"), (),
        ),
        "build-focus": (
            (
                "run_context", "outcomes", "focus_authority_receipt",
                "focus_authority_anchor",
            ), ("output",), (),
        ),
        "build-corpus": (
            ("audit", "outcomes", "run_context"),
            ("gold_output", "pairs_output"), ("receipt_output",),
        ),
        "build-fixtures": (
            (
                "decagon_packet", "human_gate_response", "run_context", "outcomes",
                "focus_authority_receipt", "focus_authority_anchor",
            ), ("output",), (),
        ),
        "build-source-policy": (("run_context",), ("output",), ()),
        "audit-voice-rules": (("run_context",), ("output",), ()),
        "preview-checkin": (("mc_snapshot", "outcomes", "run_context"), ("output",), ()),
        "verify": (
            (
                "run_context", "corpus_authority_manifest", "phase_1_corpus_receipt",
                "phase_2_audit_receipt", "phase_2_corpus_receipt", "phase_1_before",
                "phase_1_after", "phase_2_before", "phase_2_after",
            ) + _SUPPLEMENT_ARGUMENTS,
            ("report",), (),
        ),
    }
    if args.command == "init-run":
        return
    inputs, outputs, receipts = contracts[args.command]
    _validate_distinct_paths(
        inputs=_present_paths(args, inputs),
        outputs=_present_paths(args, outputs),
        receipts=_present_paths(args, receipts),
        workspace_root=Path(getattr(args, "workspace_root", ".")),
    )


def main(argv: Optional[Sequence[str]] = None) -> Dict[str, object]:
    args = _parser().parse_args(argv)
    _validate_command_paths(args)
    dispatch: Dict[str, Callable[[argparse.Namespace], Dict[str, object]]] = {
        "init-run": lambda value: init_run(
            value.generated_at, Path(value.outcomes), Path(value.output)
        ),
        "capture-boundaries": _capture_boundaries,
        "audit-history": _audit_history,
        "ingest-human-gate": _ingest_human_gate,
        "ingest-history-correction": _ingest_history_correction,
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
