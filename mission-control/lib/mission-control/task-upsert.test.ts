import { describe, expect, test } from "bun:test";
import { resolveTaskUpsert } from "./task-upsert";

function errorMessage(run: () => unknown): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

describe("deduplicated task upsert", () => {
  test("creates when the dedupe key has no match", () => {
    expect(resolveTaskUpsert(null, { title: "New", dedupeKey: "k" }, 200)).toEqual({
      operation: "create",
      fields: { title: "New", dedupeKey: "k", createdAt: 200, updatedAt: 200 },
    });
  });

  test("updates the existing task without replacing its identity or creation time", () => {
    expect(resolveTaskUpsert({ _id: "task-1", createdAt: 100, updatedAt: 100 }, { title: "Updated", dedupeKey: "k" }, 200)).toEqual({
      operation: "update",
      id: "task-1",
      fields: { title: "Updated", dedupeKey: "k", updatedAt: 200 },
    });
  });

  test("cannot mutate an outreach decision binding through generic keyed POST", () => {
    const existing = {
      _id: "task-1",
      createdAt: 100,
      updatedAt: 100,
      candidateId: "candidate-1",
      draftSha256: "a".repeat(64),
      outreachDecision: {
        candidateId: "candidate-1",
        draftSha256: "a".repeat(64),
        decision: "approve" as const,
        decidedBy: "jt" as const,
        decidedAt: 100,
      },
    };
    expect(errorMessage(() => resolveTaskUpsert(existing, { candidateId: "candidate-1", draftSha256: "b".repeat(64) }, 200)))
      .toContain("outreach review task is immutable");
  });

  test("cannot mutate an undecided outreach review snapshot through generic keyed POST", () => {
    const existing = {
      _id: "task-1",
      createdAt: 100,
      updatedAt: 100,
      title: "Exact review content",
      candidateId: "candidate-1",
      draftSha256: "a".repeat(64),
      outreachReview: {
        candidateId: "candidate-1",
        draftSha256: "a".repeat(64),
        admittedBy: "server" as const,
        admittedAt: 100,
      },
    };
    expect(errorMessage(() => resolveTaskUpsert(existing, { title: "Forged replacement", dedupeKey: "k" }, 200)))
      .toContain("outreach review task is immutable");
  });
});
