// The cockpit's state owner: reads, freshness, the stored run, writes, failures and Undo.
// Framework-free so it can be driven end to end in tests; React subscribes to it.
import { sliceOneActions, actionContext, isReadOnlyInSliceOne } from "./actions";
import type { CockpitApi } from "./api";
import { savedAnswer } from "./answer";
import { familyOf, seriesOf } from "./classify";
import { trackedFields } from "./changes";
import { isExpired } from "./eligibility";
import { planRun } from "./exceptions";
import { connectionState, initialHealth, recordRead } from "./freshness";
import type { ConnectionState, ReadHealth } from "./freshness";
import { formatWeekdayTime, localDateKey } from "./format";
import { statusWord } from "./labels";
import {
  acknowledge, backgroundCheck, clearOutcome, detectChanges, foldWrite, itemChangedKeys, moveNext, movePrevious, moveTo,
  pause, recordOutcome, resume, rollover, snapshotEntry, startRun,
} from "./run";
import type { RunStorage } from "./storage";
import { validateCard } from "./validity";
import { executePlan, failurePhrase, planFor, undoPlan } from "./writes";
import type { ActRequest, WritePlan } from "./writes";
import type { LeftReason, RawTask, RunChange, RunItem, StoredRun } from "./types";
import { nudgeDueAt } from "./block";

const SAVE_FAILED = "Progress could not be saved in this browser. The run works until you close this page.";

export type Screen = "loading" | "runStart" | "emptyRun" | "runResume" | "item" | "runSummary" | "rolloverSummary";

export interface Failure {
  itemId: string;
  plan: WritePlan;
  request: ActRequest | null;
  failedStep: number;
  firstAttemptAt: number;
  phrase: string;
  kind: "network" | "refused" | "server";
}

export interface CockpitState {
  screen: Screen;
  tasks: RawTask[];
  health: ReadHealth;
  run: StoredRun | null;
  rollover: StoredRun | null;
  changes: RunChange[];
  busy: boolean;
  failure: Failure | null;
  notice: string | null;
  emptyNote: string | null;
  now: number;
}

export interface ControllerDeps {
  api: CockpitApi;
  clock: () => number;
  storage: RunStorage;
  timeZone: string;
}

export interface OpenItemChange {
  task: RawTask;
  keys: string[];
  before: Record<string, unknown>;
}

export class CockpitController {
  private state: CockpitState;
  private listeners = new Set<() => void>();

  constructor(private readonly deps: ControllerDeps) {
    this.state = {
      screen: "loading", tasks: [], health: initialHealth, run: null, rollover: null, changes: [],
      busy: false, failure: null, notice: null, emptyNote: null, now: deps.clock(),
    };
  }

  getState = (): CockpitState => this.state;

  subscribe = (listener: () => void): (() => void) => {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  };

  private set(patch: Partial<CockpitState>) {
    this.state = { ...this.state, ...patch, now: this.deps.clock() };
    for (const listener of this.listeners) listener();
  }

  /** False when this browser refused to store the run (quota, blocked storage). */
  private persist(run: StoredRun | null): boolean {
    return run ? this.deps.storage.save({ ...run, lastSeenAt: this.deps.clock() }) : true;
  }

  private setRun(run: StoredRun | null, patch: Partial<CockpitState> = {}) {
    const saved = this.persist(run);
    this.set({ ...patch, run, ...(saved ? {} : { notice: SAVE_FAILED }) });
  }

  private today() {
    return localDateKey(this.deps.clock(), this.deps.timeZone);
  }

  // ---- reads ----------------------------------------------------------------------------

  private async read(): Promise<boolean> {
    const startedAt = this.deps.clock();
    try {
      const tasks = await this.withDecidedElsewhere(await this.deps.api.listTasks());
      this.set({ tasks, health: recordRead(this.state.health, { ok: true, startedAt, finishedAt: this.deps.clock() }) });
      return true;
    } catch {
      this.set({ health: recordRead(this.state.health, { ok: false, startedAt, finishedAt: this.deps.clock() }) });
      return false;
    }
  }

  /**
   * GET /api/tasks leaves archived rows out, and deciding a lane packet in the Work list archives
   * it. When an unhandled run item is missing, read the archived rows once to learn what happened
   * instead of reporting it as gone (review finding 4).
   */
  private async withDecidedElsewhere(tasks: RawTask[]): Promise<RawTask[]> {
    const run = this.state.run;
    if (!run) return tasks;
    const present = new Set(tasks.map((task) => task._id));
    const missing = new Set(run.items.filter((item) => !item.outcome && !item.left && !present.has(item.id)).map((item) => item.id));
    if (missing.size === 0) return tasks;
    try {
      return [...tasks, ...(await this.deps.api.listArchived()).filter((task) => missing.has(task._id))];
    } catch {
      return tasks;
    }
  }

  connection(): ConnectionState {
    return connectionState(this.state.health, this.deps.clock());
  }

  async load(): Promise<void> {
    await this.read();
    if (this.state.health.lastGoodAt === null) return;
    const today = this.today();
    const { previous } = rollover(this.deps.storage.latestBefore(today), today, this.deps.clock());
    if (previous) this.deps.storage.save(previous);
    this.set({ rollover: previous });
    this.enterToday();
  }

  /** The entry screen for today's date: start, empty, resume or summary. */
  private enterToday() {
    if (this.state.rollover) return this.set({ screen: "rolloverSummary" });
    const run = this.deps.storage.load(this.today());
    if (!run) return this.set({ run: null, screen: this.previewIds().length > 0 ? "runStart" : "emptyRun" });
    if (run.phase === "complete") return this.set({ run, screen: "runSummary", changes: [] });
    const left = { ...run, phase: "paused" as const, pausedAt: run.pausedAt ?? run.lastSeenAt ?? run.startedAt };
    const back = resume(left, this.state.tasks, this.deps.clock(), this.deps.timeZone);
    this.setRun({ ...back.run, phase: back.changes.length > 0 ? "queueChanged" : "paused" }, { screen: "runResume", changes: back.changes });
  }

  previewIds(): string[] {
    return planRun(this.state.tasks, this.deps.clock(), this.deps.timeZone).ids;
  }

  async refresh(): Promise<void> {
    // A poll that lands during the operator's own write would see that write before it is folded
    // into the snapshot and report it as someone else's change (review finding 7). Skip it.
    if (this.state.busy) return;
    const ok = await this.read();
    if (!ok) return;
    const { screen, run } = this.state;
    if (screen === "loading") return this.load();
    if (run && run.localDate !== this.today() && run.closedAt === undefined) {
      const { previous } = rollover(run, this.today(), this.deps.clock());
      if (previous) this.deps.storage.save(previous);
      this.set({ rollover: previous, run: null });
      return this.enterToday();
    }
    if (screen === "runStart" || screen === "emptyRun") {
      return this.set({ screen: this.previewIds().length > 0 ? "runStart" : "emptyRun" });
    }
    if (!run) return;
    if (screen === "runResume") {
      return this.set({ changes: detectChanges(run, this.state.tasks, this.deps.clock(), this.deps.timeZone) });
    }
    const checked = backgroundCheck(run, this.state.tasks, this.deps.clock(), this.deps.timeZone);
    this.setRun(checked.run, { changes: checked.changes });
  }

  // ---- run flow -------------------------------------------------------------------------

  startRun() {
    const run = startRun(this.state.tasks, this.deps.clock(), this.deps.timeZone);
    this.setRun(run, { screen: run.items.length > 0 ? "item" : "emptyRun", changes: [] });
  }

  pauseRun() {
    if (!this.state.run) return;
    const run = pause(this.state.run, this.deps.clock());
    this.setRun(run, { screen: "runResume", changes: detectChanges(run, this.state.tasks, this.deps.clock(), this.deps.timeZone), failure: null });
  }

  async acknowledgeAndResume(): Promise<void> {
    if (!this.state.run) return;
    const run = acknowledge(this.state.run, this.state.tasks, this.deps.clock(), this.deps.timeZone);
    this.setRun(run, { screen: run.phase === "complete" ? "runSummary" : "item", changes: [] });
  }

  closeRun() {
    if (!this.state.run) return;
    this.setRun({ ...this.state.run, closedAt: this.deps.clock() });
  }

  dismissRollover() {
    this.set({ rollover: null });
    this.enterToday();
  }

  async checkAgain(): Promise<void> {
    await this.refresh();
    if (this.state.screen === "emptyRun") this.set({ emptyNote: "Checked just now. Nothing new yet." });
  }

  /** Item boundaries show any pending change summary before moving the operator. */
  private boundaryHold(): boolean {
    const run = this.state.run;
    if (run?.phase === "queueChanged" && this.state.screen === "item") {
      this.set({ screen: "runResume", changes: detectChanges(run, this.state.tasks, this.deps.clock(), this.deps.timeZone) });
      return true;
    }
    return false;
  }

  async next(): Promise<void> {
    const run = this.state.run;
    if (!run || this.boundaryHold()) return;
    const moved = moveNext(run, this.leaveReason());
    this.setRun(moved.run, { screen: moved.atEnd ? "runSummary" : "item", notice: moved.notice ?? null, failure: null });
  }

  previous() {
    const run = this.state.run;
    if (!run || this.boundaryHold()) return;
    const moved = movePrevious(run);
    this.setRun(moved.run, { notice: moved.notice ?? null, failure: null, screen: "item" });
  }

  goTo(id: string) {
    const run = this.state.run;
    if (!run || this.boundaryHold()) return;
    this.setRun(moveTo(run, id), { screen: "item", failure: null });
  }

  clearNotice() {
    if (this.state.notice) this.set({ notice: null });
  }

  /** Re-render relative times and expiry without a read. */
  tick() {
    this.set({});
  }

  /** Transition 3: the surface was hidden. */
  onHidden() {
    const run = this.state.run;
    if (run && this.state.screen === "item" && run.phase === "inProgress") this.setRun(pause(run, this.deps.clock()));
  }

  /** Transitions 4 and 5: back on the surface; compare a fresh read before going anywhere. */
  async onVisible(): Promise<void> {
    const run = this.state.run;
    if (!run || run.phase !== "paused" || this.state.screen !== "item") return this.refresh();
    if (!(await this.read())) return;
    const back = resume(this.state.run!, this.state.tasks, this.deps.clock(), this.deps.timeZone);
    this.setRun(back.run, back.changes.length > 0 ? { screen: "runResume", changes: back.changes } : {});
  }

  /** Why moving past the current item leaves it unhandled, or undefined when it is actionable. */
  private leaveReason(): LeftReason | undefined {
    const task = this.currentTask();
    if (!task) return "removed";
    if (!validateCard(task).ok) return "invalid";
    if (isExpired(task, this.deps.clock())) return "expired";
    if (isReadOnlyInSliceOne(familyOf(task))) return "readOnly";
    return undefined;
  }

  // ---- the current item -----------------------------------------------------------------

  currentItem(): RunItem | null {
    const run = this.state.run;
    return run ? run.items[run.cursor] ?? null : null;
  }

  currentTask(): RawTask | null {
    const item = this.currentItem();
    return item ? this.state.tasks.find((task) => task._id === item.id) ?? null : null;
  }

  /** Another writer changed the open item since its snapshot (DECISIONS 11.4). */
  openItemChange(): OpenItemChange | null {
    const run = this.state.run;
    const item = this.currentItem();
    const task = this.currentTask();
    if (!run || !item || !task || item.outcome || item.left) return null;
    const keys = itemChangedKeys(run, task);
    if (keys.length === 0) return null;
    const before = run.snapshot.find((entry) => entry.id === task._id)!.fields;
    return { task, keys, before };
  }

  ackItemChange() {
    const run = this.state.run;
    const task = this.currentTask();
    if (!run || !task) return;
    let next: StoredRun = { ...run, snapshot: run.snapshot.map((entry) => (entry.id === task._id ? snapshotEntry(task) : entry)) };
    if (next.phase === "queueChanged" && detectChanges(next, this.state.tasks, this.deps.clock(), this.deps.timeZone).length === 0) {
      next = { ...next, phase: "inProgress" };
    }
    this.setRun(next);
  }

  /** Writes pause while loading, stale, invalid, changed-and-unread, after a failure, or mid-write. */
  paused(): boolean {
    const task = this.currentTask();
    const connection = this.connection();
    return (
      this.state.busy || this.state.failure !== null || !task || connection === "stale" || connection === "checking" ||
      !validateCard(task).ok || this.openItemChange() !== null
    );
  }

  permitted() {
    const task = this.currentTask();
    const item = this.currentItem();
    if (!task || !item) return ["previous", "next"];
    if (item.outcome) return ["previous", "next"];
    return sliceOneActions(actionContext(task, this.deps.clock(), { paused: this.paused() }));
  }

  // ---- writes ---------------------------------------------------------------------------

  async act(request: ActRequest): Promise<void> {
    const task = this.currentTask();
    if (!task || !(this.permitted() as string[]).includes(request.action)) return;
    const firstAttemptAt = this.deps.clock();
    await this.run(planFor(request, task, firstAttemptAt), request, 0, firstAttemptAt, false);
  }

  async retry(): Promise<void> {
    const failure = this.state.failure;
    if (!failure || this.state.busy) return;
    this.set({ failure: null });
    await this.run(failure.plan, failure.request, failure.failedStep, failure.firstAttemptAt, true);
  }

  dismissFailure() {
    this.set({ failure: null });
  }

  /**
   * Undo is a write: it pauses with every other write (stale, checking, failure, mid-write) and is
   * bound to the state the operator's own write left. Once another writer has changed the item,
   * Undo is no longer offered, so it can never overwrite their change (review finding 2).
   */
  canUndo(): boolean {
    const item = this.currentItem();
    const task = this.currentTask();
    const run = this.state.run;
    if (!item?.undo || !task || !run || this.state.busy || this.state.failure) return false;
    const connection = this.connection();
    if (connection === "stale" || connection === "checking") return false;
    return itemChangedKeys(run, task).length === 0;
  }

  async undo(): Promise<void> {
    const item = this.currentItem();
    if (!item?.undo || !this.canUndo()) return;
    const now = this.deps.clock();
    await this.run(undoPlan(item.id, item.undo, now), null, 0, now, false);
  }

  private async run(plan: WritePlan, request: ActRequest | null, fromStep: number, firstAttemptAt: number, retry: boolean) {
    this.set({ busy: true, notice: null });
    const result = await executePlan(this.deps.api, plan, { fromStep, firstAttemptAt, retry });
    if (!result.ok) {
      this.set({
        busy: false,
        failure: { itemId: plan.itemId, plan, request, failedStep: result.failedStep, firstAttemptAt, phrase: failurePhrase(plan.action), kind: result.error.kind },
      });
      // A refusal usually means the record moved on; read again now so Changed shows at once.
      if (result.error.kind === "refused") await this.refresh();
      return;
    }
    this.applySuccess(plan, request);
  }

  /** Reflect a confirmed write locally, fold it into the snapshot, and record the outcome. */
  private applySuccess(plan: WritePlan, request: ActRequest | null) {
    const now = this.deps.clock();
    const before = this.state.tasks.find((task) => task._id === plan.itemId)!;
    let after: RawTask = before;
    let run = this.state.run!;
    for (const step of plan.steps) {
      if (step.kind === "feedback") {
        const feedback = [...(after.feedback ?? []), { id: `local-${now}`, body: step.body, author: "jt" as const, createdAt: now }];
        after = { ...after, feedback };
      } else {
        const { auditSource: _source, auditEvidence: _evidence, ...fields } = step.fields;
        after = { ...after, ...fields };
        run = foldWrite(run, plan.itemId, trackedFields(fields));
      }
    }
    const tasks = this.state.tasks.map((task) => (task._id === plan.itemId ? after : task));
    run = request ? recordOutcome(run, plan.itemId, this.outcomeFor(request, before, plan), now) : clearOutcome(run, plan.itemId, this.undoLine(before, after));
    this.setRun(run, { tasks, busy: false, failure: null });
  }

  private outcomeFor(request: ActRequest, task: RawTask, plan: WritePlan): Partial<RunItem> {
    const tz = this.deps.timeZone;
    switch (request.action) {
      case "start":
        return { line: "Started. Status is now In progress.", undo: plan.undo };
      case "saveAnswer":
        return { line: "Answer saved. It is in the feedback history. You can complete the item now." };
      case "complete": {
        const answered = seriesOf(task) !== null && seriesOf(task) !== "P" && savedAnswer(task.feedback) !== null;
        return { outcome: "completed", did: answered ? "Answer recorded, then completed." : "Completed.", line: "Marked done. Press J for the next item.", undo: plan.undo };
      }
      case "approve":
      case "reject": {
        const word = request.action === "approve" ? "Approved" : "Rejected";
        const noted = request.note.trim().length > 0;
        return {
          outcome: request.action === "approve" ? "approved" : "rejected",
          did: noted ? `${word}. Note recorded.` : `${word}.`,
          line: request.action === "approve"
            ? `Approved.${noted ? " Your note is in the feedback history." : ""} Press J for the next item.`
            : "Rejected. This cannot be undone. Press J for the next item.",
          undo: undefined,
        };
      }
      case "defer":
        return {
          outcome: "deferred",
          deferredUntil: request.until,
          did: `Deferred until ${formatWeekdayTime(request.until, tz)}.`,
          line: `Deferred until ${formatWeekdayTime(request.until, tz)}. It leaves today's run.`,
          undo: plan.undo,
        };
      case "block": {
        const waitingOn = { who: request.park.who, what: request.park.what, since: this.deps.clock(), nudgeAfterDays: request.park.nudgeAfterDays };
        return {
          outcome: "parked",
          parked: { who: request.park.who, nudgeDueAt: nudgeDueAt(waitingOn), days: request.park.nudgeAfterDays },
          did: `Parked on ${request.park.who}. Nudge after ${request.park.nudgeAfterDays} days.`,
          line: `Parked on ${request.park.who}. It returns to today's run if no reply by day ${request.park.nudgeAfterDays}.`,
          undo: undefined,
        };
      }
    }
  }

  private undoLine(before: RawTask, after: RawTask): string {
    if (before.snoozedUntil !== after.snoozedUntil) return "Undone. The item is back in today's run.";
    const answerKept = seriesOf(after) !== null && savedAnswer(after.feedback) !== null ? " Your saved answer stays in the feedback history." : "";
    return `Undone. Status is back to ${statusWord(after.status)}.${answerKept}`;
  }
}
