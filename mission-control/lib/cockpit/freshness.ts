// Read freshness (DECISIONS 15): stale after 5 minutes without a good read (actions pause);
// degraded after two failed or slow (over 10 s) reads in a row (actions stay available).

export const POLL_MS = 60_000;
export const STALE_MS = 5 * 60_000;
export const SLOW_MS = 10_000;
const DEGRADED_AFTER = 2;
const RETRY_BASE_MS = 8_000;
const RETRY_MAX_MS = 60_000;

export interface ReadHealth {
  lastGoodAt: number | null;
  consecutiveBad: number;
  lastAttemptAt: number | null;
}

export const initialHealth: ReadHealth = { lastGoodAt: null, consecutiveBad: 0, lastAttemptAt: null };

export function recordRead(health: ReadHealth, read: { ok: boolean; startedAt: number; finishedAt: number }): ReadHealth {
  const slow = read.finishedAt - read.startedAt > SLOW_MS;
  return {
    lastGoodAt: read.ok ? read.finishedAt : health.lastGoodAt,
    consecutiveBad: !read.ok || slow ? health.consecutiveBad + 1 : 0,
    lastAttemptAt: read.finishedAt,
  };
}

export type ConnectionState = "checking" | "fresh" | "stale" | "degraded";

export function connectionState(health: ReadHealth, now: number): ConnectionState {
  if (health.lastGoodAt === null) return "checking";
  if (now - health.lastGoodAt > STALE_MS) return "stale";
  if (health.consecutiveBad >= DEGRADED_AFTER) return "degraded";
  return "fresh";
}

export function retryDelay(consecutiveBad: number): number {
  return Math.min(RETRY_MAX_MS, RETRY_BASE_MS * 2 ** Math.max(0, consecutiveBad - DEGRADED_AFTER));
}
