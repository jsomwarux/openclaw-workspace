// Curated order (DECISIONS 1.3 to 1.7): Q, P, AP by code number, then other cards by
// sortOrder. priority and rankScore are never read.
import { decisionCode, familyOf } from "./classify";
import type { RawTask } from "./types";

export type QueueGroup = "Q" | "P" | "AP" | "Other cards";
export const GROUPS: QueueGroup[] = ["Q", "P", "AP", "Other cards"];

export function groupOf(task: RawTask): QueueGroup {
  return familyOf(task) === "decision" ? decisionCode(task.title)!.series : "Other cards";
}

const finite = (value: unknown): value is number => typeof value === "number" && Number.isFinite(value);

/** Missing values sort after present ones; present ones ascend. */
function ascendingMissingLast(a: unknown, b: unknown): number {
  if (finite(a) && finite(b)) return a - b;
  if (finite(a)) return -1;
  if (finite(b)) return 1;
  return 0;
}

export function curatedCompare(a: RawTask, b: RawTask): number {
  const group = GROUPS.indexOf(groupOf(a)) - GROUPS.indexOf(groupOf(b));
  if (group !== 0) return group;
  if (groupOf(a) !== "Other cards") {
    return decisionCode(a.title)!.number - decisionCode(b.title)!.number || a._id.localeCompare(b._id, "en");
  }
  return (
    ascendingMissingLast(a.sortOrder, b.sortOrder) ||
    ascendingMissingLast(a.createdAt, b.createdAt) ||
    (a.title ?? "").localeCompare(b.title ?? "", "en") ||
    a._id.localeCompare(b._id, "en")
  );
}

export function curatedOrder(tasks: RawTask[]): RawTask[] {
  return [...tasks].sort(curatedCompare);
}
