# AI Implementation Intelligence System

Created: 2026-05-15
Purpose: give JT a compounding edge in AI implementation, governance, workflow design, and operationalization.

## Core Thesis
The winning edge is not one smarter agent. It is a delivery system where every discovery call, build, failure, client objection, test case, and post-launch issue upgrades the next engagement.

JT should build an **Implementation Intelligence System** around these loops:
1. Diagnose the workflow better than competitors.
2. Govern the risky parts before building.
3. Build narrow, useful systems fast.
4. Test with golden cases and failure cases.
5. Document runbooks, owners, approval boundaries, and rollback paths.
6. Capture lessons after every build.
7. Turn repeated lessons into checklists, templates, skills, agents, and proof assets.

## Existing Edge
Already present:
- n8n agent with `tasks/lessons.md` loop.
- AI governance readiness skill.
- Agent Operations Layer Audit offer.
- Client OS template for capturing repeatable IP.
- Proof gates preventing overclaiming.
- Content/proof distribution system.
- Project lessons rule forcing agents to read `lessons.md` before builds.

Gap: the lessons loop exists for n8n, but not yet for the full consulting lifecycle.

## Phase 0 Rule — Prove The Case File Before Building Agents

Before creating standalone agents, validate one complete workflow intelligence loop manually.

Canonical artifact: `memory/consulting/workflow-case-file-template.md`

Every client workflow should produce one Workflow Case File with:
- workflow name, owner, users, systems, data sources
- current-state workflow map
- exception types and hidden dependencies
- approval-boundary map
- first safe build recommendation
- golden and failure test cases
- launch acceptance checklist
- rollback/manual fallback
- runbook skeleton
- post-launch review notes
- lessons captured
- reusable patterns extracted

Do not split the system into multiple agents until this artifact has been tested on at least one anonymized workflow and the handoffs are clear.

Phase 0 validation test:
1. Create one anonymized Aya/Altmark-safe Workflow Case File.
2. Run the existing AI governance readiness skill against it.
3. Add one small golden/failure test pack.
4. Add a runbook skeleton.
5. Extract three reusable pattern candidates.
6. Only then decide which standalone agent should be built first.

## Recommended Agent/Skill Stack

### 1. Workflow Discovery Agent
Role: turn messy client inputs into a buildable workflow spec.

Inputs:
- discovery call transcript/notes
- screenshots, spreadsheets, SOPs, Slack/email snippets, forms, reports
- buyer goals and constraints

Outputs:
- current-state workflow map
- actors/owners/systems/data sources
- exception types
- approval points
- automation candidates
- “do not automate” boundaries
- first safe build recommendation

Lessons loop:
- `~/projects/workflow-discovery-agent/tasks/lessons.md`
- After each discovery: add missed questions, confusing client language, hidden dependencies, better prompts, better diagrams.

Why it matters:
Most AI implementers skip real workflow discovery and jump to tools. This agent makes JT better at the highest-leverage upstream step.

### 2. Governance + Risk Agent
Role: convert a workflow spec into approval boundaries, failure modes, launch gates, and client-ready risk controls.

Inputs:
- workflow spec from Discovery Agent
- data sensitivity
- external-action risk
- compliance/privacy constraints

Outputs:
- can automate / can draft / must approve / must not automate map
- risk register
- test cases for hallucination, stale data, wrong recipient, malformed input, duplicate records
- launch acceptance checklist
- rollback/manual fallback plan

Lessons loop:
- `~/projects/governance-risk-agent/tasks/lessons.md`
- Add every failure mode discovered in client work.

Why it matters:
This is where JT differentiates from “AI automation guy.” It makes the buyer trust the system.

### 3. Golden Test Case Agent
Role: create and maintain test packs for every client workflow.

Inputs:
- workflow spec
- sample data
- edge cases
- known bad inputs

Outputs:
- golden test cases
- adversarial/failure cases
- expected outputs
- pass/fail checklist
- regression suite to rerun before delivery

Lessons loop:
- `~/projects/workflow-test-agent/tasks/lessons.md`
- Every bug becomes a reusable test pattern.

Why it matters:
Most SMB automations are demo-tested, not workflow-tested. This creates quality proof.

### 4. Runbook + Handoff Agent
Role: produce the client-facing operating manual for every delivered system.

Inputs:
- final workflow
- owner/approver list
- infrastructure locations
- failure modes
- support boundaries

Outputs:
- how it works
- owner map
- pause/kill/restart steps
- approval workflow
- common errors and fixes
- escalation path
- client admin checklist

Lessons loop:
- `~/projects/runbook-handoff-agent/tasks/lessons.md`
- Add every client confusion, support issue, missing screenshot, and handoff gap.

Why it matters:
Handoff quality is a major trust signal and retainer wedge.

### 5. Post-Launch Improvement Agent
Role: review live/finished workflows after use and recommend improvements.

Inputs:
- logs
- errors
- client feedback
- output samples
- approval delays
- manual overrides

Outputs:
- what worked
- what failed
- what users ignored
- which exception rules need tuning
- next iteration recommendation
- retainer/support opportunity

Lessons loop:
- `~/projects/post-launch-ops-agent/tasks/lessons.md`
- Turns production usage into IP.

Why it matters:
This makes client work compound after launch instead of ending at delivery.

### 6. Implementation Pattern Library Skill
Role: central library of reusable workflow patterns.

Examples:
- exception queue
- reply drafting with human approval
- stale-data blocker
- duplicate record resolver
- weekly owner brief
- intake classifier
- document-to-tracker pipeline
- vendor follow-up queue
- local-first sensitive file automation

Artifact:
- `memory/consulting/implementation-pattern-library.md`

Why it matters:
JT should stop solving the same workflow shape from scratch.

### 7. Client Objection Intelligence Skill
Role: capture and answer objections from owners/operators.

Examples:
- “Will this replace my staff?”
- “What if it sends the wrong thing?”
- “Where does the data go?”
- “Can I turn it off?”
- “Who owns it after you leave?”
- “What if the AI makes something up?”

Artifact:
- `memory/consulting/objection-intelligence.md`

Why it matters:
Sales edge comes from answering operational fear better than competitors.

### 8. Vertical Workflow Scout Agent
Role: research one vertical and produce workflow maps + first-build candidates.

Inputs:
- vertical name
- geography, if relevant
- buyer type

Outputs:
- common workflows
- template/spreadsheet evidence
- software stack
- manual pain points
- buyer language
- first workflow candidates
- distribution channels
- joke-vertical score

Lessons loop:
- `~/projects/vertical-workflow-scout/tasks/lessons.md`

Why it matters:
This lets JT enter boring verticals faster and with real workflow language.

## Corrected Build Order

### Phase 0 — Validate the artifact before agent sprawl
1. **Workflow Case File template + data-handling rules**
2. **Manual Phase 0 test on one anonymized workflow**
3. **One governance pass using the existing AI governance readiness skill**
4. **One small golden/failure test pack**
5. **One runbook skeleton**
6. **Three reusable pattern candidates**

This proves the delivery loop before creating multiple standalone agents.

### Phase 1 — Build only after Phase 0 proves the handoff
7. **Workflow Discovery + Governance combined v0**
8. **Implementation Pattern Library v0 seeded from the Phase 0 test**

Discovery and governance should stay together at first. Splitting them too early creates handoff overhead before the artifact shape is stable.

### Phase 2 — Quality moat
9. **Golden Test Case / Acceptance Gate**
10. **Runbook + Handoff template or agent**

These make delivery look professional and safer than competitors.

### Phase 3 — Compound after live usage
11. **Post-Launch Improvement Agent**
12. **Client Objection Intelligence Skill**
13. **Vertical Workflow Scout Agent**

These are useful, but should wait until the first workflow case-file loop is validated.

## Operating Protocol For Every Client Workflow

1. Discovery Agent creates workflow spec.
2. Governance Agent creates boundary/risk map.
3. Build Agent/n8n Agent builds narrow first version.
4. Golden Test Agent creates and runs test pack.
5. Runbook Agent creates handoff package.
6. Post-Launch Agent reviews usage and failures.
7. Lessons from all agents update pattern library, objection library, and relevant lessons.md files.
8. Proof gate checks whether anything can become content, website proof, deck snippet, or referral asset.

## What To Avoid
- Too many agents before one loop is working.
- Agents that produce analysis without a final client artifact.
- Generic “AI consultant” frameworks.
- Building autonomous agents before approval boundaries and tests exist.
- Storing client secrets or private data in reusable examples.
- Overclaiming client results before proof gates are clean.

## First Concrete Move
Create the Workflow Discovery Agent first. It should produce a client-ready workflow spec and feed the existing AI governance readiness skill and n8n build process.

Done state for Phase 1:
- `~/projects/workflow-discovery-agent/CLAUDE.md`
- `~/projects/workflow-discovery-agent/tasks/lessons.md`
- `memory/consulting/implementation-pattern-library.md`
- MC task to test it on Aya/Altmark-safe anonymized workflow notes
