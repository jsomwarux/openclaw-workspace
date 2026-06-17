import { describe, expect, test } from "bun:test";
import { priorityBadgeClassName, priorityRank, sortWorkSignals } from "./work-priority";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: overrides.id ?? "task",
    source: "task",
    title: overrides.title ?? "Task",
    owner: "jt",
    status: overrides.status ?? "awaiting-decision",
    lane: "work",
    priority: overrides.priority ?? "medium",
    ageDays: 0,
    evidence: [],
    updatedAt: overrides.updatedAt ?? 100,
    raw: {},
    ...overrides,
  };
}

describe("work priority ordering", () => {
  test("orders high priority tasks above newer medium tasks", () => {
    const sorted = sortWorkSignals([
      signal({ id: "new-medium", priority: "medium", updatedAt: 300 }),
      signal({ id: "old-high", priority: "high", updatedAt: 100 }),
      signal({ id: "low", priority: "low", updatedAt: 400 }),
    ]);

    expect(sorted.map((item) => item.id).join(",")).toBe("old-high,new-medium,low");
  });

  test("demotes done work below active tasks of the same priority", () => {
    const sorted = sortWorkSignals([
      signal({ id: "done", status: "done", priority: "high", updatedAt: 500 }),
      signal({ id: "active", status: "awaiting-decision", priority: "high", updatedAt: 100 }),
    ]);

    expect(sorted.map((item) => item.id).join(",")).toBe("active,done");
  });

  test("assigns distinct visual classes per priority", () => {
    expect(priorityRank("high")).toBe(3);
    expect(priorityBadgeClassName("high")).toContain("rose");
    expect(priorityBadgeClassName("medium")).toContain("amber");
    expect(priorityBadgeClassName("low")).toContain("zinc");
  });
});
