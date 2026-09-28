import { LANE_PACKET_SCHEMA, type ApprovalState, type ClosureKind, type DoneEvidenceType, type GrowthLane } from "./lane-packet";
import type { Signal } from "./types";

export const GROWTH_LANE_LABELS: Record<GrowthLane, string> = {
  linkedin: "LinkedIn",
  x: "X",
  outreach: "Outreach",
  jobs: "Jobs",
  apps: "Apps",
  "passive-income": "Passive income",
  networking: "Networking",
  "profile-site": "Profile/site",
};

export const EVIDENCE_LABELS: Record<DoneEvidenceType, string> = {
  "post-url": "Post URL",
  "message-ref": "Sent message reference",
  "application-ref": "Application confirmation",
  "rsvp-ref": "RSVP confirmation",
  "profile-edit-ref": "Profile edit reference",
  "deploy-ref": "Deploy reference",
  none: "None (internal card)",
};

const APPROVAL_LABELS: Record<ApprovalState, string> = {
  pending: "Pending approval",
  approved: "Approved",
  rejected: "Rejected",
};

const CLOSURE_LABELS: Record<ClosureKind, string> = {
  rejected: "Rejected",
  skipped: "Skipped",
  expired: "Expired",
  "no-action": "No action",
};

const ACTOR_LABELS = { jt: "JT", eve: "Eve", server: "Mission Control" } as const;

const DATE_TIME = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  hour: "numeric",
  minute: "2-digit",
  timeZone: "America/New_York",
});

export function isLanePacketSignal(signal: Signal): boolean {
  return signal.packetSchema === LANE_PACKET_SCHEMA && Boolean(signal.growthLane);
}

function isTerminal(signal: Signal): boolean {
  return Boolean(signal.closureReason) || signal.status === "done" || signal.status === "archived";
}

/** Envelope rows for the drawer, in reading order. */
export function lanePacketDetails(signal: Signal): Array<[string, string]> {
  if (!isLanePacketSignal(signal) || !signal.growthLane) return [];
  const rows: Array<[string, string]> = [["Lane", GROWTH_LANE_LABELS[signal.growthLane]]];
  if (signal.approvalState) rows.push(["Approval", APPROVAL_LABELS[signal.approvalState]]);
  if (signal.doneEvidenceType) rows.push(["Evidence required", EVIDENCE_LABELS[signal.doneEvidenceType]]);
  if (typeof signal.estMinutes === "number") rows.push(["Estimated time", `${signal.estMinutes} min`]);
  if (typeof signal.expiresAt === "number") rows.push(["Expires", DATE_TIME.format(new Date(signal.expiresAt))]);
  if (signal.artifactRef) rows.push(["Artifact", `${signal.artifactRef.system} · ${signal.artifactRef.id}`]);
  if (signal.payloadHash) rows.push(["Version", signal.payloadHash.slice(0, 12)]);
  if (signal.doneEvidence) rows.push(["Evidence recorded", `${EVIDENCE_LABELS[signal.doneEvidence.type]}: ${signal.doneEvidence.ref}`]);
  if (signal.outcomeRef) rows.push(["Outcome", `${signal.outcomeRef.system} · ${signal.outcomeRef.id}`]);
  if (signal.closureReason) {
    const { kind, closedBy, note } = signal.closureReason;
    rows.push(["Closed", `${CLOSURE_LABELS[kind]} by ${ACTOR_LABELS[closedBy]}${note ? ` — ${note}` : ""}`]);
  }
  return rows;
}

export type LanePacketActions = {
  canApprove: boolean;
  canComplete: boolean;
  needsEvidence: boolean;
  canClose: boolean;
};

/** Mirrors the server state machine so the drawer only offers transitions that can succeed. */
export function lanePacketActions(signal: Signal, now: number): LanePacketActions {
  const needsEvidence = signal.doneEvidenceType !== "none";
  if (isTerminal(signal)) return { canApprove: false, canComplete: false, needsEvidence, canClose: false };
  const expired = typeof signal.expiresAt === "number" && now >= signal.expiresAt;
  const approvedCurrent = signal.approvalState === "approved" && signal.approvedPayloadHash === signal.payloadHash;
  return {
    canApprove: !expired && signal.approvalState === "pending",
    canComplete: needsEvidence ? approvedCurrent : true,
    needsEvidence,
    canClose: true,
  };
}
