# Claude Design Prompt - Mission Control Fresh Redesign

Copy/paste the prompt below into Claude Design.

---

You are Claude Design acting as a senior product designer, information architect, and frontend systems designer.

Your task is to create a completely new, optimal design for "Mission Control," an internal operating dashboard for JT Somwaru and Eve, his AI Chief of Staff. Do not optimize the current visual design. Do not make a prettier version of the existing sidebar dashboard. Start from first principles and design the best possible command center for the actual operating system described below.

## Core Context

Mission Control is not a normal productivity app. It is JT's personal and business command center for coordinating human decisions, AI agent work, consulting pipeline, job applications, content systems, crons, costs, memory, proof logs, and autonomous overnight execution.

JT is an AI implementation specialist and operator-builder. His North Star is financial freedom through high-earning, low-maintenance income streams. His current priority order is:
1. AI implementation consulting and client/revenue work
2. App building and marketing toward eventual passive income
3. Crypto monitoring as an opportunity scan
4. Health as the base layer

Mission Control should help him answer, fast:
- What needs my attention now?
- What is Eve handling?
- What is blocked by me?
- What changed since I last looked?
- What work is actually moving me toward $10K/month, $30K/month, and eventually $100K/month?
- Which systems are healthy, stale, failing, expensive, or drifting?
- What proof has been created that can turn into revenue, content, jobs, or credibility?

The primary design principle: Mission Control should reduce attention-splitting. It should not become a beautiful graveyard of tabs. It should feel like an operational cockpit that surfaces the next decision, the current state of the machine, and the evidence behind it.

## Technical Context

Current app:
- Next.js 15 App Router
- TypeScript
- Tailwind CSS
- Convex for task data
- Local API routes reading OpenClaw files
- Localhost internal tool, no public auth requirement

Current data sources:
- Tasks: Convex via `/api/tasks`
- Crons/schedule: `~/.openclaw/cron/jobs.json` via `/api/cron`
- Memory: `~/.openclaw/workspace/memory/` via `/api/memory`
- Proof/audit logs: `~/.openclaw/workspace/proofs/` via `/api/proofs`
- Agents: `mission-control/data/agents.json` or `/api/agents`
- Costs: `/api/costs`
- Overnight work: `/api/overnight`
- Passive income ideas: `/api/passive-income`
- Skills: `/api/skills`

You may redesign navigation, page grouping, layout hierarchy, naming, density, and interaction patterns. Assume the underlying data sources can be reused or lightly adapted, but do not propose a giant backend rebuild unless absolutely necessary.

## Current Tabs and What They Are Supposed To Do

Treat these as functional requirements, not design constraints. You may combine, rename, or reorganize them if a better information architecture exists.

### Overview
Current role: high-level landing dashboard with active task counts, cron counts, failed job count, proofs today, active tasks, quick links, and gateway restart.
Optimal role: the daily command surface. It should show the top decisions and system state in priority order, not a generic metric grid. It should answer: what matters now, what changed, what is blocked by JT, what Eve completed, what is risky, and what action has the highest leverage.

### Tasks
Current role: task board with todo, in-progress, done; assignee JT/Eve/both; priority; project; descriptions with Drive links.
Optimal role: the work router. It should distinguish JT decisions, Eve-owned execution, waiting/blocked items, high-priority North Star work, and stale tasks. It should make the next action obvious and prevent the board from becoming a backlog swamp.

### Pipeline / Consulting
Current role: consulting strategy, ICP tiers, automated prospect flow, niche strategy, outreach agents.
Optimal role: revenue command center for consulting. It should show live pipeline, top opportunities, proof assets, warm-intro/referral actions, outreach readiness, client delivery status, and revenue next steps. It should make the path to $10K/month visible.

### Vibe Marketing
Current role: app/product marketing system and content flow.
Optimal role: distribution engine for apps and proof. It should show which app or proof asset is being marketed, what content is queued, what channels are active, what experiments are running, and whether the work is producing users, replies, proof, or silence.

### Passive Income
Current role: passive income ideas from scouts/strategist reports with scores and statuses.
Optimal role: opportunity portfolio. It should force prioritization, show which ideas are exploring/building/launched/shelved, and prevent JT from spreading attention across too many low-proof app ideas.

### Schedule
Current role: cron jobs and scheduled automations.
Optimal role: automation control tower. It should show what runs when, what failed, what is stale, what is too expensive, what feeds downstream systems, and what is safe/unsafe to change. It should distinguish harmless schedules from business-critical automations.

### Memory
Current role: memory browser over workspace memory files.
Optimal role: source-of-truth lookup. It should help JT and Eve retrieve decisions, project status, rules, client context, and past work without digging through files. It should surface freshness and authority: what is current, stale, contradicted, or needs verification.

### Agents
Current role: agent team view.
Optimal role: org chart for AI labor. It should show each agent's job, owner domain, last run, current task, health, output quality, permissions, and whether it needs JT, Eve, or no one.

### Monitor
Current role: placeholder deployment monitor.
Optimal role: system health. It should show OpenClaw gateway health, Mission Control app health, Convex/local backend, n8n, Tailscale, Drive sync, cron heartbeat, and key app/site uptime signals if available.

### Costs
Current role: cost dashboard.
Optimal role: burn-rate and model-routing control. It should show today's spend, weekly/monthly trend, expensive jobs, runaway risk, premium-model usage, cost per system, and whether spend is justified by output.

### History
Current role: archived/done tasks.
Optimal role: completed work ledger. It should help answer what shipped, what was closed, what was deferred, and what evidence exists. It should connect completed work to proofs, content, portfolio updates, and follow-up tasks.

### Audit
Current role: proof/action trail from JSONL logs.
Optimal role: trust ledger. It should show verified work, files changed, Drive docs created, deployments, scripts run, failures, and proof gaps. It should make Eve's claims auditable.

### Overnight
Current role: overnight autonomy runs, completed/skipped tasks, queue decisions.
Optimal role: autonomous work review. It should show what Eve did while JT was away, what was skipped and why, what needs approval, what follow-up exists, and whether the overnight agent obeyed cost/quality constraints.

### Skills
Current role: custom and bundled skills.
Optimal role: capability library. It should show what Eve can do, when to use each skill, quality/state, last used, outputs created, and missing capability gaps.

### Systems
Current role: diagrams of systems such as consulting pipeline, content machine, job market, crypto intelligence, passive income, overnight autonomy, Spanish learning, health tracking.
Optimal role: systems map. It should show how agents, files, crons, tasks, and outputs connect. It should be useful for debugging and strategic understanding, not decorative.

## Additional Operating Domains To Account For

Mission Control must represent these operating lanes clearly:
- North Star dashboard: $10K/month safe, $30K/month free, $100K/month rich
- Consulting revenue: Altmark/client delivery, prospect pipeline, proof assets, referrals, website conversion
- Job market: selective AI implementation roles, application packages, apply tasks, stale follow-ups
- Content/proof distribution: LinkedIn, X, AI Ops Teardowns, proof bank
- App portfolio: Vista, Nash Satoshi, Glow Index, Action Arena, app marketing
- Crypto intelligence: research/ranking and material alerts only, no trading
- Health/base layer: daily check-ins and health reports
- System operations: crons, costs, gateway, errors, proof logs, memory

## Design Mandate

Create a new design system and product architecture from scratch.

Do:
- Design for dense, repeated operational use.
- Prefer calm, sharp, high-signal interfaces over decorative dashboards.
- Make priority, ownership, freshness, risk, and next action visually obvious.
- Build around decision queues, system health, proof, and revenue movement.
- Use status semantics consistently: healthy, stale, blocked, failed, waiting on JT, Eve-owned, automated, manual.
- Include mobile and desktop behavior.
- Use compact cards, tables, split panes, command bars, timelines, and inspection drawers where useful.
- Design empty states, error states, stale-data states, and loading states.
- Include navigation architecture and page grouping.
- Include the first screen in detail.
- Include a component system: cards, badges, task rows, health indicators, proof links, filters, command buttons, drawers, modals.
- Include interaction patterns for triage, search, filtering, task status changes, and drilling into evidence.
- Include a clean implementation handoff that a frontend engineer can build in Next.js/Tailwind.

Do not:
- Do not preserve the current sidebar/nav just because it exists.
- Do not produce a generic SaaS analytics dashboard.
- Do not make a landing page or marketing-style hero.
- Do not use big empty cards, decorative gradients, bokeh blobs, or generic AI/neon styling.
- Do not make everything look like a task board.
- Do not hide the hard decisions behind pretty metrics.
- Do not suggest social features, public sharing, onboarding flows, or team-account concepts. This is for JT and Eve.
- Do not assume all tabs deserve equal weight.
- Do not over-focus on charts if a ranked decision list would be more useful.

## Desired Output From You

Produce a complete redesign brief with these sections:

1. Product Thesis
Explain what Mission Control should be, in one sharp paragraph.

2. Information Architecture
Propose the optimal navigation. You may consolidate current tabs. Explain what becomes primary, secondary, and archival.

3. First Screen / Command Center
Design the first viewport in detail. Include layout, zones, what data appears, and what JT should be able to decide within 30 seconds.

4. Page-by-Page Redesign
For every major page or consolidated section, define:
- Purpose
- Primary user questions it answers
- Core modules
- Data shown
- Key interactions
- Empty/error/stale states

5. Visual System
Define the aesthetic: density, spacing, typography, color roles, status colors, icon usage, table/card behavior, responsive behavior. Make it sophisticated and utilitarian, not generic dark-mode SaaS.

6. Component Inventory
List reusable components needed to build the redesign.

7. Interaction Model
Explain how JT triages tasks, opens evidence, changes status, filters by owner/project/risk, approves Eve work, and traces claims back to files/proofs.

8. Mobile Strategy
Define what mobile should prioritize. Assume mobile is for triage and quick decisions, not deep system debugging.

9. Implementation Handoff
Give a practical Next.js/Tailwind implementation plan: route structure, layout components, data dependencies, and any recommended API shaping. Keep it feasible.

10. Ruthless Design Review
Critique your own design. What could become cluttered? What should be cut? What must be protected from becoming another backlog swamp?

## Success Criteria

The best answer should make JT say:
- "This finally shows me what matters."
- "I can see what Eve did, what I need to decide, and what is moving money."
- "This is a true operating system, not just a dashboard."
- "A frontend agent could build this without needing to ask what each tab means."

Think deeply. Redesign from the mission, not from the current UI.
