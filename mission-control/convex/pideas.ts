import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

const statusValidator = v.union(
  v.literal("exploring"),
  v.literal("building"),
  v.literal("launched"),
  v.literal("shelved")
);

export const listPideas = query({
  args: {
    status: v.optional(statusValidator),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("pideas")
        .withIndex("by_status", (q) => q.eq("status", args.status!))
        .collect();
    }
    return await ctx.db.query("pideas").collect();
  },
});

export const syncPideas = mutation({
  args: {
    ideas: v.array(
      v.object({
        title: v.string(),
        score: v.number(),
        status: statusValidator,
        source: v.string(),
        reportDate: v.string(),
        concept: v.string(),
        revenueModel: v.string(),
        jtStackFit: v.string(),
        longevitySignal: v.string(),
        researchSignal: v.string(),
        creativityCheck: v.string(),
      })
    ),
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db.query("pideas").collect();
    const existingMap = new Map(existing.map((e) => [e.title, e]));

    let created = 0;
    let updated = 0;
    const now = Date.now();

    for (const idea of args.ideas) {
      const match = existingMap.get(idea.title);
      if (match) {
        await ctx.db.patch(match._id, { ...idea, updatedAt: now });
        updated++;
      } else {
        await ctx.db.insert("pideas", { ...idea, createdAt: now, updatedAt: now });
        created++;
      }
    }

    return { created, updated };
  },
});
