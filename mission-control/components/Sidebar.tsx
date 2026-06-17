"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { mobileNavInnerClassName, mobileNavShellClassName } from "@/lib/mission-control/nav-layout";
import { missionControlNav, mobileNav } from "@/lib/mission-control/routes";
import { cn } from "@/lib/utils";

export default function Sidebar() {
  const path = usePathname();

  const isActive = (item: (typeof missionControlNav)[number]) =>
    item.aliases.some((href) => (href === "/" ? path === "/" : path.startsWith(href)));

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
          {missionControlNav.map((item) => {
            const { href, icon: Icon, label, desc } = item;
            const active = isActive(item);
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
                <span className="min-w-0">
                  <span className="block">{label}</span>
                  <span className="block text-[9px] font-normal text-zinc-600">{desc}</span>
                </span>
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
      <nav className={mobileNavShellClassName}>
        <div className={mobileNavInnerClassName}>
          {mobileNav.map((item) => {
            const { href, icon: Icon, label } = item;
            const active = isActive(item);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex min-w-0 flex-col items-center justify-center gap-1 rounded-md px-1 py-2 text-center transition-colors",
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
