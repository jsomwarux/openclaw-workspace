import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const tasksSource = readFileSync(fileURLToPath(new URL("../../convex/tasks.ts", import.meta.url)), "utf8");
const schemaSource = readFileSync(fileURLToPath(new URL("../../convex/schema.ts", import.meta.url)), "utf8");

function mutationSource(name: string, nextName: string): string {
  return tasksSource.slice(
    tasksSource.indexOf(`export const ${name} =`),
    tasksSource.indexOf(`export const ${nextName} =`),
  );
}

describe("Convex outreach authority boundary", () => {
  test("both public outreach mutations require and validate a server capability", () => {
    expect(tasksSource).toContain("export const createOutreachReview = mutation");
    expect(tasksSource).toContain("export const decideOutreach = mutation");
    expect(tasksSource.match(/capability: v\.string\(\)/g)?.length).toBe(2);
    expect(tasksSource.match(/assertServerCapability\(capability, process\.env\.OUTREACH_DECISION_CAPABILITY\)/g)?.length).toBe(2);
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
    expect(mutationSource("autoArchive", "updatePipelineStage")).toContain("if (task.outreachReview) continue;");
  });

  test("backfillClientIds skips outreach review snapshots", () => {
    expect(tasksSource.slice(tasksSource.indexOf("export const backfillClientIds ="))).toContain("!t.outreachReview");
  });
});
