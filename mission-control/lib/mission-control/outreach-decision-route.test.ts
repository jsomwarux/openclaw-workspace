import { describe, expect, test } from "bun:test";
import { createOutreachDecisionHandlers } from "./outreach-decision-route";

const SHA = "a".repeat(64);

describe("outreach decision API contract", () => {
  test("POST records only the server-owned JT decision", async () => {
    let received: Record<string, unknown> | null = null;
    const handlers = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: "server-secret",
      peerCapability: "review-secret",
      decide: async (input) => {
        received = input;
        const { capability: _capability, ...decisionInput } = input;
        return {
          decision: { ...decisionInput, decidedBy: "jt", decidedAt: 123 },
          created: true,
        };
      },
      lookup: async () => ({ authorized: false, state: "absent" }),
    });
    const response = await handlers.POST(new Request("http://localhost/api/tasks/outreach-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com" },
      body: JSON.stringify({
        taskId: "task-1",
        candidateId: "candidate-1",
        draftSha256: SHA,
        decision: "approve",
      }),
    }));
    expect(response.status).toBe(200);
    expect(received).toEqual({ taskId: "task-1", candidateId: "candidate-1", draftSha256: SHA, decision: "approve", capability: "server-secret" });
    expect(await response.json()).toEqual({
      decision: { taskId: "task-1", candidateId: "candidate-1", draftSha256: SHA, decision: "approve", decidedBy: "jt", decidedAt: 123 },
      created: true,
    });
  });

  test("POST rejects caller-authored server fields before mutation", async () => {
    let calls = 0;
    const handlers = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: "server-secret",
      peerCapability: "review-secret",
      decide: async () => { calls += 1; throw new Error("not reached"); },
      lookup: async () => ({ authorized: false, state: "absent" }),
    });
    for (const extra of [
      { decidedBy: "jt" },
      { decidedAt: 123 },
      { outreachDecision: { decision: "approve" } },
      { capability: "caller-authored" },
    ]) {
      const response = await handlers.POST(new Request("http://localhost/api/tasks/outreach-decision", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com" },
        body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: SHA, decision: "approve", ...extra }),
      }));
      expect(response.status).toBe(400);
    }
    expect(calls).toBe(0);
  });

  test("POST maps immutable conflicts to 409 and malformed input to 400", async () => {
    const handlers = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: "server-secret",
      peerCapability: "review-secret",
      decide: async () => { throw new Error("outreach decision is immutable; create a new versioned task"); },
      lookup: async () => ({ authorized: false, state: "absent" }),
    });
    const conflict = await handlers.POST(new Request("http://localhost/api/tasks/outreach-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com" },
      body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: SHA, decision: "reject" }),
    }));
    expect(conflict.status).toBe(409);

    const malformed = await handlers.POST(new Request("http://localhost/api/tasks/outreach-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com" },
      body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: "bad", decision: "approve" }),
    }));
    expect(malformed.status).toBe(400);
  });

  test("GET returns exact approved, rejected, or absent fail-closed lookup", async () => {
    const calls: unknown[] = [];
    const handlers = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: "server-secret",
      peerCapability: "review-secret",
      decide: async () => { throw new Error("not reached"); },
      lookup: async (input) => {
        calls.push(input);
        return { authorized: true, state: "approved", taskId: "task-1" };
      },
    });
    const response = await handlers.GET(new Request(`http://localhost/api/tasks/outreach-decision?candidateId=candidate-1&draftSha256=${SHA}`));
    expect(response.status).toBe(200);
    expect(calls).toEqual([{ candidateId: "candidate-1", draftSha256: SHA }]);
    expect(await response.json()).toEqual({ authorized: true, state: "approved", taskId: "task-1" });
  });

  test("GET rejects malformed or missing identity without querying", async () => {
    let calls = 0;
    const handlers = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: "server-secret",
      peerCapability: "review-secret",
      decide: async () => { throw new Error("not reached"); },
      lookup: async () => { calls += 1; return { authorized: false, state: "absent" }; },
    });
    const response = await handlers.GET(new Request("http://localhost/api/tasks/outreach-decision?candidateId=candidate-1"));
    expect(response.status).toBe(400);
    expect(calls).toBe(0);
  });

  test("POST fails closed for missing configuration, identity, or a mismatched identity", async () => {
    let calls = 0;
    const request = (login?: string) => new Request("http://localhost/api/tasks/outreach-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json", ...(login ? { "Tailscale-User-Login": login } : {}) },
      body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: SHA, decision: "approve" }),
    });
    const missingConfig = createOutreachDecisionHandlers({
      trustedJtLogin: undefined,
      serverCapability: "server-secret",
      peerCapability: "review-secret",
      decide: async () => { calls += 1; return {}; },
      lookup: async () => ({}),
    });
    expect((await missingConfig.POST(request("jt@example.com"))).status).toBe(503);

    const configured = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: "server-secret",
      peerCapability: "review-secret",
      decide: async () => { calls += 1; return {}; },
      lookup: async () => ({}),
    });
    expect((await configured.POST(request())).status).toBe(401);
    expect((await configured.POST(request("attacker@example.com"))).status).toBe(401);

    const colliding = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: "same-secret",
      peerCapability: "same-secret",
      decide: async () => { calls += 1; return {}; },
      lookup: async () => ({}),
    });
    expect((await colliding.POST(request("jt@example.com"))).status).toBe(503);
    for (const [serverCapability, peerCapability] of [
      ["", "review-secret"],
      ["server-secret", ""],
      ["server-secret", undefined],
    ] as const) {
      const invalid = createOutreachDecisionHandlers({
        trustedJtLogin: "jt@example.com",
        serverCapability,
        peerCapability,
        decide: async () => { calls += 1; return {}; },
        lookup: async () => ({}),
      });
      expect((await invalid.POST(request("jt@example.com"))).status).toBe(503);
    }
    expect(calls).toBe(0);
  });

  test("never leaks arbitrary decision or lookup dependency errors", async () => {
    const leakedCapability = "decision-secret-do-not-return";
    const handlers = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: leakedCapability,
      peerCapability: "review-secret",
      decide: async () => { throw new Error(`Convex decision failed capability=${leakedCapability}`); },
      lookup: async () => { throw new Error(`Convex lookup failed capability=${leakedCapability}`); },
    });
    const postResponse = await handlers.POST(new Request("http://localhost/api/tasks/outreach-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com" },
      body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: SHA, decision: "approve" }),
    }));
    const postText = await postResponse.text();
    expect(postResponse.status).toBe(500);
    expect(JSON.parse(postText)).toEqual({ error: "outreach decision request failed" });
    expect(postText).not.toContain(leakedCapability);
    expect(postText).not.toContain("Convex");

    const getResponse = await handlers.GET(new Request(`http://localhost/api/tasks/outreach-decision?candidateId=candidate-1&draftSha256=${SHA}`));
    const getText = await getResponse.text();
    expect(getResponse.status).toBe(500);
    expect(JSON.parse(getText)).toEqual({ error: "outreach decision request failed" });
    expect(getText).not.toContain(leakedCapability);
    expect(getText).not.toContain("Convex");
  });

  test("does not echo an allowlisted conflict even when it equals the capability", async () => {
    const capability = "outreach decision is immutable; create a new versioned task";
    const handlers = createOutreachDecisionHandlers({
      trustedJtLogin: "jt@example.com",
      serverCapability: capability,
      peerCapability: "review-secret",
      decide: async () => { throw new Error(capability); },
      lookup: async () => ({ authorized: false, state: "absent" }),
    });
    const response = await handlers.POST(new Request("http://localhost/api/tasks/outreach-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com" },
      body: JSON.stringify({ taskId: "task-1", candidateId: "candidate-1", draftSha256: SHA, decision: "approve" }),
    }));
    const text = await response.text();
    expect(response.status).toBe(409);
    expect(JSON.parse(text)).toEqual({ error: "outreach decision conflict" });
    expect(text).not.toContain(capability);
  });
});
