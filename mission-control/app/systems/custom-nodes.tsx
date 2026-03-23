"use client";
import { memo } from "react";
import { Handle, Position, type NodeProps } from "reactflow";
import { Clock, Cpu, Send, Bell, Timer } from "lucide-react";

/* ── shared handle styles ── */
const handleStyle = { background: "#555", width: 6, height: 6, border: "none" };

/* ── theme helpers ── */
interface NodeTheme {
  bg: string;
  border: string;
  accent: string;
  text: string;
}

function themeFor(
  dark: boolean,
  accent: { dark: string; light: string; border: string; borderLight: string }
): NodeTheme {
  return {
    bg: dark ? "#1a1a1a" : "#f9fafb",
    border: dark ? accent.border : accent.borderLight,
    accent: dark ? accent.dark : accent.light,
    text: dark ? "#e4e4e7" : "#18181b",
  };
}

/* ── color palettes per node type ── */
const palettes = {
  input: { dark: "#2dd4bf", light: "#0d9488", border: "#2dd4bf55", borderLight: "#0d948855" },
  process: { dark: "#a1a1aa", light: "#52525b", border: "#52525b55", borderLight: "#a1a1aa55" },
  output: { dark: "#4ade80", light: "#16a34a", border: "#4ade8055", borderLight: "#16a34a55" },
  alert: { dark: "#fbbf24", light: "#d97706", border: "#fbbf2455", borderLight: "#d9770655" },
  cron: { dark: "#a78bfa", light: "#7c3aed", border: "#a78bfa55", borderLight: "#7c3aed55" },
};

/* ── icon map ── */
const icons = {
  input: Cpu,
  process: Cpu,
  output: Send,
  alert: Bell,
  cron: Timer,
};

/* ── generic node renderer ── */
function BaseNode({
  data,
  type,
}: NodeProps<{ label: string; dark: boolean; subtitle?: string }> & {
  type: keyof typeof palettes;
}) {
  const dark = data.dark ?? true;
  const t = themeFor(dark, palettes[type]);
  const Icon = icons[type];

  return (
    <div
      style={{
        background: t.bg,
        border: `1.5px solid ${t.border}`,
        borderRadius: 10,
        padding: "8px 14px",
        minWidth: 110,
        maxWidth: 170,
        textAlign: "center",
      }}
    >
      <Handle type="target" position={Position.Left} style={handleStyle} />
      <div style={{ display: "flex", alignItems: "center", gap: 6, justifyContent: "center" }}>
        <Icon size={13} color={t.accent} />
        <span
          style={{
            fontSize: 11,
            fontWeight: 600,
            color: t.text,
            lineHeight: "1.3",
          }}
        >
          {data.label}
        </span>
      </div>
      {data.subtitle && (
        <div
          style={{
            fontSize: 9,
            color: t.accent,
            marginTop: 3,
            fontWeight: 500,
            opacity: 0.85,
          }}
        >
          {data.subtitle}
        </div>
      )}
      <Handle type="source" position={Position.Right} style={handleStyle} />
    </div>
  );
}

/* ── exported node components ── */
export const InputNode = memo((props: NodeProps) => <BaseNode {...props} type="input" />);
InputNode.displayName = "InputNode";

export const ProcessNode = memo((props: NodeProps) => <BaseNode {...props} type="process" />);
ProcessNode.displayName = "ProcessNode";

export const OutputNode = memo((props: NodeProps) => <BaseNode {...props} type="output" />);
OutputNode.displayName = "OutputNode";

export const AlertNode = memo((props: NodeProps) => <BaseNode {...props} type="alert" />);
AlertNode.displayName = "AlertNode";

export const CronNode = memo((props: NodeProps) => <BaseNode {...props} type="cron" />);
CronNode.displayName = "CronNode";

/* ── node type registry for React Flow ── */
export const customNodeTypes = {
  inputNode: InputNode,
  processNode: ProcessNode,
  outputNode: OutputNode,
  alertNode: AlertNode,
  cronNode: CronNode,
};
