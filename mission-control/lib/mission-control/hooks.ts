"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { agentToSignal, cronToSignal, proofToSignal, taskToSignal } from "./adapters";
import { commandBrief } from "./command-brief";
import { commandQueue } from "./score";
import type { Signal } from "./types";

type ApiState = {
  tasks: any[];
  crons: any[];
  proofs: any[];
  agents: any[];
  costs: any | null;
};

type RouteKey = keyof ApiState;

const EMPTY_STATE: ApiState = {
  tasks: [],
  crons: [],
  proofs: [],
  agents: [],
  costs: null,
};

async function fetchJson(path: string) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${path} returned ${res.status}`);
  return res.json();
}

export function useMissionControlData() {
  const [data, setData] = useState<ApiState>(EMPTY_STATE);
  const dataRef = useRef<ApiState>(EMPTY_STATE);
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState<Partial<Record<RouteKey, string>>>({});
  const [lastUpdated, setLastUpdated] = useState<number | null>(null);

  useEffect(() => {
    dataRef.current = data;
  }, [data]);

  const refresh = useCallback(async () => {
    const nextErrors: Partial<Record<RouteKey, string>> = {};
    const previous = dataRef.current;

    const [tasks, crons, proofs, agents, costs] = await Promise.all([
      fetchJson("/api/tasks")
        .then((json) => json.tasks ?? [])
        .catch((error) => {
          nextErrors.tasks = error.message;
          return previous.tasks;
        }),
      fetchJson("/api/cron")
        .then((json) => json.jobs ?? [])
        .catch((error) => {
          nextErrors.crons = error.message;
          return previous.crons;
        }),
      fetchJson("/api/proofs?limit=20")
        .then((json) => json.entries ?? [])
        .catch((error) => {
          nextErrors.proofs = error.message;
          return previous.proofs;
        }),
      fetchJson("/api/agents")
        .then((json) => json.agents ?? [])
        .catch((error) => {
          nextErrors.agents = error.message;
          return previous.agents;
        }),
      fetchJson("/api/costs")
        .catch((error) => {
          nextErrors.costs = error.message;
          return previous.costs;
        }),
    ]);

    setData({ tasks, crons, proofs, agents, costs });
    setErrors(nextErrors);
    setLastUpdated(Date.now());
    setLoading(false);
  }, []);

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 30_000);
    return () => clearInterval(interval);
  }, [refresh]);

  const signals = useMemo<Signal[]>(() => {
    return [
      ...data.tasks.map(taskToSignal),
      ...data.crons.map(cronToSignal),
      ...data.proofs.map(proofToSignal),
      ...data.agents.map(agentToSignal),
    ];
  }, [data.agents, data.crons, data.proofs, data.tasks]);

  const queue = useMemo(() => commandQueue(signals), [signals]);
  const eveHandling = useMemo(
    () => signals.filter((signal) => signal.owner === "eve" && signal.status === "in-progress").slice(0, 6),
    [signals],
  );
  const risk = useMemo(
    () =>
      signals
        .filter((signal) => ["failed", "stale", "blocked"].includes(signal.status))
        .sort((a, b) => b.updatedAt - a.updatedAt)
        .slice(0, 6),
    [signals],
  );

  const revenue = useMemo(() => {
    const revenueTasks = data.tasks.filter((task) => {
      const text = `${task.project ?? ""} ${task.title ?? ""}`.toLowerCase();
      return /(consult|pipeline|job|apply|client|altmark|revenue|sales|outreach)/.test(text);
    });
    return {
      active: revenueTasks.filter((task) => task.status !== "done" && task.status !== "archived").length,
      high: revenueTasks.filter((task) => task.priority === "high").length,
      done: revenueTasks.filter((task) => task.status === "done").length,
      costToday: data.costs?.today?.total_usd ?? null,
      costAlerts: data.costs?.alerts ?? [],
    };
  }, [data.costs, data.tasks]);

  const brief = useMemo(() => commandBrief({ queue, signals, revenue }), [queue, revenue, signals]);

  return {
    ...data,
    signals,
    queue,
    eveHandling,
    risk,
    revenue,
    brief,
    loading,
    errors,
    degraded: Object.keys(errors),
    lastUpdated,
    refresh,
  };
}
