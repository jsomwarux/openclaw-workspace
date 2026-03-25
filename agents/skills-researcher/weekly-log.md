# Skills Researcher — Weekly Log
_Week starting 2026-03-21 — reset after 2026-W12 synthesis_

---

## 2026-03-21 — Daily Scan

### 🟠 Claude Code Channels — Anthropic ships OpenClaw-competitive Telegram/Discord for Claude Code
- **Source:** Multiple (VentureBeat, MacStories, X @Noahhh1005, India Today)
- **URL:** https://venturebeat.com/orchestration/anthropic-just-shipped-an-openclaw-killer-called-claude-code-channels
- **Summary:** Anthropic launched Claude Code Channels (March 20, 2026) — developers can now control Claude Code sessions from Telegram and Discord while away from their computer. VentureBeat headline: "Anthropic just shipped an OpenClaw killer." Cloud sessions also available at claude.ai/code. Supports same Telegram+Discord channels OpenClaw uses.
- **Relevance:** JT Somwaru Consulting (competitive awareness) / Job Market (demonstrate multi-platform agent UX patterns) / Eve stack context
- **Fits:** main (Eve awareness) + consulting context
- **Cost:** Included with Claude Code ($20/mo Pro or above)
- **Severity rationale:** New capability from Anthropic directly competing with our primary AI OS (OpenClaw). JT should know. Not 🔴 (no breaking change, no cost impact).
- **Content angle:** JT has an angle here — OpenClaw vs Claude Code Channels comparison from a power-user perspective.

### 🟠 HubSpot + Claude MCP Connector — live, setup takes an afternoon
- **Source:** X @ReedDailey, @allenxmarketing (confirmed by HubSpot Releasebot — ChatGPT connector also writes to CRM)
- **URL:** https://x.com/ReedDailey/status/2033713330326581660
- **Summary:** Claude + HubSpot integration via MCP is live and confirmed. AI agents can update records, trigger workflows, pull contact data from HubSpot — no manual copy-paste. Multiple practitioners confirming it works. HubSpot also shipped a ChatGPT connector with CRM write access. This directly validates JT's HubSpot expansion target from MEMORY.md.
- **Relevance:** JT Somwaru Consulting — HubSpot is explicit expansion target in MEMORY.md. MCP implementation path for SMB CRM clients is now concrete.
- **Fits:** research-agent / jt-consulting-pipeline / potential new consulting service offering
- **Cost:** Free (MCP is open protocol); HubSpot API key + Claude subscription required
- **Severity rationale:** Q3 and Q4 pass — installable today, applies at JT's scale. Validates HubSpot niche with concrete technical path.

---

## 2026-03-24 — Daily Scan

### 🔴 OpenClaw v2026.3.23 — Production update required (JT running v2026.3.13, 2 versions behind)
- **Source:** GitHub openclaw/openclaw releases API
- **URL:** https://github.com/openclaw/openclaw/releases/tag/v2026.3.23
- **Summary:** Two new releases shipped March 23–24: v2026.3.22 (major) and v2026.3.23 (fixes). JT is on v2026.3.13. Breaking changes in v2026.3.22: Chrome extension relay path fully removed (affects browser tooling); new Plugin SDK surface (`openclaw/plugin-sdk/*`); legacy CLAWDBOT_*/MOLTBOT_* env vars removed; ClawHub-first plugin install behavior. Critical fixes in v2026.3.23 that directly affect Eve's production stack: (1) `agents/web_search` was using stale/default provider instead of configured one — Eve's Brave Search may have been broken; (2) `openrouter/auto` pricing refresh was recursing infinitely on bootstrap, breaking OpenRouter cost tracking; (3) Gateway crash loop under launchd/systemd fixed; (4) Subagent timeout false negatives fixed (affects overnight crons); (5) ClawHub macOS auth fixed (affects `openclaw skills`); (6) Telegram threading fix for DM topics; (7) `openclaw doctor --fix` now cleans up stale plugin refs.
- **Relevance:** Eve infrastructure — production system running on OpenClaw
- **Fits:** main / infrastructure
- **Cost:** Free (standard update)
- **Active tool:** YES — OpenClaw is JT's primary AI OS
- **Severity rationale:** web_search provider bug + openrouter pricing crash + gateway crash loop = confirmed production impact on Eve's live stack. Update is available now via `openclaw update`.

### 🟠 Agentforce Contact Center — Salesforce launched at Enterprise Connect 2026, new Trailhead trail live
- **Source:** X @trailhead (8 likes, 583 views), @Red_Hibbert_LLC, @johniosifov
- **URL:** https://sforce.co/4swkscI (Trailhead trail) | https://x.com/trailhead/status/2034738713138254096
- **Summary:** Salesforce launched "Agentforce Contact Center" at Enterprise Connect 2026 — positioned as "the only contact center solution that unifies voice, digital, CRM, and AI agents natively." Trailhead trail launched with it. Multiple practitioners noting it. Product extends Agentforce's footprint into contact center/voice territory — relevant to JT's Agentforce consulting positioning and job market target (AI Solutions Architect roles at Salesforce shops).
- **Relevance:** JT Somwaru Consulting (Agentforce niche) / Job Market (upskill signal for AI Implementation Lead targeting)
- **Fits:** job-market-agent / jt-consulting-pipeline
- **Cost:** Free (Trailhead learning); Contact Center license required for deployment
- **Severity rationale:** New Agentforce product = new consulting surface + Trailhead trail is actionable today. JT should complete the trail this week for job market differentiation. Doesn't unblock active client work (no Salesforce client yet) but directly hits job market positioning.

### 🟡/🟢 findings (KB only)
- Kimi K2.5 — leading open-weights model, closer to frontier. No immediate routing impact.
- Agentforce Contact Center GA — Voice+CRM+AI native, "End of Frankenstein Contact Center." Consulting context but no active Salesforce client.
- n8n-local-desktop (kkomelin/n8n-local-desktop) — Fully local n8n + Ollama. Demo use case.
- Google Colab MCP Server — AI agents can interact with Colab directly. Low priority.
- Fingerprint MCP Server (fraud detection) — Insurance niche relevant, no active insurance client.
- General Input — "Zapier for AI agents" by @jackjoliet. Early stage, unverified.

### 2026-03-24 🟡/🟢 findings (KB only)
- HubSpot named #8 Fast Company Most Innovative 2026 — cited as "first CRM to connect to ChatGPT, Claude, AND Gemini." Validates existing HubSpot MC tasks.
- Errand AI — MCP-native automation platform, exposes its own MCP endpoint for IDE delegation. Early stage.
- n8n Electron wrapper — local n8n + Ollama in desktop app. Demo/accessibility angle, not production relevant.
- Kimi K2.5 — open-weights model advancing toward frontier. No routing impact at current scale.
- Synapse SDK — built-in MCP server exposing agent toolkit to Claude Desktop/Cursor/VS Code. Solanum-related.

