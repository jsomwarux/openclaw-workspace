import { describe, expect, test } from "bun:test";
import { commandQueue, computeScore, needsJT, scoreBand } from "./score";
import type { Factors, Signal } from "./types";

const now = Date.now();

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: "task-1",
    source: "task",
    title: "Approve Altmark retainer",
    owner: "jt",
    status: "awaiting-decision",
    lane: "revenue",
    priority: "high",
    ageDays: 1,
    evidence: [],
    updatedAt: now,
    raw: {},
    ...overrides,
  };
}

describe("computeScore", () => {
  test("weights revenue proximity, urgency, unblock, risk, and north star alignment", () => {
    const factors: Factors = {
      revenue: 3,
      unblock: 1,
      urgency: 2,
      risk: 1,
      northStar: 3,
      effortOver30: false,
    };

    expect(computeScore(factors)).toBe(70);
  });

  test("applies effort penalty without dropping below zero", () => {
    expect(
      computeScore({
        revenue: 0,
        unblock: 0,
        urgency: 0,
        risk: 0,
        northStar: 0,
        effortOver30: true,
      }),
    ).toBe(0);
  });
});

describe("scoreBand", () => {
  test("maps scores to high, medium, and low bands", () => {
    expect(scoreBand(70)).toBe("high");
    expect(scoreBand(40)).toBe("medium");
    expect(scoreBand(39)).toBe("low");
  });
});

describe("needsJT", () => {
  test("only qualifies JT-owned decision, approval, or blocked signals", () => {
    expect(needsJT(signal({ owner: "jt", status: "awaiting-decision" }))).toBe(true);
    expect(needsJT(signal({ owner: "jt", status: "awaiting-approval" }))).toBe(true);
    expect(needsJT(signal({ owner: "jt", status: "blocked" }))).toBe(true);
    expect(needsJT(signal({ owner: "eve", status: "blocked" }))).toBe(false);
    expect(needsJT(signal({ owner: "jt", status: "in-progress" }))).toBe(false);
  });
});

describe("commandQueue", () => {
  test("sorts JT decision work by computed score and caps at seven items", () => {
    const items = [
      signal({ id: "low", title: "Review low priority app idea", lane: "ship", priority: "low" }),
      signal({ id: "high", title: "Approve paid consulting step", lane: "revenue", dollars: 9000, priority: "high" }),
      signal({ id: "eve", title: "Eve is handling this", owner: "eve", lane: "machine", status: "in-progress" }),
      ...Array.from({ length: 8 }, (_, index) =>
        signal({
          id: `extra-${index}`,
          title: `Extra ${index}`,
          lane: "work",
          priority: index === 0 ? "high" : "medium",
          ageDays: index + 2,
        }),
      ),
    ];

    const queue = commandQueue(items);

    expect(queue).toHaveLength(7);
    expect(queue[0].id).toBe("high");
    expect(queue.some((item) => item.id === "eve")).toBe(false);
    expect(queue.every((item) => typeof item.score === "number")).toBe(true);
  });
});
