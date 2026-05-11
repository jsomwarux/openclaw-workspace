# AI Ops Teardowns — Content Templates

## X Template
[Company/category] probably does not need another chatbot.

The first AI workflow I would build is [workflow].

Inputs:
- [input 1]
- [input 2]
- [input 3]

Flow:
1. [step]
2. [step]
3. [step]
4. human approves the risky part
5. everything gets logged

AI is most useful as the exception layer.

## LinkedIn Template
Most AI implementations start in the wrong place.

If I were building AI ops for [company/category], I would not start with a chatbot.

I would start with [workflow].

The current process probably looks something like this:
- [manual process]
- [handoff/problem]
- [missed deadline/stale info]
- [owner has no visibility]

The workflow I would build:
1. [input ingestion]
2. [classification/extraction]
3. [exception detection]
4. [draft/action preparation]
5. [human approval]
6. [audit log / weekly summary]

The important part is not that AI writes something.

The important part is that the business knows what is stuck, who owns it, what changed, and what needs approval.

That is where AI implementation actually starts.

## Workflow Map Template
# [Title]

## Business Context

## Current Manual Process

## Failure Modes

## Proposed AI Ops Workflow
| Step | Input | System action | Human boundary | Output |
|---|---|---|---|---|

## n8n Node Sketch
1. Trigger:
2. Data source:
3. Clean/normalize:
4. AI extraction/classification:
5. Rules/thresholds:
6. Approval queue:
7. Notification:
8. Audit log:
9. Error handling:

## Why This Is Reusable

## Content Hook
