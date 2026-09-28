from __future__ import annotations

import copy
import unittest
from datetime import datetime, timedelta, timezone

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.checkin import project_checkin


NOW = datetime(2026, 9, 28, 16, 0, tzinfo=timezone.utc)
PAYLOAD_HASH = "a" * 64
PACKET_HASH = "b" * 64
RUN_ID = "sha256:" + "c" * 64
PUBLICATION_URL = "https://www.linkedin.com/posts/jt_content-001"


def _packet(
    task_id: str = "task-001",
    content_id: str = "content-001",
    **overrides: object,
) -> dict[str, object]:
    packet: dict[str, object] = {
        "taskId": task_id,
        "status": "todo",
        "approvalState": "approved",
        "packetHash": PACKET_HASH,
        "payloadHash": PAYLOAD_HASH,
        "approvedPayloadHash": PAYLOAD_HASH,
        "contentId": content_id,
        "projectionType": "publication_acknowledgment",
    }
    packet.update(overrides)
    return packet


def _snapshot(
    *packets: dict[str, object],
    captured_at: datetime = datetime(2026, 9, 28, 15, 30, tzinfo=timezone.utc),
) -> dict[str, object]:
    snapshot: dict[str, object] = {
        "schemaVersion": "linkedin-mc-snapshot.v1",
        "runId": RUN_ID,
        "capturedAt": captured_at.isoformat(),
        "validUntil": (captured_at + timedelta(hours=2)).isoformat(),
        "sourceUrl": "http://127.0.0.1:3000/api/tasks",
        "rawSha256": "d" * 64,
        "totalTaskCount": len(packets),
        "linkedinLanePacketCount": len(packets),
        "packets": list(packets),
    }
    snapshot["projectionSha256"] = sha256_hex(canonical_bytes(snapshot))
    return snapshot


def _event(
    event_id: str,
    event_type: str,
    payload: dict[str, object],
    *,
    packet: dict[str, object] | None = None,
    recorded_at: str = "2026-09-28T15:00:00+00:00",
) -> dict[str, object]:
    packet = packet or _packet()
    event: dict[str, object] = {
        "schemaVersion": "linkedin-content-outcome.v1",
        "outcomeEventId": event_id,
        "packetId": packet["contentId"],
        "eventType": event_type,
        "recordedAt": recorded_at,
        "sourcePointer": {
            "sourceType": "mission_control_packet",
            "sourceId": packet["taskId"],
            "sourceSha256": packet["payloadHash"],
        },
        "payload": payload,
    }
    event["eventSha256"] = sha256_hex(canonical_bytes(event))
    return event


def _published(
    packet: dict[str, object] | None = None,
    *,
    event_id: str = "published-001",
    recorded_at: str = "2026-09-20T16:00:00+00:00",
    url: str = PUBLICATION_URL,
) -> dict[str, object]:
    return _event(
        event_id,
        "publication_acknowledged",
        {"publicationUrl": url, "publishedAt": recorded_at},
        packet=packet,
        recorded_at=recorded_at,
    )


def _completed_packet(publication: dict[str, object]) -> dict[str, object]:
    payload = publication["payload"]
    assert isinstance(payload, dict)
    return _packet(
        status="done",
        projectionType="metrics_followup",
        closureType="completed",
        doneEvidenceType="post-url",
        doneEvidence={
            "type": "post-url",
            "ref": payload["publicationUrl"],
            "recordedAt": 1_790_000_000_000,
            "recordedBy": "jt",
        },
        closureOutcomePointer={
            "system": "linkedin-content-os",
            "id": publication["outcomeEventId"],
            "recordedAt": 1_790_000_000_000,
            "url": payload["publicationUrl"],
        },
    )


class LinkedInCheckinProjectionTests(unittest.TestCase):
    def test_no_unresolved_items_returns_no_task(self) -> None:
        self.assertIsNone(project_checkin(_snapshot(), [], NOW))

    def test_outcome_event_cannot_invent_an_approved_packet(self) -> None:
        self.assertIsNone(project_checkin(_snapshot(), [_published()], NOW))

    def test_aggregates_one_or_many_publication_acknowledgments(self) -> None:
        first = _packet()
        second = _packet("task-002", "content-002")

        preview = project_checkin(_snapshot(first, second), [], NOW)

        assert preview is not None
        self.assertEqual(preview["schemaVersion"], "linkedin-checkin-preview.v1")
        self.assertFalse(preview["liveWriteAuthorized"])
        self.assertEqual(preview["sourceSnapshotSha256"], _snapshot(first, second)["projectionSha256"])
        task = preview["task"]
        assert isinstance(task, dict)
        self.assertEqual(task["dedupeKey"], "linkedin-checkin:v1")
        self.assertEqual(task["project"], "LinkedIn Content OS")
        self.assertEqual(task["assignee"], "jt")
        self.assertEqual(task["dueDateSource"], "self")
        self.assertEqual(task["dueDate"], int(NOW.timestamp() * 1000))
        self.assertEqual(len(task["exactSteps"]), 2)
        self.assertIn("task-001", task["exactSteps"][0])
        self.assertIn("task-002", task["exactSteps"][1])
        self.assertIn("posted / not yet / won't post", task["exactSteps"][0])
        self.assertIn("no-action", task["exactSteps"][0])
        self.assertNotIn("feedback", task)

    def test_not_yet_preserves_identity_and_uses_next_eligible_date(self) -> None:
        packet = _packet()
        deferred = _event(
            "deferred-001",
            "publication_deferred",
            {"nextCheckAt": "2026-09-30T14:00:00+00:00"},
            packet=packet,
        )

        self.assertIsNone(project_checkin(_snapshot(packet), [deferred], NOW))
        due = datetime(2026, 9, 30, 14, 0, tzinfo=timezone.utc)
        preview = project_checkin(
            _snapshot(packet, captured_at=due - timedelta(minutes=30)),
            [deferred],
            due,
        )

        assert preview is not None
        task = preview["task"]
        assert isinstance(task, dict)
        self.assertEqual(task["dedupeKey"], "linkedin-checkin:v1")
        self.assertEqual(task["dueDate"], int(due.timestamp() * 1000))
        self.assertEqual(len(task["exactSteps"]), 1)

    def test_posted_requires_linkedin_url_and_packet_byte_binding(self) -> None:
        packet = _packet()
        invalid_url = _published(packet, url="https://example.com/posts/not-linkedin")
        wrong_binding = _published(packet, event_id="wrong-binding")
        source = dict(wrong_binding["sourcePointer"])
        source["sourceSha256"] = "e" * 64
        wrong_binding["sourcePointer"] = source
        wrong_binding["eventSha256"] = sha256_hex(
            canonical_bytes({key: value for key, value in wrong_binding.items() if key != "eventSha256"})
        )

        with self.assertRaisesRegex(ValueError, "LinkedIn"):
            project_checkin(_snapshot(packet), [invalid_url], NOW)
        with self.assertRaisesRegex(ValueError, "approved packet"):
            project_checkin(_snapshot(packet), [wrong_binding], NOW)

    def test_wont_post_is_a_closed_decline_and_resolves_publication_prompt(self) -> None:
        packet = _packet()
        declined = _event(
            "declined-001",
            "publication_declined",
            {"declineReason": "quality_fit"},
            packet=packet,
        )

        self.assertIsNone(project_checkin(_snapshot(packet), [declined], NOW))

        malformed = copy.deepcopy(declined)
        malformed["payload"] = {"declineReason": "maybe"}
        malformed["eventSha256"] = sha256_hex(
            canonical_bytes({key: value for key, value in malformed.items() if key != "eventSha256"})
        )
        with self.assertRaisesRegex(ValueError, "declineReason"):
            project_checkin(_snapshot(packet), [malformed], NOW)

    def test_seven_day_metrics_uses_same_task_and_never_prompts_at_24_hours(self) -> None:
        packet = _packet()
        published = _published(packet, recorded_at="2026-09-20T16:00:00+00:00")
        terminal = _completed_packet(published)

        day_one = datetime(2026, 9, 21, 16, 0, tzinfo=timezone.utc)
        self.assertIsNone(
            project_checkin(
                _snapshot(terminal, captured_at=day_one - timedelta(minutes=30)),
                [published],
                day_one,
            )
        )

        day_seven = datetime(2026, 9, 27, 16, 0, tzinfo=timezone.utc)
        preview = project_checkin(
            _snapshot(terminal, captured_at=day_seven - timedelta(minutes=30)),
            [published],
            day_seven,
        )

        assert preview is not None
        task = preview["task"]
        assert isinstance(task, dict)
        self.assertEqual(task["dedupeKey"], "linkedin-checkin:v1")
        self.assertEqual(task["dueDate"], int(day_seven.timestamp() * 1000))
        self.assertEqual(len(task["exactSteps"]), 1)
        self.assertIn("seven-day", task["exactSteps"][0])
        self.assertIn("metrics_unknown", task["exactSteps"][0])

    def test_metric_snapshot_resolves_followup_without_coercing_missing_values(self) -> None:
        packet = _packet()
        published = _published(packet)
        terminal = _completed_packet(published)
        metrics = _event(
            "metrics-001",
            "metric_snapshot",
            {
                "windowDays": 7,
                "metrics": {"impressions": 123},
                "collectionMethod": "jt_manual",
            },
            packet=packet,
            recorded_at="2026-09-28T15:00:00+00:00",
        )

        self.assertIsNone(project_checkin(_snapshot(terminal), [published, metrics], NOW))

    def test_early_metric_snapshot_cannot_suppress_the_full_day_seven_prompt(self) -> None:
        packet = _packet()
        published = _published(packet, recorded_at="2026-09-20T16:00:00+00:00")
        terminal = _completed_packet(published)
        early = _event(
            "metrics-early",
            "metric_snapshot",
            {
                "windowDays": 7,
                "metrics": {"impressions": 123},
                "collectionMethod": "jt_manual",
            },
            packet=packet,
            recorded_at="2026-09-26T16:00:00+00:00",
        )
        day_seven = datetime(2026, 9, 27, 16, 0, tzinfo=timezone.utc)

        preview = project_checkin(
            _snapshot(terminal, captured_at=day_seven - timedelta(minutes=30)),
            [published, early],
            day_seven,
        )

        assert preview is not None
        self.assertIn("seven-day", preview["task"]["exactSteps"][0])

    def test_future_publication_and_metric_events_fail_authoritative_clock(self) -> None:
        packet = _packet()
        future_publication = _published(
            packet, recorded_at="2026-09-28T16:00:00.000001+00:00"
        )
        with self.assertRaisesRegex(ValueError, "future"):
            project_checkin(_snapshot(packet), [future_publication], NOW)

        published = _published(packet, recorded_at="2026-09-20T16:00:00+00:00")
        terminal = _completed_packet(published)
        future_metric = _event(
            "metrics-future",
            "metric_snapshot",
            {
                "windowDays": 7,
                "metrics": {"impressions": 123},
                "collectionMethod": "jt_manual",
            },
            packet=packet,
            recorded_at="2026-09-28T16:00:00.000001+00:00",
        )
        with self.assertRaisesRegex(ValueError, "future"):
            project_checkin(_snapshot(terminal), [published, future_metric], NOW)

    def test_published_at_cannot_be_after_publication_recorded_at(self) -> None:
        packet = _packet()
        publication = _event(
            "published-future-published-at",
            "publication_acknowledged",
            {
                "publicationUrl": PUBLICATION_URL,
                "publishedAt": "2026-09-28T15:00:00.000001+00:00",
            },
            packet=packet,
            recorded_at="2026-09-28T15:00:00+00:00",
        )

        with self.assertRaisesRegex(ValueError, "publishedAt"):
            project_checkin(_snapshot(packet), [publication], NOW)

    def test_unknown_only_day_seven_snapshot_closes_without_fake_zero(self) -> None:
        packet = _packet()
        published = _published(packet, recorded_at="2026-09-20T16:00:00+00:00")
        terminal = _completed_packet(published)
        unknown = _event(
            "metrics-unknown",
            "metric_snapshot",
            {
                "windowDays": 7,
                "metricsUnknown": True,
                "collectionMethod": "jt_manual",
            },
            packet=packet,
            recorded_at="2026-09-27T16:00:00+00:00",
        )
        day_seven = datetime(2026, 9, 27, 16, 0, tzinfo=timezone.utc)

        self.assertIsNone(
            project_checkin(
                _snapshot(terminal, captured_at=day_seven - timedelta(minutes=30)),
                [published, unknown],
                day_seven,
            )
        )

    def test_mixed_gaps_emit_one_task_with_publication_steps_before_metrics(self) -> None:
        open_packet = _packet("task-001", "content-001")
        published = _published(
            _packet("task-002", "content-002"),
            event_id="published-002",
            recorded_at="2026-09-20T16:00:00+00:00",
            url="https://www.linkedin.com/posts/jt_content-002",
        )
        terminal = _completed_packet(published)
        terminal["taskId"] = "task-002"
        terminal["contentId"] = "content-002"

        preview = project_checkin(_snapshot(open_packet, terminal), [published], NOW)

        assert preview is not None
        task = preview["task"]
        assert isinstance(task, dict)
        self.assertEqual(task["dedupeKey"], "linkedin-checkin:v1")
        self.assertEqual(len(task["exactSteps"]), 2)
        self.assertIn("posted / not yet / won't post", task["exactSteps"][0])
        self.assertIn("seven-day", task["exactSteps"][1])

    def test_repeat_projection_is_byte_identical_and_has_no_reminder_rows(self) -> None:
        packet = _packet()
        snapshot = _snapshot(packet)
        snapshot_before = canonical_bytes(snapshot)
        events: list[dict[str, object]] = []
        events_before = canonical_bytes(events)

        first = project_checkin(snapshot, events, NOW)
        second = project_checkin(snapshot, events, NOW)

        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        self.assertEqual(canonical_bytes(snapshot), snapshot_before)
        self.assertEqual(canonical_bytes(events), events_before)
        self.assertNotIn(b"capability", canonical_bytes(first).lower())
        self.assertNotIn(b"credential", canonical_bytes(first).lower())
        self.assertNotIn(b"request command", canonical_bytes(first).lower())

    def test_snapshot_mismatch_changed_payload_and_staleness_fail_closed(self) -> None:
        packet = _packet()
        snapshot = _snapshot(packet)
        snapshot["rawSha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "projectionSha256"):
            project_checkin(snapshot, [], NOW)

        changed = _snapshot(_packet(approvedPayloadHash="e" * 64))
        with self.assertRaisesRegex(ValueError, "approved payload"):
            project_checkin(changed, [], NOW)

        with self.assertRaisesRegex(ValueError, "stale"):
            project_checkin(_snapshot(packet), [], NOW + timedelta(hours=2))

    def test_snapshot_status_content_identity_and_ttl_are_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "status"):
            project_checkin(_snapshot(_packet(status="unknown")), [], NOW)

        with self.assertRaisesRegex(ValueError, "contentId"):
            project_checkin(
                _snapshot(_packet("task-001"), _packet("task-002")), [], NOW
            )

        packet = _packet()
        boundary = datetime(2026, 9, 28, 17, 30, tzinfo=timezone.utc)
        self.assertIsNotNone(project_checkin(_snapshot(packet), [], boundary))
        with self.assertRaisesRegex(ValueError, "stale"):
            project_checkin(
                _snapshot(packet), [], boundary + timedelta(microseconds=1)
            )

    def test_deferral_cannot_outlive_packet_expiry(self) -> None:
        expiry = datetime(2026, 9, 29, 0, 0, tzinfo=timezone.utc)
        packet = _packet(expiresAt=int(expiry.timestamp() * 1000))
        deferred = _event(
            "deferred-after-expiry",
            "publication_deferred",
            {"nextCheckAt": "2026-09-29T01:00:00+00:00"},
            packet=packet,
        )

        with self.assertRaisesRegex(ValueError, "expiry"):
            project_checkin(_snapshot(packet), [deferred], NOW)

    def test_terminal_packet_requires_matching_hash_bound_publication_closure(self) -> None:
        publication = _published()
        terminal = _completed_packet(publication)

        with self.assertRaisesRegex(ValueError, "publication closure"):
            project_checkin(_snapshot(terminal), [], NOW)

        wrong_event = _published(event_id="different-publication")
        with self.assertRaisesRegex(ValueError, "publication closure"):
            project_checkin(_snapshot(terminal), [wrong_event], NOW)

    def test_terminal_closure_timestamps_cannot_predate_publication(self) -> None:
        publication = _published(recorded_at="2026-09-20T16:00:00+00:00")
        terminal = _completed_packet(publication)
        terminal["doneEvidence"] = {
            **terminal["doneEvidence"],
            "recordedAt": 1,
        }
        terminal["closureOutcomePointer"] = {
            **terminal["closureOutcomePointer"],
            "recordedAt": 1,
        }

        with self.assertRaisesRegex(ValueError, "predates publication"):
            project_checkin(_snapshot(terminal), [publication], NOW)

    def test_terminal_closure_timestamps_cannot_exceed_authoritative_now(self) -> None:
        publication = _published(recorded_at="2026-09-20T16:00:00+00:00")
        future_millis = int((NOW + timedelta(microseconds=1)).timestamp() * 1000) + 1
        for field in ("doneEvidence", "closureOutcomePointer"):
            with self.subTest(field=field):
                terminal = _completed_packet(publication)
                terminal[field] = {
                    **terminal[field],
                    "recordedAt": future_millis,
                }
                with self.assertRaisesRegex(ValueError, "authoritative now"):
                    project_checkin(_snapshot(terminal), [publication], NOW)

    def test_day_seven_boundary_uses_absolute_time_across_offsets(self) -> None:
        packet = _packet()
        published = _published(packet, recorded_at="2026-09-20T12:00:00-04:00")
        terminal = _completed_packet(published)
        epsilon_before = datetime(2026, 9, 27, 15, 59, 59, 999999, tzinfo=timezone.utc)
        boundary = datetime(2026, 9, 27, 16, 0, tzinfo=timezone.utc)

        self.assertIsNone(
            project_checkin(
                _snapshot(terminal, captured_at=epsilon_before - timedelta(minutes=30)),
                [published],
                epsilon_before,
            )
        )
        self.assertIsNotNone(
            project_checkin(
                _snapshot(terminal, captured_at=boundary - timedelta(minutes=30)),
                [published],
                boundary,
            )
        )

    def test_resigned_terminal_projection_cannot_smuggle_a_non_linkedin_url(self) -> None:
        publication = _published()
        terminal = _completed_packet(publication)
        evidence = dict(terminal["doneEvidence"])
        evidence["ref"] = "https://example.com/posts/not-linkedin"
        terminal["doneEvidence"] = evidence

        with self.assertRaisesRegex(ValueError, "LinkedIn"):
            project_checkin(_snapshot(terminal), [publication], NOW)

    def test_duplicate_event_identity_fails_closed(self) -> None:
        packet = _packet()
        deferred = _event(
            "deferred-001",
            "publication_deferred",
            {"nextCheckAt": "2026-09-29T16:00:00+00:00"},
            packet=packet,
        )

        with self.assertRaisesRegex(ValueError, "duplicate outcomeEventId"):
            project_checkin(_snapshot(packet), [deferred, copy.deepcopy(deferred)], NOW)

    def test_terminal_published_packet_is_metrics_only_and_never_reenters_publication(self) -> None:
        published = _published(recorded_at="2026-09-20T16:00:00+00:00")
        terminal = _completed_packet(published)

        preview = project_checkin(_snapshot(terminal), [published], NOW)

        assert preview is not None
        task = preview["task"]
        assert isinstance(task, dict)
        self.assertEqual(len(task["exactSteps"]), 1)
        self.assertIn("seven-day", task["exactSteps"][0])
        self.assertNotIn("posted / not yet / won't post", task["exactSteps"][0])
        self.assertNotIn("approvalState", canonical_bytes(preview).decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
