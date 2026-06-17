import { describe, expect, test } from "bun:test";
import { shipGroups, shipSummary } from "./ship";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: overrides.id ?? "signal",
    source: "task",
    title: overrides.title ?? "Ship task",
    owner: "jt",
    status: overrides.status ?? "awaiting-decision",
    lane: "ship",
    priority: overrides.priority ?? "medium",
    ageDays: 0,
    evidence: overrides.evidence ?? [],
    updatedAt: overrides.updatedAt ?? 100,
    raw: {},
    ...overrides,
  };
}

describe("shipSummary", () => {
  test("counts active app/content shipping work and proof coverage", () => {
    const summary = shipSummary([
      signal({ id: "vista", title: "Vista: submit first durable directory listing", priority: "high" }),
      signal({ id: "proof", title: "Vista share card shipped", status: "done", evidence: [{ kind: "file", label: "proof", quality: "verified" }] }),
      signal({ id: "machine", title: "OpenClaw cron cleanup", lane: "machine" }),
    ]);

    expect(summary.active).toBe(1);
    expect(summary.high).toBe(1);
    expect(summary.proofed).toBe(1);
  });
});

describe("shipGroups", () => {
  test("groups app distribution, content, and release work separately", () => {
    const groups = shipGroups([
      signal({ id: "nash", title: "Nash Satoshi: submit first methodology-backed directory listing" }),
      signal({ id: "content", title: "Draft AppFolio AI Ops teardown", project: "Content" }),
      signal({ id: "release", title: "Action Arena App Store submission by July 15" }),
    ]);

    expect(groups.apps.map((item) => item.id).join(",")).toBe("nash");
    expect(groups.content.map((item) => item.id).join(",")).toBe("content");
    expect(groups.releases.map((item) => item.id).join(",")).toBe("release");
  });
});
