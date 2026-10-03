import { describe, expect, test } from "bun:test";
import { actionContext, permittedActions, sliceOneActions } from "./actions";
import { ANSWER_MAX, answerBody, decisionBody, savedAnswer, validateAnswer, validateDecisionNote } from "./answer";
import { validateCard } from "./validity";
import { FIXTURE_NOW, allFixtureTasks, fx } from "./fixtures/data";
import type { RawTask } from "./types";

const NOW = FIXTURE_NOW;
const ctx = (task: RawTask, over: { paused?: boolean } = {}) => actionContext(task, NOW, { paused: over.paused ?? false });
const actions = (task: RawTask, over: { paused?: boolean } = {}) => permittedActions(ctx(task, over));
const answered = (task: RawTask): RawTask => ({ ...task, feedback: [{ id: "1-1", body: "Answer: go with option two", author: "jt", createdAt: NOW - 1000 }] });

describe("permitted actions (DECISIONS 5.7 with override 1)", () => {
  test("generic task, not started", () => {
    expect(actions(fx("F04"))).toEqual(["start", "complete", "defer", "block", "previous", "next"]);
  });

  test("generic task, in progress", () => {
    expect(actions({ ...fx("F04"), status: "in-progress" })).toEqual(["complete", "defer", "block", "previous", "next"]);
  });

  test("a waiting card whose nudge is due acts like a card not yet started", () => {
    expect(actions(fx("F07"))).toEqual(["start", "complete", "defer", "block", "previous", "next"]);
  });

  test("generic task already done: move only", () => {
    expect(actions(fx("F10"))).toEqual(["previous", "next"]);
  });

  test("Q and AP: Save answer until an answer is saved, then Complete; never Start", () => {
    for (const id of ["F01", "F03"] as const) {
      expect(actions(fx(id))).toEqual(["saveAnswer", "defer", "block", "previous", "next"]);
      expect(actions(answered(fx(id)))).toEqual(["complete", "defer", "block", "previous", "next"]);
    }
  });

  test("P: Approve and Reject; never Complete, Start or Save answer", () => {
    expect(actions(fx("F02"))).toEqual(["approve", "reject", "defer", "block", "previous", "next"]);
  });

  test("lane packet, open, not expired: Approve, Reject, Defer, Block, Start; Complete only when internal", () => {
    expect(actions(fx("F05"))).toEqual(["approve", "reject", "defer", "block", "start", "previous", "next"]);
    expect(actions({ ...fx("F05"), doneEvidenceType: "none" })).toEqual(["approve", "reject", "complete", "defer", "block", "start", "previous", "next"]);
  });

  test("lane packet, open, expired: Reject only", () => {
    expect(actions(fx("F06"))).toEqual(["reject", "previous", "next"]);
  });

  test("lane packet, closed: move only, and no Defer", () => {
    expect(actions({ ...fx("F05"), status: "done" })).toEqual(["previous", "next"]);
    expect(actions({ ...fx("F05"), status: "archived" })).toEqual(["previous", "next"]);
  });

  test("outreach review: Approve and Reject while pending; move only once decided; Defer never offered", () => {
    expect(actions(fx("F11"))).toEqual(["approve", "reject", "previous", "next"]);
    expect(actions({ ...fx("F11"), outreachDecision: { decision: "reject" }, status: "done" })).toEqual(["previous", "next"]);
  });

  test("any paused state allows only Previous and Next", () => {
    for (const task of allFixtureTasks()) expect(actions(task, { paused: true })).toEqual(["previous", "next"]);
  });

  test("an invalid card allows only Previous and Next", () => {
    expect(actions({ ...fx("F04"), title: "  " })).toEqual(["previous", "next"]);
  });

  test("slice one renders lane packets and outreach reviews read-only", () => {
    expect(sliceOneActions(ctx(fx("F05")))).toEqual(["previous", "next"]);
    expect(sliceOneActions(ctx(fx("F06")))).toEqual(["previous", "next"]);
    expect(sliceOneActions(ctx(fx("F11")))).toEqual(["previous", "next"]);
    expect(sliceOneActions(ctx(fx("F02")))).toEqual(["approve", "reject", "defer", "block", "previous", "next"]);
  });
});

describe("answer before Complete (DECISIONS 5.1)", () => {
  test("only a jt entry that starts with 'Answer: ' and says something counts as saved", () => {
    expect(savedAnswer(undefined)).toBe(null);
    expect(savedAnswer([{ id: "1", body: "Answer: yes", author: "eve", createdAt: 1 }])).toBe(null);
    expect(savedAnswer([{ id: "1", body: "Answer:", author: "jt", createdAt: 1 }])).toBe(null);
    expect(savedAnswer([{ id: "1", body: "answer: yes", author: "jt", createdAt: 1 }])).toBe(null);
    expect(savedAnswer([{ id: "1", body: "Note: Answer: yes", author: "jt", createdAt: 1 }])).toBe(null);
    const latest = savedAnswer([
      { id: "1", body: "Answer: first", author: "jt", createdAt: 1 },
      { id: "2", body: "Answer: second", author: "jt", createdAt: 2 },
    ]);
    expect(latest?.body).toBe("Answer: second");
  });

  test("answers are trimmed, must say something, and must fit the 4,000-character feedback body with the prefix", () => {
    expect(answerBody("  keep the second option \n")).toBe("Answer: keep the second option");
    expect(validateAnswer("   ")).toEqual({ ok: false, error: "Enter an answer before saving." });
    expect(ANSWER_MAX).toBe(3992);
    expect(validateAnswer("x".repeat(3992))).toEqual({ ok: true, body: `Answer: ${"x".repeat(3992)}` });
    expect(answerBody("x".repeat(3992))).toHaveLength(4000);
    expect(validateAnswer("x".repeat(3993))).toEqual({ ok: false, error: "Shorten the answer to 3,992 characters or fewer." });
  });

  test("P decisions record one feedback entry; the note is optional", () => {
    expect(decisionBody("approve", "")).toBe("Decision: Approved.");
    expect(decisionBody("reject", "  wrong lane  ")).toBe("Decision: Rejected. wrong lane");
    expect(validateDecisionNote("")).toEqual({ ok: true });
    expect(validateDecisionNote("x".repeat(3980))).toEqual({ ok: true });
    expect(decisionBody("approve", "x".repeat(3980))).toHaveLength(4000);
    expect(validateDecisionNote("x".repeat(3981))).toEqual({ ok: false, error: "Shorten the note to 3,980 characters or fewer." });
  });
});

describe("invalid cards (DECISIONS 9)", () => {
  test("every fixture is valid", () => {
    for (const task of allFixtureTasks()) expect(validateCard(task)).toEqual({ ok: true });
  });

  test("one plain sentence per failed check", () => {
    expect(validateCard({ ...fx("F04"), title: " ", status: "blocked" })).toEqual({ ok: false, reasons: ["No title is recorded.", "Its status is not one this app recognizes."] });
    expect(validateCard({ ...fx("F04"), title: undefined })).toEqual({ ok: false, reasons: ["No title is recorded."] });
    expect(validateCard({ ...fx("F04"), assignee: "JT" })).toEqual({ ok: false, reasons: ["Its owner is not one this app recognizes."] });
    expect(validateCard({ ...fx("F04"), priority: "urgent" })).toEqual({ ok: false, reasons: ["Its priority is not one this app recognizes."] });
    expect(validateCard({ ...fx("F05"), payloadHash: undefined })).toEqual({ ok: false, reasons: ["Its approval details are incomplete."] });
    expect(validateCard({ ...fx("F05"), doneEvidenceType: undefined })).toEqual({ ok: false, reasons: ["Its approval details are incomplete."] });
    const review = fx("F11");
    expect(validateCard({ ...review, outreachReview: { ...review.outreachReview, snapshotSha256: undefined } })).toEqual({ ok: false, reasons: ["Its review details are incomplete."] });
    expect(validateCard({ ...review, outreachDecision: { decision: "maybe" } })).toEqual({ ok: false, reasons: ["Its review details are incomplete."] });
  });
});
