// Shared types for the daily cockpit (/cockpit). The display contracts come from the
// design bundle's view model; this file adds the raw task row and the stored run record.
import type {
  DecisionSeries,
  ExceptionLabel,
  FeedbackEntry,
  HandledOutcome,
  ItemFamily,
  RunPhase,
  RunSnapshotEntry,
  Verbatim,
} from "@/docs/design/mission-control-redesign/reference/view-model";

export type { DecisionSeries, ExceptionLabel, FeedbackEntry, HandledOutcome, ItemFamily, RunPhase, Verbatim };

export interface WaitingOn {
  who: string;
  what: string;
  since: number;
  nudgeAfterDays: number;
}

export interface OutreachReviewRecord {
  candidateId?: string;
  cohortId?: string;
  draftSha256?: string;
  subject?: string;
  body?: string;
  verifierReport?: string;
  snapshotSha256?: string;
  reviewCycle?: number;
  [key: string]: unknown;
}

export interface OutreachDecisionRecord {
  decision?: string;
  decidedBy?: string;
  decidedAt?: number;
  [key: string]: unknown;
}

/** One row of GET /api/tasks. Every field is read verbatim; nothing is defaulted. */
export interface RawTask {
  _id: string;
  title?: string;
  description?: string;
  status?: string;
  assignee?: string;
  priority?: string;
  project?: string;
  sortOrder?: number;
  createdAt?: number;
  updatedAt?: number;
  firstAction?: string;
  whyItMatters?: string;
  doneState?: string;
  exactSteps?: string[];
  pasteReadyPrompt?: string;
  pasteDestination?: string;
  evidenceLinks?: string[];
  sourceSystem?: string;
  feedback?: FeedbackEntry[];
  dueDate?: number;
  dueDateSource?: string;
  waitingOn?: WaitingOn;
  snoozedUntil?: number;
  packetSchema?: string;
  payloadHash?: string;
  admittedPayloadHash?: string;
  approvedPayloadHash?: string;
  approvalState?: string;
  expiresAt?: number;
  doneEvidenceType?: string;
  outreachReview?: OutreachReviewRecord;
  outreachDecision?: OutreachDecisionRecord;
  [key: string]: unknown;
}

/** Why an item was left behind without a handling outcome. */
export type LeftReason = "invalid" | "expired" | "readOnly" | "removed";

export interface UndoRecord {
  kind: "start" | "complete" | "defer";
  /** Fields that restore the state before the write. */
  restore: Record<string, unknown>;
}

export interface RunItem {
  id: string;
  outcome?: HandledOutcome;
  left?: LeftReason;
  exception?: ExceptionLabel;
  undo?: UndoRecord;
  /** Status line shown when the item is open again. */
  line?: string;
  /** Plain sentence for the run summary's Handled list. */
  did?: string;
  /** True when the outcome was observed on the record, not written from this run. */
  elsewhere?: boolean;
  parked?: { who: string; nudgeDueAt: number; days: number };
  deferredUntil?: number;
}

/** The fields the change check compares. Feedback and updatedAt are left out on purpose. */
export type TrackedFields = Record<string, unknown>;

export interface SnapshotEntry extends RunSnapshotEntry {
  fingerprint: string;
  fields: TrackedFields;
}

export interface StoredRun {
  version: 1;
  localDate: string;
  phase: RunPhase;
  size: number;
  order: "curated";
  items: RunItem[];
  cursor: number;
  snapshot: SnapshotEntry[];
  /** Every task id present at start or at the last acknowledge. New ids are additions. */
  knownIds: string[];
  /** Task ids present when the run started. Only these may join later as urgent exceptions. */
  startIds: string[];
  startedAt: number;
  rebasedAt: number;
  /** Last time the operator did something in this run; stands in for "when you left". */
  lastSeenAt?: number;
  pausedAt?: number;
  completedAt?: number;
  closedAt?: number;
  unfinished?: boolean;
}

export type ChangeKind = "changed" | "addedToBacklog" | "expired" | "removedFromRun" | "movedUp" | "addedToRun" | "displaced";

export interface RunChange {
  kind: ChangeKind;
  itemId: string;
  title: string;
  where: string;
  detail: string;
  affectsOpenItem: boolean;
  inRun: boolean;
}
