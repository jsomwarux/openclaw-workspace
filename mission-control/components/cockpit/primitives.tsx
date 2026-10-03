// Small shared pieces of the cockpit UI. Every color, size and radius is a bundle token by name.
import type { ReactNode } from "react";
import { cx as cn } from "./cx";

export const focusRing =
  "focus-visible:[outline:var(--mc-ring-w)_solid_var(--mc-ring-c)] focus-visible:outline-offset-2 focus-visible:[box-shadow:var(--mc-ring-shadow)]";
export const press = "transition-transform duration-[160ms] ease-out active:scale-[.97] disabled:cursor-default";

const base = `${focusRing} ${press} cursor-pointer`;

export const button = {
  primary: `${base} border border-mc-accent-deep bg-mc-accent text-mc-accent-on hover:bg-mc-accent-hover font-semibold`,
  secondary: `${base} border border-mc-line-control bg-mc-surface text-mc-ink hover:bg-mc-control-hover font-semibold`,
  quiet: `${base} border border-mc-line-strong bg-mc-surface text-mc-ink hover:bg-mc-control-hover`,
  ink: `${base} border border-mc-ink bg-mc-ink text-mc-accent-on font-semibold`,
  inkOutline: `${base} border border-mc-ink bg-mc-surface text-mc-ink hover:bg-mc-control-hover font-bold`,
  link: `${focusRing} cursor-pointer border-none bg-transparent font-semibold text-mc-accent-deep underline hover:text-mc-ink`,
};

/** Desktop action sizes (README: primary 9/18, secondary 9/16, radius 4). */
export const desk = {
  primary: `${button.primary} rounded-btn px-d18 py-d9 text-mc-14`,
  secondary: `${button.secondary} rounded-btn px-d16 py-d9 text-mc-14`,
  inkOutline: `${button.inkOutline} rounded-btn px-d18 py-d9 text-mc-14`,
  confirm: `${button.primary} rounded-btn px-d14 py-d7 text-mc-14`,
  confirmInk: `${button.ink} rounded-btn px-d14 py-d7 text-mc-14`,
  cancel: `${button.secondary} rounded-btn px-d14 py-d7 text-mc-14 font-medium`,
  header: `${button.quiet} rounded-btn px-d10 py-d4 text-mc-13 font-medium`,
};

/** Mobile sizes: 48 px primary, 44 px others, radius 6. */
export const mobile = {
  primary: `${button.primary} min-h-[48px] rounded-card text-mc-16 font-bold`,
  secondary: `${button.secondary} min-h-[48px] rounded-card text-mc-15`,
  small: `${button.secondary} min-h-[44px] rounded-card text-mc-14`,
  move: `${button.quiet} min-h-[44px] rounded-card text-mc-14 font-medium`,
  ink: `${button.ink} min-h-[48px] rounded-card text-mc-16 font-bold`,
  inkOutline: `${button.inkOutline} min-h-[48px] rounded-card text-mc-16`,
};

export function MonoLabel({ children, className }: { children: ReactNode; className?: string }) {
  return <span className={cn("font-mc-mono text-mc-11 font-medium uppercase tracking-[.06em] text-mc-ink-muted", className)}>{children}</span>;
}

export function KeyChip({ children, onAccent = false }: { children: ReactNode; onAccent?: boolean }) {
  return (
    <span
      aria-hidden="true"
      className={cn(
        "rounded-chip border px-d5 font-mc-mono text-mc-11 font-medium",
        onAccent ? "border-mc-accent-tint text-mc-accent-on" : "border-mc-line-table text-mc-ink-muted",
      )}
    >
      {children}
    </span>
  );
}

export function MissingChip({ emphasis = false }: { emphasis?: boolean }) {
  return (
    <span className={cn("rounded-chip border px-d6 font-mc-mono text-mc-11 font-medium text-mc-ink-secondary", emphasis ? "border-mc-ink" : "border-mc-line-control")}>
      Missing
    </span>
  );
}

export function FromDescriptionChip() {
  return <span className="rounded-chip border border-mc-line-missing px-d6 font-mc-mono text-mc-11 font-medium text-mc-ink-secondary">From description</span>;
}

export function TagChip({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <span className={cn("self-start rounded-chip border border-mc-ink px-d6 font-mc-mono text-mc-11 font-semibold uppercase tracking-[.06em]", className)}>
      {children}
    </span>
  );
}

/** The 2 px ink notice panel used for expired, changed and invalid states. */
export function NoticePanel({ tag, children, role = "alert" }: { tag: string; children: ReactNode; role?: "alert" | "status" }) {
  return (
    <section role={role} className="flex flex-col gap-d10 rounded-panel border-2 border-mc-ink bg-mc-notice px-d16 py-d14">
      <TagChip>{tag}</TagChip>
      {children}
    </section>
  );
}
