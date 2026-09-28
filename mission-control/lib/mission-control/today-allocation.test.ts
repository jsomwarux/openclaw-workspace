import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { allocateToday, commandQueue } from "./score";
import { buildScoreContext } from "./score-context";
import { commandBrief } from "./command-brief";
import { primaryActionVerb, todayRankingExplanation } from "./reason-codes";
import type { FocusRow, Signal } from "./types";
import type { GrowthLane } from "./lane-packet";

const NOW = Date.UTC(2026, 8, 28, 13, 0, 0);
const DAY = 24 * 60 * 60 * 1000;

function signal(overrides: Partial<Signal> = {}): Signal {
  return {
    id: "task",
    source: "task",
    title: "Task",
    owner: "jt",
    status: "todo",
    lane: "work",
    priority: "medium",
    ageDays: 0,
    evidence: [],
    updatedAt: NOW - DAY,
    raw: {},
    ...overrides,
  };
}

function packet(id: string, growthLane: GrowthLane, overrides: Partial<Signal> = {}): Signal {
  return signal({
    id,
    title: `Packet ${id}`,
    lane: growthLane === "jobs" || growthLane === "outreach" ? "revenue" : "ship",
    packetSchema: "lane-packet-v1",
    growthLane,
    estMinutes: 15,
    expiresAt: NOW + 3 * DAY,
    approvalState: "pending",
    doneEvidenceType: "post-url",
    ...overrides,
  });
}

const baseFocus: FocusRow = { weekOf: "2026-09-28", projects: [], gate: 0, mandate: "none" };
const ctxWith = (focus: FocusRow = baseFocus) => buildScoreContext({ focus, collected: 0, now: NOW });

// A mixed legacy queue: cash, deadline, proof, a waiting nudge, an Eve task, a snoozed task.
const legacySignals: Signal[] = [
  signal({ id: "cash", title: "Collect deposit", lane: "revenue", dollars: 5000, updatedAt: NOW - 3 * DAY }),
  signal({ id: "deadline", title: "File certification", dueDate: NOW + DAY, dueDateSource: "external" }),
  signal({ id: "proof", title: "Capture proof", proofRequired: true, updatedAt: NOW - 2 * DAY }),
  signal({ id: "plain-new", title: "Plain new", updatedAt: NOW - 1000 }),
  signal({ id: "plain-old", title: "Plain old", updatedAt: NOW - 5 * DAY }),
  signal({ id: "nudge", title: "Waiting", waitingOn: { who: "Client", what: "access", since: NOW - 10 * DAY, nudgeAfterDays: 3 } }),
  signal({ id: "eve", title: "Eve work", owner: "eve", status: "in-progress" }),
  signal({ id: "snoozed", title: "Snoozed", snoozedUntil: NOW + DAY, proofRequired: true }),
];

describe("one function owns Today ordering", () => {
  test("commandQueue is exactly allocateToday's queue", () => {
    const ctx = ctxWith({ ...baseFocus, laneCapacity: [{ lane: "linkedin", minutes: 15 }] });
    const signals = [...legacySignals, packet("li-1", "linkedin"), packet("li-2", "linkedin")];
    expect(commandQueue(signals, ctx)).toEqual(allocateToday(signals, ctx).queue);
  });

  test("with no lane capacity configured, Today's order is unchanged from the legacy scorer", () => {
    const ids = allocateToday(legacySignals, ctxWith()).queue.map((item) => item.id);
    expect(ids).toEqual(["cash", "deadline", "proof", "plain-new", "nudge", "plain-old"]);
  });

  test("Priority Audit outputs (priority, sortOrder, rankScore) never change Today order", () => {
    const baseline = allocateToday(legacySignals, ctxWith()).queue.map((item) => item.id);
    const audited = legacySignals.map((item, index) => ({
      ...item,
      priority: index % 2 === 0 ? ("low" as const) : ("high" as const),
      raw: { sortOrder: 100 - index, rankScore: index * 7 },
    }));
    expect(allocateToday(audited, ctxWith()).queue.map((item) => item.id)).toEqual(baseline);
  });

  test("the command brief's top action is the queue head, never a re-ranked pick", () => {
    const queue = [signal({ id: "head", score: 10 }), signal({ id: "second", score: 90 })];
    const brief = commandBrief({ queue, signals: queue, revenue: { active: 0, high: 0, done: 0, costToday: null, costAlerts: [] } });
    expect(brief.topAction?.id).toBe("head");
  });

  test("no other Today module sorts the queue", () => {
    const read = (name: string) => readFileSync(fileURLToPath(new URL(`./${name}`, import.meta.url)), "utf8");
    expect(read("score.ts").match(/\.sort\(/g)?.length).toBe(1);
    expect(read("command-brief.ts").includes("score ?? 0")).toBe(false);
    expect(read("hooks.ts").includes("commandQueue(")).toBe(false);
    expect(read("hooks.ts")).toContain("allocateToday(");
  });

  test("the NOW card never offers the generic Approve shortcut for a lane packet", () => {
    const shared = { owner: "both" as const, priority: "high" as const, status: "awaiting-approval" as const };
    expect(primaryActionVerb(signal(shared))).toBe("Approve");
    expect(primaryActionVerb(packet("li-1", "linkedin", shared))).toBe("Inspect");
  });

  test("the drawer explains a Today rank from the scorer, not from priority", () => {
    const text = todayRankingExplanation(signal({ priority: "high", score: 40, reasonCodes: ["cash:5000", "proof"] }));
    expect(text).toContain("$5,000");
    expect(text).toContain("Proof asset");
    expect(text.toLowerCase()).toContain("priority does not change today order");
    expect(todayRankingExplanation(signal({ reasonCodes: [] }))).toContain("most recent update");
  });
});

describe("per-lane minute capacity from the focus row", () => {
  const capped = (laneCapacity: FocusRow["laneCapacity"]) => ctxWith({ ...baseFocus, laneCapacity });

  test("keeps packets within a lane's minutes and reports the rest as explicit overflow", () => {
    const signals = [
      packet("li-1", "linkedin", { updatedAt: NOW - 1000 }),
      packet("li-2", "linkedin", { updatedAt: NOW - 2000 }),
      packet("li-3", "linkedin", { updatedAt: NOW - 3000 }),
    ];
    const result = allocateToday(signals, capped([{ lane: "linkedin", minutes: 30 }]));
    expect(result.queue.map((item) => item.id)).toEqual(["li-1", "li-2"]);
    expect(result.overflow).toEqual([{ lane: "linkedin", count: 1, minutes: 15 }]);
  });

  test("capacity filters without reordering, and later items fill the freed slots", () => {
    const signals = [
      signal({ id: "cash", lane: "revenue", dollars: 5000 }),
      packet("li-1", "linkedin", { proofRequired: true, updatedAt: NOW - 1000 }),
      packet("li-2", "linkedin", { proofRequired: true, updatedAt: NOW - 2000 }),
      signal({ id: "plain", updatedAt: NOW - 3000 }),
    ];
    const result = allocateToday(signals, capped([{ lane: "linkedin", minutes: 15 }]));
    expect(result.queue.map((item) => item.id)).toEqual(["cash", "li-1", "plain"]);
    expect(result.overflow).toEqual([{ lane: "linkedin", count: 1, minutes: 15 }]);
  });

  test("a lane with 0 minutes stays silent; unlisted lanes and legacy tasks are uncapped", () => {
    const signals = [packet("x-1", "x"), packet("jobs-1", "jobs"), packet("jobs-2", "jobs"), signal({ id: "legacy" })];
    const result = allocateToday(signals, capped([{ lane: "x", minutes: 0 }]));
    expect(result.queue.map((item) => item.id).sort()).toEqual(["jobs-1", "jobs-2", "legacy"]);
    expect(result.overflow).toEqual([{ lane: "x", count: 1, minutes: 15 }]);
  });

  test("a packet larger than its lane's capacity overflows instead of silently disappearing", () => {
    const result = allocateToday([packet("jobs-big", "jobs", { estMinutes: 45 })], capped([{ lane: "jobs", minutes: 30 }]));
    expect(result.queue).toHaveLength(0);
    expect(result.overflow).toEqual([{ lane: "jobs", count: 1, minutes: 45 }]);
  });

  test("a genuine external deadline inside 24 hours bypasses capacity but still consumes it", () => {
    const signals = [
      packet("jobs-due", "jobs", { dueDate: NOW + 6 * 60 * 60 * 1000, dueDateSource: "external", estMinutes: 30 }),
      packet("jobs-later", "jobs", { estMinutes: 15, updatedAt: NOW }),
    ];
    const result = allocateToday(signals, capped([{ lane: "jobs", minutes: 20 }]));
    expect(result.queue.map((item) => item.id)).toEqual(["jobs-due"]);
    expect(result.overflow).toEqual([{ lane: "jobs", count: 1, minutes: 15 }]);
    const selfDeadline = allocateToday([packet("self-due", "jobs", { dueDate: NOW + 60_000, dueDateSource: "self", estMinutes: 30 })], capped([{ lane: "jobs", minutes: 20 }]));
    expect(selfDeadline.queue).toHaveLength(0);
  });

  test("overflow lists lanes in canonical lane order", () => {
    const signals = [packet("jobs-1", "jobs"), packet("li-1", "linkedin"), packet("x-1", "x")];
    const result = allocateToday(signals, capped([{ lane: "jobs", minutes: 0 }, { lane: "linkedin", minutes: 0 }, { lane: "x", minutes: 0 }]));
    expect(result.overflow.map((entry) => entry.lane)).toEqual(["linkedin", "x", "jobs"]);
  });
});

describe("expiry and snooze are automatic in Today", () => {
  test("an open packet past expiry never reaches Today and is counted as expired", () => {
    const signals = [packet("fresh", "jobs"), packet("stale", "jobs", { expiresAt: NOW })];
    const result = allocateToday(signals, ctxWith());
    expect(result.queue.map((item) => item.id)).toEqual(["fresh"]);
    expect(result.expired).toBe(1);
  });

  test("snoozed and closed packets stay out; a legacy task with no envelope is never treated as expired", () => {
    const signals = [
      packet("snoozed", "jobs", { snoozedUntil: NOW + DAY }),
      packet("closed", "jobs", { status: "archived" }),
      signal({ id: "legacy", raw: { expiresAt: NOW - DAY } }),
    ];
    const result = allocateToday(signals, ctxWith());
    expect(result.queue.map((item) => item.id)).toEqual(["legacy"]);
    expect(result.expired).toBe(0);
  });
});
