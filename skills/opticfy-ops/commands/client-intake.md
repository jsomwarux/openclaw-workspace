---
description: Run a structured discovery session and produce a client brief + engagement scope
argument-hint: "<company name or prospect description>"
---

# /client-intake

Initial discovery workflow for a new prospect or client. Produces a structured brief,
identifies the highest-value automation opportunity, and outputs an engagement proposal outline.

## Usage

```
/client-intake $ARGUMENTS
```

Provide: company name, niche, and any research already gathered. I'll ask the right questions
if context is missing.

## Output

```markdown
## Client Brief: [Company Name]
**Date:** [Date] | **Contact:** [Name, Title] | **Niche:** [Industry]

### Company Overview
[3-4 sentences: what they do, size, location, key operations]

### Current Pain Points
| Pain Point | Estimated Impact | Priority |
|------------|-----------------|----------|
| [Problem] | [$X or X hrs/wk] | High/Med/Low |

### Tech Stack
| Tool | Purpose | Integration Potential |
|------|---------|----------------------|
| [Tool] | [What it's used for] | [API / Export only / Manual] |

### Highest-Value Automation Opportunity
[2-3 sentences: what to automate, why, estimated ROI]

### Proposed Engagement
**Service:** [e.g., Data Anomaly Audit / n8n Workflow / Dashboard]
**Scope:** [What's included and excluded]
**Timeline:** [Delivery estimate]
**Price:** $[X] — [payment terms]

### Quick Wins (deliverable within 2 weeks)
1. [Quick win #1 with measurable outcome]
2. [Quick win #2]

### Expansion Path
[What larger engagement this leads to — $X project after initial win]

### Open Questions
- [ ] [What we still need to confirm before scoping]
```

## If Client Folder Exists

Check `~/projects/jt-consulting-pipeline/clients/[slug]/research.md` first.
Use existing research as the basis — don't repeat work already done.

## Tips

1. **Lead with the pain, not the solution.** Find what's costing them money or time *today*.
2. **Tech stack matters more than company size.** A tool with no API = a manual process we can automate.
3. **Always identify the expansion path.** The $500 audit should lead to a $3,000 automation contract.
4. **Name the ROI.** "Save 5 hours/week" > "streamline your workflow."
