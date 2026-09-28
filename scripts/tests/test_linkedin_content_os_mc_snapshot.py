import json
import socket
import subprocess
import unittest
import urllib.request
from datetime import datetime, timedelta, timezone
from unittest import mock

from scripts.linkedin_content_os.canonical import sha256_hex
from scripts.linkedin_content_os.mc_snapshot import (
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
    "consumerNow": "2099-09-28T13:00:00+00:00",
}


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


def _raw(*tasks: dict[str, object]) -> bytes:
    return json.dumps({"tasks": list(tasks)}, separators=(",", ":")).encode("utf-8")


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

    def test_validates_minimal_hash_bound_wrapper_without_task_bodies(self) -> None:
        raw = _raw(_task("task-1"), {"_id": "legacy-1", "title": "legacy"})

        snapshot = validate_snapshot(raw, RUN_CONTEXT)

        self.assertEqual(snapshot["schemaVersion"], "linkedin-mc-snapshot.v1")
        self.assertEqual(snapshot["runId"], RUN_CONTEXT["runId"])
        self.assertEqual(snapshot["capturedAt"], GENERATED_AT)
        self.assertEqual(snapshot["validUntil"], "2099-09-28T14:00:00+00:00")
        self.assertEqual(snapshot["sourceUrl"], SOURCE_URL)
        self.assertEqual(snapshot["rawSha256"], sha256_hex(raw))
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
            "consumerNow": "2099-09-28T13:00:00Z",
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
            [packet["taskId"] for packet in approved_linkedin_packets(snapshot)],
            ["valid"],
        )
        self.assertEqual(snapshot["linkedinLanePacketCount"], 1)

    def test_preserves_nonterminal_and_governed_completed_projections_only(self) -> None:
        outcome = {
            "system": "linkedin-content-os",
            "id": "publication_acknowledged:content-002",
        }
        tasks = (
            _task("open"),
            _task("published", status="done", contentId="content-002", outcomeRef=outcome),
            _task(
                "wrong-outcome",
                status="done",
                outcomeRef={"system": "linkedin-content-os", "id": "other:content-003"},
            ),
            _task("no-outcome", status="done"),
            _task("archived", status="archived", closureReason={"kind": "no-action"}),
        )

        snapshot = validate_snapshot(_raw(*tasks), RUN_CONTEXT)
        projected = approved_linkedin_packets(snapshot)

        self.assertEqual([item["taskId"] for item in projected], ["open", "published"])
        self.assertEqual(projected[0]["projectionType"], "publication_acknowledgment")
        self.assertEqual(projected[1]["projectionType"], "metrics_followup")
        self.assertEqual(projected[1]["closureType"], "completed")
        self.assertEqual(projected[1]["closureOutcomePointer"], outcome)

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
            approved_linkedin_packets(snapshot)

        snapshot = validate_snapshot(_raw(_task("valid")), RUN_CONTEXT)
        packet = dict(snapshot["packets"][0])
        packet["description"] = "must not survive"
        snapshot["packets"] = [packet]
        with self.assertRaisesRegex(ValueError, "canonical fields"):
            approved_linkedin_packets(snapshot)

    def test_fails_closed_on_run_context_mismatch_or_staleness(self) -> None:
        raw = _raw(_task("valid"))
        invalid_contexts = (
            {**RUN_CONTEXT, "runId": "wrong"},
            {**RUN_CONTEXT, "generatedAt": "2099-09-28T12:00:00"},
            {**RUN_CONTEXT, "consumerNow": "2099-09-28T14:00:00.000001+00:00"},
        )
        for context in invalid_contexts:
            with self.subTest(context=context), self.assertRaises(ValueError):
                validate_snapshot(raw, context)

        snapshot = validate_snapshot(raw, RUN_CONTEXT)
        mutated = dict(snapshot)
        mutated["runId"] = "wrong"
        with self.assertRaisesRegex(ValueError, "runId"):
            approved_linkedin_packets(mutated)
        mutated = dict(snapshot)
        mutated["validUntil"] = (
            datetime.fromisoformat(GENERATED_AT) + timedelta(hours=3)
        ).isoformat()
        with self.assertRaisesRegex(ValueError, "validUntil"):
            approved_linkedin_packets(mutated)


if __name__ == "__main__":
    unittest.main()
