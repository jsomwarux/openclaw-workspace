import { describe, expect, test } from "bun:test";
import { primaryActionVerb, reasonChip, reasonChips } from "./reason-codes";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal> = {}): Signal {
  return {
    id: "t1",
    source: "task",
    title: "Task",
    owner: "jt",
    status: "in-progress",
    lane: "revenue",
    ageDays: 1,
    evidence: [],
    updatedAt: 0,
    raw: {},
    ...overrides,
  };
}

describe("reason chips", () => {
  test("renders cash codes as human money, not raw scorer output", () => {
    expect(reasonChip("cash:3500").label).toBe("$3,500");
    expect(reasonChip("cash:3500").tone).toBe("cash");
  });

  test("renders a deadline code as a short due date", () => {
    expect(reasonChip("deadline:2026-07-15").label).toBe("Due Jul 15");
  });

  test("renders unblock, proof, risk, stability, and nudge codes", () => {
    expect(reasonChip("unblocks:3").label).toBe("Unblocks 3");
    expect(reasonChip("unblocks:agent").label).toBe("Unblocks agent");
    expect(reasonChip("proof").label).toBe("Proof asset");
    expect(reasonChip("risk").label).toBe("Stops a loss");
    expect(reasonChip("stability").label).toBe("Stability");
    expect(reasonChip("nudge-due").label).toBe("Nudge due");
  });

  test("flags an unexplained rank in red so a silent scorer bug stays visible", () => {
    const chip = reasonChip("unexplained");

    expect(chip.label).toBe("Unexplained rank");
    expect(chip.tone).toBe("danger");
  });

  test("dedupes codes because scoreSignal merges stored and derived reasons", () => {
    expect(reasonChips(["proof", "proof", "risk"]).map((chip) => chip.label)).toEqual([
      "Proof asset",
      "Stops a loss",
    ]);
  });
});

describe("primary action verb", () => {
  test("an approval gate asks for approval", () => {
    expect(primaryActionVerb(signal({ status: "awaiting-approval" }))).toBe("Approve");
  });

  test("a due nudge asks for a nudge", () => {
    expect(primaryActionVerb(signal({ reasonCodes: ["nudge-due"] }))).toBe("Nudge");
  });

  test("a pitched deal with dollars asks to be marked sent", () => {
    expect(primaryActionVerb(signal({ dollars: 2250, pipelineStage: "pitched" }))).toBe("Mark sent");
  });

  test("dollars without a pitched stage stay a plain open", () => {
    expect(primaryActionVerb(signal({ dollars: 2250, pipelineStage: "lead" }))).toBe("Open");
  });

  test("anything else opens for inspection", () => {
    expect(primaryActionVerb(signal())).toBe("Open");
  });
});
