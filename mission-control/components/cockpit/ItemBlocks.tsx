"use client";
// The blocks of the current item, shared by the desktop panes and the mobile column.
import { useEffect, useRef, useState } from "react";
import type { ReactNode, RefObject } from "react";
import { cx as cn } from "./cx";
import { changedPhrase, changeRows, trackedFields } from "@/lib/cockpit/changes";
import { inlineSegments } from "@/lib/cockpit/description";
import type { DescriptionBlock } from "@/lib/cockpit/description";
import { formatShort } from "@/lib/cockpit/format";
import type { OpenItemChange } from "@/lib/cockpit/controller";
import type { ItemViewModel } from "@/lib/cockpit/view";
import type { FeedbackEntry, Verbatim } from "@/lib/cockpit/types";
import { FromDescriptionChip, MissingChip, MonoLabel, NoticePanel, button, desk, focusRing, mobile as mob } from "./primitives";

// ---- inline text ------------------------------------------------------------------------

function Inline({ text }: { text: string }) {
  return (
    <>
      {inlineSegments(text).map((segment, i) => (segment.bold ? <strong key={i} className="font-semibold">{segment.text}</strong> : <span key={i}>{segment.text}</span>))}
    </>
  );
}

// ---- state panels -----------------------------------------------------------------------

export function ChangedPanel({ change, timeZone, onAck, mobile }: { change: OpenItemChange; timeZone: string; onAck: () => void; mobile: boolean }) {
  const phrase = changedPhrase(change.keys);
  const when = typeof change.task.updatedAt === "number" ? ` at ${formatShort(change.task.updatedAt, timeZone)}` : "";
  const rows = changeRows(change.keys, change.before, trackedFields(change.task), timeZone);
  return (
    <NoticePanel tag="Changed while you were looking">
      <div className="text-mc-16 font-semibold">{`Another writer edited this item${when}. ${phrase.charAt(0).toUpperCase()}${phrase.slice(1)} changed.`}</div>
      {rows.map((row) => (
        <div key={row.label} className="flex flex-col gap-d6">
          <div className="flex flex-col gap-d2">
            <MonoLabel>{rows.length > 1 ? `Previous version · ${row.label}` : "Previous version"}</MonoLabel>
            <div className={cn("whitespace-pre-wrap text-mc-ink-muted [overflow-wrap:anywhere]", row.long && "max-h-40 overflow-auto")}>{row.before}</div>
          </div>
          <div className="flex flex-col gap-d2">
            <MonoLabel>Now</MonoLabel>
            <div className={cn("whitespace-pre-wrap [overflow-wrap:anywhere]", row.long && "max-h-40 overflow-auto")}>{row.after}</div>
          </div>
        </div>
      ))}
      <button type="button" onClick={onAck} className={cn(mobile ? `${mob.primary} self-start px-d18` : `${desk.primary} self-start font-bold`)}>
        I have read the new version
      </button>
    </NoticePanel>
  );
}

export function ExpiredPanel({ text }: { text: string }) {
  return (
    <NoticePanel tag="Expired">
      <div className="text-mc-16 font-semibold">{text}</div>
      <div>Approval is no longer possible. You can still reject it. Moving on leaves it unhandled.</div>
    </NoticePanel>
  );
}

export function InvalidPanel({ reasons, source, onRecheck, mobile }: { reasons: string[]; source: Verbatim<string>; onRecheck: () => void; mobile: boolean }) {
  return (
    <NoticePanel tag="Invalid card">
      <div className="text-mc-16 font-semibold">This card cannot be acted on.</div>
      <ul className="m-0 list-disc pl-d18">
        {reasons.map((reason) => <li key={reason}>{reason}</li>)}
      </ul>
      <div>
        Fix the card where it was created, then check again. Source:{" "}
        {source.kind === "value" ? source.value : "Missing"}.
      </div>
      <button type="button" onClick={onRecheck} className={cn(mobile ? `${mob.secondary} self-start px-d18` : `${desk.secondary} self-start`)}>
        Check again
      </button>
    </NoticePanel>
  );
}

// ---- heading and slots ------------------------------------------------------------------

export function ItemHeading({ view, mobile, changedKeys = [] }: { view: ItemViewModel; mobile: boolean; changedKeys?: string[] }) {
  return (
    <>
      <div className="flex flex-col gap-d2">
        <div className="font-mc-mono text-mc-12 font-medium text-mc-ink-muted">{mobile ? view.mobileEyebrow : view.eyebrow}</div>
        {view.exception && <div className="font-mc-mono text-mc-12 font-semibold text-mc-ink">{view.exception.text}</div>}
        {changedKeys.includes("title") && <MonoLabel className="text-mc-ink">Title · Changed</MonoLabel>}
      </div>
      <h1 className={cn("m-0 font-bold tracking-[-.015em] [overflow-wrap:anywhere] [text-wrap:balance]", mobile ? "text-mc-22 leading-[1.22]" : "text-mc-24 leading-[1.2]")}>
        {view.titleText}
      </h1>
    </>
  );
}

function changedMark(keys: string[], typedKey: string, slot: Verbatim<string>) {
  const changed = keys.includes(typedKey) || (slot.kind === "value" && slot.source === "description" && keys.includes("description"));
  return changed ? " · Changed" : "";
}

export function FirstActionBlock({ slot, changedKeys, mobile }: { slot: Verbatim<string>; changedKeys: string[]; mobile: boolean }) {
  const missing = slot.kind === "missing";
  return (
    <div
      className={cn(
        "flex flex-col gap-d6 rounded-card",
        missing ? "border-2 border-dashed border-mc-line-missing" : "border-2 border-mc-ink bg-mc-surface",
        missing && (mobile ? "bg-mc-surface" : "bg-mc-page"),
        mobile ? "px-d14 py-d12" : "px-d16 py-d14",
      )}
    >
      <div className="flex flex-wrap items-center gap-d8">
        <MonoLabel>{`First action${changedMark(changedKeys, "firstAction", slot)}`}</MonoLabel>
        {missing ? <MissingChip /> : slot.source === "description" && <FromDescriptionChip />}
      </div>
      <div className="whitespace-pre-wrap text-mc-17 font-semibold leading-[1.35] [overflow-wrap:anywhere]">
        {missing ? "This item has no first action recorded." : slot.value}
      </div>
    </div>
  );
}

export function TextSlot({ label, slot, changed }: { label: string; slot: Verbatim<string>; changed: string }) {
  return (
    <div className="flex flex-col gap-d4">
      <div className="flex flex-wrap items-center gap-d8">
        <MonoLabel>{`${label}${changed}`}</MonoLabel>
        {slot.kind === "missing" ? <MissingChip /> : slot.source === "description" && <FromDescriptionChip />}
      </div>
      {slot.kind === "value" ? <div className="whitespace-pre-wrap [overflow-wrap:anywhere]">{slot.value}</div> : <div className="text-mc-ink-secondary">Not recorded for this item.</div>}
    </div>
  );
}

export function SlotBlocks({ view, changedKeys, mobile }: { view: ItemViewModel; changedKeys: string[]; mobile: boolean }) {
  return (
    <>
      <FirstActionBlock slot={view.slots.firstAction} changedKeys={changedKeys} mobile={mobile} />
      <TextSlot label="Why it matters" slot={view.slots.whyItMatters} changed={changedMark(changedKeys, "whyItMatters", view.slots.whyItMatters)} />
      <TextSlot label="Done when" slot={view.slots.doneState} changed={changedMark(changedKeys, "doneState", view.slots.doneState)} />
      {view.authority && (
        <div className="flex flex-col gap-d3 rounded-card border border-dashed border-mc-ink-muted bg-mc-surface px-d12 py-d10">
          <div className="flex flex-wrap items-center gap-d8">
            <MonoLabel>Authority · needs your approval</MonoLabel>
            {view.authority.text === null && <MissingChip />}
          </div>
          <div className="whitespace-pre-wrap [overflow-wrap:anywhere]">{view.authority.text ?? "No authority boundary is recorded for this item."}</div>
        </div>
      )}
    </>
  );
}

// ---- description and answer box ---------------------------------------------------------

export function AnswerBox({
  value, onChange, error, saved, mobile, textareaRef,
}: {
  value: string;
  onChange: (value: string) => void;
  error: string | null;
  saved: FeedbackEntry | null;
  mobile: boolean;
  textareaRef: RefObject<HTMLTextAreaElement | null>;
}) {
  if (saved) {
    return (
      <div className="flex flex-col gap-d4 rounded-card border border-mc-line-table bg-mc-surface px-d12 py-d10">
        <MonoLabel>Your answer · Saved</MonoLabel>
        <div className="whitespace-pre-wrap [overflow-wrap:anywhere]">{saved.body.slice("Answer: ".length)}</div>
      </div>
    );
  }
  return (
    <label className="flex flex-col gap-d4">
      <MonoLabel>Your answer</MonoLabel>
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        rows={4}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? "answer-error" : undefined}
        className={cn(
          focusRing,
          "w-full resize-y rounded-btn border border-mc-line-control bg-mc-surface px-d9 py-d7 font-mc-sans text-mc-ink",
          mobile ? "text-[16px]" : "text-mc-14",
        )}
      />
      {error && <span id="answer-error" role="alert" className="text-mc-12 font-medium text-mc-error">{error}</span>}
    </label>
  );
}

function Block({ block, answerBox }: { block: DescriptionBlock; answerBox: ReactNode }) {
  switch (block.kind) {
    case "heading":
      return <h2 className="m-0 text-mc-15 font-semibold [overflow-wrap:anywhere]">{block.text}</h2>;
    case "paragraph":
      return (
        <p className="m-0 [overflow-wrap:anywhere]">
          {block.lines.map((line, i) => (
            <span key={i}>
              {i > 0 && <br />}
              <Inline text={line} />
            </span>
          ))}
        </p>
      );
    case "bullets":
      return (
        <ul className="m-0 flex list-disc flex-col gap-d4 pl-d18">
          {block.items.map((item, i) => (
            <li key={i} className="[overflow-wrap:anywhere]">
              {item.label && <strong className="font-semibold">{item.label}</strong>}
              <Inline text={item.text} />
              {item.children.length > 0 && (
                <ol className="m-0 mt-d4 flex list-decimal flex-col gap-d2 pl-d18">
                  {item.children.map((child, j) => <li key={j} value={Number(child.n)}><Inline text={child.text} /></li>)}
                </ol>
              )}
            </li>
          ))}
        </ul>
      );
    case "ordered":
      return (
        <ol className="m-0 flex list-decimal flex-col gap-d2 pl-d18">
          {block.items.map((item, i) => <li key={i} value={Number(item.n)} className="[overflow-wrap:anywhere]"><Inline text={item.text} /></li>)}
        </ol>
      );
    case "answerSlot":
      return <>{answerBox}</>;
  }
}

export function DescriptionSection({ view, answerBox }: { view: ItemViewModel; answerBox: ReactNode }) {
  const blocks = view.descriptionBlocks ?? [];
  const inline = blocks.some((block) => block.kind === "answerSlot");
  if (blocks.length === 0 && !view.answerSlot) return null;
  return (
    <div className="flex flex-col gap-d10">
      {blocks.length > 0 && <MonoLabel>Description</MonoLabel>}
      {blocks.map((block, i) => <Block key={i} block={block} answerBox={answerBox} />)}
      {view.answerSlot && !inline && answerBox}
    </div>
  );
}

export function OutreachBlock({ view }: { view: ItemViewModel }) {
  if (!view.outreach) return null;
  const field = (label: string, value: Verbatim<string>) => (
    <div className="flex flex-col gap-d4">
      <div className="flex items-center gap-d8"><MonoLabel>{label}</MonoLabel>{value.kind === "missing" && <MissingChip />}</div>
      {value.kind === "value" && <div className="whitespace-pre-wrap [overflow-wrap:anywhere]">{value.value}</div>}
    </div>
  );
  return (
    <div className="flex flex-col gap-d12">
      {field("Subject", view.outreach.subject)}
      {field("Body", view.outreach.body)}
      {field("Verifier report", view.outreach.verifierReport)}
    </div>
  );
}

// ---- context sections -------------------------------------------------------------------

const sectionRule = "flex flex-col border-t border-mc-line pt-d16";

export function StepsSection({ view, mobile, first, changedKeys = [] }: { view: ItemViewModel; mobile: boolean; first: boolean; changedKeys?: string[] }) {
  const steps = view.steps;
  const changed = changedKeys.includes("exactSteps") ? " · Changed" : "";
  return (
    <div className={cn("flex flex-col gap-d8", !first && sectionRule)}>
      <div className="flex items-center gap-d8">
        <MonoLabel>{steps.kind === "value" ? `Exact steps · ${steps.value.length}${changed}` : `Exact steps${changed}`}</MonoLabel>
        {steps.kind === "missing" && <MissingChip />}
      </div>
      {steps.kind === "missing" ? (
        <div className="text-mc-ink-secondary">No steps are recorded for this item.</div>
      ) : (
        <ol className={cn("m-0 flex list-none flex-col p-0", mobile ? "gap-d8" : "gap-d6")}>
          {steps.value.map((step, i) => (
            <li key={i} className={cn("flex", mobile ? "gap-d10" : "gap-d12")}>
              <span className={cn("flex-none pt-d1 font-mc-mono text-mc-13 font-medium text-mc-ink-muted", mobile ? "w-[18px]" : "w-[20px]")}>{i + 1}</span>
              <span className="whitespace-pre-wrap [overflow-wrap:anywhere]">{step}</span>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

async function copyText(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch {
    // fall through to the older copy command
  }
  try {
    const area = document.createElement("textarea");
    area.value = text;
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(area);
    return ok;
  } catch {
    return false;
  }
}

export function PromptSection({ view, mobile, changedKeys = [] }: { view: ItemViewModel; mobile: boolean; changedKeys?: string[] }) {
  const promptLabel = changedKeys.includes("pasteReadyPrompt") || changedKeys.includes("pasteDestination") ? "Paste-ready prompt · Changed" : "Paste-ready prompt";
  const [expanded, setExpanded] = useState(false);
  const [copy, setCopy] = useState<"idle" | "copied" | "failed">("idle");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => () => { if (timer.current) clearTimeout(timer.current); }, []);
  const prompt = view.prompt;
  const usable = prompt.kind === "value" && view.validity.ok;

  const onCopy = async () => {
    if (prompt.kind !== "value") return;
    const ok = await copyText(prompt.value);
    setCopy(ok ? "copied" : "failed");
    if (timer.current) clearTimeout(timer.current);
    if (ok) timer.current = setTimeout(() => setCopy("idle"), 1800);
  };

  const destination = (
    <div className={cn("flex gap-d8", mobile ? "flex-wrap items-baseline" : "items-baseline")}>
      <span className="flex-none text-mc-13 font-semibold">Where to paste</span>
      {view.destination.kind === "value" ? <span className="[overflow-wrap:anywhere]">{view.destination.value}</span> : <MissingChip />}
    </div>
  );
  const failure = copy === "failed" && (
    <div role="alert" className="text-mc-13 font-medium text-mc-error">The prompt could not be copied. Select the text below and copy it by hand.</div>
  );
  const box = usable && (
    <pre
      tabIndex={0}
      aria-label="Paste-ready prompt text"
      className={cn(
        focusRing,
        "m-0 overflow-auto whitespace-pre-wrap rounded-card border border-mc-line-table bg-mc-surface font-mc-mono font-normal leading-[1.55] text-mc-ink [overflow-wrap:anywhere]",
        mobile ? "px-d12 py-d10 text-mc-12" : "px-d14 py-d12 text-[calc(var(--mc-fs,14px)*0.8929)]",
        mobile ? (expanded ? "h-[480px]" : "h-[240px]") : expanded ? "h-[640px]" : "h-[300px]",
      )}
    >
      {prompt.value}
    </pre>
  );
  const copyLabel = copy === "copied" ? "Copied" : "Copy prompt";

  if (mobile) {
    return (
      <div className={cn("gap-d8", sectionRule)}>
        <div className="flex items-baseline gap-d8">
          <MonoLabel>{promptLabel}</MonoLabel>
          <span className="flex-1 text-right font-mc-mono text-mc-11 text-mc-ink-muted">{view.promptMeta}</span>
        </div>
        {destination}
        {usable && (
          <button type="button" onClick={onCopy} className={`${focusRing} min-h-[48px] w-full cursor-pointer rounded-card border border-mc-accent-deep bg-mc-accent-tint text-mc-15 font-bold text-mc-accent-ink transition-transform duration-[160ms] ease-out active:scale-[.97]`}>
            {copyLabel}
          </button>
        )}
        {failure}
        {box}
        {usable && (
          <button type="button" onClick={() => setExpanded(!expanded)} className={`${mob.move} w-full`}>
            {expanded ? "Collapse" : "Show more"}
          </button>
        )}
      </div>
    );
  }
  return (
    <div className={cn("gap-d8", sectionRule)}>
      <div className="flex items-center gap-d12">
        <MonoLabel>{promptLabel}</MonoLabel>
        <span className="flex-1 font-mc-mono text-mc-12 text-mc-ink-muted">{view.promptMeta}</span>
        {usable && (
          <>
            <button type="button" onClick={() => setExpanded(!expanded)} className={`${button.quiet} rounded-btn px-d10 py-d5 text-mc-13 font-medium`}>
              {expanded ? "Collapse" : "Show more"}
            </button>
            <button type="button" onClick={onCopy} className={`${button.primary} min-w-[112px] rounded-btn px-d12 py-d5 text-mc-13`}>
              {copyLabel}
            </button>
          </>
        )}
      </div>
      {destination}
      {failure}
      {box}
    </div>
  );
}

export function EvidenceSection({ view, emphasis, message, mobile = false }: { view: ItemViewModel; emphasis: boolean; message: string | null; mobile?: boolean }) {
  const [copied, setCopied] = useState<string | null>(null);
  const count = view.evidence.length;
  return (
    <div className={cn("gap-d6", sectionRule)}>
      <div className="flex items-center gap-d8">
        <MonoLabel>{count > 0 ? `Evidence links · ${count}` : "Evidence links"}</MonoLabel>
        {count === 0 && <MissingChip emphasis={emphasis} />}
      </div>
      {count === 0 ? (
        <div className="text-mc-ink-secondary">No links are recorded for this item.</div>
      ) : (
        <ul className="m-0 flex list-none flex-col gap-d4 p-0">
          {view.evidence.map((entry, i) => (
            <li key={`${entry.text}-${i}`} className="font-mc-mono text-mc-12">
              {entry.kind === "web" ? (
                <a href={entry.text} target="_blank" rel="noopener noreferrer" className={cn(focusRing, "text-mc-accent-deep [overflow-wrap:anywhere] hover:text-mc-ink", mobile && "inline-flex min-h-[44px] items-center")}>
                  {entry.text}
                </a>
              ) : (
                <span className="flex flex-wrap items-baseline gap-d8">
                  <span className="[overflow-wrap:anywhere]">{entry.text}</span>
                  <button
                    type="button"
                    onClick={async () => setCopied((await copyText(entry.text)) ? entry.text : null)}
                    className={cn(button.link, "p-0 font-mc-sans text-mc-12", mobile && "min-h-[44px] min-w-[44px] px-d8")}
                  >
                    {copied === entry.text ? "Path copied" : "Copy path"}
                  </button>
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
      {message && <div role="status" className="text-mc-13 font-medium">{message}</div>}
    </div>
  );
}

export function FreshnessSection({ view, mobile }: { view: ItemViewModel; mobile: boolean }) {
  const row = (label: string, value: ReactNode) => (
    <>
      <dt className="font-semibold">{label}</dt>
      <dd className="m-0 [overflow-wrap:anywhere]">{value}</dd>
    </>
  );
  const verbatim = (value: Verbatim<string>) => (value.kind === "value" ? value.value : <MissingChip />);
  return (
    <div className={cn("gap-d8", sectionRule)}>
      <MonoLabel>Freshness and source</MonoLabel>
      <dl className={cn("m-0 grid gap-x-d16 gap-y-d6", mobile ? "grid-cols-[108px_1fr] gap-x-d12" : "grid-cols-[150px_1fr]")}>
        {row("Last changed", view.freshness.lastChanged ?? <MissingChip />)}
        {row("Created", view.freshness.created ?? <MissingChip />)}
        {row("Source", verbatim(view.freshness.source))}
        {row("Project", verbatim(view.freshness.project))}
        {row("Description", view.freshness.description === "present" ? "Recorded. Shown with the item." : <MissingChip />)}
      </dl>
    </div>
  );
}

export function FeedbackSection({ view }: { view: ItemViewModel }) {
  return (
    <div className={cn("gap-d6", sectionRule)}>
      <MonoLabel>{view.feedback.length > 0 ? `Feedback history · ${view.feedback.length}` : "Feedback history"}</MonoLabel>
      {view.feedback.length === 0 ? (
        <div className="text-mc-ink-secondary">None recorded.</div>
      ) : (
        <ol className="m-0 flex list-none flex-col p-0">
          {view.feedback.map((entry) => (
            <li key={entry.id} className="flex flex-col gap-d4 border-t border-mc-line-soft py-d10 first:border-t-0 first:pt-d4">
              <span className="font-mc-mono text-mc-12 text-mc-ink-muted">{`${entry.author} · ${entry.when}`}</span>
              <span className="whitespace-pre-wrap [overflow-wrap:anywhere]">{entry.body}</span>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
