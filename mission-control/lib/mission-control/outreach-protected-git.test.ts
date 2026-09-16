import { describe, expect, test } from "bun:test";
import { createHash } from "node:crypto";
import { canonicalJson } from "./canonical-json";
import { hashSuppressionBinding, type SuppressionBinding } from "./outreach-suppression-binding";
import { verifyProtectedSuppressionBinding } from "./outreach-protected-git";

const enc = new TextEncoder();
async function sha(value: Uint8Array | string) {
  return createHash("sha256").update(value).digest("hex");
}

async function authority() {
  const admission = {
    schema_version: "prospect-candidate-v2",
    prospect_id: "prospect.alpha",
    organization: { name: "Alpha", name_fact_id: "fact-org:alpha" },
  };
  const admissionBytes = enc.encode(canonicalJson(admission));
  const admissionBlobSha256 = await sha(admissionBytes);
  const receipt = {
    prospect_id: "prospect.alpha",
    evidence_commit: "d".repeat(40),
    manifest_path: "admission/candidate.json",
    manifest_blob_sha256: admissionBlobSha256,
    attestation_id: `channel_${"f".repeat(20)}`,
    owner_revision: "1".repeat(64),
  };
  const gate = {
    draft_request: { gate_receipt_hash: await sha(canonicalJson(receipt)) },
    gate_receipt: receipt,
  };
  const gateBytes = enc.encode(canonicalJson(gate));
  const raw = {
    schemaVersion: "outreach-suppression-binding-v1" as const,
    repository: "jsomwarux/jt-ops",
    commitSha: "a".repeat(40),
    gatePath: "gates/gate.json",
    gateBlobOid: "b".repeat(40),
    gateBlobSha256: await sha(gateBytes),
    gateArtifactHash: await sha(canonicalJson(gate)),
    admissionCommitSha: "d".repeat(40),
    admissionPath: "admission/candidate.json",
    admissionBlobOid: "c".repeat(40),
    admissionBlobSha256,
    channelAttestationId: `channel_${"f".repeat(20)}`,
    channelOwnerRevision: "1".repeat(64),
    prospectId: "prospect.alpha",
    organizationFactId: "fact-org:alpha",
    channelFingerprint: "2".repeat(64),
  };
  const binding: SuppressionBinding = { ...raw, bindingHash: await hashSuppressionBinding(raw) };
  return { binding, gateBytes, admissionBytes };
}

describe("protected suppression binding admission", () => {
  test("accepts only the exact canonical gate and admission bytes", async () => {
    const { binding, gateBytes, admissionBytes } = await authority();
    const reads: unknown[] = [];
    await verifyProtectedSuppressionBinding(binding, async (request) => {
      reads.push(request);
      return request.path === binding.gatePath
        ? { bytes: gateBytes, blobOid: binding.gateBlobOid }
        : { bytes: admissionBytes, blobOid: binding.admissionBlobOid };
    });
    expect(reads).toEqual([
      { repository: "jsomwarux/jt-ops", commitSha: binding.commitSha, path: binding.gatePath },
      { repository: "jsomwarux/jt-ops", commitSha: binding.admissionCommitSha, path: binding.admissionPath },
    ]);
  });

  test("rejects a self-consistent caller forgery when protected bytes disagree", async () => {
    const { binding, gateBytes, admissionBytes } = await authority();
    const forgedAdmission = enc.encode(canonicalJson({
      schema_version: "prospect-candidate-v2",
      prospect_id: binding.prospectId,
      organization: { name: "Forged", name_fact_id: binding.organizationFactId },
    }));
    const forgedRaw = {
      ...binding,
      admissionBlobSha256: await sha(forgedAdmission),
    };
    delete (forgedRaw as Partial<SuppressionBinding>).bindingHash;
    const forged = {
      ...forgedRaw,
      bindingHash: await hashSuppressionBinding(forgedRaw),
    } as SuppressionBinding;
    let error = "";
    try {
      await verifyProtectedSuppressionBinding(forged, async (request) => (
        request.path === binding.gatePath
          ? { bytes: gateBytes, blobOid: binding.gateBlobOid }
          : { bytes: admissionBytes, blobOid: binding.admissionBlobOid }
      ));
    } catch (caught) { error = String(caught); }
    expect(error).toContain("protected suppression binding mismatch");
  });

  test("rejects a caller-computed gate artifact hash that is not the protected gate", async () => {
    const { binding, gateBytes, admissionBytes } = await authority();
    const forgedRaw = { ...binding, gateArtifactHash: "9".repeat(64) };
    delete (forgedRaw as Partial<SuppressionBinding>).bindingHash;
    const forged = { ...forgedRaw, bindingHash: await hashSuppressionBinding(forgedRaw) } as SuppressionBinding;
    let error = "";
    try {
      await verifyProtectedSuppressionBinding(forged, async (request) => (
        request.path === binding.gatePath
          ? { bytes: gateBytes, blobOid: binding.gateBlobOid }
          : { bytes: admissionBytes, blobOid: binding.admissionBlobOid }
      ));
    } catch (caught) { error = String(caught); }
    expect(error).toContain("protected suppression binding mismatch");
  });

  test("rejects a caller blob OID that differs from git rev-parse", async () => {
    const { binding, gateBytes, admissionBytes } = await authority();
    const forgedRaw = { ...binding, gateBlobOid: "9".repeat(40) };
    delete (forgedRaw as Partial<SuppressionBinding>).bindingHash;
    const forged = { ...forgedRaw, bindingHash: await hashSuppressionBinding(forgedRaw) } as SuppressionBinding;
    let error = "";
    try {
      await verifyProtectedSuppressionBinding(forged, async (request) => (
        request.path === binding.gatePath
          ? { bytes: gateBytes, blobOid: binding.gateBlobOid }
          : { bytes: admissionBytes, blobOid: binding.admissionBlobOid }
      ));
    } catch (caught) { error = String(caught); }
    expect(error).toContain("protected suppression binding mismatch");
  });
});
