import { describe, expect, test } from "bun:test";
import { deferAvailable, deferOptions, deferPatch, deferUndoValue, untilForDate, zonedTime } from "./defer";
import { nudgeDueAt, parkPatch, validatePark } from "./block";
import { FIXTURE_NOW, fx } from "./fixtures/data";

const HOUR = 3_600_000;
const DAY = 24 * HOUR;
const NY = "America/New_York";
const iso = (ms: number | null) => (ms === null ? null : new Date(ms).toISOString());

describe("Defer is a snooze (DECISIONS override 1)", () => {
  test("8:00 local wall time converts to the right instant, across the end of daylight saving", () => {
    expect(iso(zonedTime(2026, 10, 4, 8, 0, NY))).toBe("2026-10-04T12:00:00.000Z");
    expect(iso(zonedTime(2026, 11, 1, 8, 0, NY))).toBe("2026-11-01T13:00:00.000Z");
    expect(iso(zonedTime(2026, 10, 4, 8, 0, "UTC"))).toBe("2026-10-04T08:00:00.000Z");
  });

  test("offers tomorrow at 8am (selected by default), next week, and a date", () => {
    // Sat Oct 3 2026, 12:00 in New York.
    const now = Date.parse("2026-10-03T16:00:00Z");
    const options = deferOptions(fx("F04"), now, NY);
    expect(options.map((option) => option.id)).toEqual(["tomorrow", "nextWeek", "date"]);
    expect(options[0]).toMatchObject({ id: "tomorrow", label: "Tomorrow, 8:00 AM", until: Date.parse("2026-10-04T12:00:00Z"), disabledReason: null });
    expect(options[0].detail).toBe("Sun, Oct 4, 08:00 EDT");
    expect(options[1]).toMatchObject({ id: "nextWeek", label: "Next week, Monday 8:00 AM", until: Date.parse("2026-10-05T12:00:00Z") });
    expect(options[2]).toMatchObject({ id: "date", label: "Pick a date", until: null });
  });

  test("on a Sunday, next week skips tomorrow's Monday", () => {
    const sunday = Date.parse("2026-10-04T16:00:00Z");
    const options = deferOptions(fx("F04"), sunday, NY);
    expect(iso(options[0].until)).toBe("2026-10-05T12:00:00.000Z");
    expect(iso(options[1].until)).toBe("2026-10-12T12:00:00.000Z");
  });

  test("a picked date snoozes until 8:00 local that day and must be after today", () => {
    const now = Date.parse("2026-10-03T16:00:00Z");
    expect(untilForDate(fx("F04"), "2026-10-20", now, NY)).toEqual({ ok: true, until: Date.parse("2026-10-20T12:00:00Z") });
    expect(untilForDate(fx("F04"), "2026-10-03", now, NY)).toEqual({ ok: false, error: "Choose a date after today." });
    expect(untilForDate(fx("F04"), "2026-09-30", now, NY)).toEqual({ ok: false, error: "Choose a date after today." });
    expect(untilForDate(fx("F04"), "", now, NY)).toEqual({ ok: false, error: "Choose a date." });
    expect(untilForDate(fx("F04"), "2026-02-30", now, NY)).toEqual({ ok: false, error: "Choose a date." });
  });

  test("on a lane packet, no option may pass expiresAt", () => {
    // F05 expires Oct 5, 01:09 UTC. Tomorrow 08:00 UTC fits; next Monday 08:00 UTC does not.
    const options = deferOptions(fx("F05"), FIXTURE_NOW, "UTC");
    expect(options[0].disabledReason).toBe(null);
    expect(options[1].disabledReason).toBe("Not available: this item expires Oct 5, 01:09 UTC.");
    expect(untilForDate(fx("F05"), "2026-10-04", FIXTURE_NOW, "UTC")).toEqual({ ok: true, until: Date.parse("2026-10-04T08:00:00Z") });
    expect(untilForDate(fx("F05"), "2026-10-05", FIXTURE_NOW, "UTC")).toEqual({ ok: false, error: "This item expires Oct 5, 01:09 UTC. Choose a date before then." });
  });

  test("Defer is hidden on outreach reviews, closed packets, and packets that expire before tomorrow 8am", () => {
    expect(deferAvailable(fx("F04"), FIXTURE_NOW, "UTC")).toBe(true);
    expect(deferAvailable(fx("F05"), FIXTURE_NOW, "UTC")).toBe(true);
    expect(deferAvailable(fx("F11"), FIXTURE_NOW, "UTC")).toBe(false);
    expect(deferAvailable({ ...fx("F05"), status: "done" }, FIXTURE_NOW, "UTC")).toBe(false);
    expect(deferAvailable({ ...fx("F05"), expiresAt: FIXTURE_NOW + 6 * HOUR }, FIXTURE_NOW, "UTC")).toBe(false);
  });

  test("writes only snoozedUntil, with the change attributed to jt", () => {
    expect(deferPatch(123)).toEqual({ snoozedUntil: 123, auditSource: "jt", auditEvidence: "Deferred from Mission Control run" });
  });

  test("Undo writes back the previous snooze, or the moment of Undo when there was none", () => {
    expect(deferUndoValue(FIXTURE_NOW - 30 * DAY, FIXTURE_NOW)).toBe(FIXTURE_NOW - 30 * DAY);
    expect(deferUndoValue(undefined, FIXTURE_NOW)).toBe(FIXTURE_NOW);
  });
});

describe("Block parks the item on a person (DECISIONS 6)", () => {
  test("validates who, what and a whole number of days from 1 to 365, keeping the values", () => {
    expect(validatePark({ who: " ", what: "", days: "0" })).toEqual({ ok: false, errors: {
      who: "Enter who you are waiting on.", what: "Enter what you are waiting for.", days: "Enter a whole number of days from 1 to 365." } });
    for (const days of ["1.5", "366", "", "-3", "1e1", "ten"]) {
      expect(validatePark({ who: "Pat", what: "the lease", days })).toEqual({ ok: false, errors: { days: "Enter a whole number of days from 1 to 365." } });
    }
    expect(validatePark({ who: " Pat ", what: " the lease ", days: " 14 " })).toEqual({ ok: true, value: { who: "Pat", what: "the lease", nudgeAfterDays: 14 } });
    expect(validatePark({ who: "Pat", what: "x", days: "365" })).toMatchObject({ ok: true });
  });

  test("one write: waitingOn, waiting-external status, and an evidence string", () => {
    expect(parkPatch({ who: "Pat", what: "the lease", nudgeAfterDays: 14 }, FIXTURE_NOW)).toEqual({
      waitingOn: { who: "Pat", what: "the lease", since: FIXTURE_NOW, nudgeAfterDays: 14 },
      status: "waiting-external",
      auditSource: "jt",
      auditEvidence: "Parked from Mission Control run",
    });
    expect(nudgeDueAt({ who: "Pat", what: "x", since: FIXTURE_NOW, nudgeAfterDays: 14 })).toBe(FIXTURE_NOW + 14 * DAY);
  });
});
