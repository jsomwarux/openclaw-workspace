import { describe, expect, test } from "bun:test";
import {
  assertOutreachIdentityMutation,
  assertOutreachTaskRemoval,
  resolveOutreachDecision,
  resolveOutreachLookup,
} from "./outreach-decision";
import { normalizeTaskInput, validateTaskAdmission } from "./task-admission";

const SHA_A = "a".repeat(64);
const SHA_B = "b".repeat(64);

const task = {
  _id: "task-1",
  candidateId: "candidate-1",
  draftSha256: SHA_A,
  outreachReview: {
    candidateId: "candidate-1",
    draftSha256: SHA_A,
    admittedBy: "server" as const,
    admittedAt: 50,
  },
};

function expectError(fn: () => unknown, message: string) {
  try {
    fn();
  } catch (error) {
    expect(error instanceof Error ? error.message : String(error)).toContain(message);
    return;
  }
  throw new Error(`Expected error containing: ${message}`);
}

describe("immutable outreach decision", () => {
  test("records the first JT decision against the exact candidate and draft", () => {
    expect(resolveOutreachDecision(task, { candidateId: "candidate-1", draftSha256: SHA_A, decision: "approve" }, 123)).toEqual({
      operation: "create",
      decision: {
        candidateId: "candidate-1",
        draftSha256: SHA_A,
        decision: "approve",
        decidedBy: "jt",
        decidedAt: 123,
      },
    });
  });

  test("returns an identical existing decision without changing its time", () => {
    const outreachDecision = {
      candidateId: "candidate-1",
      draftSha256: SHA_A,
      decision: "reject" as const,
      decidedBy: "jt" as const,
      decidedAt: 100,
    };
    expect(resolveOutreachDecision({ ...task, outreachDecision }, { candidateId: "candidate-1", draftSha256: SHA_A, decision: "reject" }, 999)).toEqual({
      operation: "existing",
      decision: outreachDecision,
    });
  });

  test("rejects a reversal on the same task", () => {
    const outreachDecision = {
      candidateId: "candidate-1",
      draftSha256: SHA_A,
      decision: "approve" as const,
      decidedBy: "jt" as const,
      decidedAt: 100,
    };
    expectError(
      () => resolveOutreachDecision({ ...task, outreachDecision }, { candidateId: "candidate-1", draftSha256: SHA_A, decision: "reject" }, 999),
      "outreach decision is immutable; create a new versioned task",
    );
  });

  test("rejects candidate or draft mismatch", () => {
    expectError(() => resolveOutreachDecision(task, { candidateId: "other", draftSha256: SHA_A, decision: "approve" }, 123), "outreach decision identity does not match task");
    expectError(() => resolveOutreachDecision(task, { candidateId: "candidate-1", draftSha256: SHA_B, decision: "approve" }, 123), "outreach decision identity does not match task");
  });

  test("rejects a generic task that has no server-owned outreach review marker", () => {
    expectError(
      () => resolveOutreachDecision(
        { _id: "generic", candidateId: "candidate-1", draftSha256: SHA_A },
        { candidateId: "candidate-1", draftSha256: SHA_A, decision: "approve" },
        123,
      ),
      "server-admitted outreach review required",
    );
  });

  test("rejects malformed identities and decisions", () => {
    expectError(() => resolveOutreachDecision(task, { candidateId: "", draftSha256: SHA_A, decision: "approve" }, 123), "candidateId required");
    expectError(() => resolveOutreachDecision(task, { candidateId: "candidate-1", draftSha256: "A".repeat(64), decision: "approve" }, 123), "draftSha256 must be 64 lowercase hex characters");
    expectError(() => resolveOutreachDecision(task, { candidateId: "candidate-1", draftSha256: SHA_A, decision: "maybe" as never }, 123), "decision must be approve or reject");
  });

  test("blocks generic identity mutation after JT decides", () => {
    const decided = {
      ...task,
      outreachDecision: {
        candidateId: "candidate-1",
        draftSha256: SHA_A,
        decision: "approve" as const,
        decidedBy: "jt" as const,
        decidedAt: 100,
      },
    };
    expectError(() => assertOutreachIdentityMutation(decided, { draftSha256: SHA_B }), "outreach decision identity is immutable");
    expectError(() => assertOutreachIdentityMutation(decided, { candidateId: "other" }), "outreach decision identity is immutable");
    assertOutreachIdentityMutation(decided, { title: "safe" });
  });

  test("blocks generic identity mutation after server review admission and before JT decides", () => {
    expectError(() => assertOutreachIdentityMutation(task, { draftSha256: SHA_B }), "outreach review identity is immutable");
    expectError(() => assertOutreachIdentityMutation(task, { candidateId: "other" }), "outreach review identity is immutable");
    assertOutreachIdentityMutation(task, { title: "safe" });
  });

  test("blocks generic deletion after JT decides", () => {
    expectError(
      () => assertOutreachTaskRemoval({
        ...task,
        outreachDecision: {
          candidateId: "candidate-1",
          draftSha256: SHA_A,
          decision: "approve",
          decidedBy: "jt",
          decidedAt: 100,
        },
      }),
      "outreach decision task is immutable",
    );
    assertOutreachTaskRemoval({ _id: "ordinary" });
  });

  test("blocks generic deletion after server review admission", () => {
    expectError(() => assertOutreachTaskRemoval(task), "outreach review task is immutable");
    assertOutreachTaskRemoval({ _id: "ordinary" });
  });

  test("generic task admission preserves draft identity but rejects decision authority", () => {
    expectError(
      () => validateTaskAdmission({ candidateId: "candidate-1", draftSha256: SHA_A, outreachDecision: { decision: "approve" } }),
      "outreach decisions require the specialized endpoint",
    );
    expect(normalizeTaskInput({ candidateId: "candidate-1", draftSha256: SHA_A })).toEqual({
      candidateId: "candidate-1",
      draftSha256: SHA_A,
    });
    expectError(
      () => validateTaskAdmission({ outreachReview: { candidateId: "candidate-1", draftSha256: SHA_A } }),
      "outreach review eligibility requires the specialized endpoint",
    );
  });
});

describe("outreach decision lookup", () => {
  test("authorizes only an exact approved binding", () => {
    const decision = {
      candidateId: "candidate-1",
      draftSha256: SHA_A,
      decision: "approve" as const,
      decidedBy: "jt" as const,
      decidedAt: 100,
    };
    expect(resolveOutreachLookup({ ...task, outreachDecision: decision }, "candidate-1", SHA_A)).toEqual({
      authorized: true,
      state: "approved",
      decision,
      taskId: "task-1",
    });
  });

  test("fails closed for rejection, absence, or mismatch", () => {
    const rejected = {
      ...task,
      outreachDecision: {
        candidateId: "candidate-1",
        draftSha256: SHA_A,
        decision: "reject" as const,
        decidedBy: "jt" as const,
        decidedAt: 100,
      },
    };
    expect(resolveOutreachLookup(rejected, "candidate-1", SHA_A).state).toBe("rejected");
    expect(resolveOutreachLookup(task, "candidate-1", SHA_A)).toEqual({ authorized: false, state: "absent" });
    expect(resolveOutreachLookup({ _id: "generic", candidateId: "candidate-1", draftSha256: SHA_A, outreachDecision: rejected.outreachDecision }, "candidate-1", SHA_A))
      .toEqual({ authorized: false, state: "absent" });
    expect(resolveOutreachLookup(rejected, "candidate-1", SHA_B)).toEqual({ authorized: false, state: "absent" });
  });
});
