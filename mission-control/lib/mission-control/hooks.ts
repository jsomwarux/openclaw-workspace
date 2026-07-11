"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { agentToSignal, cronToSignal, proofToSignal, taskToSignal } from "./adapters";
import { cashStrip, type CashStrip } from "./cash-strip";
import { commandBrief } from "./command-brief";
import { commandQueue } from "./score";
import type { Signal } from "./types";

type RevenueResponse = {
  metrics?: { totalCollected: number; weightedForecast: number };
  available?: { northStar?: boolean };
};

type ApiState = {
  tasks: any[];
  crons: any[];
  proofs: any[];
  agents: any[];
  costs: any | null;
  revenueFile: RevenueResponse | null;
};

type RouteKey = keyof ApiState;

const EMPTY_STATE: ApiState = {
  tasks: [],
  crons: [],
  proofs: [],
  agents: [],
  costs: null,
  revenueFile: null,
};

const POLL_MS = 60_000;
const EVE_IN_FLIGHT = ["in-progress", "failed", "stale"];

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

    const [tasks, crons, proofs, agents, costs, revenueFile] = await Promise.all([
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
      fetchJson("/api/revenue")
        .catch((error) => {
          nextErrors.revenueFile = error.message;
          return previous.revenueFile;
        }),
    ]);

    setData({ tasks, crons, proofs, agents, costs, revenueFile });
    setErrors(nextErrors);
    setLastUpdated(Date.now());
    setLoading(false);
  }, []);

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, POLL_MS);
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
    () => signals.filter((signal) => signal.owner === "eve" && EVE_IN_FLIGHT.includes(signal.status)).slice(0, 8),
    [signals],
  );

  const waitingOn = useMemo(
    () =>
      signals
        .filter((signal) => Boolean(signal.waitingOn?.who))
        .sort((a, b) => (a.waitingOn?.since ?? 0) - (b.waitingOn?.since ?? 0)),
    [signals],
  );

  const risk = useMemo(
    () =>
      signals
        .filter((signal) => ["failed", "stale", "blocked"].includes(signal.status))
        .sort((a, b) => b.updatedAt - a.updatedAt)
        .slice(0, 8),
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

  const cash = useMemo<CashStrip>(() => {
    const metrics = data.revenueFile?.metrics ?? null;
    const available = Boolean(data.revenueFile?.available?.northStar) && !errors.revenueFile;
    return cashStrip({ metrics, available, now: Date.now() });
  }, [data.revenueFile, errors.revenueFile]);

  // Before the first response lands there is nothing to be unavailable about.
  const cashPending = loading && data.revenueFile === null;

  const brief = useMemo(() => commandBrief({ queue, signals, revenue }), [queue, revenue, signals]);

  return {
    ...data,
    signals,
    queue,
    eveHandling,
    waitingOn,
    risk,
    revenue,
    cash,
    cashPending,
    brief,
    loading,
    errors,
    degraded: Object.keys(errors),
    lastUpdated,
    refresh,
  };
}

export type AuditEntry = {
  _id: string;
  taskId: string;
  field: string;
  oldValue: string;
  newValue: string;
  evidence: string;
  source: "eve" | "jt" | "model";
  ts: number;
};

/** The rank audit is the drawer's receipt for a score. It loads only when a task is open. */
export function useTaskAudit(taskId: string | null) {
  const [entries, setEntries] = useState<AuditEntry[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!taskId) {
      setEntries([]);
      return;
    }

    let cancelled = false;
    setLoading(true);

    fetchJson(`/api/task-audit?taskId=${encodeURIComponent(taskId)}`)
      .then((json) => {
        if (cancelled) return;
        const rows: AuditEntry[] = json.entries ?? [];
        setEntries([...rows].sort((a, b) => b.ts - a.ts));
      })
      .catch(() => {
        if (!cancelled) setEntries([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [taskId]);

  return { entries, loading };
}
