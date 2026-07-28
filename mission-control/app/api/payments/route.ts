/**
 * Read-only HTTP API for the collected-cash ledger. This is the system of record
 * for collected consulting cash — the cockpit reads it here, never from
 * pipeline.jsonl (which zeroes items once paid).
 *
 * GET /api/payments → { payments, metrics }
 */
import { NextResponse } from "next/server";
import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";
import { computeCollected, DEFAULT_GATE_AMOUNT, type Payment } from "@/lib/mission-control/collected";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export const dynamic = "force-dynamic";

export async function GET() {
  const rows = await convex.query(api.payments.list, {});
  const payments: Payment[] = rows.map((row) => ({
    clientName: row.clientName,
    amount: row.amount,
    paidOn: row.paidOn,
    milestone: row.milestone,
    kind: row.kind,
    cleared: row.cleared,
    source: row.source,
  }));

  const metrics = computeCollected(payments, {
    now: Date.now(),
    gateAmount: DEFAULT_GATE_AMOUNT,
    gateBasis: "monthly",
  });

  return NextResponse.json({ payments: rows, metrics });
}
