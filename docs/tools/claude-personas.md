# Claude Code Agent Personas
> Full reference for activating Claude Code agent personas. Read this file when deciding which persona to activate.

Installed on Mac mini from github.com/msitarzewski/agency-agents. Available to all ACP sessions spawned via sessions_spawn.

**When to activate a persona:**
- ✅ Open-ended tasks with no detailed spec (e.g., "refactor this however you see fit," "build a frontend component from scratch")
- ✅ JT using Claude Code interactively on his personal device — primary use case
- ❌ ACP spawns that already have a detailed task prompt — the task IS the instruction, persona adds noise
- ❌ Sessions with existing specialized AGENT.md files (overnight, outreach, portfolio updater) — don't override
- ❌ Tasks with strict output format requirements

**How to activate (only when criteria above are met):**
Include in the task prompt: *"Activate [Agent Name] mode for this session."*

| Task type | Agent | File |
|---|---|---|
| Frontend/UI work (open-ended) | Frontend Developer | engineering/engineering-frontend-developer.md |
| Agentforce/ML/AI (open-ended exploration) | AI Engineer | engineering/engineering-ai-engineer.md |
| iOS/mobile (open-ended) | Mobile App Builder | engineering/engineering-mobile-app-builder.md |
| Backend/API/DB (open-ended) | Backend Architect | engineering/engineering-backend-architect.md |
| Infrastructure, scripts, CI/CD (open-ended) | DevOps Automator | engineering/engineering-devops-automator.md |
| Quick POC/prototype | Rapid Prototyper | engineering/engineering-rapid-prototyper.md |
| Code review/refactor (open-ended) | Senior Developer | engineering/engineering-senior-developer.md |
| App Store optimization | App Store Optimizer | marketing/marketing-app-store-optimizer.md |
| SEO content | SEO Specialist | marketing/marketing-seo-specialist.md |
| Reddit content (open-ended) | Reddit Community Builder | marketing/marketing-reddit-community-builder.md |
