# Weekly Log — Skills & API Researcher

## Week: 2026-W19 (May 4 - May 10, 2026)

<!-- Daily scans append below -->


## 2026-05-02 — Daily Scan

### X API STATUS
✅ All 6 queries successful (~$0.30 total)

### 🟠 Findings — 0 items passed quality gate

No new 🔴/🟠 findings today. All signals were either:
- Not in JT's active stack (Meta CLI, Higgsfield AI, Blender MCP, Specter, Envio, etc.)
- Duplicate from previous scans (Clawdi v2.0, Claude Code v2.1.121, OpenRouter latest endpoints, insurance signals)
- Unverified third-party tools (Franklin Run resume, Codex-in-Claude plugin)
- Community content, not official releases (n8n templates)

### 🟡 Findings (KB only)
1. Meta CLI + MCP for ads platform — not in JT's stack
2. Higgsfield AI MCP server — creative/3D, not in stack
3. Anthropic Blender MCP connector — 3D tool, not in stack
4. ast-outline MCP v0.2.0 — niche AST tool, not in stack
5. Franklin Run — resume Claude/Codex sessions on rate limits. Third-party, unverified.
6. OpenAI Codex plugin inside Claude Code — links to notella.app (third-party), not official
7. Specter MCP server — private market data, not in stack
8. Envio Docs MCP + v3.0.0 alpha — blockchain indexer, not in stack
9. GPT-5.5 available in Make — duplicate, JT uses OpenRouter
10. Agentstead pricing update — JT doesn't use Agentstead
11. Ungate Cursor proxy update — JT doesn't use Cursor
12. Duck Creek insurance Agentic AI — already logged Apr 29
13. Insurance claims experience strategy — low engagement (0❤️, 1👁)
14. n8n community templates — not official releases

### DUPLICATE Findings (skipped)
15. Clawdi v2.0 — already in MC from 2026-04-25
16. Claude Code v2.1.121 — already in MC from 2026-04-28
17. OpenRouter latest endpoints — already evaluated Apr 28 (KB only)
18. Insurance signals (Daseingram, AInsure, etc.) — already logged Apr 21-30

### Quality Gate Results
- Pushed to MC: 0
- KB only: 14
- Duplicate skipped: 4
- Telegram JT: NO (no 🔴/🟠 findings — per AGENTS.md, 🟡 only = no message)

## 2026-05-04 — Daily Scan

### X API STATUS
❌ Credits depleted (402 error). Tier 1 web fallback executed.

### 🟠 Findings — 1 item passed quality gate

1. [🟠 OpenClaw v2026.5.1 — Codex binary fix + plugin ecosystem expansion]
   - Source: Web search — GitHub releases https://github.com/openclaw/openclaw/releases (2 days ago) + Releasebot (8 hours ago)
   - Key finding: (1) Codex/app-server resolves managed binaries from bundled dist chunks — fixes false missing-binary startup failures. (2) Gateway/CLI repairs stale managed service definitions. (3) ACPX and OpenTelemetry externalized to separate packages. (4) 20+ plugins prepped for beta publishing (Google Chat, LINE, Matrix, Discord, WhatsApp, Brave, Codex, etc.)
   - Impact: Critical fix for JT's Codex ACP harness. Major plugin ecosystem expansion signals OpenClaw maturing as a platform.
   - Quality gate: PASS — first action: check version, update if needed, verify Codex ACP harness starts
   - Shoutout: YES — OpenClaw ecosystem
   - MC: pushed ✅ (priority: medium, id: j570hj9t7cndww1v346z15xvx9863ps8)

### 🟡 Findings (KB only)
2. Anthropic retired 1M context window beta for Sonnet 4.5/4 — JT uses Sonnet 4.6/Opus 4.6, unaffected
3. Versium REACH MCP server — contact data enrichment, not in JT's stack
4. n8n May 2026 blog content — guides/tutorials, not a product release
5. Insurance AI trends (Lemonade/Porch earnings) — market commentary, not actionable
6. MCP 2026 roadmap — already known from March

### DUPLICATE Findings (skipped)
7. Claude Mythos — already evaluated Apr 23 (gated preview, not public)

### Quality Gate Results
- Pushed to MC: 1 (OpenClaw v2026.5.1 — MEDIUM priority)
- KB only: 5
- Duplicate skipped: 1
- Telegram JT: YES (1 🟠 finding, 1 shoutout opportunity)

## 2026-05-04 — Daily Scan

### X API STATUS
❌ Credits depleted (402 error). Tier 1 web fallback executed.

### 🟠 Findings — 0 items passed quality gate

No new 🔴/🟠 findings today. All signals were either:
- Duplicate from previous scans (OpenClaw v2026.5.1, Claude Mythos)
- Not in JT's active stack (Versium REACH MCP)
- Not a product release (n8n May blog content)
- Generic market commentary (insurance AI trends)
- Old news (MCP 2026 roadmap)

### 🟡 Findings (KB only)
1. Anthropic retired 1M context window beta for Sonnet 4.5/4 — JT uses Sonnet 4.6/Opus 4.6, unaffected
2. Versium REACH MCP server — contact data enrichment, not in JT's stack
3. n8n May 2026 blog content — guides/tutorials, not a product release
4. Insurance AI trends (Lemonade/Porch earnings) — market commentary, not actionable
5. MCP 2026 roadmap — already known from March

### DUPLICATE Findings (skipped)
6. OpenClaw v2026.5.1 — already in MC from 2026-05-04
7. Claude Mythos — already evaluated Apr 23 (gated preview, not public)

### Quality Gate Results
- Pushed to MC: 0
- KB only: 5
- Duplicate skipped: 2
- Telegram JT: NO (no 🔴/🟠 findings — per AGENTS.md, 🟡 only = no message)

### 2026-05-04 Daily Scan
- **OpenClaw v2026.5.3 + v2026.5.3-1** — Released today (May 4). New bundled file-transfer plugin (file_fetch, dir_list, dir_fetch, file_write) for paired nodes with default-deny path policy. WhatsApp libsignal fix. Gateway env preservation fix. Plugin prerelease fallback. Google Meet realtime voice fixes. Memory/LanceDB apache-arrow fix. Severity: 🟠 | Source: GitHub releases
- **OpenRouter new models (last 14d):** x-ai/grok-4.3 ($1.25/$2.50, 1M ctx), ibm-granite/granite-4.1-8b ($0.05/$0.10, 131K ctx), openrouter/owl-alpha (FREE, 1M ctx, agentic), poolside/laguna-xs.2/m.1 (FREE, coding), qwen/qwen3.6-flash ($0.25/$1.50, 1M ctx), qwen/qwen3.6-max-preview ($1.04/$6.24), openai/gpt-5.5 ($5/$30), openai/gpt-5.5-pro ($30/$180), deepseek/deepseek-chat-v3.1 ($0.15/$0.75, 32K ctx). Severity: 🟠 for DeepSeek V3.1 (cheaper than V3 0324), 🟡 for rest.
- **n8n** — 2.18.5-2.18.7, 2.19.0-2.19.2: bug fixes only, no new features. Severity: 🟢
- **Anthropic** — No new posts since Apr 17 (Claude Design). Severity: 🟢
- **Cowork plugins** — sp-global added Apr 30, no new commits since. Severity: 🟢
- **X API** — Credits depleted, daily scan ran web-only. Need to fund or check subscription.

### Daily Scan — May 5, 2026
- Discoveries: 4 | 🟠: 3 | 🟡: 1 | KB: 4
- [🟠] HouseCanary MCP Server — Property valuations and data tools for AI agents.
- [🟠] ATTOM MCP Server — Standardized property data access for LLMs.
- [🟠] Claude Design — Collaborative visual creation tool from Anthropic Labs.
- [🟡] sp-global plugin — New knowledge-work plugin added by Anthropic.


### 2026-05-05 — Daily Scan continuation
- X API: all 6 daily queries attempted; blocked by CreditsDepleted 402. Web fallback completed.
- [🟠] OpenClaw v2026.5.4 — current local version is 2026.5.3-1; release includes plugin/secrets/channel contract fixes, active-memory recall crash guard, Gateway/startup performance work, and UI/cron improvements. Quality gate PASS because JT actively runs OpenClaw and first action is version check + normal upgrade path. Source: https://github.com/openclaw/openclaw/releases/tag/v2026.5.4
- [🟡] OpenRouter new models — Grok 4.3, IBM Granite 4.1 8B, Mistral Medium 3.5, Owl Alpha/free, NVIDIA Nemotron/free, Poolside/free coding models. KB only until benchmarked against JT routing needs.
- [🟢] Anthropic news — no newer post than Claude Design Apr 17.
- [🟢] Cowork plugins — latest commit unchanged from tracked SHA 9789ea78ad66e395a9c709146cacecdc14ce2abf.
- [🟢] Clawhub/npm scan — no gate-passing new skill/plugin for current stack.
[2026-05-06] 🟠 OpenClaw 2026.5.5 — fixes heartbeat/TUI session poisoning, cron maintenance after restarts, Telegram/Codex progress rendering, iOS pairing, hidden runtime-context leakage into context engines, approval delivery retries, and generated-media duplicate fallback posts. Source: https://github.com/openclaw/openclaw/releases/tag/v2026.5.5 | Relevance: OpenClaw/Eve reliability | First action: run `openclaw gateway status && npm install -g openclaw@2026.5.5 && openclaw gateway restart` after confirming update window. | Priority: medium.
