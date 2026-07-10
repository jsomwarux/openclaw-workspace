"use client";

import { Fragment, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  ArrowUpDown,
  BarChart3,
  ChevronDown,
  ChevronUp,
  CircleDollarSign,
  FileText,
  Lightbulb,
  RefreshCw,
  Search,
  Sparkles,
  Target,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { PassiveIncomeStatus, ScoreDimension } from "@/lib/mission-control/passive-income";

type SortKey = "score" | "title" | "reportDate" | "detailCompleteness";
type Decision = "build" | "watch" | "pass" | "queued" | "explore";

type Idea = {
  title: string;
  score: number;
  status: PassiveIncomeStatus;
  source: string;
  sourceFile: string;
  reportDate: string;
  concept: string;
  revenueModel: string;
  jtStackFit: string;
  longevitySignal: string;
  researchSignal: string;
  creativityCheck: string;
  scoreRationale: string;
  scoreBreakdown: ScoreDimension[];
  detailCompleteness: number;
  decision: Decision;
};

const STATUS_COLORS: Record<PassiveIncomeStatus, string> = {
  exploring: "border-amber-500/30 bg-amber-500/10 text-amber-300",
  building: "border-blue-500/30 bg-blue-500/10 text-blue-300",
  launched: "border-emerald-500/30 bg-emerald-500/10 text-emerald-300",
  shelved: "border-zinc-700 bg-zinc-800/40 text-zinc-400",
};

const DECISION_LABELS: Record<Decision | "all", string> = {
  all: "All",
  build: "Build",
  watch: "Watch",
  pass: "Pass",
  queued: "Queued",
  explore: "Explore",
};

function scoreTone(score: number) {
  if (score >= 7.8) return "border-emerald-500/30 bg-emerald-500/10 text-emerald-300";
  if (score >= 6.5) return "border-amber-500/30 bg-amber-500/10 text-amber-300";
  return "border-red-500/30 bg-red-500/10 text-red-300";
}

function MetricCard({
  label,
  value,
  detail,
  icon: Icon,
  tone = "neutral",
}: {
  label: string;
  value: string | number;
  detail: string;
  icon: typeof Lightbulb;
  tone?: "neutral" | "good" | "warn" | "blue";
}) {
  return (
    <div className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-zinc-500">{label}</p>
          <p className="mt-2 text-2xl font-semibold tracking-tight text-zinc-100">{value}</p>
        </div>
        <span
          className={cn(
            "rounded-md border p-2",
            tone === "good" && "border-emerald-500/30 bg-emerald-500/10 text-emerald-300",
            tone === "warn" && "border-[#f0883e]/30 bg-[#f0883e]/10 text-[#f0883e]",
            tone === "blue" && "border-blue-500/30 bg-blue-500/10 text-blue-300",
            tone === "neutral" && "border-[#20262d] bg-[#111] text-zinc-400",
          )}
        >
          <Icon size={16} />
        </span>
      </div>
      <p className="mt-3 text-xs leading-relaxed text-zinc-500">{detail}</p>
    </div>
  );
}

function DetailField({ label, value }: { label: string; value: string }) {
  if (!value) return null;
  return (
    <div>
      <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-zinc-600">{label}</p>
      <p className="mt-1 text-xs leading-relaxed text-zinc-400">{value}</p>
    </div>
  );
}

function ScoreBreakdown({ dimensions }: { dimensions: ScoreDimension[] }) {
  if (dimensions.length === 0) {
    return <p className="text-xs text-zinc-600">No source scorecard was captured for this idea.</p>;
  }

  return (
    <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
      {dimensions.map((dimension) => (
        <div key={dimension.label} className="rounded-md border border-[#20262d] bg-[#0b0d10] p-3">
          <div className="flex items-center justify-between gap-2">
            <p className="truncate text-[11px] text-zinc-500">{dimension.label}</p>
            <p className="font-mono text-xs text-zinc-200">{dimension.value.toFixed(1)}</p>
          </div>
          <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[#1a1f25]">
            <div className="h-full rounded-full bg-emerald-400" style={{ width: `${Math.min(100, Math.max(0, dimension.value * 10))}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

export default function PassiveIncomePage() {
  const [ideas, setIdeas] = useState<Idea[] | undefined>(undefined);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [decisionFilter, setDecisionFilter] = useState<Decision | "all">("all");
  const [sortKey, setSortKey] = useState<SortKey>("score");
  const [sortAsc, setSortAsc] = useState(false);
  const [query, setQuery] = useState("");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<string | null>(null);

  useEffect(() => {
    void loadIdeas();
  }, []);

  async function loadIdeas() {
    setSyncing(true);
    setLoadError(null);
    setSyncResult(null);
    try {
      const res = await fetch("/api/passive-income", { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const loadedIdeas = Array.isArray(data.ideas) ? data.ideas : [];
      setIdeas(loadedIdeas);
      setSyncResult(`Loaded ${loadedIdeas.length} ideas`);
      window.setTimeout(() => setSyncResult(null), 3000);
    } catch (error) {
      setLoadError(error instanceof Error ? error.message : "Unknown error");
      setIdeas([]);
      setSyncResult("Load failed");
    } finally {
      setSyncing(false);
    }
  }

  const filtered = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    return (ideas ?? []).filter((idea) => {
      const matchesDecision = decisionFilter === "all" || idea.decision === decisionFilter;
      const haystack = `${idea.title} ${idea.concept} ${idea.scoreRationale} ${idea.revenueModel}`.toLowerCase();
      return matchesDecision && (!normalizedQuery || haystack.includes(normalizedQuery));
    });
  }, [decisionFilter, ideas, query]);

  const sorted = useMemo(() => {
    return [...filtered].sort((a, b) => {
      const dir = sortAsc ? 1 : -1;
      if (sortKey === "score") return (a.score - b.score) * dir;
      if (sortKey === "detailCompleteness") return (a.detailCompleteness - b.detailCompleteness) * dir;
      if (sortKey === "title") return a.title.localeCompare(b.title) * dir;
      return a.reportDate.localeCompare(b.reportDate) * dir;
    });
  }, [filtered, sortAsc, sortKey]);

  const stats = useMemo(() => {
    const list = ideas ?? [];
    const total = list.length;
    const buildable = list.filter((idea) => idea.decision === "build").length;
    const rationale = list.filter((idea) => idea.scoreRationale).length;
    const avgScore = total ? list.reduce((sum, idea) => sum + idea.score, 0) / total : 0;
    return { total, buildable, rationale, avgScore };
  }, [ideas]);

  const decisionCounts = useMemo(() => {
    const counts: Record<Decision, number> = { build: 0, watch: 0, pass: 0, queued: 0, explore: 0 };
    for (const idea of ideas ?? []) counts[idea.decision] += 1;
    return counts;
  }, [ideas]);

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6 flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <Link href="/ship" className="mb-3 inline-flex items-center gap-2 text-xs text-zinc-500 transition-colors hover:text-zinc-300">
            <ArrowLeft size={13} />
            Ship
          </Link>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-emerald-300">Ship / Passive Income</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Passive income decision board</h1>
          <p className="mt-1 max-w-3xl text-xs leading-relaxed text-zinc-500">
            Ranked app and micro-product ideas from Scout and Strategist reports, with the reason each score earned its place.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {syncResult && <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-[10px] text-emerald-300">{syncResult}</span>}
          <button
            type="button"
            onClick={loadIdeas}
            disabled={syncing}
            className="inline-flex items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 transition-colors hover:border-[#38414a] disabled:opacity-50"
          >
            <RefreshCw size={13} className={syncing ? "animate-spin" : ""} />
            Refresh
          </button>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-4">
        <MetricCard icon={Lightbulb} label="Total Ideas" value={stats.total} detail="Deduped ideas parsed from passive-income reports." tone="blue" />
        <MetricCard icon={Target} label="Build Calls" value={stats.buildable} detail="Ideas the strategist marked as active build candidates." tone="good" />
        <MetricCard icon={Sparkles} label="Rationales" value={stats.rationale} detail="Ideas with an explicit score explanation visible on the board." tone="warn" />
        <MetricCard icon={BarChart3} label="Avg Score" value={stats.avgScore.toFixed(1)} detail="Portfolio average across parsed scored ideas." />
      </div>

      <section className="mt-4 rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex flex-wrap gap-2">
            {(["all", "build", "watch", "explore", "queued", "pass"] as const).map((decision) => {
              const active = decisionFilter === decision;
              const count = decision === "all" ? stats.total : decisionCounts[decision];
              return (
                <button
                  key={decision}
                  type="button"
                  onClick={() => setDecisionFilter(decision)}
                  className={cn(
                    "rounded-md border px-3 py-1.5 text-[11px] font-medium transition-colors",
                    active ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-200" : "border-[#20262d] text-zinc-500 hover:border-[#38414a] hover:text-zinc-300",
                  )}
                >
                  {DECISION_LABELS[decision]} ({count})
                </button>
              );
            })}
          </div>

          <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
            <label className="relative">
              <Search size={13} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-zinc-600" />
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search ideas"
                className="h-9 w-full rounded-md border border-[#20262d] bg-[#090b0e] pl-8 pr-3 text-xs text-zinc-300 outline-none transition-colors placeholder:text-zinc-700 focus:border-emerald-500/40 sm:w-56"
              />
            </label>
            <select
              value={sortKey}
              onChange={(event) => setSortKey(event.target.value as SortKey)}
              className="h-9 rounded-md border border-[#20262d] bg-[#090b0e] px-3 text-xs text-zinc-400 outline-none focus:border-emerald-500/40"
            >
              <option value="score">Score</option>
              <option value="detailCompleteness">Detail</option>
              <option value="reportDate">Date</option>
              <option value="title">Title</option>
            </select>
            <button
              type="button"
              onClick={() => setSortAsc(!sortAsc)}
              title="Reverse sort"
              className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-[#20262d] bg-[#090b0e] text-zinc-500 transition-colors hover:border-[#38414a] hover:text-zinc-300"
            >
              <ArrowUpDown size={14} />
            </button>
          </div>
        </div>
      </section>

      {ideas === undefined ? (
        <div className="py-16 text-center text-sm text-zinc-600">Loading...</div>
      ) : loadError ? (
        <div className="py-16 text-center">
          <Lightbulb size={32} className="mx-auto mb-3 text-red-500/60" />
          <p className="text-sm text-red-400">Passive income ideas failed to load</p>
          <p className="mt-1 text-xs text-zinc-600">{loadError}</p>
        </div>
      ) : sorted.length === 0 ? (
        <div className="py-16 text-center">
          <Lightbulb size={32} className="mx-auto mb-3 text-zinc-700" />
          <p className="text-sm text-zinc-500">No matching ideas</p>
          <p className="mt-1 text-xs text-zinc-600">Clear the filters or refresh the report parser.</p>
        </div>
      ) : (
        <div className="mt-5 overflow-hidden rounded-lg border border-[#20262d] bg-[#0d1014]">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[920px] text-left text-[11px]">
              <thead>
                <tr className="border-b border-[#20262d] bg-[#0a0d10]">
                  <th className="px-4 py-3 font-medium text-zinc-500">Rank</th>
                  <th className="px-4 py-3 font-medium text-zinc-500">Idea</th>
                  <th className="px-4 py-3 font-medium text-zinc-500">Score</th>
                  <th className="px-4 py-3 font-medium text-zinc-500">Decision</th>
                  <th className="px-4 py-3 font-medium text-zinc-500">Why It Scored There</th>
                  <th className="px-4 py-3 font-medium text-zinc-500">Source</th>
                </tr>
              </thead>
              <tbody>
                {sorted.map((idea, index) => {
                  const id = `${idea.title}-${idea.reportDate}`;
                  const expanded = expandedId === id;
                  return (
                    <Fragment key={id}>
                      <tr
                        onClick={() => setExpandedId(expanded ? null : id)}
                        className={cn("cursor-pointer border-b border-[#171c21] transition-colors", expanded ? "bg-[#11161b]" : "hover:bg-[#101419]")}
                      >
                        <td className="px-4 py-3 font-mono text-zinc-600">{index + 1}</td>
                        <td className="px-4 py-3">
                          <p className="font-medium text-zinc-100">{idea.title}</p>
                          <p className="mt-1 line-clamp-2 max-w-md text-zinc-500">{idea.concept || "No concept captured yet."}</p>
                        </td>
                        <td className="px-4 py-3">
                          <span className={cn("inline-flex min-w-12 justify-center rounded border px-2 py-1 font-mono text-[11px]", scoreTone(idea.score))}>
                            {idea.score.toFixed(1)}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex flex-col gap-1">
                            <span className="w-fit rounded border border-[#20262d] bg-[#11161b] px-2 py-0.5 text-[10px] uppercase text-zinc-300">{DECISION_LABELS[idea.decision]}</span>
                            <span className={cn("w-fit rounded border px-2 py-0.5 text-[10px] uppercase", STATUS_COLORS[idea.status])}>{idea.status}</span>
                          </div>
                        </td>
                        <td className="max-w-md px-4 py-3 text-zinc-400">
                          <p className="line-clamp-3 leading-relaxed">{idea.scoreRationale}</p>
                        </td>
                        <td className="px-4 py-3 text-zinc-500">
                          <p>{idea.source}</p>
                          <p className="mt-1 font-mono text-[10px] text-zinc-700">{idea.detailCompleteness}/7 fields</p>
                        </td>
                      </tr>
                      {expanded && (
                        <tr className="border-b border-[#171c21] bg-[#090b0e]">
                          <td colSpan={6} className="px-4 py-5">
                            <div className="space-y-5">
                              <div>
                                <p className="mb-2 flex items-center gap-2 text-sm font-semibold text-zinc-100">
                                  <CircleDollarSign size={15} className="text-emerald-300" />
                                  Scorecard
                                </p>
                                <ScoreBreakdown dimensions={idea.scoreBreakdown} />
                              </div>

                              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                                <DetailField label="Optimal Description" value={idea.concept} />
                                <DetailField label="Revenue Model" value={idea.revenueModel} />
                                <DetailField label="JT Stack Fit" value={idea.jtStackFit} />
                                <DetailField label="Longevity Signal" value={idea.longevitySignal} />
                                <DetailField label="Research Signal" value={idea.researchSignal} />
                                <DetailField label="Creativity Check" value={idea.creativityCheck} />
                              </div>

                              <div className="flex flex-wrap items-center gap-2 border-t border-[#171c21] pt-4 text-[11px] text-zinc-600">
                                <FileText size={13} />
                                <span>{idea.sourceFile}</span>
                              </div>
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
