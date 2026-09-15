import { describe, expect, test } from "bun:test";
import { assertOutreachTaskMutable, resolveOutreachDecision, resolveOutreachLookup } from "./outreach-decision";
import type { OutreachReviewSnapshot } from "./outreach-review";
import { normalizeTaskInput, validateTaskAdmission } from "./task-admission";

const DRAFT = "a".repeat(64);
const SNAPSHOT = "b".repeat(64);
const COMMIT = "c".repeat(40);
const bind = (path: string) => ({ repository: "owner/repo", commitSha: COMMIT, path, blobSha256: DRAFT });
const review: OutreachReviewSnapshot = {
  candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: DRAFT,
  subject: "Subject", body: "Exact draft", verifierReport: "VERDICT: CONFIRM",
  reviewAuthorityId: "jt", verifierActorId: "verifier-1",
  gitBindings: { evidence: bind("evidence"), policy: bind("policy"), gate: bind("gate"), draft: bind("draft"), verifier: bind("verifier") },
  snapshotSha256: SNAPSHOT, reviewCycle: 1, admittedBy: "server", admittedAt: 50,
};
const task = { _id: "task-1", status: "todo", candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: DRAFT, outreachReview: review };

function expectError(fn: () => unknown, message: string) {
  try { fn(); } catch (error) { expect(error instanceof Error ? error.message : String(error)).toContain(message); return; }
  throw new Error(`Expected error containing: ${message}`);
}

describe("immutable outreach decision", () => {
  test("binds the first JT decision to candidate, draft, and snapshot then closes the task", () => {
    expect(resolveOutreachDecision(task, { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve" }, 123)).toEqual({
      operation: "create",
      decision: { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve", decidedBy: "jt", decidedAt: 123 },
      status: "done",
    });
  });

  test("returns an exact same-value retry after closure and rejects reversal", () => {
    const decision = { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "reject" as const, decidedBy: "jt" as const, decidedAt: 100 };
    expect(resolveOutreachDecision({ ...task, status: "done", outreachDecision: decision }, { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "reject" }, 999))
      .toEqual({ operation: "existing", decision });
    expectError(() => resolveOutreachDecision({ ...task, status: "done", outreachDecision: decision }, { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve" }, 999), "immutable");
  });

  test("rejects snapshot mismatch, generic tasks, and non-todo first decisions", () => {
    expectError(() => resolveOutreachDecision(task, { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: "d".repeat(64), decision: "approve" }, 123), "identity");
    expectError(() => resolveOutreachDecision({ ...task, outreachReview: undefined }, { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve" }, 123), "server-admitted");
    expectError(() => resolveOutreachDecision({ ...task, status: "done" }, { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve" }, 123), "active");
  });

  test("generic task paths cannot forge or mutate snapshot authority", () => {
    expectError(() => assertOutreachTaskMutable(task), "immutable");
    assertOutreachTaskMutable({ _id: "ordinary" });
    for (const forged of [{ outreachReview: review }, { outreachDecision: { decision: "approve" } }, { reviewCycle: 1 }, { snapshotSha256: SNAPSHOT }]) {
      expectError(() => validateTaskAdmission(forged), "specialized endpoint");
    }
    expect(normalizeTaskInput({ candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, reviewCycle: 1 }))
      .toEqual({ candidateId: "candidate-1", draftSha256: DRAFT });
  });
});

describe("outreach decision lookup", () => {
  const approved = { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve" as const, decidedBy: "jt" as const, decidedAt: 100 };
  const rejected = { ...approved, decision: "reject" as const };

  test("returns pending, approved, and rejected states for the exact active snapshot", () => {
    expect(resolveOutreachLookup(task, "candidate-1", DRAFT, SNAPSHOT)).toEqual({ authorized: false, state: "pending", taskId: "task-1" });
    expect(resolveOutreachLookup({ ...task, status: "done", outreachDecision: approved }, "candidate-1", DRAFT, SNAPSHOT)).toEqual({ authorized: true, state: "approved", decision: approved, taskId: "task-1" });
    expect(resolveOutreachLookup({ ...task, status: "done", outreachDecision: rejected }, "candidate-1", DRAFT, SNAPSHOT)).toEqual({ authorized: false, state: "rejected", decision: rejected, taskId: "task-1" });
  });

  test("returns absent for archived, missing, or mismatched snapshots", () => {
    expect(resolveOutreachLookup({ ...task, status: "archived", outreachDecision: approved }, "candidate-1", DRAFT, SNAPSHOT)).toEqual({ authorized: false, state: "absent" });
    expect(resolveOutreachLookup(task, "candidate-1", DRAFT, "d".repeat(64))).toEqual({ authorized: false, state: "absent" });
    expect(resolveOutreachLookup(null, "candidate-1", DRAFT, SNAPSHOT)).toEqual({ authorized: false, state: "absent" });
  });
});
