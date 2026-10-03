// What counts as a change (state map Part B "material change"), told in plain words.
// updatedAt and feedback are not compared: a saved answer bumps updatedAt and must never
// flag itself (DECISIONS 11.7, GAPS 9). A fingerprint of the fields below is compared instead.
import { isLanePacket } from "./classify";
import { countWord, durationText, formatShort } from "./format";
import { approvalWord, proofWord, statusWord } from "./labels";
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

/**
 * How a record closed by someone else reads, on the Resume screen and in the summary alike, or
 * null when it is not closed. A generic card can be archived without being done (review 2, finding 4).
 */
export function closedElsewhere(task: RawTask): string | null {
  if (task.status === "done") return "Marked done elsewhere.";
  if (task.status !== "archived") return null;
  if (!isLanePacket(task)) return "Archived elsewhere.";
  const kind = (task.closureReason as { kind?: string } | undefined)?.kind;
  return kind === "rejected" ? "Rejected elsewhere."
    : kind === "skipped" ? "Skipped elsewhere."
      : kind === "no-action" ? "Closed elsewhere with no action."
        : kind === "expired" ? "Expired and closed."
          : "Closed elsewhere.";
}

/** One plain sentence for a run item that changed while the operator was away. */
export function describeChange(before: TrackedFields, task: RawTask, now: number): string {
  const after = trackedFields(task);
  if (!isClosedStatus(before.status) && isClosedStatus(after.status)) return closedElsewhere(task) ?? "Closed elsewhere.";
  if (!before.outreachDecision && after.outreachDecision) return "Decided elsewhere.";
  const keys = changedKeys(before, after);
  if (isLanePacket(task) && keys.includes("payloadHash")) {
    const expiry = typeof task.expiresAt === "number" && task.expiresAt > now ? ` Expires in ${durationText(task.expiresAt - now)}.` : "";
    return `Edited since you left. Approval is pending for the new version.${expiry}`;
  }
  return `Edited since you left: ${changedPhrase(keys)} changed.`;
}

export interface ChangeRow { label: string; before: string; after: string; long?: boolean }

const LONG_TEXT = new Set(["title", "description", "firstAction", "whyItMatters", "doneState", "pasteReadyPrompt", "pasteDestination", "exactSteps", "evidenceLinks"]);
const ROW_LABELS: Record<string, string> = {
  title: "Title", description: "Description", firstAction: "First action", whyItMatters: "Why it matters", doneState: "Done when",
  exactSteps: "Exact steps", pasteReadyPrompt: "Paste-ready prompt", pasteDestination: "Where to paste", evidenceLinks: "Evidence links",
  status: "Status", assignee: "Owner", priority: "Priority", sortOrder: "Place in the saved order", waitingOn: "Waiting on",
  snoozedUntil: "Snoozed until", dueDate: "Deadline", dueDateSource: "Deadline type", approvalState: "Approval", expiresAt: "Expires",
  doneEvidenceType: "Proof needed", outreachDecision: "Decision",
};

/** One field's value in plain words. Hashes and stored enum names never reach the screen. */
function words(key: string, value: unknown, timeZone: string): string {
  if (value === undefined || value === null || value === "") return "Missing";
  switch (key) {
    case "status": return statusWord(String(value));
    case "approvalState": return approvalWord(String(value));
    case "doneEvidenceType": return value === "none" ? "No proof needed" : proofWord(String(value)) ?? "Not recognized";
    case "dueDateSource": return value === "external" ? "External deadline" : value === "self" ? "Self-set deadline" : "Not recognized";
    case "snoozedUntil":
    case "dueDate":
    case "expiresAt": return typeof value === "number" ? formatShort(value, timeZone) : "Not recognized";
    case "sortOrder": return `Position ${String(value)}`;
    case "exactSteps": return Array.isArray(value) ? value.map((step, i) => `${i + 1}. ${String(step)}`).join("\n") : "Not recognized";
    case "evidenceLinks": return Array.isArray(value) ? value.map(String).join("\n") : "Not recognized";
    case "waitingOn": {
      const waiting = value as { who?: string; what?: string };
      return `Waiting on ${waiting.who ?? "Missing"}: ${waiting.what ?? "Missing"}`;
    }
    case "outreachDecision": {
      const decision = (value as { decision?: string }).decision;
      return decision === "approve" ? "Approved" : decision === "reject" ? "Rejected" : "Not recognized";
    }
    default: return typeof value === "string" ? value : String(value);
  }
}

/** Previous and current values for the "Changed underneath me" panel, in plain words. */
export function changeRows(keys: string[], before: TrackedFields, after: TrackedFields, timeZone: string): ChangeRow[] {
  const rows: ChangeRow[] = [];
  for (const key of keys) {
    if (key === "payloadHash") {
      rows.push({ label: "Content", before: "The version you saw", after: "A newer version" });
    } else if (key === "approvedPayloadHash") {
      continue;
    } else if (!rows.some((row) => row.label === ROW_LABELS[key])) {
      rows.push({ label: ROW_LABELS[key] ?? "Another field", before: words(key, before[key], timeZone), after: words(key, after[key], timeZone), ...(LONG_TEXT.has(key) ? { long: true } : {}) });
    }
  }
  return rows;
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
  const reorders = changes.filter((change) => ["movedUp", "displaced", "removedFromRun", "addedToRun"].includes(change.kind));
  const order = reorders.length === 0
    ? "Order and run size are unchanged."
    : "The order changes when you acknowledge: items that moved up come right after the item you are on.";
  const open = changes.some((change) => change.affectsOpenItem)
    ? `Item ${position(run)} changed. Read it again before you act.`
    : `Item ${position(run)} is unchanged since you left.`;
  return `${order} ${open}`;
}
