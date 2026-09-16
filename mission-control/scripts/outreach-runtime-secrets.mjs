#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  chmodSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  renameSync,
  rmdirSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";

const KEYCHAIN_HELPER = "./.runtime/outreach-keychain-helper";
const KEYCHAIN_HELPER_SOURCE = "./scripts/outreach-keychain-helper.swift";
const KEYCHAIN_HELPER_PROTOCOL = "outreach-capabilities-v3";
const CAPABILITY_LOCK = "./.runtime/outreach-capability.lock";
export const AUTHORITY_VERIFIER_ACTOR_ID = "openclaw:review-verifier-v1";

export function buildKeychainHelperRequest(
  helperPath = KEYCHAIN_HELPER,
  compilerPath = "/usr/bin/swiftc",
) {
  return {
    file: compilerPath,
    args: [KEYCHAIN_HELPER_SOURCE, "-o", helperPath],
  };
}

function supportsCurrentKeychainHelper(helperPath) {
  if (!existsSync(helperPath)) return false;
  const result = spawnSync(helperPath, ["probe", KEYCHAIN_HELPER_PROTOCOL], {
    stdio: ["ignore", "ignore", "ignore"],
  });
  return result.status === 0;
}

function sourceDigest(sourcePath = KEYCHAIN_HELPER_SOURCE) {
  return createHash("sha256").update(readFileSync(sourcePath)).digest("hex");
}

function hasCurrentHelperSource(helperPath, digest) {
  const stampPath = `${helperPath}.sha256`;
  if (!supportsCurrentKeychainHelper(helperPath) || !existsSync(stampPath)) return false;
  return readFileSync(stampPath, "utf8").trim() === digest;
}

function ensurePrivateDirectory(path) {
  mkdirSync(path, { recursive: true, mode: 0o700 });
  chmodSync(path, 0o700);
}

function ensureKeychainHelperUnlocked(
  helperPath = KEYCHAIN_HELPER,
  compilerPath = "/usr/bin/swiftc",
) {
  const digest = sourceDigest();
  if (hasCurrentHelperSource(helperPath, digest)) return;
  const helperDirectory = dirname(helperPath);
  ensurePrivateDirectory(helperDirectory);
  const temporaryDirectory = mkdtempSync(join(helperDirectory, ".outreach-helper-"));
  chmodSync(temporaryDirectory, 0o700);
  const temporaryHelper = join(temporaryDirectory, "outreach-keychain-helper");
  const temporaryStamp = join(temporaryDirectory, "outreach-keychain-helper.sha256");
  try {
    const request = buildKeychainHelperRequest(temporaryHelper, compilerPath);
    run(request.file, request.args, { stdio: ["ignore", "ignore", "pipe"] });
    chmodSync(temporaryHelper, 0o700);
    if (!supportsCurrentKeychainHelper(temporaryHelper)) {
      throw new Error("secure capability helper protocol is unavailable");
    }
    writeFileSync(temporaryStamp, `${digest}\n`, { mode: 0o600 });
    chmodSync(temporaryStamp, 0o600);
    renameSync(temporaryHelper, helperPath);
    renameSync(temporaryStamp, `${helperPath}.sha256`);
  } finally {
    rmSync(temporaryDirectory, { recursive: true, force: true });
  }
}

function assertOwnerOnlyLock(lockPath) {
  const status = statSync(lockPath);
  const currentUid = typeof process.getuid === "function" ? process.getuid() : status.uid;
  if (!status.isDirectory() || status.uid !== currentUid || (status.mode & 0o777) !== 0o700) {
    throw new Error("capability runtime lock is insecure");
  }
}

function acquireOwnerOnlyLock(lockPath, timeoutMs = 10_000) {
  ensurePrivateDirectory(dirname(lockPath));
  const deadline = Date.now() + timeoutMs;
  while (true) {
    try {
      mkdirSync(lockPath, { mode: 0o700 });
      chmodSync(lockPath, 0o700);
      assertOwnerOnlyLock(lockPath);
      return;
    } catch (error) {
      if (error?.code !== "EEXIST") throw error;
      try {
        assertOwnerOnlyLock(lockPath);
      } catch (lockError) {
        if (lockError?.code === "ENOENT") continue;
        throw lockError;
      }
      if (Date.now() >= deadline) throw new Error("capability runtime lock timed out");
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 20);
    }
  }
}

export function withOwnerOnlyLock(lockPath, operation) {
  acquireOwnerOnlyLock(lockPath);
  try {
    return operation();
  } finally {
    rmdirSync(lockPath);
  }
}

async function withOwnerOnlyLockAsync(lockPath, operation) {
  acquireOwnerOnlyLock(lockPath);
  try {
    return await operation();
  } finally {
    rmdirSync(lockPath);
  }
}

export function ensureKeychainHelper(
  helperPath = KEYCHAIN_HELPER,
  compilerPath = "/usr/bin/swiftc",
) {
  return withOwnerOnlyLock(`${helperPath}.lock`, () => {
    ensureKeychainHelperUnlocked(helperPath, compilerPath);
  });
}

export function buildInstallerRequest() {
  return { args: ["install-set"], input: undefined };
}

export function buildRuntimeEnvironment(review, decision, login, authorityWrite, authorityRead) {
  const values = [review, decision, login, authorityWrite, authorityRead].map((value) =>
    typeof value === "string" ? value.trim() : "",
  );
  const baseValues = values.slice(0, 3);
  const authorityValues = values.slice(3);
  const authorityPresence = [authorityWrite, authorityRead].map((value) => value !== undefined);
  const hasCompleteAuthorityPair = authorityPresence.every(Boolean) && authorityValues.every(Boolean);
  const hasInvalidAuthorityPair = authorityPresence.some(Boolean) && !hasCompleteAuthorityPair;
  const capabilities = hasCompleteAuthorityPair
    ? [values[0], values[1], values[3], values[4]]
    : [values[0], values[1]];
  if (
    baseValues.some((value) => !value)
    || hasInvalidAuthorityPair
    || new Set(capabilities).size !== capabilities.length
  ) {
    throw new Error("outreach capability configuration is invalid");
  }
  const environment = {
    OUTREACH_REVIEW_CAPABILITY: values[0],
    OUTREACH_DECISION_CAPABILITY: values[1],
    OUTREACH_DECISION_JT_LOGIN: values[2],
  };
  if (!hasCompleteAuthorityPair) return environment;
  return {
    ...environment,
    OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY: values[3],
    OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY: values[4],
    OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID: AUTHORITY_VERIFIER_ACTOR_ID,
  };
}

export function buildConvexEnvironmentChanges(review, decision, authorityWrite, authorityRead) {
  const values = buildRuntimeEnvironment(
    review, decision, "local-runtime", authorityWrite, authorityRead,
  );
  const changes = [
    { name: "OUTREACH_REVIEW_CAPABILITY", value: values.OUTREACH_REVIEW_CAPABILITY },
    { name: "OUTREACH_DECISION_CAPABILITY", value: values.OUTREACH_DECISION_CAPABILITY },
  ];
  if ("OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY" in values) {
    changes.push(
      {
        name: "OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY",
        value: values.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
      },
      {
        name: "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY",
        value: values.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
      },
      {
        name: "OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID",
        value: values.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID,
      },
    );
  } else {
    changes.push(
      { name: "OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY" },
      { name: "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY" },
      { name: "OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID" },
    );
  }
  return changes;
}

export function buildServiceProcessEnvironment(baseEnvironment, runtimeEnvironment) {
  const environment = { ...baseEnvironment };
  delete environment.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY;
  delete environment.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY;
  delete environment.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID;
  return { ...environment, ...runtimeEnvironment };
}

export function resolveTailscaleLogin(status) {
  const userId = String(status?.Self?.UserID ?? "");
  const login = status?.User?.[userId]?.LoginName;
  if (typeof login !== "string" || !login.trim()) {
    throw new Error("trusted Tailscale login could not be resolved");
  }
  return login.trim();
}

function run(file, args, options = {}) {
  const result = spawnSync(file, args, {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
    ...options,
  });
  if (result.status !== 0) {
    throw new Error("secure capability operation failed");
  }
  return result;
}

function readLegacyCapability(helperPath, kind) {
  if (!['review', 'decision'].includes(kind)) throw new Error("unknown capability kind");
  const result = run(helperPath, ["read", kind], { stdio: ["ignore", "pipe", "pipe"] });
  const value = result.stdout.trim();
  if (!value) throw new Error("stored capability is empty");
  return value;
}

function validateCapabilitySet(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("outreach capability configuration is invalid");
  }
  const expected = [
    "decision",
    "review",
    "reviewAuthorityRead",
    "reviewAuthorityWrite",
    "version",
  ];
  const actual = Object.keys(value).sort();
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) {
    throw new Error("outreach capability configuration is invalid");
  }
  if (value.version !== 1) throw new Error("outreach capability configuration is invalid");
  const environment = buildRuntimeEnvironment(
    value.review,
    value.decision,
    "local-runtime",
    value.reviewAuthorityWrite,
    value.reviewAuthorityRead,
  );
  return {
    review: environment.OUTREACH_REVIEW_CAPABILITY,
    decision: environment.OUTREACH_DECISION_CAPABILITY,
    authorityWrite: environment.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
    authorityRead: environment.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
  };
}

export function parseCapabilitySetRead(result) {
  if (result.status === 3) return undefined;
  if (result.status !== 0) throw new Error("secure capability operation failed");
  try {
    return validateCapabilitySet(JSON.parse(result.stdout));
  } catch (error) {
    if (error instanceof Error && error.message === "outreach capability configuration is invalid") {
      throw error;
    }
    throw new Error("outreach capability configuration is invalid");
  }
}

export function readCapabilitySetFromHelper(helperPath) {
  const result = spawnSync(helperPath, ["read-set"], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
  });
  const capabilitySet = parseCapabilitySetRead(result);
  if (capabilitySet) return capabilitySet;
  return {
    review: readLegacyCapability(helperPath, "review"),
    decision: readLegacyCapability(helperPath, "decision"),
    authorityWrite: undefined,
    authorityRead: undefined,
  };
}

export function installCapabilitySetFromHelper(helperPath) {
  const request = buildInstallerRequest();
  run(helperPath, request.args, { stdio: ["ignore", "ignore", "pipe"] });
  const capabilitySet = readCapabilitySetFromHelper(helperPath);
  if (!capabilitySet.authorityWrite || !capabilitySet.authorityRead) {
    throw new Error("outreach capability configuration is invalid");
  }
  return capabilitySet;
}

function lockedCapabilitySet() {
  return withOwnerOnlyLock(CAPABILITY_LOCK, () => {
    ensureKeychainHelperUnlocked();
    return readCapabilitySetFromHelper(KEYCHAIN_HELPER);
  });
}

function currentTailscaleLogin() {
  const result = run("/opt/homebrew/bin/tailscale", ["status", "--json"], {
    stdio: ["ignore", "pipe", "pipe"],
  });
  return resolveTailscaleLogin(JSON.parse(result.stdout));
}

function install() {
  return withOwnerOnlyLock(CAPABILITY_LOCK, () => {
    ensureKeychainHelperUnlocked();
    const values = installCapabilitySetFromHelper(KEYCHAIN_HELPER);
    buildRuntimeEnvironment(
      values.review,
      values.decision,
      currentTailscaleLogin(),
      values.authorityWrite,
      values.authorityRead,
    );
  });
}

async function syncConvex() {
  return withOwnerOnlyLockAsync(CAPABILITY_LOCK, async () => {
    ensureKeychainHelperUnlocked();
    const config = JSON.parse(readFileSync(new URL("../.convex/local/default/config.json", import.meta.url), "utf8"));
    if (typeof config.adminKey !== "string" || !config.adminKey || typeof config.ports?.cloud !== "number") {
      throw new Error("local Convex authority is unavailable");
    }
    const values = readCapabilitySetFromHelper(KEYCHAIN_HELPER);
    const changes = buildConvexEnvironmentChanges(
      values.review,
      values.decision,
      values.authorityWrite,
      values.authorityRead,
    );
    const response = await fetch(`http://127.0.0.1:${config.ports.cloud}/api/update_environment_variables`, {
      method: "POST",
      headers: {
        authorization: `Convex ${config.adminKey}`,
        "content-type": "application/json",
        "convex-client": "mission-control-secure-config-v1",
      },
      body: JSON.stringify({ changes }),
    });
    if (!response.ok) throw new Error("local Convex capability sync failed");
  });
}

function runWithSecrets(command) {
  if (!command.length) throw new Error("missing service command");
  const capabilities = lockedCapabilitySet();
  const values = buildRuntimeEnvironment(
    capabilities.review,
    capabilities.decision,
    currentTailscaleLogin(),
    capabilities.authorityWrite,
    capabilities.authorityRead,
  );
  const result = spawnSync(command[0], command.slice(1), {
    env: buildServiceProcessEnvironment(process.env, values),
    stdio: "inherit",
  });
  process.exit(result.status ?? 1);
}

const [mode, separator, ...command] = process.argv.slice(2);
if (import.meta.main) {
  try {
    if (mode === "install") install();
    else if (mode === "sync-convex") await syncConvex();
    else if (["run-next", "run-convex"].includes(mode) && separator === "--") runWithSecrets(command);
    else throw new Error("unsupported secure capability operation");
  } catch (error) {
    console.error(error instanceof Error ? error.message : "secure capability operation failed");
    process.exit(2);
  }
}
