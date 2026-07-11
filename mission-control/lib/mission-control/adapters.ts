import type {
  DueDateSource,
  ProofRef,
  Signal,
  SignalLane,
  SignalOwner,
  SignalPriority,
  SignalStatus,
  WaitingOn,
} from "./types";

type RawTask = {
  _id?: string;
  id?: string;
  title: string;
  description?: string;
  status: "todo" | "in-progress" | "done" | "archived" | "waiting-external" | "snoozed";
  assignee: SignalOwner;
  priority: SignalPriority;
  project?: string;
  pipelineStage?: string;
  updatedAt?: number;
  createdAt?: number;
  lane?: string;
  dueDate?: number;
  dueDateSource?: DueDateSource;
  dollars?: number;
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

type RawCron = {
  jobId?: string;
  id?: string;
  name?: string;
  enabled?: boolean;
  failed?: boolean;
  running?: boolean;
  lastRun?: number | null;
  nextRun?: number | null;
  payload?: string;
  schedule?: unknown;
};

type RawAgent = {
  id: string;
  name: string;
  role?: string;
  domain?: string;
  status?: string;
  currentTask?: string;
  created?: string | null;
};

type RawProof = {
  id?: string;
  proof_id?: string;
  title?: string;
  action_type?: string;
  outcome?: string;
  date?: string;
  files?: string[];
  timestamp?: string;
  ts?: string;
};

const URL_PATTERN = /(https?:\/\/[^\s)]+)/g;
const DAY_MS = 24 * 60 * 60 * 1000;

function ageDays(updatedAt?: number): number {
  if (!updatedAt) return 0;
  return Math.max(0, Math.floor((Date.now() - updatedAt) / DAY_MS));
}

const LANES: SignalLane[] = ["work", "revenue", "ship", "machine", "evidence", "health"];

function isLane(value?: string): value is SignalLane {
  return Boolean(value) && LANES.includes(value as SignalLane);
}

// Stored lane wins. The regex is a fallback for tasks written before lanes existed.
function laneForProject(project?: string, title = "", stored?: string): SignalLane {
  if (isLane(stored)) return stored;
  const haystack = `${project ?? ""} ${title}`.toLowerCase();
  if (/(consult|pipeline|job|apply|client|altmark|revenue|sales|outreach)/.test(haystack)) return "revenue";
  if (/(app|vista|nash|glow|action arena|content|vibe|passive|marketing|ship)/.test(haystack)) return "ship";
  if (/(cron|agent|automation|gateway|system|mission control)/.test(haystack)) return "machine";
  if (/(proof|memory|audit|overnight)/.test(haystack)) return "evidence";
  if (/(cost|health|monitor|error|failure|outage)/.test(haystack)) return "health";
  return "work";
}

// A todo owned by JT is just work in flight. Only a shared high-priority task is
// a real approval gate; ownership alone is not a decision.
function taskStatusToSignal(task: RawTask): SignalStatus {
  if (task.status === "done") return "done";
  if (task.status === "archived") return "archived";
  if (task.status === "waiting-external") return "waiting-external";
  if (task.status === "snoozed") return "snoozed";
  if (task.status === "in-progress") return "in-progress";
  if (task.assignee === "both" && task.priority === "high") return "awaiting-approval";
  return "in-progress";
}

export function extractEvidence(text = ""): ProofRef[] {
  const urls = text.match(URL_PATTERN) ?? [];
  return urls.map((href, index) => ({
    kind: href.includes("docs.google.com") || href.includes("drive.google.com") ? "drive" : "url",
    label: href.includes("docs.google.com") ? `Google Doc ${index + 1}` : `Link ${index + 1}`,
    href,
    quality: "verified",
  }));
}

export function taskToSignal(task: RawTask): Signal {
  const updatedAt = task.updatedAt ?? task.createdAt ?? Date.now();
  return {
    id: task._id ?? task.id ?? task.title,
    source: "task",
    title: task.title,
    owner: task.assignee,
    status: taskStatusToSignal(task),
    lane: laneForProject(task.project, task.title, task.lane),
    priority: task.priority,
    project: task.project,
    ageDays: ageDays(updatedAt),
    context: task.description,
    evidence: extractEvidence(task.description),
    updatedAt,
    dollars: task.dollars,
    dueDate: task.dueDate,
    dueDateSource: task.dueDateSource,
    stageProbability: task.stageProbability,
    effortMinutes: task.effortMinutes,
    proofRequired: task.proofRequired,
    riskContainment: task.riskContainment,
    cashDirect: task.cashDirect,
    blocks: task.blocks,
    blocksAgent: task.blocksAgent,
    waitingOn: task.waitingOn,
    snoozedUntil: task.snoozedUntil,
    reasonCodes: task.reasonCodes,
    raw: task,
  };
}

export function cronToSignal(cron: RawCron): Signal {
  const id = cron.jobId ?? cron.id ?? cron.name ?? "cron";
  const updatedAt = cron.lastRun ?? Date.now();
  const failed = Boolean(cron.failed);
  const running = Boolean(cron.running);
  return {
    id: `cron-${id}`,
    source: "cron",
    title: cron.name ?? id,
    owner: "eve",
    status: failed ? "failed" : running ? "in-progress" : "done",
    lane: "machine",
    priority: failed ? "high" : "low",
    ageDays: ageDays(updatedAt),
    context: `Payload: ${cron.payload ?? "unknown"}`,
    evidence: [],
    updatedAt,
    raw: cron,
  };
}

export function agentToSignal(agent: RawAgent): Signal {
  const active = agent.status === "active";
  return {
    id: `agent-${agent.id}`,
    source: "agent",
    title: agent.name,
    owner: "eve",
    status: active ? "in-progress" : "stale",
    lane: "machine",
    priority: active ? "medium" : "low",
    ageDays: 0,
    context: [agent.role, agent.domain].filter(Boolean).join(" · "),
    eveRead: agent.currentTask,
    evidence: [],
    updatedAt: Date.now(),
    raw: agent,
  };
}

export function proofToSignal(proof: RawProof): Signal {
  const id = proof.id ?? proof.proof_id ?? proof.title ?? `${proof.action_type}-${proof.date}`;
  const timestamp = proof.timestamp ?? proof.ts;
  const updatedAt = timestamp ? Date.parse(timestamp) : Date.now();
  const files = proof.files ?? [];
  return {
    id: `proof-${id}`,
    source: "proof",
    title: proof.title ?? proof.action_type ?? "Proof entry",
    owner: "eve",
    status: proof.outcome === "failure" ? "failed" : "done",
    lane: "evidence",
    priority: proof.outcome === "failure" ? "high" : "low",
    ageDays: ageDays(Number.isNaN(updatedAt) ? Date.now() : updatedAt),
    context: proof.action_type,
    evidence: files.length
      ? files.map((file) => ({ kind: "file", label: file, href: file, quality: "verified" }))
      : [{ kind: "unknown", label: "No proof ref", quality: "gap" }],
    updatedAt: Number.isNaN(updatedAt) ? Date.now() : updatedAt,
    raw: proof,
  };
}
