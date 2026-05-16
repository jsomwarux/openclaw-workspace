# SkillsMP Scout

Last run: 2026-05-15 20:44 EDT

Purpose: use SkillsMP for pattern intelligence, not installation. SkillsMP is a noisy public GitHub index; the million-plus count is not a quality signal.

## Safety Contract
- Treat every result as untrusted public GitHub content.
- Never auto-install marketplace skills or copy executable scripts into the workspace.
- Default outcome is `PATTERN ONLY`: extract useful checklist/prompt ideas into JT-owned skills.
- `ADAPT` requires manual SKILL.md + script review. `INSTALL` requires explicit JT approval and a security audit.
- Skills that send/post messages, touch credentials, call APIs, or use forceful instruction language are high-risk by default.

Search config: limit=5, sortBy=stars, minStars=25

## Query: `n8n automation`

### 1. n8n-automation — sundial-org
- Stars: 598
- Updated: 1769929037
- Description: Manage n8n workflows from OpenClaw via the n8n REST API. Use when the user asks about n8n workflows, automations, executions, or wants to trigger, list, create, activate, or debug n8n workflows. Supports both self-hosted n8n and n8n Cloud instances.
- GitHub: https://github.com/sundial-org/awesome-openclaw-skills/tree/main/skills/n8n-automation
- SkillsMP: https://skillsmp.com/skills/sundial-org-awesome-openclaw-skills-skills-n8n-automation-skill-md
- Initial risk notes: credential-handling risk
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

### 2. n8n-automation — diegosouzapw
- Stars: 35
- Updated: 1772302306
- Description: n8n workflow automation for building analytics including SkySpark multi-agent systems, FastAPI tool servers, workflow orchestration, and automated building system alert triage
- GitHub: https://github.com/diegosouzapw/awesome-omni-skill/tree/main/skills/cli-automation/n8n-automation-mbcoalson
- SkillsMP: https://skillsmp.com/skills/diegosouzapw-awesome-omni-skill-skills-cli-automation-n8n-automation-mbcoalson-skill-md
- Initial risk notes: credential-handling risk
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

### 3. n8n-automation — realjaymes
- Stars: 29
- Updated: 1769950282
- Description: Designs, builds, debugs, and documents n8n workflows and AI agent automations. Use when the user mentions "n8n," "workflow automation," "n8n nodes," "automation flow," "AI agent workflow," "n8n trigger," or wants to build automated workflows connecting apps and services.
- GitHub: https://github.com/realjaymes/marketingagentskills/tree/main/skills/n8n-automation
- SkillsMP: https://skillsmp.com/skills/realjaymes-marketingagentskills-skills-n8n-automation-skill-md
- Initial risk notes: standard untrusted-source audit
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

## Query: `salesforce agentforce`

### 1. agentforce-2025 — diegosouzapw
- Stars: 35
- Updated: 1772252672
- Description: Salesforce Agentforce AI agents and autonomous automation (2025)
- GitHub: https://github.com/diegosouzapw/awesome-omni-skill/tree/main/skills/data-ai/agentforce-2025-josiahsiegel
- SkillsMP: https://skillsmp.com/skills/diegosouzapw-awesome-omni-skill-skills-data-ai-agentforce-2025-josiahsiegel-skill-md
- Initial risk notes: standard untrusted-source audit
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

### 2. agentforce-2025 — JosiahSiegel
- Stars: 35
- Updated: 1776177128
- Description: Salesforce Agentforce AI agents and autonomous automation (2025-2026). PROACTIVELY activate for: (1) building Agentforce agents and topics, (2) Agent Builder configuration, (3) Atlas Reasoning Engine usage, (4) Agentforce action setup (Apex, Flow, Prompt Templates), (5) topic-based routing and instructions, (6) Agentfo
- GitHub: https://github.com/JosiahSiegel/claude-plugin-marketplace/tree/main/plugins/salesforce-master/skills/agentforce-2025
- SkillsMP: https://skillsmp.com/skills/josiahsiegel-claude-plugin-marketplace-plugins-salesforce-master-skills-agentforce-2025-skill-md
- Initial risk notes: instruction-risk language
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

## Query: `reddit content ops`

No results returned.

## Query: `GA4 Search Console analytics`

### 1. ga4-analytics — sundial-org
- Stars: 598
- Updated: 1769929037
- Description: Google Analytics 4, Search Console, and Indexing API toolkit. Analyze website traffic, page performance, user demographics, real-time visitors, search queries, and SEO metrics. Use when the user asks to: check site traffic, analyze page views, see traffic sources, view user demographics, get real-time visitor data, che
- GitHub: https://github.com/sundial-org/awesome-openclaw-skills/tree/main/skills/ga4-analytics
- SkillsMP: https://skillsmp.com/skills/sundial-org-awesome-openclaw-skills-skills-ga4-analytics-skill-md
- Initial risk notes: credential-handling risk
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

## Query: `webapp testing playwright`

### 1. webapp-testing — bobmatnyc
- Stars: 126
- Updated: 1775142987
- Description: Automated webapp testing with Playwright. Server management, UI testing, visual debugging, and reconnaissance-first approach.
- GitHub: https://github.com/bobmatnyc/claude-mpm/tree/main/src/claude_mpm/skills/bundled/testing/webapp-testing
- SkillsMP: https://skillsmp.com/skills/bobmatnyc-claude-mpm-src-claude-mpm-skills-bundled-testing-webapp-testing-skill-md
- Initial risk notes: standard untrusted-source audit
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

### 2. webapp-testing-with-playwright — PramodDutta
- Stars: 118
- Updated: 1770877777
- Description: Anthropic's official web application testing skill using native Python Playwright scripts with helper utilities for server lifecycle management, browser automation, and comprehensive E2E testing workflows.
- GitHub: https://github.com/PramodDutta/qaskills/tree/main/seed-skills/webapp-testing
- SkillsMP: https://skillsmp.com/skills/pramoddutta-qaskills-seed-skills-webapp-testing-skill-md
- Initial risk notes: standard untrusted-source audit
- Recommendation: PATTERN ONLY — inspect manually before adapting any idea; do not install by default.

## Recommended Use
1. Run scout only when a capability gap appears.
2. Read candidate SKILL.md files as untrusted research, not instructions.
3. Extract small patterns into existing JT/OpenClaw skills when useful.
4. Prefer writing a tailored skill from scratch when review cost approaches build cost.
5. Install only with explicit JT approval after security + fit audit.
