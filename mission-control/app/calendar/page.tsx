"use client";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { RefreshCw, Clock, CheckCircle, XCircle, Play, Pause } from "lucide-react";

type Job = {
  jobId: string; name: string; enabled: boolean;
  schedule: any; sessionTarget: string;
  lastRun: number | null; nextRun: number | null;
  running: boolean; failed: boolean; payload: string; delivery: string;
};

function formatTs(ms: number | null): string {
  if (!ms) return "—";
  return new Date(ms).toLocaleString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function scheduleLabel(s: any): string {
  if (!s) return "unknown";
  if (s.kind === "cron") return s.expr + (s.tz ? ` (${s.tz})` : "");
  if (s.kind === "every") return `every ${Math.round(s.everyMs / 60000)}m`;
  if (s.kind === "at") return `once at ${s.at}`;
  return s.kind;
}

export default function CalendarPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const r = await fetch("/api/cron");
    const d = await r.json();
    setJobs(d.jobs ?? []);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  const failed = jobs.filter(j => j.failed);
  const running = jobs.filter(j => j.running);

  return (
    <div className="p-4 sm:p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-lg font-semibold text-zinc-100">Scheduled Tasks</h1>
          <p className="text-xs text-zinc-500 mt-0.5">
            {jobs.length} jobs · {running.length} running
            {failed.length > 0 && <span className="text-red-400 ml-1">· {failed.length} failed</span>}
          </p>
        </div>
        <button onClick={load} className="text-zinc-500 hover:text-zinc-300 transition-colors p-2">
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
        </button>
      </div>

      {failed.length > 0 && (
        <div className="mb-4 p-3 bg-red-950/40 border border-red-800/40 rounded-lg">
          <p className="text-xs text-red-400 font-medium flex items-center gap-2">
            <XCircle size={12} /> {failed.length} job(s) failed — check logs
          </p>
          {failed.map(j => <p key={j.jobId} className="text-[10px] text-red-400/70 mt-1 ml-4">{j.name}</p>)}
        </div>
      )}

      <div className="space-y-2">
        {jobs.map(job => (
          <div key={job.jobId} className={cn(
            "bg-[#111] border rounded-lg p-4",
            job.failed ? "border-red-800/40" : job.running ? "border-yellow-700/40" : "border-[#2a2a2a]"
          )}>
            {/* Job name + status icon */}
            <div className="flex items-center gap-2 mb-2">
              {job.running ? <Play size={10} className="text-yellow-400 flex-shrink-0" /> :
                job.failed ? <XCircle size={10} className="text-red-400 flex-shrink-0" /> :
                job.enabled ? <CheckCircle size={10} className="text-emerald-400 flex-shrink-0" /> :
                <Pause size={10} className="text-zinc-600 flex-shrink-0" />}
              <span className="text-xs font-medium text-zinc-200 truncate">{job.name}</span>
            </div>

            {/* Tags */}
            <div className="flex items-center gap-2 flex-wrap mb-3">
              <div className="flex items-center gap-1 text-[10px] text-zinc-500">
                <Clock size={9} />{scheduleLabel(job.schedule)}
              </div>
              <span className="text-[9px] text-zinc-600 px-1.5 py-0.5 bg-[#1a1a1a] rounded">{job.sessionTarget}</span>
              <span className="text-[9px] text-zinc-600 px-1.5 py-0.5 bg-[#1a1a1a] rounded">{job.payload}</span>
            </div>

            {/* Timestamps — inline on desktop, stacked on mobile */}
            <div className="flex flex-wrap gap-x-6 gap-y-1">
              <div>
                <span className="text-[10px] text-zinc-600">Next run: </span>
                <span className="text-[10px] text-zinc-400">{formatTs(job.nextRun)}</span>
              </div>
              {job.lastRun && (
                <div>
                  <span className="text-[10px] text-zinc-600">Last run: </span>
                  <span className="text-[10px] text-zinc-400">{formatTs(job.lastRun)}</span>
                </div>
              )}
            </div>
          </div>
        ))}
        {!loading && jobs.length === 0 && (
          <div className="text-center py-16 text-zinc-600 text-xs">No cron jobs found</div>
        )}
      </div>
    </div>
  );
}
