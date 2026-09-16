import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import {
  AUTHORITY_VERIFIER_ACTOR_ID,
  buildKeychainHelperRequest,
  buildInstallerRequest,
  buildConvexEnvironmentChanges,
  buildRuntimeEnvironment,
  buildServiceProcessEnvironment,
  resolveTailscaleLogin,
} from "../../scripts/outreach-runtime-secrets.mjs";

function captureError(run: () => unknown): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

describe("outreach runtime secret handling", () => {
  test("can compile the ignored Keychain helper from checked-in source", () => {
    expect(buildKeychainHelperRequest()).toEqual({
      file: "/usr/bin/swiftc",
      args: [
        "./scripts/outreach-keychain-helper.swift",
        "-o",
        "./.runtime/outreach-keychain-helper",
      ],
    });
    const runtime = readFileSync("scripts/outreach-runtime-secrets.mjs", "utf8");
    expect(runtime).toContain("function install() {\n  ensureKeychainHelper();");
  });

  test("generates and stores capabilities inside the Keychain helper", () => {
    const request = buildInstallerRequest();
    expect(request.args).toEqual(["install"]);
    expect(request.input).toBe(undefined);
  });

  test("requires distinct nonblank capabilities and a resolved JT login", () => {
    expect(buildRuntimeEnvironment("review-a", "decision-b", "jt@example.com")).toEqual({
      OUTREACH_REVIEW_CAPABILITY: "review-a",
      OUTREACH_DECISION_CAPABILITY: "decision-b",
      OUTREACH_DECISION_JT_LOGIN: "jt@example.com",
    });
    let equalRejected = false;
    let blankLoginRejected = false;
    try { buildRuntimeEnvironment("same", "same", "jt@example.com"); } catch { equalRejected = true; }
    try { buildRuntimeEnvironment("review-a", "decision-b", " "); } catch { blankLoginRejected = true; }
    expect(equalRejected).toBe(true);
    expect(blankLoginRejected).toBe(true);
  });

  test("starts existing services without the optional authority capability pair", () => {
    expect(buildRuntimeEnvironment("review-a", "decision-b", "jt@example.com", undefined, undefined)).toEqual({
      OUTREACH_REVIEW_CAPABILITY: "review-a",
      OUTREACH_DECISION_CAPABILITY: "decision-b",
      OUTREACH_DECISION_JT_LOGIN: "jt@example.com",
    });
  });

  test("removes inherited authority variables when the optional pair is absent", () => {
    const runtime = buildRuntimeEnvironment("review-a", "decision-b", "jt@example.com");
    expect(buildServiceProcessEnvironment({
      PATH: "/bin",
      OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY: "stale-write",
      OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY: "stale-read",
      OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID: "stale-actor",
    }, runtime)).toEqual({
      PATH: "/bin",
      OUTREACH_REVIEW_CAPABILITY: "review-a",
      OUTREACH_DECISION_CAPABILITY: "decision-b",
      OUTREACH_DECISION_JT_LOGIN: "jt@example.com",
    });
  });

  test("fails closed when only one authority capability is configured", () => {
    expect(captureError(() => buildRuntimeEnvironment(
      "review-a", "decision-b", "jt@example.com", "authority-write-c", undefined,
    ))).toBe("outreach capability configuration is invalid");
    expect(captureError(() => buildRuntimeEnvironment(
      "review-a", "decision-b", "jt@example.com", undefined, "authority-read-d",
    ))).toBe("outreach capability configuration is invalid");
  });

  test("rejects every collision among all four capability roles", () => {
    const baseline = ["review-a", "decision-b", "authority-write-c", "authority-read-d"];
    for (let left = 0; left < baseline.length; left += 1) {
      for (let right = left + 1; right < baseline.length; right += 1) {
        const colliding = [...baseline];
        colliding[right] = colliding[left];
        expect(captureError(() => buildRuntimeEnvironment(
          colliding[0], colliding[1], "jt@example.com", colliding[2], colliding[3],
        ))).toBe("outreach capability configuration is invalid");
      }
    }
  });

  test("injects the complete authority pair and fixed verifier actor ID", () => {
    expect(AUTHORITY_VERIFIER_ACTOR_ID).toBe("openclaw:review-verifier-v1");
    expect(buildRuntimeEnvironment(
      "review-a", "decision-b", "jt@example.com", "authority-write-c", "authority-read-d",
    )).toEqual({
      OUTREACH_REVIEW_CAPABILITY: "review-a",
      OUTREACH_DECISION_CAPABILITY: "decision-b",
      OUTREACH_DECISION_JT_LOGIN: "jt@example.com",
      OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY: "authority-write-c",
      OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY: "authority-read-d",
      OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID: "openclaw:review-verifier-v1",
    });
  });

  test("resolves the current Tailscale owner's login without hardcoding it", () => {
    const status = {
      Self: { UserID: 7 },
      User: { "7": { LoginName: "jt@example.com" } },
    };
    expect(resolveTailscaleLogin(status)).toBe("jt@example.com");
  });

  test("syncs the existing capability values when the optional pair is absent", () => {
    expect(buildConvexEnvironmentChanges("review-a", "decision-b")).toEqual([
      { name: "OUTREACH_REVIEW_CAPABILITY", value: "review-a" },
      { name: "OUTREACH_DECISION_CAPABILITY", value: "decision-b" },
    ]);
  });

  test("syncs the same complete authority capability set and actor mapping to Convex", () => {
    expect(buildConvexEnvironmentChanges(
      "review-a", "decision-b", "authority-write-c", "authority-read-d",
    )).toEqual([
      { name: "OUTREACH_REVIEW_CAPABILITY", value: "review-a" },
      { name: "OUTREACH_DECISION_CAPABILITY", value: "decision-b" },
      { name: "OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY", value: "authority-write-c" },
      { name: "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY", value: "authority-read-d" },
      {
        name: "OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID",
        value: "openclaw:review-verifier-v1",
      },
    ]);
  });

  test("never leaks capability values through configuration failures or installer arguments", () => {
    const secret = "authority-secret-must-not-leak";
    let message = "";
    try {
      buildRuntimeEnvironment("review-a", "decision-b", "jt@example.com", secret, secret);
    } catch (error) {
      message = error instanceof Error ? error.message : String(error);
    }
    expect(message).toBe("outreach capability configuration is invalid");
    expect(message).not.toContain(secret);
    expect(JSON.stringify(buildInstallerRequest())).not.toContain(secret);

    const helper = readFileSync("scripts/outreach-keychain-helper.swift", "utf8");
    expect(helper).toContain('"review-authority-write"');
    expect(helper).toContain('"review-authority-read"');
    expect(helper).not.toContain("standardOutput.write(review");
    expect(helper).not.toContain("standardOutput.write(decision");
  });

  test("the live Next launcher injects capabilities from Keychain", () => {
    const launcher = readFileSync("../scripts/mission-control-start.sh", "utf8");
    expect(launcher).toContain("scripts/outreach-runtime-secrets.mjs run-next --");
    expect(launcher).not.toContain("OUTREACH_REVIEW_CAPABILITY=");
    expect(launcher).not.toContain("OUTREACH_DECISION_CAPABILITY=");
  });

  test("the live Convex launcher injects capabilities from Keychain", () => {
    const launcher = readFileSync("../scripts/mission-control-convex-sync.sh", "utf8");
    expect(launcher).toContain("scripts/outreach-runtime-secrets.mjs run-convex --");
    expect(launcher).not.toContain("OUTREACH_REVIEW_CAPABILITY=");
    expect(launcher).not.toContain("OUTREACH_DECISION_CAPABILITY=");
  });

  test("the runtime entrypoint executes under the Node binary used by launchers", () => {
    const result = spawnSync(
      "/opt/homebrew/opt/node@22/bin/node",
      ["scripts/outreach-runtime-secrets.mjs", "unsupported"],
      { encoding: "utf8" },
    );
    expect(result.status).toBe(2);
    expect(result.stderr).toContain("unsupported secure capability operation");
  });
});
