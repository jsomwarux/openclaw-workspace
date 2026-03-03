"use client";
import { useEffect, useState, useCallback } from "react";
import { RefreshCw, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";
import { cn } from "@/lib/utils";

type CostData = {
  today: { date: string; total_usd: number; by_model: Record<string, any>; alerts_fired: any[] };
  yesterday: { date: string; total_usd: number } | null;
  month: {
    label: string; total_usd: number; pace_usd: number;
    goal_usd: number; cap_usd: number; days_elapsed: number;
    days_in_month: number; pct_of_goal: number;
  };
  by_model: Record<string, { sessions: number; cost_usd: number; input_tokens: number; output_tokens: number; cache_read: number }>;
  daily_trend: { date: string; total_usd: number }[];
  alerts: { type: string; message: string; level: "warning" | "critical" }[];
  thresholds: { session: number; daily: number; monthly: number; goal: number };
};

function fmt(n: number) { return `$${n.toFixed(3)}`; }
function fmtShort(n: number) { return `$${n.toFixed(2)}`; }
function fmtTokens(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k`;
  return `${n}`;
}

function ModelRow({ model, data, monthTotal }: { model: string; data: any; monthTotal: number }) {
  const share = monthTotal > 0 ? (data.cost_usd / monthTotal) * 100 : 0;
  const cacheRatio = (data.input_tokens + data.cache_read) > 0
    ? (data.cache_read / (data.input_tokens + data.cache_read)) * 100 : 0;

  const modelColors: Record<string, string> = {
    "claude-sonnet-4-6": "bg-violet-500/20 text-violet-300",
    "claude-opus-4-6":   "bg-red-500/20 text-red-300",
    "llama-3.3-70b-versatile": "bg-emerald-500/20 text-emerald-300",
  };
  const color = modelColors[model] ?? "bg-zinc-700/30 text-zinc-300";

  return (
    <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
      <div className="flex items-start justify-between gap-2 mb-3">
        <span className={cn("text-[10px] px-2 py-0.5 rounded font-mono font-medium", color)}>
          {model}
        </span>
        <span className="text-sm font-bold font-mono text-zinc-100">{fmtShort(data.cost_usd)}</span>
      </div>
      {/* Cost share bar */}
      <div className="h-1 bg-[#2a2a2a] rounded-full mb-3 overflow-hidden">
        <div className="h-full bg-emerald-500/60 rounded-full" style={{ width: `${share}%` }} />
      </div>
      <div className="grid grid-cols-2 gap-x-4 gap-y-1">
        <div>
          <p className="text-[9px] text-zinc-600">Sessions</p>
          <p className="text-[11px] text-zinc-300 font-mono">{data.sessions}</p>
        </div>
        <div>
          <p className="text-[9px] text-zinc-600">Share</p>
          <p className="text-[11px] text-zinc-300 font-mono">{share.toFixed(0)}%</p>
        </div>
        <div>
          <p className="text-[9px] text-zinc-600">Input</p>
          <p className="text-[11px] text-zinc-300 font-mono">{fmtTokens(data.input_tokens)}</p>
        </div>
        <div>
          <p className="text-[9px] text-zinc-600">Output</p>
          <p className="text-[11px] text-zinc-300 font-mono">{fmtTokens(data.output_tokens)}</p>
        </div>
        <div>
          <p className="text-[9px] text-zinc-600">Cache Read</p>
          <p className="text-[11px] text-zinc-300 font-mono">{fmtTokens(data.cache_read)}</p>
        </div>
        <div>
          <p className="text-[9px] text-zinc-600">Cache Hit%</p>
          <p className={cn("text-[11px] font-mono", cacheRatio > 50 ? "text-emerald-400" : "text-zinc-400")}>
            {cacheRatio.toFixed(0)}%
          </p>
        </div>
      </div>
    </div>
  );
}

function TrendBar({ trend }: { trend: { date: string; total_usd: number }[] }) {
  const max = Math.max(...trend.map(d => d.total_usd), 0.01);
  return (
    <div className="flex items-end gap-1 h-16">
      {trend.map((d) => {
        const pct = (d.total_usd / max) * 100;
        const isToday = d.date === trend[trend.length - 1]?.date;
        return (
          <div key={d.date} className="flex-1 flex flex-col items-center gap-1 group relative">
            <div className="absolute bottom-full mb-1 hidden group-hover:flex flex-col items-center z-10">
              <div className="bg-[#1a1a1a] border border-[#333] rounded px-2 py-1 text-[9px] text-zinc-300 whitespace-nowrap">
                {d.date.slice(5)}: {fmtShort(d.total_usd)}
              </div>
            </div>
            <div
              className={cn("w-full rounded-t-sm transition-all", isToday ? "bg-emerald-500/80" : "bg-zinc-700/50")}
              style={{ height: `${Math.max(pct, 4)}%` }}
            />
          </div>
        );
      })}
    </div>
  );
}

export default function CostsPage() {
  const [data, setData] = useState<CostData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await fetch("/api/costs");
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setData(await r.json());
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  if (loading) return (
    <div className="p-6 flex items-center justify-center h-64">
      <RefreshCw size={16} className="text-zinc-600 animate-spin" />
    </div>
  );

  if (error || !data) return (
    <div className="p-6">
      <p className="text-xs text-red-400">Failed to load cost data: {error}</p>
    </div>
  );

  const { today, yesterday, month, by_model, daily_trend, alerts } = data;
  const dayChange = yesterday ? today.total_usd - yesterday.total_usd : null;
  const modelEntries = Object.entries(by_model).filter(([, d]) => d.cost_usd > 0).sort((a, b) => b[1].cost_usd - a[1].cost_usd);

  return (
    <div className="p-4 sm:p-6 max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-lg font-semibold text-zinc-100">Cost Dashboard</h1>
          <p className="text-xs text-zinc-500 mt-0.5">Daily · Monthly · By Model — as of {today.date}</p>
        </div>
        <button onClick={load} className="text-zinc-500 hover:text-zinc-300 transition-colors p-2">
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
        </button>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="mb-4 space-y-2">
          {alerts.map((a, i) => (
            <div key={i} className={cn("flex items-start gap-2 rounded-lg px-3 py-2.5 border text-xs",
              a.level === "critical"
                ? "bg-red-500/10 border-red-500/30 text-red-300"
                : "bg-yellow-500/10 border-yellow-500/30 text-yellow-300"
            )}>
              <AlertTriangle size={12} className="flex-shrink-0 mt-0.5" />
              {a.message}
            </div>
          ))}
        </div>
      )}
      {alerts.length === 0 && (
        <div className="mb-4 flex items-center gap-2 text-[10px] text-emerald-400">
          <CheckCircle size={11} /> No cost alerts — within all thresholds
        </div>
      )}

      {/* Top stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {/* Today */}
        <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
          <p className="text-[10px] text-zinc-500 mb-1">Today</p>
          <p className="text-xl font-bold font-mono text-zinc-100">{fmtShort(today.total_usd)}</p>
          {dayChange !== null && (
            <p className={cn("text-[9px] mt-1", dayChange >= 0 ? "text-zinc-500" : "text-emerald-400")}>
              {dayChange >= 0 ? "+" : ""}{fmtShort(dayChange)} vs yesterday
            </p>
          )}
          <p className="text-[9px] text-zinc-600 mt-0.5">limit: {fmtShort(data.thresholds.daily)}</p>
        </div>

        {/* Yesterday */}
        <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
          <p className="text-[10px] text-zinc-500 mb-1">Yesterday</p>
          <p className="text-xl font-bold font-mono text-zinc-100">
            {yesterday ? fmtShort(yesterday.total_usd) : "—"}
          </p>
          <p className="text-[9px] text-zinc-600 mt-1">{yesterday?.date ?? "no data"}</p>
        </div>

        {/* Month to date */}
        <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
          <p className="text-[10px] text-zinc-500 mb-1">Month to Date</p>
          <p className="text-xl font-bold font-mono text-zinc-100">{fmtShort(month.total_usd)}</p>
          <div className="h-1 bg-[#2a2a2a] rounded-full mt-2 mb-1 overflow-hidden">
            <div
              className={cn("h-full rounded-full", month.pct_of_goal >= 100 ? "bg-red-500" : month.pct_of_goal >= 75 ? "bg-yellow-500" : "bg-emerald-500")}
              style={{ width: `${Math.min(month.pct_of_goal, 100)}%` }}
            />
          </div>
          <p className="text-[9px] text-zinc-600">{month.pct_of_goal.toFixed(0)}% of {fmtShort(month.goal_usd)} goal</p>
        </div>

        {/* Monthly pace */}
        <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
          <p className="text-[10px] text-zinc-500 mb-1">Monthly Pace</p>
          <p className={cn("text-xl font-bold font-mono", month.pace_usd >= month.cap_usd ? "text-red-400" : month.pace_usd >= month.goal_usd ? "text-yellow-400" : "text-emerald-400")}>
            {fmtShort(month.pace_usd)}
          </p>
          <p className="text-[9px] text-zinc-600 mt-1">day {month.days_elapsed}/{month.days_in_month}</p>
          <p className="text-[9px] text-zinc-600">cap: {fmtShort(month.cap_usd)}</p>
        </div>
      </div>

      {/* Daily trend */}
      <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4 mb-4">
        <div className="flex items-center justify-between mb-3">
          <p className="text-[10px] text-zinc-500 uppercase tracking-wider">Daily Spend — Last {daily_trend.length} Days</p>
          <TrendingUp size={12} className="text-zinc-600" />
        </div>
        <TrendBar trend={daily_trend} />
        <div className="flex justify-between mt-2">
          <span className="text-[9px] text-zinc-700">{daily_trend[0]?.date.slice(5)}</span>
          <span className="text-[9px] text-emerald-500">today ▲</span>
        </div>
      </div>

      {/* By model — month */}
      {modelEntries.length > 0 && (
        <div>
          <p className="text-[10px] text-zinc-500 uppercase tracking-wider mb-3">By Model — {month.label}</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {modelEntries.map(([model, d]) => (
              <ModelRow key={model} model={model} data={d} monthTotal={month.total_usd} />
            ))}
          </div>
        </div>
      )}

      {/* Thresholds reference */}
      <div className="mt-6 bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
        <p className="text-[10px] text-zinc-500 uppercase tracking-wider mb-2">Alert Thresholds</p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Per Session", value: data.thresholds.session },
            { label: "Daily Limit", value: data.thresholds.daily },
            { label: "Monthly Goal", value: data.thresholds.goal },
            { label: "Monthly Cap",  value: data.thresholds.monthly },
          ].map(t => (
            <div key={t.label}>
              <p className="text-[9px] text-zinc-600">{t.label}</p>
              <p className="text-xs text-zinc-300 font-mono">{fmtShort(t.value)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
