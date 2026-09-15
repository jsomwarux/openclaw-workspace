import { describe, expect, test } from "bun:test";
import { resolveOutreachReviewCreateOnly } from "./outreach-review";

const SHA = "a".repeat(64);
const input = {
  title: "Review exact draft",
  dedupeKey: `outreach:candidate-1:${SHA}`,
  candidateId: "candidate-1",
  draftSha256: SHA,
};

function message(run: () => unknown) {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

describe("server-authorized outreach review admission", () => {
  test("creates one task with a server-stamped marker and no capability field", () => {
    const result = resolveOutreachReviewCreateOnly(null, input, 123);
    if (result.operation !== "create") throw new Error("expected create operation");
    expect(result).toEqual({
      operation: "create",
      fields: {
        ...input,
        outreachReview: {
          candidateId: "candidate-1",
          draftSha256: SHA,
          admittedBy: "server",
          admittedAt: 123,
        },
        createdAt: 123,
        updatedAt: 123,
      },
    });
    expect("capability" in result.fields).toBe(false);
  });

  test("is idempotent only for the same server-marked review version", () => {
    const existing = {
      _id: "task-1",
      ...input,
      outreachReview: {
        candidateId: "candidate-1",
        draftSha256: SHA,
        admittedBy: "server" as const,
        admittedAt: 100,
      },
    };
    expect(resolveOutreachReviewCreateOnly(existing, input, 999)).toEqual({ operation: "existing", id: "task-1" });
  });

  test("rejects an unmarked or mismatched task occupying the dedupe key", () => {
    expect(message(() => resolveOutreachReviewCreateOnly({ _id: "generic", ...input }, input, 123)))
      .toContain("existing task is not the same server-admitted outreach review");
    expect(message(() => resolveOutreachReviewCreateOnly({
      _id: "other",
      ...input,
      outreachReview: {
        candidateId: "candidate-2",
        draftSha256: SHA,
        admittedBy: "server",
        admittedAt: 100,
      },
    }, input, 123))).toContain("existing task is not the same server-admitted outreach review");
  });
});
