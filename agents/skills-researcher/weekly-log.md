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


