import { describe, expect, test } from "bun:test";
import { normalizeTaskInput, validateTaskAdmission } from "./task-admission";

function errorMessage(run: () => void): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

const admitted = {
  title: "Promoted validation",
  sourceSystem: "nightly-validation-controller",
  dedupeKey: "nightly-validation:candidate:hash",
  firstAction: "Open the artifact",
  whyItMatters: "It could compound",
  doneState: "Decision recorded",
  evidenceLinks: ["memory/agent-portfolio/runs/2026-08-24/promotions.json"],
  workstream: "compounding-bet",
  promotionScore: 32,
  verdict: "promote",
  verifierConfirmed: true,
  verifiedAt: new Date().toISOString(),
  candidateId: "candidate",
  sourceHash: "sha256:hash",
  evidenceScore: 4,
  distributionScore: 3,
  fatalConstraint: false,
};

describe("task admission contract", () => {
  test("preserves every additive operating-system field", () => {
    expect(normalizeTaskInput({
      ...admitted,
      reviewAt: 1_800_000_000_000,
      hypothesis: "Demand exists",
      nextTest: "Run three interviews",
      killDate: 1_810_000_000_000,
      revivalTrigger: "A buyer requests it",
    })).toMatchObject({
      ...admitted,
      reviewAt: 1_800_000_000_000,
      hypothesis: "Demand exists",
      nextTest: "Run three interviews",
      killDate: 1_810_000_000_000,
      revivalTrigger: "A buyer requests it",
    });
  });

  test("preserves audit metadata only for update callers", () => {
    expect(normalizeTaskInput({ title: "Task", auditSource: "jt", auditEvidence: "Manual review" })).toEqual({ title: "Task" });
    expect(normalizeTaskInput(
      { title: "Task", auditSource: "jt", auditEvidence: "Manual review" },
      { includeAudit: true },
    )).toEqual({ title: "Task", auditSource: "jt", auditEvidence: "Manual review" });
  });

  test("rejects below-threshold nightly promotions", () => {
    expect(errorMessage(() => validateTaskAdmission({ ...admitted, promotionScore: 29 }))).toContain("promotionScore");
  });

  test("enforces the complete nightly verifier gate", () => {
    const cases: Array<[string, Record<string, unknown>]> = [
      ["verdict", { verdict: "continue" }],
      ["verifierConfirmed", { verifierConfirmed: false }],
      ["verifiedAt", { verifiedAt: "2026-08-20T00:00:00Z" }],
      ["candidateId", { candidateId: "" }],
      ["sourceHash", { sourceHash: "" }],
      ["evidenceScore", { evidenceScore: 3 }],
      ["distributionScore", { distributionScore: 2 }],
      ["fatalConstraint", { fatalConstraint: true }],
    ];
    for (const [field, override] of cases) {
      expect(errorMessage(() => validateTaskAdmission({ ...admitted, ...override }, new Date("2026-08-24T23:30:00Z")))).toContain(field);
    }
  });

  test("rejects legacy nightly aliases before normalization can hide them", () => {
    expect(errorMessage(() => validateTaskAdmission({ title: "Bypass", source: "nightly-validation-controller" }))).toContain("sourceSystem");
    expect(errorMessage(() => validateTaskAdmission({ title: "Bypass", dedupe_key: "nightly-validation:c:h" }))).toContain("dedupeKey");
    expect(errorMessage(() => validateTaskAdmission({ title: "Bypass", verifier_confirmed: true }))).toContain("snake_case");
  });

  test("rejects incomplete nightly promotions but leaves legacy callers compatible", () => {
    expect(errorMessage(() => validateTaskAdmission({ title: "Incomplete", sourceSystem: "nightly-validation-controller" }))).toContain("dedupeKey");
    expect(errorMessage(() => validateTaskAdmission({ title: "Legacy task" }))).toBe(undefined);
  });
});
