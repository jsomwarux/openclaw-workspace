# Weekly Systems Review — 2026-05-17

## Executive Summary
Grade: B / not clean A-level.

System is functional, but drift remains: cron volume is far above the 20/day cap, gateway process is hot/heavy, bootstrap files are near limits, gateway LaunchAgent throttle is still too aggressive, and OpenClaw update is available. Safe fixes applied this run: Job Application Auto-Builder model/timeout corrected to Sonnet/1200s, Health Check-in timeout bumped to 120s, passive-income strategist best-effort delivery made explicit, and one Mission Control follow-up task created.

## Cron Health
- Jobs checked: 52.
- Erroring job: `b2357bd5-651d-4151-80df-49e4a928826f` Job Application Auto-Builder — latest run failed with `session current, model openrouter/anthropic/claude-sonnet-4-6 failed`; last duration 331s. Fix applied: model changed from `openai-codex/gpt-5.5` to `openrouter/anthropic/claude-sonnet-4-6` per job-application Sonnet-only rule; timeout bumped 900s → 1200s.
- Delivery issue: `922082ee-da62-4b6e-b9e3-909c3446e381` passive-income-strategist had lastDeliveryStatus `not-delivered` on 2026-05-13 even though run status was ok. Prompt already requires explicit Telegram message tool send; fallback delivery is now explicitly best-effort. Not resent because the run is stale and today's 3PM strategist run is pending.
- Near-timeout job: Health Check-in last duration 81.1s / 90s. Fix applied: timeout bumped 90s → 120s.
- Never-ran job: `f96cc24f-55e6-4064-a075-b897156a22f2` AI Ops Teardown Weekly Draft — scheduled Sunday 7:15PM, created recently, first run pending.
- Invocation cap: estimated daily invocations remain high: Sun 41, Mon 39, Tue 36, Wed 36, Thu 35, Fri 35, Sat 33. This exceeds the ≤20/day cap and needs pruning/consolidation.
- Sunday 10AM conflict: Weekly Systems Review overlaps with Heartbeat at 10AM; noted only, per instruction.

## File Budgets
- AGENTS.md: 27,013 / 28,000 — warning zone, under hard cap.
- MEMORY.md: 19,820 / 20,000 — warning zone, very close to cap.
- TOOLS.md: 15,139 / 16,000 — warning zone.
- HEARTBEAT.md: 15,997 / 16,000 — essentially at cap; must compact before any append.

Recommended extraction/compaction:
- HEARTBEAT.md: move older protocol detail/history to `docs/agents/workflow-protocols.md` or heartbeat archive.
- MEMORY.md: move older App Marketing/ReelFarm and Strategic Decisions detail to `docs/memory/MEMORY-full.md` and keep only current state.
- TOOLS.md: archive older app/tool references into `docs/tools/TOOLS-full.md`.

## Process Health
- Gateway is reachable and LaunchAgent running: pid 29836.
- Gateway node process is hot/heavy: ~40.5% CPU and ~1.86GB RAM at snapshot. This should be investigated if sustained for 10+ minutes; likely contributor is high cron load/session volume.
- n8n process: ~224MB, low CPU.
- Mission Control Convex/Next processes present, low CPU.
- Watchdog LaunchAgent listed: `com.openclaw.gateway-watchdog`.

## LaunchAgent Config
- `ai.openclaw.gateway` ThrottleInterval = 1 — drift; should be ≥10. Not self-resolved because gateway LaunchAgent/service changes are sensitive.
- `com.openclaw.gateway-watchdog` StartInterval = 600 — OK, at upper allowed bound.

## Version
- Current OpenClaw: 2026.5.3-1 (2eae30e).
- Update available: 2026.5.12 (`openclaw status` also reports update available). Do not auto-update without JT approval.
- Web check: GitHub result for openclaw/openclaw showed fresh activity and npm install latest reference; local status is the stronger source for installed/update state.

## Plugin Audit
- `~/.claude/settings.json`: `context-mode@context-mode` is `false` ✅.
- Enabled Claude plugin also includes `claude-warden@claude-warden-marketplace`.
- `~/.openclaw/extensions/` contains `.openclaw-install-backups`; no unexpected active extension found in shallow listing.
- Repeated warning remains: duplicate `lossless-claw` plugin id detected; global plugin overrides global plugin path. This has not broken recall in this run but should be cleaned when doing config hygiene.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: exists/readable.
- `scripts/gateway-watchdog.sh`: exists/readable/executable.
- `health/health.sqlite`: exists/readable.
- `tasks/pending.jsonl`: valid JSONL, 4 non-empty lines, 0 parse errors.

## Weekly Maintenance Split
### Autoresearch Enrollment
- Read `agents/autoresearch/targets.md`.
- Modified skills/agents in last 7 days reviewed. Recent scoreable additions such as ai-ops-teardown, ai-governance-readiness, high-stakes-draft-eval, workflow-skillify, sports-gm, opticfy-pipeline, and mission-control-priority-auditor already have targets/checklists.
- No new enrollment needed this run.

### Future Signals
- Read `memory/future-signals.md`.
- No active signal trigger is clearly met from current MEMORY/project state. Fantasy Sports Agent remains gated; Sports GM Phase 1 is active but demand triggers not verified as met. ViewTrack and creator briefing remain gated by revenue/content/creator conditions.

### Passive-Income Idea Queue
- Mission Control reachable.
- No pruning/promotions completed from the initial query due API shape mismatch during first attempt; follow-up systemic MC task created instead. Pruning should be repeated after cron pruning work, using the dict `tasks` response shape.

### Weekly Cost Review
Total 7-day spend: $1.313.
- gpt-5.5: $1.206 (92%, 3 sessions)
- deepseek/deepseek-chat-v3-0324: $0.107 (8%, 7 sessions)
Most expensive session: 2026-05-17 Cron: prospect-discovery $1.206.
Monthly pace: $9.76 vs $50 target; $40.24 headroom.
Observation: Groq/Llama unused this week; simple cron routing may not be taking the cheapest path.

## Issues Fixed This Run
1. Job Application Auto-Builder patched to Sonnet model and 1200s timeout.
2. Health Check-in timeout bumped from 90s to 120s.
3. Passive-income strategist fallback delivery made best-effort explicit.
4. Mission Control task created: `Fix weekly systems review drift: cron cap, gateway load, bootstrap budgets`.

## Needs JT Attention / Deferred
1. Cron cap is materially exceeded: estimated 33–41/day vs ≤20 target. Needs pruning/consolidation.
2. Gateway process is hot/heavy; recheck after cron pruning and consider restart/update if still high.
3. Gateway LaunchAgent ThrottleInterval remains 1; should be ≥10.
4. Bootstrap files are near limits, especially HEARTBEAT.md and MEMORY.md; compact before appending.
5. OpenClaw update available: 2026.5.12. Manual approval recommended before update.
6. Duplicate lossless-claw plugin warning should be cleaned during config hygiene.

## Next Review
2026-05-24.
