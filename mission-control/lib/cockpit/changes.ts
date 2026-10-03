// What counts as a change (state map Part B "material change"), told in plain words.
// updatedAt and feedback are not compared: a saved answer bumps updatedAt and must never
// flag itself (DECISIONS 11.7, GAPS 9). A fingerprint of the fields below is compared instead.
import { isLanePacket } from "./classify";
import { countWord, durationText } from "./format";
import type { RawTask, RunChange, StoredRun, TrackedFields } from "./types";

export const TRACKED_KEYS = [
  "title", "description", "status", "assignee", "priority", "sortOrder", "firstAction", "whyItMatters", "doneState",
  "exactSteps", "pasteReadyPrompt", "pasteDestination", "evidenceLinks", "waitingOn", "snoozedUntil", "dueDate",
  "dueDateSource", "payloadHash", "approvalState", "approvedPayloadHash", "expiresAt", "doneEvidenceType", "outreachDecision",
] as const;

const PHRASES: Record<(typeof TRACKED_KEYS)[number], string> = {
  title: "the title",
  description: "the description",
  status: "the status",
  assignee: "the owner",
  priority: "the priority",
  sortOrder: "its place in the saved order",
  firstAction: "the first action",
  whyItMatters: "why it matters",
  doneState: "the done condition",
  exactSteps: "the steps",
  pasteReadyPrompt: "the prompt",
  pasteDestination: "where to paste",
  evidenceLinks: "the evidence links",
  waitingOn: "who it is waiting on",
  snoozedUntil: "the snooze time",
  dueDate: "the deadline",
  dueDateSource: "the deadline",
  payloadHash: "the approved content",
  approvalState: "the approval",
  approvedPayloadHash: "the approval",
  expiresAt: "the expiry",
  doneEvidenceType: "the proof needed",
  outreachDecision: "the decision",
};

function canonical(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical((value as Record<string, unknown>)[key])]));
  }
  return value;
}

export function trackedFields(task: Record<string, unknown>): TrackedFields {
  const fields: TrackedFields = {};
  for (const key of TRACKED_KEYS) if (task[key] !== undefined) fields[key] = canonical(task[key]);
  return fields;
}

export function fingerprint(fields: TrackedFields): string {
  return JSON.stringify(TRACKED_KEYS.map((key) => [key, fields[key] ?? null]));
}

/** The tracked keys whose values differ, in display order. */
export function changedKeys(before: TrackedFields, after: TrackedFields): string[] {
  return TRACKED_KEYS.filter((key) => JSON.stringify(before[key] ?? null) !== JSON.stringify(after[key] ?? null));
}

function joinPhrases(phrases: string[]): string {
  const unique = [...new Set(phrases)];
  if (unique.length <= 1) return unique.join("");
  return `${unique.slice(0, -1).join(", ")} and ${unique[unique.length - 1]}`;
}

/** "the title and the done condition" */
export function changedPhrase(keys: string[]): string {
  return joinPhrases(keys.map((key) => PHRASES[key as keyof typeof PHRASES] ?? key));
}

const isClosedStatus = (status: unknown) => status === "done" || status === "archived";

/** One plain sentence for a run item that changed while the operator was away. */
export function describeChange(before: TrackedFields, task: RawTask, now: number): string {
  const after = trackedFields(task);
  if (!isClosedStatus(before.status) && isClosedStatus(after.status)) {
    return isLanePacket(task) && after.status === "archived" ? "Closed elsewhere." : "Marked done elsewhere.";
  }
  if (!before.outreachDecision && after.outreachDecision) return "Decided elsewhere.";
  const keys = changedKeys(before, after);
  if (isLanePacket(task) && keys.includes("payloadHash")) {
    const expiry = typeof task.expiresAt === "number" && task.expiresAt > now ? ` Expires in ${durationText(task.expiresAt - now)}.` : "";
    return `Edited since you left. Approval is pending for the new version.${expiry}`;
  }
  return `Edited since you left: ${changedPhrase(keys)} changed.`;
}

const position = (run: StoredRun) => `${run.cursor + 1} of ${run.size}`;

/** "None affect item 6 of 7. One affects a later item." */
export function changeHeadline(changes: RunChange[], run: StoredRun): string {
  const open = changes.filter((change) => change.affectsOpenItem).length;
  const later = changes.filter((change) => change.inRun && !change.affectsOpenItem).length;
  if (open === 0 && later === 0) return "None affect today's run.";
  const first = open > 0 ? `This affects item ${position(run)}, where you left.` : `None affect item ${position(run)}.`;
  if (later === 0) return first;
  return `${first} ${later === 1 ? "One affects a later item." : `${countWord(later)} affect later items.`}`;
}

/** "Order and run size are unchanged. Item 6 of 7 is unchanged since you left." */
export function changeClosingLine(changes: RunChange[], run: StoredRun): string {
  const reorders = changes.filter((change) => change.kind === "movedUp" || change.kind === "removedFromRun" || change.kind === "addedToRun");
  const order = reorders.length === 0
    ? "Order and run size are unchanged."
    : "The order changes when you acknowledge: items that moved up come right after the item you are on.";
  const open = changes.some((change) => change.affectsOpenItem)
    ? `Item ${position(run)} changed. Read it again before you act.`
    : `Item ${position(run)} is unchanged since you left.`;
  return `${order} ${open}`;
}
