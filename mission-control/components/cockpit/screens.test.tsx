import { describe, expect, test } from "bun:test";
import { renderToStaticMarkup } from "react-dom/server";
import { actionContext, sliceOneActions } from "@/lib/cockpit/actions";
import { FIXTURE_NOW, ID, allFixtureTasks, fx } from "@/lib/cockpit/fixtures/data";
import { startRun } from "@/lib/cockpit/run";
import { buildItemView } from "@/lib/cockpit/view";
import type { RawTask } from "@/lib/cockpit/types";
import { DesktopItem } from "./DesktopItem";
import { MobileItem } from "./MobileItem";
import { DecisionPanel } from "./Panels";
import { ShortcutsOverlay } from "./Overlays";
import type { ButtonAction, ItemScreenProps } from "./model";

const NOW = FIXTURE_NOW;

function props(task: RawTask, over: Partial<ItemScreenProps> = {}): ItemScreenProps {
  const run = startRun(allFixtureTasks(), NOW, "UTC");
  const index = Math.max(0, run.items.findIndex((item) => item.id === task._id));
  const item = run.items[index] ?? { id: task._id };
  const view = buildItemView(task, item, { ...run, cursor: index }, NOW, "UTC");
  const buttons = sliceOneActions(actionContext(task, NOW, { paused: false })).filter((action) => action !== "previous" && action !== "next") as ButtonAction[];
  const noop = () => {};
  return {
    view, change: null, timeZone: "UTC", positionText: `${index + 1} of 7`, handledText: "0 handled",
    freshText: "Up to date · checked Oct 3, 00:00 UTC", freshShort: "Up to date", banner: null, rail: [],
    actions: { buttons, paused: null, readOnly: view.readOnly ? { text: "Read only for now.", title: view.titleText } : null, resolved: false, line: null, canUndo: false, failure: null, busy: false },
    panel: null, answerBox: null, evidenceEmphasis: false, evidenceMessage: false, notice: null,
    onPause: noop, onQueue: noop, onHelp: noop, onPrevious: noop, onNext: noop, onAckChange: noop, onRecheck: noop,
    onAction: noop, onUndo: noop, onRetry: noop, onDismiss: noop, onGoTo: noop,
    ...over,
  };
}

const buttonLabels = (html: string) => [...html.matchAll(/<button[^>]*>(.*?)<\/button>/g)].map((match) => match[1].replace(/<[^>]+>/g, ""));

describe("current item screens", () => {
  test("Q card offers Save answer, not Complete, and shows the lifted First action with its chip", () => {
    const html = renderToStaticMarkup(<DesktopItem {...props(fx("F01"))} />);
    const labels = buttonLabels(html);
    expect(labels).toContain("Save answer");
    expect(labels.some((label) => label.startsWith("Complete"))).toBe(false);
    expect(html).toContain("From description");
    expect(html).toContain("sample words value content context follow the step check....");
  });

  test("P card offers Approve and Reject with no key chip on either", () => {
    const html = renderToStaticMarkup(<DesktopItem {...props(fx("F02"))} />);
    const labels = buttonLabels(html);
    expect(labels).toContain("Approve");
    expect(labels).toContain("Reject");
    expect(labels).toContain("DeferD");
    expect(html).toContain("Authority · needs your approval");
  });

  test("lane packet renders read-only with a link to the Work list and no write buttons", () => {
    const html = renderToStaticMarkup(<DesktopItem {...props(fx("F05"))} />);
    const labels = buttonLabels(html);
    for (const action of ["Approve", "Reject", "Start", "Block"]) expect(labels).not.toContain(action);
    expect(html).toContain('href="/work"');
    expect(html).toContain("Approval pending · Edited after it was added · Expires in 2 days · Proof needed to finish: application reference");
  });

  test("outreach review shows subject, body and verifier report in full", () => {
    const review = fx("F11");
    const html = renderToStaticMarkup(<DesktopItem {...props(review)} />);
    expect(html).toContain(review.outreachReview!.subject as string);
    expect(html).toContain(review.outreachReview!.verifierReport as string);
  });

  test("the prompt renders verbatim inside a pre, never as Markdown", () => {
    const html = renderToStaticMarkup(<DesktopItem {...props(fx("F04"))} />);
    expect(html).toContain("108 lines · 10,533 characters");
    expect(html).toContain("<pre");
    expect(html).toContain("# reason task with detail line draft target text only option example point plan...");
    expect(html).not.toContain("<h1>reason task");
  });

  test("mobile: primary action in thumb reach, 44 px minimum targets", () => {
    const html = renderToStaticMarkup(<MobileItem {...props(fx("F04"))} />);
    expect(buttonLabels(html).slice(-6)).toEqual(["Start", "Complete", "Defer", "Block", "← Previous", "Next →"]);
    expect(html).toContain("min-h-[48px]");
    expect(html).toContain("min-h-[44px]");
  });

  test("an invalid card shows its reasons and offers only Previous and Next", () => {
    const html = renderToStaticMarkup(<DesktopItem {...props({ ...fx("F04"), title: "", status: "blocked" }, { actions: { buttons: [], paused: "This card cannot be acted on. You can move to another item.", readOnly: null, resolved: false, line: null, canUndo: false, failure: null, busy: false } })} />);
    expect(html).toContain("Title missing");
    expect(html).toContain("Its status is not one this app recognizes.");
    expect(buttonLabels(html).filter((label) => !/Previous|Next|Pause|Queue|Shortcuts|Check again|Show more|Copy prompt/.test(label))).toEqual([]);
  });
});

describe("Approve and Reject confirmation", () => {
  test("Reject confirms with an ink button; neither panel shows a key chip", () => {
    const reject = renderToStaticMarkup(<DecisionPanel mobile={false} kind="reject" note="" error={null} onNote={() => {}} onConfirm={() => {}} onCancel={() => {}} busy={false} />);
    expect(reject).toContain("Reject this item?");
    expect(reject).toContain("This cannot be undone.");
    expect(reject).toContain("bg-mc-ink");
    expect(reject).toContain("Note (optional)");
    const approve = renderToStaticMarkup(<DecisionPanel mobile={false} kind="approve" note="" error={null} onNote={() => {}} onConfirm={() => {}} onCancel={() => {}} busy={false} />);
    expect(approve).toContain("Approve this item?");
    expect(approve).not.toContain("aria-hidden=\"true\">A<");
  });

  test("the shortcuts overlay states the rule", () => {
    const html = renderToStaticMarkup(<ShortcutsOverlay onClose={() => {}} />);
    expect(html).toContain("Approve and Reject have no shortcut. Click the button, then confirm with Enter or a click. Reject cannot be undone.");
    for (const key of ["J", "K", "Q", "C", "D", "E", "Enter", "Esc", "?"]) expect(html).toContain(`>${key}</kbd>`);
  });
});

test("fixture ids used above exist", () => {
  expect(Object.keys(ID)).toHaveLength(12);
});
