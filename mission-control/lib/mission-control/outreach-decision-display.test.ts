import { describe, expect, test } from "bun:test";
import { outreachDecisionView } from "./outreach-decision-display";

const SHA = "a".repeat(64);

describe("outreach review decision display", () => {
  test("shows pending controls only for a task with an exact outreach draft identity", () => {
    expect(outreachDecisionView({ source: "task", status: "todo", candidateId: "candidate-1", draftSha256: SHA })).toEqual({
      candidateId: "candidate-1",
      draftSha256: SHA,
      state: "pending",
    });
    expect(outreachDecisionView({ source: "task", status: "todo", candidateId: "candidate-1" })).toBe(null);
    expect(outreachDecisionView({ source: "proof", status: "todo", candidateId: "candidate-1", draftSha256: SHA })).toBe(null);
    expect(outreachDecisionView({ source: "task", status: "archived", candidateId: "candidate-1", draftSha256: SHA })).toBe(null);
    expect(outreachDecisionView({ source: "task", status: "done", candidateId: "candidate-1", draftSha256: SHA })).toBe(null);
  });

  test("renders an immutable approved or rejected decision instead of pending controls", () => {
    const approved = {
      candidateId: "candidate-1",
      draftSha256: SHA,
      decision: "approve" as const,
      decidedBy: "jt" as const,
      decidedAt: 123,
    };
    expect(outreachDecisionView({ source: "task", status: "todo", candidateId: "candidate-1", draftSha256: SHA, outreachDecision: approved })).toEqual({
      candidateId: "candidate-1",
      draftSha256: SHA,
      state: "approved",
      decision: approved,
    });
  });

  test("fails closed when the stored decision does not match the task identity", () => {
    expect(outreachDecisionView({
      source: "task",
      status: "todo",
      candidateId: "candidate-1",
      draftSha256: SHA,
      outreachDecision: {
        candidateId: "other",
        draftSha256: SHA,
        decision: "approve",
        decidedBy: "jt",
        decidedAt: 123,
      },
    })).toEqual({ candidateId: "candidate-1", draftSha256: SHA, state: "invalid" });
  });
});
