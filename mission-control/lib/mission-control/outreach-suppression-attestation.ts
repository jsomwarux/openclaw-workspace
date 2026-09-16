import { createHmac, timingSafeEqual } from "node:crypto";
import { canonicalJson } from "./canonical-json";
import type { OutreachReviewSubmission } from "./outreach-review";

const DOMAIN = "mission-control/outreach-suppression-admission-v1\0";
const DIGEST = /^[a-f0-9]{64}$/;

function key(secret: string | undefined): string {
  if (!secret?.trim()) throw new Error("suppression admission attestation unavailable");
  return secret;
}

function immutableRequest(submission: OutreachReviewSubmission): OutreachReviewSubmission {
  return {
    candidateId: submission.candidateId,
    cohortId: submission.cohortId,
    draftSha256: submission.draftSha256,
    subject: submission.subject,
    body: submission.body,
    verifierReport: submission.verifierReport,
    reviewAuthorityId: submission.reviewAuthorityId,
    verifierActorId: submission.verifierActorId,
    gitBindings: submission.gitBindings,
    ...(submission.suppressionBinding ? { suppressionBinding: submission.suppressionBinding } : {}),
  };
}

export async function createSuppressionAdmissionAttestation(
  submission: OutreachReviewSubmission,
  decisionCapability: string | undefined,
): Promise<string> {
  return createHmac("sha256", key(decisionCapability))
    .update(DOMAIN)
    .update(canonicalJson(immutableRequest(submission)))
    .digest("hex");
}

export async function verifySuppressionAdmissionAttestation(
  submission: OutreachReviewSubmission,
  attestation: unknown,
  decisionCapability: string | undefined,
): Promise<boolean> {
  if (typeof attestation !== "string" || !DIGEST.test(attestation) || !decisionCapability?.trim()) return false;
  const expected = await createSuppressionAdmissionAttestation(submission, decisionCapability);
  return timingSafeEqual(Buffer.from(attestation, "hex"), Buffer.from(expected, "hex"));
}
