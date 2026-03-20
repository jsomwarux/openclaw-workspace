---
name: jt-consulting-pipeline
description: Orchestrates the full consulting client acquisition pipeline — research, analysis, n8n demo build, presentation deck, and outreach draft. Use when JT says "run the pipeline on", "research this prospect", "build a demo for", "run a full pipeline", "start the pipeline for", or names a new company to pursue as a consulting client. NOT for: existing active clients (Aya), portfolio updates, or job applications.
---

# jt-consulting-pipeline

Orchestrates the consulting client acquisition pipeline end-to-end.
Spawns each pipeline agent in sequence, handles the JT review gate,
and delivers the completed outreach draft for final send.

## Step 0: Preflight Check (Run This First)

Before spawning any pipeline agents, run the preflight script. It validates n8n is running, all agent directories exist, and checks the client artifact state.

```bash
bash ~/.openclaw/workspace/skills/opticfy-pipeline/scripts/preflight.sh [client-slug]
# Example: bash ~/.openclaw/workspace/skills/opticfy-pipeline/scripts/preflight.sh brothers-supply
```

If it exits non-zero: fix reported errors before proceeding. A failed preflight (especially n8n down) will cause agent spawns to fail silently mid-pipeline.

## Tier Routing — Classify Before Starting

Before spawning any agents, assign a tier. This determines the pipeline path.

| Signal | Tier |
|--------|------|
| Referral / warm intro | T1 |
| Research surfaces a highly specific, verifiable hook (e.g. a named article, a quote, a job posting) | T1 |
| Qualified niche fit, no exceptional hook | T2 |
| Cold list prospect with minimal research | T3 |

**T1 path:** Research → Analysis → [JT Review] → n8n Custom Build → Presentation → Outreach → [JT sends]
**T2 path:** Research (light brief) → Template Config → Deck (from template) → Outreach → [optional JT review] → [overnight can send]
**T3 path:** Quick surface research → Outreach Agent (cold hook batch) → [no review needed] → Reply → promotes to T2

Write `tier: 1 | 2 | 3` and `jt_review_required: true` into the client's `brief.json` before handoff to the next agent. `jt_review_required` defaults to true for ALL tiers — never send without JT approval unless he explicitly sets it to false for a given tier.

## Pipeline Stages (T1 Full)

```
Research Agent → Analysis Agent → [JT Review] → n8n Agent → Presentation Agent → Outreach Agent → [JT Send]
```

All shared client data lives at: `~/projects/jt-consulting-pipeline/clients/[slug]/`
Pipeline tracker: `~/projects/jt-consulting-pipeline/pipeline.md`

## Agent Paths

| Agent | CLAUDE.md | Model | Invoke |
|-------|-----------|-------|--------|
| Research Agent | `~/projects/research-agent/CLAUDE.md` | `anthropic/claude-sonnet-4-6` | `spawn coding-agent in ~/projects/research-agent` |
| Analysis Agent | `~/projects/analysis-agent/CLAUDE.md` | `anthropic/claude-sonnet-4-6` | `spawn coding-agent in ~/projects/analysis-agent` |
| n8n Agent | `~/projects/n8n-agent/CLAUDE.md` | Codex CLI (gpt-5.2-codex) | `spawn coding-agent in ~/projects/n8n-agent` |
| Presentation Agent | `~/projects/presentation-agent/CLAUDE.md` | `groq/llama-3.3-70b-versatile` | `spawn coding-agent in ~/projects/presentation-agent` |
| Outreach Agent | `~/projects/outreach-agent/CLAUDE.md` | `groq/llama-3.3-70b-versatile` | `spawn coding-agent in ~/projects/outreach-agent` |

**Model rule:** Always pass `model` explicitly when spawning via sessions_spawn. Never rely on default — default may be Opus after a gateway event.

## Quick Start — Full Pipeline Run

### 1. Research Stage
Spawn the research agent with a discovery or named-company request:
```
spawn coding-agent in ~/projects/research-agent
task: "Find me 5 prospects in [niche]" OR "Research [Company Name] in [niche]"
```

Wait for `PIPELINE_HANDOFF: research-complete` in the result.

### 2. Analysis Stage
For each company with research complete, spawn analysis agent:
```
spawn coding-agent in ~/projects/analysis-agent
task: |
  PIPELINE_INPUT
  slug: [slug]
  company: [Company Name]
  niche: [niche]
  platform: [n8n | agentforce | both]
  research_path: ~/projects/jt-consulting-pipeline/clients/[slug]/research.md
```

**Always spawn with `thinking: medium`** — this is the most consequential step in the pipeline.

Wait for `PIPELINE_HANDOFF: analysis-complete`.

### 3. JT Review Gate
When analysis is complete:
1. Read `~/projects/jt-consulting-pipeline/clients/[slug]/brief.md`
2. Read `~/projects/jt-consulting-pipeline/clients/[slug]/brief.json` → generate **Execution Plan**:
   - What the n8n agent will build (trigger, main steps, output)
   - Which agents run next and in what order
   - Estimated build complexity (Low / Medium / High)
   - Any open questions the build agent will need answered
3. Send to JT via Telegram: brief.md contents + Execution Plan summary (keep plan to 5–8 lines)
4. Wait for JT's response
5. If approved: proceed to Step 4
6. If redirect: note feedback, re-spawn analysis agent with notes

### 4. n8n Build Stage
After JT approval, spawn n8n agent:
```
spawn coding-agent in ~/projects/n8n-agent
task: |
  PIPELINE_INPUT
  slug: [slug]
  company: [Company Name]
  brief_json: ~/projects/jt-consulting-pipeline/clients/[slug]/brief.json
```

Wait for `PIPELINE_HANDOFF: workflow-built`.

### 5. Presentation Stage
After workflow built, spawn presentation agent:
```
spawn coding-agent in ~/projects/presentation-agent
task: |
  PIPELINE_INPUT
  slug: [slug]
  company: [Company Name]
  brief_json: ~/projects/jt-consulting-pipeline/clients/[slug]/brief.json
  workflow_docs: ~/projects/jt-consulting-pipeline/clients/[slug]/workflow-docs.md
```

Wait for `PIPELINE_HANDOFF: deck-built`.

### 6. Outreach Stage
After deck built, spawn outreach agent:
```
spawn coding-agent in ~/projects/outreach-agent
task: |
  PIPELINE_INPUT
  slug: [slug]
  company: [Company Name]
  brief_json: ~/projects/jt-consulting-pipeline/clients/[slug]/brief.json
  deck_instructions: ~/projects/jt-consulting-pipeline/clients/[slug]/deck-instructions.md
```

Wait for `PIPELINE_HANDOFF: outreach-drafted`.

### 7. Google Drive Sync (MANDATORY — runs after every pipeline stage that produces an artifact)

After **deck-built** (Step 5):
```bash
cd ~/.openclaw/workspace && python3 scripts/pipeline_drive_sync.py \
  --slug [slug] --client "[Company Name]" --stage deck
```

After **outreach-drafted** (Step 6):
```bash
cd ~/.openclaw/workspace && python3 scripts/pipeline_drive_sync.py \
  --slug [slug] --client "[Company Name]" --stage outreach
```

Or sync both at once:
```bash
cd ~/.openclaw/workspace && python3 scripts/pipeline_drive_sync.py \
  --slug [slug] --client "[Company Name]" --stage all
```

**Drive structure created:**
```
Eve — Drafts/
└── JT Somwaru — Client Pipeline/
    └── [Company Name]/
        ├── [Company Name] — Outreach Draft     ← Google Doc
        └── [Company Name] — Presentation Deck  ← Google Doc (with Slides link)
```

Include Drive links in the JT review message (Step 8).

### 8. Final JT Review
When outreach draft and Drive sync are complete:
1. Run `pipeline_drive_sync.py --stage all` (if not already done per step)
2. Read `~/projects/jt-consulting-pipeline/clients/[slug]/outreach-draft.md`
3. Send to JT via Telegram with the full draft + Drive links
4. JT reviews, edits, and sends the email themselves
5. Update pipeline.md status to "✉️ Pitched"

## PIPELINE_HANDOFF Detection

Each agent ends its output with a `PIPELINE_HANDOFF` block. When a coding-agent
session completes, parse the result for this block. Extract stage + slug + next_agent
and proceed accordingly.

**After every PIPELINE_HANDOFF, immediately push stage to Mission Control:**
```bash
curl -s -X POST http://localhost:3000/api/pipeline \
  -H "Content-Type: application/json" \
  -d "{\"slug\": \"[slug]\", \"stage\": \"[stage]\", \"company\": \"[Company Name]\"}"
```

Example blocks to match:
- `stage: research-complete` → push to Convex → spawn analysis-agent (thinking: medium)
- `stage: analysis-complete` → push to Convex → generate execution plan → trigger JT review gate
- `stage: workflow-built`    → push to Convex → spawn presentation-agent
- `stage: deck-built`        → push to Convex → spawn outreach-agent
- `stage: outreach-drafted`  → push to Convex → deliver to JT for send

## JT Review Gate — Telegram Message Format

When sending brief.md for JT review, format as:

```
🧠 Brief ready: [Company Name]

[Brief.md contents — full text]

---
Reply APPROVE to start the n8n build, or tell me what to redirect.
```

When sending outreach draft for JT review:

```
📤 Outreach ready: [Company Name]

[outreach-draft.md contents — full text, including all follow-ups and send cadence]

---
Day 0 email is ready to send. Follow-ups 1–3 are pre-written for the thread.
Edit anything, then let me know when Day 0 is sent so I can update the pipeline.
```

## Delivery Framework (mandatory — every engagement)
See full spec: `~/projects/jt-consulting-pipeline/DELIVERY-FRAMEWORK.md`

1. **Workflow decomposition** — split every automated step into Mechanical vs Judgment Call → `clients/[slug]/workflow-decomposition.md`
2. **Client KB** — persistent context that compounds across projects → `clients/[slug]/kb/`
3. **Skill templating** — after delivery, evaluate if workflow is 80%+ reusable → template to `~/.openclaw/workspace/skills/`
4. **Adjacent workflow map** — after first delivery, proactively map 3–5 next workflows → `clients/[slug]/adjacent-workflows.md`
5. **Workflow collapse log** — log before/after story (anonymized) → `~/projects/jt-consulting-pipeline/workflow-collapse-log.md`

## File Checklist Per Slug

After full pipeline run, `clients/[slug]/` should contain:
- [ ] research.md
- [ ] analysis.md
- [ ] brief.json
- [ ] brief.md
- [ ] workflow-decomposition.md ← **Delivery Framework Step 1**
- [ ] workflow.json
- [ ] workflow-docs.md
- [ ] flow-diagram.md
- [ ] mock_data/ (directory)
- [ ] demo-results.json
- [ ] build-deck.js
- [ ] deck-instructions.md
- [ ] deck-url.txt
- [ ] outreach-draft.md (includes: initial email + 3 follow-ups + send cadence + specificity check)
- [ ] production-deploy.md (n8n agent: post-approval deploy instructions)
- [ ] kb/ (directory — start at delivery, grow over time) ← **Delivery Framework Step 2**
- [ ] adjacent-workflows.md (produce within 1 week of first delivery) ← **Delivery Framework Step 4**
