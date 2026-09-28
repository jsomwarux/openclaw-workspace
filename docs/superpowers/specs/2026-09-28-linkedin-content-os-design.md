# LinkedIn Content OS Design

**Status:** Proposed design for JT review  
**Date:** 2026-09-28  
**Scope:** LinkedIn only. The system prepares review-ready content and exactly one accompanying image. JT remains the only publisher.

## 1. Decision

Build a closed-loop LinkedIn Content OS, not a recurring post generator.

The system will continuously collect current work and market signals, normalize them into evidence-bound candidates, rank them against JT's commercial goals and recent feed, generate at most one review packet per scheduled selection run, and learn from JT's edits and real outcomes. A valid run may output `SKIP`.

The approved **Approval is not execution** post becomes acceptance fixture 1. It is not the final deliverable.

The prior "two manual packets, then automate" gate is too narrow for this system. There are three materially different source and visual modes, so automation requires three accepted fixtures:

1. verified build/project proof;
2. company or niche teardown;
3. AI news supplied by JT or found through approved public sources.

## 2. Goals

- Produce two or three strong LinkedIn candidates per week when the evidence supports them.
- Keep every candidate current, original, buyer-relevant, evidence-safe, and recognizably in JT's voice.
- Maintain a useful mix of build proof, teardowns, and AI news without filling quotas with weak posts.
- Make the system aware of what JT is building, what has just shipped, what matters in his target markets, and what is already overused in his feed.
- Attach exactly one image to every post, routed to the safest and clearest visual format for that source type.
- Give JT one complete Mission Control review packet containing the post, evidence, exactly one rendered and validated image, alt text, crop guidance, and decision controls.
- Learn from edits, rejections, publication, seven-day performance, qualified replies, recruiter interest, and buyer conversations.

## 3. Non-goals

- No automatic publishing, commenting, replying, or scheduling to LinkedIn.
- No engagement bait, generic thought leadership, or algorithm-chasing.
- No unverified claims, inferred client results, private workflow exposure, or screenshots that depend on blur for safety.
- No second task board or editable shadow database beside Mission Control and canonical owner files.
- No fixed three-post quota. `SKIP` is a correct output.
- No model fine-tuning in v1. Retrieval over a small labeled gold set is more controllable and easier to evaluate.
- No private LinkedIn scraping or unsupported LinkedIn automation.

## 4. Approaches considered

### A. Template generator

Run a weekly prompt over recent notes and generate three posts.

**Rejected:** fast to build, but it repeats angles, cannot prove freshness, has no candidate competition, and does not learn from JT's edits or commercial outcomes.

### B. Fully autonomous content agent

Give one agent broad access to files and the web, then ask it to research, choose, draft, design, and schedule.

**Rejected:** too much authority in one opaque run. It makes provenance, debugging, deduplication, privacy, and evaluation weak.

### C. Evidence-bound content operating system

Separate collection, normalization, ranking, generation, review, and learning behind versioned contracts.

**Selected:** each stage is independently testable, weak signals can fail closed, the final packet preserves evidence, and model vendors can change without changing system truth.

## 5. System architecture

```text
Project/build signals ----\
JT-supplied X/news --------> Signal collectors -> Candidate ledger -> Ranker + mix controller
Company/niche signals -----/                                      |
                                                                   v
Gold set + voice rules ---------------------------------> Writer + visual router
                                                                   |
                                                                   v
Evidence/voice/privacy/originality/visual QA -> Mission Control review packet
                                                                   |
                                                         JT edits / approves / posts
                                                                   |
                                                                   v
Published URL + edits + outcomes -> Learning ledger -> future retrieval/ranking
```

### Ownership and authority precedence

- **Canonical project truth:** project repositories, accepted proofs, client state, recent-build records, and verified daily notes.
- **Signal and candidate state:** append-only local JSONL ledgers with stable IDs, hashes, source pointers, and expiry.
- **Mission Control:** the only human review and decision surface.
- **Drive:** readable final packet and image artifact when required; never workflow truth.
- **Notion:** optional calendar projection after approval; never the candidate owner.
- **OpenClaw:** orchestration and model routing; never sole execution truth.
- **n8n:** deterministic scheduled collection and routing only after the local contracts pass manual proofs.

When sources conflict, authority is resolved in this order:

1. accepted client/project proof and explicit JT decisions;
2. authoritative project status or release receipt;
3. canonical domain state;
4. recent-build and daily-memory projections;
5. research summaries and model inferences.

Lower-ranked sources may discover a conflict but may not overwrite higher-ranked truth. The conflict blocks the signal until the authoritative owner resolves it.

Only JT may authorize publication of client-identifying facts, client metrics, private screenshots, or information not already covered by a recorded public-proof permission. A publication permission record binds the approver, exact permitted claims/assets, source hash, decision timestamp, and expiry or revocation state. Automated privacy checks can reject material but cannot grant publication permission.

## 6. Source collectors

Every collector emits the same versioned `ContentSignalV1` contract. Collectors do not write drafts.

### 6.1 Current work and shipped projects

Preferred sources, in order:

1. accepted proof ledger entries and client-safe outcome records;
2. `memory/content/recent-builds.md`;
3. project-level `CLAUDE.md`, lessons, release notes, and accepted handoffs;
4. current Mission Control work with verified completion evidence;
5. daily notes and current-efforts files, subject to freshness checks.

A project signal is eligible only if it contains:

- what changed;
- who or what it was for;
- proof or a source pointer;
- a publishability classification;
- a safe claim set;
- one non-obvious judgment, result, or operating lesson;
- a freshness timestamp.

The collector must not interpret "done" from prose alone. Accepted proof or an authoritative status transition is required.

### 6.2 JT-supplied AI news and X posts

JT can forward a post, URL, screenshot, or short note. The collector stores the supplied item, attempts to resolve the primary source, extracts the dated claim, and marks whether JT already has an earned angle. If primary-source resolution fails, the signal is retained as `observed` but is ineligible for drafting.

Engagement is discovery evidence, not truth. The system must verify material claims against a primary source before drafting. "When possible" means the collector may preserve an unresolved signal, but that signal remains ineligible and cannot become a candidate until primary evidence is bound.

### 6.3 Public AI trend discovery

The discovery lane watches an allowlisted set of public sources relevant to JT's niches: official product or company announcements, research papers, release notes, trusted industry publications, and public X accounts. It clusters duplicate coverage into one event.

An event is eligible only when it is:

- fresh enough to matter;
- relevant to a Tier 1 or Tier 2 niche;
- supported by a primary source;
- meaningfully connected to JT's implementation experience;
- not already saturated in JT's recent posts or candidate ledger.

### 6.4 Company and niche teardown discovery

The teardown collector looks for public change events, not merely popular companies:

- new product or service launch;
- funding tied to operational expansion;
- hiring patterns that reveal workflow load;
- regulatory or market changes;
- public customer complaints or support bottlenecks;
- a workflow-heavy business model with a visible operating constraint.

The system never claims internal access. A teardown must state that it is a public-evidence hypothesis about what JT would build.

### 6.5 Source-health and freshness rules

Each collector reports:

- last successful run;
- newest source timestamp;
- items read, accepted, rejected, and deduplicated;
- rejection reasons;
- cursor or checkpoint;
- cost;
- error state.

A stale or failed collector cannot silently contribute old signals. Its candidates are suppressed and the selection receipt names the missing lane.

Initial freshness windows are fixed configuration:

- accepted project/build proof: 30 days from acceptance or a newer verified outcome;
- JT-supplied AI news: 7 days from the primary event;
- public AI news: 5 days from the primary event;
- company change trigger: 14 days;
- niche/regulatory trigger: 14 days unless the source declares a shorter effective window.

Retries use bounded exponential backoff with a maximum of three attempts per run. A successful later run clears the collector error but does not revive expired candidates; it must emit a new signal if the authoritative source changed. The allowlist is versioned, changes require JT approval, and each source has one declared owner. Collector failure suppresses only its dependent candidates, never healthy lanes.

## 7. Canonical contracts

Every record uses canonical JSON, `schemaVersion`, a stable identifier, `createdAt`, an idempotency key, and an exact SHA-256 event or payload hash. Unknown fields fail closed at write boundaries. Timestamps are RFC 3339 with explicit offsets. Enums below are closed.

Unless a field says otherwise, identifiers, URIs, enums, and prose values are UTF-8 strings; timestamps are RFC 3339 strings; hashes are exactly 64 lowercase hexadecimal characters; scores are integers; arrays are ordered, non-empty when required, and contain no duplicate identifiers. Optional fields must be absent rather than `null`. Validation rejects unknown enum values, unsafe relative paths, traversal, control characters, and noncanonical JSON.

### 7.1 `ContentSignalV1`

Required fields:

- `signalId`
- `sourceType`: `project`, `jt_supplied_news`, `public_ai_news`, `company_trigger`, `niche_trigger`
- `sourceUri` or local source pointer
- `sourcePublishedAt`
- `observedAt`
- `sourceHash`
- `primaryEvidence[]`
- `summary`
- `niche`
- `entities[]`
- `freshUntil`
- `privacyClass`
- `collectorVersion`
- `schemaVersion`: literal `content-signal.v1`
- `idempotencyKey`: source namespace plus stable source identity
- `publishability`: `public`, `permission_required`, or `prohibited`
- `permissionRef`: required when `publishability=public` depends on an approval record
- `safeClaims[]`: exact claim strings with evidence pointers
- `earnedLesson`: the non-obvious judgment, outcome, or operating lesson
- `state`: `observed`, `eligible`, `rejected`, or `expired`
- `rejectionReason`: required for rejected records
- `payloadSha256`

The unique constraint is `schemaVersion + idempotencyKey + payloadSha256`. Exact replay is a no-write success. The same idempotency key with changed bytes creates a new version linked through `supersedesSignalId`.

### 7.2 `ContentCandidateV1`

Required fields:

- stable `candidateId`
- source signal IDs and hashes
- lane: `build_proof`, `teardown`, or `ai_news`
- proposed thesis
- earned-angle explanation
- safe claim set
- target reader
- commercial objective
- novelty cluster
- visual path
- expiry
- feature-level score breakdown
- hard-gate results
- status and append-only decisions
- `schemaVersion`: literal `content-candidate.v1`
- `semanticKey`: canonical `lane|niche|problem|mechanism|outcome` tuple
- `state`: `proposed`, `ineligible`, `scored`, `selected`, `packet_building`, `ready`, `admitted`, `held`, `rejected`, `expired`, or `consumed`
- `scoreConfigVersion`
- `scoreBreakdown`: closed map of the eight integer dimensions in §9.2 plus the five exact deductions
- `decisionEvents[]` as append-only event pointers
- `payloadSha256`

### 7.3 `ContentPacketV1`

Required fields:

- candidate binding
- final post text
- claim-to-evidence map
- selected gold-set exemplars and why they were selected
- image route; an optional internal Claude Design prompt may exist only in `visual_pending`
- alt text
- crop and safe-area guidance
- privacy and rights result
- voice, originality, stale-pattern, and distribution checks
- intended publication window and expiry
- exact JT decision options
- `schemaVersion`: literal `content-packet.v1`
- `packetVersion`: positive integer
- `revisionFamilyId`: stable across every revision of one selected candidate
- `state`: `drafted`, `visual_pending`, `rendered`, `qa_passed`, `admitted`, `approved`, `revision_requested`, `held`, `rejected`, `expired`, `posted`, `outcome_pending`, or `closed`
- `visualPrompt`: optional intermediate production input
- `imageAsset`: required before `rendered`, containing local asset pointer, MIME type, pixel dimensions, byte length, and SHA-256
- `draftSha256`: required from `drafted` onward; binds candidate, post text, claim map, visual route, and any visual prompt
- `payloadSha256`: absent before `rendered`; required from `rendered` onward and binds `draftSha256` plus the image asset hash, alt text, crop guidance, privacy result, and rights result
- `supersedesPacketId`: required for any revised payload

### 7.4 `ContentOutcomeV1`

Every event requires:

- `schemaVersion`: literal `content-outcome.v1`;
- `outcomeEventId`;
- `packetId`, `packetVersion`, `revisionFamilyId`, and bound `payloadSha256`;
- `eventType`: `rejected`, `edit_delta`, `approved`, `posted`, `metric_snapshot`, `qualified_reply`, `profile_signal`, `commercial_outcome`, `correction`, or `deletion`;
- `occurredAt`;
- `sourcePointer`;
- one typed payload from the closed list below;
- `eventSha256`.

Typed payloads:

- `rejected`: reason enum plus optional JT note;
- `edit_delta`: approved text hash, final text hash, exact final text, and structured inserted/deleted/replaced spans;
- `approved`: exact payload hash and governed JT identity;
- `posted`: canonical LinkedIn URL, publication timestamp, exact final published text, final text SHA-256, approved text SHA-256, and `changedAfterApproval` boolean;
- `metric_snapshot`: observation window (`24h` or `7d`), numeric metrics with unavailable fields absent, and collection method;
- `qualified_reply`: audience class, attributable post URL, evidence pointer, and qualification reason; no private message body is required;
- `profile_signal`: signal type, attributable post URL when known, and source confidence;
- `commercial_outcome`: `buyer_conversation`, `recruiter_conversation`, `referral`, or `opportunity`, plus evidence pointer and attribution confidence;
- `correction`: target event ID, corrected fields, reason, and correcting actor;
- `deletion`: target event ID, reason, and actor; deletion is a tombstone, never physical removal.

Outcome events are globally timestamp-ordered per packet, append-only, and idempotent on `outcomeEventId + eventSha256`. A conflicting replay fails closed.

### 7.5 `PublicationPermissionV1`

Required fields:

- `schemaVersion`: literal `publication-permission.v1`
- stable `permissionId`
- `approver`: required for `grant`, `revoke`, or `supersede` and bound to JT's governed identity
- `actor`: JT for `grant`, `revoke`, and `supersede`; deterministic system actor for `expire`
- exact `allowedClaimHashes[]`
- exact `allowedAssetHashes[]`
- `sourceRefs[]`
- `decidedAt`
- `expiresAt` or explicit `no_expiry`
- `eventType`: `grant`, `revoke`, `expire`, or `supersede`
- `supersedesPermissionEventId`: required for `revoke`, `expire`, or `supersede`
- `eventSha256`

Permission state is derived from the append-only event chain; events are never mutated. Only the governed JT decision boundary may grant, revoke, or supersede permission. Expiry may be emitted deterministically when `expiresAt` passes. A source owner or model may recommend a scope but cannot activate it.

### 7.6 State transitions

Allowed transitions are closed:

- Signal: `observed -> eligible|rejected|expired`; `eligible -> rejected|expired`.
- Candidate: `proposed -> ineligible|scored|expired`; `scored -> selected|expired`; `selected -> packet_building|expired`; `packet_building -> ready|rejected|expired`; `ready -> admitted|expired`; `admitted -> held|rejected|consumed|expired`; `held -> admitted|rejected|expired`.
- Packet: `drafted -> visual_pending|rendered|rejected|expired`; `visual_pending -> rendered|rejected|expired`; `rendered -> qa_passed|rejected|expired`; `qa_passed -> admitted|expired`; `admitted -> approved|revision_requested|held|rejected|expired`; `revision_requested -> closed`; `held -> approved|revision_requested|rejected|expired`; `approved -> posted|expired`; `posted -> outcome_pending|closed`; `outcome_pending -> closed`.

A revision never mutates the current packet. The old packet moves to `closed`, and a new packet in the same `revisionFamilyId` starts at `drafted` with `supersedesPacketId`. The revision-family lock remains unresolved throughout this handoff, including the interval after the old version closes and before the replacement passes QA. Terminal states cannot transition. Every transition is an append-only event with actor, reason code, timestamp, prior-state hash, and resulting-state hash.

Closed rejection reasons are: `missing_primary_evidence`, `unsafe_claim`, `permission_missing`, `permission_expired`, `privacy_risk`, `rights_risk`, `stale`, `duplicate`, `weak_positioning`, `no_earned_angle`, `no_visual_path`, `voice_failure`, `qa_failure`, `jt_rejected`, and `superseded`.

Impressions and reactions are weak signals. Qualified conversations, profile checks from target readers, and attributable opportunities carry more weight.

## 8. Gold set and retrieval

Yes, the system needs a gold set. It is three separately versioned collections with different authority:

- **Voice gold:** JT-authored, JT-selected, JT-approved, or exact final published text. Only JT can admit or remove examples. The writer may receive exact prose from this collection.
- **Mechanics references:** external posts admitted by a curator receipt. The store retains source/provenance and extracted mechanics, but the writer receives only the mechanics labels and never the external prose.
- **Negative set:** JT-rejected drafts, exact edit patterns, banned structures, and failed visuals. JT decisions and deterministic guard failures may add records; all other additions require JT approval.

Every entry binds collection, stable ID, source hash, admission actor, admitted-at timestamp, mode, niche, labels, and status. Collection manifests are immutable versions; updates create a new manifest. Retrieval records the exact manifest versions used.

### Positive examples

- JT-authored posts JT says sound like him;
- approved drafts;
- published final text;
- high-confidence proof posts with valid claims;
- external reference posts used only in the separate mechanics-reference collection.

### Negative examples

- JT-rejected drafts;
- banned sentence shapes and stale structures;
- repeated angles;
- posts that were accurate but commercially weak;
- visual examples JT rejected.

### Labels

- source mode;
- target reader;
- hook mechanic;
- sentence and paragraph rhythm;
- proof density;
- CTA type;
- visual type;
- JT edit distance;
- rejection reason;
- seven-day outcome class;
- commercial outcome class.

Retrieval uses the current candidate's mode, niche, target reader, and objective. It selects at most three voice-gold examples, two negative examples, and two mechanics records. External prose never enters the writer context. It never dumps the entire corpus into the writer.

The current voice profile and evidence corpus are the seed. The empty edit-delta ledger is a blocking data gap for claiming the system is self-improving.

## 9. Candidate scoring and portfolio selection

### 9.1 Hard gates

A candidate is rejected before scoring if any of these fail:

- authoritative evidence or primary source missing;
- unsafe or unapproved client claim;
- no earned JT angle;
- semantic duplicate inside the cooldown window;
- no buyer, recruiter, or builder positioning value;
- no viable one-image route;
- stale or expired source;
- public premise relies on private knowledge;
- the post would expose the internal content system rather than useful external proof.

Missing primary evidence is always a hard failure, never a score penalty. Supplementary evidence quality may affect the evidence score after this gate passes.

### 9.2 Base score: 100 points

- Commercial relevance to target readers: 20
- Strength and specificity of evidence: 20
- Earned JT angle: 15
- Freshness or timeliness: 15
- Workflow specificity and usefulness: 10
- Novelty versus the last 45 days: 10
- Visual clarity in one image: 5
- Likelihood of prompting a qualified conversation: 5

Dimensions use only these anchors:

- **Commercial relevance (0/5/10/15/20):** none; broad builder interest; one named target-reader class; a current target-reader problem; direct support for a current buyer/recruiter objective.
- **Evidence (0/5/10/15/20):** none; weak secondary-only; one sufficient primary source; multiple corroborating sources or accepted project proof; accepted proof plus exact claim-level bindings and permission where required. Hard gates still apply before scoring.
- **Earned JT angle (0/5/10/15):** generic summary; adjacent opinion; direct relevant experience; verified build/decision experience that materially changes the interpretation.
- **Freshness (0/5/10/15):** remaining TTL at or below 25%; above 25% through 50%; above 50% through 75%; above 75%.
- **Workflow usefulness (0/5/10):** abstract observation; names inputs/owner/system or decision; provides a coherent implementable workflow shape without exposing protected implementation IP.
- **Novelty (0/5/10):** repeats two of problem/mechanism/outcome from recent published history; repeats one; repeats none. Exact `semanticKey` matches are already hard-blocked.
- **Visual clarity (0/3/5):** viable but dense reconstruction; clear visual requiring production; safe source or simple schematic already defined.
- **Qualified-conversation potential (0/2/5):** no target action; likely relevance to a named reader; directly exposes a problem a named target reader could discuss or buy help with.

Exact deductions:

- permission required but valid permission exists with less than 72 hours remaining: -15;
- same niche already published twice in the previous seven days: -10;
- same visual route used for the previous three published posts: -5;
- supplementary evidence is single-source or incomplete but primary evidence is sufficient: -5;
- thesis requires context that cannot fit clearly in the post: -10;

Any unresolved privacy risk, expired permission, or missing primary evidence is a hard failure rather than a deduction.

No candidate below 75 before diversity adjustment can become a packet. Scores are inspectable, never shown as a proxy for certainty. Ties resolve by evidence score, then commercial relevance, then newest primary-event timestamp, then lexicographic `candidateId`.

Exact duplicate blocking uses normalized source hashes and exact `semanticKey` matches. A `semanticKey` match inside 45 days is a hard failure. A pinned semantic-similarity checker may flag near-duplicates for QA, but it cannot silently block or select candidates; its model/version, threshold, and result must be recorded.

`semanticKey` components are controlled taxonomy IDs, not free prose. They are NFKC-normalized, lowercased ASCII slugs and joined exactly as `lane|niche|problem|mechanism|outcome`. A new taxonomy term requires a versioned taxonomy entry with definition and aliases before scoring; models cannot invent one inline.

### 9.3 Mix controller

The mix is a rolling target, not a weekly quota. Over the latest eight **published** posts, aim for:

- three build/project proof posts;
- three company/niche teardowns;
- two AI news posts.

The selector first applies the 75-point eligibility threshold, then ranks eligible candidates. For each lane, `deficit = targetCount - actualCount` in the last eight published posts. Diversity adjustment is `clamp(deficit * 2, -6, +6)`. It cannot make an ineligible candidate eligible. It never promotes a weak lane to satisfy the mix.

### 9.4 Selection behavior

Each scheduled selection run emits zero or one packet. A second packet in the same week requires a separate run and a different semantic cluster. Maximum: three newly admitted revision families per Monday-through-Sunday ET week. Replays and revisions of an existing family do not consume another weekly slot. Approval and publication have no separate quota, but only payloads admitted under the weekly cap may reach them.

Only one unresolved `revisionFamilyId` may exist at a time. The family lock begins when its first packet enters `admitted` and persists across holds, revision requests, superseded packet versions, and pre-QA replacement work. It releases only when the latest family version is `rejected`, `expired`, `posted`, or `closed` with no replacement in progress. Later runs may collect and score candidates but may not admit another family. `hold` expires at the earlier of seven days or the packet's content expiry. Expiry returns the candidate to `expired`; it does not erase JT's decision history.

## 10. Writing system

The writer receives only:

- the bound candidate and claim map;
- the most relevant gold-set examples;
- current voice and platform rules;
- recent-post semantic clusters;
- required output schema.

It does not receive the full workspace.

Generation sequence:

1. draft the factual spine from evidence;
2. choose the best structure for the candidate mode;
3. translate through JT's voice;
4. remove unsupported or generic claims;
5. compare against recent semantic clusters;
6. produce one final post, not a menu of drafts;
7. run deterministic and model-based QA.

Model routing remains replaceable. Initial model choice should be decided through blinded JT ratings on the three fixtures, factual accuracy, hard-gate pass rate, and edit distance. Vendor reputation alone is not enough.

## 11. Exactly-one-image production and router

Every packet must choose exactly one route. A Claude Design prompt is an intermediate production input, not the final visual. A packet cannot reach `rendered`, `qa_passed`, or Mission Control admission until one concrete image asset exists and its bytes, dimensions, type, and hash are recorded.

The visual-production component owns rendering and validation:

- safe screenshot capture/crop;
- reconstruction or diagram rendering;
- primary-source crop creation;
- ingestion of the image returned from a manual Claude Design step when no approved API path exists;
- storage under a packet-versioned local asset path;
- asset hashing, metadata extraction, and QA.

### 11.1 Workflow or project build

Preferred order:

1. permission-safe screenshot of the real workflow when it is legible and reveals no client, credential, URL, record, prompt, or proprietary routing detail;
2. reconstructed workflow map with dummy labels;
3. clean decision-boundary or before/after diagram.

Blur is not sanitization. If a screenshot needs blur to be safe, use a reconstruction instead.

The screenshot route requires a recorded permission result naming the source, reviewer, allowed scope, timestamp, and expiry. A renderer may reject a screenshot; it may not grant permission.

### 11.2 AI news

Use a clean crop of the authoritative announcement or primary-source artifact with source attribution and date only when reuse is permitted. The crop must preserve context and must not imply JT created or endorsed the source material. If reuse rights are unclear, render a text-first source card that paraphrases the announcement, names and links the source in packet metadata, and uses no logo, proprietary artwork, or source screenshot.

### 11.3 Company or niche teardown

Use one clean system schematic showing public input, proposed workflow, human approval point, system of record, and operating outcome. It must be labeled `Proposed system based on public information` and the packet must retain the public sources used to construct it.

### 11.4 Claude Design production path

When any of the three core modes needs a designed reconstruction or schematic, produce a complete Claude Design prompt with:

- 1080 x 1350 portrait canvas;
- one idea and one focal hierarchy;
- cold, restrained systems-architect aesthetic;
- exact on-image copy;
- layout zones and safe margins;
- typography, color, and contrast rules;
- required labels and attribution;
- prohibited imagery, claims, logos, and decorative clutter.

If this route requires JT to paste the prompt into Claude Design, the packet remains `visual_pending`. The returned image is ingested, hashed, and checked before the packet can become review-ready.

### 11.5 Visual QA

- readable at mobile feed width;
- no more than one conceptual message;
- no tiny node labels or illegible screenshots;
- no client/private data;
- no unlicensed or misleading imagery;
- correct attribution;
- alt text describes the informational content, not decorative style;
- 4:5 crop and safe areas verified.

## 12. Review packet and Mission Control

The packet becomes one governed Mission Control card. The card must show:

- why this candidate won;
- the post text;
- exactly one rendered and validated image;
- evidence and claim bindings;
- freshness and expiry;
- all QA results;
- the intended reader and outcome hypothesis;
- `approve`, `edit`, `reject`, and `hold` actions;
- a required rejection reason taxonomy when rejected.

Approval binds the exact post and visual payload hash. A changed post or image requires a new version. Approval never means publication.

Lifecycle rules:

- `edit` creates a new packet version, links the old version through `supersedesPacketId`, and clears approval;
- `revision_requested` blocks later admission until a revised payload passes QA;
- `reject` is terminal for that packet version and requires a reason;
- `hold` obeys the backpressure and expiry rules in §9.4;
- `approved` permits JT to publish but performs no external action;
- only a JT-supplied or independently verified publication URL moves the packet to `posted`;
- the `posted` outcome records the exact final published text and hash; if JT changed text during manual publication, it also emits an `edit_delta` event before outcome attribution;
- no metrics or outcomes may mark a packet posted.

## 13. Learning loop

The system learns from four classes of evidence:

1. **Taste:** JT's approval, rejection, and edit delta.
2. **Quality:** factual corrections, guard failures, privacy issues, and originality failures.
3. **Distribution:** impressions, reactions, comments, saves, and reposts.
4. **Business value:** qualified replies, target-reader profile views, recruiter conversations, referrals, buyer conversations, and opportunities.

Rules become durable only after evidence:

- one edit updates the case record;
- the same edit pattern three times proposes a voice rule;
- a rule becomes active only after JT approval or a deterministic safety reason;
- performance never overrides factual, privacy, or voice gates;
- low reach alone does not condemn a post at JT's current audience size.

V1 does not change weights automatically. It may produce a calibration proposal only after at least 30 published posts, including at least eight from each core mode. The proposal must separate commercial outcomes from reach metrics, include old and proposed weights, show sensitivity on the full labeled set, define rollback, and wait for explicit JT approval. Safety, privacy, evidence, rights, and publication gates are never learnable weights.

## 14. Automated schedule

The target operating rhythm after acceptance is:

- **Daily:** collectors ingest new proof, project, news, and company signals; deduplicate and expire candidates.
- **Monday morning:** portfolio review and first selection run.
- **Wednesday morning:** second selection run using new evidence and the week's first decision.
- **Friday morning:** optional third selection run only when a candidate clears the same threshold.
- **After JT posts:** request the final published text and URL once; capture exact edits.
- **24 hours and seven days after posting:** read or request outcome metrics, then append outcome events.
- **Monthly:** review gold-set coverage, lane mix, stale sources, repeated edits, and commercial outcomes.

This is a target rhythm, not authorization to create or enable jobs. Every recurring job requires a separate explicit JT approval at the schedule gate. No recurring schedule is created or enabled until each of the three modes has one accepted manual fixture, replay/deduplication is proven, stale sources fail closed, and the kill switch is tested.

The kill switch is owned by JT. When engaged, it blocks collection and selection before network or model calls and cannot be bypassed by a retry. Recurring automation is disabled by default until the separate schedule gate. Recovery requires a dry run, source-health proof, zero duplicate admission, and explicit re-enable approval. Disabling the system preserves ledgers and open decisions.

## 15. Failure behavior

- Source unavailable: suppress affected candidates and name the gap.
- Primary evidence missing: reject candidate.
- Candidate below threshold: `SKIP`.
- Duplicate or stale candidate: expire without drafting.
- Writer or image failure: preserve candidate and receipt; do not emit a partial Mission Control card.
- QA failure: one bounded repair attempt, then reject with reason.
- Mission Control unavailable: retain packet locally and retry idempotently; never create a second review surface.
- Outcome unavailable: mark unknown; never infer zero.
- Conflicting source facts: block until resolved.

## 16. Evaluation and acceptance

### Fixture 1: build proof

Use **Approval is not execution** to prove exact-payload evidence binding, buyer-facing writing, and a single decision-boundary visual.

### Fixture 2: teardown

Choose a current public company trigger and prove public-evidence collection, company scoring, no-internal-access framing, and a proposed-system schematic.

### Fixture 3: AI news

Use a JT-supplied X post or approved public signal and prove primary-source verification, differentiation from summary content, attribution, and either a rights-cleared source crop or the compliant original text-first source-card fallback.

### Acceptance measures

- 100% of material claims map to evidence.
- Zero privacy or rights failures.
- Zero semantic duplicates inside the cooldown window.
- All deterministic guards pass.
- JT rates voice, usefulness, and visual fit independently from 1–5 for each fixture. Every dimension must score at least 4, and no safety/evidence/rights hard gate may fail.
- Exact edit distance and rejection reasons are captured.
- Packet replay creates no duplicate.
- Approval is exact-payload-bound and does not publish.
- Source outage and stale-candidate tests fail closed.

A material claim is any externally checkable statement about a company, product, event, client, build, metric, chronology, capability, or outcome. Every material claim needs a bound source pointer and exact supporting excerpt or structured field.

Fixture sources are frozen locally with source URI, retrieval timestamp, exact bytes or compliant excerpt, and SHA-256. Expected eligibility, lane, hard-gate results, semantic key, minimum score, visual route, and lifecycle transitions are declared before implementation. Live mutable webpages cannot be the sole acceptance oracle.

Deterministic acceptance guards are: schema validation, canonical hashing, state-transition validation, permission/expiry validation, exact semantic-key cooldown, evidence coverage, banned-pattern/voice guard, privacy/secret scan, image metadata and dimensions, attribution/rights result, payload replay, and Mission Control idempotency.

## 17. Bounded implementation programs

Each program receives its own approved implementation plan and acceptance gate. Later programs may depend on accepted artifacts from earlier programs; they are not one giant build plan.

### Program 1: contracts and corpus

Freeze all five typed schemas, authority/permission records, rejection taxonomy, lifecycle state machines, taxonomy, frozen fixture sources, and the three versioned gold-set collections. Materialize the prose contracts as machine-readable schemas and transition tests, including every globally required stable ID and idempotency key. Repair the edit-delta capture path and reconcile stale current-efforts/intelligence inputs. Defer Notion, n8n, recurrence, and model optimization.

### Program 2: deterministic candidate engine

Build append-only signal and candidate ledgers, deduplication, expiry, hard gates, fixed scoring, mix control, source-health receipts, and tests. Use frozen fixtures only.

### Program 3: three manual fixtures

Produce and evaluate one build, one teardown, and one AI-news packet. Keep JT as the only publisher.

### Program 4: generation and visual production

Automate gold-set retrieval, single-draft generation, visual-route selection, concrete image production/ingestion, deterministic guards, and bounded repair. The three core modes are the entire scope.

### Program 5: Mission Control and outcomes

Build exact-payload review admission, lifecycle transitions, decisions, edit deltas, publication receipts, and append-only outcomes. Drive and Notion projection remain deferred unless separately justified.

### Program 6: scheduled collectors and selectors

This program requires separate JT approval to create or enable any recurring job. Enable one source and one selection run at a time. Prove freshness, deduplication, source health, kill switch, cost, and rollback before adding the next. n8n is optional and must earn its use by reducing proven deterministic burden.

### Deferred: calibration and optional integrations

Automatic recalibration, any fourth content mode, Notion projection, and n8n routing are outside v1. After at least 30 published posts and eight per core mode, the system may propose, but not apply, score/model changes under §13.

## 18. Opus 5.5 adversarial review gate

The Opus review happens after this design is internally reviewed and before the implementation plan is frozen.

The prompt must be self-contained and ask Opus to attack:

- wrong abstractions and duplicated owners;
- missing signal sources or stale-source risks;
- scoring and mix-controller failure modes;
- gold-set contamination and overfitting;
- company/news selection quality;
- evidence, privacy, rights, and attribution failures;
- image-route feasibility;
- learning-loop incentives and misleading metrics;
- operational burden, cost, and silent failures;
- implementation sequence and unnecessary complexity.

Opus must return one recommended architecture and a ranked `remove`, `simplify`, `add`, and `defer` list. It must distinguish verified facts from assumptions and may not propose automatic publishing.

## 19. Success condition

The system is successful when JT can open Mission Control two or three times in a strong week, see one complete evidence-bound post-and-image packet at a time, make a fast decision, publish it himself, and have the system learn from the final text and outcome without creating duplicate work or stale filler.
