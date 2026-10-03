// Defer is a snooze (DECISIONS override 1, Confirmed 2026-10-03): tomorrow at 8am local
// (the default), next week, or a date. It writes snoozedUntil only. A lane packet's snooze
// may not pass expiresAt. Hidden on outreach reviews and closed packets.
import { familyOf, isLanePacket } from "./classify";
import { isClosedPacket, isExpired } from "./eligibility";
import { formatShort, formatWeekdayTime, localDateKey } from "./format";
import type { RawTask } from "./types";

export type DeferOptionId = "tomorrow" | "nextWeek" | "date";
export interface DeferOption {
  id: DeferOptionId;
  label: string;
  detail: string | null;
  until: number | null;
  disabledReason: string | null;
}

const DEFER_HOUR = 8;

/** Offset of the zone from UTC at an instant, in ms. */
function zoneOffset(ms: number, timeZone: string): number {
  const p: Record<string, number> = {};
  const format = new Intl.DateTimeFormat("en-US", {
    timeZone, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit",
  });
  for (const part of format.formatToParts(new Date(ms))) if (part.type !== "literal") p[part.type] = Number(part.value);
  return Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute, p.second) - Math.floor(ms / 1000) * 1000;
}

/** The instant at which the wall clock in timeZone reads y-m-d h:min. */
export function zonedTime(year: number, month: number, day: number, hour: number, minute: number, timeZone: string): number {
  const wall = Date.UTC(year, month - 1, day, hour, minute);
  const first = wall - zoneOffset(wall, timeZone);
  return wall - zoneOffset(first, timeZone);
}

function localYmd(ms: number, timeZone: string): { y: number; m: number; d: number; weekday: number } {
  const [y, m, d] = localDateKey(ms, timeZone).split("-").map(Number);
  return { y, m, d, weekday: new Date(Date.UTC(y, m - 1, d)).getUTCDay() };
}

function eightAmAfter(now: number, days: number, timeZone: string): number {
  const { y, m, d } = localYmd(now, timeZone);
  const date = new Date(Date.UTC(y, m - 1, d + days));
  return zonedTime(date.getUTCFullYear(), date.getUTCMonth() + 1, date.getUTCDate(), DEFER_HOUR, 0, timeZone);
}

function passesExpiry(task: RawTask, until: number): boolean {
  return isLanePacket(task) && typeof task.expiresAt === "number" && until > task.expiresAt;
}

export function deferOptions(task: RawTask, now: number, timeZone: string): DeferOption[] {
  const { weekday } = localYmd(now, timeZone);
  const toMonday = (8 - weekday) % 7 || 7;
  const option = (id: DeferOptionId, label: string, until: number): DeferOption => ({
    id,
    label,
    detail: formatWeekdayTime(until, timeZone),
    until,
    disabledReason: passesExpiry(task, until) ? `Not available: this item expires ${formatShort(task.expiresAt!, timeZone)}.` : null,
  });
  return [
    option("tomorrow", "Tomorrow, 8:00 AM", eightAmAfter(now, 1, timeZone)),
    option("nextWeek", "Next week, Monday 8:00 AM", eightAmAfter(now, toMonday === 1 ? 8 : toMonday, timeZone)),
    { id: "date", label: "Pick a date", detail: null, until: null, disabledReason: null },
  ];
}

export function untilForDate(task: RawTask, value: string, now: number, timeZone: string): { ok: true; until: number } | { ok: false; error: string } {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return { ok: false, error: "Choose a date." };
  const [y, m, d] = [Number(match[1]), Number(match[2]), Number(match[3])];
  const check = new Date(Date.UTC(y, m - 1, d));
  if (check.getUTCFullYear() !== y || check.getUTCMonth() !== m - 1 || check.getUTCDate() !== d) return { ok: false, error: "Choose a date." };
  if (value <= localDateKey(now, timeZone)) return { ok: false, error: "Choose a date after today." };
  const until = zonedTime(y, m, d, DEFER_HOUR, 0, timeZone);
  if (passesExpiry(task, until)) {
    return { ok: false, error: `This item expires ${formatShort(task.expiresAt!, timeZone)}. Choose a date before then.` };
  }
  return { ok: true, until };
}

/** Whether Defer may render at all for this item. */
export function deferAvailable(task: RawTask, now: number, timeZone: string): boolean {
  if (familyOf(task) === "outreachReview" || isClosedPacket(task) || isExpired(task, now)) return false;
  return !passesExpiry(task, eightAmAfter(now, 1, timeZone));
}

export function deferPatch(until: number): Record<string, unknown> {
  return { snoozedUntil: until, auditSource: "jt", auditEvidence: "Deferred from Mission Control run" };
}

/**
 * The value Undo writes back. The backend cannot remove snoozedUntil (Phase 0 finding), so
 * when there was no snooze before, Undo writes the moment of Undo: already past, so the
 * item is eligible exactly as before.
 */
export function deferUndoValue(previous: number | undefined, now: number): number {
  return typeof previous === "number" ? previous : now;
}
