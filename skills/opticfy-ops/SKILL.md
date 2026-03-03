# opticfy-ops — Opticfy Client Operations Skill

## When to Use
Load this skill when:
- Starting a new Opticfy client engagement (intake, scoping)
- Documenting a client's current workflow before automating it
- Creating a runbook for an n8n workflow or automation we've built
- Evaluating a client's existing tech stack
- Running a Data Anomaly Audit engagement
- Generating a client status report or change request

## Architecture Note
This skill is modeled on Anthropic's Cowork Operations plugin (`anthropics/knowledge-work-plugins/operations`).
Key pattern: **skills = domain knowledge that fires automatically; commands = explicit workflows you invoke.**
Commands live in `skills/opticfy-ops/commands/`. Each is a standalone template with output format + tips.

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
- Data Anomaly Audit is the lowest-risk entry point for new clients; always offer it if they're hesitant

**Vendor/Tech Evaluation**
- Score each tool on: integration capability, data export access, API availability, and vendor lock-in risk
- Highest-value automation targets: any tool with CSV export but no webhook = manual process we can automate

---

## Usage

When JT invokes a command (e.g., "run /process-doc for Aya's rent roll process"), read the corresponding
command file in `skills/opticfy-ops/commands/` and follow it as the structured template for that task.

All commands work standalone (JT provides context) or with client data files (upload/paste data).

---

## Client Context Files
Client data lives at: `~/projects/opticfy-pipeline/clients/[slug]/`
Research output: `research.md` | Analysis: `analysis.md` | Outreach: `outreach/`

Always check if a client folder exists before starting a new engagement.
