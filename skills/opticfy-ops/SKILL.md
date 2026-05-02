---
name: jt-consulting-ops
description: Five-command consulting operations skill for active client work — /client-intake, /process-doc, /runbook, /vendor-eval, /anomaly-audit. Use when JT says "client intake", "document this workflow", "write a runbook", "vendor eval", "process doc", "evaluate their stack", or is doing scoping/onboarding work with an existing or signed client. NOT for: pipeline outreach or new prospect research (use jt-consulting-pipeline skill), portfolio updates, or job applications.
---

# jt-consulting-ops — Consulting Client Operations Skill

## When to Use
Load this skill when:
- Starting a new consulting client engagement (intake, scoping)
- Documenting a client's current workflow before automating it
- Creating a runbook for an n8n workflow or automation we've built
- Evaluating a client's existing tech stack
- Running a Data Anomaly Audit engagement
- Generating a client status report or change request

## Architecture Note
This skill is modeled on Anthropic's Cowork Operations plugin (`anthropics/knowledge-work-plugins/operations`).
Key pattern: **skills = domain knowledge that fires automatically; commands = explicit workflows you invoke.**
Commands live in `skills/jt-consulting-ops/commands/`. Each is a standalone template with output format + tips.

---

## Available Commands

| Command | What It Does |
|---------|-------------|
| `/client-intake` | Discovery session → structured brief, scope doc, and engagement proposal |
| `/process-doc` | Document a client's current workflow → SOP with RACI, flowchart, edge cases |
| `/runbook` | Create a runbook for an n8n workflow or automation we've built for a client |
| `/vendor-eval` | Evaluate a client's existing tech stack → gaps, risks, automation-readiness score |
| `/anomaly-audit` | Run structured anomaly analysis on client data → revenue leak report |

---

## Client Operating System — mandatory for active clients

Every active client engagement should create a Client OS folder using `templates/client-os/`.

This is the services-as-software layer:
- **Live dashboard from day one** — clients should see status like a SaaS product, not wait for vague updates
- **Weekly account-owner update** — wins, misses, blockers, and next week's plan
- **Quarterly decision-maker review** — talk to the buyer, not only the day-to-day operator
- **Decision log + failure log** — every judgement call and miss becomes reusable IP
- **Raw + cleaned inputs + tagged outputs** — preserve the data moat before building software
- **Automation candidates** — automate patterns observed in manual delivery, not assumptions

Rule: manual delivery is not a failure state. Manual delivery is the data-collection phase. Do the work by hand until the edge cases are visible, document them, then encode the repeatable pattern into automations/agents.

---

## Domain Skills (background knowledge — fires automatically)

**Process Documentation**
- Always capture exceptions and edge cases, not just the happy path
- RACI matrix is mandatory for any process involving 2+ people or departments
- Document current state first, optimized state second — never skip baseline

**Workflow Automation (n8n / Agentforce)**
- Before documenting: confirm which system triggers the workflow (webhook, schedule, manual)
- Always document rollback: how do we undo this if something breaks?
- Runbooks must be written for someone unfamiliar with the system

**Client Engagement**
- Quick-win framing: every engagement should deliver something measurable within 2 weeks
- Anchor to ROI: time saved, revenue recovered, errors eliminated — not features built
- Treat every client like a SaaS account: live dashboard, weekly update, quarterly decision-maker review
- Capture every repeatable task, edge case, failure, judgement call, client objection, raw input, cleaned input, delivered output, and outcome produced
- Turn the first 10 sales-call objections into landing-page/proposal copy before scaling outreach
- Data Anomaly Audit is the lowest-risk entry point for new clients; always offer it if they're hesitant

**Vendor/Tech Evaluation**
- Score each tool on: integration capability, data export access, API availability, and vendor lock-in risk
- Highest-value automation targets: any tool with CSV export but no webhook = manual process we can automate

---

---

## Services-as-Software Operating Doctrine

Use consulting as the manual data-collection layer that becomes productized services, agents, and eventually software-like income.

**Niche / offer filter**
Before prioritizing a new consulting offer or vertical, answer:
1. Is this already an outsourced line item inside one industry?
2. Is the work mostly pattern recognition / rule application, not deep human-only strategy?
3. Is services spend meaningfully larger than software/tool spend?
4. Can JT credibly document and manually run the workflow before automating it?

**First-client rule**
Land early clients directly. Sales calls are research. Record/transcribe when possible, then capture:
- objections heard
- what they hated about the last vendor/tool/process
- exact words used to describe pain
- why they bought or ghosted

**Ghosting signal**
If a prospect ghosts twice, treat it as targeting/offer/data feedback, not a follow-up problem. Log it and adjust ICP, trigger, offer, or proof.

**Pricing rule**
Price the outcome like a service, report on it like a product. Prefer: setup fee + monthly retainer tied to an outcome metric + optional upside/performance component when credible. Do not anchor below a floor that makes high-quality delivery impossible.

**Scale order**
Do not scale marketing/sales/COO before delivery can run without JT. Hiring/order of delegation when needed:
1. Delivery operator
2. Technical automator
3. Head of delivery
Then scale demand.

## Usage

When JT invokes a command (e.g., "run /process-doc for Aya's rent roll process"), read the corresponding
command file in `skills/jt-consulting-ops/commands/` and follow it as the structured template for that task.

All commands work standalone (JT provides context) or with client data files (upload/paste data).

---

## Client Context Files
Client data lives at: `~/projects/jt-consulting-pipeline/clients/[slug]/`
Research output: `research.md` | Analysis: `analysis.md` | Outreach: `outreach/`

Always check if a client folder exists before starting a new engagement.

When an engagement becomes active, copy `skills/opticfy-ops/templates/client-os/` into the client folder and maintain it as the source of truth for delivery, retention, and future automation.
