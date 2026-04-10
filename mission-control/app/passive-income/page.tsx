"use client";

import { Fragment, useState } from "react";
import { useQuery, useMutation } from "convex/react";
import { api } from "../../convex/_generated/api";
import {
  RefreshCw, ChevronDown, ChevronUp, TrendingUp, Lightbulb,
  Trophy, BarChart2,
} from "lucide-react";
import { cn } from "@/lib/utils";

type Status = "exploring" | "building" | "launched" | "shelved";
type SortKey = "score" | "title" | "reportDate";

const STATUS_COLORS: Record<Status, { bg: string; text: string; border: string }> = {
  exploring: { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/30" },
  building:  { bg: "bg-blue-500/10",  text: "text-blue-400",  border: "border-blue-500/30"  },
  launched:  { bg: "bg-emerald-500/10", text: "text-emerald-400", border: "border-emerald-500/30" },
  shelved:   { bg: "bg-zinc-700/20",  text: "text-zinc-500",  border: "border-zinc-600/30"  },
};

function scoreBadge(score: number) {
  if (score === 0) return { bg: "bg-zinc-700/20", text: "text-zinc-500", border: "border-zinc-600/30" };
  if (score < 5) return { bg: "bg-red-500/10", text: "text-red-400", border: "border-red-500/30" };
  if (score < 7.9) return { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/30" };
  return { bg: "bg-emerald-500/10", text: "text-emerald-400", border: "border-emerald-500/30" };
}

export default function PassiveIncomePage() {
  const ideas = useQuery(api.pideas.listPideas, {});
  const syncMutation = useMutation(api.pideas.syncPideas);

  const [statusFilter, setStatusFilter] = useState<Status | "all">("all");
  const [sortKey, setSortKey] = useState<SortKey>("score");
  const [sortAsc, setSortAsc] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<string | null>(null);

  const handleSync = async () => {
    setSyncing(true);
    setSyncResult(null);
    try {
      const res = await fetch("/api/passive-income");
      const data = await res.json();
      if (data.ideas?.length) {
        const result = await syncMutation({ ideas: data.ideas });
        setSyncResult(`Synced: ${result.created} new, ${result.updated} updated`);
      } else {
        setSyncResult("No ideas found in reports");
      }
    } catch {
      setSyncResult("Sync failed");
    } finally {
      setSyncing(false);
      setTimeout(() => setSyncResult(null), 4000);
    }
  };

  const filtered = ideas
    ? ideas.filter((i) => statusFilter === "all" || i.status === statusFilter)
    : [];

  const sorted = [...filtered].sort((a, b) => {
    const dir = sortAsc ? 1 : -1;
    if (sortKey === "score") return (a.score - b.score) * dir;
    if (sortKey === "title") return a.title.localeCompare(b.title) * dir;
    return a.reportDate.localeCompare(b.reportDate) * dir;
  });

  // Stats
  const total = ideas?.length ?? 0;
  const avgScore = total ? (ideas!.reduce((s, i) => s + i.score, 0) / total) : 0;
  const topScore = total ? Math.max(...ideas!.map((i) => i.score)) : 0;
  const statusCounts = {
    exploring: ideas?.filter((i) => i.status === "exploring").length ?? 0,
    building: ideas?.filter((i) => i.status === "building").length ?? 0,
    launched: ideas?.filter((i) => i.status === "launched").length ?? 0,
    shelved: ideas?.filter((i) => i.status === "shelved").length ?? 0,
  };

  const statCards = [
    { label: "Total Ideas", value: total, icon: Lightbulb, color: "text-violet-400" },
    { label: "Avg Score", value: avgScore.toFixed(1), icon: BarChart2, color: "text-sky-400" },
    { label: "Top Score", value: topScore.toFixed(1), icon: Trophy, color: "text-emerald-400" },
    { label: "Exploring", value: statusCounts.exploring, icon: TrendingUp, color: "text-amber-400" },
  ];

  return (
    <div className="p-4 sm:p-6 max-w-6xl space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-zinc-100">Passive Income</h1>
          <p className="text-xs text-zinc-500 mt-0.5">Ideas from weekly scout & strategist reports</p>
        </div>
        <div className="flex items-center gap-3">
          {syncResult && (
            <span className="text-[10px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 rounded-full px-3 py-1">
              {syncResult}
            </span>
          )}
          <button
            onClick={handleSync}
            disabled={syncing}
            className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-200 bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-1.5 hover:border-emerald-500/40 hover:text-emerald-400 transition-colors disabled:opacity-50"
          >
            <RefreshCw size={12} className={syncing ? "animate-spin" : ""} />
            Sync from Reports
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {statCards.map((s) => {
          const Icon = s.icon;
          return (
            <div key={s.label} className="bg-[#111] border border-[#2a2a2a] rounded-xl p-4">
              <div className="flex items-center gap-2 mb-2">
                <Icon size={13} className={s.color} />
                <p className="text-[10px] text-zinc-500 uppercase tracking-wider">{s.label}</p>
              </div>
              <p className={cn("text-xl font-semibold", s.color)}>{s.value}</p>
            </div>
          );
        })}
      </div>

      {/* Status breakdown */}
      <div className="flex flex-wrap gap-2">
        {(["all", "exploring", "building", "launched", "shelved"] as const).map((s) => {
          const active = statusFilter === s;
          const count = s === "all" ? total : statusCounts[s];
          const sc = s !== "all" ? STATUS_COLORS[s] : null;
          return (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={cn(
                "text-[11px] font-medium px-3 py-1 rounded-full border transition-colors",
                active
                  ? sc
                    ? `${sc.bg} ${sc.text} ${sc.border}`
                    : "bg-zinc-700/30 text-zinc-200 border-zinc-600"
                  : "text-zinc-500 border-[#2a2a2a] hover:border-zinc-600 hover:text-zinc-300"
              )}
            >
              {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)} ({count})
            </button>
          );
        })}

        {/* Sort dropdown */}
        <div className="ml-auto flex items-center gap-1.5">
          <select
            value={sortKey}
            onChange={(e) => setSortKey(e.target.value as SortKey)}
            className="text-[11px] bg-[#111] border border-[#2a2a2a] text-zinc-400 rounded-lg px-2 py-1 focus:outline-none focus:border-zinc-600"
          >
            <option value="score">Score</option>
            <option value="title">Title</option>
            <option value="reportDate">Date</option>
          </select>
          <button
            onClick={() => setSortAsc(!sortAsc)}
            className="text-zinc-500 hover:text-zinc-300 p-1"
          >
            {sortAsc ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
        </div>
      </div>

      {/* Table */}
      {ideas === undefined ? (
        <div className="text-center py-16 text-zinc-600 text-sm">Loading...</div>
      ) : sorted.length === 0 ? (
        <div className="text-center py-16">
          <Lightbulb size={32} className="mx-auto text-zinc-700 mb-3" />
          <p className="text-sm text-zinc-500">No ideas yet</p>
          <p className="text-xs text-zinc-600 mt-1">Click Sync to import from reports</p>
        </div>
      ) : (
        <div className="bg-[#111] border border-[#2a2a2a] rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[700px] text-[11px]">
              <thead>
                <tr className="border-b border-[#2a2a2a] bg-[#0d0d0d]">
                  <th className="text-left py-2.5 px-4 text-zinc-500 font-medium">Title</th>
                  <th className="text-left py-2.5 px-4 text-zinc-500 font-medium w-16">Score</th>
                  <th className="text-left py-2.5 px-4 text-zinc-500 font-medium w-24">Status</th>
                  <th className="text-left py-2.5 px-4 text-zinc-500 font-medium w-36">Source</th>
                  <th className="text-left py-2.5 px-4 text-zinc-500 font-medium">Concept</th>
                </tr>
              </thead>
              <tbody>
                {sorted.map((idea) => {
                  const id = idea._id;
                  const expanded = expandedId === id;
                  const sc = scoreBadge(idea.score);
                  const stc = STATUS_COLORS[idea.status];

                  return (
                    <Fragment key={id}>
                      <tr
                        onClick={() => setExpandedId(expanded ? null : id)}
                        className={cn(
                          "border-b border-[#1a1a1a] cursor-pointer transition-colors",
                          expanded ? "bg-[#151515]" : "hover:bg-[#131313]"
                        )}
                      >
                        <td className="py-3 px-4 text-zinc-200 font-medium">{idea.title}</td>
                        <td className="py-3 px-4">
                          <span className={cn("text-[10px] font-medium px-1.5 py-0.5 rounded border", sc.bg, sc.text, sc.border)}>
                            {idea.score > 0 ? idea.score.toFixed(1) : "—"}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <span className={cn("text-[9px] font-medium px-2 py-0.5 rounded-full border uppercase", stc.bg, stc.text, stc.border)}>
                            {idea.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-zinc-500">{idea.source}</td>
                        <td className="py-3 px-4 text-zinc-400 max-w-[300px] truncate">
                          {idea.concept.slice(0, 80)}{idea.concept.length > 80 ? "..." : ""}
                        </td>
                      </tr>
                      {expanded && (
                        <tr className="bg-[#0e0e0e]">
                          <td colSpan={5} className="px-4 py-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[11px]">
                              <DetailField label="Concept" value={idea.concept} />
                              <DetailField label="Revenue Model" value={idea.revenueModel} />
                              <DetailField label="JT Stack Fit" value={idea.jtStackFit} />
                              <DetailField label="Longevity Signal" value={idea.longevitySignal} />
                              <DetailField label="Research Signal" value={idea.researchSignal} />
                              <DetailField label="Creativity Check" value={idea.creativityCheck} />
                            </div>
                          </td>
                        </tr>
                      )}
                    </Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

function DetailField({ label, value }: { label: string; value: string }) {
  if (!value) return null;
  return (
    <div>
      <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1">{label}</p>
      <p className="text-zinc-400 leading-relaxed">{value}</p>
    </div>
  );
}

