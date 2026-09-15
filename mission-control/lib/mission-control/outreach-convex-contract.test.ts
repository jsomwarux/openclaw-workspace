import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const tasksSource = readFileSync(fileURLToPath(new URL("../../convex/tasks.ts", import.meta.url)), "utf8");
const schemaSource = readFileSync(fileURLToPath(new URL("../../convex/schema.ts", import.meta.url)), "utf8");

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
});
