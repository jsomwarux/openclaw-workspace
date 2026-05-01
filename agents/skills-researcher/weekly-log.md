# Weekly Log — Skills & API Researcher

## Week: 2026-W18 (April 27 - May 3, 2026)

<!-- Daily scans append below -->


## 2026-04-25 — Daily Scan

### X API STATUS
✅ All 6 queries successful (~$0.30 total)

### 🔴 Findings — 1 item, DUPLICATE (already in MC)

1. [🔴 MCP RCE vulnerability — CVE-2026-30615]
   - Source: X @isectech_ + The Hacker News + The Register
   - Status: DUPLICATE — already pushed to MC on 2026-04-24 (id: j576c6j3gac3v7ttwgm53kzmh585eghm)
   - Skipped: MC push, Telegram, technical-angles (already logged)

### 🟠 Findings — 2 items, passed quality gate

2. [🟠 OpenAI GPT-5.5 Spud — new model released]
   - Source: X @NorthTechy + Axios/CNBC/TechCrunch confirmed (Apr 23, 2026)
   - Key finding: GPT-5.5 "smartest and most intuitive to use model yet" — rolling out to Plus/Pro/Business/Enterprise in ChatGPT and Codex. Fundamental shift toward agentic computing.
   - Impact: JT uses OpenRouter — if gpt-5.5 is available, could improve coding/agent performance.
   - Quality gate: PASS — first action: check OpenRouter for gpt-5.5 availability
   - Shoutout: NO (model release, not tool feature)
   - MC: pushed ✅ (priority: medium, id: j57b93kv52q43z3sy4tmhscxsx85h3xx)

3. [🟠 Clawdi v2.0 — cross-agent sync (iCloud for AI agents)]
   - Source: X @PhalaNetwork (29❤️, 1.2K👁, shipped 59m ago)
   - Key finding: "iCloud for AI agents" — install once, OpenClaw/Hermes/Claude Code/Codex share memory, keys, skills, files across devices.
   - Impact: JT works across Mac mini, laptop — solves real friction point for agent state portability.
   - Quality gate: PASS — first action: visit Clawdi docs and test sync
   - Shoutout: YES — OpenClaw ecosystem tool
   - MC: pushed ✅ (priority: medium, id: j57fc086cwfp84v7n82j85j66185ghym)

### 🟡 Findings (KB only)
4. GitHub CLI v2.90 `gh skill` — package manager for agent skills. Not in JT's OpenClaw-centric workflow.
5. Claude Code removed from new Pro signups — doesn't affect JT (already has access).
6. Further AI insurance — 78❤️/31.9K impressions. Already logged Apr 21-24.
7. AInsure alpha — insurance AI platform with 10+ agents. Competitor signal only.
8. Weaviate 1.37 MCP server — not in JT's stack (uses Convex + Qdrant).
9. GT Protocol MCP server — crypto trading, not consulting.
10. brainctl 2.5.0 HTTP MCP — dev tooling, not in stack.

### Quality Gate Results
- Pushed to MC: 2 (GPT-5.5, Clawdi v2.0 — both MEDIUM priority)
- Duplicate skipped: 1 (MCP RCE — already in MC)
- KB only: 7
- Telegram JT: YES (2 🟠 findings, 1 shoutout opportunity)

## 2026-04-27 — Daily Scan

### X API STATUS
✅ All 6 queries successful (~$0.30 total)

### 🟠 Findings — 1 item, passed quality gate

1. [🟠 Salesforce Headless 360 — every workflow now API/MCP/CLI]
   - Source: X @MercFromNibel + Salesforce official https://www.salesforce.com/news/stories/salesforce-headless-360-announcement/ (TDX 2026)
   - Key finding: Salesforce exposes every workflow, object, and automation as an API, MCP tool, and CLI command. Not an integration layer — the platform itself is now headless. AI agents can operate Salesforce without a browser or human login.
   - Impact: Fundamental platform shift for JT's Agentforce consulting. Demo architecture must account for native MCP/API access instead of UI automation.
   - Quality gate: PASS — first action: read official announcement + evaluate demo architecture changes
   - Shoutout: YES — Salesforce/Agentforce ecosystem
   - MC: pushed ✅ (priority: medium, id: j5784wxtqcexdnmz6qfg11f16h85m2ex)

### 🟡 Findings (KB only)
2. FreeLLMAPI — OpenAI-compatible proxy aggregating 14 free providers. "Personal experimentation only" per GitHub. Not suitable for JT's production consulting work.
3. Claude Code Setup plugin — scans code to recommend MCP servers. Unverified (0❤️, 21👁 tweet), no official Anthropic announcement found.

### DUPLICATE Findings (skipped)
4. MCP RCE vulnerability (CVE-2026-30615) — already in MC from 2026-04-24
5. Clawdi v2.0 — already in MC from 2026-04-25
6. GPT-5.5 Spud — already in MC from 2026-04-25
7. Further AI insurance — already logged Apr 21-25
8. AInsure alpha — already logged Apr 25

### Quality Gate Results
- Pushed to MC: 1 (Salesforce Headless 360 — MEDIUM priority)
- KB only: 2
- Duplicate skipped: 5
- Telegram JT: YES (1 🟠 finding, 1 shoutout opportunity)

## 2026-04-28 — Daily Scan

### X API STATUS
✅ All 6 queries successful (~$0.30 total)

### 🟠 Findings — 1 item, passed quality gate

1. [🟠 Claude Code v2.1.121 — alwaysLoad MCP + plugin prune]
   - Source: X @jqueryscript + GitHub releases https://github.com/anthropics/claude-code/releases/tag/v2.1.121 (6h ago)
   - Key finding: `alwaysLoad` option skips tool-search deferral for specified MCP servers — eliminates latency. `claude plugin prune` removes orphaned auto-installed plugins.
   - Impact: Direct workflow improvement for JT's daily Claude Code usage. Latency reduction on frequently-used MCP tools.
   - Quality gate: PASS — first action: update Claude Code, configure alwaysLoad for top MCP servers, run plugin prune
   - Shoutout: YES — Claude Code ecosystem
   - MC: pushed ✅ (priority: medium, id: j5708jtyz8653hw8nneegdn9m185pkax)

### 🟡 Findings (KB only)
2. OpenRouter latest endpoints — `claude-sonnet-latest`, `gpt-latest`, etc. Non-determinism risk for production consulting work.
3. OpenAI Codex plugin inside Claude Code — unverified claim (2❤️, 54👁), no official confirmation.
4. Swiper Studio MCP server — build sliders by chatting. Not in JT's stack.
5. Freshkeeper — already evaluated Apr 25 (0 stars, unverified).

### DUPLICATE Findings (skipped)
6. Salesforce Headless 360 — already in MC from 2026-04-27
7. Clawdi v2.0 — already in MC from 2026-04-25
8. GPT-5.5 Spud — already in MC from 2026-04-25
9. MCP RCE vulnerability — already in MC from 2026-04-24
10. Further AI / AInsure insurance — already logged Apr 21-28

### Quality Gate Results
- Pushed to MC: 1 (Claude Code v2.1.121 — MEDIUM priority)
- KB only: 4
- Duplicate skipped: 5
- Telegram JT: YES (1 🟠 finding, 1 shoutout opportunity)

## 2026-04-29 — Daily Scan

### X API STATUS
✅ All 6 queries successful (~$0.30 total)

### 🟠 Findings — 0 items passed quality gate

No new 🔴/🟠 findings today. All signals were either duplicates from previous scans or failed the quality gate.

### 🟡 Findings (KB only)
1. Ungate — Cursor subscription proxy for Claude/ChatGPT. Not in JT's stack.
2. mongodb-mcp-server — official MongoDB MCP for Atlas. JT uses Convex/Qdrant.
3. Agentstead pricing update — lowered Claude costs. JT doesn't use Agentstead.
4. GPT Proto — multi-model API adding Gemini 3.1 Pro. JT uses OpenRouter directly.
5. Anthropic scaling MCP for production — blog post about MCP direction. Generic news.
6. macOS background execution without cursor control — unverified claim, no tool name.
7. n8n community templates (FB Messenger, AI news digest) — community content, not official release.

### DUPLICATE Findings (skipped)
8. Claude Code v2.1.121 — already in MC from 2026-04-28
9. OpenRouter latest endpoints — already evaluated Apr 28 (KB only)
10. GPT-5.5 Spud — already in MC from 2026-04-25
11. Clawdi v2.0 — already in MC from 2026-04-25
12. MCP RCE vulnerability — already in MC from 2026-04-24
13. Salesforce Headless 360 — already in MC from 2026-04-27
14. Weaviate v1.37 — already evaluated Apr 24 (KB only)
15. GitHub CLI gh skill — already evaluated Apr 24 (KB only)
16. Insurance signals — already logged Apr 21-28

### Quality Gate Results
- Pushed to MC: 0
- KB only: 7
- Duplicate skipped: 9
- Telegram JT: NO (no 🔴/🟠 findings — per AGENTS.md, 🟡 only = no message)

## 2026-04-30 — Daily Scan

### X API STATUS
⚠️ Queries 1-5 returned no fresh data (likely cached/credits depleted). Query 6 (insurance) returned results. Tier 1 web fallback executed for queries 1-5.

### 🟠 Findings — 1 item passed quality gate

1. [🟠 OpenClaw v2026.4.26 — Google Live Talk + realtime voice plugins]
   - Source: Web search — GitHub releases https://github.com/openclaw/openclaw/releases/tag/v2026.4.26 (2 days ago) + Releasebot
   - Key finding: (1) Generic browser realtime transport contract, (2) Google Live browser Talk sessions with constrained ephemeral tokens, (3) Gateway relay for backend-only realtime voice plugins, (4) Gemini TTS support, (5) Model Auth status card improvements for OAuth health monitoring
   - Impact: Significant platform update for JT's primary agent platform. Realtime voice capabilities + better OAuth visibility.
   - Quality gate: PASS — first action: check version, update if needed, test Model Auth status card
   - Shoutout: YES — OpenClaw ecosystem
   - MC: pushed ✅ (priority: medium, id: j5733sjmx2b41ahb38mm9kvkyd85thkd)

### 🟡 Findings (KB only)
2. n8n April 2026 stability release — bug fixes, new nodes, UI upgrades, safer webhooks. No specific breakthrough feature.
3. Claude Code Bedrock service tier + OpenTelemetry logging — JT doesn't use Bedrock/Vertex. Incremental fixes.
4. Duck Creek insurance-focused Agentic AI Platform — competitor signal, not directly actionable.

### DUPLICATE Findings (skipped)
5. Claude Code v2.1.121 — already in MC from 2026-04-28
6. Insurance signals (Daseingram, AInsure, etc.) — already logged Apr 21-29

### Quality Gate Results
- Pushed to MC: 1 (OpenClaw v2026.4.26 — MEDIUM priority)
- KB only: 3
- Duplicate skipped: 2
- Telegram JT: YES (1 🟠 finding, 1 shoutout opportunity)
