import { describe, expect, test } from "bun:test";
import { outreachDecisionView } from "./outreach-decision-display";
import type { OutreachReviewSnapshot } from "./outreach-review";

const DRAFT = "a".repeat(64);
const SNAPSHOT = "b".repeat(64);
const COMMIT = "c".repeat(40);
const bind = (path: string) => ({ repository: "owner/repo", commitSha: COMMIT, path, blobSha256: DRAFT });
const review: OutreachReviewSnapshot = {
  candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: DRAFT,
  subject: "Persisted subject", body: "Persisted exact body", verifierReport: "VERDICT: CONFIRM",
  reviewAuthorityId: "jt", verifierActorId: "verifier-1",
  gitBindings: { evidence: bind("evidence"), policy: bind("policy"), gate: bind("gate"), draft: bind("draft"), verifier: bind("verifier") },
  snapshotSha256: SNAPSHOT, reviewCycle: 1, admittedBy: "server", admittedAt: 1,
};
const base = { source: "task", status: "todo", candidateId: "candidate-1", draftSha256: DRAFT, outreachReview: review } as const;

describe("outreach review decision display", () => {
  test("shows pending controls and content only from the persisted immutable snapshot", () => {
    expect(outreachDecisionView({ ...base, description: "forged subject and body" })).toEqual({
      candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT,
      state: "pending", snapshot: review,
    });
  });

  test("renders a closed exact decision and rejects a mismatched snapshot binding", () => {
    const approved = { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve" as const, decidedBy: "jt" as const, decidedAt: 123 };
    expect(outreachDecisionView({ ...base, status: "done", outreachDecision: approved })).toEqual({
      candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT,
      state: "approved", snapshot: review, decision: approved,
    });
    expect(outreachDecisionView({ ...base, outreachDecision: { ...approved, snapshotSha256: "d".repeat(64) } })).toEqual({
      candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT,
      state: "invalid", snapshot: review,
    });
  });

  test("hides generic, archived, and incomplete review tasks", () => {
    expect(outreachDecisionView({ source: "task", status: "todo", candidateId: "candidate-1", draftSha256: DRAFT })).toBe(null);
    expect(outreachDecisionView({ ...base, status: "archived" })).toBe(null);
    expect(outreachDecisionView({ ...base, outreachReview: { ...review, snapshotSha256: "bad" } })).toBe(null);
  });
});
