# JT Outbound Operating System v2

**Status:** Active as of July 2026. Supersedes all prior outreach sequencing, scoring, and messaging rules.
**Owner:** JT Somwaru. All sends are manually reviewed and sent by JT. Agents research, score, draft, and log. Agents never send.
**Context:** Prior system produced 0 replies across multiple months. Root causes: visibility/volume failure, proof buried in M2, developer-facing offer names, channel-ICP mismatch, homework CTAs.

---

## 1. Diagnosis Summary (why v1 failed)

Ranked by likelihood times impact:

1. **Visibility failure and starved volume.** DMs gated behind unaccepted connection requests never render. Unverified email deliverability may be routing to spam. The contact-completeness rule (LinkedIn URL AND verified email) strangled the send-ready pool. Drafts synced to Drive are not sends. Absolute zero signal (no accepts, no negative replies) points to messages not being seen.
2. **Proof buried in M2.** Production proof at a real NYC PM firm is the only differentiator, and the old M1 rule withheld it. The no-proof-in-M1 rule is dead. Proof claim goes in M1, always.
3. **Offers named in JT's language, not the buyer's.** Nobody buys n8n or a Context OS. They buy not getting burned by a lapsed vendor COI. Prices fine, names replaced.
4. **Channel-ICP mismatch plus ignored warm channel.** LinkedIn-first is wrong for trades. Referral asks to Yair, Gil, Karen, and Sam Foy were never systematized. Warm intros are the highest-probability next signed deal.
5. **Homework CTAs.** "Curious what that process looks like right now?" asks a stranger for unpaid effort. CTAs are now concrete yes/no asks tied to visible proof.

**Open data gap:** total historical sends by channel was never tracked. Action 1 in Section 8 closes this.

---

## 2. Strategic Shift Rules

- Proof claim in M1 copy, always. One sentence: built, running, for whom (anonymized), what it catches.
- Artifact placement: LinkedIn M1 carries the one-pager image inline. Email M1 carries no link (deliverability protection). Email M2 delivers the artifact link unconditionally.
- Artifacts are hosted at jtsomwaru.com/proof/ with analytics enabled. Loom for video, PNG for DMs, PDF for email.
- Honest framing only: "This exists. It runs today at a firm like yours. Making it yours takes two to three weeks, flat fee." Never imply bespoke work that is a template.
- Build once per niche, personalize one sentence per prospect. No custom builds, decks, or demos before a first reply, including T1.
- Artifact-building phase is capped at three assets (Section 4). After that, sending is the job.

---

## 3. 30-Day Outbound System

### ICP priority
- 80 percent: NYC metro property management firms, roughly 200 to 3,000 units, rent-stabilized exposure or AppFolio/Yardi/Buildium signals.
- 20 percent: NYC GCs and specialty trades running multi-unit jobs.
- Paused to trigger-only: wholesale distribution, Agentforce/insurance.

### Scoring: four binary gates (replaces 0-100 score)
1. Niche has a live proof asset.
2. Reachable channel: verified email OR accepted LinkedIn connection. Not both required.
3. Named buyer: principal or director of ops. Under 500 units, the owner.
4. Trigger bonus: ops job posting, portfolio growth, PM software in stack, heavy stabilized portfolio.

- All four gates = T1.
- Gates 1-3 = T2.
- Anything less = dead, do not load.
- Research cap: 10 minutes per prospect, 15 for T1. Hard stop.

### Minimum proof rule
No live artifact for the niche means no sends to the niche. This currently kills wholesale outbound. Correct behavior.

### Sequence A: property management (email primary)
| Day | Touch | Content |
|-----|-------|---------|
| 1 | Email M1 | Proof claim in copy, no link, concrete yes/no CTA |
| 2 | LinkedIn connection request | Blank or one non-pitch line |
| 4 | LinkedIn DM (if connected) | One-pager PNG attached |
| 5 | Email M2 | Loom link delivered unconditionally |
| 10 | Email M3 | Second angle: DHCR renewals or arrears |
| 18 | Email breakup | Close loop plus referral ask. Recycle in 90 days |

### Sequence B: trades (email plus phone)
| Day | Touch | Content |
|-----|-------|---------|
| 1 | Email M1 | One-pager link included |
| 4 | Phone call | Office line. Reference the email |
| 8 | Email M2 | Loom walkthrough |
| 15 | Email breakup | Close loop |

### Volume targets
- 15 new prospects fully launched per week.
- 60 per month, roughly 200 total touches.
- Realistic solo with manual review if research caps hold.

### Stop rules
- Full sequence, no reply: archive.
- Email bounced plus no connection accept within 7 days: dead.
- Zero bespoke work pre-reply, no exceptions.
- Maximum one message-variant change per week.

---

## 4. Proof/Artifact Stack

Build these three in order. Nothing else until all three exist.

### Asset 1: COI Compliance Autopilot proof pack
- **Niche:** property management.
- **Pain:** lapsed vendor certs mean liability exposure and lender/insurance compliance failures.
- **Shows:** status sheet with color-coded expirations, auto-drafted vendor chase email, 30/14/7-day internal alert.
- **Format:** one-page annotated PNG/PDF plus 90-second Loom. Names redacted.
- **Build time:** 3 to 4 hours.
- **Plugs in:** PNG in LinkedIn M1, hosted link in email M2.

### Asset 2: Job Status Dashboard pack
- **Niche:** GCs and trades.
- **Pain:** owner cannot answer "where are we on 4B" without three phone calls.
- **Shows:** live Aya dashboard, floor by floor, project details blurred. Requires Gil's permission.
- **Format:** 60-second Loom plus one snapshot PNG.
- **Build time:** 2 hours.

### Asset 3: Arrears Follow-up one-pager
- **Niche:** property management, second angle.
- **Pain:** delinquency chasing is inconsistent and unlogged.
- **Label:** "currently deploying at the same Bronx firm." Honest status only.
- **Build time:** 2 hours.
- **Note:** DHCR renewal tracker becomes angle four once the Matt proposal closes.

### One-pager spec (Asset 1)
- **Header:** "Vendor COIs expire. This system notices before you do."
- **Body:** three stacked annotated screenshots: compliance sheet, auto-drafted chase email, alert.
- **Footer:** "In production at a Bronx property management firm since spring 2026. Flat-fee setup, two to three weeks, runs on the email and sheets you already use."
- **Redaction:** all names, addresses, unit identifiers.
- **Output:** PNG for DMs, PDF hosted at jtsomwaru.com/proof/coi with analytics on.

---

## 5. Offer Framing (outbound names)

| Outbound name | Price | One-line pitch |
|---------------|-------|----------------|
| COI Compliance Autopilot | $3,500 flat, live in 2 to 3 weeks | Replaces spreadsheet-and-memory cert tracking. Flags expirations at 30/14/7 days, drafts the chase email, logs everything |
| Arrears Follow-up Engine | $3,500 | Turns the delinquency report into a consistent, logged tenant outreach sequence |
| DHCR Renewal Tracker | $3,500 Phase 1 | Rent roll in, renewal calendar and drafted notices out |
| Job Status Dashboard | $1,500 to $2,500 | Live progress from the tracking sheets the team already keeps |
| Ops Process Map | $2,500, credits toward any build | Two weeks. Maps intake-to-done workflows, delivers a prioritized automation plan. Discovery wedge |

**Universal positioning line:** fixed fee, fixed scope, you own everything, no subscription, no platform migration.

**Background line** (used once, M2 or profile, never M1): "Six years as a business systems analyst at Spectrum Enterprise taught me that automation fails when nobody maps the handoffs first. I map first, then build."

---

## 6. Message Templates

### a) NYC property management

**M1 email, no artifact**
Subject: vendor COIs at [Firm]
> Hi [Name], quick one. I built a system for a Bronx property management firm that watches every vendor COI, flags certs 30 days before they lapse, and drafts the chase email automatically. Running in production since spring. Worth a 90 second look at how it works?

**M1 LinkedIn, with artifact (post-accept)**
> Thanks for connecting, [Name]. One page attached on a COI tracking system I run for a Bronx PM firm. It catches expiring vendor certs and drafts the chase emails before anyone has to remember. If lapsed COIs have ever bitten you during a refi or a claim, happy to send the 90 second walkthrough.

**M2 email, artifact delivered unconditionally**
> Easier to show than describe. 90 seconds, real system, names redacted: [link]. If your cert tracking is already airtight, ignore me. If it is a spreadsheet someone checks when they remember, that is exactly what this replaces.

**Channel pivot, LinkedIn after email silence**
> Sent you a note by email last week on the COI system, may have hit spam. One-pager attached here instead. Worth a look?

### b) Plumbing/HVAC/trades

**M1 email, no artifact**
Subject: job status without the phone calls
> Hi [Name], I built a live progress dashboard for a NYC construction firm. Floor by floor, room by room, pulled from the tracking sheets the crew already keeps. The owner stopped calling supers to find out where jobs stand. Do you get that visibility today, or is it calls and memory?

**M1 with artifact:** same message plus "One page snapshot attached, details blurred."

**M2 email**
> Here is the 60 second walkthrough of the actual dashboard, project details blurred: [link]. Flat fee setup, two to three weeks, runs off your existing sheets. If Q3 jobs are stacking, this is the season it pays for itself.

**Pivot, second angle**
> Different question. How do service requests come in today, calls and texts into one person's phone? I turn that into a logged intake queue with automatic follow-ups. Happy to sketch what that looks like at your volume if you reply with a rough weekly call count.

### c) Wholesale distribution (HOLD until an artifact exists)

**M1**
> Hi [Name], most distributors I talk to have one person who just knows when accounts are due to reorder. I build systems that watch order history and flag accounts going quiet before they churn. Is that tribal knowledge at [Company], or systematized?

**M2 with artifact**
> One page on the reorder-radar pattern, built from production systems I run for NYC ops firms: [link]. If account managers are your early warning system today, worth five minutes.

---

## 7. Measurement Loop

### Track per prospect
niche, tier, buyer title, channel, variant ID, dates per touch, connection sent/accepted, email delivered or bounced, artifact views (Loom counts plus site analytics), reply and sentiment, kill reason.

### Signal thresholds
- Never judge a message variant under 30 sends.
- Never judge a channel under 100 touches.
- Funnel expectations for a tight ICP: connection accepts 25 to 40 percent, email delivery above 95 percent, artifact views 15 to 30 percent of delivered, replies 3 to 8 percent.

### Diagnostics
- Healthy views, zero replies at 50 sends: offer or CTA problem.
- Near-zero views: visibility problem. Fix plumbing, not copy.
- Under 2 percent replies at 100 clean touches: change offer or ICP, not adjectives.

### Weekly review (Friday, 30 minutes)
1. Sends versus target. If missed, nothing else in the review matters.
2. Funnel rates against thresholds.
3. One change maximum, logged in a decisions file.

---

## 8. Immediate Next 72 Hours

Execute in order. Each action is agent-executable or JT-executable as noted.

1. **Baseline and deliverability audit.** Count every touch ever sent, by channel, into one sheet. Verify SPF, DKIM, and DMARC on the sending domain. Seed-test to Gmail, Outlook, and Yahoo inboxes and log inbox versus spam placement. (Agent: audit and sheet. JT: DNS access and seed accounts.)
2. **Permission and referral asks.** Message Yair for anonymized-proof sign-off and a one-line testimonial. Message Gil for a named quote on the dashboard. Ask Yair, Gil, Karen, and Sam Foy each for one intro to an operator who fights these problems. (JT sends. Agent drafts.)
3. **Build the COI proof pack** to the Section 4 spec: record the 90-second Loom, produce the one-pager, host at jtsomwaru.com/proof/coi with analytics enabled. (JT records Loom. Agent builds one-pager and page.)
4. **Rebuild the list:** 40 NYC PM firms, 200 to 3,000 units, passing all binary gates, 10-minute research cap each, verified email or LinkedIn (not both required), loaded into the tracker with Section 7 fields. (Agent.)
5. **Launch week one:** send the first 15 M1 emails Monday through Wednesday, LinkedIn connections the following day, log every touch and every artifact view. (JT sends. Agent logs.)

---

## Agent Rules (pipeline compliance)

- Agents never send outreach. Draft, score, log, sync only.
- Research caps are hard stops: 10 minutes standard, 15 minutes T1.
- No custom builds, decks, or demos generated pre-reply for any tier.
- Any factual claim in a draft about a prospect must carry a source link or an UNVERIFIED flag.
- Wholesale and Agentforce prospects are logged as market-sensing only. No drafts generated.
- Variant IDs required on every draft so the measurement loop can attribute results.
