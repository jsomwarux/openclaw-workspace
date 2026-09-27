import { describe, expect, test } from "bun:test";
import { ConvexHttpClient } from "convex/browser";
import { getFunctionName, type FunctionReference } from "convex/server";

// The route builds its Convex client at module load. Every mutation below is
// stubbed on the client prototype, so nothing reaches this address.
process.env.NEXT_PUBLIC_CONVEX_URL ??= "http://127.0.0.1:3210";

const TASK_ID = "synthetic-task-id-1";
const NO_REJECTION = Symbol("no rejection");

type MutationCall = { name: string; args: unknown };
type Outcome = { reject: Error } | { resolve: unknown };

/**
 * Replaces only ConvexHttpClient's network call while `run` executes; the real
 * route module runs unmodified. The original is restored even if `run` fails.
 */
async function withConvexMutation(outcome: Outcome, run: (calls: MutationCall[]) => Promise<void>): Promise<void> {
  const original = ConvexHttpClient.prototype.mutation;
  const calls: MutationCall[] = [];
  const stub = async (fn: FunctionReference<"mutation">, args?: Record<string, unknown>) => {
    calls.push({ name: getFunctionName(fn), args });
    if ("reject" in outcome) throw outcome.reject;
    return outcome.resolve;
  };
  ConvexHttpClient.prototype.mutation = stub as unknown as ConvexHttpClient["mutation"];
  try {
    await run(calls);
  } finally {
    ConvexHttpClient.prototype.mutation = original;
  }
}

/** The value a handler rejects with, or NO_REJECTION when it resolves. */
async function rejection(run: () => Promise<unknown>): Promise<unknown> {
  try {
    await run();
    return NO_REJECTION;
  } catch (error) {
    return error;
  }
}

/** What ConvexHttpClient throws for an uncaught mutation error: `new Error(errorMessage)`. */
function convexUncaught(code: string): Error {
  return new Error(
    `[Request ID: 0f3c9a2b7d1e4c58] Server Error\nUncaught Error: ${code}\n` +
      "    at rethrowGenericLanePacketError (../convex/tasks.ts:188:9)\n" +
      "    at async handler (../convex/tasks.ts:906:21)\n",
  );
}

async function loadRoute() {
  return import("../../app/api/tasks/[id]/route");
}

function params(id = TASK_ID) {
  return { params: Promise.resolve({ id }) };
}

function patchRequest(body: Record<string, unknown> | string) {
  return new Request(`http://localhost/api/tasks/${TASK_ID}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

function deleteRequest() {
  return new Request(`http://localhost/api/tasks/${TASK_ID}`, { method: "DELETE" });
}

/** The exact bytes of an enumerated error body: no request ID, stack, or other dependency text. */
async function expectEnumeratedError(response: Response, status: number, error: string) {
  expect(response.status).toBe(status);
  expect(await response.text()).toBe(JSON.stringify({ error }));
}

describe("/api/tasks/[id] maps lane-packet guard refusals instead of surfacing a 500", () => {
  test("PATCH: generic Done or archive on a lane packet (LANE_PACKET_TRANSITION_REQUIRED) is 409", async () => {
    const { PATCH } = await loadRoute();
    await withConvexMutation({ reject: convexUncaught("LANE_PACKET_TRANSITION_REQUIRED") }, async (calls) => {
      const response = await PATCH(patchRequest({ status: "done" }), params());
      await expectEnumeratedError(response, 409, "lane packet change requires /api/tasks/lane-packet");
      expect(calls).toEqual([{ name: "tasks:update", args: { id: TASK_ID, status: "done" } }]);
    });
  });

  test("PATCH: any generic write to a closed lane packet (LANE_PACKET_CLOSED) is 409", async () => {
    const { PATCH } = await loadRoute();
    await withConvexMutation({ reject: convexUncaught("LANE_PACKET_CLOSED") }, async (calls) => {
      const response = await PATCH(patchRequest({ status: "todo" }), params());
      await expectEnumeratedError(response, 409, "lane packet is already closed");
      expect(calls).toEqual([{ name: "tasks:update", args: { id: TASK_ID, status: "todo" } }]);
    });
  });

  test("DELETE: deleting a lane packet (LANE_PACKET_TRANSITION_REQUIRED) is 409", async () => {
    const { DELETE } = await loadRoute();
    await withConvexMutation({ reject: convexUncaught("LANE_PACKET_TRANSITION_REQUIRED") }, async (calls) => {
      const response = await DELETE(deleteRequest(), params());
      await expectEnumeratedError(response, 409, "lane packet change requires /api/tasks/lane-packet");
      expect(calls).toEqual([{ name: "tasks:remove", args: { id: TASK_ID } }]);
    });
  });

  test("PATCH: an invalid lane-packet write (LANE_PACKET_INVALID) is 400", async () => {
    const { PATCH } = await loadRoute();
    await withConvexMutation({ reject: convexUncaught("LANE_PACKET_INVALID") }, async (calls) => {
      const response = await PATCH(patchRequest({ dedupeKey: "a-different-key" }), params());
      await expectEnumeratedError(response, 400, "invalid lane packet request");
      expect(calls).toHaveLength(1);
    });
  });
});

describe("/api/tasks/[id] keeps its prior behavior for everything else", () => {
  const unrelated: Array<[string, () => Error]> = [
    ["a network failure", () => new Error("connect ECONNREFUSED 127.0.0.1:3210 internal-host-detail")],
    ["an existing generic guard", () => convexUncaught("Task not found: synthetic-task-id-1")],
    ["an unenumerated lane-packet-like code", () => convexUncaught("LANE_PACKET_SOMETHING_NEW internal detail")],
  ];

  for (const [label, makeError] of unrelated) {
    test(`${label} is rethrown unchanged by PATCH and DELETE, never rendered into a response`, async () => {
      const { PATCH, DELETE } = await loadRoute();
      const patchError = makeError();
      await withConvexMutation({ reject: patchError }, async () => {
        expect(await rejection(() => PATCH(patchRequest({ title: "Renamed" }), params()))).toBe(patchError);
      });
      const deleteError = makeError();
      await withConvexMutation({ reject: deleteError }, async () => {
        expect(await rejection(() => DELETE(deleteRequest(), params()))).toBe(deleteError);
      });
    });
  }

  test("PATCH still fails on a malformed body before calling Convex", async () => {
    const { PATCH } = await loadRoute();
    await withConvexMutation({ resolve: null }, async (calls) => {
      const caught = await rejection(() => PATCH(patchRequest("{not-json"), params()));
      expect(caught instanceof Error).toBe(true);
      expect(calls).toHaveLength(0);
    });
  });

  test("a legacy PATCH forwards the id and body unchanged and returns the same success body", async () => {
    const { PATCH } = await loadRoute();
    const body = { title: "Legacy renamed", status: "done", priority: "high", snoozedUntil: 1_790_000_000_000 };
    await withConvexMutation({ resolve: null }, async (calls) => {
      const response = await PATCH(patchRequest(body), params());
      expect(response.status).toBe(200);
      expect(await response.text()).toBe(JSON.stringify({ success: true }));
      expect(calls).toEqual([{ name: "tasks:update", args: { id: TASK_ID, ...body } }]);
    });
  });

  test("a legacy DELETE forwards only the id and returns the same success body", async () => {
    const { DELETE } = await loadRoute();
    await withConvexMutation({ resolve: null }, async (calls) => {
      const response = await DELETE(deleteRequest(), params());
      expect(response.status).toBe(200);
      expect(await response.text()).toBe(JSON.stringify({ success: true }));
      expect(calls).toEqual([{ name: "tasks:remove", args: { id: TASK_ID } }]);
    });
  });
});
