import { describe, expect, test } from "bun:test";
import { createOutreachSuppressionHandlers } from "./outreach-suppression-route";

const DECISION = "decision-secret";
const READ = "authority-read-secret";
const REVIEW = "review-secret";
const WRITE = "authority-write-secret";
const tuple = { prospectId: "prospect.alpha", organizationFactId: "fact-org:alpha", channelFingerprint: "a".repeat(64) };
const submission = { schemaVersion: "outreach-suppression-event-v1", requestId: "suppression_request_" + "b".repeat(20), ...tuple, state: "clear", evidenceToken: "evidence_" + "c".repeat(64) };

function deps(overrides: Record<string, unknown> = {}) {
  return {
    enabled: "true", trustedJtLogin: "jt@example.com", decisionCapability: DECISION,
    readCapability: READ, reviewCapability: REVIEW, authorityWriteCapability: WRITE,
    record: async () => ({ created: true, event: {} }), query: async () => ({ clear: false }),
    ...overrides,
  } as any;
}
function post(capability = DECISION, login = "jt@example.com", body: unknown = submission) {
  return new Request("http://localhost/api/tasks/outreach-suppression", { method: "POST", headers: { "Content-Type": "application/json", "Tailscale-User-Login": login, "X-Outreach-Decision-Capability": capability }, body: JSON.stringify(body) });
}
function get(capability = READ) {
  const query = new URLSearchParams(tuple);
  return new Request(`http://localhost/api/tasks/outreach-suppression?${query}`, { headers: { "X-Outreach-Review-Authority-Read-Capability": capability } });
}

describe("suppression owner HTTP boundary", () => {
  test("disabled fails 503 before capability or dependency access", async () => {
    let calls = 0;
    const handlers = createOutreachSuppressionHandlers(deps({ enabled: undefined, record: async () => { calls++; }, query: async () => { calls++; } }));
    for (const response of [await handlers.POST(post("wrong", "attacker@example.com")), await handlers.GET(get("wrong"))]) {
      expect(response.status).toBe(503);
      expect(await response.json()).toEqual({ error: "outreach suppression owner is not configured" });
    }
    expect(calls).toBe(0);
  });

  test("POST is JT-only and decision-write-only; GET is read-only capability", async () => {
    let records = 0; let queries = 0;
    const handlers = createOutreachSuppressionHandlers(deps({ record: async () => { records++; return { created: true, event: {} }; }, query: async () => { queries++; return { clear: false }; } }));
    expect((await handlers.POST(post(READ))).status).toBe(401);
    expect((await handlers.POST(post(DECISION, "attacker@example.com"))).status).toBe(403);
    expect((await handlers.GET(get(DECISION))).status).toBe(401);
    expect((await handlers.POST(post())).status).toBe(200);
    expect((await handlers.GET(get())).status).toBe(200);
    expect({ records, queries }).toEqual({ records: 1, queries: 1 });
  });

  test("rejects caller actor/time/server fields and sanitizes dependency errors", async () => {
    let calls = 0;
    const handlers = createOutreachSuppressionHandlers(deps({ record: async () => { calls++; throw new Error("secret downstream"); } }));
    for (const body of [{ ...submission, actorId: "jt" }, { ...submission, observedAt: "2026-09-16T00:00:00Z" }, { ...submission, sequence: 1 }]) {
      expect((await handlers.POST(post(DECISION, "jt@example.com", body))).status).toBe(400);
    }
    const failed = await handlers.POST(post());
    expect(failed.status).toBe(500);
    expect(await failed.json()).toEqual({ error: "outreach suppression request failed" });
    expect(calls).toBe(1);
  });
});
