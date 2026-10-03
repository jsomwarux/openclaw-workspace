"use client";
// Confirm panels and the park form. Inline in the decision pane on desktop; bottom sheets on
// mobile. The confirm button takes focus on open (KEYBOARD.md, Accessibility).
import { useEffect, useRef } from "react";
import type { FormEvent, ReactNode } from "react";
import { cx as cn } from "./cx";
import type { DeferOption, DeferOptionId } from "@/lib/cockpit/defer";
import type { ParkErrors } from "@/lib/cockpit/block";
import { desk, focusRing, mobile as mob } from "./primitives";

function Frame({ mobile, label, role = "alertdialog", onCancel, children }: { mobile: boolean; label: string; role?: "alertdialog" | "group"; onCancel: () => void; children: ReactNode }) {
  if (!mobile) {
    return (
      <div role={role} aria-label={label} className="flex flex-col gap-d10 rounded-card border border-mc-line-control bg-mc-page px-d14 py-d12">
        {children}
      </div>
    );
  }
  return (
    <div className="fixed inset-0 z-[80]">
      <div aria-hidden="true" onClick={onCancel} className="absolute inset-0 bg-[var(--mc-scrim)]" />
      <div
        role={role}
        aria-label={label}
        aria-modal="true"
        className="absolute inset-x-0 bottom-0 flex max-h-[92%] flex-col gap-d12 overflow-auto rounded-t-sheet border-t border-mc-line-strong bg-mc-surface px-d16 pb-[calc(16px+env(safe-area-inset-bottom))] pt-d20"
      >
        {children}
      </div>
    </div>
  );
}

function Title({ mobile, children }: { mobile: boolean; children: ReactNode }) {
  return <div className={mobile ? "text-mc-18 font-bold" : "font-semibold"}>{children}</div>;
}

function Body({ children }: { children: ReactNode }) {
  return <div className="text-mc-ink-secondary">{children}</div>;
}

function Buttons({ mobile, confirm, onCancel, hint = true }: { mobile: boolean; confirm: ReactNode; onCancel: () => void; hint?: boolean }) {
  if (mobile) {
    return (
      <>
        {confirm}
        <button type="button" onClick={onCancel} className={mob.secondary}>Cancel</button>
      </>
    );
  }
  return (
    <div className="flex flex-wrap items-center gap-d8">
      {confirm}
      <button type="button" onClick={onCancel} className={desk.cancel}>Cancel</button>
      {hint && <span className="text-mc-12 text-mc-ink-muted">Enter confirms · Esc cancels</span>}
    </div>
  );
}

export function CompletePanel({ mobile, body, onConfirm, onCancel, busy }: { mobile: boolean; body: string; onConfirm: () => void; onCancel: () => void; busy: boolean }) {
  return (
    <Frame mobile={mobile} label="Confirm complete" onCancel={onCancel}>
      <Title mobile={mobile}>Mark this item done?</Title>
      <Body>{body}</Body>
      <Buttons
        mobile={mobile}
        onCancel={onCancel}
        confirm={<button type="button" autoFocus disabled={busy} onClick={onConfirm} className={mobile ? mob.primary : desk.confirm}>Complete</button>}
      />
    </Frame>
  );
}

export function DeferPanel({
  mobile, options, choice, date, minDate, error, onChoose, onDate, onConfirm, onCancel, busy,
}: {
  mobile: boolean;
  options: DeferOption[];
  choice: DeferOptionId;
  date: string;
  minDate: string;
  error: string | null;
  onChoose: (id: DeferOptionId) => void;
  onDate: (value: string) => void;
  onConfirm: () => void;
  onCancel: () => void;
  busy: boolean;
}) {
  return (
    <Frame mobile={mobile} label="Confirm defer" onCancel={onCancel}>
      <Title mobile={mobile}>Defer this item?</Title>
      <Body>It is snoozed and leaves today&apos;s run. It comes back at the time you choose.</Body>
      <fieldset className="m-0 flex flex-col gap-d6 border-0 p-0">
        <legend className="sr-only">Defer until</legend>
        {options.map((option) => (
          <label key={option.id} className={cn("flex items-start gap-d8", mobile && "min-h-[44px] items-center", option.disabledReason && "text-mc-ink-muted")}>
            <input
              type="radio"
              name="defer-until"
              value={option.id}
              checked={choice === option.id}
              disabled={option.disabledReason !== null}
              onChange={() => onChoose(option.id)}
              className={`${focusRing} mt-[3px] accent-[var(--mc-accent)]`}
            />
            <span className="flex flex-col">
              <span className="font-semibold">{option.label}</span>
              {option.detail && <span className="font-mc-mono text-mc-12 text-mc-ink-muted">{option.detail}</span>}
              {option.disabledReason && <span className="text-mc-12">{option.disabledReason}</span>}
            </span>
          </label>
        ))}
        {choice === "date" && (
          <label className="flex flex-col gap-d3 text-mc-13 font-medium">
            Date
            <input
              type="date"
              value={date}
              min={minDate}
              onChange={(event) => onDate(event.target.value)}
              className={cn(focusRing, "w-[200px] rounded-btn border border-mc-line-control bg-mc-surface px-d9 py-d7 font-mc-sans text-mc-ink", mobile ? "min-h-[44px] text-[16px]" : "text-mc-14")}
            />
          </label>
        )}
        {error && <span role="alert" className="text-mc-12 font-medium text-mc-error">{error}</span>}
      </fieldset>
      <Buttons
        mobile={mobile}
        onCancel={onCancel}
        confirm={<button type="button" autoFocus disabled={busy} onClick={onConfirm} className={mobile ? mob.primary : desk.confirm}>Defer</button>}
      />
    </Frame>
  );
}

export function DecisionPanel({
  mobile, kind, note, error, onNote, onConfirm, onCancel, busy,
}: {
  mobile: boolean;
  kind: "approve" | "reject";
  note: string;
  error: string | null;
  onNote: (value: string) => void;
  onConfirm: () => void;
  onCancel: () => void;
  busy: boolean;
}) {
  const confirmRef = useRef<HTMLButtonElement>(null);
  useEffect(() => confirmRef.current?.focus(), []);
  const approve = kind === "approve";
  return (
    <Frame mobile={mobile} label={approve ? "Confirm approve" : "Confirm reject"} onCancel={onCancel}>
      <Title mobile={mobile}>{approve ? "Approve this item?" : "Reject this item?"}</Title>
      <Body>
        {approve
          ? "Your decision is saved as a note on this item and it leaves today's run. It records your decision; it does not authorize anything else. This cannot be undone."
          : "It closes for good and leaves today's run. This cannot be undone."}
      </Body>
      <label className="flex flex-col gap-d3 text-mc-13 font-medium">
        Note (optional)
        <textarea
          value={note}
          rows={3}
          onChange={(event) => onNote(event.target.value)}
          aria-invalid={error ? true : undefined}
          className={cn(focusRing, "w-full resize-y rounded-btn border border-mc-line-control bg-mc-surface px-d9 py-d7 font-mc-sans font-normal text-mc-ink", mobile ? "text-[16px]" : "text-mc-14")}
        />
        {error && <span role="alert" className="text-mc-12 font-medium text-mc-error">{error}</span>}
      </label>
      <Buttons
        mobile={mobile}
        onCancel={onCancel}
        confirm={
          <button ref={confirmRef} type="button" disabled={busy} onClick={onConfirm} className={approve ? (mobile ? mob.primary : desk.confirm) : mobile ? mob.ink : desk.confirmInk}>
            {approve ? "Approve" : "Reject"}
          </button>
        }
      />
    </Frame>
  );
}

export interface ParkDraft { who: string; what: string; days: string }

export function BlockForm({
  mobile, draft, errors, onChange, onSubmit, onCancel, busy,
}: {
  mobile: boolean;
  draft: ParkDraft;
  errors: ParkErrors;
  onChange: (draft: ParkDraft) => void;
  onSubmit: () => void;
  onCancel: () => void;
  busy: boolean;
}) {
  const field = (key: keyof ParkDraft, label: string, extra: string, type: "text" | "number" = "text") => (
    <label className={cn("flex flex-col gap-d3", mobile ? "text-mc-14 font-semibold" : "text-mc-13 font-medium", extra)}>
      {label}
      <input
        type={type}
        inputMode={type === "number" ? "numeric" : undefined}
        min={type === "number" ? 1 : undefined}
        max={type === "number" ? 365 : undefined}
        autoFocus={key === "who"}
        value={draft[key]}
        onChange={(event) => onChange({ ...draft, [key]: event.target.value })}
        aria-invalid={errors[key] ? true : undefined}
        className={cn(focusRing, "rounded-btn border border-mc-line-control bg-mc-surface px-d9 py-d7 font-mc-sans font-normal text-mc-ink", mobile ? "min-h-[44px] rounded-card text-[16px]" : "text-mc-14")}
      />
      {errors[key] && <span role="alert" className="text-mc-12 font-medium text-mc-error">{errors[key]}</span>}
    </label>
  );
  const submit = (event: FormEvent) => {
    event.preventDefault();
    onSubmit();
  };
  return (
    <Frame mobile={mobile} label="Park on a person" role="group" onCancel={onCancel}>
      <form onSubmit={submit} noValidate className="flex flex-col gap-d10">
        <Title mobile={mobile}>Park this item on a person</Title>
        <Body>It leaves today&apos;s run and returns when the nudge is due.</Body>
        {field("who", "Who are you waiting on", "")}
        {field("what", "What are you waiting for", "")}
        {field("days", "Nudge after (days)", mobile ? "w-[160px]" : "w-[140px]", "number")}
        <div className={cn(mobile ? "flex flex-col gap-d12" : "flex gap-d8")}>
          <button type="submit" disabled={busy} className={mobile ? mob.primary : desk.confirm}>Park it</button>
          <button type="button" onClick={onCancel} className={mobile ? mob.secondary : desk.cancel}>Cancel</button>
        </div>
      </form>
    </Frame>
  );
}
