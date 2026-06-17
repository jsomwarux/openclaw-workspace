import type { Signal } from "./types";

type RevenueSnapshot = {
  active: number;
  high: number;
  done: number;
  costToday: number | null;
  costAlerts: unknown[];
};

export type CommandBrief = {
  headline: string;
  topAction: Signal | null;
  latestProof: Signal | null;
  urgentJtCount: number;
  riskCount: number;
  revenuePressure: number;
};

function isJtPressure(signal: Signal) {
  return (
    signal.owner === "jt" &&
    signal.priority === "high" &&
    ["awaiting-decision", "awaiting-approval", "blocked"].includes(signal.status)
  );
}

function isRisk(signal: Signal) {
  return ["failed", "blocked", "stale"].includes(signal.status);
}

function latestProofSignal(signals: Signal[]) {
  return (
    signals
      .filter((signal) => signal.source === "proof")
      .sort((a, b) => b.updatedAt - a.updatedAt)[0] ?? null
  );
}

function topQueuedAction(queue: Signal[]) {
  return (
    [...queue].sort((a, b) => {
      const scoreDelta = (b.score ?? 0) - (a.score ?? 0);
      if (scoreDelta !== 0) return scoreDelta;
      return b.updatedAt - a.updatedAt;
    })[0] ?? null
  );
}

export function commandBrief({
  queue,
  signals,
  revenue,
}: {
  queue: Signal[];
  signals: Signal[];
  revenue: RevenueSnapshot;
}): CommandBrief {
  const topAction = topQueuedAction(queue);
  const latestProof = latestProofSignal(signals);
  const urgentJtCount = signals.filter(isJtPressure).length;
  const riskCount = signals.filter(isRisk).length;
  const revenuePressure = revenue.high;

  const parts = [
    urgentJtCount ? `${urgentJtCount} high-priority JT items` : "",
    revenuePressure ? `${revenuePressure} revenue-path high` : "",
    riskCount ? `${riskCount} risk signal${riskCount === 1 ? "" : "s"}` : "",
  ].filter(Boolean);

  return {
    headline: parts.length ? parts.join(" · ") : "Command is clear.",
    topAction,
    latestProof,
    urgentJtCount,
    riskCount,
    revenuePressure,
  };
}
