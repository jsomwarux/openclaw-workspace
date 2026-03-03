"use client";
import { useState, useEffect, useCallback, useRef } from "react";
import { Plus, X, ChevronDown, ChevronUp, RefreshCw, GripVertical } from "lucide-react";
import { cn, formatRelative } from "@/lib/utils";

type Status = "todo" | "in-progress" | "done";
type Priority = "high" | "medium" | "low";
type Assignee = "jt" | "eve" | "both";

type Task = {
  _id: string;
  title: string;
  description?: string;
  status: Status;
  priority: Priority;
  assignee: Assignee;
  project?: string;
  sortOrder?: number;
  updatedAt: number;
};

const COLUMNS: { id: Status; label: string; color: string }[] = [
  { id: "todo",        label: "To Do",       color: "text-zinc-400"   },
  { id: "in-progress", label: "In Progress",  color: "text-yellow-400" },
  { id: "done",        label: "Done",         color: "text-emerald-400"},
];

const PRIORITY_COLORS: Record<Priority, string> = {
  high:   "bg-red-500/20 text-red-400 border-red-500/30",
  medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  low:    "bg-zinc-700/40 text-zinc-400 border-zinc-600/30",
};

const ASSIGNEE_COLORS: Record<Assignee, string> = {
  jt:   "bg-blue-500/20 text-blue-400",
  eve:  "bg-emerald-500/20 text-emerald-400",
  both: "bg-purple-500/20 text-purple-400",
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNew, setShowNew] = useState(false);
  const [mobileCol, setMobileCol] = useState<Status>("todo");
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());
  const [dragId, setDragId] = useState<string | null>(null);
  const [form, setForm] = useState({
    title: "", description: "", status: "todo" as Status,
    assignee: "jt" as Assignee, priority: "medium" as Priority, project: "",
  });
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      const r = await fetch("/api/tasks");
      const d = await r.json();
      setTasks(d.tasks ?? []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
    pollRef.current = setInterval(fetchTasks, 5000);
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [fetchTasks]);

  function toggleExpanded(id: string) {
    setExpandedIds(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!form.title.trim()) return;
    await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: form.title.trim(),
        description: form.description || undefined,
        status: form.status,
        assignee: form.assignee,
        priority: form.priority,
        project: form.project || undefined,
      }),
    });
    setForm({ title: "", description: "", status: "todo", assignee: "jt", priority: "medium", project: "" });
    setShowNew(false);
    fetchTasks();
  }

  async function handleStatusChange(id: string, status: Status) {
    // Optimistic update
    setTasks(prev => prev.map(t => t._id === id ? { ...t, status } : t));
    await fetch("/api/tasks", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, status }),
    });
    fetchTasks();
  }

  async function handleRemove(id: string) {
    // Optimistic update
    setTasks(prev => prev.filter(t => t._id !== id));
    await fetch(`/api/tasks?id=${encodeURIComponent(id)}`, { method: "DELETE" });
  }

  function byStatus(status: Status) {
    return tasks.filter(t => t.status === status).sort((a, b) => {
      const order = { high: 0, medium: 1, low: 2 };
      const priorityDiff = order[a.priority] - order[b.priority];
      if (priorityDiff !== 0) return priorityDiff;
      // Within same priority: use explicit sortOrder, then createdAt ascending
      const aSort = a.sortOrder ?? 999;
      const bSort = b.sortOrder ?? 999;
      return aSort - bSort;
    });
  }

  function handleDragStart(id: string) { setDragId(id); }
  function handleDragOver(e: React.DragEvent) { e.preventDefault(); }
  async function handleDrop(status: Status) {
    if (!dragId) return;
    await handleStatusChange(dragId, status);
    setDragId(null);
  }

  const TaskCard = ({ task }: { task: Task }) => {
    const dragFromHandle = useRef(false);
    return (
    <div
      draggable
      onDragStart={(e) => {
        if (!dragFromHandle.current) { e.preventDefault(); return; }
        dragFromHandle.current = false;
        handleDragStart(task._id);
      }}
      onDragEnd={() => { dragFromHandle.current = false; }}
      className="group bg-[#1a1a1a] border border-[#2a2a2a] hover:border-[#3a3a3a] rounded-md p-3 transition-all select-text"
    >
      <div className="flex items-start gap-2">
        {/* Drag handle — only this triggers drag on desktop */}
        <div
          className="hidden md:flex items-center flex-shrink-0 mt-0.5 cursor-grab active:cursor-grabbing text-zinc-700 hover:text-zinc-400 transition-colors"
          onPointerDown={() => { dragFromHandle.current = true; }}
        >
          <GripVertical size={12} />
        </div>
        <p className="text-xs text-zinc-200 font-medium leading-relaxed flex-1">{task.title}</p>
        <button
          onClick={() => handleRemove(task._id)}
          className="opacity-0 group-hover:opacity-100 transition-opacity text-zinc-600 hover:text-red-400 flex-shrink-0 p-0.5"
        ><X size={11} /></button>
      </div>

      {task.description && (
        <>
          <button
            onClick={e => { e.stopPropagation(); toggleExpanded(task._id); }}
            className="flex items-center gap-1 mt-1.5 text-[9px] text-zinc-500 hover:text-emerald-400 transition-colors"
          >
            {expandedIds.has(task._id)
              ? <><ChevronUp size={9} /> Hide steps</>
              : <><ChevronDown size={9} /> View steps</>
            }
          </button>
          {expandedIds.has(task._id) && (
            <p className="text-[10px] text-zinc-500 mt-1.5 leading-relaxed whitespace-pre-wrap border-t border-[#2a2a2a] pt-1.5">{task.description}</p>
          )}
        </>
      )}

      <div className="flex items-center gap-1.5 mt-2 flex-wrap">
        <span className={cn("text-[9px] px-1.5 py-0.5 rounded border font-medium", PRIORITY_COLORS[task.priority])}>
          {task.priority}
        </span>
        <span className={cn("text-[9px] px-1.5 py-0.5 rounded font-medium", ASSIGNEE_COLORS[task.assignee])}>
          {task.assignee === "both" ? "JT + Eve" : task.assignee.toUpperCase()}
        </span>
        {task.project && (
          <span className="text-[9px] text-zinc-500 px-1.5 py-0.5 bg-[#222] rounded">{task.project}</span>
        )}
      </div>

      {/* Mobile: quick status change buttons */}
      <div className="md:hidden flex gap-1 mt-2 pt-2 border-t border-[#2a2a2a]">
        {COLUMNS.filter(c => c.id !== task.status).map(c => (
          <button
            key={c.id}
            onClick={() => handleStatusChange(task._id, c.id)}
            className={cn("text-[9px] px-2 py-0.5 rounded border transition-colors", 
              "border-[#333] text-zinc-500 hover:text-zinc-200 hover:border-[#444]"
            )}
          >
            → {c.label}
          </button>
        ))}
      </div>

      <p className="text-[9px] text-zinc-600 mt-1.5">{formatRelative(task.updatedAt)}</p>
    </div>
  );
  };

  return (
    <div className="p-4 sm:p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-lg font-semibold text-zinc-100">Task Board</h1>
          <p className="text-xs text-zinc-500 mt-0.5">
            {tasks.length} tasks · {byStatus("in-progress").length} in progress
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={fetchTasks} className="text-zinc-600 hover:text-zinc-400 transition-colors p-1.5">
            <RefreshCw size={12} className={loading ? "animate-spin" : ""} />
          </button>
          <button
            onClick={() => setShowNew(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-medium transition-colors active:scale-[.97]"
          >
            <Plus size={12} /> New Task
          </button>
        </div>
      </div>

      {/* New Task Modal */}
      {showNew && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-end sm:items-center justify-center" onClick={() => setShowNew(false)}>
          <form
            onSubmit={handleCreate}
            onClick={e => e.stopPropagation()}
            className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-t-xl sm:rounded-lg p-5 w-full sm:max-w-md space-y-4"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-zinc-200">New Task</h2>
              <button type="button" onClick={() => setShowNew(false)} className="p-1"><X size={14} className="text-zinc-500" /></button>
            </div>
            <input
              autoFocus
              placeholder="Task title..."
              value={form.title}
              onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
              className="w-full bg-[#111] border border-[#333] rounded px-3 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-600"
            />
            <textarea
              placeholder="Description (optional)..."
              value={form.description}
              onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
              rows={2}
              className="w-full bg-[#111] border border-[#333] rounded px-3 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-600 resize-none"
            />
            <input
              placeholder="Project (optional)..."
              value={form.project}
              onChange={e => setForm(f => ({ ...f, project: e.target.value }))}
              className="w-full bg-[#111] border border-[#333] rounded px-3 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-600"
            />
            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="text-[10px] text-zinc-500 block mb-1">Assignee</label>
                <select value={form.assignee} onChange={e => setForm(f => ({ ...f, assignee: e.target.value as Assignee }))}
                  className="w-full bg-[#111] border border-[#333] rounded px-2 py-2 text-xs text-zinc-100 focus:outline-none focus:border-emerald-600">
                  <option value="jt">JT</option>
                  <option value="eve">Eve</option>
                  <option value="both">Both</option>
                </select>
              </div>
              <div>
                <label className="text-[10px] text-zinc-500 block mb-1">Priority</label>
                <select value={form.priority} onChange={e => setForm(f => ({ ...f, priority: e.target.value as Priority }))}
                  className="w-full bg-[#111] border border-[#333] rounded px-2 py-2 text-xs text-zinc-100 focus:outline-none focus:border-emerald-600">
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>
              <div>
                <label className="text-[10px] text-zinc-500 block mb-1">Status</label>
                <select value={form.status} onChange={e => setForm(f => ({ ...f, status: e.target.value as Status }))}
                  className="w-full bg-[#111] border border-[#333] rounded px-2 py-2 text-xs text-zinc-100 focus:outline-none focus:border-emerald-600">
                  <option value="todo">To Do</option>
                  <option value="in-progress">In Progress</option>
                  <option value="done">Done</option>
                </select>
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <button type="button" onClick={() => setShowNew(false)} className="px-3 py-2 text-xs text-zinc-400 hover:text-zinc-200 transition-colors">Cancel</button>
              <button type="submit" className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-medium transition-colors">Create</button>
            </div>
          </form>
        </div>
      )}

      {/* ── Mobile: tab switcher ── */}
      <div className="md:hidden">
        <div className="flex border border-[#2a2a2a] rounded-lg overflow-hidden mb-4">
          {COLUMNS.map(col => (
            <button
              key={col.id}
              onClick={() => setMobileCol(col.id)}
              className={cn(
                "flex-1 py-2.5 text-xs font-medium transition-colors",
                mobileCol === col.id ? "bg-[#1a1a1a] text-zinc-200" : "text-zinc-500 hover:text-zinc-300"
              )}
            >
              <span className={mobileCol === col.id ? col.color : ""}>{col.label}</span>
              <span className="ml-1.5 text-[9px] text-zinc-600">({byStatus(col.id).length})</span>
            </button>
          ))}
        </div>
        <div className="space-y-2">
          {loading ? (
            <div className="text-center py-12 text-zinc-600 text-xs">Loading...</div>
          ) : byStatus(mobileCol).length === 0 ? (
            <div className="text-center py-12 text-zinc-700 text-xs">No tasks here</div>
          ) : (
            byStatus(mobileCol).map(task => <TaskCard key={task._id} task={task} />)
          )}
        </div>
      </div>

      {/* ── Desktop: 3-column Kanban ── */}
      <div className="hidden md:grid grid-cols-3 gap-4">
        {COLUMNS.map(col => (
          <div
            key={col.id}
            onDragOver={handleDragOver}
            onDrop={() => handleDrop(col.id)}
            className="bg-[#111] border border-[#2a2a2a] rounded-lg p-3 min-h-[60vh]"
          >
            <div className="flex items-center justify-between mb-3">
              <span className={cn("text-xs font-semibold uppercase tracking-wider", col.color)}>{col.label}</span>
              <span className="text-[10px] text-zinc-600 bg-[#1a1a1a] px-1.5 py-0.5 rounded">
                {byStatus(col.id).length}
              </span>
            </div>
            <div className="space-y-2">
              {byStatus(col.id).map(task => <TaskCard key={task._id} task={task} />)}
              {byStatus(col.id).length === 0 && !loading && (
                <div className="text-center py-8 text-zinc-700 text-[10px]">empty</div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
