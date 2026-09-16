import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { canonicalJson, hashCanonicalJson } from "./canonical-json";
import { validateSuppressionBindingHash, type SuppressionBinding } from "./outreach-suppression-binding";

export type ProtectedGitRequest = { repository: string; commitSha: string; path: string };
export type ProtectedGitResult = { bytes: Uint8Array; blobOid: string };
export type ProtectedGitReader = (request: ProtectedGitRequest) => Promise<ProtectedGitResult>;

export class ProtectedGitBindingMismatchError extends Error {
  constructor() { super("protected suppression binding mismatch"); }
}
export class ProtectedGitDependencyError extends Error {
  constructor() { super("protected Git authority unavailable"); }
}

const PROTECTED_REPOSITORY = "jsomwarux/jt-ops";
const PROTECTED_ORIGIN = "git@github.com:jsomwarux/jt-ops.git";
const GIT_TIMEOUT_MS = 15_000;
const MAX_BLOB_BYTES = 2 * 1024 * 1024;
function gitEnvironment(): NodeJS.ProcessEnv {
  const home = process.env.HOME?.trim();
  const agent = process.env.SSH_AUTH_SOCK?.trim();
  if (!home || !agent) throw new ProtectedGitDependencyError();
  return {
    PATH: "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin",
    NODE_ENV: "production",
    HOME: home,
    SSH_AUTH_SOCK: agent,
    GIT_CONFIG_NOSYSTEM: "1",
    GIT_CONFIG_GLOBAL: "/dev/null",
    GIT_TERMINAL_PROMPT: "0",
  };
}

function git(cwd: string, args: string[], encoding: "utf8" | "buffer" = "utf8", mismatch = false) {
  const result = spawnSync("git", args, {
    cwd,
    encoding: encoding === "utf8" ? "utf8" : null,
    timeout: GIT_TIMEOUT_MS,
    maxBuffer: MAX_BLOB_BYTES,
    env: gitEnvironment(),
  });
  if (result.error) throw new ProtectedGitDependencyError();
  if (result.status !== 0) throw mismatch ? new ProtectedGitBindingMismatchError() : new ProtectedGitDependencyError();
  return result.stdout;
}

export async function readProtectedGitFile(request: ProtectedGitRequest): Promise<ProtectedGitResult> {
  if (request.repository !== PROTECTED_REPOSITORY) throw new ProtectedGitBindingMismatchError();
  const remote = spawnSync("git", ["ls-remote", PROTECTED_ORIGIN, "refs/heads/main"], {
    encoding: "utf8", timeout: GIT_TIMEOUT_MS, maxBuffer: 64 * 1024,
    env: gitEnvironment(),
  });
  const lines = remote.status === 0 && !remote.error ? remote.stdout.trim().split("\n").filter(Boolean) : [];
  if (lines.length !== 1 || !/^[a-f0-9]{40}\s+refs\/heads\/main$/.test(lines[0])) {
    throw new ProtectedGitDependencyError();
  }
  const tip = lines[0].split(/\s+/)[0];
  const directory = mkdtempSync(join(tmpdir(), "mission-control-protected-git-"));
  const bare = join(directory, "authority.git");
  try {
    git(directory, ["init", "--quiet", "--bare", bare]);
    git(bare, ["fetch", "--quiet", "--no-tags", PROTECTED_ORIGIN, `${tip}:refs/heads/main`]);
    const resolved = String(git(bare, ["rev-parse", `${request.commitSha}^{commit}`], "utf8", true)).trim();
    if (resolved !== request.commitSha) throw new ProtectedGitBindingMismatchError();
    const ancestor = spawnSync("git", ["merge-base", "--is-ancestor", resolved, "refs/heads/main"], {
      cwd: bare, encoding: "utf8", timeout: GIT_TIMEOUT_MS, env: gitEnvironment(),
    });
    if (ancestor.error) throw new ProtectedGitDependencyError();
    if (ancestor.status === 1) throw new ProtectedGitBindingMismatchError();
    if (ancestor.status !== 0) throw new ProtectedGitDependencyError();
    const blobOid = String(git(bare, ["rev-parse", `${resolved}:${request.path}`], "utf8", true)).trim();
    if (!/^[a-f0-9]{40,64}$/.test(blobOid)) throw new ProtectedGitBindingMismatchError();
    const bytes = git(bare, ["show", `${resolved}:${request.path}`], "buffer", true) as Buffer;
    return { bytes: new Uint8Array(bytes), blobOid };
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

async function sha256(value: Uint8Array): Promise<string> {
  return createHash("sha256").update(value).digest("hex");
}

function object(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function decodeObject(bytes: Uint8Array): Record<string, unknown> {
  try {
    const parsed = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
    if (!object(parsed)) throw new Error("invalid object");
    return parsed;
  } catch {
    throw new ProtectedGitBindingMismatchError();
  }
}

export async function verifyProtectedSuppressionBinding(
  binding: SuppressionBinding,
  read: ProtectedGitReader = readProtectedGitFile,
): Promise<void> {
  try { await validateSuppressionBindingHash(binding); }
  catch { throw new ProtectedGitBindingMismatchError(); }
  if (binding.repository !== PROTECTED_REPOSITORY) throw new ProtectedGitBindingMismatchError();
  const gate = await read({ repository: binding.repository, commitSha: binding.commitSha, path: binding.gatePath });
  const admission = await read({ repository: binding.repository, commitSha: binding.admissionCommitSha, path: binding.admissionPath });
  if (
    gate.blobOid !== binding.gateBlobOid || admission.blobOid !== binding.admissionBlobOid
    || await sha256(gate.bytes) !== binding.gateBlobSha256
    || await sha256(admission.bytes) !== binding.admissionBlobSha256
  ) {
    throw new ProtectedGitBindingMismatchError();
  }
  const gateArtifact = decodeObject(gate.bytes);
  const admissionArtifact = decodeObject(admission.bytes);
  if (await hashCanonicalJson(gateArtifact) !== binding.gateArtifactHash) throw new ProtectedGitBindingMismatchError();
  const gateKeys = Object.keys(gateArtifact).sort();
  if (gateKeys.length !== 2 || gateKeys[0] !== "draft_request" || gateKeys[1] !== "gate_receipt") {
    throw new ProtectedGitBindingMismatchError();
  }
  const request = gateArtifact.draft_request;
  const receipt = gateArtifact.gate_receipt;
  if (!object(request) || !object(receipt)) throw new ProtectedGitBindingMismatchError();
  if (
    request.gate_receipt_hash !== await hashCanonicalJson(receipt)
    || receipt.prospect_id !== binding.prospectId
    || receipt.evidence_commit !== binding.admissionCommitSha
    || receipt.manifest_path !== binding.admissionPath
    || receipt.manifest_blob_sha256 !== binding.admissionBlobSha256
    || receipt.attestation_id !== binding.channelAttestationId
    || receipt.owner_revision !== binding.channelOwnerRevision
    || admissionArtifact.schema_version !== "prospect-candidate-v2"
    || admissionArtifact.prospect_id !== binding.prospectId
    || !object(admissionArtifact.organization)
    || admissionArtifact.organization.name_fact_id !== binding.organizationFactId
  ) throw new ProtectedGitBindingMismatchError();
  // Ensure the canonicalizer accepts the complete objects; caller-controlled exotic values never survive.
  try {
    canonicalJson(gateArtifact);
    canonicalJson(admissionArtifact);
  } catch { throw new ProtectedGitBindingMismatchError(); }
}
