"use client";
// Current item, desktop (README 1): header, status banner, queue rail, decision pane, context pane.
import { cx as cn } from "./cx";
import {
  DescriptionSection, EvidenceSection, FeedbackSection, FreshnessSection, ItemHeading, OutreachBlock, PromptSection, SlotBlocks, StepsSection,
} from "./ItemBlocks";
import { FailurePanel, QuietBox, ReadOnlyBox, StatePanels, StatusBanner, StatusLine } from "./ItemShared";
import { KeyChip, MonoLabel, button, desk, focusRing } from "./primitives";
import { ACTION_LABELS } from "./model";
import type { ItemScreenProps, RailRow } from "./model";

type HeaderProps = Pick<ItemScreenProps, "positionText" | "handledText" | "freshText" | "onHelp"> & { onPause?: () => void; onQueue?: () => void };

/** The 44 px desktop header. While loading there is no run position and no actions. */
export function DesktopHeader({ props, queueOpen }: { props: HeaderProps; queueOpen?: boolean }) {
  return (
    <header className="flex h-header flex-none items-center gap-d28 border-b border-mc-line bg-mc-surface px-d16">
      <span className="text-mc-15 font-bold tracking-[-.01em]">Mission Control</span>
      <span className="flex items-baseline gap-d6"><MonoLabel>Order</MonoLabel><span className="font-semibold">Curated order</span></span>
      {props.positionText && (
        <span className="flex items-baseline gap-d6">
          <MonoLabel>Today&apos;s run</MonoLabel>
          <span className="font-semibold">{props.positionText}</span>
          <span className="text-mc-ink-muted">· {props.handledText}</span>
        </span>
      )}
      <span className="flex-1" />
      <span className="text-mc-13 text-mc-ink-muted">{props.freshText}</span>
      <div className="flex items-center gap-d10">
        {props.onPause && <button type="button" onClick={props.onPause} className={desk.header}>Pause run</button>}
        {props.onQueue && <button type="button" onClick={props.onQueue} aria-pressed={queueOpen} className={`${desk.header} flex items-center gap-d8`}>Queue<KeyChip>Q</KeyChip></button>}
        <button type="button" onClick={props.onHelp} className={`${desk.header} flex items-center gap-d8`}>Shortcuts<KeyChip>?</KeyChip></button>
      </div>
    </header>
  );
}

function Rail({ rows, onGoTo }: { rows: RailRow[]; onGoTo: (id: string) => void }) {
  return (
    <nav aria-label="Today's run" className="flex w-rail flex-none flex-col overflow-auto border-r border-mc-line bg-mc-panel pb-d16 pt-d8">
      {rows.map((row, i) => (
        <div key={row.id} className="flex flex-col">
          {(i === 0 || rows[i - 1].group !== row.group) && (
            <div className="px-d12 pb-d4 pt-d12 font-mc-mono text-mc-11 font-medium uppercase tracking-[.06em] text-mc-ink-muted">{row.group}</div>
          )}
          <button
            type="button"
            onClick={() => onGoTo(row.id)}
            aria-current={row.current ? "step" : undefined}
            title={row.exception ? `${row.title}\n${row.exception}` : row.title}
            className={cn(
              focusRing,
              "flex min-h-[calc(var(--mc-qrow)-3px)] w-full cursor-pointer items-center gap-d8 border-l-[3px] px-d12 py-d6 text-left text-mc-13 hover:bg-mc-panel-hover focus-visible:outline-offset-[-2px]",
              row.current ? "border-mc-accent bg-mc-accent-tint font-bold text-mc-ink" : "border-transparent bg-transparent",
              !row.current && (row.handled ? "text-mc-ink-muted" : "text-mc-ink"),
            )}
          >
            <span className="w-[16px] flex-none font-mc-mono text-mc-12 font-medium">{row.position}</span>
            <span className="min-w-0 flex-1 truncate">{row.title}</span>
            <span className="flex-none text-mc-11 font-normal text-mc-ink-muted">{row.status}</span>
          </button>
        </div>
      ))}
    </nav>
  );
}

function ActionRow({ props }: { props: ItemScreenProps }) {
  const { actions } = props;
  if (actions.failure) return <FailurePanel failure={actions.failure} onRetry={props.onRetry} onDismiss={props.onDismiss} mobile={false} />;
  if (props.panel) return <>{props.panel}</>;
  if (actions.readOnly) return <ReadOnlyBox readOnly={actions.readOnly} />;
  if (actions.paused) return <QuietBox>{actions.paused}</QuietBox>;
  if (actions.resolved || actions.buttons.length === 0) return null;
  return (
    <div className="flex flex-wrap gap-d8 pt-d4">
      {actions.buttons.map((action, i) => {
        const primary = i === 0 && action !== "reject";
        const style = action === "reject" ? desk.inkOutline : primary ? desk.primary : desk.secondary;
        const chip = action === "complete" ? "C" : action === "defer" ? "D" : null;
        return (
          <button
            key={action}
            type="button"
            data-action={action}
            disabled={actions.busy}
            onClick={() => props.onAction(action)}
            className={cn(style, chip && "flex items-center gap-d8")}
          >
            {ACTION_LABELS[action]}
            {chip && <KeyChip onAccent={primary}>{chip}</KeyChip>}
          </button>
        );
      })}
    </div>
  );
}

export function DesktopItem(props: ItemScreenProps) {
  const { view } = props;
  const changedKeys = props.change?.keys ?? [];
  return (
    <>
      <DesktopHeader props={props} />
      {props.banner && <StatusBanner banner={props.banner} mobile={false} />}
      <div className="flex min-h-0 flex-1">
        <Rail rows={props.rail} onGoTo={props.onGoTo} />
        <main className="flex min-w-0 flex-1">
          <section aria-label="Decision" className="flex w-[clamp(380px,34%,480px)] flex-none flex-col overflow-auto border-r border-mc-line bg-mc-surface">
            <div className="flex flex-1 flex-col gap-d16 px-d24 pb-d12 pt-d20">
              <StatePanels props={props} mobile={false} />
              <ItemHeading view={view} mobile={false} changedKeys={changedKeys} />
              <SlotBlocks view={view} changedKeys={changedKeys} mobile={false} />
              <DescriptionSection view={view} answerBox={props.answerBox} />
              <OutreachBlock view={view} />
              <ActionRow props={props} />
              {!props.panel && <StatusLine actions={props.actions} onUndo={props.onUndo} mobile={false} />}
            </div>
            <div className="sticky bottom-0 flex flex-none flex-col gap-d8 border-t border-mc-line bg-mc-surface px-d24 py-d10">
              {props.notice && <div role="status" aria-live="polite" className="text-mc-13 text-mc-ink-secondary">{props.notice}</div>}
              <div className="flex items-center gap-d8">
                <button type="button" onClick={props.onPrevious} className={`${button.quiet} flex items-center gap-d8 rounded-btn px-d12 py-d7 text-mc-13 font-semibold`}>
                  ← Previous<KeyChip>K</KeyChip>
                </button>
                <span className="flex-1 text-center font-mc-mono text-mc-12 font-medium text-mc-ink-muted">{props.positionText}</span>
                <button type="button" onClick={props.onNext} className={`${button.quiet} flex items-center gap-d8 rounded-btn px-d12 py-d7 text-mc-13 font-semibold`}>
                  Next →<KeyChip>J</KeyChip>
                </button>
              </div>
            </div>
          </section>
          <section aria-label="Context" className="flex min-w-0 flex-1 flex-col gap-d24 overflow-auto px-d32 pb-d40 pt-d20">
            <StepsSection view={view} mobile={false} first changedKeys={changedKeys} />
            <PromptSection key={view.id} view={view} mobile={false} changedKeys={changedKeys} />
            <EvidenceSection view={view} emphasis={props.evidenceEmphasis} message={props.evidenceMessage} />
            <FreshnessSection view={view} mobile={false} />
            <FeedbackSection view={view} />
          </section>
        </main>
      </div>
    </>
  );
}
