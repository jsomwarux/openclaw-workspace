---
name: jt-consulting-pipeline
description: Orchestrates the full consulting client acquisition pipeline — research, analysis, n8n demo build, presentation deck, and outreach draft. Use when JT says "run the pipeline on", "research this prospect", "build a demo for", "run a full pipeline", "start the pipeline for", or names a new company to pursue as a consulting client. NOT for: existing active clients (Aya), portfolio updates, or job applications.
---

# jt-consulting-pipeline

Orchestrates the consulting client acquisition pipeline end-to-end.
Spawns each pipeline agent in sequence, handles the JT review gate,
and delivers the completed outreach draft for final send.

## 🚨 Pipeline Integrity Guard (Hard Rule)
**Never generate an outreach draft (`outreach-draft.md`) or upload outreach to Drive unless `research.md` has been completed.**
If JT says "skip research" or "fast track to outreach":
1. Refuse. 
2. Explain that bypassing research leads to targeting bankrupt companies and inactive CTOs.
3. Automatically run a lightweight web validation of the company and CTO *first* before generating even a single drafted line.

## Step 0: Preflight Check (Run This First)

Before spawning any pipeline agents, run the preflight script. It validates n8n is running, all agent directories exist, and checks the client artifact state.

```bash
bash ~/.openclaw/workspace/skills/jt-consulting-pipeline/scripts/preflight.sh [client-slug]
# Example: bash ~/.openclaw/workspace/skills/jt-consulting-pipeline/scripts/preflight.sh brothers-supply
```

If it exits non-zero: fix reported errors before proceeding. A failed preflight (especially n8n down) will cause agent spawns to fail silently mid-pipeline.

## Outreach Task Safety Gate — buyer channel + duplicate check

Before generating outreach, uploading outreach, or creating any M1/M2/M3 task:
1. Check `pipeline.md`, the client slug folder, and existing Drive client/T3 batch folders for the company name and obvious aliases.
2. Confirm every prospect that passes the outreach threshold has a named buyer and one reachable channel: verified email OR accepted LinkedIn connection. Both are useful but no longer mandatory under Outbound v2 adopted 2026-07-02.
3. If the only channel is an unaccepted LinkedIn profile, write `channel_status: connection_path_only` in `brief.json`, create/return a connection/request next step, and do **not** call the packet send-ready yet.
4. If a duplicate active client/prospect exists, update the existing record instead of creating a new client folder or duplicate outreach task.

## Tier Routing — Classify Before Starting

Classify prospects by strategic value, not just personalization quality. A warm intro or specific hook can raise a score, but never automatically makes a prospect T1.

Hard gates before scoring:
- Prospect fits JT's non-developer AI implementation positioning.
- Prospect maps to n8n workflow automation, Agentforce activation, AI Context OS, dashboarding, or ops implementation.
- Prospect is NYC/metro, referral-connected, or clearly remote-serviceable without enterprise-procurement drag.
- Agentforce prospects require confirmed Salesforce, Novidea, or Salesforce-native workflow evidence.
- Before send-ready status, prospect has buyer access plus one reachable channel: verified email OR accepted LinkedIn connection.

Outbound v2 binary gates:
1. Niche has a live proof asset.
2. Reachable channel exists: verified email OR accepted LinkedIn connection.
3. Named buyer exists.
4. Trigger bonus exists: ops job posting, portfolio growth, PM software in stack, rent-stabilized exposure, or similar.

Tier thresholds and actions:
- **T1 = all four gates.** Run proof-led outreach and JT review. No custom demo/build/deck before reply.
- **T2 = gates 1-3.** Run light research, niche template, one personalized line, JT review, and strict measurement.
- **Hold/dead = anything less.** Create the single missing-next-step task only when useful; otherwise archive.

Priority bias for June 2026: property management/real estate ops first, construction/skilled trades second, wholesale limited-test, Agentforce insurance/Data Cloud as strategic proof unless Salesforce stack and buyer trigger are confirmed.

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

**Drive structure created (T1/T2 — individual client folders):**
```
Eve — Drafts/
└── Consulting/
    └── Clients/
        └── [Client Name]/
            ├── Outreach/
            │   └── LinkedIn/  ← outreach-draft.md (Google Doc)
            └── Decks/         ← deck-url.txt (Google Doc with Slides link)
```

**Email drafts are NOT auto-synced by pipeline_drive_sync.py.** After writing `email-draft.md`:
```bash
python3 ~/.openclaw/workspace/scripts/drive_drafts.py \
  --title "[Client Name] — Email Draft" \
  --path "Consulting/Clients/[Client Name]/Outreach/Email" \
  --file ~/projects/jt-consulting-pipeline/clients/[slug]/email-draft.md
```

**T3 prospects (cold batch):** T3s do NOT get individual client folders. M1 is sent from the shortlist. After batch is drafted:
1. Compile all T3 DM drafts into one document
2. Upload to `Eve — Drafts/Consulting/Clients/T3 Batches/[Batch Name]/`
3. Create MC task per prospect with M2 follow-up
4. If T3 replies → promote to T2 → run `pipeline_drive_sync.py --slug [slug] --client "[Name]" --stage all`

**Existing client folders in Drive (verify before creating):**
AFGO Mechanical, BJD Property Management, Citadel Property Management, G-Net Construction, Maxwell Plumb Mechanical, Park Avenue Building & Roofing, RSI International, Wynne Plumbing & Heating. Benfield Electric Supply and Edmer Supply are T3 — T3 Batches folder only, no individual folder.

Include Drive links in the JT review message (Step 8).

### 8. Final JT Review + Send Confirmation
When outreach draft and Drive sync are complete:
1. Run `pipeline_drive_sync.py --stage all` (if not already done per step)
2. Read `~/projects/jt-consulting-pipeline/clients/[slug]/outreach-draft.md`
3. Send to JT via Telegram with the full draft + Drive links
4. Include this confirmation line in the Telegram message:
   ```
   ---
   After you send, reply with: "sent M1 via [LinkedIn/Email]" and I'll update the pipeline and close this task.
   ```
5. When JT confirms the send (same turn or later): run `outreach_update.py` to update outreach-draft.md, pipeline.md, close the MC task, and create the M2 follow-up task.

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
