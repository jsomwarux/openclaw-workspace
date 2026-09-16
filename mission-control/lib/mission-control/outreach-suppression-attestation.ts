import { canonicalJson } from "./canonical-json";
import type { OutreachReviewSubmission } from "./outreach-review";

const DOMAIN = "mission-control/outreach-suppression-admission-v1\0";
const DIGEST = /^[a-f0-9]{64}$/;

function key(secret: string | undefined): string {
  if (!secret?.trim()) throw new Error("suppression admission attestation unavailable");
  return secret;
}

const algorithm = { name: "HMAC", hash: "SHA-256" } as const;
const encoder = new TextEncoder();

function hex(bytes: ArrayBuffer): string {
  return Array.from(new Uint8Array(bytes), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function bytes(value: string): ArrayBuffer {
  const decoded = new Uint8Array(value.length / 2);
  for (let index = 0; index < decoded.length; index++) {
    decoded[index] = Number.parseInt(value.slice(index * 2, index * 2 + 2), 16);
  }
  return decoded.buffer;
}

async function hmacKey(secret: string, usage: "sign" | "verify") {
  return crypto.subtle.importKey("raw", encoder.encode(secret), algorithm, false, [usage]);
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
  const secret = key(decisionCapability);
  const material = encoder.encode(`${DOMAIN}${canonicalJson(immutableRequest(submission))}`);
  return hex(await crypto.subtle.sign("HMAC", await hmacKey(secret, "sign"), material));
}

export async function verifySuppressionAdmissionAttestation(
  submission: OutreachReviewSubmission,
  attestation: unknown,
  decisionCapability: string | undefined,
): Promise<boolean> {
  if (typeof attestation !== "string" || !DIGEST.test(attestation) || !decisionCapability?.trim()) return false;
  const material = encoder.encode(`${DOMAIN}${canonicalJson(immutableRequest(submission))}`);
  return crypto.subtle.verify(
    "HMAC",
    await hmacKey(decisionCapability, "verify"),
    bytes(attestation),
    material,
  );
}
