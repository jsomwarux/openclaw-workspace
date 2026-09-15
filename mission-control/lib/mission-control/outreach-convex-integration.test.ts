// @ts-expect-error The local Bun ambient shim omits runtime hook exports.
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { createOutreachReview, decideOutreach, findOutreachDecision, getOutreachReviewState } from "../../convex/tasks";
import type { OutreachReviewSubmission } from "./outreach-review";

const SHA = "a".repeat(64);
const COMMIT = "b".repeat(40);
type Handler = (context: any, args: any) => Promise<any>;
const createReviewHandler = (createOutreachReview as unknown as { _handler: Handler })._handler;
const reviewStateHandler = (getOutreachReviewState as unknown as { _handler: Handler })._handler;
const decideHandler = (decideOutreach as unknown as { _handler: Handler })._handler;
const decisionLookupHandler = (findOutreachDecision as unknown as { _handler: Handler })._handler;

async function rejectedMessage(run: () => Promise<unknown>): Promise<string> {
  try {
    await run();
    return "";
  } catch (error) {
    return String(error);
  }
}

function submission(body = "Exact draft"): OutreachReviewSubmission & { capability: string } {
  const bind = (path: string) => ({ repository: "owner/repo", commitSha: COMMIT, path, blobSha256: SHA });
  return {
    candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: SHA,
    subject: "Subject", body, verifierReport: "VERDICT: CONFIRM",
    reviewAuthorityId: "jt", verifierActorId: "verifier-1",
    gitBindings: { evidence: bind("evidence.json"), policy: bind("policy.json"), gate: bind("gate.json"), draft: bind("draft.txt"), verifier: bind("verify.md") },
    capability: "review-secret",
  };
}

type Row = Record<string, any> & { _id: string };

class MemoryDb {
  rows: Row[] = [];
  reads = 0;
  writes = 0;
  version = 0;

  query() {
    this.reads += 1;
    return {
      withIndex: (_name: string, apply: (q: any) => any) => {
        const filters: Array<[string, unknown]> = [];
        const q = { eq: (field: string, value: unknown) => { filters.push([field, value]); return q; } };
        apply(q);
        return { collect: async () => this.rows.filter((row) => filters.every(([field, value]) => row[field] === value)) };
      },
    };
  }

  async insert(_table: string, fields: Record<string, unknown>) {
    this.writes += 1;
    const id = `task-${this.rows.length + 1}`;
    this.rows.push({ _id: id, ...fields });
    this.version += 1;
    return id;
  }

  async get(id: string) {
    this.reads += 1;
    return this.rows.find((row) => row._id === id) ?? null;
  }

  async patch(id: string, fields: Record<string, unknown>) {
    this.writes += 1;
    const row = this.rows.find((candidate) => candidate._id === id);
    if (!row) throw new Error("missing");
    Object.assign(row, fields);
    this.version += 1;
  }
}

function ctx(db: MemoryDb) { return { db } as any; }

class OptimisticConflict extends Error {}

class OptimisticStore {
  rows: Row[] = [];
  version = 0;
  private arrivals = 0;
  private releaseFirstReads!: () => void;
  private firstReadBarrier = new Promise<void>((resolve) => { this.releaseFirstReads = resolve; });

  private async synchronizeFirstTwoReads() {
    if (this.arrivals >= 2) return;
    this.arrivals += 1;
    if (this.arrivals === 2) this.releaseFirstReads();
    await this.firstReadBarrier;
  }

  private transactionDb() {
    const store = this;
    const startVersion = store.version;
    const snapshot = structuredClone(store.rows);
    return {
      query() {
        return {
          withIndex: (_name: string, apply: (q: any) => any) => {
            const filters: Array<[string, unknown]> = [];
            const q = { eq: (field: string, value: unknown) => { filters.push([field, value]); return q; } };
            apply(q);
            return {
              collect: async () => {
                await store.synchronizeFirstTwoReads();
                return snapshot.filter((row) => filters.every(([field, value]) => row[field] === value));
              },
            };
          },
        };
      },
      async insert(_table: string, fields: Record<string, unknown>) {
        if (store.version !== startVersion) throw new OptimisticConflict();
        const id = `task-${store.rows.length + 1}`;
        store.rows.push({ _id: id, ...structuredClone(fields) });
        store.version += 1;
        return id;
      },
    } as any;
  }

  async run<T>(handler: (context: any, args: any) => Promise<T>, args: any): Promise<T> {
    for (;;) {
      try {
        return await handler({ db: this.transactionDb() }, args);
      } catch (error) {
        if (!(error instanceof OptimisticConflict)) throw error;
      }
    }
  }
}

describe("registered Convex outreach handlers", () => {
  const previousReview = process.env.OUTREACH_REVIEW_CAPABILITY;
  const previousDecision = process.env.OUTREACH_DECISION_CAPABILITY;
  beforeEach(() => {
    process.env.OUTREACH_REVIEW_CAPABILITY = "review-secret";
    process.env.OUTREACH_DECISION_CAPABILITY = "decision-secret";
  });
  afterEach(() => {
    if (previousReview === undefined) delete process.env.OUTREACH_REVIEW_CAPABILITY; else process.env.OUTREACH_REVIEW_CAPABILITY = previousReview;
    if (previousDecision === undefined) delete process.env.OUTREACH_DECISION_CAPABILITY; else process.env.OUTREACH_DECISION_CAPABILITY = previousDecision;
  });

  test("stores the complete snapshot and returns the exact admission response", async () => {
    const db = new MemoryDb();
    const result = await createReviewHandler(ctx(db), submission());
    expect(Object.keys(result).sort()).toEqual(["created", "reviewCycle", "snapshotSha256", "taskId"]);
    expect(result).toMatchObject({ taskId: "task-1", created: true, reviewCycle: 1 });
    expect(db.rows[0].outreachReview.body).toBe("Exact draft");
    expect(db.rows[0].description).not.toContain("Exact draft");
  });

  test("exact retry is idempotent and two distinct snapshots consume the budget", async () => {
    const db = new MemoryDb();
    const first = await createReviewHandler(ctx(db), submission());
    const retry = await createReviewHandler(ctx(db), submission());
    const second = await createReviewHandler(ctx(db), submission("Changed draft"));
    expect(retry).toEqual({ ...first, created: false });
    expect(second.reviewCycle).toBe(2);
    expect(db.rows).toHaveLength(2);
    expect(await rejectedMessage(() => createReviewHandler(ctx(db), submission("Third draft")))).toContain("OUTREACH_REVIEW_CYCLE_LIMIT");
    expect(db.rows).toHaveLength(2);
  });

  test("optimistic retries make concurrent duplicate admission idempotent", async () => {
    const store = new OptimisticStore();
    const [left, right] = await Promise.all([
      store.run(createReviewHandler, submission()),
      store.run(createReviewHandler, submission()),
    ]);
    expect(store.rows).toHaveLength(1);
    expect([left.created, right.created].sort()).toEqual([false, true]);
    expect(left.taskId).toBe(right.taskId);
    expect(left.snapshotSha256).toBe(right.snapshotSha256);
  });

  test("optimistic retries allocate distinct concurrent cycles and reject a concurrent third", async () => {
    const firstStore = new OptimisticStore();
    const [first, second] = await Promise.all([
      firstStore.run(createReviewHandler, submission("Draft one")),
      firstStore.run(createReviewHandler, submission("Draft two")),
    ]);
    expect(firstStore.rows).toHaveLength(2);
    expect([first.reviewCycle, second.reviewCycle].sort()).toEqual([1, 2]);

    const thirdStore = new OptimisticStore();
    thirdStore.rows.push(structuredClone(firstStore.rows[0]));
    thirdStore.version = 1;
    const attempts = await Promise.allSettled([
      thirdStore.run(createReviewHandler, submission("Concurrent distinct A")),
      thirdStore.run(createReviewHandler, submission("Concurrent distinct B")),
    ]);
    expect(thirdStore.rows).toHaveLength(2);
    expect(attempts.filter((result) => result.status === "fulfilled")).toHaveLength(1);
    const rejected = attempts.find((result) => result.status === "rejected");
    expect(rejected?.status === "rejected" ? String(rejected.reason) : "").toContain("OUTREACH_REVIEW_CYCLE_LIMIT");
  });

  test("review count query returns exact state and authenticates before any read", async () => {
    const db = new MemoryDb();
    expect(await rejectedMessage(() => reviewStateHandler(ctx(db), { candidateId: "candidate-1", cohortId: "cohort-2", capability: "wrong" }))).toContain("server capability required");
    expect(db.reads).toBe(0);
    await createReviewHandler(ctx(db), submission());
    const state = await reviewStateHandler(ctx(db), { candidateId: "candidate-1", cohortId: "cohort-2", capability: "review-secret" });
    expect(state).toMatchObject({ candidateId: "candidate-1", cohortId: "cohort-2", reviewCount: 1, remainingCycles: 1 });
  });

  test("all four public outreach handlers reject missing, wrong, and swapped capabilities before database access", async () => {
    const calls = [
      (db: MemoryDb, capability: any) => createReviewHandler(ctx(db), { ...submission(), capability }),
      (db: MemoryDb, capability: any) => reviewStateHandler(ctx(db), { candidateId: "candidate-1", cohortId: "cohort-2", capability }),
      (db: MemoryDb, capability: any) => decideHandler(ctx(db), { taskId: "task-1" as any, candidateId: "candidate-1", draftSha256: SHA, snapshotSha256: SHA, decision: "approve", capability }),
      (db: MemoryDb, capability: any) => decisionLookupHandler(ctx(db), { candidateId: "candidate-1", draftSha256: SHA, snapshotSha256: SHA, capability }),
    ];
    const rejectedCapabilities = [undefined, "wrong", "review-secret", "decision-secret"];
    for (const [index, call] of calls.entries()) {
      const expected = index < 2 ? "review-secret" : "decision-secret";
      for (const candidate of rejectedCapabilities.filter((value) => value !== expected)) {
        const db = new MemoryDb();
        expect(await rejectedMessage(() => call(db, candidate))).toContain("server capability required");
        expect({ reads: db.reads, writes: db.writes }).toEqual({ reads: 0, writes: 0 });
      }
    }
  });

  test("decision mutation and lookup authenticate directly and bind the exact snapshot", async () => {
    const db = new MemoryDb();
    const admitted = await createReviewHandler(ctx(db), submission());
    const decisionArgs = { taskId: admitted.taskId as any, candidateId: "candidate-1", draftSha256: SHA, snapshotSha256: admitted.snapshotSha256, decision: "approve" as const, capability: "decision-secret" };
    const readsBefore = db.reads;
    expect(await rejectedMessage(() => decideHandler(ctx(db), { ...decisionArgs, capability: "review-secret" }))).toContain("server capability required");
    expect(await rejectedMessage(() => decisionLookupHandler(ctx(db), { candidateId: "candidate-1", draftSha256: SHA, snapshotSha256: admitted.snapshotSha256, capability: "review-secret" }))).toContain("server capability required");
    expect(db.reads).toBe(readsBefore);
    const decided = await decideHandler(ctx(db), decisionArgs);
    expect(decided).toMatchObject({ created: true, decision: { snapshotSha256: admitted.snapshotSha256, decision: "approve" } });
    expect(db.rows[0].status).toBe("done");
    const lookup = await decisionLookupHandler(ctx(db), { candidateId: "candidate-1", draftSha256: SHA, snapshotSha256: admitted.snapshotSha256, capability: "decision-secret" });
    expect(lookup).toMatchObject({ authorized: true, state: "approved", taskId: "task-1" });
  });

  test("decision and lookup reject a snapshot whose persisted content no longer matches its canonical hash", async () => {
    const db = new MemoryDb();
    const admitted = await createReviewHandler(ctx(db), submission());
    db.rows[0].outreachReview.body = "tampered persisted body";
    const decisionArgs = { taskId: admitted.taskId as any, candidateId: "candidate-1", draftSha256: SHA, snapshotSha256: admitted.snapshotSha256, decision: "approve" as const, capability: "decision-secret" };
    const writesBefore = db.writes;
    expect(await rejectedMessage(() => decideHandler(ctx(db), decisionArgs))).toContain("OUTREACH_DECISION_CONFLICT");
    expect(await rejectedMessage(() => decisionLookupHandler(ctx(db), { candidateId: "candidate-1", draftSha256: SHA, snapshotSha256: admitted.snapshotSha256, capability: "decision-secret" }))).toContain("OUTREACH_DECISION_CONFLICT");
    expect(db.writes).toBe(writesBefore);
  });
});
