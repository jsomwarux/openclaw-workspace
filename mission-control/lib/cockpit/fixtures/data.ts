// The design bundle's twelve fixture records (source/02-fixtures.json), shaped exactly like
// GET /api/tasks rows. Used by tests and the development fixture harness only.
import fixtures from "@/docs/design/mission-control-redesign/source/02-fixtures.json";
import type { RawTask } from "../types";

export const FIXTURE_NOW: number = fixtures._meta.fixtureNow;

export type FixtureId = "F01" | "F02" | "F03" | "F04" | "F05" | "F06" | "F07" | "F08" | "F09" | "F10" | "F11" | "F12";

/** A fresh deep copy of one fixture task, so tests can edit it freely. */
export function fx(id: FixtureId): RawTask {
  const found = fixtures.fixtures.find((entry) => entry.fixtureId === id);
  if (!found) throw new Error(`unknown fixture ${id}`);
  return structuredClone(found.task) as RawTask;
}

export function allFixtureTasks(): RawTask[] {
  return fixtures.fixtures.map((entry) => structuredClone(entry.task) as RawTask);
}

export function fixtureIdOf(task: RawTask): FixtureId | null {
  const found = fixtures.fixtures.find((entry) => entry.task._id === task._id);
  return found ? (found.fixtureId as FixtureId) : null;
}

export const ID = Object.fromEntries(
  fixtures.fixtures.map((entry) => [entry.fixtureId, entry.task._id]),
) as Record<FixtureId, string>;
