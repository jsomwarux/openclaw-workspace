import { canonicalJson } from "./canonical-json";
import { validatePreSendReceiptSubmission, validateSuppressionBindingHash, type PreSendReceiptSubmission } from "./outreach-suppression-binding";
import type { OutreachDecision } from "./outreach-decision";

export type PreSendReceipt = PreSendReceiptSubmission & {
  preSendReceiptId: string;
  createdAt: number;
  receiptHash: string;
};

const RECEIPT_ID = /^pre_send_[a-f0-9]{20}$/;
const ENTROPY = /^[a-f0-9]{20}$/;
const DIGEST = /^[a-f0-9]{64}$/;
const FIELDS = ["schemaVersion", "requestId", "suppressionBinding", "missionControlEventId", "missionControlOwnerRevision", "missionControlObservedAt", "consultingEventId", "consultingOwnerRevision", "consultingObservedAt", "reviewId", "snapshotSha256", "draftSha256", "decisionSha256", "messageStage", "preSendReceiptId", "createdAt", "receiptHash"] as const;

function record(value: unknown): value is Record<string, unknown> { return Boolean(value) && typeof value === "object" && !Array.isArray(value); }
function exact(value: Record<string, unknown>) { const a = Object.keys(value).sort(); const b = [...FIELDS].sort(); return a.length === b.length && a.every((key, index) => key === b[index]); }
async function sha(value: string) { const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value)); return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join(""); }
export async function hashOutreachDecisionForPreSend(decision: OutreachDecision) {
  return sha(canonicalJson({ domain: "mission-control/outreach-decision", version: 1, decision }));
}
export async function hashPreSendReceiptSubmission(input: PreSendReceiptSubmission) {
  validatePreSendReceiptSubmission(input);
  await validateSuppressionBindingHash(input.suppressionBinding);
  return sha(`outreach-pre-send-receipt-v1\0${canonicalJson(input)}`);
}
async function validateReceipt(value: unknown): Promise<PreSendReceipt> {
  if (!record(value) || !exact(value) || !RECEIPT_ID.test(String(value.preSendReceiptId ?? "")) || !Number.isSafeInteger(value.createdAt) || Number(value.createdAt) < 0 || !DIGEST.test(String(value.receiptHash ?? ""))) throw new Error("corrupt pre-send receipt");
  const { preSendReceiptId: _id, createdAt: _time, receiptHash, ...submission } = value;
  if (await hashPreSendReceiptSubmission(submission as PreSendReceiptSubmission) !== receiptHash) throw new Error("corrupt pre-send receipt");
  return value as PreSendReceipt;
}

async function validateReceiptRows(rows: PreSendReceipt[]): Promise<PreSendReceipt[]> {
  const receipts = await Promise.all(rows.map(validateReceipt));
  const requestIds = new Set<string>();
  const receiptIds = new Set<string>();
  for (const receipt of receipts) {
    if (requestIds.has(receipt.requestId) || receiptIds.has(receipt.preSendReceiptId)) {
      throw new Error("corrupt pre-send receipt");
    }
    requestIds.add(receipt.requestId);
    receiptIds.add(receipt.preSendReceiptId);
  }
  return receipts;
}

export async function resolvePreSendReceiptAdmission(rows: PreSendReceipt[], input: PreSendReceiptSubmission, createdAt: number, entropy: string) {
  const receiptHash = await hashPreSendReceiptSubmission(input);
  if (!Number.isSafeInteger(createdAt) || createdAt < 0 || !ENTROPY.test(entropy)) throw new Error("invalid pre-send receipt");
  const receipts = await validateReceiptRows(rows);
  const duplicate = receipts.find((receipt) => receipt.requestId === input.requestId);
  if (duplicate) {
    if (duplicate.receiptHash !== receiptHash) throw new Error("conflict");
    return { operation: "existing" as const, receipt: duplicate };
  }
  return { operation: "create" as const, receipt: { ...input, preSendReceiptId: `pre_send_${entropy}`, createdAt, receiptHash } };
}

export async function resolvePreSendReceiptLookup(rows: PreSendReceipt[], preSendReceiptId: string): Promise<PreSendReceipt | null> {
  if (!RECEIPT_ID.test(preSendReceiptId)) throw new Error("invalid pre-send receipt id");
  const receipts = await validateReceiptRows(rows);
  const exactRows = receipts.filter((receipt) => receipt.preSendReceiptId === preSendReceiptId);
  if (exactRows.length > 1) throw new Error("corrupt pre-send receipt");
  return exactRows[0] ?? null;
}
