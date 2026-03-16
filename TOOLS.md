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

## Cloudflare Browser Rendering — /crawl (preferred for full-site crawls)
- Replaces Firecrawl for full-site ingestion. One API call crawls an entire site.
- Async: POST to start → receive job_id → GET to poll results
- Free during beta for `render: false` (static sites). Headless/JS rendering billed under Workers pricing.
- Supports: HTML, Markdown, JSON output | incremental re-crawls via `modifiedSince` | depth/limit/pattern controls
- **Primary use cases:** H.C. Oswald RAG ingestion (Shopify catalog), prospect full-site crawls in research-agent
- Endpoint: `POST https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl`
- Auth: `Authorization: Bearer <CF_API_TOKEN>` | Credentials in `~/.config/env/global.env` (CF_ACCOUNT_ID, CF_API_TOKEN)
- Quick example (static site, markdown):
  ```
  curl -X POST 'https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl' \
    -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' \
    -d '{"url":"https://example.com","formats":["markdown"],"render":false,"options":{"includePatterns":["https://example.com/products/**"]}}'
  ```
- Structured extraction (JSON + prompt): add `"formats":["json"],"jsonOptions":{"prompt":"Extract services, tech stack, key contacts"}`
- Docs: https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/

## Page CRO Reference (on-demand — coreyhaines31/marketingskills)
- Full CRO framework at: https://github.com/coreyhaines31/marketingskills/tree/main/skills/page-cro
- Use when: optimizing jtsomwaru.com conversions, or auditing a client's landing page
- Framework covers: value prop clarity, headline effectiveness, CTA friction, social proof placement, mobile experience
- Not installed as a skill (low frequency) — fetch the SKILL.md directly when needed

## Deepgram Nova-2 (not yet configured — future use)
- Speech-to-text API | $0.002/min | Multi-speaker detection, fast turnaround
- Use case: Phase 2 UGC pipeline (script timing verification), any future transcription at scale
- Current alternative: Groq whisper-large-v3 (free, already configured) — prefer Groq for single-speaker tasks
- Docs: https://developers.deepgram.com | Sign up + add API key to global.env when needed

## Firecrawl (fallback — use /crawl above for full-site work)
- Key: fc-0d0961fa920a466a869fdd4068b9fe7e
- `POST https://api.firecrawl.dev/v1/scrape` `{"url":"...","formats":["markdown"]}`
- Auth header: `Authorization: Bearer fc-0d0961fa920a466a869fdd4068b9fe7e`
- Use for: single-page scrapes where Cloudflare /crawl is overkill

## Scrapling
- Library: `pip install "scrapling[ai]"` — adaptive Python web scraping framework
- NOT a native OpenClaw feature — used inside Python scripts exec'd by OpenClaw
- Key classes: `Fetcher` (fast HTTP + TLS fingerprint spoofing), `StealthyFetcher` (Cloudflare bypass), `DynamicFetcher` (Playwright browser automation)
- Adaptive selectors: `page.css('.selector', auto_save=True)` — auto-relocates elements when site structure changes
- MCP server: `scrapling.readthedocs.io/en/latest/ai/mcp-server/` — wire as tool in research-agent for consulting pipeline
- Docs: scrapling.readthedocs.io | GitHub: github.com/D4Vinci/Scrapling
- Use case: StreetEasy scraper resilience (upgrade plan: memory/analysis/scrapling-evaluation-2026-03-02.md)

## OpenRouter
- Status: ✅ Active | Profile: openrouter:default
- Routing: Anthropic → direct (prompt caching = 90% savings). Everything else → openrouter/provider/model
- Key models: openrouter/openai/gpt-4o | openrouter/x-ai/grok-3 | openrouter/google/gemini-2.5-pro | openrouter/google/gemini-2.5-flash-preview | openrouter/google/gemini-3.1-flash-lite-preview | openrouter/google/gemini-3-pro-preview | openrouter/moonshot/kimi-k2 | openrouter/deepseek/deepseek-r1
- **Image generation:** `google/gemini-2.5-flash-image` (NB1, GA) | `google/gemini-3.1-flash-image-preview` (NB2, $0.50/$3 per M) — NB2 adds visual grounding (searches web for real locations/species before generating), extreme aspect ratios (1:4, 1:8 for banners), 512px option, thinking mode toggle (off by default). 95% of Pro quality. Cost workflow: Batch API (50% discount) → 5-8 variations at 512px → upscale winner only. Thinking ON only for complex infographics or visual grounding + spatial reasoning.
- Gemini 2.5 Pro: $1.25/$10 per M tokens, 1M context, flat pricing — use for large doc analysis (>100K tokens), RAG ingestion. Gemini 3-pro-preview: $2/$12 (≤200K) or $4/$18 (>200K) — better reasoning but expensive at large context, not worth it for doc ingestion.
- Gemini 3.1 Flash-Lite: $0.25/$1.50 per M tokens, 1M context, 2.5x faster than 2.5 Flash, 45% faster output — use for cheap high-volume tasks: KB reads, content batch gen, summarization, quick lookups. Replaces gemini-2.5-flash-preview for non-reasoning tasks. Verified routing: google/gemini-3.1-flash-lite-preview-20260303.
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

## Claude Code Agent Personas (~/.claude/agents/)
Installed on Mac mini from github.com/msitarzewski/agency-agents. Available to all ACP sessions spawned via sessions_spawn.

**When to activate a persona:**
- ✅ Open-ended tasks with no detailed spec (e.g., "refactor this however you see fit," "build a frontend component from scratch")
- ✅ JT using Claude Code interactively on his personal device — primary use case
- ❌ ACP spawns that already have a detailed task prompt — the task IS the instruction, persona adds noise
- ❌ Sessions with existing specialized AGENT.md files (overnight, outreach, portfolio updater) — don't override
- ❌ Tasks with strict output format requirements

**How to activate (only when criteria above are met):**
Include in the task prompt: *"Activate [Agent Name] mode for this session."*

| Task type | Agent | File |
|---|---|---|
| Frontend/UI work (open-ended) | Frontend Developer | engineering/engineering-frontend-developer.md |
| Agentforce/ML/AI (open-ended exploration) | AI Engineer | engineering/engineering-ai-engineer.md |
| iOS/mobile (open-ended) | Mobile App Builder | engineering/engineering-mobile-app-builder.md |
| Backend/API/DB (open-ended) | Backend Architect | engineering/engineering-backend-architect.md |
| Infrastructure, scripts, CI/CD (open-ended) | DevOps Automator | engineering/engineering-devops-automator.md |
| Quick POC/prototype | Rapid Prototyper | engineering/engineering-rapid-prototyper.md |
| Code review/refactor (open-ended) | Senior Developer | engineering/engineering-senior-developer.md |
| App Store optimization | App Store Optimizer | marketing/marketing-app-store-optimizer.md |
| SEO content | SEO Specialist | marketing/marketing-seo-specialist.md |
| Reddit content (open-ended) | Reddit Community Builder | marketing/marketing-reddit-community-builder.md |

## Consulting Pipeline Agents (~/projects/)
- research-agent/ | analysis-agent/ | n8n-agent/ (n8n: localhost:5678) | agentforce-agent/ (sf CLI needed)
- crypto-agent/ | job-market-agent/ | ranking-app-agent/
- Pipeline: ~/projects/jt-consulting-pipeline/ | Skill: skills/jt-consulting-pipeline/SKILL.md

## Drive Drafts
- Script: scripts/drive_drafts.py | Account: openclawagenteve14@gmail.com | Root: "Eve — Drafts"
- **Preferred: use `--path` for full control** (supports deep folder structure)
- **Folder structure (post-2026-03-09 restructure):**
  ```
  Eve — Drafts/
  ├── Consulting/
  │   ├── Clients/[Client Name]/Outreach/LinkedIn/
  │   ├── Clients/[Client Name]/Outreach/Email/
  │   ├── Clients/[Client Name]/Decks/
  │   ├── Clients/[Client Name]/Research/
  │   ├── Templates/
  │   └── Case Studies/
  ├── Content/
  │   ├── X/
  │   └── LinkedIn/
  ├── Job Applications/
  │   ├── Resumes/
  │   └── Cover Letters/
  ├── Research/
  ├── Frameworks/
  └── Analysis/
  ```
- **Routing table:**
  | Content type | `--path` value |
  |---|---|
  | Client LinkedIn outreach DMs | `Consulting/Clients/[Client]/Outreach/LinkedIn` |
  | Client cold emails | `Consulting/Clients/[Client]/Outreach/Email` |
  | Proposal decks | `Consulting/Clients/[Client]/Decks` |
  | Resumes | `Job Applications/Resumes` |
  | Cover letters | `Job Applications/Cover Letters` |
  | X posts (personal brand) | `Content/X` |
  | LinkedIn posts (personal brand) | `Content/LinkedIn` |
  | Vibe marketing review (Nash Satoshi) | `Content/Vibe Marketing/Nash Satoshi` |
  | Vibe marketing review (Vista) | `Content/Vibe Marketing/Vista` |
  | Vibe marketing review (future products) | `Content/Vibe Marketing/[Product Name]` |
  | Research files | `Research` |
  | Framework/methodology docs | `Frameworks` |
  | Analysis reports | `Analysis` |
  | T2/template decks | `Consulting/Templates` |
- **Command:**
  ```
  cd ~/.openclaw/workspace && python3 scripts/drive_drafts.py \
    --title "[Descriptive Title]" --path "[path from table above]" --file [path]
  ```
- **Legacy `--project`/`--type`** still works for non-consulting projects (e.g. Vista, Nash Satoshi)

## Mission Control — Task Push Template
- **Quick push (copy-paste and fill in):**
  ```
  curl -s -X POST http://localhost:3000/api/tasks \
    -H 'Content-Type: application/json' \
    -d '{"title":"[TITLE]","description":"[DESCRIPTION]","status":"todo","priority":"[high|medium|low]","assignee":"[eve|JT]","project":"[Job Market|Skills|Consulting|passive-income]","sortOrder":[N]}'
  ```
- **Check for duplicates first:** `curl -s http://localhost:3000/api/tasks | python3 -c "import sys,json; [print(t['title']) for t in json.load(sys.stdin)]" | grep -i "[keyword]"`
- **sortOrder bands:** HIGH: 10-40 quick wins | 50-90 alerts | 100+ strategic | MEDIUM: 10,20,30… | speculative: 500+

## Consulting Pipeline Drive Sync
- Script: `python3 ~/.openclaw/workspace/scripts/pipeline_drive_sync.py --slug [slug] --client "[Name]" --stage [deck|outreach|all]`
- Syncs deck + outreach draft to Google Drive: Eve — Drafts / Consulting / Clients / [Company Name] / Outreach|Decks/
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
