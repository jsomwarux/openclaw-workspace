import { describe, expect, test } from "bun:test";
import { resolveTaskCreateOnly } from "./task-create-only";

describe("atomic create-only task resolution", () => {
  test("creates a task when the dedupe key has no match", () => {
    expect(resolveTaskCreateOnly(null, { title: "New", dedupeKey: "version-1" }, 200)).toEqual({
      operation: "create",
      fields: { title: "New", dedupeKey: "version-1", createdAt: 200, updatedAt: 200 },
    });
  });

  test("returns the existing id without fields that could patch human state", () => {
    expect(resolveTaskCreateOnly(
      { _id: "task-1" },
      { title: "Replacement", dedupeKey: "version-1", status: "todo" },
      200,
    )).toEqual({ operation: "existing", id: "task-1" });
  });
});
