// @ts-expect-error Bun runtime hook exports are omitted from the ambient shim.
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { appendOutreachSuppressionEvent, findOutreachSuppressionState, createOutreachPreSendReceipt, findOutreachPreSendReceipt, findOutreachSuppressionReview } from "../../convex/tasks";
import { resolveOutreachReviewAdmission } from "./outreach-review";
import { resolveOutreachDecision } from "./outreach-decision";
import { hashOutreachDecisionForPreSend } from "./outreach-pre-send-receipt";
import { hashSuppressionBinding } from "./outreach-suppression-binding";

type Handler = (ctx: any, args: any) => Promise<any>;
const append = (appendOutreachSuppressionEvent as any)._handler as Handler;
const lookup = (findOutreachSuppressionState as any)._handler as Handler;
const createReceipt = (createOutreachPreSendReceipt as any)._handler as Handler;
const getReceipt = (findOutreachPreSendReceipt as any)._handler as Handler;
const findReview = (findOutreachSuppressionReview as any)._handler as Handler;

class Db {
  rows: Record<string, any>[] = [];
  reads = 0; writes = 0;
  query(table: string) {
    this.reads++;
    const rows = this.rows.filter((row) => row.__table === table);
    return { collect: async () => rows, withIndex: (_name: string, apply: (q: any) => any) => { const filters: [string, unknown][] = []; const q = { eq: (key: string, value: unknown) => { filters.push([key, value]); return q; } }; apply(q); return { collect: async () => rows.filter((row) => filters.every(([key, value]) => row[key] === value)) }; } };
  }
  async insert(table: string, fields: Record<string, unknown>) { this.writes++; const id = `${table}-${this.rows.length + 1}`; this.rows.push({ __table: table, _id: id, ...structuredClone(fields) }); return id; }
}
const ctx = (db: Db) => ({ db }) as any;
const base = { schemaVersion: "outreach-suppression-event-v1", requestId: "suppression_request_" + "1".repeat(20), prospectId: "prospect.alpha", organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64), state: "clear", evidenceToken: "evidence_" + "3".repeat(64) };
async function message(run: () => Promise<unknown>) { try { await run(); return ""; } catch (error) { return String(error); } }

describe("direct Convex suppression boundary", () => {
  const original = { flag: process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED, decision: process.env.OUTREACH_DECISION_CAPABILITY, read: process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY, review: process.env.OUTREACH_REVIEW_CAPABILITY, write: process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY };
  beforeEach(() => { process.env.OUTREACH_DECISION_CAPABILITY = "decision"; process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY = "read"; process.env.OUTREACH_REVIEW_CAPABILITY = "review"; process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY = "write"; delete process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED; });
  afterEach(() => { for (const [key, value] of Object.entries(original)) { const name = ({ flag: "OUTREACH_SUPPRESSION_OWNER_ENABLED", decision: "OUTREACH_DECISION_CAPABILITY", read: "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY", review: "OUTREACH_REVIEW_CAPABILITY", write: "OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY" } as const)[key as keyof typeof original]; if (value === undefined) delete process.env[name]; else process.env[name] = value; } });

  test("every public handler rejects disabled before database access", async () => {
    for (const call of [
      (db: Db) => append(ctx(db), { ...base, capability: "decision" }),
      (db: Db) => lookup(ctx(db), { prospectId: base.prospectId, organizationFactId: base.organizationFactId, channelFingerprint: base.channelFingerprint, capability: "read" }),
      (db: Db) => createReceipt(ctx(db), { capability: "review" }),
      (db: Db) => getReceipt(ctx(db), { preSendReceiptId: "pre_send_" + "1".repeat(20), capability: "read" }),
      (db: Db) => findReview(ctx(db), { reviewId: "review_" + "1".repeat(20), capability: "decision" }),
    ]) { const db = new Db(); expect(await message(() => call(db))).toContain("OUTREACH_SUPPRESSION_OWNER_NOT_CONFIGURED"); expect({ reads: db.reads, writes: db.writes }).toEqual({ reads: 0, writes: 0 }); }
  });

  test("every pairwise-equal capability configuration fails before database access", async () => {
    process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED = "true";
    const names = [
      "OUTREACH_DECISION_CAPABILITY",
      "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY",
      "OUTREACH_REVIEW_CAPABILITY",
      "OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY",
    ] as const;
    for (let left = 0; left < names.length; left++) {
      for (let right = left + 1; right < names.length; right++) {
        process.env.OUTREACH_DECISION_CAPABILITY = "decision";
        process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY = "read";
        process.env.OUTREACH_REVIEW_CAPABILITY = "review";
        process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY = "write";
        process.env[names[right]] = process.env[names[left]];
        const db = new Db();
        expect(await message(() => findReview(ctx(db), {
          reviewId: "review_" + "1".repeat(20), capability: process.env.OUTREACH_DECISION_CAPABILITY!,
        }))).toContain("OUTREACH_SUPPRESSION_OWNER_NOT_CONFIGURED");
        expect({ reads: db.reads, writes: db.writes }).toEqual({ reads: 0, writes: 0 });
      }
    }
  });

  test("generic task routes cannot access suppression owners or capability environment", () => {
    for (const source of [
      readFileSync("app/api/tasks/route.ts", "utf8"),
      readFileSync("app/api/tasks/[id]/route.ts", "utf8"),
    ]) {
      for (const forbidden of [
        "OUTREACH_SUPPRESSION_OWNER_ENABLED", "outreachSuppressionEvents", "outreachPreSendReceipts",
        "appendOutreachSuppressionEvent", "findOutreachSuppressionState", "findOutreachSuppressionReview",
        "createOutreachPreSendReceipt", "findOutreachPreSendReceipt",
      ]) expect(source).not.toContain(forbidden);
    }
  });

  test("write and read capabilities cannot cross and one append is immutable", async () => {
    process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED = "true";
    const db = new Db();
    expect(await message(() => append(ctx(db), { ...base, capability: "read" }))).toContain("server capability required");
    expect(await message(() => lookup(ctx(db), { prospectId: base.prospectId, organizationFactId: base.organizationFactId, channelFingerprint: base.channelFingerprint, capability: "decision" }))).toContain("server capability required");
    const result = await append(ctx(db), { ...base, capability: "decision" });
    expect(result.created).toBe(true);
    expect(db.writes).toBe(1);
    const state = await lookup(ctx(db), { prospectId: base.prospectId, organizationFactId: base.organizationFactId, channelFingerprint: base.channelFingerprint, capability: "read" });
    expect(state.clear).toBe(true);
  });

  test("review lookup returns a binding only for one exact approved active immutable snapshot", async () => {
    process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED = "true";
    const rawBinding = {
      schemaVersion: "outreach-suppression-binding-v1" as const,
      repository: "owner/repo", commitSha: "a".repeat(40), gatePath: "gate.json",
      gateBlobOid: "1".repeat(40), gateBlobSha256: "b".repeat(64), gateArtifactHash: "c".repeat(64),
      admissionCommitSha: "d".repeat(40), admissionPath: "admission/candidate.json",
      admissionBlobOid: "2".repeat(40), admissionBlobSha256: "e".repeat(64), channelAttestationId: `channel_${"f".repeat(20)}`,
      channelOwnerRevision: "1".repeat(64), prospectId: "prospect.alpha",
      organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64),
    };
    const suppressionBinding = { ...rawBinding, bindingHash: await hashSuppressionBinding(rawBinding) };
    const bind = (path: string) => ({ repository: "owner/repo", commitSha: "a".repeat(40), path, blobSha256: path === "gate.json" ? "b".repeat(64) : "3".repeat(64) });
    const admitted = await resolveOutreachReviewAdmission([], {
      candidateId: "prospect.alpha", cohortId: "cohort-2", draftSha256: "4".repeat(64),
      subject: "Subject", body: "Exact approved draft", verifierReport: "VERDICT: CONFIRM",
      reviewAuthorityId: `review_${"5".repeat(20)}`, verifierActorId: "verifier-1",
      gitBindings: { evidence: bind("evidence.json"), policy: bind("policy.json"), gate: bind("gate.json"), draft: bind("draft.txt"), verifier: bind("verify.md") },
      suppressionBinding,
    }, 100);
    if (admitted.operation !== "create") throw new Error("expected review creation");
    const approve = resolveOutreachDecision(admitted.fields, {
      candidateId: admitted.fields.candidateId, draftSha256: admitted.fields.draftSha256,
      snapshotSha256: admitted.fields.outreachReview.snapshotSha256, decision: "approve",
    }, 101);
    const reject = resolveOutreachDecision(admitted.fields, {
      candidateId: admitted.fields.candidateId, draftSha256: admitted.fields.draftSha256,
      snapshotSha256: admitted.fields.outreachReview.snapshotSha256, decision: "reject",
    }, 101);
    if (approve.operation !== "create" || reject.operation !== "create") throw new Error("expected decisions");
    const rows = [
      { ...admitted.fields, status: "todo", outreachDecision: undefined },
      { ...admitted.fields, status: "done", outreachDecision: reject.decision },
      { ...admitted.fields, status: "archived", outreachDecision: approve.decision },
      { ...admitted.fields, status: "done", outreachDecision: { ...approve.decision, snapshotSha256: "9".repeat(64) } },
    ];
    for (const row of rows) {
      const db = new Db();
      db.rows.push({ __table: "tasks", _id: "task-1", ...structuredClone(row) });
      expect(await message(() => findReview(ctx(db), {
        reviewId: admitted.fields.outreachReview.reviewAuthorityId, capability: "decision",
      }))).toContain("OUTREACH_SUPPRESSION_REVIEW_NOT_FOUND");
    }
    const approved = new Db();
    approved.rows.push({ __table: "tasks", _id: "task-1", ...structuredClone(admitted.fields), status: "done", outreachDecision: approve.decision });
    expect(await findReview(ctx(approved), {
      reviewId: admitted.fields.outreachReview.reviewAuthorityId, capability: "decision",
    })).toEqual({ suppressionBinding });
  });

  test("creates and reads one immutable receipt only for the exact approved bound review", async () => {
    process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED = "true";
    const db = new Db();
    const rawBinding = {
      schemaVersion: "outreach-suppression-binding-v1" as const,
      repository: "owner/repo", commitSha: "a".repeat(40), gatePath: "gate.json",
      gateBlobOid: "1".repeat(40), gateBlobSha256: "b".repeat(64), gateArtifactHash: "c".repeat(64),
      admissionCommitSha: "d".repeat(40), admissionPath: "admission/candidate.json",
      admissionBlobOid: "2".repeat(40), admissionBlobSha256: "e".repeat(64), channelAttestationId: `channel_${"f".repeat(20)}`,
      channelOwnerRevision: "1".repeat(64), prospectId: "prospect.alpha",
      organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64),
    };
    const suppressionBinding = { ...rawBinding, bindingHash: await hashSuppressionBinding(rawBinding) };
    const bind = (path: string) => ({ repository: "owner/repo", commitSha: "a".repeat(40), path, blobSha256: path === "gate.json" ? "b".repeat(64) : "3".repeat(64) });
    const admitted = await resolveOutreachReviewAdmission([], {
      candidateId: "prospect.alpha", cohortId: "cohort-2", draftSha256: "4".repeat(64),
      subject: "Subject", body: "Exact approved draft", verifierReport: "VERDICT: CONFIRM",
      reviewAuthorityId: `review_${"5".repeat(20)}`, verifierActorId: "verifier-1",
      gitBindings: { evidence: bind("evidence.json"), policy: bind("policy.json"), gate: bind("gate.json"), draft: bind("draft.txt"), verifier: bind("verify.md") },
      suppressionBinding,
    }, 100);
    if (admitted.operation !== "create") throw new Error("expected review creation");
    const decision = resolveOutreachDecision(admitted.fields, {
      candidateId: admitted.fields.candidateId,
      draftSha256: admitted.fields.draftSha256,
      snapshotSha256: admitted.fields.outreachReview.snapshotSha256,
      decision: "approve",
    }, 101);
    if (decision.operation !== "create") throw new Error("expected decision creation");
    db.rows.push({ __table: "tasks", _id: "task-1", ...structuredClone(admitted.fields), status: "done", outreachDecision: decision.decision });
    const receiptInput = {
      schemaVersion: "outreach-pre-send-receipt-v1", requestId: `pre_send_request_${"6".repeat(20)}`,
      suppressionBinding, missionControlEventId: `suppression_event_${"7".repeat(20)}`,
      missionControlOwnerRevision: "8".repeat(64), missionControlObservedAt: "2026-09-16T14:00:00Z",
      consultingEventId: `suppression_event_${"9".repeat(20)}`, consultingOwnerRevision: "a".repeat(64),
      consultingObservedAt: "2026-09-16T14:00:01Z", reviewId: admitted.fields.outreachReview.reviewAuthorityId,
      snapshotSha256: admitted.fields.outreachReview.snapshotSha256, draftSha256: admitted.fields.draftSha256,
      decisionSha256: await hashOutreachDecisionForPreSend(decision.decision), messageStage: "M1",
    };
    expect(await message(() => createReceipt(ctx(db), { ...receiptInput, capability: "read" }))).toContain("server capability required");
    const created = await createReceipt(ctx(db), { ...receiptInput, capability: "review" });
    expect(created.created).toBe(true);
    const retry = await createReceipt(ctx(db), { ...receiptInput, capability: "review" });
    expect(retry).toEqual({ created: false, receipt: created.receipt });
    expect(await getReceipt(ctx(db), { preSendReceiptId: created.receipt.preSendReceiptId, capability: "read" }))
      .toEqual({ found: true, receipt: created.receipt });
  });
});
