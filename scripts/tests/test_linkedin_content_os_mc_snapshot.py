import json
import socket
import subprocess
import unittest
import urllib.request
from datetime import datetime, timedelta, timezone
from unittest import mock

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.mc_snapshot import (
    MAX_RESPONSE_BYTES,
    approved_linkedin_packets,
    capture_tasks,
    validate_snapshot,
)


SOURCE_URL = "http://127.0.0.1:3000/api/tasks"
PAYLOAD_HASH = "a" * 64
PACKET_HASH = "b" * 64
GENERATED_AT = "2099-09-28T12:00:00+00:00"
RUN_CONTEXT = {
    "runId": "sha256:" + "c" * 64,
    "generatedAt": GENERATED_AT,
}
NOW = datetime(2099, 9, 28, 13, 0, tzinfo=timezone.utc)


def _task(task_id: str, **overrides: object) -> dict[str, object]:
    task: dict[str, object] = {
        "_id": task_id,
        "title": "must not leak",
        "description": "must not leak",
        "packetSchema": "lane-packet-v1",
        "growthLane": "linkedin",
        "status": "todo",
        "approvalState": "approved",
        "packetHash": PACKET_HASH,
        "payloadHash": PAYLOAD_HASH,
        "approvedPayloadHash": PAYLOAD_HASH,
        "contentId": "content-001",
        "expiresAt": 4_095_244_800_000,
    }
    task.update(overrides)
    return task


def _completed_task(task_id: str, **overrides: object) -> dict[str, object]:
    content_id = overrides.pop("contentId", "content-001")
    task = _task(
        task_id,
        status="done",
        artifactRef={
            "system": "linkedin-content-os",
            "id": content_id,
            "sha256": PACKET_HASH,
        },
        doneEvidenceType="post-url",
        doneEvidence={
            "type": "post-url",
            "ref": "https://www.linkedin.com/posts/jt_{}".format(task_id),
            "recordedAt": 4_095_237_600_000,
            "recordedBy": "jt",
        },
        outcomeRef={
            "system": "linkedin-content-os",
            "id": "fixture-outcome-{}".format(task_id),
            "recordedAt": 4_095_237_600_000,
        },
    )
    task.pop("packetHash")
    task.pop("contentId")
    task.update(overrides)
    return task


def _raw(*tasks: dict[str, object]) -> bytes:
    return json.dumps({"tasks": list(tasks)}, separators=(",", ":")).encode("utf-8")


def _resign(snapshot: dict[str, object]) -> dict[str, object]:
    resigned = dict(snapshot)
    resigned.pop("projectionSha256", None)
    resigned["projectionSha256"] = sha256_hex(canonical_bytes(resigned))
    return resigned


class _Headers:
    def __init__(self, content_type: str = "application/json; charset=utf-8") -> None:
        self.content_type = content_type

    def get_content_type(self) -> str:
        return self.content_type.split(";", 1)[0]


class _Response:
    def __init__(
        self,
        body: bytes,
        *,
        url: str = SOURCE_URL,
        status: int = 200,
        content_type: str = "application/json; charset=utf-8",
    ) -> None:
        self.body = body
        self.url = url
        self.status = status
        self.headers = _Headers(content_type)

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, amount: int = -1) -> bytes:
        return self.body if amount < 0 else self.body[:amount]

    def geturl(self) -> str:
        return self.url


class _Opener:
    def __init__(self, response: _Response) -> None:
        self.response = response
        self.requests: list[tuple[urllib.request.Request, float]] = []

    def open(self, request: urllib.request.Request, timeout: float) -> _Response:
        self.requests.append((request, timeout))
        return self.response


class MissionControlSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        clock = mock.patch(
            "scripts.linkedin_content_os.mc_snapshot._utc_now",
            return_value=NOW,
        )
        clock.start()
        self.addCleanup(clock.stop)
        self.process_patches = [
            mock.patch.object(subprocess, name, side_effect=AssertionError("process denied"))
            for name in ("Popen", "run", "call", "check_call", "check_output")
        ]
        for patcher in self.process_patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.network_patches = [
            mock.patch.object(
                socket.socket,
                "connect",
                side_effect=AssertionError("socket connect denied"),
            ),
            mock.patch.object(
                socket,
                "create_connection",
                side_effect=AssertionError("socket connection denied"),
            ),
            mock.patch.object(
                urllib.request,
                "urlopen",
                side_effect=AssertionError("urlopen denied"),
            ),
        ]
        for patcher in self.network_patches:
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_capture_uses_one_exact_read_only_loopback_request(self) -> None:
        body = _raw(_task("task-1"))
        opener = _Opener(_Response(body))

        with mock.patch(
            "scripts.linkedin_content_os.mc_snapshot.urllib.request.build_opener",
            return_value=opener,
        ) as build_opener:
            captured = capture_tasks()

        self.assertEqual(captured, body)
        build_opener.assert_called_once()
        handlers = build_opener.call_args.args
        self.assertEqual(len(handlers), 2)
        self.assertIsInstance(handlers[0], urllib.request.ProxyHandler)
        self.assertEqual(handlers[0].proxies, {})
        self.assertEqual(type(handlers[1]).__name__, "_NoRedirectHandler")
        self.assertEqual(len(opener.requests), 1)
        request, timeout = opener.requests[0]
        self.assertEqual(request.full_url, SOURCE_URL)
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(timeout, 5.0)
        headers = {key.lower(): value for key, value in request.header_items()}
        self.assertEqual(headers, {"accept": "application/json"})
        self.assertNotIn("authorization", headers)
        self.assertFalse(any("capability" in key for key in headers))

    def test_capture_rejects_nonexact_urls_redirects_and_non_json(self) -> None:
        invalid_urls = (
            "http://localhost:3000/api/tasks",
            "https://127.0.0.1:3000/api/tasks",
            "http://127.0.0.1:3000/api/tasks?include=archived",
            "http://127.0.0.1:3000/api/tasks/",
            "http://user@127.0.0.1:3000/api/tasks",
        )
        with mock.patch(
            "scripts.linkedin_content_os.mc_snapshot.urllib.request.build_opener"
        ) as build_opener:
            for url in invalid_urls:
                with self.subTest(url=url), self.assertRaises(ValueError):
                    capture_tasks(url)
            build_opener.assert_not_called()

        cases = (
            _Response(b'{}', url="http://127.0.0.1:3000/login"),
            _Response(b'{}', content_type="text/html"),
            _Response(b'{}', status=204),
        )
        for response in cases:
            opener = _Opener(response)
            with self.subTest(response=response), mock.patch(
                "scripts.linkedin_content_os.mc_snapshot.urllib.request.build_opener",
                return_value=opener,
            ), self.assertRaises(ValueError):
                capture_tasks()
            self.assertEqual(len(opener.requests), 1)

    def test_capture_accepts_exactly_8_mib_and_rejects_one_byte_more(self) -> None:
        exact = b"x" * MAX_RESPONSE_BYTES
        overflow = exact + b"x"
        for body, accepted in ((exact, True), (overflow, False)):
            opener = _Opener(_Response(body))
            context = (
                self.subTest(size=len(body)),
                mock.patch(
                    "scripts.linkedin_content_os.mc_snapshot.urllib.request.build_opener",
                    return_value=opener,
                ),
            )
            with context[0], context[1]:
                if accepted:
                    self.assertEqual(capture_tasks(), body)
                else:
                    with self.assertRaisesRegex(ValueError, "size limit"):
                        capture_tasks()
            self.assertEqual(len(opener.requests), 1)

    def test_validates_minimal_hash_bound_wrapper_without_task_bodies(self) -> None:
        raw = _raw(_task("task-1"), {"_id": "legacy-1", "title": "legacy"})

        snapshot = validate_snapshot(raw, RUN_CONTEXT)

        self.assertEqual(snapshot["schemaVersion"], "linkedin-mc-snapshot.v1")
        self.assertEqual(snapshot["runId"], RUN_CONTEXT["runId"])
        self.assertEqual(snapshot["capturedAt"], GENERATED_AT)
        self.assertEqual(snapshot["validUntil"], "2099-09-28T14:00:00+00:00")
        self.assertEqual(snapshot["sourceUrl"], SOURCE_URL)
        self.assertEqual(snapshot["rawSha256"], sha256_hex(raw))
        self.assertEqual(
            snapshot["projectionSha256"],
            sha256_hex(
                canonical_bytes(
                    {key: value for key, value in snapshot.items() if key != "projectionSha256"}
                )
            ),
        )
        self.assertEqual(snapshot["totalTaskCount"], 2)
        self.assertEqual(snapshot["linkedinLanePacketCount"], 1)
        self.assertEqual(len(snapshot["packets"]), 1)
        packet = snapshot["packets"][0]
        self.assertEqual(
            set(packet),
            {
                "taskId",
                "status",
                "approvalState",
                "packetHash",
                "payloadHash",
                "approvedPayloadHash",
                "contentId",
                "expiresAt",
                "projectionType",
            },
        )
        self.assertNotIn("title", json.dumps(snapshot))
        self.assertNotIn("description", json.dumps(snapshot))

    def test_preserves_the_run_context_generated_at_as_captured_at(self) -> None:
        context = {
            **RUN_CONTEXT,
            "generatedAt": "2099-09-28T12:00:00Z",
        }

        snapshot = validate_snapshot(_raw(_task("task-1")), context)

        self.assertEqual(snapshot["capturedAt"], context["generatedAt"])
        self.assertEqual(snapshot["validUntil"], "2099-09-28T14:00:00+00:00")

    def test_filters_on_exact_lane_packet_approval_contract(self) -> None:
        candidates = [
            _task("valid"),
            _task("wrong-schema", packetSchema="other"),
            _task("wrong-lane", growthLane="jobs"),
            _task("pending", approvalState="pending"),
            _task("changed", approvedPayloadHash="d" * 64),
        ]

        snapshot = validate_snapshot(_raw(*candidates), RUN_CONTEXT)

        self.assertEqual(
            [packet["taskId"] for packet in approved_linkedin_packets(snapshot, RUN_CONTEXT)],
            ["valid"],
        )
        self.assertEqual(snapshot["linkedinLanePacketCount"], 1)

    def test_preserves_nonterminal_and_governed_completed_projections_only(self) -> None:
        outcome = {
            "system": "linkedin-content-os",
            "id": "fixture-outcome-002",
            "recordedAt": 4_095_237_600_000,
            "url": "https://www.linkedin.com/posts/jt_content-002",
        }
        tasks = (
            _task("open"),
            _completed_task(
                "published",
                contentId="content-002",
                outcomeRef=outcome,
            ),
            _completed_task(
                "missing-closure",
                contentId="content-004",
                doneEvidence=None,
            ),
            _completed_task(
                "malformed-pointer",
                contentId="content-005",
                outcomeRef={
                    "system": "linkedin-content-os",
                    "id": "contains spaces",
                    "recordedAt": 4_095_237_600_000,
                },
            ),
            _completed_task(
                "overlong-pointer",
                contentId="content-007",
                outcomeRef={
                    "system": "linkedin-content-os",
                    "id": "x" * 129,
                    "recordedAt": 4_095_237_600_000,
                },
            ),
            _completed_task(
                "wrong-system",
                contentId="content-008",
                outcomeRef={
                    "system": "other-system",
                    "id": "fixture-outcome-008",
                    "recordedAt": 4_095_237_600_000,
                },
            ),
            _completed_task(
                "malformed-evidence",
                contentId="content-009",
                doneEvidence={
                    "type": "post-url",
                    "ref": "not-a-url",
                    "recordedAt": 4_095_237_600_000,
                    "recordedBy": "jt",
                },
            ),
            _task(
                "wrong-outcome",
                status="done",
                outcomeRef={"system": "linkedin-content-os", "id": "other:content-003"},
            ),
            _task("no-outcome", status="done"),
            _task("archived", status="archived", closureReason={"kind": "no-action"}),
        )

        self.assertNotIn("closureType", tasks[1])
        self.assertNotIn("packetHash", tasks[1])
        self.assertNotIn("contentId", tasks[1])

        snapshot = validate_snapshot(_raw(*tasks), RUN_CONTEXT)
        projected = approved_linkedin_packets(snapshot, RUN_CONTEXT)

        self.assertEqual([item["taskId"] for item in projected], ["open", "published"])
        self.assertEqual(projected[0]["projectionType"], "publication_acknowledgment")
        self.assertEqual(projected[1]["projectionType"], "metrics_followup")
        self.assertEqual(projected[1]["closureType"], "completed")
        self.assertEqual(projected[1]["closureOutcomePointer"], outcome)
        self.assertEqual(projected[1]["doneEvidenceType"], "post-url")
        self.assertEqual(projected[1]["doneEvidence"]["recordedBy"], "jt")
        self.assertEqual(projected[1]["contentId"], "content-002")
        self.assertEqual(projected[1]["closureOutcomePointer"]["id"], "fixture-outcome-002")

    def test_rejects_invalid_json_duplicates_task_ids_and_missing_source_hash(self) -> None:
        invalid_raw = (
            b"not-json",
            b'{"tasks":[],"tasks":[]}',
            b'{"tasks":"not-a-list"}',
            _raw(_task("duplicate"), _task("duplicate")),
        )
        for raw in invalid_raw:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validate_snapshot(raw, RUN_CONTEXT)

        snapshot = validate_snapshot(_raw(_task("valid")), RUN_CONTEXT)
        snapshot.pop("rawSha256")
        with self.assertRaisesRegex(ValueError, "rawSha256"):
            approved_linkedin_packets(snapshot, RUN_CONTEXT)

        snapshot = validate_snapshot(_raw(_task("valid")), RUN_CONTEXT)
        packet = dict(snapshot["packets"][0])
        packet["description"] = "must not survive"
        snapshot["packets"] = [packet]
        snapshot = _resign(snapshot)
        with self.assertRaisesRegex(ValueError, "canonical fields"):
            approved_linkedin_packets(snapshot, RUN_CONTEXT)

    def test_persisted_projection_digest_detects_unresigned_tampering(self) -> None:
        snapshot = validate_snapshot(_raw(_task("valid")), RUN_CONTEXT)
        packet = dict(snapshot["packets"][0])
        packet["contentId"] = "tampered"
        snapshot["packets"] = [packet]

        with self.assertRaisesRegex(ValueError, "projectionSha256"):
            approved_linkedin_packets(snapshot, RUN_CONTEXT)

    def test_run_context_is_immutable_and_unknown_fields_fail_closed(self) -> None:
        context = dict(RUN_CONTEXT)
        before = canonical_bytes(context)

        snapshot = validate_snapshot(_raw(_task("valid")), context)
        approved_linkedin_packets(snapshot, context)

        self.assertEqual(canonical_bytes(context), before)
        with self.assertRaisesRegex(ValueError, "fields are not canonical"):
            validate_snapshot(
                _raw(_task("valid")),
                {**RUN_CONTEXT, "consumerNow": "2099-09-28T13:00:00Z"},
            )

    def test_resigned_metrics_metadata_must_remain_well_formed(self) -> None:
        task = _completed_task(
            "published",
            contentId="content-002",
            outcomeRef={
                "system": "linkedin-content-os",
                "id": "fixture-outcome-002",
                "recordedAt": 4_095_237_600_000,
            },
        )
        snapshot = validate_snapshot(_raw(task), RUN_CONTEXT)
        packet = dict(snapshot["packets"][0])
        packet["closureOutcomePointer"] = {
            "system": "linkedin-content-os",
            "id": "contains spaces",
            "recordedAt": 4_095_237_600_000,
        }
        snapshot["packets"] = [packet]

        with self.assertRaisesRegex(ValueError, "governed publication outcome"):
            approved_linkedin_packets(_resign(snapshot), RUN_CONTEXT)

        snapshot = validate_snapshot(_raw(task), RUN_CONTEXT)
        packet = dict(snapshot["packets"][0])
        pointer = dict(packet["closureOutcomePointer"])
        pointer["recordedAt"] = True
        packet["closureOutcomePointer"] = pointer
        snapshot["packets"] = [packet]
        with self.assertRaisesRegex(ValueError, "governed publication outcome"):
            approved_linkedin_packets(_resign(snapshot), RUN_CONTEXT)

        snapshot = validate_snapshot(_raw(task), RUN_CONTEXT)
        packet = dict(snapshot["packets"][0])
        evidence = dict(packet["doneEvidence"])
        evidence["ref"] = "not-a-url"
        packet["doneEvidence"] = evidence
        snapshot["packets"] = [packet]
        with self.assertRaisesRegex(ValueError, "completion evidence"):
            approved_linkedin_packets(_resign(snapshot), RUN_CONTEXT)

        bad_url_task = _completed_task(
            "bad-url",
            contentId="content-006",
            outcomeRef={
                "system": "linkedin-content-os",
                "id": "fixture-outcome-006",
                "recordedAt": 4_095_237_600_000,
                "url": "https://example.com/not-linkedin",
            },
        )
        self.assertEqual(
            validate_snapshot(_raw(bad_url_task), RUN_CONTEXT)["packets"],
            [],
        )

    def test_rejects_resigned_type_value_count_and_order_tampering_as_value_error(self) -> None:
        base = validate_snapshot(_raw(_task("b"), _task("a", contentId="content-002")), RUN_CONTEXT)
        cases: list[dict[str, object]] = []

        for field, value in (
            ("taskId", 7),
            ("taskId", "contains spaces"),
            ("status", "invented"),
            ("approvalState", "pending"),
            ("packetHash", "bad"),
            ("payloadHash", False),
            ("approvedPayloadHash", 3),
            ("contentId", ""),
            ("contentId", "contains spaces"),
            ("expiresAt", True),
            ("projectionType", "other"),
        ):
            changed = dict(base)
            packet = dict(changed["packets"][0])
            packet[field] = value
            changed["packets"] = [packet, changed["packets"][1]]
            cases.append(_resign(changed))

        for field, value in (
            ("rawSha256", False),
            ("totalTaskCount", True),
            ("linkedinLanePacketCount", True),
            ("capturedAt", 7),
            ("validUntil", []),
            ("sourceUrl", "http://localhost:3000/api/tasks"),
        ):
            changed = dict(base)
            changed[field] = value
            cases.append(_resign(changed))

        reordered = dict(base)
        reordered["packets"] = list(reversed(base["packets"]))
        cases.append(_resign(reordered))

        for changed in cases:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                approved_linkedin_packets(changed, RUN_CONTEXT)

    def test_fails_closed_on_run_context_mismatch_or_staleness(self) -> None:
        raw = _raw(_task("valid"))
        invalid_contexts = (
            {**RUN_CONTEXT, "runId": "wrong"},
            {**RUN_CONTEXT, "generatedAt": "2099-09-28T12:00:00"},
            {**RUN_CONTEXT, "consumerNow": "2099-09-28T13:00:00+00:00"},
        )
        for context in invalid_contexts:
            with self.subTest(context=context), self.assertRaises(ValueError):
                validate_snapshot(raw, context)

        snapshot = validate_snapshot(raw, RUN_CONTEXT)
        valid_other_context = {
            **RUN_CONTEXT,
            "runId": "sha256:" + "d" * 64,
        }
        with self.assertRaisesRegex(ValueError, "current run context"):
            approved_linkedin_packets(snapshot, valid_other_context)

        later_run_context = {
            "runId": RUN_CONTEXT["runId"],
            "generatedAt": "2099-09-28T13:00:00+00:00",
        }
        with self.assertRaisesRegex(ValueError, "current run context"):
            approved_linkedin_packets(snapshot, later_run_context)

        with mock.patch(
            "scripts.linkedin_content_os.mc_snapshot._utc_now",
            return_value=datetime(2099, 9, 28, 14, 0, 0, 1, tzinfo=timezone.utc),
        ), self.assertRaisesRegex(ValueError, "stale"):
            approved_linkedin_packets(snapshot, RUN_CONTEXT)

        with mock.patch(
            "scripts.linkedin_content_os.mc_snapshot._utc_now",
            return_value=datetime(2099, 9, 28, 11, 59, 59, tzinfo=timezone.utc),
        ):
            with self.assertRaisesRegex(ValueError, "before capturedAt"):
                approved_linkedin_packets(snapshot, RUN_CONTEXT)
            with self.assertRaisesRegex(ValueError, "before capturedAt"):
                validate_snapshot(raw, RUN_CONTEXT)

        mutated = dict(snapshot)
        mutated["validUntil"] = (
            datetime.fromisoformat(GENERATED_AT) + timedelta(hours=3)
        ).isoformat()
        mutated = _resign(mutated)
        with self.assertRaisesRegex(ValueError, "validUntil"):
            approved_linkedin_packets(mutated, RUN_CONTEXT)


if __name__ == "__main__":
    unittest.main()
