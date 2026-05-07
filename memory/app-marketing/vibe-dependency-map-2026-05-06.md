# Vibe Marketing Dependency Map — 2026-05-06

## Purpose
Decide whether X/Reddit/TikTok systems should stay under `agents/vibe-marketing/` or move into the new App Marketing OS.

## Executive Finding
Do not move files yet.

`agents/vibe-marketing/` is not the ideal long-term root, but it has too many live dependencies to move safely in one pass. The optimal posture is:

1. Keep `agents/vibe-marketing/` as the current compatibility layer.
2. Treat `memory/app-marketing/` as the strategic source of truth.
3. Treat JT's laptop as the ReelFarm/TikTok execution layer.
4. Migrate to a cleaner `agents/app-marketing/` structure only after replacing or updating cron/script references.

## Current Cron Dependencies

### Enabled
- `vibe-marketing-generate` (`870bf3ff-55c9-49c0-9970-361c81a0920b`)
  - Schedule: Monday 4:45 AM ET.
  - Reads/follows `agents/vibe-marketing/AGENT.md`.
  - Generates weekly product content for Nash Satoshi/Vista/future products.
  - Still active and therefore blocks immediate file moves.

- `ReelFarm Daily Strategy Intel` (`a97df783-31c5-4269-a4f0-3ece75af838d`)
  - Schedule: daily 5:15 PM ET.
  - Reads `agents/reelfarm-intel/daily-prompt.md`.
  - Should remain in `memory/reelfarm/`/`agents/reelfarm-intel/`, not Vibe.

- `ReelFarm Weekly Strategy Synthesis` (`bb0819d0-8900-4e2a-99a2-28ab950365ab`)
  - Schedule: Sunday 5 PM ET.
  - Reads `agents/reelfarm-intel/weekly-prompt.md`.
  - Strategy/intel only; not posting execution.

### Disabled / Legacy
- `vibe-post-vista-friday` (`a81aa240-8eac-4874-a9cb-ddfd0aa238e2`) — disabled.
- `vibe-post-vista-sunday` (`06050403-afb5-4783-a95a-fc6708ce61ec`) — disabled.
- `vibe-post-nash-tuesday` (`365e8277-f552-4192-9fce-e99dce68f77b`) — disabled.
- `vibe-post-nash-thursday` (`faf41f37-938c-4bdb-baaa-fe84769a6160`) — disabled.

These disabled jobs still contain old “build and publish slideshow via ReelFarm” payloads. They are not currently dangerous because they are disabled, but they are stale and should remain disabled unless JT explicitly reactivates Mac mini TikTok posting.

## Script/File Dependencies

### Hard references to `agents/vibe-marketing/`
- `scripts/vibe-post.py`
  - Reads `agents/vibe-marketing/queue.jsonl`.
  - Reads `agents/vibe-marketing/performance-log.jsonl`.
  - Reads `agents/vibe-marketing/product-registry.json`.
  - Calls `scripts/reelfarm-create-slideshow.py`.
  - Legacy Mac mini publishing path. Keep but do not treat as active.

- `scripts/vista-photo-selector.py`
- `scripts/nash-photo-selector.py`
- `scripts/photo-selector.py`
  - Read `agents/vibe-marketing/real-photos/...`.
  - Legacy/optional asset pipeline.

- `scripts/add_vista_q.py`, `scripts/patch_caption.py`
  - Utility scripts tied to old queue/posting flow.

- `agents/launch-kit/AGENT.md`
  - Uses `agents/vibe-marketing/product-registry.json` as the trigger/source for product launch kits.

- `agents/overnight/AGENT.md`
  - Reads `agents/vibe-marketing/product-registry.json`.

- `scripts/critical-files-integrity.py`
  - Tracks `agents/vibe-marketing/AGENT.md` as a critical file.

- Autoresearch files:
  - `agents/autoresearch/checklists/vibe-marketing.md`
  - `agents/autoresearch/targets.md`
  - prior logs point at `agents/vibe-marketing/AGENT.md`.

## Current Content Ownership

### Product X
Current: `agents/vibe-marketing/`.
Long-term better home: `agents/app-marketing/product-content/`.
Reason: product X is app/product marketing, not necessarily “vibe marketing.”

### Reddit
Current: `agents/vibe-marketing/`.
Long-term better home: `agents/app-marketing/product-content/reddit-rules.md` or equivalent.
Reason: Reddit needs strict community-native rules and product-specific promo boundaries. It should live under the broader App Marketing OS, not a TikTok/vibe-oriented agent.

### TikTok/ReelFarm
Current: mixed/stale:
- Vibe Marketing still has TikTok copy/queue/platform rules.
- ReelFarm Intel has current strategy intelligence.
- JT laptop owns actual creation/posting.

Long-term better split:
- `memory/reelfarm/` + `agents/reelfarm-intel/` = TikTok/ReelFarm trend intelligence.
- `memory/app-marketing/` = metrics handoff + strategy + asset map.
- `agents/app-marketing/product-content/` = optional hook/slide copy recommendations.
- JT laptop = execution.

### Personal Brand
Current: `agents/content-scheduler/` and `agents/content-calendar/`.
Keep there.

### Sports / Action Arena / Dynasty Simulator
Current: `skills/sports-gm/SKILL.md` plus sports crons.
Keep there. Do not fold into Vibe Marketing.

## Recommended Migration Plan

### Phase 0 — Current safe state
Done:
- App Marketing OS docs created in `memory/app-marketing/`.
- MEMORY.md trimmed under 20k and corrected.
- Vibe AGENT.md patched to stop assuming active Mac mini ReelFarm publishing.
- Old Mac mini TikTok posting crons verified disabled.

### Phase 1 — Compatibility wrapper
Keep `agents/vibe-marketing/` where it is, but make it explicitly subordinate to `memory/app-marketing/`.
Patch `vibe-marketing-generate` prompt later so it reads:
1. `memory/app-marketing/os-spec.md`
2. `memory/app-marketing/app-registry.md`
3. then `agents/vibe-marketing/AGENT.md`

This gives strategic control to the OS without moving files.

### Phase 2 — Extract product content agent
Create `agents/app-marketing/product-content/AGENT.md` that owns:
- product X drafts
- Reddit drafts
- monthly LinkedIn product posts
- optional TikTok hook/slide copy suggestions

Then update the Monday cron to use the new path.

### Phase 3 — Archive or freeze legacy posting scripts
Once laptop ReelFarm handoff is fully documented:
- Keep `scripts/vibe-post.py` as legacy/manual fallback.
- Do not delete until confirmed no cron/script references remain.
- Add top-of-file legacy warning to `scripts/vibe-post.py` if needed.

### Phase 4 — Move state carefully
Only after cron/script updates:
- Move `product-registry.json` or mirror it into `memory/app-marketing/app-registry.json`.
- Move X/Reddit/LinkedIn queue state into an app-marketing path.
- Keep old path symlink or compatibility shim if needed.

## Recommendation
For the next step, do not move files. Instead:
1. Patch the active `vibe-marketing-generate` cron prompt to read App Marketing OS first.
2. Create a clean `agents/app-marketing/product-content/AGENT.md` as the future owner.
3. Run one dry generation/report pass before changing cron ownership.

This avoids breaking active systems while moving toward the correct architecture.
