import {
  Smartphone, Twitter, Video, MessageCircle, Linkedin,
  ChevronRight, Calendar, Star, Clock, Bot, FolderOpen,
  BarChart2, AlertCircle, CheckCircle, Hourglass, Zap,
} from "lucide-react";

/* ─── Products ─── */
const products = [
  {
    name: "Nash Satoshi",
    slug: "nash-satoshi",
    tagline: "Crypto game theory rankings — 4-model AI consensus",
    url: "nashsatoshi.com",
    status: "active",
    color: "amber",
    platforms: ["X", "TikTok", "Reddit", "LinkedIn"],
    accounts: {
      X: "@NashSatoshi",
      TikTok: "@NashSatoshi (dedicated — warmup before first post)",
      Reddit: "Community account (50+ karma required)",
      LinkedIn: "JT's personal LinkedIn (monthly only)",
    },
    audience: "Crypto holders, game theory nerds, AI community",
    themes: ["Game theory consensus model", "4-model ensemble scoring", "Ranked coin analysis", "Narrative phase tracking"],
    proof: "4-model AI consensus (Claude, GPT-4, Gemini, Grok) · Game Theory Consensus Framework · Ranked 200+ coins",
    subreddits: ["r/CryptoCurrency", "r/CryptoMoonShots"],
  },
  {
    name: "Vista",
    slug: "vista",
    tagline: "Movie rating app — live on App Store",
    url: "App Store",
    status: "active",
    color: "sky",
    platforms: ["X", "TikTok", "Reddit", "LinkedIn"],
    accounts: {
      X: "@jts_14",
      TikTok: "@jts_14 (personal brand — build-in-public energy)",
      Reddit: "JT's personal account (50+ karma required)",
      LinkedIn: "JT's personal LinkedIn (monthly only)",
    },
    audience: "Movie fans, solo dev community, iOS app enthusiasts",
    themes: ["Solo dev ship story", "App Store submission process", "Movie discovery", "Build-in-public moments"],
    proof: "Live on App Store (March 2026) · Built solo · iOS native",
    subreddits: ["r/movies", "r/MovieSuggestions"],
  },
  {
    name: "Glow Index",
    slug: "glow-index",
    tagline: "Skincare rankings on Replit",
    url: "Replit",
    status: "pending",
    color: "zinc",
    platforms: ["X", "TikTok", "Reddit"],
    accounts: {
      X: "TBD",
      TikTok: "Dedicated account required (skincare niche ≠ JT's audience)",
      Reddit: "Dedicated account",
      LinkedIn: "N/A",
    },
    audience: "Skincare community, beauty enthusiasts",
    themes: ["Product rankings", "Ingredient analysis", "Honest skincare reviews"],
    proof: "Built on Replit",
    blocker: "Blocked on n8n workflow + ngrok URL setup",
    subreddits: ["r/SkincareAddiction", "r/AsianBeauty"],
  },
];

/* ─── Content flow steps ─── */
const flowSteps = [
  { label: "Trend Research", icon: BarChart2, detail: "2 web searches/product before generating — what's working in niche this week" },
  { label: "Hook First", icon: Zap, detail: "Write + score hooks in isolation · only 7+ hooks proceed to full body writing" },
  { label: "Generate", icon: Bot, detail: "3 X posts · 2 TikTok scripts · 1 Reddit post · LinkedIn (1st Monday only)" },
  { label: "Score", icon: Star, detail: "3 dimensions × 10 pts each: Hook · Platform Fit · Authenticity — ALL three must hit 7+" },
  { label: "Queue", icon: CheckCircle, detail: "Approved → queue.jsonl · Review needed → flagged · Below 4 → discarded silently" },
  { label: "Drive Upload", icon: FolderOpen, detail: "Formatted markdown review per product → Content/Vibe Marketing/[Product]/" },
  { label: "JT Reviews", icon: AlertCircle, detail: "Telegram summary with account routing · JT posts manually · reply to log" },
  { label: "Log Performance", icon: BarChart2, detail: "Tell Eve what landed → logged to performance-log.jsonl → biases next week's generation" },
];

/* ─── Agents ─── */
const agents = [
  {
    name: "vibe-marketing-generate",
    schedule: "Mon 4:45AM ET",
    status: "active",
    desc: "Weekly batch generation for all active products. Reads product registry, generates X + TikTok + Reddit + LinkedIn (monthly) content, scores everything, queues approved pieces, uploads formatted review to Drive, pings JT.",
    timeout: "720s",
    model: "claude-sonnet-4-6",
  },
];

/* ─── Scoring rubric ─── */
const rubricRows = [
  { dim: "Hook Strength", desc: "Does the first line stop the scroll?", pass: "7+", fail: "<7 = discard or flag" },
  { dim: "Platform Fit", desc: "Does it feel native to this platform's format, length, and tone?", pass: "7+", fail: "<7 = discard or flag" },
  { dim: "Authenticity", desc: "Could JT say this? Is it grounded in real proof points, not marketing language?", pass: "7+", fail: "<7 = discard or flag" },
];

/* ─── Volume per platform ─── */
const volumeRows = [
  { platform: "X", icon: Twitter, volume: "3 posts / product / week", account: "See routing per product", color: "sky" },
  { platform: "TikTok", icon: Video, volume: "2 scripts / product / week", account: "Dedicated or @jts_14", color: "pink" },
  { platform: "Reddit", icon: MessageCircle, volume: "1 post / product / week (max 1 per sub every 2 weeks)", account: "Community account", color: "orange" },
  { platform: "LinkedIn", icon: Linkedin, volume: "1 post / product / month (1st Monday only)", account: "JT's personal LinkedIn", color: "blue" },
];

/* ─── Drive structure ─── */
const driveStructure = [
  { path: "Content/LinkedIn/", desc: "JT's personal brand LinkedIn posts (weekly file)", system: "Personal Brand" },
  { path: "Content/X/", desc: "JT's personal brand X posts (weekly file)", system: "Personal Brand" },
  { path: "Content/Vibe Marketing/Nash Satoshi/", desc: "Formatted review: X + TikTok + Reddit + LinkedIn (monthly)", system: "Vibe Marketing" },
  { path: "Content/Vibe Marketing/Vista/", desc: "Formatted review: X + TikTok + Reddit + LinkedIn (monthly)", system: "Vibe Marketing" },
  { path: "Content/Vibe Marketing/[Product]/", desc: "Future products added automatically", system: "Vibe Marketing" },
];

/* ─── Hook techniques ─── */
const hookTechniques = [
  { name: "Loss Aversion", example: "\"Most people are evaluating crypto wrong — and it's costing them\"" },
  { name: "Curiosity Gap", example: "\"Nash Satoshi ranked 200 coins. The #1 was not what anyone expected.\"" },
  { name: "Specificity as Credibility", example: "\"4 AI models. 127 data points. One consensus score.\"" },
  { name: "Contrarian Signal", example: "\"The coin everyone is buying right now scored 3.2/10 on game theory.\"" },
  { name: "Pattern Interrupt", example: "\"You're watching reviews wrong.\" (Vista)" },
];

/* ─── Color helpers ─── */
const colors: Record<string, { border: string; bg: string; text: string; dot: string }> = {
  amber:  { border: "border-amber-500/40",  bg: "bg-amber-500/10",  text: "text-amber-400",  dot: "bg-amber-400"  },
  sky:    { border: "border-sky-500/40",    bg: "bg-sky-500/10",    text: "text-sky-400",    dot: "bg-sky-400"    },
  zinc:   { border: "border-zinc-600/40",   bg: "bg-zinc-700/10",   text: "text-zinc-400",   dot: "bg-zinc-500"   },
  pink:   { border: "border-pink-500/40",   bg: "bg-pink-500/10",   text: "text-pink-400",   dot: "bg-pink-400"   },
  orange: { border: "border-orange-500/40", bg: "bg-orange-500/10", text: "text-orange-400", dot: "bg-orange-400" },
  blue:   { border: "border-blue-500/40",   bg: "bg-blue-500/10",   text: "text-blue-400",   dot: "bg-blue-400"   },
};

function SectionHeader({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-sm font-semibold text-zinc-100 border-l-2 border-violet-500 pl-3 mb-4">
      {children}
    </h2>
  );
}

/* ═══════════════════════════════════════════════════════════════
   PAGE
   ═══════════════════════════════════════════════════════════════ */
export default function VibePage() {
  return (
    <div className="p-4 sm:p-6 max-w-6xl space-y-10">

      {/* ── 1. Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-zinc-100">Vibe Marketing System</h1>
          <p className="text-xs text-zinc-500 mt-0.5">Passive income app promotion — automated weekly content generation</p>
        </div>
        <span className="inline-flex items-center gap-1.5 text-[10px] font-medium text-violet-400 bg-violet-500/10 border border-violet-500/30 rounded-full px-3 py-1 w-fit">
          <span className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" />
          Active — Mon 4:45AM
        </span>
      </div>

      {/* ── 2. Products ── */}
      <section>
        <SectionHeader>Products</SectionHeader>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {products.map((p) => {
            const c = colors[p.color];
            const isActive = p.status === "active";
            const isPending = p.status === "pending";
            return (
              <div key={p.slug} className={`bg-[#111] border ${c.border} rounded-xl p-5 hover:border-opacity-70 transition-colors`}>
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <p className={`text-sm font-semibold ${c.text}`}>{p.name}</p>
                    <p className="text-[10px] text-zinc-500 mt-0.5">{p.url}</p>
                  </div>
                  <span className={`text-[9px] font-medium px-2 py-0.5 rounded-full border ${
                    isActive
                      ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/30"
                      : "text-zinc-500 bg-zinc-700/20 border-zinc-600/30"
                  }`}>
                    {isActive ? "ACTIVE" : "PENDING"}
                  </span>
                </div>

                <p className="text-[11px] text-zinc-400 mb-3 leading-relaxed">{p.tagline}</p>

                {/* Platforms */}
                <div className="mb-3">
                  <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1.5">Platforms</p>
                  <div className="flex flex-wrap gap-1">
                    {p.platforms.map((pl) => (
                      <span key={pl} className={`text-[9px] px-1.5 py-0.5 rounded border ${c.bg} ${c.border} ${c.text}`}>
                        {pl}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Account routing */}
                <div className="mb-3">
                  <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1.5">Account Routing</p>
                  <div className="space-y-1">
                    {Object.entries(p.accounts).map(([platform, account]) => (
                      <div key={platform} className="flex gap-2 text-[10px]">
                        <span className="text-zinc-600 w-14 flex-shrink-0">{platform}</span>
                        <span className="text-zinc-400">{account}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Audience + Proof */}
                <div className="space-y-2 pt-2.5 border-t border-[#2a2a2a] text-[10px]">
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Audience</p>
                    <p className="text-zinc-400">{p.audience}</p>
                  </div>
                  <div>
                    <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Proof Points</p>
                    <p className="text-zinc-400">{p.proof}</p>
                  </div>
                  {isPending && p.blocker && (
                    <div className="flex items-start gap-1.5 mt-2 p-2 bg-amber-500/5 border border-amber-500/20 rounded-lg">
                      <AlertCircle size={10} className="text-amber-400 flex-shrink-0 mt-0.5" />
                      <p className="text-[10px] text-amber-400">{p.blocker}</p>
                    </div>
                  )}
                </div>

                {/* Reddit subs */}
                <div className="mt-2.5 pt-2.5 border-t border-[#2a2a2a]">
                  <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1">Reddit Targets</p>
                  <p className="text-[10px] text-zinc-400">{p.subreddits.join(" · ")}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── 3. Content Flow ── */}
      <section>
        <SectionHeader>Weekly Content Flow</SectionHeader>
        <div className="overflow-x-auto -mx-4 px-4 sm:mx-0 sm:px-0">
          <div className="flex items-start gap-1 min-w-[1000px]">
            {flowSteps.map((step, i) => {
              const Icon = step.icon;
              return (
                <div key={step.label} className="flex items-start">
                  <div className="bg-[#111] border border-[#2a2a2a] rounded-xl p-3 w-[130px] flex-shrink-0 hover:border-violet-500/30 transition-colors">
                    <div className="flex items-center gap-1.5 mb-2">
                      <Icon size={12} className="text-violet-400 flex-shrink-0" />
                      <p className="text-[11px] font-medium text-zinc-200 truncate">{step.label}</p>
                    </div>
                    <p className="text-[9px] text-zinc-500 leading-relaxed">{step.detail}</p>
                  </div>
                  {i < flowSteps.length - 1 && (
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

      {/* ── 4. Volume per Platform ── */}
      <section>
        <SectionHeader>Volume per Platform</SectionHeader>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          {volumeRows.map((v) => {
            const Icon = v.icon;
            const c = colors[v.color];
            return (
              <div key={v.platform} className={`bg-[#111] border ${c.border} rounded-xl p-4`}>
                <div className="flex items-center gap-2 mb-3">
                  <div className={`p-1.5 rounded-lg ${c.bg}`}>
                    <Icon size={13} className={c.text} />
                  </div>
                  <p className={`text-xs font-semibold ${c.text}`}>{v.platform}</p>
                </div>
                <p className="text-[11px] text-zinc-200 font-medium mb-1">{v.volume}</p>
                <p className="text-[10px] text-zinc-500 leading-relaxed">{v.account}</p>
              </div>
            );
          })}
        </div>
        <p className="text-[10px] text-zinc-600 mt-2 pl-1">
          * Reddit: max 1 post per subreddit every 2 weeks — alternates between 2 subs per product. Karma check required before posting.
        </p>
      </section>

      {/* ── 5. Active Agent ── */}
      <section>
        <SectionHeader>Active Agent</SectionHeader>
        {agents.map((a) => (
          <div key={a.name} className="bg-[#111] border border-[#2a2a2a] rounded-xl p-5 hover:border-[#3a3a3a] transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
              <div className="flex-1">
                <div className="flex items-center gap-2.5 mb-2">
                  <Bot size={14} className="text-violet-400" />
                  <p className="text-sm font-semibold text-zinc-200 font-mono">{a.name}</p>
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                </div>
                <p className="text-[11px] text-zinc-400 leading-relaxed mb-3">{a.desc}</p>
                <div className="flex flex-wrap gap-3 text-[10px]">
                  <div className="flex items-center gap-1.5 text-zinc-500">
                    <Calendar size={10} />
                    <span>{a.schedule}</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-zinc-500">
                    <Clock size={10} />
                    <span>Timeout: {a.timeout}</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-zinc-500">
                    <Zap size={10} />
                    <span>{a.model}</span>
                  </div>
                </div>
              </div>
              <div className="flex flex-col gap-1.5 text-[10px] min-w-[160px]">
                <p className="text-[9px] text-zinc-600 uppercase tracking-wider mb-0.5">Step sequence</p>
                {["0: Dedup guard", "1: Load context + trends", "2: Generate content", "3: Score all pieces", "4: Save to queue.jsonl", "5: Drive upload (per product)", "6: Telegram summary", "7: Update state.json"].map((s) => (
                  <div key={s} className="flex items-center gap-1.5 text-zinc-500">
                    <span className="w-1 h-1 rounded-full bg-violet-500/50" />
                    {s}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </section>

      {/* ── 6. Scoring Rubric ── */}
      <section>
        <SectionHeader>Content Scoring Rubric</SectionHeader>
        <div className="bg-[#111] border border-[#2a2a2a] rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[500px] text-[11px]">
              <thead>
                <tr className="border-b border-[#2a2a2a] bg-[#0d0d0d]">
                  <th className="text-left py-2.5 px-4 text-zinc-500 font-medium">Dimension</th>
                  <th className="text-left py-2.5 px-4 text-zinc-500 font-medium">What it measures</th>
                  <th className="text-left py-2.5 px-4 text-emerald-400 font-medium">Pass</th>
                  <th className="text-left py-2.5 px-4 text-red-400 font-medium">Fail</th>
                </tr>
              </thead>
              <tbody>
                {rubricRows.map((r, i) => (
                  <tr key={r.dim} className={i < rubricRows.length - 1 ? "border-b border-[#1a1a1a]" : ""}>
                    <td className="py-3 px-4 text-violet-400 font-medium">{r.dim}</td>
                    <td className="py-3 px-4 text-zinc-400">{r.desc}</td>
                    <td className="py-3 px-4 text-emerald-400">{r.pass}</td>
                    <td className="py-3 px-4 text-red-400">{r.fail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-4 py-3 border-t border-[#2a2a2a] bg-[#0d0d0d]">
            <p className="text-[10px] text-zinc-600">All three dimensions must score 7+ for <span className="text-emerald-400">approved</span> status. Any score 4–6 = <span className="text-amber-400">review_needed</span>. Any score &lt;4 = discarded silently. Banned words (revolutionary, game-changer, etc.) or 🚀🔥💯 = automatic discard regardless of score.</p>
          </div>
        </div>
      </section>

      {/* ── 7. Hook Writing System ── */}
      <section>
        <SectionHeader>Hook Writing System</SectionHeader>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          {hookTechniques.map((h) => (
            <div key={h.name} className="bg-[#111] border border-[#2a2a2a] rounded-xl p-4 hover:border-violet-500/20 transition-colors">
              <p className="text-xs font-semibold text-violet-400 mb-2">{h.name}</p>
              <p className="text-[10px] text-zinc-400 italic leading-relaxed">{h.example}</p>
            </div>
          ))}
          <div className="bg-[#111] border border-[#2a2a2a] rounded-xl p-4 flex items-center gap-2">
            <AlertCircle size={12} className="text-zinc-600 flex-shrink-0" />
            <p className="text-[10px] text-zinc-600 leading-relaxed">Hooks generated + scored first. Only 7+ hooks proceed to full body writing — prevents wasted work on weak openings.</p>
          </div>
        </div>
      </section>

      {/* ── 8. Drive Folder Structure ── */}
      <section>
        <SectionHeader>Drive Folder Structure</SectionHeader>
        <div className="bg-[#111] border border-[#2a2a2a] rounded-xl overflow-hidden">
          <table className="w-full text-[11px]">
            <thead>
              <tr className="border-b border-[#2a2a2a] bg-[#0d0d0d]">
                <th className="text-left py-2.5 px-4 text-zinc-500 font-medium">Drive Path</th>
                <th className="text-left py-2.5 px-4 text-zinc-500 font-medium">Contents</th>
                <th className="text-left py-2.5 px-4 text-zinc-500 font-medium">System</th>
              </tr>
            </thead>
            <tbody>
              {driveStructure.map((d, i) => (
                <tr key={d.path} className={i < driveStructure.length - 1 ? "border-b border-[#1a1a1a]" : ""}>
                  <td className="py-3 px-4 font-mono text-[10px] text-emerald-400">{d.path}</td>
                  <td className="py-3 px-4 text-zinc-400">{d.desc}</td>
                  <td className="py-3 px-4">
                    <span className={`text-[9px] px-1.5 py-0.5 rounded border ${
                      d.system === "Personal Brand"
                        ? "text-sky-400 border-sky-500/30 bg-sky-500/10"
                        : "text-violet-400 border-violet-500/30 bg-violet-500/10"
                    }`}>
                      {d.system}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ── 9. Performance Feedback Loop ── */}
      <section>
        <SectionHeader>Performance Feedback Loop</SectionHeader>
        <div className="bg-[#111] border border-[#2a2a2a] rounded-xl p-5">
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-[11px]">
            {[
              { step: "1", label: "Post Content", desc: "JT posts approved content manually from Drive review doc", icon: Smartphone },
              { step: "2", label: "Check Numbers", desc: "At week's end, note which posts got traction (likes, replies, views)", icon: BarChart2 },
              { step: "3", label: "Tell Eve", desc: "\"Nash Satoshi game theory post did well\" or \"Vista TikTok flopped\" in chat", icon: MessageCircle },
              { step: "4", label: "Logged + Applied", desc: "Logged to performance-log.jsonl → next Monday generation reads last 4 weeks, biases toward what worked", icon: CheckCircle },
            ].map((s) => {
              const Icon = s.icon;
              return (
                <div key={s.step} className="flex flex-col items-start gap-2">
                  <div className="flex items-center gap-2">
                    <div className="w-5 h-5 rounded-full bg-violet-500/20 border border-violet-500/40 flex items-center justify-center text-[9px] font-bold text-violet-400">
                      {s.step}
                    </div>
                    <Icon size={12} className="text-violet-400" />
                    <p className="text-xs font-medium text-zinc-200">{s.label}</p>
                  </div>
                  <p className="text-[10px] text-zinc-400 leading-relaxed pl-7">{s.desc}</p>
                </div>
              );
            })}
          </div>
          <div className="mt-4 pt-4 border-t border-[#2a2a2a] flex items-start gap-2">
            <Hourglass size={11} className="text-zinc-600 flex-shrink-0 mt-0.5" />
            <p className="text-[10px] text-zinc-600 leading-relaxed">
              No automated X analytics fetcher — manual feedback loop is simpler and more signal-rich. When data accumulates (4+ weeks), generation starts biasing toward proven hook structures and themes automatically.
            </p>
          </div>
        </div>
      </section>

      {/* ── 10. Pre-launch Checklist ── */}
      <section>
        <SectionHeader>Pre-Launch Checklist (One-Time Setup)</SectionHeader>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {[
            { item: "Create @NashSatoshi TikTok account", deadline: "Before Mon Mar 16 4:45AM", done: false, urgent: true },
            { item: "@NashSatoshi TikTok 3-day warmup (scroll crypto niche 15min/day, follow + engage)", deadline: "Wed Mar 18 complete", done: false, urgent: true },
            { item: "Build Reddit karma — crypto community account (50+ comments)", deadline: "2–3 weeks", done: false, urgent: false },
            { item: "Build Reddit karma — Vista / personal account (50+ comments in r/movies)", deadline: "2–3 weeks", done: false, urgent: false },
            { item: "Unblock Glow Index (n8n workflow + ngrok URL)", deadline: "Whenever n8n is set up", done: false, urgent: false },
          ].map((c) => (
            <div
              key={c.item}
              className={`bg-[#111] border rounded-xl p-4 flex items-start gap-3 ${
                c.urgent ? "border-amber-500/30" : "border-[#2a2a2a]"
              }`}
            >
              <div className={`mt-0.5 flex-shrink-0 w-4 h-4 rounded border-2 flex items-center justify-center ${
                c.done
                  ? "bg-emerald-500/20 border-emerald-500"
                  : c.urgent
                  ? "border-amber-500"
                  : "border-zinc-600"
              }`}>
                {c.done && <CheckCircle size={10} className="text-emerald-400" />}
              </div>
              <div>
                <p className={`text-[11px] font-medium ${c.done ? "text-zinc-500 line-through" : "text-zinc-200"}`}>
                  {c.item}
                </p>
                <p className={`text-[10px] mt-0.5 ${c.urgent ? "text-amber-400" : "text-zinc-600"}`}>
                  {c.deadline}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}
