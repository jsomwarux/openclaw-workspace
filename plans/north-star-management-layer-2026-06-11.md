# North Star Management Layer - 2026-06-11

- [x] Back up touched files and cron payloads under `docs/audits/north-star-layer-backups-20260611162829/`.
- [x] Create `memory/north-star.md` capped under 2K chars.
- [x] Seed `memory/pipeline.jsonl` from the June snapshot plus JT corrections.
- [x] Create `memory/pipeline-backlog.md` so stale prospects do not inflate active forecast.
- [x] Create `memory/send-queue.md` with the first pipeline-advancing queue.
- [x] Add deterministic parser/forecast/queue helper at `scripts/north_star_pipeline.py`.
- [x] Patch Morning Brief, outreach-pipeline, Weekly Systems Review, and Monthly Goal-Skills Gap prompts to read the North Star layer.
- [x] Archive and disable approved CUT crons only: `t3-cold-hook`, `Weekly Seeds Prompt`, `Build Ideas Sync`, `reddit-karma-daily-reminder`.
- [x] Verify JSONL parse, scoreboard cap, forecast math, cron state, cron volume, secret scan, and backups.

## Follow-up E Verification Sweep
- [x] Back up config/cron/memory/guard files under `docs/audits/followup-e-backups-20260611164648/`.
- [x] Run cron-runtime Sonnet preflight; initial rejection confirmed allowlist gap, then exact approved model entry was added and rerun returned `SONNET_PREFLIGHT_OK`.
- [x] Remove Nash TikTok Groq override so the disabled digest appender inherits default routing.
- [x] Enhance `scripts/model_routing_guard.py` to fail enabled cron `payload.model` values outside configured/runtime-allowlisted models.
- [x] Trim `MEMORY.md` below 7K and document non-bootstrap injected-file sizes.
- [x] Add Convex `--instance-secret` redaction and first-Sunday upstream env-support check.
- [x] Create 2026-07-11 Mission Control cleanup task for stale disabled cron deletion after rollback window.
