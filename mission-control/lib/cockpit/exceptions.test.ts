import { describe, expect, test } from "bun:test";
import { planRun, urgentException } from "./exceptions";
import { FIXTURE_NOW, ID, allFixtureTasks, fx } from "./fixtures/data";
import type { FixtureId } from "./fixtures/data";
import type { RawTask } from "./types";

const HOUR = 3_600_000;
const DAY = 24 * HOUR;
const NOW = FIXTURE_NOW;
const UTC = "UTC";
const byId = Object.fromEntries(Object.entries(ID).map(([fixture, id]) => [id, fixture]));
const names = (plan: { ids: string[] }) => plan.ids.map((id) => byId[id] ?? id);

function withEdits(edits: Partial<Record<FixtureId, Partial<RawTask>>>): RawTask[] {
  return allFixtureTasks().map((task) => {
    const fixture = byId[task._id] as FixtureId;
    return edits[fixture] ? { ...task, ...edits[fixture] } : task;
  });
}

describe("urgent exception triggers (DECISIONS 3.1, 3.2)", () => {
  test("a pending lane packet expiring within 24 hours jumps, with a label that says why", () => {
    const packet = { ...fx("F05"), expiresAt: NOW + 5 * HOUR };
    expect(urgentException(packet, NOW, UTC)).toEqual({
      reason: "approvalExpiresSoon",
      text: "Moved up: approval expires in 5 hours (Oct 3, 05:00 UTC)",
    });
  });

  test("exactly 24 hours qualifies; a millisecond more does not; expired does not", () => {
    expect(urgentException({ ...fx("F05"), expiresAt: NOW + DAY }, NOW, UTC)?.reason).toBe("approvalExpiresSoon");
    expect(urgentException({ ...fx("F05"), expiresAt: NOW + DAY + 1 }, NOW, UTC)).toBe(null);
    expect(urgentException({ ...fx("F05"), expiresAt: NOW }, NOW, UTC)).toBe(null);
    expect(urgentException(fx("F06"), NOW, UTC)).toBe(null);
  });

  test("an approved or closed packet never jumps", () => {
    expect(urgentException({ ...fx("F05"), expiresAt: NOW + HOUR, approvalState: "approved" }, NOW, UTC)).toBe(null);
    expect(urgentException({ ...fx("F05"), expiresAt: NOW + HOUR, status: "done" }, NOW, UTC)).toBe(null);
  });

  test("an overdue external deadline jumps; self-set or unsourced deadlines never do", () => {
    expect(urgentException({ ...fx("F12"), dueDateSource: "external" }, NOW, UTC)).toEqual({
      reason: "externalDeadlineOverdue",
      text: "Moved up: external deadline passed Aug 21 (42 days overdue)",
    });
    expect(urgentException(fx("F12"), NOW, UTC)).toBe(null);
    expect(urgentException({ ...fx("F12"), dueDateSource: undefined }, NOW, UTC)).toBe(null);
    expect(urgentException({ ...fx("F12"), dueDateSource: "external", dueDate: NOW + HOUR }, NOW, UTC)).toBe(null);
  });

  test("a waiting card with an overdue nudge does not jump", () => {
    expect(urgentException(fx("F07"), NOW, UTC)).toBe(null);
  });
});

describe("run planning at start (DECISIONS 1.8, 2, 3.4, 3.5)", () => {
  test("no exceptions: the curated order cut to 7", () => {
    const plan = planRun(allFixtureTasks(), NOW, UTC);
    expect(names(plan)).toEqual(["F01", "F02", "F03", "F07", "F12", "F04", "F05"]);
    expect(plan.exceptions).toEqual({});
  });

  test("an exception inside the cut moves to position 1", () => {
    const plan = planRun(withEdits({ F05: { expiresAt: NOW + 5 * HOUR } }), NOW, UTC);
    expect(names(plan)).toEqual(["F05", "F01", "F02", "F03", "F07", "F12", "F04"]);
    expect(plan.exceptions[ID.F05]?.reason).toBe("approvalExpiresSoon");
  });

  test("an exception outside the cut displaces the last curated item; the run stays 7", () => {
    const plan = planRun(withEdits({ F08: { dueDate: NOW - 2 * DAY, dueDateSource: "external" } }), NOW, UTC);
    expect(names(plan)).toEqual(["F08", "F01", "F02", "F03", "F07", "F12", "F04"]);
    expect(plan.ids).toHaveLength(7);
  });

  test("several exceptions order by the earliest expiresAt or dueDate", () => {
    const plan = planRun(withEdits({
      F05: { expiresAt: NOW + 2 * HOUR },
      F08: { dueDate: NOW - 2 * DAY, dueDateSource: "external" },
      F12: { dueDateSource: "external" },
    }), NOW, UTC);
    expect(names(plan).slice(0, 3)).toEqual(["F12", "F08", "F05"]);
  });

  test("fewer than 7 eligible: the run is that size; none eligible: an empty plan", () => {
    const few = [fx("F01"), fx("F02"), fx("F09"), fx("F10")];
    expect(names(planRun(few, NOW, UTC))).toEqual(["F01", "F02"]);
    expect(planRun([fx("F06"), fx("F09"), fx("F10")], NOW, UTC).ids).toEqual([]);
  });
});
