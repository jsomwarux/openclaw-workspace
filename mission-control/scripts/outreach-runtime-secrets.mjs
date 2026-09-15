#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync } from "node:fs";

const KEYCHAIN_HELPER = "./.runtime/outreach-keychain-helper";

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

export function buildRuntimeEnvironment(review, decision, login) {
  const values = [review, decision, login].map((value) =>
    typeof value === "string" ? value.trim() : "",
  );
  if (values.some((value) => !value) || values[0] === values[1]) {
    throw new Error("outreach capability configuration is invalid");
  }
  return {
    OUTREACH_REVIEW_CAPABILITY: values[0],
    OUTREACH_DECISION_CAPABILITY: values[1],
    OUTREACH_DECISION_JT_LOGIN: values[2],
  };
}

export function buildConvexEnvironmentChanges(review, decision) {
  const values = buildRuntimeEnvironment(review, decision, "local-runtime");
  return [
    { name: "OUTREACH_REVIEW_CAPABILITY", value: values.OUTREACH_REVIEW_CAPABILITY },
    { name: "OUTREACH_DECISION_CAPABILITY", value: values.OUTREACH_DECISION_CAPABILITY },
  ];
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
  if (!['review', 'decision'].includes(kind)) throw new Error("unknown capability kind");
  ensureKeychainHelper();
  const result = run(KEYCHAIN_HELPER, ["read", kind], { stdio: ["ignore", "pipe", "pipe"] });
  const value = result.stdout.trim();
  if (!value) throw new Error("stored capability is empty");
  return value;
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
  buildRuntimeEnvironment(read("review"), read("decision"), currentTailscaleLogin());
}

async function syncConvex() {
  const config = JSON.parse(readFileSync(new URL("../.convex/local/default/config.json", import.meta.url), "utf8"));
  if (typeof config.adminKey !== "string" || !config.adminKey || typeof config.ports?.cloud !== "number") {
    throw new Error("local Convex authority is unavailable");
  }
  const changes = buildConvexEnvironmentChanges(read("review"), read("decision"));
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
  const values = buildRuntimeEnvironment(read("review"), read("decision"), currentTailscaleLogin());
  const result = spawnSync(command[0], command.slice(1), {
    env: { ...process.env, ...values },
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
