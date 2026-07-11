import { v } from "convex/values";
import { mutation, query, internalMutation } from "./_generated/server";
import type { Doc } from "./_generated/dataModel";
import type { MutationCtx } from "./_generated/server";
import { taskStatus, waitingOn } from "./schema";

const auditSource = v.union(v.literal("eve"), v.literal("jt"), v.literal("model"));

// Fields whose changes must leave an audit trail.
const AUDITED_FIELDS = ["dollars", "dueDate", "waitingOn", "stageProbability", "priority"] as const;
type AuditedField = (typeof AUDITED_FIELDS)[number];

function serialize(value: unknown): string {
  if (value === undefined) return "";
  if (typeof value === "string") return value;
  return JSON.stringify(value);
}

async function auditChanges(
  ctx: MutationCtx,
  task: Doc<"tasks">,
  fields: Record<string, unknown>,
  source: "eve" | "jt" | "model",
  evidence: string,
) {
  const ts = Date.now();
  for (const field of AUDITED_FIELDS) {
    if (!(field in fields)) continue;
    const oldValue = serialize(task[field as AuditedField]);
    const newValue = serialize(fields[field]);
    if (oldValue === newValue) continue;
    await ctx.db.insert("priorityAudit", {
      taskId: task._id,
      field,
      oldValue,
      newValue,
      evidence,
      source,
      ts,
    });
  }
}

export const list = query({
  args: {
    status: v.optional(taskStatus),
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
    status: taskStatus,
    assignee: v.union(v.literal("jt"), v.literal("eve"), v.literal("both")),
    priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
    project: v.optional(v.string()),
    sortOrder: v.optional(v.number()),
    slug: v.optional(v.string()),
    pipelineStage: v.optional(v.string()),
    dueDate: v.optional(v.number()),
    dueDateSource: v.optional(v.union(v.literal("external"), v.literal("self"))),
    dollars: v.optional(v.number()),
    stageProbability: v.optional(v.number()),
    effortMinutes: v.optional(v.number()),
    lane: v.optional(v.string()),
    waitingOn: v.optional(waitingOn),
    snoozedUntil: v.optional(v.number()),
    proofRequired: v.optional(v.boolean()),
    reasonCodes: v.optional(v.array(v.string())),
    rankScore: v.optional(v.number()),
    rankUpdatedAt: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    return await ctx.db.insert("tasks", { ...args, createdAt: now, updatedAt: now });
  },
});

export const updateStatus = mutation({
  args: {
    id: v.id("tasks"),
    status: taskStatus,
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
    status: v.optional(taskStatus),
    assignee: v.optional(v.union(v.literal("jt"), v.literal("eve"), v.literal("both"))),
    priority: v.optional(v.union(v.literal("high"), v.literal("medium"), v.literal("low"))),
    project: v.optional(v.string()),
    sortOrder: v.optional(v.number()),
    slug: v.optional(v.string()),
    pipelineStage: v.optional(v.string()),
    dueDate: v.optional(v.number()),
    dueDateSource: v.optional(v.union(v.literal("external"), v.literal("self"))),
    dollars: v.optional(v.number()),
    stageProbability: v.optional(v.number()),
    effortMinutes: v.optional(v.number()),
    lane: v.optional(v.string()),
    waitingOn: v.optional(waitingOn),
    snoozedUntil: v.optional(v.number()),
    proofRequired: v.optional(v.boolean()),
    reasonCodes: v.optional(v.array(v.string())),
    rankScore: v.optional(v.number()),
    rankUpdatedAt: v.optional(v.number()),
    auditSource: v.optional(auditSource),
    auditEvidence: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const { id, auditSource: source, auditEvidence, ...fields } = args;
    const task = await ctx.db.get(id);
    if (!task) throw new Error(`Task not found: ${id}`);
    await auditChanges(ctx, task, fields, source ?? "jt", auditEvidence ?? "manual edit");
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

// Returns only non-archived tasks
export const listActive = query({
  args: {},
  handler: async (ctx) => {
    const all = await ctx.db.query("tasks").order("desc").collect();
    return all.filter((t) => t.status !== "archived");
  },
});

// Returns only archived tasks
export const listArchived = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_status", (q) => q.eq("status", "archived"))
      .order("desc")
      .collect();
  },
});

// Auto-archive: moves done tasks older than 7 days to archived
export const autoArchive = internalMutation({
  args: {},
  handler: async (ctx) => {
    const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const doneTasks = await ctx.db
      .query("tasks")
      .withIndex("by_status", (q) => q.eq("status", "done"))
      .collect();
    let archived = 0;
    for (const task of doneTasks) {
      if (task.updatedAt < sevenDaysAgo) {
        await ctx.db.patch(task._id, { status: "archived", updatedAt: Date.now() });
        archived++;
      }
    }
    return { archived };
  },
});

export const updatePipelineStage = mutation({
  args: {
    id: v.id("tasks"),
    pipelineStage: v.string(),
    description: v.optional(v.string()),
    status: v.optional(taskStatus),
  },
  handler: async (ctx, args) => {
    const { id, ...fields } = args;
    await ctx.db.patch(id, { ...fields, updatedAt: Date.now() });
  },
});

export const setFocus = mutation({
  args: {
    weekOf: v.string(),
    projects: v.array(v.string()),
    gate: v.number(),
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("focus")
      .withIndex("by_weekOf", (q) => q.eq("weekOf", args.weekOf))
      .first();
    if (existing) {
      await ctx.db.patch(existing._id, { projects: args.projects, gate: args.gate });
      return existing._id;
    }
    return await ctx.db.insert("focus", { ...args, createdAt: Date.now() });
  },
});

export const getFocus = query({
  args: { weekOf: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("focus")
      .withIndex("by_weekOf", (q) => q.eq("weekOf", args.weekOf))
      .first();
  },
});

export const logAudit = mutation({
  args: {
    taskId: v.string(),
    field: v.string(),
    oldValue: v.string(),
    newValue: v.string(),
    evidence: v.optional(v.string()),
    source: v.optional(auditSource),
  },
  handler: async (ctx, args) => {
    return await ctx.db.insert("priorityAudit", {
      taskId: args.taskId,
      field: args.field,
      oldValue: args.oldValue,
      newValue: args.newValue,
      evidence: args.evidence ?? "manual edit",
      source: args.source ?? "jt",
      ts: Date.now(),
    });
  },
});

export const listAudit = query({
  args: { taskId: v.optional(v.string()) },
  handler: async (ctx, args) => {
    if (args.taskId) {
      return await ctx.db
        .query("priorityAudit")
        .withIndex("by_taskId", (q) => q.eq("taskId", args.taskId!))
        .collect();
    }
    return await ctx.db.query("priorityAudit").withIndex("by_ts").order("desc").take(100);
  },
});
