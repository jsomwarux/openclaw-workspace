import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.linkedin_content_os.canonical import canonical_bytes, read_jsonl, sha256_hex
from scripts.linkedin_content_os.fixtures import (
    DECAGON_PACKET_PATH,
    DECAGON_PAYLOAD_HASH,
    PRE_GATE_BLOB_ID,
    PRE_GATE_COMMIT,
    PRE_GATE_PATH,
    build_evaluation_fixtures,
    extract_git_object,
    select_build_proof,
)


ROOT = Path(__file__).resolve().parents[2]
GENERATED_AT = "2026-09-28T16:00:00Z"


def _git_blob_id(payload: bytes) -> str:
    header = "blob {}\0".format(len(payload)).encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def _provenance(
    proof_id: str,
    payload: bytes,
    *,
    path: str = "evidence/proof.json",
    permission: object = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "proofId": proof_id,
        "repository": "jt-ops",
        "commit": "1" * 40,
        "path": path,
        "gitObjectId": _git_blob_id(payload),
        "contentSha256": sha256_hex(payload),
    }
    if permission is not None:
        result["permissionEvidenceRef"] = "/permission"
        result["permissionEvidenceSha256"] = sha256_hex(
            canonical_bytes(permission)
        )
    return result


def _proof(
    proof_id: str = "proof-alpha",
    *,
    permission_status: str = "approved-anonymized",
    expires_at: str = "2026-12-31T23:59:59Z",
    active_prospect: bool = False,
    active_employer: bool = False,
    protected: bool = False,
    facts: object = None,
    verified_at: str = "2026-09-20T12:00:00Z",
) -> tuple[dict[str, object], bytes, dict[str, object]]:
    document: dict[str, object] = {
        "schemaVersion": "permissioned-proof.v1",
        "proofId": proof_id,
        "verifiedAt": verified_at,
        "facts": facts
        if facts is not None
        else [
            {
                "factId": "fact-1",
                "conceptId": "exception-routing",
                "outboundText": "A bounded workflow routes exceptions into a daily digest.",
            }
        ],
        "permission": {
            "status": permission_status,
            "evidenceRef": "/permission",
            "expiresAt": expires_at,
        },
        "activeProspectConflict": active_prospect,
        "activeEmployerConflict": active_employer,
        "protectedInternalPremise": protected,
    }
    payload = canonical_bytes(document)
    return document, payload, _provenance(
        proof_id, payload, permission=document["permission"]
    )


class GitExtractionTests(unittest.TestCase):
    def test_extracts_only_the_exact_read_only_git_object(self) -> None:
        payload = b'{"proof":"exact"}\n'
        runner = Mock(
            return_value=subprocess.CompletedProcess([], 0, stdout=payload, stderr=b"")
        )
        git_dir = Path("/tmp/jt-ops.git")

        extracted = extract_git_object(
            git_dir,
            PRE_GATE_COMMIT,
            PRE_GATE_PATH,
            _git_blob_id(payload),
            runner=runner,
        )

        self.assertEqual(extracted, payload)
        runner.assert_called_once_with(
            [
                "git",
                "--git-dir",
                str(git_dir),
                "show",
                "{}:{}".format(PRE_GATE_COMMIT, PRE_GATE_PATH),
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertNotIn("shell", runner.call_args.kwargs)
        self.assertNotIn("env", runner.call_args.kwargs)

    def test_rejects_non_exact_git_inputs_and_blob_mismatch(self) -> None:
        runner = Mock()
        with self.assertRaisesRegex(ValueError, "commit"):
            extract_git_object(Path("/tmp/repo.git"), "HEAD", "a.json", "a" * 40, runner=runner)
        with self.assertRaisesRegex(ValueError, "repository-relative"):
            extract_git_object(Path("/tmp/repo.git"), "1" * 40, "../a.json", "a" * 40, runner=runner)
        payload = b"not-the-bound-object"
        runner.return_value = subprocess.CompletedProcess([], 0, stdout=payload, stderr=b"")
        with self.assertRaisesRegex(ValueError, "Git object ID"):
            extract_git_object(Path("/tmp/repo.git"), "1" * 40, "a.json", "a" * 40, runner=runner)


class SelectionTests(unittest.TestCase):
    def test_selects_permissioned_claim_bound_non_expired_proof(self) -> None:
        document, payload, provenance = _proof()
        result = select_build_proof(
            [(document, payload, provenance)], generated_at=GENERATED_AT
        )
        self.assertEqual(result["classification"], "positive")
        self.assertEqual(result["permissionState"], "approved-anonymized")
        self.assertEqual(result["expectedGateResult"], "accept")
        self.assertNotIn("postCopy", result)
        self.assertNotIn("image", result)

    def test_ranks_permission_then_specificity_then_freshness_then_id(self) -> None:
        approved_vague = _proof(
            "z-vague", facts=[{"factId": "f", "conceptId": "c", "outboundText": "Built it."}]
        )
        approved_specific_old = _proof("b-specific", verified_at="2026-09-10T12:00:00Z")
        approved_specific_new_b = _proof("b-new", verified_at="2026-09-21T12:00:00Z")
        approved_specific_new_a = _proof("a-new", verified_at="2026-09-21T12:00:00Z")
        missing_new = _proof("missing", verified_at="2026-09-27T12:00:00Z")
        missing_doc = missing_new[0]
        missing_doc["permission"] = None
        missing_payload = canonical_bytes(missing_doc)
        missing = (missing_doc, missing_payload, _provenance("missing", missing_payload))

        result = select_build_proof(
            [missing, approved_vague, approved_specific_old, approved_specific_new_b, approved_specific_new_a],
            generated_at=GENERATED_AT,
        )
        self.assertEqual(result["fixtureId"], "a-new")

    def test_missing_permission_is_an_explicit_gap(self) -> None:
        document, _, _ = _proof("missing")
        document["permission"] = None
        payload = canonical_bytes(document)
        provenance = _provenance("missing", payload)
        result = select_build_proof([(document, payload, provenance)], generated_at=GENERATED_AT)
        self.assertEqual(result["classification"], "gap")
        self.assertEqual(result["permissionState"], "missing")
        self.assertEqual(result["failureReason"], "permission_missing")

    def test_rejects_every_fail_closed_disqualifier(self) -> None:
        cases = [
            (dict(permission_status="internal-only"), "permission_internal_only"),
            (dict(expires_at="2026-09-01T00:00:00Z"), "permission_expired"),
            (dict(facts=[]), "claim_bindings_missing"),
            (dict(active_prospect=True), "active_prospect_conflict"),
            (dict(active_employer=True), "active_employer_conflict"),
            (dict(protected=True), "protected_internal_premise"),
        ]
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                document, payload, provenance = _proof(reason, **overrides)
                result = select_build_proof(
                    [(document, payload, provenance)], generated_at=GENERATED_AT
                )
                self.assertEqual(result["classification"], "gap")
                self.assertEqual(result["failureReason"], reason)
                self.assertNotEqual(result["expectedGateResult"], "accept")

    def test_rejected_candidate_cannot_eclipse_valid_candidate(self) -> None:
        rejected = _proof(
            "a-rejected",
            protected=True,
            facts=[
                {
                    "factId": "f",
                    "conceptId": "c",
                    "outboundText": "Extremely specific protected evidence with many words must never outrank admissible proof.",
                }
            ],
            verified_at="2026-09-27T12:00:00Z",
        )
        valid = _proof("z-valid", verified_at="2026-09-10T12:00:00Z")
        result = select_build_proof(
            [rejected, valid], generated_at=GENERATED_AT
        )
        self.assertEqual(result["classification"], "positive")
        self.assertEqual(result["fixtureId"], "z-valid")

    def test_rejects_test_fixture_path_as_authority(self) -> None:
        document, payload, provenance = _proof()
        provenance["path"] = "scripts/tests/fixtures/linkedin_content_os/proof.json"
        with self.assertRaisesRegex(ValueError, "test fixture"):
            select_build_proof([(document, payload, provenance)], generated_at=GENERATED_AT)

    def test_rejects_mismatched_exact_bytes_and_source_hashes(self) -> None:
        document, payload, provenance = _proof()
        provenance["contentSha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "content SHA-256"):
            select_build_proof([(document, payload, provenance)], generated_at=GENERATED_AT)

    def test_rejects_mismatched_permission_evidence_digest(self) -> None:
        document, _, _ = _proof()
        payload = canonical_bytes(document)
        provenance = _provenance(
            "proof-alpha", payload, permission=document["permission"]
        )
        provenance["permissionEvidenceSha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "permission evidence SHA-256"):
            select_build_proof([(document, payload, provenance)], generated_at=GENERATED_AT)


class FixtureBuildTests(unittest.TestCase):
    def test_test_proof_records_are_strict_input_data_not_authority(self) -> None:
        fixture_path = (
            ROOT
            / "scripts/tests/fixtures/linkedin_content_os/proof-records.jsonl"
        )
        rows = read_jsonl(fixture_path)
        self.assertEqual([row["proofId"] for row in rows], [
            "approved-specific", "approved-vague", "missing-permission"
        ])
        self.assertTrue(
            str(fixture_path.relative_to(ROOT)).startswith("scripts/tests/fixtures/")
        )

    def test_builds_exact_negative_current_gap_and_missing_mode_gaps(self) -> None:
        pre_gate = b'{"schema_version":"proof-asset-card-v1","card_id":"cohort-two-coi-proof-v1","status":"verified","verified_by":"jt","verified_at":"2026-09-16T00:00:00Z","system_revision":"revision","facts":[{"fact_id":"proof-coi-reminder-routing","concept_id":"coi-reminder-routing","sentence_id":"coi-reminder-routing-v1","outbound_text":"A workflow routes reminders.","claim_values":[]}]}\n'
        runner = Mock(
            return_value=subprocess.CompletedProcess([], 0, stdout=pre_gate, stderr=b"")
        )
        with tempfile.TemporaryDirectory() as directory:
            git_dir = Path(directory) / "jt-ops.git"
            git_dir.mkdir()
            with patch(
                "scripts.linkedin_content_os.fixtures.PRE_GATE_BLOB_ID",
                _git_blob_id(pre_gate),
            ), patch(
                "scripts.linkedin_content_os.fixtures.PRE_GATE_CONTENT_SHA256",
                sha256_hex(pre_gate),
            ):
                records = build_evaluation_fixtures(
                    ROOT, git_dir, generated_at=GENERATED_AT, runner=runner
                )

        self.assertEqual(
            [(record["mode"], record["classification"]) for record in records],
            [
                ("internal_machinery", "negative"),
                ("build_proof", "gap"),
                ("company_teardown", "gap"),
                ("ai_news", "gap"),
            ],
        )
        negative = records[0]
        self.assertEqual(negative["payloadHash"], DECAGON_PAYLOAD_HASH)
        self.assertEqual(negative["sourceRefs"][0]["path"], DECAGON_PACKET_PATH)
        self.assertEqual(negative["failureReason"], "protected_internal_premise")
        current = records[1]
        self.assertEqual(current["failureReason"], "permission_missing")
        self.assertEqual(current["sourceRefs"][0]["contentSha256"], sha256_hex(pre_gate))
        self.assertEqual(current["sourceRefs"][0]["gitObjectId"], _git_blob_id(pre_gate))
        self.assertEqual(records[2]["failureReason"], "evidence_missing")
        self.assertEqual(records[3]["failureReason"], "evidence_missing")
        self.assertTrue(all("postCopy" not in record for record in records))
        self.assertTrue(all("image" not in record for record in records))

    def test_real_decagon_packet_matches_bound_payload_and_bytes(self) -> None:
        packet = json.loads((ROOT / DECAGON_PACKET_PATH).read_text())
        self.assertEqual(packet["payloadHash"], DECAGON_PAYLOAD_HASH)
        self.assertEqual(
            sha256_hex((ROOT / DECAGON_PACKET_PATH).read_bytes()),
            "48448f87b3f5d8dec47bb2ee8113a3c58b5fa63bbfc6883f86c18f4ecdff516d",
        )


if __name__ == "__main__":
    unittest.main()
