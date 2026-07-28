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
    referralEligible: true, // Karen referral ask now eligible
  },
  {
    slug: "marketsmith",
    name: "MSI",
    emoji: "📊",
    stage: "active-delivery",
    status: "Signed 80-hr Nexus engagement $10,800; kickoff 50% collected, remaining 50% in delivery.",
    lastTouch: "2026-07-17",
    referralEligible: false, // mid-delivery, no referral gate cleared
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
