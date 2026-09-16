import type { GitBinding } from "./outreach-review";
import { canonicalJson } from "./canonical-json";

export type SuppressionBinding = {
  schemaVersion: "outreach-suppression-binding-v1";
  repository: string;
  commitSha: string;
  gatePath: string;
  gateBlobSha256: string;
  gateArtifactHash: string;
  admissionCommitSha: string;
  admissionPath: string;
  admissionBlobSha256: string;
  channelAttestationId: string;
  channelOwnerRevision: string;
  prospectId: string;
  organizationFactId: string;
  channelFingerprint: string;
  bindingHash: string;
};

const FIELDS = ["schemaVersion", "repository", "commitSha", "gatePath", "gateBlobSha256", "gateArtifactHash", "admissionCommitSha", "admissionPath", "admissionBlobSha256", "channelAttestationId", "channelOwnerRevision", "prospectId", "organizationFactId", "channelFingerprint"] as const;
const DIGEST = /^[a-f0-9]{64}$/;
const COMMIT = /^[a-f0-9]{40}$/;
const PORTABLE = /^[a-z0-9][a-z0-9._:-]{0,127}$/;
const REPOSITORY = /^[a-z0-9][a-z0-9._-]{0,63}\/[a-z0-9][a-z0-9._-]{0,99}$/;
const PATH = /^[A-Za-z0-9._/-]+$/;
const ATTESTATION = /^channel_[a-f0-9]{20}$/;
const REVIEW = /^review_[a-f0-9]{20}$/;
const REQUEST = /^pre_send_request_[a-f0-9]{20}$/;
const EVENT = /^suppression_event_[a-f0-9]{20}$/;
const UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;

function record(value: unknown): value is Record<string, unknown> { return Boolean(value) && typeof value === "object" && !Array.isArray(value); }
function exact(value: Record<string, unknown>, fields: readonly string[]) { const a = Object.keys(value).sort(); const b = [...fields].sort(); return a.length === b.length && a.every((key, i) => key === b[i]); }
function safePath(value: unknown): value is string { return typeof value === "string" && PATH.test(value) && !value.startsWith("/") && !value.includes("\\") && value.split("/").every((part) => part && part !== "." && part !== ".."); }
async function sha(parts: string[]): Promise<string> { const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(parts.join(""))); return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join(""); }

function validateBindingFields(value: Record<string, unknown>) {
  if (value.schemaVersion !== "outreach-suppression-binding-v1" || !REPOSITORY.test(String(value.repository ?? "")) || !COMMIT.test(String(value.commitSha ?? "")) || !safePath(value.gatePath)) throw new Error("invalid suppression binding");
  for (const key of ["gateBlobSha256", "gateArtifactHash", "admissionBlobSha256", "channelOwnerRevision", "channelFingerprint"] as const) if (!DIGEST.test(String(value[key] ?? ""))) throw new Error("invalid suppression binding");
  if (!COMMIT.test(String(value.admissionCommitSha ?? "")) || !safePath(value.admissionPath) || !ATTESTATION.test(String(value.channelAttestationId ?? "")) || !PORTABLE.test(String(value.prospectId ?? "")) || !PORTABLE.test(String(value.organizationFactId ?? ""))) throw new Error("invalid suppression binding");
}

export async function hashSuppressionBinding(value: Omit<SuppressionBinding, "bindingHash">): Promise<string> {
  const raw = value as unknown;
  if (!record(raw) || !exact(raw, FIELDS)) throw new Error("invalid suppression binding");
  validateBindingFields(raw);
  return sha(["outreach-suppression-binding-v1\0", canonicalJson(value)]);
}

export function validateSuppressionBinding(value: unknown, gateBinding?: GitBinding): asserts value is SuppressionBinding {
  if (!record(value) || !exact(value, [...FIELDS, "bindingHash"]) || !DIGEST.test(String(value.bindingHash ?? ""))) throw new Error("invalid suppression binding");
  validateBindingFields(value);
  if (gateBinding && (value.repository !== gateBinding.repository || value.commitSha !== gateBinding.commitSha || value.gatePath !== gateBinding.path || value.gateBlobSha256 !== gateBinding.blobSha256)) throw new Error("invalid suppression binding");
}

export async function validateSuppressionBindingHash(value: unknown, gateBinding?: GitBinding): Promise<SuppressionBinding> {
  validateSuppressionBinding(value, gateBinding);
  const { bindingHash, ...withoutHash } = value;
  if (await hashSuppressionBinding(withoutHash) !== bindingHash) throw new Error("invalid suppression binding");
  return value;
}

export async function deriveSuppressionClearInputs(reviewId: string, binding: SuppressionBinding) {
  if (!REVIEW.test(reviewId)) throw new Error("invalid review id");
  await validateSuppressionBindingHash(binding);
  const evidenceToken = `evidence_${await sha(["suppression-clear-evidence-v1\0", reviewId, "\0", binding.bindingHash])}`;
  const [consultingRequest, missionRequest] = await Promise.all([
    sha(["suppression-clear-request-v1\0", "consulting-pipeline", "\0", binding.bindingHash]),
    sha(["suppression-clear-request-v1\0", "mission-control", "\0", binding.bindingHash]),
  ]);
  const make = (request: string) => ({
    schemaVersion: "outreach-suppression-event-v1" as const,
    requestId: `suppression_request_${request.slice(0, 20)}`,
    prospectId: binding.prospectId, organizationFactId: binding.organizationFactId,
    channelFingerprint: binding.channelFingerprint, state: "clear" as const, evidenceToken,
  });
  return { consulting: make(consultingRequest), missionControl: make(missionRequest) };
}

const RECEIPT_FIELDS = ["schemaVersion", "requestId", "suppressionBinding", "missionControlEventId", "missionControlOwnerRevision", "missionControlObservedAt", "consultingEventId", "consultingOwnerRevision", "consultingObservedAt", "reviewId", "snapshotSha256", "draftSha256", "decisionSha256", "messageStage"] as const;
export type PreSendReceiptSubmission = {
  schemaVersion: "outreach-pre-send-receipt-v1";
  requestId: string;
  suppressionBinding: SuppressionBinding;
  missionControlEventId: string;
  missionControlOwnerRevision: string;
  missionControlObservedAt: string;
  consultingEventId: string;
  consultingOwnerRevision: string;
  consultingObservedAt: string;
  reviewId: string;
  snapshotSha256: string;
  draftSha256: string;
  decisionSha256: string;
  messageStage: "M1" | "M2" | "M3";
};
export function validatePreSendReceiptSubmission(value: unknown): asserts value is PreSendReceiptSubmission {
  if (!record(value) || !exact(value, RECEIPT_FIELDS) || value.schemaVersion !== "outreach-pre-send-receipt-v1" || !REQUEST.test(String(value.requestId ?? ""))) throw new Error("invalid pre-send receipt");
  validateSuppressionBinding(value.suppressionBinding);
  if (!EVENT.test(String(value.missionControlEventId ?? "")) || !EVENT.test(String(value.consultingEventId ?? "")) || !REVIEW.test(String(value.reviewId ?? ""))) throw new Error("invalid pre-send receipt");
  for (const key of ["missionControlOwnerRevision", "consultingOwnerRevision", "snapshotSha256", "draftSha256", "decisionSha256"] as const) if (!DIGEST.test(String(value[key] ?? ""))) throw new Error("invalid pre-send receipt");
  for (const key of ["missionControlObservedAt", "consultingObservedAt"] as const) if (typeof value[key] !== "string" || !UTC.test(value[key] as string) || !Number.isFinite(Date.parse(value[key] as string))) throw new Error("invalid pre-send receipt");
  if (!/^M[123]$/.test(String(value.messageStage ?? ""))) throw new Error("invalid pre-send receipt");
}
