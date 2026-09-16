import { describe, expect, test } from "bun:test";
import {
  chmodSync,
  existsSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { spawn, spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  AUTHORITY_VERIFIER_ACTOR_ID,
  buildKeychainHelperRequest,
  buildInstallerRequest,
  buildConvexEnvironmentChanges,
  buildRuntimeEnvironment,
  buildServiceProcessEnvironment,
  buildLockedReexecRequest,
  ensureV3KeychainHelper,
  installCapabilitySetFromHelper,
  parseCapabilitySetRead,
  readCapabilitySetFromHelpers,
  resolveTailscaleLogin,
} from "../../scripts/outreach-runtime-secrets.mjs";

function captureError(run: () => unknown): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

function executable(path: string, source: string) {
  writeFileSync(path, source, { mode: 0o700 });
  chmodSync(path, 0o700);
}

describe("outreach runtime secret handling", () => {
  test("targets a separate stable v3 helper path", () => {
    expect(buildKeychainHelperRequest()).toEqual({
      file: "/usr/bin/swiftc",
      args: [
        "./scripts/outreach-keychain-helper.swift",
        "-o",
        "./.runtime/outreach-keychain-helper-v3",
      ],
    });
  });

  test("compiles v3 only when absent and leaves legacy helper bytes unchanged", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-keychain-helper-test-"));
    const legacyPath = join(directory, "outreach-keychain-helper");
    const v3Path = join(directory, "outreach-keychain-helper-v3");
    try {
      executable(legacyPath, "#!/bin/sh\nexit 2\n");
      const legacyBefore = readFileSync(legacyPath);

      ensureV3KeychainHelper(v3Path);

      const probe = spawnSync(v3Path, ["probe", "outreach-capabilities-v3"], { encoding: "utf8" });
      expect(probe.status).toBe(0);
      expect(probe.stdout).toBe("");
      expect(readFileSync(legacyPath)).toEqual(legacyBefore);
      expect(statSync(v3Path).mode & 0o777).toBe(0o700);
      expect(statSync(`${v3Path}.sha256`).mode & 0o777).toBe(0o600);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("v3 protocol or source mismatch fails closed without replacing bytes", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-keychain-mismatch-test-"));
    const v3Path = join(directory, "outreach-keychain-helper-v3");
    try {
      executable(v3Path, [
        "#!/bin/sh",
        '[ "$1" = "probe" ] && [ "$2" = "outreach-capabilities-v3" ] && exit 0',
        "exit 2",
        "",
      ].join("\n"));
      writeFileSync(`${v3Path}.sha256`, "stale-source-digest\n", { mode: 0o600 });
      const before = readFileSync(v3Path);

      expect(captureError(() => ensureV3KeychainHelper(v3Path)))
        .toBe("v3 capability helper mismatch; explicit versioned migration required");

      expect(readFileSync(v3Path)).toEqual(before);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("generates and stores capabilities inside the Keychain helper", () => {
    const request = buildInstallerRequest();
    expect(request.args).toEqual(["install-set"]);
    expect(request.input).toBe(undefined);
    const helper = readFileSync("scripts/outreach-keychain-helper.swift", "utf8");
    expect(helper.match(/store\(capabilitySetService/g)?.length).toBe(1);
    expect(helper).toContain('args == ["read-set"]');
  });

  test("parses one captured versioned four-capability set and rejects collisions", () => {
    const encoded = JSON.stringify({
      version: 1,
      review: "review-a",
      decision: "decision-b",
      reviewAuthorityWrite: "authority-write-c",
      reviewAuthorityRead: "authority-read-d",
    });
    expect(parseCapabilitySetRead({ status: 0, stdout: `${encoded}\n` })).toEqual({
      review: "review-a",
      decision: "decision-b",
      authorityWrite: "authority-write-c",
      authorityRead: "authority-read-d",
    });
    expect(captureError(() => parseCapabilitySetRead({
      status: 0,
      stdout: JSON.stringify({
        version: 1,
        review: "same",
        decision: "decision-b",
        reviewAuthorityWrite: "same",
        reviewAuthorityRead: "authority-read-d",
      }),
    }))).toBe("outreach capability configuration is invalid");
    expect(captureError(() => parseCapabilitySetRead({
      status: 0,
      stdout: JSON.stringify({
        version: 1,
        review: "review-a",
        decision: "decision-b",
        reviewAuthorityWrite: " ",
        reviewAuthorityRead: "\t",
      }),
    }))).toBe("outreach capability configuration is invalid");
  });

  test("each Keychain item is read only by its owning helper", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-legacy-helper-test-"));
    const legacyPath = join(directory, "legacy-helper");
    const v3Path = join(directory, "v3-helper");
    const logPath = join(directory, "calls.log");
    try {
      executable(v3Path, [
        "#!/bin/sh",
        `printf 'v3:%s\\n' "$1" >> '${logPath}'`,
        '[ "$1" = "read-set" ] && exit 3',
        "exit 2",
        "",
      ].join("\n"));
      executable(legacyPath, [
        "#!/bin/sh",
        `printf 'legacy:%s:%s\\n' "$1" "$2" >> '${logPath}'`,
        '[ "$1:$2" = "read:review" ] && printf \'legacy-review\\n\' && exit 0',
        '[ "$1:$2" = "read:decision" ] && printf \'legacy-decision\\n\' && exit 0',
        "exit 2",
        "",
      ].join("\n"));
      expect(readCapabilitySetFromHelpers(v3Path, legacyPath)).toEqual({
        review: "legacy-review",
        decision: "legacy-decision",
        authorityWrite: undefined,
        authorityRead: undefined,
      });
      expect(readFileSync(logPath, "utf8").trim().split("\n")).toEqual([
        "v3:read-set",
        "legacy:read:review",
        "legacy:read:decision",
      ]);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("a failed explicit rotation preserves the prior readable set", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-failed-rotation-test-"));
    const helperPath = join(directory, "rotation-helper");
    const statePath = join(directory, "set.json");
    const prior = JSON.stringify({
      version: 1,
      review: "review-a",
      decision: "decision-b",
      reviewAuthorityWrite: "authority-write-c",
      reviewAuthorityRead: "authority-read-d",
    });
    try {
      writeFileSync(statePath, prior);
      executable(helperPath, [
        "#!/bin/sh",
        'case "$1" in',
        `  read-set) cat '${statePath}' ;;`,
        "  install-set) exit 2 ;;",
        "  *) exit 2 ;;",
        "esac",
        "",
      ].join("\n"));

      expect(captureError(() => installCapabilitySetFromHelper(helperPath)))
        .toBe("secure capability operation failed");
      expect(readFileSync(statePath, "utf8")).toBe(prior);
      expect(readCapabilitySetFromHelpers(helperPath, join(directory, "unused-legacy")).review)
        .toBe("review-a");
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("macOS advisory lock blocks contention and releases when holder dies", async () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-lockf-test-"));
    const lockPath = join(directory, "capability.lock");
    const readyPath = join(directory, "ready");
    try {
      const holder = spawn("/usr/bin/lockf", [
        lockPath,
        "/bin/sh",
        "-c",
        `touch '${readyPath}'; sleep 10`,
      ]);
      const deadline = Date.now() + 2_000;
      while (!existsSync(readyPath) && Date.now() < deadline) {
        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 10);
      }
      expect(existsSync(readyPath)).toBe(true);
      expect(spawnSync("/usr/bin/lockf", ["-t", "0", lockPath, "/usr/bin/true"]).status)
        .not.toBe(0);
      holder.kill("SIGKILL");
      await new Promise<void>((resolve) => holder.once("exit", () => resolve()));
      expect(spawnSync("/usr/bin/lockf", ["-t", "1", lockPath, "/usr/bin/true"]).status)
        .toBe(0);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("lockf re-exec uses only nonsecret arguments and an internal guard", () => {
    const request = buildLockedReexecRequest(["sync-convex"]);
    expect(request.file).toBe("/usr/bin/lockf");
    expect(request.args).toContain("--outreach-lock-held");
    expect(JSON.stringify(request)).not.toContain("authority-secret-must-not-leak");
  });

  test("helper subprocesses fail closed on a bounded timeout", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-helper-timeout-test-"));
    const v3Path = join(directory, "v3-helper");
    try {
      executable(v3Path, "#!/bin/sh\nsleep 1\n");
      const startedAt = Date.now();
      expect(captureError(() => readCapabilitySetFromHelpers(
        v3Path,
        join(directory, "legacy-helper"),
        25,
      ))).toBe("secure capability operation timed out");
      expect(Date.now() - startedAt < 500).toBe(true);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
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

  test("fails closed when both authority capabilities are present but blank", () => {
    expect(captureError(() => buildRuntimeEnvironment(
      "review-a", "decision-b", "jt@example.com", " ", "\t",
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
      { name: "OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY" },
      { name: "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY" },
      { name: "OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID" },
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
    expect(helper).toContain('"reviewAuthorityWrite"');
    expect(helper).toContain('"reviewAuthorityRead"');
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
