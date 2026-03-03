---
description: Document a client's current business process — SOP with RACI, flowchart, and edge cases
argument-hint: "<process name or description>"
---

# /process-doc

Document a client's existing workflow as a complete SOP before automating it.
This is the foundation step for any automation engagement — you cannot build what you don't understand.

## Usage

```
/process-doc $ARGUMENTS
```

Walk me through the process or paste existing docs. I'll structure it completely.

## Output

```markdown
## Process Document: [Process Name]
**Client:** [Company] | **Owner:** [Person/Team] | **Last Updated:** [Date]
**Automation Readiness:** [High / Medium / Low] | **Est. Time to Automate:** [X weeks]

### Purpose
[Why this process exists and what it accomplishes]

### Scope
**Included:** [What's in scope]
**Excluded:** [What's out of scope — important for automation boundaries]

### RACI Matrix
| Step | Responsible | Accountable | Consulted | Informed |
|------|------------|-------------|-----------|----------|
| [Step] | [Who does it] | [Who owns outcome] | [Who to ask] | [Who to notify] |

### Process Flow
```
[Step 1] → [Step 2] → [Decision: X?]
                              ↓ Yes          ↓ No
                         [Step 3a]       [Step 3b]
                              ↓
                         [Step 4] → [End]
```

### Detailed Steps

#### Step 1: [Name]
- **Who**: [Role]
- **When**: [Trigger or timing]
- **How**: [Exact actions — be specific, name the tools]
- **Output**: [What this step produces]
- **Time**: [How long it takes]

#### Step 2: [Name]
[Same format]

### Exceptions and Edge Cases
| Scenario | Frequency | Current Handling | Automation Risk |
|----------|-----------|-----------------|-----------------|
| [Exception] | [Daily/Weekly/Rare] | [What they do] | [High/Low] |

### Automation Opportunity Map
| Step | Can Automate? | How | Tool |
|------|--------------|-----|------|
| [Step] | Yes/Partial/No | [Method] | [n8n / Agentforce / Script] |

### Metrics (current state baseline)
| Metric | Current | Target After Automation |
|--------|---------|------------------------|
| Time per cycle | [X hrs] | [Y hrs] |
| Error rate | [X%] | [Y%] |
| Cost per cycle | [$X] | [$Y] |
```

## Tips

1. **Document current state, not ideal state.** What they *actually* do, including the workarounds.
2. **Exceptions are gold.** "Usually we do X, but sometimes Y" — that's what breaks automations.
3. **Name the bottleneck.** Which step has the longest wait time or most errors?
4. **Automation readiness check:** Any step with "copy from [tool A] to [tool B]" manually = automate first.
