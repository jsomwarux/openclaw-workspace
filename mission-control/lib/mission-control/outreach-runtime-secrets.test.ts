import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import {
  buildKeychainHelperRequest,
  buildInstallerRequest,
  buildConvexEnvironmentChanges,
  buildRuntimeEnvironment,
  resolveTailscaleLogin,
} from "../../scripts/outreach-runtime-secrets.mjs";

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

  test("resolves the current Tailscale owner's login without hardcoding it", () => {
    const status = {
      Self: { UserID: 7 },
      User: { "7": { LoginName: "jt@example.com" } },
    };
    expect(resolveTailscaleLogin(status)).toBe("jt@example.com");
  });

  test("syncs only the two capability values to local Convex", () => {
    expect(buildConvexEnvironmentChanges("review-a", "decision-b")).toEqual([
      { name: "OUTREACH_REVIEW_CAPABILITY", value: "review-a" },
      { name: "OUTREACH_DECISION_CAPABILITY", value: "decision-b" },
    ]);
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
