import type { Workstream } from "./types";

export const NIGHTLY_PROMOTION_THRESHOLD = 30;
export const NIGHTLY_EVIDENCE_THRESHOLD = 4;
export const NIGHTLY_DISTRIBUTION_THRESHOLD = 3;
const VERIFICATION_FRESHNESS_MS = 24 * 60 * 60 * 1000;

const TASK_FIELDS = [
  "title", "description", "status", "assignee", "priority", "project", "sortOrder", "slug",
  "pipelineStage", "dueDate", "dueDateSource", "dollars", "stageProbability", "effortMinutes",
  "lane", "waitingOn", "snoozedUntil", "proofRequired", "riskContainment", "cashDirect", "blocks",
  "blocksAgent", "reasonCodes", "rankScore", "rankUpdatedAt",
  "firstAction", "whyItMatters", "doneState", "evidenceLinks", "sourceSystem", "reviewAt", "dedupeKey",
  "workstream", "hypothesis", "nextTest", "killDate", "promotionScore", "revivalTrigger",
  "verdict", "verifierConfirmed", "verifiedAt", "candidateId", "sourceHash", "evidenceScore",
  "distributionScore", "fatalConstraint",
] as const;

const SNAKE_CASE_NIGHTLY_ALIASES = [
  "first_action", "why_it_matters", "done_state", "evidence_links", "source_system",
  "promotion_score", "verifier_confirmed", "verified_at", "candidate_id", "source_hash",
  "evidence_score", "distribution_score", "fatal_constraint",
] as const;

const WORKSTREAMS: Workstream[] = ["paid-delivery", "career-hedge", "compounding-bet", "administrative", "other"];

export function normalizeTaskInput(
  input: Record<string, unknown>,
  options: { includeAudit?: boolean } = {},
): Record<string, unknown> {
  const fields: readonly string[] = options.includeAudit
    ? [...TASK_FIELDS, "auditSource", "auditEvidence"]
    : TASK_FIELDS;
  return Object.fromEntries(fields.filter((field) => input[field] !== undefined).map((field) => [field, input[field]]));
}

export function validateTaskAdmission(input: Record<string, unknown>, now = new Date()): void {
  if (input.source === "nightly-validation-controller") {
    throw new Error("sourceSystem is required; source cannot identify nightly admission");
  }
  if (input.dedupe_key !== undefined) throw new Error("dedupeKey is required; dedupe_key is not accepted");
  if (SNAKE_CASE_NIGHTLY_ALIASES.some((field) => input[field] !== undefined)) {
    throw new Error("snake_case nightly aliases are not accepted");
  }
  if (input.workstream !== undefined && !WORKSTREAMS.includes(input.workstream as Workstream)) {
    throw new Error("invalid workstream");
  }
  if (input.sourceSystem !== "nightly-validation-controller") return;

  for (const field of ["dedupeKey", "firstAction", "whyItMatters", "doneState", "workstream"] as const) {
    if (typeof input[field] !== "string" || !input[field]) throw new Error(`${field} required for nightly admission`);
  }
  if (!Array.isArray(input.evidenceLinks) || input.evidenceLinks.length === 0) {
    throw new Error("evidenceLinks required for nightly admission");
  }
  if (typeof input.promotionScore !== "number" || input.promotionScore < NIGHTLY_PROMOTION_THRESHOLD) {
    throw new Error(`promotionScore must be at least ${NIGHTLY_PROMOTION_THRESHOLD}`);
  }
  if (input.verdict !== "promote") throw new Error("verdict must be promote");
  if (input.verifierConfirmed !== true) throw new Error("verifierConfirmed must be true");
  if (typeof input.verifiedAt !== "string") throw new Error("verifiedAt is required");
  const verifiedAt = Date.parse(input.verifiedAt);
  const verificationAge = now.getTime() - verifiedAt;
  if (!Number.isFinite(verifiedAt) || verificationAge < 0 || verificationAge > VERIFICATION_FRESHNESS_MS) {
    throw new Error("verifiedAt must be a fresh timestamp within 24 hours");
  }
  for (const field of ["candidateId", "sourceHash"] as const) {
    if (typeof input[field] !== "string" || !input[field]) throw new Error(`${field} required for nightly admission`);
  }
  if (typeof input.evidenceScore !== "number" || input.evidenceScore < NIGHTLY_EVIDENCE_THRESHOLD) {
    throw new Error(`evidenceScore must be at least ${NIGHTLY_EVIDENCE_THRESHOLD}`);
  }
  if (typeof input.distributionScore !== "number" || input.distributionScore < NIGHTLY_DISTRIBUTION_THRESHOLD) {
    throw new Error(`distributionScore must be at least ${NIGHTLY_DISTRIBUTION_THRESHOLD}`);
  }
  if (input.fatalConstraint !== false) throw new Error("fatalConstraint must be false");
}
