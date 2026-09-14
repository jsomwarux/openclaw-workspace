import { describe, expect, test } from "bun:test";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";

type CreateOnlyMutation = (
  input: Record<string, unknown>,
) => Promise<{ id: string; created: boolean }>;
type CreatePostHandler = (
  mutate: CreateOnlyMutation,
) => (request: Request) => Promise<Response>;

const routeFile = fileURLToPath(new URL("../../app/api/tasks/create-only/route.ts", import.meta.url));
const handlerModulePath = "./task-create-only-post";

async function loadCreatePostHandler(): Promise<CreatePostHandler | undefined> {
  const routeExists = existsSync(routeFile);
  expect(routeExists).toBe(true);
  if (!routeExists) return undefined;
  const handler = await import(handlerModulePath) as { createPostHandler?: CreatePostHandler };
  expect(typeof handler.createPostHandler).toBe("function");
  return handler.createPostHandler;
}

function taskRequest(body: Record<string, unknown>) {
  return new Request("http://localhost/api/tasks/create-only", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

describe("dedicated create-only task route", () => {
  test("returns an explicit capability marker when it creates a task", async () => {
    const createPostHandler = await loadCreatePostHandler();
    if (!createPostHandler) return;
    let received: Record<string, unknown> | undefined;
    const post = createPostHandler(async (input) => {
      received = input;
      return { id: "task-new", created: true };
    });

    const response = await post(taskRequest({ title: "New", dedupeKey: "version-1" }));

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({
      id: "task-new",
      created: true,
      success: true,
      writeMode: "create-only",
    });
    expect(received).toMatchObject({
      title: "New",
      dedupeKey: "version-1",
      status: "todo",
      assignee: "eve",
      priority: "medium",
    });
  });

  test("returns the same capability marker when the task already exists", async () => {
    const createPostHandler = await loadCreatePostHandler();
    if (!createPostHandler) return;
    const post = createPostHandler(async () => ({ id: "task-existing", created: false }));

    const response = await post(taskRequest({ title: "Existing", dedupeKey: "version-1" }));

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({
      id: "task-existing",
      created: false,
      success: true,
      writeMode: "create-only",
    });
  });

  test("rejects a missing dedupe key without calling the mutation", async () => {
    const createPostHandler = await loadCreatePostHandler();
    if (!createPostHandler) return;
    let mutations = 0;
    const post = createPostHandler(async () => {
      mutations += 1;
      return { id: "unexpected", created: true };
    });

    const response = await post(taskRequest({ title: "Unsafe" }));

    expect(response.status).toBe(400);
    expect(mutations).toBe(0);
  });

  test("an older server has no POST handler that can mutate through the dedicated path", async () => {
    process.env.NEXT_PUBLIC_CONVEX_URL ??= "http://127.0.0.1:3210";
    const legacyDynamicRoutePath = "../../app/api/tasks/[id]/route";
    const legacyDynamicRoute = await import(legacyDynamicRoutePath);

    expect("POST" in legacyDynamicRoute).toBe(false);
  });
});
