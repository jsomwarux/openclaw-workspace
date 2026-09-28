from __future__ import annotations

import unittest
from pathlib import Path

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.voice_rules import build_voice_rule_retirements


ROOT = Path(__file__).resolve().parents[2]
EFFECTIVE_DATE = "2026-09-28"
OWNER_PATHS = (
    Path("docs/agents/content-rules.md"),
    Path("memory/content-voice.md"),
    Path("skills/wednesday-linkedin/SKILL.md"),
)
RECONCILED_AUTHORITY = (
    "Exact JT-final LinkedIn text, evidence safety, and reconciled gates outrank "
    "fixed-day, fixed-format, and quota mechanics."
)


class VoiceRuleRetirementTests(unittest.TestCase):
    def _owner_documents(self) -> dict[str, bytes]:
        return {str(path): (ROOT / path).read_bytes() for path in OWNER_PATHS}

    def test_all_owner_surfaces_retire_conflicting_generation_authority(self) -> None:
        documents = self._owner_documents()
        for path, payload in documents.items():
            text = payload.decode("utf-8")
            with self.subTest(path=path):
                self.assertIn(RECONCILED_AUTHORITY, text)
                self.assertNotIn("target 5:1 ratio", text)
                self.assertNotIn("150-250 words. Prose only. No headers, no bullet lists.", text)
                self.assertNotIn("Wednesday is the most important post of the week", text)
                self.assertNotIn("Wednesday is JT's most important LinkedIn post", text)

        wednesday = documents["skills/wednesday-linkedin/SKILL.md"].decode("utf-8")
        self.assertNotIn("Wednesday is the highest-stakes post of the week", wednesday)
        self.assertNotIn(
            "Use this skill whenever drafting or reviewing a Wednesday LinkedIn case study post.",
            wednesday,
        )
        self.assertNotIn("Four moves, in order:", wednesday)

        voice = documents["memory/content-voice.md"].decode("utf-8")
        self.assertNotIn("## Content Calendar — Format by Day", voice)
        self.assertNotIn("For a normal weekly queue:", voice)

    def test_retirement_artifact_is_source_bound_and_complete(self) -> None:
        documents = self._owner_documents()
        artifact = build_voice_rule_retirements(documents, effective_date=EFFECTIVE_DATE)
        self.assertEqual(artifact["schemaVersion"], "linkedin-voice-rule-retirements.v1")
        self.assertEqual(artifact["effectiveDate"], EFFECTIVE_DATE)
        self.assertEqual(artifact["historicalBottleneck"], "quality_fit")
        self.assertEqual(artifact["legacyPostedFalseAuthority"], "status_unknown")
        self.assertEqual(artifact["ownerSourceSha256"], {
            path: sha256_hex(payload) for path, payload in sorted(documents.items())
        })

        retirements = artifact["retirements"]
        self.assertEqual(
            {record["oldRule"] for record in retirements},
            {
                "pronoun_ratio_5_to_1",
                "mandatory_wednesday_case_study",
                "universal_150_to_250_prose_only",
                "fixed_weekly_linkedin_quota",
            },
        )
        for record in retirements:
            with self.subTest(rule=record["oldRule"]):
                self.assertEqual(
                    set(record),
                    {
                        "oldRule",
                        "ownerSurfaces",
                        "replacementRule",
                        "reason",
                        "regressionTest",
                        "effectiveDate",
                    },
                )
                self.assertTrue(record["ownerSurfaces"])
                self.assertEqual(record["replacementRule"], RECONCILED_AUTHORITY)
                self.assertTrue(record["reason"])
                self.assertTrue(record["regressionTest"])
                self.assertEqual(record["effectiveDate"], EFFECTIVE_DATE)

        unsigned = dict(artifact)
        digest = unsigned.pop("retirementArtifactSha256")
        self.assertEqual(digest, sha256_hex(canonical_bytes(unsigned)))

    def test_retirement_builder_fails_closed_if_any_owner_still_conflicts(self) -> None:
        documents = self._owner_documents()
        documents[str(OWNER_PATHS[0])] += b"\nTarget 5:1 ratio.\n"
        with self.assertRaisesRegex(ValueError, "retired voice rule"):
            build_voice_rule_retirements(documents, effective_date=EFFECTIVE_DATE)

    def test_retirement_builder_refuses_missing_or_extra_owner_surfaces(self) -> None:
        documents = self._owner_documents()
        documents.pop(str(OWNER_PATHS[0]))
        with self.assertRaisesRegex(ValueError, "owner surfaces"):
            build_voice_rule_retirements(documents, effective_date=EFFECTIVE_DATE)

        documents = self._owner_documents()
        documents["extra.md"] = b"safe"
        with self.assertRaisesRegex(ValueError, "owner surfaces"):
            build_voice_rule_retirements(documents, effective_date=EFFECTIVE_DATE)


if __name__ == "__main__":
    unittest.main()
