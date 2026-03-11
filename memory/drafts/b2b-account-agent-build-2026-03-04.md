# B2B Account Service Agent — Build Summary
**Date:** 2026-03-04
**Purpose:** Salesforce Lead Agentforce SE interview demo

## Files Created

### Apex Classes (16 files)
- `force-app/main/default/classes/AccountHealthLookupAction.cls`
- `force-app/main/default/classes/AccountHealthLookupAction.cls-meta.xml`
- `force-app/main/default/classes/AccountHealthLookupActionTest.cls`
- `force-app/main/default/classes/AccountHealthLookupActionTest.cls-meta.xml`
- `force-app/main/default/classes/CaseCreationAction.cls`
- `force-app/main/default/classes/CaseCreationAction.cls-meta.xml`
- `force-app/main/default/classes/CaseCreationActionTest.cls`
- `force-app/main/default/classes/CaseCreationActionTest.cls-meta.xml`
- `force-app/main/default/classes/OpportunityStatusAction.cls`
- `force-app/main/default/classes/OpportunityStatusAction.cls-meta.xml`
- `force-app/main/default/classes/OpportunityStatusActionTest.cls`
- `force-app/main/default/classes/OpportunityStatusActionTest.cls-meta.xml`
- `force-app/main/default/classes/ActivityCreationAction.cls`
- `force-app/main/default/classes/ActivityCreationAction.cls-meta.xml`
- `force-app/main/default/classes/ActivityCreationActionTest.cls`
- `force-app/main/default/classes/ActivityCreationActionTest.cls-meta.xml`

### GenAI Function XMLs (4 files)
- `force-app/main/default/genAiFunctions/Account_Health_Lookup/Account_Health_Lookup.genAiFunction-meta.xml`
- `force-app/main/default/genAiFunctions/Create_Support_Case/Create_Support_Case.genAiFunction-meta.xml`
- `force-app/main/default/genAiFunctions/Opportunity_Status_Lookup/Opportunity_Status_Lookup.genAiFunction-meta.xml`
- `force-app/main/default/genAiFunctions/Create_Activity/Create_Activity.genAiFunction-meta.xml`

### AgentScript YAMLs (2 files)
- `force-app/main/default/aiAuthoringBundles/B2B_Account_Service_Agent/InternalUserVerificationGate.yaml`
- `force-app/main/default/aiAuthoringBundles/B2B_Account_Service_Agent/CaseSeverityRouter.yaml`

**Total: 22 files**

## Demo Walkthrough (5 min)
1. **Account Health Check** — Ask about Meridian Partners → returns Green health (9/10), open $420K opp, CFO contact
2. **Critical Case Creation** — "Acme Corp API integration is completely down" → P1, auto-escalated, SLA 1 hour
3. **Opportunity Status** — Ask about TechStar renewal → stage, close date, exec call next step
4. **Activity Scheduling** — Schedule executive demo for Apex Solutions → ACT-[id], 3 days out

## AgentScript Differentiator
Two AgentScript files demonstrate deterministic routing — the interview differentiator. Point to:
- InternalUserVerificationGate: shows compliance-first design
- CaseSeverityRouter: shows deterministic P1 escalation bypassing LLM judgment

## Before Demo Checklist
- [ ] Deploy to scratch org: sf project deploy start --source-dir force-app --target-org agentforce-demo
- [ ] Verify all 4 topics route correctly in agent preview
- [ ] Test P1 escalation path with "system down" description
- [ ] Load demo script (this file)

## Known Limitations
- All data is mocked — no live SOQL queries (appropriate for demo environment without full data model)
- AgentScript YAML is Spring 26 spec — verify format with latest Salesforce docs before demo
- ActivityCreationAction scheduledDate uses +3 calendar days, not business days (acceptable for demo)
- **Bot definition directory not created** (`bots/B2B_Account_Service_Agent/` missing) — the bot meta.xml and botVersion-meta.xml are needed for deployment. Copy the Ecommerce_Service_Agent directory structure as a reference and update for B2B topics. Apex actions and GenAI functions are ready; bot wiring is the missing step before `sf project deploy` will wire topics.
