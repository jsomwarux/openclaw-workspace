import { describe, expect, test } from "bun:test";
import { createOutreachPreSendReceiptHandlers } from "./outreach-pre-send-receipt-route";
import { hashSuppressionBinding } from "./outreach-suppression-binding";

async function submission() {
  const raw = { schemaVersion: "outreach-suppression-binding-v1" as const, repository: "owner/repo", commitSha: "a".repeat(40), gatePath: "gate.json", gateBlobOid: "1".repeat(40), gateBlobSha256: "b".repeat(64), gateArtifactHash: "c".repeat(64), admissionCommitSha: "d".repeat(40), admissionPath: "admission/candidate.json", admissionBlobOid: "2".repeat(40), admissionBlobSha256: "e".repeat(64), channelAttestationId: `channel_${"f".repeat(20)}`, channelOwnerRevision: "1".repeat(64), prospectId: "prospect.alpha", organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64) };
  return { schemaVersion: "outreach-pre-send-receipt-v1", requestId: "pre_send_request_" + "3".repeat(20), suppressionBinding: { ...raw, bindingHash: await hashSuppressionBinding(raw) }, missionControlEventId: "suppression_event_" + "4".repeat(20), missionControlOwnerRevision: "5".repeat(64), missionControlObservedAt: "2026-09-16T14:00:00Z", consultingEventId: "suppression_event_" + "6".repeat(20), consultingOwnerRevision: "7".repeat(64), consultingObservedAt: "2026-09-16T14:00:01Z", reviewId: "review_" + "8".repeat(20), snapshotSha256: "9".repeat(64), draftSha256: "a".repeat(64), decisionSha256: "b".repeat(64), messageStage: "M1" };
}
function deps(overrides: Record<string, unknown> = {}) { return { enabled: "true", reviewCapability: "review", readCapability: "read", decisionCapability: "decision", authorityWriteCapability: "write", create: async () => ({ created: true, receipt: {} }), lookup: async () => ({ found: false }), ...overrides } as any; }

describe("pre-send receipt HTTP owner", () => {
  test("disabled fails before authentication or dependencies", async () => {
    let calls = 0; const handlers = createOutreachPreSendReceiptHandlers(deps({ enabled: undefined, create: async () => { calls++; }, lookup: async () => { calls++; } }));
    const response = await handlers.POST(new Request("http://localhost/api/tasks/outreach-pre-send-receipt", { method: "POST", body: "{}" }));
    expect(response.status).toBe(503); expect(calls).toBe(0);
  });
  test("POST uses review write and GET uses authority read; swapped caps fail", async () => {
    const body = await submission(); let writes = 0; let reads = 0;
    const handlers = createOutreachPreSendReceiptHandlers(deps({ create: async () => { writes++; return { created: true, receipt: {} }; }, lookup: async () => { reads++; return { found: false }; } }));
    const post = (cap: string) => new Request("http://localhost/api/tasks/outreach-pre-send-receipt", { method: "POST", headers: { "Content-Type": "application/json", "X-Outreach-Review-Capability": cap }, body: JSON.stringify(body) });
    const get = (cap: string) => new Request(`http://localhost/api/tasks/outreach-pre-send-receipt?preSendReceiptId=pre_send_${"c".repeat(20)}`, { headers: { "X-Outreach-Review-Authority-Read-Capability": cap } });
    expect((await handlers.POST(post("read"))).status).toBe(401); expect((await handlers.GET(get("review"))).status).toBe(401);
    expect((await handlers.POST(post("review"))).status).toBe(200); expect((await handlers.GET(get("read"))).status).toBe(200);
    expect({ writes, reads }).toEqual({ writes: 1, reads: 1 });
  });
});
