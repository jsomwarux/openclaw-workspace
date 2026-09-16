import type { OutreachDecision } from "./outreach-decision";
import { validateSuppressionBinding, validateSuppressionBindingHash, type SuppressionBinding } from "./outreach-suppression-binding";
import { canonicalJson, hashCanonicalJson } from "./canonical-json";
export { canonicalJson, hashCanonicalJson } from "./canonical-json";

export type GitBinding = {
  repository: string;
  commitSha: string;
  path: string;
  blobSha256: string;
};

export type OutreachGitBindings = {
  evidence: GitBinding;
  policy: GitBinding;
  gate: GitBinding;
  draft: GitBinding;
  verifier: GitBinding;
};

export type OutreachReviewSubmission = {
  candidateId: string;
  cohortId: string;
  draftSha256: string;
  subject: string;
  body: string;
  verifierReport: string;
  reviewAuthorityId: string;
  verifierActorId: string;
  gitBindings: OutreachGitBindings;
  suppressionBinding?: SuppressionBinding;
};

export type OutreachReviewSnapshot = OutreachReviewSubmission & {
  snapshotSha256: string;
  reviewCycle: 1 | 2;
  admittedBy: "server";
  admittedAt: number;
};

export type StoredOutreachReviewTask = {
  _id?: string;
  id?: string;
  candidateId?: string;
  cohortId?: string;
  draftSha256?: string;
  status?: string;
  outreachReview?: OutreachReviewSnapshot;
  outreachDecision?: OutreachDecision;
};

export type OutreachReviewErrorCode = "invalid_request" | "too_large" | "cycle_limit" | "corrupt_authority";

export class OutreachReviewContractError extends Error {
  constructor(readonly code: OutreachReviewErrorCode) {
    super(code);
  }
}

const ID_PATTERN = /^[a-z0-9][a-z0-9._:-]{0,127}$/;
const REPOSITORY_PATTERN = /^[a-z0-9][a-z0-9._-]{0,63}\/[a-z0-9][a-z0-9._-]{0,99}$/;
const COMMIT_PATTERN = /^[a-f0-9]{40}$/;
const SHA256_PATTERN = /^[a-f0-9]{64}$/;
const BINDING_NAMES = ["evidence", "policy", "gate", "draft", "verifier"] as const;
const SUBMISSION_FIELDS = [
  "candidateId", "cohortId", "draftSha256", "subject", "body", "verifierReport",
  "reviewAuthorityId", "verifierActorId", "gitBindings",
] as const;
const SUBMISSION_FIELDS_WITH_SUPPRESSION = [...SUBMISSION_FIELDS, "suppressionBinding"] as const;

export function validateOutreachReviewKey(candidateId: unknown, cohortId: unknown): asserts candidateId is string {
  if (typeof candidateId !== "string" || !ID_PATTERN.test(candidateId) || typeof cohortId !== "string" || !ID_PATTERN.test(cohortId)) {
    throw new OutreachReviewContractError("invalid_request");
  }
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

function requireString(value: unknown, max: number, sizeSensitive = false): asserts value is string {
  if (typeof value !== "string" || value.length === 0 || hasLoneSurrogate(value)) {
    throw new OutreachReviewContractError("invalid_request");
  }
  if (value.length > max) {
    throw new OutreachReviewContractError(sizeSensitive ? "too_large" : "invalid_request");
  }
}

function validateGitPath(path: unknown): asserts path is string {
  requireString(path, 512);
  if (!/^[A-Za-z0-9._/-]+$/.test(path) || path.startsWith("/") || path.includes("\\") || path.includes("\0")) {
    throw new OutreachReviewContractError("invalid_request");
  }
  const segments = path.split("/");
  if (segments.some((segment) => segment === "" || segment === "." || segment === "..")) {
    throw new OutreachReviewContractError("invalid_request");
  }
}

function exactKeys(value: Record<string, unknown>, expected: readonly string[]): boolean {
  const actual = Object.keys(value).sort();
  return actual.length === expected.length && actual.every((key, index) => key === [...expected].sort()[index]);
}

export function validateOutreachReviewSubmission(value: unknown): asserts value is OutreachReviewSubmission {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new OutreachReviewContractError("invalid_request");
  const input = value as Record<string, unknown>;
  if (!exactKeys(input, SUBMISSION_FIELDS) && !exactKeys(input, SUBMISSION_FIELDS_WITH_SUPPRESSION)) throw new OutreachReviewContractError("invalid_request");
  validateOutreachReviewKey(input.candidateId, input.cohortId);
  for (const field of ["reviewAuthorityId", "verifierActorId"] as const) {
    if (typeof input[field] !== "string" || !ID_PATTERN.test(input[field])) throw new OutreachReviewContractError("invalid_request");
  }
  if (typeof input.draftSha256 !== "string" || !SHA256_PATTERN.test(input.draftSha256)) {
    throw new OutreachReviewContractError("invalid_request");
  }
  requireString(input.subject, 200, true);
  requireString(input.body, 20_000, true);
  requireString(input.verifierReport, 20_000, true);
  if (!input.gitBindings || typeof input.gitBindings !== "object" || Array.isArray(input.gitBindings)) {
    throw new OutreachReviewContractError("invalid_request");
  }
  const bindings = input.gitBindings as Record<string, unknown>;
  if (!exactKeys(bindings, BINDING_NAMES)) throw new OutreachReviewContractError("invalid_request");
  for (const name of BINDING_NAMES) {
    const binding = bindings[name];
    if (!binding || typeof binding !== "object" || Array.isArray(binding)) throw new OutreachReviewContractError("invalid_request");
    const record = binding as Record<string, unknown>;
    if (!exactKeys(record, ["repository", "commitSha", "path", "blobSha256"])) throw new OutreachReviewContractError("invalid_request");
    if (typeof record.repository !== "string" || !REPOSITORY_PATTERN.test(record.repository)) throw new OutreachReviewContractError("invalid_request");
    if (typeof record.commitSha !== "string" || !COMMIT_PATTERN.test(record.commitSha)) throw new OutreachReviewContractError("invalid_request");
    if (typeof record.blobSha256 !== "string" || !SHA256_PATTERN.test(record.blobSha256)) throw new OutreachReviewContractError("invalid_request");
    validateGitPath(record.path);
  }
  if (input.suppressionBinding !== undefined) {
    try {
      validateSuppressionBinding(input.suppressionBinding, bindings.gate as GitBinding);
      if (input.suppressionBinding.prospectId !== input.candidateId || !/^review_[a-f0-9]{20}$/.test(String(input.reviewAuthorityId))) throw new Error("binding identity mismatch");
    }
    catch { throw new OutreachReviewContractError("invalid_request"); }
  }
}

export async function hashOutreachReviewSubmission(input: OutreachReviewSubmission): Promise<string> {
  validateOutreachReviewSubmission(input);
  if (input.suppressionBinding) {
    try { await validateSuppressionBindingHash(input.suppressionBinding, input.gitBindings.gate); }
    catch { throw new OutreachReviewContractError("invalid_request"); }
  }
  try { return await hashCanonicalJson({ domain: "mission-control/outreach-review-snapshot", version: 1, snapshot: input }); }
  catch { throw new OutreachReviewContractError("invalid_request"); }
}

function snapshotSubmission(snapshot: OutreachReviewSnapshot): OutreachReviewSubmission {
  return {
    candidateId: snapshot.candidateId,
    cohortId: snapshot.cohortId,
    draftSha256: snapshot.draftSha256,
    subject: snapshot.subject,
    body: snapshot.body,
    verifierReport: snapshot.verifierReport,
    reviewAuthorityId: snapshot.reviewAuthorityId,
    verifierActorId: snapshot.verifierActorId,
    gitBindings: snapshot.gitBindings,
    ...(snapshot.suppressionBinding ? { suppressionBinding: snapshot.suppressionBinding } : {}),
  };
}

export async function summarizeOutreachReviews(
  tasks: StoredOutreachReviewTask[], candidateId: string, cohortId: string,
) {
  validateOutreachReviewKey(candidateId, cohortId);
  const authoritative = tasks.filter((task) => task.outreachReview !== undefined);
  const validated: Array<StoredOutreachReviewTask & { outreachReview: OutreachReviewSnapshot }> = [];
  for (const task of authoritative) {
    const snapshot = task.outreachReview!;
    try {
      validateOutreachReviewSubmission(snapshotSubmission(snapshot));
      if (
        task.candidateId !== candidateId || task.cohortId !== cohortId
        || task.draftSha256 !== snapshot.draftSha256
        || snapshot.candidateId !== candidateId || snapshot.cohortId !== cohortId
        || snapshot.admittedBy !== "server"
        || (snapshot.reviewCycle !== 1 && snapshot.reviewCycle !== 2)
        || !Number.isFinite(snapshot.admittedAt)
        || !SHA256_PATTERN.test(snapshot.snapshotSha256)
        || await hashOutreachReviewSubmission(snapshotSubmission(snapshot)) !== snapshot.snapshotSha256
      ) throw new Error("invalid snapshot");
    } catch {
      throw new OutreachReviewContractError("corrupt_authority");
    }
    validated.push(task as StoredOutreachReviewTask & { outreachReview: OutreachReviewSnapshot });
  }
  const hashes = new Set(validated.map((task) => task.outreachReview.snapshotSha256));
  const cycles = new Set(validated.map((task) => task.outreachReview.reviewCycle));
  if (
    validated.length > 2 || hashes.size !== validated.length || cycles.size !== validated.length
    || validated.some((task, index) => [...validated].sort((a, b) => a.outreachReview.reviewCycle - b.outreachReview.reviewCycle)[index].outreachReview.reviewCycle !== index + 1)
  ) throw new OutreachReviewContractError("corrupt_authority");
  const ordered = [...validated].sort((a, b) => a.outreachReview.reviewCycle - b.outreachReview.reviewCycle);
  const latestTask = ordered.at(-1);
  return {
    candidateId,
    cohortId,
    reviewCount: ordered.length,
    remainingCycles: 2 - ordered.length,
    latest: latestTask ? {
      taskId: latestTask._id ?? latestTask.id ?? "",
      draftSha256: latestTask.outreachReview.draftSha256,
      snapshotSha256: latestTask.outreachReview.snapshotSha256,
      reviewCycle: latestTask.outreachReview.reviewCycle,
      decided: Boolean(latestTask.outreachDecision),
    } : null,
    tasks: ordered,
  };
}

export async function resolveOutreachReviewAdmission(
  existing: StoredOutreachReviewTask[], input: OutreachReviewSubmission, now: number,
) {
  validateOutreachReviewSubmission(input);
  const snapshotSha256 = await hashOutreachReviewSubmission(input);
  const summary = await summarizeOutreachReviews(existing, input.candidateId, input.cohortId);
  const exact = summary.tasks.filter((task) => task.outreachReview.snapshotSha256 === snapshotSha256);
  if (exact.length === 1) {
    return { operation: "existing" as const, taskId: exact[0]._id ?? exact[0].id ?? "", reviewCycle: exact[0].outreachReview.reviewCycle, snapshotSha256 };
  }
  if (summary.reviewCount >= 2) throw new OutreachReviewContractError("cycle_limit");
  const reviewCycle = (summary.reviewCount + 1) as 1 | 2;
  const outreachReview: OutreachReviewSnapshot = { ...input, snapshotSha256, reviewCycle, admittedBy: "server", admittedAt: now };
  return {
    operation: "create" as const,
    fields: {
      title: `Review outreach draft: ${input.cohortId} / ${input.candidateId} / cycle ${reviewCycle}`,
      description: `Immutable outreach review ${input.cohortId}/${input.candidateId} cycle ${reviewCycle}; snapshot ${snapshotSha256}`,
      status: "todo" as const,
      assignee: "jt" as const,
      priority: "high" as const,
      project: "AI Workflow Growth OS",
      workstream: "paid-delivery" as const,
      sourceSystem: "jt-ops-outreach-review",
      dedupeKey: `outreach-review:${input.cohortId}:${input.candidateId}:${snapshotSha256}`,
      candidateId: input.candidateId,
      cohortId: input.cohortId,
      draftSha256: input.draftSha256,
      outreachReview,
      createdAt: now,
      updatedAt: now,
    },
  };
}
