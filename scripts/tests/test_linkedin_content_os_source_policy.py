from __future__ import annotations

from pathlib import Path
import unittest

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.source_policy import (
    build_source_policy,
    evidence_satisfies,
    validate_source_policy,
)


GENERATED_AT = "2026-09-28T16:30:00Z"
ROOT = Path(__file__).resolve().parents[2]


class SourcePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = build_source_policy(GENERATED_AT)

    def test_policy_has_exact_closed_family_set_and_hash(self) -> None:
        self.assertEqual(self.policy["schemaVersion"], "linkedin-source-policy.v1")
        self.assertEqual(self.policy["generatedAt"], GENERATED_AT)
        families = self.policy["families"]
        self.assertEqual(
            {record["family"] for record in families},
            {
                "client_delivery",
                "field_lesson",
                "engineering_recipe",
                "teardown_trigger",
                "ai_event",
                "internal_machinery",
            },
        )
        unsigned = dict(self.policy)
        digest = unsigned.pop("sourcePolicySha256")
        self.assertEqual(digest, sha256_hex(canonical_bytes(unsigned)))
        self.assertEqual(validate_source_policy(self.policy), self.policy)

    def test_every_family_owns_evidence_conflicts_permission_and_freshness(self) -> None:
        for record in self.policy["families"]:
            with self.subTest(family=record["family"]):
                self.assertEqual(
                    set(record),
                    {
                        "family",
                        "status",
                        "owner",
                        "requiredEvidence",
                        "conflictChecks",
                        "permissionRule",
                        "freshnessRule",
                    },
                )
                self.assertTrue(record["owner"])
                self.assertTrue(record["requiredEvidence"])
                self.assertTrue(record["conflictChecks"])
                self.assertTrue(record["permissionRule"])
                self.assertTrue(record["freshnessRule"])

    def test_family_owners_and_evidence_match_reconciled_contract(self) -> None:
        by_family = {record["family"]: record for record in self.policy["families"]}

        client = by_family["client_delivery"]
        self.assertEqual(client["status"], "allowed")
        self.assertEqual(client["owner"], "jt-ops immutable proof-asset Git object")
        self.assertIn("permission_evidence", client["requiredEvidence"])

        field = by_family["field_lesson"]
        self.assertEqual(field["owner"], "JT-confirmed field note or append-only outcome event")
        self.assertIn("jt_confirmation", field["requiredEvidence"])

        recipe = by_family["engineering_recipe"]
        self.assertEqual(recipe["owner"], "accepted verifier claim plus execution artifact")
        self.assertIn("protected_purpose_removed", recipe["conflictChecks"])
        self.assertNotIn("internal_machinery", recipe["requiredEvidence"])

        teardown = by_family["teardown_trigger"]
        self.assertEqual(teardown["owner"], "primary public source")
        self.assertEqual(
            teardown["conflictChecks"],
            [
                "consulting_suppression",
                "client_conflict",
                "prospect_conflict",
                "job_conflict",
                "employer_conflict",
            ],
        )

        ai_event = by_family["ai_event"]
        self.assertEqual(
            ai_event["owner"],
            "proven X Intelligence Router, JT-supplied source, or approved primary public source",
        )
        self.assertEqual(
            ai_event["requiredEvidence"],
            {
                "allOf": ["bound_jt_artifact"],
                "oneOf": [
                    ["proven_x_intelligence_router"],
                    ["jt_supplied_source"],
                    ["approved_primary_public_source"],
                ],
            },
        )
        self.assertNotIn("approved_primary_source", canonical_bytes(ai_event).decode("utf-8"))

    def test_ai_event_evidence_accepts_each_source_branch_with_bound_jt_artifact(self) -> None:
        ai_event = next(
            record for record in self.policy["families"] if record["family"] == "ai_event"
        )
        for source in (
            "proven_x_intelligence_router",
            "jt_supplied_source",
            "approved_primary_public_source",
        ):
            with self.subTest(source=source):
                self.assertTrue(
                    evidence_satisfies(ai_event, {source, "bound_jt_artifact"})
                )

        self.assertFalse(evidence_satisfies(ai_event, {"bound_jt_artifact"}))
        self.assertFalse(evidence_satisfies(ai_event, {"jt_supplied_source"}))
        self.assertFalse(
            evidence_satisfies(
                ai_event, {"approved_primary_source", "bound_jt_artifact"}
            )
        )

    def test_internal_machinery_is_absolute_prohibition(self) -> None:
        by_family = {record["family"]: record for record in self.policy["families"]}
        internal = by_family["internal_machinery"]
        self.assertEqual(internal["status"], "prohibited")
        self.assertEqual(internal["owner"], "no implicit override")
        self.assertEqual(internal["permissionRule"], "prohibited")
        self.assertIn("internal_machinery_prohibited", internal["conflictChecks"])
        self.assertEqual(internal["freshnessRule"], "not_applicable")

        recipe = by_family["engineering_recipe"]
        self.assertNotEqual(recipe["status"], "override")
        self.assertNotIn("implicit_override", canonical_bytes(recipe).decode("utf-8"))
        self.assertFalse(evidence_satisfies(internal, {"none"}))

    def test_evidence_evaluation_accepts_only_closed_canonical_allowed_family(self) -> None:
        client = next(
            record for record in self.policy["families"] if record["family"] == "client_delivery"
        )
        self.assertTrue(
            evidence_satisfies(
                client,
                {"immutable_git_object", "claim_level_facts", "permission_evidence"},
            )
        )

        for mutation in (
            {**client, "status": "prohibited"},
            {**client, "requiredEvidence": []},
            {**client, "family": "unknown_family"},
            {**client, "extra": True},
        ):
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError):
                    evidence_satisfies(mutation, set())

    def test_content_rules_make_internal_machinery_prohibition_absolute(self) -> None:
        content_rules = (ROOT / "docs/agents/content-rules.md").read_text(encoding="utf-8")
        self.assertIn(
            "V1 prohibits posts about JT's internal content machinery without exception.",
            content_rules,
        )
        self.assertNotIn(
            "unless JT explicitly asks for that topic",
            content_rules,
        )

    def test_policy_refuses_unknown_fields_and_test_fixture_authority(self) -> None:
        mutated = dict(self.policy)
        mutated["unknown"] = True
        with self.assertRaises(ValueError):
            validate_source_policy(mutated)

        self.assertNotIn("scripts/tests/fixtures/", canonical_bytes(self.policy).decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
