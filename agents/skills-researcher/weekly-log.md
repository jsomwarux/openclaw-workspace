# Daily Scan Updates — Apr 4, 2026

## Agentforce, HubSpot, and Salesforce AI Integration Updates
- **Source:** [Digital Applied](https://www.digitalapplied.com/blog/crm-ai-agent-salesforce-hubspot-zoho-2026-guide)
  - Highlights of integrating AI agents into CRM workflows.

## AI Tools Release Overview
- **Source:** [Dust Blog](https://dust.tt/blog/top-ai-agent-tools) 
  - Discusses various AI agent tools available now.

## Model Context Protocol (MCP) Updates
- **Source:** [Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- MCP's role in enhancing AI-assisted software development.

## n8n Workflow Automation
- **Source:** [n8n.io](https://n8n.io/)
- Comprehensive guide to n8n's AI capabilities and integrations.

## AI Implementation and Consulting Advancements
- **Source:** [IBM](https://www.ibm.com/think/topics/ai-workflow)
- Introduction to IBM's AI-powered workflow automation services.

---

# Daily Scan — Apr 7, 2026

## 🔴 OpenClaw v2026.4.5 — MAJOR RELEASE (April 6, 2026)
- **Source:** https://github.com/openclaw/openclaw/releases/tag/v2026.4.5
- **Released:** April 6, 2026 | JT running: v2026.3.31 | Gap: 4 versions
- **What's new:**
  - **Breaking config changes** — legacy aliases removed (talk.voiceId, talk.apiKey, agents.*.sandbox.perSession, browser.ssrfPolicy, hooks.internal.handlers, channel/group/room toggles). `openclaw doctor --fix` handles migration.
  - **Video generation** — built-in `video_generate` tool (xAI grok-imagine-video, Alibaba Wan, Runway)
  - **Music generation** — built-in `music_generate` tool (Google Lyria, MiniMax providers, ComfyUI workflow)
  - **New bundled providers** — Qwen, Fireworks AI, StepFun, **MiniMax TTS**, **MiniMax Search**, Ollama Web Search
  - **Amazon Bedrock + Mantle** — bundled Mantle support + embeddings (Titan, Cohere, Nova, TwelveLabs)
  - **Claude CLI MCP bridge** — OpenClaw tools exposed to Claude CLI runs via loopback MCP
  - **Dreaming/memory** — experimental weighted short-term recall, /dreaming command, multilingual tagging
  - **ClawHub in Skills panel** — search/install skills directly in OpenClaw UI
  - **12-language UI** — Chinese, Portuguese, German, Spanish, Japanese, Korean, French, Turkish, Indonesian, Polish, Ukrainian
  - **Amazon Bedrock embeddings** — for memory/search
- **Relevance:** JT's primary infrastructure. Breaking config changes = must migrate. New video/music tools = content production. MiniMax TTS/Search = potential research pipeline upgrade. ClawHub integration = easier skill discovery.
- **Severity:** 🔴 Critical — breaking config change requires action; 4-version gap; new capabilities
- **Note:** MC task already exists: "🔴 OpenClaw v2026.4.1 — Update required (running v2026.3.31)" — update title to reflect v2026.4.5
- **Fits:** Eve (main) | Cost: Free (OSS update)

## 🟠 Hybro — OpenClaw-native multi-agent interoperability layer (Show HN, April 2026)
- **Source:** https://news.ycombinator.com/item?id=47609291 | Docs: https://docs.hybro.ai
- **What:** Interoperability layer connecting local OpenClaw agents with remote agents via Hybro Hub. Demo shows OpenClaw running locally + remote agents in same workflow.
- **Relevance:** Could enable hybrid local/remote consulting demo architectures
- **Severity:** 🟡 — early-stage (founder seeking feedback), no public release yet, no install command
- **Fits:** research-agent | Cost: unknown | Via: HN

## 🟡 Qwen 3.6 Plus Preview — Free on OpenRouter, 1M context
- **Source:** https://www.buildfastwithai.com/blogs/qwen-3-6-plus-preview-review
- **What:** Free on OpenRouter with 1M context, addresses overthinking issues
- **Relevance:** Could replace MiniMax M2 for certain tasks, saving cost
- **Severity:** 🟢/🟡 — need to test vs MiniMax M2; no immediate action
- **Fits:** routing optimization | Cost: Free | Via: web

## 🟡 Anthropic Cowork Plugin — pdf-viewer + MCP server (March 28)
- **Source:** https://github.com/anthropics/knowledge-work-plugins/commit/f55b539c38beb1cd994ed7f79fe7f70476ea1296
- **What:** New pdf-viewer plugin with local MCP server. Merged March 28. Commit activity confirmed new since last check.
- **Relevance:** Could enhance consulting document processing workflows
- **Severity:** 🟡 — KB only, no specific first action
- **Fits:** n8n-agent | Cost: Free | Via: GitHub

## 🟢 n8n 2.16.0 — Released April 7 (bug fixes + MCP async execution)
- **Source:** https://github.com/n8n-io/n8n/releases
- **What:** Bug fixes — MCP executions now async, Anthropic node uses models endpoint, Pipedrive v2 node. No new features.
- **Relevance:** MCP async execution is good for n8n-agent reliability
- **Severity:** 🟢 — bug fixes only, no breaking changes
- **Fits:** n8n-agent | Cost: Free | Via: GitHub

## 🟢 Qwen 3.6 Plus Preview on OpenRouter — 1M context, free
- **Source:** web search
- **What:** Free tier model on OpenRouter with 1M context, addresses overthinking
- **Relevance:** potential cost savings routing tier
- **Severity:** 🟢 — no specific first action, need benchmarking vs MiniMax M2

## 🟢 Goose AI Agent — Open-source engineering automation (April 6)
- **Source:** https://aitoolly.com/ai-news/article/2026-04-06-goose-an-open-source-and-extensible-ai-agent-designed-to-automate-complex-engineering-tasks
- **What:** Open-source AI agent for engineering tasks
- **Relevance:** tangential
- **Severity:** 🟢 — early stage, no direct relevance to JT stack

## 🟢 Cursor vs Claude Code — Wired coverage
- **Source:** https://www.wired.com/story/cusor-launches-coding-agent-openai-anthropic/
- **What:** Cursor launched new AI agent to compete with Claude Code and Codex
- **Relevance:** JT uses Claude Code for Agentforce builds
- **Severity:** 🟢 — competitive landscape, no action needed

## 🟢 Microsoft Agent Governance Toolkit — Enterprise agent governance
- **Source:** https://letsdatascience.com/news/microsoft-releases-agent-governance-toolkit-for-autonomous-a-2e26e8dc
- **What:** 7-package multi-language system for governing autonomous AI agents (April 3)
- **Relevance:** Enterprise governance pattern — possible consulting angle
- **Severity:** 🟢 — enterprise only, not immediately actionable

