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

export const workstream = v.union(
  v.literal("paid-delivery"),
  v.literal("career-hedge"),
  v.literal("compounding-bet"),
  v.literal("administrative"),
  v.literal("other"),
);

// Collected cash is stored per-payment. pipeline.jsonl zeroes items once paid, so
// it can never be the system of record for collected cash — this table is.
export const paymentKind = v.union(
  v.literal("consulting"),
  v.literal("unemployment"),
  v.literal("other"),
);

// The $10K gate can be read two ways. Store which one, never assume it.
export const gateBasis = v.union(v.literal("monthly"), v.literal("all-time"));

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
    firstAction: v.optional(v.string()),
    whyItMatters: v.optional(v.string()),
    doneState: v.optional(v.string()),
    evidenceLinks: v.optional(v.array(v.string())),
    sourceSystem: v.optional(v.string()),
    reviewAt: v.optional(v.number()),
    dedupeKey: v.optional(v.string()),
    workstream: v.optional(workstream),
    hypothesis: v.optional(v.string()),
    nextTest: v.optional(v.string()),
    killDate: v.optional(v.number()),
    promotionScore: v.optional(v.number()),
    revivalTrigger: v.optional(v.string()),
    verdict: v.optional(v.string()),
    verifierConfirmed: v.optional(v.boolean()),
    verifiedAt: v.optional(v.string()),
    candidateId: v.optional(v.string()),
    sourceHash: v.optional(v.string()),
    evidenceScore: v.optional(v.number()),
    distributionScore: v.optional(v.number()),
    fatalConstraint: v.optional(v.boolean()),
    clientId: v.optional(v.id("clients")),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_status", ["status"])
    .index("by_assignee", ["assignee"])
    .index("by_project", ["project"])
    .index("by_slug", ["slug"])
    .index("by_dedupeKey", ["dedupeKey"])
    .index("by_client", ["clientId"]),

  clients: defineTable({
    slug: v.string(), // matches memory/clients/<slug>
    name: v.string(),
    emoji: v.optional(v.string()),
    stage: v.union(
      v.literal("active-delivery"),
      v.literal("blocked"),
      v.literal("pending"),
      v.literal("closed-won"),
      v.literal("archived"),
    ),
    status: v.optional(v.string()),
    waitingOn: v.optional(waitingOn),
    lastTouch: v.optional(v.number()),
    memoryPath: v.optional(v.string()),
    referralEligible: v.optional(v.boolean()),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_slug", ["slug"])
    .index("by_stage", ["stage"]),

  payments: defineTable({
    clientId: v.optional(v.id("clients")),
    clientName: v.string(), // denormalized so a payment always renders
    amount: v.number(), // USD, positive = money in
    paidOn: v.number(), // epoch ms — the clearance date
    milestone: v.optional(v.string()),
    kind: paymentKind,
    cleared: v.boolean(), // true = cleared, false = invoiced/pending
    source: v.optional(v.string()), // evidence / provenance note
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_client", ["clientId"])
    .index("by_paidOn", ["paidOn"])
    .index("by_kind", ["kind"]),

  focus: defineTable({
    weekOf: v.string(),
    projects: v.array(v.string()),
    gate: v.number(),
    // Which window the gate runs on. Defaults to "monthly" in code when absent.
    gateBasis: v.optional(gateBasis),
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
