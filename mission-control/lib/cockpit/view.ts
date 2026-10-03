// Pure builders that turn records and the run into what each screen shows. Every displayed
// field is Verbatim: read as stored, lifted from a description line, or Missing.
import { isReadOnlyInSliceOne } from "./actions";
import { familyOf, seriesOf } from "./classify";
import { parseDescription } from "./description";
import type { DescriptionBlock } from "./description";
import { isDecidedOutreach, isEligible, isExpired, isParked, nudgeDue } from "./eligibility";
import { planRun } from "./exceptions";
import { durationText, formatFull, formatLongDay, formatMonthDay, formatShort, formatWeekdayTime, relativeAgo, ageText } from "./format";
import { approvalWord, proofWord, statusWord } from "./labels";
import { curatedCompare, groupOf, GROUPS } from "./order";
import type { QueueGroup } from "./order";
import { itemResolved } from "./run";
import { liftSlots } from "./slots";
import type { Slots } from "./slots";
import { KNOWN_STATUSES, validateCard } from "./validity";
import type { ExceptionLabel, ItemFamily, RawTask, RunItem, StoredRun, Verbatim } from "./types";

export interface EvidenceEntry { text: string; kind: "web" | "file" }
export interface FeedbackRow { id: string; author: string; when: string; body: string }

export interface ItemViewModel {
  id: string;
  family: ItemFamily;
  position: number;
  size: number;
  eyebrow: string;
  mobileEyebrow: string;
  title: Verbatim<string>;
  titleText: string;
  statusLabel: string;
  exception: ExceptionLabel | null;
  slots: Slots;
  descriptionBlocks: DescriptionBlock[] | null;
  answerSlot: boolean;
  authority: { text: string | null } | null;
  steps: Verbatim<string[]>;
  prompt: Verbatim<string>;
  promptMeta: string;
  destination: Verbatim<string>;
  evidence: EvidenceEntry[];
  freshness: { lastChanged: string | null; created: string | null; source: Verbatim<string>; project: Verbatim<string>; description: "present" | "missing" };
  feedback: FeedbackRow[];
  validity: { ok: true } | { ok: false; reasons: string[] };
  expired: string | null;
  outreach: { subject: Verbatim<string>; body: Verbatim<string>; verifierReport: Verbatim<string>; decided: string | null } | null;
  readOnly: boolean;
  removed: boolean;
}

const URL_PATTERN = /(https?:\/\/[^\s)]+)/g;
const MISSING = { kind: "missing" } as const;

function text(value: unknown): Verbatim<string> {
  return typeof value === "string" && value.length > 0 ? { kind: "value", value, source: "field" } : MISSING;
}

export function evidenceOf(task: RawTask): EvidenceEntry[] {
  const fromDescription = typeof task.description === "string" ? task.description.match(URL_PATTERN) ?? [] : [];
  const stored = Array.isArray(task.evidenceLinks) ? task.evidenceLinks.filter((entry) => typeof entry === "string") : [];
  return [...fromDescription, ...stored].map((entry) => ({ text: entry, kind: /^https?:\/\//i.test(entry) ? "web" : "file" }));
}

/** The plain status word for a record as it stands now. */
export function liveStatus(task: RawTask, now: number, item?: RunItem): string {
  if (item?.outcome === "rejected") return "Rejected";
  if (isExpired(task, now)) return "Expired";
  if (!KNOWN_STATUSES.includes(task.status ?? "")) return "Status not recognized";
  if (familyOf(task) === "outreachReview" && !isDecidedOutreach(task) && task.status === "todo") return "Awaiting decision";
  if (typeof task.snoozedUntil === "number" && task.snoozedUntil > now && task.status !== "done") return "Deferred";
  if (isParked(task) && !nudgeDue(task, now) && task.status !== "done") return "Waiting";
  return statusWord(task.status);
}

function authorityOf(task: RawTask, slots: Slots, now: number): { text: string | null } | null {
  const family = familyOf(task);
  if (family === "lanePacket") {
    const parts = [approvalWord(task.approvalState)];
    if (task.payloadHash && task.admittedPayloadHash && task.payloadHash !== task.admittedPayloadHash) parts.push("Edited after it was added");
    if (isExpired(task, now)) parts.push("Expired");
    else if (typeof task.expiresAt === "number") parts.push(`Expires in ${durationText(task.expiresAt - now)}`);
    const proof = proofWord(task.doneEvidenceType);
    if (proof) parts.push(`Proof needed to finish: ${proof}`);
    return { text: parts.join(" · ") };
  }
  if (family === "outreachReview") {
    const decision = task.outreachDecision?.decision;
    const parts = [decision === "approve" ? "Decided: approved" : decision === "reject" ? "Decided: rejected" : "Approval pending"];
    if (typeof task.outreachReview?.reviewCycle === "number") parts.push(`Review cycle ${task.outreachReview.reviewCycle}`);
    return { text: parts.join(" · ") };
  }
  if (slots.guard) return { text: slots.guard.kind === "value" ? slots.guard.value : null };
  return null;
}

export function buildItemView(task: RawTask | null, item: RunItem, run: StoredRun, now: number, timeZone: string): ItemViewModel {
  const removed = task === null;
  const record: RawTask = task ?? { _id: item.id, ...(run.snapshot.find((entry) => entry.id === item.id)?.fields ?? {}) };
  const position = run.items.findIndex((candidate) => candidate.id === item.id) + 1;
  const family = familyOf(record);
  const series = seriesOf(record);
  const slots = liftSlots(record);
  const answerSlot = series === "Q" || series === "AP";
  const validity = removed ? { ok: false as const, reasons: ["It is no longer in Mission Control."] } : validateCard(record);
  const statusLabel = liveStatus(record, now, item);
  const title = text(record.title);
  const titleText = title.kind === "value" && record.title!.trim().length > 0 ? title.value : "Title missing";
  const owner = record.assignee ?? "Missing";
  const priority = record.priority ?? "Missing";
  const prompt = text(record.pasteReadyPrompt);
  const lines = prompt.kind === "value" ? prompt.value.replace(/\n$/, "").split("\n").length : 0;
  const steps: Verbatim<string[]> = Array.isArray(record.exactSteps) && record.exactSteps.length > 0
    ? { kind: "value", value: record.exactSteps, source: "field" }
    : MISSING;
  const review = record.outreachReview;
  return {
    id: record._id,
    family,
    position,
    size: run.size,
    eyebrow: `${position} of ${run.size} · ${statusLabel} · Owner: ${owner} · Priority: ${priority}`,
    mobileEyebrow: `${statusLabel} · Owner: ${owner} · Priority: ${priority}`,
    title,
    titleText,
    statusLabel,
    exception: item.exception ?? null,
    slots,
    descriptionBlocks: slots.remainingDescription ? parseDescription(slots.remainingDescription, { answerSlot }) : null,
    answerSlot,
    authority: authorityOf(record, slots, now),
    steps,
    prompt,
    promptMeta: prompt.kind === "missing"
      ? "Missing"
      : !validity.ok
        ? "Not available for an invalid card"
        : `${lines} ${lines === 1 ? "line" : "lines"} · ${prompt.value.length.toLocaleString("en-US")} characters`,
    destination: text(record.pasteDestination),
    evidence: evidenceOf(record),
    freshness: {
      lastChanged: typeof record.updatedAt === "number" ? `${formatFull(record.updatedAt, timeZone)} · ${relativeAgo(record.updatedAt, now)}` : null,
      created: typeof record.createdAt === "number" ? `${formatFull(record.createdAt, timeZone)} · ${relativeAgo(record.createdAt, now)}` : null,
      source: text(record.sourceSystem),
      project: text(record.project),
      description: typeof record.description === "string" && record.description.length > 0 ? "present" : "missing",
    },
    feedback: (record.feedback ?? []).map((entry) => ({ id: entry.id, author: entry.author, when: formatFull(entry.createdAt, timeZone), body: entry.body })),
    validity,
    expired: isExpired(record, now) ? `This item expired on ${formatShort(record.expiresAt!, timeZone)} (${relativeAgo(record.expiresAt!, now)}).` : null,
    outreach: review
      ? {
          subject: text(review.subject),
          body: text(review.body),
          verifierReport: text(review.verifierReport),
          decided: record.outreachDecision?.decision === "approve" ? "Approved" : record.outreachDecision?.decision === "reject" ? "Rejected" : null,
        }
      : null,
    readOnly: isReadOnlyInSliceOne(family),
    removed,
  };
}

// ---- queue ------------------------------------------------------------------------------

export interface QueueRowView {
  id: string;
  position: number | null;
  title: string;
  status: string;
  owner: string;
  age: string;
  blocker: string | null;
  inRun: boolean;
  current: boolean;
  exception: ExceptionLabel | null;
}
export interface QueueGroupView { name: QueueGroup; rows: QueueRowView[]; dividerBefore: number | null }
export interface QueueViewModel {
  groups: QueueGroupView[];
  counts: { inRun: number; handled: number; current: number; upNext: number; outside: number };
}

export function blockerOf(task: RawTask): string | null {
  if (isParked(task)) return `Waiting on ${task.waitingOn!.who}: ${task.waitingOn!.what}`;
  if (typeof task.title === "string" && task.title.startsWith("Blocked") && typeof task.description === "string" && task.description.length > 0) {
    return task.description.split("\n")[0];
  }
  return null;
}

/** The queue. Before a run starts, today's planned run stands in for it. */
export function queueView(tasks: RawTask[], run: StoredRun | null, now: number, timeZone: string): QueueViewModel {
  const items: RunItem[] = run?.items ?? planRun(tasks, now, timeZone).ids.map((id) => ({ id }));
  const cursor = run ? run.cursor : -1;
  const complete = run?.phase === "complete";
  const index = new Map(tasks.map((task) => [task._id, task]));
  const inRun = new Map(items.map((item, i) => [item.id, i]));

  const row = (task: RawTask): QueueRowView => {
    const i = inRun.get(task._id);
    const item = i === undefined ? undefined : items[i];
    let status = liveStatus(task, now);
    if (item && i !== undefined) {
      if (itemResolved(item)) status = "Handled";
      else if (i > cursor) status = "Up next";
    }
    return {
      id: task._id,
      position: i === undefined ? null : i + 1,
      title: typeof task.title === "string" && task.title.trim() ? task.title : "Title missing",
      status,
      owner: task.assignee ?? "Missing",
      age: ageText(task.createdAt, now),
      blocker: blockerOf(task),
      inRun: i !== undefined,
      current: i === cursor && !complete,
      exception: item?.exception ?? null,
    };
  };

  const known = [...tasks];
  for (const item of items) {
    if (!index.has(item.id)) {
      const fields = run?.snapshot.find((entry) => entry.id === item.id)?.fields ?? {};
      known.push({ _id: item.id, ...fields, status: "archived" });
    }
  }

  const groups = GROUPS.map((name): QueueGroupView => {
    const members = known.filter((task) => groupOf(task) === name);
    const running = members.filter((task) => inRun.has(task._id)).sort((a, b) => inRun.get(a._id)! - inRun.get(b._id)!);
    const outside = members.filter((task) => !inRun.has(task._id)).sort(curatedCompare);
    const rows = [...running, ...outside].map(row);
    return { name, rows, dividerBefore: name === "Other cards" && running.length > 0 && outside.length > 0 ? running.length : null };
  }).filter((group) => group.rows.length > 0);

  const resolved = items.filter(itemResolved).length;
  const current = cursor >= 0 && !complete && items[cursor] && !itemResolved(items[cursor]) ? 1 : 0;
  return {
    groups,
    counts: {
      inRun: items.length,
      handled: resolved,
      current,
      upNext: items.filter((item, i) => i > cursor && !itemResolved(item)).length,
      outside: tasks.filter((task) => !inRun.has(task._id)).length,
    },
  };
}

// ---- run start --------------------------------------------------------------------------

export interface RunStartViewModel {
  headline: string;
  date: string;
  breakdown: string;
  first: { title: string; firstAction: Verbatim<string>; position: string } | null;
  whyFirst: string;
  exceptions: { title: string; text: string }[];
  outside: number;
  eligible: number;
}

const WHY_FIRST: Record<QueueGroup, string> = {
  Q: "Curated order puts Q cards first, in number order.",
  P: "Curated order puts P cards first when no Q card is waiting, in number order.",
  AP: "Curated order puts AP cards next after Q and P, in number order. None of those are waiting.",
  "Other cards": "No Q, P or AP card is waiting, so other cards follow their saved sequence. This one comes first.",
};

export function runStartView(tasks: RawTask[], now: number, timeZone: string): RunStartViewModel {
  const plan = planRun(tasks, now, timeZone);
  const index = new Map(tasks.map((task) => [task._id, task]));
  const planned = plan.ids.map((id) => index.get(id)!);
  const count = (name: QueueGroup) => planned.filter((task) => groupOf(task) === name).length;
  const first = planned[0];
  const firstException = first ? plan.exceptions[first._id] : undefined;
  return {
    headline: `${planned.length} ${planned.length === 1 ? "item" : "items"}, ready to start`,
    date: formatLongDay(now, timeZone),
    breakdown: GROUPS.map((name) => `${name} ${count(name)}`).join(" · "),
    first: first
      ? { title: typeof first.title === "string" && first.title.trim() ? first.title : "Title missing", firstAction: liftSlots(first).firstAction, position: `1 of ${planned.length}` }
      : null,
    whyFirst: firstException ? `It is an urgent exception. ${firstException.text}.` : first ? WHY_FIRST[groupOf(first)] : "",
    exceptions: Object.entries(plan.exceptions).map(([id, label]) => ({ title: index.get(id)?.title ?? "", text: label.text })),
    outside: tasks.length - planned.length,
    eligible: tasks.filter((task) => isEligible(task, now)).length,
  };
}

// ---- summary ----------------------------------------------------------------------------

export interface SummaryViewModel {
  headline: string;
  meta: string;
  counts: string;
  stillNeedsYou: { id: string; title: string; detail: string }[];
  handled: { position: number; title: string; did: string }[];
  addedSinceStart: string | null;
}

function readOnlyNote(family: ItemFamily): string {
  return family === "outreachReview"
    ? "Not decided yet. Outreach reviews are decided in the current interface for now: open the Work list."
    : "Not decided yet. Lane packets are decided in the current interface for now: open the Work list.";
}

export function summaryView(run: StoredRun, tasks: RawTask[], now: number, timeZone: string): SummaryViewModel {
  const index = new Map(tasks.map((task) => [task._id, task]));
  const titleOf = (id: string) => {
    const title = index.get(id)?.title ?? run.snapshot.find((entry) => entry.id === id)?.fields.title;
    return typeof title === "string" && title.trim() ? title : "Title missing";
  };
  const count = (outcome: string) => run.items.filter((item) => item.outcome === outcome).length;
  const rejected = count("rejected");
  const counts = `${count("completed")} completed · ${count("approved")} approved · ${count("parked")} parked · ${count("deferred")} deferred${rejected ? ` · ${rejected} rejected` : ""}`;

  const stillNeedsYou = run.items.flatMap((item) => {
    const task = index.get(item.id);
    const entry = (detail: string) => [{ id: item.id, title: titleOf(item.id), detail }];
    if (item.outcome === "parked" && item.parked) return entry(`Parked on ${item.parked.who}. Nudge due ${formatMonthDay(item.parked.nudgeDueAt, timeZone)}.`);
    if (item.outcome === "deferred" && item.deferredUntil) return entry(`Deferred until ${formatWeekdayTime(item.deferredUntil, timeZone)}.`);
    if (item.outcome) return [];
    if (item.left === "invalid") return entry("This card cannot be acted on. Fix it where it was created.");
    if (item.left === "expired") {
      return entry(task?.expiresAt ? `Expired ${formatShort(task.expiresAt, timeZone)}. You can still reject it in the current interface.` : "Expired.");
    }
    if (item.left === "readOnly") return entry(readOnlyNote(task ? familyOf(task) : "lanePacket"));
    if (item.left === "removed") return entry("It is no longer in Mission Control.");
    return entry(run.unfinished ? "Not handled before the day ended." : "Not handled yet.");
  });

  const handledCount = run.items.filter((item) => item.outcome).length;
  const added = tasks.filter((task) => typeof task.createdAt === "number" && task.createdAt > run.startedAt && !run.items.some((item) => item.id === task._id)).length;
  return {
    headline: `${handledCount} of ${run.size} handled`,
    meta: `${formatLongDay(run.startedAt, timeZone)} · Curated order · ${counts}`,
    counts,
    stillNeedsYou,
    handled: run.items.map((item, i) => ({
      position: i + 1,
      title: titleOf(item.id),
      did: item.did ?? (item.outcome ? "Handled." : item.left ? "Left unhandled." : "Not handled."),
    })),
    addedSinceStart: added === 0
      ? null
      : `Added to the backlog since the run started: ${added} ${added === 1 ? "item. It is" : "items. They are"} not part of today's run.`,
  };
}
