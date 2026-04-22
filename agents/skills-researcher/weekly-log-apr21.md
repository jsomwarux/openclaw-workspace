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
