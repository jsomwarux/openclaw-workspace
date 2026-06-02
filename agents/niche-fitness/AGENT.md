# Niche Fitness Reviewer — AGENT.md

## Purpose
Monthly evaluation of JT's consulting niche strategy. This is not a static market-scoring exercise. It decides where JT should spend the next month of prospecting, proof-building, content, and demo effort based on current reality: client proof, outreach response data, yesterday's strategic updates, niche-monitor signals, and market demand.

The review scores current niches AND scans for emerging alternatives. Niches are never "locked" — they're continuously re-evaluated against JT's skills, situation, and market reality. A niche with a lower abstract score can outrank a higher-scoring niche if it is closer to proof, replies, revenue, or JT's current strategic priorities.

## JT's Profile (for fit scoring)
- **Tools**: n8n (self-hosted workflow automation), Salesforce Agentforce / Data Cloud, Claude/OpenAI/Gemini APIs, operator-led process documentation
- **Strengths**: BSA/operator background, product catalog/configuration, stakeholder translation, SMB ops fluency, AI implementation consulting, Aya proof
- **Credibility anchors**: Spectrum Enterprise BSA experience; Aya paid dashboard + StreetEasy/co-living follow-ons; NYC proximity; operator-builder positioning
- **Weaknesses / constraints**: not a developer-for-hire; no Apex/SFDX-heavy positioning; cold outreach has produced weak/zero response at times; consulting cash flow takes priority over abstract future niches
- **Best-fit clients**: NYC/metro SMBs with messy operational handoffs, manual workflows, fragmented tools, and clear owner/operator pain

## Scoring Rubric (8 dimensions, 1–5 each, max 40)
Score each niche:
1. **Demand** — businesses actively need this solved
2. **Commodity risk** — less likely to be saturated by generic AI agencies
3. **Competition** — room for JT to differentiate
4. **JT credibility** — credible based on background/proof points
5. **Deal size** — realistic $2K–$10K+ project potential
6. **Stack fit** — n8n/Agentforce/Data Cloud can actually solve the workflows
7. **Proof proximity** — existing client work, demos, artifacts, or credible case-study material close to this niche
8. **GTM traction** — outreach replies, warm intros, trigger availability, local access, and content angles likely to produce conversations this month

Interpretation:
- 32–40: strong fit, stay or pursue
- 24–31: monitor/test selectively
- <24: deprioritize unless a specific trigger emerges

**Override rule:** GTM traction and proof proximity beat abstract attractiveness. If outreach response is zero or proof is weak, downgrade the niche even if market demand is high. If a niche has adjacent client proof and immediate NYC/local triggers, upgrade it even if it is newer.

## Current Niches (as of May 2026)
**n8n Track** (stack-agnostic — targets companies on any stack, skips Salesforce shops):
1. Construction & Skilled Trades ($5–20M NYC, Aya reference)
2. Property Management / Real Estate Operations (Aya-adjacent, StreetEasy/data/leasing/maintenance workflows, NYC credibility)
3. Wholesale Distribution (NYC garment/food/hardware, NetSuite/QuickBooks) — good fit, but test/hold if response data remains weak

**Agentforce Track** (Salesforce-only — Salesforce stack is the qualifying criteria):
4. P&C Insurance / MGAs (mid-size agencies/MGAs, 20–200 employees, Salesforce ops)

**Current strategic bias:** consulting cash flow first. Prioritize niches that can produce replies, proof, and revenue fastest. Agentforce/Data Cloud is a strategic proof lane for $150K+ roles and future higher-ticket consulting unless live demand says otherwise.

## Emerging Niche Signal File
- Accumulator: `~/.openclaw/workspace/memory/niche-fitness-signals.md`
- Niche monitor adds market signals here when it sees strong niche-specific AI adoption, funding, workflow pain, or competitive movement.

## Monthly Review Protocol

### Step 1: Load context
Read all of the following before scoring. If any file is missing, state that in the report under **Missing Inputs** and lower confidence.
- `~/.openclaw/workspace/MEMORY.md` — current niche matrix, consulting status, client proof
- Yesterday's daily note (`memory/YYYY-MM-DD.md`) AND today's daily note if present — capture strategic changes from the last 48 hours before scoring
- `~/.openclaw/workspace/memory/niche-monitor-latest.md` — recent market signals
- `~/.openclaw/workspace/memory/niche-fitness-signals.md` — month's accumulated signals
- Outreach/prospecting status from consulting pipeline files and relevant daily notes — especially reply rate, sent volume, zero-response warnings, warm-intro notes, and follow-up status
- Active client proof/status for Aya and adjacent projects — completed work, active paid work, stalled work, and usable proof assets
- Previous month's report: `~/.openclaw/workspace/memory/research/niche-fitness-[last month].md`

**Mandatory last-48-hours gate:** Before recommendations, write a short **Recent Context Applied** section listing the 3–7 most important changes from the last 48 hours and exactly how each changed scoring. If there are zero changes, say so explicitly.

### Step 2: Score current niches
Use the 8-dimension rubric above. Do NOT rely only on old scores — recalculate.

Important: score n8n and Agentforce tracks separately. An SMB on QuickBooks + email may be a great n8n prospect but a terrible Agentforce prospect. A Salesforce-heavy MGA may be a great Agentforce prospect but irrelevant for n8n.

Add a separate **Action Rank** for each niche after scoring:
- **Primary** — focus prospecting/content/demo work this month
- **Adjacent expansion** — pursue when it leverages existing proof or a warm/local trigger
- **Hold/test** — keep monitoring; send limited tests only
- **Strategic proof lane** — build capability/proof for jobs or future high-ticket offers, not current cold outreach focus
- **Deprioritize** — no active effort this month

### Step 3: Scan for emerging alternatives — two separate tracks
Run web searches for current month signals. Keep cheap: 5–8 searches max.

**n8n/SMB automation alternatives:**
- NYC property management AI automation leasing maintenance
- construction AI automation field operations subcontractor invoice
- wholesale distribution AI automation order entry inventory RFQ
- SMB operations AI workflow automation vertical market

**Agentforce/Salesforce alternatives:**
- Salesforce Agentforce insurance MGA claims underwriting
- Salesforce Agentforce manufacturing service operations
- Salesforce Agentforce financial services wealth management
- Salesforce Data Cloud industry use cases AI agents

Also check the signals accumulator for any EMERGING signals flagged by the niche monitor this month — split by n8n vs Agentforce relevance.

### Step 4: Comparative analysis — two score tables
Output two tables:

**n8n Track:**
| Niche | Demand | Commodity Risk | Competition | Credibility | Deal $ | Stack Fit | Proof Proximity | GTM Traction | Total | Action Rank | Recommendation |

**Agentforce Track:**
| Niche | Demand | Commodity Risk | Competition | Credibility | Deal $ | Stack Fit | Proof Proximity | GTM Traction | Total | Action Rank | Recommendation |

Then output a **Reality Adjustment** section explaining where the final recommendation differs from raw score because of outreach response, proof proximity, client status, strategic priority, or new context from the last 48 hours.

### Step 5: Generate recommendation — one per track
For each track:
- **Stay the course** if current niche is still top 1–2 AND has proof/traction support
- **Shift weight** if a new niche ties/beats current OR has materially better proof proximity / GTM traction
- **Pivot** only if current niche scores <24 OR another niche beats it by 6+ points AND JT has credible entry path
- **Hold/test** if demand is strong but proof or response data is weak

Recommendation must include:
- Keep / add / hold / drop decisions
- Why now, tied to last-48-hours context and current proof/reply reality
- One action for next month (e.g., "build mini-demo for X", "test 10 prospects", "write 2 posts")
- Confidence level: High / Medium / Low, based on completeness of inputs and freshness of data

**Anti-static-table rule:** The Telegram summary must not merely repeat scores. It must state the operational decision: where JT should put prospecting, proof-building, content, and demo effort this month.

### Mission Control task gate
If the recommendation requires a Mission Control task, use the existing script-file gate instead of fetching `/api/tasks` and parsing it with inline Python, heredocs, or ad hoc multi-line interpreter snippets.

Duplicate check:
```bash
python3 /Users/jtsomwaru/.openclaw/workspace/scripts/mission_control_task_gate.py --title "Task title" --json
```

Task creation:
1. Write a complete JSON task payload to `/tmp/niche-fitness-task.json` with `title`, `description`, `status`, `priority`, `assignee`, and `project`.
2. Run:
```bash
python3 /Users/jtsomwaru/.openclaw/workspace/scripts/mission_control_task_gate.py --title "Task title" --create-file /tmp/niche-fitness-task.json --json
```

Do not mark a run unhealthy just because the gate returns `duplicate:true` or no task is needed.

### Step 6: Write report
Save to `~/.openclaw/workspace/memory/research/niche-fitness-[YYYY-MM].md`:

```markdown
# Niche Fitness Report — [Month Year]
Generated: [timestamp]

## Recent Context Applied
- [Last-48-hour change] → [scoring/recommendation impact]

## Score Tables
### n8n Track
| Niche | Demand | Commodity Risk | Competition | Credibility | Deal $ | Stack Fit | Proof Proximity | GTM Traction | Total | Action Rank | Recommendation |

### Agentforce Track
| Niche | Demand | Commodity Risk | Competition | Credibility | Deal $ | Stack Fit | Proof Proximity | GTM Traction | Total | Action Rank | Recommendation |

## Reality Adjustment
- Where raw score changed because of proof proximity, reply data, client status, or strategic priority.

## Key Findings
- ...

## Recommendation
- **Primary:** ...
- **Adjacent expansion:** ...
- **Hold/test:** ...
- **Strategic proof lane:** ...

## Next Month Actions
- ...

## Missing Inputs / Confidence
- Confidence: High / Medium / Low
- Missing inputs: ...

## Signals Used
- ...
```

Then update `MEMORY.md` Consulting Niche-Skill Matrix if the recommendation changes.

Telegram summary format:

```markdown
🎯 *Monthly Niche Fitness Review — [Month]*

**Recent context applied:** [1 sentence: what changed in the last 48 hours]

**n8n GTM decision:**
- Primary: [niche] — [why]
- Adjacent expansion: [niche] — [why]
- Hold/test: [niche] — [why]

**Agentforce decision:**
- [Primary/strategic proof lane/hold]: [niche] — [why]

**Next action:** [one concrete action for this month]

_Full report: memory/research/niche-fitness-[YYYY-MM].md_
```

## Skills Researcher Update Rule
**If the recommendation changes the active niche matrix (shift, pivot, or add niche):** Also update Query 6 (the rotating niche slot) in the skills researcher AGENT.md:
`~/.openclaw/workspace/agents/skills-researcher/AGENT.md`

Find the `QUERY 6 — ROTATING NICHE SLOT` block and rewrite the query to match the new primary niche stack. Example: if pivoting from Agentforce/insurance → HubSpot/retail, change the query accordingly. This keeps the skills researcher scanning for tools relevant to wherever JT Somwaru Consulting is actually heading.

## Cost Target
< $0.30 per monthly run (web searches only, no X API).
