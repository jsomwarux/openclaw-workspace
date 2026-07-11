import { describe, expect, test } from "bun:test";
import { commandQueue, scoreBand, scoreSignal, scoreTask } from "./score";
import type { ScoreContext, Signal } from "./types";

const now = Date.UTC(2026, 6, 11); // 2026-07-11
const DAY = 24 * 60 * 60 * 1000;

function signal(overrides: Partial<Signal> = {}): Signal {
  return {
    id: "task-1",
    source: "task",
    title: "Task",
    owner: "jt",
    status: "in-progress",
    lane: "work",
    priority: "medium",
    ageDays: 1,
    evidence: [],
    updatedAt: now,
    raw: {},
    ...overrides,
  };
}

// The three canonical tasks the model has to get right.
const dhcrDeposit = signal({
  id: "dhcr",
  title: "Collect DHCR deposit",
  lane: "revenue",
  project: "Consulting",
  dollars: 3500,
  stageProbability: 1,
  dueDate: now + 2 * DAY,
  dueDateSource: "external",
});

const waitingOnYair = signal({
  id: "yair",
  title: "Yair signs the scope doc",
  lane: "revenue",
  project: "Consulting",
  priority: "high",
  dollars: 2000,
  stageProbability: 0.5,
  waitingOn: { who: "Yair", what: "signed scope doc", since: now - 2 * DAY, nudgeAfterDays: 3 },
});

const shipApp = signal({
  id: "ship-app",
  title: "Ship Vista onboarding polish",
  lane: "ship",
  project: "App Marketing",
  priority: "high",
  proofRequired: true,
  riskContainment: true,
});

const cashMandate: ScoreContext = {
  now,
  mandate: "consulting-cash",
  collected: 0,
  focus: { weekOf: "2026-07-06", projects: ["Consulting"], gate: 5000 },
};

describe("scoreTask factors", () => {
  test("a 3500-dollar external-deadline task outranks everything else", () => {
    const queue = commandQueue([shipApp, waitingOnYair, dhcrDeposit, signal({ id: "filler" })], cashMandate);
    expect(queue[0].id).toBe("dhcr");
    expect(queue[0].score).toBe(52); // 40 cash + 12 deadline
    expect(queue[0].reasonCodes).toEqual(["cash:3500", "deadline:2026-07-13"]);
  });

  test("cash impact bands on expected value, not headline dollars", () => {
    const at3000 = scoreTask(signal({ lane: "revenue", dollars: 6000, stageProbability: 0.5 }), { now });
    expect(at3000.factors.cashImpact).toBe(40);

    const at1000 = scoreTask(signal({ lane: "revenue", dollars: 4000, stageProbability: 0.25 }), { now });
    expect(at1000.factors.cashImpact).toBe(30);

    const indirect = scoreTask(signal({ lane: "ship", dollars: 9000 }), { now });
    expect(indirect.factors.cashImpact).toBe(15);

    const none = scoreTask(signal({ lane: "revenue", dollars: 0 }), { now });
    expect(none.factors.cashImpact).toBe(0);
    expect(none.reasonCodes).not.toContain("cash:0");
  });

  test("deadline pressure only counts external dates and halves self-set ones", () => {
    const external = (dueDate: number) => scoreTask(signal({ dueDate, dueDateSource: "external" }), { now });
    expect(external(now).factors.deadlinePressure).toBe(15);
    expect(external(now + 3 * DAY).factors.deadlinePressure).toBe(12);
    expect(external(now + 6 * DAY).factors.deadlinePressure).toBe(8);
    expect(external(now + 30 * DAY).factors.deadlinePressure).toBe(0);

    const self = scoreTask(signal({ dueDate: now, dueDateSource: "self" }), { now });
    expect(self.factors.deadlinePressure).toBe(8);
  });

  test("unblock value comes from the explicit blocks field, not the title text", () => {
    expect(scoreTask(signal({ title: "This blocks everything" }), { now }).factors.unblockValue).toBe(0);
    expect(scoreTask(signal({ blocks: 1 }), { now }).factors.unblockValue).toBe(8);
    expect(scoreTask(signal({ blocks: 2 }), { now }).factors.unblockValue).toBe(15);
    expect(scoreTask(signal({ blocksAgent: true }), { now }).factors.unblockValue).toBe(15);
  });

  test("proof, risk, and stability each add their fixed weight", () => {
    const result = scoreTask(signal({ lane: "health", proofRequired: true, riskContainment: true }), { now });
    expect(result.factors).toMatchObject({ proofLeverage: 10, riskContainment: 10, stability: 10 });
    expect(result.score).toBe(30);
    expect(result.reasonCodes).toEqual(["proof", "risk", "stability"]);
  });
});

describe("modifiers", () => {
  test("focus penalty applies off-focus and is overridden by cash impact 30 or more", () => {
    const offFocus = scoreTask(signal({ project: "App Marketing", proofRequired: true }), cashMandate);
    expect(offFocus.score).toBe(0); // 10 proof - 15 focus penalty, clamped
    expect(offFocus.reasonCodes).toContain("focus-penalty");

    const offFocusButCash = scoreTask(
      signal({ project: "App Marketing", lane: "revenue", dollars: 1500 }),
      cashMandate,
    );
    expect(offFocusButCash.reasonCodes).not.toContain("focus-penalty");
    expect(offFocusButCash.score).toBe(30);
  });

  test("effort demotion hits long tasks with weak cash impact only", () => {
    const long = scoreTask(signal({ project: "Consulting", effortMinutes: 90, proofRequired: true }), cashMandate);
    expect(long.reasonCodes).toContain("effort-demotion");
    expect(long.score).toBe(0);

    const longButCash = scoreTask(
      signal({ project: "Consulting", lane: "revenue", dollars: 1200, effortMinutes: 90 }),
      cashMandate,
    );
    expect(longButCash.reasonCodes).not.toContain("effort-demotion");
  });

  test("a ship-lane zero-dollar task never exceeds 25 under the consulting-cash mandate", () => {
    const capped = scoreTask(shipApp, cashMandate);
    expect(capped.score).toBeLessThanOrEqual(25);
    expect(capped.reasonCodes).toContain("ship-capped");

    // A ship task that would otherwise clear 25 is still held to the cap.
    const heavyShip = signal({
      id: "heavy-ship",
      lane: "ship",
      project: "Consulting", // in focus, so no focus penalty muddies the math
      blocks: 2,
      proofRequired: true,
      riskContainment: true,
    });
    expect(scoreTask(heavyShip, cashMandate).score).toBe(25); // 35 uncapped
    expect(scoreTask(heavyShip, cashMandate).reasonCodes).toContain("ship-capped");

    // Gate already met: the cap lifts and the real score comes through.
    const gateMet = scoreTask(heavyShip, { ...cashMandate, collected: 5000 });
    expect(gateMet.score).toBe(35);
    expect(gateMet.reasonCodes).not.toContain("ship-capped");

    // A ship task carrying real dollars is not capped.
    const shipWithCash = scoreTask({ ...heavyShip, dollars: 4000, cashDirect: true }, cashMandate);
    expect(shipWithCash.reasonCodes).not.toContain("ship-capped");
    expect(shipWithCash.score).toBeGreaterThan(25);
  });
});

describe("explainability", () => {
  test("every scored task at 50 or more carries nonempty reason codes", () => {
    const candidates = [dhcrDeposit, shipApp, waitingOnYair, signal({ lane: "health", riskContainment: true })];
    for (const candidate of candidates) {
      const result = scoreTask(candidate, cashMandate);
      if (result.score >= 50) expect(result.reasonCodes.length).toBeGreaterThan(0);
    }
  });

  test("a task with no factors firing scores zero and carries no reason codes", () => {
    // The "unexplained" guard in scoreTask is a backstop, not a live path: every factor
    // that contributes points also pushes a reason code, so a 50-plus score with empty
    // reasonCodes is unreachable through this API. What is reachable is the opposite
    // degenerate case — nothing fires, so there is nothing to explain.
    const result = scoreTask(signal({ lane: "work" }), { now });
    expect(result.score).toBe(0);
    expect(result.reasonCodes).toEqual([]);
  });

  test("scoreSignal attaches score, band, and reason codes to the signal", () => {
    const scored = scoreSignal(dhcrDeposit, cashMandate);
    expect(scored.score).toBe(52);
    expect(scored.band).toBe("medium");
    expect(scored.reasonCodes).toContain("cash:3500");
  });
});

describe("scoreBand", () => {
  test("maps scores to high, medium, and low bands", () => {
    expect(scoreBand(70)).toBe("high");
    expect(scoreBand(40)).toBe("medium");
    expect(scoreBand(39)).toBe("low");
  });
});

describe("commandQueue exclusions", () => {
  test("a task waiting on someone else is excluded until its nudge comes due", () => {
    const queue = commandQueue([waitingOnYair], cashMandate);
    expect(queue).toHaveLength(0);
  });

  test("the same task surfaces as a nudge once nudgeAfterDays has passed", () => {
    const overdue = {
      ...waitingOnYair,
      waitingOn: { ...waitingOnYair.waitingOn!, since: now - 5 * DAY },
    };
    const queue = commandQueue([overdue], cashMandate);
    expect(queue).toHaveLength(1);
    expect(queue[0].title).toBe("Nudge Yair: signed scope doc");
    expect(queue[0].reasonCodes).toContain("nudge-due");
  });

  test("done, archived, and snoozed work never enters the queue", () => {
    const items = [
      signal({ id: "done", status: "done" }),
      signal({ id: "archived", status: "archived" }),
      signal({ id: "snoozed", status: "snoozed" }),
      signal({ id: "snoozed-until", snoozedUntil: now + DAY }),
      signal({ id: "snooze-expired", snoozedUntil: now - DAY, proofRequired: true }),
    ];
    const queue = commandQueue(items, { now });
    expect(queue.map((item) => item.id)).toEqual(["snooze-expired"]);
  });

  test("eve's in-progress and stale work is excluded but her failures escalate to JT", () => {
    const items = [
      signal({ id: "eve-working", owner: "eve", status: "in-progress" }),
      signal({ id: "eve-failed", owner: "eve", status: "failed", riskContainment: true }),
      // Stale is idle, not actionable: it belongs to the EVE HAS IT strip, not the queue.
      signal({ id: "eve-stale", owner: "eve", status: "stale" }),
    ];
    const queue = commandQueue(items, { now });
    expect(queue.map((item) => item.id)).toEqual(["eve-failed"]);
  });

  test("agent and proof signals never enter the queue, whatever their status", () => {
    const items = [
      signal({ id: "agent-stale", source: "agent", owner: "eve", status: "stale", lane: "machine" }),
      signal({ id: "agent-failed", source: "agent", owner: "eve", status: "failed", lane: "machine" }),
      signal({ id: "agent-jt", source: "agent", owner: "jt", status: "failed", lane: "machine" }),
      signal({ id: "proof-gap", source: "proof", owner: "jt", status: "stale", lane: "evidence" }),
      signal({ id: "jt-task", proofRequired: true }),
    ];
    const queue = commandQueue(items, { now });
    expect(queue.map((item) => item.id)).toEqual(["jt-task"]);
  });

  test("a failed cron escalates but a running one does not", () => {
    const items = [
      signal({ id: "cron-failed", source: "cron", owner: "eve", status: "failed", lane: "machine" }),
      signal({ id: "cron-running", source: "cron", owner: "eve", status: "in-progress", lane: "machine" }),
    ];
    const queue = commandQueue(items, { now });
    expect(queue.map((item) => item.id)).toEqual(["cron-failed"]);
  });

  test("a jt cash task outranks every machine item that survives the exclusions", () => {
    const items = [
      signal({ id: "agent-a", source: "agent", owner: "eve", status: "stale", lane: "machine" }),
      signal({ id: "agent-b", source: "agent", owner: "eve", status: "stale", lane: "machine" }),
      signal({ id: "agent-c", source: "agent", owner: "eve", status: "stale", lane: "machine" }),
      signal({
        id: "cron-failed",
        source: "cron",
        owner: "eve",
        status: "failed",
        lane: "machine",
        riskContainment: true,
      }),
      signal({ id: "eve-stale-task", owner: "eve", status: "stale" }),
      signal({ id: "eve-failed-task", owner: "eve", status: "failed" }),
      signal({
        id: "jt-cash",
        lane: "revenue",
        project: "Consulting",
        dollars: 3500,
        stageProbability: 0.6,
      }),
    ];
    const queue = commandQueue(items, cashMandate);
    expect(queue[0].id).toBe("jt-cash");
    expect(queue.some((item) => item.source === "agent")).toBe(false);
    expect(queue.map((item) => item.id)).toEqual(["jt-cash", "cron-failed", "eve-failed-task"]);
  });

  test("sorts by score, tiebreaks on recency then title, and caps at seven", () => {
    const items = [
      dhcrDeposit,
      shipApp,
      ...Array.from({ length: 9 }, (_, index) =>
        signal({ id: `filler-${index}`, title: `Filler ${index}`, updatedAt: now - index * 1000 }),
      ),
    ];
    const queue = commandQueue(items, cashMandate);
    expect(queue).toHaveLength(7);
    expect(queue[0].id).toBe("dhcr");
    const scores = queue.map((item) => item.score ?? 0);
    expect([...scores].sort((a, b) => b - a)).toEqual(scores);
  });
});
