/**
 * Collected cash, derived from the stored payments ledger — never from
 * pipeline.jsonl (which zeroes items once paid) or the north-star.md regex.
 * This is the single source of truth for "how much has JT actually collected".
 */

export type GateBasis = "monthly" | "all-time";

export type Payment = {
  clientName: string;
  amount: number;
  paidOn: number; // epoch ms
  milestone?: string;
  kind: "consulting" | "unemployment" | "other";
  cleared: boolean;
  source?: string;
};

export type CollectedMetrics = {
  consultingAllTime: number;
  unemploymentAllTime: number;
  totalAllTime: number;
  consultingMonth: number;
  unemploymentMonth: number;
  totalMonth: number;
  gateBasis: GateBasis;
  gateAmount: number;
  /** Consulting cash counted against the gate, on the gate's basis. */
  gateCollected: number;
  /** Positive = still short of the gate; negative = over. */
  gapToGate: number;
};

export const DEFAULT_GATE_AMOUNT = 10_000;

function sameMonth(a: number, b: number): boolean {
  const da = new Date(a);
  const db = new Date(b);
  return da.getFullYear() === db.getFullYear() && da.getMonth() === db.getMonth();
}

/** Cleared payments only. A pending/invoiced row is not collected cash. */
function sum(payments: Payment[], predicate: (p: Payment) => boolean): number {
  return payments.reduce((total, p) => (p.cleared && predicate(p) ? total + p.amount : total), 0);
}

export function computeCollected(
  payments: Payment[],
  opts: { now: number; gateAmount?: number; gateBasis?: GateBasis },
): CollectedMetrics {
  const now = opts.now;
  const gateAmount = opts.gateAmount ?? DEFAULT_GATE_AMOUNT;
  const gateBasis = opts.gateBasis ?? "monthly";

  const isConsulting = (p: Payment) => p.kind === "consulting";
  const isUnemployment = (p: Payment) => p.kind === "unemployment";
  const inMonth = (p: Payment) => p.paidOn <= now && sameMonth(p.paidOn, now);

  const consultingAllTime = sum(payments, isConsulting);
  const unemploymentAllTime = sum(payments, isUnemployment);
  const consultingMonth = sum(payments, (p) => isConsulting(p) && inMonth(p));
  const unemploymentMonth = sum(payments, (p) => isUnemployment(p) && inMonth(p));

  const gateCollected = gateBasis === "monthly" ? consultingMonth : consultingAllTime;

  return {
    consultingAllTime,
    unemploymentAllTime,
    totalAllTime: consultingAllTime + unemploymentAllTime,
    consultingMonth,
    unemploymentMonth,
    totalMonth: consultingMonth + unemploymentMonth,
    gateBasis,
    gateAmount,
    gateCollected,
    gapToGate: gateAmount - gateCollected,
  };
}
