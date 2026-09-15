import { describe, expect, test } from "bun:test";
import { authorizeJtIdentity, assertServerCapability } from "./outreach-auth";

function message(run: () => unknown) {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

describe("outreach authority", () => {
  test("fails closed when JT identity configuration or trusted Tailscale identity is missing", () => {
    expect(message(() => authorizeJtIdentity(new Headers(), undefined))).toContain("JT login is not configured");
    expect(message(() => authorizeJtIdentity(new Headers(), "jt@example.com"))).toContain("JT identity required");
  });

  test("rejects a mismatched Tailscale identity and accepts only the configured login", () => {
    expect(message(() => authorizeJtIdentity(new Headers({ "Tailscale-User-Login": "other@example.com" }), "jt@example.com")))
      .toContain("JT identity required");
    expect(authorizeJtIdentity(new Headers({ "Tailscale-User-Login": "jt@example.com" }), "jt@example.com"))
      .toEqual({ login: "jt@example.com" });
  });

  test("rejects direct mutation access without the protected server capability", () => {
    expect(message(() => assertServerCapability(undefined, "configured-secret"))).toContain("server capability required");
    expect(message(() => assertServerCapability("wrong", "configured-secret"))).toContain("server capability required");
    expect(message(() => assertServerCapability("configured-secret", undefined))).toContain("server capability is not configured");
    expect(assertServerCapability("configured-secret", "configured-secret")).toBe(undefined);
  });
});
