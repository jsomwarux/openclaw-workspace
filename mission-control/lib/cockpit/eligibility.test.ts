import { describe, expect, test } from "bun:test";
import { decisionCode, familyOf } from "./classify";
import { isEligible, isExpired, nudgeDue } from "./eligibility";
import { curatedOrder, groupOf } from "./order";
import { FIXTURE_NOW, allFixtureTasks, fixtureIdOf, fx } from "./fixtures/data";
import type { RawTask } from "./types";

const DAY = 86_400_000;
const NOW = FIXTURE_NOW;
const ids = (tasks: RawTask[]) => tasks.map((task) => fixtureIdOf(task) ?? task._id);

function task(over: Partial<RawTask>): RawTask {
  return { _id: over._id ?? "t", title: "A task", status: "todo", assignee: "jt", priority: "high", createdAt: NOW - DAY, updatedAt: NOW - DAY, ...over };
}

describe("decision card detection (DECISIONS 1.4)", () => {
  test("reads the program prefix, the code and the number", () => {
    expect(decisionCode("Sample DC Q1: step check")).toEqual({ series: "Q", number: 1 });
    expect(decisionCode("Sample DC P12: value")).toEqual({ series: "P", number: 12 });
    expect(decisionCode("Sample DC AP7: field")).toEqual({ series: "AP", number: 7 });
    expect(decisionCode("Q3: no program prefix")).toEqual({ series: "Q", number: 3 });
  });

  test("refuses titles that only look similar", () => {
    for (const title of ["q1: lower case", "Sample Q1 no colon", "SampleQ1: no space", "Sample Q1234: four digits", "Blocked: note entry", "", undefined]) {
      expect(decisionCode(title)).toBe(null);
    }
  });

  test("families: lane packet and outreach review win over a decision-looking title", () => {
    expect(familyOf(fx("F01"))).toBe("decision");
    expect(familyOf(fx("F04"))).toBe("generic");
    expect(familyOf(fx("F05"))).toBe("lanePacket");
    expect(familyOf(fx("F11"))).toBe("outreachReview");
    expect(familyOf(task({ title: "X Q1: packet", packetSchema: "lane-packet-v1" }))).toBe("lanePacket");
  });
});

describe("eligibility (DECISIONS 1.1, data contract 7.1 step 1)", () => {
  test("the fixture set: expired packet, agent-owned and done cards are out; everything else is in", () => {
    const eligible = allFixtureTasks().filter((t) => isEligible(t, NOW));
    expect(ids(eligible).sort()).toEqual(["F01", "F02", "F03", "F04", "F05", "F07", "F08", "F11", "F12"]);
  });

  test("closed statuses are out", () => {
    for (const status of ["done", "archived", "snoozed"]) expect(isEligible(task({ status }), NOW)).toBe(false);
    for (const status of ["todo", "in-progress", "waiting-external"]) expect(isEligible(task({ status }), NOW)).toBe(true);
  });

  test("a lane packet at or past expiresAt is out; one millisecond before is in", () => {
    const packet = fx("F05");
    expect(isEligible({ ...packet, expiresAt: NOW }, NOW)).toBe(false);
    expect(isExpired({ ...packet, expiresAt: NOW }, NOW)).toBe(true);
    expect(isEligible({ ...packet, expiresAt: NOW + 1 }, NOW)).toBe(true);
    expect(isExpired(fx("F06"), NOW)).toBe(true);
    expect(isExpired({ ...fx("F06"), status: "done" }, NOW)).toBe(false);
  });

  test("a future snooze hides the card; a passed one does not", () => {
    expect(isEligible(task({ snoozedUntil: NOW + 1 }), NOW)).toBe(false);
    expect(isEligible(task({ snoozedUntil: NOW }), NOW)).toBe(true);
    expect(isEligible(fx("F12"), NOW)).toBe(true);
  });

  test("owner eve is out; jt and both are in", () => {
    expect(isEligible(task({ assignee: "eve" }), NOW)).toBe(false);
    expect(isEligible(task({ assignee: "both" }), NOW)).toBe(true);
  });

  test("a parked card stays out until now - since is strictly more than nudgeAfterDays", () => {
    const parked = (since: number) => task({ status: "waiting-external", waitingOn: { who: "Pat", what: "the lease", since, nudgeAfterDays: 14 } });
    expect(isEligible(parked(NOW - 14 * DAY), NOW)).toBe(false);
    expect(nudgeDue(parked(NOW - 14 * DAY), NOW)).toBe(false);
    expect(isEligible(parked(NOW - 14 * DAY - 1), NOW)).toBe(true);
    expect(nudgeDue(fx("F07"), NOW)).toBe(true);
  });

  test("waiting-external alone does not hide a JT card", () => {
    expect(isEligible(task({ status: "waiting-external" }), NOW)).toBe(true);
  });

  test("an outreach review that already has a decision is out", () => {
    const decided = { ...fx("F11"), outreachDecision: { decision: "reject", decidedBy: "jt", decidedAt: NOW - DAY } };
    expect(isEligible(decided, NOW)).toBe(false);
    expect(isEligible(fx("F11"), NOW)).toBe(true);
  });
});

describe("curated order (DECISIONS 1.3 to 1.7)", () => {
  test("fixture order: Q, P, AP by number, then other cards by sortOrder, then those without one", () => {
    const eligible = allFixtureTasks().filter((t) => isEligible(t, NOW));
    expect(ids(curatedOrder(eligible))).toEqual(["F01", "F02", "F03", "F07", "F12", "F04", "F05", "F11", "F08"]);
  });

  test("decision numbers compare as numbers, not strings", () => {
    const cards = ["Q10", "Q2", "Q1", "P12", "P3", "AP9", "AP10"].map((code, index) => task({ _id: code, title: `Growth OS ${code}: decide`, sortOrder: 300 - index }));
    expect(curatedOrder(cards).map((card) => card._id)).toEqual(["Q1", "Q2", "Q10", "P3", "P12", "AP9", "AP10"]);
  });

  test("priority and rankScore never change the order", () => {
    const a = task({ _id: "a", sortOrder: 20, priority: "low", rankScore: 99 });
    const b = task({ _id: "b", sortOrder: 10, priority: "high", rankScore: 1 });
    expect(curatedOrder([a, b]).map((card) => card._id)).toEqual(["b", "a"]);
  });

  test("tie-break: shared sortOrder by createdAt, then title A to Z, then id; missing sortOrder last", () => {
    const shared = [
      task({ _id: "late", sortOrder: 220, createdAt: NOW - 1 * DAY, title: "A" }),
      task({ _id: "early", sortOrder: 220, createdAt: NOW - 3 * DAY, title: "Z" }),
      task({ _id: "same-b", sortOrder: 220, createdAt: NOW - 2 * DAY, title: "Beta" }),
      task({ _id: "same-a", sortOrder: 220, createdAt: NOW - 2 * DAY, title: "Alpha" }),
      task({ _id: "id-2", sortOrder: 220, createdAt: NOW - 2 * DAY, title: "Alpha" }),
      task({ _id: "none-old", createdAt: NOW - 90 * DAY }),
      task({ _id: "low", sortOrder: 5, createdAt: NOW }),
    ];
    expect(curatedOrder(shared).map((card) => card._id)).toEqual(["low", "early", "id-2", "same-a", "same-b", "late", "none-old"]);
  });

  test("groups", () => {
    expect(groupOf(fx("F01"))).toBe("Q");
    expect(groupOf(fx("F02"))).toBe("P");
    expect(groupOf(fx("F03"))).toBe("AP");
    expect(groupOf(fx("F05"))).toBe("Other cards");
    expect(groupOf(fx("F08"))).toBe("Other cards");
  });
});
