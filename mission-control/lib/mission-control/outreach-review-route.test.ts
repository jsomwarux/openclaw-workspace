import { describe, expect, test } from "bun:test";
import { createOutreachReviewPostHandler } from "./outreach-review-route";

const SHA = "a".repeat(64);
const body = {
  title: "Review exact draft",
  dedupeKey: `outreach:candidate-1:${SHA}`,
  candidateId: "candidate-1",
  draftSha256: SHA,
};

function request(payload: Record<string, unknown> = body, capability?: string) {
  return new Request("http://localhost/api/tasks/outreach-review", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(capability ? { "X-Outreach-Review-Capability": capability } : {}),
    },
    body: JSON.stringify(payload),
  });
}

describe("dedicated outreach review admission route", () => {
  test("passes the configured server capability to the atomic admission mutation", async () => {
    let received: Record<string, unknown> | undefined;
    const post = createOutreachReviewPostHandler({
      serverCapability: "server-secret",
      peerCapability: "decision-secret",
      admit: async (input) => { received = input; return { id: "task-1", created: true }; },
    });
    const response = await post(request({ ...body, status: "done", assignee: "eve", priority: "low" }, "server-secret"));
    expect(response.status).toBe(200);
    expect(received).toMatchObject({ ...body, capability: "server-secret", status: "todo", assignee: "jt", priority: "high" });
    expect(await response.json()).toEqual({ id: "task-1", created: true, success: true, writeMode: "create-only", reviewMode: "outreach-review" });
  });

  test("fails closed for missing server configuration or caller capability", async () => {
    let calls = 0;
    const unconfigured = createOutreachReviewPostHandler({
      serverCapability: undefined,
      peerCapability: "decision-secret",
      admit: async () => { calls += 1; return { id: "bad", created: true }; },
    });
    expect((await unconfigured(request(body, "server-secret"))).status).toBe(503);

    const configured = createOutreachReviewPostHandler({
      serverCapability: "server-secret",
      peerCapability: "decision-secret",
      admit: async () => { calls += 1; return { id: "bad", created: true }; },
    });
    expect((await configured(request(body))).status).toBe(401);
    expect((await configured(request(body, "wrong"))).status).toBe(401);

    const colliding = createOutreachReviewPostHandler({
      serverCapability: "same-secret",
      peerCapability: "same-secret",
      admit: async () => { calls += 1; return { id: "bad", created: true }; },
    });
    expect((await colliding(request(body, "same-secret"))).status).toBe(503);
    for (const [serverCapability, peerCapability] of [
      ["", "decision-secret"],
      ["server-secret", ""],
      ["server-secret", undefined],
    ] as const) {
      const invalid = createOutreachReviewPostHandler({
        serverCapability,
        peerCapability,
        admit: async () => { calls += 1; return { id: "bad", created: true }; },
      });
      expect((await invalid(request(body, serverCapability || "server-secret"))).status).toBe(503);
    }
    expect(calls).toBe(0);
  });

  test("rejects caller-authored eligibility and malformed identity before mutation", async () => {
    let calls = 0;
    const post = createOutreachReviewPostHandler({
      serverCapability: "server-secret",
      peerCapability: "decision-secret",
      admit: async () => { calls += 1; return { id: "bad", created: true }; },
    });
    expect((await post(request({ ...body, outreachReview: { admittedBy: "server" } }, "server-secret"))).status).toBe(400);
    expect((await post(request({ ...body, capability: "caller-authored" }, "server-secret"))).status).toBe(400);
    expect((await post(request({ ...body, draftSha256: "bad" }, "server-secret"))).status).toBe(400);
    expect(calls).toBe(0);
  });
});
