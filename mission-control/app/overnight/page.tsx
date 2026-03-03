"use client";
import { useState, useEffect, useCallback } from "react";
import { ChevronDown, ChevronUp, X } from "lucide-react";
import { cn } from "@/lib/utils";

type CompletedTask = {
  name: string;
  output?: string;
  whatWasDone?: string;
  reviewNeeded?: string;
  cost?: string;
};

type SkippedTask = {
  name: string;
  reason: string;
};

type Run = {
  date: string;
  model: string;
  subagents: string;
  totalCost: string;
  completedTasks: CompletedTask[];
  skippedTasks: SkippedTask[];
  feedbackItems: string[];
  portfolioLines: string[];
};

type QueueItem = {
  id?: string;
  slug?: string;
  title?: string;
  name?: string;
  description?: string;
  notes?: string;
  score?: number;
  tags?: string[];
  file?: string;
  status?: string;
};

export default function OvernightPage() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [completedOpen, setCompletedOpen] = useState(true);
  const [skippedOpen, setSkippedOpen] = useState(false);
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());
  const [fileViewer, setFileViewer] = useState<{ path: string; content: string | null } | null>(null);

  const fetchRuns = useCallback(async () => {
    try {
      const r = await fetch("/api/overnight");
      const d = await r.json();
      setRuns(d.runs ?? []);
      if (d.runs?.length && !selectedDate) {
        setSelectedDate(d.runs[0].date);
      }
    } finally {
      setLoading(false);
    }
  }, [selectedDate]);

  const fetchQueue = useCallback(async () => {
    const r = await fetch("/api/overnight?action=queue");
    const d = await r.json();
    const pending = (d.items ?? []).filter((i: QueueItem) => i.status === "queued");
    setQueue(pending);
  }, []);

  useEffect(() => {
    fetchRuns();
    fetchQueue();
  }, [fetchRuns, fetchQueue]);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") setFileViewer(null);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  async function openFile(filePath: string) {
    setFileViewer({ path: filePath, content: null });
    const r = await fetch(`/api/overnight?action=file&path=${encodeURIComponent(filePath)}`);
    const d = await r.json();
    setFileViewer({ path: filePath, content: d.content ?? d.error ?? "Could not load file" });
  }

  async function handleDecision(item: QueueItem, status: "approved" | "rejected") {
    const itemId = item.id || item.slug;
    if (!itemId) return;
    await fetch("/api/overnight", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: itemId, status }),
    });
    setQueue(prev => prev.filter(q => (q.id || q.slug) !== itemId));
    setSavedIds(prev => new Set(prev).add(itemId));
    setTimeout(() => {
      setSavedIds(prev => {
        const next = new Set(prev);
        next.delete(itemId);
        return next;
      });
    }, 2000);
  }

  const selected = runs.find(r => r.date === selectedDate);

  function costColor(cost: string) {
    const num = parseFloat(cost.replace("$", ""));
    if (isNaN(num)) return "text-zinc-400";
    if (num < 0.5) return "text-emerald-400";
    if (num <= 1.0) return "text-yellow-400";
    return "text-red-400";
  }

  function costBgColor(cost: string) {
    const num = parseFloat(cost.replace("$", ""));
    if (isNaN(num)) return "bg-zinc-500/20 border-zinc-500/30";
    if (num < 0.5) return "bg-emerald-500/20 border-emerald-500/30";
    if (num <= 1.0) return "bg-yellow-500/20 border-yellow-500/30";
    return "bg-red-500/20 border-red-500/30";
  }

  function scoreColor(score: number) {
    if (score >= 8) return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
    if (score >= 6) return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
    return "bg-zinc-700/40 text-zinc-400 border-zinc-600/30";
  }

  function truncateModel(model: string) {
    const slash = model.indexOf("/");
    return slash >= 0 ? model.slice(slash + 1) : model;
  }

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-[60vh]">
        <p className="text-sm text-zinc-500">Loading overnight runs...</p>
      </div>
    );
  }

  if (runs.length === 0 && queue.length === 0) {
    return (
      <div className="p-6 flex items-center justify-center min-h-[60vh]">
        <p className="text-sm text-zinc-500">No overnight runs yet. First run at 3 AM.</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-lg font-semibold text-zinc-100">Overnight Work</h1>
        <p className="text-xs text-zinc-500 mt-0.5">
          {runs.length} run{runs.length !== 1 ? "s" : ""} logged
          {queue.length > 0 && ` · ${queue.length} pending review`}
        </p>
      </div>

      {/* Date tabs */}
      {runs.length > 1 && (
        <div className="flex gap-1 flex-wrap">
          {runs.map(run => (
            <button
              key={run.date}
              onClick={() => setSelectedDate(run.date)}
              className={cn(
                "text-xs px-3 py-1.5 rounded border transition-colors",
                selectedDate === run.date
                  ? "border-emerald-500/50 text-emerald-400 bg-emerald-950/30"
                  : "border-[#2a2a2a] text-zinc-400 hover:text-zinc-200 hover:border-[#3a3a3a]"
              )}
            >
              {run.date}
            </button>
          ))}
        </div>
      )}

      {/* Selected run details */}
      {selected && (
        <>
          {/* Overview card */}
          <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
            <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500 mb-3">Run Overview</p>
            <div className="flex items-center gap-4 flex-wrap">
              <div>
                <p className="text-[10px] text-zinc-500">Date</p>
                <p className="text-sm text-zinc-100">{selected.date}</p>
              </div>
              <div>
                <p className="text-[10px] text-zinc-500">Model</p>
                <p className="text-sm text-zinc-100">{truncateModel(selected.model)}</p>
              </div>
              <div>
                <p className="text-[10px] text-zinc-500">Sub-agents</p>
                <p className="text-sm text-zinc-100">{selected.subagents}</p>
              </div>
              <div>
                <p className="text-[10px] text-zinc-500">Cost</p>
                <span className={cn(
                  "text-xs px-2 py-0.5 rounded border font-medium inline-block",
                  costBgColor(selected.totalCost), costColor(selected.totalCost)
                )}>
                  {selected.totalCost}
                </span>
              </div>
            </div>
          </div>

          {/* Feedback Needed */}
          {selected.feedbackItems.length > 0 && (
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
              <p className="text-xs font-semibold uppercase tracking-widest text-yellow-400 mb-3">Feedback Needed</p>
              <ol className="list-decimal list-inside space-y-1.5">
                {selected.feedbackItems.map((item, i) => (
                  <li key={i} className="text-sm text-zinc-200">{item}</li>
                ))}
              </ol>
            </div>
          )}

          {/* Completed Tasks */}
          <div className="bg-[#111] border border-[#2a2a2a] rounded-lg">
            <button
              onClick={() => setCompletedOpen(!completedOpen)}
              className="w-full flex items-center justify-between p-4"
            >
              <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
                Completed Tasks ({selected.completedTasks.length})
              </p>
              {completedOpen ? <ChevronUp size={14} className="text-zinc-500" /> : <ChevronDown size={14} className="text-zinc-500" />}
            </button>
            {completedOpen && (
              <div className="px-4 pb-4 space-y-3">
                {selected.completedTasks.map((task, i) => (
                  <div key={i} className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-md p-3">
                    <div className="flex items-start justify-between gap-2">
                      <p className="text-sm text-zinc-100 font-medium">{task.name}</p>
                      {task.cost && (
                        <span className="text-[10px] text-zinc-500 flex-shrink-0">{task.cost}</span>
                      )}
                    </div>
                    {task.whatWasDone && (
                      <p className="text-xs text-zinc-400 mt-1.5">{task.whatWasDone}</p>
                    )}
                    {task.reviewNeeded && (
                      <div className="mt-2 bg-yellow-500/10 border border-yellow-500/30 rounded px-2.5 py-1.5">
                        <p className="text-xs text-yellow-400">Review needed: {task.reviewNeeded}</p>
                      </div>
                    )}
                    {task.output && (
                      <button
                        onClick={() => openFile(task.output!)}
                        className="mt-2 text-xs px-3 py-1.5 rounded border border-[#2a2a2a] hover:border-emerald-500/50 text-zinc-300 hover:text-emerald-400 transition-colors"
                      >
                        📄 View Output
                      </button>
                    )}
                  </div>
                ))}
                {selected.completedTasks.length === 0 && (
                  <p className="text-xs text-zinc-600 text-center py-4">No completed tasks</p>
                )}
              </div>
            )}
          </div>

          {/* Skipped Tasks */}
          {selected.skippedTasks.length > 0 && (
            <div className="bg-[#111] border border-[#2a2a2a] rounded-lg">
              <button
                onClick={() => setSkippedOpen(!skippedOpen)}
                className="w-full flex items-center justify-between p-4"
              >
                <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
                  Skipped Tasks ({selected.skippedTasks.length})
                </p>
                {skippedOpen ? <ChevronUp size={14} className="text-zinc-500" /> : <ChevronDown size={14} className="text-zinc-500" />}
              </button>
              {skippedOpen && (
                <div className="px-4 pb-4 space-y-2">
                  {selected.skippedTasks.map((task, i) => (
                    <div key={i} className="flex items-start gap-2 py-1.5">
                      <span className="text-sm text-zinc-300">{task.name}</span>
                      <span className="text-xs text-zinc-500">— {task.reason}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Portfolio Lines */}
          {selected.portfolioLines.length > 0 && (
            <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
              <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500 mb-3">Portfolio Updates</p>
              <div className="space-y-1.5">
                {selected.portfolioLines.map((line, i) => (
                  <p key={i} className="text-xs text-zinc-300">{line}</p>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {/* Portfolio Queue */}
      {queue.length > 0 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500 mb-3">
            🌐 Portfolio Queue — Pending Review
          </p>
          <div className="space-y-3">
            {queue.map(item => {
              const itemId = item.id || item.slug || "";
              return (
                <div key={itemId} className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    {item.score !== undefined && (
                      <span className={cn(
                        "text-xs px-2 py-0.5 rounded border font-medium flex-shrink-0",
                        scoreColor(item.score)
                      )}>
                        {item.score}
                      </span>
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-zinc-100 font-medium">{item.title || item.name || itemId}</p>
                      {item.description && (
                        <p className="text-xs text-zinc-400 mt-1">{item.description}</p>
                      )}
                      {item.notes && (
                        <p className="text-xs text-zinc-400 mt-1 italic">{item.notes}</p>
                      )}
                      {item.tags && item.tags.length > 0 && (
                        <div className="flex gap-1 mt-2 flex-wrap">
                          {item.tags.map(tag => (
                            <span key={tag} className="text-[9px] px-1.5 py-0.5 bg-[#1a1a1a] border border-[#2a2a2a] rounded text-zinc-500">
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 mt-3">
                    <button
                      onClick={() => handleDecision(item, "approved")}
                      className="text-xs px-3 py-1.5 rounded border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition-colors"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => handleDecision(item, "rejected")}
                      className="text-xs px-3 py-1.5 rounded border border-rose-500/30 bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 transition-colors"
                    >
                      Reject
                    </button>
                    {item.file && (
                      <button
                        onClick={() => openFile(item.file!)}
                        className="text-xs px-3 py-1.5 rounded border border-[#2a2a2a] hover:border-emerald-500/50 text-zinc-300 hover:text-emerald-400 transition-colors"
                      >
                        📄 View
                      </button>
                    )}
                    {savedIds.has(itemId) && (
                      <span className="text-xs text-emerald-400 ml-1">✓ Saved</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* File Viewer Slide-out */}
      {fileViewer && (
        <div className="fixed right-0 top-0 h-screen w-2/5 min-w-[20rem] bg-[#0d0d0d] border-l border-[#2a2a2a] z-50 flex flex-col">
          <div className="flex items-center justify-between px-4 py-3 border-b border-[#2a2a2a]">
            <p className="text-xs text-zinc-500 truncate">{fileViewer.path}</p>
            <button
              onClick={() => setFileViewer(null)}
              className="text-zinc-500 hover:text-zinc-300 transition-colors p-1"
            >
              <X size={14} />
            </button>
          </div>
          <div className="flex-1 overflow-auto p-4">
            {fileViewer.content === null ? (
              <p className="text-xs text-zinc-500">Loading...</p>
            ) : (
              <pre className="font-mono text-xs text-zinc-300 whitespace-pre-wrap">{fileViewer.content}</pre>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
