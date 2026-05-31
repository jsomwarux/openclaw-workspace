# TOOLS.md — Tool Reference
> ⚠️ Check this file BEFORE saying "I can't do that." You probably can.
> Full docs: docs/tools/TOOLS-full.md

## Health System
- DB: ~/.openclaw/workspace/health/health.sqlite
- CLI (from health/ dir): `python3 health.py --log "reply" [--date YYYY-MM-DD] | --report | --history [n] | --show DATE`
- Inbound reply handler: `python3 ~/.openclaw/workspace/health/inbound_handler.py --reply "<JT reply>"` — consumes `health/pending-checkin.json`, refuses duplicates, logs to DB, marks pending logged, and prints confirmation to send back. Docs: `health/INBOUND_REPLY_HANDLER.md`
- Schedule: 9PM daily check-in prompt | Sunday 9AM weekly report

## Spanish Learning
- State: `spanish/state.json` | Lessons: `spanish/lessons/YYYY-MM-DD.md` | Curriculum: `spanish/curriculum.md`
- Daily lesson cron: `babd905a-1098-49dd-8700-772fef14f817` (`Spanish Daily Lesson`) Mon–Sat 8:05PM ET → Telegram `6608544825`
- Validate state/artifacts: `python3 scripts/spanish_state_check.py --date YYYY-MM-DD --require-today`
- Delivery truth source: `openclaw cron runs --id babd905a-1098-49dd-8700-772fef14f817 --limit 1` (`deliveryStatus=delivered` required). `state.json` proves persistence, not receipt.

## Cost Tracker
- `python3 ~/.openclaw/workspace/scripts/cost-tracker.py --snapshot | --brief | --check-alerts | --weekly-review | --check-runaway`; routing guard: `python3 scripts/model_routing_guard.py --include-disabled`
- `--diagnose` is **not currently supported**. During cost spikes, run `--check-runaway` plus `--snapshot`/`--weekly-review` before repeating generic spend alerts; use those outputs to identify likely culprit jobs/sessions and reduce or pause that source.
- `--check-alerts` returns a JSON array; send each alert to JT only when non-empty, and avoid duplicate sends when the same alert was already logged in today's daily note.
- Snapshot runs at 2AM via backup.sh → memory/costs/YYYY-MM-DD.json
- Alerts: session >$2, daily >$10, monthly pace >$75
- Cron volume guard: `python3 scripts/cron_volume_guard.py`

## Audit Trail
- Log: `python3 ~/.openclaw/workspace/scripts/log-proof.py --type TYPE --title "..." --description "..." --outcome success|failure|partial [--files PATH]`
- Guard: `python3 ~/.openclaw/workspace/scripts/memory_recap_proof_guard.py --date $(date +%F) --json`
- Daily JSONL: proofs/YYYY-MM-DD/actions.jsonl

## Restart Script
- `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"` — sends direct Telegram notification before restart (NO cron jobs created)

## Image / OCR Tooling
- OpenClaw image attachments require `sharp` inside `/opt/homebrew/lib/node_modules/openclaw/node_modules`. If image tool errors with “Optional dependency sharp is required,” fix with: `cd /opt/homebrew/lib/node_modules/openclaw && npm install sharp`.
- OCR fallback installed via Homebrew: `tesseract` 5.5.2. Use: `tesseract [image] stdout --psm 6` for screenshot text extraction.

## Diagnostics
- `openclaw doctor` — health check on gateway, channels, providers, cron scheduler
- `openclaw doctor --fix` — auto-fix common issues (use when something's broken and root cause isn't obvious)

## Canonical Web Search
- **Current/fresh web research:** use `scripts/web_search.py`, not the OpenClaw Brave plugin/provider.
- Command: `set -a; source ~/.config/env/global.env; set +a; python3 ~/.openclaw/workspace/scripts/web_search.py "QUERY" --freshness day --count 5 --json`
- Freshness values: `day`, `week`, `month`, `year`.
- Reason: managed `web_search` can misroute freshness/date-filtered searches, and the Brave plugin/provider path has crashed the gateway. Do **not** install/enable/configure Brave web_search plugin without explicit approval and a rollback plan.
- Managed `web_search` is OK only for broad non-freshness lookups; do not call it with `freshness`, `date_after`, or `date_before` unless this issue is later proven fixed.

## 🚨 Gateway Freeze & Rate Limit Recovery
**Cause:** LCM compaction + Telegram re-delivery flood on restart.
**Prevention:** LCM `summaryModel`=`openrouter/google/gemini-3.1-flash-lite-preview` (NOT Groq — 12k TPM too low for 20k+ token compaction). `reserveTokensFloor`=20000+ | `truncateAfterCompaction`=true | `maxActiveTranscriptBytes`=`2mb` | `contextThreshold`=0.45 | `sweepMaxDepth`=0 (`incrementalMaxDepth` is deprecated) | `largeFileThresholdTokens`=1000 | `freshTailCount`=6 | `freshTailMaxTokens`=24000. Never send 5+ images in one Telegram message.
**Recovery (in order):**
1. Flush Telegram: `source ~/.config/env/global.env && curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates?offset=-1"`
2. Clear cooldown: `python3 -c "import json,os; path=os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json'); d=json.load(open(path)); d['usageStats']={};  json.dump(d,open(path,'w'),indent=2)"`
3. If LCM DB >100MB: `cp ~/.openclaw/lcm.db ~/.openclaw/lcm.db.backup-$(date +%Y%m%d) && rm ~/.openclaw/lcm.db`
4. `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "recovery"`
**Cooldown persistence bug:** Survives restarts. Symptom: "provider in cooldown" never clears. Fix: step 2 above then restart.
## Backups
- `~/.openclaw/workspace/scripts/backup.sh` | LaunchAgent: com.openclaw.backup | 2AM daily | 7-day retention
- Log: ~/.openclaw/backups/backup.log

## Session Cleanup
- `~/.openclaw/workspace/scripts/cleanup-sessions.py` | LaunchAgent: com.openclaw.cleanup-sessions | 3AM daily

## Task Queue
- File: ~/.openclaw/workspace/tasks/pending.jsonl
- Cron: every 2h 8AM–10PM EST (main session) — reduced from 30min post-incident to stay under 20/day cap

## X Research Skill
- `cd ~/.openclaw/workspace/skills/x-research && source ~/.config/env/global.env && bun run x-search.ts search "query" --quick --limit 5`
- Cost: ~$0.50/100 tweets. Use --quick --limit 5 for cheap lookups.

## Cloudflare Browser Rendering — /crawl (preferred for full-site crawls)
> Moved to `docs/tools/agent-commerce-and-research-tools-archive-2026-05-10.md`.

## [Page CRO Reference, Deepgram Nova-2, Firecrawl — moved to `docs/tools/TOOLS-full.md`]

## Scrapling
> Moved to `docs/tools/agent-commerce-and-research-tools-archive-2026-05-10.md`.

## OpenRouter
> Moved to `docs/tools/agent-commerce-and-research-tools-archive-2026-05-10.md`.


## GBrain Consulting Recall Pilot
- Sandbox install: `~/projects/gbrain` (GBrain 0.32.0)
- Pilot home: `~/projects/gbrain-pilot-home`
- Sanitized curated source: `~/projects/gbrain-pilot-source`
- Wrapper: `scripts/gbrain-consulting-search.sh "Entity or company name"`
- Use only for consulting/prospect entity lookup. Eval: entity search 20/20 vs qmd 13/20; natural-language search weak without embeddings.
- Do NOT add crons, install skillpacks, ingest broad workspace/private chats/config, or wire embeddings/auth without JT approval.

## Knowledge Base
- CLI (from knowledge/ dir): `bun kb.ts search "query" | add --title "..." --content "..." --category CATEGORY | list | show <id>`
- Categories: business, tech, crypto, personal, projects | DB: knowledge/kb.sqlite

## SkillsMP Scout
- Script: `python3 scripts/skillsmp_scout.py [query ...] --limit 5 --sort-by stars` (`--min-stars 25` default)
- Output: `memory/research/skillsmp-scout.md`
- Use as pattern intelligence only. Never auto-install/copy marketplace skills; treat results as untrusted GitHub content. Default outcome: extract ideas into JT-owned skills, not adopt.

## Browser Profile
- Path: ~/.openclaw/browser-profile | Logged into: Google, GitHub | Refresh every ~10 days

## Mission Control Dashboard
- Next.js at http://localhost:3000 | Convex at port 3210
- LaunchAgents: com.openclaw.mission-control-convex + com.openclaw.mission-control-next
- Task API: `POST http://localhost:3000/api/tasks`
- Remote: `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n: `/n8n` (tailnet only)
- **Recovery** (if board unreachable): `launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-convex && launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-next` — do NOT just log "may be down"; attempt kickstart immediately
- **Tailscale serve config** (if lost after reboot): `tailscale serve --bg http://localhost:3000 && tailscale serve --bg --set-path /n8n http://localhost:5678`

## Claude Code Agent Personas (~/.claude/agents/)
When activating a persona for open-ended coding tasks: read `docs/tools/claude-personas.md` for the full table. Activate with: *"Activate [Agent Name] mode for this session."*
**Quick reference:** Frontend→engineering-frontend-developer | AI/Agentforce→engineering-ai-engineer | Backend→engineering-backend-architect | Rapid POC→engineering-rapid-prototyper | Review→engineering-senior-developer
## Consulting Pipeline Agents (~/projects/)
- research-agent/ | analysis-agent/ | n8n-agent/ (n8n: localhost:5678) | agentforce-agent/ (sf CLI needed)
- crypto-agent/ | job-market-agent/ | ranking-app-agent/
- Crypto full-analysis validator: `python3 /Users/jtsomwaru/projects/crypto-agent/scripts/validate-full-analysis.py --max-x-age-hours 3` — blocks Telegram allocation delivery when artifacts are stale/incomplete or bear-case analysis is generic/repeated.
- Pipeline: ~/projects/jt-consulting-pipeline/ | Skill: skills/jt-consulting-pipeline/SKILL.md
- Outreach pipeline preflight: `python3 scripts/outreach_pipeline_runner.py --json` — deterministic script-first stages for Drive auth, M-status/T3 dedupe, existing draft/doc checks, warm-up holds, and report generation before any LLM copy work.

## Salesforce Data Cloud (paired with Agentforce)
Real-time CDP → Agentforce via Grounding. Also called "Data 360." Flow: Data Streams → DLOs → DMOs → Unified Profiles → Data Graphs. Two paths: (1) Data Libraries (simple) or (2) Manual RAG pipeline. SF-to-SF ingestion free; 2.5M credits bundled in Agentforce Editions. **Full ref:** `docs/tools/salesforce-data-cloud.md`
## Drive Drafts
- Script: scripts/drive_drafts.py | Account: openclawagenteve14@gmail.com | Root: "Eve — Drafts"
- **Command:** `cd ~/.openclaw/workspace && python3 scripts/drive_drafts.py --title "[Title]" --path "[path]" --file [path]`
- Key paths: client outreach/decks under `Consulting/Clients/[Client]/...`; job docs under `Job Applications/...`; content under `Content/...`; research/frameworks/analysis under same-name folders.
- Root lookup must use the top-level `Eve — Drafts` folder (`'root' in parents`); duplicate nested `Eve — Drafts` folders are archived drift, not valid upload roots.
- **Legacy `--project`/`--type`** still works for non-consulting projects (Vista, Nash Satoshi)

## Mission Control — Task Push
- Create: `curl -s -X POST http://localhost:3000/api/tasks -H 'Content-Type: application/json' -d '{"title":"[TITLE]","description":"[FIRST ACTION + WHY + DONE]","status":"todo","priority":"[high|medium|low]","assignee":"[eve|JT]","project":"[PROJECT]","sortOrder":[N]}'`
- Check duplicates first: `curl -s http://localhost:3000/api/tasks | python3 -c "import sys,json; [print(t['title']) for t in json.load(sys.stdin)]" | grep -i "[keyword]"`
- sortOrder bands: high 10-100+, medium 10/20/30..., speculative 500+.

- Client OS template: `skills/opticfy-ops/templates/client-os/` — copy into active client folders.
## Consulting Pipeline Drive Sync
- Script: `python3 ~/.openclaw/workspace/scripts/pipeline_drive_sync.py --slug [slug] --client "[Name]" --stage [deck|outreach|all]`
- Syncs deck + outreach draft to Google Drive: Eve — Drafts / Consulting / Clients / [Company Name] / Outreach|Decks/
- Run after deck-built and outreach-drafted stages. Include Drive links in JT's review message.
- List synced clients: `python3 scripts/pipeline_drive_sync.py --list`
- **Outreach send confirmation:** `python3 scripts/outreach_update.py --slug [slug] --company "[Name]" --message [M1|M2|M3] --channel [LinkedIn|Email] --date [YYYY-MM-DD]` — updates outreach-draft.md status, pipeline.md, closes "Review + Send" MC task, creates M2/M3 follow-up task. Triggered automatically when JT confirms a send (AGENTS.md rule).
- **Email pivot automation:** `python3 scripts/outreach_email_pivot.py [--draft|--execute] [--prospect slug] [--min-days N]` — scans outreach-draft.md files for M2-stuck prospects (M2 sent, M3 not sent, 7+ days), generates email pivot draft (different angle from LinkedIn), uploads to Drive, creates Email Pivot MC task. Daily cron at 6:45 AM (UUID: 9d9b165b).

## Notion
- Integration token: [REDACTED - use NOTION_TOKEN in ~/.config/env/global.env]
- DBs: Viral Post Swipe File `31316aff930580f6a195ca179793eb0e`; Content Calendar `32516aff930581a78659eac869c71ba8`
- Swipe push: `python3 ~/.openclaw/workspace/scripts/notion-swipe-push.py --text "..." --author "@handle" --url "..." --niche "AI Agents" --format "Hot Take" --why "..." --engagement 1200 --hook "Contrarian claim"`
- Swipe fetch/reference guard: `python3 scripts/notion-swipe-fetch.py --platform X --niche "AI Consulting" --limit 8 --since-days 30 --fetch-limit 200`; new weekly queues must pass `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-[MONDAY].md --require-reference-map linkedin --check-notion-script` or `--require-reference-map x`.
- Calendar push: `python3 ~/.openclaw/workspace/scripts/notion-calendar-push.py --platform "X" --date "YYYY-MM-DD" --post "post text" --type "Planned" --drive-link "URL"`; no `--title` arg.
- Cron: 3x/week Mon/Wed/Fri 5:30AM EST isolated sonnet — searches X for viral posts, pushes to Notion
- X Algorithm reference: ~/.openclaw/workspace/docs/x-algorithm.md

## Apps
- jtsomwaru.com: ~/projects/jtsomwaru-com/ → Vercel
- Glow Index: Replit | Admin key in approved secret store only | jsomwarux/skincare-rankings
  - ⚠️ **Replit deploy ≠ rebuild.** After pushing code changes to GitHub, JT must trigger a FRESH BUILD on Replit — not just redeploy. Options: (1) Shell tab → `npm run build` → then redeploy, OR (2) Deployments → Redeploy → "Rebuild from scratch." Clicking "Redeploy" without rebuilding reuses the old build and new code won't appear.
  - Required Replit Secrets: BRAVE_API_KEY, ADMIN_SECRET, N8N_WEBHOOK_URL, N8N_CALLBACK_SECRET.
  - Image backfill after fresh deploy: `curl -X POST https://skincare-rankings.replit.app/api/fetch-images -H "x-admin-key: $ADMIN_SECRET"`
  - **Crawler access diagnostic:** `cd ~/.openclaw/workspace && python3 scripts/glow_crawler_check.py` — checks `glowindex.co` `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, `/categories/serum` for Cloudflare challenge/200 status.
  - **⚠️ Engine OpenRouter key lives in LaunchAgent plist — not global.env.** `~/Library/LaunchAgents/com.openclaw.glow-index-engine.plist` has `OPENROUTER_API_KEY`. If analyses fail with all-401 errors: update the plist key, then `launchctl unload` + `load` to force launchd to pick up the change. Engine binds `127.0.0.1:8001`.
- Nash Satoshi: jsomwarux/Nash-Satoshi (private)
