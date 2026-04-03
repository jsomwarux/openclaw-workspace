# Skills Researcher — Weekly Log
_Week starting 2026-03-28 — reset after 2026-W13 synthesis_

## 2026-03-28 — Daily Scan

No new 🔴/🟠 findings.

X queries 1-6: Mostly echoes of March 25-27 posts. No new high-signal releases from core tools.

Web research:
- OpenClaw: still v2026.3.24 (no new release). State current.
- Cowork plugins: commit f55b539c (pdf-viewer) — already in state.json from 7AM weekly synthesis.
- Anthropic: Claude Mythos leak (upcoming model, unreleased, fails priority gate) → 🟡 KB #352.
- Cowork pdf-viewer: annotation + form-fill + sign via local MCP server, merged 2026-03-28 → 🟡 KB #353.
- npm: routine channel plugin maintenance (Lark v2026.3.26, Weixin v2.1.1), no new skill packages.
- HN: single result, no actionable signal.


---

## 2026-03-30 — Daily Scan

### 🔴 OpenClaw v2026.3.28 — Update required (running v2026.3.24, 4 patch versions behind)
- **Source:** GitHub openclaw/openclaw releases API
- **URL:** https://github.com/openclaw/openclaw/releases/tag/v2026.3.28
- **Published:** 2026-03-29 01:34 UTC
- **Summary:** Significant release with 2 breaking changes + 4+ production-relevant fixes for Eve's stack.
  - **⚠️ Breaking #1:** Qwen portal OAuth removed — migrate to Model Studio API key (`openclaw onboard --auth-choice modelstudio-api-key`). Not in use, but Doctor will fail on stale config entries.
  - **⚠️ Breaking #2:** Auto config migrations older than 2 months are dropped — very old legacy keys now fail validation instead of being silently rewritten. Run `openclaw doctor` after update.
  - **Rate-limit cooldown scoping fixed** — cooldowns now per-model (not per-auth-profile), so one 429 no longer blocks all models. Escalation ladder changed from 1min→1hr exponential to 30s/1min/5min stepped — directly fixes past Eve freezes.
  - **Gemini 3.1 routing fixed** — pro/flash/flash-lite now resolve correctly for all Google provider aliases. Was broken, causing routing failures when using Gemini 3.1 Flash-Lite for cheap tasks.
  - **xAI/Grok** — moved to Responses API, `x_search` added as first-class tool.
  - **Plugins/hooks** — `requireApproval` added to `before_tool_call` hooks (exec approval overlay, Telegram buttons, `/approve` command).
  - **ACP/channels** — `/acp spawn codex --bind here` now works in Discord/iMessage without creating a child thread.
  - **`runHeartbeatOnce` plugin API** — plugins can now trigger a single heartbeat with delivery target override.
  - **OpenAI image tools** — Codex registered for image analysis, fixes image analysis on OpenRouter and MiniMax.
  - **Auto-reply fix** — suppresses `{"action":"NO_REPLY"}` JSON envelopes before channel delivery (was causing visible garbage in some channels).
  - **MCP/channels** — Gateway-backed channel MCP bridge added with Claude-facing conversation tools.
- **Relevance:** Eve infrastructure — production system. Rate-limit cooldown fix + Gemini routing fix are directly operational.
- **Fits:** main / infrastructure
- **Cost:** Free
- **Active tool:** YES (OpenClaw) → Shoutout flag triggered
- **Severity:** 🔴 — Breaking config changes + rate-limit fix affect production immediately.


### 🟡/🟢 findings (KB only)
- DenchClaw — open-source AI CRM on OpenClaw, 185+ PH votes, launched 2026-03-26. File-system-backed CRM queryable via OpenClaw natural language. KB #357. Ecosystem signal — validates OpenClaw as vertical app platform.
- Notion 3.4 Database Agents — released 2026-03-26. AI agents read/write Notion DBs with memory. JT uses Notion lightly (content calendar only). KB #358.
- n8n MCP / x_search Grok: echoes of prior week findings.


---

## 2026-04-01 — Daily Scan

### 🟠 OpenClaw v2026.3.31 — Stable release; supersedes open v2026.3.28 task
- **Source:** GitHub openclaw/openclaw releases API
- **URL:** https://github.com/openclaw/openclaw/releases/tag/v2026.3.31
- **Published:** 2026-03-31 20:54 UTC
- **Current install:** v2026.3.28 (open update task already exists)
- **Summary:** Major stable release with breaking changes + critical production fixes:
  - **⚠️ Breaking:** Skills/install now fails closed on dangerous-code findings — `--dangerously-force-unsafe-install` required for previously-passing skill installs
  - **⚠️ Breaking:** Plugin SDK — legacy compat subpaths deprecated, migration warnings emitted; bundled `openclaw/plugin-sdk/*` is the forward path
  - **⚠️ Breaking:** Node commands now disabled until node pairing is approved
  - **Cron/isolated sessions fix** — model override in cron jobs now carries correctly across retry restarts. Was causing cron failures for jobs with model overrides (directly operational for Eve)
  - **Memory/QMD mask fix** — `--mask` preferred over `--glob` for default collections. Was causing collection collisions on restart
  - **Background tasks unified** — ACP, subagents, cron, background CLI all under SQLite-backed control plane. New `openclaw flows list|show|cancel` commands
  - **Cron/announce fix** — multi-line cron reports now delivered in full to Telegram (was collapsing to last chunk)
  - **Compaction model consistency** — `agents.defaults.compaction.model` now resolves consistently for manual `/compact` and engine paths
  - **Tasks/gateway stall fix** — maintenance sweep no longer stalls gateway event loop under synchronous SQLite pressure (gateway hanging ~1min after startup — fixed)
  - **Telegram/retries fix** — 429/retry_after backoff preserved for safe delivery retries
  - **ACP session recovery** — dead-session queue-owner repair fixed
- **Relevance:** Eve infrastructure — cron model override fix + QMD mask fix are directly operational
- **Fits:** main / infrastructure
- **Cost:** Free
- **Active tool:** YES (OpenClaw) → Shoutout flag triggered
- **Severity:** 🟠

### 🟡/🟢 findings (KB only)
- Anthropic Batch API 300k tokens (Opus 4.6 + Sonnet 4.6, March 30) — useful for long-form batch tasks, no active blocking use case. KB.
- Claude Haiku 3 retirement April 19, 2026 — not in use in Eve's stack. KB.
- Agentforce Contact Center launch — Salesforce launched native voice+digital AI contact center, $800M ARR. Major product but no active SF client → fails priority gate. KB.
- OpenClaw v2026.4.1-beta.1 (today) — per-cron tool allowlists, SearXNG bundled, compaction/cooldown fixes. BETA → 🟡.
- DBHub MCP server (bytebase/dbhub) — database-to-Claude MCP bridge, 3.9/5 GitRated. Not immediately blocking. KB.
- n8n — no specific new node/feature release confirmed via X. Low-signal posts only.

---

## 2026-04-02 — Daily Scan

### 🔴 OpenClaw v2026.4.1 — Stable release (running v2026.3.31)
- **Source:** GitHub openclaw/openclaw releases API
- **URL:** https://github.com/openclaw/openclaw/releases/tag/v2026.4.1
- **Published:** 2026-04-01 16:58 UTC
- **Current install:** v2026.3.31 (last update task: done)
- **Summary:** New stable release with multiple production-relevant changes:
  - **Per-cron tool allowlists** — `openclaw cron --tools` now lets individual jobs restrict which tools fire. Directly operational for Eve crons.
  - **`agents.defaults.params`** — global default provider parameters (e.g. temperature, max_tokens) configurable once at agent level.
  - **Failover retry cap** — `auth.cooldowns.rateLimitedProfileRotations` knob added; caps same-provider retries before cross-provider fallback. Directly addresses past rate-limit loops.
  - **Compaction model consistency fix** — `agents.defaults.compaction.model` now resolves for manual `/compact` and engine paths. Was already flagged as needed fix — now confirmed in stable.
  - **Webchat chat history** — `gateway.webchat.chatHistoryMaxChars` configurable.
  - **SearXNG bundled** — new web_search provider plugin (self-hosted search, no API key).
  - **Bedrock Guardrails** — added to bundled Bedrock provider.
  - **macOS Voice Wake** — trigger Talk Mode by voice.
  - **Tasks `/tasks` chat command** — see recent background tasks inline in chat.
  - **Gateway reload fix** — startup config writes (auth tokens, Control UI origins) no longer trigger restart loop.
  - **Telegram errorPolicy + errorCooldownMs** — configurable per-account/chat/topic error suppression. Directly relevant to Telegram delivery.
- **Relevance:** Eve infrastructure — production system. Rate-limit + compaction + Telegram fixes are directly operational.
- **Fits:** main / infrastructure
- **Cost:** Free
- **Active tool:** YES (OpenClaw) → Shoutout flag triggered
- **Severity:** 🔴

### 🟠 Agentforce Contact Center — GA launch (Enterprise Connect 2026)
- **Source:** X @johniosifov (multiple posts, 44-74❤️) + web (CX Today, PRNewswire, Martechcube)
- **URL:** https://www.cxtoday.com/contact-center/salesforce-agentforce-contact-center-ccaas-crm-battle/
- **Published:** ~March 28 – April 2, 2026
- **Summary:** Salesforce launched Agentforce Contact Center at Enterprise Connect 2026. Unified voice, digital channels, CRM data, and AI agents in a single platform. AI agents achieving 40-60% containment. Agentforce overall at $800M ARR (launched 18 months ago). US Dept of Labor rolling out Agentforce. Framed as full CCaaS entry — direct challenge to Genesys/Five9/NICE.
- **Relevance:** JT Somwaru Consulting — Agentforce is JT's primary enterprise tool. Contact Center is a new product line = new Agentforce skill to learn. Validates Agentforce investment ($800M ARR in 18 months). Shoutout opportunity.
- **Fits:** consulting (Agentforce niche) / job market
- **Cost:** N/A (Salesforce product)
- **Severity:** 🟠
- **Content angle:** React post on $800M ARR speed + 40-60% containment stat. "Agentforce just hit $800M ARR 18 months after launch. For context, Slack took 7 years." Tag @salesforce or @Agentforce.

### 🟡/🟢 findings (KB only)
- Qwen3.6 Plus Preview FREE on OpenRouter — released Mar 30, 1M context, $0 in/out, #3 programming benchmark. Note: collects training data. KB #359.
- Pinecone Assistant n8n node — new node collapses 12-node RAG pipeline to 1. No active client RAG build. KB #360.
- n8n native MCP + AI Agent nodes — confirmed in multiple sources as existing capability (not new release). n8n has MCP support, RAG nodes, ReAct agent chains. Context item, no action. KB #361.
- Claw Dev multi-provider update — coding IDE added OpenRouter, OpenAI, Copilot, Z AI. Not in JT's active stack. KB #362.
- Agentforce $800M ARR stat — separate KB entry for job-market positioning. KB #363.
