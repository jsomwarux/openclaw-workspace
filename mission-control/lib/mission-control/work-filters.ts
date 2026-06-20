import type { Signal } from "./types";
import { sortWorkSignals } from "./work-priority";

export type WorkFilter = "all" | "jt" | "eve" | "high" | "blocked" | "done";

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
  if (filter === "done") {
    return sortDoneSignals(signals.filter(isDone));
  }

  const activeSignals = signals.filter(isActive);
  const matching = activeSignals.filter((signal) => {
    if (filter === "jt") return signal.owner === "jt";
    if (filter === "eve") return signal.owner === "eve";
    if (filter === "high") return signal.priority === "high";
    if (filter === "blocked") return signal.status === "blocked" || signal.status === "stale" || signal.ageDays >= 14;
    return true;
  });

  return sortWorkSignals(matching);
}
