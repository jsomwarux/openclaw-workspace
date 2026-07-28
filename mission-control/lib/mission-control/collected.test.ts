import { describe, expect, test } from "bun:test";
import { computeCollected, type Payment } from "./collected";

const ms = (iso: string) => Date.parse(iso);
const NOW = ms("2026-07-28");

// The reconciled ledger confirmed with JT on 2026-07-28. All consulting, cleared.
const LEDGER: Payment[] = [
  { clientName: "Altmark", amount: 4000, paidOn: ms("2026-05-01"), milestone: "Foundation infrastructure", kind: "consulting", cleared: true },
  { clientName: "Altmark", amount: 2250, paidOn: ms("2026-06-01"), milestone: "COI expiration tracking", kind: "consulting", cleared: true },
  { clientName: "Altmark", amount: 2250, paidOn: ms("2026-06-01"), milestone: "Rent delinquency 50%", kind: "consulting", cleared: true },
  { clientName: "Aya", amount: 1500, paidOn: ms("2026-06-01"), milestone: "Dashboard", kind: "consulting", cleared: true },
  { clientName: "Aya", amount: 1000, paidOn: ms("2026-07-28"), milestone: "Dashboard updates", kind: "consulting", cleared: true },
  { clientName: "SoberLife", amount: 3000, paidOn: ms("2026-07-28"), milestone: "Phase 1", kind: "consulting", cleared: true },
  { clientName: "MSI", amount: 5400, paidOn: ms("2026-07-28"), milestone: "Kickoff 50%", kind: "consulting", cleared: true },
];

describe("computeCollected", () => {
  test("July MTD consulting collected is $9,400 with a $600 gap to the $10K gate", () => {
    const m = computeCollected(LEDGER, { now: NOW });
    expect(m.gateBasis).toBe("monthly");
    expect(m.consultingMonth).toBe(9400);
    expect(m.gateCollected).toBe(9400);
    expect(m.gapToGate).toBe(600);
  });

  test("all-time consulting collected is $19,400", () => {
    const m = computeCollected(LEDGER, { now: NOW });
    expect(m.consultingAllTime).toBe(19400);
    expect(m.totalAllTime).toBe(19400); // no unemployment in the ledger
  });

  test("all-time basis counts the full ledger against the gate", () => {
    const m = computeCollected(LEDGER, { now: NOW, gateBasis: "all-time" });
    expect(m.gateCollected).toBe(19400);
    expect(m.gapToGate).toBe(-9400);
  });

  test("pending (uncleared) payments never count as collected", () => {
    const withPending: Payment[] = [
      ...LEDGER,
      { clientName: "MSI", amount: 5400, paidOn: ms("2026-07-28"), milestone: "Completion 50%", kind: "consulting", cleared: false },
    ];
    const m = computeCollected(withPending, { now: NOW });
    expect(m.consultingMonth).toBe(9400);
  });

  test("unemployment is tracked separately from consulting", () => {
    const withUi: Payment[] = [
      ...LEDGER,
      { clientName: "NYSDOL", amount: 2200, paidOn: ms("2026-07-10"), kind: "unemployment", cleared: true },
    ];
    const m = computeCollected(withUi, { now: NOW });
    expect(m.consultingMonth).toBe(9400); // unchanged
    expect(m.unemploymentMonth).toBe(2200);
    expect(m.totalMonth).toBe(11600);
    expect(m.gateCollected).toBe(9400); // gate is consulting-only
  });
});
