import { canonicalJson, hashCanonicalJson, type GitBinding } from "./outreach-review";

export type OutreachReviewAuthoritySubmission = {
  candidateId: string;
  draftSha256: string;
  authorityBundleHash: string;
  verifierReportSha256: string;
  verifierGitBinding: GitBinding;
  builderActorId: string;
  drafterActorId: string;
};

export type OutreachReviewAuthority = OutreachReviewAuthoritySubmission & {
  verifierActorId: string;
  reviewId: string;
  observedAt: number;
  authorityRevision: string;
};

export type OutreachReviewAuthorityLookup = Pick<
  OutreachReviewAuthoritySubmission,
  "candidateId" | "draftSha256" | "authorityBundleHash" | "verifierReportSha256" | "verifierGitBinding"
>;

export type OutreachReviewAuthorityErrorCode = "invalid_request" | "conflict" | "corrupt_authority";

export class OutreachReviewAuthorityError extends Error {
  constructor(readonly code: OutreachReviewAuthorityErrorCode) {
    super(code);
  }
}

const REPOSITORY_PATTERN = /^[a-z0-9][a-z0-9._-]{0,63}\/[a-z0-9][a-z0-9._-]{0,99}$/;
const COMMIT_PATTERN = /^[a-f0-9]{40}$/;
const SHA256_PATTERN = /^[a-f0-9]{64}$/;
const ENTROPY_PATTERN = /^[a-f0-9]{40}$/;
const REVIEW_ID_PATTERN = /^review_[a-f0-9]{20}$/;
const REVISION_PATTERN = /^review_authority_[a-f0-9]{20}$/;
const GIT_BINDING_FIELDS = ["repository", "commitSha", "path", "blobSha256"] as const;
const SUBMISSION_FIELDS = [
  "candidateId", "draftSha256", "authorityBundleHash", "verifierReportSha256",
  "verifierGitBinding", "builderActorId", "drafterActorId",
] as const;
const LOOKUP_FIELDS = [
  "candidateId", "draftSha256", "authorityBundleHash", "verifierReportSha256", "verifierGitBinding",
] as const;
const AUTHORITY_FIELDS = [...SUBMISSION_FIELDS, "verifierActorId", "reviewId", "observedAt", "authorityRevision"] as const;

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function hasExactKeys(value: Record<string, unknown>, expected: readonly string[]): boolean {
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  return actual.length === wanted.length && actual.every((key, index) => key === wanted[index]);
}

function hasLoneSurrogate(value: string): boolean {
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) return true;
      index += 1;
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      return true;
    }
  }
  return false;
}

function requireId(value: unknown): asserts value is string {
  if (
    typeof value !== "string" || value.trim() === "" || value.length > 128
    || hasLoneSurrogate(value) || /[\u0000-\u001f\u007f-\u009f]/.test(value)
  ) {
    throw new OutreachReviewAuthorityError("invalid_request");
  }
}

function requireDigest(value: unknown): asserts value is string {
  if (typeof value !== "string" || !SHA256_PATTERN.test(value)) throw new OutreachReviewAuthorityError("invalid_request");
}

function validateGitPath(value: unknown): asserts value is string {
  if (
    typeof value !== "string" || value.length === 0 || value.length > 512
    || !/^[A-Za-z0-9._/-]+$/.test(value) || value.startsWith("/") || value.includes("\\") || value.includes("\0")
  ) throw new OutreachReviewAuthorityError("invalid_request");
  if (value.split("/").some((segment) => segment === "" || segment === "." || segment === "..")) {
    throw new OutreachReviewAuthorityError("invalid_request");
  }
}

function validateGitBinding(value: unknown, expectedBlobSha256: string): asserts value is GitBinding {
  if (!isRecord(value) || !hasExactKeys(value, GIT_BINDING_FIELDS)) throw new OutreachReviewAuthorityError("invalid_request");
  if (typeof value.repository !== "string" || !REPOSITORY_PATTERN.test(value.repository)) {
    throw new OutreachReviewAuthorityError("invalid_request");
  }
  if (typeof value.commitSha !== "string" || !COMMIT_PATTERN.test(value.commitSha)) {
    throw new OutreachReviewAuthorityError("invalid_request");
  }
  requireDigest(value.blobSha256);
  if (value.blobSha256 !== expectedBlobSha256) throw new OutreachReviewAuthorityError("invalid_request");
  validateGitPath(value.path);
}

function validateLookupFields(value: Record<string, unknown>): void {
  requireId(value.candidateId);
  requireDigest(value.draftSha256);
  requireDigest(value.authorityBundleHash);
  requireDigest(value.verifierReportSha256);
  validateGitBinding(value.verifierGitBinding, value.verifierReportSha256);
}

export function validateOutreachReviewAuthoritySubmission(
  value: unknown,
): asserts value is OutreachReviewAuthoritySubmission {
  if (!isRecord(value) || !hasExactKeys(value, SUBMISSION_FIELDS)) throw new OutreachReviewAuthorityError("invalid_request");
  validateLookupFields(value);
  requireId(value.builderActorId);
  requireId(value.drafterActorId);
  if (value.builderActorId === value.drafterActorId) throw new OutreachReviewAuthorityError("invalid_request");
}

export function validateOutreachReviewAuthorityLookup(value: unknown): asserts value is OutreachReviewAuthorityLookup {
  if (!isRecord(value) || !hasExactKeys(value, LOOKUP_FIELDS)) throw new OutreachReviewAuthorityError("invalid_request");
  validateLookupFields(value);
}

export async function hashOutreachReviewAuthoritySubmission(
  input: OutreachReviewAuthoritySubmission,
): Promise<string> {
  validateOutreachReviewAuthoritySubmission(input);
  return hashCanonicalJson({
    domain: "mission-control/outreach-review-authority-submission",
    version: 1,
    submission: input,
  });
}

function submissionFromAuthority(authority: OutreachReviewAuthority): OutreachReviewAuthoritySubmission {
  return {
    candidateId: authority.candidateId,
    draftSha256: authority.draftSha256,
    authorityBundleHash: authority.authorityBundleHash,
    verifierReportSha256: authority.verifierReportSha256,
    verifierGitBinding: { ...authority.verifierGitBinding },
    builderActorId: authority.builderActorId,
    drafterActorId: authority.drafterActorId,
  };
}

function detachedAuthority(authority: OutreachReviewAuthority): OutreachReviewAuthority {
  return {
    ...authority,
    verifierGitBinding: { ...authority.verifierGitBinding },
  };
}

function sameTuple(left: OutreachReviewAuthorityLookup, right: OutreachReviewAuthorityLookup): boolean {
  return left.candidateId === right.candidateId
    && left.draftSha256 === right.draftSha256
    && left.authorityBundleHash === right.authorityBundleHash
    && left.verifierReportSha256 === right.verifierReportSha256;
}

function sameKey(left: OutreachReviewAuthorityLookup, right: OutreachReviewAuthorityLookup): boolean {
  return sameTuple(left, right)
    && canonicalJson(left.verifierGitBinding) === canonicalJson(right.verifierGitBinding);
}

async function validateStoredAuthority(value: unknown): Promise<OutreachReviewAuthority> {
  try {
    if (!isRecord(value) || !hasExactKeys(value, AUTHORITY_FIELDS)) throw new Error("shape");
    const authority = value as OutreachReviewAuthority;
    const submission = submissionFromAuthority(authority);
    validateOutreachReviewAuthoritySubmission(submission);
    requireId(authority.verifierActorId);
    if (
      authority.verifierActorId === authority.builderActorId
      || authority.verifierActorId === authority.drafterActorId
      || !REVIEW_ID_PATTERN.test(authority.reviewId)
      || !Number.isSafeInteger(authority.observedAt)
      || authority.observedAt < 0
      || !REVISION_PATTERN.test(authority.authorityRevision)
    ) throw new Error("invalid authority");
    return authority;
  } catch {
    throw new OutreachReviewAuthorityError("corrupt_authority");
  }
}

async function validateAuthorityRows(
  rows: readonly OutreachReviewAuthority[],
  expectedKey: OutreachReviewAuthorityLookup,
): Promise<OutreachReviewAuthority | null> {
  const authorities = await Promise.all(rows.map(validateStoredAuthority));
  if (authorities.some((authority) => !sameTuple(authority, expectedKey))) {
    throw new OutreachReviewAuthorityError("corrupt_authority");
  }
  const exact = authorities.filter((authority) => sameKey(authority, expectedKey));
  if (exact.length > 1) throw new OutreachReviewAuthorityError("corrupt_authority");
  return exact[0] ?? null;
}

export async function resolveOutreachReviewAuthorityAdmission(
  rows: readonly OutreachReviewAuthority[],
  input: OutreachReviewAuthoritySubmission,
  verifierActorId: string,
  observedAt: number,
  serverEntropy: string,
) {
  validateOutreachReviewAuthoritySubmission(input);
  requireId(verifierActorId);
  if (verifierActorId === input.builderActorId || verifierActorId === input.drafterActorId) {
    throw new OutreachReviewAuthorityError("invalid_request");
  }
  const existing = await validateAuthorityRows(rows, input);
  if (existing) {
    const [existingSubmissionSha256, incomingSubmissionSha256] = await Promise.all([
      hashOutreachReviewAuthoritySubmission(submissionFromAuthority(existing)),
      hashOutreachReviewAuthoritySubmission(input),
    ]);
    if (existingSubmissionSha256 === incomingSubmissionSha256 && existing.verifierActorId === verifierActorId) {
      return { operation: "existing" as const, authority: detachedAuthority(existing) };
    }
    throw new OutreachReviewAuthorityError("conflict");
  }
  if (!Number.isSafeInteger(observedAt) || observedAt < 0 || !ENTROPY_PATTERN.test(serverEntropy)) {
    throw new OutreachReviewAuthorityError("invalid_request");
  }
  return {
    operation: "create" as const,
    authority: {
      ...input,
      verifierGitBinding: { ...input.verifierGitBinding },
      verifierActorId,
      reviewId: `review_${serverEntropy.slice(0, 20)}`,
      observedAt,
      authorityRevision: `review_authority_${serverEntropy.slice(20)}`,
    },
  };
}

export async function resolveOutreachReviewAuthorityLookup(
  rows: readonly OutreachReviewAuthority[],
  lookup: OutreachReviewAuthorityLookup,
): Promise<OutreachReviewAuthority | null> {
  validateOutreachReviewAuthorityLookup(lookup);
  const authority = await validateAuthorityRows(rows, lookup);
  if (!authority) return null;
  return detachedAuthority(authority);
}
