import { describe, expect, test } from "bun:test";
import {
  canonicalJson,
  hashCanonicalJson,
  hashOutreachReviewSubmission,
  resolveOutreachReviewAdmission,
  summarizeOutreachReviews,
  validateOutreachReviewSubmission,
  type OutreachReviewSubmission,
  type StoredOutreachReviewTask,
} from "./outreach-review";
import { hashSuppressionBinding } from "./outreach-suppression-binding";

const SHA = "a".repeat(64);
const COMMIT = "b".repeat(40);

function binding(path: string) {
  return { repository: "owner/repo", commitSha: COMMIT, path, blobSha256: SHA };
}

function submission(overrides: Partial<OutreachReviewSubmission> = {}): OutreachReviewSubmission {
  return {
    candidateId: "candidate-1",
    cohortId: "cohort-2",
    draftSha256: SHA,
    subject: "A useful subject",
    body: "Hello buyer,\n\nThis is the exact draft.",
    verifierReport: "VERDICT: CONFIRM\nFailures: none.",
    reviewAuthorityId: "jt",
    verifierActorId: "verifier-1",
    gitBindings: {
      evidence: binding("evidence.json"),
      policy: binding("policy.json"),
      gate: binding("gate.json"),
      draft: binding("draft.txt"),
      verifier: binding("verifier.md"),
    },
    ...overrides,
  };
}

function thrown(run: () => unknown): boolean {
  try {
    run();
    return false;
  } catch {
    return true;
  }
}

async function storedTask(id: string, input: OutreachReviewSubmission, cycle: 1 | 2, now = 100): Promise<StoredOutreachReviewTask> {
  const snapshotSha256 = await hashOutreachReviewSubmission(input);
  return {
    _id: id,
    candidateId: input.candidateId,
    cohortId: input.cohortId,
    draftSha256: input.draftSha256,
    status: "todo",
    outreachReview: { ...input, snapshotSha256, reviewCycle: cycle, admittedBy: "server", admittedAt: now },
  };
}

async function errorCode(run: () => Promise<unknown>) {
  try { await run(); } catch (error) { return error && typeof error === "object" && "code" in error ? error.code : undefined; }
  return undefined;
}

describe("canonical outreach review snapshot", () => {
  test("accepts an exact copy-free suppression binding only when it matches the protected gate binding", async () => {
    const base = submission();
    const withoutHash = {
      schemaVersion: "outreach-suppression-binding-v1" as const,
      repository: "owner/repo", commitSha: COMMIT, gatePath: "gate.json", gateBlobSha256: SHA,
      gateArtifactHash: "c".repeat(64), admissionCommitSha: "d".repeat(40), admissionPath: "admission/candidate.json", admissionBlobSha256: "e".repeat(64),
      channelAttestationId: `channel_${"f".repeat(20)}`, channelOwnerRevision: "1".repeat(64),
      prospectId: "candidate-1", organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64),
    };
    const suppressionBinding = { ...withoutHash, bindingHash: await hashSuppressionBinding(withoutHash) };
    const bound = { ...base, reviewAuthorityId: "review_" + "3".repeat(20), suppressionBinding };
    validateOutreachReviewSubmission(bound);
    expect(await hashOutreachReviewSubmission(bound)).not.toBe(await hashOutreachReviewSubmission(base));
    expect(thrown(() => validateOutreachReviewSubmission({ ...bound, suppressionBinding: { ...suppressionBinding, gatePath: "other.json" } }))).toBe(true);
    expect(thrown(() => validateOutreachReviewSubmission({ ...bound, suppressionBinding: { ...suppressionBinding, channel: "owner@example.org" } }))).toBe(true);
  });

  test("uses deterministic canonical JSON and the versioned SHA-256 golden vector", async () => {
    const value = { version: 1, snapshot: { candidateId: "candidate-1" }, domain: "mission-control/outreach-review-snapshot" };
    expect(canonicalJson(value)).toBe('{"domain":"mission-control/outreach-review-snapshot","snapshot":{"candidateId":"candidate-1"},"version":1}');
    expect(await hashCanonicalJson(value)).toBe("ef5e31cf315c3c5f4d83a6f6ebdbc621a85677e1b884f312f3bd96f3c4f4843e");
    expect(canonicalJson({ b: 2, a: 1 })).toBe(canonicalJson({ a: 1, b: 2 }));
    expect(canonicalJson(["a", "b"])).not.toBe(canonicalJson(["b", "a"]));
    expect(canonicalJson({ text: "café" })).toBe('{"text":"café"}');
  });

  test("rejects identity aliases, unsafe Git bindings, lone surrogates, and oversized content", () => {
    for (const bad of [" candidate-1", "candidate-1 ", "Candidate-1", "candidaté-1", ""] as const) {
      expect(thrown(() => validateOutreachReviewSubmission(submission({ candidateId: bad })))).toBe(true);
    }
    for (const path of ["/absolute", "../escape", "a/../b", "a//b", "a\\b", "a/./b", "bad\0path"] as const) {
      expect(thrown(() => validateOutreachReviewSubmission(submission({ gitBindings: { ...submission().gitBindings, evidence: binding(path) } })))).toBe(true);
    }
    expect(thrown(() => validateOutreachReviewSubmission(submission({ body: "\ud800" })))).toBe(true);
    expect(thrown(() => validateOutreachReviewSubmission(submission({ subject: "x".repeat(201) })))).toBe(true);
    expect(thrown(() => validateOutreachReviewSubmission(submission({ body: "x".repeat(20_001) })))).toBe(true);
    expect(thrown(() => validateOutreachReviewSubmission(submission({ verifierReport: "x".repeat(20_001) })))).toBe(true);
  });

  test("every submitted field changes the snapshot hash", async () => {
    const original = submission();
    const baseline = await hashOutreachReviewSubmission(original);
    const variants = [
      submission({ candidateId: "candidate-2" }), submission({ cohortId: "cohort-3" }),
      submission({ draftSha256: "c".repeat(64) }), submission({ subject: "Changed" }),
      submission({ body: "Changed" }), submission({ verifierReport: "VERDICT: FAIL" }),
      submission({ reviewAuthorityId: "jt-2" }), submission({ verifierActorId: "verifier-2" }),
      submission({ gitBindings: { ...original.gitBindings, evidence: binding("other.json") } }),
    ];
    for (const variant of variants) expect(await hashOutreachReviewSubmission(variant)).not.toBe(baseline);
  });
});

describe("server-owned two-cycle admission", () => {
  test("creates server-derived immutable cycle one fields", async () => {
    const result = await resolveOutreachReviewAdmission([], submission(), 123);
    expect(result.operation).toBe("create");
    if (result.operation !== "create") throw new Error("expected create");
    expect(result.fields).toMatchObject({
      candidateId: "candidate-1", cohortId: "cohort-2", draftSha256: SHA,
      status: "todo", assignee: "jt", priority: "high",
      outreachReview: { ...submission(), reviewCycle: 1, admittedBy: "server", admittedAt: 123 },
    });
    expect(result.fields.description).not.toContain(submission().body);
    expect(result.fields.description).not.toContain(submission().verifierReport);
    expect(result.fields.dedupeKey).toContain(result.fields.outreachReview.snapshotSha256);
    expect("capability" in result.fields).toBe(false);
  });

  test("returns one exact retry unchanged, then allocates cycle two and rejects a third", async () => {
    const first = await storedTask("task-1", submission(), 1);
    expect(await resolveOutreachReviewAdmission([first], submission(), 999)).toEqual({
      operation: "existing", taskId: "task-1", reviewCycle: 1,
      snapshotSha256: first.outreachReview!.snapshotSha256,
    });
    const secondInput = submission({ verifierReport: "VERDICT: REVISE" });
    const second = await resolveOutreachReviewAdmission([first], secondInput, 200);
    expect(second.operation).toBe("create");
    if (second.operation !== "create") throw new Error("expected create");
    expect(second.fields.outreachReview.reviewCycle).toBe(2);
    const secondStored = await storedTask("task-2", secondInput, 2, 200);
    expect(await errorCode(() => resolveOutreachReviewAdmission([first, secondStored], submission({ body: "third draft" }), 300)))
      .toBe("cycle_limit");
  });

  test("validates the complete authoritative set before allowing an exact retry", async () => {
    const first = await storedTask("task-1", submission(), 1);
    expect(await errorCode(() => resolveOutreachReviewAdmission([first, { ...first, _id: "task-2" }], submission(), 999)))
      .toBe("corrupt_authority");
  });

  test("fails closed for duplicate cycles, gaps, malformed server snapshots, and more than two records", async () => {
    const first = await storedTask("task-1", submission(), 1);
    const second = await storedTask("task-2", submission({ verifierReport: "second" }), 2);
    expect(await errorCode(() => summarizeOutreachReviews([first, { ...second, outreachReview: { ...second.outreachReview!, reviewCycle: 1 } }], "candidate-1", "cohort-2"))).toBe("corrupt_authority");
    expect(await errorCode(() => summarizeOutreachReviews([{ ...second, outreachReview: { ...second.outreachReview!, reviewCycle: 2 } }], "candidate-1", "cohort-2"))).toBe("corrupt_authority");
    expect(await errorCode(() => summarizeOutreachReviews([{ ...first, outreachReview: { ...first.outreachReview!, snapshotSha256: "bad" } }], "candidate-1", "cohort-2"))).toBe("corrupt_authority");
    const third = await storedTask("task-3", submission({ body: "third" }), 2);
    expect(await errorCode(() => summarizeOutreachReviews([first, second, third], "candidate-1", "cohort-2"))).toBe("corrupt_authority");
  });

  test("ignores generic unmarked rows but never malformed server authority", async () => {
    const generic = { _id: "generic", candidateId: "candidate-1", cohortId: "cohort-2", status: "todo" };
    const result = await resolveOutreachReviewAdmission([generic], submission(), 123);
    expect(result.operation).toBe("create");
    if (result.operation !== "create") throw new Error("expected create");
    expect(result.fields.outreachReview.reviewCycle).toBe(1);
  });
});
