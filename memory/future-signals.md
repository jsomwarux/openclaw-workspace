# Future Signals — "Not Now But Track"
> Reviewed weekly during weekly-synthesis (Sunday 8AM). Eve flags any signal whose trigger conditions are met.
> Add entry any time a tool/technique/strategy is evaluated and deferred. Never let "not now" disappear.

## Format
```
### [Name]
- **What:** [one-line description]
- **Why deferred:** [honest reason]
- **Trigger:** [what has to be true before this becomes actionable]
- **Logged:** [date]
- **Potential value:** [what it unlocks]
```

---

## Active Signals

### DGX Spark — Personal Model Fine-Tuning
- **What:** NVIDIA DGX Spark (~$3-5K) enables local model training/fine-tuning on personal content. Technique: fine-tune on business data, synthetic data generation via distillation (e.g. Qwen 3.5), autonomous self-improvement loops (Karpathy autoresearch repo).
- **Why deferred:** No compatible hardware (Mac mini). JT isn't a developer — executing this correctly requires ML depth. Current stack generating revenue, no need to pivot.
- **Trigger:** (1) DGX Spark price drops below $2K OR Apple Silicon equivalent emerges, AND (2) a client explicitly asks for "custom model trained on our data" OR JT has 5+ named clients and is looking to differentiate services.
- **Logged:** 2026-03-11
- **Potential value:** $15-25K consulting engagement for clients with large historical datasets (wholesale order history, job cost records). Also useful for personalizing JT's own content/outreach voice at scale.

### Clay — Personal CRM & Lead Enrichment
- **What:** Clay enriches leads automatically (LinkedIn, company data, tech stack signals) and manages follow-up sequences. Built exactly for consultant-scale outreach pipelines.
- **Why deferred:** Outreach volume is still low (T1 is 1 prospect: H.C. Oswald). Manual research-agent handles current needs. Clay costs ~$150/mo at useful tiers.
- **Trigger:** JT is running 8+ active outreach prospects simultaneously AND manually tracking follow-ups is taking >2hrs/week.
- **Logged:** 2026-03-11
- **Potential value:** Replaces manual research-agent work for T2/T3 outreach. Serious consultants use it at scale. Directly feeds pipeline revenue.

### Cloudflare MCP Server
- **What:** MCP server exposing all 2,500+ Cloudflare API endpoints (DNS, Workers, R2, Zero Trust, etc.) via two tools: search() and execute(). Would give n8n-agent and research-agent direct Cloudflare control.
- **Why deferred:** JT's current n8n pipelines don't require Cloudflare management. Adds complexity without a clear immediate use case.
- **Trigger:** JT starts hosting client automations on Cloudflare Workers (likely when offering "managed automation" service tier) OR begins managing DNS/infrastructure for clients.
- **Logged:** 2026-03-11
- **Potential value:** Full infrastructure automation capability from within agents. Relevant if JT ever productizes hosted automation delivery.

### geo-seo-claude — AI Search Optimization Tool
- **What:** Open-source tool that runs GEO audits, delivers AI visibility snapshots, analyzes schema markup for LLMs, and exports PDF reports. Specifically designed for optimizing sites for ChatGPT, Perplexity, Claude search.
- **Why deferred:** jtsomwaru.com already has llms.txt, JSON-LD schema, and open AI crawler access. Current GEO foundation is solid. The tool is brand new (March 2026) and repo maturity is unknown.
- **Trigger:** (1) jtsomwaru.com is not appearing in relevant AI search results despite optimizations, OR (2) JT wants to offer GEO optimization as a consulting service and needs an audit tool for client sites.
- **Logged:** 2026-03-11
- **Potential value:** Could become a deliverable in consulting engagements ("AI search visibility audit"). Low effort to run once mature.

### Karpathy autoresearch — Automated Model Self-Improvement
- **What:** Repo by Andrej Karpathy implementing autonomous model improvement loops using reinforcement learning from verifiable rewards. Runs on both Nvidia and Apple Silicon.
- **Why deferred:** Requires hardware + ML depth to use meaningfully. Tied to the DGX Spark signal above.
- **Trigger:** Same as DGX Spark signal. These two are bundled.
- **Logged:** 2026-03-11
- **Potential value:** Same as DGX Spark — personalized model for consulting work or client deliverable.

### Scribe/Guidde — Screen Recording → SOPs
- **What:** Records screen and auto-generates process documentation (SOPs, onboarding guides) from the recording. Good for client handoffs.
- **Why deferred:** No regular client meetings yet. Not enough client volume to justify.
- **Trigger:** JT is running 3+ active client projects simultaneously AND spending time manually writing up "how to use what I built" documentation.
- **Logged:** 2026-03-11
- **Potential value:** Saves 2-4hrs per client handoff. Makes deliverables feel more premium. Could be included as a line item in proposals.

### QuickBooks AI — Auto-Draft Invoices
- **What:** AI-assisted invoice drafting connected to project/time data.
- **Why deferred:** JT has only invoiced Aya twice. Manual invoicing takes 10 minutes at this volume.
- **Trigger:** JT has 4+ active billing clients simultaneously.
- **Logged:** 2026-03-11
- **Potential value:** Reduces billing overhead. More importantly: forces proper time/project tracking, which improves future scoping accuracy.

### Free Tool Strategy — Lead Gen for Consulting
- **What:** Build a free "AI Automation Readiness Quiz" or "ROI Calculator" for SMBs. Tool lives on jtsomwaru.com, solves a real problem (should I automate X?), leads naturally to consulting engagement. Full methodology: coreyhaines31/marketingskills → free-tool-strategy skill.
- **Why deferred:** No active inbound traffic to jtsomwaru.com yet that would benefit from a conversion tool. Zero lead volume means a conversion optimizer can't do its job.
- **Trigger:** jtsomwaru.com getting 200+ organic visits/week OR paid traffic campaign is running. Whichever comes first.
- **Logged:** 2026-03-12
- **Potential value:** Turns passive site visitors into warm leads with a clear buying signal. "AI Readiness Score" gives JT a conversation opener that feels like value delivery, not a pitch.

### AI UGC Video Production — Consulting Service
- **What:** Full AI video production pipeline (Script → Character via Nano Banana Pro JSON → Voice via ElevenLabs + CapCut two-step → Lipsync via WAN lipsync/InfiniteTalk → Edit in CapCut). Replaces 5-person creative teams at 80%+ margins. $5K–8K/month per client, 40–50 videos delivered.
- **Why deferred:** Different ICP (DTC/e-commerce brands) from current consulting focus (construction/wholesale/property mgmt SMBs). Adding a second service vertical right now dilutes focus. Window is 6–12 months before commoditization, but current niche opportunity is more immediate.
- **Trigger:** (1) Consulting generating $10K+/month recurring revenue consistently, AND (2) inbound request from a brand/DTC client specifically asking for content production, OR (3) n8n/Agentforce niche shows signs of saturation.
- **Logged:** 2026-03-12
- **Potential value:** High-margin creative service. $5K–8K/month per client, production cost ~$50/client/month at scale. Can run alongside consulting without conflicting once pipeline is established.
- **Key technique to preserve:** Nano Banana Pro JSON prompting (not text prompts). `"avoid"` array is critical for non-AI look. Color grading: Pinterest reference → Gemini JSON extraction → paste as generation reference. Character consistency: generate one good image, animate it with different WAN lipsync audio (same face every video). Voice: CapCut normalization first, then ElevenLabs on top.

### Vugola — Automated Video Clipping for TikTok/Reels/Shorts
- **What:** Send a YouTube link to a Telegram bot → Vugola finds viral moments → adds captions → face tracks → schedules and posts. Full long-form to short-form pipeline with zero manual editing. Has an OpenClaw integration (ClawHub skill likely exists).
- **Why deferred:** JT has no long-form video content to clip right now. Nash Satoshi and Vista have no YouTube channels. JT isn't on podcasts yet. Nothing to feed the tool.
- **Trigger:** JT goes on a podcast or records a YouTube video, OR Nash Satoshi/Vista launches a YouTube channel with long-form content. Whichever comes first.
- **Logged:** 2026-03-12
- **How it integrates:** Eve receives YouTube link → passes to Vugola via OpenClaw skill → Vugola handles clipping/captions/posting. JT's only input is one Telegram message with the link.
- **Potential value:** Turns one long-form video into a week of TikTok/Reels content automatically. High leverage once there's a video content flywheel. Pairs with PostBridge for scheduling.

### SEO Content Pipeline for jtsomwaru.com
- **What:** Automated blog pipeline using Claude Code + Keyword Everywhere API + Data For SEO API. Researches target keywords ("Agentforce implementation guide," "n8n vs Make for construction companies," "AI automation NYC small business"), writes posts, publishes to site, then uses Google Search Console data to refresh underperforming content. GA4 + GTM tracks consulting lead signups from each post.
- **Why deferred:** jtsomwaru.com has no blog section. Needs a content build before the pipeline matters. Also SEO takes 3-6 months to compound — not a quick win.
- **Trigger:** Outreach volume is consistent AND JT wants an inbound consulting lead channel to reduce dependence on cold outreach. Or: jtsomwaru.com gets a blog section added.
- **Logged:** 2026-03-12
- **APIs needed:** Keyword Everywhere (~$10 credits, pay-as-you-go) + Data For SEO (enterprise, may be overkill — Keyword Everywhere may be enough to start). Google Search Console free. GA4 free.
- **Best target keywords for consulting:** "Agentforce implementation guide," "n8n automation for [niche]," "AI workflow automation NYC," "Salesforce Agentforce vs [X]," "[niche] AI automation case study"
- **Potential value:** Organic inbound consulting leads. Compounds over time. Differentiates jtsomwaru.com from a portfolio site to an authority site.

### Passive Income App KPI Dashboard
- **What:** Daily automated tracking for Vista and Nash Satoshi — App Store downloads, revenue, ratings (Vista), and traffic/ranking views (Nash Satoshi). Delivered as a lightweight daily or weekly digest to JT.
- **Why deferred:** Nash Satoshi isn't monetized, Vista just launched. Neither has enough volume to warrant a dashboard. Manual App Store Connect checks take 2 minutes.
- **Trigger:** Vista reaches 500+ downloads OR generates any revenue, OR Nash Satoshi has a consistent weekly active user base. Whichever comes first.
- **Logged:** 2026-03-12
- **Validated by:** Operators running $70K+/mo app revenue use daily KPI digests as a non-negotiable. Specifically: influencer views, organic vs paid sales, revenue vs spend, top-performing content to double down on. Tool used: **Singular** (mobile attribution platform — connects to App Store, ad accounts, influencer tracking).
- **Potential value:** Gives JT signal on what's working (which content drove downloads, which day/week had spikes). Directly feeds what the vibe marketing agent generates the following week. When trigger is hit: set up Singular free tier, wire to a daily cron that reports the 4 KPIs above via Telegram.

### PostBridge — Cross-Platform Auto-Posting (chosen over Postiz)
- **What:** PostBridge (@postbridge_ by @jackfriks) auto-posts content across TikTok, Instagram, X simultaneously. Has a dedicated OpenClaw skill on ClawHub (`jackfriks/post-bridge-social-manager`) — Eve installs the skill and posts via API directly. Skill is free; platform fees unknown but likely low.
- **Why chosen over Postiz:** Postiz is open-source/self-hostable ($0) but has no OpenClaw integration — you'd build the bridge yourself. PostBridge's ClawHub skill means zero custom integration work. Validated by operators running it at scale with OpenClaw agents.
- **Why deferred:** JT is posting manually. At current volume (2 products, 1–3 posts/week), manual is fine. PostBridge value emerges at daily posting cadence or 3+ accounts.
- **Trigger:** JT is consistently posting for Nash Satoshi AND Vista for 4+ weeks AND wants to scale to daily cadence or add a third product. "Consistently" = actually posting, not just queuing.
- **Logged:** 2026-03-12 | **Decided:** PostBridge over Postiz (2026-03-12)
- **Validated by:** OpenClaw operators running $70K+/mo B2C app revenue using PostBridge + OpenClaw agent to automate 4 TikTok accounts simultaneously.
- **To install when ready:** `openclaw skill install jackfriks/post-bridge-social-manager` then connect PostBridge account. Eve handles posting from queue.jsonl automatically.
- **Potential value:** Eliminates manual posting entirely. Enables daily cadence without JT's time.

---

## Graduated (moved from "not now" to active)
| Signal | Graduated | What triggered it |
|--------|-----------|-------------------|
| Superpowers (Claude Code skills framework) | 2026-03-11 | Clear immediate value for overnight builds and client deliverables. Installed same day. |
