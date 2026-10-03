// The daily-run state machine (state map Part B, transitions 1 to 11). Pure functions over
// the stored run record; the controller persists the results. Order is committed at start.
import { isLanePacket } from "./classify";
import { changedKeys, closedElsewhere, describeChange, fingerprint, trackedFields } from "./changes";
import { isEligible, isExpired } from "./eligibility";
import { exceptionTime, planRun, RUN_SIZE, urgentException } from "./exceptions";
import { formatShort, localDateKey, relativeAgo } from "./format";
import { curatedOrder } from "./order";
import type { ExceptionLabel, LeftReason, RawTask, RunChange, RunItem, SnapshotEntry, StoredRun } from "./types";

export function snapshotEntry(task: RawTask): SnapshotEntry {
  const fields = trackedFields(task);
  return {
    id: task._id,
    status: task.status ?? "",
    updatedAt: task.updatedAt ?? 0,
    payloadHash: task.payloadHash,
    approvalState: task.approvalState,
    expiresAt: task.expiresAt,
    fingerprint: fingerprint(fields),
    fields,
  };
}

const byId = (tasks: RawTask[]) => new Map(tasks.map((task) => [task._id, task]));
export const itemResolved = (item: RunItem) => item.outcome !== undefined || item.left !== undefined;
export const allResolved = (run: StoredRun) => run.items.every(itemResolved);

function settlePhase(run: StoredRun, now?: number): StoredRun {
  if (allResolved(run)) return { ...run, phase: "complete", completedAt: run.completedAt ?? now };
  return run.phase === "complete" ? { ...run, phase: "inProgress", completedAt: undefined } : run;
}

/** Transition 1. The snapshot covers every run item; knownIds and startIds cover every task read. */
export function startRun(tasks: RawTask[], now: number, timeZone: string): StoredRun {
  const plan = planRun(tasks, now, timeZone);
  const index = byId(tasks);
  const ids = tasks.map((task) => task._id);
  return {
    version: 1,
    localDate: localDateKey(now, timeZone),
    phase: "inProgress",
    size: plan.ids.length,
    order: "curated",
    items: plan.ids.map((id) => (plan.exceptions[id] ? { id, exception: plan.exceptions[id] } : { id })),
    cursor: 0,
    snapshot: plan.ids.map((id) => snapshotEntry(index.get(id)!)),
    knownIds: ids,
    startIds: ids,
    startedAt: now,
    rebasedAt: now,
  };
}

/** Transition 2: a successful write handles the item. The cursor stays until Next. */
export function recordOutcome(run: StoredRun, id: string, update: Partial<RunItem>, now?: number): StoredRun {
  const items = run.items.map((item) => (item.id === id ? { ...item, ...update, left: update.outcome ? undefined : item.left } : item));
  return settlePhase({ ...run, items }, now);
}

/** Undo: the item counts as open again; the status line says what was restored. */
export function clearOutcome(run: StoredRun, id: string, line: string): StoredRun {
  const items = run.items.map((item) =>
    item.id === id ? { id: item.id, exception: item.exception, line } : item,
  );
  return settlePhase({ ...run, items });
}

/** Fold the operator's own successful write into the snapshot so it is not read as a change. */
export function foldWrite(run: StoredRun, id: string, patch: Record<string, unknown>): StoredRun {
  const snapshot = run.snapshot.map((entry) => {
    if (entry.id !== id) return entry;
    const fields = { ...entry.fields, ...trackedFields(patch) };
    return { ...entry, fields, status: (fields.status as string) ?? entry.status, fingerprint: fingerprint(fields) };
  });
  return { ...run, snapshot };
}

export function moveNext(run: StoredRun, leave?: LeftReason): { run: StoredRun; atEnd: boolean; notice?: string } {
  let next = run;
  const current = run.items[run.cursor];
  if (leave && current && !itemResolved(current)) {
    next = settlePhase({ ...run, items: run.items.map((item, i) => (i === run.cursor ? { ...item, left: leave } : item)) });
  }
  if (next.cursor < next.size - 1) return { run: { ...next, cursor: next.cursor + 1 }, atEnd: false };
  if (allResolved(next)) return { run: next, atEnd: true };
  const open = next.items.findIndex((item) => !itemResolved(item));
  return { run: { ...next, cursor: open }, atEnd: false, notice: `Item ${open + 1} of ${next.size} still needs you.` };
}

export function movePrevious(run: StoredRun): { run: StoredRun; notice?: string } {
  if (run.cursor === 0) return { run, notice: "This is the first item." };
  return { run: { ...run, cursor: run.cursor - 1 } };
}

export function moveTo(run: StoredRun, id: string): StoredRun {
  const index = run.items.findIndex((item) => item.id === id);
  return index < 0 ? run : { ...run, cursor: index };
}

/** Transition 3. */
export function pause(run: StoredRun, now: number): StoredRun {
  return run.phase === "complete" ? run : { ...run, phase: "paused", pausedAt: now };
}

/** Where urgent exceptions sit after acknowledge: right after the open item, earliest first. */
function placeExceptions(run: StoredRun, tasks: RawTask[], now: number, timeZone: string): {
  items: RunItem[];
  joined: { id: string; label: ExceptionLabel; position: number }[];
  displaced: string[];
} {
  const index = byId(tasks);
  const head = run.items.slice(0, run.cursor + 1);
  const tail = run.items.slice(run.cursor + 1);
  const inRun = new Set(run.items.map((item) => item.id));
  const startIds = new Set(run.startIds);
  const labelOf = (id: string) => {
    const task = index.get(id);
    return task && isEligible(task, now) ? urgentException(task, now, timeZone) : null;
  };

  const urgentTail = tail.filter((item) => !itemResolved(item) && labelOf(item.id));
  const urgentBacklog = tasks.filter((task) => !inRun.has(task._id) && startIds.has(task._id) && labelOf(task._id));
  const urgent = [
    ...urgentTail.map((item) => ({ item, task: index.get(item.id)! })),
    ...urgentBacklog.map((task) => ({ item: { id: task._id } as RunItem, task })),
  ]
    .map((entry) => ({ ...entry, label: labelOf(entry.task._id)! }))
    .sort((a, b) => exceptionTime(a.task, a.label) - exceptionTime(b.task, b.label));
  if (urgent.length === 0) return { items: run.items, joined: [], displaced: [] };

  const urgentIds = new Set(urgent.map((entry) => entry.task._id));
  let rest = tail.filter((item) => !urgentIds.has(item.id));
  let placed = urgent.map((entry) => ({ ...entry.item, exception: entry.label }));
  // Keep the run size: drop the last unhandled curated items first, then any backlog
  // exception that still does not fit (it stays in the backlog).
  while (head.length + placed.length + rest.length > run.size) {
    const drop = [...rest].reverse().find((item) => !itemResolved(item) && !item.exception);
    if (drop) rest = rest.filter((item) => item !== drop);
    else {
      const backlogIndex = placed.map((item) => inRun.has(item.id)).lastIndexOf(false);
      if (backlogIndex < 0) break;
      placed = placed.filter((_, i) => i !== backlogIndex);
    }
  }
  const items = [...head, ...placed, ...rest];
  const kept = new Set(items.map((item) => item.id));
  const displaced = run.items.filter((item) => !kept.has(item.id)).map((item) => item.id);
  const joined = placed
    .map((item) => ({ id: item.id, label: item.exception!, position: items.indexOf(item) }))
    .filter((entry) => run.items.findIndex((item) => item.id === entry.id) !== entry.position);
  return { items, joined, displaced };
}

const where = (run: StoredRun, index: number) => `Item ${index + 1} of ${run.size}`;

/** The material changes between the snapshot and a fresh read (state map Part B). */
export function detectChanges(run: StoredRun, tasks: RawTask[], now: number, timeZone: string): RunChange[] {
  const index = byId(tasks);
  const known = new Set(run.knownIds);
  const inRun = new Set(run.items.map((item) => item.id));
  // Every item resolved and not closed: new cards join (transition 9). Derived from the items, not
  // the phase, so the text stays the same on every poll and after a reload (review finding 5).
  const reopenable = allResolved(run) && run.closedAt === undefined;

  const added = tasks
    .filter((task) => !known.has(task._id) && !inRun.has(task._id) && isEligible(task, now))
    .map((task, i): RunChange => ({
      kind: reopenable ? "addedToRun" : "addedToBacklog",
      itemId: task._id,
      title: task.title ?? "",
      where: reopenable ? `Joins today's run as item ${run.size + i + 1}` : "Not in today's run",
      detail: typeof task.createdAt === "number" ? `Created ${relativeAgo(task.createdAt, now)}.` : "Added since you left.",
      affectsOpenItem: false,
      inRun: reopenable,
    }));
  if (reopenable) return added;

  const runChanges: RunChange[] = [];
  run.items.forEach((item, i) => {
    if (itemResolved(item)) return;
    const entry = run.snapshot.find((snap) => snap.id === item.id);
    const task = index.get(item.id);
    const base = { itemId: item.id, where: where(run, i), affectsOpenItem: i === run.cursor, inRun: true };
    if (!task) {
      runChanges.push({ ...base, kind: "removedFromRun", title: String(entry?.fields.title ?? ""), detail: "It is no longer in Mission Control. It leaves today's run." });
    } else if (isExpired(task, now) && !(typeof entry?.expiresAt === "number" && entry.expiresAt <= run.rebasedAt)) {
      runChanges.push({ ...base, kind: "expired", title: task.title ?? "", detail: `Expired ${formatShort(task.expiresAt!, timeZone)}. Approval is no longer possible.` });
    } else if (entry && fingerprint(trackedFields(task)) !== entry.fingerprint) {
      runChanges.push({ ...base, kind: "changed", title: task.title ?? "", detail: describeChange(entry.fields, task, now) });
    }
  });

  const placement = placeExceptions(run, tasks, now, timeZone);
  const moved = placement.joined.map((entry): RunChange => ({
    kind: "movedUp",
    itemId: entry.id,
    title: index.get(entry.id)?.title ?? "",
    where: `Becomes item ${entry.position + 1} of ${run.size}`,
    detail: entry.label.text,
    affectsOpenItem: false,
    inRun: true,
  }));
  const displaced = placement.displaced.map((id): RunChange => ({
    kind: "displaced",
    itemId: id,
    title: index.get(id)?.title ?? String(run.snapshot.find((entry) => entry.id === id)?.fields.title ?? ""),
    where: where(run, run.items.findIndex((item) => item.id === id)),
    detail: "An urgent item takes its place. It goes back to the backlog when you acknowledge.",
    affectsOpenItem: false,
    inRun: true,
  }));

  const expiredBacklog = tasks
    .filter((task) => !inRun.has(task._id) && known.has(task._id) && isExpired(task, now) && task.expiresAt! > run.rebasedAt)
    .map((task): RunChange => ({
      kind: "expired",
      itemId: task._id,
      title: task.title ?? "",
      where: "Not in today's run",
      detail: `Expired ${formatShort(task.expiresAt!, timeZone)}. Hidden from today.`,
      affectsOpenItem: false,
      inRun: false,
    }));

  return [...runChanges, ...moved, ...displaced, ...added, ...expiredBacklog];
}

/** Transitions 4 and 5: return to the run and compare a fresh read with the snapshot. */
export function resume(run: StoredRun, tasks: RawTask[], now: number, timeZone: string): { run: StoredRun; changes: RunChange[] } {
  const changes = detectChanges(run, tasks, now, timeZone);
  if (changes.length > 0) return { run: { ...run, phase: "queueChanged" }, changes };
  return { run: settlePhase({ ...run, phase: "inProgress" }, now), changes };
}

/** Transitions 6 and 9: a background read. Nothing is reordered until acknowledge. */
export function backgroundCheck(run: StoredRun, tasks: RawTask[], now: number, timeZone: string): { run: StoredRun; changes: RunChange[] } {
  if (run.closedAt !== undefined) return { run, changes: [] };
  const changes = detectChanges(run, tasks, now, timeZone);
  // Only changes to the run itself interrupt it (transition 6). Backlog additions and expiries
  // wait for the next resume, where they are still reported (review finding 6).
  if (!changes.some((change) => change.inRun)) return { run, changes };
  return { run: { ...run, phase: run.phase === "paused" ? "paused" : "queueChanged" }, changes };
}

/** The outcome an item reached on its record without a write from this run. */
function outcomeElsewhere(task: RawTask): Partial<RunItem> | null {
  const decision = task.outreachDecision?.decision;
  if (decision === "approve") return { outcome: "approved", elsewhere: true, did: "Approved elsewhere." };
  if (decision === "reject") return { outcome: "rejected", elsewhere: true, did: "Rejected elsewhere." };
  if (task.status === "done") return { outcome: "completed", elsewhere: true, did: "Marked done elsewhere." };
  if (task.status === "archived") {
    if (isLanePacket(task) && (task.closureReason as { kind?: string } | undefined)?.kind === "rejected") {
      return { outcome: "rejected", elsewhere: true, did: "Rejected elsewhere." };
    }
    return { left: "removed", did: closedElsewhere(task) ?? "Closed elsewhere." };
  }
  return null;
}

/** Transition 7 (and 9): acknowledge the change summary and re-base the snapshot. */
export function acknowledge(run: StoredRun, tasks: RawTask[], now: number, timeZone: string): StoredRun {
  const index = byId(tasks);
  let items = run.items.map((item): RunItem => {
    if (itemResolved(item)) return item;
    const task = index.get(item.id);
    if (!task) return { ...item, left: "removed", did: "Removed elsewhere." };
    return { ...item, ...(outcomeElsewhere(task) ?? {}) };
  });

  let next: StoredRun = { ...run, items };
  if (allResolved(run) && run.closedAt === undefined) {
    const known = new Set(run.knownIds);
    const fresh = curatedOrder(tasks.filter((task) => !known.has(task._id) && isEligible(task, now))).slice(0, RUN_SIZE);
    if (fresh.length > 0 && run.closedAt === undefined) {
      items = [...items, ...fresh.map((task) => ({ id: task._id }))];
      next = { ...next, items, size: items.length, cursor: run.items.length };
    }
  } else {
    next = { ...next, items: placeExceptions(next, tasks, now, timeZone).items };
  }

  const snapshot = next.items.map((item) => {
    const task = index.get(item.id);
    return task ? snapshotEntry(task) : run.snapshot.find((entry) => entry.id === item.id)!;
  });
  return settlePhase({ ...next, snapshot, knownIds: tasks.map((task) => task._id), rebasedAt: now, phase: "inProgress" }, now);
}

/** Transition 10: an earlier day's run that was never closed is closed now, kept for its summary. */
export function rollover(run: StoredRun | null, today: string, now: number): { previous: StoredRun | null } {
  if (!run || run.localDate >= today || run.closedAt !== undefined) return { previous: null };
  return { previous: { ...run, closedAt: now, unfinished: !allResolved(run) } };
}

/** Field-level differences for the "Changed underneath me" panel. */
export function itemChangedKeys(run: StoredRun, task: RawTask): string[] {
  const entry = run.snapshot.find((snap) => snap.id === task._id);
  return entry ? changedKeys(entry.fields, trackedFields(task)) : [];
}
