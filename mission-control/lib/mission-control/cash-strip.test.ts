import { describe, expect, test } from "bun:test";
import { cashStrip, daysLeftInMonth } from "./cash-strip";

const JULY_11 = new Date(2026, 6, 11, 12).getTime();

describe("cash strip", () => {
  test("renders collected, gate, weighted, and days left on one line", () => {
    const strip = cashStrip({
      metrics: { totalCollected: 3375, weightedForecast: 5200 },
      available: true,
      now: JULY_11,
    });

    expect(strip.available).toBe(true);
    expect(strip.text).toBe("Collected $3,375 / $10K gate · Weighted $5,200 · 20d left");
  });

  test("says metrics unavailable instead of showing a false $0 when the read fails", () => {
    const strip = cashStrip({ metrics: null, available: false, now: JULY_11 });

    expect(strip.available).toBe(false);
    expect(strip.text).toBe("metrics unavailable");
  });

  test("an unavailable source never renders parsed zeros as real cash", () => {
    const strip = cashStrip({
      metrics: { totalCollected: 0, weightedForecast: 0 },
      available: false,
      now: JULY_11,
    });

    expect(strip.text).toBe("metrics unavailable");
  });

  test("counts days remaining in the gate month", () => {
    expect(daysLeftInMonth(new Date(2026, 6, 31, 12).getTime())).toBe(0);
    expect(daysLeftInMonth(new Date(2026, 1, 20, 12).getTime())).toBe(8);
  });
});
