import { NextResponse } from "next/server";
import { readFileSync, existsSync } from "fs";
import { homedir } from "os";

export async function GET() {
  const path = `${homedir()}/.openclaw/cron/jobs.json`;
  if (!existsSync(path)) return NextResponse.json({ jobs: [] });
  const raw = JSON.parse(readFileSync(path, "utf-8"));
  const jobs = (raw.jobs ?? []).map((j: any) => ({
    jobId: j.jobId,
    name: j.name || j.jobId,
    enabled: j.enabled ?? true,
    schedule: j.schedule,
    sessionTarget: j.sessionTarget,
    lastRun: j.state?.lastRunAtMs ?? null,
    nextRun: j.state?.nextRunAtMs ?? null,
    running: !!j.state?.runningAtMs,
    failed: j.state?.lastOutcome === "failure",
    payload: j.payload?.kind,
    delivery: j.delivery?.mode,
  }));
  return NextResponse.json({ jobs });
}
