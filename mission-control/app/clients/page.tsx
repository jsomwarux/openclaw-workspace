"use client";

import { useEffect, useMemo, useState } from "react";
import { RefreshCw } from "lucide-react";
import { ClientCard } from "@/components/mission-control/ClientCard";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { formatMoney } from "@/lib/mission-control/cash-strip";
import type { EnrichedClient } from "@/lib/mission-control/clients";
import { formatRelative } from "@/lib/utils";

const ACTIVE_STAGES = new Set(["active-delivery", "blocked", "pending"]);

function SummaryStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
      <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-zinc-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold tracking-tight text-zinc-100">{value}</p>
    </div>
  );
}

export default function ClientsPage() {
  const [clients, setClients] = useState<EnrichedClient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    try {
      const res = await fetch("/api/clients");
      if (!res.ok) throw new Error(`/api/clients returned ${res.status}`);
      const json = await res.json();
      setClients(json.clients ?? []);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "failed to load");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const sorted = useMemo(
    () =>
      [...clients].sort((a, b) => {
        if (b.openDollars !== a.openDollars) return b.openDollars - a.openDollars;
        return (b.lastTouch ?? 0) - (a.lastTouch ?? 0);
      }),
    [clients],
  );

  const summary = useMemo(() => {
    const activeCount = clients.filter((c) => ACTIVE_STAGES.has(c.stage)).length;
    const openDollars = clients.reduce((sum, c) => sum + c.openDollars, 0);
    const collected = clients.reduce((sum, c) => sum + c.collected, 0);
    const oldest = clients.reduce<number | null>((min, c) => {
      if (!c.lastTouch) return min;
      return min === null || c.lastTouch < min ? c.lastTouch : min;
    }, null);
    return { activeCount, openDollars, collected, oldest };
  }, [clients]);

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-emerald-300">Clients</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Where each client stands</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            Per-client status, open work, and collected cash — sorted by open dollars.
          </p>
        </div>
        <button
          onClick={load}
          className="flex w-fit items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 hover:border-[#38414a]"
        >
          <RefreshCw size={13} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
      </div>

      {error && <StateBlock kind="error" title="/api/clients unreachable" detail={error} className="mb-4" />}

      <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <SummaryStat label="Active clients" value={String(summary.activeCount)} />
        <SummaryStat label="Open $" value={summary.openDollars > 0 ? formatMoney(summary.openDollars) : "—"} />
        <SummaryStat label="Collected all-time" value={formatMoney(summary.collected)} />
        <SummaryStat label="Oldest untouched" value={summary.oldest ? formatRelative(summary.oldest) : "—"} />
      </div>

      {loading && clients.length === 0 ? (
        <StateBlock kind="loading" title="Loading clients" detail="Reading clients, payments, and client-scoped tasks." />
      ) : sorted.length === 0 ? (
        <StateBlock kind="empty" title="No clients on file yet" />
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {sorted.map((client) => (
            <ClientCard key={client._id} client={client} />
          ))}
        </div>
      )}
    </div>
  );
}
