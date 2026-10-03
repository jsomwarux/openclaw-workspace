"use client";
// The shortcuts overlay (README 7) and the static loading skeletons (README 8).
import { useEffect, useRef } from "react";
import { trapTab, useRestoreFocus } from "./focus";
import { button } from "./primitives";

const GROUPS: { label: string; keys: [string, string][] }[] = [
  { label: "Move", keys: [["J", "Next item"], ["K", "Previous item"], ["Q", "Show or hide the queue"]] },
  { label: "Act", keys: [["C", "Complete. Asks you to confirm."], ["D", "Defer. Asks you to confirm."], ["E", "Open evidence links"]] },
  { label: "Dialogs", keys: [["Enter", "Confirm"], ["Esc", "Cancel or close"]] },
  { label: "Help", keys: [["?", "Show this list"]] },
];

export function ShortcutsOverlay({ onClose }: { onClose: () => void }) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  useRestoreFocus();
  useEffect(() => closeRef.current?.focus(), []);
  const trap = trapTab(dialogRef);
  return (
    <div onClick={onClose} className="fixed inset-0 z-[95] flex items-center justify-center bg-[var(--mc-scrim)] font-mc-sans text-mc-14 text-mc-ink">
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-label="Keyboard shortcuts"
        onClick={(event) => event.stopPropagation()}
        onKeyDown={trap}
        className="flex max-h-[calc(100vh-32px)] w-[500px] max-w-[calc(100vw-32px)] flex-col gap-d16 overflow-auto rounded-panel border border-mc-line-strong bg-mc-surface px-d24 py-d20"
      >
        <div className="flex items-center">
          <span className="flex-1 text-mc-17 font-bold">Keyboard shortcuts</span>
          <button ref={closeRef} type="button" onClick={onClose} className={`${button.quiet} rounded-btn px-d10 py-d4 text-mc-13`}>Close · Esc</button>
        </div>
        {GROUPS.map((group) => (
          <div key={group.label} className="flex flex-col gap-d6">
            <span className="font-mc-mono text-mc-11 font-medium uppercase tracking-[.06em] text-mc-ink-muted">{group.label}</span>
            {group.keys.map(([key, what]) => (
              <div key={key} className="flex items-baseline gap-d12">
                <span className="w-[56px] flex-none">
                  <kbd className="rounded-chip border border-mc-line-strong bg-mc-page px-d7 py-d1 font-mc-mono text-mc-12 font-medium">{key}</kbd>
                </span>
                <span>{what}</span>
              </div>
            ))}
          </div>
        ))}
        <div className="border-t border-mc-line pt-d12 text-mc-ink-secondary">
          Approve and Reject have no shortcut. Click the button, then confirm with Enter or a click. Reject cannot be undone.
        </div>
      </div>
    </div>
  );
}

function Bar({ w, h }: { w: string; h: string }) {
  return <div className="rounded-btn bg-mc-skeleton" style={{ width: w, height: h }} />;
}

export function LoadingDesktop() {
  return (
    <div role="status" aria-label="Loading today's run" className="flex min-h-0 flex-1">
      <div className="flex w-rail flex-none flex-col gap-d12 border-r border-mc-line bg-mc-panel px-d12 py-d14">
        {Array.from({ length: 7 }, (_, i) => <Bar key={i} w="100%" h="22px" />)}
      </div>
      <div className="flex w-[clamp(380px,34%,480px)] flex-none flex-col gap-d16 border-r border-mc-line bg-mc-surface px-d24 py-d20">
        <span className="font-mc-mono text-mc-12 font-medium text-mc-ink-muted">Loading today&apos;s run…</span>
        <Bar w="55%" h="14px" /><Bar w="92%" h="30px" /><Bar w="70%" h="30px" /><Bar w="100%" h="84px" />
        <Bar w="100%" h="16px" /><Bar w="88%" h="16px" /><Bar w="100%" h="16px" /><Bar w="76%" h="16px" />
        <div className="flex gap-d8"><Bar w="84px" h="40px" /><Bar w="108px" h="40px" /><Bar w="76px" h="40px" /><Bar w="72px" h="40px" /></div>
      </div>
      <div className="flex min-w-0 flex-1 flex-col gap-d14 px-d32 py-d20">
        <Bar w="120px" h="12px" /><Bar w="100%" h="16px" /><Bar w="92%" h="16px" /><Bar w="96%" h="16px" /><Bar w="80%" h="16px" />
        <Bar w="160px" h="12px" /><Bar w="100%" h="300px" /><Bar w="120px" h="12px" /><Bar w="60%" h="16px" />
      </div>
    </div>
  );
}

export function LoadingMobile() {
  return (
    <div role="status" aria-label="Loading today's run" className="flex min-h-0 flex-1 flex-col">
      <div className="flex min-h-0 flex-1 flex-col gap-d14 p-d16">
        <span className="font-mc-mono text-mc-12 font-medium text-mc-ink-muted">Loading today&apos;s run…</span>
        <Bar w="60%" h="14px" /><Bar w="94%" h="28px" /><Bar w="72%" h="28px" /><Bar w="100%" h="84px" />
        <Bar w="100%" h="16px" /><Bar w="90%" h="16px" /><Bar w="100%" h="16px" /><Bar w="100%" h="200px" />
      </div>
      <div className="flex flex-none flex-col gap-d8 border-t border-mc-line bg-mc-surface px-d12 py-d10">
        <Bar w="100%" h="48px" /><Bar w="100%" h="44px" />
      </div>
    </div>
  );
}
