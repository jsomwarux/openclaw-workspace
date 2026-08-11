import type { Signal } from "./types";

const FIELD_LABELS: Record<string, string> = {
  dueDate: "Due date",
  dollars: "Dollars",
  stageProbability: "Stage probability",
  priority: "Priority",
  waitingOn: "Waiting on",
};

const DATE_FORMAT = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "America/New_York",
});

export function formatAuditField(field: string): string {
  return FIELD_LABELS[field] ?? field.replace(/([a-z])([A-Z])/g, "$1 $2").replace(/^./, (char) => char.toUpperCase());
}

export function formatAuditValue(field: string, value: string): string {
  if (!value) return "None";

  if (field === "dueDate") {
    const ms = Number(value);
    if (Number.isFinite(ms)) return DATE_FORMAT.format(new Date(ms));
  }

  if (field === "dollars") {
    const amount = Number(value);
    if (Number.isFinite(amount)) return `$${Math.round(amount).toLocaleString("en-US")}`;
  }

  if (field === "stageProbability") {
    const probability = Number(value);
    if (Number.isFinite(probability)) return `${Math.round(probability * 100)}%`;
  }

  return value;
}

export function needsEvidenceAttention(signal: Signal): boolean {
  return Boolean(signal.proofRequired || signal.evidence.some((ref) => ref.quality === "gap"));
}
