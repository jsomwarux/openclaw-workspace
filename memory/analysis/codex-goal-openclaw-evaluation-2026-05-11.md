# Codex `/goal` + OpenClaw Evaluation

Date: 2026-05-11
Sources:
- X post: https://x.com/Saboo_Shubham_/status/2053537881315229721
- OpenAI docs: https://developers.openai.com/codex/use-cases/follow-goals
- OpenAI Codex release notes 0.128.0
- GitHub issue documenting `/goal` lifecycle/discoverability
- Simon Willison note on Codex `/goal`
- Local OpenClaw docs/source inspection

Status: research signal and planning. Do not enable/install Codex or change OpenClaw config without JT approval.

## What the X Post Claims

Shubham Saboo says Codex `/goal` with Hermes Agent is life-changing because he can send Codex a goal from Telegram and track Codex goals in a Kanban board while Codex executes them in the wild.

Useful idea: conversational goal creation + durable background execution + visible board tracking.

Do not assume Hermes behavior maps 1:1 to OpenClaw. Validate against OpenClaw capabilities.

## What `/goal` Actually Is

Official OpenAI docs describe `/goal` as an experimental Codex CLI feature for durable long-running objectives. It is for tasks that need Codex to keep working across turns toward a verifiable stopping condition.

Observed docs/features:
- Enable from `/experimental` or `goals = true` under `[features]` in `config.toml`.
- Set goal with `/goal <objective>`.
- Inspect with `/goal`.
- Control with `/goal pause`, `/goal resume`, `/goal clear`.
- Can work independently for multiple hours.
- Best for code migrations, large refactors, experiments/prototypes, games, prompt optimization with eval suites.
- Bad for loose unrelated backlogs.
- Requires objective, constraints, validation loop, stopping condition, checkpoint/progress log.

Release notes say Codex 0.128.0 added persisted `/goal` workflows with app-server APIs, model tools, runtime continuation, and TUI controls for create/pause/resume/clear.

GitHub issue notes statuses/surfaces such as pursuing, paused, achieved, unmet, and budget-limited.

Simon Willison frames it as Codex's built-in Ralph loop: keep looping until complete or token budget exhausted.

## Local OpenClaw Reality

Local check on 2026-05-11:
- `codex` CLI is not installed on this Mac (`codex not found`).
- `~/.codex` exists only with `superpowers`, no visible CLI config.
- OpenClaw docs have bundled Codex app-server harness docs, but local source grep did not show `/goal` surfaced through OpenClaw `/codex` commands yet.
- OpenClaw already has TaskFlow, crons, isolated/current/session cron jobs, subagents, sessions_spawn, Mission Control, and persistent task tracking.

Therefore: do not treat Codex `/goal` as currently available in this OpenClaw deployment. It is a candidate future harness capability, not something to rely on today.

## Comparison to OpenClaw Patterns

### Codex `/goal`
Best when:
- one durable coding objective
- clear stop condition
- Codex owns the loop
- work benefits from repeated inspect/edit/test cycles
- progress can continue for hours without JT steering

Risk:
- experimental
- potentially high token/cost usage
- can pursue wrong objective for a long time if goal is vague
- requires strict boundaries, checkpoints, and budget limits
- not installed locally yet

### OpenClaw TaskFlow
Best when:
- multi-step orchestration with explicit state/waits/child tasks
- work may require human waits, crons, external systems, multiple agents
- the system needs durable owner context and inspection

### OpenClaw Cron
Best when:
- recurring scheduled work
- monitoring, reminders, morning briefs, periodic generation
- strict delivery/output checks

### sessions_spawn/subagents
Best when:
- one detached focused job
- research/coding/audit that can finish independently
- no durable multi-hour continuation loop needed

## Optimal Use Cases for JT/Eve if `/goal` Becomes Available

Use `/goal` only for bounded, verifiable, code-heavy or artifact-heavy work:

1. **Portfolio/app build stabilization**
   - Goal: make `npm run build` pass, fix failing pages, capture screenshot, stop only when deploy-ready.

2. **ReelFarm/App Marketing OS HTML audit artifact**
   - Goal: generate a polished HTML report from six extracted automation configs, with exact recommended setting changes and exportable JSON patch list.

3. **Prompt/eval optimization loops**
   - Goal: improve a prompt against an eval file until score improves by X or no regression remains.

4. **Large refactors/migrations**
   - Goal: migrate one module/path while preserving tests and behavior.

5. **AgentGuard/demo hardening**
   - Goal: add verification/audit/reporting capability and prove with tests/screenshot/log sample.

6. **n8n helper/tool scaffolding outside n8n runtime**
   - Goal: build local helper script or test harness, not directly mutate n8n production workflows without approval.

7. **HTML design playgrounds**
   - Goal: create interactive slider/editor artifact with copy JSON/prompt export and verify it works locally.

Avoid `/goal` for:
- vague research
- outreach writing
- content drafting
- financial/crypto decisions
- anything needing third-party messages
- broad backlog cleanup
- high-risk config/auth changes
- tasks without tests or verifiable artifacts

## Recommended Implementation

Do not install or enable Codex `/goal` yet.

Instead:
1. Keep using OpenClaw TaskFlow/cron/subagents as current durable execution system.
2. Add a goal-spec template so future `/goal` or TaskFlow jobs are written with objective, constraints, stop condition, validation, budget, and checkpoints.
3. If JT explicitly approves Codex install/enablement later, pilot on one low-risk repo task with no external side effects.
4. Track any goal in Mission Control with owner, first action, stop condition, status, and done evidence.
5. Require a goal audit before marking complete: requirement-by-requirement proof from files/tests/output.

## Pilot Candidate

Best first pilot, if approved later:

**Generate ReelFarm HTML Audit Report**

Why:
- Uses existing local markdown/screenshot-derived configs.
- No external writes.
- Clear output artifact: HTML report + copyable JSON recommendations.
- Easy verification: file opens, includes all six automations, recommendations match baseline.

Stop condition:
- `memory/reelfarm/reelfarm-audit-2026-05-11.html` exists.
- Includes all six automations.
- Has per-app/per-automation cards.
- Has exact setting changes.
- Has exportable JSON recommendation list.
- No secrets.

This is safer than starting with codebase refactors or config changes.

## Audit Follow-Up — 2026-05-11

JT asked whether the understanding and implementation were truly optimal. Audit found the strategic conclusion was correct, but two implementation surfaces were missing:

1. `MEMORY.md` did not yet record the durable Codex `/goal` stance.
2. Global `~/.claude/CLAUDE.md` did not yet point future coding sessions to the goal-mode template/rule.

Both were fixed. The goal template was also tightened with progress-log and board-visibility fields, because the actual Hermes insight is not just long-running execution; it is long-running execution that can be tracked and audited from chat/board surfaces.

Updated stance:
- Do not enable/install Codex `/goal` yet.
- Use current OpenClaw TaskFlow/cron/subagent patterns by default.
- When goal-style execution is appropriate, require one durable objective, verifiable stop condition, progress log, Mission Control/task visibility, budget/stop rules, and completion audit.
