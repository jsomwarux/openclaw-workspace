# Eve Optimization Plan - 2026-06-11

Source files:
- `docs/audits/eve-optimization-report-2026-06-11.md`
- `docs/audits/eve-playbook-2026-06-11.md`

Current source version: v2, received 2026-06-11.
Execution order: Phase 1, Phase 2B, Phase 2A, Phase 3, Phase 4, Phase 5, Phase 6, Phase 7.

## Phase Tracker

- Phase 1: status=completed - Removed 12 named disabled cron zombies, confirmed older duplicates disabled, moved Weekly Strategic Gut-Check to Sunday 6:30PM ET, and saved baseline delivery metric.
- Phase 2B: status=completed - Watchdog now uses gateway HTTP health as the recovery source of truth, has 1h restart-loop backoff plus dry-run and once-per-6h openai-codex cooldown repair; restart script uses modern bootout/bootstrap; n8n and Mission Control Next bind to `127.0.0.1`; `/n8n` tailnet path restored; requested memory secrets plus hidden recall duplicate and auth-profile audit backup were redacted. Convex remains on wildcard 3210/3211 because `convex dev` exposes no supported host bind flag.
- Phase 2A: status=completed - Moonshot fallback skipped after billing failure; removed Spanish audio language pin, backed up/reset lcm.db, restarted gateway, and verified only the intended config diff.
- Phase 3: status=completed - Built and updated `memory/jt-corpus.md` with 15 verbatim JT-writing entries from supplied X posts plus supplied LinkedIn proof posts, kept it under 15K chars, uploaded/refreshed it in Drive, and left cron wiring blocked until JT approves the corpus.
- Phase 4: status=completed - Corpus approval received; quality gate passed (15 entries, 10 X, 5 LinkedIn, 12 formats). Installed v2 corpus-first prompts on `content-generate-linkedin` and `content-generate-x`, set both to `openrouter/anthropic/claude-sonnet-4-6` with schedules unchanged, added `memory/content/edit-deltas.jsonl`, posted-reply delta logging, wrapper guard, content-audit markers, and a $10/month combined Sonnet cap alert in `scripts/cost-tracker.py`.
- Phase 5: status=completed - Created `memory/digest-queue.md`, routed reminder/FYI jobs into digest entries, added the daily 7PM ET `Evening Digest` cron, revised Morning Brief to open with a capped 3-item Send Queue, replaced the Nash full-text inline delivery contract with excerpts plus file/Drive links, backed up edited payload messages to `docs/audits/phase5-prompt-backups.md`, and left `content-reminder` intact.
- Phase 6: status=completed - Reduced bootstrap from 64,147 chars to 43,051 chars by relocating MEMORY/TOOLS detail into full docs, rewrote only the model-routing contradiction in `AGENTS.md`, fixed the stale Notion cron line in `TOOLS.md`, removed 58 default `openai/gpt-5.5` cron model overrides with backup `~/.openclaw/cron/jobs.json.backup-phase6-20260611142934`, preserved all 3 non-default overrides, and verified bootstrap smoke `BOOTSTRAP_SMOKE_OK`.
- Phase 7: status=completed - Merged `nightly-autonomous-leverage-agent` and `Overnight Autonomy Agent` into the 11PM `Night Autonomy Agent` (`f146d8b8-94e0-49ff-8e4a-5050a284e894`), disabled both originals without deleting them, archived prompts to `docs/audits/phase7-night-agent-prompts-2026-06-11.md`, added sanctioned autonomy lanes to `AGENTS.md`, added outcome KPI reporting and first-Sunday prompt rewrite ritual to Weekly Systems Review, repointed Monthly Goal-Skills Gap at those KPIs, and added `scripts/cron_snapshot.py` through the existing `critical-files-integrity` job.

## Findings Read

- Finding 1: One auth profile is carrying 80 jobs and it collapses daily.
- Finding 2: The content system cannot produce JT's voice by design.
- Finding 3: Proactivity is gated by JT's review bandwidth, not Eve's output.
- Finding 4: Self-improvement optimizes reliability more than outcomes, and prompt patches are degrading quality.
- Finding 5: Security and hygiene debt has moderate risk and cheap fixes.
