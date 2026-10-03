// Urgent exceptions (DECISIONS 3): the only two reasons an item may jump curated order,
// and the run plan at start (DECISIONS 1.8, 2).
import { isLanePacket } from "./classify";
import { isClosedPacket, isEligible } from "./eligibility";
import { durationText, formatMonthDay, formatShort } from "./format";
import { curatedCompare, curatedOrder } from "./order";
import type { ExceptionLabel, RawTask } from "./types";

export const RUN_SIZE = 7;
const DAY = 86_400_000;

export function urgentException(task: RawTask, now: number, timeZone: string): ExceptionLabel | null {
  if (typeof task.dueDate === "number" && task.dueDate < now && task.dueDateSource === "external") {
    const overdue = now - task.dueDate;
    const amount = overdue >= 3_600_000 ? durationText(overdue) : "less than an hour";
    return {
      reason: "externalDeadlineOverdue",
      text: `Moved up: external deadline passed ${formatMonthDay(task.dueDate, timeZone)} (${amount} overdue)`,
    };
  }
  if (
    isLanePacket(task) &&
    !isClosedPacket(task) &&
    task.approvalState === "pending" &&
    typeof task.expiresAt === "number" &&
    task.expiresAt - now > 0 &&
    task.expiresAt - now <= DAY
  ) {
    return {
      reason: "approvalExpiresSoon",
      text: `Moved up: approval expires in ${durationText(task.expiresAt - now)} (${formatShort(task.expiresAt, timeZone)})`,
    };
  }
  return null;
}

/** The moment that orders several exceptions: the deadline or the expiry, earliest first. */
export function exceptionTime(task: RawTask, label: ExceptionLabel): number {
  return label.reason === "externalDeadlineOverdue" ? task.dueDate! : task.expiresAt!;
}

/** Exceptions first (earliest time first), then curated order, cut to the run size. */
export function planRun(tasks: RawTask[], now: number, timeZone: string, size = RUN_SIZE): { ids: string[]; exceptions: Record<string, ExceptionLabel> } {
  const eligible = tasks.filter((task) => isEligible(task, now));
  const labelled = eligible
    .map((task) => ({ task, label: urgentException(task, now, timeZone) }))
    .filter((entry): entry is { task: RawTask; label: ExceptionLabel } => entry.label !== null)
    .sort((a, b) => exceptionTime(a.task, a.label) - exceptionTime(b.task, b.label) || curatedCompare(a.task, b.task));
  const jumped = new Set(labelled.map((entry) => entry.task._id));
  const rest = curatedOrder(eligible.filter((task) => !jumped.has(task._id)));
  const ids = [...labelled.map((entry) => entry.task._id), ...rest.map((task) => task._id)].slice(0, size);
  const exceptions: Record<string, ExceptionLabel> = {};
  for (const entry of labelled) if (ids.includes(entry.task._id)) exceptions[entry.task._id] = entry.label;
  return { ids, exceptions };
}
