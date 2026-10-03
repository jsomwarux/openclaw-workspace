"use client";
// Current item, mobile 390 x 844 (README 2): one column, actions pinned at the bottom in thumb reach.
import { cx as cn } from "./cx";
import {
  DescriptionSection, EvidenceSection, FeedbackSection, FreshnessSection, ItemHeading, OutreachBlock, PromptSection, SlotBlocks, StepsSection,
} from "./ItemBlocks";
import { FailurePanel, QuietBox, ReadOnlyBox, StatePanels, StatusBanner, StatusLine } from "./ItemShared";
import { button, mobile as mob } from "./primitives";
import { ACTION_LABELS } from "./model";
import type { ButtonAction, ItemScreenProps } from "./model";

export function MobileHeader({ positionText, handledText, freshShort, onPause, onQueue }: Pick<ItemScreenProps, "positionText" | "handledText" | "freshShort"> & { onPause?: () => void; onQueue?: () => void }) {
  return (
    <header className="flex flex-none items-center gap-d12 border-b border-mc-line bg-mc-surface py-d8 pl-d16 pr-d8">
      <div className="flex min-w-0 flex-1 flex-col">
        <span className="text-mc-17 font-bold">
          {positionText} <span className="text-mc-13 font-medium text-mc-ink-muted">· {handledText}</span>
        </span>
        <span className="font-mc-mono text-mc-11 font-medium text-mc-ink-muted">{`Order: Curated order · ${freshShort}`}</span>
      </div>
      {onPause && <button type="button" onClick={onPause} className={`${button.quiet} min-h-[44px] min-w-[64px] rounded-card text-mc-14 font-medium`}>Pause</button>}
      {onQueue && <button type="button" onClick={onQueue} className={`${button.secondary} min-h-[44px] min-w-[76px] rounded-card text-mc-15`}>Queue</button>}
    </header>
  );
}

function ActionBar({ props }: { props: ItemScreenProps }) {
  const { actions } = props;
  const blocked = Boolean(actions.failure || actions.readOnly || actions.paused);
  const buttons = blocked || actions.resolved ? [] : actions.buttons;
  const main = buttons.filter((action) => action !== "defer" && action !== "block");
  const side = buttons.filter((action) => action === "defer" || action === "block");
  const tap = (action: ButtonAction) => () => props.onAction(action);

  let row1: React.ReactNode = null;
  if (actions.resolved && !actions.failure) {
    row1 = <button type="button" onClick={props.onNext} className={`${mob.primary} w-full`}>Next item →</button>;
  } else if (main.length === 1) {
    row1 = <button type="button" data-action={main[0]} disabled={actions.busy} onClick={tap(main[0])} className={`${main[0] === "reject" ? mob.inkOutline : mob.primary} w-full`}>{ACTION_LABELS[main[0]]}</button>;
  } else if (main.length > 1) {
    row1 = (
      <div className="flex gap-d8">
        {main.map((action, i) => (
          <button
            key={action}
            type="button"
            data-action={action}
            disabled={actions.busy}
            onClick={tap(action)}
            className={cn(i === 0 ? mob.primary : action === "reject" ? mob.inkOutline : mob.secondary, i === 0 && main[1] !== "reject" ? "flex-[2]" : "flex-1")}
          >
            {ACTION_LABELS[action]}
          </button>
        ))}
      </div>
    );
  }

  return (
    <div className="flex flex-none flex-col gap-d8 border-t border-mc-line bg-mc-surface px-d12 pb-[calc(10px*var(--mc-d,1)+env(safe-area-inset-bottom))] pt-d10">
      {props.notice && <div role="status" aria-live="polite" className="px-d4 text-mc-13 text-mc-ink-secondary">{props.notice}</div>}
      {!props.panel && <StatusLine actions={actions} onUndo={props.onUndo} mobile />}
      {actions.readOnly && <ReadOnlyBox readOnly={actions.readOnly} mobile />}
      {!actions.readOnly && actions.paused && <QuietBox>{actions.paused}</QuietBox>}
      {actions.failure && <FailurePanel failure={actions.failure} onRetry={props.onRetry} onDismiss={props.onDismiss} mobile />}
      {row1}
      <div className="flex gap-d8">
        {side.map((action) => (
          <button key={action} type="button" data-action={action} disabled={actions.busy} onClick={tap(action)} className={`${mob.small} flex-1`}>{ACTION_LABELS[action]}</button>
        ))}
        <button type="button" onClick={props.onPrevious} className={`${mob.move} flex-1`}>← Previous</button>
        {!actions.resolved && <button type="button" onClick={props.onNext} className={`${mob.move} flex-1`}>Next →</button>}
      </div>
    </div>
  );
}

export function MobileItem(props: ItemScreenProps) {
  const { view } = props;
  const changedKeys = props.change?.keys ?? [];
  return (
    <>
      <MobileHeader {...props} />
      {props.banner && <StatusBanner banner={props.banner} mobile />}
      <div className="flex min-h-0 flex-1 flex-col gap-d16 overflow-auto px-d16 pb-d24 pt-d16">
        <StatePanels props={props} mobile />
        <ItemHeading view={view} mobile changedKeys={changedKeys} />
        <SlotBlocks view={view} changedKeys={changedKeys} mobile />
        <DescriptionSection view={view} answerBox={props.answerBox} />
        <OutreachBlock view={view} />
        <StepsSection view={view} mobile first={false} changedKeys={changedKeys} />
        <PromptSection key={view.id} view={view} mobile changedKeys={changedKeys} />
        <EvidenceSection view={view} emphasis={props.evidenceEmphasis} message={props.evidenceMessage} mobile />
        <FreshnessSection view={view} mobile />
        <FeedbackSection view={view} />
      </div>
      <ActionBar props={props} />
      {props.panel}
    </>
  );
}
