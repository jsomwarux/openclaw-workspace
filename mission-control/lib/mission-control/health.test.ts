import { describe, expect, test } from "bun:test";
import { healthGroups, healthSummary } from "./health";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: overrides.id ?? "health",
    source: overrides.source ?? "task",
    title: overrides.title ?? "Health signal",
    owner: overrides.owner ?? "eve",
    status: overrides.status ?? "in-progress",
    lane: overrides.lane ?? "health",
    priority: overrides.priority ?? "medium",
    ageDays: overrides.ageDays ?? 0,
    evidence: overrides.evidence ?? [],
    updatedAt: overrides.updatedAt ?? 100,
    raw: overrides.raw ?? {},
    ...overrides,
  };
}

describe("healthSummary", () => {
  test("counts failures, stale risks, cost alerts, and recovery work", () => {
    const summary = healthSummary(
      [
        signal({ id: "failed", status: "failed", priority: "high", title: "Gateway health failure" }),
        signal({ id: "stale", status: "stale", ageDays: 18, title: "Monitor stale task" }),
        signal({ id: "recovery", status: "in-progress", title: "Recover cron cleanup", priority: "medium" }),
        signal({ id: "machine", lane: "machine", status: "failed", title: "Cron failure" }),
        signal({ id: "ship", lane: "ship", title: "Ship task" }),
      ],
      { alerts: [{ level: "warning", message: "Daily cost pace high" }] },
    );

    expect(summary.failures).toBe(2);
    expect(summary.stale).toBe(1);
    expect(summary.costAlerts).toBe(1);
    expect(summary.recoveryWork).toBe(1);
    expect(summary.posture).toBe("review");
  });

  test("reports clear posture when no health or cost risk exists", () => {
    const summary = healthSummary([signal({ id: "done", status: "done", priority: "low" })], { alerts: [] });

    expect(summary.failures).toBe(0);
    expect(summary.stale).toBe(0);
    expect(summary.costAlerts).toBe(0);
    expect(summary.posture).toBe("clear");
  });
});

describe("healthGroups", () => {
  test("groups ops failures, cost pressure, stale risk, and recovery work separately", () => {
    const groups = healthGroups([
      signal({ id: "failure", status: "failed", title: "Preflight compaction failure" }),
      signal({ id: "cost", title: "Cost alert: OpenRouter monthly pace too high" }),
      signal({ id: "stale", status: "stale", ageDays: 20, title: "Domain expiration monitor stale" }),
      signal({ id: "recovery", status: "in-progress", title: "Recover gateway cooldown state" }),
      signal({ id: "machine", lane: "machine", status: "failed", title: "Cron failed latest run" }),
    ]);

    expect(groups.failures.map((item) => item.id).join(",")).toBe("failure,machine");
    expect(groups.costs.map((item) => item.id).join(",")).toBe("cost");
    expect(groups.stale.map((item) => item.id).join(",")).toBe("stale");
    expect(groups.recovery.map((item) => item.id).join(",")).toBe("recovery");
  });
});
