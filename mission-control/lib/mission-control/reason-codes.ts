import type { Signal } from "./types";

export type ReasonTone = "cash" | "urgent" | "neutral" | "muted" | "danger";

export type ReasonChip = {
  code: string;
  label: string;
  tone: ReasonTone;
};

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function shortDate(iso: string): string {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!match) return iso;
  const month = MONTHS[Number(match[2]) - 1];
  if (!month) return iso;
  return `${month} ${Number(match[3])}`;
}

function money(raw: string): string {
  const amount = Number(raw);
  if (!Number.isFinite(amount)) return `$${raw}`;
  return `$${Math.round(amount).toLocaleString("en-US")}`;
}

/**
 * Reason codes are the scorer's own words. The cockpit shows them instead of the
 * number, so every code needs a label a human can act on without a legend.
 */
export function reasonChip(code: string): ReasonChip {
  const [key, value = ""] = code.split(":");

  switch (key) {
    case "cash":
      return { code, label: money(value), tone: "cash" };
    case "deadline":
      return { code, label: `Due ${shortDate(value)}`, tone: "urgent" };
    case "unblocks":
      return { code, label: value === "agent" ? "Unblocks agent" : `Unblocks ${value}`, tone: "neutral" };
    case "proof":
      return { code, label: "Proof asset", tone: "neutral" };
    case "risk":
      return { code, label: "Stops a loss", tone: "urgent" };
    case "stability":
      return { code, label: "Stability", tone: "neutral" };
    case "nudge-due":
      return { code, label: "Nudge due", tone: "urgent" };
    case "unexplained":
      return { code, label: "Unexplained rank", tone: "danger" };
    case "focus-penalty":
      return { code, label: "Off focus", tone: "muted" };
    case "effort-demotion":
      return { code, label: "Long effort", tone: "muted" };
    case "ship-capped":
      return { code, label: "Ship capped", tone: "muted" };
    default:
      return { code, label: code, tone: "muted" };
  }
}

export function reasonChips(codes: string[] = []): ReasonChip[] {
  const seen = new Set<string>();
  const chips: ReasonChip[] = [];
  for (const code of codes) {
    if (seen.has(code)) continue;
    seen.add(code);
    chips.push(reasonChip(code));
  }
  return chips;
}

export const reasonToneClassName: Record<ReasonTone, string> = {
  cash: "border-emerald-800/60 bg-emerald-950/30 text-emerald-300",
  urgent: "border-[#f0883e]/40 bg-[#f0883e]/10 text-[#f0883e]",
  neutral: "border-[#2b333c] bg-[#12161a] text-zinc-300",
  muted: "border-[#20262d] bg-[#0f1316] text-zinc-500",
  danger: "border-red-800/60 bg-red-950/30 text-red-300",
};

export type PrimaryActionVerb = "Approve" | "Nudge" | "Mark sent" | "Open";

/**
 * The button verb comes from the item's own state, so the cockpit never asks JT
 * to translate a status into a next move.
 */
export function primaryActionVerb(signal: Signal): PrimaryActionVerb {
  if (signal.status === "awaiting-approval") return "Approve";
  if ((signal.reasonCodes ?? []).includes("nudge-due")) return "Nudge";
  if ((signal.dollars ?? 0) > 0 && signal.pipelineStage === "pitched") return "Mark sent";
  return "Open";
}
