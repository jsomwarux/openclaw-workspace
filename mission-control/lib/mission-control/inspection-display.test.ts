import { describe, expect, test } from "bun:test";
import { formatAuditField, formatAuditValue, needsEvidenceAttention } from "./inspection-display";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal> = {}): Signal {
  return {
    id: "t1",
    source: "task",
    title: "Task",
    owner: "jt",
    status: "in-progress",
    lane: "revenue",
    ageDays: 0,
    evidence: [],
    updatedAt: 0,
    raw: {},
    ...overrides,
  };
}

describe("inspection display helpers", () => {
  test("formats audit field labels for humans", () => {
    expect(formatAuditField("dueDate")).toBe("Due date");
    expect(formatAuditField("stageProbability")).toBe("Stage probability");
    expect(formatAuditField("dollars")).toBe("Dollars");
  });

  test("formats due-date audit values instead of leaking epoch milliseconds", () => {
    expect(formatAuditValue("dueDate", "1786485600000")).toBe("Aug 11, 2026");
    expect(formatAuditValue("dueDate", "")).toBe("None");
  });

  test("formats money and probability audit values", () => {
    expect(formatAuditValue("dollars", "2250")).toBe("$2,250");
    expect(formatAuditValue("stageProbability", "0.55")).toBe("55%");
  });

  test("only shows an evidence warning when proof is required or a gap ref exists", () => {
    expect(needsEvidenceAttention(signal())).toBe(false);
    expect(needsEvidenceAttention(signal({ proofRequired: true }))).toBe(true);
    expect(needsEvidenceAttention(signal({ evidence: [{ kind: "unknown", label: "No proof ref", quality: "gap" }] }))).toBe(true);
  });
});
