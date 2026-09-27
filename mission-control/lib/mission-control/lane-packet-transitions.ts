import {
  LANE_PACKET_EDITABLE_PAYLOAD_FIELDS,
  LanePacketError,
  hashLanePacketPayload,
  isDoneEvidenceType,
  isLanePacket,
  isReservedLanePacketDedupeKey,
  isTerminalLanePacket,
  parseHttpUrl,
  type ExternalEvidenceType,
  type StoredLanePacketTask,
} from "./lane-packet";

/**
 * Governed lane-packet transitions. Only these functions may write approval,
 * completion evidence, outcome pointers, or closure reasons. Generic task
 * writes pass through `resolveGenericLanePacketWrite`, which can only ever
 * re-hash an edited payload and downgrade approval, never grant it.
 */

export type LanePacketActor = "jt" | "eve";

export type LanePacketEvidenceInput = { type: ExternalEvidenceType; ref: string };
export type LanePacketOutcomeInput = { system: string; id: string; url?: string };

export type LanePacketTransition =
  | { action: "approve"; payloadHash: string }
  | { action: "reject"; payloadHash: string; note?: string }
  | { action: "complete"; evidence?: LanePacketEvidenceInput; outcomeRef?: LanePacketOutcomeInput }
  | { action: "skip"; note?: string }
  | { action: "no-action"; note?: string };

export type LanePacketTransitionRequest = LanePacketTransition & { id: string };

export type LanePacketTransitionResult =
  | { operation: "patch"; fields: Record<string, unknown> }
  | { operation: "unchanged" };

const DAY_MS = 24 * 60 * 60 * 1000;
const SHA256_PATTERN = /^[a-f0-9]{64}$/;
const JT_ONLY_ACTIONS = new Set(["approve", "reject", "complete"]);
const ACTION_FIELDS: Record<LanePacketTransition["action"], readonly string[]> = {
  approve: ["id", "action", "payloadHash"],
  reject: ["id", "action", "payloadHash", "note"],
  complete: ["id", "action", "evidence", "outcomeRef"],
  skip: ["id", "action", "note"],
  "no-action": ["id", "action", "note"],
};

function fail(code: ConstructorParameters<typeof LanePacketError>[0], message: string): never {
  throw new LanePacketError(code, message);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function boundedText(value: unknown, max: number, message: string): string {
  if (typeof value !== "string") fail("invalid", message);
  const trimmed = value.trim();
  if (!trimmed || trimmed.length > max) fail("invalid", message);
  return trimmed;
}

function parseEvidence(value: unknown): LanePacketEvidenceInput {
  if (!isRecord(value) || Object.keys(value).some((key) => key !== "type" && key !== "ref")) {
    fail("invalid", "evidence must be { type, ref }");
  }
  if (!isDoneEvidenceType(value.type) || value.type === "none") fail("invalid", "evidence type must be an external evidence type");
  return { type: value.type, ref: boundedText(value.ref, 500, "evidence ref must be 1-500 characters") };
}

function parseOutcomeRef(value: unknown): LanePacketOutcomeInput {
  if (!isRecord(value) || Object.keys(value).some((key) => !["system", "id", "url"].includes(key))) {
    fail("invalid", "outcomeRef must be { system, id, url? }");
  }
  const outcome: LanePacketOutcomeInput = {
    system: boundedText(value.system, 100, "outcomeRef.system must be 1-100 characters"),
    id: boundedText(value.id, 300, "outcomeRef.id must be 1-300 characters"),
  };
  if (value.url !== undefined) outcome.url = parseHttpUrl(value.url, "outcomeRef.url");
  return outcome;
}

export function validateLanePacketTransition(input: unknown): LanePacketTransitionRequest {
  if (!isRecord(input)) fail("invalid", "transition must be a JSON object");
  const action = input.action;
  if (typeof action !== "string" || !(action in ACTION_FIELDS)) fail("invalid", "unsupported lane packet action");
  const typedAction = action as LanePacketTransition["action"];
  if (Object.keys(input).some((key) => !ACTION_FIELDS[typedAction].includes(key))) fail("invalid", "unsupported lane packet transition field");
  const id = boundedText(input.id, 100, "id is required");
  const note = input.note === undefined ? undefined : boundedText(input.note, 1000, "note must be 1-1000 characters");
  const withNote = <T extends object>(value: T) => (note === undefined ? value : { ...value, note });

  if (typedAction === "approve" || typedAction === "reject") {
    if (typeof input.payloadHash !== "string" || !SHA256_PATTERN.test(input.payloadHash)) {
      fail("invalid", "payloadHash of the reviewed version is required");
    }
    return typedAction === "approve"
      ? { id, action: "approve", payloadHash: input.payloadHash }
      : withNote({ id, action: "reject" as const, payloadHash: input.payloadHash });
  }
  if (typedAction === "complete") {
    const request: LanePacketTransitionRequest = { id, action: "complete" };
    if (input.evidence !== undefined) request.evidence = parseEvidence(input.evidence);
    if (input.outcomeRef !== undefined) request.outcomeRef = parseOutcomeRef(input.outcomeRef);
    return request;
  }
  return withNote({ id, action: typedAction });
}

function closure(kind: "rejected" | "skipped" | "no-action", actor: LanePacketActor, now: number, note?: string) {
  return note === undefined ? { kind, closedAt: now, closedBy: actor } : { kind, note, closedAt: now, closedBy: actor };
}

/**
 * Pure state machine for one governed transition. The caller has already
 * authenticated `actor`: "jt" only after the Tailscale identity check with the
 * server-held decision capability, "eve" only with the producer capability.
 */
export function resolveLanePacketTransition(
  task: StoredLanePacketTask,
  transition: LanePacketTransition,
  actor: LanePacketActor,
  now: number,
): LanePacketTransitionResult {
  if (!isLanePacket(task)) fail("not_found", "task is not a lane packet");
  if (JT_ONLY_ACTIONS.has(transition.action) && actor !== "jt") {
    fail("forbidden", "only JT can approve, reject, or complete a lane packet");
  }
  if (isTerminalLanePacket(task)) fail("closed", "lane packet is already closed");
  const expired = task.expiresAt !== undefined && now >= task.expiresAt;

  switch (transition.action) {
    case "approve": {
      if (expired) fail("expired", "lane packet expired");
      if (transition.payloadHash !== task.payloadHash) fail("conflict", "payload changed since review; review the current version");
      if (task.approvalState === "approved" && task.approvedPayloadHash === task.payloadHash) return { operation: "unchanged" };
      return {
        operation: "patch",
        fields: { approvalState: "approved", approvedPayloadHash: task.payloadHash, approvedAt: now, updatedAt: now },
      };
    }
    case "reject": {
      if (transition.payloadHash !== task.payloadHash) fail("conflict", "payload changed since review; review the current version");
      return {
        operation: "patch",
        fields: { status: "archived", approvalState: "rejected", closureReason: closure("rejected", actor, now, transition.note), updatedAt: now },
      };
    }
    case "complete": {
      const outcome = transition.outcomeRef ? { outcomeRef: { ...transition.outcomeRef, recordedAt: now } } : {};
      if (task.doneEvidenceType === "none") {
        if (transition.evidence) fail("invalid", "internal lane packets complete without evidence");
        return { operation: "patch", fields: { status: "done", ...outcome, updatedAt: now } };
      }
      const evidence = transition.evidence;
      if (!evidence) fail("invalid", "evidence is required for an external-action lane packet");
      if (evidence.type !== task.doneEvidenceType) fail("invalid", "evidence type must match doneEvidenceType");
      if (evidence.type === "post-url") {
        try {
          parseHttpUrl(evidence.ref, "evidence", true);
        } catch {
          fail("invalid", "post-url evidence must be an https URL");
        }
      }
      if (task.approvalState !== "approved" || task.approvedPayloadHash !== task.payloadHash) {
        fail("conflict", "approve the current payload before recording completion");
      }
      return {
        operation: "patch",
        fields: {
          status: "done",
          doneEvidence: { type: evidence.type, ref: evidence.ref, recordedAt: now, recordedBy: "jt" },
          ...outcome,
          updatedAt: now,
        },
      };
    }
    case "skip":
    case "no-action": {
      const kind = transition.action === "skip" ? "skipped" : "no-action";
      return { operation: "patch", fields: { status: "archived", closureReason: closure(kind, actor, now, transition.note), updatedAt: now } };
    }
  }
}

/** Server-only expiry. Returns the typed closure for an open packet past its expiry, else null. */
export function resolveLanePacketExpiry(task: StoredLanePacketTask, now: number): Record<string, unknown> | null {
  if (!isLanePacket(task) || isTerminalLanePacket(task) || task.expiresAt === undefined || now < task.expiresAt) return null;
  return { status: "archived", closureReason: { kind: "expired", closedAt: now, closedBy: "server" }, updatedAt: now };
}

/**
 * Guard for every generic task write (update, status, pipeline stage). Returns
 * the extra governed fields the server must write alongside the caller's
 * fields, or throws. Legacy tasks pass through unchanged.
 */
export async function resolveGenericLanePacketWrite(
  task: StoredLanePacketTask,
  rawFields: Record<string, unknown>,
  _now: number,
): Promise<Record<string, unknown>> {
  const fields = Object.fromEntries(Object.entries(rawFields).filter(([, value]) => value !== undefined));
  if (!isLanePacket(task)) {
    assertGenericDedupeKey(fields.dedupeKey);
    return {};
  }
  if (isTerminalLanePacket(task)) fail("closed", "closed lane packets are immutable");
  if (fields.dedupeKey !== undefined && fields.dedupeKey !== task.dedupeKey) fail("invalid", "a lane packet's dedupeKey cannot change");
  if (fields.status === "done" && task.doneEvidenceType !== "none") {
    fail("transition_required", "external-action lane packets require evidence-backed completion");
  }
  if (fields.status === "archived") fail("transition_required", "closing a lane packet requires a typed closure reason");
  if (typeof fields.snoozedUntil === "number" && task.expiresAt !== undefined && fields.snoozedUntil > task.expiresAt) {
    fail("invalid", "snooze cannot extend past the packet's expiry");
  }

  if (!LANE_PACKET_EDITABLE_PAYLOAD_FIELDS.some((field) => field in fields)) return {};
  const payloadHash = await hashLanePacketPayload({ ...task, ...fields });
  if (payloadHash === task.payloadHash) return {};
  if (task.approvalState !== "approved") return { payloadHash };
  return { payloadHash, approvalState: "pending", approvedPayloadHash: undefined, approvedAt: undefined };
}

export function assertGenericLanePacketRemoval(task: unknown): void {
  if (isLanePacket(task)) fail("transition_required", "closing a lane packet requires a typed closure reason");
}

export function assertGenericDedupeKey(value: unknown): void {
  if (isReservedLanePacketDedupeKey(value)) fail("invalid", "dedupeKey must not use the reserved lane-packet prefix");
}

/** Snooze for at most `days`, and never past a packet's expiry. */
export function lanePacketSnoozeUntil(expiresAt: number | undefined, now: number, days: number): number {
  const requested = now + days * DAY_MS;
  return expiresAt === undefined ? requested : Math.min(requested, expiresAt);
}
