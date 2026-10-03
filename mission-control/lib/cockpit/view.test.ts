import { describe, expect, test } from "bun:test";
import { buildItemView, queueView, runStartView, summaryView } from "./view";
import { recordOutcome, moveNext, startRun } from "./run";
import { FIXTURE_NOW, ID, allFixtureTasks, fx } from "./fixtures/data";
import type { RawTask, StoredRun } from "./types";

const NOW = FIXTURE_NOW;
const UTC = "UTC";
const HOUR = 3_600_000;
const DAY = 24 * HOUR;
const run0 = () => startRun(allFixtureTasks(), NOW, UTC);
const view = (task: RawTask, run: StoredRun = run0(), position = run.items.findIndex((item) => item.id === task._id)) =>
  buildItemView(task, run.items[Math.max(position, 0)] ?? { id: task._id }, { ...run, cursor: Math.max(position, 0) }, NOW, UTC);

describe("current item view", () => {
  test("Q card: eyebrow, lifted First action, answer slot, no Authority", () => {
    const v = view(fx("F01"));
    expect(v.eyebrow).toBe("1 of 7 · Not started · Owner: jt · Priority: high");
    expect(v.titleText).toBe("Sample DC Q1: step check marker result placeholder neutral record field.");
    expect(v.slots.firstAction).toMatchObject({ kind: "value", source: "description" });
    expect(v.answerSlot).toBe(true);
    expect(v.authority).toBe(null);
    expect(v.descriptionBlocks?.map((block) => block.kind)).toEqual(["bullets", "answerSlot", "paragraph"]);
  });

  test("P card: Guard line is the authority boundary", () => {
    const v = view(fx("F02"));
    expect(v.authority).toEqual({ text: "neutral record field summary status for item review synthetic reason task with detail....." });
    expect(v.answerSlot).toBe(false);
  });

  test("lane packet: authority facts in plain words, read-only in slice one, evidence split into links and paths", () => {
    const v = view(fx("F05"));
    expect(v.authority).toEqual({ text: "Approval pending · Edited after it was added · Expires in 2 days · Proof needed to finish: application reference" });
    expect(v.readOnly).toBe(true);
    expect(v.evidence.map((entry) => entry.kind)).toEqual(["web", "web", "web", "file"]);
    expect(v.prompt).toEqual({ kind: "missing" });
    expect(v.promptMeta).toBe("Missing");
    expect(v.destination.kind).toBe("value");
  });

  test("expired packet: plain expiry sentence and authority", () => {
    const early = startRun(allFixtureTasks(), NOW - 2 * DAY, UTC);
    const run = { ...early, items: [...early.items, { id: ID.F06 }], size: early.size + 1 };
    const v = view(fx("F06"), run, run.items.length - 1);
    expect(v.statusLabel).toBe("Expired");
    expect(v.expired).toBe("This item expired on Oct 2, 00:00 UTC (1 day ago).");
    expect(v.authority?.text).toBe("Approval pending · Expired · Proof needed to finish: RSVP reference");
  });

  test("seven-field card: prompt verbatim with its size, steps, freshness and missing fields", () => {
    const v = view(fx("F04"));
    expect(v.prompt).toEqual({ kind: "value", value: fx("F04").pasteReadyPrompt, source: "field" });
    expect(v.promptMeta).toBe("108 lines · 10,533 characters");
    expect(v.steps.kind === "value" && v.steps.value).toHaveLength(4);
    expect(v.freshness.lastChanged).toBe("Sep 24, 2026, 00:00 UTC · 9 days ago");
    expect(v.freshness.source).toEqual({ kind: "missing" });
    expect(v.freshness.description).toBe("missing");
    expect(v.evidence).toEqual([]);
  });

  test("feedback history: every entry in full, newest last", () => {
    const v = view(fx("F10"), run0(), 0);
    expect(v.feedback).toHaveLength(12);
    expect(v.feedback[0]).toMatchObject({ author: "jt", body: "card note entry filler source sample......" });
    expect(v.feedback[11].when).toBe("Oct 1, 2026, 05:00 UTC");
    expect(Math.max(...v.feedback.map((entry) => entry.body.length))).toBe(4000);
  });

  test("outreach review: subject, body and verifier report verbatim, read-only", () => {
    const v = view(fx("F11"), run0(), 0);
    expect(v.outreach?.subject).toEqual({ kind: "value", value: "the step check marker.", source: "field" });
    expect(v.outreach?.verifierReport.kind === "value" && v.outreach.verifierReport.value.length).toBe(2506);
    expect(v.statusLabel).toBe("Awaiting decision");
    expect(v.readOnly).toBe(true);
  });

  test("invalid card: title missing, reasons listed", () => {
    const v = view({ ...fx("F04"), title: "", status: "blocked" }, run0(), 5);
    expect(v.titleText).toBe("Title missing");
    expect(v.validity).toEqual({ ok: false, reasons: ["No title is recorded.", "Its status is not one this app recognizes."] });
    expect(v.statusLabel).toBe("Status not recognized");
  });

  test("an urgent exception shows its label", () => {
    const tasks = allFixtureTasks().map((task) => (task._id === ID.F05 ? { ...task, expiresAt: NOW + 5 * HOUR } : task));
    const run = startRun(tasks, NOW, UTC);
    const v = buildItemView(tasks.find((task) => task._id === ID.F05)!, run.items[0], run, NOW, UTC);
    expect(v.exception?.text).toBe("Moved up: approval expires in 5 hours (Oct 3, 05:00 UTC)");
  });
});

describe("queue view (README 3, DECISIONS 1.10)", () => {
  test("groups, counts, statuses, ages and blockers", () => {
    let run = run0();
    for (let i = 0; i < 5; i += 1) {
      run = recordOutcome(run, run.items[i].id, { outcome: "completed" });
      run = moveNext(run).run;
    }
    const q = queueView(allFixtureTasks(), run, NOW, UTC);
    expect(q.counts).toEqual({ inRun: 7, handled: 5, current: 1, upNext: 1, outside: 5 });
    expect(q.groups.map((group) => `${group.name} · ${group.rows.length}`)).toEqual(["Q · 1", "P · 1", "AP · 1", "Other cards · 9"]);
    const other = q.groups[3];
    expect(other.rows.map((row) => row.position ?? "—")).toEqual([4, 5, 6, 7, "—", "—", "—", "—", "—"]);
    expect(other.dividerBefore).toBe(4);
    const statuses = Object.fromEntries(q.groups.flatMap((group) => group.rows).map((row) => [row.id, row.status]));
    expect(statuses[ID.F01]).toBe("Handled");
    expect(statuses[ID.F04]).toBe("Not started");
    expect(statuses[ID.F05]).toBe("Up next");
    expect(statuses[ID.F06]).toBe("Expired");
    expect(statuses[ID.F10]).toBe("Done");
    expect(statuses[ID.F11]).toBe("Awaiting decision");
    const rows = Object.fromEntries(q.groups.flatMap((group) => group.rows).map((row) => [row.id, row]));
    expect(rows[ID.F07].blocker).toBe("Waiting on neutral.......: words value content context follow the step..");
    expect(rows[ID.F08].blocker).toBe("Blocked on: detail line draft target text only option example point plan card note entry filler source sample words.....");
    expect(rows[ID.F04].blocker).toBe(null);
    expect([rows[ID.F01].age, rows[ID.F07].age, rows[ID.F08].age, rows[ID.F04].age]).toEqual(["2h", "129d", "1h", "9d"]);
    expect(rows[ID.F04].current).toBe(true);
    expect(other.rows.slice(4).map((row) => row.id)).toEqual([ID.F09, ID.F10, ID.F11, ID.F06, ID.F08]);
  });
});

describe("run start and summary", () => {
  test("run start: count, breakdown, first item and why, no exceptions, backlog", () => {
    const start = runStartView(allFixtureTasks(), NOW, UTC);
    expect(start.headline).toBe("7 items, ready to start");
    expect(start.breakdown).toBe("Q 1 · P 1 · AP 1 · Other cards 4");
    expect(start.first?.title).toBe("Sample DC Q1: step check marker result placeholder neutral record field.");
    expect(start.first?.firstAction).toMatchObject({ kind: "value", source: "description" });
    expect(start.whyFirst).toBe("Curated order puts Q cards first, in number order.");
    expect(start.exceptions).toEqual([]);
    expect(start.outside).toBe(5);
  });

  test("summary: counts, what still needs you, and what was done", () => {
    let run = run0();
    const outcomes = [
      { outcome: "completed" as const, did: "Answer recorded, then completed." },
      { outcome: "approved" as const, did: "Approved. Note recorded." },
      { outcome: "completed" as const, did: "Answer recorded, then completed." },
      { outcome: "parked" as const, did: "Parked on neutral........ Nudge after 14 days.", parked: { who: "neutral.......", nudgeDueAt: Date.parse("2026-10-17T00:00:00Z"), days: 14 } },
      { outcome: "completed" as const, did: "Completed." },
      { outcome: "deferred" as const, did: "Deferred until Sun, Oct 4, 08:00 UTC.", deferredUntil: Date.parse("2026-10-04T08:00:00Z") },
    ];
    outcomes.forEach((outcome, i) => { run = recordOutcome(run, run.items[i].id, outcome); });
    run = { ...run, items: run.items.map((item, i) => (i === 6 ? { ...item, left: "readOnly" as const } : item)) };
    const s = summaryView(run, allFixtureTasks(), NOW, UTC);
    expect(s.headline).toBe("6 of 7 handled");
    expect(s.counts).toBe("3 completed · 1 approved · 1 parked · 1 deferred");
    expect(s.stillNeedsYou.map((entry) => entry.detail)).toEqual([
      "Parked on neutral........ Nudge due Oct 17.",
      "Deferred until Sun, Oct 4, 08:00 UTC.",
      "Not decided yet. Lane packets are decided in the current interface for now: open the Work list.",
    ]);
    expect(s.handled.map((entry) => entry.did)).toEqual([
      "Answer recorded, then completed.", "Approved. Note recorded.", "Answer recorded, then completed.",
      "Parked on neutral........ Nudge after 14 days.", "Completed.", "Deferred until Sun, Oct 4, 08:00 UTC.", "Left unhandled.",
    ]);
  });
});
