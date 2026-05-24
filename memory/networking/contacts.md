# Warm Contacts Log
> Canonical relationship/referral tracker. Updated 2026-05-13 by xhigh relationship/referral audit.
>
> Default rule: no referral ask unless the contact has (1) current touch date from a real-world interaction, (2) specific fit criteria, (3) proof/permission gate satisfied when client proof is referenced, and (4) a concrete next action owner/date.
>
> **Hard no-ask rule:** notes, scripts, strategy docs, or generated assets are not relationship touches. If the latest real-world touch/outcome is unknown, the contact is refresh-only. Do not use the contact for referral, intro, testimonial, proof, or sales asks until this ledger is updated.

## Contact Fields / Checklist

Each contact should include:
- **Relationship source:** client, warm intro, family/network, event, cold outreach, ecosystem.
- **Warmth:** 🔥 Hot = touched ≤7 days and active; 🟡 Warm = touched ≤30 days or pending; 🧊 Stale = >30 days/no outcome captured; 🚫 Blocked = do not ask until gate clears.
- **Last touch:** exact date + what happened. If unknown, mark `unknown` and make the next action a refresh/logging step.
- **Next action:** one specific action with owner/date or explicit blocker.
- **Referral gate:** `Open`, `Blocked`, or `Validation-only`; include why.
- **Privacy/proof constraints:** what cannot be said/shared.
- **MC alignment:** matching task title or `needs task`.

## Refresh Ledger — Required Before Any Ask

| Path | Current ledger status | Blocking unknown | Refresh owner | Allowed action before refresh |
|---|---|---|---|---|
| Yair / Altmark | Blocked for referral ask | PC handoff/access path, insurance workflow acceptance/payment, redacted proof, exact latest client response | JT confirms source-of-truth outcome; Eve updates gates after evidence | Client delivery/acceptance/payment/proof cleanup only |
| Gil / Aya | Blocked for referral ask | 2026-03-20 meeting outcome, active deliverable status, accepted proof-safe evidence, permission/anonymization boundary | JT confirms latest Aya/Gil status; Eve updates Aya proof checklist | Relationship/status refresh only |
| Richard Leo / AmCham Guyana | Validation-only after refresh | Whether the agreed call happened and what was learned | JT confirms call outcome or explicitly parks | No ask; optionally park |
| Dad / Guyana family network | Validation-only after send/status log | Whether JT sent the family-network ask, who surfaced, and whether the path remains useful | JT confirms send/status; Eve logs names only after JT review | Ask may be sent only as validation text; no sales/referral conversion |

### Ask Eligibility Matrix

| Ask type | Minimum gate | If missing |
|---|---|---|
| Relationship refresh | Current contact context + one narrow question | Allowed |
| Validation / learning intro | Last touch/status known + no client proof claim + no favor/access framing | Block until status logged |
| Referral ask | Last touch/status known + fit criteria + proof gate open + privacy constraints logged | Block |
| Proof/testimonial ask | Accepted deliverable + evidence captured + permission/anonymization boundary | Block |
| Event follow-up | Exact event/date/person met + relationship value logged | Block |

## Active / Recently Relevant Contacts

### Yair — Altmark Group — CFO / Family-office referral path
- **Relationship source:** Active client / paid implementation.
- **Warmth:** 🚫 Blocked for referral ask until acceptance/payment/proof gates clear and current real-world touch outcome is captured.
- **Last touch:** Unknown current client outcome. 2026-05-13 notes/assets were updated, but internal asset creation is not a touch.
- **Next action:** JT uses `memory/clients/altmark-group/proof-assets/monday-closeout-sheet-2026-05-25.md` if no weekend reply exists to confirm latest Altmark/Yair status: PC/admin access path, insurance workflow acceptance/payment, proof capture, and whether the engagement feels complete/positive. Eve then updates `memory/clients/altmark-group/proof-assets/referral-readiness-gate-2026-05-23.md` before any Yair intro ask.
- **Referral gate:** Blocked — PC handoff/access path, insurance workflow acceptance/payment clarity, and redacted proof capture must be clean first.
- **Fit criteria:** NYC family offices/property operators with manual insurance, rent delinquency, QuickBooks/local-file, reporting, deadline, or approval-heavy workflows.
- **Privacy/proof constraints:** Do not name Altmark publicly, do not imply rent delinquency is live, do not claim ROI/hours saved/records tracked without measured evidence, no blast ask to all ~15 offices.
- **MC alignment:** `Altmark: ask Yair for 2–3 family-office intros after acceptance`.

### Dad / Family Network — Guyana warm-intro validation
- **Relationship source:** Family/network trust bridge.
- **Warmth:** 🟡 Prepared but unconfirmed — validation-only after send/status is logged; not a sales/referral path.
- **Last touch:** Unknown. 2026-05-13 scripts were created, but send status is not captured here.
- **Next action:** JT either sends the dad/family-network validation ask from `memory/research/guyana/guyana-intro-ask-scripts-2026-05-13.md` or confirms if it was already sent; Eve logs send date, names surfaced, and whether to continue/park.
- **Referral gate:** Validation-only — ask for people who understand supplier/admin/compliance/procurement pain, not customers to pitch.
- **Fit criteria:** Guyana-connected private-sector operators/advisors/suppliers/compliance/admin/procurement/accounting people close to local-content/oil-and-gas supplier workflows.
- **Privacy/proof constraints:** No government favors, no political access, no “foreign consultant” posture, no broad AI transformation claim, no implied local access beyond actual intros.
- **MC alignment:** `Guyana: ask dad/family network for supplier/operator intros`.

### Gil — Aya — Co-living / Construction
- **Relationship source:** Client engagement (construction dashboard).
- **Warmth:** 🧊 Stale in tracker — last logged touch is >30 days old; do not treat as currently hot until refreshed.
- **Last touch:** 2026-03-19 logged prep only; 2026-03-20 meeting outcome and current client status are not captured in this file.
- **Next action:** JT confirms the 2026-03-20 conversation outcome plus current dashboard/scraper/co-living status before any referral ask. If useful output/acceptance proof exists, Eve updates `memory/clients/aya/proof-evidence-checklist.md` first.
- **Referral gate:** Blocked — Aya/Gil-specific acceptance evidence, useful output confirmation, and redaction boundaries are incomplete in the cross-client proof gate.
- **Fit criteria:** Construction subs, maintenance vendors, material suppliers, property owners/operators with the same visibility/status-tracking pain.
- **Privacy/proof constraints:** Do not overclaim dashboard results; do not use Aya name/proof publicly unless permission is captured.
- **MC alignment:** `Aya co-living dashboard — quoted $2,500, awaiting approval` plus proof gate in `memory/clients/proof-pipeline-gates.md`.

### Richard Leo — AmCham Guyana — Executive Director
- **Relationship source:** Cold email / ecosystem conversation.
- **Warmth:** 🧊 Stale in tracker — last logged touch is >30 days old; may still be valuable but needs outcome refresh.
- **Last touch:** 2026-03-19 — replied positively, agreed to call next Thursday.
- **Next action:** JT confirms whether the agreed call happened and logs one outcome: useful market insight, intro path, no-show, or park. Do not treat Richard as an active gateway until that outcome exists.
- **Referral gate:** Validation-only until current relationship status is known.
- **Fit criteria:** Guyana private-sector ecosystem leads who can explain market constraints and supplier/admin pain.
- **Privacy/proof constraints:** Do not ask for government access or political leverage; listening posture only.
- **MC alignment:** Related to `Guyana: ask dad/family network for supplier/operator intros` but needs separate task only if the family-network path produces no leads.

### Robert Oswald — H.C. Oswald Supply — Owner
- **Relationship source:** Cold outreach / LinkedIn InMail.
- **Warmth:** 🧊 Stale pending connection outcome.
- **Last touch:** 2026-03-18 — connection request sent by JT.
- **Next action:** Do not surface as relationship/referral priority unless connection accepted or acquisition reset selects wholesale again.
- **Referral gate:** Blocked — not a warm referral relationship.
- **Fit criteria:** Wholesale distribution catalog/order/inventory workflow pain.
- **Privacy/proof constraints:** Use only approved demo/outreach assets; JT sends any message.
- **MC alignment:** none active; H.C. Oswald is intentionally held until site/demo polish per USER.md.

## Weekly Review Questions

Use these during the Monday relationship check:
1. Which contacts are incorrectly marked Hot despite >7 days without a logged touch?
2. Which next actions are stale because the planned meeting/send already passed?
3. Is the ask a proof/referral ask, a validation ask, or just a relationship refresh?
4. If proof is mentioned, does the relevant client proof gate allow it?
5. Is the ask narrow enough for the contact to qualify 2–3 people instead of blasting a network?
6. Are family/private-network asks framed as learning/validation, not pressure or leverage?
7. Does Mission Control have exactly one concrete next task for the relationship, not duplicate strategy tasks?

## Change Log

- 2026-05-13: Rebuilt tracker with gating fields; downgraded stale March contacts; added Yair/Altmark and Guyana family-network paths; made proof/referral blockers explicit.
- 2026-05-13 hardening: Added hard no-ask rule, refresh ledger, ask eligibility matrix, and JT-owned refresh requirements for Yair/Altmark, Gil/Aya, Richard Leo, and Guyana family-network status.
