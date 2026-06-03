# JT Toolkit Synthesis — 2026-06-02

## Scope
Compared `https://github.com/jsomwarux/jt-claude-toolkit` against the current OpenClaw workspace skills, Codex plugin, agents, Mission Control registry, and project instruction files.

## Claude Toolkit Wins
- Cleaner packaging model: two bounded plugins, `consulting-toolkit` and `product-builder`, instead of one giant operating prompt.
- Better separation of workflow design versus workflow build: `workflow-strategist` designs and `n8n-builder` implements.
- Useful missing deliverable surface: `proposal-pdf` with fixed visual tokens and pricing reconciliation.
- Strong quality language: the product `quality-pass` agent explicitly checks for AI slop, fake implementation, and LARP code.
- Thin project template idea is right: reusable process belongs in skills/plugins; project files should hold only local stack, paths, constraints, and commands.

## OpenClaw/Eve Wins
- Much deeper JT fit: non-developer positioning, consulting cash priority, NYC/remote constraint, proof/IP flywheel, Mission Control, health/cost/crypto/job-market systems, and current client/prospect state.
- Stronger consulting routing: T1/T2/T3 scoring, verified-contact gate, no-send boundaries, Drive sync, proof logging, and Mission Control next-action discipline.
- Stronger client delivery OS: Client OS templates, acceptance checklists, reusable IP/failure logs, weekly/quarterly account owner rhythms.
- Stronger privacy and proof safety: client proof defaults private; public claims require permission or anonymization.
- Better live automation: crons, scripts, proof guards, task board, daily/weekly memory, and agent registry already exist.

## Final Architecture
- **Skills:** reusable judgment workflows that should load during normal work.
- **Agents:** recurring/stateful roles or fresh delegated roles with owned artifacts.
- **Plugins:** portable bundles of stable skills for use outside this workspace.
- **AGENTS.md / CLAUDE.md:** thin project-local facts, constraints, commands, lessons, and safety rules.

## Adopted Changes
- Added workspace skills:
  - `skills/n8n-blueprint/SKILL.md`
  - `skills/proposal-pdf/SKILL.md`
  - `skills/product-build-loop/SKILL.md`
- Added workspace agents:
  - `agents/workflow-strategist/AGENT.md`
  - `agents/product-quality-pass/AGENT.md`
- Expanded portable Codex plugin:
  - `~/plugins/jt-operating-system/skills/n8n-blueprint/`
  - `~/plugins/jt-operating-system/skills/proposal-pdf/`
  - `~/plugins/jt-operating-system/skills/product-build-loop/`
- Updated routing docs and global Claude context to reflect the better split.

## Keep Out
- Do not import Claude's `resume-tailor` as-is. The workspace `job-application` skill and Drive upload rule are stricter and more accurate for JT.
- Do not import Claude's generic `new-client` command as-is. The OpenClaw pipeline has stronger preflight, tier routing, duplicate checks, verified-contact gates, Drive sync, and JT send boundaries.
- Do not use Claude's auto prettier hook globally. It is convenient, but too blunt across JT's mixed repos and can churn files silently.
- Do not turn every vertical into a plugin. Verticals are context until a repeatable paid pattern proves itself.
