import type { FocusRow, ScoreContext } from "./types";

/**
 * The focus row is keyed by the Monday of its week. Computed in local time so a
 * Sunday-evening session in ET does not roll into next week's row.
 */
export function mondayOf(now: number): string {
  const d = new Date(now);
  const dow = d.getDay(); // 0 = Sunday
  d.setDate(d.getDate() - (dow === 0 ? 6 : dow - 1));
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${month}-${day}`;
}

/**
 * The cockpit's scoring context. The mandate is what arms the ship cap in
 * score.ts; without it the cap silently never fires.
 *
 * `collected` is deliberately floored to 0 when the north-star read is
 * unavailable. A missing number must leave the cap ARMED — treating an
 * unreadable file as "gate already met" would disarm the one guard that keeps
 * ship work from outranking cash.
 */
export function buildScoreContext(input: {
  focus?: FocusRow | null;
  collected?: number | null;
  now?: number;
}): ScoreContext {
  const collected = typeof input.collected === "number" && Number.isFinite(input.collected) ? input.collected : 0;
  return {
    focus: input.focus ?? null,
    mandate: "consulting-cash",
    collected,
    now: input.now ?? Date.now(),
  };
}
