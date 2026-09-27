import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import {
  admitLanePacket,
  appendFeedback,
  create,
  createOnlyByDedupeKey,
  expireDueLanePackets,
  remove,
  setFocus,
  transitionLanePacket,
  update,
  updatePipelineStage,
  updateStatus,
  upsertByDedupeKey,
} from "../../convex/tasks";
import {
  approvalState as schemaApprovalState,
  closureReason as schemaClosureReason,
  doneEvidenceType as schemaDoneEvidenceType,
  growthLane as schemaGrowthLane,
} from "../../convex/schema";
import { ConvexTestDb, testCtx, withEnv } from "./convex-test-db";
import { APPROVAL_STATES, CLOSURE_KINDS, DONE_EVIDENCE_TYPES, GROWTH_LANES, LANE_PACKET_GOVERNED_FIELDS } from "./lane-packet";
import { FIXTURE_NOW, jobsPacketFixture, linkedinPacketFixture } from "./lane-packet-fixtures";

type Handler = (context: any, args: any) => Promise<any>;
const handler = (fn: unknown) => (fn as { _handler: Handler })._handler;
const exportedArgs = (fn: unknown) => JSON.stringify((fn as { exportArgs: () => string }).exportArgs());

const PRODUCER = "lane-producer-test-value";
const DECISION = "lane-decision-test-value";
const CONFIGURED = { LANE_PACKET_CAPABILITY: PRODUCER, LANE_PACKET_DECISION_CAPABILITY: DECISION };

async function message(run: () => Promise<unknown>): Promise<string> {
  try {
    await run();
    return "";
  } catch (error) {
    return error instanceof Error ? error.message : String(error);
  }
}

function withClock<T>(now: number, run: () => Promise<T>): Promise<T> {
  const realNow = Date.now;
  Date.now = () => now;
  return run().finally(() => { Date.now = realNow; });
}

async function admit(db: ConvexTestDb, packet: unknown = jobsPacketFixture(), capability = PRODUCER) {
  return withClock(FIXTURE_NOW, () => withEnv(CONFIGURED, () => handler(admitLanePacket)(testCtx(db), { packet, capability })));
}

async function transition(db: ConvexTestDb, id: string, body: Record<string, unknown>, actor: "jt" | "eve", capability: string, now = FIXTURE_NOW + 60_000) {
  return withClock(now, () => withEnv(CONFIGURED, () => handler(transitionLanePacket)(testCtx(db), { id, transition: body, actor, capability })));
}

function seedOutreachReviewCard(db: ConvexTestDb): string {
  return db.seed({
    title: "Review outreach draft: candidate-1 / cohort-2 / cycle 1",
    status: "todo", assignee: "jt", priority: "high", candidateId: "candidate-1", cohortId: "cohort-2",
    draftSha256: "a".repeat(64), dedupeKey: `outreach-review:cohort-2:candidate-1:${"b".repeat(64)}`,
    outreachReview: { candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: "a".repeat(64), snapshotSha256: "b".repeat(64), admittedBy: "server", reviewCycle: 1 },
    createdAt: FIXTURE_NOW - 1000, updatedAt: FIXTURE_NOW - 1000,
  });
}

describe("admitLanePacket: capability-protected, create-only, idempotent", () => {
  test("fails closed when capabilities are unconfigured, blank, or equal", async () => {
    const db = new ConvexTestDb();
    const call = (env: Record<string, string | undefined>) => withEnv(env, () => handler(admitLanePacket)(testCtx(db), { packet: jobsPacketFixture(), capability: PRODUCER }));
    expect(await message(() => call({ LANE_PACKET_CAPABILITY: undefined, LANE_PACKET_DECISION_CAPABILITY: undefined }))).toBe("LANE_PACKET_NOT_CONFIGURED");
    expect(await message(() => call({ LANE_PACKET_CAPABILITY: PRODUCER, LANE_PACKET_DECISION_CAPABILITY: "  " }))).toBe("LANE_PACKET_NOT_CONFIGURED");
    expect(await message(() => call({ LANE_PACKET_CAPABILITY: PRODUCER, LANE_PACKET_DECISION_CAPABILITY: PRODUCER }))).toBe("LANE_PACKET_NOT_CONFIGURED");
    expect(db.writes).toBe(0);
  });

  test("rejects a wrong capability and the decision capability", async () => {
    const db = new ConvexTestDb();
    expect(await message(() => admit(db, jobsPacketFixture(), "wrong"))).toBe("LANE_PACKET_UNAUTHORIZED");
    expect(await message(() => admit(db, jobsPacketFixture(), DECISION))).toBe("LANE_PACKET_UNAUTHORIZED");
    expect(db.writes).toBe(0);
  });

  test("admits one Jobs packet and one LinkedIn packet; exact retries are idempotent and write nothing", async () => {
    const db = new ConvexTestDb();
    const jobs = await admit(db, jobsPacketFixture());
    const linkedin = await admit(db, linkedinPacketFixture());
    expect(jobs).toMatchObject({ created: true, approvalState: "pending", dedupeKey: `lane-packet:v1:jobs:${jobsPacketFixture().dedupeKey}` });
    expect(linkedin).toMatchObject({ created: true, approvalState: "pending", dedupeKey: `lane-packet:v1:linkedin:${linkedinPacketFixture().dedupeKey}` });
    expect(db.writes).toBe(2);

    const jobsRetry = await admit(db, jobsPacketFixture());
    const linkedinRetry = await admit(db, linkedinPacketFixture());
    expect(jobsRetry).toEqual({ ...jobs, created: false });
    expect(linkedinRetry).toEqual({ ...linkedin, created: false });
    expect(db.writes).toBe(2);
    expect(db.rows).toHaveLength(2);

    const stored = db.snapshot(jobs.taskId)!;
    expect(stored).toMatchObject({ packetSchema: "lane-packet-v1", growthLane: "jobs", status: "todo", assignee: "jt", approvalState: "pending" });
    for (const absent of ["outreachReview", "outreachDecision", "candidateId", "cohortId", "outcomeRef", "closureReason", "doneEvidence"]) {
      expect(absent in stored).toBe(false);
    }
  });

  test("re-validates in Convex, so a direct call cannot forge governed state", async () => {
    const db = new ConvexTestDb();
    expect(await message(() => admit(db, { ...jobsPacketFixture(), approvalState: "approved" }))).toBe("LANE_PACKET_INVALID");
    expect(await message(() => admit(db, { ...jobsPacketFixture(), outcomeRef: { system: "x", id: "y" } }))).toBe("LANE_PACKET_INVALID");
    expect(db.writes).toBe(0);
  });

  test("a changed payload for an open packet conflicts instead of replacing it", async () => {
    const db = new ConvexTestDb();
    await admit(db);
    expect(await message(() => admit(db, jobsPacketFixture({ title: "Apply: a different title" })))).toBe("LANE_PACKET_CONFLICT");
    expect(db.rows).toHaveLength(1);
  });

  test("never creates or mutates an outreach review snapshot or decision", async () => {
    const db = new ConvexTestDb();
    const reviewId = seedOutreachReviewCard(db);
    const before = db.snapshot(reviewId);
    expect(await message(() => admit(db, { ...jobsPacketFixture({ lane: "outreach" }), outreachReview: {} }))).toBe("LANE_PACKET_INVALID");
    const outreachLane = await admit(db, jobsPacketFixture({ lane: "outreach", doneEvidenceType: "message-ref", dedupeKey: "eve:warm-intro:1" }));
    expect(outreachLane.created).toBe(true);
    expect(db.snapshot(reviewId)).toEqual(before);
    const stored = db.snapshot(outreachLane.taskId)!;
    expect("outreachReview" in stored || "outreachDecision" in stored).toBe(false);
    expect(await message(() => transition(db, reviewId, { action: "skip" }, "jt", DECISION))).toBe("LANE_PACKET_NOT_FOUND");
    expect(db.snapshot(reviewId)).toEqual(before);
  });
});

describe("transitionLanePacket: actor-bound capabilities", () => {
  test("JT approves only with the server-held decision capability", async () => {
    const db = new ConvexTestDb();
    const { taskId, payloadHash } = await admit(db);
    expect(await message(() => transition(db, taskId, { action: "approve", payloadHash }, "jt", PRODUCER))).toBe("LANE_PACKET_UNAUTHORIZED");
    expect(await message(() => transition(db, taskId, { action: "approve", payloadHash }, "eve", PRODUCER))).toBe("LANE_PACKET_FORBIDDEN");
    expect(await message(() => transition(db, taskId, { action: "approve", payloadHash }, "eve", DECISION))).toBe("LANE_PACKET_UNAUTHORIZED");
    expect(db.snapshot(taskId)!.approvalState).toBe("pending");
    const result = await transition(db, taskId, { action: "approve", payloadHash }, "jt", DECISION);
    expect(result).toMatchObject({ taskId, approvalState: "approved", changed: true });
    expect(db.snapshot(taskId)).toMatchObject({ approvalState: "approved", approvedPayloadHash: payloadHash });
  });

  test("evidence-backed Done writes typed evidence and the supplied outcome pointer", async () => {
    const db = new ConvexTestDb();
    const { taskId, payloadHash } = await admit(db, linkedinPacketFixture());
    await transition(db, taskId, { action: "approve", payloadHash }, "jt", DECISION);
    expect(await message(() => transition(db, taskId, { action: "complete" }, "jt", DECISION))).toBe("LANE_PACKET_INVALID");
    await transition(db, taskId, { action: "complete", evidence: { type: "post-url", ref: "https://www.linkedin.com/feed/update/urn:li:activity:7" }, outcomeRef: { system: "notion-content-calendar", id: "synthetic-row-7" } }, "jt", DECISION);
    expect(db.snapshot(taskId)).toMatchObject({
      status: "done",
      doneEvidence: { type: "post-url", ref: "https://www.linkedin.com/feed/update/urn:li:activity:7", recordedBy: "jt" },
      outcomeRef: { system: "notion-content-calendar", id: "synthetic-row-7" },
    });
  });

  test("a producer can close with a typed skip reason and nothing else", async () => {
    const db = new ConvexTestDb();
    const { taskId } = await admit(db);
    await transition(db, taskId, { action: "skip", note: "Role closed." }, "eve", PRODUCER);
    const stored = db.snapshot(taskId)!;
    expect(stored).toMatchObject({ status: "archived", closureReason: { kind: "skipped", note: "Role closed.", closedBy: "eve" } });
    expect("outcomeRef" in stored || "doneEvidence" in stored).toBe(false);
  });
});

describe("schema literals match the contract enums", () => {
  const literals = (validator: unknown): unknown[] => {
    const json = (validator as { json: { type: string; value: Array<{ type: string; value: unknown }> } }).json;
    return json.value.flatMap((member) => (member.type === "union" ? literals({ json: member }) : [member.value]));
  };

  test("growthLane, doneEvidenceType, approvalState, and closure kinds cannot drift", () => {
    expect(literals(schemaGrowthLane)).toEqual([...GROWTH_LANES]);
    expect(literals(schemaDoneEvidenceType)).toEqual([...DONE_EVIDENCE_TYPES]);
    expect(literals(schemaApprovalState)).toEqual([...APPROVAL_STATES]);
    const closureKind = (schemaClosureReason as unknown as { json: { value: Record<string, { fieldType: unknown }> } }).json.value.kind.fieldType;
    expect(literals({ json: closureKind })).toEqual([...CLOSURE_KINDS]);
  });
});

describe("lane-packet Convex code is isolated from outreach authority", () => {
  const tasksSource = readFileSync(fileURLToPath(new URL("../../convex/tasks.ts", import.meta.url)), "utf8");
  const between = (start: string, end: string) => tasksSource.slice(tasksSource.indexOf(start), tasksSource.indexOf(end));

  test("the lane-packet capability boundary reads only lane-packet capabilities", () => {
    const boundary = between("async function assertLanePacketCapability", "function lanePacketErrorCode");
    expect(boundary).toContain("process.env.LANE_PACKET_CAPABILITY");
    expect(boundary).toContain("process.env.LANE_PACKET_DECISION_CAPABILITY");
    expect(boundary.includes("OUTREACH_")).toBe(false);
  });

  test("admission, transition, and expiry never reference outreach state or capabilities", () => {
    const lanePacketMutations = between("export const admitLanePacket", "export const createOutreachReviewAuthority");
    expect(lanePacketMutations).toContain("export const transitionLanePacket");
    expect(lanePacketMutations).toContain("export const expireDueLanePackets");
    for (const forbidden of ["OUTREACH_", "outreachReview", "outreachDecision", "resolveOutreach", "assertDistinctServerCapability"]) {
      expect(lanePacketMutations.includes(forbidden)).toBe(false);
    }
  });
});

describe("generic task mutations cannot bypass the governed transitions", () => {
  test("generic mutation validators do not accept any governed envelope field", () => {
    for (const fn of [create, upsertByDedupeKey, createOnlyByDedupeKey, update]) {
      const args = exportedArgs(fn);
      for (const field of LANE_PACKET_GOVERNED_FIELDS) {
        expect(args.includes(`"${field}"`)).toBe(false);
      }
    }
  });

  test("editing payload through generic update re-hashes and invalidates approval", async () => {
    const db = new ConvexTestDb();
    const { taskId, payloadHash } = await admit(db);
    await transition(db, taskId, { action: "approve", payloadHash }, "jt", DECISION);
    await handler(update)(testCtx(db), { id: taskId, pasteReadyPrompt: "A revised answer." });
    const stored = db.snapshot(taskId)!;
    expect(stored.pasteReadyPrompt).toBe("A revised answer.");
    expect(stored.payloadHash).not.toBe(payloadHash);
    expect(stored.admittedPayloadHash).toBe(payloadHash);
    expect(stored.approvalState).toBe("pending");
    expect("approvedPayloadHash" in stored || "approvedAt" in stored).toBe(false);
  });

  test("generic done, archive, pipeline-stage archive, and delete are refused without a write", async () => {
    const db = new ConvexTestDb();
    const { taskId } = await admit(db);
    const writes = db.writes;
    expect(await message(() => handler(update)(testCtx(db), { id: taskId, status: "done" }))).toBe("LANE_PACKET_TRANSITION_REQUIRED");
    expect(await message(() => handler(updateStatus)(testCtx(db), { id: taskId, status: "done" }))).toBe("LANE_PACKET_TRANSITION_REQUIRED");
    expect(await message(() => handler(updateStatus)(testCtx(db), { id: taskId, status: "archived" }))).toBe("LANE_PACKET_TRANSITION_REQUIRED");
    expect(await message(() => handler(updatePipelineStage)(testCtx(db), { id: taskId, pipelineStage: "sent", status: "archived" }))).toBe("LANE_PACKET_TRANSITION_REQUIRED");
    expect(await message(() => handler(remove)(testCtx(db), { id: taskId }))).toBe("LANE_PACKET_TRANSITION_REQUIRED");
    expect(db.writes).toBe(writes);
    expect(db.snapshot(taskId)!.status).toBe("todo");
  });

  test("closed packets are immutable to generic writes", async () => {
    const db = new ConvexTestDb();
    const { taskId } = await admit(db);
    await transition(db, taskId, { action: "no-action" }, "jt", DECISION);
    expect(await message(() => handler(updateStatus)(testCtx(db), { id: taskId, status: "todo" }))).toBe("LANE_PACKET_CLOSED");
  });

  test("generic writers cannot claim the reserved lane-packet dedupe namespace", async () => {
    const db = new ConvexTestDb();
    const base = { title: "Generic", status: "todo", assignee: "eve", priority: "low" };
    const reserved = "lane-packet:v1:jobs:x";
    expect(await message(() => handler(create)(testCtx(db), { ...base, dedupeKey: reserved }))).toBe("LANE_PACKET_INVALID");
    expect(await message(() => handler(upsertByDedupeKey)(testCtx(db), { ...base, dedupeKey: reserved }))).toBe("LANE_PACKET_INVALID");
    expect(await message(() => handler(createOnlyByDedupeKey)(testCtx(db), { ...base, dedupeKey: reserved }))).toBe("LANE_PACKET_INVALID");
    expect(db.writes).toBe(0);
  });

  test("generic upsert never patches a lane packet, even one stored under an unreserved key", async () => {
    const db = new ConvexTestDb();
    const { taskId } = await admit(db);
    const row = db.rows.find((candidate) => candidate._id === taskId)!;
    row.dedupeKey = "legacy-unreserved-key";
    const before = db.snapshot(taskId);
    expect(await message(() => handler(upsertByDedupeKey)(testCtx(db), {
      title: "Overwrite", status: "done", assignee: "eve", priority: "low", dedupeKey: "legacy-unreserved-key",
    }))).toBe("LANE_PACKET_TRANSITION_REQUIRED");
    expect(db.snapshot(taskId)).toEqual(before);
  });

  test("feedback still appends to a lane packet without touching its hash or approval", async () => {
    const db = new ConvexTestDb();
    const { taskId, payloadHash } = await admit(db);
    await withClock(FIXTURE_NOW + 1, () => handler(appendFeedback)(testCtx(db), { id: taskId, body: "Tighten the second step.", author: "jt" }));
    expect(db.snapshot(taskId)).toMatchObject({ payloadHash, approvalState: "pending" });
    expect(db.snapshot(taskId)!.feedback).toHaveLength(1);
  });

  test("legacy generic tasks keep their existing behavior", async () => {
    const db = new ConvexTestDb();
    const id = db.seed({ title: "Legacy", status: "todo", assignee: "jt", priority: "medium", createdAt: 1, updatedAt: 1 });
    await handler(update)(testCtx(db), { id, title: "Legacy renamed", status: "done" });
    await handler(remove)(testCtx(db), { id });
    expect(db.rows).toHaveLength(0);
  });
});

describe("expireDueLanePackets: automatic, typed expiry", () => {
  test("closes only open packets past expiry with a server-typed reason", async () => {
    const db = new ConvexTestDb();
    const expiring = await admit(db, linkedinPacketFixture());
    const later = await admit(db, jobsPacketFixture({ expiresAt: FIXTURE_NOW + 10 * 24 * 60 * 60 * 1000 }));
    const legacy = db.seed({ title: "Legacy", status: "todo", assignee: "jt", priority: "medium", createdAt: 1, updatedAt: 1 });
    const at = linkedinPacketFixture().expiresAt;
    const result = await withClock(at, () => handler(expireDueLanePackets)(testCtx(db), {}));
    expect(result).toEqual({ expired: 1 });
    expect(db.snapshot(expiring.taskId)).toMatchObject({ status: "archived", closureReason: { kind: "expired", closedAt: at, closedBy: "server" } });
    expect("outcomeRef" in db.snapshot(expiring.taskId)!).toBe(false);
    expect(db.snapshot(later.taskId)!.status).toBe("todo");
    expect(db.snapshot(legacy)!.status).toBe("todo");
  });
});

describe("setFocus carries the focus-row mandate and lane capacity", () => {
  test("stores and patches mandate and laneCapacity; legacy calls leave them untouched", async () => {
    const db = new ConvexTestDb();
    const id = await handler(setFocus)(testCtx(db), {
      weekOf: "2026-09-28", projects: ["Consulting"], gate: 10000,
      mandate: "none", laneCapacity: [{ lane: "linkedin", minutes: 30 }, { lane: "jobs", minutes: 45 }],
    });
    expect(db.snapshot(id)).toMatchObject({ mandate: "none", laneCapacity: [{ lane: "linkedin", minutes: 30 }, { lane: "jobs", minutes: 45 }] });
    await handler(setFocus)(testCtx(db), { weekOf: "2026-09-28", projects: ["Consulting", "Job Market"], gate: 10000 });
    expect(db.snapshot(id)).toMatchObject({ projects: ["Consulting", "Job Market"], mandate: "none" });
  });

  test("rejects duplicate lanes and non-whole or out-of-range minutes", async () => {
    const db = new ConvexTestDb();
    for (const laneCapacity of [
      [{ lane: "jobs", minutes: 30 }, { lane: "jobs", minutes: 10 }],
      [{ lane: "jobs", minutes: -1 }],
      [{ lane: "jobs", minutes: 12.5 }],
      [{ lane: "jobs", minutes: 1441 }],
    ]) {
      expect(await message(() => handler(setFocus)(testCtx(db), { weekOf: "2026-09-28", projects: [], gate: 0, laneCapacity }))).toBe("invalid laneCapacity");
    }
    expect(db.writes).toBe(0);
  });
});
