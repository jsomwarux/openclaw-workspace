// Slot filling (DECISIONS 4): typed fields win; decision cards lift labelled description
// lines verbatim. Only lines that fill a shown slot leave the remaining description.
import { familyOf, seriesOf } from "./classify";
import type { RawTask, Verbatim } from "./types";

export interface Slots {
  firstAction: Verbatim<string>;
  whyItMatters: Verbatim<string>;
  doneState: Verbatim<string>;
  /** Authority boundary from the Guard line, P and AP cards only. */
  guard: Verbatim<string> | null;
  /** Description with lifted lines removed, or null when nothing is left to show. */
  remainingDescription: string | null;
}

const MISSING = { kind: "missing" } as const;
const LABELS = {
  firstAction: "First action:",
  whyItMatters: "Why it matters:",
  doneState: "Done:",
  guard: "Guard:",
} as const;
type SlotKey = keyof typeof LABELS;

function fromField(value: unknown): Verbatim<string> | null {
  return typeof value === "string" && value.length > 0 ? { kind: "value", value, source: "field" } : null;
}

const stripCarriageReturn = (line: string) => (line.endsWith("\r") ? line.slice(0, -1) : line);

export function liftSlots(task: RawTask): Slots {
  const description = typeof task.description === "string" ? task.description : "";
  const lines = description.split("\n");
  const lifted = new Set<number>();
  const isDecision = familyOf(task) === "decision";
  const series = seriesOf(task);

  const lift = (key: SlotKey): Verbatim<string> => {
    const label = LABELS[key];
    const index = lines.findIndex((raw, i) => !lifted.has(i) && stripCarriageReturn(raw).startsWith(label));
    if (index < 0) return MISSING;
    const rest = stripCarriageReturn(lines[index]).slice(label.length);
    const value = rest.startsWith(" ") ? rest.slice(1) : rest;
    if (value.length === 0) return MISSING;
    lifted.add(index);
    return { kind: "value", value, source: "description" };
  };

  const slot = (key: Exclude<SlotKey, "guard">, field: unknown): Verbatim<string> =>
    fromField(field) ?? (isDecision ? lift(key) : MISSING);

  const firstAction = slot("firstAction", task.firstAction);
  const whyItMatters = slot("whyItMatters", task.whyItMatters);
  const doneState = slot("doneState", task.doneState);
  const guard = isDecision && (series === "P" || series === "AP") ? lift("guard") : null;

  const remaining = lines.filter((_, i) => !lifted.has(i)).join("\n");
  return {
    firstAction,
    whyItMatters,
    doneState,
    guard,
    remainingDescription: remaining.trim().length > 0 ? remaining : null,
  };
}
