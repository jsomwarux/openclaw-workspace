import { describe, expect, test } from "bun:test";
import { liftSlots } from "./slots";
import { parseDescription } from "./description";
import { fx } from "./fixtures/data";
import type { RawTask } from "./types";

const decision = (description: string, over: Partial<RawTask> = {}): RawTask => ({
  _id: "d", title: "Growth OS Q4: pick one", status: "todo", assignee: "jt", priority: "high", description, ...over,
});

describe("slot lifting (DECISIONS 4)", () => {
  test("Q card: lifts First action, Why it matters and Done verbatim; Guard stays in the description", () => {
    const slots = liftSlots(fx("F01"));
    expect(slots.firstAction).toEqual({ kind: "value", value: "sample words value content context follow the step check....", source: "description" });
    expect(slots.whyItMatters).toEqual({ kind: "value", value: "card note entry filler source sample words value content.....", source: "description" });
    expect(slots.doneState).toEqual({ kind: "value", value: "with detail line draft target text only option example point plan card note entry.......", source: "description" });
    expect(slots.guard).toBe(null);
    expect(slots.remainingDescription).toContain("Guard: neutral record field summary status");
    expect(slots.remainingDescription).not.toContain("First action:");
    expect(slots.remainingDescription).not.toContain("Why it matters:");
    expect(slots.remainingDescription).not.toContain("\nDone:");
  });

  test("P and AP cards: Guard fills the authority boundary verbatim and leaves the description", () => {
    for (const id of ["F02", "F03"] as const) {
      const slots = liftSlots(fx(id));
      expect(slots.guard).toEqual({ kind: "value", value: "neutral record field summary status for item review synthetic reason task with detail.....", source: "description" });
      expect(slots.remainingDescription).not.toContain("Guard:");
    }
  });

  test("a typed field wins and its description line is not lifted", () => {
    const slots = liftSlots(decision("First action: from prose\nDone: prose done", { firstAction: "typed action" }));
    expect(slots.firstAction).toEqual({ kind: "value", value: "typed action", source: "field" });
    expect(slots.doneState).toEqual({ kind: "value", value: "prose done", source: "description" });
    expect(slots.remainingDescription).toBe("First action: from prose");
  });

  test("removes only the single space after the colon and keeps trailing characters", () => {
    const slots = liftSlots(decision("Done:  two spaces kept.  \nWhy it matters:no space"));
    expect(slots.doneState).toEqual({ kind: "value", value: " two spaces kept.  ", source: "description" });
    expect(slots.whyItMatters).toEqual({ kind: "value", value: "no space", source: "description" });
  });

  test("labels must start the line exactly; no match means Missing, never another line", () => {
    const slots = liftSlots(decision(" First action: indented\nfirst action: lower\nThe First action: inline\nDone when: wrong label"));
    expect(slots.firstAction).toEqual({ kind: "missing" });
    expect(slots.doneState).toEqual({ kind: "missing" });
    expect(slots.whyItMatters).toEqual({ kind: "missing" });
    expect(slots.remainingDescription).toBe(" First action: indented\nfirst action: lower\nThe First action: inline\nDone when: wrong label");
  });

  test("generic cards never lift from the description", () => {
    const generic: RawTask = { _id: "g", title: "Plain task", status: "todo", assignee: "jt", priority: "low", description: "First action: looks like a slot" };
    const slots = liftSlots(generic);
    expect(slots.firstAction).toEqual({ kind: "missing" });
    expect(slots.remainingDescription).toBe("First action: looks like a slot");
  });

  test("typed seven-field cards read straight from their fields; no description means none to render", () => {
    const slots = liftSlots(fx("F04"));
    expect(slots.firstAction).toEqual({ kind: "missing" });
    expect(slots.whyItMatters.kind).toBe("value");
    expect(slots.remainingDescription).toBe(null);
  });
});

describe("remaining description rendering (DECISIONS 4.8, 4.9)", () => {
  test("Q card: bold-label bullets, the empty Answer bullet becomes the answer box, Guard stays as text", () => {
    const blocks = parseDescription(liftSlots(fx("F01")).remainingDescription!, { answerSlot: true });
    expect(blocks.map((block) => block.kind)).toEqual(["bullets", "answerSlot", "paragraph"]);
    const bullets = blocks[0] as Extract<(typeof blocks)[number], { kind: "bullets" }>;
    expect(bullets.items.map((item) => item.label)).toEqual(["Question:", "Why:", "Proposed answer:"]);
    expect(bullets.items[0].text).toBe(" text only option example point....");
  });

  test("P card: heading and paragraph keep their order; no answer slot is offered", () => {
    const blocks = parseDescription(liftSlots(fx("F02")).remainingDescription!, { answerSlot: false });
    expect(blocks.map((block) => block.kind)).toEqual(["bullets", "heading", "paragraph"]);
    expect(blocks[1]).toEqual({ kind: "heading", text: "detail line draft target text.." });
  });

  test("without the answer slot the empty Answer bullet renders as a bullet, unchanged", () => {
    const blocks = parseDescription("- **Answer:**", { answerSlot: false });
    expect(blocks).toEqual([{ kind: "bullets", items: [{ label: "Answer:", text: "", children: [] }] }]);
  });

  test("line breaks inside a paragraph are preserved; other Markdown stays literal", () => {
    const blocks = parseDescription("Blocked on: x\nsecond line *not italic*\n# not a heading", { answerSlot: false });
    expect(blocks).toEqual([{ kind: "paragraph", lines: ["Blocked on: x", "second line *not italic*", "# not a heading"] }]);
  });

  test("ordered sub-lists attach to the bullet above them", () => {
    const blocks = parseDescription("- **Choose:** one of\n  1. first\n  2. second\n- next", { answerSlot: false });
    expect(blocks).toEqual([{ kind: "bullets", items: [
      { label: "Choose:", text: " one of", children: [{ n: "1", text: "first" }, { n: "2", text: "second" }] },
      { label: null, text: "next", children: [] },
    ] }]);
  });
});
