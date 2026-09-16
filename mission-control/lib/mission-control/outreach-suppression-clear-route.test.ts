import { describe, expect, test } from "bun:test";
import { createOutreachSuppressionClearHandler } from "./outreach-suppression-clear-route";

describe("JT-bound dual-clear action", () => {
  test("accepts only reviewId, runs consulting first, then Mission Control with derived immutable data", async () => {
    const order: string[] = [];
    const handler = createOutreachSuppressionClearHandler({
      enabled: "true", trustedJtLogin: "jt@example.com", decisionCapability: "decision", reviewCapability: "review", readCapability: "read", authorityWriteCapability: "write",
      loadReview: async () => ({ suppressionBinding: { bindingHash: "a".repeat(64) } }),
      derive: async () => ({ consulting: { requestId: "consulting" }, missionControl: { requestId: "mission" } }) as any,
      recordConsulting: async (input: any) => { order.push(`consulting:${input.requestId}`); return { created: true, eventId: `suppression_event_${"1".repeat(20)}`, ownerRevision: "2".repeat(64), observedAt: "2026-09-16T14:00:00Z" }; },
      recordMissionControl: async (input: any) => { order.push(`mission:${input.requestId}`); return { created: true, event: { eventId: `suppression_event_${"3".repeat(20)}`, observedAt: "2026-09-16T14:00:01Z" }, ownerRevision: "4".repeat(64) }; },
    } as any);
    const response = await handler(new Request("http://localhost/api/tasks/outreach-suppression/clear", { method: "POST", headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com", "X-Outreach-Decision-Capability": "decision" }, body: JSON.stringify({ reviewId: "review_" + "1".repeat(20) }) }));
    expect(response.status).toBe(200);
    expect(order).toEqual(["consulting:consulting", "mission:mission"]);
    expect(await response.json()).toEqual({
      consulting: { eventId: `suppression_event_${"1".repeat(20)}`, ownerRevision: "2".repeat(64), observedAt: "2026-09-16T14:00:00Z" },
      missionControl: { eventId: `suppression_event_${"3".repeat(20)}`, ownerRevision: "4".repeat(64), observedAt: "2026-09-16T14:00:01Z" },
    });
  });

  test("disabled and unknown fields fail before owner calls", async () => {
    let calls = 0;
    const base = { trustedJtLogin: "jt@example.com", decisionCapability: "decision", reviewCapability: "review", readCapability: "read", authorityWriteCapability: "write", loadReview: async () => { calls++; }, derive: async () => ({}), recordConsulting: async () => { calls++; }, recordMissionControl: async () => { calls++; } } as any;
    const disabled = createOutreachSuppressionClearHandler({ ...base, enabled: undefined });
    const req = (body: unknown) => new Request("http://localhost/api/tasks/outreach-suppression/clear", { method: "POST", headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com", "X-Outreach-Decision-Capability": "decision" }, body: JSON.stringify(body) });
    expect((await disabled(req({ reviewId: "review_" + "1".repeat(20) }))).status).toBe(503);
    const enabled = createOutreachSuppressionClearHandler({ ...base, enabled: "true" });
    expect((await enabled(req({ reviewId: "review_" + "1".repeat(20), prospectId: "forged" }))).status).toBe(400);
    const malformed = await enabled(new Request("http://localhost/api/tasks/outreach-suppression/clear", { method: "POST", headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com", "X-Outreach-Decision-Capability": "decision" }, body: "{" }));
    expect(malformed.status).toBe(400);
    expect(calls).toBe(0);
  });

  test("rejects malformed owner success responses without exposing dependency data", async () => {
    const handler = createOutreachSuppressionClearHandler({
      enabled: "true", trustedJtLogin: "jt@example.com", decisionCapability: "decision", reviewCapability: "review", readCapability: "read", authorityWriteCapability: "write",
      loadReview: async () => ({ suppressionBinding: { bindingHash: "a".repeat(64) } }),
      derive: async () => ({ consulting: {}, missionControl: {} }) as any,
      recordConsulting: async () => ({ created: true, eventId: "leaked@example.com" }),
      recordMissionControl: async () => ({ secret: "do-not-leak" }),
    } as any);
    const response = await handler(new Request("http://localhost/api/tasks/outreach-suppression/clear", { method: "POST", headers: { "Content-Type": "application/json", "Tailscale-User-Login": "jt@example.com", "X-Outreach-Decision-Capability": "decision" }, body: JSON.stringify({ reviewId: "review_" + "1".repeat(20) }) }));
    expect(response.status).toBe(500);
    expect(await response.json()).toEqual({ error: "outreach suppression clear failed" });
  });
});
