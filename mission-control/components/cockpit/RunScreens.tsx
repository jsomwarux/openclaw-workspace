"use client";
// Run start, empty run, resume (with what changed), and the run summary (README 4, 5, 6).
import type { ReactNode } from "react";
import { cx as cn } from "./cx";
import type { RunChange, Verbatim } from "@/lib/cockpit/types";
import type { RunStartViewModel, SummaryViewModel } from "@/lib/cockpit/view";
import { FromDescriptionChip, KeyChip, MissingChip, MonoLabel, button, desk } from "./primitives";

const KIND_WORDS: Record<RunChange["kind"], string> = {
  changed: "Changed",
  addedToBacklog: "Added to the backlog",
  expired: "Expired",
  removedFromRun: "Removed",
  movedUp: "Moved up",
  addedToRun: "Added to today's run",
};

export function RunShell({ desktop, date, onHelp, bar, children }: { desktop: boolean; date: string; onHelp: () => void; bar: ReactNode; children: ReactNode }) {
  return (
    <>
      <header className="flex flex-none items-center gap-d16 border-b border-mc-line bg-mc-surface px-d16 py-d8">
        <div className="flex min-w-0 flex-1 flex-col">
          <span className="text-mc-15 font-bold">Mission Control</span>
          <span className="font-mc-mono text-mc-11 font-medium text-mc-ink-muted">Order: Curated order</span>
        </div>
        {desktop && (
          <button type="button" onClick={onHelp} className={`${desk.header} flex items-center gap-d8`}>Shortcuts<KeyChip>?</KeyChip></button>
        )}
        <span className="font-mc-mono text-mc-12 font-medium text-mc-ink-muted">{date}</span>
      </header>
      <div className="min-h-0 flex-1 overflow-auto">
        <div className={cn("mx-auto flex max-w-run flex-col gap-d20", desktop ? "px-d32 pb-d56 pt-d40" : "px-d16 pb-d28 pt-d20")}>{children}</div>
      </div>
      <div className="flex-none border-t border-mc-line bg-mc-surface px-[12px] pb-[calc(10px+env(safe-area-inset-bottom))] pt-[10px]">
        <div className={cn("mx-auto flex max-w-run items-stretch gap-d8", desktop ? "flex-row-reverse" : "flex-col")}>{bar}</div>
      </div>
    </>
  );
}

export function BarButton({ primary = false, onClick, children }: { primary?: boolean; onClick: () => void; children: ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(primary ? `${button.primary} font-bold` : button.secondary, "min-h-[48px] rounded-card", primary ? "px-d24 text-mc-16" : "px-d20 text-mc-15")}
    >
      {children}
    </button>
  );
}

function Heading({ label, title, meta }: { label: string; title: string; meta: string }) {
  return (
    <div className="flex flex-col gap-d6">
      <MonoLabel>{label}</MonoLabel>
      <h1 className="m-0 text-mc-28 font-bold leading-[1.15] tracking-[-.02em]">{title}</h1>
      <div className="text-mc-ink-secondary">{meta}</div>
    </div>
  );
}

function Labelled({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="flex flex-col gap-d3">
      <MonoLabel>{label}</MonoLabel>
      <div>{children}</div>
    </div>
  );
}

function firstActionText(slot: Verbatim<string>) {
  return (
    <div className="flex flex-col gap-d3">
      <div className="flex items-center gap-d8">
        <MonoLabel>First action</MonoLabel>
        {slot.kind === "missing" ? <MissingChip /> : slot.source === "description" && <FromDescriptionChip />}
      </div>
      <div className="text-mc-16 font-semibold [overflow-wrap:anywhere]">{slot.kind === "value" ? slot.value : "This item has no first action recorded."}</div>
    </div>
  );
}

export function RunStartContent({ view }: { view: RunStartViewModel }) {
  return (
    <>
      <Heading label="Today's run" title={view.headline} meta={`${view.date} · Curated order · ${view.breakdown}`} />
      {view.first && (
        <div className="flex flex-col gap-d12 rounded-panel border-2 border-mc-ink bg-mc-surface px-d18 py-d16">
          <MonoLabel>{`First item · ${view.first.position}`}</MonoLabel>
          <div className="text-mc-20 font-bold leading-[1.25] [overflow-wrap:anywhere]">{view.first.title}</div>
          {firstActionText(view.first.firstAction)}
          <Labelled label="Why it is first">{view.whyFirst}</Labelled>
        </div>
      )}
      <Labelled label="Urgent exceptions">
        {view.exceptions.length === 0 ? (
          "None. No approval expires within 24 hours and no external deadline is overdue."
        ) : (
          <ul className="m-0 flex list-none flex-col gap-d6 p-0">
            {view.exceptions.map((exception) => (
              <li key={exception.title} className="flex flex-col">
                <span className="font-semibold [overflow-wrap:anywhere]">{exception.title}</span>
                <span>{exception.text}</span>
              </li>
            ))}
          </ul>
        )}
      </Labelled>
      <div className="text-mc-ink-secondary">{`${view.outside} other ${view.outside === 1 ? "item stays" : "items stay"} in the backlog and ${view.outside === 1 ? "is" : "are"} not part of today's run.`}</div>
    </>
  );
}

export function EmptyRunContent({ date, backlog, note }: { date: string; backlog: number; note: string | null }) {
  return (
    <>
      <Heading label="Today's run" title="Nothing is waiting for you" meta={`${date} · Curated order`} />
      <div className="flex flex-col gap-d6 rounded-panel border border-mc-line-notice bg-mc-surface px-d18 py-d16">
        <div className="text-mc-17 font-semibold">Today&apos;s run has no items.</div>
        <div>No cards are committed to it, and none of your agents&apos; work needs a decision from you right now.</div>
      </div>
      <Labelled label="What you can do">
        {`Check again if you expect new work. ${backlog} ${backlog === 1 ? "item is" : "items are"} in the backlog. Review them to decide whether any belong in today's run.`}
      </Labelled>
      {note && <div role="status" aria-live="polite" className="font-semibold">{note}</div>}
    </>
  );
}

export function ChangeBanner({ changes, headline, closing, label = "Changed while you were away" }: { changes: RunChange[]; headline: string; closing: string; label?: string }) {
  return (
    <section aria-label={label} className="flex flex-col gap-d12 rounded-panel border-2 border-mc-ink bg-mc-notice px-d18 py-d16">
      <div className="flex flex-col gap-d2">
        <span className="font-mc-mono text-mc-12 font-semibold uppercase tracking-[.06em]">{`${label} · ${changes.length}`}</span>
        <div className="text-mc-16 font-semibold">{headline}</div>
      </div>
      <ul className="m-0 flex list-none flex-col p-0">
        {changes.map((change) => (
          <li key={`${change.kind}-${change.itemId}`} className="flex flex-col gap-d3 border-t border-mc-line-notice py-d10">
            <div className="flex flex-wrap items-center gap-d8">
              <span className="rounded-chip border border-mc-ink px-d6 font-mc-mono text-mc-11 font-semibold uppercase tracking-[.04em]">{KIND_WORDS[change.kind]}</span>
              <span className="font-mc-mono text-mc-12 font-medium text-mc-ink-secondary">{change.where}</span>
            </div>
            <div className="font-semibold [overflow-wrap:anywhere]">{change.title || "Title missing"}</div>
            <div className="text-mc-ink-secondary">{change.detail}</div>
          </li>
        ))}
      </ul>
      <div className="border-t border-mc-line-notice pt-d10 text-mc-ink-secondary">{closing}</div>
    </section>
  );
}

export function ResumeContent({
  position, meta, changes, headline, closing, left,
}: {
  position: string;
  meta: string;
  changes: RunChange[];
  headline: string;
  closing: string;
  left: { title: string; eyebrow: string; next: { position: string; title: string } | null } | null;
}) {
  return (
    <>
      <Heading label="Today's run · paused" title={`Resume at ${position}`} meta={meta} />
      {changes.length > 0 ? (
        <ChangeBanner changes={changes} headline={headline} closing={closing} />
      ) : (
        <div className="rounded-panel border border-mc-line-notice bg-mc-surface px-d18 py-d14">
          <span className="font-semibold">Nothing changed while you were away.</span> Order, run size and every item are as you left them.
        </div>
      )}
      {left && (
        <div className="flex flex-col gap-d10 border-t border-mc-line pt-d16">
          <MonoLabel>Where you left</MonoLabel>
          <div className="text-mc-18 font-bold leading-[1.25] [overflow-wrap:anywhere]">{left.title}</div>
          <div className="font-mc-mono text-mc-12 font-medium text-mc-ink-muted">{left.eyebrow}</div>
          {left.next && (
            <div className="text-mc-ink-secondary">
              <span className="font-semibold">{`Next in the run, ${left.next.position}:`}</span> {left.next.title}
            </div>
          )}
        </div>
      )}
    </>
  );
}

export function SummaryContent({ view, label, reopen }: { view: SummaryViewModel; label: string; reopen: ReactNode }) {
  return (
    <>
      <Heading label={label} title={view.headline} meta={view.meta} />
      {reopen}
      <section className="flex flex-col gap-d4 rounded-panel border-2 border-mc-ink bg-mc-surface px-d18 py-d16">
        <span className="font-mc-mono text-mc-12 font-semibold uppercase tracking-[.06em]">{`Still needs you · ${view.stillNeedsYou.length}`}</span>
        {view.stillNeedsYou.length === 0 ? (
          <div className="border-t border-mc-line py-d10">Nothing from this run is left open.</div>
        ) : (
          <ul className="m-0 flex list-none flex-col p-0">
            {view.stillNeedsYou.map((entry) => (
              <li key={entry.id} className="flex flex-col gap-d2 border-t border-mc-line py-d10">
                <div className="font-semibold [overflow-wrap:anywhere]">{entry.title}</div>
                <div className="text-mc-ink-secondary">{entry.detail}</div>
              </li>
            ))}
          </ul>
        )}
      </section>
      <section className="flex flex-col gap-d4">
        <MonoLabel>Handled</MonoLabel>
        <ol className="m-0 list-none rounded-card border border-mc-line-table bg-mc-surface p-0">
          {view.handled.map((entry) => (
            <li key={entry.position} className="flex gap-d12 border-t border-mc-line-soft px-d14 py-d10 first:border-t-0">
              <span className="w-[18px] flex-none text-right font-mc-mono text-mc-13 font-medium text-mc-ink-muted">{entry.position}</span>
              <div className="flex min-w-0 flex-1 flex-col">
                <span className="[overflow-wrap:anywhere]">{entry.title}</span>
                <span className="text-mc-13 font-semibold text-mc-ink-secondary">{entry.did}</span>
              </div>
            </li>
          ))}
        </ol>
      </section>
      {view.addedSinceStart && <div className="text-mc-ink-secondary">{view.addedSinceStart}</div>}
    </>
  );
}
