"use client";
// The daily cockpit at /cockpit. Owns UI-only state (open panel, queue, overlay, drafts) and
// wires the framework-free controller to the screens, the keyboard and the poll.
import { useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore } from "react";
import type { ReactNode } from "react";
import { cx as cn } from "./cx";
import { httpApi } from "@/lib/cockpit/api";
import { savedAnswer, validateAnswer, validateDecisionNote } from "@/lib/cockpit/answer";
import { validatePark } from "@/lib/cockpit/block";
import type { ParkErrors } from "@/lib/cockpit/block";
import { changeClosingLine, changeHeadline } from "@/lib/cockpit/changes";
import { CockpitController } from "@/lib/cockpit/controller";
import type { CockpitState } from "@/lib/cockpit/controller";
import { deferAvailable, deferOptions, untilForDate } from "@/lib/cockpit/defer";
import type { DeferOptionId } from "@/lib/cockpit/defer";
import { browserTimeZone, formatLongDay, formatShort, formatShortDay, localDateKey, relativeAgo } from "@/lib/cockpit/format";
import { POLL_MS, retryDelay } from "@/lib/cockpit/freshness";
import { resolveKey } from "@/lib/cockpit/keyboard";
import type { KeyCommand, KeyPanel } from "@/lib/cockpit/keyboard";
import { groupOf } from "@/lib/cockpit/order";
import { browserStorage, runStorage } from "@/lib/cockpit/storage";
import { buildItemView, liveStatus, nothingToOpen, queueView, runStartView, summaryView } from "@/lib/cockpit/view";
import type { QueueRowView } from "@/lib/cockpit/view";
import type { RawTask } from "@/lib/cockpit/types";
import { DesktopHeader, DesktopItem } from "./DesktopItem";
import { AnswerBox } from "./ItemBlocks";
import { MobileHeader, MobileItem } from "./MobileItem";
import { BlockForm, CompletePanel, DecisionPanel, DeferPanel } from "./Panels";
import type { ParkDraft } from "./Panels";
import { LoadingDesktop, LoadingMobile, ShortcutsOverlay } from "./Overlays";
import { QueueSheet, QueueView } from "./Queue";
import { BarButton, ChangeBanner, EmptyRunContent, ResumeContent, RunShell, RunStartContent, SummaryContent } from "./RunScreens";
import type { ActionModel, Banner, ButtonAction, ItemScreenProps, RailRow } from "./model";

type Panel = Exclude<KeyPanel, null | "saveAnswer">;

interface Session {
  controller: CockpitController;
  timeZone: string;
  prepare?: (controller: CockpitController) => Promise<void>;
}

const NETWORK_BODY = "Nothing was changed. The connection dropped while saving. If this keeps happening, check that you are on your private network.";
const REFUSED_BODY = "Nothing was changed. Mission Control refused the change. Check the item, then try again.";
const PARTIAL_BODY = "Your note was saved, but the item was not marked done. Retry finishes the change.";

function useDesktop(): boolean {
  const query = "(min-width: 760px)";
  return useSyncExternalStore(
    (notify) => {
      const list = window.matchMedia(query);
      list.addEventListener("change", notify);
      return () => list.removeEventListener("change", notify);
    },
    () => window.matchMedia(query).matches,
    () => true,
  );
}

function Frame({ desktop, children }: { desktop: boolean; children: ReactNode }) {
  return (
    <div className="fixed inset-0 z-[60] overflow-auto bg-mc-page font-mc-sans leading-[1.45] text-mc-ink [&_*::-webkit-scrollbar-thumb]:bg-mc-line-strong">
      <div className={cn("flex h-full flex-col", desktop ? "min-h-[640px] min-w-[1100px] text-mc-14" : "text-mc-15")}>{children}</div>
    </div>
  );
}

export function CockpitApp() {
  const desktop = useDesktop();
  const [session, setSession] = useState<Session | null>(null);
  useEffect(() => {
    let cancelled = false;
    const timeZone = browserTimeZone();
    const scenario = new URLSearchParams(window.location.search).get("fixture");
    const start = async () => {
      // Development only: production builds drop this branch and the fixture chunk entirely.
      if (process.env.NODE_ENV !== "production" && process.env.NEXT_PUBLIC_COCKPIT_FIXTURES === "1" && scenario) {
        const { fixtureSession } = await import("@/lib/cockpit/fixtures/harness");
        const fixture = fixtureSession(scenario, timeZone);
        const controller = new CockpitController({ api: fixture.api, clock: fixture.clock, storage: fixture.storage, timeZone });
        if (!cancelled) setSession({ controller, timeZone, prepare: fixture.prepare });
        return;
      }
      const controller = new CockpitController({ api: httpApi(), clock: () => Date.now(), storage: runStorage(browserStorage()), timeZone });
      if (!cancelled) setSession({ controller, timeZone });
    };
    void start();
    return () => {
      cancelled = true;
    };
  }, []);
  if (!session) return <Frame desktop={desktop}>{desktop ? <LoadingDesktop /> : <LoadingMobile />}</Frame>;
  return <Cockpit session={session} desktop={desktop} />;
}

function Cockpit({ session, desktop }: { session: Session; desktop: boolean }) {
  const { controller, timeZone } = session;
  const state: CockpitState = useSyncExternalStore(controller.subscribe, controller.getState, controller.getState);
  const now = state.now;

  // ---- UI-only state ---------------------------------------------------------------------
  const [panel, setPanel] = useState<Panel | null>(null);
  const [queueOpen, setQueueOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [queueNotice, setQueueNotice] = useState<string | null>(null);
  const [evidenceMessage, setEvidenceMessage] = useState<string | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [answerError, setAnswerError] = useState<string | null>(null);
  const [deferChoice, setDeferChoice] = useState<DeferOptionId>("tomorrow");
  const [deferDate, setDeferDate] = useState("");
  const [deferError, setDeferError] = useState<string | null>(null);
  const [note, setNote] = useState("");
  const [noteError, setNoteError] = useState<string | null>(null);
  const [park, setPark] = useState<ParkDraft>({ who: "", what: "", days: "14" });
  const [parkErrors, setParkErrors] = useState<ParkErrors>({});
  const answerRef = useRef<HTMLTextAreaElement | null>(null);

  // ---- load, poll, visibility ------------------------------------------------------------
  const loaded = useRef(false);
  useEffect(() => {
    // Strict Mode runs effects twice in development; load and prepare exactly once.
    if (loaded.current) return;
    loaded.current = true;
    void (async () => {
      await controller.load();
      if (session.prepare) await session.prepare(controller);
    })();
  }, [controller, session]);

  useEffect(() => {
    const poll = setInterval(() => void controller.refresh(), POLL_MS);
    const tick = setInterval(() => controller.tick(), 30_000);
    const visibility = () => (document.hidden ? controller.onHidden() : void controller.onVisible());
    document.addEventListener("visibilitychange", visibility);
    return () => {
      clearInterval(poll);
      clearInterval(tick);
      document.removeEventListener("visibilitychange", visibility);
    };
  }, [controller]);

  const connection = controller.connection();
  useEffect(() => {
    if (connection !== "degraded" && !(connection === "checking" && state.health.consecutiveBad > 0)) return;
    const retry = setTimeout(() => void controller.refresh(), retryDelay(Math.max(2, state.health.consecutiveBad)));
    return () => clearTimeout(retry);
  }, [controller, connection, state.health.consecutiveBad, state.health.lastAttemptAt]);

  // ---- the current item ------------------------------------------------------------------
  const run = state.run;
  const item = controller.currentItem();
  const task = controller.currentTask();
  const itemKey = `${state.screen}:${run?.cursor ?? -1}:${item?.id ?? ""}`;
  useEffect(() => {
    setPanel(null);
    setAnswerError(null);
    setEvidenceMessage(null);
  }, [itemKey]);

  useEffect(() => {
    if (!queueNotice) return;
    const timer = setTimeout(() => setQueueNotice(null), 4000);
    return () => clearTimeout(timer);
  }, [queueNotice]);

  useEffect(() => {
    if (!state.notice) return;
    const timer = setTimeout(() => controller.clearNotice(), 4000);
    return () => clearTimeout(timer);
  }, [controller, state.notice]);

  const permitted = item && task ? (controller.permitted() as string[]) : [];
  const canDefer = Boolean(task && permitted.includes("defer") && deferAvailable(task, now, timeZone));
  const resolved = Boolean(item?.outcome);

  // The action buttons are replaced by the panel while it is open, so focus returns to the
  // re-rendered button for the same action rather than to the detached element.
  const [focusAction, setFocusAction] = useState<Panel | null>(null);
  useEffect(() => {
    if (panel || !focusAction) return;
    document.querySelector<HTMLElement>(`[data-action="${focusAction}"]`)?.focus();
    setFocusAction(null);
  }, [panel, focusAction]);

  const panelRef = useRef(panel);
  panelRef.current = panel;
  const closePanel = useCallback((restoreFocus = true) => {
    if (restoreFocus) setFocusAction(panelRef.current);
    setPanel(null);
  }, []);

  const openPanel = useCallback((next: Panel) => {
    setPanel(next);
    if (next === "defer") {
      setDeferChoice("tomorrow");
      setDeferDate("");
      setDeferError(null);
    }
    if (next === "approve" || next === "reject") {
      setNote("");
      setNoteError(null);
    }
    if (next === "block") {
      setPark({ who: "", what: "", days: "14" });
      setParkErrors({});
    }
  }, []);

  const saveAnswer = useCallback(async () => {
    if (!item) return;
    const result = validateAnswer(answers[item.id] ?? "");
    if (!result.ok) {
      setAnswerError(result.error);
      answerRef.current?.focus();
      return;
    }
    setAnswerError(null);
    await controller.act({ action: "saveAnswer", text: answers[item.id] ?? "" });
  }, [answers, controller, item]);

  const onAction = useCallback((action: ButtonAction) => {
    if (action === "start") void controller.act({ action: "start" });
    else if (action === "saveAnswer") void saveAnswer();
    else openPanel(action);
  }, [controller, openPanel, saveAnswer]);

  const confirmPanel = useCallback(async () => {
    if (!panel || !task) return;
    if (panel === "complete") {
      closePanel(false);
      await controller.act({ action: "complete" });
    } else if (panel === "defer") {
      const option = deferOptions(task, now, timeZone).find((candidate) => candidate.id === deferChoice);
      let until: number | null = null;
      if (deferChoice === "date") {
        const picked = untilForDate(task, deferDate, now, timeZone);
        if (!picked.ok) return setDeferError(picked.error);
        until = picked.until;
      } else if (option && !option.disabledReason) {
        until = option.until;
      }
      if (until === null) return setDeferError("Choose when the item comes back.");
      closePanel(false);
      await controller.act({ action: "defer", until });
    } else if (panel === "approve" || panel === "reject") {
      const check = validateDecisionNote(note);
      if (!check.ok) return setNoteError(check.error);
      closePanel(false);
      await controller.act({ action: panel, note });
    } else if (panel === "block") {
      const check = validatePark(park);
      if (!check.ok) return setParkErrors(check.errors);
      closePanel(false);
      await controller.act({ action: "block", park: check.value });
    }
  }, [closePanel, controller, deferChoice, deferDate, note, now, panel, park, task, timeZone]);

  const openEvidence = useCallback(() => {
    const evidence = task ? buildItemView(task, item!, run!, now, timeZone).evidence : [];
    const link = evidence.find((entry) => entry.kind === "web");
    if (link) {
      window.open(link.text, "_blank", "noopener,noreferrer");
      return;
    }
    setEvidenceMessage(nothingToOpen(evidence));
    setTimeout(() => setEvidenceMessage(null), 3500);
  }, [item, now, run, task, timeZone]);

  const reviewQueue = useCallback(async () => {
    if (state.screen === "runResume") await controller.acknowledgeAndResume();
    setQueueOpen(true);
  }, [controller, state.screen]);

  const openQueueRow = useCallback((row: QueueRowView) => {
    if (row.inRun && run) {
      setQueueOpen(false);
      controller.goTo(row.id);
    } else if (row.inRun) {
      setQueueNotice("The run has not started yet. Start the run to open its items.");
    } else {
      setQueueNotice("This item is not in today's run. Open it from the Work list in the current interface.");
    }
  }, [controller, run]);

  // ---- keyboard --------------------------------------------------------------------------
  const commands = useRef<(command: KeyCommand) => void>(() => {});
  commands.current = (command: KeyCommand) => {
    switch (command) {
      case "next": setPanel(null); void controller.next(); break;
      case "previous": setPanel(null); controller.previous(); break;
      case "openComplete": openPanel("complete"); break;
      case "openDefer": openPanel("defer"); break;
      case "openEvidence": openEvidence(); break;
      case "toggleQueue": setQueueOpen((open) => !open); break;
      case "openHelp": setHelpOpen(true); break;
      case "confirmPanel": void confirmPanel(); break;
      case "startRun": controller.startRun(); break;
      case "resumeRun": void controller.acknowledgeAndResume(); break;
      case "escape":
        if (helpOpen) setHelpOpen(false);
        else if (queueOpen) setQueueOpen(false);
        else if (panel) closePanel();
        break;
    }
  };
  const keyContext = {
    screen: state.screen,
    desktop,
    helpOpen,
    queueOpen,
    panel: panel as KeyPanel,
    canComplete: !resolved && permitted.includes("complete"),
    canDefer: !resolved && canDefer,
  };
  const contextRef = useRef(keyContext);
  contextRef.current = keyContext;
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null;
      const command = resolveKey(
        { key: event.key, ctrlKey: event.ctrlKey, metaKey: event.metaKey, altKey: event.altKey, shiftKey: event.shiftKey, repeat: event.repeat, targetTag: target?.tagName, targetEditable: target?.isContentEditable },
        contextRef.current,
      );
      if (!command) return;
      event.preventDefault();
      commands.current(command);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  // ---- derived text ----------------------------------------------------------------------
  const lastGood = state.health.lastGoodAt;
  const freshText = connection === "checking" ? "Checking…"
    : connection === "stale" ? `Out of date · last checked ${formatShort(lastGood!, timeZone)}`
      : connection === "degraded" ? `Connection unreliable · last checked ${formatShort(lastGood!, timeZone)}`
        : `Up to date · checked ${formatShort(lastGood!, timeZone)}`;
  const freshShort = connection === "checking" ? "Checking…" : connection === "stale" ? "Out of date" : connection === "degraded" ? "Connection unreliable" : "Up to date";
  const banner: Banner | null = connection === "stale"
    ? { tag: "Out of date", text: `Last checked ${formatShort(lastGood!, timeZone)} (${relativeAgo(lastGood!, now)}). This item may have changed since.`, button: "Refresh now", onClick: () => void controller.refresh() }
    : connection === "degraded"
      ? { tag: "Connection", text: `The connection is slow or dropping. Showing the copy from ${formatShort(lastGood!, timeZone)}. Retrying automatically.`, button: "Retry now", onClick: () => void controller.refresh() }
      : null;
  const positionText = run ? `${run.cursor + 1} of ${run.size}` : "";
  const handledCount = run ? run.items.filter((entry) => entry.outcome).length : 0;
  const handledText = `${handledCount} handled`;
  const today = formatShortDay(now, timeZone);
  const queue = useMemo(() => queueView(state.tasks, run, now, timeZone), [state.tasks, run, now, timeZone]);
  const byId = useMemo(() => new Map(state.tasks.map((entry) => [entry._id, entry])), [state.tasks]);

  // ---- overlays shared by every screen ---------------------------------------------------
  const help = desktop && helpOpen && <ShortcutsOverlay onClose={() => setHelpOpen(false)} />;
  const backLabel = state.screen === "item" ? `← Back to item ${positionText}` : state.screen === "runSummary" ? "← Back to the run summary" : state.screen === "runStart" ? "← Back to run start" : "← Back";
  const sheet = !desktop && queueOpen && (
    <QueueSheet queue={queue} positionText={positionText || "not started"} notice={queueNotice} onClose={() => setQueueOpen(false)} onOpen={openQueueRow} />
  );

  if (state.screen === "loading") {
    return (
      <Frame desktop={desktop}>
        {desktop ? (
          <DesktopHeader props={{ positionText: "", handledText: "", freshText, onHelp: () => setHelpOpen(true) }} />
        ) : (
          <MobileHeader positionText="Today's run" handledText="loading" freshShort={freshShort} />
        )}
        {state.health.consecutiveBad > 0 && (
          <div role="status" className="flex-none border-b border-mc-line-strong bg-mc-notice px-d16 py-d8 text-mc-13">
            Mission Control did not answer. Retrying automatically.
          </div>
        )}
        {desktop ? <LoadingDesktop /> : <LoadingMobile />}
        {help}
      </Frame>
    );
  }

  if (desktop && queueOpen) {
    return (
      <Frame desktop>
        <DesktopHeader
          props={{ positionText: positionText || "Not started", handledText, freshText, onPause: () => controller.pauseRun(), onQueue: () => setQueueOpen(false), onHelp: () => setHelpOpen(true) }}
          queueOpen
        />
        <QueueView queue={queue} backLabel={backLabel} notice={queueNotice} onBack={() => setQueueOpen(false)} onOpen={openQueueRow} />
        {help}
      </Frame>
    );
  }

  // ---- run screens -----------------------------------------------------------------------
  const shell = (content: ReactNode, bar: ReactNode) => (
    <Frame desktop={desktop}>
      <RunShell desktop={desktop} date={today} onHelp={() => setHelpOpen(true)} bar={bar}>{content}</RunShell>
      {help}
      {sheet}
    </Frame>
  );

  if (state.screen === "runStart") {
    const view = runStartView(state.tasks, now, timeZone);
    return shell(
      <RunStartContent view={view} />,
      <>
        <BarButton primary onClick={() => controller.startRun()}>Start run</BarButton>
        <BarButton onClick={() => setQueueOpen(true)}>See the queue</BarButton>
      </>,
    );
  }

  if (state.screen === "emptyRun") {
    return shell(
      <EmptyRunContent date={formatLongDay(now, timeZone)} backlog={state.tasks.length} note={state.emptyNote} />,
      <>
        <BarButton primary onClick={() => void controller.checkAgain()}>Check again</BarButton>
        <BarButton onClick={() => setQueueOpen(true)}>Review the backlog</BarButton>
      </>,
    );
  }

  if (state.screen === "runResume" && run) {
    const current = run.items[run.cursor];
    const currentTask = current ? byId.get(current.id) : undefined;
    const nextItem = run.items[run.cursor + 1];
    const left = run.pausedAt ?? run.lastSeenAt ?? run.startedAt;
    const leftView = current && currentTask ? buildItemView(currentTask, current, run, now, timeZone) : null;
    return shell(
      <ResumeContent
        position={positionText}
        meta={`${handledText} · You left ${formatShort(left, timeZone)} (${relativeAgo(left, now)})`}
        changes={state.changes}
        headline={changeHeadline(state.changes, run)}
        closing={changeClosingLine(state.changes, run)}
        left={leftView ? {
          title: leftView.titleText,
          eyebrow: leftView.eyebrow,
          next: nextItem ? { position: `${run.cursor + 2} of ${run.size}`, title: byId.get(nextItem.id)?.title ?? "Title missing" } : null,
        } : null}
      />,
      <>
        <BarButton primary onClick={() => void controller.acknowledgeAndResume()}>
          {state.changes.length > 0 ? `Acknowledge and resume at ${positionText}` : `Resume at ${positionText}`}
        </BarButton>
        <BarButton onClick={() => void reviewQueue()}>Review the queue first</BarButton>
      </>,
    );
  }

  if (state.screen === "rolloverSummary" && state.rollover) {
    const view = summaryView(state.rollover, state.tasks, now, timeZone);
    const label = `Run summary · ${formatLongDay(state.rollover.startedAt, timeZone)}${state.rollover.unfinished ? " · Unfinished" : ""}`;
    return shell(
      <SummaryContent view={view} label={label} reopen={null} />,
      <BarButton primary onClick={() => controller.dismissRollover()}>Continue to today</BarButton>,
    );
  }

  if (state.screen === "runSummary" && run) {
    const view = summaryView(run, state.tasks, now, timeZone);
    const reopened = run.phase === "queueChanged" && state.changes.length > 0;
    const reopen = reopened ? (
      <ChangeBanner changes={state.changes} headline="New work arrived after the run finished." closing="Acknowledge to add it to today's run." label="New since the run finished" />
    ) : null;
    const bar = reopened ? (
      <>
        <BarButton primary onClick={() => void controller.acknowledgeAndResume()}>Acknowledge and continue</BarButton>
        <BarButton onClick={() => setQueueOpen(true)}>See the queue</BarButton>
      </>
    ) : run.closedAt !== undefined ? (
      <div role="status" aria-live="polite" className="flex min-h-[48px] flex-1 items-center font-semibold">
        Run closed for today. The next run starts when you open Mission Control tomorrow.
      </div>
    ) : (
      <>
        <BarButton primary onClick={() => controller.closeRun()}>Close the run</BarButton>
        <BarButton onClick={() => setQueueOpen(true)}>See the queue</BarButton>
      </>
    );
    return shell(<SummaryContent view={view} label="Run summary" reopen={reopen} />, bar);
  }

  // ---- the item screen -------------------------------------------------------------------
  if (!run || !item) {
    return shell(<EmptyRunContent date={formatLongDay(now, timeZone)} backlog={state.tasks.length} note={null} />, null);
  }

  const view = buildItemView(task, item, run, now, timeZone);
  const change = controller.openItemChange();
  const buttons = (permitted.filter((action) => action !== "previous" && action !== "next") as ButtonAction[])
    .filter((action) => action !== "defer" || canDefer);
  const paused = !task || resolved ? null
    : connection === "stale" ? "Actions are paused until this item refreshes."
      : change ? "Actions are paused until you confirm you have read the new version."
        : !view.validity.ok ? "This card cannot be acted on. You can move to another item."
          : null;
  const failure = state.failure && state.failure.itemId === item.id ? {
    title: `Could not ${state.failure.phrase}.`,
    body: state.failure.failedStep > 0 ? PARTIAL_BODY : state.failure.kind === "refused" ? REFUSED_BODY : NETWORK_BODY,
  } : null;
  const readOnlyText = view.family === "outreachReview"
    ? "Approve and Reject for outreach reviews happen in the current interface for now."
    : view.expired
      ? "Rejecting an expired lane packet happens in the current interface for now."
      : "Approve, Reject and proof entry for lane packets happen in the current interface for now.";
  const actions: ActionModel = {
    buttons,
    paused,
    readOnly: view.readOnly && !resolved && view.validity.ok ? { text: readOnlyText, title: view.titleText } : null,
    resolved,
    line: item.line ?? null,
    canUndo: controller.canUndo() && !panel,
    failure,
    busy: state.busy,
  };

  const rail: RailRow[] = run.items.map((entry, i) => {
    const record: RawTask | undefined = byId.get(entry.id);
    const fallback = run.snapshot.find((snap) => snap.id === entry.id)?.fields ?? {};
    const shape: RawTask = record ?? { _id: entry.id, ...fallback };
    const title = typeof shape.title === "string" && shape.title.trim() ? shape.title : "Title missing";
    const status = entry.outcome ? "Handled"
      : i === run.cursor ? liveStatus(shape, now, entry)
        : i > run.cursor ? (entry.exception ? "Moved up" : "Up next")
          : liveStatus(shape, now, entry);
    return { id: entry.id, position: i + 1, title, status, group: groupOf(shape), current: i === run.cursor, handled: Boolean(entry.outcome), exception: entry.exception?.text ?? null };
  });

  const panelNode = panel && task ? (
    panel === "complete" ? (
      <CompletePanel mobile={!desktop} busy={state.busy} body="No proof is recorded for this type of item. It leaves today's run." onConfirm={() => void confirmPanel()} onCancel={() => closePanel()} />
    ) : panel === "defer" ? (
      <DeferPanel
        mobile={!desktop}
        busy={state.busy}
        options={deferOptions(task, now, timeZone)}
        choice={deferChoice}
        date={deferDate}
        minDate={localDateKey(now + 86_400_000, timeZone)}
        error={deferError}
        onChoose={(id) => { setDeferChoice(id); setDeferError(null); }}
        onDate={(value) => { setDeferDate(value); setDeferError(null); }}
        onConfirm={() => void confirmPanel()}
        onCancel={() => closePanel()}
      />
    ) : panel === "approve" || panel === "reject" ? (
      <DecisionPanel mobile={!desktop} busy={state.busy} kind={panel} note={note} error={noteError} onNote={(value) => { setNote(value); setNoteError(null); }} onConfirm={() => void confirmPanel()} onCancel={() => closePanel()} />
    ) : (
      <BlockForm mobile={!desktop} busy={state.busy} draft={park} errors={parkErrors} onChange={(draft) => { setPark(draft); setParkErrors({}); }} onSubmit={() => void confirmPanel()} onCancel={() => closePanel()} />
    )
  ) : null;

  const answerBox = view.answerSlot && task ? (
    <AnswerBox
      value={answers[item.id] ?? ""}
      onChange={(value) => { setAnswers((all) => ({ ...all, [item.id]: value })); setAnswerError(null); }}
      error={answerError}
      saved={savedAnswer(task.feedback)}
      mobile={!desktop}
      textareaRef={answerRef}
    />
  ) : null;

  const props: ItemScreenProps = {
    view,
    change,
    timeZone,
    positionText,
    handledText,
    freshText,
    freshShort,
    banner,
    rail,
    actions,
    panel: panelNode,
    answerBox,
    evidenceEmphasis: evidenceMessage !== null,
    evidenceMessage,
    notice: state.notice,
    onPause: () => { setPanel(null); controller.pauseRun(); },
    onQueue: () => setQueueOpen((open) => !open),
    onHelp: () => setHelpOpen(true),
    onPrevious: () => { setPanel(null); controller.previous(); },
    onNext: () => { setPanel(null); void controller.next(); },
    onAckChange: () => controller.ackItemChange(),
    onRecheck: () => void controller.refresh(),
    onAction,
    onUndo: () => void controller.undo(),
    onRetry: () => void controller.retry(),
    onDismiss: () => controller.dismissFailure(),
    onGoTo: (id) => controller.goTo(id),
  };

  return (
    <Frame desktop={desktop}>
      {desktop ? <DesktopItem {...props} /> : <MobileItem {...props} />}
      {help}
      {sheet}
    </Frame>
  );
}
