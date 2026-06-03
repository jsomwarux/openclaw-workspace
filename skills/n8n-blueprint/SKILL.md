---
name: n8n-blueprint
description: "Design an airtight n8n workflow blueprint before a builder creates nodes. Use for client automations, webhook/cron/Gmail workflows, node-by-node specs, JSON contracts, error handling, test payloads, and single-LLM versus ensemble decisions."
---

# n8n Blueprint

Use this to design the workflow. Do not build nodes in the same pass unless JT explicitly asks for implementation after approving the blueprint.

## Read First
- Project lessons: `~/projects/n8n-agent/tasks/lessons.md`
- Build protocols: `docs/agents/workflow-protocols.md`
- Client context: `~/projects/jt-consulting-pipeline/clients/[slug]/brief.json`, `research.md`, `analysis.md`, and Client OS files when present

## Required Output
```markdown
# Workflow: [name]

## Trigger
[Webhook, cron, Gmail Trigger, manual. Include exact schedule/path/event.]

## Node-by-Node Spec
Node 1 - [name] ([n8n node type])
- Purpose:
- Config:
- Input:
- Output:
- Failure path:

## Data Contracts
[Exact JSON request/response shape for every LLM, webhook, HTTP, sheet, or database step.]

## Error Handling
[Per node: failure mode, fallback, log target, alert owner, retry/stop rule.]

## Test Payloads
[Happy path plus edge cases, no-result path, malformed input, duplicate input.]

## Model Architecture
[Single LLM or multi-LLM ensemble. Include cost/accuracy tradeoff and final recommendation.]

## Build Handoff
[What the builder can implement now, what is blocked, what client access/data is still needed.]
```

## JT-Specific Rules
- Query n8n MCP/node docs before specifying unfamiliar node fields.
- Prefer single LLM for deterministic extraction, routing, formatting, and simple classification.
- Use a 4-LLM cross-examination ensemble only when auditability or qualitative risk justifies the cost.
- For Anthropic HTTP nodes: POST `/v1/messages`, set `max_tokens`, parse `content[0].text`, and require JSON-only output when downstream nodes parse it.
- Production n8n on Windows stays native Node + NSSM. Never recommend WSL2/Docker for that environment.
- Preserve `.n8n` and encryption keys before any migration.
- Read File nodes under NSSM may be restricted to `C:\WINDOWS\system32\config\systemprofile\.n8n-files`.
- Gmail Trigger version mismatch may require manually recreating the node in target n8n.

## Quality Gate
- No ambiguous node names, field values, data shapes, or branch behavior.
- Every branch has a test payload.
- Every sensitive or external action has a human-review, rollback, or alert boundary.
- The builder can implement without making design decisions.
