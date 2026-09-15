import { describe, expect, test } from "bun:test";
import { appendTaskFeedback, parseTaskFeedbackAppend } from "./task-feedback";

function errorMessage(run: () => void): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

describe("append-only task feedback", () => {
  test("appends one server-owned entry and preserves prior history", () => {
    const prior = [{ id: "100-1", body: "First note", author: "jt" as const, createdAt: 100 }];
    expect(appendTaskFeedback(prior, { body: "  Tighten the opening.  ", author: "jt" }, 200)).toEqual([
      ...prior,
      { id: "200-2", body: "Tighten the opening.", author: "jt", createdAt: 200 },
    ]);
  });

  test("rejects blank, oversized, and invalid-author feedback", () => {
    expect(errorMessage(() => appendTaskFeedback([], { body: "   ", author: "jt" }, 200))).toBe("feedback body required");
    expect(errorMessage(() => appendTaskFeedback([], { body: "x".repeat(4001), author: "jt" }, 200))).toBe("feedback body too long");
    expect(errorMessage(() => appendTaskFeedback([], { body: "note", author: "model" as "jt" }, 200))).toBe("feedback author invalid");
  });

  test("accepts only the dedicated append-feedback API shape", () => {
    expect(parseTaskFeedbackAppend({ action: "append-feedback", id: "task-1", body: "Note", author: "jt" })).toEqual({
      id: "task-1", body: "Note", author: "jt",
    });
    expect(errorMessage(() => parseTaskFeedbackAppend({ action: "replace-feedback", id: "task-1", body: "Note", author: "jt" }))).toBe("append-feedback action required");
    expect(errorMessage(() => parseTaskFeedbackAppend({ action: "append-feedback", id: "", body: "Note", author: "jt" }))).toBe("id required");
    expect(errorMessage(() => parseTaskFeedbackAppend({ action: "append-feedback", id: "task-1", body: "   ", author: "jt" }))).toBe("feedback body required");
    expect(errorMessage(() => parseTaskFeedbackAppend({ action: "append-feedback", id: "task-1", body: "x".repeat(4001), author: "jt" }))).toBe("feedback body too long");
  });
});
