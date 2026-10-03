import { describe, expect, test } from "bun:test";
import {
  acknowledge, allResolved, backgroundCheck, clearOutcome, detectChanges, foldWrite, moveNext, movePrevious,
  pause, recordOutcome, resume, rollover, startRun,
} from "./run";
import { changeHeadline, changeClosingLine } from "./changes";
import { planRun } from "./exceptions";
import { FIXTURE_NOW, ID, allFixtureTasks } from "./fixtures/data";
import type { FixtureId } from "./fixtures/data";
import type { RawTask, StoredRun } from "./types";

const MINUTE = 60_000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;
const NOW = FIXTURE_NOW;
const UTC = "UTC";
const byId = Object.fromEntries(Object.entries(ID).map(([fixture, id]) => [id, fixture]));
const runNames = (run: StoredRun) => run.items.map((item) => byId[item.id] ?? item.id);

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
    next = recordOutcome(next, next.items[i].id, { outcome: "completed", did: "Completed." });
    next = moveNext(next).run;
  }
  return next;
}

const newCard: RawTask = { _id: "new-card", title: "Blocked: note entry filler source sample words.", status: "todo", assignee: "jt", priority: "high", createdAt: NOW - 50 * MINUTE, updatedAt: NOW - 50 * MINUTE };

describe("transition 1: Not started to In progress (snapshot taken at start)", () => {
  test("commits the planned run, the cursor at 1, and a snapshot of every run item", () => {
    const run = startRun(allFixtureTasks(), NOW, UTC);
    expect(run.phase).toBe("inProgress");
    expect(run.localDate).toBe("2026-10-03");
    expect(runNames(run)).toEqual(["F01", "F02", "F03", "F07", "F12", "F04", "F05"]);
    expect(run.size).toBe(7);
    expect(run.cursor).toBe(0);
    expect(run.snapshot.map((entry) => entry.id)).toEqual(run.items.map((item) => item.id));
    expect(run.knownIds).toHaveLength(12);
  });

  test("transition 11: before start, the plan simply follows the latest read", () => {
    expect(planRun(tasksWith(), NOW, UTC).ids).toHaveLength(7);
    expect(planRun(tasksWith({ F01: { status: "done" } }), NOW, UTC).ids[0]).toBe(ID.F02);
  });
});

describe("transition 2: handling items, and moving", () => {
  test("a handled item resolves; Next moves one position; the denominator never changes", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    run = recordOutcome(run, ID.F01, { outcome: "completed" });
    expect(run.items[0].outcome).toBe("completed");
    expect(run.cursor).toBe(0);
    run = moveNext(run).run;
    expect(run.cursor).toBe(1);
    run = recordOutcome(run, ID.F02, { outcome: "parked", parked: { who: "Pat", nudgeDueAt: NOW + 14 * DAY, days: 14 } });
    expect(run.size).toBe(7);
    expect(movePrevious(run).run.cursor).toBe(0);
    expect(movePrevious({ ...run, cursor: 0 }).notice).toBe("This is the first item.");
  });

  test("moving past an item that cannot be acted on leaves it unhandled, for the summary", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    run = moveNext(run, "invalid").run;
    expect(run.items[0].left).toBe("invalid");
    expect(run.items[0].outcome).toBe(undefined);
  });

  test("Undo clears the outcome so the item counts as open again", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    run = recordOutcome(run, ID.F01, { outcome: "completed", undo: { kind: "complete", restore: { status: "todo" } } });
    run = clearOutcome(run, ID.F01, "Undone. Status is back to Not started.");
    expect(run.items[0].outcome).toBe(undefined);
    expect(run.items[0].undo).toBe(undefined);
    expect(run.items[0].line).toBe("Undone. Status is back to Not started.");
  });
});

describe("transition 8: complete when every item is handled", () => {
  test("the last outcome completes the run; Next at the end then opens the summary", () => {
    let run = handled(startRun(allFixtureTasks(), NOW, UTC), 6);
    expect(run.phase).toBe("inProgress");
    run = recordOutcome(run, run.items[6].id, { outcome: "completed" });
    expect(allResolved(run)).toBe(true);
    expect(run.phase).toBe("complete");
    expect(moveNext(run).atEnd).toBe(true);
  });

  test("Next at the end with an unhandled item goes back to it and says why", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    run = { ...run, cursor: 6 };
    const moved = moveNext(run);
    expect(moved.atEnd).toBe(false);
    expect(moved.run.cursor).toBe(0);
    expect(moved.notice).toBe("Item 1 of 7 still needs you.");
  });
});

describe("transitions 3, 4, 5: pause and return", () => {
  test("pause records when you left", () => {
    const run = pause(startRun(allFixtureTasks(), NOW, UTC), NOW + HOUR);
    expect(run.phase).toBe("paused");
    expect(run.pausedAt).toBe(NOW + HOUR);
  });

  test("return with nothing changed goes straight back to In progress", () => {
    const run = pause(startRun(allFixtureTasks(), NOW, UTC), NOW + HOUR);
    const back = resume(run, allFixtureTasks(), NOW + 2 * HOUR, UTC);
    expect(back.changes).toEqual([]);
    expect(back.run.phase).toBe("inProgress");
  });

  test("return after another writer changed things: Queue changed, with each change explained", () => {
    // Run started Sep 30, 23:00 UTC: F06 was more than 24 hours from expiry (so not an
    // urgent exception) and F08 did not exist yet.
    const startedAt = NOW - 49 * HOUR;
    const before = allFixtureTasks().filter((task) => task._id !== ID.F08);
    let run = startRun(before, startedAt, UTC);
    expect(runNames(run)).toEqual(["F01", "F02", "F03", "F07", "F12", "F04", "F05"]);
    run = handled(run, 5);
    run = pause(run, NOW - 3 * HOUR);
    const after = tasksWith({ F05: { payloadHash: "f".repeat(64), updatedAt: NOW - 2 * HOUR } });
    const back = resume(run, after, NOW, UTC);
    expect(back.run.phase).toBe("queueChanged");
    expect(back.changes.map((change) => [change.kind, byId[change.itemId] ?? change.itemId, change.where, change.detail])).toEqual([
      ["changed", "F05", "Item 7 of 7", "Edited since you left. Approval is pending for the new version. Expires in 2 days."],
      ["addedToBacklog", "F08", "Not in today's run", "Created 50 minutes ago."],
      ["expired", "F06", "Not in today's run", "Expired Oct 2, 00:00 UTC. Hidden from today."],
    ]);
    expect(changeHeadline(back.changes, back.run)).toBe("None affect item 6 of 7. One affects a later item.");
    expect(changeClosingLine(back.changes, back.run)).toBe("Order and run size are unchanged. Item 6 of 7 is unchanged since you left.");
  });

  test("your own writes and feedback never count as changes", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    run = foldWrite(run, ID.F04, { status: "in-progress", auditSource: "jt" });
    const mine = tasksWith({ F04: { status: "in-progress", updatedAt: NOW + MINUTE, feedback: [{ id: "x", body: "Answer: yes", author: "jt", createdAt: NOW + MINUTE }] } });
    expect(detectChanges(run, mine, NOW + 2 * MINUTE, UTC)).toEqual([]);
  });

  test("a text edit names what changed, in plain words", () => {
    const run = startRun(allFixtureTasks(), NOW, UTC);
    const changes = detectChanges(run, tasksWith({ F04: { doneState: "new done", title: "new title" } }), NOW + MINUTE, UTC);
    expect(changes.map((change) => change.detail)).toEqual(["Edited since you left: the title and the done condition changed."]);
  });
});

describe("transitions 6 and 7: a background change, then acknowledge", () => {
  test("a change to the open item moves the run to Queue changed without reordering anything", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    run = { ...run, cursor: 5 };
    const checked = backgroundCheck(run, tasksWith({ F04: { doneState: "rewritten" } }), NOW + MINUTE, UTC);
    expect(checked.run.phase).toBe("queueChanged");
    expect(checked.changes[0]).toMatchObject({ kind: "changed", affectsOpenItem: true, where: "Item 6 of 7" });
    expect(runNames(checked.run)).toEqual(runNames(run));
  });

  test("acknowledge re-bases the snapshot; handled items stay handled", () => {
    let run = handled(startRun(allFixtureTasks(), NOW, UTC), 2);
    const edited = tasksWith({ F04: { doneState: "rewritten" } });
    run = backgroundCheck(run, edited, NOW + MINUTE, UTC).run;
    run = acknowledge(run, edited, NOW + 2 * MINUTE, UTC);
    expect(run.phase).toBe("inProgress");
    expect(detectChanges(run, edited, NOW + 3 * MINUTE, UTC)).toEqual([]);
    expect(run.items.slice(0, 2).map((item) => item.outcome)).toEqual(["completed", "completed"]);
  });

  test("an item done elsewhere counts as handled after acknowledge", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    const done = tasksWith({ F12: { status: "done" } });
    expect(detectChanges(run, done, NOW + MINUTE, UTC)[0].detail).toBe("Marked done elsewhere.");
    run = acknowledge(run, done, NOW + MINUTE, UTC);
    expect(run.items[4]).toMatchObject({ outcome: "completed", elsewhere: true });
  });

  test("an item deleted elsewhere leaves the run as removed", () => {
    let run = startRun(allFixtureTasks(), NOW, UTC);
    const gone = allFixtureTasks().filter((task) => task._id !== ID.F12);
    expect(detectChanges(run, gone, NOW + MINUTE, UTC)[0]).toMatchObject({ kind: "removedFromRun", detail: "It is no longer in Mission Control. It leaves today's run." });
    run = acknowledge(run, gone, NOW + MINUTE, UTC);
    expect(run.items[4].left).toBe("removed");
  });
});

describe("urgent exceptions mid-run (DECISIONS 3.4, 3.5, 3.7)", () => {
  test("a backlog item that turns urgent joins right after the open item, displacing the last curated item", () => {
    let run = handled(startRun(allFixtureTasks(), NOW, UTC), 2);
    expect(run.cursor).toBe(2);
    const urgent = tasksWith({ F08: { dueDate: NOW - DAY, dueDateSource: "external" } });
    const checked = backgroundCheck(run, urgent, NOW + MINUTE, UTC);
    expect(runNames(checked.run)).toEqual(runNames(run));
    const moved = checked.changes.find((change) => change.kind === "movedUp");
    expect(moved).toMatchObject({ itemId: ID.F08, where: "Becomes item 4 of 7", detail: "Moved up: external deadline passed Oct 2 (1 day overdue)" });
    run = acknowledge(checked.run, urgent, NOW + 2 * MINUTE, UTC);
    expect(runNames(run)).toEqual(["F01", "F02", "F03", "F08", "F07", "F12", "F04"]);
    expect(run.items[3].exception?.reason).toBe("externalDeadlineOverdue");
    expect(run.size).toBe(7);
  });

  test("an urgent item already in the run moves up to just after the open item, never before it", () => {
    let run = handled(startRun(allFixtureTasks(), NOW, UTC), 1);
    run = acknowledge(run, tasksWith({ F05: { expiresAt: NOW + 3 * HOUR } }), NOW + MINUTE, UTC);
    expect(runNames(run)).toEqual(["F01", "F02", "F05", "F03", "F07", "F12", "F04"]);
    expect(run.cursor).toBe(1);
  });

  test("a brand-new urgent card never joins a committed run", () => {
    const run = startRun(allFixtureTasks(), NOW, UTC);
    const urgentNew = { ...newCard, dueDate: NOW - DAY, dueDateSource: "external" };
    const changes = detectChanges(run, tasksWith({}, [urgentNew]), NOW + MINUTE, UTC);
    expect(changes.map((change) => change.kind)).toEqual(["addedToBacklog"]);
    expect(runNames(acknowledge(run, tasksWith({}, [urgentNew]), NOW + MINUTE, UTC))).toEqual(runNames(run));
  });
});

describe("transition 9: reopen the same day", () => {
  test("a new eligible card after completion reopens the run instead of starting a second one", () => {
    let run = handled(startRun(allFixtureTasks(), NOW, UTC), 7);
    expect(run.phase).toBe("complete");
    const checked = backgroundCheck(run, tasksWith({}, [newCard]), NOW + HOUR, UTC);
    expect(checked.run.phase).toBe("queueChanged");
    expect(checked.changes).toHaveLength(1);
    expect(checked.changes[0]).toMatchObject({ kind: "addedToRun", where: "Joins today's run as item 8" });
    run = acknowledge(checked.run, tasksWith({}, [newCard]), NOW + HOUR, UTC);
    expect(run.phase).toBe("inProgress");
    expect(run.size).toBe(8);
    expect(run.cursor).toBe(7);
    expect(run.items[7].id).toBe("new-card");
  });

  test("a closed run does not reopen", () => {
    const run = { ...handled(startRun(allFixtureTasks(), NOW, UTC), 7), closedAt: NOW + MINUTE };
    expect(backgroundCheck(run, tasksWith({}, [newCard]), NOW + HOUR, UTC).run.phase).toBe("complete");
  });
});

describe("transition 10: local date rollover", () => {
  test("an earlier day's run that was not closed is closed as unfinished and kept for its summary", () => {
    const run = pause(handled(startRun(allFixtureTasks(), NOW, UTC), 3), NOW + HOUR);
    const result = rollover(run, "2026-10-04", NOW + DAY);
    expect(result.previous).toMatchObject({ localDate: "2026-10-03", unfinished: true, closedAt: NOW + DAY });
    expect(result.previous?.items.slice(0, 3).map((item) => item.outcome)).toEqual(["completed", "completed", "completed"]);
  });

  test("a complete but unclosed run closes without the unfinished mark; today's run is untouched", () => {
    const complete = handled(startRun(allFixtureTasks(), NOW, UTC), 7);
    expect(rollover(complete, "2026-10-04", NOW + DAY).previous?.unfinished).toBe(false);
    expect(rollover(complete, "2026-10-03", NOW).previous).toBe(null);
    expect(rollover({ ...complete, closedAt: NOW }, "2026-10-04", NOW + DAY).previous).toBe(null);
    expect(rollover(null, "2026-10-04", NOW).previous).toBe(null);
  });
});
