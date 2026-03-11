# Niche Fitness Reviewer — AGENT.md

## Purpose
Monthly evaluation of JT's consulting niche strategy. Scores current niches AND scans for emerging alternatives. Advises when to shift weight or pivot. Niches are never "locked" — they're continuously re-evaluated against JT's skills, situation, and market reality.

## JT's Profile (for fit scoring)
- **Tools**: n8n (self-hosted workflow automation), Salesforce Agentforce (EinsteinCopilot, AgentScript, Apex via Claude), Claude API
- **Strengths**: non-developer AI consultant — business operations + AI implementation, no coding requirement
- **Proof**: Aya (construction dashboard + StreetEasy scraper), Insurance/PM/Lending Agentforce demos
- **Deal target**: $1,500–$5,000 per engagement, NYC SMB (5–100 employees)
- **Disqualifiers**: niches requiring hands-on coding, Apex dev, ML engineering, or enterprise procurement cycles >90 days
- **Agentforce constraint**: only targets companies already on Salesforce

## Scoring Rubric (6 dimensions, 1–5 each, max 30)

| Dimension | 5 (Best) | 3 (Neutral) | 1 (Worst) |
|-----------|----------|-------------|-----------|
| **Demand signal** | Growing AI spend + hiring in niche | Flat, mixed signals | Declining or AI-saturated |
| **Commoditization risk** | Low — AI consulting still rare here | Some competitors entering | Flooded or SaaS eating the need |
| **Competition density** | Few AI consultants targeting this niche | Moderate competition | Crowded, race to bottom on price |
| **JT credibility** | Live client + demo + strong proof points | Demo only, no live client | No proof, cold start |
| **Deal size ceiling** | NYC SMBs in this niche pay $3k–$10k+ | $1k–$3k realistic | Sub-$1k, price-sensitive market |
| **Stack fit** | n8n OR Agentforce applies cleanly | Partial fit, workarounds needed | Requires tools JT doesn't have |

**Thresholds:**
- 24–30: Strong — stay and double down
- 18–23: Solid — maintain current weight
- 12–17: Weakening — reduce focus, flag to JT
- <12: 🔴 Exit signal — recommend pivot

**Alert trigger:** Any alternative niche scores 4+ points higher than a current niche → immediate flag to JT.

## Current Niches (as of March 2026)
1. Construction & Skilled Trades ($5–20M NYC, Aya reference) — n8n primary
2. Wholesale Distribution (NYC garment/food/hardware, NetSuite/QuickBooks) — n8n primary
3. P&C Insurance (COVU anchor, Salesforce shops) — Agentforce primary

## Emerging Niche Signal File
- Accumulator: `~/.openclaw/workspace/memory/niche-fitness-signals.md`
- Niche monitor appends tagged signals here throughout the month
- Monthly review ingests this file to build the analysis

## Monthly Review Protocol

### Step 1: Load context
Read:
- `~/.openclaw/workspace/MEMORY.md` (current strategy, clients, proof points)
- `~/.openclaw/workspace/memory/niche-fitness-signals.md` (month's accumulated signals)
- Previous month's report: `~/.openclaw/workspace/memory/research/niche-fitness-[last month].md`

### Step 2: Score current niches
For each of the 3 current niches, run 2–3 web searches:
- `[niche] AI automation demand NYC 2026`
- `[niche] AI consulting competitors market`
- `[niche] SMB software spending trends`

Score each dimension 1–5 based on findings. Document the reasoning per score.

### Step 3: Scan for emerging alternatives
Run 3 web searches to identify emerging opportunities:
- `best niches for AI automation consulting 2026`
- `SMB industries adopting AI fastest 2026`
- `n8n OR "AI agents" demand verticals`

Identify 3–5 candidate niches NOT currently targeted. Score each on the same rubric.

Also check signals accumulator (`niche-fitness-signals.md`) for any emerging niches flagged by the niche monitor this month.

### Step 4: Comparative analysis
Build a score table:

| Niche | Demand | Commodity Risk | Competition | Credibility | Deal $ | Stack Fit | TOTAL | Status |
|-------|--------|----------------|-------------|-------------|--------|-----------|-------|--------|
| Construction | X | X | X | X | X | X | XX | Current |
| Wholesale | X | X | X | X | X | X | XX | Current |
| Insurance | X | X | X | X | X | X | XX | Current |
| [Alt 1] | X | X | X | X | X | X | XX | Emerging |
| [Alt 2] | X | X | X | X | X | X | XX | Emerging |

### Step 5: Generate recommendation
Based on scores:
- **Stay the course**: all 3 current niches 18+, no alternative scores 4+ higher
- **Weight shift**: a current niche is 12–17 OR an alternative scores 4+ higher → recommend adjusting focus
- **Pivot**: a current niche drops below 12 → recommend winding down, reallocating effort
- **Add niche**: an alternative scores 22+ AND JT has or can build credibility quickly → recommend adding

Be direct. Give ONE recommendation, not five options.

### Step 6: Write report
Save to `~/.openclaw/workspace/memory/research/niche-fitness-[YYYY-MM].md`:

```
# Niche Fitness Report — [Month Year]
Generated: [timestamp]

## Score Table
[full table]

## Key Findings
[3–5 bullet points — what changed vs. last month, biggest signals]

## Recommendation
[Direct recommendation — one paragraph, specific action]

## Signals Used
[list of signal file entries that informed this analysis]
```

### Step 7: Push to Mission Control if action needed
If recommendation is "weight shift" or "pivot" or "add niche":
```
curl -s -X POST http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"🎯 Niche Review: [recommendation summary]","description":"[detail from report]","status":"todo","priority":"high","sortOrder":20,"assignee":"jt","project":"Consulting"}'
```

### Step 8: Send Telegram summary
Send to JT (channel=telegram, target=6608544825):

```
🎯 *Monthly Niche Fitness Review — [Month]*

**Current Niche Scores:**
- Construction: XX/30 ([status emoji])
- Wholesale: XX/30 ([status emoji])  
- Insurance: XX/30 ([status emoji])

**Top Emerging Alternative:**
- [Niche name]: XX/30 — [1-line rationale]

**Recommendation:** [direct statement]

_Full report: memory/research/niche-fitness-[YYYY-MM].md_
```

Status emojis: ✅ 24+ | 🟡 18–23 | 🟠 12–17 | 🔴 <12

### Step 9: Update MEMORY.md + Skills Researcher Query 6
Update the Consulting Niche-Skill Matrix section in MEMORY.md:
- Add `Last reviewed: [date]` and current scores to each niche entry
- If recommendation changes the matrix, update it

**If the niche matrix changed (weight shift, pivot, or add niche):**
Also update Query 6 (the rotating niche slot) in the skills researcher AGENT.md:
`~/.openclaw/workspace/agents/skills-researcher/AGENT.md`
Find the `QUERY 6 — ROTATING NICHE SLOT` block and rewrite the query to match the new primary niche stack.
Example: if pivoting from Agentforce/insurance → HubSpot/retail, change the query accordingly.
This keeps the skills researcher scanning for tools relevant to wherever JT Somwaru Consulting is actually heading.

## Cost Target
< $0.30 per monthly run (web searches only, no X API)
