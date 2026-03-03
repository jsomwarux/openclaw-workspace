"use client";
import { useEffect, useState, useRef } from "react";
import { Search, FileText, ChevronLeft } from "lucide-react";
import { formatDate } from "@/lib/utils";

type MemoryEntry = {
  file: string; section: string; content: string; preview: string; mtime: number;
};

export default function MemoryPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MemoryEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState<MemoryEntry | null>(null);
  const timer = useRef<any>(null);

  async function search(q: string) {
    setLoading(true);
    const r = await fetch(`/api/memory?q=${encodeURIComponent(q)}`);
    const d = await r.json();
    setResults(d.results ?? []);
    setTotal(d.total ?? 0);
    setLoading(false);
  }

  useEffect(() => { search(""); }, []);

  function onQueryChange(q: string) {
    setQuery(q);
    clearTimeout(timer.current);
    timer.current = setTimeout(() => search(q), 250);
  }

  const FILE_COLORS: Record<string, string> = {
    "MEMORY.md":    "text-emerald-400",
    "SOUL.md":      "text-purple-400",
    "HEARTBEAT.md": "text-yellow-400",
    "AGENTS.md":    "text-blue-400",
    "TOOLS.md":     "text-orange-400",
  };

  const Detail = ({ entry }: { entry: MemoryEntry }) => (
    <div>
      {/* Mobile back button */}
      <button
        onClick={() => setSelected(null)}
        className="md:hidden flex items-center gap-1 text-xs text-zinc-400 hover:text-zinc-200 mb-4 transition-colors"
      >
        <ChevronLeft size={14} /> Back
      </button>
      <div className="flex items-center gap-2 mb-1">
        <span className={`text-xs font-medium ${FILE_COLORS[entry.file] ?? "text-zinc-400"}`}>{entry.file}</span>
        <span className="text-zinc-600">›</span>
        <span className="text-xs text-zinc-400">{entry.section}</span>
      </div>
      <p className="text-[10px] text-zinc-600 mb-4">{formatDate(entry.mtime)}</p>
      <pre className="text-xs text-zinc-300 whitespace-pre-wrap font-mono leading-relaxed bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
        {entry.content}
      </pre>
    </div>
  );

  const List = () => (
    <>
      <div className="p-4 border-b border-[#2a2a2a]">
        <h1 className="text-sm font-semibold text-zinc-200 mb-3">Memory Browser</h1>
        <div className="relative">
          <Search size={12} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
          <input
            value={query}
            onChange={e => onQueryChange(e.target.value)}
            placeholder="Search memory..."
            className="w-full pl-8 pr-3 py-2.5 bg-[#1a1a1a] border border-[#333] rounded text-xs text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-700"
          />
        </div>
        <p className="text-[10px] text-zinc-600 mt-2">{total} section(s)</p>
      </div>
      <div className="flex-1 overflow-y-auto">
        {results.map((r, i) => (
          <button
            key={i}
            onClick={() => setSelected(r)}
            className={`w-full text-left p-3 border-b border-[#1e1e1e] hover:bg-[#1a1a1a] transition-colors active:bg-[#1a1a1a] ${selected === r ? "bg-[#1a1a1a]" : ""}`}
          >
            <div className="flex items-center gap-2 mb-1">
              <FileText size={10} className={FILE_COLORS[r.file] ?? "text-zinc-500"} />
              <span className="text-[9px] text-zinc-500">{r.file}</span>
            </div>
            <p className="text-[11px] text-zinc-300 font-medium truncate">{r.section}</p>
            <p className="text-[10px] text-zinc-600 mt-0.5 line-clamp-2 leading-relaxed">{r.preview}</p>
          </button>
        ))}
        {!loading && results.length === 0 && (
          <div className="text-center py-8 text-zinc-600 text-xs">No results</div>
        )}
      </div>
    </>
  );

  return (
    <>
      {/* ── Mobile: stacked (list → detail) ── */}
      <div className="md:hidden flex flex-col h-[calc(100vh-7rem)]">
        {selected ? (
          <div className="flex-1 overflow-y-auto p-4">
            <Detail entry={selected} />
          </div>
        ) : (
          <div className="flex flex-col flex-1 overflow-hidden">
            <List />
          </div>
        )}
      </div>

      {/* ── Desktop: side-by-side panels ── */}
      <div className="hidden md:flex h-screen overflow-hidden">
        {/* List */}
        <div className="w-80 border-r border-[#2a2a2a] flex flex-col flex-shrink-0">
          <List />
        </div>

        {/* Detail */}
        <div className="flex-1 overflow-y-auto p-6">
          {selected ? (
            <Detail entry={selected} />
          ) : (
            <div className="flex items-center justify-center h-full text-zinc-600 text-xs">
              Select a section to read
            </div>
          )}
        </div>
      </div>
    </>
  );
}
