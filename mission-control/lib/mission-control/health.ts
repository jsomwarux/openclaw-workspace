import { sortWorkSignals } from "./work-priority";
import type { Signal } from "./types";

type CostAlert = {
  level?: string;
  message?: string;
};

type CostState = {
  alerts?: CostAlert[];
};

export type HealthSummary = {
  failures: number;
  stale: number;
  costAlerts: number;
  recoveryWork: number;
  posture: "clear" | "review";
};

export type HealthGroups = {
  failures: Signal[];
  costs: Signal[];
  stale: Signal[];
  recovery: Signal[];
};

function isHealthRelevant(signal: Signal) {
  return signal.lane === "health" || signal.lane === "machine" || ["failed", "blocked", "stale"].includes(signal.status);
}

function isFailure(signal: Signal) {
  return signal.status === "failed" || signal.status === "blocked";
}

function isStale(signal: Signal) {
  return signal.status === "stale" || signal.ageDays >= 14;
}

function isCostSignal(signal: Signal) {
  const text = `${signal.project ?? ""} ${signal.title} ${signal.context ?? ""}`.toLowerCase();
  return /(cost|spend|budget|openrouter|token|runaway|api usage|wallet)/.test(text);
}

function isRecoverySignal(signal: Signal) {
  if (signal.status === "done") return false;
  const text = `${signal.project ?? ""} ${signal.title} ${signal.context ?? ""}`.toLowerCase();
  return /(recover|cleanup|fix|repair|restart|health|monitor|guard|cooldown|failure|outage)/.test(text);
}

export function healthSummary(signals: Signal[], costs: CostState | null = null): HealthSummary {
  const relevant = signals.filter(isHealthRelevant);
  const failures = relevant.filter(isFailure).length;
  const stale = relevant.filter((signal) => !isFailure(signal) && isStale(signal)).length;
  const recoveryWork = relevant.filter((signal) => !isFailure(signal) && !isStale(signal) && isRecoverySignal(signal)).length;
  const costAlerts = costs?.alerts?.length ?? 0;

  return {
    failures,
    stale,
    costAlerts,
    recoveryWork,
    posture: failures + stale + costAlerts > 0 ? "review" : "clear",
  };
}

export function healthGroups(signals: Signal[]): HealthGroups {
  const groups: HealthGroups = {
    failures: [],
    costs: [],
    stale: [],
    recovery: [],
  };

  for (const signal of sortWorkSignals(signals.filter(isHealthRelevant))) {
    if (isFailure(signal)) groups.failures.push(signal);
    else if (isCostSignal(signal)) groups.costs.push(signal);
    else if (isStale(signal)) groups.stale.push(signal);
    else if (isRecoverySignal(signal)) groups.recovery.push(signal);
  }

  return groups;
}
