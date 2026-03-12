"use client";
import { useState, useEffect, useCallback } from "react";
import { Search, Archive } from "lucide-react";
import { cn, formatDate } from "@/lib/utils";

type Task = {
  _id: string;
  title: string;
  description?: string;
  status: string;
  priority: "high" | "medium" | "low";
  assignee: "jt" | "eve" | "both";
  project?: string;
  updatedAt: number;
  createdAt: number;
};

const PRIORITY_COLORS: Record<string, string> = {
  high: "bg-red-500/20 text-red-400 border-red-500/30",
  medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  low: "bg-zinc-700/40 text-zinc-400 border-zinc-600/30",
};

const ASSIGNEE_COLORS: Record<string, string> = {
  jt: "bg-blue-500/20 text-blue-400",
  eve: "bg-emerald-500/20 text-emerald-400",
  both: "bg-purple-500/20 text-purple-400",
};

export default function HistoryPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterProject, setFilterProject] = useState<string>("all");

  const fetchArchived = useCallback(async () => {
    try {
      const r = await fetch("/api/tasks?include=archived");
      const d = await r.json();
      setTasks(d.tasks ?? []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchArchived();
  }, [fetchArchived]);

  const projects = Array.from(new Set(tasks.map((t) => t.project).filter(Boolean))) as string[];

  const filtered = tasks.filter((t) => {
    const q = search.toLowerCase();
    const matchesSearch =
      !q ||
      t.title.toLowerCase().includes(q) ||
      t.description?.toLowerCase().includes(q) ||
      t.project?.toLowerCase().includes(q) ||
      t.assignee.toLowerCase().includes(q);
    const matchesProject = filterProject === "all" || t.project === filterProject;
    return matchesSearch && matchesProject;
  });

  return (
    <div className="p-4 sm:p-6 max-w-5xl">
      {/* Header */}
      <div className="mb-5">
        <div className="flex items-center gap-2">
          <Archive size={16} className="text-zinc-500" />
          <h1 className="text-lg font-semibold text-zinc-100">History</h1>
        </div>
        <p className="text-xs text-zinc-500 mt-1">
          {filtered.length} archived task{filtered.length !== 1 ? "s" : ""}
        </p>
      </div>

      {/* Search + Filter bar */}
      <div className="flex flex-col sm:flex-row gap-2 mb-5">
        <div className="relative flex-1">
          <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-600" />
          <input
            type="text"
            placeholder="Search archived tasks..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-[#111] border border-[#2a2a2a] rounded-md pl-9 pr-3 py-2.5 text-xs text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-600 transition-colors"
          />
        </div>
        {projects.length > 0 && (
          <select
            value={filterProject}
            onChange={(e) => setFilterProject(e.target.value)}
            className="bg-[#111] border border-[#2a2a2a] rounded-md px-3 py-2.5 text-xs text-zinc-100 focus:outline-none focus:border-emerald-600"
          >
            <option value="all">All Projects</option>
            {projects.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Task list */}
      {loading ? (
        <div className="text-center py-16 text-zinc-600 text-xs">Loading...</div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16">
          <Archive size={24} className="mx-auto text-zinc-700 mb-2" />
          <p className="text-xs text-zinc-600">
            {search || filterProject !== "all" ? "No tasks match your filters" : "No archived tasks yet"}
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {filtered.map((task) => (
            <div
              key={task._id}
              className="bg-[#111] border border-[#2a2a2a] rounded-md p-4 hover:border-[#3a3a3a] transition-colors"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <p className="text-xs text-zinc-200 font-medium">{task.title}</p>
                  {task.description && (
                    <p className="text-[10px] text-zinc-500 mt-1 leading-relaxed line-clamp-2">
                      {task.description}
                    </p>
                  )}
                </div>
                <p className="text-[10px] text-zinc-600 flex-shrink-0 whitespace-nowrap">
                  {formatDate(task.updatedAt)}
                </p>
              </div>
              <div className="flex items-center gap-1.5 mt-2.5 flex-wrap">
                <span
                  className={cn(
                    "text-[9px] px-1.5 py-0.5 rounded border font-medium",
                    PRIORITY_COLORS[task.priority]
                  )}
                >
                  {task.priority}
                </span>
                <span
                  className={cn(
                    "text-[9px] px-1.5 py-0.5 rounded font-medium",
                    ASSIGNEE_COLORS[task.assignee]
                  )}
                >
                  {task.assignee === "both" ? "JT + Eve" : task.assignee.toUpperCase()}
                </span>
                {task.project && (
                  <span className="text-[9px] text-zinc-500 px-1.5 py-0.5 bg-[#1a1a1a] rounded">
                    {task.project}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
