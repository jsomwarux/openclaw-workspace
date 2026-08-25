import fs from "fs";
import path from "path";
import { NextResponse } from "next/server";
import { parseNightlyValidationSnapshot, type NightlyRunFile } from "@/lib/mission-control/nightly-validation";

const WORKSPACE = path.join(process.env.HOME ?? "", ".openclaw/workspace");
const PORTFOLIO_DIR = path.join(WORKSPACE, "memory/agent-portfolio");
const QUEUE_FILE = path.join(PORTFOLIO_DIR, "validation-queue.jsonl");
const RUNS_DIR = path.join(PORTFOLIO_DIR, "runs");
const STATE_FILE = path.join(WORKSPACE, "memory/job-state/nightly-validation.md");

function readOptional(filePath: string): string {
  return fs.existsSync(filePath) ? fs.readFileSync(filePath, "utf-8") : "";
}

function readRunFiles(): NightlyRunFile[] {
  if (!fs.existsSync(RUNS_DIR)) return [];
  const runs: NightlyRunFile[] = [];
  for (const dateEntry of fs.readdirSync(RUNS_DIR, { withFileTypes: true })) {
    if (!dateEntry.isDirectory()) continue;
    const dateDir = path.join(RUNS_DIR, dateEntry.name);
    for (const runEntry of fs.readdirSync(dateDir, { withFileTypes: true })) {
      if (!runEntry.isDirectory() || !runEntry.name.startsWith("run-")) continue;
      const runDir = path.join(dateDir, runEntry.name);
      const admissionPath = path.join(runDir, "admission.json");
      if (!fs.existsSync(admissionPath)) throw new Error(`incomplete nightly run ${dateEntry.name}/${runEntry.name}: admission.json missing`);
      const promotionFiles = fs.readdirSync(runDir)
        .filter((name) => /^promotions-\d{12}\.json$/.test(name))
        .map((name) => ({ name, text: fs.readFileSync(path.join(runDir, name), "utf-8") }));
      runs.push({
        runId: `${dateEntry.name}/${runEntry.name}`,
        admissionText: fs.readFileSync(admissionPath, "utf-8"),
        promotionFiles,
      });
    }
  }
  return runs;
}

export async function GET() {
  try {
    const snapshot = parseNightlyValidationSnapshot({
      queueText: readOptional(QUEUE_FILE),
      stateText: readOptional(STATE_FILE),
      runFiles: readRunFiles(),
    });
    return NextResponse.json(snapshot);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : String(error) },
      { status: 500 },
    );
  }
}
