# App Marketing OS — Experiment Tracking Schema
Date: 2026-05-19

## Purpose
Make every app-marketing experiment measurable enough to decide scale / iterate / kill.

## Required Fields
- `id`: stable slug, e.g. `vista_taste_card_soft_prompt_20260519`
- `app`: Vista / Nash Satoshi / Glow Index / Action Arena
- `channel`: X / TikTok / Reddit / creator DM / newsletter / SEO / ASO / directory
- `source_tag`: short tag used in URL, notes, or post registry
- `source_url`: live post, page, directory, or message URL when available
- `target`: audience, creator, community, keyword, or page type
- `asset`: card/page/post/outreach asset used
- `hypothesis`: if we do X for Y, Z should happen because...
- `run_date`
- `owner`: eve / jt / both
- `gate`: what must be true before launch
- `primary_metric`
- `secondary_metric`
- `baseline`
- `24h_result`
- `72h_result`
- `7d_result`
- `attribution_confidence`: high / medium / low
- `decision`: planned / running / scale / iterate / kill / blocked
- `decision_reason`
- `next_action`

## Decision Rules
- No source tag = no scale decision.
- No 72h result = keep as `running` or `blocked`, not `successful`.
- 3 clean failures = kill format/channel unless a materially different asset is proposed.
- Missing metric path for 2 weeks = MEASURE_FIRST; do not increase content volume.

## Source Tag Examples
- `vista_tastecard_filmtok_soft_20260519`
- `vista_reddit_top4_prompt_20260519`
- `nash_aiagents_receipt_x_20260519`
- `nash_newsletter_receipt_soft_20260519`
- `glow_verdictcard_creator_soft_20260519`
- `glow_productverdict_seo_batch1_20260519`
