import { describe, expect, test } from "bun:test";
import { legacyRedirects, missionControlNav, mobileNav } from "./routes";

describe("mission control routes", () => {
  test("sets primary nav to the five lanes: Today, Clients, Money, Library, Systems", () => {
    expect(missionControlNav.map((item) => item.label)).toEqual(["Today", "Clients", "Money", "Library", "Systems"]);
    expect(missionControlNav.map((item) => item.href)).toEqual(["/", "/clients", "/consulting", "/library", "/machine"]);
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

  test("Library aliases the existing skills surface for now", () => {
    const library = missionControlNav.find((item) => item.label === "Library");

    expect(library?.href).toBe("/library");
    expect(library?.aliases.includes("/skills")).toBe(true);
    expect(legacyRedirects["/library"]).toBe("/skills");
  });

  test("mobile nav mirrors the same five lanes", () => {
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
