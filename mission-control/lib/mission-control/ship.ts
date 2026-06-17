import { sortWorkSignals } from "./work-priority";
import type { Signal } from "./types";

export type ShipSummary = {
  active: number;
  high: number;
  blocked: number;
  proofed: number;
};

export type ShipGroups = {
  apps: Signal[];
  content: Signal[];
  releases: Signal[];
};

function isShipSignal(signal: Signal) {
  return signal.lane === "ship";
}

function isActive(signal: Signal) {
  return signal.status !== "done";
}

function hasVerifiedProof(signal: Signal) {
  return signal.evidence.some((ref) => ref.quality === "verified");
}

function shipKind(signal: Signal): keyof ShipGroups {
  const text = `${signal.project ?? ""} ${signal.title} ${signal.context ?? ""}`.toLowerCase();
  if (/(post|content|draft|linkedin|teardown|thread|x research|swipe|vibe marketing)/.test(text)) return "content";
  if (/(app store|submission|launch|release|ship|implement|share card|export|vendor number)/.test(text)) return "releases";
  return "apps";
}

export function shipSummary(signals: Signal[]): ShipSummary {
  const shipSignals = signals.filter(isShipSignal);
  return {
    active: shipSignals.filter(isActive).length,
    high: shipSignals.filter((signal) => signal.priority === "high").length,
    blocked: shipSignals.filter((signal) => ["blocked", "failed", "stale"].includes(signal.status) || signal.ageDays >= 14).length,
    proofed: shipSignals.filter(hasVerifiedProof).length,
  };
}

export function shipGroups(signals: Signal[]): ShipGroups {
  const groups: ShipGroups = {
    apps: [],
    content: [],
    releases: [],
  };

  for (const signal of sortWorkSignals(signals.filter(isShipSignal))) {
    groups[shipKind(signal)].push(signal);
  }

  return groups;
}
