// Block parks the item on a person (DECISIONS 6): who, what, nudge after N days. One write.
import { DAY_MS } from "./eligibility";
import type { WaitingOn } from "./types";

export interface ParkInput { who: string; what: string; days: string }
export interface ParkValue { who: string; what: string; nudgeAfterDays: number }
export type ParkErrors = Partial<Record<"who" | "what" | "days", string>>;

export function validatePark(input: ParkInput): { ok: true; value: ParkValue } | { ok: false; errors: ParkErrors } {
  const errors: ParkErrors = {};
  const who = input.who.trim();
  const what = input.what.trim();
  const daysText = input.days.trim();
  const days = /^\d+$/.test(daysText) ? Number(daysText) : NaN;
  if (!who) errors.who = "Enter who you are waiting on.";
  if (!what) errors.what = "Enter what you are waiting for.";
  if (!Number.isInteger(days) || days < 1 || days > 365) errors.days = "Enter a whole number of days from 1 to 365.";
  if (Object.keys(errors).length > 0) return { ok: false, errors };
  return { ok: true, value: { who, what, nudgeAfterDays: days } };
}

export function parkPatch(value: ParkValue, now: number): Record<string, unknown> {
  return {
    waitingOn: { who: value.who, what: value.what, since: now, nudgeAfterDays: value.nudgeAfterDays },
    status: "waiting-external",
    auditSource: "jt",
    auditEvidence: "Parked from Mission Control run",
  };
}

/** The item becomes eligible again once now is strictly past this instant. */
export function nudgeDueAt(waitingOn: WaitingOn): number {
  return waitingOn.since + waitingOn.nudgeAfterDays * DAY_MS;
}
