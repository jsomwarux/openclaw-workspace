export default function MonitorPage() {
  return (
    <div className="p-6">
      <h1 className="text-lg font-semibold text-zinc-100 mb-1">Deployment Monitor</h1>
      <p className="text-xs text-zinc-500 mb-8">Active VMs, wallet balances, domain expirations</p>
      <div className="grid grid-cols-3 gap-4">
        {["VMs / Servers", "Wallet Balance", "Domain Expirations"].map(label => (
          <div key={label} className="bg-[#111] border border-[#2a2a2a] border-dashed rounded-lg p-6 text-center">
            <p className="text-xs text-zinc-500 mb-2">{label}</p>
            <p className="text-[10px] text-zinc-700">Configure in api/monitor/route.ts</p>
          </div>
        ))}
      </div>
    </div>
  );
}
