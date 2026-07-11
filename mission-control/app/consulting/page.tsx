import { existsSync, readFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import { AlertTriangle, BriefcaseBusiness, DollarSign, FileText, RefreshCw, Send, Target, TrendingUp } from "lucide-react";
import { RevenueTaskRails } from "@/components/mission-control/RevenueTaskRails";
import { parseNorthStarMetrics, parsePipelineJsonl, type RevenueMetric } from "@/lib/mission-control/revenue";
import { cn } from "@/lib/utils";

export const dynamic = "force-dynamic";

const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function readWorkspaceFile(path: string) {
  const fullPath = join(homedir(), ".openclaw", "workspace", path);
  if (!existsSync(fullPath)) return "";
  return readFileSync(fullPath, "utf-8");
}

function formatMoney(value = 0) {
  return money.format(value);
}

function MetricCard({
  label,
  value,
  detail,
  tone = "neutral",
  icon: Icon,
}: {
  label: string;
  value: string;
  detail: string;
  tone?: "neutral" | "good" | "warn" | "blue";
  icon: typeof DollarSign;
}) {
  return (
    <div className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-zinc-500">{label}</p>
          <p className="mt-2 text-2xl font-semibold tracking-tight text-zinc-100">{value}</p>
        </div>
        <span
          className={cn(
            "rounded-md border p-2",
            tone === "good" && "border-emerald-500/30 bg-emerald-500/10 text-emerald-300",
            tone === "warn" && "border-[#f0883e]/30 bg-[#f0883e]/10 text-[#f0883e]",
            tone === "blue" && "border-blue-500/30 bg-blue-500/10 text-blue-300",
            tone === "neutral" && "border-[#20262d] bg-[#111] text-zinc-400",
          )}
        >
          <Icon size={16} />
        </span>
      </div>
      <p className="mt-3 text-xs leading-relaxed text-zinc-500">{detail}</p>
    </div>
  );
}

export default function RevenuePage() {
  const northStar = readWorkspaceFile("memory/north-star.md");
  const pipelineJsonl = readWorkspaceFile("memory/pipeline.jsonl");
  const metrics: RevenueMetric = parseNorthStarMetrics(northStar);
  const pipeline = parsePipelineJsonl(pipelineJsonl);
  const activePipeline = pipeline.items.filter((item) => item.stage !== "closed").slice(0, 7);
  const nextCashGate = activePipeline.find((item) => item.stage === "active") ?? activePipeline[0];

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-emerald-300">Revenue</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Cash path cockpit</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            Consulting cash, weighted pipeline, selective job upside, and app distribution work in one lane.
          </p>
        </div>
        <a
          href="/consulting"
          className="flex w-fit items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 hover:border-[#38414a]"
        >
          <RefreshCw size={13} />
          Refresh
        </a>
      </div>

      <div className="grid gap-3 md:grid-cols-4">
        <MetricCard
          icon={DollarSign}
          label="Earned Consulting"
          value={formatMoney(metrics.consultingCollected)}
          detail="Current June earned income excluding unemployment. This is the truth metric."
          tone="good"
        />
        <MetricCard
          icon={TrendingUp}
          label="Weighted Pipeline"
          value={formatMoney(metrics.weightedForecast)}
          detail="Forecast from pipeline value times probability. Useful, but not cash."
          tone="blue"
        />
        <MetricCard
          icon={Target}
          label="$10K Gap"
          value={formatMoney(metrics.gapWithForecast)}
          detail={`${formatMoney(metrics.gapCollected)} gap if only collected cash counts.`}
          tone="warn"
        />
        <MetricCard
          icon={BriefcaseBusiness}
          label="Total Collected"
          value={formatMoney(metrics.totalCollected)}
          detail={`${formatMoney(metrics.unemploymentCollected)} is unemployment, so it stays separate from earned momentum.`}
        />
      </div>

      <section className="mt-4 rounded-lg border border-[#f0883e]/30 bg-[#120f0b] p-4">
        <div className="flex items-start gap-3">
          <span className="rounded-md border border-[#f0883e]/30 bg-[#f0883e]/10 p-2 text-[#f0883e]">
            <AlertTriangle size={16} />
          </span>
          <div className="min-w-0">
            <p className="text-sm font-semibold text-zinc-100">Next cash gate</p>
            <p className="mt-1 text-xs leading-relaxed text-zinc-400">{nextCashGate?.name ?? "No active pipeline item found"}</p>
            <p className="mt-2 text-xs leading-relaxed text-zinc-500">{nextCashGate?.next_action ?? "Refresh pipeline data."}</p>
          </div>
        </div>
      </section>

      <div className="mt-5 grid gap-5 xl:grid-cols-[1.35fr_0.65fr]">
        <section>
          <div className="mb-3 flex items-center justify-between gap-3">
            <h2 className="text-sm font-semibold text-zinc-100">Consulting Pipeline</h2>
          </div>
          <div className="overflow-hidden rounded-lg border border-[#20262d] bg-[#0d1014]">
            <div className="grid grid-cols-[1fr_86px_72px_84px] gap-3 border-b border-[#20262d] px-4 py-3 font-mono text-[10px] uppercase tracking-wider text-zinc-600 max-md:hidden">
              <span>Opportunity</span>
              <span>Value</span>
              <span>Prob.</span>
              <span>Weighted</span>
            </div>
            <div className="divide-y divide-[#16191d]">
              {activePipeline.map((item) => (
                <div key={item.name} className="grid gap-2 px-4 py-3 md:grid-cols-[1fr_86px_72px_84px] md:items-center">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-zinc-100">{item.name}</p>
                    <p className="mt-1 line-clamp-2 text-[11px] leading-relaxed text-zinc-600">{item.next_action}</p>
                  </div>
                  <span className="text-xs text-zinc-300">{formatMoney(item.value)}</span>
                  <span className="text-xs text-zinc-500">{item.weight}%</span>
                  <span className="text-xs font-medium text-emerald-300">{formatMoney(item.weightedValue)}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        <div className="space-y-5">
          <section>
            <h2 className="mb-3 text-sm font-semibold text-zinc-100">Send Queue</h2>
            <div className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
              <div className="flex items-center gap-2 text-xs font-medium text-zinc-200">
                <Send size={14} className="text-emerald-300" />
                JT presses send
              </div>
              <p className="mt-2 text-xs leading-relaxed text-zinc-500">
                Current queue starts with Altmark/Yair, then Petri, HPM, and Superior follow-ups. Outreach remains draft/review only.
              </p>
              <p className="mt-3 font-mono text-[10px] uppercase tracking-wider text-zinc-600">memory/send-queue.md</p>
            </div>
          </section>

          <RevenueTaskRails />

          <section className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
            <div className="flex items-center gap-2 text-xs font-medium text-zinc-200">
              <FileText size={14} className="text-blue-300" />
              Source freshness
            </div>
            <p className="mt-2 text-xs leading-relaxed text-zinc-500">
              Data comes from <span className="text-zinc-300">north-star.md</span>, <span className="text-zinc-300">pipeline.jsonl</span>, and live Mission Control tasks.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
