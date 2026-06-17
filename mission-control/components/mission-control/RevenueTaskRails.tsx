"use client";

import { useEffect, useMemo, useState } from "react";
import { revenueTasks } from "@/lib/mission-control/revenue";

type Task = {
  title: string;
  project?: string;
  priority?: string;
  status?: string;
  description?: string;
};

function TaskRail({ title, tasks, empty }: { title: string; tasks: Task[]; empty: string }) {
  return (
    <section>
      <h2 className="mb-3 text-sm font-semibold text-zinc-100">{title}</h2>
      <div className="space-y-2">
        {tasks.length === 0 ? (
          <div className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4 text-xs text-zinc-500">{empty}</div>
        ) : (
          tasks.map((task) => (
            <div key={`${task.project}-${task.title}`} className="rounded-lg border border-[#20262d] bg-[#0d1014] p-3">
              <div className="flex items-start justify-between gap-3">
                <p className="min-w-0 truncate text-sm font-medium text-zinc-100">{task.title}</p>
                <span className="shrink-0 rounded bg-[#16191d] px-2 py-1 text-[10px] uppercase text-zinc-500">{task.priority ?? "none"}</span>
              </div>
              <p className="mt-1 line-clamp-2 text-[11px] leading-relaxed text-zinc-600">{task.description || task.project || task.status}</p>
            </div>
          ))
        )}
      </div>
    </section>
  );
}

export function RevenueTaskRails() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let live = true;
    fetch("/api/tasks")
      .then((response) => response.json())
      .then((data) => {
        if (live) setTasks(data.tasks ?? []);
      })
      .finally(() => {
        if (live) setLoading(false);
      });
    return () => {
      live = false;
    };
  }, []);

  const grouped = useMemo(() => revenueTasks(tasks), [tasks]);

  if (loading) {
    return (
      <div className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4 text-xs text-zinc-500">
        Loading live job and app upside tasks.
      </div>
    );
  }

  return (
    <>
      <TaskRail title="Job Upside" tasks={grouped.jobUpside} empty="No active job applications found." />
      <TaskRail title="App Upside" tasks={grouped.appUpside} empty="No active app marketing tasks found." />
    </>
  );
}
