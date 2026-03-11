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

---

## Graduated (moved from "not now" to active)
| Signal | Graduated | What triggered it |
|--------|-----------|-------------------|
| Superpowers (Claude Code skills framework) | 2026-03-11 | Clear immediate value for overnight builds and client deliverables. Installed same day. |
