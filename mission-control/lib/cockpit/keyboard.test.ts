import { describe, expect, test } from "bun:test";
import { resolveKey } from "./keyboard";
import type { KeyContext, KeyInput } from "./keyboard";

const item: KeyContext = { screen: "item", desktop: true, helpOpen: false, queueOpen: false, panel: null, canComplete: true, canDefer: true };
const key = (k: string, over: Partial<KeyInput> = {}): KeyInput => ({ key: k, ...over });

describe("keyboard map (KEYBOARD.md)", () => {
  test("move, act and help keys on the current item", () => {
    expect(resolveKey(key("j"), item)).toBe("next");
    expect(resolveKey(key("J", { shiftKey: true }), item)).toBe("next");
    expect(resolveKey(key("k"), item)).toBe("previous");
    expect(resolveKey(key("c"), item)).toBe("openComplete");
    expect(resolveKey(key("d"), item)).toBe("openDefer");
    expect(resolveKey(key("e"), item)).toBe("openEvidence");
    expect(resolveKey(key("q"), item)).toBe("toggleQueue");
    expect(resolveKey(key("?", { shiftKey: true }), item)).toBe("openHelp");
    expect(resolveKey(key("Escape"), item)).toBe("escape");
  });

  test("C and D open their confirm panels only where those actions are permitted", () => {
    const paused = { ...item, canComplete: false, canDefer: false };
    expect(resolveKey(key("c"), paused)).toBe(null);
    expect(resolveKey(key("d"), paused)).toBe(null);
    expect(resolveKey(key("j"), paused)).toBe("next");
    expect(resolveKey(key("e"), paused)).toBe("openEvidence");
  });

  test("Enter confirms an open confirm panel, unless a button has focus", () => {
    for (const panel of ["complete", "defer", "reject", "approve"] as const) {
      expect(resolveKey(key("Enter"), { ...item, panel })).toBe("confirmPanel");
      expect(resolveKey(key("Enter", { targetTag: "BUTTON" }), { ...item, panel })).toBe(null);
    }
    expect(resolveKey(key("Enter"), item)).toBe(null);
  });

  test("ignored: modifiers, held keys, typing, the open overlay, and mobile", () => {
    for (const mod of ["ctrlKey", "metaKey", "altKey"] as const) expect(resolveKey(key("j", { [mod]: true }), item)).toBe(null);
    expect(resolveKey(key("j", { repeat: true }), item)).toBe(null);
    expect(resolveKey(key("j", { targetTag: "TEXTAREA" }), item)).toBe(null);
    expect(resolveKey(key("j", { targetTag: "INPUT" }), item)).toBe(null);
    expect(resolveKey(key("j", { targetEditable: true }), item)).toBe(null);
    expect(resolveKey(key("Escape", { targetTag: "TEXTAREA" }), item)).toBe("escape");
    expect(resolveKey(key("j"), { ...item, helpOpen: true })).toBe(null);
    expect(resolveKey(key("Escape"), { ...item, helpOpen: true })).toBe("escape");
    expect(resolveKey(key("j"), { ...item, desktop: false })).toBe(null);
  });

  test("with the queue view open only Q, ? and Esc act", () => {
    const queue = { ...item, queueOpen: true };
    expect(resolveKey(key("q"), queue)).toBe("toggleQueue");
    expect(resolveKey(key("?"), queue)).toBe("openHelp");
    expect(resolveKey(key("Escape"), queue)).toBe("escape");
    for (const k of ["j", "k", "c", "d", "e", "Enter"]) expect(resolveKey(key(k), queue)).toBe(null);
  });

  test("run screens: Enter starts or resumes; ? and Esc work; letters do nothing", () => {
    expect(resolveKey(key("Enter"), { ...item, screen: "runStart" })).toBe("startRun");
    expect(resolveKey(key("Enter"), { ...item, screen: "runResume" })).toBe("resumeRun");
    expect(resolveKey(key("Enter", { targetTag: "BUTTON" }), { ...item, screen: "runStart" })).toBe(null);
    for (const screen of ["runSummary", "emptyRun", "rolloverSummary"] as const) expect(resolveKey(key("Enter"), { ...item, screen })).toBe(null);
    for (const screen of ["runStart", "runResume", "runSummary", "emptyRun"] as const) {
      expect(resolveKey(key("?"), { ...item, screen })).toBe("openHelp");
      expect(resolveKey(key("j"), { ...item, screen })).toBe(null);
    }
  });
});

describe("Approve and Reject have no single-key shortcut (DECISIONS 5.6, 12)", () => {
  const printable = [
    ..."abcdefghijklmnopqrstuvwxyz",
    ..."ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    ..."0123456789",
    ..."`~!@#$%^&*()-_=+[]{}\\|;:'\",.<>/? ",
    "Enter", "Tab", "Backspace", "Delete", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Home", "End",
  ];
  const modifierSets: Partial<KeyInput>[] = [
    {}, { shiftKey: true }, { ctrlKey: true }, { metaKey: true }, { altKey: true },
    { ctrlKey: true, shiftKey: true }, { metaKey: true, shiftKey: true }, { altKey: true, shiftKey: true },
  ];
  const contexts: KeyContext[] = [
    item, { ...item, panel: "complete" }, { ...item, panel: "defer" }, { ...item, panel: "block" },
    { ...item, canComplete: false, canDefer: false }, { ...item, queueOpen: true },
  ];

  test("no key, chord or Shift combination opens an Approve or Reject panel", () => {
    for (const context of contexts) {
      for (const k of printable) {
        for (const mods of modifierSets) {
          const command = resolveKey({ key: k, ...mods }, context);
          expect(["openApprove", "openReject", "approve", "reject"].includes(String(command))).toBe(false);
        }
      }
    }
  });

  test("with an Approve or Reject panel open, only a plain Enter confirms; no letter, chord or Shift+Enter does", () => {
    for (const panel of ["approve", "reject"] as const) {
      const open = { ...item, panel };
      for (const k of printable) {
        for (const mods of modifierSets) {
          const command = resolveKey({ key: k, ...mods }, open);
          const plainEnter = k === "Enter" && Object.keys(mods).length === 0;
          expect(command === "confirmPanel").toBe(plainEnter);
        }
      }
    }
  });
});
