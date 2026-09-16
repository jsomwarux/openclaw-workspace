import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import type { OutreachReviewSubmission } from "./outreach-review";
import {
  createSuppressionAdmissionAttestation,
  verifySuppressionAdmissionAttestation,
} from "./outreach-suppression-attestation";

const binding = {
  schemaVersion: "outreach-suppression-binding-v1" as const,
  repository: "jsomwarux/jt-ops", commitSha: "a".repeat(40), gatePath: "gate.json",
  gateBlobOid: "b".repeat(40), gateBlobSha256: "c".repeat(64), gateArtifactHash: "d".repeat(64),
  admissionCommitSha: "e".repeat(40), admissionPath: "admission.json",
  admissionBlobOid: "f".repeat(40), admissionBlobSha256: "1".repeat(64),
  channelAttestationId: `channel_${"2".repeat(20)}`, channelOwnerRevision: "3".repeat(64),
  prospectId: "candidate-1", organizationFactId: "fact-org", channelFingerprint: "4".repeat(64),
  bindingHash: "5".repeat(64),
};
const bind = (path: string) => ({ repository: "jsomwarux/jt-ops", commitSha: "a".repeat(40), path, blobSha256: "c".repeat(64) });
const submission: OutreachReviewSubmission = {
  candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: "6".repeat(64),
  subject: "Subject", body: "Exact body", verifierReport: "VERDICT: CONFIRM",
  reviewAuthorityId: `review_${"7".repeat(20)}`, verifierActorId: "verifier-1",
  gitBindings: { evidence: bind("evidence.json"), policy: bind("policy.json"), gate: bind("gate.json"), draft: bind("draft.json"), verifier: bind("verify.json") },
  suppressionBinding: binding,
};

describe("server-only suppression admission attestation", () => {
  test("uses runtime-portable Web Crypto because Convex imports this module", () => {
    const source = readFileSync("lib/mission-control/outreach-suppression-attestation.ts", "utf8");
    expect(source).not.toContain("node:crypto");
    expect(source).not.toContain("Buffer.from");
    expect(source).toContain("crypto.subtle.sign");
    expect(source).toContain("crypto.subtle.verify");
  });
  test("binds the entire immutable review request under a domain-separated HMAC", async () => {
    const attestation = await createSuppressionAdmissionAttestation(submission, "decision-secret");
    expect(/^[a-f0-9]{64}$/.test(attestation)).toBe(true);
    expect(await verifySuppressionAdmissionAttestation(submission, attestation, "decision-secret")).toBe(true);
    expect(await verifySuppressionAdmissionAttestation({ ...submission, subject: "Changed" }, attestation, "decision-secret")).toBe(false);
    expect(await verifySuppressionAdmissionAttestation(submission, attestation, "different-secret")).toBe(false);
  });

  test("rejects missing secrets and malformed attestations without echoing them", async () => {
    let message = "";
    try { await createSuppressionAdmissionAttestation(submission, " "); }
    catch (error) { message = String(error); }
    expect(message).toBe("Error: suppression admission attestation unavailable");
    expect(await verifySuppressionAdmissionAttestation(submission, "not-a-digest", "decision-secret")).toBe(false);
  });
});
