"""Canonical JSON and exact-prefix JSONL file operations."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, List, Tuple


def canonical_bytes(value: object) -> bytes:
    """Return deterministic compact JSON encoded as UTF-8."""

    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    """Return the lowercase SHA-256 digest for exact bytes."""

    return hashlib.sha256(value).hexdigest()


def _strict_object(pairs: List[Tuple[str, Any]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key {!r}".format(key))
        value[key] = item
    return value


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read strict JSONL containing one JSON object per non-blank row."""

    rows: list[dict[str, object]] = []
    text = path.read_text(encoding="utf-8")

    def reject_non_standard_constant(constant: str) -> None:
        raise ValueError("non-standard JSON constant {}".format(constant))

    for row_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            raise ValueError("blank row {} in {}".format(row_number, path))
        try:
            value: Any = json.loads(
                line,
                object_pairs_hook=_strict_object,
                parse_constant=reject_non_standard_constant,
            )
        except (json.JSONDecodeError, ValueError) as error:
            raise ValueError(
                "invalid JSON row {} in {}: {}".format(row_number, path, error)
            ) from error
        if not isinstance(value, dict):
            raise ValueError("non-object row {} in {}".format(row_number, path))
        rows.append(value)
    return rows


def _write_bytes_atomic(path: Path, payload: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=".{}.".format(path.name), suffix=".tmp"
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temporary_path), str(path))
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def write_json_atomic(path: Path, value: object) -> None:
    """Atomically replace a file with exact canonical JSON bytes."""

    _write_bytes_atomic(path, canonical_bytes(value))


@contextmanager
def _exclusive_path_lock(path: Path) -> Iterator[None]:
    lock_path = path.with_name(".{}.lock".format(path.name))
    descriptor = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o600)
    with os.fdopen(descriptor, "a+b") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def append_jsonl_exact_prefix(path: Path, row: dict[str, object]) -> None:
    """Append one canonical row and prove all prior bytes remain unchanged."""

    row_bytes = canonical_bytes(row)
    with _exclusive_path_lock(path):
        existed = path.exists()
        original = path.read_bytes() if existed else b""
        separator = b"\n" if original and not original.endswith(b"\n") else b""
        appended = separator + row_bytes + b"\n"

        try:
            with path.open("ab") as handle:
                handle.write(appended)
                handle.flush()
                os.fsync(handle.fileno())
            after = path.read_bytes()
            expected = original + appended
            if not after.startswith(original) or after != expected:
                raise RuntimeError(
                    "append did not preserve the prior bytes as an exact prefix"
                )
        except Exception:
            if existed:
                _write_bytes_atomic(path, original)
            else:
                path.unlink(missing_ok=True)
            raise
