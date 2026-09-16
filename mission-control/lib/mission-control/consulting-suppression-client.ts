import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const PYTHON = "/usr/bin/python3";
const SCRIPT = "/Users/jtsomwaru/projects/jt-consulting-pipeline/scripts/suppression_owner.py";
const CWD = "/Users/jtsomwaru/projects/jt-consulting-pipeline";
const EVENT = /^suppression_event_[a-f0-9]{20}$/;
const DIGEST = /^[a-f0-9]{64}$/;
type Input = { schemaVersion: "outreach-suppression-event-v1"; requestId: string; prospectId: string; organizationFactId: string; channelFingerprint: string; state: "clear"; evidenceToken: string; actorId: "jt:mission-control-clear" };
type Runner = (file: string, args: string[], options: { cwd: string; timeout: number; maxBuffer: number; env: Record<string, string> }) => Promise<{ stdout: string; stderr: string }>;

function parse(value: string) {
  const lines = value.split("\n").filter((line) => line.length > 0);
  if (lines.length !== 1) throw new Error("consulting suppression owner failed");
  let parsed: unknown;
  try { parsed = JSON.parse(lines[0]); } catch { throw new Error("consulting suppression owner failed"); }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("consulting suppression owner failed");
  const record = parsed as Record<string, unknown>;
  const keys = Object.keys(record).sort(); const expected = ["created", "eventId", "observedAt", "ownerRevision"].sort();
  if (keys.length !== expected.length || keys.some((key, index) => key !== expected[index]) || typeof record.created !== "boolean" || !EVENT.test(String(record.eventId ?? "")) || !DIGEST.test(String(record.ownerRevision ?? "")) || typeof record.observedAt !== "string" || !Number.isFinite(Date.parse(record.observedAt))) throw new Error("consulting suppression owner failed");
  return record as { created: boolean; eventId: string; ownerRevision: string; observedAt: string };
}

export async function recordConsultingSuppressionClear(input: Input, run: Runner = execFileAsync as unknown as Runner) {
  const args = [SCRIPT, "record", "--schema-version", input.schemaVersion, "--request-id", input.requestId, "--prospect-id", input.prospectId, "--organization-fact-id", input.organizationFactId, "--channel-fingerprint", input.channelFingerprint, "--state", input.state, "--actor-id", input.actorId, "--evidence-token", input.evidenceToken];
  const { stdout, stderr } = await run(PYTHON, args, { cwd: CWD, timeout: 5000, maxBuffer: 64 * 1024, env: { LANG: "C.UTF-8" } });
  if (stderr !== "") throw new Error("consulting suppression owner failed");
  return parse(stdout);
}
