# JT Somwaru Consulting AI Consulting: Complete Client Engagement Playbook
*Last updated: 2026-03-03 | Two tracks: Agentforce + n8n*

---

## THE BIG PICTURE

Every engagement follows this arc:

```
FIND → QUALIFY → PREP → DISCOVER → DESIGN → BUILD → TEST → DEPLOY → SUPPORT
 1wk  1 call   30min  60-90min  1-2 days  2-5 days 1-2 days  1 day  ongoing
```

Total typical engagement: 2-3 weeks from signed agreement to production.

**Two delivery tracks — different niches, different stacks:**

| Track | Skill | Target Niches | Qualifying Signal |
|-------|-------|--------------|-------------------|
| **Agentforce** | Salesforce Agentforce | Insurance, Mid-large PM/RE | Already on Salesforce Enterprise+ |
| **n8n** | n8n automation | Construction/Skilled Trades ($5-20M), Wholesale Distribution | Using ServiceTitan, Jobber, QuickBooks, NetSuite, or spreadsheets |

---

## STAGE 1: FIND THE CLIENT

### Agentforce Prospects (Salesforce shops)
- **Insurance** — COVU is Tier 1 anchor. Zipari secondary. Any NYC insurer/insurtech on Salesforce.
- **Mid-to-large Property Management / Real Estate** — Rudin, TF Cornerstone, Dermot, GFP, Landsman. Larger PM firms tend to be on Salesforce.
- **Lending / Fintech** — Biz2Credit (Tier 1, confirmed Salesforce). NYC commercial lenders.

### n8n Prospects (non-Salesforce shops)
- **Construction + Skilled Trades ($5-20M)** — GCs, electricians, HVAC, plumbing. On ServiceTitan, Jobber, Buildertrend. Aya is your reference client.
- **Wholesale Distribution** — NYC garment district, food/bev, hardware. On QuickBooks, NetSuite, or industry ERPs.
- **Small PM companies** — On AppFolio or Buildium (NOT Salesforce) → n8n, not Agentforce.

### Outreach Message Framework

**Agentforce track:**
> "I help [insurance/property management] companies automate [specific pain point] using Salesforce's new AI agent platform, Agentforce. One of my clients went from [X manual hours] to [Y automated resolution rate] in [Z weeks]. Would you be open to a 15-minute call to see if this could work for your team?"

**n8n track:**
> "I help [construction/trades/wholesale] companies automate [specific pain point] — like job scheduling, invoicing, and follow-ups — without replacing your existing tools. One workflow I built for a NYC construction client eliminated [X] hours of manual work per week. Would you be open to a 15-minute call?"

### Qualifying Questions (Before You Pitch)

**Agentforce qualifying:**
1. "What Salesforce edition are you on?" (Need Enterprise, Unlimited, or Performance)
2. "Do you currently use Service Cloud, Sales Cloud, or both?"
3. "How many support cases/tickets do you handle per month?"
4. "What's your biggest bottleneck — customer response time, internal processes, or data lookup?"
5. "Have you looked into Agentforce or Salesforce AI features yet?"

**n8n qualifying:**
1. "What tools do you use to run your business day-to-day?" (ServiceTitan, Jobber, QuickBooks, etc.)
2. "What does your team do manually that you wish happened automatically?"
3. "How many [jobs/orders/transactions] do you process per week?"
4. "Do you have someone technical on staff, or is it mostly field operations?"
5. "What's the most time-consuming administrative task for your team?"

### Kill the Deal Early If:

**Agentforce:**
- They're on Salesforce Professional Edition (Agentforce requires Enterprise+)
- No budget for Agentforce licenses (Flex Credits ~$0.10/action)
- Salesforce org is a disaster and they won't pay for cleanup first
- They want a chatbot, not an agent

**n8n:**
- No digital tools at all — purely paper/verbal processes (n8n needs something to integrate with)
- No consistent, repeatable processes (automation requires a defined workflow to automate)
- They need a full CRM implementation first — that's a different project

---

## STAGE 2: PRE-DISCOVERY PREP (30 minutes before the call)

**Do this before every discovery call — non-negotiable.** This is how you walk in sounding like an expert.

Run an agent briefing with Eve:
1. Company research: what they do, revenue scale, employee count, NYC presence
2. Their tech stack if findable (LinkedIn, G2, Salesforce AppExchange customer reviews)
3. Common pain points for this industry + company size
4. What their competitors are doing with AI/automation
5. 2-3 specific examples you can reference during the call ("companies like yours are seeing X")

For **Agentforce calls**: know their Salesforce edition if findable, any known integrations.
For **n8n calls**: know what tools dominate their industry (ServiceTitan for HVAC, Jobber for smaller trades, Buildertrend for GCs, etc.).

After the briefing, you should be able to name 2-3 specific pain points before they tell you. This creates immediate credibility.

---

## STAGE 3: THE DISCOVERY CALL

60-90 minutes. The single most important meeting. What you learn here determines everything.

### The 5 Discovery Sections

#### SECTION A: Business Context (10 minutes)

| # | Question | Why You Need This |
|---|---|---|
| A1 | "Walk me through your company — what do you do, who are your customers, and what's your scale?" | Sets the frame. Agent tone, vocabulary, and complexity depend on this. |
| A2 | "What does your team structure look like? Who handles customer inquiries today?" | Tells you if this is a service agent, sales agent, or internal agent (Agentforce) or which workflows to automate (n8n). |
| A3 | "What's the business problem you're trying to solve? What's it costing you today?" | Becomes your ROI story and the agent's/automation's success metric. |
| A4 | "Have you tried any solutions for this already? What worked and what didn't?" | Avoids repeating past failures. Reveals what they actually value. |
| A5 | "What does success look like 90 days after we launch?" | Defines acceptance criteria and deliverables. |

#### SECTION B: Process Mapping (20 minutes)

For each process the agent/automation will handle:

| # | Question | What This Becomes |
|---|---|---|
| B1 | "Walk me through exactly what happens when [trigger event occurs]. Step by step." | A **Topic** (Agentforce) or a **Workflow** (n8n) |
| B2 | "What information does your team need to look up to handle this? Where does that data live?" | **Actions** (Agentforce: SOQL/Apex) or **nodes** (n8n: API calls) |
| B3 | "What decisions does your team make? What are the rules?" | **AgentScript conditional logic** (Agentforce) or **IF nodes** (n8n) |
| B4 | "When does this need to be escalated to a human?" | **Escalation guardrails** (Agentforce) or **Slack/email alert** (n8n) |
| B5 | "What information do you typically need from the customer/requester?" | **Input variables** / conversation flow (Agentforce) or **form/trigger fields** (n8n) |
| B6 | "What's the most common version of this request? And the edge case?" | Happy path + error handling in both tracks |
| B7 | "How do you want [the agent / the notifications] to sound? Formal? Casual?" | Agent tone instructions (Agentforce) or message templates (n8n) |
| B8 | "Are there things it should NEVER do or say?" | **Guardrails** (Agentforce) or hard-coded exclusions (n8n) |

Repeat B1-B8 for every process.

#### SECTION C: Data & Systems (15 minutes)

**Agentforce:**

| # | Question | Why |
|---|---|---|
| C1 | "Show me your Salesforce org — what custom objects do you have?" | Maps the data model |
| C2 | "Where does your customer data live? All in Salesforce or spread across systems?" | Determines if you need external integrations |
| C3 | "Do you have a knowledge base, FAQ, or help center?" | Becomes agent knowledge grounding |
| C4 | "What existing Flows do you have in Salesforce?" | Can reuse as agent actions |
| C5 | "Do you have custom Apex that handles business logic?" | Same — reuse if exists |
| C6 | "How clean is your data? Duplicates, missing fields, inconsistencies?" | Dirty data = agent failures |

**n8n:**

| # | Question | Why |
|---|---|---|
| C1 | "What tools do you use for [jobs/orders/customers]?" | Determines which n8n nodes to build |
| C2 | "Do these tools have APIs or do you use them manually?" | Determines integration feasibility |
| C3 | "Where does customer/job data currently live?" | Source of truth for the workflow |
| C4 | "Do you use Google Workspace, Microsoft 365, or Slack?" | Common notification targets |
| C5 | "Are there any tools you want to replace as part of this?" | Scope — be careful here |

#### SECTION D: Technical Requirements (10 minutes)

**Agentforce:**

| # | Question | Why |
|---|---|---|
| D1 | "What Salesforce edition and licenses do you have?" | Confirms Agentforce compatibility |
| D2 | "Do you have Agentforce licenses or Flex Credits already?" | If not, they purchase from Salesforce first |
| D3 | "Do you have sandbox environments available?" | Need Developer Sandbox minimum |
| D4 | "Do you use any DevOps tools? (Copado, Gearset, GitHub Actions)" | Determines deployment path |
| D5 | "Where should this agent be accessible? Website chat? Slack? Inside Salesforce?" | Channel deployment |
| D6 | "Any security or compliance requirements? (HIPAA, SOX, etc.)" | May need additional guardrails |
| D7 | "Who on your team will be the point of contact for testing and approval?" | Your go-to person |
| D8 | "Who will maintain the agent after launch? Do you have a Salesforce admin?" | Determines documentation depth |

**n8n:**

| # | Question | Why |
|---|---|---|
| D1 | "Do you have someone who can help set up API access for [their tool]?" | n8n needs API credentials |
| D2 | "Do you have a server/VPS, or is everything on laptops?" | Determines if n8n is self-hosted or cloud |
| D3 | "Any compliance requirements? (healthcare, financial data handling)" | May affect what we can automate |
| D4 | "Who on your team will receive alerts/notifications from the automation?" | Determines output nodes |
| D5 | "Who will call me if something breaks?" | Your go-to contact |

#### SECTION E: Scope & Timeline (10 minutes)

| # | Question | Why |
|---|---|---|
| E1 | "Of everything we discussed, what's the highest priority? If we could only launch one thing, what would it be?" | Defines MVP |
| E2 | "Is there a deadline or event driving this?" | Sets timeline |
| E3 | "What's your budget range for this project?" | Determines scope |
| E4 | "Who needs to approve this project?" | Identifies decision maker |

---

## STAGE 4: THE PROPOSAL

Write and send within 24-48 hours of discovery. Strike while it's warm.

### Proposal Structure

**1. Executive Summary** (1 paragraph)
- What they told you their problem is (use their exact words)
- What you're going to build
- Expected outcome/ROI

**2. Architecture / Automation Design**

*Agentforce:* Agent name + type, Topics + descriptions, Actions per topic, Channel(s), Escalation paths

*n8n:* Workflow name, Trigger event, Step-by-step process map, Integrations, Notification/output design

**3. Scope of Work**
- What you will build
- What the client is responsible for (org/API access, data cleanup, licenses, UAT)
- What is explicitly NOT included (prevents scope creep — be specific)

**4. Timeline**
- Phase 1: Setup & Access (Day 1-2)
- Phase 2: Build (Day 3-7)
- Phase 3: Testing (Day 8-10)
- Phase 4: Deployment & Training (Day 11-12)

**5. Pricing**
- Your fixed project fee
- *Agentforce note:* Client is responsible for their own Salesforce/Agentforce license costs
- *n8n note:* Client is responsible for any paid API tiers from their tools (ServiceTitan, Jobber, etc.)

**6. What the Client Needs to Provide**
- *Agentforce:* Sandbox access, dedicated user account, Agentforce licenses/Flex Credits, 2-4 hours for UAT
- *n8n:* API credentials for their tools, webhook access if needed, 1-2 hours for testing walkthrough

---

## STAGE 5: CONTRACT & SOW

**Do not start work without a signed agreement.** This is non-negotiable.

Minimum contract terms to include:
- Exact scope (reference the proposal — attach it as Exhibit A)
- Fixed fee amount + payment terms (50% upfront, 50% on deployment)
- What constitutes "done" — specific acceptance criteria
- Change order process — anything outside scope is a new SOW
- IP ownership — client owns all metadata, code, and configurations deployed to their org/server
- Confidentiality — you won't share their business processes or data
- Limitation of liability

Use a simple 1-2 page consulting agreement. Send via DocuSign or similar for digital signature. Do not start the kickoff until the deposit clears.

---

## STAGE 6: CLIENT ONBOARDING (Day 1-2)

### Agentforce Onboarding

**Step 1: Get Access**

> "To begin work, I need the following:
>
> 1. A **Developer Sandbox** (or Developer Pro Sandbox) — please create one if you don't have one available
> 2. A **user account** in that sandbox with System Administrator profile
> 3. The **login URL** for the sandbox (format: https://[orgname]--[sandboxname].sandbox.my.salesforce.com)
> 4. **Confirmation that Agentforce is enabled** in the sandbox (Setup → Agentforce Agents should be visible)
> 5. The name and email of your **point of contact** during the build
>
> Required permissions on my user: System Administrator profile, or at minimum: Customize Application, Modify All Data, View Setup and Configuration, Author Apex, Manage Flows, Einstein Agent User."

**Step 2: Set Up the Client Project**

```bash
cd ~/projects/agentforce-agent/agentforce-project
mkdir -p client-projects/[client-name]/{design,testing,deployment-package,deliverables}
cd client-projects/[client-name]

# Create SFDX project
sf project generate --name sf-project --template standard
cd sf-project

# Authenticate client sandbox
sf org login web --alias [client-name]-sandbox

# Set as default
sf config set target-org [client-name]-sandbox
```

**Step 3: Discovery Brief to Claude Code**

```
NEW AGENTFORCE CLIENT PROJECT

CLIENT: [Company Name]
INDUSTRY: [Industry]
SALESFORCE EDITION: [Enterprise/Unlimited/Performance]
ORG ALIAS: [client-name]-sandbox
API VERSION: 64.0

BUSINESS CONTEXT: [Notes from Section A]

AGENT PURPOSE: [One sentence]
AGENT TYPE: [ExternalCopilot / InternalCopilot]
CHANNEL: [Website chat / Slack / Salesforce console]

TOPICS AND PROCESSES:

TOPIC 1: [Name]
- What it handles: [from B1]
- Data lookups: [from B2]
- Decision rules: [from B3]
- Escalation triggers: [from B4]
- Info to collect: [from B5]
- Happy path: [from B6]
- Edge cases: [from B6]
- Tone: [from B7]
- Guardrails (never do): [from B8]

[Repeat for each topic]

EXISTING SALESFORCE ASSETS:
- Custom objects: [from C1]
- Existing Flows to reuse: [from C4]
- Existing Apex to reuse: [from C5]
- Knowledge base: [from C3]

SECURITY/COMPLIANCE: [from D6]

ESCALATION: [describe what happens]

First, connect to the client's org via MCP and do:
1. Retrieve org metadata to understand the data model
2. List all custom objects, fields, relationships
3. List existing Flows and Apex classes
4. Confirm Agentforce is enabled
5. Report back what you found before building anything
```

**Step 4: Validate Org Against Discovery**

Claude Code will query the org and report back. Common discrepancies:
- Client says "we track orders in Salesforce" → no Order object, there's a custom `Purchase__c`
- Client says "we have a Flow for that" → it's broken or outdated
- Fields mentioned in discovery don't exist or are named differently
- Data messier than expected

Resolve discrepancies with the client before designing anything.

### n8n Onboarding

**Step 1: Get Access**

> "To begin work, I need the following:
>
> 1. **API credentials** for [ServiceTitan / Jobber / QuickBooks / their tool] — specifically: [API key or OAuth setup instructions]
> 2. **Access to your n8n instance** — or we'll set up a fresh self-hosted n8n (I'll guide you through this, takes ~30 min)
> 3. **Test data** — a few sample [jobs/orders/records] to test against
> 4. **Notification target** — the email address or Slack channel where alerts should go
> 5. The name and email of your **point of contact** during the build"

**Step 2: Set Up n8n Project**
```bash
# If client doesn't have n8n yet — set up self-hosted
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Document all credentials in client project folder
mkdir -p ~/projects/n8n-agent/client-projects/[client-name]/{workflows,credentials,testing,deliverables}
```

---

## STAGE 7: DESIGN (Day 2-3)

### Agentforce Design Prompt

```
Based on the client brief and org metadata retrieved, design the complete 
Agentforce agent architecture. Create a design document at:
client-projects/[client-name]/design/agent-architecture.md

Include:

1. AGENT OVERVIEW
   - Agent name, type, description
   - Target channel(s)
   - Target user persona

2. TOPIC MAP
   For each topic:
   - Topic name and API name
   - Description (what the LLM reads to decide when to route here)
   - Scope (boundaries)
   - Instructions summary
   - Actions with: name, description, target type (Apex/Flow/SOQL), 
     inputs, outputs, whether existing or new
   - Transition rules
   - Escalation criteria

3. VARIABLE MAP
   - All variables tracked across conversation turns
   - Where set / where used

4. METADATA INVENTORY
   - GenAiPlanner (agent)
   - GenAiPlugins (topics)
   - GenAiFunctions (actions)
   - GenAiPromptTemplates (if any)
   - Apex classes + test classes
   - Flows
   - Custom objects/fields (if new)
   - Permission sets

5. DEPENDENCY MAP — deployment order

6. TEST PLAN OUTLINE

Do NOT build anything yet. Design only. Client approves before build begins.
```

### n8n Design Prompt

```
Based on the client brief, design the complete n8n automation workflow.
Create a design document at:
client-projects/[client-name]/design/workflow-design.md

Include:

1. WORKFLOW OVERVIEW
   - Workflow name and purpose
   - Trigger type (webhook, schedule, manual)
   - Systems involved

2. STEP-BY-STEP FLOW
   For each step:
   - Node name and type
   - Input data
   - Processing/transformation
   - Output data
   - Error handling

3. INTEGRATION MAP
   - Each external service: auth method, API endpoints used, rate limits
   - Credential requirements

4. ERROR HANDLING PLAN
   - What happens if [service] is unavailable
   - Retry logic
   - Alert on failure: who gets notified, how

5. TEST PLAN
   - Test scenarios with sample data
   - Expected outputs

Do NOT build anything yet.
```

### Get Client Approval on Design

> "Here's the design for your [agent / automation]. Please confirm:
> 1. Are the [topics/workflow steps] correct and complete?
> 2. Do the [actions/integrations] match your actual business process?
> 3. Are the escalation/alert rules right?
> 4. Is there anything missing?
> 5. Are there any terms, product names, or phrases to use or avoid?"

Do not build until the client approves. This prevents scope creep.

---

## STAGE 8: BUILD (Day 3-7)

### Agentforce Build Prompt

```
The client has approved the architecture in:
client-projects/[client-name]/design/agent-architecture.md

Build the complete agent. API Version: 64.0
Target org: [client-name]-sandbox
Project directory: ~/projects/agentforce-agent/agentforce-project/client-projects/[client-name]/sf-project/
Deploy command: sf project deploy start --source-dir force-app --target-org [client-name]-sandbox

Follow this order:

PHASE 1 - FOUNDATION
1. Create any new custom objects or fields needed
2. Create any new permission sets needed
3. Deploy foundation metadata

PHASE 2 - ACTIONS
4. Build all Apex classes with @InvocableMethod annotation
   - Full error handling (try/catch, null checks)
   - Descriptive @InvocableVariable descriptions (LLM reads these)
   - Follow client naming conventions
5. Build all Apex test classes (90%+ coverage)
6. Build all Flows (Autolaunched only, bypass logic, Fault paths on DML)
7. Deploy all actions and run all Apex tests

PHASE 3 - AGENT
8. Create the Agent Script (.agent file):
   - All topics from architecture doc
   - All actions wired to targets
   - Conditional logic for decision rules
   - Topic transitions + variable management
   - Tone and guardrail instructions
9. Create all GenAi metadata (Planner, Plugins, Functions)
10. Create Bot and BotVersion metadata
11. Deploy everything to sandbox

PHASE 4 - VERIFICATION
12. Verify agent appears in Setup > Agentforce Agents
13. Confirm all topics and actions present in Agentforce Builder
14. Run basic smoke test via Builder preview
15. Report any issues

Save all files in client SFDX project directory.
Create deployment log at client-projects/[client-name]/deployment-log.md
```

### n8n Build Prompt

```
The client has approved the workflow design in:
client-projects/[client-name]/design/workflow-design.md

Build the complete n8n workflow.
n8n instance: [URL]
Client project directory: ~/projects/n8n-agent/client-projects/[client-name]/

PHASE 1 - CREDENTIALS
1. Set up all credentials in n8n (use credential IDs, not hardcoded keys)
2. Test each connection is live

PHASE 2 - WORKFLOW
3. Build the workflow step by step per the design doc
4. Add error handling to every node that calls an external service
5. Add error workflow that alerts [contact] via [email/Slack] on failure
6. Export workflow JSON to client-projects/[client-name]/workflows/

PHASE 3 - TESTING
7. Run with test data for each scenario in the test plan
8. Verify each step produces expected output
9. Test error scenario (what happens when [service] returns an error)

Report status of every node. Flag any deviations from design.
```

### During Build: Questions That Will Come Up

| Question | How to Answer |
|---|---|
| "The client's org doesn't have [object/field]. Should I create it?" | Check with client first. Never create objects without approval. |
| "There's an existing Flow but it doesn't have the right inputs. Modify or new?" | Usually create new. Modifying existing Flows risks breaking current processes. |
| "The client's Apex doesn't follow best practices. Should I refactor?" | No — note it for the client, don't fix what's out of scope. |
| "This action needs data from an external system." | Ask client if there's an existing integration. If not, may be out of scope. |
| "Business rule has ambiguity." | Ask the client. Never guess on business logic. |

---

## STAGE 9: TEST (Day 8-10)

### Testing Prompt (Agentforce)

```
The agent is deployed to [client-name]-sandbox. Run comprehensive tests.
For each topic:

1. HAPPY PATH TEST — most common request. Verify correct topic, action, data, response.
2. MISSING INFO TEST — request missing required info. Verify agent asks for it, doesn't fail.
3. EDGE CASE TEST — unusual or invalid data. Verify graceful handling.
4. ESCALATION TEST — request that should escalate. Verify escalation triggers.
5. OUT OF SCOPE TEST — unrelated request. Verify guardrails hold.
6. TOPIC TRANSITION TEST — start in one topic, shift to another. Verify smooth transition.
7. MULTI-TURN TEST — 4-5 message conversation. Verify context maintained.

Create test results at client-projects/[client-name]/testing/test-results.md
For any FAIL: diagnose, fix, retest.
```

### Testing Prompt (n8n)

```
The workflow is deployed. Run tests for each scenario:

1. TRIGGER TEST — fire the trigger with valid data. Verify full workflow completes.
2. MISSING DATA TEST — trigger with incomplete data. Verify error handling activates.
3. EXTERNAL SERVICE TIMEOUT — simulate API unavailability. Verify alert fires.
4. DUPLICATE TRIGGER — fire the same trigger twice. Verify no duplicate actions.
5. VOLUME TEST — run 10 triggers in sequence. Verify consistent results.

Log results at client-projects/[client-name]/testing/test-results.md
Fix any failures, retest until all pass.
```

### Client UAT

**Agentforce:**
> "The agent is ready for your testing in the sandbox. Go to Setup → Agentforce Agents → [Name] → Open in Builder → use the Conversation Preview panel to chat with the agent. Test these scenarios: [list 5-10 specific scenarios]. For each note: what you typed, what it responded, whether it was correct, anything wrong or missing."

**n8n:**
> "The automation is live. To test: [trigger the workflow via X]. Check that [expected output] appears in [location]. I'll run through it live with you on a 30-min call if helpful."

---

## STAGE 10: DEPLOY TO PRODUCTION (Day 11-12)

### Agentforce Deployment Package Prompt

```
Client UAT is complete and approved. Prepare the production deployment package.

1. Deployment package at client-projects/[client-name]/deployment-package/
   - All metadata in correct order
   - package.xml manifest
   - Pre-deployment checklist
   - Post-deployment checklist

2. Deployment guide at client-projects/[client-name]/deliverables/deployment-guide.md
   - Prerequisites
   - Exact commands
   - How to verify each step
   - How to activate the agent
   - How to connect to channel
   - Rollback instructions

3. Maintenance guide at client-projects/[client-name]/deliverables/maintenance-guide.md
   - How to modify instructions
   - How to add a topic
   - How to add an action
   - Common issues + troubleshooting
   - When to call JT Somwaru Consulting vs. handle internally

4. Project summary at client-projects/[client-name]/deliverables/project-summary.md
   - What was built, key metrics to track, next steps
```

### Deployment Options

**Option A: Client deploys themselves** — Hand them the package + guide. Their admin runs it. You're available on call.
**Option B: You deploy for them** — Client gives you temporary production access. You deploy, verify, activate, then remove your access.
**Option C: CI/CD pipeline** — Push to their GitHub/Bitbucket. Their pipeline handles promotion. (Enterprise clients only)

### Post-Deployment Checklist (send to client)

> 1. Setup → Agentforce Agents → [Name] → Activate
> 2. Assign "Einstein Agent User" permission set to agent's running user
> 3. [Website]: Add Embedded Messaging snippet to your site
> 4. [Slack]: Connect agent in Slack administration
> 5. Test one real conversation to confirm it works
> 6. Monitor the first 24 hours
> 7. Check Agentforce Analytics after 1 week

---

## STAGE 11: POST-LAUNCH SUPPORT

### The Handoff Meeting (30 minutes)

Cover:
1. How to access Agentforce Analytics / n8n execution logs
2. How to read conversation/execution logs
3. Metrics to watch (resolution rate, escalation rate, execution success rate)
4. How to make simple changes
5. When to call JT Somwaru Consulting vs. handle internally

### Upsell Signals

| Signal | Upsell |
|---|---|
| "The agent is great for service — could we do sales?" | New agent for sales team |
| "We're getting questions the agent can't handle" | Add new topic to existing agent |
| "Can it also update records / send emails / create tasks?" | Add new actions |
| "We want this on website AND Slack" | Multi-channel deployment |
| "Another department wants one" | Second agent engagement |
| "Can we get reports on performance?" | Analytics dashboard |
| "The automation is working — can we do [next workflow]?" | Phase 2 n8n engagement → eventual Agentforce upsell as they grow |

### Retainer Model

| Tier | Monthly | Includes |
|------|---------|----------|
| Basic | $750/mo | 2 hours support, bug fixes, minor tweaks |
| Standard | $2,000/mo | 5 hours, monthly optimization review, one topic/action or workflow addition/mo |
| Premium | $4,000/mo | 10 hours, weekly optimization, unlimited minor changes, priority response |

*(Rates reflect NYC consulting market; adjust down for smaller clients, up for enterprise)*

---

## CLIENT FAQ RESPONSES

### Before They Buy

| Question | Your Answer |
|---|---|
| "How is this different from a chatbot?" | "Chatbots follow scripts. Agentforce agents reason, look up real data in your Salesforce, take actions, and make decisions based on your business rules. It's the difference between a phone tree and an actual employee." |
| "Will it replace our support team?" | "No — it handles the repetitive stuff so your team can focus on complex issues. Think of it as a new team member that handles Tier 1 and escalates Tier 2+ to your humans." |
| "What if the agent says something wrong?" | "We build guardrails into every agent — things it cannot say or do. We test extensively before launch. You can monitor every conversation in real-time." |
| "How much does Agentforce cost from Salesforce?" | "About $0.10 per action via Flex Credits. A typical conversation uses 3-5 actions — roughly $0.30-0.50 per conversation vs. $5-15 for a human-handled interaction." |
| "How long until ROI?" | "Most clients see measurable impact within the first month — reduced response times, fewer escalations, team time freed for higher-value work." |
| "Can we try it before committing?" | "Yes — I build and test everything in a sandbox first. You interact with the agent and approve it before it goes anywhere near production." |
| "We're not on Salesforce — can you still help?" | "Yes, through n8n automation. I can automate your [ServiceTitan/Jobber/QuickBooks] workflows without requiring Salesforce. Different tool, same outcome: less manual work." |

### During the Build

| Question | Your Answer |
|---|---|
| "Can the agent access [external system]?" | "If there's an API or existing Salesforce integration, yes. If not, we can build one, but that's additional scope." |
| "Can we change things after launch?" | "Absolutely. Instructions, topics, and actions can all be updated. I'll provide a maintenance guide and training." |
| "What happens if Salesforce is down?" | "The agent runs on Salesforce infrastructure — same uptime SLA as your CRM. Salesforce's SLA covers it." |
| "Who owns the code/metadata you create?" | "You do. Everything is deployed directly into your Salesforce org or your n8n instance. You own all of it." |

---

## COMPLETE PROMPT TEMPLATES (Quick Reference)

### Template: New Agentforce Client Kickoff

```
NEW AGENTFORCE CLIENT PROJECT

CLIENT: [Company Name]
INDUSTRY: [Industry]
SALESFORCE EDITION: [Enterprise/Unlimited/Performance]
ORG ALIAS: [client-name]-sandbox
API VERSION: 64.0
PROJECT DIR: ~/projects/agentforce-agent/agentforce-project/client-projects/[client-name]/

Step 1: Create project structure
Step 2: Initialize SFDX project in sf-project/
Step 3: Connect to client org (alias already authenticated)
Step 4: Org discovery — retrieve all custom objects, Flows, Apex classes, 
        existing Agentforce agents, Permission Sets, edition/licenses
        Save to design/org-discovery.md
Step 5: Report back findings
```

### Template: New n8n Client Kickoff

```
NEW N8N AUTOMATION PROJECT

CLIENT: [Company Name]
INDUSTRY: [Industry]
TOOLS THEY USE: [ServiceTitan / Jobber / QuickBooks / etc.]
PROJECT DIR: ~/projects/n8n-agent/client-projects/[client-name]/

Step 1: Create project structure (workflows/, credentials/, testing/, deliverables/)
Step 2: Test connectivity to client's tools (API key provided: [Y/N])
Step 3: Discovery — what API endpoints are available for [their tools]
        What data can we read/write?
        What webhooks are available?
        Save to design/api-discovery.md
Step 4: Report back what's possible vs. what was scoped
```

### Template: Agent Build (After Design Approval)

```
BUILD AGENTFORCE AGENT FOR [CLIENT NAME]

Approved architecture: client-projects/[client-name]/design/agent-architecture.md
Target org: [client-name]-sandbox
API version: 64.0
Deploy command: sf project deploy start --source-dir force-app --target-org [client-name]-sandbox

Agent Name: [Name]
Agent Type: [ExternalCopilot / InternalCopilot]
Agent Tone: [Formal / Friendly / Technical]

TOPIC 1: [Name]
Description for LLM: "[...]"
Scope: "[...]"
Instructions: [bullet list]
NEVER: [guardrails]
Escalation: If [trigger], [action]

Actions:
1. [Action Name] — Type: [Apex/Flow] — Inputs: [...] — Outputs: [...]
2. [...]

[Repeat for each topic]

GLOBAL GUARDRAILS: [list]
ESCALATION RULES: [list]
VARIABLES: [list with where set/used]

Build, deploy, run Apex tests, verify in Agentforce Builder. Report every component deployed.
```

### Template: n8n Workflow Build

```
BUILD N8N WORKFLOW FOR [CLIENT NAME]

Approved design: client-projects/[client-name]/design/workflow-design.md
n8n instance: [URL]

Workflow Name: [Name]
Trigger: [webhook / cron / manual]
Systems: [list]

WORKFLOW STEPS:
1. [Trigger node] — [what it receives]
2. [Transform/filter] — [what it does]
3. [API call to X] — [endpoint, inputs, outputs]
4. [Conditional logic] — if [condition], then [action], else [action]
5. [Output — email/Slack/update record]

ERROR HANDLING:
- On any node failure: send alert to [contact] via [method]
- Retry logic: [X] retries with [Y] second delay

Export workflow JSON to workflows/ directory.
Test with provided sample data. Report all node results.
```

### Template: Testing

```
TEST [AGENTFORCE AGENT / N8N WORKFLOW] FOR [CLIENT NAME]

Run all 7 test types (happy path, missing info, edge case, escalation, 
out of scope, transition, multi-turn).

Test results: client-projects/[client-name]/testing/test-results.md
Format: Test ID | Description | Input | Expected | Actual | PASS/FAIL | Notes

Fix all failures, retest until all pass.
```

---

## PRICING QUICK REFERENCE

### Agentforce Projects

| Engagement Type | Price | Timeline |
|---|---|---|
| Single-topic agent | $2,500–$5,000 | 1 week |
| Multi-topic agent (3-5 topics) | $7,500–$15,000 | 2-3 weeks |
| Multi-agent ecosystem | $20,000–$50,000 | 4-8 weeks |
| Agent audit/assessment | $1,500–$3,000 | 2-3 days |

### n8n Projects

| Engagement Type | Price | Timeline |
|---|---|---|
| Single workflow automation | $1,500–$3,500 | 3-5 days |
| Multi-workflow system (3-5 workflows) | $5,000–$10,000 | 1-2 weeks |
| Full ops automation package | $12,000–$25,000 | 3-5 weeks |
| Workflow audit/optimization | $750–$1,500 | 1-2 days |

### Ongoing Retainers (both tracks)

| Tier | Monthly | Includes |
|------|---------|----------|
| Basic | $750/mo | 2 hrs support, bug fixes |
| Standard | $2,000/mo | 5 hrs, monthly review, 1 addition/mo |
| Premium | $4,000/mo | 10 hrs, weekly review, unlimited minor changes |

---

## YOUR COMPETITIVE EDGE

1. **Discovery call → working agent/automation in days, not weeks** — traditional consultants take months
2. **Two-track delivery** — you can serve companies whether or not they're on Salesforce
3. **Aya as reference client** — live construction/co-living client for n8n track; real PM client for Agentforce track
4. **Agent-assisted preparation** — 30-min pre-call briefing means you walk in knowing their industry pain points cold
5. **Automated testing and documentation** — Claude Code runs test suites and generates deliverables that consultants do manually
6. **Templates and patterns** — not starting from scratch each time; every engagement makes the next one faster
7. **Upsell path built in** — n8n clients naturally grow into Agentforce clients as they scale onto Salesforce

The client doesn't need to know you use Claude Code or n8n agents internally. They see fast delivery, high quality, and competitive pricing.
