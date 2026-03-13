import {
  Star, Zap, Send, ChevronRight, MapPin, Clock,
  Search, ListFilter, FileText, MessageSquare, UserCheck, PhoneCall, Bot,
} from "lucide-react";

/* ─── Tier data ─── */
const tiers = [
  {
    name: "T1 — Custom Build",
    icon: Star,
    accent: "amber",
    volume: "2–4 / month",
    when: "Exceptional fit, strong hook, custom demo justified",
    how: "Manual. JT decides. Eve builds demo from scratch.",
    example: "H.C. Oswald (Product Knowledge Copilot — RAG over Shopify catalog)",
    effort: "4–6 hrs research + build + deck",
    border: "border-amber-500/40",
    bg: "bg-amber-500/10",
    text: "text-amber-400",
    dot: "bg-amber-400",
  },
  {
    name: "T2 — Template",
    icon: Zap,
    accent: "emerald",
    volume: "8–12 / month",
    when: "Fits a niche template, good hook found",
    how: "Automated nightly. Eve researches, writes brief + LinkedIn DM, stages for JT approval.",
    example: "Inventory Reorder Intelligence | Construction Job Cost Monitor (building)",
    effort: "~2 hrs research (automated), JT reviews + approves",
    border: "border-emerald-500/40",
    bg: "bg-emerald-500/10",
    text: "text-emerald-400",
    dot: "bg-emerald-400",
  },
  {
    name: "T3 — Cold Hook",
    icon: Send,
    accent: "sky",
    volume: "50–100 / month",
    when: "NYC metro, fits ICP, no strong hook yet",
    how: "Automated. Eve generates cold hooks nightly, stages in Drive. JT batch-approves.",
    example: "Reply → auto-promotes to T2",
    effort: "Minimal — Eve generates, JT approves batch",
    border: "border-sky-500/40",
    bg: "bg-sky-500/10",
    text: "text-sky-400",
    dot: "bg-sky-400",
  },
];

/* ─── Pipeline steps ─── */
const pipelineSteps = [
  { label: "Discovery", icon: Search, detail: "prospect-discovery cron · Sun 1AM · 20-30 prospects/week" },
  { label: "Shortlist", icon: ListFilter, detail: "wholesale-distribution.md · construction-trades.md · property-management.md · T1/T2/T3 classified" },
  { label: "Research", icon: Bot, detail: "outreach-pipeline cron · 2AM daily · 2 T2s/night · web search + company analysis" },
  { label: "Brief + DM", icon: FileText, detail: "brief.md + outreach-draft.md · auto-uploaded to Drive · Consulting/Clients/[Company]/" },
  { label: "JT Review", icon: UserCheck, detail: "Telegram summary · reply send [company] to approve · or edit in Drive first" },
  { label: "Outreach Sent", icon: MessageSquare, detail: "LinkedIn DM · follow-up cadence: Day 5, Day 10, Day 17" },
  { label: "Reply?", icon: MessageSquare, detail: "T3 reply → promote to T2 · T2/T1 reply → schedule call" },
  { label: "Discovery Call", icon: PhoneCall, detail: "JT leads · Eve preps talking points from brief" },
];

/* ─── Agents ─── */
const agents = [
  { name: "prospect-discovery", schedule: "Sun 1AM", status: "active", desc: "Finds 20–30 NYC prospects across wholesale/construction/PM, classifies T1/T2/T3, appends to shortlists, pings JT" },
  { name: "outreach-pipeline", schedule: "Daily 2AM", status: "active", desc: "Processes top 2 T2s from shortlist → research → brief → DM draft → Drive → Telegram summary" },
  { name: "overnight-autonomy", schedule: "Daily 3AM", status: "active", desc: "General MC task execution — separate from pipeline" },
  { name: "research-agent", schedule: "On-demand", status: "active", desc: "Deep company research sub-agent, spawned by outreach-pipeline per prospect" },
];

/* ─── Niches ─── */
const niches = [
  {
    name: "Wholesale Distribution",
    target: "NYC metro wholesale distributors (plumbing, HVAC parts, electrical, building materials, industrial)",
    size: "10–75 employees, $3M–$30M revenue, family-owned preferred",
    platform: "n8n",
    template: "Inventory Reorder Intelligence",
    proof: "H.C. Oswald (outreach sent), Brothers Supply (DM drafted)",
    skip: "Skip if on Salesforce/SAP/Oracle",
    color: "emerald",
  },
  {
    name: "Construction + Skilled Trades",
    target: "NYC GCs, HVAC/plumbing/electrical contractors, commercial renovation",
    size: "10–50 employees, $5M–$20M revenue",
    platform: "n8n",
    template: "Construction Job Cost Monitor (building)",
    proof: "Aya ($1,500 dashboard + $1,000 scraper — active client)",
    skip: "Skip if on Salesforce/SAP/Oracle",
    color: "amber",
  },
  {
    name: "Property Management",
    target: "NYC residential property managers, co-op/condo management (AppFolio/Buildium shops)",
    size: "10–50 employees, 500–5,000 units managed",
    platform: "n8n",
    template: "PM Operations (building)",
    proof: "PMOperationsAgent + TenantServiceAgent built",
    skip: "Skip if on Salesforce → route to Insurance niche instead",
    color: "sky",
  },
  {
    name: "Insurance Operations",
    target: "NYC insurance agencies, MGAs (Managing General Agents), Salesforce-native brokerages",
    size: "20–200 employees, Salesforce CRM confirmed",
    platform: "Agentforce",
    template: "InsuranceServiceAgent (built — claims intake, routing, FAQ)",
    proof: "InsuranceServiceAgent built and ready to demo",
    skip: "Skip if NOT on Salesforce — Salesforce is the qualifying criteria",
    color: "violet",
  },
];

/* ─── ICP table ─── */
const icpRows = [
  { signal: "Location", t1: "NYC metro", t2: "NYC metro", t3: "NYC metro", skip: "Outside metro" },
  { signal: "Size", t1: "10–75 employees", t2: "10–75 employees", t3: "10–150 employees", skip: ">150" },
  { signal: "Hook", t1: "Exceptional specific hook", t2: "Template fit + hook", t3: "NYC ICP match", skip: "No hook, no fit" },
  { signal: "Stack", t1: "Any", t2: "n8n-compatible OR Salesforce (insurance)", t3: "Any", skip: "SAP/Oracle enterprise. Note: Salesforce = skip for n8n targets, but = qualifying for Agentforce/insurance." },
  { signal: "Action", t1: "JT decides, custom build", t2: "Auto nightly pipeline", t3: "Auto cold hook batch", skip: "Archive" },
];

/* ─── Helpers ─── */
const nicheColors: Record<string, { border: string; bg: string; text: string }> = {
  emerald: { border: "border-emerald-500/30", bg: "bg-emerald-500/10", text: "text-emerald-400" },
  amber:   { border: "border-amber-500/30",   bg: "bg-amber-500/10",   text: "text-amber-400"   },
  sky:     { border: "border-sky-500/30",      bg: "bg-sky-500/10",     text: "text-sky-400"     },
  violet:  { border: "border-violet-500/30",   bg: "bg-violet-500/10",  text: "text-violet-400"  },
};

function SectionHeader({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-sm font-semibold text-zinc-100 border-l-2 border-emerald-500 pl-3 mb-4">
      {children}
    </h2>
  );
}

/* ═══════════════════════════════════════════════════════════════
   PAGE
   ═══════════════════════════════════════════════════════════════ */
export default function ConsultingPage() {
  return (
    <div className="p-4 sm:p-6 max-w-6xl space-y-10">

      {/* ── 1. Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-zinc-100">Consulting Strategy</h1>
          <p className="text-xs text-zinc-500 mt-0.5">JT Somwaru Consulting — NYC AI Automation</p>
        </div>
        <span className="inline-flex items-center gap-1.5 text-[10px] font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 rounded-full px-3 py-1 w-fit">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          Pipeline Active
        </span>
      </div>

      {/* ── 2. Tier System ── */}
      <section>
        <SectionHeader>Tier System</SectionHeader>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {tiers.map((t) => {
            const Icon = t.icon;
            return (
              <div
                key={t.name}
                className={`bg-[#111] border ${t.border} rounded-xl p-5 hover:border-opacity-70 transition-colors`}
              >
                <div className="flex items-center gap-2.5 mb-3">
                  <div className={`p-2 rounded-lg ${t.bg}`}>
                    <Icon size={16} className={t.text} />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-zinc-200">{t.name}</p>
                    <p className="text-[10px] text-zinc-500">{t.volume}</p>
                  </div>
                </div>

                <div className="space-y-2.5 text-[11px] leading-relaxed">
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">When</p>
                    <p className="text-zinc-400">{t.when}</p>
                  </div>
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">How</p>
                    <p className="text-zinc-400">{t.how}</p>
                  </div>
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Example</p>
                    <p className={t.text}>{t.example}</p>
                  </div>
                  <div className="pt-2 border-t border-[#2a2a2a]">
                    <div className="flex items-center gap-1.5">
                      <Clock size={10} className="text-zinc-600" />
                      <p className="text-zinc-500 text-[10px]">{t.effort}</p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── 3. Pipeline Flow ── */}
      <section>
        <SectionHeader>Automated Pipeline Flow</SectionHeader>
        <div className="overflow-x-auto -mx-4 px-4 sm:mx-0 sm:px-0">
          <div className="flex items-start gap-1 min-w-[900px]">
            {pipelineSteps.map((step, i) => {
              const Icon = step.icon;
              return (
                <div key={step.label} className="flex items-start">
                  <div className="bg-[#111] border border-[#2a2a2a] rounded-xl p-3 w-[130px] flex-shrink-0 hover:border-emerald-500/30 transition-colors">
                    <div className="flex items-center gap-1.5 mb-2">
                      <Icon size={12} className="text-emerald-400 flex-shrink-0" />
                      <p className="text-[11px] font-medium text-zinc-200 truncate">{step.label}</p>
                    </div>
                    <p className="text-[9px] text-zinc-500 leading-relaxed">{step.detail}</p>
                  </div>
                  {i < pipelineSteps.length - 1 && (
                    <div className="flex items-center self-center pt-3 px-0.5 flex-shrink-0">
                      <ChevronRight size={14} className="text-zinc-700" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── 4. Active Agents ── */}
      <section>
        <SectionHeader>Active Agents</SectionHeader>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {agents.map((a) => (
            <div key={a.name} className="bg-[#111] border border-[#2a2a2a] rounded-xl p-4 hover:border-[#3a3a3a] transition-colors">
              <div className="flex items-center justify-between mb-2">
                <p className="text-xs font-semibold text-zinc-200 font-mono">{a.name}</p>
                <div className="flex items-center gap-2">
                  <span className="text-[9px] text-zinc-500 bg-zinc-800 rounded px-1.5 py-0.5">{a.schedule}</span>
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                </div>
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed">{a.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── 5. Niche Targets ── */}
      <section>
        <SectionHeader>Niche Targets</SectionHeader>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {niches.map((n) => {
            const c = nicheColors[n.color];
            return (
              <div key={n.name} className={`bg-[#111] border ${c.border} rounded-xl p-5 hover:border-opacity-70 transition-colors`}>
                <p className={`text-sm font-semibold ${c.text} mb-3`}>{n.name}</p>
                <div className="space-y-2.5 text-[11px] leading-relaxed">
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Target</p>
                    <p className="text-zinc-400">{n.target}</p>
                  </div>
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Size</p>
                    <p className="text-zinc-400">{n.size}</p>
                  </div>
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Platform</p>
                    <span className={`text-[9px] px-1.5 py-0.5 rounded border ${c.bg} ${c.border} ${c.text}`}>{n.platform}</span>
                  </div>
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Template</p>
                    <p className={c.text}>{n.template}</p>
                  </div>
                  <div className="pt-2 border-t border-[#2a2a2a]">
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Proof</p>
                    <p className="text-zinc-400">{n.proof}</p>
                  </div>
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Skip if</p>
                    <p className="text-zinc-600 text-[10px]">{n.skip}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── 6. Geography Rule ── */}
      <section>
        <div className="bg-[#111] border border-[#2a2a2a] rounded-xl p-5">
          <div className="flex items-start gap-3">
            <MapPin size={16} className="text-emerald-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-semibold text-zinc-200 mb-1">NYC Metro Only</p>
              <p className="text-[11px] text-zinc-400 leading-relaxed">
                Manhattan · Brooklyn · Queens · Bronx · Staten Island · Long Island · Westchester · Northern NJ
              </p>
              <p className="text-[10px] text-zinc-600 mt-2">
                Outside NYC metro = skip. No exceptions until 4–5 named client outcomes.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── 7. ICP Quick Reference ── */}
      <section>
        <SectionHeader>ICP Quick Reference</SectionHeader>
        <div className="overflow-x-auto -mx-4 px-4 sm:mx-0 sm:px-0">
          <table className="w-full min-w-[600px] text-[11px]">
            <thead>
              <tr className="border-b border-[#2a2a2a]">
                <th className="text-left py-2.5 pr-4 text-zinc-500 font-medium">Signal</th>
                <th className="text-left py-2.5 pr-4 text-amber-400 font-medium">T1</th>
                <th className="text-left py-2.5 pr-4 text-emerald-400 font-medium">T2</th>
                <th className="text-left py-2.5 pr-4 text-sky-400 font-medium">T3</th>
                <th className="text-left py-2.5 text-red-400 font-medium">Skip</th>
              </tr>
            </thead>
            <tbody>
              {icpRows.map((row) => (
                <tr key={row.signal} className="border-b border-[#1a1a1a]">
                  <td className="py-2.5 pr-4 text-zinc-300 font-medium">{row.signal}</td>
                  <td className="py-2.5 pr-4 text-zinc-400">{row.t1}</td>
                  <td className="py-2.5 pr-4 text-zinc-400">{row.t2}</td>
                  <td className="py-2.5 pr-4 text-zinc-400">{row.t3}</td>
                  <td className="py-2.5 text-zinc-600">{row.skip}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
