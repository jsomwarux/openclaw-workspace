import { describe, expect, test } from "bun:test";
import { deferTaskPatch, priorityOptions, rankingExplanation } from "./work-actions";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: overrides.id ?? "task",
    source: "task",
    title: overrides.title ?? "Task",
    owner: overrides.owner ?? "jt",
    status: overrides.status ?? "awaiting-decision",
    lane: "work",
    priority: overrides.priority ?? "high",
    project: overrides.project,
    ageDays: overrides.ageDays ?? 3,
    evidence: overrides.evidence ?? [],
    updatedAt: overrides.updatedAt ?? 100,
    raw: {},
    ...overrides,
  };
}

describe("work drawer actions", () => {
  test("exposes explicit priority options for the task drawer", () => {
    expect(priorityOptions.map((option) => option.value).join(",")).toBe("high,medium,low");
    expect(priorityOptions.map((option) => option.label).join(",")).toBe("High,Medium,Low");
  });

  test("defers a task without marking it done", () => {
    expect(deferTaskPatch()).toMatchObject({ priority: "low", status: "todo" });
  });

  test("explains why a task is ranked where it is", () => {
    const explanation = rankingExplanation(signal({ priority: "high", status: "awaiting-decision", ageDays: 15, project: "App Marketing" }));

    expect(explanation).toContain("High priority");
    expect(explanation).toContain("awaiting-decision");
    expect(explanation).toContain("15 days");
    expect(explanation).toContain("App Marketing");
  });
});
