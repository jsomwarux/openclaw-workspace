import { describe, expect, test } from "bun:test";
import { legacyRedirects, missionControlNav, mobileNav } from "./routes";

describe("mission control routes", () => {
  test("cuts primary nav to Cockpit, Money, and Systems", () => {
    expect(missionControlNav.map((item) => item.label)).toEqual(["Cockpit", "Money", "Systems"]);
    expect(missionControlNav.map((item) => item.href)).toEqual(["/", "/consulting", "/machine"]);
  });

  test("drops Ship, Work, Evidence, and Health as their own nav entries", () => {
    const labels = missionControlNav.map((item) => item.label);

    expect(labels.includes("Ship")).toBe(false);
    expect(labels.includes("Work")).toBe(false);
    expect(labels.includes("Evidence")).toBe(false);
    expect(labels.includes("Health")).toBe(false);
  });

  test("Systems absorbs the machine, evidence, and health surfaces as aliases", () => {
    const systems = missionControlNav.find((item) => item.label === "Systems");

    expect(systems?.href).toBe("/machine");
    expect(systems?.aliases.includes("/evidence")).toBe(true);
    expect(systems?.aliases.includes("/health")).toBe(true);
    expect(systems?.aliases.includes("/machine")).toBe(true);
  });

  test("mobile nav mirrors the same three lanes", () => {
    expect(mobileNav).toEqual(missionControlNav);
  });

  test("keeps the legacy redirects working after the nav cut", () => {
    expect(legacyRedirects["/tasks"]).toBe("/work");
    expect(legacyRedirects["/vibe"]).toBe("/ship");
    expect(legacyRedirects["/agents"]).toBe("/machine");
    expect(legacyRedirects["/audit"]).toBe("/evidence");
    expect(legacyRedirects["/monitor"]).toBe("/health");
    expect(legacyRedirects["/costs"]).toBe("/health");
  });

  test("keeps Passive Income reachable rather than redirecting it away", () => {
    expect(legacyRedirects["/passive-income"]).toBe(undefined);
  });
});
