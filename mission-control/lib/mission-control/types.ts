export type SignalSource = "task" | "cron" | "agent" | "proof";
export type SignalOwner = "jt" | "eve" | "both";
export type SignalStatus =
  | "awaiting-decision"
  | "awaiting-approval"
  | "blocked"
  | "in-progress"
  | "done"
  | "failed"
  | "stale"
  | "archived"
  | "waiting-external"
  | "snoozed";
export type SignalLane = "work" | "revenue" | "ship" | "machine" | "evidence" | "health";
export type SignalPriority = "high" | "medium" | "low";
export type ScoreBand = "high" | "medium" | "low";

export type ProofRef = {
  kind: "file" | "drive" | "url" | "jsonl" | "unknown";
  label: string;
  href?: string;
  quality: "verified" | "partial" | "gap";
};

export type DueDateSource = "external" | "self";

export type WaitingOn = {
  who: string;
  what: string;
  since: number;
  nudgeAfterDays: number;
};

export type Signal = {
  id: string;
  source: SignalSource;
  title: string;
  owner: SignalOwner;
  status: SignalStatus;
  lane: SignalLane;
  priority?: SignalPriority;
  project?: string;
  pipelineStage?: string;
  dollars?: number;
  ageDays: number;
  dueToday?: boolean;
  context?: string;
  eveRead?: string;
  evidence: ProofRef[];
  updatedAt: number;
  raw: unknown;
  score?: number;
  band?: ScoreBand;

  // Scoring inputs — stored on the task, never inferred from text.
  dueDate?: number;
  dueDateSource?: DueDateSource;
  stageProbability?: number;
  effortMinutes?: number;
  proofRequired?: boolean;
  riskContainment?: boolean;
  cashDirect?: boolean;
  blocks?: number;
  blocksAgent?: boolean;
  waitingOn?: WaitingOn;
  snoozedUntil?: number;
  reasonCodes?: string[];
};

// One additive contribution per factor, before modifiers.
export type Factors = {
  cashImpact: number;
  deadlinePressure: number;
  unblockValue: number;
  proofLeverage: number;
  riskContainment: number;
  stability: number;
};

export type ScoreResult = {
  score: number;
  factors: Factors;
  reasonCodes: string[];
};

export type FocusRow = {
  weekOf: string;
  projects: string[];
  gate: number;
};

export type Mandate = "consulting-cash" | "none";

export type ScoreContext = {
  focus?: FocusRow | null;
  mandate?: Mandate;
  /** Cash collected so far against the focus row's gate. */
  collected?: number;
  now?: number;
};
