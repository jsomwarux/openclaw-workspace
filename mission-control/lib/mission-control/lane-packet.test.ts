import { describe, expect, test } from "bun:test";
import {
  DONE_EVIDENCE_TYPES,
  GROWTH_LANES,
  LANE_PACKET_SCHEMA,
  LanePacketError,
  hashLanePacketPayload,
  isLanePacket,
  lanePacketDedupeKey,
  resolveLanePacketAdmission,
  signalLaneForGrowthLane,
  validateLanePacketSubmission,
  type StoredLanePacketTask,
} from "./lane-packet";
import { FIXTURE_NOW, jobsPacketFixture, linkedinPacketFixture } from "./lane-packet-fixtures";

const DAY_MS = 24 * 60 * 60 * 1000;

function failure(run: () => unknown): { code: string; message: string } {
  try {
    run();
  } catch (error) {
    if (error instanceof LanePacketError) return { code: error.code, message: error.message };
    return { code: "non-contract-error", message: String(error) };
  }
  return { code: "none", message: "" };
}

async function asyncFailure(run: () => Promise<unknown>): Promise<{ code: string; message: string }> {
  try {
    await run();
  } catch (error) {
    if (error instanceof LanePacketError) return { code: error.code, message: error.message };
    return { code: "non-contract-error", message: String(error) };
  }
  return { code: "none", message: "" };
}

function validJobs(overrides: Record<string, unknown> = {}) {
  return { ...jobsPacketFixture(), ...overrides } as Record<string, unknown>;
}

async function admittedTask(submission = jobsPacketFixture(), id = "task-1"): Promise<StoredLanePacketTask> {
  const resolved = await resolveLanePacketAdmission([], validateLanePacketSubmission(submission, FIXTURE_NOW), FIXTURE_NOW);
  if (resolved.operation !== "create") throw new Error("expected create");
  return { _id: id, ...resolved.fields } as StoredLanePacketTask;
}

describe("typed eight-lane enum", () => {
  test("is exactly the eight Growth OS lanes, in canonical order", () => {
    expect([...GROWTH_LANES]).toEqual([
      "linkedin", "x", "outreach", "jobs", "apps", "passive-income", "networking", "profile-site",
    ]);
  });

  test("rejects a lane outside the enum, including the legacy Signal lanes", () => {
    for (const lane of ["revenue", "ship", "work", "LinkedIn", "", "content"]) {
      expect(failure(() => validateLanePacketSubmission(validJobs({ lane }), FIXTURE_NOW)).code).toBe("invalid");
    }
  });

  test("derives the Signal routing lane server-side for every growth lane", () => {
    const derived = GROWTH_LANES.map((lane) => [lane, signalLaneForGrowthLane(lane)]);
    expect(derived).toEqual([
      ["linkedin", "ship"], ["x", "ship"], ["outreach", "revenue"], ["jobs", "revenue"],
      ["apps", "ship"], ["passive-income", "ship"], ["networking", "work"], ["profile-site", "ship"],
    ]);
  });
});

describe("submission validation", () => {
  test("accepts the Jobs and LinkedIn fixtures", () => {
    expect(validateLanePacketSubmission(jobsPacketFixture(), FIXTURE_NOW).lane).toBe("jobs");
    expect(validateLanePacketSubmission(linkedinPacketFixture(), FIXTURE_NOW).lane).toBe("linkedin");
  });

  test("requires every seven-field card field that is not optional", () => {
    for (const field of ["title", "whyItMatters", "exactSteps", "doneState"]) {
      const input = validJobs();
      delete input[field];
      expect(failure(() => validateLanePacketSubmission(input, FIXTURE_NOW)).code).toBe("invalid");
    }
    expect(failure(() => validateLanePacketSubmission(validJobs({ exactSteps: [] }), FIXTURE_NOW)).code).toBe("invalid");
    expect(failure(() => validateLanePacketSubmission(validJobs({ exactSteps: ["ok", "  "] }), FIXTURE_NOW)).code).toBe("invalid");
    expect(failure(() => validateLanePacketSubmission(validJobs({ title: "   " }), FIXTURE_NOW)).code).toBe("invalid");
  });

  test("requires a paste destination whenever a paste-ready prompt is supplied", () => {
    const input = validJobs();
    delete input.pasteDestination;
    expect(failure(() => validateLanePacketSubmission(input, FIXTURE_NOW)).message).toBe("pasteDestination is required with pasteReadyPrompt");
  });

  test("requires the envelope: artifactRef, doneEvidenceType, expiresAt, estMinutes", () => {
    for (const field of ["artifactRef", "doneEvidenceType", "expiresAt", "estMinutes", "dedupeKey", "sourceSystem"]) {
      const input = validJobs();
      delete input[field];
      expect(failure(() => validateLanePacketSubmission(input, FIXTURE_NOW)).code).toBe("invalid");
    }
  });

  test("types artifactRef as { system, id, url?, sha256 } with a lowercase SHA-256", () => {
    const bad = [
      { system: "drive", id: "x", sha256: "A".repeat(64) },
      { system: "drive", id: "x", sha256: "1".repeat(63) },
      { system: "", id: "x", sha256: "1".repeat(64) },
      { system: "drive", id: "", sha256: "1".repeat(64) },
      { system: "drive", id: "x", sha256: "1".repeat(64), url: "javascript:alert(1)" },
      { system: "drive", id: "x", sha256: "1".repeat(64), extra: true },
    ];
    for (const artifactRef of bad) {
      expect(failure(() => validateLanePacketSubmission(validJobs({ artifactRef }), FIXTURE_NOW)).code).toBe("invalid");
    }
    const noUrl = validateLanePacketSubmission(validJobs({ artifactRef: { system: "jt-ops", id: "p/1", sha256: "3".repeat(64) } }), FIXTURE_NOW);
    expect(noUrl.artifactRef).toEqual({ system: "jt-ops", id: "p/1", sha256: "3".repeat(64) });
  });

  test("types doneEvidenceType to the enumerated evidence kinds", () => {
    expect([...DONE_EVIDENCE_TYPES]).toEqual([
      "post-url", "message-ref", "application-ref", "rsvp-ref", "profile-edit-ref", "deploy-ref", "none",
    ]);
    expect(failure(() => validateLanePacketSubmission(validJobs({ doneEvidenceType: "screenshot" }), FIXTURE_NOW)).code).toBe("invalid");
  });

  test("bounds expiresAt to the future and estMinutes to a positive whole number", () => {
    expect(failure(() => validateLanePacketSubmission(validJobs({ expiresAt: FIXTURE_NOW }), FIXTURE_NOW)).code).toBe("invalid");
    expect(failure(() => validateLanePacketSubmission(validJobs({ expiresAt: FIXTURE_NOW + 91 * DAY_MS }), FIXTURE_NOW)).code).toBe("invalid");
    for (const estMinutes of [0, -5, 2.5, 481, Number.NaN]) {
      expect(failure(() => validateLanePacketSubmission(validJobs({ estMinutes }), FIXTURE_NOW)).code).toBe("invalid");
    }
  });

  test("rejects forged governed state instead of silently dropping it", () => {
    const forged = [
      ["approvalState", "approved"],
      ["approvedPayloadHash", "4".repeat(64)],
      ["admittedPayloadHash", "4".repeat(64)],
      ["outcomeRef", { system: "job-tracker", id: "applied-1" }],
      ["closureReason", { kind: "skipped" }],
      ["doneEvidence", { type: "application-ref", ref: "X" }],
      ["packetSchema", LANE_PACKET_SCHEMA],
      ["growthLane", "jobs"],
      ["status", "done"],
      ["assignee", "eve"],
      ["feedback", []],
      ["rankScore", 99],
      ["reasonCodes", ["cash:9000"]],
    ] as const;
    for (const [field, value] of forged) {
      expect(failure(() => validateLanePacketSubmission(validJobs({ [field]: value }), FIXTURE_NOW))).toEqual({
        code: "invalid",
        message: "governed lane packet fields are server-derived",
      });
    }
  });

  test("never lets generic admission carry outreach review or decision state", () => {
    const outreach = [
      ["outreachReview", {}], ["outreachDecision", {}], ["candidateId", "c-1"], ["cohortId", "cohort-2"],
      ["draftSha256", "5".repeat(64)], ["snapshotSha256", "5".repeat(64)], ["reviewCycle", 1],
      ["decision", "approve"], ["suppressionBinding", {}],
    ] as const;
    for (const [field, value] of outreach) {
      const input = validJobs({ lane: "outreach", [field]: value });
      expect(failure(() => validateLanePacketSubmission(input, FIXTURE_NOW))).toEqual({
        code: "invalid",
        message: "outreach review and decision state requires the specialized outreach routes",
      });
    }
  });

  test("rejects unknown fields and a reserved or malformed producer dedupe key", () => {
    expect(failure(() => validateLanePacketSubmission(validJobs({ surprise: 1 }), FIXTURE_NOW)).message).toBe("unsupported lane packet field");
    for (const dedupeKey of ["lane-packet:v1:jobs:x", "", "has space", "a".repeat(201)]) {
      expect(failure(() => validateLanePacketSubmission(validJobs({ dedupeKey }), FIXTURE_NOW)).code).toBe("invalid");
    }
    expect(failure(() => validateLanePacketSubmission(validJobs({ sourceSystem: "nightly-validation-controller" }), FIXTURE_NOW)).code).toBe("invalid");
  });

  test("error messages never echo caller input", () => {
    const secretish = "CANARY-INPUT-MUST-NOT-ECHO";
    const messages = [
      failure(() => validateLanePacketSubmission(validJobs({ lane: secretish }), FIXTURE_NOW)).message,
      failure(() => validateLanePacketSubmission(validJobs({ [secretish]: 1 }), FIXTURE_NOW)).message,
      failure(() => validateLanePacketSubmission(validJobs({ dedupeKey: `${secretish} x` }), FIXTURE_NOW)).message,
    ];
    for (const message of messages) expect(message.includes(secretish)).toBe(false);
  });
});

describe("payload hash", () => {
  test("is deterministic, key-order independent, and covers the card content", async () => {
    const base = validateLanePacketSubmission(jobsPacketFixture(), FIXTURE_NOW);
    const reordered = validateLanePacketSubmission(
      Object.fromEntries(Object.entries(jobsPacketFixture()).reverse()),
      FIXTURE_NOW,
    );
    expect(await hashLanePacketPayload(base)).toBe(await hashLanePacketPayload(reordered));
    expect(/^[a-f0-9]{64}$/.test(await hashLanePacketPayload(base))).toBe(true);

    for (const change of [
      { title: "Different title" },
      { exactSteps: ["Only one step"] },
      { pasteReadyPrompt: "Different prompt" },
      { doneState: "Different done" },
      { artifactRef: { ...base.artifactRef, sha256: "9".repeat(64) } },
      { doneEvidenceType: "message-ref" as const },
    ]) {
      expect(await hashLanePacketPayload({ ...base, ...change })).not.toBe(await hashLanePacketPayload(base));
    }
  });

  test("ignores scheduling metadata that does not change what JT approves", async () => {
    const base = validateLanePacketSubmission(jobsPacketFixture(), FIXTURE_NOW);
    const rescheduled = { ...base, expiresAt: base.expiresAt + DAY_MS, estMinutes: 40, priority: "high" as const };
    expect(await hashLanePacketPayload(rescheduled)).toBe(await hashLanePacketPayload(base));
  });
});

describe("idempotent create-only admission keyed by dedupeKey + payloadHash", () => {
  test("creates a server-derived pending packet on first admission", async () => {
    const submission = validateLanePacketSubmission(jobsPacketFixture(), FIXTURE_NOW);
    const resolved = await resolveLanePacketAdmission([], submission, FIXTURE_NOW);
    expect(resolved.operation).toBe("create");
    if (resolved.operation !== "create") return;
    const payloadHash = await hashLanePacketPayload(submission);
    expect(resolved.fields).toMatchObject({
      packetSchema: LANE_PACKET_SCHEMA,
      growthLane: "jobs",
      lane: "revenue",
      status: "todo",
      assignee: "jt",
      priority: "medium",
      approvalState: "pending",
      payloadHash,
      admittedPayloadHash: payloadHash,
      dedupeKey: lanePacketDedupeKey("jobs", submission.dedupeKey),
      createdAt: FIXTURE_NOW,
      updatedAt: FIXTURE_NOW,
    });
    for (const absent of ["outcomeRef", "closureReason", "doneEvidence", "approvedPayloadHash", "outreachReview", "outreachDecision", "feedback"]) {
      expect(absent in resolved.fields).toBe(false);
    }
    expect(Object.values(resolved.fields).some((value) => value === undefined)).toBe(false);
  });

  test("namespaces the stored dedupe key by schema version and lane", () => {
    expect(lanePacketDedupeKey("linkedin", "eve:post:1")).toBe("lane-packet:v1:linkedin:eve:post:1");
  });

  test("an exact retry returns the existing packet without a write, even after the card was edited", async () => {
    const existing = await admittedTask();
    const edited = { ...existing, payloadHash: "8".repeat(64), approvalState: "pending" as const };
    const resolved = await resolveLanePacketAdmission([edited], validateLanePacketSubmission(jobsPacketFixture(), FIXTURE_NOW), FIXTURE_NOW + 1000);
    expect(resolved).toMatchObject({ operation: "existing", id: "task-1", payloadHash: "8".repeat(64), approvalState: "pending" });
  });

  test("a different payload for an open packet with the same key is a conflict, not a silent replace", async () => {
    const existing = await admittedTask();
    const changed = validateLanePacketSubmission(jobsPacketFixture({ title: "Apply: revised title" }), FIXTURE_NOW);
    expect(await asyncFailure(() => resolveLanePacketAdmission([existing], changed, FIXTURE_NOW))).toEqual({
      code: "conflict",
      message: "an open lane packet with this dedupeKey has a different payload",
    });
  });

  test("a revised payload may be admitted as a new packet once every prior version is closed", async () => {
    const closed = { ...(await admittedTask()), status: "archived" as const, closureReason: { kind: "rejected" as const, closedAt: FIXTURE_NOW, closedBy: "jt" as const } };
    const revised = validateLanePacketSubmission(jobsPacketFixture({ title: "Apply: revised title" }), FIXTURE_NOW);
    const resolved = await resolveLanePacketAdmission([closed], revised, FIXTURE_NOW);
    expect(resolved.operation).toBe("create");
  });

  test("fails closed when the namespaced key belongs to a non-packet task", async () => {
    const legacy = { _id: "legacy-1", title: "Legacy", status: "todo", dedupeKey: lanePacketDedupeKey("jobs", jobsPacketFixture().dedupeKey) };
    const outreachCard = { ...legacy, _id: "outreach-1", outreachReview: { snapshotSha256: "6".repeat(64) } };
    for (const task of [legacy, outreachCard]) {
      expect(await asyncFailure(() => resolveLanePacketAdmission([task as StoredLanePacketTask], validateLanePacketSubmission(jobsPacketFixture(), FIXTURE_NOW), FIXTURE_NOW))).toEqual({
        code: "conflict",
        message: "dedupeKey belongs to a task that is not a lane packet",
      });
    }
  });

  test("a producer-asserted payloadHash must equal the server-computed hash", async () => {
    const submission = validateLanePacketSubmission(jobsPacketFixture(), FIXTURE_NOW);
    const computed = await hashLanePacketPayload(submission);
    const asserted = validateLanePacketSubmission({ ...jobsPacketFixture(), payloadHash: computed }, FIXTURE_NOW);
    expect((await resolveLanePacketAdmission([], asserted, FIXTURE_NOW)).operation).toBe("create");
    const wrong = validateLanePacketSubmission({ ...jobsPacketFixture(), payloadHash: "7".repeat(64) }, FIXTURE_NOW);
    expect(await asyncFailure(() => resolveLanePacketAdmission([], wrong, FIXTURE_NOW))).toEqual({
      code: "invalid",
      message: "payloadHash does not match the server-computed payload hash",
    });
  });

  test("isLanePacket recognizes only server-admitted packets", async () => {
    expect(isLanePacket(await admittedTask())).toBe(true);
    expect(isLanePacket({ _id: "x", title: "Legacy" })).toBe(false);
    expect(isLanePacket({ _id: "x", title: "Legacy", growthLane: "jobs" })).toBe(false);
    expect(isLanePacket(null)).toBe(false);
  });
});
