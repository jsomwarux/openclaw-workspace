import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { paymentKind } from "./schema";

export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("payments").withIndex("by_paidOn").order("desc").collect();
  },
});

// Task 2: link each payment to its seeded client by exact clientName → clients.name.
// Reports any ledger row whose name does not resolve to a client.
export const linkClients = mutation({
  args: {},
  handler: async (ctx) => {
    const clients = await ctx.db.query("clients").collect();
    const byName = new Map(clients.map((c) => [c.name, c._id]));
    const payments = await ctx.db.query("payments").collect();

    let linked = 0;
    const unmatched: string[] = [];
    for (const p of payments) {
      const clientId = byName.get(p.clientName);
      if (!clientId) {
        unmatched.push(`${p.clientName} · ${p.milestone ?? "?"}`);
        continue;
      }
      await ctx.db.patch(p._id, { clientId, updatedAt: Date.now() });
      linked++;
    }
    return { linked, unmatched };
  },
});

export const create = mutation({
  args: {
    clientId: v.optional(v.id("clients")),
    clientName: v.string(),
    amount: v.number(),
    paidOn: v.number(),
    milestone: v.optional(v.string()),
    kind: paymentKind,
    cleared: v.boolean(),
    source: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    return await ctx.db.insert("payments", { ...args, createdAt: now, updatedAt: now });
  },
});

// The known consulting ledger as reconciled with JT on 2026-07-28. Idempotent:
// wipes the table first so re-running never double-counts. Dates for the four
// pre-July payments are month-inferred (no exact day is logged); the three July
// payments use the confirmation date, so no invented day is presented as known.
const SEED: Array<{
  clientName: string;
  amount: number;
  paidOn: string;
  milestone: string;
  source: string;
}> = [
  { clientName: "Altmark", amount: 4000, paidOn: "2026-05-01", milestone: "Foundation infrastructure", source: "date not logged, month inferred" },
  { clientName: "Altmark", amount: 2250, paidOn: "2026-06-01", milestone: "COI expiration tracking", source: "date not logged, month inferred" },
  { clientName: "Altmark", amount: 2250, paidOn: "2026-06-01", milestone: "Rent delinquency 50%", source: "date not logged, month inferred" },
  { clientName: "Aya", amount: 1500, paidOn: "2026-06-01", milestone: "Dashboard", source: "date not logged, month inferred" },
  { clientName: "Aya", amount: 1000, paidOn: "2026-07-28", milestone: "Dashboard updates", source: "confirmed by JT 2026-07-28" },
  { clientName: "SoberLife", amount: 3000, paidOn: "2026-07-28", milestone: "Phase 1", source: "confirmed by JT 2026-07-28" },
  { clientName: "MSI", amount: 5400, paidOn: "2026-07-28", milestone: "Kickoff 50%", source: "confirmed by JT 2026-07-28" },
];

export const seedInitial = mutation({
  args: {},
  handler: async (ctx) => {
    const existing = await ctx.db.query("payments").collect();
    for (const row of existing) await ctx.db.delete(row._id);

    const now = Date.now();
    let inserted = 0;
    for (const row of SEED) {
      await ctx.db.insert("payments", {
        clientName: row.clientName,
        amount: row.amount,
        paidOn: Date.parse(row.paidOn),
        milestone: row.milestone,
        kind: "consulting",
        cleared: true,
        source: row.source,
        createdAt: now,
        updatedAt: now,
      });
      inserted++;
    }
    return { inserted };
  },
});
