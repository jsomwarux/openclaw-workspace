import { describe, expect, test } from "bun:test";
import { createOutreachDecisionHandlers } from "./outreach-decision-route";

const DRAFT = "a".repeat(64);
const SNAPSHOT = "b".repeat(64);
const capability = "decision-secret";

function dependencies(overrides: Record<string, unknown> = {}) {
  return {
    trustedJtLogin: "jt@example.com",
    serverCapability: capability,
    peerCapability: "review-secret",
    decide: async () => ({ decision: { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve", decidedBy: "jt", decidedAt: 123 }, created: true }),
    lookup: async () => ({ authorized: false, state: "pending", taskId: "task-1" }),
    ...overrides,
  };
}

function postRequest(payload: Record<string, unknown> = {}, login = "jt@example.com") {
  return new Request("http://localhost/api/tasks/outreach-decision", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Tailscale-User-Login": login },
    body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve", ...payload }),
  });
}

function getRequest(token = capability, snapshot = SNAPSHOT) {
  return new Request(`http://localhost/api/tasks/outreach-decision?candidateId=candidate-1&draftSha256=${DRAFT}&snapshotSha256=${snapshot}`, {
    headers: { "X-Outreach-Decision-Capability": token },
  });
}

describe("outreach decision API contract", () => {
  test("POST records only the server-owned exact JT decision", async () => {
    let received: unknown;
    const handlers = createOutreachDecisionHandlers(dependencies({ decide: async (input: unknown) => {
      received = input;
      return { decision: { candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve", decidedBy: "jt", decidedAt: 123 }, created: true };
    } }));
    const response = await handlers.POST(postRequest());
    expect(response.status).toBe(200);
    expect(received).toEqual({ taskId: "task-1", candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve", capability });
  });

  test("POST rejects caller authority and missing snapshot before mutation", async () => {
    let calls = 0;
    const handlers = createOutreachDecisionHandlers(dependencies({ decide: async () => { calls += 1; return {}; } }));
    for (const payload of [{ decidedBy: "jt" }, { capability: "forged" }, { snapshotSha256: "" }, { decision: "maybe" }]) {
      const response = await handlers.POST(postRequest(payload));
      expect(response.status).toBe(400);
      expect(await response.json()).toEqual({ error: "invalid outreach decision request" });
    }
    expect(calls).toBe(0);
  });

  test("GET requires the decision capability and returns exact state", async () => {
    let received: unknown;
    const handlers = createOutreachDecisionHandlers(dependencies({ lookup: async (input: unknown) => { received = input; return { authorized: false, state: "pending", taskId: "task-1" }; } }));
    expect((await handlers.GET(getRequest("wrong"))).status).toBe(401);
    const response = await handlers.GET(getRequest());
    expect(response.status).toBe(200);
    expect(received).toEqual({ candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, capability });
    expect(await response.json()).toEqual({ authorized: false, state: "pending", taskId: "task-1" });
  });

  test("POST requires JT identity and distinguishes missing, forbidden, and unconfigured", async () => {
    const handlers = createOutreachDecisionHandlers(dependencies());
    const missing = new Request("http://localhost/api/tasks/outreach-decision", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: DRAFT, snapshotSha256: SNAPSHOT, decision: "approve" }) });
    expect((await handlers.POST(missing)).status).toBe(401);
    expect((await handlers.POST(postRequest({}, "attacker@example.com"))).status).toBe(403);
    const unconfigured = createOutreachDecisionHandlers(dependencies({ trustedJtLogin: undefined }));
    const response = await unconfigured.POST(postRequest());
    expect(response.status).toBe(503);
    expect(await response.json()).toEqual({ error: "outreach authority is not configured" });
  });

  test("maps not-found and immutable codes without exposing dependency text", async () => {
    for (const [message, status, body] of [
      ["OUTREACH_REVIEW_NOT_FOUND", 404, { error: "outreach review not found" }],
      ["OUTREACH_DECISION_CONFLICT", 409, { error: "outreach decision conflict" }],
    ] as const) {
      const handlers = createOutreachDecisionHandlers(dependencies({ decide: async () => { throw new Error(message); } }));
      const response = await handlers.POST(postRequest());
      expect(response.status).toBe(status);
      expect(await response.json()).toEqual(body);
    }
  });

  test("never leaks arbitrary decision or lookup dependency errors", async () => {
    const secret = "decision-secret-do-not-leak";
    const handlers = createOutreachDecisionHandlers(dependencies({
      serverCapability: secret,
      decide: async () => { throw new Error(`Convex ${secret}`); },
      lookup: async () => { throw new Error(`Convex ${secret}`); },
    }));
    for (const response of [await handlers.POST(postRequest()), await handlers.GET(getRequest(secret))]) {
      const text = await response.text();
      expect(response.status).toBe(500);
      expect(JSON.parse(text)).toEqual({ error: "outreach decision request failed" });
      expect(text).not.toContain(secret);
    }
  });
});
