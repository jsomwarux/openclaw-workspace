// The cockpit's only backend: the existing /api/tasks routes. Lane-packet and outreach
// decision routes are slice two and are not called from here.
import type { RawTask } from "./types";

export type ApiErrorKind = "network" | "refused" | "server";

export class ApiError extends Error {
  constructor(readonly kind: ApiErrorKind, readonly status?: number) {
    super(`${kind}${status ? ` ${status}` : ""}`);
  }
}

export interface CockpitApi {
  listTasks(): Promise<RawTask[]>;
  patchTask(id: string, fields: Record<string, unknown>): Promise<void>;
  appendFeedback(id: string, body: string): Promise<void>;
}

async function send(fetchImpl: typeof fetch, url: string, init?: RequestInit): Promise<unknown> {
  let response: Response;
  try {
    response = await fetchImpl(url, { cache: "no-store", ...init });
  } catch {
    throw new ApiError("network");
  }
  if (response.status >= 400 && response.status < 500) throw new ApiError("refused", response.status);
  if (!response.ok) throw new ApiError("server", response.status);
  try {
    return await response.json();
  } catch {
    throw new ApiError("server", response.status);
  }
}

const json = (body: unknown): RequestInit => ({ method: "PATCH", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });

export function httpApi(fetchImpl: typeof fetch = (...args) => fetch(...args)): CockpitApi {
  return {
    async listTasks() {
      const body = (await send(fetchImpl, "/api/tasks")) as { tasks?: RawTask[]; items?: RawTask[] } | RawTask[];
      const tasks = Array.isArray(body) ? body : body.tasks ?? body.items;
      if (!Array.isArray(tasks)) throw new ApiError("server");
      return tasks;
    },
    async patchTask(id, fields) {
      await send(fetchImpl, "/api/tasks", json({ id, ...fields }));
    },
    async appendFeedback(id, body) {
      await send(fetchImpl, "/api/tasks", json({ action: "append-feedback", id, body, author: "jt" }));
    },
  };
}
