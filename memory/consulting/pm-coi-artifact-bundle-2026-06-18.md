# PM COI Artifact Bundle - 2026-06-18

Status: review-ready draft packet. JT sends nothing until he approves. Use only anonymized or synthetic data.

Drive: https://docs.google.com/document/d/1_TLbeYj4J4ubaUAG-OhqdAnjwhTC1xU-IUjcMYr-ZSI/edit

Sprint control: `memory/consulting/pm-artifact-led-outreach-sprint-2026-06-18.md`

## Asset
Vendor COI / insurance-expiration tracker for property-management operators.

## Buyer Problem
Property teams do not need another generic AI assistant. They need a daily view of which vendor insurance certificates are expired, expiring soon, missing proof, or blocked on unclear ownership before a gap becomes a liability issue.

## Proof-Safe Demo Shape
Use dummy rows only.

Columns to show:
- Vendor
- Property
- Certificate type
- Expiration date
- Days remaining
- Status
- Exception reason
- Follow-up owner
- Recommended next action
- Approval state
- Evidence link
- Last checked

Demo statuses:
- Current
- Expires in 30 days
- Expires in 14 days
- Expires in 7 days
- Expired
- Missing certificate
- Manual review

Manual-review examples:
- Missing expiration date
- Vendor name mismatch
- Certificate type unclear
- Owner approval required
- Duplicate vendor record
- Email not verified

## 60-90s Loom Outline
1. Open with the operational pain: "This is the kind of property-management workflow that quietly becomes expensive when nobody owns the exception."
2. Show the source input: a vendor certificate list or inbox export with expiration dates and missing proof.
3. Show the tracker: each row lands in current, expiring, expired, missing, or manual review.
4. Show the exception queue: unclear or risky rows do not get automatic vendor emails.
5. Show the approved action: routine rows can draft a vendor follow-up, but a human reviewer approves before anything external goes out.
6. Close with the buyer result: "The point is not AI sending messages. The point is seeing what changed, who owns it, and what needs approval before a cert lapses."

## Annotated Screenshot Copy
Suggested screenshot title:
Vendor COI Tracking: Expiring Certificates And Review Queue

Callouts:
1. Source data stays simple: vendor, property, certificate type, expiration date.
2. Expiration windows are visible at 30, 14, and 7 days.
3. Missing or unclear rows go to manual review instead of normal follow-up.
4. Each row has a follow-up owner and approval state.
5. The audit trail shows what changed and who approved the next action.

Caption:
This is the useful first layer for PM automation: not an autonomous bot, a review queue that catches expiring or missing vendor insurance before it becomes a liability problem.

## One-Page Buyer Note
### Vendor COI Tracking That Catches The Gap Before It Becomes A Problem

Most property-management teams already have the information somewhere: vendor certificates, expiration dates, renewal emails, property assignments, and staff knowledge.

The issue is that the exception is usually not visible until someone asks:
- Which certificates expire this month?
- Which vendors are missing proof?
- Which property is exposed if the certificate lapses?
- Who owns the follow-up?
- Which rows are too unclear to automate?

The workflow I would show first is narrow:
1. Pull the current vendor/certificate list from the existing source.
2. Classify every row by status and expiration window.
3. Hold unclear, missing, or risky rows in manual review.
4. Draft routine vendor follow-up for approved rows.
5. Leave an audit trail showing what changed and who approved the next step.

The useful outcome is not "AI for property management."

It is a daily queue that shows what changed, who owns it, and what needs approval before a COI expires.

## Artifact-Led M1 Template
Use this for the first PM batch only after buyer role and channel status are verified. Replace bracketed text before sending.

Subject: vendor certificates

[First name], noticed [Company] manages [specific portfolio or portal/software signal]. I put together a short example of a vendor COI tracker that flags expiring certificates, missing proof, and review-needed rows before anyone emails the vendor.

Short look: [Loom or screenshot link]

Curious what your team uses for that today?

## Pre-Output Checklist
- [x] No em dashes in the draft message.
- [x] Subject line present, 2 words, lower-case, internal-looking.
- [x] M1 proof rule honored: reusable anonymized/synthetic PM artifact, not named-client proof.
- [x] CTA is reply-sized.
- [x] No signature block in M1.
- [x] Individual signal required before send: portfolio, portal/software, role, post, job opening, or leadership signal must be inserted.
- [x] Opener format: observation plus artifact.
- [x] Anti-patterns checked: avoids assertive pain opener, binary close, self-promotional opener, pitch-first named proof, and niche-generic hook.

## First-Batch Prospect Fit
Start enrichment with the top five from `memory/consulting/nyc-property-management-lookalike-list-v1-2026-06-12.md`:
1. Z+G Property Group
2. MyPropertyMan
3. Clinton Management
4. Lisa Management
5. NYC Management / Besen Partners

Before send-ready status:
- Verify one operator/buyer LinkedIn profile URL.
- Verify one email address.
- Dedupe against pipeline files and existing tasks.
- Pick only one artifact angle per prospect.

## Guardrails
- Do not name Altmark, Aya, Yair, Navid, Matt, or any private client.
- Do not use private screenshots, tenant/vendor data, balances, addresses, policies, or internal file paths.
- Do not claim measured ROI, hours saved, or client endorsement unless verified and permissioned.
- Do not build custom demos, decks, or individual client folders before reply.
- Stop after two LinkedIn touches plus one email pivot if there is no response.
