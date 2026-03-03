import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const list = query({
  args: {
    status: v.optional(v.union(v.literal("todo"), v.literal("in-progress"), v.literal("done"))),
    assignee: v.optional(v.union(v.literal("jt"), v.literal("eve"), v.literal("both"))),
  },
  handler: async (ctx, args) => {
    let q = ctx.db.query("tasks");
    if (args.status) {
      return await q.withIndex("by_status", (q) => q.eq("status", args.status!)).collect();
    }
    return await q.order("desc").collect();
  },
});

export const create = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
    status: v.union(v.literal("todo"), v.literal("in-progress"), v.literal("done")),
    assignee: v.union(v.literal("jt"), v.literal("eve"), v.literal("both")),
    priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
    project: v.optional(v.string()),
    sortOrder: v.optional(v.number()),
    slug: v.optional(v.string()),
    pipelineStage: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    return await ctx.db.insert("tasks", { ...args, createdAt: now, updatedAt: now });
  },
});

export const updateStatus = mutation({
  args: {
    id: v.id("tasks"),
    status: v.union(v.literal("todo"), v.literal("in-progress"), v.literal("done")),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, { status: args.status, updatedAt: Date.now() });
  },
});

export const update = mutation({
  args: {
    id: v.id("tasks"),
    title: v.optional(v.string()),
    description: v.optional(v.string()),
    status: v.optional(v.union(v.literal("todo"), v.literal("in-progress"), v.literal("done"))),
    assignee: v.optional(v.union(v.literal("jt"), v.literal("eve"), v.literal("both"))),
    priority: v.optional(v.union(v.literal("high"), v.literal("medium"), v.literal("low")),),
    project: v.optional(v.string()),
    sortOrder: v.optional(v.number()),
    slug: v.optional(v.string()),
    pipelineStage: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const { id, ...fields } = args;
    await ctx.db.patch(id, { ...fields, updatedAt: Date.now() });
  },
});

export const remove = mutation({
  args: { id: v.id("tasks") },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.id);
  },
});

export const findBySlug = query({
  args: { slug: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_slug", (q) => q.eq("slug", args.slug))
      .first();
  },
});

export const updatePipelineStage = mutation({
  args: {
    id: v.id("tasks"),
    pipelineStage: v.string(),
    description: v.optional(v.string()),
    status: v.optional(v.union(v.literal("todo"), v.literal("in-progress"), v.literal("done"))),
  },
  handler: async (ctx, args) => {
    const { id, ...fields } = args;
    await ctx.db.patch(id, { ...fields, updatedAt: Date.now() });
  },
});
