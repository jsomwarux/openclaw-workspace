# Altmark Proof / Permission / Referral Gates — 2026-05-13

Purpose: keep Altmark revenue, proof, and referrals sequenced so JT can convert the work into assets without overclaiming, exposing client data, or asking too early.

## Canonical Gate Order

Do not move to the next gate until the prior gate is true or explicitly deferred in notes.

1. **Acceptance/payment clarity gate**
   - PC handoff/access path is confirmed.
   - Insurance-expiration workflow is demonstrated or dry-run verified.
   - Yair/Navid acceptance wording is captured.
   - Insurance workflow payment/approval status is known.
   - Rent-delinquency deposit timing is known separately from data-readiness cleanup.
   - No rent-delinquency build starts until a cleaned sample report is approved.

2. **Proof capture gate**
   - Capture only redacted evidence: workflow/status tracker, run log/audit trail, local infrastructure/folder view, open-items tracker, acceptance wording.
   - Remove tenant names, account numbers, policy numbers, internal financials, credentials/tokens, private file paths, and unapproved metrics.
   - Save evidence or notes under `memory/clients/altmark-group/proof-assets/`.
   - Fill `referral-proof-package-template.md` with verified facts only.

3. **Permission/anonymization gate**
   - Default public posture: anonymized NYC family-office/property-ops proof.
   - Do not name Altmark, Yair, Navid, Matt, or any internal workflow detail publicly unless JT has explicit permission.
   - Do not claim hours saved, records tracked, exceptions surfaced, or ROI unless measured.
   - Label paraphrased acceptance as paraphrase; use exact quotes only when captured.

4. **Referral ask gate**
   - Ask Yair for 2–3 qualified intros only after acceptance/payment clarity is clean and proof capture is safe.
   - Use `memory/consulting/yair-family-office-intro-ask-2026-05-13.md`.
   - Ask for fit-qualified intros, not a blast to all ~15 family offices.
   - First referred-prospect frame: diagnostic around manual reporting/document deadlines/local files/approval-heavy workflows — not generic AI.

5. **Distribution gate**
   - AI Ops Teardown/content may be published while anonymized, but must not imply the full Altmark system is live or that rent delinquency is automated.
   - Any posted URL or measurable reply becomes a proof asset only after it is logged in `memory/content/posted-log.jsonl` or the relevant proof file.

## Cross-Client Source

This Altmark gate rolls up to the broader proof system at `memory/clients/proof-pipeline-gates.md`. If the broader gate and this file conflict, use the stricter rule.

## Quick Decision Rule

If the next action would increase trust, payment clarity, verified proof, or qualified referrals: proceed.
If it requires an unverified claim, public naming, broad blast, or automation against dirty data: stop and gather evidence first.
