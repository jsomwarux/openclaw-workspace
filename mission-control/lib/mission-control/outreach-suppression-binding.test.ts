import { describe, expect, test } from "bun:test";
import {
  deriveSuppressionClearInputs,
  hashSuppressionBinding,
  validateSuppressionBinding,
  validatePreSendReceiptSubmission,
  type SuppressionBinding,
} from "./outreach-suppression-binding";

const binding: Omit<SuppressionBinding, "bindingHash"> = {
  schemaVersion: "outreach-suppression-binding-v1",
  repository: "owner/repo",
  commitSha: "a".repeat(40),
  gatePath: "gates/candidate.json",
  gateBlobSha256: "b".repeat(64),
  gateArtifactHash: "c".repeat(64),
  admissionCommitSha: "d".repeat(40),
  admissionPath: "admission/candidate.json",
  admissionBlobSha256: "e".repeat(64),
  channelAttestationId: `channel_${"f".repeat(20)}`,
  channelOwnerRevision: "1".repeat(64),
  prospectId: "prospect.alpha",
  organizationFactId: "fact-org:alpha",
  channelFingerprint: "2".repeat(64),
};

describe("immutable suppression binding and pre-send receipt", () => {
  test("binds every copy-free field and rejects mutable paths or mismatched review Git authority", async () => {
    const complete = { ...binding, bindingHash: await hashSuppressionBinding(binding) };
    validateSuppressionBinding(complete, {
      repository: binding.repository,
      commitSha: binding.commitSha,
      path: binding.gatePath,
      blobSha256: binding.gateBlobSha256,
    });
    let invalidPath = false; try { await hashSuppressionBinding({ ...binding, gatePath: "/tmp/gate.json" }); } catch { invalidPath = true; }
    expect(invalidPath).toBe(true);
    expect(thrown(() => validateSuppressionBinding(complete, {
      repository: binding.repository,
      commitSha: binding.commitSha,
      path: "other.json",
      blobSha256: binding.gateBlobSha256,
    }))).toBe(true);
  });

  test("derives retry-stable owner clear IDs from review ID and binding hash", async () => {
    const complete = { ...binding, bindingHash: await hashSuppressionBinding(binding) };
    const first = await deriveSuppressionClearInputs("review_" + "3".repeat(20), complete);
    expect(/^suppression_request_[a-f0-9]{20}$/.test(first.consulting.requestId)).toBe(true);
    expect(/^suppression_request_[a-f0-9]{20}$/.test(first.missionControl.requestId)).toBe(true);
    expect(first.consulting.requestId).not.toBe(first.missionControl.requestId);
    expect(first.consulting.evidenceToken).toBe(first.missionControl.evidenceToken);
    expect(await deriveSuppressionClearInputs("review_" + "3".repeat(20), complete)).toEqual(first);
  });

  test("accepts exact copy-free pre-send submissions and rejects raw channel or copy", async () => {
    const suppressionBinding = { ...binding, bindingHash: await hashSuppressionBinding(binding) };
    const input = {
      schemaVersion: "outreach-pre-send-receipt-v1",
      requestId: "pre_send_request_" + "4".repeat(20),
      suppressionBinding,
      missionControlEventId: "suppression_event_" + "5".repeat(20),
      missionControlOwnerRevision: "6".repeat(64),
      missionControlObservedAt: "2026-09-16T14:00:00Z",
      consultingEventId: "suppression_event_" + "7".repeat(20),
      consultingOwnerRevision: "8".repeat(64),
      consultingObservedAt: "2026-09-16T14:00:01Z",
      reviewId: "review_" + "9".repeat(20),
      snapshotSha256: "a".repeat(64),
      draftSha256: "b".repeat(64),
      decisionSha256: "c".repeat(64),
      messageStage: "M1",
    };
    validatePreSendReceiptSubmission(input);
    expect(thrown(() => validatePreSendReceiptSubmission({ ...input, channel: "owner@example.org" }))).toBe(true);
    expect(thrown(() => validatePreSendReceiptSubmission({ ...input, body: "copy" }))).toBe(true);
    expect(thrown(() => validatePreSendReceiptSubmission({ ...input, consultingObservedAt: "2026-09-16 10:00:01-04:00" }))).toBe(true);
  });
});

function thrown(run: () => unknown) { try { run(); return false; } catch { return true; } }
