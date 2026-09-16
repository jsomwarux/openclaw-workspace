#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync } from "node:fs";

const KEYCHAIN_HELPER = "./.runtime/outreach-keychain-helper";
export const AUTHORITY_VERIFIER_ACTOR_ID = "openclaw:review-verifier-v1";

export function buildKeychainHelperRequest() {
  return {
    file: "/usr/bin/swiftc",
    args: ["./scripts/outreach-keychain-helper.swift", "-o", KEYCHAIN_HELPER],
  };
}

function ensureKeychainHelper() {
  if (existsSync(KEYCHAIN_HELPER)) return;
  mkdirSync("./.runtime", { recursive: true });
  const request = buildKeychainHelperRequest();
  run(request.file, request.args, { stdio: ["ignore", "ignore", "pipe"] });
}

export function buildInstallerRequest() {
  return { args: ["install"], input: undefined };
}

export function buildRuntimeEnvironment(review, decision, login, authorityWrite, authorityRead) {
  const values = [review, decision, login, authorityWrite, authorityRead].map((value) =>
    typeof value === "string" ? value.trim() : "",
  );
  const baseValues = values.slice(0, 3);
  const authorityValues = values.slice(3);
  const hasCompleteAuthorityPair = authorityValues.every(Boolean);
  const hasPartialAuthorityPair = authorityValues.some(Boolean) && !hasCompleteAuthorityPair;
  const capabilities = hasCompleteAuthorityPair
    ? [values[0], values[1], values[3], values[4]]
    : [values[0], values[1]];
  if (
    baseValues.some((value) => !value)
    || hasPartialAuthorityPair
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
    throw new Error(`secure capability operation failed: ${file}`);
  }
  return result;
}

function read(kind) {
  if (!['review', 'decision', 'review-authority-write', 'review-authority-read'].includes(kind)) {
    throw new Error("unknown capability kind");
  }
  ensureKeychainHelper();
  const result = run(KEYCHAIN_HELPER, ["read", kind], { stdio: ["ignore", "pipe", "pipe"] });
  const value = result.stdout.trim();
  if (!value) throw new Error("stored capability is empty");
  return value;
}

function readOptional(kind) {
  if (!['review-authority-write', 'review-authority-read'].includes(kind)) {
    throw new Error("unknown optional capability kind");
  }
  ensureKeychainHelper();
  const result = run(KEYCHAIN_HELPER, ["read-optional", kind], {
    stdio: ["ignore", "pipe", "pipe"],
  });
  return result.stdout.trim() || undefined;
}

function readCapabilitySet() {
  return {
    review: read("review"),
    decision: read("decision"),
    authorityWrite: readOptional("review-authority-write"),
    authorityRead: readOptional("review-authority-read"),
  };
}

function currentTailscaleLogin() {
  const result = run("/opt/homebrew/bin/tailscale", ["status", "--json"], {
    stdio: ["ignore", "pipe", "pipe"],
  });
  return resolveTailscaleLogin(JSON.parse(result.stdout));
}

function install() {
  ensureKeychainHelper();
  const request = buildInstallerRequest();
  run(KEYCHAIN_HELPER, request.args, { stdio: ["ignore", "ignore", "pipe"] });
  const values = readCapabilitySet();
  buildRuntimeEnvironment(
    values.review,
    values.decision,
    currentTailscaleLogin(),
    values.authorityWrite,
    values.authorityRead,
  );
}

async function syncConvex() {
  const config = JSON.parse(readFileSync(new URL("../.convex/local/default/config.json", import.meta.url), "utf8"));
  if (typeof config.adminKey !== "string" || !config.adminKey || typeof config.ports?.cloud !== "number") {
    throw new Error("local Convex authority is unavailable");
  }
  const values = readCapabilitySet();
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
}

function runWithSecrets(command) {
  if (!command.length) throw new Error("missing service command");
  const capabilities = readCapabilitySet();
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
