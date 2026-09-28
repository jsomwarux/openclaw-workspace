# LinkedIn Content OS — Opus 5.5 Reconciliation

**Status:** Decision-ready reconciliation; no implementation authorized  
**Date:** 2026-09-28  
**Owner:** Eve  
**Reviewer:** Claude Opus 5.5, read-only  
**Design reviewed:** `2026-09-28-linkedin-content-os-design.md` at `1401783d7054298003476a658e08e389ed5dcd3f`  
**Design SHA-256:** `934789311ac39555a600da469444237efabf0cea360d78755bcd74c066312e7e`  
**Review source:** `reports/growth-os/2026-09-28-opus-5-5-linkedin-content-os-review.md`  
**Review SHA-256:** `d6f09dc8bb54af8a7ccaf706599fc6f8922a9af434a4800b364ed2bab4ff4102`

## 1. Objective

Reconcile the Opus adversarial review against the committed design without implementing code, creating content, admitting a Mission Control card, changing a schedule, or publishing anything.

The output of this gate is a corrected architecture baseline and a bounded sequence for the later implementation plan. Numeric thresholds unsupported by observed data remain hypotheses rather than requirements.

## 2. Executive decision

**Verdict: accept the architectural critique, reject its false precision.**

The original design's durable core survives:

- evidence-bound claims;
- fail-closed gates;
- exactly one concrete image per packet;
- exact-payload approval;
- Mission Control as the sole human decision surface;
- JT as the only publisher;
- `SKIP` as a valid outcome;
- three materially distinct modes;
- no automatic publishing, commenting, replying, or LinkedIn scheduling.

Five material changes are required before an implementation plan can be approved:

1. Treat **quality/fit**, admitted-to-posted conversion, acknowledgment completeness, decision latency, and edit distance as primary operating metrics. Historical `posted:false` values are not reliable evidence of non-publication.
2. Make **Mission Control the sole owner of review state**. Local ledgers may mirror governed decisions but may not create a second review lifecycle.
3. Replace per-post manual design work with **three versioned deterministic image templates**, rendered before review and delivered through a mobile-accessible artifact URL.
4. Replace the 100-point ranker and quota-like mix adjustment with **deterministic gates, a small auditable quality rubric, and lane ceilings**.
5. Reorder delivery so the system proves the review-and-post rail with real fixtures before building collection and selection machinery.

## 3. Evidence confirmed during reconciliation

- `memory/content/posted-log.jsonl` contains 101 LinkedIn rows, only 3 marked posted, and no captured real public URL. The sole `public_url` value is a placeholder.
- `memory/content/edit-deltas.jsonl` is empty.
- `memory/content/current-efforts.md` was last updated 2026-05-07 and contains stale priorities.
- Recent build records are dominated by internal machinery. They are discovery pointers, not automatic publication evidence.
- Mission Control's lane-packet route exposes `POST` and `PATCH`, but no governed read route. Its actions are approve, reject, complete, skip, and no-action; it has no native hold or revision-request transition.
- Mission Control edits recompute the payload hash and clear prior approval, so exact-payload approval and in-card edit capture already exist.
- Mission Control requires `post-url` evidence for a LinkedIn completion.
- The jt-ops proof schema contains `permission_status` values `internal-only`, `approved-anonymized`, and `approved-named`, plus permission evidence.
- `n8n-agent/tasks/lessons.md` is useful source material, but it is not uniformly bound to execution IDs and error artifacts. It cannot be treated wholesale as accepted proof.

JT clarified on 2026-09-28 that the principal historical bottleneck was **quality/fit**: generated posts did not yet warrant publication. He also reported that some posts may have been published without being acknowledged to the system, so the current ledger overstates non-publication. JT approved the reconciled defaults: independently evidenced general engineering recipes may qualify after protected purpose removal; the positive build-proof fixture should use permissioned anonymized client proof; v1 uses three original fixed templates with no screenshots or source crops; and edits should happen inside Mission Control when practical.

## 4. Finding-by-finding disposition

### Adopt

| Opus finding | Reconciled decision |
|---|---|
| Publishing is the binding constraint | Adopt. Measure admitted-to-posted rate, decision latency, and exact edit distance. Include rejected, expired, and not-posted packets in denominators. |
| Fixture 1 exposes internal job machinery | Adopt. Freeze the Decagon/Jobs version as a negative fixture. Re-source the positive build-proof fixture from permissioned client proof or a field lesson that contains no protected system purpose. |
| Manual per-post image creation creates avoidable friction | Adopt. Use one versioned template per mode, render before admission, and bind the exact PNG hash to the card. |
| Local and Mission Control lifecycles will drift | Adopt. Mission Control owns review state. Local state ends at admission and mirrors later governed decisions. |
| Original score is lane-biased and falsely precise | Adopt. Replace it with deterministic gates plus a small rubric and lane ceilings. |
| Relationship conflicts are missing | Adopt. Block clients, active prospects, suppressed organizations, and active employers/applications unless JT explicitly overrides the exact card. Query canonical owners; do not hardcode a company list. |
| Internal machinery needs an explicit prohibition | Adopt. Outreach, prospecting, job-search automation, content-system internals, Mission Control internals, proof hygiene, and Eve/OpenClaw internals are prohibited source families in v1. |
| Gold-set design is too broad for the available corpus | Adopt. Use exact LinkedIn voice gold plus contrastive JT edit pairs. Keep negative rules in deterministic guards. Defer external mechanics prose. |
| Drive is part of the posting rail | Adopt. A review-ready card needs a mobile-accessible, immutable image artifact. Drive may store the artifact but never owns workflow truth. |
| The implementation order is backwards | Adopt. Prove templates, Mission Control review, and posted fixtures before building the selection engine. |
| Screenshots and source crops expand privacy and rights risk | Adopt for v1. Use original templates only. Reconsider screenshots/crops after the rail is proven and permission/rights contracts exist. |
| Autonomous Post Detection is a competing generator | Adopt for LinkedIn v1. It may emit a signal only; it may not generate or admit a LinkedIn packet outside this OS. |

### Adopt with changes

| Opus recommendation | Reconciled decision |
|---|---|
| Lock covers pending review only | Adopt. Approval releases the admission lock. Approved-but-unposted cards remain measurable open publication opportunities, not blockers to reviewing the next card. |
| 72-hour review TTL and admission + 5-day posting TTL | Treat as pilot defaults, not established truths. The implementation plan must make them configuration values and test them in the manual pilot. |
| Close approved-but-unposted as `not_posted` | Adopt the semantic outcome. Use Mission Control's existing governed `no-action` closure with a typed note code unless a later design proves a new transition is necessary. Do not expand Mission Control prematurely. |
| Remove `PublicationPermissionV1` | Adopt for v1 client claims because jt-ops already owns publishability and permission evidence. Revisit only if v1 later admits non-client assets that jt-ops cannot govern. |
| X Intelligence Router is the sole news owner | Make it the canonical automated owner. Retain bounded manual intake for JT-supplied links and approved primary public sources until the router is operationally proven. No duplicate automated collector. |
| `content-focus.json` is JT-authored and renewed monthly | Replace with a versioned focus snapshot generated from canonical business/job state. JT approves changes or corrections, not routine monthly file authorship. Stale focus blocks admission and raises one bounded renewal decision. |
| `n8n-agent/tasks/lessons.md` is a primary build source | Use it for discovery. A lesson becomes evidence only when it binds to a verifier receipt, execution artifact, accepted client proof, or JT field note. |
| Ban internal-system tokens | Use source-family classification and claim review as the primary control. A banned-name guard is defense in depth, not the authority, because words such as “prospect” can appear in legitimate buyer-facing contexts. |
| One lifecycle and four schemas | Adopt the simplification target: signal, candidate, packet, and outcome. The packet's post-admission review state is mirrored from Mission Control, not independently advanced. |
| `(problem, mechanism)` semantic key over 60 days | Adopt the coarser key and inclusion of in-flight/rejected items. Treat 60 and 30 days as initial configuration subject to labeled-history testing. Near-duplicate checks must produce receipts and may not silently rewrite taxonomy. |
| 0–9 quality rubric | Adopt as the preferred replacement for the 100-point score. Q1 may be deterministic; Q2/Q3 require citations and calibration. Exact eligibility thresholds remain provisional until JT labels the evaluation set. |
| Mode-specific freshness windows | Adopt the distinction, not every proposed number as permanent. Client proof remains eligible while permission and facts re-verify; engineering recipes get a longer window than news; AI events and company triggers use their primary-event dates; regulations may remain relevant through their effective date. Admission must leave enough time for review. |
| Retrieval of two voice examples plus one contrastive pair | Adopt as the v1 ceiling. Use exact JT-final LinkedIn text, distinct structures, least-recently-used preference, and origin caps. Do not use embeddings until corpus size or measured retrieval failure justifies them. |
| Remove conflicting legacy voice constraints | Adopt where workspace rules conflict with verified JT voice or evidence safety. Fixed bullets, invented-ROI structures, forced compression, fixed-day case studies, and stale creator mechanics may not override the reconciled gold set and hard gates. Each retired rule requires an owner-file update and regression check during Program 0. |
| Add `angleEvidenceRef` and typed claim attribution | Adopt. Candidate claims distinguish public fact, vendor assertion, JT-verified fact, and hypothesis; every earned angle resolves to a proof fact, verified artifact, or JT field note. |
| Three posted fixtures plus a four-week pilot | Adopt as the schedule-readiness gate. Packet construction can be accepted before recurrence, but no recurring job is authorized until all three modes have been posted through the governed rail and the pilot passes. |
| Three templates built from one Claude Design session | Adopt three templates, not the vendor-specific creation ritual. The final assets must be versioned code/templates with deterministic validation; how the first visual direction is created is an implementation choice. |
| One weekday scheduled job | Defer the frequency and time. A schedule is a separate red gate and must be justified after the pilot. |

### Reject or defer

| Opus recommendation | Reason |
|---|---|
| Treat every n8n lesson as execution-backed proof | Workspace evidence does not support that universal claim. |
| Force every teardown into exactly four steps with approval at step four | This is a useful template option, not a universal workflow truth. Require a real owner, system of record, decision boundary, and coherent workflow; do not invent steps to satisfy layout. |
| Hard cap teardown subjects at roughly 500 employees | Unsupported proxy. Commercial relevance, public evidence, conflict checks, and buyer fit are the real gates. |
| Hard-code 60% posted, five-minute median decisions, 0.25 edit distance, 60-day cooldown, or $20/month as final acceptance values | These are hypotheses with no calibrated baseline. Preserve them as pilot starting targets only. |
| Reach learning begins at 1,000 median impressions | Unsupported threshold and secondary to qualified outcomes. Defer reach-based changes entirely in v1. |
| Require JT to answer recurring per-post metrics questions | Adds operator burden and conflicts with the goal of reducing posting friction. Prefer one bounded weekly capture or authoritative platform data if later approved. |
| Require 24-hour metric snapshots | Unnecessary operator burden and too noisy at current volume. Keep one seven-day observation when available; otherwise record `metrics_unknown`. |
| Expand embeddings, external mechanics, or source allowlists now | Defer. Use deterministic retrieval, primary sources, and small versioned allowlists until a measured gap justifies expansion. The review's exact caps of 8 changelogs and 10 trade sources are not evidence-backed requirements. |
| Create or enable any cron now | Explicitly outside this gate. |

## 5. Reconciled architecture

### 5.1 Owners

- **Evidence and client publishability:** jt-ops proof records.
- **Current commercial/career focus:** versioned snapshot derived from canonical owners; JT resolves changes and conflicts.
- **News intelligence:** X Intelligence Router when proven; bounded manual JT/primary-source intake until then.
- **Relationship conflicts:** consulting pipeline, suppression owner, and job-market/application owner.
- **Signals, candidates, pre-admission packet records, and receipts:** append-only local ledgers.
- **Review state and human decisions:** Mission Control only.
- **Image delivery:** immutable Drive asset referenced by hash from Mission Control.
- **Publication:** JT only.
- **Orchestration:** OpenClaw after a separately approved schedule gate.
- **n8n and Notion:** unused in v1 unless later evidence shows they remove real burden.

### 5.2 Allowed source families

- `client_delivery`: eligible only with claim-level jt-ops facts and sufficient publishability.
- `field_lesson`: eligible when written or confirmed by JT and stripped of protected/client identifiers.
- `engineering_recipe`: eligible only with supporting execution/verification evidence and a buyer-facing translation.
- `teardown_trigger`: eligible from primary public evidence with no private-knowledge premise.
- `ai_event`: eligible from a primary dated source plus a bound JT artifact or lesson.
- `internal_machinery`: prohibited in v1.

Every claim carries a closed attribution type: `public_fact`, `vendor_assertion`, `jt_verified_fact`, or `hypothesis`. Vendor assertions are attributed as such; numbers come from primary sources or verified proof facts; hypotheses may not be rewritten as inside knowledge.

### 5.3 Candidate gates

Before scoring, a candidate must pass:

1. allowed source family;
2. no unresolved relationship conflict;
3. every material claim bound to an exact excerpt, structured proof fact, or verified artifact;
4. permission valid for the claim scope and intended publication window;
5. at least one resolved JT angle/evidence reference;
6. mapping to a current approved focus target;
7. mode-specific subject fit;
8. sufficient content life remaining at admission;
9. no semantic duplicate across published, in-flight, or recently rejected work;
10. no protected internal premise or engagement-bait CTA;
11. valid exactly-one-image specification.

`SKIP` is the correct result when no candidate passes.

### 5.4 Ranking

Use a small 0–9 quality rubric:

- `Q1 proof specificity` (0–3, deterministic);
- `Q2 earned angle strength` (0–3, cited model judgment);
- `Q3 reader consequence` (0–3, cited model judgment).

Rank quality first, then lane deficit, urgency, proof specificity, and stable candidate ID. Use lane ceilings, not minimum quotas. The exact eligibility cutoff and cooldown windows are set only after a labeled evaluation set exposes their error rate.

### 5.5 Review lifecycle

```text
local: observed -> eligible -> selected -> drafted -> rendered -> qa_passed
                                                     |-> rejected / expired
Mission Control: admitted(pending) -> approved -> completed(post URL)
                                |-> rejected
                                |-> skipped / no-action / expired
mirror: governed MC events -> append-only outcome records
```

- No local `hold` or `revision_requested` authority.
- A revision is a new packet version after JT rejects with a parseable revise note.
- Approval releases the one-card review lock but never publishes.
- Completion requires JT and `post-url` evidence.
- Composer edits are `unknown` unless exact final text is captured; they are never inferred as zero.
- A governed read-back path is a prerequisite. The current dedicated route has no GET/read boundary.

### 5.5 Publication acknowledgment and performance check-in

The content card remains the sole lifecycle owner. A single deduplicated **LinkedIn check-in task** is a derived reminder surface, never a second content record. Its projector reads two hash-bound inputs: a governed read-only Mission Control snapshot for current packet approval/closure state and the append-only outcome ledger for publication/performance facts. It cannot infer approval from outcomes or write back to either owner.

- It exists only while one or more acknowledged facts are missing.
- It aggregates unresolved items instead of creating one reminder task per post.
- For an approved packet without a publication outcome, it asks JT to record exactly one of: `posted`, `not_yet`, or `wont_post`.
- `posted` requires the LinkedIn URL and requests exact final text. If final text is unavailable, the publication is still recorded and edit distance remains `unknown`.
- `not_yet` preserves the approved packet and re-surfaces the same deduplicated check-in on the next eligible daily review; it creates no new packet or reminder row.
- `wont_post` closes the opportunity through the governed `no-action` path with a typed reason such as `quality_fit`, `stale`, `timing`, or `other`.
- Seven days after a confirmed publication, the same check-in task asks once for a bounded performance snapshot: impressions, reactions, comments, reposts, qualified replies, and downstream opportunity signal. Missing values are recorded as `metrics_unknown`; no 24-hour prompt is created.
- Completing the check-in writes governed outcome events against the original packet and removes the reminder when no unresolved item remains.
- The reminder may appear in Mission Control's normal daily queue but may not alter Today ranking logic, bypass task capacity, or create a cron during Program 0.

### 5.6 Image lifecycle

- One template per mode: build proof, teardown, AI news.
- Original 1080×1350 render; no real workflow screenshots, vendor screenshots, source crops, or logos in v1.
- Deterministic content limits, safe-area, overflow, attribution, privacy, dimensions, MIME, byte-length, and hash checks.
- Render before review.
- Upload as a new immutable Drive file and bind its checksum/hash in Mission Control.
- JT approves the exact text-plus-image payload and remains the only publisher.

## 6. Corrected delivery sequence

### Program 0 — Truth and corpus reset

- replace stale current-effort input with a versioned focus snapshot;
- classify historical LinkedIn rows as `posted_confirmed`, `not_posted_confirmed`, or `status_unknown`; never convert legacy `posted:false` into confirmed non-publication;
- recover URLs and exact final text for known or possibly posted LinkedIn examples through one bounded audit;
- construct voice-gold v0 and contrastive pairs;
- classify sources into allowed/prohibited families;
- build and label the positive and negative evaluation fixtures;
- encode quality/fit as the confirmed historical bottleneck;
- specify and locally prove the single deduplicated Mission Control check-in contract without admitting a live task or changing a schedule.

**Gate:** Program 0 pauses after producing the proposed focus snapshot, bounded historical-recovery request, and fixture-gap report. JT must (a) confirm or correct the focus snapshot, (b) answer the bounded recovery request, and (c) identify or approve a genuinely permissioned anonymized client-proof record. The implementation then ingests those answers as typed events, rebuilds the audit/corpus/fixtures, and receives fresh independent verification. Program 0 cannot close while the positive fixture is only `gap:permission_missing`. The principal cause, source-family policy, visual baseline, fixture class, and editing path are already decided. Live check-in admission remains a later explicit gate.

### Program 1 — Templates and governed delivery rail

- build three versioned image templates and deterministic validation;
- establish immutable Drive delivery;
- map the LinkedIn packet onto the existing lane-packet contract;
- add or identify a governed read-back path;
- prove replay, exact-payload approval, edits, rejection, expiry, no-action, and evidence-backed completion.

**Gate:** separate implementation plan and independent verification. No live card without a later explicit admission approval.

### Program 2 — Three posted manual fixtures

- one permissioned build/field-proof packet;
- one public-evidence teardown;
- one primary-source AI-news packet with a JT angle;
- all three use the real template, Drive, Mission Control, manual JT publication, final-text capture, and URL receipt.

**Gate:** each is accurate, safe, useful, visually acceptable, and posted through the governed rail. Failure stops engine work for diagnosis.

### Program 3 — Deterministic candidate engine

- append-only intake/candidate records;
- source health, expiry, gates, coarse dedupe, Q1, lane ceilings, and receipts;
- frozen positive and negative tests;
- no recurrence.

### Program 4 — Generation and on-demand pilot

- bounded retrieval, one-draft generation, visual specification, Q2/Q3, claim support, one repair;
- four-week on-demand shadow/pilot period;
- measure admitted-to-posted rate, decision latency, edit distance, safety, duplicates, and supply by lane.

**Gate:** JT sets final schedule-readiness thresholds after observing the pilot baseline.

### Program 5 — Schedule

Requires a separate explicit JT approval. Frequency, time, cost ceiling, kill switch, rollback, and source rollout are decided from pilot evidence. Enable one capability at a time.

## 7. Decisions resolved for the Program 0 plan

1. **Historical bottleneck:** quality/fit. JT did not believe most generated drafts warranted publication.
2. **Historical truth:** some posts may have been published without acknowledgment. Legacy `posted:false` is therefore `status_unknown` unless independent evidence confirms non-publication.
3. **Build-proof boundary:** an evidenced general engineering recipe may qualify only after protected purpose removal and buyer-facing translation.
4. **Fixture source:** use permissioned anonymized client proof for the positive build-proof fixture. The Decagon version remains a negative fixture.
5. **Visual baseline:** three fixed original templates; no screenshots, source crops, or logos in v1.
6. **Editing path:** edit inside Mission Control when practical. If JT edits in LinkedIn and does not supply final text, edit distance remains `unknown`.
7. **Reminder design:** one deduplicated Mission Control check-in derived from missing publication/performance facts; never one task per post and never a second lifecycle.

Conservative boundaries remain: no internal machinery, no client/prospect/employer teardown, no screenshots/crops, no recurring schedule, no inferred edit or outcome data, and no live Mission Control write without its later gate.

## 8. Acceptance criteria for this reconciliation

- Every material Opus recommendation is classified as adopt, adopt with changes, reject, or defer.
- Verified workspace facts are separated from reviewer assumptions.
- The corrected design preserves JT-only publication and the explicit schedule gate.
- The sequence tests the posting rail before selection-engine complexity.
- No code, content asset, Mission Control card, provider call, recurring job, schedule, or publication action occurs.

## 9. Proof assets

- Original design and hash: listed in the header.
- Opus review and hash: listed in the header.
- Workspace evidence: posted ledger counts, empty edit-delta ledger, stale current-efforts file, Mission Control route and transition code, jt-ops proof schema, and n8n lessons corpus inspected on 2026-09-28.
- Implementation proof: **not available; implementation is intentionally unauthorized.**

## 10. Next gate

Write and review one canonical implementation plan for **Program 0 only**. The plan may build local contracts, fixtures, audits, and read-only/staged proof for the check-in design, but it may not admit a live Mission Control task, deploy, schedule, generate publication assets, or collapse Programs 0–5 into one build authorization.
