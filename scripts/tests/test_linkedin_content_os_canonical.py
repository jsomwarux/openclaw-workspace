import hashlib
import multiprocessing
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from scripts.linkedin_content_os.canonical import (
    append_jsonl_exact_prefix,
    canonical_bytes,
    read_jsonl,
    sha256_hex,
    write_json_atomic,
)


def _append_in_child(path_text: str, event: str, result_queue: object) -> None:
    try:
        append_jsonl_exact_prefix(Path(path_text), {"event": event})
    except Exception as error:
        result_queue.put(("error", type(error).__name__))
    else:
        result_queue.put(("ok", event))


class CanonicalBytesTests(unittest.TestCase):
    def test_serializes_sorted_compact_utf8_json(self) -> None:
        value = {"z": [3, {"b": True, "a": "café"}], "a": "✓"}

        self.assertEqual(
            canonical_bytes(value),
            b'{"a":"\xe2\x9c\x93","z":[3,{"a":"caf\xc3\xa9","b":true}]}',
        )

    def test_hashes_exact_bytes_with_sha256(self) -> None:
        value = b'{"a":"\xe2\x9c\x93"}'

        self.assertEqual(sha256_hex(value), hashlib.sha256(value).hexdigest())


class ReadJsonlTests(unittest.TestCase):
    def test_reads_object_rows_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            path.write_bytes(b'{"first":1}\n{"second":2}\n')

            self.assertEqual(read_jsonl(path), [{"first": 1}, {"second": 2}])

    def test_refuses_blank_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            path.write_bytes(b'{"first":1}\n\n{"second":2}\n')

            with self.assertRaisesRegex(ValueError, "blank row 2"):
                read_jsonl(path)

    def test_refuses_corrupt_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            path.write_bytes(b'{"first":1}\nnot-json\n')

            with self.assertRaisesRegex(ValueError, "invalid JSON row 2"):
                read_jsonl(path)

    def test_refuses_non_standard_nan_constant(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            path.write_bytes(b'{"value":NaN}\n')

            with self.assertRaisesRegex(ValueError, "invalid JSON row 1"):
                read_jsonl(path)

    def test_refuses_non_object_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            path.write_bytes(b'{"first":1}\n[1,2]\n')

            with self.assertRaisesRegex(ValueError, "non-object row 2"):
                read_jsonl(path)

    def test_refuses_duplicate_keys_in_top_level_object(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            path.write_bytes(b'{"event":"first","event":"second"}\n')

            with self.assertRaisesRegex(ValueError, "duplicate JSON key 'event'"):
                read_jsonl(path)

    def test_refuses_duplicate_keys_in_nested_object(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            path.write_bytes(b'{"outer":{"id":1,"id":2}}\n')

            with self.assertRaisesRegex(ValueError, "duplicate JSON key 'id'"):
                read_jsonl(path)


class AtomicJsonWriteTests(unittest.TestCase):
    def test_replaces_whole_file_with_exact_canonical_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_bytes(b"old-state")

            write_json_atomic(path, {"z": 2, "a": "✓"})

            self.assertEqual(path.read_bytes(), b'{"a":"\xe2\x9c\x93","z":2}')
            self.assertEqual(list(path.parent.iterdir()), [path])

    def test_replace_failure_preserves_original_and_removes_temp_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            original = b"old-state"
            path.write_bytes(original)

            with mock.patch(
                "scripts.linkedin_content_os.canonical.os.replace",
                side_effect=OSError("replace failed"),
            ):
                with self.assertRaisesRegex(OSError, "replace failed"):
                    write_json_atomic(path, {"new": True})

            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(list(path.parent.iterdir()), [path])


class ExactPrefixAppendTests(unittest.TestCase):
    def test_append_preserves_prior_bytes_as_exact_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            original = b'{"event":"first"}'
            path.write_bytes(original)

            append_jsonl_exact_prefix(path, {"z": 2, "a": "✓"})

            after = path.read_bytes()
            self.assertTrue(after.startswith(original))
            self.assertEqual(
                after,
                original + b'\n{"a":"\xe2\x9c\x93","z":2}\n',
            )
            self.assertEqual(
                read_jsonl(path),
                [{"event": "first"}, {"a": "✓", "z": 2}],
            )

    def test_prefix_verification_failure_restores_original_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            original = b'{"event":"first"}\n'
            path.write_bytes(original)

            real_read_bytes = Path.read_bytes
            reads = iter([original, b"corrupted-after-append"])

            def controlled_read_bytes(candidate: Path) -> bytes:
                if candidate == path:
                    return next(reads)
                return real_read_bytes(candidate)

            with mock.patch.object(Path, "read_bytes", controlled_read_bytes):
                with self.assertRaisesRegex(RuntimeError, "exact prefix"):
                    append_jsonl_exact_prefix(path, {"event": "second"})

            with path.open("rb") as handle:
                self.assertEqual(handle.read(), original)

    def test_concurrent_writers_serialize_read_append_and_verify(self) -> None:
        context = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_bytes(b'{"event":"original"}\n')
            initial_read_barrier = context.Barrier(2)
            verification_read_barrier = context.Barrier(2)
            result_queue = context.Queue()
            real_read_bytes = Path.read_bytes
            read_count = [0]

            def coordinated_read_bytes(candidate: Path) -> bytes:
                if candidate == path:
                    read_count[0] += 1
                    barrier = (
                        initial_read_barrier
                        if read_count[0] == 1
                        else verification_read_barrier
                    )
                    try:
                        barrier.wait(timeout=0.5)
                    except threading.BrokenBarrierError:
                        pass
                return real_read_bytes(candidate)

            processes = [
                context.Process(
                    target=_append_in_child,
                    args=(str(path), event, result_queue),
                )
                for event in ("first", "second")
            ]
            with mock.patch.object(Path, "read_bytes", coordinated_read_bytes):
                for process in processes:
                    process.start()
                for process in processes:
                    process.join(timeout=5)

            for process in processes:
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=1)
                self.assertEqual(process.exitcode, 0)

            results = [result_queue.get(timeout=1) for _ in processes]
            self.assertEqual(sorted(results), [("ok", "first"), ("ok", "second")])
            self.assertEqual(
                {row["event"] for row in read_jsonl(path)},
                {"original", "first", "second"},
            )

    def test_absent_file_is_restored_to_absence_after_verification_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"

            with mock.patch.object(Path, "read_bytes", return_value=b"corrupted"):
                with self.assertRaisesRegex(RuntimeError, "exact prefix"):
                    append_jsonl_exact_prefix(path, {"event": "first"})

            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
