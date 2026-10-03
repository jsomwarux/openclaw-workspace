// Which items may enter today's run (DECISIONS 1.1, data contract 7.1 step 1).
import { isLanePacket, isOutreachReview } from "./classify";
import type { RawTask } from "./types";

export const DAY_MS = 86_400_000;
const CLOSED_STATUSES = new Set(["done", "archived", "snoozed"]);

export function isClosedPacket(task: RawTask): boolean {
  return isLanePacket(task) && (task.status === "done" || task.status === "archived");
}

/** An open lane packet at or past its expiresAt. Closed packets never read as expired. */
export function isExpired(task: RawTask, now: number): boolean {
  return isLanePacket(task) && !isClosedPacket(task) && typeof task.expiresAt === "number" && now >= task.expiresAt;
}

export function isParked(task: RawTask): boolean {
  return Boolean(task.waitingOn && typeof task.waitingOn.who === "string" && task.waitingOn.who.length > 0);
}

/** The nudge is due once now - since is strictly more than nudgeAfterDays days. */
export function nudgeDue(task: RawTask, now: number): boolean {
  if (!isParked(task)) return false;
  const { since, nudgeAfterDays } = task.waitingOn!;
  return now - since > nudgeAfterDays * DAY_MS;
}

export function isDecidedOutreach(task: RawTask): boolean {
  return isOutreachReview(task) && typeof task.outreachDecision === "object" && task.outreachDecision !== null;
}

export function isEligible(task: RawTask, now: number): boolean {
  if (typeof task.status === "string" && CLOSED_STATUSES.has(task.status)) return false;
  if (isExpired(task, now)) return false;
  if (typeof task.snoozedUntil === "number" && task.snoozedUntil > now) return false;
  if (task.assignee === "eve") return false;
  if (isParked(task) && !nudgeDue(task, now)) return false;
  if (isDecidedOutreach(task)) return false;
  return true;
}
