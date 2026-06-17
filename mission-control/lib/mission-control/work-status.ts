import type { SignalStatus } from "./types";

export type TaskStatus = "todo" | "in-progress" | "done";

export const statusOptions: { value: TaskStatus; label: string }[] = [
  { value: "todo", label: "Todo" },
  { value: "in-progress", label: "Doing" },
  { value: "done", label: "Done" },
];

export function toTaskStatus(status: SignalStatus): TaskStatus {
  if (status === "done") return "done";
  if (status === "in-progress") return "in-progress";
  return "todo";
}

export function statusActionLabel(status: TaskStatus): string {
  return statusOptions.find((option) => option.value === status)?.label ?? status;
}
