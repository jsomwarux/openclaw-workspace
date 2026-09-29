from __future__ import annotations

import copy
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

from scripts.linkedin_content_os.canonical import sha256_hex
from scripts.linkedin_content_os.manual_fixtures import (
    build_manual_fixture,
    validate_manual_fixture,
)


NOW = datetime(2026, 9, 28, 20, 30, tzinfo=timezone.utc)


def _spec(lane: str) -> dict[str, object]:
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
            "attributionType": "public_fact",
            "sourceId": "primary-1",
            "excerptIndex": 0,
        }
    ]
    spec: dict[str, object] = {
        "schemaVersion": "manual-linkedin-fixture-source.v1",
        "packetId": "linkedin-{}-2026-09-28-v1".format(lane),
        "revisionFamilyId": "linkedin-{}-2026-09-28".format(lane),
        "packetVersion": 1,
        "lane": lane,
        "createdAt": "2026-09-28T20:00:00+00:00",
        "expiresAt": "2026-10-03T00:00:00+00:00",
        "targetReader": "Enterprise AI operations leaders",
        "commercialObjective": "Show governed AI workflow judgment.",
        "whyThisWon": "Fresh primary evidence supports a buyer-relevant operating lesson.",
        "postText": "Access is not one switch.\n\nIdentity and data permissions must stay separate.",
        "sources": [source],
        "claims": claims,
        "earnedAngle": {
            "kind": "jt_field_lesson",
            "path": "memory/content/technical-angles.md",
            "excerpt": "Source-of-truth drift before automation",
            "fileSha256": "1" * 64,
        },
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
            "title": "Access is a chain, not a switch",
            "subtitle": "OpenAI Enterprise release notes · Sep 24, 2026",
            "stages": ["Identity", "Data access", "Action scope", "Human approval"],
            "footer": "Source: OpenAI Enterprise release notes",
        }
    return spec


class ManualFixtureTests(unittest.TestCase):
    def test_cli_runs_from_repository_root(self) -> None:
        repository = Path(__file__).resolve().parents[2]
        source = repository / "memory/content/linkedin-content-os/manual-fixtures/sources/appfolio-column-teardown.v1.json"
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
                    "2026-09-28T20:30:00-04:00",
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
                with self.assertRaisesRegex(ValueError, "hash|asset"):
                    validate_manual_fixture(tampered, root, now=NOW)

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
            conflict["postText"] = "Conflicting replay"
            with self.assertRaisesRegex(ValueError, "conflicting replay"):
                build_manual_fixture(conflict, root, now=NOW)


if __name__ == "__main__":
    unittest.main()
