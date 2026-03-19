# Skills Researcher — Weekly Log
_Week starting 2026-03-14 — reset after 2026-W11 synthesis_

---

## 2026-03-14 — Daily Scan

### 🟠 n8n CVE-2025-68613 — RCE Actively Exploited, CISA KEV
- **CVSS:** 9.9 (n8n self-score) / 8.8 (NIST) | Expression injection → RCE in workflow expression evaluator
- **Affects:** n8n 0.211.0 → pre-1.120.4 | Patched in 1.120.4, 1.121.1, 1.122.0
- **Our instance:** ✅ already at 1.122.0 — no action needed on Eve's Mac mini
- **Client risk:** Aya uses n8n — if their instance is self-hosted and older than 1.120.4, they're exposed to server takeover by any authenticated user
- **Action:** Advisory conversation with Aya recommended. Consulting differentiation opportunity.
- **Sources:** Bleeping Computer, The Hacker News, CISA KEV, Vulert (confirmed 1–3 days ago)
- **Note:** Already in Mission Control (🔴 task from weekly synthesis). No duplicate push.
- **Content angle:** Added to technical-angles.md

### 🟡 @openclaw/voice-call v2026.3.13 — Official Voice Plugin
- Official OpenClaw plugin: Twilio + Telnyx + Plivo providers. STT + LLM + TTS in gateway.
- Gives Eve a real phone number for inbound/outbound AI voice calls
- Install: `openclaw plugins install @openclaw/voice-call`
- Relevance: future consulting demo capability; could differentiate service offerings
- Source: npm + docs.openclaw.ai

### 🟡 OpenRouter Stealth Models — Hunter Alpha & Healer Alpha
- Hunter Alpha: 1T-param, 1M context, agentic/long-horizon tasks + tool use, currently FREE
- Healer Alpha: multimodal omni-model, currently FREE
- ⚠️ All prompts and completions recorded for model improvement — NOT safe for production client data
- Community speculation: Hunter Alpha = Gemini 3.1 thinking, Healer Alpha = Gemma 3.5/4
- Source: @OpenRouter (1.9K likes, 937K views)

### 🟡 Cowork Plugins: Commands → Skills Migration (2026-03-13)
- Anthropics/knowledge-work-plugins commit 89f6599: all plugins migrated commands/*.md → skills format
- Version bumps across all Cowork plugins
- Impact on us: Cowork Implementation is CLOSED per MEMORY.md. Low priority.
- New commit SHA: 89f6599ddf (was: 1316b65083)

### 🟡 n8n TinyFish Integration — Visual Web Scraping Node
- Official @Tiny_Fish + n8n integration: drag-and-drop visual web scraping, open-source
- Relevant for Aya StreetEasy scraper enhancements or new client research automations
- Source: @DataChaz (50 likes, 11K views)

### 🟡 Google Gemini Embedding 2 — Multimodal Embedding Model
- First fully multimodal embedding model on Gemini architecture, preview via Gemini API + Vertex AI
- Better semantic search across text + image. Relevant for future RAG pipelines.
- Source: @googledevs (1.9K likes, 255K views)

---

## 2026-03-16 — Daily Scan

### 🟡 Agentforce Contact Center — Salesforce Native CCaaS, Enterprise Connect 2026
- Salesforce launched native telephony + unified routing baked into the CRM. CRM-native, not bolted-on.
- Agentforce ARR surged +169% in Q4 earnings — demand is real and accelerating.
- CCaaS market is dissolving INTO Salesforce (major competitors disrupted).
- JT's Agentforce niche: Salesforce shops are now being pitched a full native contact center stack — creates implementation demand.
- Priority gate: no active Agentforce client → 🟡, but strong forward consulting signal.
- Source: Enterprise Connect 2026 / @Littl3Lobst3r + investor.salesforce.com

### 🟡 CoinMarketCap MCP Server — Real-Time Crypto Data for AI Agents
- Official CMC MCP server launched: live prices, market cap, volume, sentiment for AI agents via MCP.
- Direct fit: crypto-agent could integrate for richer market intelligence without custom scraping.
- Cost: likely free tier (CMC offers free API tier). Unvetted — GitHub check needed.
- Source: @CoinMarketCap (202 likes, 278K views) — official account, high credibility.

### 🟡 OpenClaw v2026.3.13-1 — Recovery Patch (no new features)
- Recovery release: fixes broken v2026.3.13 tag/release path. GitHub tag only — npm still at 2026.3.13.
- Bugfixes: compaction token count sanity check, Telegram thread media SSRF policy, Discord metadata fetch.
- No config changes needed. State updated.

### 🟢 n8n Roofing Construction Automation — $5K Workflow Pattern
- @hamza_automates: n8n workflow for roofers — reads job requests, pulls project details, auto-processes.
- Signals: construction/skilled trades niche (our primary!) is actively being automated with n8n.
- Our construction job-tracker template is already built (2026-03-15). Community validation.
- Source: @hamza_automates (215 likes, 26K views)

### 🟢 OpenClaw Browser Plugin — Real Chrome Profile + CRM Automation
- @aisearchmastery: OpenClaw new update enables live Chrome profile use — Gmail, LinkedIn, CRM actions.
- Relevance: consulting demo potential (show clients AI controlling their real browser).
- Source: X (0 likes but video demo visible)

### Previously noted (no change needed):
- n8n CVE-2025-68613: our instance at 1.122.0 ✅, already in MC + log.
- OpenRouter stealth models: already logged 2026-03-14, still 🟡.
- Anthropic Academy Claude Code courses: already in MC as 🟠 task.

---

## 2026-03-17 — Daily Scan

### 🟠 CoinMarketCap MCP Server — Promoted from 🟡 (2026-03-16)
- Official CoinMarketCap MCP server: real-time prices, market cap, volume, listings via natural language.
- Re-assessed today: directly fits crypto-agent + Nash Satoshi live data ingestion. Installable now with free CMC API key.
- MC task pushed: "🟠 CoinMarketCap MCP Server — live crypto data for crypto-agent"
- Source: @CoinMarketCap (201 likes, 282K views) + coinmarketcap.com/api/mcp/
- Technical angle added.

### 🟡 Anthropic Advanced Tool Use — Tool Search + Programmatic Calling + Tool Use Examples
- Already on board as 🔴 task. No new action needed. Confirming still active/relevant.
- Context: reduces 50K+ token bloat in heavy-tool agent builds. Relevant to n8n-agent and research-agent.
- Source: anthropic.com/engineering/advanced-tool-use

### 🟡 OpenRouter Hunter Alpha + Healer Alpha Stealth Models (re-confirmed)
- Hunter Alpha: 1T params, 1M context, agentic use, currently free. Community: likely Gemini 3.1 thinking or Kimi K2.5.
- Healer Alpha: omni-modal, free, 128K context.
- ⚠️ Both log all prompts/completions — not safe for client data. Monitor for official reveal.
- Already logged 2026-03-14.

### 🟡 n8n CVE-2025-68613 CVSS 10.0 RCE — CONFIRMED PATCHED
- CISA-mandated patch (CVE-2025-68613). n8n instance on Mac mini: ✅ 1.122.0 (patched). No action needed.
- Source: @the_yellow_fall / CISA KEV / securityonline.info

### 🟡 Agentforce CCaaS Disruption — Enterprise Connect 2026 Signal (re-confirmed)
- Salesforce Agentforce Contact Center = native telephony + CRM routing. Major CCaaS players disrupted.
- Validates JT's Agentforce consulting niche and Lead SE job application (deadline 03/27).
- Already in weekly log 2026-03-16.

### 🟢 deAPI n8n Integration — 8 operations, 4 workflow templates
- Official deAPI + n8n integration. 8 operations. Data API with 1,000+ app connections.
- Low relevance to current consulting niches. Background signal only.
- Source: @deAPI_ (11 likes)

### 🟢 OKX Agent Trade Kit — MCP for Trading Agents
- OKX launched open-source MCP server + CLI for trading AI agents on their exchange. Natural language execution.
- Not relevant — JT doesn't do autonomous trading. Crypto monitoring only.
- Source: @okx (799 likes, 5.5M views)

---

## 2026-03-18 Daily Scan

### 🟡 Google Colab MCP Server
- **Source:** X/@googledevs (421 likes, 91K views) + @GoogleColab (579 likes) — 2026-03-18
- **URL:** https://x.com/googledevs/status/2033955386211151896
- **What:** Open-source MCP server giving AI agents programmatic notebook write+execute access inside Google Colab's secure cloud environment
- **Severity:** 🟡 — interesting capability, not an active build need, no client work blocked by absence
- **Goal:** App dev / consulting demos (data analysis workflows)
- **Action:** KB'd (#307)

### 🟡 Figma MCP — 5 new partners (Cursor, Warp, Factory, Augment Code, Firebender)
- **Source:** X/@figma — 2026-03-13
- **URL:** https://x.com/figma/status/2032124661278892484
- **What:** Figma expanded MCP server to 5 new development tool partners
- **Severity:** 🟡 — no Figma in current consulting stack, low relevance
- **Action:** KB'd (#305)

### 🟡 Hunter Alpha — mystery model on OpenRouter (possible DeepSeek V4)
- **Source:** web search / news9live.com — 2026-03-18
- **URL:** https://www.news9live.com/technology/artificial-intelligence/hunter-alpha-ai-model-deepseek-v4-rumours-openrouter-2944584
- **What:** Unidentified model appeared on OpenRouter, specs suggest possible DeepSeek V4
- **Severity:** 🟡 — unverified speculation, watch for official announcement
- **Action:** KB'd (#306)

### 🟡 Anthropic knowledge-work-plugins: commands → skills migration (2026-03-13)
- **Source:** GitHub/anthropics — SHA 89f6599ddf (same as state.json — already tracking)
- **What:** All 14 Cowork plugins migrated from commands/ to skills/ format. bio-research removed.
- **Severity:** 🟡 — structural change, relevant if JT builds Cowork plugins (currently CLOSED decision)
- **Action:** KB'd (#309)

### 🟡 n8n + Claude API: 34% improvement in scam detection filtering
- **Source:** X/@AutomationBrief — 2026-03-14
- **URL:** https://x.com/AutomationBrief/status/2032592904611397766
- **What:** Real-world case of Claude API + n8n automating scam detection with Gemini 2.5 Flash integration. 34% improvement in false-positive filtering.
- **Severity:** 🟡 — validates n8n+Claude stack for classification/filtering workflows. Pattern applicable to consulting builds.
- **Action:** KB'd (pattern logged)

_X API note: Queries 1, 2, 5, 6 returned 503 (X API service unavailable). Queries 3 (n8n) and 4 (MCP) succeeded._


