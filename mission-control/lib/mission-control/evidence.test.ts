import { describe, expect, test } from "bun:test";
import { evidenceGroups, evidenceSummary } from "./evidence";
import type { Signal } from "./types";

function signal(overrides: Partial<Signal>): Signal {
  return {
    id: overrides.id ?? "proof",
    source: "proof",
    title: overrides.title ?? "Proof entry",
    owner: "eve",
    status: overrides.status ?? "done",
    lane: "evidence",
    priority: overrides.priority ?? "low",
    ageDays: overrides.ageDays ?? 0,
    evidence: overrides.evidence ?? [{ kind: "file", label: "proof", quality: "verified" }],
    updatedAt: overrides.updatedAt ?? 100,
    raw: overrides.raw ?? {},
    ...overrides,
  };
}

describe("evidenceSummary", () => {
  test("counts proof coverage, latest proof, gaps, and failures", () => {
    const summary = evidenceSummary([
      signal({ id: "latest", title: "Mission Control Machine Lane", updatedAt: 300 }),
      signal({ id: "gap", title: "Unverified research note", evidence: [{ kind: "unknown", label: "No proof ref", quality: "gap" }], updatedAt: 200 }),
      signal({ id: "failure", title: "Failed proof", status: "failed", priority: "high", updatedAt: 100 }),
      signal({ id: "work", lane: "work", source: "task", title: "Work task" }),
    ]);

    expect(summary.total).toBe(3);
    expect(summary.verified).toBe(2);
    expect(summary.gaps).toBe(1);
    expect(summary.failures).toBe(1);
    expect(summary.latestTitle).toBe("Mission Control Machine Lane");
  });
});

describe("evidenceGroups", () => {
  test("groups buyer proof, system proof, content proof, and proof gaps separately", () => {
    const groups = evidenceGroups([
      signal({ id: "client", title: "Altmark Rent Delinquency Testing Pack", context: "client delivery" }),
      signal({ id: "system", title: "Mission Control Machine Lane", context: "system cockpit" }),
      signal({ id: "content", title: "AppFolio AI Ops Teardown Draft", context: "LinkedIn content asset" }),
      signal({ id: "gap", title: "Proof entry missing files", evidence: [{ kind: "unknown", label: "No proof ref", quality: "gap" }] }),
    ]);

    expect(groups.buyer.map((item) => item.id).join(",")).toBe("client");
    expect(groups.system.map((item) => item.id).join(",")).toBe("system");
    expect(groups.content.map((item) => item.id).join(",")).toBe("content");
    expect(groups.gaps.map((item) => item.id).join(",")).toBe("gap");
  });
});
