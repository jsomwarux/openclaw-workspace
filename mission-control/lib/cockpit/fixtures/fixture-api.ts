// An in-memory stand-in for /api/tasks, for tests and the development fixture harness. It
// mirrors the backend rules the cockpit depends on (data contract sections 4 to 6) so a test
// cannot pass by writing something the real backend would refuse. It never touches the network.
import { ApiError } from "../api";
import type { ApiErrorKind, CockpitApi } from "../api";
import { isLanePacket, isOutreachReview } from "../classify";
import { KNOWN_STATUSES } from "../validity";
import type { RawTask } from "../types";

type Failure = { kind: ApiErrorKind; after: number; applied: boolean };

export class FixtureApi implements CockpitApi {
  private tasks: RawTask[];
  private failures: Failure[] = [];
  private readFailures = 0;
  readonly writes: { id: string; kind: "patch" | "feedback"; payload: unknown }[] = [];
  readonly audit: { taskId: string; field: string; evidence: unknown; source: unknown }[] = [];
  readDelayMs = 0;
  /** True: a delayed read returns the records as they were when it was sent, not when it is answered. */
  readSnapshotFirst = false;
  writeDelayMs = 0;
  reads = 0;
  archivedReads = 0;

  constructor(tasks: RawTask[], private readonly clock: () => number) {
    this.tasks = structuredClone(tasks);
  }

  /** The next write fails. after: let that many writes succeed first. applied: the write lands anyway. */
  failNext(kind: ApiErrorKind, options: { after?: number; applied?: boolean } = {}) {
    this.failures.push({ kind, after: options.after ?? 0, applied: options.applied ?? false });
  }

  failReads(count: number) {
    this.readFailures = count;
  }

  task(id: string): RawTask {
    const found = this.tasks.find((task) => task._id === id);
    if (!found) throw new Error(`no task ${id}`);
    return structuredClone(found);
  }

  /** Another writer edits a card (bumps updatedAt, as the backend does). */
  edit(id: string, fields: Partial<RawTask>) {
    this.tasks = this.tasks.map((task) => (task._id === id ? { ...task, ...fields, updatedAt: this.clock() } : task));
  }

  add(task: RawTask) {
    this.tasks = [...this.tasks, structuredClone(task)];
  }

  remove(id: string) {
    this.tasks = this.tasks.filter((task) => task._id !== id);
  }

  async listTasks(): Promise<RawTask[]> {
    this.reads += 1;
    const served = structuredClone(this.tasks.filter((task) => task.status !== "archived"));
    if (this.readDelayMs > 0) await new Promise((resolve) => setTimeout(resolve, this.readDelayMs));
    if (this.readFailures > 0) {
      this.readFailures -= 1;
      throw new ApiError("network");
    }
    return this.readSnapshotFirst ? served : structuredClone(this.tasks.filter((task) => task.status !== "archived"));
  }

  /** Like GET /api/tasks?include=archived: archived rows only. */
  async listArchived(): Promise<RawTask[]> {
    this.archivedReads += 1;
    if (this.readFailures > 0) {
      this.readFailures -= 1;
      throw new ApiError("network");
    }
    return structuredClone(this.tasks.filter((task) => task.status === "archived"));
  }

  /** A slow response: the write has landed, the reply has not arrived yet. */
  private async delayWrite() {
    if (this.writeDelayMs > 0) await new Promise((resolve) => setTimeout(resolve, this.writeDelayMs));
  }

  private takeFailure(): Failure | null {
    const next = this.failures[0];
    if (!next) return null;
    if (next.after > 0) {
      next.after -= 1;
      return null;
    }
    this.failures.shift();
    return next;
  }

  async patchTask(id: string, fields: Record<string, unknown>): Promise<void> {
    const failure = this.takeFailure();
    if (failure && !failure.applied) throw new ApiError(failure.kind, failure.kind === "refused" ? 400 : undefined);
    const task = this.tasks.find((candidate) => candidate._id === id);
    if (!task) throw new ApiError("server", 500);
    const { auditSource, auditEvidence, ...changes } = fields;
    if ("feedback" in changes) throw new ApiError("refused", 400);
    if (isOutreachReview(task)) throw new ApiError("refused", 409);
    if (changes.status !== undefined && !KNOWN_STATUSES.includes(String(changes.status))) throw new ApiError("refused", 400);
    if (isLanePacket(task)) {
      if (task.status === "done" || task.status === "archived") throw new ApiError("refused", 409);
      if (changes.status === "done" && task.doneEvidenceType !== "none") throw new ApiError("refused", 409);
      if (changes.status === "archived") throw new ApiError("refused", 409);
      if (typeof changes.snoozedUntil === "number" && typeof task.expiresAt === "number" && changes.snoozedUntil > task.expiresAt) {
        throw new ApiError("refused", 409);
      }
    }
    for (const key of ["snoozedUntil", "waitingOn"]) {
      if (key in changes && changes[key] === null) throw new ApiError("server", 500);
    }
    for (const field of ["dollars", "dueDate", "waitingOn", "stageProbability", "priority"]) {
      if (field in changes) this.audit.push({ taskId: id, field, evidence: auditEvidence ?? "manual edit", source: auditSource ?? "jt" });
    }
    this.writes.push({ id, kind: "patch", payload: fields });
    this.tasks = this.tasks.map((candidate) => (candidate._id === id ? { ...candidate, ...changes, updatedAt: this.clock() } : candidate));
    await this.delayWrite();
    if (failure) throw new ApiError(failure.kind);
  }

  async appendFeedback(id: string, body: string): Promise<void> {
    const failure = this.takeFailure();
    if (failure && !failure.applied) throw new ApiError(failure.kind, failure.kind === "refused" ? 400 : undefined);
    const trimmed = body.trim();
    if (trimmed.length === 0 || trimmed.length > 4000) throw new ApiError("refused", 400);
    const task = this.tasks.find((candidate) => candidate._id === id);
    if (!task) throw new ApiError("server", 500);
    const now = this.clock();
    const feedback = [...(task.feedback ?? [])];
    feedback.push({ id: `${now}-${feedback.length + 1}`, body: trimmed, author: "jt", createdAt: now });
    this.writes.push({ id, kind: "feedback", payload: trimmed });
    this.tasks = this.tasks.map((candidate) => (candidate._id === id ? { ...candidate, feedback, updatedAt: now } : candidate));
    await this.delayWrite();
    if (failure) throw new ApiError(failure.kind);
  }
}
