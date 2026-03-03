---
description: Create a runbook for an n8n workflow or automation built for a client
argument-hint: "<workflow name or description>"
---

# /runbook

Create a step-by-step operational runbook for an n8n automation, Agentforce flow, or any
recurring automated process we've built for a client. Runbooks are for handoffs, maintenance,
and troubleshooting — written for someone who didn't build the system.

## Usage

```
/runbook $ARGUMENTS
```

Describe the automation or walk me through what it does. I'll structure it as a maintainable runbook.

## Output

```markdown
## Runbook: [Automation Name]
**Client:** [Company] | **Built By:** Eve/JT | **Date:** [Date]
**Frequency:** [Triggered by X / Runs every Y / Manual]
**n8n Workflow ID:** [ID or URL if available]

### Purpose
[What this automation does and why it exists]

### Architecture Overview
```
[Trigger] → [Step 1] → [Step 2] → [Output/Destination]
```
**Tools involved:** [n8n / Agentforce / Google Sheets / etc.]

### Prerequisites
- [ ] [API key or credential needed — where to find it]
- [ ] [Access permission required]
- [ ] [Data format or input requirement]

### How to Run (if manual trigger)

#### Step 1: [Name]
```
[Exact action: e.g., "Open n8n at http://[client-url]:5678, find workflow '[Name]', click Execute"]
```
**Expected result:** [What should happen]
**If it fails:** [What to check first]

#### Step 2: [Name]
[Same format]

### Monitoring

**Where to check:** [n8n execution log / Slack alert / Google Sheet output]
**Success signal:** [What "it worked" looks like]
**Failure signal:** [What "it failed" looks like — error message or missing output]

### Troubleshooting
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| [What you see] | [Why it happens] | [Exact fix] |
| Workflow not triggering | Webhook URL changed | Re-register webhook in [tool] |
| API rate limit error | Too many runs | Add [X] second delay between items |

### Maintenance
| Task | Frequency | Who |
|------|-----------|-----|
| Check execution log for errors | Weekly | Client / JT |
| Rotate API key | [Per vendor policy] | JT |
| Review output quality | Monthly | Client |

### Rollback
[How to pause or disable the automation if something breaks]
1. Open n8n → find workflow → toggle Active OFF
2. [Any manual cleanup needed]

### Contact
**If automation breaks:** [JT contact method]
**Response time:** [SLA if applicable]
```

## Tips

1. **Be painfully specific.** "Run the workflow" is not a step. "Open n8n at [URL], find '[Name]', click Execute" is.
2. **Include the failure path.** Every step needs "if it fails, do X."
3. **Screenshot the expected output.** If the client can see what success looks like, they can self-diagnose.
4. **Credential hygiene.** Note where every API key lives and when it expires.
