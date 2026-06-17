import { ArrowUpRight, Bot, CheckCircle, FolderOpen, MessageCircle, Smartphone, Twitter, Video } from "lucide-react";

const products = [
  {
    name: "Nash Satoshi",
    detail: "Crypto ranking proof, methodology receipts, X/TikTok/Reddit distribution.",
    status: "active",
  },
  {
    name: "Vista",
    detail: "App Store movie rating app, ASO, share cards, directories, rating precision tests.",
    status: "active",
  },
  {
    name: "Glow Index",
    detail: "Skincare ranking app, SEO/GEO pilot, dedicated niche distribution.",
    status: "pending",
  },
];

const flow = [
  "Trend research",
  "Hook scoring",
  "Generate X/TikTok/Reddit drafts",
  "Quality score",
  "Queue for JT review",
  "Drive upload",
  "Manual post",
  "Performance log",
];

export default function LegacyVibePage() {
  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-violet-300">Legacy</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Vibe Marketing System</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            Archived reference for the old app-promotion system. The active Ship cockpit now lives at <span className="text-zinc-300">/ship</span>.
          </p>
        </div>
        <a
          href="/ship"
          className="inline-flex w-fit items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 hover:border-[#38414a]"
        >
          Open Ship <ArrowUpRight size={13} />
        </a>
      </div>

      <section className="grid gap-3 md:grid-cols-3">
        {products.map((product) => (
          <div key={product.name} className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold text-zinc-100">{product.name}</p>
                <p className="mt-2 text-xs leading-relaxed text-zinc-500">{product.detail}</p>
              </div>
              <span className="rounded border border-violet-500/30 bg-violet-500/10 px-2 py-0.5 text-[10px] uppercase text-violet-300">
                {product.status}
              </span>
            </div>
          </div>
        ))}
      </section>

      <section className="mt-5 rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
        <div className="mb-4 flex items-center gap-2">
          <Bot size={15} className="text-violet-300" />
          <h2 className="text-sm font-semibold text-zinc-100">Weekly Content Flow</h2>
        </div>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
          {flow.map((item, index) => (
            <div key={item} className="rounded-lg border border-[#20262d] bg-[#0f1316] p-3">
              <p className="font-mono text-[10px] text-zinc-600">0{index + 1}</p>
              <p className="mt-1 text-xs font-medium text-zinc-200">{item}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-5 rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
        <div className="mb-4 flex items-center gap-2">
          <CheckCircle size={15} className="text-emerald-300" />
          <h2 className="text-sm font-semibold text-zinc-100">Legacy Routing Notes</h2>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          <div className="rounded-lg border border-[#20262d] bg-[#0f1316] p-3">
            <div className="flex items-center gap-2 text-xs font-medium text-zinc-200">
              <Smartphone size={13} className="text-blue-300" />
              Products
            </div>
            <p className="mt-2 text-xs leading-relaxed text-zinc-500">Vista, Nash Satoshi, and Glow Index remain the app-distribution focus.</p>
          </div>
          <div className="rounded-lg border border-[#20262d] bg-[#0f1316] p-3">
            <div className="flex items-center gap-2 text-xs font-medium text-zinc-200">
              <FolderOpen size={13} className="text-emerald-300" />
              Storage
            </div>
            <p className="mt-2 text-xs leading-relaxed text-zinc-500">Approved drafts were routed to Drive; JT still presses post manually.</p>
          </div>
          <div className="rounded-lg border border-[#20262d] bg-[#0f1316] p-3">
            <div className="flex items-center gap-2 text-xs font-medium text-zinc-200">
              <Twitter size={13} className="text-sky-300" />
              X + LinkedIn
            </div>
            <p className="mt-2 text-xs leading-relaxed text-zinc-500">Proof-led posts only; no forced generic app marketing.</p>
          </div>
          <div className="rounded-lg border border-[#20262d] bg-[#0f1316] p-3">
            <div className="flex items-center gap-2 text-xs font-medium text-zinc-200">
              <Video size={13} className="text-pink-300" />
              TikTok + Reddit
            </div>
            <p className="mt-2 text-xs leading-relaxed text-zinc-500">Warm accounts before posting; route Reddit carefully by community rules.</p>
          </div>
        </div>
        <div className="mt-3 flex items-center gap-2 text-[11px] text-zinc-600">
          <MessageCircle size={12} />
          This page is reference-only. Use /ship for current operating work.
        </div>
      </section>
    </div>
  );
}
