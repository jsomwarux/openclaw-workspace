import { expect, test } from "bun:test";
import { normalizeRecentSearchStartTime } from "./api";

test("clamps shorthand since values older than the recent-search window", () => {
  const now = new Date("2026-06-17T11:27:00.000Z");

  const normalized = normalizeRecentSearchStartTime("14d", now);

  expect(normalized.startTime).toBe("2026-06-10T11:27:00.000Z");
  expect(normalized.clamped).toBe(true);
});

test("clamps ISO since values older than the recent-search window", () => {
  const now = new Date("2026-06-17T11:27:00.000Z");

  const normalized = normalizeRecentSearchStartTime("2026-06-03T11:27:00.000Z", now);

  expect(normalized.startTime).toBe("2026-06-10T11:27:00.000Z");
  expect(normalized.clamped).toBe(true);
});

test("keeps since values inside the recent-search window unchanged", () => {
  const now = new Date("2026-06-17T11:27:00.000Z");

  const normalized = normalizeRecentSearchStartTime("3d", now);

  expect(normalized.startTime).toBe("2026-06-14T11:27:00.000Z");
  expect(normalized.clamped).toBe(false);
});
