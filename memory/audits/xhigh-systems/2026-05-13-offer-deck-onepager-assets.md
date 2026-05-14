# XHigh Systems Audit — Offer / Deck / One-Pager Asset System

Date: 2026-05-13
Workspace: `/Users/jtsomwaru/.openclaw/workspace`

## Before grade

**B / B+**

JT had strong raw assets, but the system was not A+ because the source of truth was scattered across offer docs, one-pagers, Strategy Jobs Pack, hidden site pages, proof snippets, and MC tasks. The Property/Family Office wedge was clearly the best current buyer path, but the generic AI Operations one-pager could still be mistaken as canonical. Drive had the Strategy Jobs Pack, but the local asset system did not name one canonical hierarchy.

## After grade

**A-**

The hierarchy is now explicit and proof-safe. Remaining gap: the Property/Family Office one-pager still needs final Drive-ready packaging/upload and link-back in the asset index before this becomes A+.

## Inventory findings

### Primary offer: Property / Family-Office AI Operations Diagnostic

- Canonical offer: `memory/consulting/property-family-office-ai-ops-offer-2026-05-13.md`
- Buyer-facing one-pager: `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`
- Offer page copy: `memory/consulting/property-family-office-offer-page-copy-2026-05-13.md`
- Hidden website page: `/Users/jtsomwaru/projects/jtsomwaru-com/src/app/property-family-office-ai-ops/page.tsx`
- Status: strongest current buyer-facing lane. Specific, operational, proof-safe, and aligned with Altmark/Yair family-office referral path.
- Risk: must not be used for referral asks until Altmark PC handoff, acceptance wording, payment/deposit clarity, and proof permission gates are clean.

### Secondary validation offer: Guyana Local Content Operations Sprint

- Capability brief: `memory/research/guyana/local-content-ops-capability-brief-2026-05-13.md`
- Validation sprint: `memory/research/guyana/local-content-ops-validation-sprint-2026-05-13.md`
- Intro scripts: `memory/research/guyana/guyana-intro-ask-scripts-2026-05-13.md`
- Hidden website page: `/Users/jtsomwaru/projects/jtsomwaru-com/src/app/guyana/GuyanaContent.tsx`
- Status: good validation asset if kept warm-intro/operator-first.
- Risk: older government/city-services demo docs still exist and should stay parked unless a specific warm government/partner meeting appears.

### Proof/referral system

- Altmark referral pack: `memory/clients/altmark-group/proof-assets/referral-engine-pack-2026-05-13.md`
- Gate file: `memory/clients/altmark-group/proof-assets/proof-permission-referral-gates-2026-05-13.md`
- Anonymized proof snippet: `memory/proof-assets/2026-05-13-anonymized-ai-ops-proof-snippet.md`
- Status: proof-safe language exists.
- Risk: no named client/ROI/testimonial claims until explicit permission and measured evidence exist.

### Drive / deck status

- `python3 scripts/pipeline_drive_sync.py --list` confirms `Eve — Drafts / Consulting / Strategy Jobs / 2026-05-13` exists.
- Client deck/outreach Drive sync script exists: `scripts/pipeline_drive_sync.py`.
- No unsafe external send was performed.

### Website hidden/public status

- `/property-family-office-ai-ops` has `robots: { index: false, follow: false }`.
- `/guyana` has `robots: { index: false, follow: false }`.
- Both are hidden/noindex and should remain that way until JT intentionally approves public indexing.

## Files changed

1. `memory/consulting/offer-asset-index-2026-05-13.md`
   - Created canonical asset hierarchy, source paths, use cases, gates, Drive/source-of-truth status, hidden/public status, and proof-safe claim rules.
2. `memory/consulting/buyer-facing-one-pager-checklist.md`
   - Created pre-send/pre-upload checklist for one-pagers and deck inserts.
3. `memory/drafts/ai-operations-diagnostic-one-pager.md`
   - Added source-of-truth note marking it as the general fallback, not the current canonical referral asset.
4. `memory/audits/xhigh-systems/2026-05-13-offer-deck-onepager-assets.md`
   - This report.

## Tasks changed

- Updated existing MC task: `Property/Family Office: package diagnostic as call-ready one-pager`
- Task id/status: `j57cbhgfre12ctpy5f0pdtkn9186nqzt`
- Change: replaced generic legacy description with a concrete first action, why it matters, done state, source files, Drive upload requirement, and proof guardrails.

## Validation

```json
{
  "index_created": "present",
  "checklist_created": "present",
  "generic_one_pager_has_source_note": true,
  "property_page_noindex": true,
  "guyana_page_noindex": true,
  "mc_task_updated": "j57cbhgfre12ctpy5f0pdtkn9186nqzt"
}
```

Additional validation performed:

- Required bootstrap size check: `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md` returned within budgets.
- Asset inventory searched local workspace and `~/projects` for offer/deck/one-pager/diagnostic/proof/Guyana/Altmark assets.
- Mission Control API read succeeded via `GET http://localhost:3000/api/tasks`.
- Drive listing succeeded via `python3 scripts/pipeline_drive_sync.py --list` and showed Strategy Jobs Pack folder.

## Remaining blockers

1. **A+ blocker:** upload the Property/Family Office call-ready one-pager to Drive and link it back in `memory/consulting/offer-asset-index-2026-05-13.md`.
2. **Proof gate blocker:** Altmark acceptance/payment/proof permission gates must be resolved before Yair/family-office referral ask.
3. **Strategy drift blocker:** keep older Guyana government/city-services demo docs parked unless a specific warm government/partner meeting exists.

## Recommendation

Do not create more consulting strategy assets right now. The next highest-leverage move is packaging the Property/Family Office one-pager into a Drive-ready review asset, then using it only after Altmark proof/referral gates are clean.
