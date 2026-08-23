# Claim: Revised Job Pipeline Reactivation — 2026-08-22

## Claim

The approved revised job pipeline is configured with weekday evidence-backed research, Tue/Thu submitted-application tracking, a disabled legacy auto-builder, GPT-5.6 Sol application routing, and a preserved legacy snapshot.

## Acceptance Criteria

- Research job enabled at `15 5 * * 1-5` in `America/New_York`, GPT-5.6 Sol, direct Telegram announce.
- Tracker enabled at `15 10 * * 2,4` in `America/New_York`.
- Auto-builder disabled.
- Legacy three-job definitions preserved as valid JSON.
- Model-routing and cron-volume guards pass.
- Job-application and targeting rules are consistent across durable instruction surfaces.

## Artifacts

- `plans/job-pipeline-reactivation-2026-08-22.md`
- `config/cron-snapshots/job-pipeline-legacy-before-reactivation-2026-08-22.json`
- `config/cron-snapshots/job-market-scoring-criteria-legacy-2026-08-22.md`
- `memory/job-state/job-market-daily-research.md`
- `skills/job-application/SKILL.md`
- `scripts/model_routing_guard.py`
- `scripts/test_model_routing_guard.py`
- `MEMORY.md`, `USER.md`, `AGENTS.md`, `directives/00-README.md`
- `/Users/jtsomwaru/projects/job-market-agent/profile/jt-profile.md`
- `/Users/jtsomwaru/projects/job-market-agent/knowledge/scoring-criteria.md`

## Verifier Commands

- `python3 -m unittest scripts/test_model_routing_guard.py -v`
- `python3 scripts/model_routing_guard.py --include-disabled`
- `python3 scripts/cron_volume_guard.py`
- `jq -e '.jobs | length == 3' config/cron-snapshots/job-pipeline-legacy-before-reactivation-2026-08-22.json`
- Inspect live cron jobs `eve-job-market-daily-005`, `b2357bd5-651d-4151-80df-49e4a928826f`, and `b0b04601-7518-4681-9761-4bbe5054ce9b`.

## Builder Evidence

- Unit tests: 2 passed.
- Model-routing guard: `ok: true`.
- Cron-volume guard: `ok: true`, 9 enabled jobs, 45 estimated weekly invocations, no collisions or warnings.
- Tracker script dry check: `ok: true`, 0 active applications, 0 flagged.

## Verifier Verdict

Initial fresh-context verdict: NOT DONE because the active profile retained a $130K-$149K exception and the active scoring rubric retained consulting/build/market-intelligence routing. Builder corrected both contradictions and archived the full legacy scoring rubric.

Final fresh-context verdict: **CONFIRMED**. The verifier independently confirmed all live cron settings, disabled auto-builder state, both legacy snapshots, verifier commands, tracker dry-check, $150K floor, evidence gate, employment-only research scope, on-demand packages, and GPT-5.6 Sol routing.
