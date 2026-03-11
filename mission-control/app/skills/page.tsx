"use client";
import { useEffect, useState } from "react";
import { RefreshCw, Terminal, FileCode, Wrench, Package } from "lucide-react";
import { cn } from "@/lib/utils";

type Skill = {
  slug:        string;
  name:        string;
  description: string;
  source:      "custom" | "bundled";
  commands:    string[];
  files:       string[];
  hasScript:   boolean;
  version:     string | null;
};

const SOURCE_STYLES = {
  custom:  "bg-emerald-950/60 text-emerald-400 border-emerald-500/30",
  bundled: "bg-zinc-800/60  text-zinc-400  border-zinc-600/30",
};

function SkillCard({ skill }: { skill: Skill }) {
  return (
    <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4 flex flex-col gap-3 hover:border-zinc-700 transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="text-base">{skill.source === "custom" ? "🌿" : "📦"}</span>
          <div className="min-w-0">
            <p className="text-sm font-semibold text-zinc-200 truncate">{skill.name}</p>
            <p className="text-[10px] font-mono text-zinc-500">{skill.slug}{skill.version ? ` · v${skill.version}` : ""}</p>
          </div>
        </div>
        <span className={cn("text-[9px] px-2 py-0.5 rounded border font-medium shrink-0", SOURCE_STYLES[skill.source])}>
          {skill.source}
        </span>
      </div>

      {/* Description */}
      {skill.description && (
        <p className="text-[11px] text-zinc-400 leading-relaxed line-clamp-3">{skill.description}</p>
      )}

      {/* Commands */}
      {skill.commands.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {skill.commands.map(cmd => (
            <span
              key={cmd}
              className="inline-flex items-center gap-1 text-[10px] font-mono bg-zinc-900 border border-zinc-800 text-emerald-400 px-2 py-0.5 rounded"
            >
              <Terminal size={9} />
              {cmd}
            </span>
          ))}
        </div>
      )}

      {/* Footer: files + script badge */}
      {(skill.files.length > 0 || skill.hasScript) && (
        <div className="flex items-center gap-2 pt-1 border-t border-[#1e1e1e]">
          {skill.hasScript && (
            <span className="flex items-center gap-1 text-[10px] text-sky-400">
              <FileCode size={10} /> has scripts
            </span>
          )}
          {skill.files.length > 0 && (
            <span className="text-[10px] text-zinc-500">
              {skill.files.length} extra file{skill.files.length !== 1 ? "s" : ""}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

export default function SkillsPage() {
  const [custom,  setCustom]  = useState<Skill[]>([]);
  const [bundled, setBundled] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter,  setFilter]  = useState<"all" | "custom" | "bundled">("all");
  const [query,   setQuery]   = useState("");

  async function load() {
    setLoading(true);
    const d = await fetch("/api/skills").then(r => r.json());
    setCustom(d.custom   ?? []);
    setBundled(d.bundled ?? []);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  const all = filter === "all" ? [...custom, ...bundled]
    : filter === "custom"     ? custom
    : bundled;

  const displayed = query.trim()
    ? all.filter(s =>
        s.name.toLowerCase().includes(query.toLowerCase()) ||
        s.slug.toLowerCase().includes(query.toLowerCase()) ||
        s.description.toLowerCase().includes(query.toLowerCase()) ||
        s.commands.some(c => c.toLowerCase().includes(query.toLowerCase()))
      )
    : all;

  return (
    <div className="p-6 space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-zinc-200">Skills</h1>
          <p className="text-xs text-zinc-500 mt-0.5">
            {custom.length} custom · {bundled.length} bundled
          </p>
        </div>
        <button
          onClick={load}
          className="flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-200 border border-[#2a2a2a] hover:border-zinc-600 px-3 py-1.5 rounded transition-colors"
        >
          <RefreshCw size={12} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
      </div>

      {/* Filter + search bar */}
      <div className="flex flex-wrap items-center gap-2">
        {(["all", "custom", "bundled"] as const).map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={cn(
              "text-xs px-3 py-1.5 rounded border transition-colors capitalize",
              filter === f
                ? "bg-emerald-950/60 text-emerald-400 border-emerald-500/30"
                : "text-zinc-400 border-[#2a2a2a] hover:text-zinc-200 hover:border-zinc-600"
            )}
          >
            {f === "all" ? `All (${custom.length + bundled.length})` :
             f === "custom"  ? `Custom (${custom.length})` :
             `Bundled (${bundled.length})`}
          </button>
        ))}
        <input
          type="text"
          placeholder="Search skills or commands…"
          value={query}
          onChange={e => setQuery(e.target.value)}
          className="ml-auto text-xs bg-[#111] border border-[#2a2a2a] rounded px-3 py-1.5 text-zinc-300 placeholder-zinc-600 focus:outline-none focus:border-zinc-600 w-56"
        />
      </div>

      {/* Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-40 text-xs text-zinc-600">Loading…</div>
      ) : displayed.length === 0 ? (
        <div className="flex items-center justify-center h-40 text-xs text-zinc-600">No skills found</div>
      ) : (
        <>
          {/* Custom skills section (when showing all) */}
          {filter === "all" && custom.length > 0 && (
            <section className="space-y-3">
              <div className="flex items-center gap-2">
                <Wrench size={12} className="text-emerald-500" />
                <h2 className="text-xs font-semibold uppercase tracking-wider text-emerald-500">Custom Skills</h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
                {custom
                  .filter(s => !query || displayed.includes(s))
                  .map(s => <SkillCard key={s.slug} skill={s} />)}
              </div>
            </section>
          )}

          {/* Bundled skills section (when showing all) */}
          {filter === "all" && bundled.length > 0 && (
            <section className="space-y-3">
              <div className="flex items-center gap-2">
                <Package size={12} className="text-zinc-500" />
                <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">Bundled Skills</h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
                {bundled
                  .filter(s => !query || displayed.includes(s))
                  .map(s => <SkillCard key={s.slug} skill={s} />)}
              </div>
            </section>
          )}

          {/* Flat grid for filtered views */}
          {filter !== "all" && (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
              {displayed.map(s => <SkillCard key={s.slug} skill={s} />)}
            </div>
          )}

          {/* Search results flat */}
          {filter === "all" && query && (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
              {displayed.map(s => <SkillCard key={s.slug} skill={s} />)}
            </div>
          )}
        </>
      )}
    </div>
  );
}
