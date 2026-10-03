// Plain-language dates, ages and durations. Times show in the operator's browser zone with
// the zone name (GAPS 21). Parts are assembled by hand so ICU wording ("at") never leaks in.

const MINUTE = 60_000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

type Parts = Record<string, string>;

function parts(ms: number, timeZone: string, options: Intl.DateTimeFormatOptions): Parts {
  const out: Parts = {};
  for (const part of new Intl.DateTimeFormat("en-US", { timeZone, ...options }).formatToParts(new Date(ms))) {
    out[part.type] = part.value;
  }
  return out;
}

const CLOCK: Intl.DateTimeFormatOptions = { hour: "2-digit", minute: "2-digit", hourCycle: "h23", timeZoneName: "short" };

/** "Oct 3, 05:00 UTC" */
export function formatShort(ms: number, timeZone: string): string {
  const p = parts(ms, timeZone, { month: "short", day: "numeric", ...CLOCK });
  return `${p.month} ${p.day}, ${p.hour}:${p.minute} ${p.timeZoneName}`;
}

/** "Sep 24, 2026, 00:00 UTC" */
export function formatFull(ms: number, timeZone: string): string {
  const p = parts(ms, timeZone, { year: "numeric", month: "short", day: "numeric", ...CLOCK });
  return `${p.month} ${p.day}, ${p.year}, ${p.hour}:${p.minute} ${p.timeZoneName}`;
}

/** "Sun, Oct 4, 08:00 EDT" */
export function formatWeekdayTime(ms: number, timeZone: string): string {
  const p = parts(ms, timeZone, { weekday: "short", month: "short", day: "numeric", ...CLOCK });
  return `${p.weekday}, ${p.month} ${p.day}, ${p.hour}:${p.minute} ${p.timeZoneName}`;
}

/** "Aug 21" */
export function formatMonthDay(ms: number, timeZone: string): string {
  const p = parts(ms, timeZone, { month: "short", day: "numeric" });
  return `${p.month} ${p.day}`;
}

/** "Saturday, Oct 3" */
export function formatLongDay(ms: number, timeZone: string): string {
  const p = parts(ms, timeZone, { weekday: "long", month: "short", day: "numeric" });
  return `${p.weekday}, ${p.month} ${p.day}`;
}

/** "Sat, Oct 3" */
export function formatShortDay(ms: number, timeZone: string): string {
  const p = parts(ms, timeZone, { weekday: "short", month: "short", day: "numeric" });
  return `${p.weekday}, ${p.month} ${p.day}`;
}

/** "2026-10-03" in the given zone. Runs are keyed by this. */
export function localDateKey(ms: number, timeZone: string): string {
  const p = parts(ms, timeZone, { year: "numeric", month: "2-digit", day: "2-digit" });
  return `${p.year}-${p.month}-${p.day}`;
}

const plural = (n: number, unit: string) => `${n} ${unit}${n === 1 ? "" : "s"}`;

/** "5 hours", "2 days", "45 minutes". Rounds down to the largest whole unit. */
export function durationText(ms: number): string {
  const span = Math.max(0, ms);
  if (span >= DAY) return plural(Math.floor(span / DAY), "day");
  if (span >= HOUR) return plural(Math.floor(span / HOUR), "hour");
  return plural(Math.max(1, Math.floor(span / MINUTE)), "minute");
}

/** "9 days ago", "3 hours ago", "38 minutes ago", "just now". Rounds to the nearest unit. */
export function relativeAgo(ms: number, now: number): string {
  const span = now - ms;
  if (span < MINUTE) return "just now";
  if (span >= DAY) return `${plural(Math.round(span / DAY), "day")} ago`;
  if (span >= HOUR) return `${plural(Math.round(span / HOUR), "hour")} ago`;
  return `${plural(Math.round(span / MINUTE), "minute")} ago`;
}

/** Queue age since createdAt: hours under 48 hours ("2h", "<1h"), otherwise days ("9d"). */
export function ageText(createdAt: number | undefined, now: number): string {
  if (typeof createdAt !== "number") return "—";
  const span = Math.max(0, now - createdAt);
  if (span < 48 * HOUR) {
    const hours = Math.round(span / HOUR);
    return hours < 1 ? "<1h" : `${hours}h`;
  }
  return `${Math.round(span / DAY)}d`;
}

const NUMBER_WORDS = ["None", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"];
export function countWord(n: number): string {
  return NUMBER_WORDS[n] ?? String(n);
}

export function browserTimeZone(): string {
  return Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
}
