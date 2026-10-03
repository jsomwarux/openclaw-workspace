// Development-only scenarios for screenshots and manual checks. Loaded only when
// NEXT_PUBLIC_COCKPIT_FIXTURES=1 and the URL carries ?fixture=<scenario>. Everything runs
// against the in-memory FixtureApi: no request reaches /api/tasks or Convex.
import type { CockpitController } from "../controller";
import { isEligible } from "../eligibility";
import { recordOutcome, snapshotEntry, startRun } from "../run";
import { memoryStorage, runStorage } from "../storage";
import type { RunStorage } from "../storage";
import { localDateKey } from "../format";
import { FIXTURE_NOW, ID, allFixtureTasks } from "./data";
import { FixtureApi } from "./fixture-api";
import type { RawTask } from "../types";

const MINUTE = 60_000;
const HOUR = 60 * MINUTE;

export const SCENARIOS = [
  "first-load", "active", "q-card", "p-card", "item", "empty", "stale", "degraded", "failed", "changed",
  "invalid", "expired", "summary", "resume", "loading",
] as const;
export type Scenario = (typeof SCENARIOS)[number];

export interface FixtureSession {
  api: FixtureApi;
  clock: () => number;
  storage: RunStorage;
  prepare: (controller: CockpitController) => Promise<void>;
}

/** The prototype's run: items 1 to 5 handled the way the design shows, item 6 (F04) open. */
async function playToItemSix(controller: CockpitController) {
  controller.startRun();
  await controller.act({ action: "saveAnswer", text: "Keep the proposed answer. It matches what the client asked for." });
  await controller.act({ action: "complete" });
  await controller.next();
  await controller.act({ action: "approve", note: "Approved as recommended." });
  await controller.next();
  await controller.act({ action: "saveAnswer", text: "Ship the draft as written." });
  await controller.act({ action: "complete" });
  await controller.next();
  await controller.act({ action: "block", park: { who: "neutral.......", what: "words value content context follow the step..", nudgeAfterDays: 14 } });
  await controller.next();
  await controller.act({ action: "complete" });
  await controller.next();
  controller.clearNotice();
}

const invalidCard: RawTask = {
  _id: "fx-invalid-card", title: "", status: "blocked", assignee: "jt", priority: "high", sortOrder: 13,
  createdAt: FIXTURE_NOW - 3 * HOUR, updatedAt: FIXTURE_NOW - 3 * HOUR,
};

export function fixtureSession(scenario: string, timeZone: string): FixtureSession {
  const started = Date.now();
  let offset = 0;
  const clock = () => FIXTURE_NOW + (Date.now() - started) + offset;
  const advance = (ms: number) => { offset += ms; };
  const backing = memoryStorage();
  const storage = runStorage(backing, "mission-control:cockpit-fixture-run");
  let tasks = allFixtureTasks();
  if (scenario === "empty") tasks = tasks.filter((task) => !isEligible(task, FIXTURE_NOW));
  if (scenario === "invalid") tasks = [...tasks, invalidCard];
  const api = new FixtureApi(tasks, clock);

  if (scenario === "loading") api.readDelayMs = 24 * HOUR;

  if (scenario === "expired") {
    // A run committed 49 hours earlier, when F06 had not expired yet; F06 is item 6.
    const early = startRun(tasks, FIXTURE_NOW - 49 * HOUR, timeZone);
    let run = { ...early, localDate: localDateKey(FIXTURE_NOW, timeZone) };
    run = { ...run, items: run.items.map((item, i) => (i === 5 ? { id: ID.F06 } : item)), snapshot: run.snapshot.map((entry, i) => (i === 5 ? snapshotEntry(tasks.find((task) => task._id === ID.F06)!) : entry)) };
    for (let i = 0; i < 5; i += 1) run = recordOutcome(run, run.items[i].id, { outcome: "completed", did: "Completed." });
    storage.save({ ...run, cursor: 5, pausedAt: FIXTURE_NOW - 3 * HOUR });
  }

  if (scenario === "resume") {
    // Started three hours ago, before F08 existed; F05 was edited while away.
    const early = startRun(tasks.filter((task) => task._id !== ID.F08), FIXTURE_NOW - 3 * HOUR, timeZone);
    let run = { ...early, localDate: localDateKey(FIXTURE_NOW, timeZone) };
    for (let i = 0; i < 5; i += 1) run = recordOutcome(run, run.items[i].id, { outcome: "completed", did: "Completed." });
    storage.save({ ...run, cursor: 5, phase: "paused", pausedAt: FIXTURE_NOW - 3 * HOUR });
    api.edit(ID.F05, { payloadHash: "f".repeat(64), updatedAt: FIXTURE_NOW - 2 * HOUR });
  }

  const prepare = async (controller: CockpitController) => {
    switch (scenario) {
      case "active":
      case "item":
      case "failed":
        await playToItemSix(controller);
        if (scenario === "failed") api.failNext("network");
        return;
      case "q-card":
        controller.startRun();
        return;
      case "p-card":
        controller.startRun();
        await controller.next();
        return;
      case "stale":
        await playToItemSix(controller);
        api.failReads(1_000_000);
        advance(38 * MINUTE);
        await controller.refresh();
        return;
      case "degraded":
        await playToItemSix(controller);
        api.failReads(1_000_000);
        await controller.refresh();
        await controller.refresh();
        return;
      case "changed":
        await playToItemSix(controller);
        advance(MINUTE);
        api.edit(ID.F04, { doneState: "The agent session shows the prompt pasted and the reply saved to the project folder." });
        await controller.refresh();
        return;
      case "invalid":
        controller.startRun();
        for (let i = 0; i < 6; i += 1) await controller.next();
        controller.clearNotice();
        return;
      case "expired":
        await controller.acknowledgeAndResume();
        return;
      case "summary":
        await playToItemSix(controller);
        await controller.act({ action: "complete" });
        await controller.next();
        await controller.next();
        return;
      default:
        return;
    }
  };

  return { api, clock, storage, prepare };
}
