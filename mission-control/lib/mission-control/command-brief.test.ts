import { describe, expect, test } from "bun:test";
import { commandBrief } from "./command-brief";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: overrides.id ?? "signal",
    source: overrides.source ?? "task",
    title: overrides.title ?? "Task",
    owner: overrides.owner ?? "jt",
    status: overrides.status ?? "awaiting-decision",
    lane: overrides.lane ?? "work",
    priority: overrides.priority ?? "medium",
    ageDays: overrides.ageDays ?? 0,
    evidence: overrides.evidence ?? [],
    updatedAt: overrides.updatedAt ?? 100,
    raw: {},
    ...overrides,
  };
}

describe("commandBrief", () => {
  test("selects the highest ranked action and counts urgent JT work", () => {
    const brief = commandBrief({
      queue: [
        signal({ id: "medium", title: "Medium task", priority: "medium", score: 50 }),
        signal({ id: "high", title: "High task", priority: "high", score: 80 }),
      ],
      signals: [
        signal({ id: "high-1", priority: "high", owner: "jt", status: "awaiting-decision" }),
        signal({ id: "high-2", priority: "high", owner: "jt", status: "blocked" }),
        signal({ id: "eve-high", priority: "high", owner: "eve", status: "in-progress" }),
      ],
      revenue: { active: 4, high: 2, done: 1, costToday: null, costAlerts: [] },
    });

    expect(brief.topAction?.title).toBe("High task");
    expect(brief.urgentJtCount).toBe(2);
    expect(brief.headline).toContain("2 high-priority JT items");
  });

  test("surfaces latest proof and risk count", () => {
    const brief = commandBrief({
      queue: [],
      signals: [
        signal({ id: "proof-old", source: "proof", title: "Old proof", lane: "evidence", status: "done", updatedAt: 100 }),
        signal({ id: "proof-new", source: "proof", title: "New proof", lane: "evidence", status: "done", updatedAt: 300 }),
        signal({ id: "risk", status: "failed", lane: "machine", updatedAt: 200 }),
      ],
      revenue: { active: 0, high: 0, done: 0, costToday: null, costAlerts: [] },
    });

    expect(brief.latestProof?.title).toBe("New proof");
    expect(brief.riskCount).toBe(1);
    expect(brief.headline).toContain("1 risk signal");
  });

  test("reports clear state when there is no action pressure", () => {
    const brief = commandBrief({
      queue: [],
      signals: [signal({ source: "proof", lane: "evidence", status: "done", title: "Proof" })],
      revenue: { active: 0, high: 0, done: 0, costToday: 0, costAlerts: [] },
    });

    expect(brief.headline).toBe("Command is clear.");
    expect(brief.topAction).toBe(null);
  });
});
