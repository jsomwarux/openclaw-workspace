"use client";
// The queue (README 3): a full view on desktop, a bottom sheet on mobile.
import { useEffect, useRef } from "react";
import { cx as cn } from "./cx";
import type { QueueRowView, QueueViewModel } from "@/lib/cockpit/view";
import { KeyChip, button, focusRing } from "./primitives";

const ORDER_TEXT = "Q, P and AP follow their numbers, then other cards in their saved sequence. No other order is active.";

function groupTitle(name: string, count: number) {
  return `${name} · ${count} ${count === 1 ? "item" : "items"}`;
}

function rowLook(row: QueueRowView) {
  return cn(
    "border-l-[3px]",
    row.current ? "border-mc-accent bg-mc-accent-tint font-bold text-mc-ink" : "border-transparent bg-transparent",
    !row.current && (row.inRun && row.status !== "Handled" ? "text-mc-ink" : "text-mc-ink-muted"),
  );
}

export function QueueView({ queue, backLabel, notice, onBack, onOpen }: { queue: QueueViewModel; backLabel: string; notice: string | null; onBack: () => void; onOpen: (row: QueueRowView) => void }) {
  const c = queue.counts;
  const columns = "grid grid-cols-[44px_minmax(240px,1.6fr)_140px_56px_56px_minmax(220px,1.4fr)] gap-x-d12";
  return (
    <div className="min-h-0 flex-1 overflow-auto bg-mc-page">
      <div className="mx-auto flex max-w-queue flex-col gap-d14 px-d24 pb-d48 pt-d20">
        <div className="flex items-start gap-d16">
          <div className="flex flex-1 flex-col gap-d4">
            <h1 className="m-0 text-mc-22 font-bold tracking-[-.015em]">Queue</h1>
            <div><span className="font-bold">Order: Curated order.</span> <span className="text-mc-ink-secondary">{ORDER_TEXT}</span></div>
          </div>
          <button type="button" autoFocus onClick={onBack} className={`${button.secondary} flex items-center gap-d10 rounded-btn px-d14 py-d8 text-mc-14`}>
            {backLabel}<KeyChip>Esc</KeyChip>
          </button>
        </div>
        <div className="flex flex-wrap gap-x-d28 gap-y-d4 border-y border-mc-line py-d10 text-mc-13">
          <span><b>{c.inRun}</b> in today&apos;s run</span>
          <span><b>{c.handled}</b> handled</span>
          <span><b>{c.current}</b> current</span>
          <span><b>{c.upNext}</b> up next</span>
          <span><b>{c.outside}</b> outside today&apos;s run</span>
        </div>
        {notice && <div role="status" aria-live="polite" className="rounded-btn border border-mc-line-strong bg-mc-surface px-d12 py-d8 text-mc-13 font-medium">{notice}</div>}
        <div className="overflow-hidden rounded-card border border-mc-line-table bg-mc-surface">
          <div className={`${columns} border-b border-mc-line-table bg-mc-panel px-d12 py-d8 font-mc-mono text-mc-11 font-medium uppercase tracking-[.06em] text-mc-ink-muted`}>
            <span className="text-right">Pos.</span><span>Item</span><span>Status</span><span>Owner</span><span className="text-right">Age</span><span>Blocker</span>
          </div>
          {queue.groups.map((group) => (
            <div key={group.name} className="flex flex-col">
              <div className="border-b border-mc-line px-d12 pb-d6 pt-d14 font-mc-mono text-mc-12 font-semibold uppercase tracking-[.06em]">{groupTitle(group.name, group.rows.length)}</div>
              {group.rows.map((row, i) => (
                <div key={row.id} className="flex flex-col">
                  {group.dividerBefore === i && (
                    <div className="border-b border-t border-dashed border-b-mc-line-soft border-t-mc-line-missing bg-mc-page px-d12 pb-d6 pt-d10 text-mc-12 font-semibold text-mc-ink-secondary">
                      Not in today&apos;s run
                    </div>
                  )}
                  <button
                    type="button"
                    onClick={() => onOpen(row)}
                    aria-current={row.current ? "step" : undefined}
                    className={cn(
                      columns, focusRing, rowLook(row),
                      "min-h-[var(--mc-qrow)] w-full cursor-pointer items-center border-b border-b-mc-line-soft py-d4 pl-d9 pr-d12 text-left text-mc-13 hover:bg-mc-row-hover focus-visible:outline-offset-[-2px]",
                    )}
                  >
                    <span className="text-right font-mc-mono text-mc-12 font-medium">{row.position ?? "—"}</span>
                    <span className="flex min-w-0 flex-col">
                      <span title={row.title} className="truncate">{row.title}</span>
                      {row.exception && <span className="truncate font-mc-mono text-mc-11 font-semibold text-mc-ink">{row.exception.text}</span>}
                    </span>
                    <span>{row.status}</span>
                    <span className="font-mc-mono text-mc-12">{row.owner}</span>
                    <span className="text-right font-mc-mono text-mc-12">{row.age}</span>
                    <span title={row.blocker ?? undefined} className={cn("truncate", row.blocker ? "text-mc-ink" : "text-mc-ink-muted")}>{row.blocker ?? "None recorded"}</span>
                  </button>
                </div>
              ))}
            </div>
          ))}
        </div>
        <div className="text-mc-12 text-mc-ink-muted">Age counts from when the item was created. A dash means the item is not in today&apos;s run.</div>
      </div>
    </div>
  );
}

export function QueueSheet({ queue, positionText, notice, onClose, onOpen }: { queue: QueueViewModel; positionText: string; notice: string | null; onClose: () => void; onOpen: (row: QueueRowView) => void }) {
  const closeRef = useRef<HTMLButtonElement>(null);
  useEffect(() => closeRef.current?.focus(), []);
  return (
    <div className="fixed inset-0 z-[90]">
      <div aria-hidden="true" onClick={onClose} className="absolute inset-0 bg-[var(--mc-scrim)]" />
      <div role="dialog" aria-modal="true" aria-label="Queue" className="absolute inset-x-0 bottom-0 flex h-[88%] flex-col overflow-hidden rounded-t-sheet border-t border-mc-line-strong bg-mc-surface">
        <div className="flex flex-none items-center gap-d12 border-b border-mc-line py-d10 pl-d16 pr-d8">
          <div className="flex flex-1 flex-col">
            <span className="text-mc-18 font-bold">Queue</span>
            <span className="font-mc-mono text-mc-11 font-medium text-mc-ink-muted">{`Order: Curated order · ${positionText}`}</span>
            <span className="font-mc-mono text-mc-11 font-medium text-mc-ink-muted">{`Today's run ${queue.counts.inRun} · Outside today's run ${queue.counts.outside}`}</span>
          </div>
          <button ref={closeRef} type="button" onClick={onClose} className={`${button.secondary} min-h-[44px] min-w-[68px] rounded-card text-mc-15`}>Close</button>
        </div>
        {notice && <div role="status" aria-live="polite" className="border-b border-mc-line px-d16 py-d8 text-mc-13 font-medium">{notice}</div>}
        <div className="min-h-0 flex-1 overflow-auto pb-[calc(12px+env(safe-area-inset-bottom))]">
          {queue.groups.map((group) => (
            <div key={group.name} className="flex flex-col">
              <div className="px-d16 pb-d4 pt-d14 font-mc-mono text-mc-11 font-medium uppercase tracking-[.06em] text-mc-ink-muted">{groupTitle(group.name, group.rows.length)}</div>
              {group.rows.map((row, i) => (
                <div key={row.id} className="flex flex-col">
                  {group.dividerBefore === i && (
                    <div className="border-t border-dashed border-mc-line-missing bg-mc-page px-d16 pb-d6 pt-d10 text-mc-12 font-semibold text-mc-ink-secondary">Not in today&apos;s run</div>
                  )}
                  <button
                    type="button"
                    onClick={() => onOpen(row)}
                    aria-current={row.current ? "step" : undefined}
                    className={cn(focusRing, rowLook(row), "flex min-h-[calc(var(--mc-qrow)+22px)] w-full cursor-pointer flex-col justify-center gap-d2 border-b border-b-mc-line-soft px-d16 py-d8 text-left text-mc-14 focus-visible:outline-offset-[-2px]")}
                  >
                    <span className="flex items-baseline gap-d10">
                      <span className="w-[18px] flex-none font-mc-mono text-mc-13 font-medium">{row.position ?? "—"}</span>
                      <span className="min-w-0 flex-1 truncate">{row.title}</span>
                    </span>
                    <span className="truncate pl-[28px] text-mc-12 font-normal text-mc-ink-muted">
                      {[row.exception?.text, row.status, `Owner: ${row.owner}`, `Age ${row.age}`, row.blocker ?? "No blocker recorded"].filter(Boolean).join(" · ")}
                    </span>
                  </button>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
