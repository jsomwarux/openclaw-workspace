// View-model types for Mission Control. Types only: no runtime code.
// Enforces the "verbatim or missing" rule from source/product-ux-guide.md, principle 1.
// Task fields come from source/01-data-contract.md section 2.

/** A displayed value is either read verbatim from the record, lifted verbatim from a
 *  description line, or missing. Components must render `missing` as a "Missing" chip.
 *  Never default, infer, trim, summarize or reformat a `value`. */
export type Verbatim<T> =
  | { kind: 'value'; value: T; source: 'field' | 'description' }
  | { kind: 'missing' };

export type ItemFamily = 'generic' | 'decision' | 'lanePacket' | 'outreachReview';
export type DecisionSeries = 'Q' | 'P' | 'AP';

/** Plain-language status shown to the operator. Never show stored enum names. */
export type DisplayStatus =
  | 'Not started' | 'In progress' | 'Waiting' | 'Done' | 'Rejected' | 'Deferred'
  | 'Expired' | 'Awaiting decision' | 'Status not recognized';

/** Run state of an item inside today's run. Lives in run storage, not on the task. */
export type RunItemState = 'handled' | 'current' | 'upNext';

export type ActionId =
  | 'start' | 'complete' | 'approve' | 'reject' | 'defer' | 'block' | 'previous' | 'next';

export type HandledOutcome =
  | 'completed' | 'approved' | 'rejected' | 'parked' | 'deferred';

export interface EvidenceLink { text: string; kind: 'web' | 'file' }

export interface FeedbackEntry {
  id: string;            // "<createdAt>-<n>", server-assigned
  body: string;          // 1 to 4,000 characters, shown in full
  author: 'jt' | 'eve';  // declared by the caller, not verified
  createdAt: number;     // epoch ms
}

export interface AuthorityView {
  approvalState: 'pending' | 'approved' | 'rejected';
  editedAfterAdmission: boolean;      // payloadHash !== admittedPayloadHash
  expiresAt?: number;
  expired: boolean;
  proofRequired?: string;             // plain label, e.g. "application reference"
  guardLine?: string;                 // "Guard:" line from a decision card description, verbatim
}

export interface ExceptionLabel {
  reason: 'approvalExpiresSoon' | 'externalDeadlineOverdue';
  text: string;                       // "Moved up: approval expires in 5 hours (Oct 3, 04:00 UTC)"
}

export interface ItemView {
  id: string;
  family: ItemFamily;
  series?: DecisionSeries;            // decision cards only
  title: Verbatim<string>;
  status: DisplayStatus;
  owner: string;                      // "jt" or "eve", verbatim
  priority: Verbatim<string>;
  firstAction: Verbatim<string>;
  whyItMatters: Verbatim<string>;
  doneState: Verbatim<string>;
  steps: Verbatim<string[]>;
  prompt: Verbatim<string>;           // keep the exact string; Copy copies this
  pasteDestination: Verbatim<string>;
  evidence: Verbatim<EvidenceLink[]>;
  authority?: AuthorityView;          // only when the item needs approval
  exception?: ExceptionLabel;         // only when it jumped ahead of curated order
  freshness: { lastChangedAt: number; createdAt: number };
  source: Verbatim<string>;           // sourceSystem
  project: Verbatim<string>;
  description: Verbatim<string>;
  feedback: FeedbackEntry[];          // empty list renders "None recorded."
  /** Only actions the backend permits for this family and status (README, DECISIONS). */
  actions: ActionId[];
  validity: { ok: true } | { ok: false; reasons: string[] };  // plain-language reasons
}

export interface QueueRow {
  id: string;
  position: number | null;            // null when outside today's run
  group: 'Q' | 'P' | 'AP' | 'Other cards';
  title: string;                      // verbatim
  status: string;                     // Handled | live status | Up next | Not started | Waiting | Done | Expired | Awaiting decision
  owner: string;
  age: string;                        // "2h", "9d"
  blocker: string | null;             // null renders "None recorded"
  inRun: boolean;
  current: boolean;
}

export type RunPhase = 'notStarted' | 'inProgress' | 'paused' | 'queueChanged' | 'complete';

export interface RunSnapshotEntry {
  id: string;
  status: string;
  updatedAt: number;
  payloadHash?: string;
  approvalState?: string;
  expiresAt?: number;
}

export interface RunRecord {
  localDate: string;                  // YYYY-MM-DD in the operator's time zone
  phase: RunPhase;
  size: number;                       // 7
  order: 'curated';
  items: { id: string; state: RunItemState; outcome?: HandledOutcome; deferredOnce?: boolean }[];
  cursor: number;                     // index of the current item
  snapshot: RunSnapshotEntry[];       // taken at start; re-based on acknowledge
  pausedAt?: number;
}

export type ChangeKind = 'changed' | 'addedToBacklog' | 'expired' | 'removedFromRun';
export interface RunChange {
  kind: ChangeKind;
  itemId: string;
  title: string;                      // verbatim
  where: string;                      // "Item 7 of 7" | "Not in today's run"
  detail: string;                     // plain sentence
  affectsOpenItem: boolean;
}

export type ScreenState =
  | 'normal' | 'loading' | 'emptyRun' | 'stale' | 'degraded'
  | 'actionFailed' | 'changedUnderneath' | 'invalidCard' | 'expired';
