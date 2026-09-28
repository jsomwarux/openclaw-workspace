import { describe, expect, test } from "bun:test";
import { createLanePacketHandlers, lanePacketDependencyErrorResponse } from "./lane-packet-route";
import { LANE_PACKET_GOVERNED_FIELDS } from "./lane-packet";
import { FIXTURE_NOW, jobsPacketFixture } from "./lane-packet-fixtures";

process.env.NEXT_PUBLIC_CONVEX_URL ??= "http://127.0.0.1:3210";

const PRODUCER = "lane-producer-test-value";
const DECISION = "lane-decision-test-value";
const JT_LOGIN = "jt@example.test";

type Calls = { admit: unknown[]; transition: unknown[] };

function dependencies(overrides: Record<string, unknown> = {}, calls: Calls = { admit: [], transition: [] }) {
  return {
    producerCapability: PRODUCER,
    decisionCapability: DECISION,
    trustedJtLogin: JT_LOGIN,
    now: () => FIXTURE_NOW,
    admit: async (input: unknown) => {
      calls.admit.push(input);
      return { taskId: "task-1", created: true, dedupeKey: "lane-packet:v1:jobs:k", payloadHash: "a".repeat(64), approvalState: "pending" as const };
    },
    transition: async (input: unknown) => {
      calls.transition.push(input);
      return { taskId: "task-1", changed: true, status: "todo", approvalState: "approved", payloadHash: "a".repeat(64) };
    },
    ...overrides,
  };
}

function post(body: unknown, headers: Record<string, string> = { "X-Lane-Packet-Capability": PRODUCER }) {
  return new Request("http://localhost/api/tasks/lane-packet", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...headers },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

function patch(body: unknown, headers: Record<string, string>) {
  return new Request("http://localhost/api/tasks/lane-packet", {
    method: "PATCH",
    headers: { "Content-Type": "application/json", ...headers },
    body: JSON.stringify(body),
  });
}

describe("POST /api/tasks/lane-packet admission", () => {
  test("admits a valid packet with the producer capability and reports create-only semantics", async () => {
    const calls: Calls = { admit: [], transition: [] };
    const { POST } = createLanePacketHandlers(dependencies({}, calls));
    const response = await POST(post(jobsPacketFixture()));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({
      taskId: "task-1", created: true, dedupeKey: "lane-packet:v1:jobs:k", payloadHash: "a".repeat(64),
      approvalState: "pending", writeMode: "create-only",
    });
    expect(calls.admit).toHaveLength(1);
    expect(calls.admit[0]).toMatchObject({ capability: PRODUCER, packet: { lane: "jobs", title: jobsPacketFixture().title } });
  });

  test("fails closed with 503 when capabilities are missing, blank, or equal, before reading the body", async () => {
    for (const overrides of [
      { producerCapability: undefined },
      { decisionCapability: " " },
      { decisionCapability: PRODUCER },
    ]) {
      const calls: Calls = { admit: [], transition: [] };
      const { POST } = createLanePacketHandlers(dependencies(overrides, calls));
      const response = await POST(post("{not-json"));
      expect(response.status).toBe(503);
      expect(await response.json()).toEqual({ error: "lane packet authority is not configured" });
      expect(calls.admit).toHaveLength(0);
    }
  });

  test("returns 401 for a missing or wrong capability, including the decision capability", async () => {
    const headerSets: Array<Record<string, string>> = [{}, { "X-Lane-Packet-Capability": "wrong" }, { "X-Lane-Packet-Capability": DECISION }];
    for (const headers of headerSets) {
      const calls: Calls = { admit: [], transition: [] };
      const { POST } = createLanePacketHandlers(dependencies({}, calls));
      const response = await POST(post(jobsPacketFixture(), headers));
      expect(response.status).toBe(401);
      expect(await response.json()).toEqual({ error: "lane packet capability required" });
      expect(calls.admit).toHaveLength(0);
    }
  });

  test("returns 400 with a fixed message for invalid JSON, forged state, and outreach fields", async () => {
    const { POST } = createLanePacketHandlers(dependencies());
    expect((await POST(post("{not-json"))).status).toBe(400);
    const forged = await POST(post({ ...jobsPacketFixture(), approvalState: "approved" }));
    expect(forged.status).toBe(400);
    expect(await forged.json()).toEqual({ error: "governed lane packet fields are server-derived" });
    const outreach = await POST(post({ ...jobsPacketFixture(), outreachDecision: { decision: "approve" } }));
    expect(await outreach.json()).toEqual({ error: "outreach review and decision state requires the specialized outreach routes" });
  });

  test("maps Convex failures to enumerated responses without leaking details", async () => {
    const cases: Array<[string, number, string]> = [
      ["[CONVEX M(tasks:admitLanePacket)] Uncaught Error: LANE_PACKET_CONFLICT at handler", 409, "lane packet conflict"],
      ["Uncaught Error: LANE_PACKET_INVALID", 400, "invalid lane packet request"],
      ["Uncaught Error: LANE_PACKET_NOT_CONFIGURED", 503, "lane packet authority is not configured"],
      ["Uncaught Error: LANE_PACKET_UNAUTHORIZED", 401, "lane packet capability required"],
      ["connect ECONNREFUSED 127.0.0.1:3210 secret-host-detail", 500, "lane packet request failed"],
    ];
    for (const [message, status, error] of cases) {
      const { POST } = createLanePacketHandlers(dependencies({ admit: async () => { throw new Error(message); } }));
      const response = await POST(post(jobsPacketFixture()));
      expect(response.status).toBe(status);
      expect(await response.json()).toEqual({ error });
    }
  });
});

describe("PATCH /api/tasks/lane-packet transitions", () => {
  const approve = { id: "task-1", action: "approve", payloadHash: "a".repeat(64) };

  test("JT decisions require the Tailscale JT identity and use the server-held decision capability", async () => {
    const calls: Calls = { admit: [], transition: [] };
    const { PATCH } = createLanePacketHandlers(dependencies({}, calls));
    const response = await PATCH(patch(approve, { "Tailscale-User-Login": JT_LOGIN }));
    expect(response.status).toBe(200);
    expect(calls.transition[0]).toEqual({ id: "task-1", transition: { action: "approve", payloadHash: "a".repeat(64) }, actor: "jt", capability: DECISION });
  });

  test("identity failures are 401/403, and a missing JT login config is 503", async () => {
    const { PATCH } = createLanePacketHandlers(dependencies());
    expect((await PATCH(patch(approve, {}))).status).toBe(401);
    expect((await PATCH(patch(approve, { "Tailscale-User-Login": "someone-else@example.test" }))).status).toBe(403);
    const unconfigured = createLanePacketHandlers(dependencies({ trustedJtLogin: undefined }));
    expect((await unconfigured.PATCH(patch(approve, { "Tailscale-User-Login": JT_LOGIN }))).status).toBe(503);
    const equalCaps = createLanePacketHandlers(dependencies({ decisionCapability: PRODUCER }));
    expect((await equalCaps.PATCH(patch(approve, { "Tailscale-User-Login": JT_LOGIN }))).status).toBe(503);
  });

  test("a producer capability may only skip or close with no action, as actor eve", async () => {
    const calls: Calls = { admit: [], transition: [] };
    const { PATCH } = createLanePacketHandlers(dependencies({}, calls));
    const skip = await PATCH(patch({ id: "task-1", action: "skip", note: "Role closed." }, { "X-Lane-Packet-Capability": PRODUCER }));
    expect(skip.status).toBe(200);
    expect(calls.transition[0]).toEqual({ id: "task-1", transition: { action: "skip", note: "Role closed." }, actor: "eve", capability: PRODUCER });

    for (const body of [approve, { id: "task-1", action: "complete", evidence: { type: "application-ref", ref: "X" } }, { id: "task-1", action: "reject", payloadHash: "a".repeat(64) }]) {
      const response = await PATCH(patch(body, { "X-Lane-Packet-Capability": PRODUCER }));
      expect(response.status).toBe(403);
      expect(await response.json()).toEqual({ error: "producers may only skip or close lane packets with no action" });
    }
    expect(calls.transition).toHaveLength(1);
    expect((await PATCH(patch({ id: "task-1", action: "skip" }, { "X-Lane-Packet-Capability": "wrong" }))).status).toBe(401);
  });

  test("a producer header never falls through to JT identity", async () => {
    const calls: Calls = { admit: [], transition: [] };
    const { PATCH } = createLanePacketHandlers(dependencies({}, calls));
    const response = await PATCH(patch(approve, { "X-Lane-Packet-Capability": PRODUCER, "Tailscale-User-Login": JT_LOGIN }));
    expect(response.status).toBe(403);
    expect(calls.transition).toHaveLength(0);
  });

  test("maps transition failures to enumerated responses", async () => {
    const cases: Array<[string, number, string]> = [
      ["LANE_PACKET_NOT_FOUND", 404, "lane packet not found"],
      ["LANE_PACKET_CONFLICT", 409, "lane packet conflict"],
      ["LANE_PACKET_CLOSED", 409, "lane packet is already closed"],
      ["LANE_PACKET_EXPIRED", 409, "lane packet expired"],
      ["LANE_PACKET_FORBIDDEN", 403, "lane packet action forbidden"],
      ["LANE_PACKET_INVALID", 400, "invalid lane packet request"],
      ["something else entirely", 500, "lane packet request failed"],
    ];
    for (const [message, status, error] of cases) {
      const { PATCH } = createLanePacketHandlers(dependencies({ transition: async () => { throw new Error(`Uncaught Error: ${message}`); } }));
      const response = await PATCH(patch(approve, { "Tailscale-User-Login": JT_LOGIN }));
      expect(response.status).toBe(status);
      expect(await response.json()).toEqual({ error });
    }
  });

  test("generic-path guard errors map to 409/400 and unknown errors are not swallowed", () => {
    expect(lanePacketDependencyErrorResponse(new Error("Uncaught Error: LANE_PACKET_TRANSITION_REQUIRED"))?.status).toBe(409);
    expect(lanePacketDependencyErrorResponse(new Error("Uncaught Error: LANE_PACKET_CLOSED"))?.status).toBe(409);
    expect(lanePacketDependencyErrorResponse(new Error("Uncaught Error: LANE_PACKET_INVALID"))?.status).toBe(400);
    expect(lanePacketDependencyErrorResponse(new Error("Task not found: x"))).toBe(null);
  });
});

describe("generic /api/tasks rejects the governed envelope", () => {
  async function loadHandlers() {
    return import("../../app/api/tasks/route");
  }

  test("POST and PATCH return 400 for any envelope field before touching Convex", async () => {
    const { POST, PATCH } = await loadHandlers();
    for (const field of LANE_PACKET_GOVERNED_FIELDS) {
      const created = await POST(new Request("http://localhost/api/tasks", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: "Generic", [field]: "x" }),
      }));
      expect(created.status).toBe(400);
      expect(await created.json()).toEqual({ error: "lane packet envelope fields require /api/tasks/lane-packet" });
      const patched = await PATCH(new Request("http://localhost/api/tasks", {
        method: "PATCH", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: "task-1", [field]: "x" }),
      }));
      expect(patched.status).toBe(400);
    }
  });

  test("POST rejects the reserved lane-packet dedupe namespace", async () => {
    const { POST } = await loadHandlers();
    const response = await POST(new Request("http://localhost/api/tasks?mode=create-only", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "Generic", dedupeKey: "lane-packet:v1:jobs:x" }),
    }));
    expect(response.status).toBe(400);
    expect(await response.json()).toEqual({ error: "dedupeKey must not use the reserved lane-packet prefix" });
  });
});
