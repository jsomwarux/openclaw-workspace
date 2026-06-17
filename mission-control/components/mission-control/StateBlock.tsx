import { AlertTriangle, CheckCircle2, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

type StateBlockProps = {
  kind: "loading" | "empty" | "error" | "stale" | "gap";
  title: string;
  detail?: string;
  className?: string;
};

const styles = {
  loading: "border-zinc-800 bg-zinc-950/60 text-zinc-400",
  empty: "border-emerald-900/50 bg-emerald-950/10 text-emerald-300",
  error: "border-red-900/60 bg-red-950/20 text-red-300",
  stale: "border-amber-900/60 bg-amber-950/20 text-amber-300",
  gap: "border-red-900/60 bg-red-950/20 text-red-300",
};

export function StateBlock({ kind, title, detail, className }: StateBlockProps) {
  const Icon = kind === "loading" ? Loader2 : kind === "empty" ? CheckCircle2 : AlertTriangle;
  return (
    <div className={cn("rounded-lg border p-4", styles[kind], className)}>
      <div className="flex items-center gap-2 text-xs font-semibold">
        <Icon size={14} className={kind === "loading" ? "animate-spin" : ""} />
        {title}
      </div>
      {detail && <p className="mt-1 text-[11px] leading-relaxed text-zinc-500">{detail}</p>}
    </div>
  );
}
