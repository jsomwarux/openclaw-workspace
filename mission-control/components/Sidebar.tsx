"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, CheckSquare, Calendar, Brain,
  Users, Server, DollarSign, FileText, Moon, Wrench, Archive, Building2, Sparkles, Network, Coins,
} from "lucide-react";
import { cn } from "@/lib/utils";

const nav = [
  { href: "/",         icon: LayoutDashboard, label: "Overview"   },
  { href: "/tasks",    icon: CheckSquare,      label: "Tasks"      },
  { href: "/consulting", icon: Building2,      label: "Pipeline"   },
  { href: "/vibe",       icon: Sparkles,       label: "Vibe Mktg"  },
  { href: "/passive-income", icon: Coins,      label: "Passive $"  },
  { href: "/calendar", icon: Calendar,         label: "Schedule"   },
  { href: "/memory",   icon: Brain,            label: "Memory"     },
  { href: "/agents",   icon: Users,            label: "Agents"     },
  { href: "/monitor",  icon: Server,           label: "Monitor"    },
  { href: "/costs",    icon: DollarSign,       label: "Costs"      },
  { href: "/history",  icon: Archive,          label: "History"    },
  { href: "/audit",    icon: FileText,         label: "Audit"      },
  { href: "/overnight", icon: Moon,            label: "Overnight"  },
  { href: "/skills",    icon: Wrench,          label: "Skills"     },
  { href: "/systems",   icon: Network,         label: "Systems"    },
];

// Primary nav items shown in bottom bar (mobile)
const mobileNav = nav.slice(0, 5);

export default function Sidebar() {
  const path = usePathname();

  const isActive = (href: string) =>
    href === "/" ? path === "/" : path.startsWith(href);

  return (
    <>
      {/* ── Desktop sidebar ── */}
      <aside className="hidden md:flex fixed left-0 top-0 h-screen w-52 flex-col border-r border-[#2a2a2a] bg-[#0d0d0d] z-40">
        {/* Logo */}
        <div className="px-5 py-5 border-b border-[#2a2a2a]">
          <div className="flex items-center gap-2">
            <span className="text-accent text-lg font-semibold tracking-tight">🤖 Eve</span>
          </div>
          <p className="text-[10px] text-zinc-500 mt-0.5 tracking-widest uppercase">Mission Control</p>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
          {nav.map(({ href, icon: Icon, label }) => {
            const active = isActive(href);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded text-xs transition-all",
                  active
                    ? "bg-emerald-950/60 text-emerald-400 font-medium"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-white/5"
                )}
              >
                <Icon size={14} />
                {label}
              </Link>
            );
          })}
        </nav>

        {/* Status footer */}
        <div className="px-4 py-3 border-t border-[#2a2a2a]">
          <div className="flex items-center gap-2 text-[10px] text-zinc-500">
            <span className="status-dot bg-emerald-400 glow" />
            Eve · online
          </div>
        </div>
      </aside>

      {/* ── Mobile top bar ── */}
      <header className="md:hidden fixed top-0 left-0 right-0 h-12 flex items-center px-4 border-b border-[#2a2a2a] bg-[#0d0d0d] z-40">
        <span className="text-sm font-semibold text-emerald-400 tracking-tight">🤖 Mission Control</span>
      </header>

      {/* ── Mobile bottom nav ── */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-[#0d0d0d] border-t border-[#2a2a2a] z-40">
        <div className="flex items-center h-full overflow-x-auto scrollbar-none px-1">
          {nav.map(({ href, icon: Icon, label }) => {
            const active = isActive(href);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex-shrink-0 flex flex-col items-center justify-center gap-1 py-2 px-3 transition-colors min-w-[60px]",
                  active ? "text-emerald-400" : "text-zinc-500 hover:text-zinc-300"
                )}
              >
                <Icon size={18} />
                <span className="text-[9px] font-medium whitespace-nowrap">{label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
