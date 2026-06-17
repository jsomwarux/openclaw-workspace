import type { Signal, SignalPriority, SignalStatus } from "./types";

const PRIORITY_RANK: Record<SignalPriority, number> = {
  high: 3,
  medium: 2,
  low: 1,
};

const STATUS_RANK: Record<SignalStatus, number> = {
  failed: 5,
  blocked: 5,
  stale: 4,
  "awaiting-decision": 3,
  "awaiting-approval": 3,
  "in-progress": 2,
  done: 0,
};

export function priorityRank(priority?: SignalPriority): number {
  return priority ? PRIORITY_RANK[priority] : 0;
}

export function priorityBadgeClassName(priority?: SignalPriority): string {
  if (priority === "high") return "border-rose-500/40 bg-rose-500/10 text-rose-300";
  if (priority === "medium") return "border-amber-500/35 bg-amber-500/10 text-amber-300";
  if (priority === "low") return "border-zinc-700 bg-zinc-900/80 text-zinc-400";
  return "border-[#20262d] bg-[#111] text-zinc-500";
}

export function priorityRailClassName(priority?: SignalPriority): string {
  if (priority === "high") return "border-l-rose-500";
  if (priority === "medium") return "border-l-amber-500";
  if (priority === "low") return "border-l-zinc-700";
  return "border-l-[#20262d]";
}

export function sortWorkSignals(signals: Signal[]): Signal[] {
  return [...signals].sort((a, b) => {
    const priorityDelta = priorityRank(b.priority) - priorityRank(a.priority);
    if (priorityDelta !== 0) return priorityDelta;

    const statusDelta = STATUS_RANK[b.status] - STATUS_RANK[a.status];
    if (statusDelta !== 0) return statusDelta;

    return b.updatedAt - a.updatedAt;
  });
}
