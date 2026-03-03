"use client";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { Github, RefreshCw } from "lucide-react";

type Agent = {
  id: string; name: string; emoji: string; role: string; domain: string;
  workspace: string | null; github: string | null; status: string; skills: string[];
  crons: { id: string; name: string; schedule: string }[];
  currentTask: string; created: string | null;
};

const STATUS_STYLES: Record<string, string> = {
  active:  "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  planned: "bg-zinc-700/30 text-zinc-400 border-zinc-600/30",
};

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const d = await fetch("/api/agents").then(r => r.json());
    setAgents(d.agents ?? []);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  const active  = agents.filter(a => a.status === "active");
  const planned = agents.filter(a => a.status === "planned");

  function AgentCard({ agent }: { agent: Agent }) {
    return (
      <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-2.5">
            <span className="text-2xl">{agent.emoji}</span>
            <div>
              <p className="text-sm font-semibold text-zinc-200">{agent.name}</p>
              <p className="text-[10px] text-zinc-500">{agent.role}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            {agent.github && (
              <a
                href={`https://github.com/${agent.github}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-zinc-600 hover:text-zinc-300 transition-colors"
                title={agent.github}
              >
                <Github size={12} />
              </a>
            )}
            <span className={cn("text-[9px] px-2 py-0.5 rounded border font-medium", STATUS_STYLES[agent.status] ?? STATUS_STYLES.planned)}>
              {agent.status}
            </span>
          </div>
        </div>

        <p className="text-[11px] text-zinc-400 leading-relaxed mb-3">{agent.domain}</p>

        {agent.currentTask && (
          <div className="mb-3">
            <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1">Current</p>
            <p className="text-[10px] text-zinc-400">{agent.currentTask}</p>
          </div>
        )}

        {agent.skills.length > 0 && (
          <div className="mb-3">
            <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1.5">Skills</p>
            <div className="flex flex-wrap gap-1">
              {agent.skills.map(s => (
                <span key={s} className="text-[9px] px-1.5 py-0.5 bg-blue-500/10 text-blue-400 rounded border border-blue-500/20">{s}</span>
              ))}
            </div>
          </div>
        )}

        {agent.crons.length > 0 && (
          <div>
            <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1.5">Scheduled</p>
            <div className="space-y-1">
              {agent.crons.map(c => (
                <div key={c.id} className="flex items-center justify-between text-[10px]">
                  <span className="text-zinc-400">{c.name}</span>
                  <span className="text-zinc-600">{c.schedule}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {agent.workspace && (
          <div className="mt-3 pt-3 border-t border-[#2a2a2a]">
            <p className="text-[9px] text-zinc-600 font-mono truncate">
              {agent.workspace.replace(process.env.HOME ?? "/Users/jtsomwaru", "~")}
            </p>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-lg font-semibold text-zinc-100">Agent Team</h1>
          <p className="text-xs text-zinc-500 mt-0.5">
            {active.length} active · {planned.length} planned
          </p>
        </div>
        <button onClick={load} className="text-zinc-500 hover:text-zinc-300 transition-colors p-2">
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
        </button>
      </div>

      {active.length > 0 && (
        <div className="mb-8">
          <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3">Active</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {active.map(a => <AgentCard key={a.id} agent={a} />)}
          </div>
        </div>
      )}

      {planned.length > 0 && (
        <div>
          <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3">Planned</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {planned.map(a => <AgentCard key={a.id} agent={a} />)}
          </div>
        </div>
      )}
    </div>
  );
}
