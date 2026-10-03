import { describe, expect, test } from "bun:test";
import { ApiError, httpApi } from "./api";
import { executePlan, failurePhrase, planFor } from "./writes";
import { connectionState, recordRead, retryDelay, STALE_MS } from "./freshness";
import { memoryStorage, runStorage } from "./storage";
import { FixtureApi } from "./fixtures/fixture-api";
import { startRun } from "./run";
import { FIXTURE_NOW, ID, allFixtureTasks, fx } from "./fixtures/data";

const NOW = FIXTURE_NOW;

type Call = { url: string; method: string; body: unknown };
function fakeFetch(responses: { status: number; json?: unknown }[] | Error) {
  const calls: Call[] = [];
  const fetchImpl = async (url: string, init?: RequestInit) => {
    calls.push({ url, method: init?.method ?? "GET", body: init?.body ? JSON.parse(String(init.body)) : undefined });
    if (responses instanceof Error) throw responses;
    const next = responses.shift() ?? { status: 200, json: {} };
    return new Response(JSON.stringify(next.json ?? {}), { status: next.status, headers: { "content-type": "application/json" } });
  };
  return { calls, fetchImpl: fetchImpl as unknown as typeof fetch };
}

describe("HTTP client: the existing /api/tasks surface, nothing new", () => {
  test("reads GET /api/tasks and accepts a bare array or an object", async () => {
    const one = fakeFetch([{ status: 200, json: { tasks: [{ _id: "a" }] } }, { status: 200, json: [{ _id: "b" }] }]);
    const api = httpApi(one.fetchImpl);
    expect((await api.listTasks()).map((task) => task._id)).toEqual(["a"]);
    expect((await api.listTasks()).map((task) => task._id)).toEqual(["b"]);
    expect(one.calls.map((call) => `${call.method} ${call.url}`)).toEqual(["GET /api/tasks", "GET /api/tasks"]);
  });

  test("writes fields with PATCH /api/tasks and feedback with append-feedback as jt", async () => {
    const { calls, fetchImpl } = fakeFetch([{ status: 200, json: { success: true } }, { status: 200, json: { success: true } }]);
    const api = httpApi(fetchImpl);
    await api.patchTask("t1", { status: "done" });
    await api.appendFeedback("t1", "Answer: yes");
    expect(calls).toEqual([
      { url: "/api/tasks", method: "PATCH", body: { id: "t1", status: "done" } },
      { url: "/api/tasks", method: "PATCH", body: { action: "append-feedback", id: "t1", body: "Answer: yes", author: "jt" } },
    ]);
  });

  test("a refused write, a server error and a dropped connection are told apart", async () => {
    const refused = httpApi(fakeFetch([{ status: 400, json: { error: "bad" } }]).fetchImpl);
    const server = httpApi(fakeFetch([{ status: 500 }]).fetchImpl);
    const dropped = httpApi(fakeFetch(new TypeError("fetch failed")).fetchImpl);
    for (const [api, kind] of [[refused, "refused"], [server, "server"], [dropped, "network"]] as const) {
      try {
        await api.patchTask("t1", { status: "done" });
        expect("no error").toBe(kind);
      } catch (error) {
        expect(error instanceof ApiError && error.kind).toBe(kind);
      }
    }
  });
});

describe("write plans (DECISIONS 5, 6, override 1)", () => {
  test("each action becomes ordered steps; P decisions append the note first, then mark done", () => {
    expect(planFor({ action: "start" }, fx("F04"), NOW).steps).toEqual([{ kind: "patch", fields: { status: "in-progress" } }]);
    expect(planFor({ action: "complete" }, fx("F04"), NOW).steps).toEqual([{ kind: "patch", fields: { status: "done" } }]);
    expect(planFor({ action: "saveAnswer", text: " yes " }, fx("F01"), NOW).steps).toEqual([{ kind: "feedback", body: "Answer: yes" }]);
    expect(planFor({ action: "approve", note: "ship it" }, fx("F02"), NOW).steps).toEqual([
      { kind: "feedback", body: "Decision: Approved. ship it" },
      { kind: "patch", fields: { status: "done" } },
    ]);
    expect(planFor({ action: "reject", note: "" }, fx("F02"), NOW).steps[0]).toEqual({ kind: "feedback", body: "Decision: Rejected." });
    expect(planFor({ action: "defer", until: NOW + 1 }, fx("F04"), NOW).steps).toEqual([
      { kind: "patch", fields: { snoozedUntil: NOW + 1, auditSource: "jt", auditEvidence: "Deferred from Mission Control run" } },
    ]);
  });

  test("undo records what to restore: the previous status, or the previous snooze", () => {
    expect(planFor({ action: "start" }, fx("F07"), NOW).undo).toEqual({ kind: "start", restore: { status: "waiting-external" } });
    expect(planFor({ action: "complete" }, fx("F04"), NOW).undo).toEqual({ kind: "complete", restore: { status: "todo" } });
    expect(planFor({ action: "defer", until: NOW + 1 }, fx("F12"), NOW).undo).toEqual({ kind: "defer", restore: { snoozedUntil: fx("F12").snoozedUntil } });
    expect(planFor({ action: "defer", until: NOW + 1 }, fx("F04"), NOW).undo).toEqual({ kind: "defer", restore: { snoozedUntil: null } });
    expect(planFor({ action: "block", park: { who: "Pat", what: "x", nudgeAfterDays: 3 } }, fx("F04"), NOW).undo).toBe(undefined);
    expect(planFor({ action: "approve", note: "" }, fx("F02"), NOW).undo).toBe(undefined);
    expect(planFor({ action: "saveAnswer", text: "x" }, fx("F01"), NOW).undo).toBe(undefined);
  });

  test("failure phrases are plain", () => {
    expect(failurePhrase("complete")).toBe("mark this item done");
    expect(failurePhrase("saveAnswer")).toBe("save your answer");
    expect(failurePhrase("undo")).toBe("undo that change");
  });

  test("a failed second step retries from that step only; the note is never appended twice", async () => {
    const api = new FixtureApi(allFixtureTasks(), () => NOW);
    const plan = planFor({ action: "approve", note: "ok" }, fx("F02"), NOW);
    api.failNext("network", { after: 1 });
    const first = await executePlan(api, plan, { fromStep: 0, firstAttemptAt: NOW, retry: false });
    expect(first).toMatchObject({ ok: false, failedStep: 1 });
    expect(api.task(ID.F02).feedback).toHaveLength(1);
    expect(api.task(ID.F02).status).toBe("todo");
    const retry = await executePlan(api, plan, { fromStep: 1, firstAttemptAt: NOW, retry: true });
    expect(retry).toEqual({ ok: true });
    expect(api.task(ID.F02).feedback).toHaveLength(1);
    expect(api.task(ID.F02).status).toBe("done");
  });

  test("a feedback write that landed but reported failure is not repeated on retry", async () => {
    const api = new FixtureApi(allFixtureTasks(), () => NOW);
    const plan = planFor({ action: "saveAnswer", text: "keep option two" }, fx("F01"), NOW);
    api.failNext("network", { applied: true });
    const first = await executePlan(api, plan, { fromStep: 0, firstAttemptAt: NOW, retry: false });
    expect(first).toMatchObject({ ok: false, failedStep: 0 });
    expect(api.task(ID.F01).feedback).toHaveLength(1);
    expect(await executePlan(api, plan, { fromStep: 0, firstAttemptAt: NOW, retry: true })).toEqual({ ok: true });
    expect(api.task(ID.F01).feedback).toHaveLength(1);
  });

  test("a first attempt never skips a feedback write, even when the same words were saved before", async () => {
    const api = new FixtureApi(allFixtureTasks(), () => NOW);
    const plan = planFor({ action: "saveAnswer", text: "same words" }, fx("F01"), NOW);
    await executePlan(api, plan, { fromStep: 0, firstAttemptAt: NOW, retry: false });
    await executePlan(api, plan, { fromStep: 0, firstAttemptAt: NOW, retry: false });
    expect(api.task(ID.F01).feedback).toHaveLength(2);
  });

  test("the fixture backend refuses generic writes on outreach reviews, as the real one does", async () => {
    const api = new FixtureApi(allFixtureTasks(), () => NOW);
    const result = await executePlan(api, planFor({ action: "complete" }, fx("F11"), NOW), { fromStep: 0, firstAttemptAt: NOW, retry: false });
    expect(result).toMatchObject({ ok: false, error: { kind: "refused" } });
  });
});

describe("read freshness (DECISIONS 15)", () => {
  test("stale after five minutes without a good read; degraded after two bad reads in a row", () => {
    let health = recordRead({ lastGoodAt: null, consecutiveBad: 0, lastAttemptAt: null }, { ok: true, startedAt: NOW, finishedAt: NOW + 200 });
    expect(connectionState(health, NOW + 1000)).toBe("fresh");
    expect(connectionState(health, NOW + 200 + STALE_MS)).toBe("fresh");
    expect(connectionState(health, NOW + 201 + STALE_MS)).toBe("stale");
    health = recordRead(health, { ok: false, startedAt: NOW + 60_000, finishedAt: NOW + 61_000 });
    expect(connectionState(health, NOW + 61_000)).toBe("fresh");
    health = recordRead(health, { ok: true, startedAt: NOW + 120_000, finishedAt: NOW + 131_000 });
    expect(health.lastGoodAt).toBe(NOW + 131_000);
    expect(connectionState(health, NOW + 131_000)).toBe("degraded");
    health = recordRead(health, { ok: true, startedAt: NOW + 140_000, finishedAt: NOW + 140_500 });
    expect(connectionState(health, NOW + 140_500)).toBe("fresh");
    expect(connectionState({ lastGoodAt: null, consecutiveBad: 0, lastAttemptAt: null }, NOW)).toBe("checking");
  });

  test("automatic retry every 8 seconds with backoff", () => {
    expect([2, 3, 4, 5, 9].map(retryDelay)).toEqual([8_000, 16_000, 32_000, 60_000, 60_000]);
  });
});

describe("run storage: browser storage keyed by local date (DECISIONS 8, override 2)", () => {
  test("saves and loads by date, never clears other keys, and finds the latest earlier run", () => {
    const backing = memoryStorage({ "someone-else": "keep" });
    const runs = runStorage(backing, "mc-test");
    const run = startRun(allFixtureTasks(), NOW, "UTC");
    runs.save(run);
    runs.save({ ...run, localDate: "2026-10-01" });
    expect(runs.load("2026-10-03")?.items).toHaveLength(7);
    expect(runs.load("2026-10-02")).toBe(null);
    expect(runs.latestBefore("2026-10-04")?.localDate).toBe("2026-10-03");
    expect(runs.latestBefore("2026-10-03")?.localDate).toBe("2026-10-01");
    expect(backing.getItem("someone-else")).toBe("keep");
  });

  test("unreadable entries and a storage that throws read as no run, without crashing", () => {
    const backing = memoryStorage({ "mc-test:2026-10-03": "{not json" });
    expect(runStorage(backing, "mc-test").load("2026-10-03")).toBe(null);
    const broken = { getItem() { throw new Error("blocked"); }, setItem() { throw new Error("blocked"); }, key() { throw new Error("blocked"); }, get length(): number { throw new Error("blocked"); } };
    const runs = runStorage(broken, "mc-test");
    expect(runs.load("2026-10-03")).toBe(null);
    expect(runs.latestBefore("2026-10-03")).toBe(null);
    expect(runs.save(startRun(allFixtureTasks(), NOW, "UTC"))).toBe(false);
  });
});
