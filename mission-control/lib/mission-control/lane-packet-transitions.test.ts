import { describe, expect, test } from "bun:test";
import {
  LanePacketError,
  hashLanePacketPayload,
  resolveLanePacketAdmission,
  validateLanePacketSubmission,
  type LanePacketSubmission,
  type StoredLanePacketTask,
} from "./lane-packet";
import {
  assertGenericDedupeKey,
  assertGenericLanePacketRemoval,
  lanePacketSnoozeUntil,
  resolveGenericLanePacketWrite,
  resolveLanePacketExpiry,
  resolveLanePacketTransition,
  validateLanePacketTransition,
  type LanePacketTransition,
} from "./lane-packet-transitions";
import { FIXTURE_NOW, jobsPacketFixture, linkedinPacketFixture } from "./lane-packet-fixtures";

const DAY_MS = 24 * 60 * 60 * 1000;
const LATER = FIXTURE_NOW + 60_000;

async function packet(submission: LanePacketSubmission = jobsPacketFixture()): Promise<StoredLanePacketTask> {
  const resolved = await resolveLanePacketAdmission([], validateLanePacketSubmission(submission, FIXTURE_NOW), FIXTURE_NOW);
  if (resolved.operation !== "create") throw new Error("expected create");
  return { _id: "task-1", ...resolved.fields } as StoredLanePacketTask;
}

async function approved(submission?: LanePacketSubmission): Promise<StoredLanePacketTask> {
  const task = await packet(submission);
  const result = await resolveLanePacketTransition(task, { action: "approve", payloadHash: task.payloadHash! }, "jt", FIXTURE_NOW);
  if (result.operation !== "patch") throw new Error("expected patch");
  return { ...task, ...result.fields } as StoredLanePacketTask;
}

async function rejection(run: () => Promise<unknown> | unknown): Promise<{ code: string; message: string }> {
  try {
    await run();
  } catch (error) {
    if (error instanceof LanePacketError) return { code: error.code, message: error.message };
    return { code: "non-contract-error", message: String(error) };
  }
  return { code: "none", message: "" };
}

function patchOf(result: Awaited<ReturnType<typeof resolveLanePacketTransition>>): Record<string, unknown> {
  if (result.operation !== "patch") throw new Error("expected patch");
  return result.fields;
}

describe("approval binds to the exact payload JT reviewed", () => {
  test("JT approves the current payload hash", async () => {
    const task = await packet();
    const fields = patchOf(await resolveLanePacketTransition(task, { action: "approve", payloadHash: task.payloadHash! }, "jt", LATER));
    expect(fields).toEqual({ approvalState: "approved", approvedPayloadHash: task.payloadHash, approvedAt: LATER, updatedAt: LATER });
  });

  test("a producer can never approve", async () => {
    const task = await packet();
    expect(await rejection(() => resolveLanePacketTransition(task, { action: "approve", payloadHash: task.payloadHash! }, "eve", LATER))).toEqual({
      code: "forbidden",
      message: "only JT can approve, reject, or complete a lane packet",
    });
  });

  test("approving a stale hash fails instead of approving content JT never saw", async () => {
    const task = await packet();
    expect(await rejection(() => resolveLanePacketTransition(task, { action: "approve", payloadHash: "0".repeat(64) }, "jt", LATER))).toEqual({
      code: "conflict",
      message: "payload changed since review; review the current version",
    });
  });

  test("re-approving the same hash is an idempotent no-op", async () => {
    const task = await approved();
    expect(await resolveLanePacketTransition(task, { action: "approve", payloadHash: task.payloadHash! }, "jt", LATER)).toEqual({ operation: "unchanged" });
  });

  test("an expired or closed packet cannot be approved", async () => {
    const task = await packet();
    expect((await rejection(() => resolveLanePacketTransition(task, { action: "approve", payloadHash: task.payloadHash! }, "jt", task.expiresAt!))).code).toBe("expired");
    const closed = { ...task, status: "archived", closureReason: { kind: "skipped" as const, closedAt: LATER, closedBy: "eve" as const } };
    expect((await rejection(() => resolveLanePacketTransition(closed, { action: "approve", payloadHash: task.payloadHash! }, "jt", LATER))).code).toBe("closed");
  });

  test("transitions refuse anything that is not a server-admitted lane packet, including outreach review cards", async () => {
    const outreachCard = { _id: "review-1", title: "Review outreach draft", status: "todo", outreachReview: { snapshotSha256: "6".repeat(64) } };
    const legacy = { _id: "legacy-1", title: "Legacy", status: "todo" };
    for (const task of [outreachCard, legacy]) {
      expect(await rejection(() => resolveLanePacketTransition(task as StoredLanePacketTask, { action: "skip" }, "jt", LATER))).toEqual({
        code: "not_found",
        message: "task is not a lane packet",
      });
    }
  });
});

describe("editing governed payload content re-hashes and invalidates approval", () => {
  test("a payload edit on an approved packet yields a new hash and returns approval to pending", async () => {
    const task = await approved();
    const edit = { pasteReadyPrompt: "A revised answer." };
    const governed = await resolveGenericLanePacketWrite(task, edit, LATER);
    const expectedHash = await hashLanePacketPayload({ ...task, ...edit });
    expect(expectedHash).not.toBe(task.payloadHash);
    expect(governed).toEqual({ payloadHash: expectedHash, approvalState: "pending", approvedPayloadHash: undefined, approvedAt: undefined });
  });

  test("the edited payload can then be approved only under its new hash", async () => {
    const task = await approved();
    const governed = await resolveGenericLanePacketWrite(task, { title: "Apply: revised" }, LATER);
    const edited = { ...task, title: "Apply: revised", ...governed } as StoredLanePacketTask;
    expect((await rejection(() => resolveLanePacketTransition(edited, { action: "approve", payloadHash: task.payloadHash! }, "jt", LATER))).code).toBe("conflict");
    expect(patchOf(await resolveLanePacketTransition(edited, { action: "approve", payloadHash: edited.payloadHash! }, "jt", LATER)).approvalState).toBe("approved");
  });

  test("an identical edit or a non-payload edit keeps the hash and the approval", async () => {
    const task = await approved();
    expect(await resolveGenericLanePacketWrite(task, { title: task.title }, LATER)).toEqual({});
    expect(await resolveGenericLanePacketWrite(task, { priority: "high" }, LATER)).toEqual({});
  });

  test("legacy generic tasks pass through untouched", async () => {
    expect(await resolveGenericLanePacketWrite({ _id: "legacy", title: "Legacy", status: "todo" }, { status: "done", title: "x" }, LATER)).toEqual({});
  });
});

describe("generic writes cannot forge completion, closure, or deletion", () => {
  test("generic Done on an external-action packet requires the evidence-backed transition", async () => {
    const task = await approved();
    expect(await rejection(() => resolveGenericLanePacketWrite(task, { status: "done" }, LATER))).toEqual({
      code: "transition_required",
      message: "external-action lane packets require evidence-backed completion",
    });
  });

  test("an internal packet (doneEvidenceType none) may be marked Done generically", async () => {
    const task = await packet(jobsPacketFixture({ doneEvidenceType: "none" }));
    expect(await resolveGenericLanePacketWrite(task, { status: "done" }, LATER)).toEqual({});
  });

  test("generic archive requires a typed closure reason", async () => {
    const task = await packet();
    expect(await rejection(() => resolveGenericLanePacketWrite(task, { status: "archived" }, LATER))).toEqual({
      code: "transition_required",
      message: "closing a lane packet requires a typed closure reason",
    });
  });

  test("closed and completed packets are immutable through generic writes", async () => {
    const task = await packet();
    const closed = { ...task, status: "archived", closureReason: { kind: "no-action" as const, closedAt: LATER, closedBy: "jt" as const } };
    const done = { ...task, status: "done" };
    for (const terminal of [closed, done]) {
      expect(await rejection(() => resolveGenericLanePacketWrite(terminal, { status: "todo" }, LATER))).toEqual({
        code: "closed",
        message: "closed lane packets are immutable",
      });
    }
  });

  test("the dedupe identity cannot change and generic tasks cannot claim the reserved prefix", async () => {
    const task = await packet();
    expect((await rejection(() => resolveGenericLanePacketWrite(task, { dedupeKey: "other" }, LATER))).code).toBe("invalid");
    expect((await rejection(() => resolveGenericLanePacketWrite({ _id: "legacy", status: "todo" }, { dedupeKey: "lane-packet:v1:jobs:x" }, LATER))).code).toBe("invalid");
    expect((await rejection(() => assertGenericDedupeKey("lane-packet:v1:jobs:x"))).code).toBe("invalid");
    expect(await rejection(() => assertGenericDedupeKey("nightly:abc"))).toEqual({ code: "none", message: "" });
    expect(await rejection(() => assertGenericDedupeKey(undefined))).toEqual({ code: "none", message: "" });
  });

  test("deleting a lane packet is refused; legacy deletes are unaffected", async () => {
    expect((await rejection(() => assertGenericLanePacketRemoval(null))).code).toBe("none");
    expect((await rejection(() => assertGenericLanePacketRemoval({ _id: "legacy", title: "Legacy" }))).code).toBe("none");
    expect(await rejection(async () => assertGenericLanePacketRemoval(await packet()))).toEqual({
      code: "transition_required",
      message: "closing a lane packet requires a typed closure reason",
    });
  });

  test("snooze cannot extend past expiry; the bounded snooze helper stops at expiry", async () => {
    const task = await packet();
    expect((await rejection(() => resolveGenericLanePacketWrite(task, { snoozedUntil: task.expiresAt! + 1 }, LATER))).code).toBe("invalid");
    expect(await resolveGenericLanePacketWrite(task, { snoozedUntil: task.expiresAt! }, LATER)).toEqual({});
    expect(lanePacketSnoozeUntil(task.expiresAt, LATER, 7)).toBe(task.expiresAt!);
    expect(lanePacketSnoozeUntil(LATER + 30 * DAY_MS, LATER, 7)).toBe(LATER + 7 * DAY_MS);
    expect(lanePacketSnoozeUntil(undefined, LATER, 7)).toBe(LATER + 7 * DAY_MS);
  });
});

describe("external-action Done requires typed evidence and may record an outcome pointer", () => {
  test("JT records matching evidence and an outcome pointer on an approved packet", async () => {
    const task = await approved();
    const fields = patchOf(await resolveLanePacketTransition(task, {
      action: "complete",
      evidence: { type: "application-ref", ref: "PORTAL-CONF-12345" },
      outcomeRef: { system: "job-tracker", id: "applications/synthetic-acme" },
    }, "jt", LATER));
    expect(fields).toEqual({
      status: "done",
      doneEvidence: { type: "application-ref", ref: "PORTAL-CONF-12345", recordedAt: LATER, recordedBy: "jt" },
      outcomeRef: { system: "job-tracker", id: "applications/synthetic-acme", recordedAt: LATER },
      updatedAt: LATER,
    });
  });

  test("without a supplied outcome pointer, none is fabricated", async () => {
    const task = await approved(linkedinPacketFixture());
    const fields = patchOf(await resolveLanePacketTransition(task, {
      action: "complete",
      evidence: { type: "post-url", ref: "https://www.linkedin.com/feed/update/urn:li:activity:1" },
    }, "jt", LATER));
    expect("outcomeRef" in fields).toBe(false);
  });

  test("evidence must match doneEvidenceType, be present, and be well-formed", async () => {
    const task = await approved(linkedinPacketFixture());
    const cases: Array<[LanePacketTransition, string]> = [
      [{ action: "complete", evidence: { type: "message-ref", ref: "msg-1" } }, "evidence type must match doneEvidenceType"],
      [{ action: "complete" }, "evidence is required for an external-action lane packet"],
      [{ action: "complete", evidence: { type: "post-url", ref: "not a url" } }, "post-url evidence must be an https URL"],
      [{ action: "complete", evidence: { type: "post-url", ref: "http://example.com/post" } }, "post-url evidence must be an https URL"],
    ];
    for (const [transition, message] of cases) {
      expect(await rejection(() => resolveLanePacketTransition(task, transition, "jt", LATER))).toEqual({ code: "invalid", message });
    }
  });

  test("completion requires approval of the current payload", async () => {
    const pending = await packet();
    expect(await rejection(() => resolveLanePacketTransition(pending, { action: "complete", evidence: { type: "application-ref", ref: "X-1" } }, "jt", LATER))).toEqual({
      code: "conflict",
      message: "approve the current payload before recording completion",
    });
    const drifted = { ...(await approved()), payloadHash: "9".repeat(64) };
    expect((await rejection(() => resolveLanePacketTransition(drifted, { action: "complete", evidence: { type: "application-ref", ref: "X-1" } }, "jt", LATER))).code).toBe("conflict");
  });

  test("a producer cannot record completion", async () => {
    const task = await approved();
    expect((await rejection(() => resolveLanePacketTransition(task, { action: "complete", evidence: { type: "application-ref", ref: "X-1" } }, "eve", LATER))).code).toBe("forbidden");
  });

  test("an internal packet completes without evidence and rejects stray evidence", async () => {
    const task = await packet(jobsPacketFixture({ doneEvidenceType: "none" }));
    expect(patchOf(await resolveLanePacketTransition(task, { action: "complete" }, "jt", LATER))).toEqual({ status: "done", updatedAt: LATER });
    expect(await rejection(() => resolveLanePacketTransition(task, { action: "complete", evidence: { type: "application-ref", ref: "X" } }, "jt", LATER))).toEqual({
      code: "invalid",
      message: "internal lane packets complete without evidence",
    });
  });

  test("a real outcome can still be recorded after expiry if the packet was approved and never closed", async () => {
    const task = await approved();
    const fields = patchOf(await resolveLanePacketTransition(task, { action: "complete", evidence: { type: "application-ref", ref: "X-1" } }, "jt", task.expiresAt! + DAY_MS));
    expect(fields.status).toBe("done");
  });
});

describe("reject, skip, expiry, and no-action need a typed closure reason and never fabricate an outcome", () => {
  test("a producer may skip; the closure is typed and carries no outcome or evidence", async () => {
    const task = await packet();
    const fields = patchOf(await resolveLanePacketTransition(task, { action: "skip", note: "Posting closed before review." }, "eve", LATER));
    expect(fields).toEqual({
      status: "archived",
      closureReason: { kind: "skipped", note: "Posting closed before review.", closedAt: LATER, closedBy: "eve" },
      updatedAt: LATER,
    });
  });

  test("JT closes with no-action", async () => {
    const task = await packet(linkedinPacketFixture());
    const fields = patchOf(await resolveLanePacketTransition(task, { action: "no-action" }, "jt", LATER));
    expect(fields).toEqual({ status: "archived", closureReason: { kind: "no-action", closedAt: LATER, closedBy: "jt" }, updatedAt: LATER });
  });

  test("JT rejects the reviewed payload; approval becomes rejected", async () => {
    const task = await packet();
    const fields = patchOf(await resolveLanePacketTransition(task, { action: "reject", payloadHash: task.payloadHash!, note: "Wrong seniority." }, "jt", LATER));
    expect(fields).toEqual({
      status: "archived",
      approvalState: "rejected",
      closureReason: { kind: "rejected", note: "Wrong seniority.", closedAt: LATER, closedBy: "jt" },
      updatedAt: LATER,
    });
    expect((await rejection(() => resolveLanePacketTransition(task, { action: "reject", payloadHash: task.payloadHash! }, "eve", LATER))).code).toBe("forbidden");
    expect((await rejection(() => resolveLanePacketTransition(task, { action: "reject", payloadHash: "0".repeat(64) }, "jt", LATER))).code).toBe("conflict");
  });

  test("a closed packet cannot be closed again", async () => {
    const task = await packet();
    const closed = { ...task, status: "archived", closureReason: { kind: "skipped" as const, closedAt: LATER, closedBy: "eve" as const } };
    expect((await rejection(() => resolveLanePacketTransition(closed, { action: "no-action" }, "jt", LATER))).code).toBe("closed");
  });

  test("expiry is server-only: it closes an open expired packet with a typed reason", async () => {
    const task = await packet();
    expect(resolveLanePacketExpiry(task, task.expiresAt! - 1)).toBe(null);
    expect(resolveLanePacketExpiry(task, task.expiresAt!)).toEqual({
      status: "archived",
      closureReason: { kind: "expired", closedAt: task.expiresAt, closedBy: "server" },
      updatedAt: task.expiresAt,
    });
    const done = { ...task, status: "done" };
    expect(resolveLanePacketExpiry(done, task.expiresAt! + 1)).toBe(null);
    expect(resolveLanePacketExpiry({ _id: "legacy", title: "Legacy", status: "todo" }, task.expiresAt! + 1)).toBe(null);
  });
});

describe("transition request validation", () => {
  test("accepts each action's exact shape", () => {
    expect(validateLanePacketTransition({ id: "t1", action: "approve", payloadHash: "a".repeat(64) })).toEqual({ id: "t1", action: "approve", payloadHash: "a".repeat(64) });
    expect(validateLanePacketTransition({ id: "t1", action: "skip" })).toEqual({ id: "t1", action: "skip" });
    expect(validateLanePacketTransition({ id: "t1", action: "complete", evidence: { type: "rsvp-ref", ref: "evt-1" }, outcomeRef: { system: "calendar", id: "evt-1", url: "https://example.com/e/1" } })).toEqual({
      id: "t1", action: "complete", evidence: { type: "rsvp-ref", ref: "evt-1" }, outcomeRef: { system: "calendar", id: "evt-1", url: "https://example.com/e/1" },
    });
  });

  test("rejects callers who try to type the expiry, stamp outcome times, or add fields", async () => {
    const bad = [
      { id: "t1", action: "expire" },
      { id: "t1", action: "approve" },
      { action: "skip" },
      { id: "t1", action: "skip", closureReason: { kind: "skipped" } },
      { id: "t1", action: "complete", outcomeRef: { system: "s", id: "i", recordedAt: 1 } },
      { id: "t1", action: "complete", evidence: { type: "none", ref: "x" } },
      { id: "t1", action: "no-action", note: "x".repeat(1001) },
      [],
    ];
    for (const input of bad) {
      expect((await rejection(() => validateLanePacketTransition(input))).code).toBe("invalid");
    }
  });
});
