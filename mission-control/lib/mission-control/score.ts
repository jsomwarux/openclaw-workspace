import type { Factors, ScoreBand, Signal } from "./types";

const WEIGHTS = {
  revenue: 0.3,
  unblock: 0.2,
  urgency: 0.2,
  risk: 0.15,
  northStar: 0.15,
} as const;

export function computeScore(factors: Factors): number {
  const weighted =
    factors.revenue * WEIGHTS.revenue +
    factors.unblock * WEIGHTS.unblock +
    factors.urgency * WEIGHTS.urgency +
    factors.risk * WEIGHTS.risk +
    factors.northStar * WEIGHTS.northStar;
  const effortPenalty = factors.effortOver30 ? 12 : 0;
  const score = Math.round((100 * weighted) / 3) - effortPenalty;
  return Math.max(0, Math.min(100, score));
}

export function scoreBand(score: number): ScoreBand {
  if (score >= 70) return "high";
  if (score >= 40) return "medium";
  return "low";
}

export function needsJT(signal: Signal): boolean {
  return (
    signal.owner === "jt" &&
    ["awaiting-decision", "awaiting-approval", "blocked"].includes(signal.status)
  );
}

export function deriveFactors(signal: Signal): Factors {
  const revenueLane = signal.lane === "revenue";
  const shippingLane = signal.lane === "ship";
  const highPriority = signal.priority === "high";
  const stale = signal.status === "stale" || signal.ageDays >= 14;

  return {
    revenue: revenueLane ? (signal.dollars && signal.dollars >= 8000 ? 3 : 2) : shippingLane ? 1 : 0,
    unblock: signal.status === "blocked" && signal.owner === "jt" ? 3 : signal.status === "blocked" ? 2 : 0,
    urgency: signal.dueToday ? 3 : highPriority ? 3 : signal.priority === "medium" ? 2 : stale ? 0 : 1,
    risk: signal.status === "failed" ? 3 : signal.status === "stale" ? 2 : stale ? 1 : 1,
    northStar: revenueLane ? 3 : shippingLane ? 2 : 1,
    effortOver30: false,
  };
}

export function scoreSignal(signal: Signal): Signal {
  const score = computeScore(deriveFactors(signal));
  return { ...signal, score, band: scoreBand(score) };
}

export function commandQueue(signals: Signal[]): Signal[] {
  return signals
    .filter(needsJT)
    .map(scoreSignal)
    .sort((a, b) => {
      const scoreDiff = (b.score ?? 0) - (a.score ?? 0);
      if (scoreDiff !== 0) return scoreDiff;
      const updatedDiff = b.updatedAt - a.updatedAt;
      if (updatedDiff !== 0) return updatedDiff;
      return a.title.localeCompare(b.title);
    })
    .slice(0, 7);
}
