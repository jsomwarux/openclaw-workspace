# Future Signals

## Fantasy Sports Agent + Dynasty App
**What:** Build a gap-monitoring agent that watches dynasty fantasy football Twitter/Reddit for unmet needs, then auto-develops app ideas based on signals. First concrete app likely a dynasty-specific analytics tool (age curves by archetype, college-to-NFL translation layer). JT has a fantasy X account to build audience around it.
**Why deferred:** Financial runway pressure — job apps and consulting are priority. Also need to validate the specific gap before building.
**Trigger:** Job offer accepted OR consulting generating $3K+/mo consistently. At that point, dynasty tool is a weekend build worth testing.
**Notes from conversation:** Dynasty > redraft (less competition, more passionate audience, KeepTradeCut is weak on analytics). PlayerProfiler covers general advanced stats — the gap is dynasty-specific decision tools. X content flywheel first, build second. — "Not Now But Track"
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

### ViewTrack ($24-79/month social analytics + OpenClaw plugin)
- **What:** Cross-platform video performance tracker (TikTok/IG/YT/X) with native OpenClaw integration. Pulls views, engagement, hook patterns from competitor accounts. Feeds performance data back into AI content agent for self-improvement loop.
- **Why deferred:** Half the product is unbuilt (Dec 2025 features still "coming"). Nash Satoshi and Vista have $0 revenue — paying for optimization infrastructure before content is running is wrong order of operations. Performance feedback loop already exists in vibe marketing AGENT.md.
- **Trigger:** Nash Satoshi OR Vista hits $300/month in revenue AND at least 4 weeks of content posted. At that point, trial Basic plan ($24/month), wire OpenClaw plugin into vibe-marketing agent as live performance source.
- **Logged:** 2026-03-20
- **Potential value:** Closes the self-improvement loop gap. Competitor hook analysis feeds directly into weekly content generation.

### Creator Briefing System — Daily Angles for Hired Creators
- **What:** When JT hires UGC creators for Nash Satoshi or Vista, the vibe marketing system shifts from weekly batch generation to daily micro-ideas. Each creator gets a short daily brief: trending hook, suggested angle for the day, ICP framing. ViewTrack API feeds hook performance data back into the brief generator so it learns what converts.
- **Why deferred:** No creators hired yet. No point building a daily briefing pipeline with no recipients.
- **Trigger:** JT hires first UGC creator for Nash Satoshi or Vista. At that point: (1) shift vibe-marketing agent from weekly to daily, (2) wire ViewTrack API (see ViewTrack signal), (3) create a daily creator-brief cron that generates 3 hook angles per product per day and sends to creator.
- **Logged:** 2026-03-22
- **Potential value:** Closes the feedback loop between what's posted and what's generated next. Enables compound improvement — each week's content is better than the last because it's built on real performance data, not assumptions.

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

### Nano Banana 2 (NB2) — AI Image Generation for Vibe Marketing + Guyana Demos
- **What:** `google/gemini-3.1-flash-image-preview` on OpenRouter ($0.50/$3 per M tokens). Key capability: **visual grounding** — searches the web for real images of specific locations/species before generating, meaning it can accurately depict Georgetown landmarks, real construction sites, actual building types. Also: extreme aspect ratios (9:16 for TikTok), 512px batch-to-upscale workflow to keep cost ≈ NB1. 95% of Pro quality at fraction of the cost.
- **Why deferred (vibe marketing):** Currently vibe marketing outputs slide *text copy* only — JT assembles visuals manually. NB2 could generate the actual TikTok slide images directly from the content spec (Nash Satoshi: dark/navy data-forward, Vista: cinematic dark + film grain). Not worth automating until TikTok accounts are warmed and posting is consistent.
- **Why deferred (Guyana):** Guyana contact hasn't confirmed intro yet. If/when demo builds start, NB2 is the right tool for visual assets — Georgetown church, drainage infrastructure, government building imagery — without stock photo licensing.
- **Trigger A (vibe):** Nash Satoshi TikTok warmed + 4 weeks consistent manual posting + JT wants to remove manual image assembly. Add NB2 image generation step to vibe-marketing-generate cron.
- **Trigger B (Guyana):** Contact confirms intro to local firm → demo build phase → use NB2 for visual assets in demos.
- **Model route when ready:** `openrouter/google/gemini-3.1-flash-image-preview` (already in TOOLS.md)
- **Logged:** 2026-03-15

### Virlo API — TikTok Trend Intelligence for Vibe Marketing
- **What:** Virlo API (api.virlo.ai/v1) provides real TikTok trend data before posting: trending topics by niche (Orbit endpoint), outlier creator analysis (small accounts with outsized views = proven format signals), hashtag performance (avg views, avg comments), top videos by category. Replaces guessing with actual this-week signal.
- **Why deferred:** Nash Satoshi TikTok account doesn't exist yet. Not posting consistently. Wiring trend intelligence into an automation that isn't running is complexity with no return.
- **Trigger:** Nash Satoshi TikTok account is warmed up AND JT has posted consistently for 4+ weeks. At that point: add a Virlo pre-analysis step to the vibe-marketing-generate cron — run Orbit for niche keywords, pull top videos, update a TRENDING-NOW.md file, then generate content based on that data instead of Claude's general knowledge.
- **Logged:** 2026-03-15
- **Integration note:** Use PostBridge (already chosen) for posting — NOT Postiz. Postiz has no OpenClaw integration. PostBridge has a native OpenClaw skill (`jackfriks/post-bridge-social-manager`). Virlo handles the *what to post* signal; PostBridge handles the *posting*.
- **Potential value:** Vibe marketing cron posts what's trending in crypto/movie niche *this week* instead of evergreen guesses. Higher save/share rate = algorithm push = organic reach without paid spend.

### Remotion — React-Based Video Generation for TikTok/Demos
- **What:** Remotion turns React components into exported MP4 video files. Claude Code scaffolds the scene components (SVG visuals, data tables, animated slides); you tweak timing and copy; export runs locally. First reel ~1 hour; by the third reuse of scene architecture it's under 10 minutes. $0 production cost beyond Claude subscription.
- **Why deferred:** Nash Satoshi TikTok account isn't warmed up yet. Building the Remotion pipeline before the posting infrastructure exists is backwards.
- **Trigger:** Nash Satoshi TikTok is warmed up AND JT has posted manually for 2+ weeks. At that point, replace the "JT records himself" script mode for Nash Satoshi TikTok with Remotion-generated animated slideshows that don't require camera time.
- **Logged:** 2026-03-15
- **Two use cases (activate separately):**
  - **Nash Satoshi TikTok:** Faceless animated slides — dark background, ranking table movements, game theory visualizations. Maps directly to the branded palette already defined in the product registry. No camera, 10 min/reel at steady state.
  - **jtsomwaru.com consulting demos:** Animated workflow demos for construction job tracker and PM maintenance triage — more compelling than static screenshots in outreach and on the site. Build after Nash Satoshi Remotion pipeline is working.
- **First action when trigger is met:** `npx create-video@latest` in a new project dir. Ask Claude Code to scaffold a 6-slide Nash Satoshi ranking reveal component — Hook slide → problem → model approach → ranking table → movement highlight → CTA. Reuse the component architecture for every subsequent week; only the data changes.
- **Potential value:** Removes camera requirement from Nash Satoshi TikTok entirely. Consulting demo videos that would cost $2–5K/month from a design agency, built in hours.

### AppKittie — App Rebuild Opportunity Scanner
- **What:** appkittie.com filters App Store apps by revenue (e.g. $50K+/mo) and rating. Sort low-to-high on rating to find high-revenue, poorly-rated apps worth rebuilding. Strategy: "find demand, then build a better version."
- **Why deferred:** Nash Satoshi and Glow Index are already built and stalled. Bottleneck is monetization, not idea generation. Adding another app idea stream creates distraction, not progress. Passive income strategist cron already covers this angle (and more) every Sunday.
- **Trigger:** Nash Satoshi OR Glow Index is actively generating revenue (any amount, consistently for 4+ weeks). At that point, use AppKittie for one manual research session to identify the next passive income build — don't automate it, just check it once.
- **Logged:** 2026-03-15
- **Potential value:** Validated demand before building. Reduces passive income app failure rate. Worth a 30-minute manual review at the right time.

### n8n lessons.md — Category Index
- **What:** Add a Quick Index table at the top of `~/projects/n8n-agent/tasks/lessons.md` grouping lesson numbers by category (Webhook/HTTP, Code nodes, Sheets, Auth, Data flow/$json, etc.). Agent reads index first, jumps to relevant cluster instead of scanning all lessons linearly.
- **Why deferred:** File is 21KB / 52 lessons — still fast to read in full. Index adds noise before it adds value.
- **Trigger:** lessons.md hits ~80 lessons OR ~40KB. At that point add the index and log a lesson in lessons.md itself about using it.
- **First action when triggered:** Eve adds the index block at line 3 of lessons.md, commits, updates this signal as Graduated.
- **Logged:** 2026-03-17
- **Potential value:** Prevents agent from missing applicable lessons as the file grows past 100 entries.

---

## Graduated (moved from "not now" to active)
| Signal | Graduated | What triggered it |
|--------|-----------|-------------------|
| Superpowers (Claude Code skills framework) | 2026-03-11 | Clear immediate value for overnight builds and client deliverables. Installed same day. |

## Job Posting Sniper — consulting lead signal agent
**What:** Monitor LinkedIn/Indeed for NYC SMBs posting Ops/Marketing/Sales Manager roles. Job posting = public admission of budget + pain. Pitch: "before you hire for $120K/yr, try n8n at $3,500." Agent scans daily → extracts company + decision-maker → generates T2-style outreach → drops into pipeline queue.
**Why deferred:** Existing T2/T3 pipeline (prospect-discovery + outreach-pipeline + t3-cold-hook) hasn't converted first client yet. LinkedIn job API requires partner program; Indeed gated. Build complexity is higher than task description implies. Adding lead volume before funnel converts is premature.
**Trigger:** 2+ closed consulting clients from existing pipeline AND existing pipeline is consistently saturated (20+ T2 prospects queued). Re-evaluate at that point.
**Note:** The "hire vs. automate" pitch angle is immediately usable in T3 cold hooks without building the sniper — wire it in as a copy variant for Ops/Marketing-adjacent prospects.

## Bright Data MCP Server
- **What:** Web scraping/unlocker MCP with 60+ tools including LinkedIn dataset APIs, Web Unlocker (bypasses aggressive bot protection), structured extraction
- **Why deferred:** No active scraping gap. Current stack (Cloudflare /crawl + Firecrawl + Scrapling) covers all current use cases. Research-agent has zero Firecrawl code. Nash Satoshi staying on Gumloop.
- **Trigger:** Activate when EITHER: (1) research-agent or Nash Satoshi pipeline is actively getting blocked by bot protection on sites Firecrawl misses, OR (2) outreach volume hits 50+ prospects/week and LinkedIn manual contact search is a bottleneck
- **Date deferred:** 2026-03-21

## UI UX Pro Max skill (Claude Code)
- **What:** Design skill for Claude Code — generates polished UI components, not "AI slop" aesthetics. Real design systems, bold typography.
- **Why deferred:** Current UI work on jtsomwaru.com is maintenance-level. Not doing intensive component design right now.
- **Trigger:** Starting a new client dashboard build OR jtsomwaru.com v2 redesign. Install at: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Added: 2026-03-22

## LightRAG (graph + vector hybrid RAG)
- **What:** Hybrid retrieval combining knowledge graphs with vector search. Significantly better than naive chunking for large, interconnected knowledge bases (catalogs, policy docs, multi-entity data).
- **Why deferred:** No RAG deployment currently at scale. H.C. Oswald Cloudflare /crawl ingestion is the candidate but hasn't started.
- **Trigger:** Any client RAG ingestion project with >5k documents OR H.C. Oswald catalog ingestion begins. Repo: https://github.com/hkuds/lightrag
- Added: 2026-03-22
