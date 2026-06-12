# JT Consulting Pipeline — Claude Instructions

## Purpose
This repo is JT's consulting pipeline: prospect research, client folders, outreach drafts, delivery notes, proof capture, and reusable consulting IP.

## Read First
- `~/.openclaw/workspace/MEMORY.md` for active client status.
- `~/.openclaw/workspace/docs/agents/capability-routing-map.md` for skill/plugin/agent routing.
- `~/.openclaw/workspace/skills/opticfy-pipeline/SKILL.md` for prospect/outreach pipeline work.
- `~/.openclaw/workspace/skills/opticfy-ops/SKILL.md` for active client delivery.
- `~/.openclaw/workspace/skills/ai-context-os/SKILL.md` when client knowledge, SOPs, rules, examples, or edge cases need to become agent-ready context and evals.
- `~/.openclaw/workspace/skills/client-proof-capture/SKILL.md` whenever deliverables become proof, content, referral, or portfolio material.

## Hard Rules
- JT always sends outreach. Draft only.
- Client proof is private by default. Public naming requires explicit permission; otherwise use redacted, anonymized, or synthetic examples.
- Active clients need a Client OS copied from `~/.openclaw/workspace/skills/opticfy-ops/templates/client-os/`.
- Do not claim a workflow is accepted, paid, live, or proof-safe without local evidence.
- Do not put secrets, credentials, or private client data into shareable files.
- Prospect tiers are score-gated: T1 = 80+ proof-led custom, T2 = 60-79 template/validation, T3 = 40-59 market-sensing only. Warm intro or a specific hook never automatically makes T1.

## Workflow Routing
- New prospect or research packet: use `opticfy-pipeline`.
- Active/signed client delivery: use `opticfy-ops`.
- Context/knowledge readiness sprint: use `ai-context-os`.
- Accepted deliverable or proof opportunity: use `client-proof-capture`.
- LinkedIn/social proof extraction: use `linkedin-corpus` plus `content-generation`.
- Portfolio update candidate: use `portfolio-card` after proof gates pass.

## Done Means
- The relevant client/prospect file is updated.
- Any Mission Control task has a concrete first action, why it matters, and done state.
- Proof-sensitive work states whether it is blocked, private-ready, or publish-ready.
- Drive sync is run for substantive review artifacts when required.
