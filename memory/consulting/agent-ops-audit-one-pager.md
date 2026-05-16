# Agent Operations Layer Audit — One-Pager

Created: 2026-05-15
Owner: JT Somwaru Consulting
Status: draft-ready for JT review; no external messages sent.
Drive draft: https://docs.google.com/document/d/1Bkw1jnxIi2hhol-ewBL5_6K1GDahBCvN9fx0FNGgM0o/edit
Source: `memory/consulting/agent-operations-layer-audit.md`

## Who This Is For

Founder-led SMBs, service businesses, agencies, property operators, construction/trades companies, and local operators that are already using AI somewhere in the business — ChatGPT, automations, browser agents, Zapier/n8n, AI writing tools, spreadsheet helpers, or one-off scripts — but do not yet have a reliable operating layer around them.

Best fit buyers:
- Owner, COO, CFO, controller, ops lead, or department head
- Teams where one person “knows how the automations work”
- Businesses using AI for quoting, admin, marketing, reporting, research, customer replies, documentation, or follow-up
- Teams worried that AI/automation work is becoming useful but fragile

## The Problem

Most small businesses do not have an AI adoption problem anymore.

They have an AI operations problem.

AI is already showing up in daily work: employees use ChatGPT, someone built a Zap, an assistant drafts emails, a browser extension touches customer data, a script runs on one laptop, or an automation nobody fully owns still fires every week.

That creates quiet risk:
- Nobody has a complete registry of agents, automations, prompts, jobs, and owners
- Some tools can send messages, edit records, scrape sites, spend money, or touch sensitive data
- Approval rules are unclear
- Business process knowledge lives in Slack/email threads instead of runbooks
- Useful AI work breaks when one employee is unavailable
- Review queues grow instead of shrinking workload
- There is no kill switch, audit trail, or fallback path

## The Diagnostic Promise

In a 7-day Agent Operations Layer Audit, JT maps the business’s AI/automation footprint, documents the highest-risk workflows, and identifies the first governed system worth building.

The output is not generic AI training.

It is a practical operating map: what exists, who owns it, what can run safely, what needs approval, what should be killed, and which workflow is ready for a controlled first build.

## What The Audit Covers

1. **Agent + automation registry**  
   Tools, scripts, automations, scheduled jobs, browser agents, AI workflows, owners, purpose, schedule, access, and risk.

2. **Workflow memory map**  
   Where the business’s real SOPs live today: Slack/email threads, spreadsheets, docs, templates, screenshots, inbox patterns, and manual handoffs.

3. **Zombie + shadow automation check**  
   Forgotten jobs, personal-laptop workflows, unmanaged browser profiles, unclear API key usage, unowned scripts, and tools with external-action risk.

4. **Approval-boundary map**  
   What can be automated, what can be drafted, what must be approved, and what should never be automated.

5. **Exception dashboard spec**  
   The exact states that should interrupt a human: stuck work, changed status, missing data, overdue approvals, failed runs, or risky external action.

6. **First governed workflow recommendation**  
   One narrow workflow that can produce value without turning into business-critical spaghetti.

7. **Runbook + handoff package**  
   Owner, pause/kill/restart path, failure modes, audit log expectations, backup owner, and escalation rules.

## AI Boundary Rules

**Can automate:** formatting, status checks, scheduled summaries, deterministic routing, duplicate checks, report preparation.

**Can draft:** customer/vendor replies, internal summaries, classifications, research notes, follow-up messages, SOP drafts.

**Must approve:** external sends, customer/vendor-facing action, financial updates, CRM/source-system edits, escalations, sensitive commitments.

**Must not automate:** payments, transfers, legal/compliance decisions, account credentials, irreversible deletes, or sensitive client commitments.

## Example First Builds

- A registry of every AI/automation touchpoint in the business
- A weekly exception brief for stuck work and approvals
- A controlled customer/vendor reply-drafting workflow
- A local-first reporting workflow for sensitive files
- A document/intake classifier with human review
- A kill-switch/runbook layer around existing n8n/Zapier/scripts
- A lightweight dashboard showing what changed, what failed, and who owns the next action

## What Good Looks Like After The Audit

The team can answer:
- What AI/automation systems are running?
- Who owns each one?
- What data can each touch?
- What can each system send, edit, spend, or trigger?
- What breaks if the owner is out?
- What requires human approval?
- What should be paused or killed?
- What is the safest first workflow to improve next?

## Best First CTA

> Worth doing a 30-minute AI operations diagnostic? I can map the automations, agents, approval points, and fragile workflows already inside the business, then show you the first system worth cleaning up or building.

## Proof / Claim Boundaries

Use anonymized examples only. Do not name active clients or imply measured metrics, reduced risk, compliance outcomes, or live client acceptance unless proof gates are clean and permission exists.

## Recommendation

Verdict: Ready after buyer review
First safe build: Agent/automation registry + approval-boundary map
Do first: Use this one-pager in warm conversations where the buyer already uses AI informally or has fragile automations/scripts
Do not do yet: Pitch a broad AI platform, chatbot, or autonomous agent system before the audit identifies one controlled workflow
Expansion trigger: Buyer can name at least one AI/automation workflow that is useful, fragile, risky, or owned by only one person
