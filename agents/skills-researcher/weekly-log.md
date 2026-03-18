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


