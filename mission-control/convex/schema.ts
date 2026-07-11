import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export const taskStatus = v.union(
  v.literal("todo"),
  v.literal("in-progress"),
  v.literal("done"),
  v.literal("archived"),
  v.literal("waiting-external"),
  v.literal("snoozed"),
);

export const waitingOn = v.object({
  who: v.string(),
  what: v.string(),
  since: v.number(),
  nudgeAfterDays: v.number(),
});

export default defineSchema({
  tasks: defineTable({
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
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_status", ["status"])
    .index("by_assignee", ["assignee"])
    .index("by_project", ["project"])
    .index("by_slug", ["slug"]),

  focus: defineTable({
    weekOf: v.string(),
    projects: v.array(v.string()),
    gate: v.number(),
    createdAt: v.number(),
  }).index("by_weekOf", ["weekOf"]),

  priorityAudit: defineTable({
    taskId: v.string(),
    field: v.string(),
    oldValue: v.string(),
    newValue: v.string(),
    evidence: v.string(),
    source: v.union(v.literal("eve"), v.literal("jt"), v.literal("model")),
    ts: v.number(),
  })
    .index("by_taskId", ["taskId"])
    .index("by_ts", ["ts"]),

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
