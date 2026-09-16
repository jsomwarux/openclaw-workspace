import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const tasksSource = readFileSync(fileURLToPath(new URL("../../convex/tasks.ts", import.meta.url)), "utf8");
const schemaSource = readFileSync(fileURLToPath(new URL("../../convex/schema.ts", import.meta.url)), "utf8");
const reviewRouteSource = readFileSync(fileURLToPath(new URL("../../app/api/tasks/outreach-review/route.ts", import.meta.url)), "utf8");
const decisionRouteSource = readFileSync(fileURLToPath(new URL("../../app/api/tasks/outreach-decision/route.ts", import.meta.url)), "utf8");

function mutationSource(name: string, nextName: string): string {
  return tasksSource.slice(
    tasksSource.indexOf(`export const ${name} =`),
    tasksSource.indexOf(`export const ${nextName} =`),
  );
}

describe("Convex outreach authority boundary", () => {
  test("defines an append-only exact-key authority table with the domain record and no capability", () => {
    expect(schemaSource).toContain("outreachReviewAuthorities: defineTable({");
    for (const field of [
      "candidateId", "draftSha256", "authorityBundleHash", "verifierReportSha256", "verifierGitBinding",
      "builderActorId", "drafterActorId", "verifierActorId", "reviewId", "observedAt", "authorityRevision",
    ]) expect(schemaSource).toContain(`${field}:`);
    expect(schemaSource).toContain(
      '.index("by_exact_authority", ["candidateId", "draftSha256", "authorityBundleHash", "verifierReportSha256"])',
    );
    expect(schemaSource).not.toContain("outreachReviewAuthorities: defineTable({\n    capability:");
  });

  test("exports specialized append-only authority write and exact lookup handlers", () => {
    const write = mutationSource("createOutreachReviewAuthority", "findOutreachReviewAuthority");
    const lookup = mutationSource("findOutreachReviewAuthority", "createOutreachReview");
    expect(write).toContain("export const createOutreachReviewAuthority = mutation");
    expect(lookup).toContain("export const findOutreachReviewAuthority = query");
    expect(write).toContain('ctx.db.insert("outreachReviewAuthorities"');
    expect(write).not.toContain("ctx.db.patch");
    expect(write).not.toContain("ctx.db.delete");
    expect(lookup).not.toContain("ctx.db.patch");
    expect(lookup).not.toContain("ctx.db.delete");
  });

  test("authority handlers authenticate four distinct capabilities before database access", () => {
    for (const [name, next] of [
      ["createOutreachReviewAuthority", "findOutreachReviewAuthority"],
      ["findOutreachReviewAuthority", "createOutreachReview"],
    ] as const) {
      const source = mutationSource(name, next);
      for (const capability of [
        "OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY",
        "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY",
        "OUTREACH_REVIEW_CAPABILITY",
        "OUTREACH_DECISION_CAPABILITY",
      ]) expect(source).toContain(`process.env.${capability}`);
      expect(source.indexOf("await assertOutreachAuthorityCapability")).toBeGreaterThan(-1);
      expect(source.indexOf("await assertOutreachAuthorityCapability")).toBeLessThan(source.indexOf("ctx.db"));
    }
  });

  test("review admission and JT decision validate distinct least-privilege capabilities", () => {
    expect(tasksSource).toContain("export const createOutreachReview = mutation");
    expect(tasksSource).toContain("export const decideOutreach = mutation");
    expect(tasksSource.match(/capability: v\.string\(\)/g)?.length).toBe(6);
    const reviewMutation = mutationSource("createOutreachReview", "updateStatus");
    const decisionMutation = mutationSource("decideOutreach", "findOutreachDecision");
    expect(reviewMutation).toContain("process.env.OUTREACH_REVIEW_CAPABILITY");
    expect(reviewMutation).toContain("process.env.OUTREACH_DECISION_CAPABILITY");
    expect(decisionMutation).toContain("process.env.OUTREACH_DECISION_CAPABILITY");
    expect(decisionMutation).toContain("process.env.OUTREACH_REVIEW_CAPABILITY");
    expect(reviewRouteSource).toContain("process.env.OUTREACH_REVIEW_CAPABILITY");
    expect(reviewRouteSource).toContain("process.env.OUTREACH_DECISION_CAPABILITY");
    expect(decisionRouteSource).toContain("process.env.OUTREACH_DECISION_CAPABILITY");
    expect(decisionRouteSource).toContain("process.env.OUTREACH_REVIEW_CAPABILITY");
    expect(tasksSource.match(/assertDistinctServerCapability\(/g)?.length).toBe(4);
  });

  test("persists the complete typed snapshot and indexes candidate plus cohort", () => {
    for (const field of [
      "cohortId", "subject", "body", "verifierReport", "reviewAuthorityId", "verifierActorId",
      "gitBindings", "snapshotSha256", "reviewCycle",
    ]) expect(schemaSource).toContain(`${field}:`);
    expect(schemaSource).toContain('.index("by_outreach_candidate_cohort", ["candidateId", "cohortId"])');
    const reviewMutation = mutationSource("createOutreachReview", "getOutreachReviewState");
    expect(reviewMutation).toContain('withIndex("by_outreach_candidate_cohort"');
    expect(reviewMutation).toContain("resolveOutreachReviewAdmission");
    expect(reviewMutation).toContain("taskId:");
    expect(reviewMutation).toContain("reviewCycle:");
    expect(reviewMutation).toContain("snapshotSha256:");
  });

  test("review count and decision lookup authenticate before database access", () => {
    for (const [name, next] of [
      ["getOutreachReviewState", "updateStatus"],
      ["findOutreachDecision", "findBySlug"],
    ] as const) {
      const source = mutationSource(name, next);
      expect(source.indexOf("await assertDistinctServerCapability")).toBeGreaterThan(-1);
      expect(source.indexOf("await assertDistinctServerCapability")).toBeLessThan(source.indexOf("ctx.db"));
    }
  });

  test("stores the server review marker but never stores the capability", () => {
    expect(schemaSource).toContain("outreachReview: v.optional(outreachReview)");
    expect(schemaSource).not.toContain("capability: v.");
  });

  for (const [name, nextName] of [
    ["updateStatus", "update"],
    ["update", "remove"],
    ["remove", "decideOutreach"],
    ["updatePipelineStage", "setFocus"],
  ] as const) {
    test(`${name} loads the task and freezes outreach review snapshots`, () => {
      const source = mutationSource(name, nextName);
      expect(source).toContain("const task = await ctx.db.get");
      expect(source).toContain("assertOutreachTaskMutable(task);");
    });
  }

  test("autoArchive skips outreach review snapshots", () => {
    expect(mutationSource("autoArchive", "updatePipelineStage")).toContain("if (task.outreachReview || task.outreachDecision) continue;");
  });

  test("backfillClientIds skips outreach review snapshots", () => {
    const source = tasksSource.slice(tasksSource.indexOf("export const backfillClientIds ="));
    expect(source).toContain("!t.outreachReview");
    expect(source).toContain("!t.outreachDecision");
  });
});
