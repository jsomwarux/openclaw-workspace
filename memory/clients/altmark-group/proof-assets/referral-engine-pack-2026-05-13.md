# Altmark Referral Engine Pack — 2026-05-13

Purpose: turn the Altmark implementation into a usable referral engine for NYC family-office/property-ops buyers without overclaiming, exposing private client details, or asking Yair too early.

## Executive Recommendation

Use Altmark as a **post-delivery referral wedge**, not a public case study yet.

Best next move: finish the PC handoff, get explicit acceptance on the insurance expiration workflow, clarify payment/deposit status, capture redacted proof, then ask Yair for **2–3 highly relevant family-office introductions**.

The offer should be framed as:

> Local-first AI operations systems for family offices and property operators where sensitive workflows live across local files, QuickBooks/Desktop-style tools, AppFolio exports, spreadsheets, inboxes, and manual follow-up.

Do not lead with “AI.” Lead with the operational outcome: **exception visibility, audit trail, human approval, and cleaner handoffs around existing systems.**

## What Proof Exists Now vs What Still Needs Capture

### Proof that exists now

Evidence from existing notes:
- Yair, Altmark CFO, initiated contact with JT on Twitter and invited JT to the Bronx office.
- JT prepared a revised AI Operations Build proposal for Altmark in April 2026.
- Foundation infrastructure was scoped at $4,000 and paid in full at kickoff per proposal terms.
- Insurance Expiration Tracking was scoped at $2,250 and is marked finished in the client status notes.
- Dedicated workflow PC setup is marked done and planned for office delivery/handoff.
- The engagement is local-first/self-hosted because sensitive data, QuickBooks/Desktop-style environment, files, and auditability matter.
- Rent delinquency is paused because Altmark’s tenant ledger/reporting hygiene is not clean enough yet. This is a strong implementation-judgment proof point: JT is not automating against dirty inputs.
- Yair may be able to connect JT to roughly 15 NYC-area family offices interested in similar systems.

### Proof still needed before asking for referrals

Capture before using Altmark as the referral engine:
- Confirm PC handoff completed or remote access path accepted.
- Confirm insurance expiration workflow was demonstrated or dry-run verified.
- Confirm logs/audit trail were shown.
- Get acceptance wording from Yair/Navid: exact quote if possible, otherwise a paraphrase labeled as paraphrase.
- Confirm insurance workflow payment/approval status.
- Confirm rent-delinquency deposit timing separately from data-readiness cleanup.
- Capture redacted screenshots:
  - workflow/status tracker
  - log/audit trail
  - folder or local infrastructure view that shows ownership without exposing secrets
- Capture first usable metric, if true and verified:
  - records tracked
  - exceptions surfaced
  - manual review time reduced
  - missed-expiration risk reduced

### TODO / missing evidence

- Exact live acceptance wording is not in the notes yet.
- Exact payment status for the insurance workflow is unknown.
- Exact number of records/policies tracked is not in the notes yet.
- Exact time saved is not verified yet.
- Permission to name Altmark publicly is not present. Default to anonymized proof.

## Anonymized Proof Narrative JT Can Use

Short version:

> I recently built a local-first automation setup for a NYC family-office/property-ops team. The first workflow focused on insurance expiration tracking: keeping sensitive files inside their environment, surfacing upcoming/overdue exceptions, and showing an audit trail so the team could review what changed without replacing their existing systems.

Slightly fuller version:

> The useful part was not “AI magic.” It was implementation judgment. The team had sensitive operational workflows spread across local files, reports, and manual follow-up. Instead of forcing a new SaaS tool, we built a local workflow path: track the insurance expiration process, surface exceptions, show logs/audit trail, and keep human approval around anything sensitive. The next workflow, rent delinquency, is intentionally gated until the source report and tenant ledgers are clean enough to trust.

Referral-context version:

> This is the pattern I think applies to a lot of family offices: the data is valuable, the workflows are recurring, but the environment is too sensitive or too desktop/local-file-heavy for generic SaaS. The right first step is a diagnostic: map the workflows, find the exception layer, confirm data readiness, then build one narrow system with audit trail and human approval.

## Screenshot / Proof Checklist for PC Handoff

Only capture redacted, non-sensitive evidence. Do not include tenant names, account numbers, policy numbers, vendor private details, internal financials, credentials, tokens, file paths containing secrets, or unapproved metrics.

### Before handoff
- PC boots cleanly.
- Automation folder structure visible.
- Credential storage approach documented but secrets hidden.
- Backup/export path documented.
- Insurance workflow dry-run passes.
- Any local-only dependency documented.

### During handoff
- Photo/screenshot: dedicated workflow PC installed or accessible.
- Screenshot: redacted workflow/status tracker.
- Screenshot: redacted run log/audit trail.
- Screenshot: open-items tracker with owner/date, if created.
- Note: who attended and who confirmed what.
- Note: Yair/Navid acceptance wording.

### After handoff
- Before/after mini-map:
  - before: manual insurance tracking across files/spreadsheets/team memory
  - after: local workflow + exception review + logs/audit trail
- Metric slot:
  - records tracked: TODO
  - exceptions surfaced: TODO
  - review time saved: TODO
  - missed-expiration risk reduced: qualitative unless measured
- Caveat slot:
  - rent delinquency is not live yet because data readiness is still being cleaned up.

## Referral Offer Framing

Offer name: **Family Office AI Operations Diagnostic**

Plain-English framing:

> A short diagnostic for family offices and property operators that want AI/automation but need it around existing systems, sensitive files, local/desktop workflows, audit trail, and human approval.

What the diagnostic produces:
- Current-state workflow map.
- Source-system and report/export readiness review.
- Exception inventory: overdue, missing, changed, risky, approval-needed.
- Human-in-the-loop rules: what can be flagged, drafted, summarized, or prepared, and what must require approval.
- Ranked first-build candidates by ROI, risk, data readiness, implementation complexity, and proof value.
- Recommended first build with acceptance criteria, timeline, and dependencies.

Best first-build categories:
- Insurance / COI / vendor document expiration tracking.
- Rent delinquency reporting and approved outreach prep.
- Loan/debt deadline tracking.
- QuickBooks / bank / cash-risk review queues.
- Owner-ready weekly exception brief.
- Local-first workflow host for sensitive operations.

Recommended referral ask:

> “Could you introduce me to 2–3 family offices where manual reporting, renewals, collections, QuickBooks/local-file workflows, or document follow-up are a real operational headache?”

## Warm-Intro Ask Variants for Yair

Use only after PC handoff, workflow acceptance, and payment/deposit status are clean.

### Variant 1 — Short text

Yair, glad we got the first system live. Since this setup is built around the exact constraints a lot of family offices have: local files, sensitive docs, audit trail, and human approval, I think it could be relevant to a few of the other offices you mentioned.

Would you be comfortable introducing me to 2–3 where this kind of local-first automation would be useful?

### Variant 2 — Slightly warmer

Yair, now that the first workflow is live, I think there’s a clean way to explain this to other family offices: local-first automation for back-office workflows that are too sensitive, too manual, or too tied to existing systems for generic SaaS.

If you’re comfortable, I’d appreciate introductions to 2–3 offices where insurance tracking, rent delinquency, QuickBooks/bank reporting, document follow-up, or owner reporting are still manual.

I’d start with a diagnostic, not a broad pitch: map the workflow, check the data, and only recommend a build if there’s a clear first system worth implementing.

### Variant 3 — Most conservative / relationship-first

Yair, once we’ve fully closed the loop on the PC handoff and first workflow acceptance, I’d value your read on something.

You mentioned other family offices may have similar needs. If there are 2–3 where the fit is genuinely strong, would you be open to making a simple intro? I’d keep it narrow: a workflow diagnostic around manual reporting, document deadlines, local files, and approval-heavy back-office processes.

No broad AI pitch. Just a practical review of where automation would actually be safe and useful.

## Follow-Up Sequence After Yair Says Yes

### Step 1 — Ask Yair to qualify intros before sending names

> That would be great. The best fit is someone with recurring back-office workflows that are manual today: insurance renewals, rent delinquency, QuickBooks/bank reporting, document follow-up, owner summaries, or anything deadline/risk-heavy.
>
> If you can think of 2–3 where that pain is real, I’ll send you a short forwardable blurb.

### Step 2 — Send Yair the forwardable blurb

> Forwardable blurb:
>
> JT built a local-first automation setup for a family-office/property-operations workflow where sensitive files, existing systems, human approval, and audit trail mattered. The useful part is that it works around the tools already in place instead of forcing a new SaaS system. If you have manual insurance tracking, rent delinquency, QuickBooks/bank reporting, document follow-up, or owner-reporting workflows, it may be worth a short diagnostic conversation.

### Step 3 — After intro lands, JT reply to referred prospect

> [Name], good to meet you, and thanks Yair for the intro.
>
> I usually start these with a short workflow diagnostic, not a broad AI pitch. The goal is to map the manual reporting/approval bottlenecks, check whether the data is clean enough to build around, and identify the first workflow that would actually be safe and useful to automate.
>
> Curious what workflow is creating the most manual follow-up for your team right now?

### Step 4 — If referred prospect asks what JT built

> The recent example was a local-first workflow setup for a property/family-office environment. First workflow: insurance expiration tracking with exception visibility and audit trail. The important constraint was keeping sensitive files and approvals inside the client’s operating environment instead of forcing everything into another SaaS tool.

### Step 5 — If prospect wants a call

> Makes sense. A 30-minute diagnostic is enough for the first pass. I’d want to understand the workflow owner, source systems, current reports/exports, what fails when it gets missed, and what should never happen automatically.

## Risks / Do-Not-Say List

Do not say:
- “Altmark case study” publicly unless JT has explicit permission.
- “We saved X hours” unless measured.
- “The full system is live” because rent delinquency and other modules are not live yet.
- “AI handles rent delinquency outreach” because that workflow is gated by ledger/report cleanup and deposit timing.
- “Autonomous financial actions” or anything implying money movement without approval.
- “Generic AI consulting” or “AI agency.”
- “I can automate all of this” before diagnostic and data-readiness review.
- “Yair said you need this.” Keep the intro respectful and diagnostic-led.
- Any private Altmark detail: tenant names, policy details, accounts, ledgers, internal reports, staff issues, office-specific sensitive context.

Use instead:
- “local-first”
- “exception visibility”
- “audit trail”
- “human approval”
- “around existing systems”
- “workflow diagnostic”
- “data readiness before automation”
- “first safe build”

## Immediate Next Actions

1. Complete or confirm PC handoff path with Yair/Navid.
2. Run the insurance expiration workflow demonstration or dry-run verification.
3. Show logs/audit trail and write down open items with owner/date.
4. Ask for written acceptance: “Can you confirm this first workflow is accepted as live?”
5. Clarify insurance workflow payment/approval status.
6. Clarify rent-delinquency deposit timing, while keeping build gated on cleaned report/data readiness.
7. Capture redacted proof screenshots and acceptance wording.
8. Fill in `proof-assets/referral-proof-package-template.md` with verified facts only.
9. Send Yair one of the warm-intro ask variants.
10. Use the AI Operations Diagnostic one-pager as the first-call frame for any referred prospect.
