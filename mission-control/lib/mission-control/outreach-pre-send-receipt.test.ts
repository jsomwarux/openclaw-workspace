import { describe, expect, test } from "bun:test";
import { hashSuppressionBinding } from "./outreach-suppression-binding";
import { resolvePreSendReceiptAdmission, resolvePreSendReceiptLookup } from "./outreach-pre-send-receipt";

async function input() {
  const raw = { schemaVersion: "outreach-suppression-binding-v1" as const, repository: "owner/repo", commitSha: "a".repeat(40), gatePath: "gate.json", gateBlobSha256: "b".repeat(64), gateArtifactHash: "c".repeat(64), admissionCommitSha: "d".repeat(40), admissionPath: "admission/candidate.json", admissionBlobSha256: "e".repeat(64), channelAttestationId: `channel_${"f".repeat(20)}`, channelOwnerRevision: "1".repeat(64), prospectId: "prospect.alpha", organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64) };
  return { schemaVersion: "outreach-pre-send-receipt-v1" as const, requestId: "pre_send_request_" + "3".repeat(20), suppressionBinding: { ...raw, bindingHash: await hashSuppressionBinding(raw) }, missionControlEventId: "suppression_event_" + "4".repeat(20), missionControlOwnerRevision: "5".repeat(64), missionControlObservedAt: "2026-09-16T14:00:00Z", consultingEventId: "suppression_event_" + "6".repeat(20), consultingOwnerRevision: "7".repeat(64), consultingObservedAt: "2026-09-16T14:00:01Z", reviewId: "review_" + "8".repeat(20), snapshotSha256: "9".repeat(64), draftSha256: "a".repeat(64), decisionSha256: "b".repeat(64), messageStage: "M1" as const };
}

describe("immutable pre-send receipt owner", () => {
  test("creates an immutable server receipt and exact retry is idempotent", async () => {
    const submission = await input();
    const created = await resolvePreSendReceiptAdmission([], submission, 123, "c".repeat(20));
    expect(created.operation).toBe("create");
    if (created.operation !== "create") throw new Error("expected create");
    expect(created.receipt.preSendReceiptId).toBe("pre_send_" + "c".repeat(20));
    expect(/^[a-f0-9]{64}$/.test(created.receipt.receiptHash)).toBe(true);
    expect("body" in created.receipt).toBe(false);
    expect(await resolvePreSendReceiptAdmission([created.receipt], submission, 999, "d".repeat(20))).toEqual({ operation: "existing", receipt: created.receipt });
    let conflict = ""; try { await resolvePreSendReceiptAdmission([created.receipt], { ...submission, messageStage: "M2" }, 999, "d".repeat(20)); } catch (error) { conflict = String(error); }
    expect(conflict.includes("conflict")).toBe(true);
  });

  test("GET lookup accepts only the opaque ID and rejects corrupt stored state", async () => {
    const submission = await input();
    const created = await resolvePreSendReceiptAdmission([], submission, 123, "c".repeat(20));
    if (created.operation !== "create") throw new Error("expected create");
    expect(await resolvePreSendReceiptLookup([created.receipt], created.receipt.preSendReceiptId)).toEqual(created.receipt);
    let corrupt = false; try { await resolvePreSendReceiptLookup([{ ...created.receipt, receiptHash: "0".repeat(64) }], created.receipt.preSendReceiptId); } catch { corrupt = true; }
    expect(corrupt).toBe(true);
  });

  test("rejects duplicate stored request or receipt identities before idempotency", async () => {
    const submission = await input();
    const created = await resolvePreSendReceiptAdmission([], submission, 123, "c".repeat(20));
    if (created.operation !== "create") throw new Error("expected create");
    const sameRequest = await resolvePreSendReceiptAdmission([], submission, 124, "d".repeat(20));
    const sameReceiptId = await resolvePreSendReceiptAdmission([], { ...submission, requestId: "pre_send_request_" + "d".repeat(20) }, 125, "c".repeat(20));
    if (sameRequest.operation !== "create" || sameReceiptId.operation !== "create") throw new Error("expected create");
    for (const rows of [
      [created.receipt, sameRequest.receipt],
      [created.receipt, sameReceiptId.receipt],
    ]) {
      let failure = "";
      try { await resolvePreSendReceiptAdmission(rows, submission, 999, "e".repeat(20)); } catch (error) { failure = String(error); }
      expect(failure.includes("corrupt pre-send receipt")).toBe(true);
    }
  });
});
