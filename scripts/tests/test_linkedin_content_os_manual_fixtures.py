from __future__ import annotations

import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from PIL import Image

from scripts.linkedin_content_os.canonical import (
    _exclusive_path_lock,
    canonical_bytes,
    sha256_hex,
)
from scripts.linkedin_content_os import manual_fixtures
from scripts.linkedin_content_os.manual_fixtures import (
    _draft_binding,
    _payload_binding,
    build_manual_fixture,
    validate_manual_fixture,
)


NOW = datetime(2026, 9, 28, 20, 30, tzinfo=timezone.utc)
REPOSITORY = Path(__file__).resolve().parents[2]
ANGLE_PATH = "memory/drafts/linkedin-property-ops-source-to-decision-trail-2026-08-02.md"
ANGLE_EXCERPT = (
    "It proves what the workflow saw, what it was allowed to touch, what it held back, "
    "and where the decision landed."
)
NEVER_POSTED_PATH = "memory/drafts/linkedin-exception-control-plane-2026-06-14.md"
CANONICAL_LEDGER = "memory/content/linkedin-content-os/outcomes.v1.jsonl"
POSTED_LOG = "memory/content/posted-log.jsonl"
SYNTHETIC_URL = "https://www.linkedin.com/feed/update/urn:li:activity:7490053069380964353/"
TRACKED_NOW = datetime.fromisoformat("2026-09-30T12:00:00-04:00")
_ISOLATED_FILES = (
    "scripts/build_linkedin_manual_fixtures.py",
    POSTED_LOG,
    ANGLE_PATH,
    NEVER_POSTED_PATH,
    CANONICAL_LEDGER,
    "memory/content/linkedin-content-os/corpus-authority-manifest.v1.json",
    "memory/content/linkedin-content-os/manual-fixtures/evidence/manual-fixture-conflict-evidence.v1.json",
)


def _event(**fields: object) -> dict[str, object]:
    event: dict[str, object] = {"schemaVersion": "linkedin-content-outcome.v1", **fields}
    event["eventSha256"] = sha256_hex(canonical_bytes(event))
    return event


def _legacy_row_hash(repository: Path, source_file: str) -> str:
    rows = [
        json.loads(line)
        for line in (repository / POSTED_LOG).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    matches = [row for row in rows if row.get("source_file") == source_file]
    assert len(matches) == 1, source_file
    return sha256_hex(canonical_bytes(matches[0]))


def _isolated_repository(destination: Path) -> Path:
    """Copy the working-tree fixture code and governed inputs into one real-path repository.

    The canonical ledger is truncated to the Program 0 approved prefix so every test
    starts from governed state and appends only its own synthetic events.
    """

    shutil.copytree(
        REPOSITORY / "scripts/linkedin_content_os",
        destination / "scripts/linkedin_content_os",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    for relative in _ISOLATED_FILES:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPOSITORY / relative, target)
    manifest = json.loads(
        (destination / "memory/content/linkedin-content-os/corpus-authority-manifest.v1.json").read_text(
            encoding="utf-8"
        )
    )
    ledger = destination / CANONICAL_LEDGER
    approved = ledger.read_bytes().splitlines(keepends=True)[: int(manifest["ledgerPosition"])]
    ledger.write_bytes(b"".join(approved))
    return destination


def _append_events(ledger: Path, events: list[dict[str, object]]) -> None:
    ledger.write_bytes(ledger.read_bytes() + b"".join(canonical_bytes(event) + b"\n" for event in events))


def _governed_publication_events(
    row_hash: str, excerpt: str, *, recorded_at: str = "2026-09-30T09:00:00-04:00"
) -> list[dict[str, object]]:
    final_text = "Synthetic governed capture for fixture tests.\n\n{}".format(excerpt)
    final_hash = sha256_hex(final_text.encode("utf-8"))
    pointer = {
        "sourceType": "linkedin_publication_capture",
        "sourceId": SYNTHETIC_URL,
        "sourceSha256": final_hash,
    }
    return [
        _event(
            outcomeEventId="history-governed:{}".format(row_hash),
            packetId="legacy:{}".format(row_hash),
            eventType="historical_status",
            recordedAt=recorded_at,
            sourcePointer=pointer,
            payload={"legacyRowSha256": row_hash, "status": "posted_confirmed"},
        ),
        _event(
            outcomeEventId="publication:{}".format(row_hash),
            packetId="legacy:{}".format(row_hash),
            eventType="publication_acknowledged",
            recordedAt=recorded_at,
            sourcePointer=pointer,
            payload={
                "publicationUrl": SYNTHETIC_URL,
                "publishedAt": "2026-08-03T10:36:50-04:00",
                "finalText": final_text,
                "finalTextSha256": final_hash,
            },
        ),
    ]


def _status_event(row_hash: str, status: str, recorded_at: str, event_id: str) -> dict[str, object]:
    return _event(
        outcomeEventId=event_id,
        packetId="legacy:{}".format(row_hash),
        eventType="historical_status",
        recordedAt=recorded_at,
        sourcePointer={
            "sourceType": "jt_human_gate_response",
            "sourceId": "sha256:{}".format("a" * 64),
            "sourceSha256": "a" * 64,
        },
        payload={"legacyRowSha256": row_hash, "status": status},
    )


def _legacy_confirmation_angle(repository: Path, confirmation_path: str, event_id: str) -> dict[str, object]:
    """The caller-selected confirmation shape accepted by the rejected c4aefea contract."""

    return {
        "kind": "jt_field_lesson",
        "path": ANGLE_PATH,
        "excerpt": ANGLE_EXCERPT,
        "fileSha256": sha256_hex((repository / ANGLE_PATH).read_bytes()),
        "confirmationPath": confirmation_path,
        "confirmationExcerpt": event_id,
        "confirmationFileSha256": sha256_hex((repository / confirmation_path).read_bytes()),
    }


def _governed_angle(repository: Path, path: str = ANGLE_PATH, excerpt: str = ANGLE_EXCERPT) -> dict[str, object]:
    return {
        "kind": "jt_field_lesson",
        "path": path,
        "excerpt": excerpt,
        "fileSha256": sha256_hex((repository / path).read_bytes()),
    }


def _run_build(repository: Path, spec: dict[str, object], artifact_root: Path, now: datetime) -> subprocess.CompletedProcess:
    spec_path = artifact_root.parent / "{}-spec.json".format(artifact_root.name)
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            "-B",
            "scripts/build_linkedin_manual_fixtures.py",
            "--source",
            str(spec_path),
            "--artifact-root",
            str(artifact_root),
            "--now",
            now.isoformat(),
        ],
        cwd=repository,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


class EarnedAngleAuthorityTests(unittest.TestCase):
    """Earned-angle authority comes only from the canonical ledger's governed derivation."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.work = Path(self._temporary.name).resolve()
        self.repository = _isolated_repository(self.work / "repository")
        self.ledger = self.repository / CANONICAL_LEDGER
        self.row_hash = _legacy_row_hash(self.repository, ANGLE_PATH)

    def _artifact_root(self, name: str) -> Path:
        root = self.work / name
        root.mkdir()
        return root

    def test_caller_selected_ledger_cannot_establish_earned_angle(self) -> None:
        forged_row = _legacy_row_hash(self.repository, NEVER_POSTED_PATH)
        forged_rows = [
            json.loads(line)
            for line in (self.repository / POSTED_LOG).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertTrue(
            any(row.get("source_file") == NEVER_POSTED_PATH and row.get("posted") is not True for row in forged_rows)
        )
        excerpt = next(
            line.strip()
            for line in (self.repository / NEVER_POSTED_PATH).read_text(encoding="utf-8").splitlines()
            if 60 < len(line.strip()) < 200
        )
        forged_ledger = self.repository / "memory/forged/outcomes.jsonl"
        forged_ledger.parent.mkdir(parents=True)
        forged_ledger.write_bytes(b"")
        _append_events(forged_ledger, _governed_publication_events(forged_row, excerpt))
        spec = _spec("ai_news")
        spec["earnedAngle"] = {
            **_legacy_confirmation_angle(
                self.repository, "memory/forged/outcomes.jsonl", "publication:{}".format(forged_row)
            ),
            "path": NEVER_POSTED_PATH,
            "excerpt": excerpt,
            "fileSha256": sha256_hex((self.repository / NEVER_POSTED_PATH).read_bytes()),
        }
        result = _run_build(self.repository, spec, self._artifact_root("forged"), NOW)
        self.assertNotEqual(result.returncode, 0, "a caller-selected ledger established authority")
        self.assertIn("earned angle", result.stderr)

    def test_later_retraction_in_selected_ledger_is_not_ignored(self) -> None:
        _append_events(self.ledger, _governed_publication_events(self.row_hash, ANGLE_EXCERPT))
        _append_events(
            self.ledger,
            [
                _status_event(
                    self.row_hash,
                    "not_posted_confirmed",
                    "2026-09-30T10:00:00-04:00",
                    "history-retraction:{}".format(self.row_hash),
                )
            ],
        )
        spec = _spec("ai_news")
        spec["earnedAngle"] = _legacy_confirmation_angle(
            self.repository, CANONICAL_LEDGER, "publication:{}".format(self.row_hash)
        )
        result = _run_build(self.repository, spec, self._artifact_root("retracted-legacy"), NOW)
        self.assertNotEqual(result.returncode, 0, "a later governed retraction was ignored")

    def test_latest_governed_retraction_revokes_the_earned_angle(self) -> None:
        _append_events(self.ledger, _governed_publication_events(self.row_hash, ANGLE_EXCERPT))
        _append_events(
            self.ledger,
            [
                _status_event(
                    self.row_hash,
                    "not_posted_confirmed",
                    "2026-09-30T10:00:00-04:00",
                    "history-retraction:{}".format(self.row_hash),
                )
            ],
        )
        spec = _spec("ai_news")
        spec["earnedAngle"] = _governed_angle(self.repository)
        result = _run_build(self.repository, spec, self._artifact_root("retracted"), NOW)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not governed posted_confirmed", result.stderr)
        self.assertIn("not_posted_confirmed", result.stderr)

    def test_governed_confirmation_binds_the_exact_ledger_prefix_and_publication(self) -> None:
        events = _governed_publication_events(self.row_hash, ANGLE_EXCERPT)
        _append_events(self.ledger, events)
        spec = _spec("ai_news")
        spec["earnedAngle"] = _governed_angle(self.repository)
        result = _run_build(self.repository, spec, self._artifact_root("governed"), NOW)
        self.assertEqual(result.returncode, 0, result.stderr)
        angle = json.loads(result.stdout)["earnedAngle"]
        ledger_lines = self.ledger.read_bytes().splitlines(keepends=True)
        self.assertEqual(angle["legacyRowSha256"], self.row_hash)
        self.assertEqual(angle["ledgerPosition"], len(ledger_lines))
        self.assertEqual(angle["ledgerPrefixSha256"], sha256_hex(b"".join(ledger_lines)))
        self.assertEqual(angle["publicationEventId"], events[1]["outcomeEventId"])
        self.assertEqual(angle["publicationEventSha256"], events[1]["eventSha256"])
        self.assertEqual(angle["publicationUrl"], SYNTHETIC_URL)
        self.assertEqual(angle["finalTextSha256"], events[1]["payload"]["finalTextSha256"])

    def test_unrelated_later_events_keep_the_bound_angle_valid_but_row_events_do_not(self) -> None:
        _append_events(self.ledger, _governed_publication_events(self.row_hash, ANGLE_EXCERPT))
        spec = _spec("ai_news")
        spec["earnedAngle"] = _governed_angle(self.repository)
        artifact_root = self._artifact_root("prefix")
        first = _run_build(self.repository, spec, artifact_root, NOW)
        self.assertEqual(first.returncode, 0, first.stderr)

        unrelated_row = _legacy_row_hash(self.repository, NEVER_POSTED_PATH)
        _append_events(
            self.ledger,
            [
                _status_event(
                    unrelated_row,
                    "status_unknown",
                    "2026-09-30T11:00:00-04:00",
                    "history-unrelated:{}".format(unrelated_row),
                )
            ],
        )
        replay = _run_build(self.repository, spec, artifact_root, NOW)
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(replay.stdout, first.stdout)

        _append_events(
            self.ledger,
            [
                _status_event(
                    self.row_hash,
                    "status_unknown",
                    "2026-09-30T12:00:00-04:00",
                    "history-later:{}".format(self.row_hash),
                )
            ],
        )
        revoked = _run_build(self.repository, spec, artifact_root, NOW)
        self.assertNotEqual(revoked.returncode, 0)
        self.assertIn("not governed posted_confirmed", revoked.stderr)

    def test_symlinked_posted_log_cannot_supply_the_source_row(self) -> None:
        _append_events(self.ledger, _governed_publication_events(self.row_hash, ANGLE_EXCERPT))
        outside = self.work / "outside-posted-log.jsonl"
        posted_log = self.repository / POSTED_LOG
        outside.write_bytes(posted_log.read_bytes())
        posted_log.unlink()
        posted_log.symlink_to(outside)
        spec = _spec("ai_news")
        spec["earnedAngle"] = _legacy_confirmation_angle(
            self.repository, CANONICAL_LEDGER, "publication:{}".format(self.row_hash)
        )
        legacy = _run_build(self.repository, spec, self._artifact_root("posted-log-legacy"), NOW)
        self.assertNotEqual(legacy.returncode, 0, "a symlinked posted log supplied the source row")
        spec["earnedAngle"] = _governed_angle(self.repository)
        governed = _run_build(self.repository, spec, self._artifact_root("posted-log"), NOW)
        self.assertNotEqual(governed.returncode, 0)
        self.assertIn("symlink", governed.stderr)

    def test_symlinked_canonical_ledger_is_rejected(self) -> None:
        _append_events(self.ledger, _governed_publication_events(self.row_hash, ANGLE_EXCERPT))
        outside = self.work / "outside-ledger.jsonl"
        outside.write_bytes(self.ledger.read_bytes())
        self.ledger.unlink()
        self.ledger.symlink_to(outside)
        spec = _spec("ai_news")
        spec["earnedAngle"] = _governed_angle(self.repository)
        result = _run_build(self.repository, spec, self._artifact_root("ledger-link"), NOW)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("canonical outcome ledger contains a symlink component", result.stderr)


class TrackedFixtureStateTests(unittest.TestCase):
    """The real repository's canonical ledger must not confirm either tracked fixture."""

    def test_accepted_set_blocks_both_candidates_until_governed_confirmation(self) -> None:
        fixture_root = REPOSITORY / "memory/content/linkedin-content-os/manual-fixtures"
        accepted_set = json.loads((fixture_root / "accepted-set.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(accepted_set["state"], "blocked_pending_governed_publication_confirmation")
        self.assertEqual(accepted_set["candidatePackets"], [])
        self.assertIs(accepted_set["externalActionsAuthorized"], False)
        blocked = accepted_set["blockedCandidates"]
        self.assertEqual(
            sorted(candidate["packetId"] for candidate in blocked),
            ["linkedin-ai-news-openai-health-2026-09-29-v1", "linkedin-teardown-servicenow-inry-2026-09-29-v1"],
        )
        for candidate in blocked:
            with self.subTest(packetId=candidate["packetId"]):
                spec_path = REPOSITORY / candidate["sourceSpec"]
                self.assertEqual(sha256_hex(spec_path.read_bytes()), candidate["sourceSpecSha256"])
                self.assertFalse((fixture_root / candidate["packetId"]).exists())
                self.assertEqual(
                    candidate["legacyRowSha256"], _legacy_row_hash(REPOSITORY, candidate["earnedAnglePath"])
                )
                with tempfile.TemporaryDirectory() as temporary:
                    with self.assertRaises(ValueError) as raised:
                        build_manual_fixture(
                            json.loads(spec_path.read_text(encoding="utf-8")), Path(temporary), now=TRACKED_NOW
                        )
                self.assertEqual(str(raised.exception), candidate["blockReason"])
        self.assertEqual(
            sorted(artifact["packetId"] for artifact in accepted_set["rejectedArtifacts"]),
            ["linkedin-ai-news-openai-health-2026-09-29-v1", "linkedin-teardown-servicenow-inry-2026-09-29-v1"],
        )


class LockPathTests(unittest.TestCase):
    def test_existing_lock_symlink_cannot_create_an_external_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            guarded = root / "guarded"
            guarded.mkdir()
            outside = root / "outside-target"
            (root / ".guarded.lock").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "lock path must not be a symlink"):
                with _exclusive_path_lock(guarded):
                    pass
            self.assertFalse(outside.exists())


def _rehash(packet: dict[str, object]) -> dict[str, object]:
    packet["draftSha256"] = sha256_hex(canonical_bytes(_draft_binding(packet)))
    packet["payloadSha256"] = sha256_hex(canonical_bytes(_payload_binding(packet)))
    return packet


def _spec(lane: str) -> dict[str, object]:
    slug_lane = lane.replace("_", "-")
    source = {
        "sourceId": "primary-1",
        "sourceType": "official_release",
        "uri": "https://example.com/official-release",
        "publishedAt": "2026-09-24T00:00:00+00:00",
        "retrievedAt": "2026-09-28T20:00:00+00:00",
        "publisher": "Example",
        "title": "Official release",
        "excerpts": [
            "Identity-only sign-in remains separate from data access.",
            "Both new permissions are off by default during the admin preview.",
        ],
    }
    claims = [
        {
            "claimId": "claim-1",
            "text": "Identity-only sign-in remains separate from data access.",
            "attributionType": "vendor_assertion",
            "sourceId": "primary-1",
            "excerptIndex": 0,
        }
    ]
    spec: dict[str, object] = {
        "schemaVersion": "manual-linkedin-fixture-source.v1",
        "packetId": "linkedin-{}-2026-09-28-v1".format(slug_lane),
        "revisionFamilyId": "linkedin-{}-2026-09-28".format(slug_lane),
        "packetVersion": 1,
        "lane": lane,
        "createdAt": "2026-09-28T20:00:00+00:00",
        "expiresAt": "2026-10-08T00:00:00+00:00" if lane == "teardown" else "2026-09-29T00:00:00+00:00",
        "targetReader": "Enterprise AI operations leaders",
        "commercialObjective": "Show governed AI workflow judgment.",
        "whyThisWon": "Fresh primary evidence supports a buyer-relevant operating lesson.",
        "postText": "Access has multiple controls.\n\nIdentity-only sign-in remains separate from data access.",
        "sources": [source],
        "claims": claims,
        "earnedAngle": _governed_angle(REPOSITORY),
        "conflictChecks": [
            {
                "check": name,
                "status": "pass",
                "evidence": {
                    "consulting_suppression": "No exact ServiceNow or INRY entity match exists in the governed client tree.",
                    "client_conflict": "No current client record names ServiceNow or INRY.",
                    "prospect_conflict": "No prospect-discovery record names ServiceNow or INRY.",
                    "job_conflict": "ServiceNow appears only in historical market commentary; no active application record names ServiceNow or INRY.",
                    "employer_conflict": "No current employer record names ServiceNow or INRY.",
                    "source_identity": "The cited URL is OpenAI's official ChatGPT release-notes page.",
                    "claim_attribution": "The release date and feature statement are attributed to the official release; operator recommendations remain separate.",
                    "protected_purpose_removed": "The public surfaces contain no private client, queue, outreach, job-search, or internal workflow material.",
                }[name],
                "evidenceRef": {
                    "path": "memory/content/linkedin-content-os/manual-fixtures/evidence/manual-fixture-conflict-evidence.v1.json",
                    "fileSha256": "89370a8f97b2b98430955f29b7c1e40de8ec9d834e99e3bfac438c12bd2166bc",
                    "recordId": {
                        "consulting_suppression": "servicenow-inry-consulting-suppression",
                        "client_conflict": "servicenow-inry-client-conflict",
                        "prospect_conflict": "servicenow-inry-prospect-conflict",
                        "job_conflict": "servicenow-inry-job-conflict",
                        "employer_conflict": "servicenow-inry-employer-conflict",
                        "source_identity": "openai-health-source-identity",
                        "claim_attribution": "openai-health-claim-attribution",
                        "protected_purpose_removed": "openai-health-protected-purpose",
                    }[name],
                },
            }
            for name in (
                ("consulting_suppression", "client_conflict", "prospect_conflict", "job_conflict", "employer_conflict")
                if lane == "teardown"
                else ("source_identity", "claim_attribution", "protected_purpose_removed")
            )
        ],
        "altText": "A five-stage control path from identity to human approval.",
        "cropGuidance": "Use the full 4:5 image; keep all text inside the 72-pixel safe area.",
        "privacyResult": {"status": "pass", "details": "Public sources and original graphics only."},
        "rightsResult": {"status": "pass", "details": "Original text-first render; no logos, screenshots, or source artwork."},
        "qa": {
            "evidence": "pass",
            "originality": "pass",
            "privacy": "pass",
            "rights": "pass",
            "strategicFit": "pass",
            "voice": "pending_human_rating",
        },
    }
    if lane == "teardown":
        spec["visual"] = {
            "template": "teardown-schematic.v1",
            "eyebrow": "PUBLIC-EVIDENCE TEARDOWN",
            "title": "Connect the bank event to the property record",
            "subtitle": "A proposed exception-first operating path",
            "stages": ["Money moves", "Validate context", "Human approval", "Ledger record", "Exception owned"],
            "footer": "Proposed system based on public information",
        }
    else:
        spec["visual"] = {
            "template": "ai-news-source-card.v1",
            "eyebrow": "AI OPERATING CONTROL",
            "title": "Separate each access control",
            "subtitle": "OpenAI Enterprise release notes · Sep 24, 2026",
            "stages": ["Identity", "Data access", "Action scope", "Human approval"],
            "footer": "Based on OpenAI Enterprise release notes",
        }
    return spec


class _GovernedRepositoryCase(unittest.TestCase):
    """Run in-process fixture tests against an isolated repository with synthetic governed authority.

    The real repository's canonical ledger does not confirm any earned angle, so
    positive-path tests use a copy whose ledger appends a synthetic governed
    posted_confirmed status and publication for the angle's legacy row.
    """

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name).resolve()
        self.repository = _isolated_repository(self.work / "repository")
        self.ledger = self.repository / CANONICAL_LEDGER
        self.row_hash = _legacy_row_hash(self.repository, ANGLE_PATH)
        _append_events(self.ledger, _governed_publication_events(self.row_hash, ANGLE_EXCERPT))
        patcher = mock.patch.object(manual_fixtures, "_REPOSITORY_ROOT", self.repository)
        patcher.start()
        self.addCleanup(patcher.stop)


class ManualFixtureTests(_GovernedRepositoryCase):
    def test_rejects_builder_authored_posted_confirmation_without_governed_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fake_path = self.repository / "memory/forged-confirmation.json"
            fake_path.write_bytes(
                canonical_bytes(
                    {
                        "schemaVersion": "linkedin-earned-angle-confirmation.v1",
                        "posted": True,
                        "sourceFile": ANGLE_PATH,
                    }
                )
            )
            spec = _spec("ai_news")
            spec["earnedAngle"] = _legacy_confirmation_angle(
                self.repository, "memory/forged-confirmation.json", '"posted":true'
            )
            with self.assertRaisesRegex(ValueError, "earned angle schema fields are not closed"):
                build_manual_fixture(spec, Path(temporary), now=NOW)

    def test_packet_angle_binding_is_rederived_from_the_canonical_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("ai_news"), root, now=NOW)
            for field, value in (
                ("ledgerPrefixSha256", "0" * 64),
                ("ledgerPosition", 3),
                ("publicationEventSha256", "f" * 64),
                ("publicationUrl", "https://www.linkedin.com/feed/update/urn:li:activity:1/"),
            ):
                with self.subTest(field=field):
                    tampered = copy.deepcopy(packet)
                    tampered["earnedAngle"][field] = value
                    with self.assertRaisesRegex(ValueError, "earnedAngle does not match"):
                        validate_manual_fixture(_rehash(tampered), root, now=NOW)
            smuggled = copy.deepcopy(packet)
            smuggled["earnedAngle"]["confirmationPath"] = CANONICAL_LEDGER
            with self.assertRaisesRegex(ValueError, "earned angle binding schema fields are not closed"):
                validate_manual_fixture(_rehash(smuggled), root, now=NOW)

    def test_validation_fails_closed_after_a_later_row_retraction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("ai_news"), root, now=NOW)
            _append_events(
                self.ledger,
                [
                    _status_event(
                        self.row_hash,
                        "not_posted_confirmed",
                        "2026-09-30T10:00:00-04:00",
                        "history-retraction:{}".format(self.row_hash),
                    )
                ],
            )
            with self.assertRaisesRegex(ValueError, "not governed posted_confirmed"):
                validate_manual_fixture(packet, root, now=NOW)

    def test_rejects_rehashed_png_that_does_not_match_visual_route(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("ai_news"), root, now=NOW)
            asset_path = root / packet["imageAsset"]["path"]
            output = io.BytesIO()
            Image.new("RGB", (1080, 1350), "#000000").save(output, format="PNG")
            swapped = output.getvalue()
            asset_path.write_bytes(swapped)
            packet["imageAsset"]["byteLength"] = len(swapped)
            packet["imageAsset"]["sha256"] = sha256_hex(swapped)
            packet["payloadSha256"] = sha256_hex(canonical_bytes(_payload_binding(packet)))
            with self.assertRaisesRegex(ValueError, "render|visual|pixel"):
                validate_manual_fixture(packet, root, now=NOW)

    def test_rejects_ancestor_symlink_escape_before_build_or_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            root = Path(temporary)
            (root / "manual-fixtures").symlink_to(Path(outside), target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink|artifact root"):
                build_manual_fixture(_spec("teardown"), root, now=NOW)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_every_governed_rule_is_enforced_on_every_fixture_surface(self) -> None:
        from scripts.linkedin_content_os.manual_fixtures import _normalize_spec
        from scripts.tests.test_linkedin_content_os_content_policy import BANNED_EXAMPLES

        representatives: dict[str, str] = {}
        for rule, text in BANNED_EXAMPLES:
            representatives.setdefault(rule, text)
        surfaces = (
            ("post", ("postText", None)),
            ("eyebrow", ("visual", "eyebrow")),
            ("title", ("visual", "title")),
            ("subtitle", ("visual", "subtitle")),
            ("stage", ("visual", "stages")),
            ("footer", ("visual", "footer")),
            ("alt", ("altText", None)),
        )
        for rule, blocked_text in sorted(representatives.items()):
            for surface, (field, nested) in surfaces:
                with self.subTest(rule=rule, surface=surface):
                    spec = _spec("ai_news")
                    if field == "postText":
                        spec[field] = "{}\n\n{}".format(spec[field], blocked_text)
                    elif nested == "stages":
                        spec[field][nested][0] = blocked_text
                    elif field == "visual":
                        spec[field][nested] = blocked_text
                    else:
                        spec[field] = blocked_text
                    with self.assertRaisesRegex(ValueError, "prohibited public copy"):
                        _normalize_spec(spec, NOW)

    def test_teardown_requires_exact_primary_story_permalink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = _spec("teardown")
            spec["sources"][0]["publisher"] = "ServiceNow"
            spec["sources"][0]["uri"] = "https://newsroom.servicenow.com/overview/default.aspx"
            with self.assertRaisesRegex(ValueError, "permalink|primary story"):
                build_manual_fixture(spec, Path(temporary), now=NOW)

    def test_official_release_claims_require_vendor_attribution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = _spec("ai_news")
            spec["claims"][0]["attributionType"] = "public_fact"
            with self.assertRaisesRegex(ValueError, "attribution"):
                build_manual_fixture(spec, Path(temporary), now=NOW)

    def test_created_at_cannot_precede_source_retrieval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = _spec("ai_news")
            spec["createdAt"] = "2026-09-28T19:59:59+00:00"
            with self.assertRaisesRegex(ValueError, "createdAt|retrievedAt|chronology"):
                build_manual_fixture(spec, Path(temporary), now=NOW)

    def test_orphan_asset_is_refused_instead_of_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = _spec("teardown")
            directory = root / "manual-fixtures" / spec["packetId"]
            directory.mkdir(parents=True)
            orphan = directory / "image.v1.png"
            orphan.write_bytes(b"orphan")
            with self.assertRaisesRegex(ValueError, "orphan"):
                build_manual_fixture(spec, root, now=NOW)
            self.assertEqual(orphan.read_bytes(), b"orphan")

    def test_renderer_rejects_horizontal_overflow(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            overwide_stage = _spec("teardown")
            overwide_stage["visual"]["stages"][0] = "Reconciliation"
            with self.assertRaisesRegex(ValueError, "overflow"):
                build_manual_fixture(overwide_stage, Path(temporary), now=NOW)

        with tempfile.TemporaryDirectory() as temporary:
            overwide_eyebrow = _spec("ai_news")
            overwide_eyebrow["visual"]["eyebrow"] = (
                "THIS EYEBROW IS FAR TOO WIDE FOR THE SAFE CARD BOUNDARY AND MUST BE REJECTED"
            )
            with self.assertRaisesRegex(ValueError, "eyebrow.*overflow"):
                build_manual_fixture(overwide_eyebrow, Path(temporary), now=NOW)

    def test_packet_records_and_validates_renderer_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("ai_news"), root, now=NOW)
            identity = packet["imageAsset"]["rendererIdentity"]
            self.assertEqual(identity["schemaVersion"], "linkedin-png-renderer.v1")
            self.assertRegex(identity["pillowVersion"], r"^\d+\.\d+")
            self.assertEqual(len(identity["regularFontSha256"]), 64)
            self.assertEqual(len(identity["monoFontSha256"]), 64)

            tampered = copy.deepcopy(packet)
            tampered["imageAsset"]["rendererIdentity"]["pillowVersion"] = "0.0-forged"
            _rehash(tampered)
            with self.assertRaisesRegex(ValueError, "renderer"):
                validate_manual_fixture(tampered, root, now=NOW)

    def test_conflict_checks_require_hash_bound_evidence_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = _spec("teardown")
            spec["conflictChecks"][0]["evidenceRef"]["recordId"] = "missing-record"
            with self.assertRaisesRegex(ValueError, "conflict evidence"):
                build_manual_fixture(spec, Path(temporary), now=NOW)

    def test_tracked_sources_build_and_replay_once_governed_confirmation_exists(self) -> None:
        fixture_root = REPOSITORY / "memory/content/linkedin-content-os/manual-fixtures"
        accepted_set = json.loads((fixture_root / "accepted-set.v1.json").read_text(encoding="utf-8"))
        blocked = accepted_set["blockedCandidates"]
        self.assertEqual(len(blocked), 2)
        with tempfile.TemporaryDirectory() as first_root, tempfile.TemporaryDirectory() as second_root:
            for candidate in blocked:
                source = json.loads((REPOSITORY / candidate["sourceSpec"]).read_text(encoding="utf-8"))
                first = build_manual_fixture(source, Path(first_root), now=TRACKED_NOW)
                second = build_manual_fixture(source, Path(second_root), now=TRACKED_NOW)
                self.assertEqual(first, second)
                for name in ("packet.v1.json", "image.v1.png"):
                    self.assertEqual(
                        (Path(first_root) / "manual-fixtures" / candidate["packetId"] / name).read_bytes(),
                        (Path(second_root) / "manual-fixtures" / candidate["packetId"] / name).read_bytes(),
                    )
                self.assertEqual(first["earnedAngle"]["legacyRowSha256"], candidate["legacyRowSha256"])
                with Image.open(Path(first_root) / first["imageAsset"]["path"]) as image:
                    self.assertEqual(image.size, (1080, 1350))

    def test_cli_builds_in_a_governed_repository(self) -> None:
        source = json.loads(
            (
                REPOSITORY
                / "memory/content/linkedin-content-os/manual-fixtures/sources/servicenow-inry-employee-front-door-teardown.v1.json"
            ).read_text(encoding="utf-8")
        )
        artifact_root = self.work / "cli-artifacts"
        artifact_root.mkdir()
        result = _run_build(self.repository, source, artifact_root, TRACKED_NOW)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"schemaVersion":"content-packet.v1"', result.stdout)

    def test_builds_one_canonical_hashed_png_packet_per_lane(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for lane in ("teardown", "ai_news"):
                packet = build_manual_fixture(_spec(lane), root, now=NOW)
                validated = validate_manual_fixture(packet, root, now=NOW)
                self.assertEqual(validated, packet)
                self.assertEqual(packet["state"], "qa_passed")
                self.assertEqual(packet["decisionOptions"], ["approve", "reject", "skip"])
                asset = packet["imageAsset"]
                asset_path = root / asset["path"]
                self.assertEqual(asset["mimeType"], "image/png")
                self.assertEqual(asset["width"], 1080)
                self.assertEqual(asset["height"], 1350)
                self.assertEqual(asset["byteLength"], len(asset_path.read_bytes()))
                self.assertEqual(asset["sha256"], sha256_hex(asset_path.read_bytes()))
                with Image.open(asset_path) as image:
                    self.assertEqual(image.size, (1080, 1350))
                    self.assertEqual(image.format, "PNG")

    def test_rejects_stale_sources_and_missing_jt_angle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            stale = _spec("ai_news")
            stale["sources"][0]["publishedAt"] = "2026-09-20T00:00:00+00:00"
            with self.assertRaisesRegex(ValueError, "freshness"):
                build_manual_fixture(stale, Path(temporary), now=NOW)
            no_angle = _spec("ai_news")
            no_angle["earnedAngle"] = {}
            with self.assertRaisesRegex(ValueError, "earned angle"):
                build_manual_fixture(no_angle, Path(temporary), now=NOW)

            forged_angle = _spec("ai_news")
            forged_angle["earnedAngle"]["fileSha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "earned angle.*hash"):
                build_manual_fixture(forged_angle, Path(temporary), now=NOW)

    def test_expiry_is_bounded_by_the_source_freshness_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = _spec("ai_news")
            spec["expiresAt"] = "2026-10-03T00:00:00+00:00"
            with self.assertRaisesRegex(ValueError, "freshness"):
                build_manual_fixture(spec, Path(temporary), now=NOW)

    def test_requires_closed_conflict_checks_and_posted_angle_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing_check = _spec("teardown")
            missing_check["conflictChecks"] = missing_check["conflictChecks"][:-1]
            with self.assertRaisesRegex(ValueError, "conflict checks"):
                build_manual_fixture(missing_check, Path(temporary), now=NOW)

            ungoverned_row = _spec("ai_news")
            ungoverned_row["earnedAngle"] = _governed_angle(
                self.repository,
                NEVER_POSTED_PATH,
                next(
                    line.strip()
                    for line in (self.repository / NEVER_POSTED_PATH).read_text(encoding="utf-8").splitlines()
                    if 60 < len(line.strip()) < 200
                ),
            )
            with self.assertRaisesRegex(ValueError, "not governed posted_confirmed"):
                build_manual_fixture(ungoverned_row, Path(temporary), now=NOW)

    def test_rejects_unbound_claims_and_invalid_visual_routes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            unbound = _spec("teardown")
            unbound["claims"][0]["excerptIndex"] = 9
            with self.assertRaisesRegex(ValueError, "claim evidence"):
                build_manual_fixture(unbound, Path(temporary), now=NOW)
            missing_label = _spec("teardown")
            missing_label["visual"]["footer"] = "Public sources"
            with self.assertRaisesRegex(ValueError, "public information"):
                build_manual_fixture(missing_label, Path(temporary), now=NOW)
            wrong_news_route = _spec("ai_news")
            wrong_news_route["visual"]["template"] = "source-screenshot.v1"
            with self.assertRaisesRegex(ValueError, "text-first"):
                build_manual_fixture(wrong_news_route, Path(temporary), now=NOW)

    def test_tampering_any_payload_binding_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("ai_news"), root, now=NOW)
            for path, value in (
                (("postText",), "Changed text"),
                (("altText",), "Changed alt text"),
                (("rightsResult", "details"), "Changed rights result"),
                (("imageAsset", "sha256"), "0" * 64),
            ):
                tampered = copy.deepcopy(packet)
                target = tampered
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaisesRegex(ValueError, "hash|asset|claim"):
                    validate_manual_fixture(tampered, root, now=NOW)

    def test_self_consistent_tampering_is_rederived_and_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("ai_news"), root, now=NOW)

            cases = []
            failed_privacy = copy.deepcopy(packet)
            failed_privacy["privacyResult"]["status"] = "fail"
            cases.append((failed_privacy, "privacyResult"))

            internal_alt = copy.deepcopy(packet)
            internal_alt["altText"] = "Mission Control access chain"
            cases.append((internal_alt, "internal"))

            wrong_lane = copy.deepcopy(packet)
            wrong_lane["lane"] = "teardown"
            cases.append((wrong_lane, "route|template|conflict"))

            bogus_claim = copy.deepcopy(packet)
            bogus_claim["claimEvidence"][0]["text"] = "A claim absent from the post."
            cases.append((bogus_claim, "claim"))

            for tampered, message in cases:
                with self.subTest(message=message):
                    with self.assertRaisesRegex(ValueError, message):
                        validate_manual_fixture(_rehash(tampered), root, now=NOW)

    def test_validation_rechecks_source_freshness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("ai_news"), root, now=NOW)
            later = datetime(2026, 9, 29, 1, 0, tzinfo=timezone.utc)
            with self.assertRaisesRegex(ValueError, "freshness"):
                validate_manual_fixture(packet, root, now=later)

    def test_rejects_traversal_ids_before_creating_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = _spec("teardown")
            spec["packetId"] = "../escaped"
            with self.assertRaisesRegex(ValueError, "packetId"):
                build_manual_fixture(spec, root, now=NOW)
            self.assertFalse((root / "escaped").exists())

    def test_rejects_symlinked_image_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = build_manual_fixture(_spec("teardown"), root, now=NOW)
            asset = root / packet["imageAsset"]["path"]
            target = root / "copied.png"
            target.write_bytes(asset.read_bytes())
            asset.unlink()
            asset.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "symlink"):
                validate_manual_fixture(packet, root, now=NOW)

    def test_exact_replay_is_byte_identical_and_conflict_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = build_manual_fixture(_spec("teardown"), root, now=NOW)
            asset = root / first["imageAsset"]["path"]
            before = asset.read_bytes()
            second = build_manual_fixture(_spec("teardown"), root, now=NOW)
            self.assertEqual(first, second)
            self.assertEqual(before, asset.read_bytes())
            conflict = _spec("teardown")
            conflict["postText"] = "Conflicting replay.\n\nIdentity-only sign-in remains separate from data access."
            with self.assertRaisesRegex(ValueError, "conflicting replay"):
                build_manual_fixture(conflict, root, now=NOW)


if __name__ == "__main__":
    unittest.main()
