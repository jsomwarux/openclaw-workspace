#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  accessSync,
  chmodSync,
  closeSync,
  constants as fsConstants,
  existsSync,
  fstatSync,
  mkdirSync,
  mkdtempSync,
  openSync,
  readFileSync,
  renameSync,
  rmSync,
  statSync,
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
const AUTHORITY_READER_PIPE_PREAMBLE = "outreach-review-authority-reader-v1\n";
const JT_OPS_ROOT = "/Users/jtsomwaru/Desktop/jt-ops";
const JT_OPS_PYTHON = "/Users/jtsomwaru/Desktop/jt-ops/.venv/bin/python";
const JT_OPS_SCRIPT = "/Users/jtsomwaru/Desktop/jt-ops/scripts/cohort_two_authority.py";
const CONFIRMED_SEND_TIMEOUT_MS = 20_000;
const PREFLIGHT_TIMEOUT_MS = 5_000;
const PRE_SEND_RECEIPT_ID = /^pre_send_[0-9a-f]{20}$/;
const SENT_EVENT_ID = /^suppression_event_[0-9a-f]{20}$/;
const HEX_64 = /^[0-9a-f]{64}$/;
const UTC_SECONDS = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
export const AUTHORITY_VERIFIER_ACTOR_ID = "openclaw:review-verifier-v1";

export function buildReviewAuthorityReaderEnvironment(authorityRead) {
  const value = typeof authorityRead === "string" ? authorityRead.trim() : "";
  if (!value) throw new Error("review-authority reader is unavailable");
  return {
    LANG: "C.UTF-8",
    LC_ALL: "C.UTF-8",
    PYTHONHASHSEED: "0",
    OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY: value,
  };
}

function validatePreSendReceiptId(value) {
  if (typeof value !== "string" || !PRE_SEND_RECEIPT_ID.test(value)) {
    throw new Error("invalid confirmed-send request");
  }
  return value;
}

export function buildConfirmedSendRequest(preSendReceiptId, authorityRead) {
  const receiptId = validatePreSendReceiptId(preSendReceiptId);
  return {
    file: JT_OPS_PYTHON,
    args: [
      JT_OPS_SCRIPT,
      "record-confirmed-send",
      "--pre-send-receipt-id",
      receiptId,
    ],
    cwd: JT_OPS_ROOT,
    env: buildReviewAuthorityReaderEnvironment(authorityRead),
  };
}

export function validateConfirmedSendPreflight({
  pythonPath = JT_OPS_PYTHON,
  scriptPath = JT_OPS_SCRIPT,
  cwd = JT_OPS_ROOT,
  spawn = spawnSync,
} = {}) {
  try {
    if (!statSync(cwd).isDirectory() || !statSync(scriptPath).isFile()) {
      throw new Error("invalid fixed path");
    }
    accessSync(pythonPath, fsConstants.X_OK);
    accessSync(scriptPath, fsConstants.R_OK);
    const result = spawn(pythonPath, ["-c", "import jsonschema"], {
      cwd,
      env: { LANG: "C.UTF-8", LC_ALL: "C.UTF-8", PYTHONHASHSEED: "0" },
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      timeout: PREFLIGHT_TIMEOUT_MS,
      killSignal: "SIGKILL",
    });
    if (result.error || result.status !== 0 || result.stdout || result.stderr) {
      throw new Error("invalid fixed runtime");
    }
  } catch {
    throw new Error("fixed jt-ops command is unavailable");
  }
}

export function parseConfirmedSendResult(stdout, stderr, status, preSendReceiptId) {
  try {
    if (status !== 0 || stderr || typeof stdout !== "string" || stdout.split("\n").length !== 2 || !stdout.endsWith("\n")) {
      throw new Error("invalid child result");
    }
    const value = JSON.parse(stdout);
    const keys = ["observedAt", "ownerRevision", "preSendReceiptId", "sentEventId", "status"];
    if (
      !value || typeof value !== "object" || Array.isArray(value)
      || Object.keys(value).sort().some((key, index) => key !== keys[index])
      || Object.keys(value).length !== keys.length
      || value.status !== "RECORDED"
      || value.preSendReceiptId !== preSendReceiptId
      || typeof value.sentEventId !== "string" || !SENT_EVENT_ID.test(value.sentEventId)
      || typeof value.ownerRevision !== "string" || !HEX_64.test(value.ownerRevision)
      || typeof value.observedAt !== "string" || !UTC_SECONDS.test(value.observedAt)
    ) {
      throw new Error("invalid child result");
    }
    return value;
  } catch {
    throw new Error("confirmed-send owner failed");
  }
}

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
  changes.push({ name: "OUTREACH_SUPPRESSION_OWNER_ENABLED" });
  return changes;
}

export function buildServiceProcessEnvironment(baseEnvironment, runtimeEnvironment) {
  const environment = { ...baseEnvironment };
  delete environment.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY;
  delete environment.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY;
  delete environment.OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID;
  delete environment.OUTREACH_SUPPRESSION_OWNER_ENABLED;
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

function readReviewAuthorityReaderEnvironment() {
  ensureV3KeychainHelper();
  const values = readCapabilitySetFromHelpers(V3_KEYCHAIN_HELPER, LEGACY_KEYCHAIN_HELPER);
  return buildReviewAuthorityReaderEnvironment(values.authorityRead);
}

export function installCapabilitySet({
  ensureHelper = ensureV3KeychainHelper,
  resolveLogin = currentTailscaleLogin,
  storeSet = () => installCapabilitySetFromHelper(V3_KEYCHAIN_HELPER),
} = {}) {
  ensureHelper();
  const login = resolveLogin();
  if (typeof login !== "string" || !login.trim()) {
    throw new Error("trusted Tailscale login could not be resolved");
  }
  // This must be the terminal operation. Once the atomic Keychain item update
  // succeeds there is no readback, sync, or other fallible work that can turn
  // a completed rotation into a reported failure.
  storeSet();
}

function install() {
  installCapabilitySet();
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

function requirePrivateCapabilityPipe(descriptor = 3, preamble = PRIVATE_PIPE_PREAMBLE) {
  validatePrivateCapabilityPipe(descriptor);
  try {
    writeFileSync(descriptor, preamble);
  } catch {
    throw new Error("private capability pipe required");
  }
}

function writeRuntimeEnvironmentToPrivatePipe(values, descriptor = 3) {
  writeFileSync(descriptor, JSON.stringify(values));
}

function writeReviewAuthorityReaderEnvironmentToPrivatePipe(descriptor = 3) {
  requirePrivateCapabilityPipe(descriptor, AUTHORITY_READER_PIPE_PREAMBLE);
  writeFileSync(descriptor, JSON.stringify(readReviewAuthorityReaderEnvironment()));
}

function parseReviewAuthorityReaderPayload(payload) {
  try {
    if (!payload?.startsWith(AUTHORITY_READER_PIPE_PREAMBLE)) {
      throw new Error("invalid private payload");
    }
    const value = JSON.parse(payload.slice(AUTHORITY_READER_PIPE_PREAMBLE.length));
    const expected = [
      "LANG", "LC_ALL", "OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY", "PYTHONHASHSEED",
    ];
    if (
      !value || typeof value !== "object" || Array.isArray(value)
      || Object.keys(value).sort().some((key, index) => key !== expected[index])
      || Object.keys(value).length !== expected.length
      || typeof value.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY !== "string"
    ) {
      throw new Error("invalid private payload");
    }
    return buildReviewAuthorityReaderEnvironment(
      value.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
    );
  } catch {
    throw new Error("secure capability operation failed");
  }
}

function runConfirmedSend(preSendReceiptId) {
  const receiptId = validatePreSendReceiptId(preSendReceiptId);
  validateConfirmedSendPreflight();
  const payload = runLockedReexec(["emit-review-authority-reader-environment"], true);
  const environment = parseReviewAuthorityReaderPayload(payload);
  const request = buildConfirmedSendRequest(
    receiptId,
    environment.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
  );
  const result = spawnSync(request.file, request.args, {
    cwd: request.cwd,
    env: request.env,
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
    timeout: CONFIRMED_SEND_TIMEOUT_MS,
    killSignal: "SIGKILL",
  });
  if (result.error) throw new Error("confirmed-send owner failed");
  const value = parseConfirmedSendResult(
    result.stdout,
    result.stderr,
    result.status,
    receiptId,
  );
  process.stdout.write(`${JSON.stringify(value)}\n`);
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
      } else if (mode === "emit-review-authority-reader-environment") {
        writeReviewAuthorityReaderEnvironmentToPrivatePipe();
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
      } else if (mode === "record-confirmed-send") {
        if (separator !== "--pre-send-receipt-id" || command.length !== 1) {
          throw new Error("invalid confirmed-send request");
        }
        runConfirmedSend(command[0]);
      } else throw new Error("unsupported secure capability operation");
    }
  } catch (error) {
    console.error(error instanceof Error ? error.message : "secure capability operation failed");
    process.exit(2);
  }
}
