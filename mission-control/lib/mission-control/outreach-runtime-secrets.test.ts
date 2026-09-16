import { describe, expect, test } from "bun:test";
import {
  chmodSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  renameSync,
  rmSync,
  statSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { spawn, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  AUTHORITY_VERIFIER_ACTOR_ID,
  CONFIRMED_SEND_REVIEWED_SOURCE,
  buildKeychainHelperRequest,
  buildInstallerRequest,
  buildConfirmedSendRequest,
  buildConvexEnvironmentChanges,
  buildReviewAuthorityReaderEnvironment,
  buildRuntimeEnvironment,
  buildServiceProcessEnvironment,
  buildLockedReexecRequest,
  ensureV3KeychainHelper,
  installCapabilitySet,
  installCapabilitySetFromHelper,
  materializeReviewedConfirmedSendScript,
  parseCapabilitySetRead,
  parseConfirmedSendResult,
  readCapabilitySetFromHelpers,
  resolveTailscaleLogin,
  validateConfirmedSendPreflight,
} from "../../scripts/outreach-runtime-secrets.mjs";

function captureError(run: () => unknown): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

function executable(path: string, source: string) {
  writeFileSync(path, source, { mode: 0o700 });
  chmodSync(path, 0o700);
}

function git(path: string, args: string[]) {
  const result = spawnSync("/usr/bin/git", ["-C", path, ...args], {
    encoding: "utf8",
    env: { LANG: "C.UTF-8", LC_ALL: "C.UTF-8", NODE_ENV: "test" },
  });
  if (result.status !== 0 || result.stderr) throw new Error("git fixture failed");
  return result.stdout.trim();
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

  test("publishes the source stamp before the v3 helper path", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-keychain-publish-order-test-"));
    const v3Path = join(directory, "outreach-keychain-helper-v3");
    const targets: string[] = [];
    try {
      ensureV3KeychainHelper(v3Path, "/usr/bin/swiftc", {
        rename: (source, target) => {
          targets.push(String(target));
          renameSync(source, target);
        },
      });
      expect(targets).toEqual([`${v3Path}.sha256`, v3Path]);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("a crash after stamp publication leaves v3 absent and recompilable", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-keychain-publish-crash-test-"));
    const v3Path = join(directory, "outreach-keychain-helper-v3");
    let publishes = 0;
    try {
      expect(captureError(() => ensureV3KeychainHelper(v3Path, "/usr/bin/swiftc", {
        rename: (source, target) => {
          publishes += 1;
          if (publishes === 2) throw new Error("simulated publish crash");
          renameSync(source, target);
        },
      }))).toBe("simulated publish crash");
      expect(existsSync(`${v3Path}.sha256`)).toBe(true);
      expect(existsSync(v3Path)).toBe(false);

      ensureV3KeychainHelper(v3Path);
      expect(spawnSync(v3Path, ["probe", "outreach-capabilities-v3"]).status).toBe(0);
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

  test("successful rotation has no fallible post-write read step", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-terminal-rotation-test-"));
    const helperPath = join(directory, "rotation-helper");
    const statePath = join(directory, "set.json");
    const callsPath = join(directory, "calls.log");
    const prior = JSON.stringify({
      version: 1,
      review: "review-a",
      decision: "decision-b",
      reviewAuthorityWrite: "authority-write-c",
      reviewAuthorityRead: "authority-read-d",
    });
    const replacement = JSON.stringify({
      version: 1,
      review: "review-new",
      decision: "decision-new",
      reviewAuthorityWrite: "authority-write-new",
      reviewAuthorityRead: "authority-read-new",
    });
    try {
      writeFileSync(statePath, prior);
      executable(helperPath, [
        "#!/bin/sh",
        `printf '%s\\n' "$1" >> '${callsPath}'`,
        'case "$1" in',
        `  install-set) printf '%s' '${replacement}' > '${statePath}' ;;`,
        "  read-set) exit 2 ;;",
        "  *) exit 2 ;;",
        "esac",
        "",
      ].join("\n"));

      expect(captureError(() => installCapabilitySetFromHelper(helperPath))).toBe(undefined);
      expect(readFileSync(statePath, "utf8")).toBe(replacement);
      expect(readFileSync(callsPath, "utf8").trim().split("\n")).toEqual(["install-set"]);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("rotation completes every external preflight before the terminal store", () => {
    const events: string[] = [];
    installCapabilitySet({
      ensureHelper: () => { events.push("helper"); },
      resolveLogin: () => { events.push("tailscale"); return "jt@example.com"; },
      storeSet: () => { events.push("store"); },
    });
    expect(events).toEqual(["helper", "tailscale", "store"]);

    events.length = 0;
    expect(captureError(() => installCapabilitySet({
      ensureHelper: () => { events.push("helper"); },
      resolveLogin: () => { events.push("tailscale"); throw new Error("tailscale failed"); },
      storeSet: () => { events.push("store"); },
    }))).toBe("tailscale failed");
    expect(events).toEqual(["helper", "tailscale"]);
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

  test("runtime capability transport never serializes onto stdout", () => {
    const runtime = readFileSync("scripts/outreach-runtime-secrets.mjs", "utf8");
    expect(runtime).not.toContain("process.stdout.write(JSON.stringify(readRuntimeEnvironment()))");
    expect(runtime).toContain("result.output[3]");
  });

  test("private capability transport requires a distinct FIFO or socket", () => {
    const runtime = readFileSync("scripts/outreach-runtime-secrets.mjs", "utf8");
    expect(runtime).toContain("channel.isFIFO() || channel.isSocket()");
    expect(runtime).toContain("sameFileIdentity(channel, stdout)");
    expect(runtime).toContain("sameFileIdentity(channel, stderr)");
  });

  test("forged internal environment emission without private fd fails before stdout or Keychain access", () => {
    const result = spawnSync(
      "/opt/homebrew/opt/node@22/bin/node",
      [
        "scripts/outreach-runtime-secrets.mjs",
        "--outreach-lock-held",
        "emit-runtime-environment",
      ],
      {
        encoding: "utf8",
        env: { ...process.env, OUTREACH_LOCKF_INTERNAL: "1" },
        stdio: ["ignore", "pipe", "pipe"],
      },
    );
    expect(result.status).toBe(2);
    expect(result.stdout).toBe("");
    expect(result.stderr).toContain("private capability pipe required");
    expect(result.stdout).not.toContain("OUTREACH_REVIEW_CAPABILITY");
  });

  for (const [name, redirection] of [
    ["stdout", "3>&1"],
    ["stderr", "3>&2"],
  ] as const) {
    test(`forged internal fd3 alias to ${name} fails before stdout or Keychain access`, () => {
      const result = spawnSync(
        "/bin/sh",
        [
          "-c",
          `exec /opt/homebrew/opt/node@22/bin/node scripts/outreach-runtime-secrets.mjs --outreach-lock-held emit-runtime-environment ${redirection}`,
        ],
        {
          encoding: "utf8",
          env: { ...process.env, OUTREACH_LOCKF_INTERNAL: "1" },
          stdio: ["ignore", "pipe", "pipe"],
        },
      );
      expect(result.status).toBe(2);
      expect(result.stdout).toBe("");
      expect(result.stderr).toBe("private capability pipe required\n");
      expect(`${result.stdout}${result.stderr}`).not.toContain("OUTREACH_REVIEW_CAPABILITY");
    });
  }

  test("forged internal regular-file fd3 fails without writing or accessing Keychain", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-forged-fd-file-test-"));
    const outputPath = join(directory, "forged-output");
    try {
      const result = spawnSync(
        "/bin/sh",
        [
          "-c",
          'exec /opt/homebrew/opt/node@22/bin/node scripts/outreach-runtime-secrets.mjs --outreach-lock-held emit-runtime-environment 3>"$FD_TARGET"',
        ],
        {
          encoding: "utf8",
          env: { ...process.env, OUTREACH_LOCKF_INTERNAL: "1", FD_TARGET: outputPath },
          stdio: ["ignore", "pipe", "pipe"],
        },
      );
      expect(result.status).toBe(2);
      expect(result.stdout).toBe("");
      expect(result.stderr).toBe("private capability pipe required\n");
      expect(readFileSync(outputPath, "utf8")).toBe("");
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("accepts a distinct parent-created fd3 pipe", () => {
    const result = spawnSync(
      "/opt/homebrew/opt/node@22/bin/node",
      [
        "-e",
        'import("./scripts/outreach-runtime-secrets.mjs").then(({ validatePrivateCapabilityPipe }) => validatePrivateCapabilityPipe(3))',
      ],
      { encoding: "utf8", stdio: ["ignore", "pipe", "pipe", "pipe"] },
    );
    expect(result.status).toBe(0);
    expect(result.stdout).toBe("");
    expect(result.stderr).toBe("");
  });

  test("lockf preserves a parent-created private fd 3 while stdout stays nonsecret", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-lockf-pipe-test-"));
    try {
      const result = spawnSync(
        "/opt/homebrew/opt/node@22/bin/node",
        [
          "-e",
          [
            'const { spawnSync } = require("node:child_process");',
            `const result = spawnSync("/usr/bin/lockf", [${JSON.stringify(join(directory, "lock"))}, "/bin/sh", "-c", "printf private-payload >&3"], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe", "pipe"] });`,
            'if (result.status !== 0 || result.stdout !== "" || result.output[3] !== "private-payload") process.exit(1);',
          ].join(" "),
        ],
        { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] },
      );
      expect(result.status).toBe(0);
      expect(result.stdout).toBe("");
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
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
      OUTREACH_SUPPRESSION_OWNER_ENABLED: "true",
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
      { name: "OUTREACH_SUPPRESSION_OWNER_ENABLED" },
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
      { name: "OUTREACH_SUPPRESSION_OWNER_ENABLED" },
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

  test("confirmed-send child receives only the authority-read capability and fixed command", () => {
    const receiptId = `pre_send_${"a".repeat(20)}`;
    const environment = buildReviewAuthorityReaderEnvironment("authority-read-only");
    expect(environment).toEqual({
      LANG: "C.UTF-8",
      LC_ALL: "C.UTF-8",
      PYTHONHASHSEED: "0",
      OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY: "authority-read-only",
    });
    const scriptPath = "/private/runtime/record_confirmed_send.py";
    const request = buildConfirmedSendRequest(
      receiptId,
      "authority-read-only",
      scriptPath,
      "/private/runtime",
    );
    expect(request).toEqual({
      file: "/usr/bin/python3",
      args: [
        "-I",
        "-S",
        scriptPath,
        "--pre-send-receipt-id",
        receiptId,
      ],
      cwd: "/private/runtime",
      env: environment,
    });
    expect(JSON.stringify(request)).not.toContain("OUTREACH_REVIEW_CAPABILITY");
    expect(JSON.stringify(request)).not.toContain("OUTREACH_DECISION_CAPABILITY");
    expect(JSON.stringify(request)).not.toContain("OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY");
    expect(JSON.stringify(request)).not.toContain("HTTP_PROXY");
  });

  test("confirmed-send materializes exact reviewed Git bytes, never mutable checkout bytes", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-reviewed-command-"));
    const repo = join(directory, "repo");
    const runtimeRoot = join(directory, "runtime");
    try {
      mkdirSync(repo, { mode: 0o700 });
      git(repo, ["init", "-q"]);
      git(repo, ["config", "user.name", "Test"]);
      git(repo, ["config", "user.email", "test@example.invalid"]);
      mkdirSync(join(repo, "scripts"), { mode: 0o700 });
      const reviewed = "#!/usr/bin/env python3\nprint('reviewed')\n";
      const workingPath = join(repo, "scripts", "record_confirmed_send.py");
      writeFileSync(workingPath, reviewed, { mode: 0o600 });
      git(repo, ["add", "scripts/record_confirmed_send.py"]);
      git(repo, ["commit", "-q", "-m", "reviewed command"]);
      const expectedCommit = git(repo, ["rev-parse", "HEAD"]);
      const expectedBlob = git(repo, [
        "rev-parse", `${expectedCommit}:scripts/record_confirmed_send.py`,
      ]);
      const expectedSha256 = createHash("sha256").update(reviewed).digest("hex");

      rmSync(workingPath);
      symlinkSync("/usr/bin/env", workingPath);
      const materialized = materializeReviewedConfirmedSendScript({
        repoPath: repo,
        runtimeRoot,
        expectedCommit,
        expectedBlob,
        expectedSha256,
      });
      try {
        expect(readFileSync(materialized.scriptPath, "utf8")).toBe(reviewed);
        expect(statSync(materialized.scriptPath).isFile()).toBe(true);
        expect(statSync(materialized.scriptPath).mode & 0o777).toBe(0o600);
        expect(statSync(materialized.runtimeDirectory).mode & 0o777).toBe(0o700);
        expect(materialized.scriptPath).not.toBe(workingPath);
      } finally {
        materialized.cleanup();
      }
      expect(existsSync(runtimeRoot) ? statSync(runtimeRoot).isDirectory() : true).toBe(true);
      expect(existsSync(materialized.runtimeDirectory)).toBe(false);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("pins the reviewed confirmed-send source that merged into jt-ops main", () => {
    // Derived from the merged jt-ops main tree, never pasted: the reviewed
    // suppression branch landed as 471e0d8 and `scripts/record_confirmed_send.py`
    // resolves there to blob d5d12ceb. A stale pin is the failure this catches --
    // the wrapper would otherwise materialize a superseded reviewed blob forever.
    expect(CONFIRMED_SEND_REVIEWED_SOURCE).toEqual({
      commit: "471e0d8cb0dbf7db8b01a235c8d26d7340328ce1",
      blobOid: "d5d12ceb0e95462c41ce7e528aa60e8bdadff8b2",
      blobSha256:
        "72c4a96b4fc0f8c86dba6357f79ac5b4d40fae236cb8b968e8719784479d0b3e",
      scriptPath: "scripts/record_confirmed_send.py",
    });
  });

  test("the reviewed confirmed-send pin is well formed and immutable", () => {
    expect(/^[0-9a-f]{40}$/.test(CONFIRMED_SEND_REVIEWED_SOURCE.commit)).toBe(true);
    expect(/^[0-9a-f]{40}$/.test(CONFIRMED_SEND_REVIEWED_SOURCE.blobOid)).toBe(true);
    expect(/^[0-9a-f]{64}$/.test(CONFIRMED_SEND_REVIEWED_SOURCE.blobSha256)).toBe(true);
    expect(Object.isFrozen(CONFIRMED_SEND_REVIEWED_SOURCE)).toBe(true);
    // The superseded pin must never come back.
    expect(CONFIRMED_SEND_REVIEWED_SOURCE.commit)
      .not.toBe("87c103d31614d9ec3d3585237a8a5721afbf9d56");
    expect(CONFIRMED_SEND_REVIEWED_SOURCE.blobOid)
      .not.toBe("46ba1cff18a8c721f96bf89e5a521980533aa062");
  });

  test("confirmed-send rejects stale commit/blob pairs before capability access", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-reviewed-command-reject-"));
    const repo = join(directory, "repo");
    try {
      mkdirSync(repo, { mode: 0o700 });
      git(repo, ["init", "-q"]);
      git(repo, ["config", "user.name", "Test"]);
      git(repo, ["config", "user.email", "test@example.invalid"]);
      mkdirSync(join(repo, "scripts"), { mode: 0o700 });
      writeFileSync(
        join(repo, "scripts", "record_confirmed_send.py"),
        "#!/usr/bin/env python3\nprint('reviewed')\n",
        { mode: 0o600 },
      );
      git(repo, ["add", "scripts/record_confirmed_send.py"]);
      git(repo, ["commit", "-q", "-m", "reviewed command"]);
      const expectedCommit = git(repo, ["rev-parse", "HEAD"]);
      const expectedSha256 = createHash("sha256")
        .update("#!/usr/bin/env python3\nprint('reviewed')\n")
        .digest("hex");
      expect(captureError(() => materializeReviewedConfirmedSendScript({
        repoPath: repo,
        runtimeRoot: join(directory, "runtime"),
        expectedCommit,
        expectedBlob: "0".repeat(40),
        expectedSha256,
      }))).toBe("fixed jt-ops command is unavailable");
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("confirmed-send rejects a correct blob whose SHA-256 disagrees", () => {
    // The Git object ID and the SHA-256 are two independent checks over the same
    // bytes. A pin that drifted on only one of them must still fail closed, and
    // it must fail before the runtime directory or any capability is touched.
    const directory = mkdtempSync(join(tmpdir(), "outreach-reviewed-sha-mismatch-"));
    const repo = join(directory, "repo");
    const runtimeRoot = join(directory, "runtime");
    try {
      mkdirSync(repo, { mode: 0o700 });
      git(repo, ["init", "-q"]);
      git(repo, ["config", "user.name", "Test"]);
      git(repo, ["config", "user.email", "test@example.invalid"]);
      mkdirSync(join(repo, "scripts"), { mode: 0o700 });
      const reviewed = "#!/usr/bin/env python3\nprint('reviewed')\n";
      writeFileSync(join(repo, "scripts", "record_confirmed_send.py"), reviewed, { mode: 0o600 });
      git(repo, ["add", "scripts/record_confirmed_send.py"]);
      git(repo, ["commit", "-q", "-m", "reviewed command"]);
      const expectedCommit = git(repo, ["rev-parse", "HEAD"]);
      const expectedBlob = git(repo, [
        "rev-parse", `${expectedCommit}:scripts/record_confirmed_send.py`,
      ]);

      expect(captureError(() => materializeReviewedConfirmedSendScript({
        repoPath: repo,
        runtimeRoot,
        expectedCommit,
        expectedBlob,
        expectedSha256: "0".repeat(64),
      }))).toBe("fixed jt-ops command is unavailable");
      // Nothing was materialized on the rejected path.
      expect(existsSync(runtimeRoot) ? readdirSync(runtimeRoot).length : 0).toBe(0);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("confirmed-send refuses a symlinked or group-readable private runtime root", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-reviewed-runtime-root-"));
    const repo = join(directory, "repo");
    try {
      mkdirSync(repo, { mode: 0o700 });
      git(repo, ["init", "-q"]);
      git(repo, ["config", "user.name", "Test"]);
      git(repo, ["config", "user.email", "test@example.invalid"]);
      mkdirSync(join(repo, "scripts"), { mode: 0o700 });
      const reviewed = "#!/usr/bin/env python3\nprint('reviewed')\n";
      writeFileSync(join(repo, "scripts", "record_confirmed_send.py"), reviewed, { mode: 0o600 });
      git(repo, ["add", "scripts/record_confirmed_send.py"]);
      git(repo, ["commit", "-q", "-m", "reviewed command"]);
      const expectedCommit = git(repo, ["rev-parse", "HEAD"]);
      const expectedBlob = git(repo, [
        "rev-parse", `${expectedCommit}:scripts/record_confirmed_send.py`,
      ]);
      const expectedSha256 = createHash("sha256").update(reviewed).digest("hex");

      // A runtime root that is a symlink is never trusted, however it resolves.
      const realRoot = join(directory, "real-root");
      mkdirSync(realRoot, { mode: 0o700 });
      const symlinkedRoot = join(directory, "symlinked-root");
      symlinkSync(realRoot, symlinkedRoot);
      expect(captureError(() => materializeReviewedConfirmedSendScript({
        repoPath: repo,
        runtimeRoot: symlinkedRoot,
        expectedCommit,
        expectedBlob,
        expectedSha256,
      }))).toBe("fixed jt-ops command is unavailable");
      expect(readdirSync(realRoot).length).toBe(0);

      // Nor is one any other account can read into.
      const openRoot = join(directory, "open-root");
      mkdirSync(openRoot, { mode: 0o700 });
      chmodSync(openRoot, 0o755);
      expect(captureError(() => materializeReviewedConfirmedSendScript({
        repoPath: repo,
        runtimeRoot: openRoot,
        expectedCommit,
        expectedBlob,
        expectedSha256,
      }))).toBe("fixed jt-ops command is unavailable");
      expect(readdirSync(openRoot).length).toBe(0);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("confirmed-send preflight requires a root-owned isolated standard-library Python", () => {
    const directory = mkdtempSync(join(tmpdir(), "outreach-confirmed-send-preflight-"));
    const python = join(directory, "python");
    try {
      executable(python, "#!/bin/sh\nexit 0\n");
      expect(captureError(() => validateConfirmedSendPreflight({
        pythonPath: join(directory, "missing-python"),
      }))).toBe("fixed jt-ops command is unavailable");
      expect(captureError(() => validateConfirmedSendPreflight({ pythonPath: python })))
        .toBe("fixed jt-ops command is unavailable");
      expect(validateConfirmedSendPreflight()).toBe(undefined);
    } finally {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  test("confirmed-send preflight proves isolated no-site stdlib without ambient environment", () => {
    let invocation: unknown;
    const fakeSpawn = ((file: string, args: string[], options: unknown) => {
      invocation = { file, args, options };
      return { status: 0, stdout: "", stderr: "" };
    }) as unknown as typeof spawnSync;
    validateConfirmedSendPreflight({ spawn: fakeSpawn });
    expect(invocation).toEqual({
      file: "/usr/bin/python3",
      args: [
        "-I", "-S", "-c",
        "import sys; assert sys.flags.isolated == 1 and sys.flags.no_site == 1",
      ],
      options: {
        cwd: "/private/var/empty",
        env: { LANG: "C.UTF-8", LC_ALL: "C.UTF-8", PYTHONHASHSEED: "0" },
        encoding: "utf8",
        stdio: ["ignore", "pipe", "pipe"],
        timeout: 5_000,
        killSignal: "SIGKILL",
      },
    });
  });

  test("confirmed-send output is exact and malformed child data cannot leak", () => {
    const receiptId = `pre_send_${"a".repeat(20)}`;
    const valid = {
      status: "RECORDED",
      preSendReceiptId: receiptId,
      sentEventId: `suppression_event_${"b".repeat(20)}`,
      ownerRevision: "c".repeat(64),
      observedAt: "2026-09-16T12:34:56Z",
    };
    expect(parseConfirmedSendResult(`${JSON.stringify(valid)}\n`, "", 0, receiptId))
      .toEqual(valid);
    const secret = "authority-read-secret-must-not-leak";
    for (const [stdout, stderr, status] of [
      [secret, "", 2],
      [`${JSON.stringify({ ...valid, extra: secret })}\n`, "", 0],
      [`${JSON.stringify(valid)}\n`, secret, 0],
    ] as const) {
      const message = captureError(() => parseConfirmedSendResult(stdout, stderr, status, receiptId));
      expect(message).toBe("confirmed-send owner failed");
      expect(message).not.toContain(secret);
    }
  });

  test("runtime CLI exposes one exact confirmed-send mode, never a generic secret runner", () => {
    const secret = "inherited-secret-must-not-leak";
    const result = spawnSync(
      "/opt/homebrew/opt/node@22/bin/node",
      [
        "scripts/outreach-runtime-secrets.mjs",
        "record-confirmed-send",
        "--pre-send-receipt-id",
        `pre_send_${"a".repeat(20)}`,
        "--",
        "/usr/bin/env",
      ],
      {
        encoding: "utf8",
        env: {
          ...process.env,
          OUTREACH_REVIEW_CAPABILITY: secret,
          OUTREACH_DECISION_CAPABILITY: secret,
          OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY: secret,
          HTTP_PROXY: `http://${secret}`,
        },
      },
    );
    expect(result.status).toBe(2);
    expect(result.stdout).toBe("");
    expect(`${result.stdout}${result.stderr}`).not.toContain(secret);
    expect(result.stderr).toBe("invalid confirmed-send request\n");
  });
});
