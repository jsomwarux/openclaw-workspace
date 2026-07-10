# Recent Builds Archived Before 2026-07-09

Entries moved from `memory/content/recent-builds.md` after the proof guard flagged the active file over its 20K target.

## Plan Review Pack Skill + Human Signal Workflow - 2026-06-06
**What:** Added `plan-review-pack` plus Client OS, AI Context OS, workflow protocol, proof, product, and video-generation wiring so internal agent plans become human-readable review/proof artifacts.
**For:** internal consulting delivery system
**Outcome:** New skill validated, portable `jt-operating-system` plugin updated/validated with cachebuster `0.2.0+codex.20260606170202`, autoresearch checklist/target added, and Mission Control task `j5728192wnpdjqhzg4bcrryj0x884rm6` created to apply it to the Altmark rent delinquency gate.
**Demonstrates:** agent operating-system design, client proof workflow packaging, human-as-signal delivery loops
**Content angle:** The useful version of human-in-the-loop is not approval on every step; it is a review pack that asks for direction, risk, taste, and acceptance at the exact right point.
**Status:** complete

## Crypto Full Analysis Atomic Pipeline - 2026-06-03
**What:** Added `scripts/run-full-analysis-pipeline.py` and X preflight enforcement inside `generate-full-analysis.py` so the crypto cron runs fetch -> X -> guard -> generate -> validate as one deterministic recovery path.
**For:** internal crypto automation
**Outcome:** Fresh pipeline passed with 25 X entries, X age 0.00h at guard time, validator ok=true for 24 coins and 6 held positions, and `checkpoint: CRYPTO_FULL_ANALYSIS_OK`; cron now calls the pipeline before Telegram delivery.
**Demonstrates:** atomic cron design, stale-evidence prevention, validator-gated delivery
**Content angle:** A deterministic writer is not enough if it trusts stale upstream evidence. The freshness gate belongs inside the writer and the pipeline.
**Status:** complete

## Crypto Full Analysis Deterministic Writer - 2026-06-03
**What:** Added a deterministic writer that converts fresh crypto portfolio, prices, X research, and whale inputs into dated analysis, Telegram summary, history, and allocation artifacts.
**For:** internal crypto automation
**Outcome:** June 3 validator passed for 24 coins, 6 held positions, 25 X entries, and `data/allocation-history/2026-06-03.json`; 6AM cron now calls the writer before Telegram delivery.
**Demonstrates:** cron reliability hardening, validator-gated artifact generation, financial-safety boundaries
**Content angle:** Production agents should not ask a model to remember to write every required artifact when deterministic code can guarantee the handoff.
**Status:** complete
