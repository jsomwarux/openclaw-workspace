# Job Opportunity Scoring Criteria
*Score each opportunity out of 25, then route it into the optimal play: apply, both, consulting outreach, or market intel.*
*Before scoring anything — read jt-profile.md, especially the ⚠️ Critical Context section.*

## Pre-Screening Gate (Run Before Scoring)

Before the existing disqualifiers, apply an evidence-backed competitiveness gate. Skip without scoring when:
- JT cannot directly evidence at least 80% of must-have requirements.
- Any of the top three responsibilities lacks a concrete paid-client or Spectrum proof point.
- Two core requirements are justified only by "JT could do this with AI agents."
- The role requires prior enterprise-wide AI program ownership, quota-carrying/pre-sales history, cloud architecture authority, or credentials JT does not have.

Auto-disqualify WITHOUT scoring if ANY of the following are true:
- Role requires writing Apex / SOQL / SOSL as a primary daily activity
- Role requires Salesforce Admin, Developer, or Architect certifications as a hard requirement
- Role title is Software Engineer, Full-Stack Developer, or ML/Data Engineer
- Role is primarily about model training, fine-tuning, or ML pipelines
- Role requires 10+ years experience in a technical domain JT doesn't have
- Role requires relocation
- Salary is clearly under $130K (if disclosed)
- Role is contract/freelance (JT has JT Somwaru Consulting for that)
- **HANDS-ON CODING AS PRIMARY FUNCTION** — auto-disqualify if 3+ of the following appear as actual job responsibilities (not preferred/nice-to-have): Python, Swift, Go, Java, Terraform, CloudFormation, CI/CD pipeline ownership, GitHub Actions, Kubernetes, Docker, serverless infrastructure build (Lambda/Fargate/etc.), REST API development. Writing code daily is the job, not a bonus. **This applies regardless of title — "Architect" and "Engineer" in the title do NOT override this rule if the daily work is coding.**
- Role is pre-sales / sales engineering where demos + deal support are the primary duty (not strategy or implementation)
- Core responsibility is explaining or defending Agentforce/platform internals to technical audiences (JT builds agents, does not advise on Agentforce architecture)

### ⚠️ CRITICAL DISAMBIGUATION (apply before scoring anything)
A role can sound like "AI strategy" while being a software engineering role. If the JD responsibilities section lists 4+ technical engineering tasks (writing code, building pipelines, deploying infrastructure), it is a software engineering role regardless of title. Score it 0 and skip.

If a role passes the gate, score it below.

---

## 1. Role Scope Fit (0–8)
*This is the most important dimension — weighted higher than salary.*

Does the job match JT's actual abilities as an AI automation consultant, agent orchestrator, and BSA?

| Score | Criteria |
|-------|----------|
| 8 | Perfect fit — AI implementation/consulting, Agentforce configuration (not dev), or AI automation with BSA bridge. JT could do 90%+ of this job today. |
| 6–7 | Strong fit — AI-adjacent role focused on strategy, tooling selection, workflow design, or client-facing implementation. Minor skill gaps easily bridged. |
| 4–5 | Good fit in one dimension — either AI/automation OR BSA/systems, but not both. Stretch role JT could grow into. |
| 2–3 | Partial fit — uses some of JT's skills but has significant requirements he can't meet without misrepresenting himself. |
| 0–1 | Weak or no fit — do not include. |

**Key questions to guide scoring:**
- Does it require *directing* AI systems vs. *building* them at the code level? (Directing = good)
- Does it require a business/client-facing layer? (Yes = good)
- Could JT genuinely do this job with his current skills + AI agent tooling? (Yes = surface it)
- Does the JD use "Apex", "SFDX", "Terraform", "MLOps", "model training" as requirements? (Yes = likely disqualify)

---

## 2. Salary (0–5)

| Score | Criteria |
|-------|----------|
| 5 | $200,000+ base |
| 4 | $175,000–$199,999 base |
| 3 | $150,000–$174,999 base |
| 2 | $130,000–$149,999 base (include with note: below target) |
| 1 | Undisclosed (include with flag) |
| 0 | Under $130,000 (skip) |

---

## 3. Company Quality (0–5)

| Score | Criteria |
|-------|----------|
| 5 | Strong brand, Glassdoor 4.0+, known AI or Salesforce leader |
| 4 | Solid company, Glassdoor 3.7+, good reputation |
| 3 | Decent company, Glassdoor 3.5+, no major red flags |
| 2 | Mixed signals — Glassdoor 3.0–3.4 or unclear culture |
| 1 | Red flags — Glassdoor <3.0 or concerning news |
| 0 | Hard avoid — Glassdoor <2.5, toxic culture confirmed, financial distress |

Automatic +0.5 signal (note in brief): Salesforce ISV partner, known AI-first culture, active Agentforce practice.

---

## 4. Location & Format (0–4)

| Score | Criteria |
|-------|----------|
| 4 | Fully remote |
| 3 | Hybrid NYC or in-office NYC |
| 2 | Remote with occasional NYC travel |
| 1 | Technically accessible but impractical |
| 0 | Relocation required — auto-disqualify (already caught in pre-screen) |

---

## 5. Career Trajectory (0–3)

Does this role advance JT toward: AI Solutions Architect → Agentforce Practice Lead → AI Consulting firm owner?

| Score | Criteria |
|-------|----------|
| 3 | High-visibility AI role — clear resume builder, network access, leadership component |
| 2 | Solid growth potential — execution-focused but room to lead and be recognized |
| 1 | Lateral or minor step — won't hurt but won't accelerate trajectory |
| 0 | Step backward — less AI exposure than his current JT Somwaru Consulting work |

---

## Scoring Summary

| Total Score | Default Action |
|-------------|----------------|
| 22–25 | 🔥 Apply if comp/location fit; consider dual-track only if JD exposes a consulting wedge |
| 20–21 | 🟠 Dual-track or consulting-first; apply only if the role is unusually strategic |
| 18–19 | 🟠 Consulting-first / stretch application; usually do not spend resume time yet |
| 15–17 | 🟡 Market intel or consulting lead only if company/ICP fit is strong |
| 12–14 | 👀 Market intel only — include only if nothing stronger found |
| 0–11 | ❌ Skip |

## Opportunity Route

Before assigning `apply` or `both`, verify the posting is live. A cached JD from BuiltIn, LinkedIn, or another aggregator is not enough. If the page/UI says the role was removed, closed, expired, or no longer accepts applications, set status `expired` and route `market-intel` only.

After scoring, assign exactly one route:

| Route | Use When | Recommended Output |
|-------|----------|--------------------|
| `apply` | 22+/25, $150K+, real fit, low misrepresentation risk, advances JT toward AI Implementation Lead / Solutions Architect | Recommend tailored resume + cover letter package only after live posting/application verification; create/update MC application task |
| `both` | 20–21/25 or strategically exceptional, and the JD reveals a clear operational AI/governance/workflow pain JT can solve in a contained engagement | Create/verify both handoffs in the same run: application task after live-posting verification + consulting job-signal note + MC review task; JT chooses sequencing |
| `consulting-outreach` | Company is hiring for AI implementation but role is too technical/senior/narrow for JT, or company is SMB/mid-market/operator-heavy and likely has immediate implementation pain | Create prospect job-signal note + MC review task for JT; no resume package |
| `market-intel` | Useful as evidence of demand, skill gap, or positioning, but not a good application or outreach target | Log pattern only; create `Verify job signal` MC task only when a specific live-JD verification step is needed |

**Important interpretation:** A full-time AI role does NOT mean the company has no consulting interest. It usually means budget + urgency exist. But the outreach must be framed as interim de-risking, implementation mapping, or pilot governance while the hire ramps — never as "hire JT instead of the employee."

---

## Role-to-Build Extraction

Before creating any job-derived build/demo/skill/consulting task, update `data/role-to-build-matrix.md`. For each 18+/25 role or strong hiring signal, extract:

1. **Hiring pain** — the operational pain the JD reveals.
2. **Proof gap** — what JT would need to prove, package, or reframe.
3. **Best move** — exactly one of `apply_package`, `consulting_bridge`, `build_demo`, `skill_or_agent`, `market_intel`, or `discard`.
4. **Mapped artifact** — the existing proof lane it belongs to, or `new` only if genuinely uncovered.
5. **Build/demo decision** — `extend existing`, `create new`, `defer`, or `no build`.
6. **Consulting angle** — contained bridge offer, or `none`.
7. **Priority vs Altmark** — default `below Altmark` unless the role has a live deadline or directly strengthens paid-client proof.
8. **Mission Control action** — one task title, or `none`.

Default to consolidation. AdoptAI, ROIFlow, AgentOps, ChampionOps, EnablementOps, AgentGuard, AgentMesh, TelcoAgent, and DealDesk are proof lanes, not excuses to create duplicates.

---

## What to Include in the Brief Per Role

For each role that clears the bar, include:
1. **Title + Company + Location/Format**
2. **Score** (X/25) with one-line rationale
3. **Salary** (stated or "undisclosed")
4. **Why it fits JT** — 2 sentences max, specific to his background
5. **Any caveats** — stretch requirements, culture flags, travel expectations
6. **Link** to job posting
7. **Recommended route** — apply / both / consulting outreach / market intel, with one sentence explaining why
8. **Role-to-build extraction** — hiring pain, proof gap, best move, mapped artifact, build/demo decision, consulting angle, priority vs Altmark, and MC action
