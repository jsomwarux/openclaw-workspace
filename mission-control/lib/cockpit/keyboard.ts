// The desktop keyboard map (KEYBOARD.md). One window-level listener asks this function what a
// key means. There is deliberately no command that opens Approve or Reject: those need a click
// (or Tab plus a native Enter on the button), then a confirm.

export type KeyScreen = "loading" | "runStart" | "runResume" | "item" | "runSummary" | "emptyRun" | "rolloverSummary";
export type KeyPanel = null | "complete" | "defer" | "block" | "approve" | "reject" | "saveAnswer";

export interface KeyInput {
  key: string;
  ctrlKey?: boolean;
  metaKey?: boolean;
  altKey?: boolean;
  shiftKey?: boolean;
  repeat?: boolean;
  targetTag?: string;
  targetEditable?: boolean;
}

export interface KeyContext {
  screen: KeyScreen;
  desktop: boolean;
  helpOpen: boolean;
  queueOpen: boolean;
  panel: KeyPanel;
  canComplete: boolean;
  canDefer: boolean;
}

export type KeyCommand =
  | "next" | "previous" | "openComplete" | "openDefer" | "openEvidence" | "toggleQueue" | "openHelp"
  | "escape" | "confirmPanel" | "startRun" | "resumeRun";

const CONFIRMABLE = new Set<KeyPanel>(["complete", "defer", "reject", "approve"]);

export function resolveKey(input: KeyInput, ctx: KeyContext): KeyCommand | null {
  if (!ctx.desktop) return null;
  if (input.ctrlKey || input.metaKey || input.altKey || input.repeat) return null;
  if (input.key === "Escape") return "escape";
  const typing = input.targetTag === "INPUT" || input.targetTag === "TEXTAREA" || input.targetTag === "SELECT" || input.targetEditable === true;
  if (typing || ctx.helpOpen) return null;
  const onButton = input.targetTag === "BUTTON" || input.targetTag === "A";
  const plainEnter = input.key === "Enter" && !input.shiftKey && !onButton;

  // With the queue view open, only Q, ? and Esc act, on every screen (review finding 8).
  if (ctx.queueOpen) {
    if (input.key === "?") return "openHelp";
    return input.key.length === 1 && input.key.toLowerCase() === "q" ? "toggleQueue" : null;
  }

  if (ctx.screen !== "item") {
    if (input.key === "?") return "openHelp";
    if (plainEnter && ctx.screen === "runStart") return "startRun";
    if (plainEnter && ctx.screen === "runResume") return "resumeRun";
    return null;
  }

  if (input.key === "?") return "openHelp";
  const k = input.key.toLowerCase();
  if (input.key === "Enter") return plainEnter && CONFIRMABLE.has(ctx.panel) ? "confirmPanel" : null;
  if (input.key.length !== 1) return null;
  switch (k) {
    case "j": return "next";
    case "k": return "previous";
    case "c": return ctx.canComplete ? "openComplete" : null;
    case "d": return ctx.canDefer ? "openDefer" : null;
    case "e": return "openEvidence";
    case "q": return "toggleQueue";
    default: return null;
  }
}
