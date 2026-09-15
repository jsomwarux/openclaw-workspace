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
  test("review admission and JT decision validate distinct least-privilege capabilities", () => {
    expect(tasksSource).toContain("export const createOutreachReview = mutation");
    expect(tasksSource).toContain("export const decideOutreach = mutation");
    expect(tasksSource.match(/capability: v\.string\(\)/g)?.length).toBe(2);
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
    expect(tasksSource.match(/assertDistinctServerCapability\(/g)?.length).toBe(2);
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
