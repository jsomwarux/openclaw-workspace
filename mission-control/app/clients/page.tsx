import { Users } from "lucide-react";
import { StateBlock } from "@/components/mission-control/StateBlock";

// Phase 1 stands up the Clients nav lane. The per-client roster and detail
// (open work, completed-this-week, archive toggle, money/proof rails) land in
// Phase 2. This placeholder keeps the nav entry from 404ing in the meantime.
export default function ClientsPage() {
  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6">
        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-emerald-300">Clients</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Where each client stands</h1>
        <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
          Per-client status, open work, and collected cash. Roster and detail arrive in Phase 2.
        </p>
      </div>
      <StateBlock
        kind="empty"
        title="Client roster is coming in Phase 2"
        detail="Collected cash by client is already live on the Money lane."
      />
      <a
        href="/consulting"
        className="mt-4 inline-flex items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 hover:border-[#38414a]"
      >
        <Users size={13} />
        See collected cash by client on Money
      </a>
    </div>
  );
}
