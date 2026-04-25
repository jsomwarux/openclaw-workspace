## 2026-04-20 — Daily Scan

### 🔴/🟠 Findings
1. [🟠 OpenAI Codex April 2026 — macOS native control + sandboxed execution] (2026-04-17)
   - Source: X @coo_pr_notes + OpenAI changelog
   - Key capability: Codex can now launch agent that operates Mac by controlling mouse+keyboard in sandboxed virtual workspace — no focus stealing
   - Also: OpenAI Agents SDK update, GPT-5.4 announced, native sandbox execution
   - Competitive impact: directly competes with OpenClaw node control for Apple device use cases
   - Quality gate: PASS — specific first action (read Codex changelog, compare to OpenClaw)
   - Fits: OpenClaw ecosystem intelligence | Cost: free | Via: X + web
   - Shoutout opportunity: NO

2. [🟠 claude-mem — Claude Code persistent memory plugin (12.9K GitHub stars)] (2026-04-20)
   - Source: X @claude_news + github.com/thedotmack/claude-mem
   - Key capability: persistent memory across Claude Code sessions — remembers project structure + past decisions
   - Impact: Eve n8n-agent spawns Claude Code for n8n builds. Without memory, every spawn re-explains architecture. claude-mem eliminates this per-build overhead
   - Quality gate: PASS — specific first action (install + configure in n8n-agent workflow)
   - Fits: n8n-agent | Cost: free (MIT) | Via: X @claude_news + web
   - Shoutout opportunity: NO

### 🟡 Findings (KB)
3. OpenClaw v2026.4.19 — beta fixes: streaming usage reporting + cross-agent routing through bound channel accounts. Minor.
4. Humwork (YC-backed) — connects AI agents with verified human experts when models fail. Human-in-the-loop startup. KB only.
5. Insurance AI signals (Query 6) — claims processing, underwriting, agentic AI in insurance. COVU anchor ICP signal. KB only.
6. CopilotKit MCP docs replacement — performance fix for third-party MCP, not new capability. KB only.
7. VictoriaMetrics MCP server — new UI + inspector, not in JT stack. KB only.
8. ClaudeKit /ck:agentize — CLI + MCP server generator, dev tooling. KB only.

### Quality Gate Results
- Pushed to MC: 2 (OpenAI Codex April 2026, claude-mem)
- KB only: 6
- Telegram JT: YES (2 🟠 findings)
## 2026-04-21 — Daily Scan

### 🔴/🟠 Findings — 3 items, all passed quality gate

1. [🟠 OpenClaw MyClaw — per-agent model picks + 13,700-skill marketplace]
   - Source: X @rohanpaul_ai (48 likes, 7.2K impressions) https://x.com/rohanpaul_ai/status/2044425195587506404
   - Key capability: Per-agent model assignment now live in OpenClaw 3.24. MyClaw companion ships skills instantly. 13,700+ skills in marketplace.
   - Impact: Eve can assign Flash-Lite to cheap crons, Sonnet only where needed — no openclaw.json editing required
   - Quality gate: PASS — first action: openclaw skills search --marketplace + test per-agent model assign
   - Shoutout: YES — OpenClaw is JT's active stack. See shoutout-opportunities.md.
   - MC: pushed ✅

2. [🟠 Shopify Official MCP Server — released 2026-04-09]
   - Source: X @BadalXAI https://x.com/BadalXAI/status/2045355511785156855
   - Key capability: Official Shopify MCP server = Claude can query Shopify catalogs natively
   - Impact: H.C. Oswald is a Shopify store and active prospect. This replaces the custom Cloudflare crawl approach for catalog RAG — and makes for a stronger demo
   - Quality gate: PASS — first action: npx @shopify/mcp-server + read shopify.dev/docs/api/mcp
   - Shoutout: NO (Shopify not in JT's active build stack)
   - MC: pushed ✅

3. [🟠 Claude Code Routines — scripted multi-step agent sequences]
   - Source: X @DataChaz (613 likes, 129.5K impressions) https://x.com/DataChaz/status/2044166157905912171
   - Key capability: Routines run scripted agent sequences without user supervision. OSS clone (Multica Autopilot) already out.
   - Impact: Every n8n-agent build re-issues the same 10 setup instructions. A routine eliminates that. Direct build quality + speed improvement.
   - Quality gate: PASS — first action: read anthropic.com/news/claude-code-routines + create ~/projects/n8n-agent/routines/standard-build.md
   - Shoutout: YES — Claude/Anthropic is JT's active stack. See shoutout-opportunities.md.
   - MC: pushed ✅

### 🟡 Findings (KB only)
4. Further AI — first AI orchestration layer built specifically for insurance. Launched today. Competitive niche signal. Logged to niche-fitness-signals.md.
5. InsurTechNY — "Most AI pilots stall before production due to integration complexity." Validates JT's pitch angle. Content angle.
6. OpenClaw v2026.4.20-beta.1 — setup wizard restyle only. Minor.
7. Claude Mythos mention — X-only, 1 like, unverified. Skip.
8. ios-simulator-mcp — iOS dev tooling, not in JT stack.
9. GLM-5.1 open model on FriendliAI — not in stack.

### Quality Gate Results
- Pushed to MC: 3 (MyClaw per-agent models, Shopify MCP, Claude Code Routines)
- KB only: 6
- Telegram JT: YES (3 🟠 findings, 2 shoutout opportunities)

## 2026-04-22 — Daily Scan

### 🔴 Findings — 1 item, passed quality gate

1. [🔴 n8n webhook exploit — Cisco Talos advisory, active malware campaigns]
   - Source: Cisco Talos blog https://blog.talosintelligence.com/the-n8n-n8mare/ + X @dailytechonx; The Hacker News confirmed
   - Key finding: n8n webhook URLs actively abused in phishing/malware campaigns since Oct 2025. Volume 686% higher in March 2026 vs Jan 2025. Attack vector: embed n8n webhook URL in phishing email, webhook triggers workflow that fingerprints device + delivers payload.
   - Impact: JT self-hosts n8n (localhost:5678 via Tailscale). Any workflow with a publicly accessible webhook trigger is a potential attack surface. Aya client workflows run on this instance.
   - Quality gate: PASS — first action: read Talos advisory + audit all active webhook workflows
   - Shoutout: NO (security advisory, not a release)
   - MC: pushed ✅ (priority: high)

### 🟡 Findings (KB only)
2. Google Deep Research Max — MCP support + Gemini 3.1 Pro, launched Apr 21. Can connect to private data via MCP. Interesting for future research-agent upgrade but not actionable vs current stack.
3. OpenAI gpt-image-2 — production image model via API, available now. Not in JT stack.
4. freshkeeper (npx) — one-command updater for Claude Code/Codex/OpenClaw. 0 GitHub stars, created Apr 21. Unverified — skip per <50 stars rule.
5. Claude Code v2.1.110 — /tui command, push notifications, plugin favorites. Minor UX, no new capability.
6. Further AI insurance orchestration (already logged Apr 21) — growing engagement (75 likes, 30.6K impressions). Confirmed competitor signal.
7. gpt-image-2 in OpenAI / Codex — not in JT stack.

### Quality Gate Results
- Pushed to MC: 1 (n8n webhook exploit — HIGH priority)
- KB only: 6
- Telegram JT: YES (1 🔴 security finding)

## 2026-04-23 — Daily Scan

### X API STATUS
All 6 X queries failed — 402 CreditsDepleted. Full fallback to Tier 1/2 web sources.

### 🟠 Findings — 1 item, passed quality gate

1. [🟠 OpenClaw v2026.4.22 — xAI TTS/image gen + /models add from chat + TUI embedded mode]
   - Source: https://github.com/openclaw/openclaw/releases/tag/v2026.4.22 (released 2026-04-23)
   - Key changes:
     * Providers/xAI: grok-imagine-image, grok-imagine-image-pro, reference-image edits, 6 live voices, MP3/WAV/PCM/G.711 TTS, grok-stt transcription, xAI realtime STT for Voice Call streaming
     * /models add <provider> <modelId> command — register any model from chat without gateway restart
     * TUI local embedded mode — terminal chats without Gateway, plugin approval gates still enforced
     * Auto-install missing provider/channel plugins during setup
     * OpenAI Responses: native web_search tool auto-used when web search enabled
     * WhatsApp per-group systemPrompt config
   - Impact: /models add directly speeds up model testing. xAI TTS adds a provider JT can use for Telegram voice replies. TUI mode enables offline prompt testing.
   - Quality gate: PASS — first action: openclaw update then /models add xai grok-imagine-image-pro
   - Shoutout: YES — OpenClaw is JT's active stack. See shoutout-opportunities.md.
   - MC: pushed ✅ (priority: medium, id: j57bxs2feqfkr7zd9p4jcx6b4585cvj6)

### 🟡 Findings (KB only)
2. Claude Mythos Preview (Apr 7, 2026) — confirmed on Bedrock + Vertex AI. "New class of intelligence for cybersecurity, autonomous coding, long-running agents." Gated to 11 organizations. Not publicly accessible.
3. Claude Design — Anthropic Labs product launched with Opus 4.7. Visual outputs: designs, prototypes, slides, one-pagers. claude.ai only, no API yet. Watch for API availability.
4. n8n 2.17.6 (Apr 23) — minor bug fix: user search in ProjectSettings. No capability changes.
5. n8n workflow limits removal — Aug 2025 announcement, not new. Already in effect.
6. Insurance AI signals — InsuranceJournal "AI makes claims professionals better" coverage. Generic market validation, no actionable signal.

### Quality Gate Results
- Pushed to MC: 1 (OpenClaw v2026.4.22 — MEDIUM priority)
- KB only: 5
- Telegram JT: YES (1 🟠 finding, 1 shoutout opportunity)
- X API: depleted — full web fallback used

## 2026-04-23 — Daily Scan (re-run detected)

### X API STATUS
All 6 X queries failed — 402 CreditsDepleted. Full fallback to Tier 1/2 web sources.

### 🟠 Findings — 1 item, already in MC

1. [🟠 OpenClaw v2026.4.22 — xAI TTS/image gen + /models add from chat + TUI embedded mode]
   - Source: https://github.com/openclaw/openclaw/releases/tag/v2026.4.22 (released 2026-04-23)
   - Key changes:
     * Providers/xAI: grok-imagine-image, grok-imagine-image-pro, reference-image edits, 6 live voices, MP3/WAV/PCM/G.711 TTS, grok-stt transcription, xAI realtime STT for Voice Call streaming
     * /models add <provider> <modelId> command — register any model from chat without gateway restart
     * TUI local embedded mode — terminal chats without Gateway, plugin approval gates still enforced
     * Auto-install missing provider/channel plugins during setup
     * OpenAI Responses: native web_search tool auto-used when web search enabled
     * WhatsApp per-group systemPrompt config
   - Impact: /models add directly speeds up model testing. xAI TTS adds a provider JT can use for Telegram voice replies. TUI mode enables offline prompt testing.
   - Quality gate: PASS — first action: openclaw update then /models add xai grok-imagine-image-pro
   - Shoutout: YES — OpenClaw is JT's active stack.
   - MC: DUPLICATE — already pushed yesterday (id: j57bxs2feqfkr7zd9p4jcx6b4585cvj6)

### 🟡 Findings (KB only)
2. Claude Mythos Preview (Apr 7, 2026) — confirmed on Bedrock + Vertex AI. "New class of intelligence for cybersecurity, autonomous coding, long-running agents." Gated to 11 organizations. Not publicly accessible.
3. Claude Design — Anthropic Labs product launched with Opus 4.7. Visual outputs: designs, prototypes, slides, one-pagers. claude.ai only, no API yet. Watch for API availability.
4. n8n 2.17.6 (Apr 23) — minor bug fix: user search in ProjectSettings. No capability changes.
5. n8n workflow limits removal — Aug 2025 announcement, not new. Already in effect.
6. Insurance AI signals — InsuranceJournal "AI makes claims professionals better" coverage. Generic market validation, no actionable signal.

### Quality Gate Results
- Pushed to MC: 0 (duplicate skipped)
- KB only: 5
- Telegram JT: NO (duplicate finding, no new actionable items)
- X API: depleted — full web fallback used

## 2026-04-24 — Daily Scan

### X API STATUS
✅ All 6 queries successful (~$0.30 total)

### 🔴 Findings — 1 item, passed quality gate

1. [🔴 MCP RCE vulnerability — CVE-2026-30615, 200k+ servers at risk]
   - Source: X @isectech_ + The Hacker News https://thehackernews.com/2026/04/anthropic-mcp-design-vulnerability.html + The Register https://www.theregister.com/2026/04/16/anthropic_mcp_design_flaw/
   - Key finding: OX Security researchers disclosed MCP design flaw enabling Arbitrary Command Execution (RCE). CVE-2026-30615 on Windsurf is zero-click — no user interaction needed, just loading a project with malicious MCP config. 200,000+ AI servers exposed.
   - Impact: JT uses MCP servers (Shopify MCP, research-agent MCP tools). Supply chain attack vector — any untrusted MCP server or cloned repo with malicious MCP config = potential RCE.
   - Quality gate: PASS — first action: read advisories + audit all installed MCP servers
   - Shoutout: NO (security advisory)
   - MC: pushed ✅ (priority: high, id: j576c6j3gac3v7ttwgm53kzmh585eghm)

### 🟡 Findings (KB only)
2. GitHub CLI v2.90 `gh skill` command — package manager for agent skills across Copilot/Claude Code/Cursor/Codex. Confirmed on GitHub Changelog. Not in JT's workflow (OpenClaw-centric stack).
3. Weaviate 1.37 MCP server — built-in MCP at /v1/mcp. Not in JT's stack (uses Convex + Qdrant).
4. Further AI insurance — 78❤️/31.8K impressions (continued growth). Already logged Apr 21-22.
5. Claude Code removed from new Pro signups — doesn't affect JT (already has access).
6. freshkeeper — 0 stars, unverified per <50 stars rule.
7. Agentrig — plugin layer for multi-agent install. Not in JT's stack.
8. AInsure alpha — insurance AI platform with 10+ agents. Competitor signal, no actionable intel.

### Quality Gate Results
- Pushed to MC: 1 (MCP RCE vulnerability — HIGH priority)
- KB only: 7
- Telegram JT: YES (1 🔴 security finding)
