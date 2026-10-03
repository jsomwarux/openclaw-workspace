// Regression tests for the fresh-context review findings (see tasks/implementation-notes.md
// section 9). Each block names the finding it pins.
import { describe, expect, test } from "bun:test";
import { CockpitController } from "./controller";
import { changeRows } from "./changes";
import { resolveKey } from "./keyboard";
import { acknowledge, backgroundCheck, detectChanges, moveNext, recordOutcome, resume, startRun } from "./run";
import { httpApi } from "./api";
import { memoryStorage, runStorage } from "./storage";
import type { KeyValueStorage } from "./storage";
import { nothingToOpen, summaryView } from "./view";
import { FixtureApi } from "./fixtures/fixture-api";
import { FIXTURE_NOW, ID, allFixtureTasks } from "./fixtures/data";
import type { FixtureId } from "./fixtures/data";
import type { RawTask, StoredRun } from "./types";

const MINUTE = 60_000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;
const NOW = FIXTURE_NOW;
const UTC = "UTC";
const byId = Object.fromEntries(Object.entries(ID).map(([fixture, id]) => [id, fixture]));

function tasksWith(edits: Partial<Record<FixtureId, Partial<RawTask>>> = {}, extra: RawTask[] = []): RawTask[] {
  return [
    ...allFixtureTasks().map((task) => {
      const fixture = byId[task._id] as FixtureId;
      return edits[fixture] ? { ...task, ...edits[fixture] } : task;
    }),
    ...extra,
  ];
}

function handled(run: StoredRun, count: number): StoredRun {
  let next = run;
  for (let i = 0; i < count; i += 1) {
    next = recordOutcome(next, next.items[i].id, { outcome: "completed" });
    next = moveNext(next).run;
  }
  return next;
}

function setup(storage: KeyValueStorage = memoryStorage()) {
  let now = NOW;
  const clock = { now: () => now, advance: (ms: number) => { now += ms; } };
  const api = new FixtureApi(allFixtureTasks(), clock.now);
  const controller = new CockpitController({ api, clock: clock.now, storage: runStorage(storage, "test"), timeZone: UTC });
  return { api, controller, clock };
}

async function at(position: number, storage?: KeyValueStorage) {
  const ctx = setup(storage);
  await ctx.controller.load();
  ctx.controller.startRun();
  for (let i = 0; i < position; i += 1) await ctx.controller.next();
  return ctx;
}

const newCard: RawTask = { _id: "new-card", title: "A new card", status: "todo", assignee: "jt", priority: "high", createdAt: NOW - 10 * MINUTE, updatedAt: NOW - 10 * MINUTE };

describe("finding 2: Undo is a write, so it pauses with every other write", () => {
  test("Undo is refused while another writer's change is unread, and never overwrites it", async () => {
    const { controller, api, clock } = await at(5);
    await controller.act({ action: "start" });
    clock.advance(MINUTE);
    api.edit(ID.F04, { status: "done" });
    await controller.refresh();
    expect(controller.canUndo()).toBe(false);
    await controller.undo();
    expect(api.task(ID.F04).status).toBe("done");
  });

  test("Undo is refused while the data is stale", async () => {
    const { controller, api, clock } = await at(5);
    await controller.act({ action: "complete" });
    api.failReads(100);
    clock.advance(6 * MINUTE);
    await controller.refresh();
    expect(controller.canUndo()).toBe(false);
    await controller.undo();
    expect(api.task(ID.F04).status).toBe("done");
  });

  test("Undo on a handled item is refused once another writer has changed that item", async () => {
    const { controller, api, clock } = await at(5);
    await controller.act({ action: "complete" });
    clock.advance(MINUTE);
    api.edit(ID.F04, { status: "in-progress", doneState: "Someone reopened it." });
    await controller.refresh();
    expect(controller.canUndo()).toBe(false);
    await controller.undo();
    expect(api.task(ID.F04).status).toBe("in-progress");
  });

  test("Undo still works when nothing else changed", async () => {
    const { controller, api } = await at(5);
    await controller.act({ action: "complete" });
    await controller.refresh();
    expect(controller.canUndo()).toBe(true);
    await controller.undo();
    expect(api.task(ID.F04).status).toBe("todo");
  });
});

describe("finding 4: a lane packet decided in the Work list is not reported as gone", () => {
  test("a packet rejected and archived elsewhere reads as rejected, and counts as handled after acknowledge", async () => {
    const { controller, api, clock } = await at(5);
    clock.advance(MINUTE);
    api.edit(ID.F05, { status: "archived", approvalState: "rejected", closureReason: { kind: "rejected", closedAt: NOW, closedBy: "jt" } });
    await controller.refresh();
    const change = controller.getState().changes.find((entry) => entry.itemId === ID.F05);
    expect(change?.detail).toBe("Rejected elsewhere.");
    await controller.next();
    await controller.acknowledgeAndResume();
    expect(controller.getState().run!.items[6]).toMatchObject({ outcome: "rejected", elsewhere: true });
  });

  test("the client reads archived records only through the existing route", async () => {
    const calls: string[] = [];
    const fetchImpl = (async (url: string) => {
      calls.push(url);
      return new Response(JSON.stringify({ tasks: [] }), { status: 200 });
    }) as unknown as typeof fetch;
    await httpApi(fetchImpl).listArchived();
    expect(calls).toEqual(["/api/tasks?include=archived"]);
  });
});

describe("finding 5: same-day reopen reads the same on every poll", () => {
  test("a new card after completion is 'added to today's run' on the first and second check and after a reload", () => {
    let run = handled(startRun(allFixtureTasks(), NOW, UTC), 7);
    const tasks = tasksWith({}, [newCard]);
    const first = backgroundCheck(run, tasks, NOW + HOUR, UTC);
    expect(first.changes.map((change) => change.kind)).toEqual(["addedToRun"]);
    const second = backgroundCheck(first.run, tasks, NOW + HOUR + MINUTE, UTC);
    expect(second.changes.map((change) => [change.kind, change.where])).toEqual([["addedToRun", "Joins today's run as item 8"]]);
    const reloaded = resume({ ...second.run, phase: "paused" }, tasks, NOW + 2 * HOUR, UTC);
    expect(reloaded.changes.map((change) => change.kind)).toEqual(["addedToRun"]);
    run = acknowledge(second.run, tasks, NOW + 2 * HOUR, UTC);
    expect(run.items).toHaveLength(8);
  });
});

describe("finding 6: changes outside the run do not interrupt the run", () => {
  test("a new backlog card mid-run leaves the run in progress; it shows at the next resume", () => {
    const run = handled(startRun(allFixtureTasks(), NOW, UTC), 2);
    const tasks = tasksWith({}, [newCard]);
    const checked = backgroundCheck(run, tasks, NOW + MINUTE, UTC);
    expect(checked.run.phase).toBe("inProgress");
    expect(detectChanges(run, tasks, NOW + MINUTE, UTC).map((change) => change.kind)).toEqual(["addedToBacklog"]);
  });

  test("an urgent item joining the run still interrupts at the next boundary", () => {
    const run = handled(startRun(allFixtureTasks(), NOW, UTC), 2);
    const checked = backgroundCheck(run, tasksWith({ F08: { dueDate: NOW - DAY, dueDateSource: "external" } }), NOW + MINUTE, UTC);
    expect(checked.run.phase).toBe("queueChanged");
  });
});

describe("finding 7: a poll during the operator's own write is ignored", () => {
  test("a refresh that lands mid-write does not leave an empty change summary", async () => {
    const { controller, api } = await at(5);
    api.writeDelayMs = 30;
    const write = controller.act({ action: "start" });
    await controller.refresh();
    await write;
    expect(controller.getState().run!.phase).toBe("inProgress");
    await controller.next();
    expect(controller.getState().screen).toBe("item");
  });
});

describe("finding 8: with the queue open, only Q, ? and Esc act on every screen", () => {
  test("run start with the queue view open", () => {
    const ctx = { screen: "runStart" as const, desktop: true, helpOpen: false, queueOpen: true, panel: null, canComplete: false, canDefer: false };
    expect(resolveKey({ key: "q" }, ctx)).toBe("toggleQueue");
    expect(resolveKey({ key: "Enter" }, ctx)).toBe(null);
    expect(resolveKey({ key: "?" }, ctx)).toBe("openHelp");
    expect(resolveKey({ key: "Escape" }, ctx)).toBe("escape");
  });
});

describe("finding 10: the change summary names an item displaced by an exception", () => {
  test("the displaced item is listed as leaving today's run", () => {
    const run = handled(startRun(allFixtureTasks(), NOW, UTC), 2);
    const changes = detectChanges(run, tasksWith({ F08: { dueDate: NOW - DAY, dueDateSource: "external" } }), NOW + MINUTE, UTC);
    expect(changes.find((change) => change.itemId === ID.F05)).toMatchObject({
      kind: "displaced",
      where: "Item 7 of 7",
      detail: "An urgent item takes its place. It goes back to the backlog when you acknowledge.",
    });
  });
});

describe("finding 11: the changed panel shows plain words, never hashes or stored enum names", () => {
  test("hash fields are summarized; enums become words", () => {
    const rows = changeRows(
      ["payloadHash", "approvalState", "doneEvidenceType", "dueDateSource", "status"],
      { payloadHash: "a".repeat(64), approvalState: "approved", doneEvidenceType: "application-ref", dueDateSource: "self", status: "todo" },
      { payloadHash: "b".repeat(64), approvalState: "pending", doneEvidenceType: "rsvp-ref", dueDateSource: "external", status: "in-progress" },
      UTC,
    );
    const text = JSON.stringify(rows);
    expect(/[0-9a-f]{64}/.test(text)).toBe(false);
    for (const raw of ['"pending"', '"approved"', "application-ref", "rsvp-ref", '"self"', '"external"', '"todo"', "in-progress"]) expect(text.includes(raw)).toBe(false);
    expect(rows.find((row) => row.label === "Approval")).toEqual({ label: "Approval", before: "Approved", after: "Approval pending" });
    expect(rows.find((row) => row.label === "Content")).toEqual({ label: "Content", before: "The version you saw", after: "A newer version" });
  });
});

describe("finding 13: a failed save is not silent", () => {
  test("when this browser cannot store progress, the operator is told", async () => {
    const full: KeyValueStorage = { getItem: () => null, setItem: () => { throw new Error("quota"); }, key: () => null, length: 0 };
    const { controller } = setup(full);
    await controller.load();
    controller.startRun();
    expect(controller.getState().notice).toBe("Progress could not be saved in this browser. The run works until you close this page.");
  });
});

describe("finding 16: a refused write triggers a fresh read", () => {
  test("after a refusal the cockpit reads again at once", async () => {
    const { controller, api } = await at(5);
    const before = api.reads;
    api.failNext("refused");
    await controller.act({ action: "start" });
    expect(api.reads).toBe(before + 1);
    expect(controller.getState().failure?.kind).toBe("refused");
  });
});

describe("finding 17: E explains when only file paths are recorded", () => {
  test("messages", () => {
    expect(nothingToOpen([])).toBe("Nothing to open: this item has no evidence links.");
    expect(nothingToOpen([{ text: "~/notes.md", kind: "file" }])).toBe("Nothing to open in the browser: this item's evidence is file paths. Use Copy path.");
  });
});

describe("finding 20: the summary's Handled list holds only handled items", () => {
  test("items left unhandled appear only under Still needs you", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    run = recordOutcome(run, run.items[0].id, { outcome: "completed", did: "Completed." });
    run = { ...run, items: run.items.map((item, i) => (i === 6 ? { ...item, left: "readOnly" as const } : item)) };
    const summary = summaryView(run, allFixtureTasks(), NOW, UTC);
    expect(summary.handled.map((entry) => entry.position)).toEqual([1]);
    expect(summary.stillNeedsYou.map((entry) => entry.id)).toContain(ID.F05);
  });
});
