import Link from "next/link";
import { AlertTriangle } from "lucide-react";
import { formatMoney } from "@/lib/mission-control/cash-strip";
import { stageBadgeClassName, stageLabel, type EnrichedClient } from "@/lib/mission-control/clients";
import { cn, formatRelative } from "@/lib/utils";

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0">
      <p className="font-mono text-[9px] uppercase tracking-[0.14em] text-zinc-600">{label}</p>
      <p className="mt-1 truncate text-sm font-semibold text-zinc-100">{value}</p>
    </div>
  );
}

export function ClientCard({ client }: { client: EnrichedClient }) {
  const blocked = client.stage === "blocked";
  const waitingWho = client.waitingOn?.who ?? "client";

  return (
    <Link
      href={`/clients/${client.slug}`}
      className="block rounded-lg border border-[#20262d] bg-[#0d1014] p-4 transition-colors hover:border-[#38414a]"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-center gap-2">
          <span className="text-lg leading-none">{client.emoji ?? "🧩"}</span>
          <p className="truncate text-base font-semibold text-zinc-100">{client.name}</p>
        </div>
        <span
          className={cn(
            "shrink-0 rounded border px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide",
            stageBadgeClassName(client.stage),
          )}
        >
          {stageLabel[client.stage]}
        </span>
      </div>

      {client.status && (
        <p className="mt-2 line-clamp-2 text-xs leading-relaxed text-zinc-500">{client.status}</p>
      )}

      {blocked && (
        <div className="mt-3 flex w-fit items-center gap-1.5 rounded border border-red-500/40 bg-red-500/10 px-2 py-1 text-[10px] font-medium text-red-300">
          <AlertTriangle size={11} />
          Waiting on {waitingWho}
        </div>
      )}

      <div className="mt-4 grid grid-cols-4 gap-3 border-t border-[#16191d] pt-3">
        <Stat label="Last touch" value={client.lastTouch ? formatRelative(client.lastTouch) : "—"} />
        <Stat label="Open tasks" value={String(client.openTaskCount)} />
        <Stat label="Open $" value={client.openDollars > 0 ? formatMoney(client.openDollars) : "—"} />
        <Stat label="Collected" value={client.collected > 0 ? formatMoney(client.collected) : "—"} />
      </div>
    </Link>
  );
}
