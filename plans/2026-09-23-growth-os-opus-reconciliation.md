# AI Workflow Growth OS — Opus Brief Reconciliation

**Date:** 2026-09-23  
**Input:** `media/inbound/openclaw-staged-d0d04c51-0ad9-4a61-9ea9-cb90c69677aa/input-growth-os-update-brief-2026-09-23---97ec18c1-cf3b-4629-9cf5-d140c05fc4f0.md`  
**Status:** Strategy decision memo. No push, merge, deployment, activation, schedule, credential, or send is authorized by this document.

## Executive decision

The brief is right about the commercial bottleneck and too broad about the response.

The Growth OS needs more reachable buyers and more approved sends. It does **not** need a system that researches every niche, generates three automation ideas per company, or treats 100 sends as the scoreboard. That would recreate the research-without-revenue failure the brief correctly identifies.

Adopt now:

1. Instantly as the selected volume-delivery platform, initially through a manual CSV bridge.
2. Two research tiers: high-touch Tier A and evidence-bounded Tier B.
3. Property-first segment templates and batch approval for exact Tier B rows.
4. A canonical suppression owner mirrored into Instantly.
5. Send/outcome receipts and a reply-card loop.

Modify:

1. `100/day` is a warmed-capacity target, not a minimum daily achievement metric. The operating metric remains **two priced conversations per week**; the scoreboard remains **cash collected**.
2. Research may generate two or three hypotheses internally, but an email leads with **one** evidence-backed problem and one relevant proof line. Listing three automations in cold copy will usually read as generic AI prospecting.
3. The volume rail stages approved rows into a paused campaign. JT still presses the final launch/send control. Replies are drafted and reviewed in Mission Control, but JT still sends the reply.
4. Multi-model grading and designed artifacts are used only where consequence or buyer-facing clarity justifies the cost—not as defaults.

Do not prioritize during the first 30-day outbound window:

1. Broad multi-niche expansion beyond the current property wedge.
2. A daily “human behavior” research engine.
3. Segments 4–7 as active cold targets.
4. A new daily quota cron/card system.

The 90-Day Playbook and its freeze were retired on 2026-09-08, so no freeze override is required. These items are deferred because list quality, campaign proof, and priced conversations are the current bottlenecks. Property managers, property owners, warm-network developers/GCs, and commercial landlords remain the first commercial wedge; broader niches re-enter only after measured reply data or a direct buyer trigger.

## 1. What actually changes

### Already covered by the current OS

- Instantly/Smartlead as a future delivery rail was already specified in the Growth OS v2 plan. The new fact is that **Instantly was selected and JT reports that mailboxes/domains were purchased**.
- The authority model already exists: admission, gate, verified-channel owner, gate-attestation owner, review authority, suppression owner, proof card, immutable review snapshots, and append-only outcomes.
- Tier A already exists as the five-prospect cohort path.
- The universal seven-field Mission Control card contract already exists.
- The synthetic inactive no-send release proof already passed.
- The manual-send rule already exists: JT approves and performs the send.

### Genuine additions

- A Tier B batch-review contract for exact rows.
- A list-source quality benchmark and list adapter.
- A paused-campaign Instantly staging adapter.
- A reply-event receiver plus reconciliation poll.
- A delivery/outcome mapping from Instantly IDs into jt-ops receipts.
- A property-first segment table that drives Tier B copy.

### Stale gates in the brief

The brief says to preserve `96a3dab`, PR #39, the four owner adapters, PR #33, and the synthetic no-send proof as future gates. They are historical gates, not remaining work. The current release boundary is:

1. Deploy merged n8n PR #9 inactive.
2. Run the single real cohort-two pilot.
3. Produce either a fail-closed no-cohort result or an exact five-prospect review packet.

Volume outreach may proceed through a manual Instantly bridge in parallel, but it must not displace this last proof loop.

## 2. Disagreements with the brief

### “At least 100 messages per day”

Disagree as an immediate hard quota. It rewards volume before list quality, deliverability, and copy are proven. Use a stepped gate:

- First batch: 25 exact, approved property-sector leads.
- First scale checkpoint: 50 delivered niche-consistent messages.
- Scale only if hard bounces are at or below 2%, complaints stay below 0.1%, suppression is correct, and at least one positive reply or buyer-confirmed pain is observed.
- Ramp toward 100/day only after those gates pass.

### “Include the two or three most valuable automations in outreach”

Disagree. Generate up to three hypotheses internally; choose one externally. The call can explore the other two. One true line plus one relevant pain is more credible than an AI-generated menu.

### “Research every niche”

Disagree during the 90-day cash mandate. The brief’s own R9 correctly deprioritizes this. Property-first volume plus warm inbound from other industries is the faster cash path.

### “Daily analysis of normal human behavior”

Defer. Source-backed job-post/process evidence is useful, but restarting a broad daily harvester before reply data exists adds another research loop. A bounded property-sector job-post harvest is allowed only when it directly feeds a live campaign.

### Autonomous send/reply after Mission Control approval

Reject under the standing outreach rule. Approval may authorize **staging**, not sending. JT presses launch/send in Instantly. The same rule applies to replies.

## 3. Decisions on the eight open questions

1. **Approval granularity:** Tier A stays one card per email. Tier B uses one daily segment batch card capped at 25 rows, with exact subject/body/source/proof hashes per row and row-level reject controls. One decision may approve the batch because every individual send is explicitly enumerated and immutable.

2. **Campaign and reply shape:** One paused campaign per `segment + sequence_version`, not one mega-campaign. Inbound events land at a hosted Mission Control/Convex HTTP owner; n8n/Mac Mini is not exposed publicly. A cursor-based API reconciliation poll repairs missed webhooks.

3. **List source:** Do not buy Apollo yet. Benchmark the first 100 property-sector records from Instantly’s available data against a manually verified gold set. Keep Instantly if at least 70% contain the correct owner/operations buyer and verified reachable email with no more than 5% invalid/wrong-person results. Otherwise test Apollo on the same companies and choose the winner. This is evidence-gated, not price-gated.

4. **Card types:** Two specialized card types sharing the seven-field base: `tier_a_outreach_review` and `tier_b_batch_review`. Combining them would weaken either high-touch evidence or batch usability.

5. **Research runtime/key:** n8n orchestrates deterministic collection and routing. Tier B uses the cheapest current extraction/classification model available through the existing protected Anthropic credential; Tier A uses a Sonnet-class synthesis pass only after evidence gates. No new provider, ensemble, or key is required before measured need.

6. **Suppression:** Mission Control + the append-only consulting owner remain canonical. Instantly’s global blocklist and lead status are mirrors. Suppression reasons are typed by scope and expiry: client/contact hold, active sequence, reply received, opt-out, hard bounce, wrong person, prior contact, and do-not-contact. A policy sequencing rule is not silently converted into a permanent contact block.

7. **Harvester sources:** Keep it paused initially. If the first 100 sends show that copy lacks evidence, restart only the property-sector job-post parsers first, then legally accessible incumbent feature-request/community sources. Do not add Glassdoor or brittle/restricted scraping. Broad Reddit/video/forum expansion waits for reply evidence or an explicit JT priority.

8. **Scoreboard sources:** Instantly stage/send/reply/bounce/unsubscribe events become jt-ops receipt/outcome records. LinkedIn and manual sends use existing confirmation records. Quotes use the consulting pipeline; cash comes only from the Mission Control payments ledger. The Friday Scoreboard derives from those owners and never asks JT to hand-enter cash.

## 4. Updated lane plan

### Lane 1 — LinkedIn content

- **Change:** none.
- **Built:** manual content bridge.
- **Depends on:** verified proof only.
- **Displaces:** nothing.

### Lane 2 — X/Grok

- **Change:** none; remains deferred.
- **Built/spec:** irrelevant to current cash path.
- **Displaces:** no Instantly or property-pilot time.

### Lane 3 — Prospect research and outreach

#### 3A: Finish the existing Tier A proof loop

- **Built:** discovery workflow, authority stack, cards, proof and suppression owners.
- **Remaining:** deploy PR #9 inactive and run the real five-prospect pilot.
- **Gate:** no schedule or downstream activation until the manual cycle succeeds.

#### 3B: Manual Instantly bridge

- **Build now:** segment-1 table, 100-record list benchmark, first 25-row exact batch, suppression CSV, paused campaign template, CSV exporter, delivery checklist.
- **JT action:** inspect the batch, upload/stage it, and press launch.
- **Gate:** 50 delivered before scale; deliverability and positive-signal gates apply.

#### 3C: Instantly API rail

- **Spec now; build after manual bridge proof:** protected key, paused-campaign staging, exact-variable mapping, canonical suppression mirror, webhook owner, reconciliation poll, outcome receipts, reply cards.
- **No automatic send:** adapter stops at `STAGED_AND_VERIFIED`.
- **Depends on:** one manual campaign, approved exact variables, API metadata, and no-send proof.

#### 3D: Research tiering

- **Build after first campaign data:** Tier B evidence grader and segment selector.
- **Tier A:** unchanged.
- **Displaces:** uniform deep research, broad niche ranking, speculative workflow generation.

### Lane 4 — Job market

- **Change:** none. Keep the employment hedge.
- **Do not mix:** recruiter tasks and consulting outreach metrics remain separate.

### Lanes 5 and 6 — Apps/passive income

- **Change:** remain deferred by opportunity cost during the first 30-day outbound window. There is no retired-mandate freeze; each lane may re-enter through a bounded distribution or buyer test.

### Lane 7 — Networking

- **Change:** warm asks become first-class cash actions; LinkedIn requests are manual and tracked as sends.
- **No automation:** JT sends connection requests and messages.

### Lane 8 — Profile/site

- **Change:** evaluate the existing property page before building anything. Do not create three new landing pages before the first campaign.
- **Trigger:** build one forwardable property-sector page only if replies or calls show the current page is the conversion bottleneck.

## 5. Instantly rail specification

### Campaign structure

- One paused campaign per `segment_id + sequence_version`.
- Example: `pm-300-5000-units-v1`.
- Campaign copy contains pass-through variable placeholders only.
- Open and link tracking off; stop on reply on; unsubscribe header on.
- Campaign never activates through the adapter.

### Exact approval snapshot

Every batch row contains:

- `batch_id`
- `prospect_id`
- `segment_id`
- `sequence_version`
- `first_name`
- `last_name`
- `company_name`
- `email`
- `source_line`
- `source_url`
- `proof_line`
- `step_1_subject`
- `step_1_body`
- optional later-step subject/body fields
- `suppression_revision`
- `row_hash`

The batch card binds the ordered row-hash list and full rendered preview. Any edit invalidates approval.

### Staging flow

1. JT approves exact rows in Mission Control.
2. Canonical channel and suppression owners are rechecked.
3. Adapter creates or updates the lead in a **paused** segment campaign using an idempotency key derived from `campaign + prospect + sequence_version`.
4. Instantly lead ID, campaign ID, payload hash, timestamp, and response ID are recorded as a stage receipt.
5. Reconciliation reads the lead back and proves custom variables match the approved snapshot.
6. Mission Control emits a launch card.
7. JT opens Instantly, verifies the paused campaign, and presses launch.

### Suppression

- Canonical owner checks before staging and again before JT’s launch card becomes actionable.
- Every canonical block is mirrored to Instantly’s global blocklist and the lead is moved out of active/default status.
- If suppression changes after a campaign starts, the system blocks the email/domain and pauses the lead.
- If either action cannot be confirmed, the entire segment campaign is paused and JT receives a blocker card.
- Instantly is never the source of truth for suppression.

Instantly says its global blocklist is checked during ongoing campaigns, and changing a lead away from the default lead status stops further sequence emails. This makes the two-action mirror appropriate, but the OS still verifies both actions. See [Instantly’s stop-sending guidance](https://help.instantly.ai/en/articles/7913412-how-to-stop-sending-to-specific-leads).

### Replies

1. Hosted endpoint records the raw vendor event before any downstream action.
2. Event is deduplicated by vendor event/message/thread ID.
3. Lead is stopped by Instantly’s stop-on-reply behavior and canonical suppression is updated to `reply_received`.
4. jt-ops writes an outcome record linked to the send receipt.
5. Mission Control creates a reply card containing the thread, recommended disposition, and exact drafted reply.
6. JT approves/edits, opens Unibox, and presses send.

Instantly’s API exposes lead custom-variable payloads and email/reply endpoints, while webhooks are available on Hypergrowth. [Lead schema](https://developer.instantly.ai/api-reference/schemas/lead), [webhook documentation](https://help.instantly.ai/en/articles/6261906-webhooks), [pricing](https://instantly.ai/pricing).

### Failure handling

- **Push fails:** no lead is considered staged; retry idempotently; never activate the campaign.
- **Read-back mismatch:** quarantine the row and invalidate its approval.
- **Webhook missed:** overlapping cursor-based API reconciliation finds replies/events; webhook is speed, polling is completeness.
- **Duplicate webhook:** idempotent no-op with duplicate receipt.
- **Suppression after staging:** block + pause lead; pause whole campaign if confirmation fails.
- **Campaign contains an unapproved lead:** block deployment/launch and require reconciliation.
- **Vendor outage:** campaign remains paused or is paused globally; no plaintext/API fallback.

### jt-ops records

- approval snapshot receipt
- channel/suppression observation receipts
- stage request/result receipt
- lead read-back receipt
- JT launch confirmation
- send/delivery/bounce/reply/unsubscribe outcome records
- reply-card decision receipt
- final manual reply confirmation

No reported metric counts without one of those receipts.

## 6. First three Mission Control cards

### Card 1 — Send Altmark the COI enhancement bundle quote

- **Title:** Altmark: quote the COI enhancement bundle
- **Why it matters:** This is the fastest path to incremental cash from a buyer who already paid and has a live workflow.
- **Exact steps:**
  1. Review the bundle: biweekly post-final notices, Matt reminders, reply detection, and monthly accuracy report.
  2. Quote `$6,000 setup + $1,500/month Managed AI Ops`.
  3. Send the quote on the existing Altmark thread.
  4. Record the sent artifact and follow-up date.
- **Paste-ready message:** “Now that the core workflows are live, I can bundle the next COI layer—biweekly post-final notices, Matt reminders, reply detection, and a monthly accuracy report—into one controlled system. The price is $6,000 to implement and $1,500/month to monitor exceptions and report accuracy. If you want it, I’ll send the one-page scope and acceptance checklist.”
- **Destination:** Existing Altmark email thread.
- **Done state:** Sent quote recorded with exact price, timestamp, recipient, and follow-up date.
- **Feedback prompt:** “What language, scope, or price should change before send?”

### Card 2 — Turn Andrew/Aya into a priced conversation

- **Title:** Andrew/Aya: price the acquisition-sourcing opportunity
- **Why it matters:** The opportunity is real but currently unpaid and undefined. A paid audit creates cash without speculatively building a property-finder system.
- **Exact steps:**
  1. Offer a `$1,500 Workflow Audit`, credited to a later build.
  2. Define the output: exact buy box, source inventory, qualification rubric, ten-property sample, and recommended recurring workflow.
  3. State that any success/finder fee is additional and subject to legal review; no brokerage/negotiation activity is included.
  4. Ask for a 30-minute buyer call.
- **Paste-ready message:** “I’m interested, and I already have pieces of the deal-intelligence approach built. I don’t want either of us doing speculative build work before Aya defines the buy box and economics. I’d start with a $1,500 workflow audit: exact acquisition criteria, source map, qualification rubric, a ten-property sample, and the scope for a recurring sourcing system. That fee credits toward the build if Aya proceeds. Any acquisition upside would be additional and written separately. Can we get the actual decision-maker on a 30-minute call?”
- **Destination:** Andrew’s current message thread.
- **Done state:** Andrew receives the price and a buyer call is scheduled or explicitly declined.
- **Feedback prompt:** “Did Andrew accept the price, counter it, or identify the decision-maker?”

### Card 3 — Approve and launch the first Instantly property batch

- **Title:** Instantly: launch the first 25-lead property-manager batch
- **Why it matters:** The system needs measured sends and replies, not more category research. This batch tests list quality, copy, and deliverability without risking the full fleet.
- **Exact steps:**
  1. Review the 25 exact rows: buyer, verified email, source line, subject, body, proof line, and suppression state.
  2. Reject any row that feels inferred, generic, or mis-targeted.
  3. Approve the immutable batch snapshot in Mission Control.
  4. Upload/stage the approved CSV into the paused segment-1 campaign.
  5. Confirm tracking off, stop-on-reply on, unsubscribe header on, and the approved mailboxes selected.
  6. Press launch in Instantly.
- **Paste-ready prompt:** Not needed; exact copy is rendered row by row in the batch snapshot.
- **Destination:** Mission Control batch card, then Instantly paused campaign.
- **Done state:** The exact approved batch is launched by JT, stage/send receipts exist, and no unapproved or suppressed row entered the campaign.
- **Feedback prompt:** “Which rows were rejected, and why?”

## 7. Inputs needed from JT, in order

1. **No input for the current analysis.** The strategy decision is complete.
2. **Instantly account metadata, not credentials:** plan/trial end date, names/status of the five pre-warmed and six done-for-you mailboxes, and whether Hypergrowth is already active. Eve should read this through a safe connector or JT may attach a redacted export; no secrets in chat.
3. **Suppression review:** Eve generates the CSV. JT only adds missing people/domains that must never receive cold outreach. The CSV should include current/former clients, active client contacts, cohort-one contacts, anyone previously contacted, replies, opt-outs, hard bounces, wrong-person outcomes, active sequences, and JT-owned/client domains.
4. **Physical mailing address and unsubscribe configuration:** enter directly in Instantly; do not put a private address in chat or source files.
5. **List-source cost decision:** after the 100-record benchmark, approve at most one month of the winning source. Do not buy Apollo before the benchmark.
6. **Hypergrowth upgrade:** on the day the first campaign launches, if it is not already active. Current official pricing lists Hypergrowth at `$97/month`, 25,000 uploaded contacts, and webhooks/API/integrations. [Instantly pricing](https://instantly.ai/pricing).
7. **API key:** only after the manual bridge succeeds and the adapter is ready for a no-send proof. Create the narrowest scoped key in Instantly and enter it through host-owned masked credential storage. Never paste it into chat, Claude, shell commands, URLs, logs, or repository files.
8. **Daily review window:** reserve 15 minutes at 8:30 AM ET for Tier B batch review during the launch period. Tier A cards remain individual.

## 8. Final sequence

1. Finish the current cohort-two gate: deploy PR #9 inactive and run the real five-prospect pilot.
2. In parallel, create segment-1 v1, the 100-record list benchmark, and the suppression CSV.
3. Produce and approve the first 25-row manual Instantly batch.
4. JT launches it manually.
5. Measure the first 50 delivered messages before scaling.
6. Build the API staging/reply rail only after the manual shape is proven.
7. Add property-adjacent segments 2 and 3 only after segment 1 produces a positive reply, buyer-confirmed pain, or priced conversation.
8. Keep segments 4–7 and broad harvesting out of the first 30-day outbound window unless reply data or a direct buyer trigger justifies them. X/Grok, apps, and passive-income work follow their own current evidence gates; none is blocked by the retired 90-day mandate.

This plan increases work where work creates buyer contact and protects JT from spending the rest of the quarter building another research machine.
