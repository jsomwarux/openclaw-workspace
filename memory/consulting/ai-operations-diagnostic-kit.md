# AI Operations Diagnostic Kit

## Purpose
Reusable delivery kit for converting warm leads into a paid diagnostic before selling a larger AI implementation build.

## Intake Questions
### Business context
1. What business outcome made you start looking at AI now?
2. Which team feels the operational pain most directly?
3. Who owns the workflow today?
4. What happens if this workflow fails, ages, or gets missed?
5. What systems are involved today?

### Workflow mapping
1. What starts the workflow?
2. What information is required to complete it?
3. Where does the work wait for a person?
4. Where does data get copied manually?
5. What are the common exceptions?
6. What gets escalated to leadership?
7. What approvals are required?
8. What must never happen automatically?

### Tool/data readiness
1. Which systems have API/export access?
2. Which systems are local-only or desktop-based?
3. Where are documents stored?
4. What reports are manually generated?
5. What data is sensitive and should stay local/private?

## Workflow Scoring Matrix
Score each candidate 1–5.

| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| Frequency | Rare | Weekly | Daily/high-volume |
| Time drain | <1 hr/week | 2–5 hrs/week | 10+ hrs/week |
| Business impact | Nice-to-have | Owner-visible | Revenue/risk/compliance impact |
| Data readiness | Messy/no access | Partial exports | Clear source/API/export |
| Automation risk | High judgment | Some review | Rules + human approval enough |
| Implementation complexity | Many systems | 2–3 systems | One clear workflow |
| Proof value | Internal only | Useful proof | Strong case-study/referral value |

## Recommendation Logic
- **Build first:** high frequency, high visibility, low/medium risk, clear owner, usable data.
- **Defer:** high complexity, unclear owner, dirty data, too much judgment.
- **Do not automate:** low frequency, low impact, or sensitive decision without review path.

## Diagnostic Output Template
1. Executive summary
2. Current-state workflow map
3. Top bottlenecks
4. Exception inventory
5. Ranked use cases
6. Recommended first build
7. Human-in-loop design
8. Risks/dependencies
9. Implementation timeline
10. Proposal / next step

## Reusable First-Build Categories
- Exception dashboard
- Document/intake classifier
- Local-first reporting workflow
- Vendor/document tracker
- Owner-ready weekly brief
- CRM/Salesforce AI agent
- n8n/Python workflow automation
