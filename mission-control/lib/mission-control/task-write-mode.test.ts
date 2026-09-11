import { describe, expect, test } from "bun:test";
import { resolveTaskWriteMode } from "./task-write-mode";

describe("task POST write-mode selection", () => {
  test("explicit create-only with a dedupe key selects atomic create-only", () => {
    expect(resolveTaskWriteMode("create-only", true)).toBe("create-only");
  });

  test("normal keyed POST remains the existing upsert", () => {
    expect(resolveTaskWriteMode(null, true)).toBe("upsert");
  });

  test("normal unkeyed POST remains create", () => {
    expect(resolveTaskWriteMode(null, false)).toBe("create");
  });

  test("create-only without a dedupe key fails closed", () => {
    let message = "";
    try { resolveTaskWriteMode("create-only", false); } catch (error) {
      message = error instanceof Error ? error.message : String(error);
    }
    expect(message).toContain("dedupeKey required");
  });

  test("unknown modes fail closed instead of changing normal behavior", () => {
    let message = "";
    try { resolveTaskWriteMode("replace", true); } catch (error) {
      message = error instanceof Error ? error.message : String(error);
    }
    expect(message).toContain("unsupported task write mode");
  });
});
