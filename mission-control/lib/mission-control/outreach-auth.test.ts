import { describe, expect, test } from "bun:test";
import { authorizeJtIdentity, assertDistinctServerCapability, secureCapabilityEqual } from "./outreach-auth";

function message(run: () => unknown) {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

async function asyncMessage(run: () => Promise<unknown>) {
  try { await run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

describe("outreach authority", () => {
  test("fails closed when JT identity configuration or trusted Tailscale identity is missing", () => {
    expect(message(() => authorizeJtIdentity(new Headers(), undefined))).toContain("JT login is not configured");
    expect(message(() => authorizeJtIdentity(new Headers(), "jt@example.com"))).toContain("JT identity required");
  });

  test("rejects a mismatched Tailscale identity and accepts only the configured login", () => {
    expect(message(() => authorizeJtIdentity(new Headers({ "Tailscale-User-Login": "other@example.com" }), "jt@example.com")))
      .toContain("JT identity forbidden");
    expect(authorizeJtIdentity(new Headers({ "Tailscale-User-Login": "jt@example.com" }), "jt@example.com"))
      .toEqual({ login: "jt@example.com" });
  });

  test("compares equal, unequal, and different-length capabilities with the cryptographic primitive", async () => {
    expect(await secureCapabilityEqual("same-secret", "same-secret")).toBe(true);
    expect(await secureCapabilityEqual("same-secret", "other-secrt")).toBe(false);
    expect(await secureCapabilityEqual("short", "a-much-longer-secret")).toBe(false);
  });

  test("rejects direct mutation access without the protected server capability", async () => {
    expect(await asyncMessage(() => assertDistinctServerCapability(undefined, "configured-secret", "peer-secret"))).toContain("server capability required");
    expect(await asyncMessage(() => assertDistinctServerCapability("wrong", "configured-secret", "peer-secret"))).toContain("server capability required");
    expect(await asyncMessage(() => assertDistinctServerCapability("configured-secret", undefined, "peer-secret"))).toContain("capability configuration is invalid");
    expect(await assertDistinctServerCapability("configured-secret", "configured-secret", "peer-secret")).toBe("configured-secret");
  });

  test("rejects equal, missing, or blank capability configuration before direct mutation access", async () => {
    for (const [configured, peer] of [
      ["same-secret", "same-secret"],
      ["", "peer-secret"],
      ["   ", "peer-secret"],
      ["configured-secret", ""],
      ["configured-secret", "   "],
      [undefined, "peer-secret"],
      ["configured-secret", undefined],
    ] as const) {
      expect(await asyncMessage(() => assertDistinctServerCapability("same-secret", configured, peer)))
        .toContain("capability configuration is invalid");
    }
  });
});
