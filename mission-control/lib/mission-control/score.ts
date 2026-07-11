import type { Factors, ScoreBand, ScoreContext, ScoreResult, Signal } from "./types";

const DAY_MS = 24 * 60 * 60 * 1000;

const MAX = {
  cashImpact: 40,
  deadlinePressure: 15,
  unblockValue: 15,
  proofLeverage: 10,
  riskContainment: 10,
  stability: 10,
} as const;

const FOCUS_PENALTY = 15;
const EFFORT_DEMOTION = 10;
const EFFORT_MINUTES_THRESHOLD = 60;
const SHIP_CAP = 25;
const QUEUE_LIMIT = 7;

function isoDate(ms: number): string {
  return new Date(ms).toISOString().slice(0, 10);
}

/** Whole days from `now` to `due`, rounded up. Negative when overdue. */
function daysUntil(due: number, now: number): number {
  return Math.ceil((due - now) / DAY_MS);
}

/**
 * A "direct" cash event is one where completing the task moves money on a
 * revenue-lane deal. Callers can override; otherwise lane decides, so dollars
 * attached to a ship/app task count as indirect.
 */
function isDirectCash(signal: Signal): boolean {
  return signal.cashDirect ?? signal.lane === "revenue";
}

function expectedCash(signal: Signal): number {
  const dollars = signal.dollars ?? 0;
  if (dollars <= 0) return 0;
  const probability = signal.stageProbability ?? 1;
  return dollars * probability;
}

function cashImpact(signal: Signal): number {
  const expected = expectedCash(signal);
  if (expected <= 0) return 0;
  if (!isDirectCash(signal)) return 15;
  if (expected >= 3000) return MAX.cashImpact;
  if (expected >= 1000) return 30;
  return 15;
}

function deadlinePressure(signal: Signal, now: number): number {
  if (!signal.dueDate || !signal.dueDateSource) return 0;
  const days = daysUntil(signal.dueDate, now);
  let base = 0;
  if (days <= 0) base = MAX.deadlinePressure;
  else if (days <= 3) base = 12;
  else if (days <= 7) base = 8;
  if (signal.dueDateSource === "self") return Math.round(base / 2);
  return base;
}

function unblockValue(signal: Signal): number {
  const blocks = signal.blocks ?? 0;
  if (signal.blocksAgent || blocks >= 2) return MAX.unblockValue;
  if (blocks === 1) return 8;
  return 0;
}

export function deriveFactors(signal: Signal, ctx: ScoreContext = {}): Factors {
  const now = ctx.now ?? Date.now();
  return {
    cashImpact: cashImpact(signal),
    deadlinePressure: deadlinePressure(signal, now),
    unblockValue: unblockValue(signal),
    proofLeverage: signal.proofRequired ? MAX.proofLeverage : 0,
    riskContainment: signal.riskContainment ? MAX.riskContainment : 0,
    stability: signal.lane === "health" ? MAX.stability : 0,
  };
}

function focusPenaltyApplies(signal: Signal, ctx: ScoreContext, cash: number): boolean {
  const projects = ctx.focus?.projects;
  if (!projects || projects.length === 0) return false;
  if (cash >= 30) return false;
  return !signal.project || !projects.includes(signal.project);
}

function shipCapApplies(signal: Signal, ctx: ScoreContext): boolean {
  if (ctx.mandate !== "consulting-cash") return false;
  const gate = ctx.focus?.gate ?? 0;
  if ((ctx.collected ?? 0) >= gate) return false;
  return signal.lane === "ship" && !signal.dollars;
}

export function scoreTask(signal: Signal, ctx: ScoreContext = {}): ScoreResult {
  const now = ctx.now ?? Date.now();
  const factors = deriveFactors(signal, ctx);
  const reasonCodes: string[] = [];

  if (factors.cashImpact > 0) reasonCodes.push(`cash:${Math.round(expectedCash(signal))}`);
  if (factors.deadlinePressure > 0 && signal.dueDate) reasonCodes.push(`deadline:${isoDate(signal.dueDate)}`);
  if (factors.unblockValue > 0) {
    reasonCodes.push(signal.blocksAgent ? "unblocks:agent" : `unblocks:${signal.blocks ?? 0}`);
  }
  if (factors.proofLeverage > 0) reasonCodes.push("proof");
  if (factors.riskContainment > 0) reasonCodes.push("risk");
  if (factors.stability > 0) reasonCodes.push("stability");

  let score =
    factors.cashImpact +
    factors.deadlinePressure +
    factors.unblockValue +
    factors.proofLeverage +
    factors.riskContainment +
    factors.stability;

  if (focusPenaltyApplies(signal, ctx, factors.cashImpact)) {
    score -= FOCUS_PENALTY;
    reasonCodes.push("focus-penalty");
  }

  if ((signal.effortMinutes ?? 0) >= EFFORT_MINUTES_THRESHOLD && factors.cashImpact < 20) {
    score -= EFFORT_DEMOTION;
    reasonCodes.push("effort-demotion");
  }

  if (shipCapApplies(signal, ctx)) {
    score = Math.min(score, SHIP_CAP);
    reasonCodes.push("ship-capped");
  }

  score = Math.max(0, Math.min(100, Math.round(score)));

  if (score >= 50 && reasonCodes.length === 0) reasonCodes.push("unexplained");

  return { score, factors, reasonCodes };
}

export function scoreBand(score: number): ScoreBand {
  if (score >= 70) return "high";
  if (score >= 40) return "medium";
  return "low";
}

export function scoreSignal(signal: Signal, ctx: ScoreContext = {}): Signal {
  const { score, reasonCodes } = scoreTask(signal, ctx);
  const merged = [...(signal.reasonCodes ?? []), ...reasonCodes];
  return { ...signal, score, band: scoreBand(score), reasonCodes: merged };
}

const EXCLUDED_STATUSES = new Set(["done", "archived", "snoozed"]);
const EVE_ESCALATIONS = new Set(["failed", "stale"]);

function nudgeDue(signal: Signal, now: number): boolean {
  const waiting = signal.waitingOn;
  if (!waiting?.who) return false;
  return now - waiting.since > waiting.nudgeAfterDays * DAY_MS;
}

/**
 * Hard exclusions first, then score. Nothing that JT cannot act on right now
 * is allowed into the queue — externally blocked work only reappears when its
 * nudge comes due, and then as a nudge, not as the underlying task.
 */
export function commandQueue(signals: Signal[], ctx: ScoreContext = {}): Signal[] {
  const now = ctx.now ?? Date.now();

  const eligible: Signal[] = [];
  for (const signal of signals) {
    if (EXCLUDED_STATUSES.has(signal.status)) continue;
    if (signal.snoozedUntil && signal.snoozedUntil > now) continue;
    if (signal.owner === "eve" && !EVE_ESCALATIONS.has(signal.status)) continue;

    const waiting = signal.waitingOn;
    if (waiting?.who) {
      if (!nudgeDue(signal, now)) continue;
      eligible.push({
        ...signal,
        title: `Nudge ${waiting.who}: ${waiting.what}`,
        reasonCodes: [...(signal.reasonCodes ?? []), "nudge-due"],
      });
      continue;
    }

    eligible.push(signal);
  }

  return eligible
    .map((signal) => scoreSignal(signal, { ...ctx, now }))
    .sort((a, b) => {
      const scoreDiff = (b.score ?? 0) - (a.score ?? 0);
      if (scoreDiff !== 0) return scoreDiff;
      const updatedDiff = b.updatedAt - a.updatedAt;
      if (updatedDiff !== 0) return updatedDiff;
      return a.title.localeCompare(b.title);
    })
    .slice(0, QUEUE_LIMIT);
}
