import { describe, expect, test } from "bun:test";
import { buildScoreContext, mondayOf } from "./score-context";
import { scoreTask } from "./score";
import type { Signal } from "./types";

const MONDAY = new Date(2026, 6, 6).getTime(); // Mon 2026-07-06
const SATURDAY = new Date(2026, 6, 11).getTime(); // Sat 2026-07-11
const SUNDAY = new Date(2026, 6, 12).getTime(); // Sun 2026-07-12

function signal(over: Partial<Signal>): Signal {
  return {
    id: "t1",
    source: "task",
    title: "t",
    owner: "jt",
    status: "in-progress",
    lane: "work",
    ageDays: 0,
    evidence: [],
    updatedAt: 0,
    raw: null,
    ...over,
  };
}

describe("mondayOf", () => {
  test("returns the same day for a Monday", () => {
    expect(mondayOf(MONDAY)).toBe("2026-07-06");
  });

  test("walks back to Monday from midweek", () => {
    expect(mondayOf(SATURDAY)).toBe("2026-07-06");
  });

  test("treats Sunday as the end of the week, not the start", () => {
    expect(mondayOf(SUNDAY)).toBe("2026-07-06");
  });
});

describe("buildScoreContext", () => {
  test("always arms the consulting-cash mandate", () => {
    expect(buildScoreContext({}).mandate).toBe("consulting-cash");
  });

  test("floors collected to 0 when the north-star read is unavailable", () => {
    expect(buildScoreContext({ collected: undefined }).collected).toBe(0);
    expect(buildScoreContext({ collected: null }).collected).toBe(0);
    expect(buildScoreContext({ collected: NaN }).collected).toBe(0);
  });

  test("passes a real collected figure through", () => {
    expect(buildScoreContext({ collected: 4200 }).collected).toBe(4200);
  });
});

describe("the wired context arms the ship cap", () => {
  const focus = { weekOf: "2026-07-06", projects: ["Consulting"], gate: 10000 };

  // External 7-day deadline (8) + proofRequired (10) + blocks 1 (8) = 26 raw.
  // project "Consulting" keeps it inside focus, isolating the cap from the penalty.
  const loadedShip = signal({
    lane: "ship",
    title: "loaded ship task",
    project: "Consulting",
    dueDate: SATURDAY + 7 * 24 * 60 * 60 * 1000,
    dueDateSource: "external",
    proofRequired: true,
    blocks: 1,
  });

  // The case the cap actually exists for: overdue (15) + blocksAgent (15) +
  // proof (10) + risk (10) = 50 raw, which clears MSI's 40 and would seize NOW.
  const worstCaseShip = signal({
    lane: "ship",
    title: "worst-case ship task",
    project: "Consulting",
    dueDate: SATURDAY - 24 * 60 * 60 * 1000,
    dueDateSource: "external",
    proofRequired: true,
    blocksAgent: true,
    riskContainment: true,
  });

  test("caps a loaded ship task at 25 when the mandate is live", () => {
    const ctx = buildScoreContext({ focus, collected: 0, now: SATURDAY });
    const { score, reasonCodes } = scoreTask(loadedShip, ctx);
    expect(score).toBe(25);
    expect(reasonCodes).toContain("ship-capped");
  });

  test("would NOT cap it with the empty context the cockpit used to pass", () => {
    const { score, reasonCodes } = scoreTask(loadedShip, { now: SATURDAY });
    expect(score).toBe(26);
    expect(reasonCodes).not.toContain("ship-capped");
  });

  test("stacks the focus penalty ahead of the cap for out-of-focus ship work", () => {
    const ctx = buildScoreContext({ focus, collected: 0, now: SATURDAY });
    const offFocus = { ...loadedShip, project: "App Marketing" };
    expect(scoreTask(offFocus, ctx).score).toBe(11); // 26 − 15, then capped
  });

  test("slams a worst-case ship task that would otherwise seize NOW from cash", () => {
    // Uncapped it beats MSI. This is the whole reason the gate must be armed.
    expect(scoreTask(worstCaseShip, { now: SATURDAY }).score).toBe(50);

    const ctx = buildScoreContext({ focus, collected: 0, now: SATURDAY });
    const capped = scoreTask(worstCaseShip, ctx);
    expect(capped.score).toBe(25);
    expect(capped.reasonCodes).toContain("ship-capped");
  });

  test("keeps the capped ship task below the MSI cash task", () => {
    const ctx = buildScoreContext({ focus, collected: 0, now: SATURDAY });
    const msi = signal({
      lane: "revenue",
      title: "MSI",
      project: "Consulting",
      dollars: 12000,
      stageProbability: 0.7,
    });
    expect(scoreTask(msi, ctx).score).toBe(40);
    expect(scoreTask(loadedShip, ctx).score).toBeLessThan(scoreTask(msi, ctx).score);
  });

  test("does not penalize Consulting cash work under the corrected focus row", () => {
    const ctx = buildScoreContext({ focus, collected: 0, now: SATURDAY });
    const altmark = signal({
      lane: "revenue",
      title: "Altmark",
      project: "Consulting",
      dollars: 2250,
      stageProbability: 0.55,
    });
    expect(scoreTask(altmark, ctx).reasonCodes).not.toContain("focus-penalty");
  });

  test("disarms the cap once the gate is met", () => {
    const ctx = buildScoreContext({ focus, collected: 10000, now: SATURDAY });
    expect(scoreTask(loadedShip, ctx).reasonCodes).not.toContain("ship-capped");
  });
});
