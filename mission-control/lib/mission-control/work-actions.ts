import type { Signal, SignalPriority } from "./types";
import type { TaskStatus } from "./work-status";

export const priorityOptions: { value: SignalPriority; label: string }[] = [
  { value: "high", label: "High" },
  { value: "medium", label: "Medium" },
  { value: "low", label: "Low" },
];

export function deferTaskPatch(): { priority: SignalPriority; status: TaskStatus } {
  return { priority: "low", status: "todo" };
}

export function rankingExplanation(signal: Signal): string {
  const pieces = [
    signal.priority ? `${capitalize(signal.priority)} priority` : "No priority set",
    `status ${signal.status}`,
    `${signal.ageDays} days old`,
  ];

  if (signal.project) pieces.push(signal.project);
  if (signal.owner) pieces.push(`${signal.owner.toUpperCase()} owned`);

  return pieces.join(" · ");
}

function capitalize(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1);
}
