import { describe, expect, test } from "bun:test";
import { CockpitController } from "./controller";
import { FixtureApi } from "./fixtures/fixture-api";
import { FIXTURE_NOW, ID, allFixtureTasks } from "./fixtures/data";
import { memoryStorage, runStorage } from "./storage";
import { isEligible } from "./eligibility";
import { startRun, pause } from "./run";
import type { RawTask } from "./types";

const MINUTE = 60_000;
const DAY = 86_400_000;

function setup(tasks: RawTask[] = allFixtureTasks(), storage = memoryStorage()) {
  let now = FIXTURE_NOW;
  const clock = { now: () => now, advance: (ms: number) => { now += ms; } };
  const api = new FixtureApi(tasks, clock.now);
  const controller = new CockpitController({ api, clock: clock.now, storage: runStorage(storage, "test"), timeZone: "UTC" });
  return { api, controller, clock, storage };
}

async function startedAt(position: number, tasks?: RawTask[]) {
  const ctx = setup(tasks);
  await ctx.controller.load();
  ctx.controller.startRun();
  for (let i = 0; i < position; i += 1) await ctx.controller.next();
  return ctx;
}

const current = (controller: CockpitController) => controller.getState().run!.items[controller.getState().run!.cursor];

describe("entry screens", () => {
  test("first load with no run today shows Run start; nothing eligible shows the empty run", async () => {
    const { controller } = setup();
    await controller.load();
    expect(controller.getState().screen).toBe("runStart");
    const empty = setup(allFixtureTasks().filter((task) => !isEligible(task, FIXTURE_NOW)));
    await empty.controller.load();
    expect(empty.controller.getState().screen).toBe("emptyRun");
  });

  test("Start run commits the run, opens item 1 and saves progress under today's date", async () => {
    const { controller, storage } = setup();
    await controller.load();
    controller.startRun();
    const state = controller.getState();
    expect(state.screen).toBe("item");
    expect(current(controller).id).toBe(ID.F01);
    expect(storage.getItem("test:2026-10-03")).toContain(ID.F01);
  });

  test("coming back mid-run goes to Resume, never straight to an item", async () => {
    const first = await startedAt(2);
    const again = new CockpitController({ api: first.api, clock: first.clock.now, storage: runStorage(first.storage, "test"), timeZone: "UTC" });
    await again.load();
    expect(again.getState().screen).toBe("runResume");
    expect(again.getState().changes).toEqual([]);
    await again.acknowledgeAndResume();
    expect(again.getState().screen).toBe("item");
    expect(current(again).id).toBe(ID.F03);
  });

  test("an unfinished run from an earlier day shows its summary first, then today's start", async () => {
    const storage = memoryStorage();
    const runs = runStorage(storage, "test");
    runs.save(pause(startRun(allFixtureTasks(), FIXTURE_NOW - DAY, "UTC"), FIXTURE_NOW - DAY + MINUTE));
    const { controller } = setup(allFixtureTasks(), storage);
    await controller.load();
    expect(controller.getState().screen).toBe("rolloverSummary");
    expect(controller.getState().rollover).toMatchObject({ localDate: "2026-10-02", unfinished: true });
    controller.dismissRollover();
    expect(controller.getState().screen).toBe("runStart");
    expect(runs.load("2026-10-02")?.closedAt).toBe(FIXTURE_NOW);
  });
});

describe("Q and AP: answer, then Complete (DECISIONS 5.1)", () => {
  test("Complete is refused until an answer is saved; Save answer appends feedback; then Complete marks it done", async () => {
    const { controller, api } = await startedAt(0);
    await controller.act({ action: "complete" });
    expect(api.writes).toEqual([]);
    await controller.act({ action: "saveAnswer", text: "Go with the second option." });
    expect(api.task(ID.F01).feedback?.map((entry) => entry.body)).toEqual(["Answer: Go with the second option."]);
    expect(current(controller).outcome).toBe(undefined);
    await controller.act({ action: "complete" });
    expect(api.task(ID.F01).status).toBe("done");
    expect(current(controller)).toMatchObject({ outcome: "completed", did: "Answer recorded, then completed.", line: "Marked done. Press J for the next item." });
  });
});

describe("P: Approve and Reject (DECISIONS 5.2)", () => {
  test("Approve appends one decision entry with the note, then marks done; no Undo", async () => {
    const { controller, api } = await startedAt(1);
    await controller.act({ action: "approve", note: "Ship it as written." });
    expect(api.task(ID.F02).feedback?.map((entry) => entry.body)).toEqual(["Decision: Approved. Ship it as written."]);
    expect(api.task(ID.F02).status).toBe("done");
    expect(current(controller)).toMatchObject({ outcome: "approved", did: "Approved. Note recorded." });
    expect(current(controller).undo).toBe(undefined);
  });

  test("Reject without a note records the decision alone", async () => {
    const { controller, api } = await startedAt(1);
    await controller.act({ action: "reject", note: "" });
    expect(api.task(ID.F02).feedback?.map((entry) => entry.body)).toEqual(["Decision: Rejected."]);
    expect(current(controller)).toMatchObject({ outcome: "rejected", line: "Rejected. This cannot be undone. Press J for the next item." });
  });
});

describe("generic actions, failure and Undo", () => {
  test("Start applies at once and can be undone", async () => {
    const { controller, api } = await startedAt(5);
    expect(current(controller).id).toBe(ID.F04);
    await controller.act({ action: "start" });
    expect(api.task(ID.F04).status).toBe("in-progress");
    expect(current(controller).line).toBe("Started. Status is now In progress.");
    await controller.undo();
    expect(api.task(ID.F04).status).toBe("todo");
    expect(current(controller).line).toBe("Undone. Status is back to Not started.");
  });

  test("a failed write changes nothing, keeps the position, and Retry repeats the same write", async () => {
    const { controller, api } = await startedAt(5);
    api.failNext("network");
    await controller.act({ action: "complete" });
    const failed = controller.getState();
    expect(failed.failure).toMatchObject({ phrase: "mark this item done", itemId: ID.F04 });
    expect(failed.run!.cursor).toBe(5);
    expect(current(controller).outcome).toBe(undefined);
    expect(api.task(ID.F04).status).toBe("todo");
    await controller.act({ action: "complete" });
    expect(api.task(ID.F04).status).toBe("todo");
    await controller.retry();
    expect(controller.getState().failure).toBe(null);
    expect(api.task(ID.F04).status).toBe("done");
    expect(current(controller).outcome).toBe("completed");
  });

  test("Defer writes snoozedUntil only; Undo writes the moment of Undo when there was no snooze", async () => {
    const { controller, api, clock } = await startedAt(5);
    const until = Date.parse("2026-10-04T08:00:00Z");
    await controller.act({ action: "defer", until });
    expect(api.task(ID.F04)).toMatchObject({ snoozedUntil: until, priority: "high", status: "todo" });
    expect(current(controller)).toMatchObject({ outcome: "deferred", deferredUntil: until, line: "Deferred until Sun, Oct 4, 08:00 UTC. It leaves today's run." });
    clock.advance(MINUTE);
    await controller.undo();
    expect(api.task(ID.F04).snoozedUntil).toBe(FIXTURE_NOW + MINUTE);
    expect(isEligible(api.task(ID.F04), FIXTURE_NOW + 2 * MINUTE)).toBe(true);
    expect(current(controller).outcome).toBe(undefined);
  });

  test("Block parks on a person in one audited write and offers no Undo", async () => {
    const { controller, api } = await startedAt(5);
    await controller.act({ action: "block", park: { who: "Pat", what: "the signed lease", nudgeAfterDays: 14 } });
    expect(api.task(ID.F04)).toMatchObject({ status: "waiting-external", waitingOn: { who: "Pat", what: "the signed lease", since: FIXTURE_NOW, nudgeAfterDays: 14 } });
    expect(api.audit).toEqual([{ taskId: ID.F04, field: "waitingOn", evidence: "Parked from Mission Control run", source: "jt" }]);
    expect(current(controller)).toMatchObject({ outcome: "parked", line: "Parked on Pat. It returns to today's run if no reply by day 14." });
    expect(current(controller).undo).toBe(undefined);
  });

  test("your own writes never trigger Changed underneath me", async () => {
    const { controller } = await startedAt(5);
    await controller.act({ action: "start" });
    await controller.refresh();
    expect(controller.openItemChange()).toBe(null);
    expect(controller.getState().run!.phase).toBe("inProgress");
  });
});

describe("paused states block every write", () => {
  test("Changed underneath me: actions pause until you confirm you read the new version", async () => {
    const { controller, api, clock } = await startedAt(5);
    clock.advance(MINUTE);
    api.edit(ID.F04, { doneState: "A new done condition." });
    await controller.refresh();
    expect(controller.openItemChange()).toMatchObject({ keys: ["doneState"] });
    await controller.act({ action: "complete" });
    expect(api.task(ID.F04).status).toBe("todo");
    controller.ackItemChange();
    expect(controller.openItemChange()).toBe(null);
    expect(controller.getState().run!.phase).toBe("inProgress");
    await controller.act({ action: "complete" });
    expect(api.task(ID.F04).status).toBe("done");
  });

  test("stale data: after five minutes without a good read, writes are refused", async () => {
    const { controller, api, clock } = await startedAt(5);
    api.failReads(10);
    clock.advance(6 * MINUTE);
    await controller.refresh();
    expect(controller.connection()).toBe("stale");
    await controller.act({ action: "complete" });
    expect(api.task(ID.F04).status).toBe("todo");
  });

  test("lane packets and outreach reviews are read-only in slice one", async () => {
    const { controller, api } = await startedAt(6);
    expect(current(controller).id).toBe(ID.F05);
    await controller.act({ action: "approve", note: "" });
    await controller.act({ action: "start" });
    expect(api.writes).toEqual([]);
  });
});

describe("moving through the run", () => {
  test("Next past a read-only item leaves it for the summary; Next at the end opens the summary", async () => {
    const { controller } = await startedAt(0);
    await controller.act({ action: "saveAnswer", text: "yes" });
    await controller.act({ action: "complete" });
    await controller.next();
    await controller.act({ action: "approve", note: "" });
    await controller.next();
    await controller.act({ action: "saveAnswer", text: "yes" });
    await controller.act({ action: "complete" });
    for (const _ of [3, 4, 5]) {
      await controller.next();
      await controller.act({ action: "complete" });
    }
    await controller.next();
    expect(current(controller).id).toBe(ID.F05);
    await controller.next();
    expect(controller.getState().run!.items[6].left).toBe("readOnly");
    expect(controller.getState().screen).toBe("runSummary");
    controller.closeRun();
    expect(controller.getState().run!.closedAt).toBe(FIXTURE_NOW);
  });

  test("a change at an item boundary shows the change summary before moving you", async () => {
    const { controller, api, clock } = await startedAt(2);
    clock.advance(MINUTE);
    api.edit(ID.F05, { payloadHash: "e".repeat(64) });
    await controller.refresh();
    expect(controller.getState().screen).toBe("item");
    await controller.next();
    expect(controller.getState().screen).toBe("runResume");
    expect(controller.getState().run!.cursor).toBe(2);
    expect(controller.getState().changes[0]).toMatchObject({ kind: "changed", itemId: ID.F05 });
    await controller.acknowledgeAndResume();
    expect(controller.getState().screen).toBe("item");
  });

  test("a hidden tab pauses the run; coming back with nothing changed returns straight to the item", async () => {
    const { controller } = await startedAt(3);
    controller.onHidden();
    expect(controller.getState().run!.phase).toBe("paused");
    await controller.onVisible();
    expect(controller.getState().run!.phase).toBe("inProgress");
    expect(controller.getState().screen).toBe("item");
  });

  test("coming back to a tab after another writer changed the run shows the change summary first", async () => {
    const { controller, api, clock } = await startedAt(3);
    controller.onHidden();
    clock.advance(10 * MINUTE);
    api.edit(ID.F05, { title: "Renamed while away" });
    await controller.onVisible();
    expect(controller.getState().screen).toBe("runResume");
    expect(controller.getState().run!.phase).toBe("queueChanged");
    expect(controller.getState().changes.map((change) => change.itemId)).toEqual([ID.F05]);
  });

  test("Pause run shows Resume with nothing changed", async () => {
    const { controller } = await startedAt(3);
    controller.pauseRun();
    expect(controller.getState().screen).toBe("runResume");
    expect(controller.getState().run!.phase).toBe("paused");
    expect(controller.getState().changes).toEqual([]);
  });
});
