import { hashCanonicalJson } from "./canonical-json";
import type { SignalLane, SignalPriority, Workstream } from "./types";

/**
 * Growth OS card envelope v1: the generic cross-lane machine contract.
 *
 * A lane packet is a human decision card admitted by a producer through
 * `POST /api/tasks/lane-packet`. The server derives every governed field
 * (approval, payload hash, completion evidence, outcome, closure); producers
 * supply only card content, the artifact pointer, and scheduling metadata.
 *
 * Outreach keeps its specialized immutable review/decision routes. Nothing in
 * this module reads, creates, or mutates an outreach review snapshot or decision.
 */

export const LANE_PACKET_SCHEMA = "lane-packet-v1" as const;

export const GROWTH_LANES = [
  "linkedin",
  "x",
  "outreach",
  "jobs",
  "apps",
  "passive-income",
  "networking",
  "profile-site",
] as const;
export type GrowthLane = (typeof GROWTH_LANES)[number];

/** The evidence JT records when the external action is done. `none` marks an internal card. */
export const DONE_EVIDENCE_TYPES = [
  "post-url",
  "message-ref",
  "application-ref",
  "rsvp-ref",
  "profile-edit-ref",
  "deploy-ref",
  "none",
] as const;
export type DoneEvidenceType = (typeof DONE_EVIDENCE_TYPES)[number];
export type ExternalEvidenceType = Exclude<DoneEvidenceType, "none">;

export const APPROVAL_STATES = ["pending", "approved", "rejected"] as const;
export type ApprovalState = (typeof APPROVAL_STATES)[number];

export const CLOSURE_KINDS = ["rejected", "skipped", "expired", "no-action"] as const;
export type ClosureKind = (typeof CLOSURE_KINDS)[number];

export type ArtifactRef = { system: string; id: string; url?: string; sha256: string };
export type OutcomeRef = { system: string; id: string; url?: string; recordedAt: number };
export type DoneEvidence = { type: ExternalEvidenceType; ref: string; recordedAt: number; recordedBy: "jt" };
export type ClosureReason = { kind: ClosureKind; note?: string; closedAt: number; closedBy: "jt" | "eve" | "server" };

export type LanePacketErrorCode =
  | "invalid"
  | "conflict"
  | "not_found"
  | "forbidden"
  | "closed"
  | "expired"
  | "transition_required";

/** Every message is a fixed string. Messages never interpolate caller input. */
export class LanePacketError extends Error {
  constructor(readonly code: LanePacketErrorCode, message: string) {
    super(message);
  }
}

export type LanePacketSubmission = {
  lane: GrowthLane;
  dedupeKey: string;
  sourceSystem: string;
  title: string;
  description?: string;
  firstAction?: string;
  whyItMatters: string;
  exactSteps: string[];
  pasteReadyPrompt?: string;
  pasteDestination?: string;
  doneState: string;
  artifactRef: ArtifactRef;
  doneEvidenceType: DoneEvidenceType;
  expiresAt: number;
  estMinutes: number;
  evidenceLinks?: string[];
  project?: string;
  priority?: SignalPriority;
  dueDate?: number;
  dueDateSource?: "external" | "self";
  dollars?: number;
  stageProbability?: number;
  cashDirect?: boolean;
  proofRequired?: boolean;
  riskContainment?: boolean;
  blocks?: number;
  workstream?: Workstream;
  /** Optional producer assertion; admission fails unless it equals the server-computed hash. */
  payloadHash?: string;
};

/** The stored-task shape the lane-packet helpers read. Legacy rows carry none of the envelope. */
export type StoredLanePacketTask = {
  _id: string;
  title?: string;
  status?: string;
  dedupeKey?: string;
  packetSchema?: typeof LANE_PACKET_SCHEMA;
  growthLane?: GrowthLane;
  description?: string;
  firstAction?: string;
  whyItMatters?: string;
  exactSteps?: string[];
  pasteReadyPrompt?: string;
  pasteDestination?: string;
  doneState?: string;
  artifactRef?: ArtifactRef;
  payloadHash?: string;
  admittedPayloadHash?: string;
  approvalState?: ApprovalState;
  approvedPayloadHash?: string;
  approvedAt?: number;
  expiresAt?: number;
  estMinutes?: number;
  doneEvidenceType?: DoneEvidenceType;
  doneEvidence?: DoneEvidence;
  outcomeRef?: OutcomeRef;
  closureReason?: ClosureReason;
  outreachReview?: unknown;
  outreachDecision?: unknown;
};

const DAY_MS = 24 * 60 * 60 * 1000;
export const MAX_EXPIRY_HORIZON_MS = 90 * DAY_MS;
export const MAX_EST_MINUTES = 480;
export const LANE_PACKET_DEDUPE_PREFIX = "lane-packet:";
const SHA256_PATTERN = /^[a-f0-9]{64}$/;
const DEDUPE_KEY_PATTERN = /^[A-Za-z0-9._:/-]{1,200}$/;
const SOURCE_SYSTEM_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$/;
const NIGHTLY_SOURCE = "nightly-validation-controller";
const WORKSTREAMS: readonly Workstream[] = ["paid-delivery", "career-hedge", "compounding-bet", "administrative", "other"];
const PRIORITIES: readonly SignalPriority[] = ["high", "medium", "low"];

/** Card content JT approves. Editing any of these creates a new payload hash. */
export const LANE_PACKET_EDITABLE_PAYLOAD_FIELDS = [
  "title",
  "description",
  "firstAction",
  "whyItMatters",
  "exactSteps",
  "pasteReadyPrompt",
  "pasteDestination",
  "doneState",
] as const;

const SUBMISSION_FIELDS = new Set<string>([
  "lane", "dedupeKey", "sourceSystem", ...LANE_PACKET_EDITABLE_PAYLOAD_FIELDS,
  "artifactRef", "doneEvidenceType", "expiresAt", "estMinutes", "evidenceLinks", "project", "priority",
  "dueDate", "dueDateSource", "dollars", "stageProbability", "cashDirect", "proofRequired",
  "riskContainment", "blocks", "workstream", "payloadHash",
]);

/** Fields that only the server may write on a lane packet. */
export const LANE_PACKET_GOVERNED_FIELDS = [
  "packetSchema", "growthLane", "artifactRef", "payloadHash", "admittedPayloadHash", "approvalState",
  "approvedPayloadHash", "approvedAt", "expiresAt", "estMinutes", "doneEvidenceType", "doneEvidence",
  "outcomeRef", "closureReason",
] as const;

const FORGED_SUBMISSION_FIELDS = new Set<string>([
  ...LANE_PACKET_GOVERNED_FIELDS.filter((field) => !SUBMISSION_FIELDS.has(field)),
  "status", "assignee", "feedback", "reasonCodes", "rankScore", "rankUpdatedAt", "sortOrder",
  "snoozedUntil", "waitingOn", "createdAt", "updatedAt",
]);

const OUTREACH_FIELDS = new Set<string>([
  "outreachReview", "outreachDecision", "candidateId", "cohortId", "draftSha256", "snapshotSha256",
  "reviewCycle", "decision", "decidedBy", "decidedAt", "suppressionBinding", "suppressionAttestation",
  "verifierReport", "reviewAuthorityId", "verifierActorId", "gitBindings",
]);

const SIGNAL_LANE_BY_GROWTH_LANE: Record<GrowthLane, SignalLane> = {
  linkedin: "ship",
  x: "ship",
  outreach: "revenue",
  jobs: "revenue",
  apps: "ship",
  "passive-income": "ship",
  networking: "work",
  "profile-site": "ship",
};

function invalid(message: string): never {
  throw new LanePacketError("invalid", message);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

export function isGrowthLane(value: unknown): value is GrowthLane {
  return typeof value === "string" && (GROWTH_LANES as readonly string[]).includes(value);
}

export function isDoneEvidenceType(value: unknown): value is DoneEvidenceType {
  return typeof value === "string" && (DONE_EVIDENCE_TYPES as readonly string[]).includes(value);
}

export function signalLaneForGrowthLane(lane: GrowthLane): SignalLane {
  return SIGNAL_LANE_BY_GROWTH_LANE[lane];
}

export function lanePacketDedupeKey(lane: GrowthLane, producerKey: string): string {
  return `${LANE_PACKET_DEDUPE_PREFIX}v1:${lane}:${producerKey}`;
}

export function isReservedLanePacketDedupeKey(value: unknown): boolean {
  return typeof value === "string" && value.startsWith(LANE_PACKET_DEDUPE_PREFIX);
}

export function isLanePacket(task: unknown): task is StoredLanePacketTask {
  return isRecord(task) && task.packetSchema === LANE_PACKET_SCHEMA && isGrowthLane(task.growthLane);
}

/** A packet is terminal once it has a typed closure or recorded completion. */
export function isTerminalLanePacket(task: StoredLanePacketTask): boolean {
  return Boolean(task.closureReason) || task.status === "done" || task.status === "archived";
}

function requiredText(value: unknown, max: number, field: string): string {
  if (typeof value !== "string") invalid(`${field} is required`);
  const trimmed = value.trim();
  if (!trimmed) invalid(`${field} is required`);
  if (trimmed.length > max) invalid(`${field} is too long`);
  return trimmed;
}

function optionalText(value: unknown, max: number, field: string): string | undefined {
  if (value === undefined) return undefined;
  return requiredText(value, max, field);
}

export function parseHttpUrl(value: unknown, field: string, httpsOnly = false): string {
  if (typeof value !== "string" || value.length > 2000) invalid(`${field} must be an http(s) URL`);
  let url: URL;
  try {
    url = new URL(value);
  } catch {
    invalid(`${field} must be an http(s) URL`);
  }
  const allowed = httpsOnly ? ["https:"] : ["https:", "http:"];
  if (!allowed.includes(url.protocol)) invalid(httpsOnly ? `${field} must be an https URL` : `${field} must be an http(s) URL`);
  return value;
}

function parseArtifactRef(value: unknown): ArtifactRef {
  if (!isRecord(value)) invalid("artifactRef is required");
  if (Object.keys(value).some((key) => !["system", "id", "url", "sha256"].includes(key))) {
    invalid("artifactRef has an unsupported field");
  }
  const system = requiredText(value.system, 100, "artifactRef.system");
  const id = requiredText(value.id, 300, "artifactRef.id");
  if (typeof value.sha256 !== "string" || !SHA256_PATTERN.test(value.sha256)) {
    invalid("artifactRef.sha256 must be 64 lowercase hex characters");
  }
  const ref: ArtifactRef = { system, id, sha256: value.sha256 };
  if (value.url !== undefined) ref.url = parseHttpUrl(value.url, "artifactRef.url");
  return ref;
}

function parseFiniteNumber(value: unknown, field: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) invalid(`${field} must be a finite number`);
  return value;
}

function parseBoolean(value: unknown, field: string): boolean | undefined {
  if (value === undefined) return undefined;
  if (typeof value !== "boolean") invalid(`${field} must be a boolean`);
  return value;
}

/**
 * Strict allowlist validation. Forged governed fields and outreach fields are
 * named explicitly so a producer learns why instead of seeing them dropped.
 */
export function validateLanePacketSubmission(input: unknown, now: number): LanePacketSubmission {
  if (!isRecord(input)) invalid("lane packet must be a JSON object");
  for (const key of Object.keys(input)) {
    if (OUTREACH_FIELDS.has(key)) invalid("outreach review and decision state requires the specialized outreach routes");
  }
  for (const key of Object.keys(input)) {
    if (FORGED_SUBMISSION_FIELDS.has(key)) invalid("governed lane packet fields are server-derived");
  }
  for (const key of Object.keys(input)) {
    if (!SUBMISSION_FIELDS.has(key)) invalid("unsupported lane packet field");
  }

  if (!isGrowthLane(input.lane)) invalid("lane must be one of the eight Growth OS lanes");
  if (typeof input.dedupeKey !== "string" || !DEDUPE_KEY_PATTERN.test(input.dedupeKey)) {
    invalid("dedupeKey must be 1-200 characters of letters, digits, and . _ : / -");
  }
  if (isReservedLanePacketDedupeKey(input.dedupeKey)) invalid("dedupeKey must not use the reserved lane-packet prefix");
  if (typeof input.sourceSystem !== "string" || !SOURCE_SYSTEM_PATTERN.test(input.sourceSystem)) {
    invalid("sourceSystem must identify the producer");
  }
  if (input.sourceSystem === NIGHTLY_SOURCE) invalid("nightly controller cards use nightly admission");

  if (!Array.isArray(input.exactSteps) || input.exactSteps.length === 0 || input.exactSteps.length > 20) {
    invalid("exactSteps must list 1-20 steps");
  }
  const exactSteps = input.exactSteps.map((step) => requiredText(step, 1000, "exactSteps"));

  const pasteReadyPrompt = optionalText(input.pasteReadyPrompt, 20_000, "pasteReadyPrompt");
  const pasteDestination = optionalText(input.pasteDestination, 300, "pasteDestination");
  if (pasteReadyPrompt !== undefined && pasteDestination === undefined) invalid("pasteDestination is required with pasteReadyPrompt");

  if (!isDoneEvidenceType(input.doneEvidenceType)) invalid("doneEvidenceType must be an enumerated evidence type");
  const expiresAt = parseFiniteNumber(input.expiresAt, "expiresAt");
  if (expiresAt <= now || expiresAt > now + MAX_EXPIRY_HORIZON_MS) invalid("expiresAt must be in the future and within 90 days");
  const estMinutes = parseFiniteNumber(input.estMinutes, "estMinutes");
  if (!Number.isInteger(estMinutes) || estMinutes < 1 || estMinutes > MAX_EST_MINUTES) {
    invalid("estMinutes must be a whole number from 1 to 480");
  }

  const submission: LanePacketSubmission = {
    lane: input.lane,
    dedupeKey: input.dedupeKey,
    sourceSystem: input.sourceSystem,
    title: requiredText(input.title, 300, "title"),
    whyItMatters: requiredText(input.whyItMatters, 2000, "whyItMatters"),
    exactSteps,
    doneState: requiredText(input.doneState, 2000, "doneState"),
    artifactRef: parseArtifactRef(input.artifactRef),
    doneEvidenceType: input.doneEvidenceType,
    expiresAt,
    estMinutes,
  };
  const description = optionalText(input.description, 4000, "description");
  if (description !== undefined) submission.description = description;
  const firstAction = optionalText(input.firstAction, 1000, "firstAction");
  if (firstAction !== undefined) submission.firstAction = firstAction;
  if (pasteReadyPrompt !== undefined) submission.pasteReadyPrompt = pasteReadyPrompt;
  if (pasteDestination !== undefined) submission.pasteDestination = pasteDestination;

  if (input.evidenceLinks !== undefined) {
    if (!Array.isArray(input.evidenceLinks) || input.evidenceLinks.length > 20) invalid("evidenceLinks must list at most 20 links");
    submission.evidenceLinks = input.evidenceLinks.map((link) => requiredText(link, 2000, "evidenceLinks"));
  }
  const project = optionalText(input.project, 100, "project");
  if (project !== undefined) submission.project = project;
  if (input.priority !== undefined) {
    if (!PRIORITIES.includes(input.priority as SignalPriority)) invalid("priority must be high, medium, or low");
    submission.priority = input.priority as SignalPriority;
  }
  if (input.dueDate !== undefined) submission.dueDate = parseFiniteNumber(input.dueDate, "dueDate");
  if (input.dueDateSource !== undefined) {
    if (input.dueDateSource !== "external" && input.dueDateSource !== "self") invalid("dueDateSource must be external or self");
    if (submission.dueDate === undefined) invalid("dueDateSource requires dueDate");
    submission.dueDateSource = input.dueDateSource;
  }
  if (input.dollars !== undefined) {
    const dollars = parseFiniteNumber(input.dollars, "dollars");
    if (dollars < 0) invalid("dollars must not be negative");
    submission.dollars = dollars;
  }
  if (input.stageProbability !== undefined) {
    const probability = parseFiniteNumber(input.stageProbability, "stageProbability");
    if (probability < 0 || probability > 1) invalid("stageProbability must be between 0 and 1");
    submission.stageProbability = probability;
  }
  const cashDirect = parseBoolean(input.cashDirect, "cashDirect");
  if (cashDirect !== undefined) submission.cashDirect = cashDirect;
  const proofRequired = parseBoolean(input.proofRequired, "proofRequired");
  if (proofRequired !== undefined) submission.proofRequired = proofRequired;
  const riskContainment = parseBoolean(input.riskContainment, "riskContainment");
  if (riskContainment !== undefined) submission.riskContainment = riskContainment;
  if (input.blocks !== undefined) {
    const blocks = parseFiniteNumber(input.blocks, "blocks");
    if (!Number.isInteger(blocks) || blocks < 0 || blocks > 100) invalid("blocks must be a whole number from 0 to 100");
    submission.blocks = blocks;
  }
  if (input.workstream !== undefined) {
    if (!WORKSTREAMS.includes(input.workstream as Workstream)) invalid("invalid workstream");
    submission.workstream = input.workstream as Workstream;
  }
  if (input.payloadHash !== undefined) {
    if (typeof input.payloadHash !== "string" || !SHA256_PATTERN.test(input.payloadHash)) {
      invalid("payloadHash must be 64 lowercase hex characters");
    }
    submission.payloadHash = input.payloadHash;
  }
  return submission;
}

type PayloadSource = {
  growthLane?: GrowthLane;
  lane?: unknown;
  artifactRef?: ArtifactRef;
  doneEvidenceType?: DoneEvidenceType;
} & Partial<Record<(typeof LANE_PACKET_EDITABLE_PAYLOAD_FIELDS)[number], unknown>>;

/** The canonical approved content: card text plus the immutable lane, artifact, and evidence contract. */
export function lanePacketPayload(source: PayloadSource): Record<string, unknown> {
  const lane = source.growthLane ?? source.lane;
  const payload: Record<string, unknown> = {
    schema: "lane-packet-payload-v1",
    lane,
    artifactRef: source.artifactRef,
    doneEvidenceType: source.doneEvidenceType,
  };
  for (const field of LANE_PACKET_EDITABLE_PAYLOAD_FIELDS) {
    if (source[field] !== undefined) payload[field] = source[field];
  }
  return payload;
}

export async function hashLanePacketPayload(source: PayloadSource): Promise<string> {
  return hashCanonicalJson(lanePacketPayload(source));
}

/** The exact row admission inserts: producer content plus server-derived envelope. */
export type LanePacketCreateFields = Omit<LanePacketSubmission, "lane" | "dedupeKey" | "priority" | "payloadHash"> & {
  status: "todo";
  assignee: "jt";
  priority: SignalPriority;
  lane: SignalLane;
  dedupeKey: string;
  packetSchema: typeof LANE_PACKET_SCHEMA;
  growthLane: GrowthLane;
  payloadHash: string;
  admittedPayloadHash: string;
  approvalState: "pending";
  createdAt: number;
  updatedAt: number;
};

export type LanePacketAdmission =
  | {
      operation: "existing";
      id: string;
      dedupeKey: string;
      payloadHash: string;
      approvalState: ApprovalState;
    }
  | { operation: "create"; fields: LanePacketCreateFields };

function withoutUndefined<T extends object>(value: T): T {
  return Object.fromEntries(Object.entries(value).filter(([, entry]) => entry !== undefined)) as T;
}

/**
 * Create-only admission keyed by the namespaced dedupeKey plus the admitted
 * payload hash. `existing` must be every stored row carrying that dedupeKey.
 * It never returns a patch: an existing packet is reported, never rewritten.
 */
export async function resolveLanePacketAdmission(
  existing: StoredLanePacketTask[],
  submission: LanePacketSubmission,
  now: number,
): Promise<LanePacketAdmission> {
  const payloadHash = await hashLanePacketPayload({ ...submission, growthLane: submission.lane });
  if (submission.payloadHash !== undefined && submission.payloadHash !== payloadHash) {
    invalid("payloadHash does not match the server-computed payload hash");
  }
  const dedupeKey = lanePacketDedupeKey(submission.lane, submission.dedupeKey);

  if (existing.some((task) => !isLanePacket(task) || task.growthLane !== submission.lane)) {
    throw new LanePacketError("conflict", "dedupeKey belongs to a task that is not a lane packet");
  }
  const sameVersion = existing.filter((task) => task.admittedPayloadHash === payloadHash);
  if (sameVersion.length > 1) throw new LanePacketError("conflict", "duplicate lane packet versions share this payload");
  if (sameVersion.length === 1) {
    const task = sameVersion[0];
    return {
      operation: "existing",
      id: task._id,
      dedupeKey,
      payloadHash: task.payloadHash ?? payloadHash,
      approvalState: task.approvalState ?? "pending",
    };
  }
  if (existing.some((task) => !isTerminalLanePacket(task))) {
    throw new LanePacketError("conflict", "an open lane packet with this dedupeKey has a different payload");
  }

  const { lane, dedupeKey: _producerKey, payloadHash: _asserted, priority, ...content } = submission;
  const fields: LanePacketCreateFields = withoutUndefined({
    ...content,
    status: "todo",
    assignee: "jt",
    priority: priority ?? "medium",
    lane: signalLaneForGrowthLane(lane),
    dedupeKey,
    packetSchema: LANE_PACKET_SCHEMA,
    growthLane: lane,
    payloadHash,
    admittedPayloadHash: payloadHash,
    approvalState: "pending",
    createdAt: now,
    updatedAt: now,
  });
  return { operation: "create", fields };
}
