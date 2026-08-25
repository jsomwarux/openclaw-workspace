import { describe, expect, test } from "bun:test";
import { resolveTaskUpsert } from "./task-upsert";

describe("deduplicated task upsert", () => {
  test("creates when the dedupe key has no match", () => {
    expect(resolveTaskUpsert(null, { title: "New", dedupeKey: "k" }, 200)).toEqual({
      operation: "create",
      fields: { title: "New", dedupeKey: "k", createdAt: 200, updatedAt: 200 },
    });
  });

  test("updates the existing task without replacing its identity or creation time", () => {
    expect(resolveTaskUpsert({ _id: "task-1", createdAt: 100, updatedAt: 100 }, { title: "Updated", dedupeKey: "k" }, 200)).toEqual({
      operation: "update",
      id: "task-1",
      fields: { title: "Updated", dedupeKey: "k", updatedAt: 200 },
    });
  });
});
