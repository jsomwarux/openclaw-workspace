"use client";
import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { CheckSquare, Calendar, Brain, Users, FileText, ArrowRight, RotateCcw } from "lucide-react";

export default function OverviewPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [crons, setCrons] = useState<any[]>([]);
  const [proofs, setProofs] = useState<any[]>([]);
  const [showRestartConfirm, setShowRestartConfirm] = useState(false);
  const [restarting, setRestarting] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

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

  const handleRestartGateway = async () => {
    setShowRestartConfirm(false);
    setRestarting(true);
    try {
      const res = await fetch("/api/gateway/restart", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        setToast({ message: "Gateway restart initiated", type: "success" });
      } else {
        setToast({ message: data.error || "Restart failed", type: "error" });
      }
    } catch {
      setToast({ message: "Failed to reach API", type: "error" });
    } finally {
      setRestarting(false);
      setTimeout(() => setToast(null), 4000);
    }
  };

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
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-zinc-100">Mission Control</h1>
          <p className="text-xs text-zinc-500 mt-1">
            Eve & JT — {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
          </p>
        </div>
        <button
          onClick={() => setShowRestartConfirm(true)}
          disabled={restarting}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-red-600/80 hover:bg-red-600 disabled:opacity-50 text-white text-xs rounded font-medium transition-colors active:scale-[.97]"
        >
          <RotateCcw size={12} className={restarting ? "animate-spin" : ""} />
          {restarting ? "Restarting…" : "Restart Gateway"}
        </button>
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

      {/* Gateway Restart Confirmation */}
      {showRestartConfirm && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-end sm:items-center justify-center" onClick={() => setShowRestartConfirm(false)}>
          <div onClick={e => e.stopPropagation()} className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-t-xl sm:rounded-lg p-5 w-full sm:max-w-sm space-y-4">
            <h2 className="text-sm font-semibold text-zinc-200">Restart Gateway?</h2>
            <p className="text-xs text-zinc-400">The assistant will be briefly offline.</p>
            <div className="flex justify-end gap-2">
              <button onClick={() => setShowRestartConfirm(false)} className="px-3 py-2 text-xs text-zinc-400 hover:text-zinc-200 transition-colors">Cancel</button>
              <button onClick={handleRestartGateway} className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-xs rounded font-medium transition-colors">Restart</button>
            </div>
          </div>
        </div>
      )}

      {/* Toast */}
      {toast && (
        <div className={`fixed bottom-20 md:bottom-6 right-6 z-50 px-4 py-2.5 rounded-lg text-xs font-medium border ${
          toast.type === "success"
            ? "bg-emerald-950/90 text-emerald-300 border-emerald-800"
            : "bg-red-950/90 text-red-300 border-red-800"
        }`}>
          {toast.message}
        </div>
      )}
    </div>
  );
}
