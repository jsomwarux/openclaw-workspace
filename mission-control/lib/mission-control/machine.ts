import { sortWorkSignals } from "./work-priority";
import type { Signal } from "./types";

export type MachineSummary = {
  cronsTotal: number;
  cronsFailed: number;
  cronsRunning: number;
  agentsActive: number;
  costAlerts: number;
  risks: number;
};

export type MachineGroups = {
  crons: Signal[];
  agents: Signal[];
  costs: Signal[];
  work: Signal[];
};

function isMachineSignal(signal: Signal) {
  return signal.lane === "machine";
}

function isRisk(signal: Signal) {
  return ["failed", "blocked", "stale"].includes(signal.status) || signal.priority === "high";
}

function isCostSignal(signal: Signal) {
  const text = `${signal.project ?? ""} ${signal.title} ${signal.context ?? ""}`.toLowerCase();
  return /(cost|spend|budget|openrouter|token|runaway|api usage)/.test(text);
}

export function machineSummary(signals: Signal[]): MachineSummary {
  const machineSignals = signals.filter(isMachineSignal);
  const crons = machineSignals.filter((signal) => signal.source === "cron");
  const agents = machineSignals.filter((signal) => signal.source === "agent");
  const costs = machineSignals.filter(isCostSignal);

  return {
    cronsTotal: crons.length,
    cronsFailed: crons.filter((signal) => signal.status === "failed").length,
    cronsRunning: crons.filter((signal) => signal.status === "in-progress").length,
    agentsActive: agents.filter((signal) => signal.status === "in-progress").length,
    costAlerts: costs.filter((signal) => signal.status !== "done" || signal.priority === "high").length,
    risks: machineSignals.filter(isRisk).length,
  };
}

export function machineGroups(signals: Signal[]): MachineGroups {
  const groups: MachineGroups = {
    crons: [],
    agents: [],
    costs: [],
    work: [],
  };

  for (const signal of sortWorkSignals(signals.filter(isMachineSignal))) {
    if (signal.source === "cron") groups.crons.push(signal);
    else if (signal.source === "agent") groups.agents.push(signal);
    else if (isCostSignal(signal)) groups.costs.push(signal);
    else groups.work.push(signal);
  }

  return groups;
}
