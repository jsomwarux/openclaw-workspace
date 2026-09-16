#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  chmodSync,
  closeSync,
  existsSync,
  fstatSync,
  mkdirSync,
  mkdtempSync,
  openSync,
  readFileSync,
  renameSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";

const LEGACY_KEYCHAIN_HELPER = "./.runtime/outreach-keychain-helper";
const V3_KEYCHAIN_HELPER = "./.runtime/outreach-keychain-helper-v3";
const KEYCHAIN_HELPER_SOURCE = "./scripts/outreach-keychain-helper.swift";
const KEYCHAIN_HELPER_PROTOCOL = "outreach-capabilities-v3";
const CAPABILITY_LOCK = "./.runtime/outreach-capability.lock";
const HELPER_TIMEOUT_MS = 5_000;
const COMPILE_TIMEOUT_MS = 30_000;
const LOCKED_OPERATION_TIMEOUT_MS = 30_000;
const CONVEX_SYNC_TIMEOUT_MS = 10_000;
const LOCKED_FLAG = "--outreach-lock-held";
const LOCKED_ENV = "OUTREACH_LOCKF_INTERNAL";
const PRIVATE_PIPE_PREAMBLE = "outreach-runtime-environment-v1\n";
export const AUTHORITY_VERIFIER_ACTOR_ID = "openclaw:review-verifier-v1";

export function buildKeychainHelperRequest(
  helperPath = V3_KEYCHAIN_HELPER,
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
    timeout: HELPER_TIMEOUT_MS,
    killSignal: "SIGKILL",
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

export function ensureV3KeychainHelper(
  helperPath = V3_KEYCHAIN_HELPER,
  compilerPath = "/usr/bin/swiftc",
  { rename = renameSync } = {},
) {
  const digest = sourceDigest();
  if (existsSync(helperPath)) {
    if (!hasCurrentHelperSource(helperPath, digest)) {
      throw new Error("v3 capability helper mismatch; explicit versioned migration required");
    }
    return;
  }
  const helperDirectory = dirname(helperPath);
  ensurePrivateDirectory(helperDirectory);
  const temporaryDirectory = mkdtempSync(join(helperDirectory, ".outreach-helper-"));
  chmodSync(temporaryDirectory, 0o700);
  const temporaryHelper = join(temporaryDirectory, "outreach-keychain-helper");
  const temporaryStamp = join(temporaryDirectory, "outreach-keychain-helper.sha256");
  try {
    const request = buildKeychainHelperRequest(temporaryHelper, compilerPath);
    run(request.file, request.args, {
      stdio: ["ignore", "ignore", "pipe"],
      timeout: COMPILE_TIMEOUT_MS,
    });
    chmodSync(temporaryHelper, 0o700);
    if (!supportsCurrentKeychainHelper(temporaryHelper)) {
      throw new Error("secure capability helper protocol is unavailable");
    }
    writeFileSync(temporaryStamp, `${digest}\n`, { mode: 0o600 });
    chmodSync(temporaryStamp, 0o600);
    rename(temporaryStamp, `${helperPath}.sha256`);
    rename(temporaryHelper, helperPath);
  } finally {
    rmSync(temporaryDirectory, { recursive: true, force: true });
  }
}

function ensureAdvisoryLockFile(lockPath = CAPABILITY_LOCK) {
  ensurePrivateDirectory(dirname(lockPath));
  const descriptor = openSync(lockPath, "a", 0o600);
  closeSync(descriptor);
  chmodSync(lockPath, 0o600);
}

export function buildLockedReexecRequest(
  operationArgs,
  {
    lockPath = CAPABILITY_LOCK,
    nodePath = process.execPath,
    scriptPath = process.argv[1] ?? "scripts/outreach-runtime-secrets.mjs",
  } = {},
) {
  return {
    file: "/usr/bin/lockf",
    args: ["-t", "10", lockPath, nodePath, scriptPath, LOCKED_FLAG, ...operationArgs],
  };
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
    timeout: HELPER_TIMEOUT_MS,
    killSignal: "SIGKILL",
    ...options,
  });
  if (result.error?.code === "ETIMEDOUT") {
    throw new Error("secure capability operation timed out");
  }
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

function readV3CapabilitySet(helperPath, timeout = HELPER_TIMEOUT_MS) {
  const result = spawnSync(helperPath, ["read-set"], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
    timeout,
    killSignal: "SIGKILL",
  });
  if (result.error?.code === "ETIMEDOUT") {
    throw new Error("secure capability operation timed out");
  }
  return parseCapabilitySetRead(result);
}

export function readCapabilitySetFromHelpers(
  v3HelperPath,
  legacyHelperPath,
  timeout = HELPER_TIMEOUT_MS,
) {
  const capabilitySet = readV3CapabilitySet(v3HelperPath, timeout);
  if (capabilitySet) return capabilitySet;
  return {
    review: readLegacyCapability(legacyHelperPath, "review"),
    decision: readLegacyCapability(legacyHelperPath, "decision"),
    authorityWrite: undefined,
    authorityRead: undefined,
  };
}

export function installCapabilitySetFromHelper(helperPath) {
  const request = buildInstallerRequest();
  run(helperPath, request.args, { stdio: ["ignore", "ignore", "pipe"] });
  const capabilitySet = readV3CapabilitySet(helperPath);
  if (!capabilitySet?.authorityWrite || !capabilitySet.authorityRead) {
    throw new Error("outreach capability configuration is invalid");
  }
  return capabilitySet;
}

function currentTailscaleLogin() {
  const result = run("/opt/homebrew/bin/tailscale", ["status", "--json"], {
    stdio: ["ignore", "pipe", "pipe"],
  });
  return resolveTailscaleLogin(JSON.parse(result.stdout));
}

function readRuntimeEnvironment() {
  ensureV3KeychainHelper();
  const values = readCapabilitySetFromHelpers(V3_KEYCHAIN_HELPER, LEGACY_KEYCHAIN_HELPER);
  return buildRuntimeEnvironment(
    values.review,
    values.decision,
    currentTailscaleLogin(),
    values.authorityWrite,
    values.authorityRead,
  );
}

function install() {
  ensureV3KeychainHelper();
  const values = installCapabilitySetFromHelper(V3_KEYCHAIN_HELPER);
  buildRuntimeEnvironment(
    values.review,
    values.decision,
    currentTailscaleLogin(),
    values.authorityWrite,
    values.authorityRead,
  );
}

async function syncConvex() {
  ensureV3KeychainHelper();
  const config = JSON.parse(readFileSync(new URL("../.convex/local/default/config.json", import.meta.url), "utf8"));
  if (typeof config.adminKey !== "string" || !config.adminKey || typeof config.ports?.cloud !== "number") {
    throw new Error("local Convex authority is unavailable");
  }
  const values = readCapabilitySetFromHelpers(V3_KEYCHAIN_HELPER, LEGACY_KEYCHAIN_HELPER);
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
    signal: AbortSignal.timeout(CONVEX_SYNC_TIMEOUT_MS),
  });
  if (!response.ok) throw new Error("local Convex capability sync failed");
}

function runService(command, values) {
  if (!command.length) throw new Error("missing service command");
  const result = spawnSync(command[0], command.slice(1), {
    env: buildServiceProcessEnvironment(process.env, values),
    stdio: "inherit",
  });
  process.exit(result.status ?? 1);
}

function runLockedReexec(operationArgs, captureOutput = false) {
  ensureAdvisoryLockFile();
  const request = buildLockedReexecRequest(operationArgs);
  const result = spawnSync(request.file, request.args, {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
    env: { ...process.env, [LOCKED_ENV]: "1" },
    stdio: captureOutput ? ["ignore", "pipe", "pipe", "pipe"] : "inherit",
    timeout: LOCKED_OPERATION_TIMEOUT_MS,
    killSignal: "SIGKILL",
  });
  if (result.error?.code === "ETIMEDOUT") throw new Error("capability lock operation timed out");
  if (result.status !== 0) throw new Error("secure capability operation failed");
  return captureOutput ? result.output[3] : result.stdout;
}

function sameFileIdentity(left, right) {
  return left.dev === right.dev && left.ino === right.ino;
}

export function validatePrivateCapabilityPipe(descriptor = 3) {
  try {
    const channel = fstatSync(descriptor);
    const stdout = fstatSync(1);
    const stderr = fstatSync(2);
    if (
      !(channel.isFIFO() || channel.isSocket())
      || sameFileIdentity(channel, stdout)
      || sameFileIdentity(channel, stderr)
    ) {
      throw new Error("invalid private capability pipe");
    }
  } catch {
    throw new Error("private capability pipe required");
  }
}

function requirePrivateCapabilityPipe(descriptor = 3) {
  validatePrivateCapabilityPipe(descriptor);
  try {
    writeFileSync(descriptor, PRIVATE_PIPE_PREAMBLE);
  } catch {
    throw new Error("private capability pipe required");
  }
}

function writeRuntimeEnvironmentToPrivatePipe(values, descriptor = 3) {
  writeFileSync(descriptor, JSON.stringify(values));
}

const cliArgs = process.argv.slice(2);
if (import.meta.main) {
  try {
    if (cliArgs[0] === LOCKED_FLAG) {
      if (process.env[LOCKED_ENV] !== "1") throw new Error("locked capability operation required");
      const [mode] = cliArgs.slice(1);
      if (mode === "install") install();
      else if (mode === "sync-convex") await syncConvex();
      else if (mode === "emit-runtime-environment") {
        requirePrivateCapabilityPipe();
        writeRuntimeEnvironmentToPrivatePipe(readRuntimeEnvironment());
      } else throw new Error("unsupported secure capability operation");
    } else {
      const [mode, separator, ...command] = cliArgs;
      if (["install", "sync-convex"].includes(mode)) {
        runLockedReexec([mode]);
      } else if (["run-next", "run-convex"].includes(mode) && separator === "--") {
        const payload = runLockedReexec(["emit-runtime-environment"], true);
        if (!payload?.startsWith(PRIVATE_PIPE_PREAMBLE)) {
          throw new Error("secure capability operation failed");
        }
        const values = JSON.parse(payload.slice(PRIVATE_PIPE_PREAMBLE.length));
        runService(command, values);
      } else throw new Error("unsupported secure capability operation");
    }
  } catch (error) {
    console.error(error instanceof Error ? error.message : "secure capability operation failed");
    process.exit(2);
  }
}
