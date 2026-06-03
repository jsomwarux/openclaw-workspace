# JT Capability Routing Map
Generated: 2026-05-31

This is the operating split for what JT does and where each repeatable pattern belongs.

## Routing Rule
- **Skill:** repeatable judgment workflow that should load inside normal work.
- **Agent:** recurring or stateful operator with a queue, cadence, or owned artifact.
- **Plugin:** portable bundle of tools/skills/assets worth installing or sharing as a unit.
- **CLAUDE.md / AGENTS.md:** project-local rules, hard constraints, commands, and “read this before changing files” guidance.

## Current Work Lanes

### Consulting Revenue
- **What JT does:** sells and delivers practical AI implementation for ops-heavy SMBs, especially property management, NYC SMB operations, wholesale distribution, construction/skilled trades, insurance/Agentforce, and productized service workflows.
- **Best surfaces:** `skills/opticfy-ops`, `skills/opticfy-pipeline`, `skills/ai-context-os`, `skills/client-proof-capture`, `skills/n8n-blueprint`, `skills/proposal-pdf`, `agents/workflow-strategist`, `agents/client-proof-engine`, project `CLAUDE.md` in `~/projects/jt-consulting-pipeline`.
- **Do not make:** a plugin for each vertical. The verticals are context, not separate products yet.

### AI Context / Knowledge Readiness
- **What JT does:** turns scattered company knowledge, SOPs, examples, edge cases, approval rules, and operator judgment into agent-ready context files and eval packs.
- **Best surfaces:** `skills/ai-context-os`, `~/projects/jtsomwaru-com/src/app/services/ai-context-os`, `skills/client-proof-capture` after client-specific context works.
- **Do not make:** a generic RAG/document-chat plugin before a client-proven pattern exists. The moat is workflow-specific extraction, evals, freshness, and vertical pattern compounding.

### Client Proof / Reusable IP
- **What JT does:** turns paid client work into anonymized proof, reusable workflow patterns, portfolio assets, content angles, and referral asks.
- **Best surfaces:** `skills/client-proof-capture` for same-turn workflow; `agents/client-proof-engine` for periodic packaging and gap detection.
- **Why:** this is the cash-to-credibility bridge. It needs gates and privacy rules, not ad hoc memory.

### LinkedIn / Content Growth
- **What JT does:** publishes proof-led operator content, LinkedIn authority/career content, app/product updates, X posts, and niche-specific takes.
- **Best surfaces:** `skills/content-generation`, `skills/linkedin-corpus`, `agents/linkedin-corpus`, `memory/content/current-niche-map.md`.
- **Plugin candidate:** bundle the content/proof skills only when portability matters.
- **Do not make:** a separate skill for every platform unless the platform has materially different inputs or verification.

### App Products
- **What JT does:** builds and markets Vista, Nash Satoshi, Glow Index, Sports GM/Dynasty content, and App Marketing OS loops.
- **Best surfaces:** existing app/project `CLAUDE.md` files plus focused agents where cadence matters (`app-marketing-product-content`, Sports GM skill), with `skills/product-build-loop` and `agents/product-quality-pass` for non-trivial build/ship quality gates.
- **Do not make:** a vertical-specific app plugin until the app has repeated build/release workflows that need portability. Project files should hold project-specific commands and gotchas; the build-quality method belongs in the skill/plugin.

### Job Market / Career Leverage
- **What JT does:** selectively applies to AI implementation / AI enablement roles and uses job posts as market-intel/proof-lane signals.
- **Best surfaces:** `skills/job-application`, `projects/job-market-agent/CLAUDE.md`, role-to-build matrix.
- **Do not make:** a plugin. The workflow is document-heavy and already skill/agent-shaped.

### Crypto / Nash / x402
- **What JT does:** monitors crypto as income/opportunity scan, uses Nash rankings for content, tracks x402 as a forward operator-builder bet.
- **Best surfaces:** `projects/crypto-agent/CLAUDE.md`, Nash project instructions, `skills/x-research`.
- **Do not make:** automated trading tools. Financial boundary stays hard.

### Operations / Chief of Staff
- **What JT does:** runs Mission Control, crons, health, cost, daily/weekly synthesis, memory, and system hygiene.
- **Best surfaces:** `AGENTS.md`, `TOOLS.md`, `HEARTBEAT.md`, system-auditor skill, Mission Control priority auditor.
- **Do not make:** another generic “Eve” plugin. This belongs in core operating rules.

## Build Priority
1. Skills that close repeatable human bottlenecks: LinkedIn examples, client proof capture.
2. Agents only where ongoing state/cadence exists: corpus maintenance, proof packaging.
3. Plugins only as distribution wrappers around stable skills/tools.
4. CLAUDE.md/AGENTS.md only for project-specific constraints and commands.

## Claude Toolkit Audit — 2026-06-02
- Claude's `jt-claude-toolkit` was stronger on portable packaging, proposal PDF styling, workflow strategist/builder split, and product quality-pass language.
- OpenClaw's system is stronger on JT-specific routing: prospect tiers, verified-contact gates, Mission Control, proof privacy, Client OS, Drive sync, and live automation state.
- Adopted missing portable pieces into OpenClaw instead of replacing the OS:
  - `skills/n8n-blueprint`
  - `skills/proposal-pdf`
  - `skills/product-build-loop`
  - `agents/workflow-strategist`
  - `agents/product-quality-pass`
  - expanded `~/plugins/jt-operating-system`
- Rejected importing Claude's `resume-tailor`, `new-client`, global prettier hook, and generic vertical plugin split because existing OpenClaw rules are stricter or safer.
