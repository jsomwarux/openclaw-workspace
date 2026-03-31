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

