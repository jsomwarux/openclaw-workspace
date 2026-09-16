// @ts-expect-error The local Bun ambient shim omits runtime hook exports.
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import {
  createOutreachReview,
  createOutreachReviewAuthority,
  decideOutreach,
  findOutreachDecision,
  findOutreachReviewAuthority,
  getOutreachReviewState,
} from "../../convex/tasks";
import type { OutreachReviewSubmission } from "./outreach-review";
import type { OutreachReviewAuthoritySubmission } from "./outreach-review-authority";

const SHA = "a".repeat(64);
const COMMIT = "b".repeat(40);
type Handler = (context: any, args: any) => Promise<any>;
const createReviewHandler = (createOutreachReview as unknown as { _handler: Handler })._handler;
const reviewStateHandler = (getOutreachReviewState as unknown as { _handler: Handler })._handler;
const decideHandler = (decideOutreach as unknown as { _handler: Handler })._handler;
const decisionLookupHandler = (findOutreachDecision as unknown as { _handler: Handler })._handler;
const createAuthorityHandler = (createOutreachReviewAuthority as unknown as { _handler: Handler })._handler;
const authorityLookupHandler = (findOutreachReviewAuthority as unknown as { _handler: Handler })._handler;

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

function authoritySubmission(
  overrides: Partial<OutreachReviewAuthoritySubmission & { capability: string }> = {},
) {
  return {
    candidateId: "candidate-1",
    draftSha256: SHA,
    authorityBundleHash: "c".repeat(64),
    verifierReportSha256: "d".repeat(64),
    verifierGitBinding: {
      repository: "owner/repo",
      commitSha: COMMIT,
      path: "reviews/verifier-report.json",
      blobSha256: "d".repeat(64),
    },
    builderActorId: "builder-1",
    drafterActorId: "drafter-1",
    capability: "authority-write-secret",
    ...overrides,
  };
}

function authorityLookup(
  input = authoritySubmission(),
  capability = "authority-read-secret",
) {
  return {
    candidateId: input.candidateId,
    draftSha256: input.draftSha256,
    authorityBundleHash: input.authorityBundleHash,
    verifierReportSha256: input.verifierReportSha256,
    verifierGitBinding: structuredClone(input.verifierGitBinding),
    capability,
  };
}

type Row = Record<string, any> & { _id: string };

function fieldValue(row: Row, field: string): unknown {
  return field.split(".").reduce<unknown>((value, segment) => (
    value && typeof value === "object" ? (value as Record<string, unknown>)[segment] : undefined
  ), row);
}

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
        return { collect: async () => this.rows.filter((row) => filters.every(([field, value]) => fieldValue(row, field) === value)) };
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

function authorityFields(row: Row) {
  const { _id: _id, ...fields } = row;
  return fields;
}

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
                return snapshot.filter((row) => filters.every(([field, value]) => fieldValue(row, field) === value));
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

describe("registered Convex outreach review authority handlers", () => {
  const previous = {
    write: process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
    read: process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
    review: process.env.OUTREACH_REVIEW_CAPABILITY,
    decision: process.env.OUTREACH_DECISION_CAPABILITY,
    verifierActor: process.env.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID,
  };

  beforeEach(() => {
    process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY = "authority-write-secret";
    process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY = "authority-read-secret";
    process.env.OUTREACH_REVIEW_CAPABILITY = "review-secret";
    process.env.OUTREACH_DECISION_CAPABILITY = "decision-secret";
    process.env.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID = "verifier-1";
  });

  afterEach(() => {
    for (const [name, value] of [
      ["OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY", previous.write],
      ["OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY", previous.read],
      ["OUTREACH_REVIEW_CAPABILITY", previous.review],
      ["OUTREACH_DECISION_CAPABILITY", previous.decision],
      ["OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID", previous.verifierActor],
    ] as const) {
      if (value === undefined) delete process.env[name]; else process.env[name] = value;
    }
  });

  test("first insert stores and returns the exact domain authority without a capability", async () => {
    const db = new MemoryDb();
    const result = await createAuthorityHandler(ctx(db), authoritySubmission());
    expect(result.created).toBe(true);
    expect(Object.keys(result.authority).sort()).toEqual([
      "authorityBundleHash", "authorityRevision", "builderActorId", "candidateId", "draftSha256",
      "drafterActorId", "observedAt", "reviewId", "verifierActorId", "verifierGitBinding",
      "verifierReportSha256",
    ].sort());
    expect(result.authority).toEqual(authorityFields(db.rows[0]));
    expect(/^review_[a-f0-9]{20}$/.test(result.authority.reviewId)).toBe(true);
    expect(/^review_authority_[a-f0-9]{20}$/.test(result.authority.authorityRevision)).toBe(true);
    expect(Number.isSafeInteger(result.authority.observedAt)).toBe(true);
    expect(result.authority.verifierActorId).toBe("verifier-1");
    expect(Object.keys(db.rows[0]).includes("capability")).toBe(false);
  });

  test("maps verifier identity only from mandatory server config before database access", async () => {
    for (const configured of [undefined, "", "   ", "x".repeat(129), "bad\nactor"]) {
      if (configured === undefined) delete process.env.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID;
      else process.env.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID = configured;
      const db = new MemoryDb();
      expect(await rejectedMessage(() => createAuthorityHandler(ctx(db), authoritySubmission())))
        .toContain("OUTREACH_REVIEW_AUTHORITY_NOT_CONFIGURED");
      expect({ reads: db.reads, writes: db.writes }).toEqual({ reads: 0, writes: 0 });
    }
    process.env.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID = "verifier-1";

    const registeredArgs = JSON.parse((createOutreachReviewAuthority as unknown as {
      exportArgs: () => string;
    }).exportArgs());
    expect(Object.keys(registeredArgs.value)).not.toContain("verifierActorId");
  });

  test("exact retry returns the original authority unchanged and conflicting retry is rejected", async () => {
    const db = new MemoryDb();
    const first = await createAuthorityHandler(ctx(db), authoritySubmission());
    const original = structuredClone(first.authority);
    const retry = await createAuthorityHandler(ctx(db), authoritySubmission());
    expect(retry).toEqual({ created: false, authority: original });
    expect(db.rows.map(authorityFields)).toEqual([original]);
    expect(await rejectedMessage(() => createAuthorityHandler(ctx(db), authoritySubmission({ drafterActorId: "drafter-2" }))))
      .toContain("OUTREACH_REVIEW_AUTHORITY_CONFLICT");
    expect(db.rows.map(authorityFields)).toEqual([original]);
  });

  test("different valid verifier Git bindings are independent first writes", async () => {
    const db = new MemoryDb();
    const first = await createAuthorityHandler(ctx(db), authoritySubmission());
    const siblingInput = authoritySubmission({
      verifierGitBinding: {
        ...authoritySubmission().verifierGitBinding,
        path: "reviews/sibling.json",
      },
    });
    const sibling = await createAuthorityHandler(ctx(db), siblingInput);
    expect(first.created).toBe(true);
    expect(sibling.created).toBe(true);
    expect(db.rows).toHaveLength(2);
    expect(await createAuthorityHandler(ctx(db), siblingInput)).toEqual({ created: false, authority: sibling.authority });
    expect(await createAuthorityHandler(ctx(db), authoritySubmission())).toEqual({ created: false, authority: first.authority });
  });

  test("optimistic concurrent identical writes converge and conflicting writes fail closed", async () => {
    const identicalStore = new OptimisticStore();
    const [left, right] = await Promise.all([
      identicalStore.run(createAuthorityHandler, authoritySubmission()),
      identicalStore.run(createAuthorityHandler, authoritySubmission()),
    ]);
    expect(identicalStore.rows).toHaveLength(1);
    expect([left.created, right.created].sort()).toEqual([false, true]);
    expect(left.authority).toEqual(right.authority);

    const conflictingStore = new OptimisticStore();
    const attempts = await Promise.allSettled([
      conflictingStore.run(createAuthorityHandler, authoritySubmission()),
      conflictingStore.run(createAuthorityHandler, authoritySubmission({ builderActorId: "builder-2" })),
    ]);
    expect(conflictingStore.rows).toHaveLength(1);
    expect(attempts.filter((result) => result.status === "fulfilled")).toHaveLength(1);
    const rejected = attempts.find((result) => result.status === "rejected");
    expect(rejected?.status === "rejected" ? String(rejected.reason) : "")
      .toContain("OUTREACH_REVIEW_AUTHORITY_CONFLICT");
  });

  test("duplicate and corrupt stored authorities fail closed", async () => {
    for (const corruptRows of [
      async () => {
        const db = new MemoryDb();
        const created = await createAuthorityHandler(ctx(db), authoritySubmission());
        db.rows.push(structuredClone(created.authority));
        return db;
      },
      async () => {
        const db = new MemoryDb();
        await createAuthorityHandler(ctx(db), authoritySubmission());
        db.rows[0].authorityRevision = "caller-controlled";
        return db;
      },
    ]) {
      const db = await corruptRows();
      const writesBefore = db.writes;
      expect(await rejectedMessage(() => createAuthorityHandler(ctx(db), authoritySubmission())))
        .toContain("OUTREACH_REVIEW_AUTHORITY_CORRUPT");
      expect(await rejectedMessage(() => authorityLookupHandler(ctx(db), authorityLookup())))
        .toContain("OUTREACH_REVIEW_AUTHORITY_CORRUPT");
      expect(db.writes).toBe(writesBefore);
    }
  });

  test("exact lookup returns the authority and absent lookup returns closed route data", async () => {
    const db = new MemoryDb();
    const created = await createAuthorityHandler(ctx(db), authoritySubmission());
    expect(await authorityLookupHandler(ctx(db), authorityLookup())).toEqual({
      authorized: true,
      authority: created.authority,
    });
    expect(await authorityLookupHandler(ctx(db), authorityLookup(authoritySubmission({ candidateId: "absent" })))).toEqual({
      authorized: false,
    });
    const changedBinding = authorityLookup();
    changedBinding.verifierGitBinding.path = "reviews/other.json";
    expect(await authorityLookupHandler(ctx(db), changedBinding)).toEqual({ authorized: false });
  });

  test("write and read authenticate all four pairwise-distinct capabilities before database access", async () => {
    const calls = [
      (db: MemoryDb, capability: any) => createAuthorityHandler(ctx(db), authoritySubmission({ capability })),
      (db: MemoryDb, capability: any) => authorityLookupHandler(ctx(db), { ...authorityLookup(), capability }),
    ];
    for (const [index, call] of calls.entries()) {
      const expected = index === 0 ? "authority-write-secret" : "authority-read-secret";
      for (const candidate of [undefined, "wrong", "authority-write-secret", "authority-read-secret", "review-secret", "decision-secret"]
        .filter((value) => value !== expected)) {
        const db = new MemoryDb();
        expect(await rejectedMessage(() => call(db, candidate))).toContain("server capability required");
        expect({ reads: db.reads, writes: db.writes }).toEqual({ reads: 0, writes: 0 });
      }
    }

    for (const [name, collision] of [
      ["OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY", "authority-write-secret"],
      ["OUTREACH_REVIEW_CAPABILITY", "authority-write-secret"],
      ["OUTREACH_DECISION_CAPABILITY", "authority-read-secret"],
    ] as const) {
      const original = process.env[name];
      process.env[name] = collision;
      const db = new MemoryDb();
      expect(await rejectedMessage(() => createAuthorityHandler(ctx(db), authoritySubmission())))
        .toContain("capability configuration is invalid");
      expect({ reads: db.reads, writes: db.writes }).toEqual({ reads: 0, writes: 0 });
      process.env[name] = original;
    }
  });
});
