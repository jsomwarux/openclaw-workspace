# Skills Researcher — Weekly Log
_Week starting 2026-03-07 — reset after 2026-W10 synthesis_

## 2026-03-07 — Daily Scan (Sat 11:30 AM ET)

### 🟠 High — Pushed to Mission Control

**🟠 Cloudflare MCP Code Mode** — Full API in 1,000 tokens, dramatically cuts context costs for agent builds
- Source: blog.cloudflare.com/code-mode-mcp + X/@zeke (652❤️ 45.5K views)
- Goal: consulting client builds, n8n-agent, MCP-connected workflows
- Cost: Free (Cloudflare Workers)
- Action: Evaluate — synergizes with FastMCP 3.0 already on board
- MC Task pushed ✅

**🟠 @supermemory/openclaw-supermemory 2.0.2** — Major version update to persistent memory plugin (updated 2026-03-06)
- Source: npm registry — published 2026-03-06 21:09 UTC
- Goal: Eve core capability — semantic cross-session memory
- Cost: Supermemory API freemium
- Action: Evaluate changelog, security review before install
- MC Task pushed ✅

### 🟡/🟢 — KB Only

- **n8n Pinecone Assistant node** (official @n8n_io, 30❤️ 3.5K views) → KB #230
- **Veryfi ClawHub skill** (receipt/invoice parsing) → KB #231
- **Gemini 3.1 Flash-Lite** ($0.25/$1.50 per 1M tokens, already on MC as medium) → KB #232
- **Anthropic Academy 13 free courses** (already on MC as tasks) → KB #233
- **Construction/trades automation validation** ($5K plumbing admin signal) → KB #234

### Already on Board (no duplicate push)
- Gemini 3.1 Flash-Lite: MC task "Update: Add Gemini 3.1 Flash-Lite to TOOLS.md model catalog" (medium)
- Anthropic Academy: MC task "🟠 Anthropic Academy — 13 Free Courses..." (medium) + individual course tasks

---

## 2026-03-10 — Daily Scan (Tue 11:30 AM ET)

### 🔴 Critical — Pushed to Mission Control

**🔴 OpenClaw v2026.3.8** — Multiple security patches + Telegram DM dedupe fix + new backup commands (state was v2026.3.2 — 3 versions missed: 3.6, 3.7, 3.8)
- Source: https://github.com/openclaw/openclaw/releases/tag/v2026.3.8
- Security patches: skills/download installs path traversal fix, Browser SSRF private-network redirect block, system.run script operand binding, MS Teams group policy authz fix
- Directly relevant: Telegram DM dedupe fix (Fixes #40005 — same DM could trigger duplicate replies), new `openclaw backup create/verify` commands, Brave `llm-context` mode for grounding
- Also: GPT-5.4 forward-compat (1,050,000 token context) now in OpenClaw
- MC Task pushed ✅

### 🟠 High — Pushed to Mission Control

**🟠 Kraken CLI MCP Server** — Official Kraken exchange CLI for AI agents, 134 commands, spot/futures/paper trading, v0.2.0 released today (2026-03-10)
- Source: https://github.com/krakenfx/kraken-cli | Via: X/@cruelhandeth (707❤️ 73.1K views)
- Goal: Crypto — could give crypto-agent live Kraken portfolio access via MCP
- 84 stars (official exchange, new repo), language: Rust
- MC Task pushed ✅

**🟠 `executor` by @RhysSullivan** — Agents run code to call any API/MCP/GraphQL server without installing CLIs (671❤️ 100.1K views)
- Source: https://x.com/RhysSullivan/status/2030885614502183367
- Goal: Consulting + Eve architecture — eliminates CLI install friction for ephemeral integrations
- MC Task pushed ✅

### 🟡/🟢 — KB Only

- **Google Cloud Managed MCP expansion** — PostgreSQL, AlloyDB, Spanner, Firestore, Bigtable → KB #252
- **GPT-5.4** — 1,050,000 token context, OpenClaw forward-compat already in → KB #253
- **Claude Opus 4.6 eval-awareness** — Anthropic engineering blog, BrowseComp test recognition → KB #254
- **Agentforce ARR +169%** — Salesforce Q4 validates niche → KB #255
- **Microsoft Copilot Cowork** — built with Claude, $30/seat/month M365 → KB #256

### Cowork Plugins — No Change
- Commit SHA: 477c893b7a63f9ee021d2ccd55d89afd1c4b7c03 (unchanged)



---

## 2026-03-11 — Daily Scan

### 🔴 Anthropic Advanced Tool Use — New API Features (Tool Search, Programmatic Calling, Tool Use Examples)
- Source: https://www.anthropic.com/engineering/advanced-tool-use
- Anthropic officially released three new API capabilities:
  1. **Tool Search Tool** — `defer_loading: true` flag marks tools as discoverable on-demand; Claude searches for tools instead of loading all 50K-134K tokens of tool definitions into context upfront
  2. **Programmatic Tool Calling** — Claude invokes tools from a code execution environment (loops, conditionals, data transforms), reducing intermediate context bloat
  3. **Tool Use Examples** — new standard for demonstrating correct tool usage beyond JSON schema
- Already in use internally: Claude for Excel uses Programmatic Tool Calling for spreadsheet operations
- Goal: All agents (Eve/research-agent/n8n-agent/consulting pipeline) | Cost: Free (API feature) | Impact: Major token savings + new agent capabilities
- Via: Official Anthropic engineering blog

### 🟡 Cowork Plugin Authoring Format Change (commands/ → skills/)
- New commits 2026-03-08 + 2026-03-10: Anthropic deprecated commands/ format, all plugin authoring now uses skills/*/SKILL.md
- SHA: 1316b6508366108158cf08503363d4b4cbc699e5 (was 477c893b)
- Legacy commands/ format still works. JT's skills already on correct format.
- Via: anthropics/knowledge-work-plugins GitHub

### 🟡 Gemini 3.1 Flash Lite — $0.25/$1.50 per M tokens
- Mentioned in OpenRouter context as Google's fastest/cheapest new model
- Already on Mission Control task board ("Update: Add Gemini 3.1 Flash-Lite to TOOLS.md model catalog") — no new action needed
- Via: web search

### 🟡 @supermemory/openclaw-supermemory v2.0.2
- OpenClaw memory plugin by @dhravya, updated 2026-03-06
- Could enhance persistent memory across sessions for Eve or research-agent
- npm: https://www.npmjs.com/package/@supermemory/openclaw-supermemory

### 🟢 LI.FI MCP Server + Agent Skills Toolkit (onchain agentic commerce)
- @lifiprotocol launched MCP server + agent skills for onchain/DeFi workflows
- Relevant to crypto-agent if JT pursues x402 protocol work
- Via: X/@lifiprotocol (277 likes)

### 🟢 @agenticmail/openclaw v0.5.51
- Email + SMS + phone number access for OpenClaw agents
- Potential use for consulting outreach automation (T3 cold hook sends)
- Via: npm search
