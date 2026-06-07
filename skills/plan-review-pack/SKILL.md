---
name: plan-review-pack
description: "Use when an internal plan, spec, agent workflow, or client deliverable needs a human-readable review artifact for JT, a client, collaborator, or proof loop."
---

# Plan Review Pack

Use this to translate agent-native plans into reviewable human artifacts.

## Core Rule
`plan.md` is for agents. A review pack is for people.

The pack should make a normal client/collaborator able to understand, comment on, accept, or redirect the work without reading terminal-native markdown, raw transcripts, or implementation logs.

## Inputs
- internal plan/spec/runbook
- raw transcript or notes, if relevant
- target workflow or deliverable
- acceptance criteria
- known risks, open questions, and decision points
- proof evidence, screenshots, demo clips, or run logs when available

## Output Structure
Create a concise Markdown artifact unless a Drive/Proof-style share link is explicitly required.

1. Objective: what the work is meant to accomplish.
2. Current understanding: workflow, users, systems, constraints.
3. Scope: in / out / assumptions.
4. Proposed plan: steps in plain English.
5. Review points: exact questions where human signal is needed.
6. Acceptance criteria: what must be true before this is done.
7. Risks and boundaries: privacy, approvals, external actions, finance, rollback.
8. Proof assets: screenshots, demo video/GIF, logs, redacted samples, or explicit `not available yet`.
9. Comment-back loop: where comments should be captured and what file/task gets updated next.

## Human-As-Signal Loop
Ask reviewers for judgment, not generic approval:
- Which option is closest?
- What language/risk/constraint is wrong?
- What edge case is missing?
- What is good enough to ship?
- What must not happen?

Then update the source plan, Client OS, or task with the resolved decision. Do not leave feedback only in chat.

## Client Rules
- Use redacted, anonymized, or synthetic data unless JT has explicit permission.
- Keep raw transcripts and sensitive files out of the review pack unless the reviewer is authorized to see them.
- If client acceptance is needed, link or update the Client OS `acceptance-checklist.md`.

## Done State
Return:
- review pack path/link
- reviewer
- open review questions
- source artifact updated
- next action and owner
