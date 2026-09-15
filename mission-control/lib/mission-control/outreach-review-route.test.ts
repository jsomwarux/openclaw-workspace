import { describe, expect, test } from "bun:test";
import { createOutreachReviewHandlers } from "./outreach-review-route";

const SHA = "a".repeat(64);
const COMMIT = "b".repeat(40);
const capability = "review-secret";
const bind = (path: string) => ({ repository: "owner/repo", commitSha: COMMIT, path, blobSha256: SHA });
const body = {
  candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: SHA,
  subject: "Subject", body: "Exact draft", verifierReport: "VERDICT: CONFIRM",
  reviewAuthorityId: "jt", verifierActorId: "verifier-1",
  gitBindings: { evidence: bind("evidence.json"), policy: bind("policy.json"), gate: bind("gate.json"), draft: bind("draft.txt"), verifier: bind("verify.md") },
};

function postRequest(payload: unknown = body, token?: string) {
  return new Request("http://localhost/api/tasks/outreach-review", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(token ? { "X-Outreach-Review-Capability": token } : {}) },
    body: JSON.stringify(payload),
  });
}

function dependencies(overrides: Record<string, unknown> = {}) {
  return {
    serverCapability: capability,
    peerCapability: "decision-secret",
    admit: async () => ({ taskId: "task-1", created: true, reviewCycle: 1 as const, snapshotSha256: "c".repeat(64) }),
    lookup: async () => ({ candidateId: "candidate-1", cohortId: "cohort-2", reviewCount: 0, remainingCycles: 2, latest: null }),
    ...overrides,
  };
}

describe("outreach review owner API", () => {
  test("POST accepts only the typed snapshot and returns the exact response", async () => {
    let received: unknown;
    const handlers = createOutreachReviewHandlers(dependencies({ admit: async (input: unknown) => {
      received = input;
      return { taskId: "task-1", created: true, reviewCycle: 1, snapshotSha256: "c".repeat(64) };
    } }));
    const response = await handlers.POST(postRequest(body, capability));
    expect(response.status).toBe(200);
    expect(received).toEqual({ ...body, capability });
    expect(await response.json()).toEqual({ taskId: "task-1", created: true, reviewCycle: 1, snapshotSha256: "c".repeat(64) });
  });

  test("POST rejects dropped, unknown, server-owned, and oversized fields before mutation", async () => {
    let calls = 0;
    const handlers = createOutreachReviewHandlers(dependencies({ admit: async () => { calls += 1; return {}; } }));
    for (const payload of [
      { ...body, subject: undefined },
      { ...body, title: "forged display" },
      { ...body, reviewCycle: 1 },
      { ...body, snapshotSha256: SHA },
    ]) {
      const response = await handlers.POST(postRequest(payload, capability));
      expect(response.status).toBe(400);
      expect(await response.json()).toEqual({ error: "invalid outreach review request" });
    }
    const oversized = await handlers.POST(postRequest({ ...body, body: "x".repeat(20_001) }, capability));
    expect(oversized.status).toBe(413);
    expect(await oversized.json()).toEqual({ error: "outreach review content too large" });
    expect(calls).toBe(0);
  });

  test("POST and GET require the distinct review capability", async () => {
    let calls = 0;
    const handlers = createOutreachReviewHandlers(dependencies({
      admit: async () => { calls += 1; return {}; }, lookup: async () => { calls += 1; return {}; },
    }));
    expect((await handlers.POST(postRequest(body))).status).toBe(401);
    expect((await handlers.GET(new Request("http://localhost/api/tasks/outreach-review?candidateId=candidate-1&cohortId=cohort-2"))).status).toBe(401);
    const collision = createOutreachReviewHandlers(dependencies({ serverCapability: "same", peerCapability: "same" }));
    expect((await collision.POST(postRequest(body, "same"))).status).toBe(503);
    expect(calls).toBe(0);
  });

  test("GET returns exact count state without review prose", async () => {
    let received: unknown;
    const state = { candidateId: "candidate-1", cohortId: "cohort-2", reviewCount: 1, remainingCycles: 1, latest: { taskId: "task-1", draftSha256: SHA, snapshotSha256: "c".repeat(64), reviewCycle: 1, decided: false } };
    const handlers = createOutreachReviewHandlers(dependencies({ lookup: async (input: unknown) => { received = input; return state; } }));
    const response = await handlers.GET(new Request("http://localhost/api/tasks/outreach-review?candidateId=candidate-1&cohortId=cohort-2", { headers: { "X-Outreach-Review-Capability": capability } }));
    expect(response.status).toBe(200);
    expect(received).toEqual({ candidateId: "candidate-1", cohortId: "cohort-2", capability });
    expect(await response.json()).toEqual(state);
  });

  test("maps stable conflicts and never leaks arbitrary POST or GET dependency errors", async () => {
    const cycle = createOutreachReviewHandlers(dependencies({ admit: async () => { throw new Error("OUTREACH_REVIEW_CYCLE_LIMIT"); } }));
    const cycleResponse = await cycle.POST(postRequest(body, capability));
    expect(cycleResponse.status).toBe(409);
    expect(await cycleResponse.json()).toEqual({ error: "outreach review cycle limit reached" });

    const corrupt = createOutreachReviewHandlers(dependencies({ lookup: async () => { throw new Error("OUTREACH_REVIEW_AUTHORITY_CORRUPT"); } }));
    const corruptResponse = await corrupt.GET(new Request("http://localhost/api/tasks/outreach-review?candidateId=candidate-1&cohortId=cohort-2", { headers: { "X-Outreach-Review-Capability": capability } }));
    expect(corruptResponse.status).toBe(409);
    expect(await corruptResponse.json()).toEqual({ error: "outreach review authority state is corrupt" });

    const secret = "review-secret-do-not-leak";
    const leaking = createOutreachReviewHandlers(dependencies({
      serverCapability: secret,
      admit: async () => { throw new Error(`Convex ${secret}`); },
      lookup: async () => { throw new Error(`Convex ${secret}`); },
    }));
    for (const response of [
      await leaking.POST(postRequest(body, secret)),
      await leaking.GET(new Request("http://localhost/api/tasks/outreach-review?candidateId=candidate-1&cohortId=cohort-2", { headers: { "X-Outreach-Review-Capability": secret } })),
    ]) {
      const text = await response.text();
      expect(response.status).toBe(500);
      expect(JSON.parse(text)).toEqual({ error: "outreach review request failed" });
      expect(text).not.toContain(secret);
    }
  });
});
