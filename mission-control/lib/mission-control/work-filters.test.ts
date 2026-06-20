import { describe, expect, test } from "bun:test";
import { filterWorkSignals, type WorkFilter } from "./work-filters";
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

describe("work lane filters", () => {
  test("keeps completed tasks out of active board filters", () => {
    const signals = [
      signal({ id: "active-high", priority: "high", status: "awaiting-decision" }),
      signal({ id: "done-high", priority: "high", status: "done", updatedAt: 300 }),
      signal({ id: "done-medium", priority: "medium", status: "done", updatedAt: 200 }),
    ];

    expect(filterWorkSignals(signals, "all").map((item) => item.id)).toEqual(["active-high"]);
    expect(filterWorkSignals(signals, "high").map((item) => item.id)).toEqual(["active-high"]);
  });

  test("shows recently completed tasks in their own done view, newest first", () => {
    const signals = [
      signal({ id: "active-high", priority: "high", status: "awaiting-decision", updatedAt: 100 }),
      signal({ id: "done-old", priority: "low", status: "done", updatedAt: 200 }),
      signal({ id: "done-new", priority: "medium", status: "done", updatedAt: 300 }),
    ];

    expect(filterWorkSignals(signals, "done").map((item) => item.id)).toEqual(["done-new", "done-old"]);
  });

  test("preserves owner and blocked filters for active tasks only", () => {
    const signals = [
      signal({ id: "jt-active", owner: "jt", status: "awaiting-decision" }),
      signal({ id: "jt-done", owner: "jt", status: "done" }),
      signal({ id: "eve-blocked", owner: "eve", status: "blocked" }),
    ];

    const filters: WorkFilter[] = ["jt", "eve", "blocked"];
    expect(filters.map((filter) => filterWorkSignals(signals, filter).map((item) => item.id))).toEqual([
      ["jt-active"],
      ["eve-blocked"],
      ["eve-blocked"],
    ]);
  });
});
