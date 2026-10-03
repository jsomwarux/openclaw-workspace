"use client";
// Pieces of the action area used by both layouts: failure, paused and read-only notices, the
// status line, and the state panels that sit above the title.
import { cx as cn } from "./cx";
import { ChangedPanel, ExpiredPanel, InvalidPanel } from "./ItemBlocks";
import { button, mobile as mob } from "./primitives";
import type { ActionModel, Banner, ItemScreenProps } from "./model";

export function StatePanels({ props, mobile }: { props: ItemScreenProps; mobile: boolean }) {
  const { view, change } = props;
  return (
    <>
      {view.expired && <ExpiredPanel text={view.expired} />}
      {change && <ChangedPanel change={change} timeZone={props.timeZone} onAck={props.onAckChange} mobile={mobile} />}
      {!view.validity.ok && <InvalidPanel reasons={view.validity.reasons} source={view.freshness.source} onRecheck={props.onRecheck} mobile={mobile} />}
    </>
  );
}

export function FailurePanel({ failure, onRetry, onDismiss, mobile }: { failure: NonNullable<ActionModel["failure"]>; onRetry: () => void; onDismiss: () => void; mobile: boolean }) {
  return (
    <div role="alert" className="flex flex-col gap-d8 rounded-card border-2 border-mc-error bg-mc-error-bg px-d14 py-d12">
      <div className="font-bold">{failure.title}</div>
      <div>{failure.body}</div>
      <div className="flex gap-d8">
        <button type="button" autoFocus onClick={onRetry} className={mobile ? `${mob.primary} px-d18` : `${button.primary} min-h-[36px] rounded-btn px-d18 text-mc-14 font-bold`}>Retry</button>
        <button type="button" onClick={onDismiss} className={mobile ? `${mob.secondary} px-d16` : `${button.secondary} min-h-[36px] rounded-btn px-d16 text-mc-14`}>Dismiss</button>
      </div>
    </div>
  );
}

export function QuietBox({ children }: { children: React.ReactNode }) {
  return <div className="rounded-card border border-mc-line-strong bg-mc-page px-d12 py-d10 text-mc-13">{children}</div>;
}

export function ReadOnlyBox({ readOnly, mobile = false }: { readOnly: NonNullable<ActionModel["readOnly"]>; mobile?: boolean }) {
  return (
    <QuietBox>
      <div>{readOnly.text}</div>
      <div className="mt-d6 flex flex-wrap items-baseline gap-x-d8 gap-y-d2">
        <a href="/work" target="_blank" rel="noopener noreferrer" className={cn(button.link, "p-0", mobile && "inline-flex min-h-[44px] items-center")}>Open the Work list</a>
        <span className="text-mc-ink-muted">and open this title there:</span>
      </div>
      <div className="mt-d2 font-semibold [overflow-wrap:anywhere]">{readOnly.title}</div>
    </QuietBox>
  );
}

export function StatusLine({ actions, onUndo, mobile }: { actions: ActionModel; onUndo: () => void; mobile: boolean }) {
  if (!actions.line) return null;
  return (
    <div role="status" aria-live="polite" className={cn("flex items-center text-mc-13", mobile ? "gap-d8 px-d4" : "gap-d12 border-t border-mc-line pt-d10")}>
      <span className="flex-1">{actions.line}</span>
      {actions.canUndo && (
        <button type="button" onClick={onUndo} className={cn(button.link, mobile ? "min-h-[44px] min-w-[60px] text-mc-14 font-bold" : "px-d4 py-d2 text-mc-13")}>
          Undo
        </button>
      )}
    </div>
  );
}

export function StatusBanner({ banner, mobile }: { banner: Banner; mobile: boolean }) {
  return (
    <div role="status" className="flex flex-none flex-wrap items-center gap-d12 border-b border-mc-line-strong bg-mc-notice px-d16 py-d8 text-mc-13">
      <span className="self-center rounded-chip border border-mc-ink px-d6 font-mc-mono text-mc-11 font-semibold uppercase tracking-[.06em]">{banner.tag}</span>
      <span className="min-w-[200px] flex-1">{banner.text}</span>
      <button type="button" onClick={banner.onClick} className={mobile ? `${button.secondary} min-h-[44px] rounded-btn px-d14 text-mc-14` : `${button.secondary} min-h-[32px] rounded-btn px-d12 py-d5 text-mc-13`}>
        {banner.button}
      </button>
    </div>
  );
}
