"use client";
import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { CheckSquare, Calendar, Brain, Users, FileText, ArrowRight } from "lucide-react";

export default function OverviewPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [crons, setCrons] = useState<any[]>([]);
  const [proofs, setProofs] = useState<any[]>([]);

  const fetchAll = useCallback(async () => {
    const [tasksRes, cronsRes, proofsRes] = await Promise.all([
      fetch("/api/tasks").then(r => r.json()),
      fetch("/api/cron").then(r => r.json()),
      fetch("/api/proofs?limit=5").then(r => r.json()),
    ]);
    setTasks(tasksRes.tasks ?? []);
    setCrons(cronsRes.jobs ?? []);
    setProofs(proofsRes.entries ?? []);
  }, []);

  useEffect(() => {
    fetchAll();
    const poll = setInterval(fetchAll, 10000);
    return () => clearInterval(poll);
  }, [fetchAll]);

  const todo = (tasks ?? []).filter(t => t.status === "todo").length;
  const inProgress = (tasks ?? []).filter(t => t.status === "in-progress").length;
  const done = (tasks ?? []).filter(t => t.status === "done").length;
  const failing = crons.filter(j => j.failed).length;

  const stats = [
    { label: "To Do",           value: todo,          color: "text-zinc-300",   href: "/tasks"    },
    { label: "In Progress",     value: inProgress,    color: "text-yellow-400", href: "/tasks"    },
    { label: "Completed",       value: done,          color: "text-emerald-400",href: "/tasks"    },
    { label: "Cron Jobs",       value: crons.length,  color: "text-zinc-300",   href: "/calendar" },
    { label: "Failed Jobs",     value: failing,       color: failing > 0 ? "text-red-400" : "text-zinc-500", href: "/calendar" },
    { label: "Proofs Today",    value: proofs.length, color: "text-zinc-300",   href: "/audit"    },
  ];

  const quickLinks = [
    { href: "/tasks",    icon: CheckSquare, label: "Task Board",    desc: "Manage shared task queue" },
    { href: "/calendar", icon: Calendar,    label: "Schedule",      desc: "Cron jobs and automations" },
    { href: "/memory",   icon: Brain,       label: "Memory",        desc: "Search Eve's memory" },
    { href: "/agents",   icon: Users,       label: "Agent Team",    desc: "All agents and their status" },
    { href: "/audit",    icon: FileText,    label: "Audit Trail",   desc: "Every significant action logged" },
  ];

  return (
    <div className="p-4 sm:p-6 max-w-5xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-zinc-100">Mission Control</h1>
        <p className="text-xs text-zinc-500 mt-1">
          Eve & JT — {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
        </p>
      </div>

      {/* Stats grid — 2 cols on mobile, 3 on sm+ */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
        {stats.map(s => (
          <Link
            key={s.label}
            href={s.href}
            className="bg-[#111] border border-[#2a2a2a] rounded-lg p-4 hover:border-[#3a3a3a] transition-colors active:scale-[.98]"
          >
            <p className={`text-2xl font-bold font-mono ${s.color}`}>{s.value}</p>
            <p className="text-[10px] text-zinc-500 mt-1">{s.label}</p>
          </Link>
        ))}
      </div>

      {/* Activity + Quick links — stacked on mobile, 2-col on sm+ */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* Active tasks */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Active Tasks</p>
            <Link href="/tasks" className="text-[10px] text-emerald-400 hover:text-emerald-300 flex items-center gap-1">
              View all <ArrowRight size={10} />
            </Link>
          </div>
          <div className="space-y-2">
            {(tasks ?? []).filter(t => t.status !== "done").slice(0, 5).map(t => (
              <div key={t._id} className="bg-[#111] border border-[#2a2a2a] rounded-md p-3">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs text-zinc-300 truncate">{t.title}</p>
                  <span className={`text-[9px] flex-shrink-0 ${t.status === "in-progress" ? "text-yellow-400" : "text-zinc-500"}`}>
                    {t.status}
                  </span>
                </div>
                {t.project && <p className="text-[9px] text-zinc-600 mt-0.5">{t.project}</p>}
              </div>
            ))}
            {(tasks ?? []).filter(t => t.status !== "done").length === 0 && (
              <p className="text-[10px] text-zinc-600 py-4 text-center">No active tasks</p>
            )}
          </div>
        </div>

        {/* Quick links */}
        <div>
          <p className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-3">Quick Access</p>
          <div className="space-y-2">
            {quickLinks.map(({ href, icon: Icon, label, desc }) => (
              <Link
                key={href}
                href={href}
                className="flex items-center gap-3 bg-[#111] border border-[#2a2a2a] rounded-md p-3 hover:border-[#3a3a3a] hover:bg-[#161616] transition-all active:scale-[.99] group"
              >
                <Icon size={14} className="text-zinc-500 group-hover:text-emerald-400 transition-colors flex-shrink-0" />
                <div className="min-w-0">
                  <p className="text-xs text-zinc-300 font-medium">{label}</p>
                  <p className="text-[10px] text-zinc-600">{desc}</p>
                </div>
                <ArrowRight size={10} className="text-zinc-700 group-hover:text-zinc-400 ml-auto flex-shrink-0 transition-colors" />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
