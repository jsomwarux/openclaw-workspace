import { describe, expect, test } from "bun:test";
import { legacyRedirects, missionControlNav } from "./routes";

describe("mission control routes", () => {
  test("uses /work as the primary Work lane instead of the legacy task board", () => {
    const work = missionControlNav.find((item) => item.label === "Work");

    expect(work?.href).toBe("/work");
    expect(work?.aliases.includes("/tasks")).toBe(false);
  });

  test("redirects the old task board route to the Work lane", () => {
    expect(legacyRedirects["/tasks"]).toBe("/work");
  });

  test("uses /ship as the primary Ship lane and preserves old vibe route as legacy", () => {
    const ship = missionControlNav.find((item) => item.label === "Ship");

    expect(ship?.href).toBe("/ship");
    expect(ship?.aliases.includes("/vibe")).toBe(true);
    expect(legacyRedirects["/vibe"]).toBe("/ship");
  });

  test("uses /machine as the primary Machine lane and preserves old agents route as legacy", () => {
    const machine = missionControlNav.find((item) => item.label === "Machine");

    expect(machine?.href).toBe("/machine");
    expect(machine?.aliases.includes("/agents")).toBe(true);
    expect(legacyRedirects["/agents"]).toBe("/machine");
  });

  test("uses /evidence as the primary Evidence lane and preserves old audit route as legacy", () => {
    const evidence = missionControlNav.find((item) => item.label === "Evidence");

    expect(evidence?.href).toBe("/evidence");
    expect(evidence?.aliases.includes("/audit")).toBe(true);
    expect(legacyRedirects["/audit"]).toBe("/evidence");
  });

  test("uses /health as the primary Health lane and preserves old monitor and cost routes as legacy", () => {
    const health = missionControlNav.find((item) => item.label === "Health");

    expect(health?.href).toBe("/health");
    expect(health?.aliases.includes("/monitor")).toBe(true);
    expect(health?.aliases.includes("/costs")).toBe(true);
    expect(legacyRedirects["/monitor"]).toBe("/health");
    expect(legacyRedirects["/costs"]).toBe("/health");
  });
});
