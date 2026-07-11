export type CashMetrics = {
  totalCollected: number;
  weightedForecast: number;
};

export type CashStrip =
  | { available: false; text: "metrics unavailable" }
  | {
      available: true;
      text: string;
      collected: number;
      weighted: number;
      gate: number;
      daysLeft: number;
    };

export const CASH_GATE = 10_000;

export function formatMoney(amount: number): string {
  return `$${Math.round(amount).toLocaleString("en-US")}`;
}

/** Days remaining in the current calendar month — the window the $10K gate runs on. */
export function daysLeftInMonth(now: number): number {
  const date = new Date(now);
  const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  return Math.max(0, lastDay - date.getDate());
}

/**
 * A failed file read must never look like $0 collected — a zero here reads as
 * "you earned nothing", which is a different decision than "we cannot see it".
 */
export function cashStrip(input: {
  metrics: CashMetrics | null;
  available: boolean;
  now: number;
}): CashStrip {
  if (!input.available || !input.metrics) {
    return { available: false, text: "metrics unavailable" };
  }

  const collected = input.metrics.totalCollected;
  const weighted = input.metrics.weightedForecast;
  const daysLeft = daysLeftInMonth(input.now);

  return {
    available: true,
    collected,
    weighted,
    gate: CASH_GATE,
    daysLeft,
    text: `Collected ${formatMoney(collected)} / $10K gate · Weighted ${formatMoney(weighted)} · ${daysLeft}d left`,
  };
}
