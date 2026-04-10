import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    status: v.union(v.literal("todo"), v.literal("in-progress"), v.literal("done"), v.literal("archived")),
    assignee: v.union(v.literal("jt"), v.literal("eve"), v.literal("both")),
    priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
    project: v.optional(v.string()),
    sortOrder: v.optional(v.number()),
    slug: v.optional(v.string()),
    pipelineStage: v.optional(v.string()),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_status", ["status"])
    .index("by_assignee", ["assignee"])
    .index("by_project", ["project"])
    .index("by_slug", ["slug"]),

  pideas: defineTable({
    title: v.string(),
    score: v.number(),
    status: v.union(v.literal("exploring"), v.literal("building"), v.literal("launched"), v.literal("shelved")),
    source: v.string(),
    reportDate: v.string(),
    concept: v.string(),
    revenueModel: v.string(),
    jtStackFit: v.string(),
    longevitySignal: v.string(),
    researchSignal: v.string(),
    creativityCheck: v.string(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_score", ["score"])
    .index("by_status", ["status"]),
});
