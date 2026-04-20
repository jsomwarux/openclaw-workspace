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

- **API Key:** `fc-0d0961fa920a466a869fdd4068b9fe7e`
- **Endpoint:** `https://api.firecrawl.dev`
- **Scrape:** `POST /v1/scrape` with `{"url": "...", "formats": ["markdown"]}`
- **Auth header:** `Authorization: Bearer fc-0d0961fa920a466a869fdd4068b9fe7e`

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
- Key: fc-0d0961fa920a466a869fdd4068b9fe7e
- `POST https://api.firecrawl.dev/v1/scrape` `{"url":"...","formats":["markdown"]}`
- Auth header: `Authorization: Bearer fc-0d0961fa920a466a869fdd4068b9fe7e`
- Use for: single-page scrapes where Cloudflare /crawl is overkill
