from __future__ import annotations

import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.manual_fixtures import (
    _draft_binding,
    _payload_binding,
    build_manual_fixture,
    validate_manual_fixture,
)


NOW = datetime(2026, 9, 28, 20, 30, tzinfo=timezone.utc)


def _rehash(packet: dict[str, object]) -> dict[str, object]:
    packet["draftSha256"] = sha256_hex(canonical_bytes(_draft_binding(packet)))
    packet["payloadSha256"] = sha256_hex(canonical_bytes(_payload_binding(packet)))
    return packet


def _spec(lane: str) -> dict[str, object]:
    repository = Path(__file__).resolve().parents[2]
    angle_path = repository / "memory/drafts/linkedin-property-ops-source-to-decision-trail-2026-08-02.md"
    confirmation_path = repository / "memory/content/linkedin-content-os/outcomes.v1.jsonl"
    angle_excerpt = (
        "It proves what the workflow saw, what it was allowed to touch, what it held back, "
        "and where the decision landed."
    )
    confirmation_excerpt = "publication:fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf"
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
        "earnedAngle": {
            "kind": "jt_field_lesson",
            "path": "memory/drafts/linkedin-property-ops-source-to-decision-trail-2026-08-02.md",
            "excerpt": angle_excerpt,
            "fileSha256": sha256_hex(angle_path.read_bytes()),
            "confirmationPath": "memory/content/linkedin-content-os/outcomes.v1.jsonl",
            "confirmationExcerpt": confirmation_excerpt,
            "confirmationFileSha256": sha256_hex(confirmation_path.read_bytes()),
        },
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
            "footer": "Source: OpenAI Enterprise release notes",
        }
    return spec


class ManualFixtureTests(unittest.TestCase):
    def test_rejects_builder_authored_posted_confirmation_without_governed_outcome(self) -> None:
        repository = Path(__file__).resolve().parents[2]
        evidence_root = repository / "memory/content/linkedin-content-os/manual-fixtures/evidence"
        with tempfile.TemporaryDirectory(dir=evidence_root) as temporary:
            fake_path = Path(temporary) / "forged-confirmation.json"
            source_path = repository / "AGENTS.md"
            source_text = source_path.read_text(encoding="utf-8")
            excerpt = source_text.splitlines()[0]
            fake_record = {
                "schemaVersion": "linkedin-earned-angle-confirmation.v1",
                "topic": "forged-builder-claim",
                "posted": True,
                "confirmationSource": "builder-authored",
                "sourceFile": "AGENTS.md",
                "sourceFileSha256": sha256_hex(source_path.read_bytes()),
                "loggedDate": "2026-09-29",
            }
            fake_path.write_bytes(canonical_bytes(fake_record))
            spec = _spec("ai_news")
            spec["earnedAngle"] = {
                "kind": "jt_field_lesson",
                "path": "AGENTS.md",
                "excerpt": excerpt,
                "fileSha256": sha256_hex(source_path.read_bytes()),
                "confirmationPath": fake_path.relative_to(repository).as_posix(),
                "confirmationExcerpt": '"posted":true',
                "confirmationFileSha256": sha256_hex(fake_path.read_bytes()),
            }
            with self.assertRaisesRegex(ValueError, "posted_confirmed|governed"):
                build_manual_fixture(spec, Path(temporary) / "artifacts", now=NOW)

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

    def test_canonical_public_text_blocks_apply_to_every_public_surface(self) -> None:
        cases = (
            ("postText", None, "Not speed but trust."),
            ("visual", "eyebrow", "EVE REVIEW QUEUE"),
            ("visual", "title", "The handoff everyone checks manually."),
            ("visual", "subtitle", "Stop condition"),
            ("visual", "stages", "state file"),
            ("visual", "footer", "My outreach automation"),
            ("altText", None, "Three checks: source, owner, and outcome."),
        )
        for field, nested, blocked_text in cases:
            with self.subTest(field=field, nested=nested):
                spec = _spec("ai_news")
                if field == "postText":
                    spec[field] = "{}\n\n{}".format(spec[field], blocked_text)
                elif field == "visual" and nested == "stages":
                    spec[field][nested][0] = blocked_text
                elif field == "visual":
                    spec[field][nested] = blocked_text
                else:
                    spec[field] = blocked_text
                with tempfile.TemporaryDirectory() as temporary:
                    with self.assertRaisesRegex(ValueError, "prohibited|blocked|internal"):
                        build_manual_fixture(spec, Path(temporary), now=NOW)

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

    def test_tracked_candidate_artifacts_replay_byte_identically(self) -> None:
        repository = Path(__file__).resolve().parents[2]
        fixture_root = repository / "memory/content/linkedin-content-os/manual-fixtures"
        accepted_set = json.loads((fixture_root / "accepted-set.v1.json").read_text(encoding="utf-8"))
        accepted_candidates = {
            candidate["packetId"]: candidate for candidate in accepted_set["candidatePackets"]
        }
        replay_now = datetime.fromisoformat("2026-09-29T21:40:00-04:00")
        source_names = (
            "servicenow-inry-employee-front-door-teardown.v1.json",
            "openai-health-summaries-ai-news.v1.json",
        )
        with tempfile.TemporaryDirectory() as temporary:
            replay_root = Path(temporary)
            for source_name in source_names:
                source = json.loads((fixture_root / "sources" / source_name).read_text(encoding="utf-8"))
                packet = build_manual_fixture(source, replay_root, now=replay_now)
                packet_id = packet["packetId"]
                tracked_directory = fixture_root / packet_id
                replay_directory = replay_root / "manual-fixtures" / packet_id
                self.assertEqual(
                    replay_directory.joinpath("packet.v1.json").read_bytes(),
                    tracked_directory.joinpath("packet.v1.json").read_bytes(),
                )
                self.assertEqual(
                    replay_directory.joinpath("image.v1.png").read_bytes(),
                    tracked_directory.joinpath("image.v1.png").read_bytes(),
                )
                candidate = accepted_candidates[packet_id]
                self.assertEqual(candidate["draftSha256"], packet["draftSha256"])
                self.assertEqual(candidate["payloadSha256"], packet["payloadSha256"])
                self.assertEqual(candidate["imageSha256"], packet["imageAsset"]["sha256"])

    def test_cli_runs_from_repository_root(self) -> None:
        repository = Path(__file__).resolve().parents[2]
        source = repository / "memory/content/linkedin-content-os/manual-fixtures/sources/servicenow-inry-employee-front-door-teardown.v1.json"
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_linkedin_manual_fixtures.py",
                    "--source",
                    str(source),
                    "--artifact-root",
                    temporary,
                    "--now",
                    "2026-09-29T20:30:00-04:00",
                ],
                cwd=repository,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
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

            forged_confirmation = _spec("ai_news")
            forged_confirmation["earnedAngle"]["confirmationFileSha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "confirmation.*hash"):
                build_manual_fixture(forged_confirmation, Path(temporary), now=NOW)

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
