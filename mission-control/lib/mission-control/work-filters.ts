import type { Signal } from "./types";
import { sortWorkSignals } from "./work-priority";

export type WorkFilter =
  | "all"
  | "jt"
  | "eve"
  | "high"
  | "blocked"
  | "done"
  | "career-hedge"
  | "waiting-jt"
  | "compounding-bets"
  | "waiting-external"
  | "archive-triggers"
  | "now"
  | "paid-delivery";

function isDone(signal: Signal): boolean {
  return signal.status === "done";
}

function isActive(signal: Signal): boolean {
  return !isDone(signal);
}

function sortDoneSignals(signals: Signal[]): Signal[] {
  return [...signals].sort((a, b) => b.updatedAt - a.updatedAt);
}

export function filterWorkSignals(signals: Signal[], filter: WorkFilter): Signal[] {
  if (filter === "archive-triggers") {
    return sortDoneSignals(signals.filter((signal) => signal.status === "archived"));
  }
  if (filter === "done") {
    return sortDoneSignals(signals.filter(isDone));
  }

  const activeSignals = signals.filter(isActive);
  const matching = activeSignals.filter((signal) => {
    if (filter === "jt") return signal.owner === "jt";
    if (filter === "eve") return signal.owner === "eve";
    if (filter === "high") return signal.priority === "high";
    if (filter === "blocked") return signal.status === "blocked" || signal.status === "stale" || signal.ageDays >= 14;
    if (filter === "now") return signal.priority === "high" && signal.status !== "waiting-external";
    if (filter === "paid-delivery") return signal.workstream === "paid-delivery";
    if (filter === "career-hedge") return signal.workstream === "career-hedge";
    if (filter === "waiting-jt") {
      return signal.waitingOn?.who.trim().toLowerCase() === "jt" || signal.status === "awaiting-approval";
    }
    if (filter === "compounding-bets") return signal.workstream === "compounding-bet";
    if (filter === "waiting-external") return signal.status === "waiting-external";
    return true;
  });

  return sortWorkSignals(matching);
}
