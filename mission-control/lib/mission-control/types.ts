export type SignalSource = "task" | "cron" | "agent" | "proof";
export type SignalOwner = "jt" | "eve" | "both";
export type SignalStatus =
  | "awaiting-decision"
  | "awaiting-approval"
  | "blocked"
  | "in-progress"
  | "done"
  | "failed"
  | "stale";
export type SignalLane = "work" | "revenue" | "ship" | "machine" | "evidence" | "health";
export type SignalPriority = "high" | "medium" | "low";
export type ScoreBand = "high" | "medium" | "low";

export type ProofRef = {
  kind: "file" | "drive" | "url" | "jsonl" | "unknown";
  label: string;
  href?: string;
  quality: "verified" | "partial" | "gap";
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
};

export type Factors = {
  revenue: 0 | 1 | 2 | 3;
  unblock: 0 | 1 | 2 | 3;
  urgency: 0 | 1 | 2 | 3;
  risk: 0 | 1 | 2 | 3;
  northStar: 0 | 1 | 2 | 3;
  effortOver30: boolean;
};
