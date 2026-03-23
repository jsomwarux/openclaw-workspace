"use client";
import { useState, useEffect } from "react";
import { Sun, Moon, ChevronDown, ChevronRight, Timer, Cpu, Send, Bell } from "lucide-react";
import { cn } from "@/lib/utils";
import { systems } from "./systems-data";
import SystemDiagram from "./SystemDiagram";

const legendItems = [
  { label: "Input", icon: Cpu, color: "text-teal-400", bg: "bg-teal-500/15", border: "border-teal-500/40" },
  { label: "Process", icon: Cpu, color: "text-zinc-400", bg: "bg-zinc-500/15", border: "border-zinc-500/40" },
  { label: "Output", icon: Send, color: "text-green-400", bg: "bg-green-500/15", border: "border-green-500/40" },
  { label: "Alert", icon: Bell, color: "text-amber-400", bg: "bg-amber-500/15", border: "border-amber-500/40" },
  { label: "Cron", icon: Timer, color: "text-purple-400", bg: "bg-purple-500/15", border: "border-purple-500/40" },
];

export default function SystemsPage() {
  const [dark, setDark] = useState(true);
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  useEffect(() => {
    const saved = localStorage.getItem("systems-theme");
    if (saved === "light") setDark(false);
  }, []);

  const toggle = () => {
    const next = !dark;
    setDark(next);
    localStorage.setItem("systems-theme", next ? "dark" : "light");
  };

  const toggleSection = (name: string) => {
    setCollapsed((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  return (
    <div
      className={cn(
        "min-h-screen transition-colors duration-200",
        dark ? "bg-[#0d0d0d]" : "bg-white"
      )}
    >
      <div className="p-4 sm:p-6 max-w-[1200px]">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1
              className={cn(
                "text-xl font-bold tracking-tight",
                dark ? "text-zinc-100" : "text-zinc-900"
              )}
            >
              Eve OS — System Architecture
            </h1>
            <p
              className={cn(
                "text-xs mt-1",
                dark ? "text-zinc-500" : "text-zinc-400"
              )}
            >
              8 automated systems running 24/7
            </p>
          </div>
          <button
            onClick={toggle}
            className={cn(
              "flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors",
              dark
                ? "bg-[#1a1a1a] border-[#2a2a2a] text-zinc-300 hover:bg-[#222]"
                : "bg-white border-gray-200 text-zinc-600 hover:bg-gray-50"
            )}
          >
            {dark ? <Moon size={14} /> : <Sun size={14} />}
            {dark ? "Dark" : "Light"}
          </button>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-2 mb-6">
          {legendItems.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.label}
                className={cn(
                  "flex items-center gap-1.5 px-2 py-1 rounded border text-[10px] font-medium",
                  item.bg,
                  item.border
                )}
              >
                <Icon size={10} className={item.color} />
                <span className={dark ? "text-zinc-300" : "text-zinc-600"}>
                  {item.label}
                </span>
              </div>
            );
          })}
        </div>

        {/* Systems */}
        <div className="space-y-3">
          {systems.map((sys) => {
            const isCollapsed = collapsed[sys.name] ?? false;
            return (
              <div
                key={sys.name}
                className={cn(
                  "rounded-xl border transition-colors",
                  dark
                    ? "bg-[#111] border-[#2a2a2a]"
                    : "bg-gray-50 border-gray-200"
                )}
              >
                {/* Section header */}
                <button
                  onClick={() => toggleSection(sys.name)}
                  className={cn(
                    "w-full flex items-center gap-3 px-5 py-4 text-left transition-colors rounded-xl",
                    dark ? "hover:bg-[#1a1a1a]" : "hover:bg-gray-100"
                  )}
                >
                  {isCollapsed ? (
                    <ChevronRight
                      size={16}
                      className={dark ? "text-zinc-500" : "text-zinc-400"}
                    />
                  ) : (
                    <ChevronDown
                      size={16}
                      className={dark ? "text-zinc-500" : "text-zinc-400"}
                    />
                  )}
                  <div>
                    <h2
                      className={cn(
                        "text-sm font-bold tracking-tight",
                        dark ? "text-zinc-100" : "text-zinc-900"
                      )}
                    >
                      {sys.name}
                    </h2>
                    <p
                      className={cn(
                        "text-[11px] mt-0.5",
                        dark ? "text-zinc-500" : "text-zinc-400"
                      )}
                    >
                      {sys.subtitle}
                    </p>
                  </div>
                </button>

                {/* Diagram */}
                {!isCollapsed && (
                  <div className="px-5 pb-5">
                    <SystemDiagram
                      nodes={sys.nodes}
                      edges={sys.edges}
                      dark={dark}
                      width={sys.width}
                      height={sys.height}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
