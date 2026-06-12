# TOOLS.md - Local Notes

> ⚠️ **Check this file BEFORE saying "I can't do that." You probably can.**
> If something isn't here, research it — don't give up.

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Health Tracking System

**Location:** `~/.openclaw/workspace/health/`
**Database:** `~/.openclaw/workspace/health/health.sqlite`
**CLI:** `python3 health.py <flags>` (run from the health/ dir)

### Schedule
- **9:00 PM EST daily** — Eve sends check-in prompt to JT via Telegram (main session cron)
- **9:00 AM Sunday** — Eve generates and sends weekly report via Telegram (isolated cron)

### Check-in Format
JT replies naturally — parser handles comma-separated, labeled, or multi-line:
```
7, neck tight, chicken + salad, 30min walk, 8
# or
energy: 7
pain: shoulders
food: eggs + rice + coffee
exercise: none
sleep: 6
```

### CLI Commands
```bash
cd ~/.openclaw/workspace/health

# Log a check-in from JT's reply
python3 health.py --log "7, neck, chicken + rice, 30min walk, 8"

# Log for a specific date
python3 health.py --log "6, lower back, pasta, none, 7" --date 2026-02-20

# Generate weekly report (also runs on Sunday automatically)
python3 health.py --report

# View recent check-ins
python3 health.py --history        # last 7
python3 health.py --history 14     # last 14

# View a specific date
python3 health.py --show 2026-02-21

# Print the check-in prompt
python3 health.py --prompt
```

### Database Schema
```sql
checkins: id, date (YYYY-MM-DD, unique), timestamp, energy (1-10),
          pain_areas (text), food (text), exercise (text),
          sleep_quality (1-10), notes, raw_response
weekly_reports: id, week_start, generated, report_text
```

### Report Intelligence
Weekly report includes: energy + sleep trends (↑↓→), most frequent pain areas,
diet patterns (protein days, vegetable days, processed food days), exercise consistency.
Suggestion logic priority: **pain area → sleep → energy → diet → exercise**.
Suggestions are specific (e.g. exact stretch + duration) not generic.

### Focus Areas
- Muscle tension (neck, shoulders, traps, lower back, hips)
- Diet: protein intake, vegetable coverage, processed food reduction

---

## Audit Trail (Proofs)

**Location:** `~/.openclaw/workspace/proofs/YYYY-MM-DD/actions.jsonl`
**Logger:** `~/.openclaw/workspace/scripts/log-proof.py`
**Format:** One JSON object per line (JSONL) — safe for concurrent append, easy to parse

Every significant action Eve takes should be logged here. If something breaks, this is the first place to look.

### Entry Schema
```json
{
  "id": "abc12345",
  "timestamp": "2026-02-21T20:00:00+00:00",
  "action_type": "automation_setup",
  "title": "Short human-readable title",
  "description": "Full description of what was done",
  "outcome": "success | failure | partial",
  "error": null,
  "cost": { "tokens": 1200, "usd": 0.004 },
  "files_affected": ["/absolute/paths/to/files"],
  "metadata": {}
}
```

### Action Types
`file_creation` · `file_edit` · `file_deletion` · `cron_setup` · `cron_removal` · `script_execution` · `research` · `deployment` · `config_change` · `backup` · `cleanup` · `security` · `kb_add` · `kb_index` · `automation_setup` · `api_call` · `other`

### Commands
```bash
# List today's entries
python3 ~/.openclaw/workspace/scripts/log-proof.py --list

# List a specific date
python3 ~/.openclaw/workspace/scripts/log-proof.py --list --date 2026-02-21

# Log an entry
python3 ~/.openclaw/workspace/scripts/log-proof.py \
  --type file_creation \
  --title "Created foo.py" \
  --description "What it does and why" \
  --outcome success \
  --files ~/.openclaw/workspace/foo.py \
  [--cost-tokens 800] [--cost-usd 0.003] \
  [--meta '{"key": "value"}']

# View raw JSONL
cat ~/.openclaw/workspace/proofs/2026-02-21/actions.jsonl | python3 -m json.tool --no-ensure-ascii | head -60
```

### Browsing History
```bash
# All proof dates
ls ~/.openclaw/workspace/proofs/

# Count entries per day
for d in ~/.openclaw/workspace/proofs/*/; do
  count=$(wc -l < "$d/actions.jsonl" 2>/dev/null || echo 0)
  echo "$(basename $d): $count entries"
done
```

---

## Session Cleanup Automation

**Problem:** OpenClaw cron jobs with `sessionTarget: "isolated"` create orphan sessions that bloat `sessions.json` (77MB+ without cleanup → 1.3MB after).

**Schedule:** Daily at 3:00 AM local time (launchd, follows EST/EDT)
**Script:** `~/.openclaw/workspace/scripts/cleanup-sessions.py`
**LaunchAgent:** `~/Library/LaunchAgents/com.openclaw.cleanup-sessions.plist`
**Log:** `~/.openclaw/backups/cleanup-sessions.log`
**Sessions file:** `~/.openclaw/agents/main/sessions/sessions.json`

### Rules
- Always preserve `agent:main:main` (main session)
- Always preserve any session updated within the last 24 hours
- Remove all other sessions (cron orphan remnants)
- Writes atomically (temp → rename) to avoid corruption
- Appends summary to today's daily note in `memory/YYYY-MM-DD.md`

### Manage
```bash
# Run manually now
python3 ~/.openclaw/workspace/scripts/cleanup-sessions.py

# Check it's registered
launchctl list | grep openclaw.cleanup-sessions

# View log
tail -30 ~/.openclaw/backups/cleanup-sessions.log

# Disable
launchctl unload ~/Library/LaunchAgents/com.openclaw.cleanup-sessions.plist

# Re-enable
launchctl load ~/Library/LaunchAgents/com.openclaw.cleanup-sessions.plist
```

---

## Automated Backups

**Schedule:** Daily at 2:00 AM local time (launchd, follows EST/EDT automatically)
**Script:** `~/.openclaw/workspace/scripts/backup.sh`
**LaunchAgent:** `~/Library/LaunchAgents/com.openclaw.backup.plist`
**Backup root:** `~/.openclaw/backups/`
**Log:** `~/.openclaw/backups/backup.log`
**Retention:** Last 7 daily backups (older ones auto-deleted)

### What's backed up
- Root `.md` files: SOUL.md, SECURITY.md, USER.md, IDENTITY.md, TOOLS.md, MEMORY.md, AGENTS.md, HEARTBEAT.md, SKILLS.md
- `memory/` directory (all daily notes and heartbeat state)
- `knowledge/` directory (KB sqlite + source files, no node_modules)
- `plans/`, `proofs/`, `tasks/`, `interventions.jsonl`

### What's NOT backed up
- `browser-profile/` (too large, re-copy manually from a working session)
- `node_modules/` (any project — restore via `bun install`)
- Docker images

### Backup structure
```
~/.openclaw/backups/
  2026-02-21/      ← timestamped snapshot
    SOUL.md
    MEMORY.md
    memory/
    knowledge/
    ...
  2026-02-22/
  backup.log       ← cumulative log
```

### Manage the schedule
```bash
# Check status
launchctl list | grep openclaw.backup

# Force a backup now
~/.openclaw/workspace/scripts/backup.sh

# Disable
launchctl unload ~/Library/LaunchAgents/com.openclaw.backup.plist

# Re-enable
launchctl load ~/Library/LaunchAgents/com.openclaw.backup.plist

# View recent backup log
tail -50 ~/.openclaw/backups/backup.log
```

### Restore process
```bash
# List available backups
ls ~/.openclaw/backups/

# Restore a specific backup (e.g. 2026-02-21)
BACKUP=~/.openclaw/backups/2026-02-21
WORKSPACE=~/.openclaw/workspace

# Restore specific files
cp "$BACKUP/MEMORY.md" "$WORKSPACE/MEMORY.md"
cp "$BACKUP/SOUL.md" "$WORKSPACE/SOUL.md"

# Restore entire memory dir
rsync -a "$BACKUP/memory/" "$WORKSPACE/memory/"

# Restore knowledge dir (then run bun install in knowledge/)
rsync -a --exclude='node_modules/' "$BACKUP/knowledge/" "$WORKSPACE/knowledge/"
cd "$WORKSPACE/knowledge" && bun install
```

---

## Browser Profile

- **Location:** `~/.openclaw/browser-profile`
- **Logged into:** Google (Gmail, Calendar, Drive), GitHub
- **Refresh cadence:** Every ~10 days — re-login to expired sessions, re-copy profile
- **Rules:** See Browser Automation Rules in AGENTS.md — financial sites, form submissions, and new login credentials are off-limits

---

## X Research Skill

- **Installed:** `~/.openclaw/workspace/skills/x-research/`
- **Token:** Stored in `~/.config/env/global.env` as `X_BEARER_TOKEN` (masked here — see env file)
- **Usage:** `cd ~/.openclaw/workspace/skills/x-research && source ~/.config/env/global.env && bun run x-search.ts search "query" --quick`
- **Cost:** ~$0.50 per 100 tweets read from X API — use `--quick --limit 5` for cheap targeted lookups
- **Best for:** On-demand X/Twitter research for specific topics, not mass automated scanning
- **Not for:** Automated niche monitoring crons (too expensive) — use web_search (Brave) for those

---

## Firecrawl

- **API Key:** stored in approved env/auth store as `FIRECRAWL_API_KEY`
- **Endpoint:** `https://api.firecrawl.dev`
- **Scrape:** `POST /v1/scrape` with `{"url": "...", "formats": ["markdown"]}`
- **Auth header:** `Authorization: Bearer $FIRECRAWL_API_KEY`

### Pipeline: Brave → Firecrawl
1. Use `web_search` (Brave) to find relevant URLs
2. Use `web_fetch` or call Firecrawl `/v1/scrape` directly to get full page content as markdown
3. Firecrawl handles JS-heavy pages and bot circumvention that plain `web_fetch` can't

---

## OpenRouter

**Status:** ✅ Active — profile `openrouter:default` configured  
**Get key:** https://openrouter.ai/keys  
**Profile name:** `openrouter:default`  
**Markup:** ~0–10% over native API price depending on model

### Hybrid Routing Rule (MANDATORY)
| Use direct Anthropic → | Use OpenRouter → |
|---|---|
| Claude Opus 4.6 | OpenAI / Codex models |
| Claude Sonnet 4.6 | Grok / xAI models |
| Claude Haiku 4.5 | Gemini Flash / Pro |
| _(anything Anthropic)_ | Kimi K2.5 / Moonshot |
| | DeepSeek, Mistral, any new model |
| | Any model we don't have a direct key for |

**Why:** Anthropic direct = prompt caching (cache_read at $0.30/1M vs $3/1M input = 90% savings on cached content). OpenRouter models don't benefit from Anthropic's cache so the markup doesn't matter.

### Adding OpenRouter key (one-time setup)
Once JT provides the key, edit `~/.openclaw/agents/main/agent/auth-profiles.json`:
```json
"openrouter:default": {
    "type": "token",
    "provider": "openrouter",
    "token": "sk-or-v1-..."
}
```
Then add to `openclaw.json` auth.profiles:
```json
"openrouter:default": {
    "provider": "openrouter",
    "mode": "token"
}
```
No restart needed — auth-profiles.json is read dynamically.

### OpenRouter Model IDs (openrouter/ prefix required)
```
# OpenAI
openrouter/openai/gpt-4o
openrouter/openai/gpt-4o-mini
openrouter/openai/o3-mini

# xAI / Grok
openrouter/x-ai/grok-3
openrouter/x-ai/grok-3-mini

# Google Gemini
openrouter/google/gemini-2.5-flash-preview
openrouter/google/gemini-2.0-flash-001
openrouter/google/gemini-2.5-pro-preview

# Kimi / Moonshot
openrouter/moonshot/kimi-k2

# DeepSeek
openrouter/deepseek/deepseek-chat
openrouter/deepseek/deepseek-r1

# Mistral
openrouter/mistralai/mistral-large
openrouter/mistralai/mistral-small
```
Full model list: https://openrouter.ai/models

### Using OpenRouter in cron payloads
```json
{
  "kind": "agentTurn",
  "model": "openrouter/google/gemini-2.5-flash-preview",
  "message": "Your task here"
}
```

### Dynamic model adoption
When testing a new model or routing a task to OpenRouter, log it:
- Add entry to `memory/costs/model-experiments.jsonl`:
  `{"date": "YYYY-MM-DD", "model": "...", "task": "...", "cost": 0.00, "verdict": "..."}`
- If a model is used >20x/month, flag in Sunday brief: "Consider direct API key for X"

### Cost tracking
OpenRouter models are tracked by the cost-tracker. Since OpenRouter's pricing varies by model, the tracker uses the per-model rates from `openrouter.ai/models` (add to PRICING dict in cost-tracker.py as models are adopted). OpenRouter appears as provider `openrouter` in the daily cost breakdown.

---

## Knowledge Base

**Location:** `~/.openclaw/workspace/knowledge/`
**Database:** `~/.openclaw/workspace/knowledge/kb.sqlite`
**CLI:** `bun kb.ts <command>` (run from the knowledge/ dir)

### Categories
- `business` — JT Somwaru Consulting, clients, market research, competitors
- `tech` — AI tools, models, APIs, dev discoveries
- `crypto` — Market analysis, token research, trends
- `personal` — Health, goals, habits, reflections
- `projects` — Project notes, decisions, progress

### Common Commands
```bash
cd ~/.openclaw/workspace/knowledge

# Add item
bun kb.ts add --title "..." --content "..." --category tech --tags "ai,llm"

# Semantic search (hybrid by default)
bun kb.ts search "AI tools for document processing"
bun kb.ts search "bitcoin trend" --category crypto --mode semantic

# List / show / delete
bun kb.ts list --category business --limit 20
bun kb.ts show <id>
bun kb.ts delete <id>

# Auto-index daily notes / research
bun kb.ts index --dir ~/.openclaw/workspace/memory --source daily-notes
bun kb.ts index --dir ~/.openclaw/workspace/memory/research --source research --recursive

# Stats
bun kb.ts stats
```

### Embedding
- Model: `Xenova/all-MiniLM-L6-v2` — 384 dims, local inference, ~22MB download on first use
- Cache: `~/.cache/xenova/`
- Search modes: `hybrid` (default), `semantic`, `keyword`

### Schema Reference
- `knowledge_items`: id, title, content, summary, category, tags (JSON array), source, source_path, created_at, updated_at
- `embeddings`: item_id, embedding (Float32Array blob), model, dims, embedded_at
- `knowledge_fts`: FTS5 virtual table (auto-synced via triggers)
- `indexed_files`: path + mtime tracking to skip unchanged files

---

## JT Somwaru Consulting Agent Projects

All agents live at `~/projects/` and are Claude Code workspaces. Invoke them via the coding-agent skill.

### Consulting Client Pipeline (5-stage)

Shared data: `~/projects/jt-consulting-pipeline/clients/[slug]/`
Pipeline tracker: `~/projects/jt-consulting-pipeline/pipeline.md`
Orchestration skill: `~/.openclaw/workspace/skills/jt-consulting-pipeline/SKILL.md`

Flow: `Research → Analysis → [JT Review] → n8n Build → Presentation → Outreach → [JT Send]`

Each agent ends with a `PIPELINE_HANDOFF` block. Eve reads it and spawns next agent.
Read the skill BEFORE running any pipeline stage.

### Research Agent
- **Location:** `~/projects/research-agent/`
- **GitHub:** `git@github.com:jsomwarux/research-agent.git`
- **Purpose:** Finds and profiles prospects. Initial research, pain signals, receptiveness, platform fit. Outputs research.md only (not brief.json — that's Analysis Agent's job).
- **Niches:** Wholesale Distribution, Insurance Operations, Construction/Trades, Real Estate Operations, Logistics/Freight
- **Output:** `~/projects/jt-consulting-pipeline/clients/[slug]/research.md`
- **Lessons:** `tasks/lessons.md` | Niche files: `niches/`
- **Invoke:** `spawn coding-agent in ~/projects/research-agent — task: [research request]`
- **Discovery mode:** "Find me 5 prospects in [niche]" → shortlist → JT selects → full research → PIPELINE_HANDOFF

### Analysis Agent
- **Location:** `~/projects/analysis-agent/`
- **GitHub:** (not yet pushed — run: `gh repo create jsomwarux/analysis-agent --private --source=. --push`)
- **Purpose:** Deep process analysis. Maps target workflow step-by-step, inventories integrations, writes precise automation spec. Outputs full brief.json + brief.md for JT review.
- **Input:** PIPELINE_INPUT task prompt with research.md path
- **Output:** `analysis.md`, `brief.json`, `brief.md` → all in `~/projects/jt-consulting-pipeline/clients/[slug]/`
- **Brief schema:** `~/projects/research-agent/templates/brief-schema.json`
- **Invoke:** `spawn coding-agent in ~/projects/analysis-agent — task: [PIPELINE_INPUT block]`

### n8n Workflow Builder Agent
- **Location:** `~/projects/n8n-agent/`
- **GitHub:** `git@github.com:jsomwarux/n8n-agent.git`
- **Purpose:** Builds production-ready n8n workflows for any client/niche. Supports 4-LLM ensemble patterns.
- **Client structure:** `clients/[client-name]/` (brief.md, workflows/, tasks/todo.md, tests/)
- **Global lessons:** `tasks/lessons.md` — read before every session
- **Active workflows:** `workflows/webhook-uppercase.json` (legacy test, deployed + verified)
- **Custom commands:** /build-workflow, /validate, /test, /new-client, /switch-client
- **MCP needs:** `n8n-mcp` server + `context7` server
- **Runtime deps:** n8n installed ✅. Set `N8N_API_URL` + `N8N_API_KEY` env vars before deploy. Connect LLM credentials in n8n UI (Claude, OpenAI, Gemini, Grok) for ensemble workflows.
- **Invoke:** `spawn coding-agent in ~/projects/n8n-agent — task: [workflow request]`

### Agentforce Development Agent
- **Location:** `~/projects/agentforce-agent/`
- **GitHub:** `git@github.com:jsomwarux/agentforce-agent.git`
- **Purpose:** Builds, deploys, and tests Salesforce Agentforce agents for clients. Expert in GenAiPlanner, topics, actions, Apex.
- **Client structure:** `client-projects/[client-name]/`
- **SFDX project:** `agentforce-project/` (force-app metadata, specs, scripts)
- **Existing agents built:** Employee Assistant (InternalCopilot, 3 topics, 7 actions), Ecommerce Service Agent (ExternalCopilot)
- **Lessons:** `lessons.md` at root — CRITICAL, read first every session
- **Skills:** agentforce-builder, agentforce-testing, apex-actions, salesforce-flows
- **Sub-agent:** agentforce-specialist
- **MCP needs:** `@salesforce/mcp` (Salesforce DX) + `@tsmztech/mcp-server-salesforce` (via npx — already available)
- **Runtime deps:** `sf` (Salesforce CLI) — ⚠️ NOT installed on this Mac mini yet
  - Install: `npm install -g @salesforce/cli`
  - After install, authenticate org: `sf org login web --alias [org-alias]`
- **Manual intervention:** Many steps CANNOT be automated — full guide at `docs/manual-intervention-guide.md`
- **Confirmed working workflow:** Deploy Apex/Flows → clean old metadata → create agent + topics + actions via Agent Builder UI → activate → test
- **Invoke:** `spawn coding-agent in ~/projects/agentforce-agent — task: [client/task description]`

### Git Config (one-time fix)
```bash
git config --global user.name "JT Somwaru"
git config --global user.email "your@email.com"
```

---

## Future Integrations to Watch

### Claude Code Security (Anthropic)
- **What it is:** An Anthropic enterprise product that performs automated security analysis of codebases via Claude Code
- **Current status:** Enterprise-only — not yet available to individual users or through the Claude Code CLI
- **Action:** When it becomes available to individual users or via CLI integration, integrate it into the deployment pipeline as a pre-deploy step alongside the manual Security Self-Review in AGENTS.md
- **Monitor:** Watch https://www.anthropic.com/news and Claude Code release notes for availability

---

## Claude Code Remote Control

**Feature:** Remote Control — lets JT monitor and interact with an active Claude Code session from his phone.
**Available on:** Max plan
**How to activate:** Inside an active Claude Code session, run `/remote-control` or `claude rc`
**Result:** Generates a URL JT can open on his phone to watch and interact with the build live

### Eve's Rule
**When spawning a significant Claude Code build** (new project, major feature, multi-file refactor), remind JT:
> "You can monitor this build from your phone — just run `/remote-control` or `claude rc` inside the session to get a link."

Don't mention it for trivial edits, but do surface it for anything that will run for more than a few minutes.

---

Add whatever helps you do your job. This is your cheat sheet.


## Salesforce Data Cloud (paired with Agentforce)
- **What it is**: Salesforce's real-time CDP — unifies customer data from any source into a single profile used as live agent context
- **Agentforce integration**: Data Cloud feeds live customer data into Agentforce agents via Grounding — agents personalize responses based on purchase history, segment membership, recent interactions
- **Key concepts**: Unified Profile, Data Streams (connectors), Segments, Data Spaces (multi-org isolation), Data Cloud for Agentforce (the bridge layer)
- **Licensing**: Consumption-based (Flex Credits $500/100k or Profiles $240-$420/1k profiles/year) — separate SKU, not bundled with standard Agentforce. Often part of "Einstein 1" packages.
- **Interview signal**: Understanding that Data Cloud is HOW Agentforce gets real-time personalization separates architecture-level candidates from surface-level ones
- **Trailhead**: trailhead.salesforce.com/content/learn/modules/salesforce-data-cloud-quick-look
- **Deep research**: memory/analysis/salesforce-data-cloud-2026-03-19.md

---

## Page CRO Reference (moved from TOOLS.md — 2026-04-20)
- Full CRO framework at: https://github.com/coreyhaines31/marketingskills/tree/main/skills/page-cro
- Use when: optimizing jtsomwaru.com conversions, or auditing a client's landing page
- Framework covers: value prop clarity, headline effectiveness, CTA friction, social proof placement, mobile experience
- Not installed as a skill (low frequency) — fetch the SKILL.md directly when needed

## Deepgram Nova-2 (moved from TOOLS.md — 2026-04-20)
- Speech-to-text API | $0.002/min | Multi-speaker detection, fast turnaround
- Use case: Phase 2 UGC pipeline (script timing verification), any future transcription at scale
- Current alternative: Groq whisper-large-v3 (free, already configured) — prefer Groq for single-speaker tasks
- Docs: https://developers.deepgram.com | Sign up + add API key to global.env when needed

## Firecrawl (moved from TOOLS.md — 2026-04-20)
- `POST https://api.firecrawl.dev/v1/scrape` `{"url":"...","formats":["markdown"]}`
- Auth header: `Authorization: Bearer $FIRECRAWL_API_KEY`
- Use for: single-page scrapes where Cloudflare /crawl is overkill

---

## GBrain Consulting Recall Pilot
- Sandbox install: `~/projects/gbrain` (GBrain 0.32.0)
- Pilot home: `~/projects/gbrain-pilot-home`
- Sanitized curated source: `~/projects/gbrain-pilot-source`
- Wrapper: `scripts/gbrain-consulting-search.sh "Entity or company name"`
- Use only for consulting/prospect entity lookup. Eval: entity search 20/20 vs qmd 13/20; natural-language search weak without embeddings.
- Do NOT add crons, install skillpacks, ingest broad workspace/private chats/config, or wire embeddings/auth without JT approval.

## JT Operating-System Routing
- Capability map: `docs/agents/capability-routing-map.md`
- New skills: `skills/client-proof-capture/SKILL.md`, `skills/linkedin-corpus/SKILL.md`, `skills/ai-context-os/SKILL.md`
- New agents: `agents/client-proof-engine/AGENT.md`, `agents/linkedin-corpus/AGENT.md`
- Portable Codex plugin scaffold: `~/plugins/jt-operating-system`; marketplace: `~/.agents/plugins/marketplace.json`

## Glow Index Ops
- Glow Index: Replit | Admin key in approved secret store only | jsomwarux/skincare-rankings.
- Replit deploy is not a rebuild. After pushing code changes to GitHub, JT must trigger a fresh build on Replit: Shell tab → `npm run build` → redeploy, or Deployments → Redeploy → "Rebuild from scratch." Plain redeploy can reuse the old build.
- Required Replit Secrets: BRAVE_API_KEY, ADMIN_SECRET, N8N_WEBHOOK_URL, N8N_CALLBACK_SECRET.
- Image backfill after fresh deploy: `curl -X POST https://skincare-rankings.replit.app/api/fetch-images -H "x-admin-key: $ADMIN_SECRET"`.
- Crawler access diagnostic: `cd ~/.openclaw/workspace && python3 scripts/glow_crawler_check.py` checks `glowindex.co` `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, `/categories/serum` for Cloudflare challenge/200 status.
- Engine OpenRouter key lives in `~/Library/LaunchAgents/com.openclaw.glow-index-engine.plist`, not `global.env`. If analyses fail with all-401 errors, update the plist key, then `launchctl unload` + `load` to force launchd to pick up the change. Engine binds `127.0.0.1:8001`.

## Tool Command Syntax Relocated From TOOLS.md - 2026-06-11 Phase 6

> Relocated from `TOOLS.md` during Phase 6 bootstrap reduction. No content was deleted; compact bootstrap file now points here.

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
- Wrapper: `scripts/gbrain-consulting-search.sh "Entity or company name"`
- Use only for consulting/prospect entity lookup; no crons/skillpacks/broad ingestion/embeddings/auth without JT approval. Full pilot paths/details: `docs/tools/TOOLS-full.md`.

## JT Operating-System Routing
- Capability map: `docs/agents/capability-routing-map.md`
- Synthesis/audit: `docs/agents/jt-toolkit-synthesis-2026-06-02.md`.
- Portable Codex plugin: `~/plugins/jt-operating-system` (skills: `ai-context-os`, `client-proof-capture`, `plan-review-pack`, `linkedin-corpus`, `n8n-blueprint`, `proposal-pdf`, `product-build-loop`).
- Workspace agents added from toolkit synthesis: `agents/workflow-strategist/AGENT.md`, `agents/product-quality-pass/AGENT.md`.
- Skills/agents/plugin scaffold details live in `docs/tools/TOOLS-full.md`.

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
- Crypto deterministic full-analysis writer: `python3 /Users/jtsomwaru/projects/crypto-agent/scripts/generate-full-analysis.py` — writes dated `latest-analysis.md`, history archive, `telegram-summary.txt`, and allocation-history JSON from fresh portfolio/prices/X/whale inputs before validator delivery.
- Crypto full-analysis pipeline: `python3 /Users/jtsomwaru/projects/crypto-agent/scripts/run-full-analysis-pipeline.py --max-x-age-hours 3 --since 1d --limit 5` — canonical 6AM/recovery path; refreshes inputs/X, runs guards, writes artifacts, validates, and returns `CRYPTO_FULL_ANALYSIS_OK` only when safe to send.
- Pipeline: ~/projects/jt-consulting-pipeline/ | Skill: skills/jt-consulting-pipeline/SKILL.md
- Outreach pipeline preflight: `python3 scripts/outreach_pipeline_runner.py --json` — deterministic script-first stages for Drive auth, M-status/T3 dedupe, existing draft/doc checks, warm-up holds, and report generation before any LLM copy work.

## Salesforce Data Cloud (paired with Agentforce)
Real-time CDP → Agentforce via Grounding. Also called "Data 360." Flow: Data Streams → DLOs → DMOs → Unified Profiles → Data Graphs. Two paths: (1) Data Libraries (simple) or (2) Manual RAG pipeline. SF-to-SF ingestion free; 2.5M credits bundled in Agentforce Editions. **Full ref:** `docs/tools/salesforce-data-cloud.md`
## Drive Drafts
- Script: scripts/drive_drafts.py | Account: openclawagenteve14@gmail.com | Root: "Eve — Drafts"
- **Command:** `cd ~/.openclaw/workspace && python3 scripts/drive_drafts.py --title "[Title]" --path "[path]" --file [path]`
- Reusing the same title/path now updates the existing Google Doc body. For corrected high-stakes drafts, verify the live Google Doc text after sync, not just the local markdown.
- Regression: `python3 -m unittest scripts/test_drive_drafts.py`
- AI Ops teardown bundles: `python3 scripts/ai_ops_teardown_drive_sync.py --json` uploads current teardown + content draft to `Consulting/AI Ops Teardowns/[date]/Teardowns` and `Content/AI Ops Teardowns/[date]/Drafts`.
- Key paths: client outreach/decks under `Consulting/Clients/[Client]/...`; job docs under `Job Applications/...`; content under `Content/...`; research/frameworks/analysis under same-name folders.
- Root lookup must use the top-level `Eve — Drafts` folder (`'root' in parents`); duplicate nested `Eve — Drafts` folders are archived drift, not valid upload roots.
- **Legacy `--project`/`--type`** still works for non-consulting projects (Vista, Nash Satoshi)

## Mission Control — Task Push
- Create: `curl -s -X POST http://localhost:3000/api/tasks -H 'Content-Type: application/json' -d '{"title":"[TITLE]","description":"[FIRST ACTION + WHY + DONE]","status":"todo","priority":"[high|medium|low]","assignee":"[jt|eve|both]","project":"[PROJECT]","sortOrder":[N]}'`
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
- Glow Index: Replit | jsomwarux/skincare-rankings | fresh build required before redeploy; full ops commands in `docs/tools/TOOLS-full.md`.
- Nash Satoshi: jsomwarux/Nash-Satoshi (private)
