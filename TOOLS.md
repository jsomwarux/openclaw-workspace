# TOOLS.md — Tool Reference
> ⚠️ Check this file BEFORE saying "I can't do that." You probably can.
> Full docs: docs/tools/TOOLS-full.md

## Health System
- DB: ~/.openclaw/workspace/health/health.sqlite
- CLI (from health/ dir): `python3 health.py --log "reply" [--date YYYY-MM-DD] | --report | --history [n] | --show DATE`
- Schedule: 9PM daily check-in prompt | Sunday 9AM weekly report

## Cost Tracker
- `python3 ~/.openclaw/workspace/scripts/cost-tracker.py --snapshot | --brief | --check-alerts | --weekly-review`
- Snapshot runs at 2AM via backup.sh → memory/costs/YYYY-MM-DD.json
- Alerts: session >$2, daily >$10, monthly pace >$75 | Goal: $50/mo

## Audit Trail
- `python3 ~/.openclaw/workspace/scripts/log-proof.py --type TYPE --title "..." --description "..." --outcome success|failure|partial [--files PATH]`
- Daily JSONL: proofs/YYYY-MM-DD/actions.jsonl

## Restart Script
- `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"` — sends direct Telegram notification before restart (NO cron jobs created)

## Diagnostics
- `openclaw doctor` — health check on gateway, channels, providers, cron scheduler
- `openclaw doctor --fix` — auto-fix common issues (use when something's broken and root cause isn't obvious)

## 🚨 Rate Limit Recovery (known workarounds)

### Cooldown Persistence Bug
Cooldown state is saved to `~/.openclaw/agents/main/agent/auth-profiles.json` and survives restarts.
Even after the actual rate limit clears, the gateway stays blocked until the file is wiped.
**Symptom:** Persistent "provider in cooldown" errors that don't resolve after waiting.
**Fix (run from terminal):**
```
python3 -c "import json,os; path=os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json'); d=json.load(open(path)); d['usageStats']={}; json.dump(d,open(path,'w'),indent=2)"
```
Then restart the gateway.

### Telegram Queue Re-Delivery Loop
On gateway restart, Telegram re-delivers any unprocessed messages. If those trigger an API call that fails (rate_limit), the cooldown gets re-written → restart → same message re-delivered → fail again → infinite loop.
**Fix:** Flush the Telegram update queue before restarting when in a rate-limit state:
```
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates?offset=-1"
```
Replace `<TOKEN>` with the bot token from `~/.config/env/global.env`.

## Backups
- `~/.openclaw/workspace/scripts/backup.sh` | LaunchAgent: com.openclaw.backup | 2AM daily | 7-day retention
- Log: ~/.openclaw/backups/backup.log

## Session Cleanup
- `~/.openclaw/workspace/scripts/cleanup-sessions.py` | LaunchAgent: com.openclaw.cleanup-sessions | 3AM daily

## Task Queue
- File: ~/.openclaw/workspace/tasks/pending.jsonl
- Schema: {id, created_at, priority (high|medium|low), title, task, context, status}
- Cron: every 2h 8AM–10PM EST (main session) — reduced from 30min post-incident to stay under 20/day cap

## X Research Skill
- `cd ~/.openclaw/workspace/skills/x-research && source ~/.config/env/global.env && bun run x-search.ts search "query" --quick --limit 5`
- Cost: ~$0.50/100 tweets. Use --quick --limit 5 for cheap lookups.

## Firecrawl
- Key: fc-0d0961fa920a466a869fdd4068b9fe7e
- `POST https://api.firecrawl.dev/v1/scrape` `{"url":"...","formats":["markdown"]}`
- Auth header: `Authorization: Bearer fc-0d0961fa920a466a869fdd4068b9fe7e`

## Scrapling
- Library: `pip install "scrapling[ai]"` — adaptive Python web scraping framework
- NOT a native OpenClaw feature — used inside Python scripts exec'd by OpenClaw
- Key classes: `Fetcher` (fast HTTP + TLS fingerprint spoofing), `StealthyFetcher` (Cloudflare bypass), `DynamicFetcher` (Playwright browser automation)
- Adaptive selectors: `page.css('.selector', auto_save=True)` — auto-relocates elements when site structure changes
- MCP server: `scrapling.readthedocs.io/en/latest/ai/mcp-server/` — wire as tool in research-agent for Opticfy pipeline
- Docs: scrapling.readthedocs.io | GitHub: github.com/D4Vinci/Scrapling
- Use case: StreetEasy scraper resilience (upgrade plan: memory/analysis/scrapling-evaluation-2026-03-02.md)

## OpenRouter
- Status: ✅ Active | Profile: openrouter:default
- Routing: Anthropic → direct (prompt caching = 90% savings). Everything else → openrouter/provider/model
- Key models: openrouter/openai/gpt-4o | openrouter/x-ai/grok-3 | openrouter/google/gemini-2.5-pro | openrouter/google/gemini-2.5-flash-preview | openrouter/google/gemini-3-pro-preview | openrouter/moonshot/kimi-k2 | openrouter/deepseek/deepseek-r1
- Gemini 2.5 Pro: $1.25/$10 per M tokens, 1M context, flat pricing — use for large doc analysis (>100K tokens), RAG ingestion. Gemini 3-pro-preview: $2/$12 (≤200K) or $4/$18 (>200K) — better reasoning but expensive at large context, not worth it for doc ingestion.
- Full list: https://openrouter.ai/models | Experiments log: memory/costs/model-experiments.jsonl

## Knowledge Base
- CLI (from knowledge/ dir): `bun kb.ts search "query" | add --title "..." --content "..." --category CATEGORY | list | show <id>`
- Categories: business, tech, crypto, personal, projects | DB: knowledge/kb.sqlite

## Browser Profile
- Path: ~/.openclaw/browser-profile | Logged into: Google, GitHub | Refresh every ~10 days

## Mission Control Dashboard
- Next.js at http://localhost:3000 | Convex at port 3210
- LaunchAgents: com.openclaw.mission-control-convex + com.openclaw.mission-control-next
- Task API: `POST http://localhost:3000/api/tasks`
- **Recovery** (if board unreachable): `launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-convex && launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-next` — do NOT just log "may be down"; attempt kickstart immediately

## Opticfy Pipeline Agents (~/projects/)
- research-agent/ | analysis-agent/ | n8n-agent/ (n8n: localhost:5678) | agentforce-agent/ (sf CLI needed)
- crypto-agent/ | job-market-agent/ | ranking-app-agent/
- Pipeline: ~/projects/opticfy-pipeline/ | Skill: skills/opticfy-pipeline/SKILL.md

## Drive Drafts
- Script: scripts/drive_drafts.py | Account: openclawagenteve14@gmail.com | Root: "Eve — Drafts"

## Opticfy Pipeline Drive Sync
- Script: `python3 ~/.openclaw/workspace/scripts/pipeline_drive_sync.py --slug [slug] --client "[Name]" --stage [deck|outreach|all]`
- Syncs deck + outreach draft to Google Drive: Eve — Drafts / Opticfy — Client Pipeline / [Company Name]/
- Run after deck-built and outreach-drafted stages. Include Drive links in JT's review message.
- List synced clients: `python3 scripts/pipeline_drive_sync.py --list`

## Notion — Viral Post Swipe File
- Integration token: ntn_I6090101509856iOb9JOeecrHaqzwG24r7PCjud0PE49iU
- Database ID: 31316aff930580f6a195ca179793eb0e
- Push script: `python3 ~/.openclaw/workspace/scripts/notion-swipe-push.py --text "..." --author "@handle" --url "..." --niche "AI Agents" --format "Hot Take" --why "..." --engagement 1200 --hook "Contrarian claim"`
- Seed script: `python3 ~/.openclaw/workspace/scripts/notion-swipe-seed.py` (one-time bulk population)
- Cron: 3x/week Mon/Wed/Fri 5:30AM EST isolated sonnet — searches X for viral posts, pushes to Notion
- X Algorithm reference: ~/.openclaw/workspace/docs/x-algorithm.md

## Apps
- jtsomwaru.com: ~/projects/jtsomwaru-com/ → Vercel
- Glow Index: Replit | Admin: /admin?key=glowindex-admin-2024-secret | jsomwarux/skincare-rankings
- Nash Satoshi: jsomwarux/Nash-Satoshi (private)
