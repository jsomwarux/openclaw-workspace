import { describe, expect, test } from "bun:test";
import { machineGroups, machineSummary } from "./machine";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: overrides.id ?? "signal",
    source: overrides.source ?? "cron",
    title: overrides.title ?? "Machine signal",
    owner: overrides.owner ?? "eve",
    status: overrides.status ?? "done",
    lane: "machine",
    priority: overrides.priority ?? "low",
    ageDays: overrides.ageDays ?? 0,
    evidence: overrides.evidence ?? [],
    updatedAt: overrides.updatedAt ?? 100,
    raw: overrides.raw ?? {},
    ...overrides,
  };
}

describe("machineSummary", () => {
  test("counts cron health, active agents, cost alerts, and risk signals", () => {
    const summary = machineSummary([
      signal({ id: "failed-cron", source: "cron", status: "failed", priority: "high" }),
      signal({ id: "healthy-cron", source: "cron", status: "done" }),
      signal({ id: "active-agent", source: "agent", status: "in-progress" }),
      signal({ id: "cost-alert", source: "task", title: "Cost alert: monthly pace too high", priority: "high" }),
      signal({ id: "ship", lane: "ship", source: "task" }),
    ]);

    expect(summary.cronsTotal).toBe(2);
    expect(summary.cronsFailed).toBe(1);
    expect(summary.agentsActive).toBe(1);
    expect(summary.costAlerts).toBe(1);
    expect(summary.risks).toBe(2);
  });
});

describe("machineGroups", () => {
  test("groups crons, agents, cost pressure, and recent machine work separately", () => {
    const groups = machineGroups([
      signal({ id: "cron", source: "cron", title: "Viral Post Swipe File X Research", status: "failed" }),
      signal({ id: "agent", source: "agent", title: "Research Agent", status: "in-progress" }),
      signal({ id: "cost", source: "task", title: "Cost alert: review monthly OpenRouter pace" }),
      signal({ id: "task", source: "task", title: "OpenClaw gateway cooldown recovery" }),
      signal({ id: "proof", lane: "evidence", source: "proof", title: "Proof entry" }),
    ]);

    expect(groups.crons.map((item) => item.id).join(",")).toBe("cron");
    expect(groups.agents.map((item) => item.id).join(",")).toBe("agent");
    expect(groups.costs.map((item) => item.id).join(",")).toBe("cost");
    expect(groups.work.map((item) => item.id).join(",")).toBe("task");
  });
});
