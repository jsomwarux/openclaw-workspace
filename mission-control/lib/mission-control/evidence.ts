import { sortWorkSignals } from "./work-priority";
import type { Signal } from "./types";

export type EvidenceSummary = {
  total: number;
  verified: number;
  gaps: number;
  failures: number;
  latestTitle: string;
};

export type EvidenceGroups = {
  buyer: Signal[];
  system: Signal[];
  content: Signal[];
  gaps: Signal[];
};

function isEvidenceSignal(signal: Signal) {
  return signal.lane === "evidence";
}

function hasProofGap(signal: Signal) {
  return signal.evidence.length === 0 || signal.evidence.some((ref) => ref.quality === "gap");
}

function hasVerifiedEvidence(signal: Signal) {
  return signal.evidence.some((ref) => ref.quality === "verified");
}

function evidenceKind(signal: Signal): keyof Omit<EvidenceGroups, "gaps"> {
  const text = `${signal.project ?? ""} ${signal.title} ${signal.context ?? ""}`.toLowerCase();
  if (/(client|altmark|rent|delinquency|dashboard|proposal|resume|cover|job|application|consult)/.test(text)) return "buyer";
  if (/(post|content|linkedin|x |thread|teardown|draft|appfolio|proof asset|voice)/.test(text)) return "content";
  return "system";
}

export function evidenceSummary(signals: Signal[]): EvidenceSummary {
  const evidenceSignals = signals.filter(isEvidenceSignal);
  const latest = [...evidenceSignals].sort((a, b) => b.updatedAt - a.updatedAt)[0];

  return {
    total: evidenceSignals.length,
    verified: evidenceSignals.filter(hasVerifiedEvidence).length,
    gaps: evidenceSignals.filter(hasProofGap).length,
    failures: evidenceSignals.filter((signal) => signal.status === "failed").length,
    latestTitle: latest?.title ?? "No proof logged",
  };
}

export function evidenceGroups(signals: Signal[]): EvidenceGroups {
  const groups: EvidenceGroups = {
    buyer: [],
    system: [],
    content: [],
    gaps: [],
  };

  for (const signal of sortWorkSignals(signals.filter(isEvidenceSignal))) {
    if (hasProofGap(signal)) {
      groups.gaps.push(signal);
      continue;
    }
    groups[evidenceKind(signal)].push(signal);
  }

  return groups;
}
