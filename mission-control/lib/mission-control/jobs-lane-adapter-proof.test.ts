import { describe, expect, test } from "bun:test";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { admitLanePacket, transitionLanePacket } from "../../convex/tasks";
import { ConvexTestDb, testCtx, withEnv } from "./convex-test-db";
import type { LanePacketSubmission } from "./lane-packet";

type Handler = (context: any, args: any) => Promise<any>;
const handler = (fn: unknown) => (fn as { _handler: Handler })._handler;

const PRODUCER = "jobs-proof-producer-test-value";
const DECISION = "jobs-proof-decision-test-value";
const CONFIGURED = {
  LANE_PACKET_CAPABILITY: PRODUCER,
  LANE_PACKET_DECISION_CAPABILITY: DECISION,
};
const NOW = Date.UTC(2026, 8, 28, 13, 0, 0);
const FIXTURE_PATH = fileURLToPath(
  new URL("./fixtures/jobs/decagon-agent-development-manager.packet.json", import.meta.url),
);
const RECEIPT_PATH = fileURLToPath(
  new URL("./fixtures/jobs/decagon-agent-development-manager.receipt.json", import.meta.url),
);
const EXPECTED_PACKET_SHA256 = "48448f87b3f5d8dec47bb2ee8113a3c58b5fa63bbfc6883f86c18f4ecdff516d";
const EXPECTED_RECEIPT_SHA256 = "7d0af58b8bdc14a69b651370a6f78277035f4e9e1d0ae9c10ac304d28043f150";
const EXPECTED_PAYLOAD_HASH = "cd252d0ca23652adc7a7395ac7dafa97c7e56323dbc92609da3a6eb257644974";

function withClock<T>(now: number, run: () => Promise<T>): Promise<T> {
  const realNow = Date.now;
  Date.now = () => now;
  return run().finally(() => { Date.now = realNow; });
}

function loadPacket(): LanePacketSubmission {
  return JSON.parse(readFileSync(FIXTURE_PATH, "utf8")) as LanePacketSubmission;
}

async function admit(db: ConvexTestDb, packet = loadPacket()) {
  return withClock(NOW, () => withEnv(CONFIGURED, () =>
    handler(admitLanePacket)(testCtx(db), { packet, capability: PRODUCER })));
}

async function transition(
  db: ConvexTestDb,
  id: string,
  body: Record<string, unknown>,
  actor: "jt" | "eve",
  capability: string,
  now: number,
) {
  return withClock(now, () => withEnv(CONFIGURED, () =>
    handler(transitionLanePacket)(testCtx(db), { id, transition: body, actor, capability })));
}

describe("Decagon Jobs packet → Mission Control governed lifecycle", () => {
  test("fixture is the exact accepted posted:false Jobs packet", () => {
    const bytes = readFileSync(FIXTURE_PATH);
    expect(createHash("sha256").update(bytes).digest("hex")).toBe(EXPECTED_PACKET_SHA256);
    expect(loadPacket()).toMatchObject({
      lane: "jobs",
      sourceSystem: "job-market-agent",
      dedupeKey: "job-market-agent:role:ashby:decagon:476e3152-3f9a-48ea-89bd-30516bccead7",
      payloadHash: EXPECTED_PAYLOAD_HASH,
      doneEvidenceType: "application-ref",
    });

    const receiptBytes = readFileSync(RECEIPT_PATH);
    expect(createHash("sha256").update(receiptBytes).digest("hex")).toBe(EXPECTED_RECEIPT_SHA256);
    expect(JSON.parse(receiptBytes.toString("utf8"))).toMatchObject({
      packetSha256: EXPECTED_PACKET_SHA256,
      payloadHash: EXPECTED_PAYLOAD_HASH,
      posted: false,
    });
  });

  test("admits once, deduplicates exact replay, completes with typed test evidence, and still deduplicates after closure", async () => {
    const db = new ConvexTestDb();
    const first = await admit(db);
    expect(first).toMatchObject({ created: true, payloadHash: EXPECTED_PAYLOAD_HASH, approvalState: "pending" });
    expect(db.rows).toHaveLength(1);

    const writesBeforeReplay = db.writes;
    const replay = await admit(db);
    expect(replay).toEqual({ ...first, created: false });
    expect(db.rows).toHaveLength(1);
    expect(db.writes).toBe(writesBeforeReplay);

    await transition(db, first.taskId, { action: "approve", payloadHash: EXPECTED_PAYLOAD_HASH }, "jt", DECISION, NOW + 60_000);
    await transition(db, first.taskId, {
      action: "complete",
      evidence: { type: "application-ref", ref: "TEST-ONLY:decagon-application-confirmation" },
      outcomeRef: { system: "job-market-agent", id: "TEST-ONLY:job-outcomes:decagon-applied" },
    }, "jt", DECISION, NOW + 120_000);

    expect(db.snapshot(first.taskId)).toMatchObject({
      status: "done",
      approvedPayloadHash: EXPECTED_PAYLOAD_HASH,
      doneEvidence: {
        type: "application-ref",
        ref: "TEST-ONLY:decagon-application-confirmation",
        recordedBy: "jt",
      },
      outcomeRef: {
        system: "job-market-agent",
        id: "TEST-ONLY:job-outcomes:decagon-applied",
      },
    });

    const writesBeforeClosedReplay = db.writes;
    const replayAfterClosure = await admit(db);
    expect(replayAfterClosure).toEqual({ ...first, created: false, approvalState: "approved" });
    expect(db.rows).toHaveLength(1);
    expect(db.writes).toBe(writesBeforeClosedReplay);
  });

  test("the same exact packet can close as typed no-action without fabricated evidence or outcome", async () => {
    const db = new ConvexTestDb();
    const admitted = await admit(db);
    await transition(db, admitted.taskId, {
      action: "no-action",
      note: "TEST-ONLY lifecycle proof; no application was submitted.",
    }, "eve", PRODUCER, NOW + 60_000);

    const stored = db.snapshot(admitted.taskId)!;
    expect(stored).toMatchObject({
      status: "archived",
      closureReason: {
        kind: "no-action",
        note: "TEST-ONLY lifecycle proof; no application was submitted.",
        closedBy: "eve",
      },
    });
    expect("doneEvidence" in stored).toBe(false);
    expect("outcomeRef" in stored).toBe(false);
  });
});
