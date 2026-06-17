"use client";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { RefreshCw } from "lucide-react";

type Entry = {
  id: string; timestamp: string; action_type: string;
  title: string; description: string; outcome: string;
  error: string | null; files_affected: string[];
  cost: { tokens?: number; usd?: number } | null;
  date: string;
};

const TYPE_COLORS: Record<string, string> = {
  automation_setup: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
  security:        "text-red-400 bg-red-500/10 border-red-500/20",
  file_creation:   "text-blue-400 bg-blue-500/10 border-blue-500/20",
  file_edit:       "text-blue-300 bg-blue-500/10 border-blue-500/20",
  config_change:   "text-yellow-400 bg-yellow-500/10 border-yellow-500/20",
  research:        "text-purple-400 bg-purple-500/10 border-purple-500/20",
  cron_setup:      "text-orange-400 bg-orange-500/10 border-orange-500/20",
  other:           "text-zinc-400 bg-zinc-700/20 border-zinc-600/20",
};

export default function AuditPage() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [types, setTypes] = useState<string[]>([]);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  async function load(type = filter) {
    setLoading(true);
    const params = new URLSearchParams({ limit: "50" });
    if (type) params.set("type", type);
    const r = await fetch(`/api/proofs?${params}`);
    const d = await r.json();
    setEntries(d.entries ?? []);
    if (d.types) setTypes(d.types);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  function handleFilter(t: string) {
    const next = filter === t ? "" : t;
    setFilter(next);
    load(next);
  }

  function formatTs(ts: string) {
    return new Date(ts).toLocaleString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  }

  return (
    <div className="p-4 sm:p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-lg font-semibold text-zinc-100">Audit Trail</h1>
          <p className="text-xs text-zinc-500 mt-0.5">{entries.length} entries · proof of every action</p>
        </div>
        <button onClick={() => load()} className="text-zinc-500 hover:text-zinc-300 transition-colors p-2">
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
        </button>
      </div>

      {/* Type filter chips */}
      <div className="flex flex-wrap gap-1.5 mb-5">
        {types.map(t => (
          <button
            key={t}
            onClick={() => handleFilter(t)}
            className={cn(
              "text-[9px] px-2 py-1 rounded border transition-all font-medium",
              filter === t
                ? (TYPE_COLORS[t] ?? TYPE_COLORS.other)
                : "text-zinc-500 border-zinc-700 bg-transparent hover:border-zinc-500"
            )}
          >
            {t.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entries */}
      <div className="space-y-2">
        {entries.map(entry => (
          <div
            key={entry.id}
            className="bg-[#111] border border-[#2a2a2a] rounded-lg overflow-hidden"
          >
            <button
              onClick={() => setExpanded(expanded === entry.id ? null : entry.id)}
              className="w-full text-left p-3 hover:bg-[#1a1a1a] transition-colors"
            >
              <div className="flex flex-col gap-1.5">
                <div className="flex items-start justify-between gap-2">
                  <p className="text-xs text-zinc-200 font-medium leading-snug">{entry.title}</p>
                  <span className={cn("text-[9px] px-1.5 py-0.5 rounded flex-shrink-0",
                    entry.outcome === "success" ? "text-emerald-400 bg-emerald-500/10" :
                    entry.outcome === "failure" ? "text-red-400 bg-red-500/10" :
                    "text-yellow-400 bg-yellow-500/10"
                  )}>{entry.outcome}</span>
                </div>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={cn("text-[9px] px-1.5 py-0.5 rounded border font-medium", TYPE_COLORS[entry.action_type] ?? TYPE_COLORS.other)}>
                    {entry.action_type.replace(/_/g, " ")}
                  </span>
                  <span className="text-[9px] text-zinc-600">{formatTs(entry.timestamp)}</span>
                  <p className="text-[10px] text-zinc-500 truncate flex-1 min-w-0">{entry.description}</p>
                </div>
              </div>
            </button>

            {expanded === entry.id && (
              <div className="px-3 pb-3 border-t border-[#1e1e1e] pt-3 space-y-2">
                <p className="text-[10px] text-zinc-400 leading-relaxed">{entry.description}</p>
                {entry.files_affected?.length > 0 && (
                  <div>
                    <p className="text-[9px] text-zinc-600 mb-1">Files</p>
                    {entry.files_affected.map((f, i) => (
                      <p key={i} className="text-[9px] text-zinc-500 font-mono">{f.replace(process.env.HOME ?? "", "~")}</p>
                    ))}
                  </div>
                )}
                {entry.cost && (
                  <div className="flex gap-3">
                    {entry.cost.tokens && <p className="text-[9px] text-zinc-600">{entry.cost.tokens.toLocaleString()} tokens</p>}
                    {entry.cost.usd && <p className="text-[9px] text-zinc-600">${entry.cost.usd.toFixed(4)}</p>}
                  </div>
                )}
                <p className="text-[9px] text-zinc-700 font-mono">id: {entry.id}</p>
              </div>
            )}
          </div>
        ))}
        {!loading && entries.length === 0 && (
          <div className="text-center py-12 text-zinc-600 text-xs">No proof entries found</div>
        )}
      </div>
    </div>
  );
}
