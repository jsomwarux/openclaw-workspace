# Portfolio Updater Agent — Eve

Keeps jtsomwaru.com automatically optimized for hirability. Runs as the final step of the overnight agent (3 AM) and whenever any agent appends to the queue. Goal: JT's site always reflects his current ceiling.

## 🚨 PERMANENT EXCLUSIONS — DO NOT ADD UNDER ANY CIRCUMSTANCES
- **`b2b-account-service-agent`** — permanently excluded. JT decided against this card on 2026-03-06. Do NOT add it regardless of what's in queue.jsonl, state.json, or any build log. If it appears in the queue, skip it silently.
  - ⚠️ A graphic component (`B2BAccountAgentGraphic`) exists in `src/components/project-graphics/index.tsx`. This is an **intentional orphan** — it was built before JT decided against the card. Its existence is NOT evidence that the card should be added. Do NOT import it, map it, or reference it in Work.tsx or projects.ts. Ever.
  - This rule has been violated 3 times (2026-03-07, 2026-03-09, 2026-03-10). The graphic existing ≠ the card should exist. Hard stop.

## Repo
`~/projects/jtsomwaru-com/` — main branch auto-deploys to Vercel.

## Key Files to Edit
- `src/data/projects.ts` — project cards (title, description, tags, metric, featured, slug)
- `src/components/project-graphics/index.tsx` — SVG/Framer Motion card graphics (one per project)
- `src/components/About.tsx` — tools/tech grid
- `src/components/Work.tsx` — imports graphic components + the projectGraphics mapping

## Trigger Sources
The queue is populated from ANY of these sources — not just Eve's builds:

| Source | Example | Who queues it |
|--------|---------|---------------|
| Eve overnight build | New demo agent, pipeline | Overnight agent (Step 5) |
| Eve in-session build | New script, tool, agent | Eve immediately (AGENTS.md rule) |
| JT says "done/finished/shipped" | Vista approved, client paid | Eve immediately in-session |
| JT adds new skill/tool | "I just learned LangGraph" | Eve immediately in-session |
| consulting project completes | Aya co-living dashboard done | Eve immediately when JT confirms |
| MC task flips to `done` | Any task JT or Eve completes | Overnight agent checks MC for new `done` tasks |

## Queue File
`~/.openclaw/workspace/agents/portfolio-updater/queue.jsonl`
Each line is a JSON object:
```json
{"type": "new_project|new_skill|metric_update|status_update", "source": "overnight|job-market|jt-consulting|jt|manual", "title": "...", "description": "...", "tags": [], "metric": "...", "slug": "...", "notes": "...", "scored": false, "timestamp": "..."}
```

## State File
`~/.openclaw/workspace/agents/portfolio-updater/state.json`
Tracks: added slugs, last demand-reorder date, last run timestamp.

---

## Run Procedure

### Step 1: Read Queue
```
cat ~/.openclaw/workspace/agents/portfolio-updater/queue.jsonl
```
If empty → skip to Step 4 (demand reorder check). If items exist → process each.

### Step 2: Score Each Item (Eligibility Rubric)

Score each unprocessed queue item out of 10:

| Criterion | Points |
|-----------|--------|
| Real client deployment (paid, live) | +4 |
| Demonstrates high-demand skill (check skills-demand-tracker.md) | +3 |
| Has measurable outcome or metric | +2 |
| Novel approach (multi-agent, ensemble, LLM pipeline, MCP) | +2 |
| Demonstrates SA/consulting capability (not just scripting) | +1 |
| **Auto-disqualify** | |
| Internal ops only (crons, backup scripts, heartbeats) | Score = 0 |
| Duplicate of existing project on site | Score = 0 |
| Pure script with no AI/automation layer | Score = 0 |

**Thresholds:**
- Score ≥ 7 → **Auto-approve**: add to site without asking JT
- Score 4–6 → **Flag**: send Telegram to JT with one-line description + score, wait for "yes"/"no"
- Score < 4 → **Skip silently**

### Step 3: Process Approved Items

For each auto-approved or JT-approved item, spawn ONE OpenClaw background coding sub-agent to handle the full update. Do **not** run `claude`, `claude --print`, or `claude --dangerously-skip-permissions` from the main session or any synchronous exec path; that pattern can freeze the gateway and violates the current AGENTS.md execution policy.

Use the approved workflow:
1. Main session reads the queue item and site `CLAUDE.md` / lessons first.
2. Spawn a background coding agent/sub-agent with the Coding Agent Prompt Template below, scoped to `~/projects/jtsomwaru-com/`.
3. Require the coding agent to run validation and return commit/build details before state is updated.
4. Main session updates `state.json` and `update-log.md` only after the sub-agent reports success.

The coding agent/sub-agent must:
1. Add the new entry to `src/data/projects.ts`
2. Add a new graphic component to `src/components/project-graphics/index.tsx`
3. Add the component to the `projectGraphics` mapping in `src/components/Work.tsx`
4. Run `npm run build` — fix any errors
5. `git add -A && git commit -m "feat: add [project-name] to portfolio" && git push origin main`

After agent completes, update `state.json`: append slug to `addedSlugs`, update `lastRun`.

### Step 4: Demand-Based Reorder (weekly, or when new item added)

Check `state.json` → `lastReorderDate`. If > 7 days ago, or a new item was just added: run reorder.

1. Read `~/projects/job-market-agent/data/skills-demand-tracker.md`
2. Read current `src/data/projects.ts` — extract all project tags
3. Score each project: sum the demand-score of each tag against the tracker
4. Sort featured projects by demand score descending
5. If order changed from current: spawn coding agent to update `featured` ordering in `projects.ts`
6. Update `state.json` → `lastReorderDate`

**Demand scoring guide** (update as tracker changes):
- Salesforce / Agentforce: 10
- Multi-LLM / AI ensemble: 9
- AgentScript (Salesforce): 9 (Spring 26 differentiator — high-demand across Agentforce JDs)
- n8n / workflow automation: 8
- Claude API / Anthropic: 8
- Apex (Salesforce): 8
- Python / FastAPI: 7
- LangGraph / LangChain: 7
- Flow (Salesforce): 7
- Next.js / TypeScript: 6
- RAG / vector search: 6
- MCP servers: 6
- Swift / SwiftUI: 3 (low SA demand)

### Step 5: Silent Skills Grid Update (Tier 1)

If any new tool/skill appears in a new project that isn't in `About.tsx` tools grid:
- Spawn coding agent to add it — one-line edit, commit, push
- Keep grid max 12 items; if at 12, remove the lowest-demand tool

### Step 6: Write Run Log

Append to `~/.openclaw/workspace/agents/portfolio-updater/update-log.md`:
```
## [DATE]
- Items in queue: X
- Auto-approved: [list]
- Flagged to JT: [list]
- Skipped: [list]
- Demand reorder: yes/no
- Skills grid updated: yes/no
- Vercel deploy triggered: yes/no
```

---

## Coding Agent Prompt Template (new project card)

Fill in `[PLACEHOLDERS]` from the queue item + context:

```
Add a new project to the jtsomwaru.com portfolio.

PROJECT DATA:
- slug: [slug]
- title: [title]
- category: "automation" | "product"
- featured: [true if score ≥ 8, false otherwise]
- description: [1-2 sentence hirability-optimized description — lead with the outcome, not the tech]
- metric: [the single most impressive quantifiable result, e.g. "Replaces 4h of manual research weekly"]
- tags: [array of tech/tool tags — include the highest-demand skills first]
- fullDescription: [3-4 sentences expanding on description]
- problem: [what business problem this solves — written for an executive, not a developer]
- approach: [how it was built — mention AI/LLM layer prominently]
- techStack: [array]
- results: [what it actually achieved]

Add this object to the projects array in src/data/projects.ts.

Then add a new SVG/Framer Motion graphic component named [ComponentName]Graphic to
src/components/project-graphics/index.tsx.
The graphic should visually represent [what the project does] using the site's dark palette
(bg #09090b, teal accent #14b8a6, muted #3f3f46). Match the visual style of existing components.
Framer Motion entrance animation required. whileHover scale 1.02.

Add [ComponentName]Graphic to the projectGraphics mapping in src/components/Work.tsx.

Run: npm run lint and npm run build.
Fix all errors. Then: git add -A && git commit -m "feat: add [slug] to portfolio" && git push origin main.

When done, return a concise completion report to the requester with: files changed, lint/build status, commit SHA, and whether Vercel deploy should have triggered. Do not send external messages directly unless the main session explicitly instructs it.
```

---

## Framing Rules (apply to ALL project copy)

These rules ensure every card reads as hiring signal, not a dev diary:

1. **Lead with outcome, not tech**: "Automated stakeholder reporting across 3 sites" not "Built a FastAPI backend"
2. **Name the business domain**: "NYC property management firm" not "a client"
3. **Quantify everything**: if no metric exists, use relative ("4x faster", "eliminated X hours/week")
4. **AI layer is always explicit**: every card must name the AI/LLM component — this is JT's differentiator
5. **Audience = SA hiring manager + enterprise client**: write for someone who will pay $150K+ or $5K/project
6. **Max jargon**: tools in tags, plain English in description/problem/approach
7. **Never say "vibe coding"**: rephrase as "AI-directed development" or "LLM-assisted rapid prototyping"

---

## What Qualifies (examples)

✅ Auto-approve (≥7):
- Client-deployed AI dashboard with measurable outcome
- Multi-agent pipeline demo built to close a job market skill gap
- MCP server or Claude plugin that a company would pay for
- LangGraph / Agentforce demo agent

⚠️ Flag to JT (4–6):
- Useful tool but internal-only (no client/employer facing)
- Interesting approach but no measurable outcome yet
- App in development without live deployment

❌ Skip (<4):
- Cron jobs, backup scripts, cleanup scripts
- Config changes, gateway patches
- Internal research documents

## What NOT to Touch
- Contact.tsx, Hero.tsx copy (update only via explicit JT instruction)
- Services.tsx (pricing — never auto-update)
- SECURITY.md, AGENTS.md, openclaw.json
