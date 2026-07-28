import type { WaitingOn } from "./types";

export type ClientStage = "active-delivery" | "blocked" | "pending" | "closed-won" | "archived";

export const stageLabel: Record<ClientStage, string> = {
  "active-delivery": "Active delivery",
  blocked: "Blocked",
  pending: "Pending",
  "closed-won": "Closed-won",
  archived: "Archived",
};

export function stageBadgeClassName(stage: ClientStage): string {
  if (stage === "blocked") return "border-red-500/40 bg-red-500/10 text-red-300";
  if (stage === "active-delivery") return "border-emerald-500/40 bg-emerald-500/10 text-emerald-300";
  if (stage === "pending") return "border-amber-500/40 bg-amber-500/10 text-amber-300";
  if (stage === "closed-won") return "border-blue-500/40 bg-blue-500/10 text-blue-300";
  return "border-zinc-700 bg-zinc-900/80 text-zinc-400";
}

// Raw task doc as returned by /api/clients (Convex shape, loosely typed for the UI).
export type ClientTask = {
  _id: string;
  title: string;
  description?: string;
  status: string;
  assignee: "jt" | "eve" | "both";
  priority: "high" | "medium" | "low";
  project?: string;
  clientId?: string;
  dollars?: number;
  stageProbability?: number;
  proofRequired?: boolean;
  updatedAt?: number;
  createdAt?: number;
  [key: string]: unknown;
};

export type ClientPayment = {
  amount: number;
  paidOn: number;
  milestone?: string;
  kind: string;
  cleared: boolean;
  source?: string;
};

export type EnrichedClient = {
  _id: string;
  slug: string;
  name: string;
  emoji?: string;
  stage: ClientStage;
  status?: string;
  waitingOn?: WaitingOn;
  lastTouch?: number;
  memoryPath?: string;
  referralEligible?: boolean;
  payments: ClientPayment[];
  collected: number;
  openDollars: number;
  openTaskCount: number;
  openTasks: ClientTask[];
  completedThisWeek: ClientTask[];
  olderCompletions: ClientTask[];
  statusFile?: { path: string; excerpt: string } | null;
  proofAssets: string[];
};

/** Next uncollected milestone hint for the Money rail. */
export function nextMilestone(client: EnrichedClient): string {
  const pending = client.payments.find((p) => !p.cleared);
  if (pending) return `${pending.milestone ?? "Payment"} — $${pending.amount.toLocaleString("en-US")} pending`;
  if (client.openDollars > 0) return `${client.openTaskCount} open task${client.openTaskCount === 1 ? "" : "s"} carrying $${client.openDollars.toLocaleString("en-US")}`;
  return "No open milestone";
}
