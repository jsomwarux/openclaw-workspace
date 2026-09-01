import { v } from "convex/values";
import { mutation, query, internalMutation } from "./_generated/server";
import type { Doc } from "./_generated/dataModel";
import type { MutationCtx } from "./_generated/server";
import { taskStatus, waitingOn, workstream } from "./schema";
import { resolveTaskUpsert } from "../lib/mission-control/task-upsert";

const auditSource = v.union(v.literal("eve"), v.literal("jt"), v.literal("model"));
const NIGHTLY_SOURCE = "nightly-validation-controller";
const NIGHTLY_PROMOTION_THRESHOLD = 30;
const NIGHTLY_FRESHNESS_MS = 24 * 60 * 60 * 1000;

const operatingSystemArgs = {
  blocks: v.optional(v.number()),
  blocksAgent: v.optional(v.boolean()),
  riskContainment: v.optional(v.boolean()),
  cashDirect: v.optional(v.boolean()),
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
};

function assertNightlyAdmission(args: Record<string, unknown>) {
  if (args.sourceSystem !== NIGHTLY_SOURCE) return;
  for (const field of ["dedupeKey", "firstAction", "whyItMatters", "doneState", "workstream"] as const) {
    if (typeof args[field] !== "string" || !args[field]) throw new Error(`${field} required for nightly admission`);
  }
  if (!Array.isArray(args.evidenceLinks) || args.evidenceLinks.length === 0) {
    throw new Error("evidenceLinks required for nightly admission");
  }
  if (typeof args.promotionScore !== "number" || args.promotionScore < NIGHTLY_PROMOTION_THRESHOLD) {
    throw new Error(`promotionScore must be at least ${NIGHTLY_PROMOTION_THRESHOLD}`);
  }
  if (args.verdict !== "promote") throw new Error("verdict must be promote");
  if (args.verifierConfirmed !== true) throw new Error("verifierConfirmed must be true");
  const verifiedAt = typeof args.verifiedAt === "string" ? Date.parse(args.verifiedAt) : Number.NaN;
  const age = Date.now() - verifiedAt;
  if (!Number.isFinite(verifiedAt) || age < 0 || age > NIGHTLY_FRESHNESS_MS) {
    throw new Error("verifiedAt must be a fresh timestamp within 24 hours");
  }
  for (const field of ["candidateId", "sourceHash"] as const) {
    if (typeof args[field] !== "string" || !args[field]) throw new Error(`${field} required for nightly admission`);
  }
  if (typeof args.evidenceScore !== "number" || args.evidenceScore < 4) throw new Error("evidenceScore must be at least 4");
  if (typeof args.distributionScore !== "number" || args.distributionScore < 3) throw new Error("distributionScore must be at least 3");
  if (args.fatalConstraint !== false) throw new Error("fatalConstraint must be false");
}

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
    ...operatingSystemArgs,
  },
  handler: async (ctx, args) => {
    assertNightlyAdmission(args);
    const now = Date.now();
    return await ctx.db.insert("tasks", { ...args, createdAt: now, updatedAt: now });
  },
});

export const upsertByDedupeKey = mutation({
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
    ...operatingSystemArgs,
    dedupeKey: v.string(),
  },
  handler: async (ctx, args) => {
    assertNightlyAdmission(args);
    const now = Date.now();
    const existing = await ctx.db
      .query("tasks")
      .withIndex("by_dedupeKey", (q) => q.eq("dedupeKey", args.dedupeKey))
      .first();
    const resolved = resolveTaskUpsert(existing, args, now);
    if (resolved.operation === "update") {
      await ctx.db.patch(resolved.id, resolved.fields);
      return { id: resolved.id, created: false };
    }
    const id = await ctx.db.insert("tasks", resolved.fields);
    return { id, created: true };
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
    ...operatingSystemArgs,
    auditSource: v.optional(auditSource),
    auditEvidence: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const { id, auditSource: source, auditEvidence, ...fields } = args;
    const task = await ctx.db.get(id);
    if (!task) throw new Error(`Task not found: ${id}`);
    assertNightlyAdmission({ ...task, ...fields });
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

/**
 * Phase 2a clientId backfill. Reviewed and approved by JT 2026-07-28: the 8
 * high-confidence title-scoped matches plus the "Local-First Voice Ops"
 * expansion (expansion work for a live client counts as client-scoped). The
 * reusable insurance-expiration n8n template and the "similar to Aya" research
 * task are deliberately excluded (reusable IP / reference use, not delivery), as
 * are all 36 description-only mentions (content/prospecting/build-idea/priority
 * context, not client-owed work). Matches by unique title substring so it is
 * reproducible and env-agnostic; idempotent (only patches open tasks).
 */
const CLIENT_BACKFILL: Array<{ match: string; client: string }> = [
  { match: "capture insurance workflow proof-safe evidence", client: "Altmark" },
  { match: "DHCR: collect kickoff inputs", client: "Altmark" },
  { match: "Local-First Voice Ops", client: "Altmark" },
  { match: "send rent delinquency source/export gate", client: "Altmark" },
  { match: "Gate acceptance/access before n8n HTTPS", client: "Altmark" },
  { match: "ask Yair for", client: "Altmark" },
  { match: "Tuesday closeout acceptance/access/payment gate", client: "Altmark" },
  { match: "Gil referral ask eligible", client: "Aya" },
  { match: "MSI: deliver remaining 50%", client: "MSI" },
  { match: "Karen referral ask eligible", client: "SoberLife" },
];

export const backfillClientIds = mutation({
  args: {},
  handler: async (ctx) => {
    const clients = await ctx.db.query("clients").collect();
    const byName = new Map(clients.map((c) => [c.name, c._id]));
    const tasks = await ctx.db.query("tasks").collect();

    const applied: Array<{ match: string; client: string; taskId: string | null; title?: string }> = [];
    for (const rule of CLIENT_BACKFILL) {
      const clientId = byName.get(rule.client);
      const task = tasks.find(
        (t) => t.title.includes(rule.match) && t.status !== "done" && t.status !== "archived",
      );
      if (!clientId || !task) {
        applied.push({ match: rule.match, client: rule.client, taskId: null });
        continue;
      }
      await ctx.db.patch(task._id, { clientId, updatedAt: Date.now() });
      applied.push({ match: rule.match, client: rule.client, taskId: task._id, title: task.title });
    }
    return { applied };
  },
});
