import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("clients").collect();
  },
});

export const getBySlug = query({
  args: { slug: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("clients")
      .withIndex("by_slug", (q) => q.eq("slug", args.slug))
      .first();
  },
});

// Reconcile a client row after JT confirms a real-world status change. This is
// deliberately keyed by stable slug so callers never depend on a stale Convex id.
export const updateBySlug = mutation({
  args: {
    slug: v.string(),
    stage: v.union(
      v.literal("active-delivery"),
      v.literal("blocked"),
      v.literal("pending"),
      v.literal("closed-won"),
      v.literal("archived"),
    ),
    status: v.string(),
    lastTouch: v.number(),
    referralEligible: v.boolean(),
  },
  handler: async (ctx, args) => {
    const client = await ctx.db
      .query("clients")
      .withIndex("by_slug", (q) => q.eq("slug", args.slug))
      .first();
    if (!client) throw new Error(`client not found: ${args.slug}`);
    await ctx.db.patch(client._id, {
      stage: args.stage,
      status: args.status,
      lastTouch: args.lastTouch,
      referralEligible: args.referralEligible,
      updatedAt: Date.now(),
    });
    return { id: client._id, slug: args.slug };
  },
});

/**
 * Seeded from memory/clients/* (status.md / README.md / metrics.md) reconciled
 * with pipeline.jsonl and the canonical state file, 2026-07-28. `name` is the
 * ledger display name so payments link by exact name; `slug`/`memoryPath` keep
 * the on-disk folder. Idempotent: wipes the table first.
 */
const SEED: Array<{
  slug: string;
  name: string;
  emoji: string;
  stage: "active-delivery" | "blocked" | "pending" | "closed-won" | "archived";
  status: string;
  lastTouch: string;
  referralEligible: boolean;
}> = [
  {
    slug: "altmark-group",
    name: "Altmark",
    emoji: "🏢",
    stage: "blocked",
    status: "Rent delinquency remainder $2,250 blocked on Yair inputs; insurance live + paid, DHCR Phase 1 pending.",
    lastTouch: "2026-07-16",
    referralEligible: false, // Yair referral gated until delinquency accepted in writing
  },
  {
    slug: "aya",
    name: "Aya",
    emoji: "🏠",
    stage: "active-delivery",
    status: "Anchor client; dashboard delivered + paid, co-living $2,500 pending approval.",
    lastTouch: "2026-07-02",
    referralEligible: true, // Gil referral ask now eligible
  },
  {
    slug: "karen-vitale",
    name: "SoberLife",
    emoji: "🧠",
    stage: "closed-won",
    status: "SoberLife-Coach Phase 1 delivered + paid; closeout tail (domain, Psychology Today/LinkedIn, content schedule).",
    lastTouch: "2026-07-02",
    referralEligible: false, // JT confirmed 2026-09-09 that Karen is not a property-operator referral source
  },
  {
    slug: "marketsmith",
    name: "MSI",
    emoji: "📊",
    stage: "closed-won",
    status: "Fully paid and closed; MSI-002 cleared, laptop returned, no further engagement active.",
    lastTouch: "2026-09-09",
    referralEligible: false,
  },
];

export const seedInitial = mutation({
  args: {},
  handler: async (ctx) => {
    const existing = await ctx.db.query("clients").collect();
    for (const row of existing) await ctx.db.delete(row._id);

    const now = Date.now();
    let inserted = 0;
    for (const c of SEED) {
      await ctx.db.insert("clients", {
        slug: c.slug,
        name: c.name,
        emoji: c.emoji,
        stage: c.stage,
        status: c.status,
        lastTouch: Date.parse(c.lastTouch),
        memoryPath: `memory/clients/${c.slug}`,
        referralEligible: c.referralEligible,
        createdAt: now,
        updatedAt: now,
      });
      inserted++;
    }
    return { inserted };
  },
});
