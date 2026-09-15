import { describe, expect, test } from "bun:test";

process.env.NEXT_PUBLIC_CONVEX_URL ??= "http://127.0.0.1:3210";

async function loadHandlers() {
  return import("../../app/api/tasks/route");
}

function malformedRequest(method: "POST" | "PATCH") {
  return new Request("http://localhost/api/tasks", {
    method,
    headers: { "Content-Type": "application/json" },
    body: "{not-json",
  });
}

describe("task route request validation", () => {
  test("returns 400 for invalid JSON before touching Convex", async () => {
    const handlers = await loadHandlers();
    expect((await handlers.POST(malformedRequest("POST"))).status).toBe(400);
    expect((await handlers.PATCH(malformedRequest("PATCH"))).status).toBe(400);
  });

  test("returns 400 for malformed card fields before touching Convex", async () => {
    const { POST } = await loadHandlers();
    const response = await POST(new Request("http://localhost/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "Bad card", exactSteps: "not-an-array" }),
    }));
    expect(response.status).toBe(400);
  });

  test("returns 400 for blank and oversized feedback before touching Convex", async () => {
    const { PATCH } = await loadHandlers();
    for (const body of ["   ", "x".repeat(4001)]) {
      const response = await PATCH(new Request("http://localhost/api/tasks", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "append-feedback", id: "task-1", body, author: "jt" }),
      }));
      expect(response.status).toBe(400);
    }
  });
});
