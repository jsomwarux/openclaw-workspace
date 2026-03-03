---
description: Evaluate a client's existing tech stack for automation readiness and integration potential
argument-hint: "<company name or tool list>"
---

# /vendor-eval

Assess a client's current tools and tech stack. Identifies automation opportunities, integration
risks, and vendor lock-in. Used during intake or before scoping an automation project.

## Usage

```
/vendor-eval $ARGUMENTS
```

Provide the client's tool list or describe their stack. I'll score it and map the opportunities.

## Output

```markdown
## Tech Stack Evaluation: [Company Name]
**Date:** [Date] | **Niche:** [Industry]

### Stack Inventory

| Tool | Category | How They Use It | API? | Webhook? | Data Export? | Automation Potential |
|------|----------|----------------|------|----------|-------------|---------------------|
| [Tool] | [CRM/PM/Accounting/etc] | [What for] | ✅/❌ | ✅/❌ | CSV/Excel/None | High/Med/Low |

### Automation Readiness Score: [X/10]

**Score breakdown:**
- Integration depth (APIs + webhooks available): [X/4]
- Data accessibility (can we get data out easily): [X/3]
- Process maturity (documented, consistent processes): [X/2]
- Team tech comfort (will they maintain it): [X/1]

### Top Automation Opportunities

#### Opportunity 1: [Name] — Est. ROI: [X hrs/wk or $X/mo]
**Current state:** [Manual process description]
**Automation:** [What we'd build]
**Tools involved:** [n8n + Tool A + Tool B]
**Complexity:** Low / Medium / High | **Timeline:** [X weeks]

#### Opportunity 2: [Name]
[Same format]

### Integration Risks

| Risk | Tool | Severity | Mitigation |
|------|------|----------|-----------|
| No API — export only | [Tool] | Medium | Schedule automated CSV import |
| Vendor lock-in | [Tool] | High | Build data mirror in Google Sheets |
| API rate limits | [Tool] | Low | Add delay/batching in n8n |

### Gaps — Tools They're Missing

| Gap | Impact | Recommended Tool | Cost |
|-----|--------|-----------------|------|
| No CRM | Can't automate follow-ups | HubSpot (free tier) | Free |
| No webhook receiver | Manual trigger only | n8n | Self-hosted |

### Recommended Implementation Sequence
1. [Quick win first — lowest effort, highest visibility]
2. [Foundation piece — enables everything else]
3. [Expansion phase — after client trust is established]
```

## Tips

1. **"CSV export only" = biggest opportunity.** That's a manual data transfer we can automate.
2. **Check API docs before promising anything.** Some tools have APIs that are read-only or rate-limited to uselessness.
3. **Vendor lock-in is a selling point for us.** If they're locked into a tool with bad integrations, they need help getting data out — that's a contract.
4. **Score honestly.** A low automation-readiness score is a larger engagement, not a disqualifier.
