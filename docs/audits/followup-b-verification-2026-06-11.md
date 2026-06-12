# Follow-up B Verification Sweep - 2026-06-11

Backup before edits:
- `docs/audits/followup-b-backups-20260611155345/`
- `docs/audits/followup-b-security-redaction-backups-20260611155823/`

Proof:
- `ec66172d` in `proofs/2026-06-11/actions.jsonl`; proof guard passed with 26 entries and no warnings.
- Final proof report marker: `c2c61713`; proof guard passed with 27 entries and no warnings.

## Numbered Results

1. **PERSISTENCE — PASS**
Evidence: after `restart-gateway.sh "follow-up B persistence verification"`, `jobs.json` verified 70 jobs / 53 enabled; live `openclaw cron list --json` listed 53 enabled and `Night Autonomy Agent` enabled. Content LinkedIn/X first 200 installed-prompt chars match Appendix A/B code-block text. The 12 Phase 1 removed jobs remain absent, and `nightly-autonomous-leverage-agent` plus `Overnight Autonomy Agent` remain disabled.

2. **CONTRADICTIONS — FIXED**
Evidence: `AGENTS.md` now states sanctioned lanes are a JT-approved Plan Mode exception within lane scope only; `rg` found no remaining `12-tool`, `12 tool`, `one-outcome`, or `one outcome` caps.

3. **LANE CARVE-OUTS — FIXED**
Evidence: `AGENTS.md` ops self-healing now excludes `openclaw.json`/auth/model config edits, creating new cron jobs, deleting jobs, external sends/posts, and cron prompt rewrites outside the first-Sunday ritual.

4. **NIGHT CONTRACT — FIXED**
Evidence: live Night Autonomy prompt contains all required markers: exactly one deliverable, local file path plus Drive link, one named blocker, recommendations-only failed run, 30 tool-call cap, and Mission Control outcome logging.

5. **MEMORY REGROWTH — FIXED**
Evidence: `MEMORY.md` now has the one-line-index/full-doc growth rule, 7K warning rule, and states the bootstrap figure covers exactly `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, and `HEARTBEAT.md`. Current index is 8,186 bytes, so JT warning is active; total bootstrap is 44,192 chars.

6. **SNAPSHOT DEDUPE — FIXED**
Evidence: `scripts/cron_snapshot.py` now hashes canonical `jobs.json`; fresh rerun returned `CRON_SNAPSHOT_NO_HASH_CHANGE config/cron-snapshots/.jobs-json.sha256`.

7. **SECURITY CLOSEOUT — BLOCKED**
Evidence: live values to rotate remain XAI/Grok API key, Anthropic API key, and n8n encryption key. Residual Convex `--instance-secret` and backup admin-key artifacts were redacted where found, but the current process-listing issue is Convex local backend itself passing `--instance-secret` in argv; moving that to env/keychain is blocked without changing the Convex runtime/CLI behavior.

8. **MISC — BLOCKED**
Evidence: manual Groq-routed Nash warm-up run failed preflight: `groq/llama-3.3-70b-versatile` is rejected by the runtime allowlist `[moonshot/kimi-k2.6, openai/gpt-5.5]`, so delivery was `not-requested`. Sunday 6PM pair resolution from Phase 1: both jobs were kept; North Star Command Center remains 6:00PM Sunday and Weekly Strategic Gut-Check moved to 6:30PM Sunday. Safe delete-after-30-day candidates: the two old night jobs, redundant 7:45PM TikTok warm-up, old weekly/content send/vibe posting jobs if no rollback is needed, with archive/snapshot retained first.

## Verification Commands

- `python3 -m py_compile scripts/cron_snapshot.py scripts/recompute_delivery_rate.py scripts/critical-files-integrity.py`
- `python3 scripts/cron_snapshot.py`
- `python3 scripts/model_routing_guard.py --include-disabled`
- `python3 scripts/cron_volume_guard.py`
- `openclaw cron list --json` parsed through Python
- `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md`
