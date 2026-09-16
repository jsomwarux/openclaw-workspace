import { canonicalJson } from "./canonical-json";

export const SUPPRESSION_NOT_CONFIGURED = "OUTREACH_SUPPRESSION_OWNER_NOT_CONFIGURED";
export const SUPPRESSION_EVENT_VERSION = "outreach-suppression-event-v1" as const;
export const SUPPRESSION_QUERY_VERSION = "outreach-suppression-query-v1" as const;
export const SUPPRESSION_OWNER = "mission-control" as const;

export type SuppressionState = "sent" | "clear" | "manual_hold" | "replied" | "opted_out" | "hard_bounce";
export type MissionControlSuppressionSubmission = {
  schemaVersion: typeof SUPPRESSION_EVENT_VERSION;
  requestId: string;
  prospectId: string;
  organizationFactId: string;
  channelFingerprint: string;
  state: SuppressionState;
  evidenceToken: string;
};
export type SuppressionEvent = MissionControlSuppressionSubmission & {
  actorId: "jt";
  eventId: string;
  sequence: number;
  observedAt: string;
  revision: string;
};
export type SuppressionTuple = Pick<SuppressionEvent, "prospectId" | "organizationFactId" | "channelFingerprint">;
export type SuppressionEventMetadata = Pick<SuppressionEvent, "eventId" | "sequence" | "state" | "actorId" | "evidenceToken" | "observedAt" | "revision">;

const PORTABLE = /^[a-z0-9][a-z0-9._:-]{0,127}$/;
const REQUEST = /^suppression_request_[a-f0-9]{20}$/;
const EVENT = /^suppression_event_[a-f0-9]{20}$/;
const DIGEST = /^[a-f0-9]{64}$/;
const EVIDENCE = /^evidence_[a-f0-9]{64}$/;
const ENTROPY = /^[a-f0-9]{20}$/;
const STATES = new Set<SuppressionState>(["sent", "clear", "manual_hold", "replied", "opted_out", "hard_bounce"]);
const SUBMISSION_FIELDS = ["schemaVersion", "requestId", "prospectId", "organizationFactId", "channelFingerprint", "state", "evidenceToken"] as const;
const EVENT_FIELDS = [...SUBMISSION_FIELDS, "actorId", "eventId", "sequence", "observedAt", "revision"] as const;

function record(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}
function exact(value: Record<string, unknown>, fields: readonly string[]) {
  const actual = Object.keys(value).sort();
  const expected = [...fields].sort();
  return actual.length === expected.length && actual.every((key, index) => key === expected[index]);
}
function utc(value: unknown): value is string {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(value)) return false;
  return Number.isFinite(Date.parse(value));
}
async function sha256(parts: Array<string | Uint8Array>): Promise<string> {
  const bytes: number[] = [];
  for (const part of parts) bytes.push(...(typeof part === "string" ? new TextEncoder().encode(part) : part));
  const digest = await crypto.subtle.digest("SHA-256", new Uint8Array(bytes));
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export function suppressionOwnerEnabled(value: string | undefined = process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED): boolean {
  return value === "true";
}
export function assertSuppressionOwnerEnabled(value?: string): void {
  if (!suppressionOwnerEnabled(value)) throw new Error(SUPPRESSION_NOT_CONFIGURED);
}

export function validateSuppressionTuple(value: unknown): asserts value is SuppressionTuple {
  if (!record(value) || !PORTABLE.test(String(value.prospectId ?? "")) || !PORTABLE.test(String(value.organizationFactId ?? "")) || !DIGEST.test(String(value.channelFingerprint ?? ""))) {
    throw new Error("invalid suppression tuple");
  }
}

export function validateMissionControlSuppressionSubmission(value: unknown): asserts value is MissionControlSuppressionSubmission {
  if (!record(value) || !exact(value, SUBMISSION_FIELDS)) throw new Error("invalid suppression submission");
  if (value.schemaVersion !== SUPPRESSION_EVENT_VERSION || !REQUEST.test(String(value.requestId ?? ""))) throw new Error("invalid suppression submission");
  validateSuppressionTuple({ prospectId: value.prospectId, organizationFactId: value.organizationFactId, channelFingerprint: value.channelFingerprint });
  if (!STATES.has(value.state as SuppressionState) || !EVIDENCE.test(String(value.evidenceToken ?? ""))) throw new Error("invalid suppression submission");
}

export async function hashSuppressionEventRevision(event: Omit<SuppressionEvent, "revision">): Promise<string> {
  const value = event as unknown;
  if (!record(value) || !exact(value, EVENT_FIELDS.filter((field) => field !== "revision"))) throw new Error("invalid suppression event");
  validateMissionControlSuppressionSubmission(Object.fromEntries(SUBMISSION_FIELDS.map((field) => [field, value[field]])));
  if (value.actorId !== "jt" || !EVENT.test(String(value.eventId ?? "")) || !Number.isSafeInteger(value.sequence) || Number(value.sequence) < 1 || !utc(value.observedAt)) throw new Error("invalid suppression event");
  return sha256(["outreach-suppression-event-revision-v1\0", canonicalJson(event)]);
}

export async function validateSuppressionEvent(value: unknown): Promise<SuppressionEvent> {
  if (!record(value) || !exact(value, EVENT_FIELDS) || !DIGEST.test(String(value.revision ?? ""))) throw new Error("invalid suppression event");
  const { revision, ...withoutRevision } = value;
  if (await hashSuppressionEventRevision(withoutRevision as Omit<SuppressionEvent, "revision">) !== revision) throw new Error("invalid suppression event");
  return value as SuppressionEvent;
}

async function validateSuppressionOwnerRows(rows: SuppressionEvent[]): Promise<SuppressionEvent[]> {
  const events = await Promise.all(rows.map(validateSuppressionEvent));
  const sequences = new Set<number>();
  const eventIds = new Set<string>();
  const requestIds = new Set<string>();
  for (const event of events) {
    if (sequences.has(event.sequence) || eventIds.has(event.eventId) || requestIds.has(event.requestId)) {
      throw new Error("corrupt suppression owner");
    }
    sequences.add(event.sequence);
    eventIds.add(event.eventId);
    requestIds.add(event.requestId);
  }
  return events.sort((left, right) => left.sequence - right.sequence);
}

export async function hashSuppressionOwnerRevision(owner: string, events: SuppressionEvent[]): Promise<string> {
  if (owner !== SUPPRESSION_OWNER && owner !== "consulting-pipeline") throw new Error("invalid owner");
  const validated = await validateSuppressionOwnerRows(events);
  return sha256([
    "outreach-suppression-owner-revision-v1\0", owner, "\0",
    ...validated.flatMap((event) => [canonicalJson(event), "\n"]),
  ]);
}

function metadata(event: SuppressionEvent): SuppressionEventMetadata {
  return {
    eventId: event.eventId, sequence: event.sequence, state: event.state, actorId: event.actorId,
    evidenceToken: event.evidenceToken, observedAt: event.observedAt, revision: event.revision,
  };
}

export async function resolveSuppressionQuery(owner: string, rows: SuppressionEvent[], tuple: SuppressionTuple, queriedAt: string) {
  validateSuppressionTuple(tuple);
  if (!utc(queriedAt)) throw new Error("invalid query time");
  const events = await validateSuppressionOwnerRows(rows);
  const latest = (items: SuppressionEvent[]) => [...items].sort((a, b) => b.sequence - a.sequence)[0] ?? null;
  const current = latest(events.filter((event) => event.prospectId === tuple.prospectId && event.organizationFactId === tuple.organizationFactId && event.channelFingerprint === tuple.channelFingerprint && ["sent", "manual_hold", "clear"].includes(event.state)));
  const prospectTerminal = latest(events.filter((event) => event.prospectId === tuple.prospectId && ["replied", "opted_out"].includes(event.state)));
  const channelTerminal = latest(events.filter((event) => event.channelFingerprint === tuple.channelFingerprint && event.state === "hard_bounce"));
  const fresh = current?.state === "clear" && Date.parse(queriedAt) >= Date.parse(current.observedAt) && Date.parse(queriedAt) - Date.parse(current.observedAt) <= 15 * 60 * 1000;
  return {
    schemaVersion: SUPPRESSION_QUERY_VERSION,
    owner,
    ...tuple,
    observed: Boolean(current || prospectTerminal || channelTerminal),
    clear: Boolean(fresh && !prospectTerminal && !channelTerminal),
    current: current ? metadata(current) : null,
    prospectTerminal: prospectTerminal ? metadata(prospectTerminal) : null,
    channelTerminal: channelTerminal ? metadata(channelTerminal) : null,
    ownerRevision: await hashSuppressionOwnerRevision(owner, events),
    queriedAt,
  };
}

export async function resolveMissionControlSuppressionAdmission(
  rows: SuppressionEvent[], input: MissionControlSuppressionSubmission, observedAt: string, entropy: string,
) {
  validateMissionControlSuppressionSubmission(input);
  if (!utc(observedAt) || !ENTROPY.test(entropy)) throw new Error("invalid suppression admission");
  const events = await validateSuppressionOwnerRows(rows);
  const duplicate = events.find((event) => event.requestId === input.requestId);
  if (duplicate) {
    const caller = Object.fromEntries(SUBMISSION_FIELDS.map((field) => [field, duplicate[field]]));
    if (canonicalJson(caller) !== canonicalJson(input)) throw new Error("conflict");
    return { operation: "existing" as const, event: duplicate };
  }
  const eventWithoutRevision: Omit<SuppressionEvent, "revision"> = {
    ...input,
    actorId: "jt",
    eventId: `suppression_event_${entropy}`,
    sequence: events.reduce((maximum, event) => Math.max(maximum, event.sequence), 0) + 1,
    observedAt,
  };
  return { operation: "append" as const, event: { ...eventWithoutRevision, revision: await hashSuppressionEventRevision(eventWithoutRevision) } };
}
