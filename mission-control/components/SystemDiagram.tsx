"use client";
import { Clock, Cpu, Database, Send, User } from "lucide-react";
import { cn } from "@/lib/utils";

export type NodeType = "trigger" | "process" | "storage" | "output" | "manual";

export interface DiagramNode {
  label: string;
  type: NodeType;
}

const nodeConfig: Record<
  NodeType,
  { icon: typeof Clock; bg: string; border: string; text: string }
> = {
  trigger: {
    icon: Clock,
    bg: "bg-blue-500/20",
    border: "border-blue-500/50",
    text: "text-blue-400",
  },
  process: {
    icon: Cpu,
    bg: "bg-purple-500/20",
    border: "border-purple-500/50",
    text: "text-purple-400",
  },
  storage: {
    icon: Database,
    bg: "bg-amber-500/20",
    border: "border-amber-500/50",
    text: "text-amber-400",
  },
  output: {
    icon: Send,
    bg: "bg-green-500/20",
    border: "border-green-500/50",
    text: "text-green-400",
  },
  manual: {
    icon: User,
    bg: "bg-orange-500/20",
    border: "border-orange-500/50",
    text: "text-orange-400",
  },
};

interface SystemDiagramProps {
  nodes: DiagramNode[];
  dark: boolean;
}

export default function SystemDiagram({ nodes, dark }: SystemDiagramProps) {
  const arrowColor = dark ? "#525252" : "#a1a1aa";

  return (
    <div className="flex items-center gap-1.5 overflow-x-auto pb-2 scrollbar-thin">
      {nodes.map((node, i) => {
        const config = nodeConfig[node.type];
        const Icon = config.icon;
        return (
          <div key={i} className="flex items-center gap-1.5 flex-shrink-0">
            <div
              className={cn(
                "flex items-center gap-2 px-3 py-2 rounded-lg border text-[11px] font-medium",
                config.bg,
                config.border
              )}
            >
              <Icon size={13} className={config.text} />
              <span className={dark ? "text-zinc-200" : "text-zinc-700"}>
                {node.label}
              </span>
            </div>
            {i < nodes.length - 1 && (
              <svg
                width="28"
                height="12"
                viewBox="0 0 28 12"
                className="flex-shrink-0"
              >
                <line
                  x1="2"
                  y1="6"
                  x2="20"
                  y2="6"
                  stroke={arrowColor}
                  strokeWidth="1.5"
                />
                <polyline
                  points="16,2 22,6 16,10"
                  fill="none"
                  stroke={arrowColor}
                  strokeWidth="1.5"
                />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  );
}
