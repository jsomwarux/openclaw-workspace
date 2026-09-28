from __future__ import annotations

import unittest

from scripts.linkedin_content_os.canonical import canonical_bytes, sha256_hex
from scripts.linkedin_content_os.source_policy import (
    build_source_policy,
    validate_source_policy,
)


GENERATED_AT = "2026-09-28T16:30:00Z"


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
            "proven X Intelligence Router or approved primary public source",
        )
        self.assertIn("bound_jt_artifact", ai_event["requiredEvidence"])

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

    def test_policy_refuses_unknown_fields_and_test_fixture_authority(self) -> None:
        mutated = dict(self.policy)
        mutated["unknown"] = True
        with self.assertRaises(ValueError):
            validate_source_policy(mutated)

        self.assertNotIn("scripts/tests/fixtures/", canonical_bytes(self.policy).decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
