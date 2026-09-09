# AI Workflow Growth Operating System Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents are available) or superpowers:executing-plans to implement this plan. Steps use checkbox syntax for tracking.

**Goal:** Build one evidence-backed workflow intelligence engine that powers consulting prospecting first, then JT's personal content, job-market packages, and app marketing, while keeping every send, post, application, schedule, production change, and paid action behind explicit approval.

**Architecture:** A new shared engine stores normalized facts, research evidence, workflow blueprints, drafts, media briefs, approvals, and outcomes. n8n executes deterministic collection and routing. OpenClaw owns orchestration, approvals, memory, and delivery queues. GPT writes and evaluates voice-sensitive copy. Grok researches public X discourse and, only with approved X OAuth access, private likes/bookmarks. Claude Code or Codex builds and maintains code-heavy components. Mission Control remains the human decision surface.

**Tech Stack:** Python 3.12, TypeScript, JSON Schema, SQLite or Postgres-compatible structured storage, n8n, OpenClaw, Mission Control/Convex, GPT-5.6 Sol, xAI/Grok, Claude Code/Codex, Google Drive, Notion, X API, GitHub Actions, pytest, Vitest.

---

## 1. Executive decision

Build one program, not five disconnected automation stacks.

Release order:

1. Consulting prospect intelligence and outreach packets.
2. JT LinkedIn and X content.
3. Job-market discovery and application packages.
4. App-marketing engine configured for Nash Satoshi, Action Arena, and Yardstick.

The consulting lane goes first because it can create revenue and produces reusable inputs for the personal-content lane: workflow teardowns, niche observations, implementation decisions, screenshots, and measured outcomes.

The first release stops at verified, send-ready packets. It does not send email. The content releases stop at post-ready drafts and media assets. They do not post. The job release stops at verified Drive packages. It does not apply. The app release stops at review-ready content queues. It does not publish.

## 2. Non-negotiable boundaries

- JT is the final sender of cold outreach.
- JT is the final publisher of LinkedIn, X, and app content.
- JT is the final applicant for jobs.
- No new or edited recurring schedule is activated without separate approval.
- No production deployment, external account mutation, paid service, or domain change occurs during plan execution unless separately approved.
- No client name, private client data, unpermissioned metric, or confidential artifact enters public content or prospect materials.
- No speculative pain is presented as fact. Every claim is labeled verified, inferred, or unknown.
- No email is considered send-ready without a named buyer and a reachable verified channel.
- No social post is considered ready without source evidence, voice validation, duplication checks, and one approved visual.
- No job package is generated until the official or authoritative posting is verified live and JT passes the evidence-backed competitiveness gate.
- AgentGuard never appears in resume Key Projects.
- Every external action has an approval record and idempotency key.

## 3. System map

### 3.1 Owner surfaces

| Fact | Authoritative owner | Consumers |
|---|---|---|
| n8n implementation patterns and failure lessons | /Users/jtsomwaru/projects/n8n-agent/tasks/lessons.md | Workflow blueprint and build agents |
| Consulting client and prospect state | Existing consulting pipeline and Mission Control | Prospect lane, daily brief |
| Tasks and approval state | Mission Control/Convex | OpenClaw and JT |
| Long-term decisions and personal preferences | OpenClaw memory | All lanes |
| Content voice and public proof rules | Existing content skills and memory/content-voice.md | Personal and app content lanes |
| Job history and application state | /Users/jtsomwaru/projects/job-market-agent | Job lane |
| Generated resumes and cover letters | Google Drive Job Applications folders | JT |
| App truth | Each app repository and its approved marketing brief | App marketing lane |
| Shared normalized research and generated candidate artifacts | New workflow-growth-engine repository | All lanes |

### 3.2 New repository

Create: /Users/jtsomwaru/projects/workflow-growth-engine

Proposed structure:

~~~text
workflow-growth-engine/
  README.md
  AGENTS.md
  CLAUDE.md
  package.json
  pyproject.toml
  config/
    lanes.json
    models.json
    source-policies.json
    approval-policies.json
  schemas/
    source-record.schema.json
    entity.schema.json
    prospect.schema.json
    workflow-blueprint.schema.json
    content-candidate.schema.json
    media-brief.schema.json
    job-candidate.schema.json
    application-package.schema.json
    app-profile.schema.json
    approval.schema.json
    outcome.schema.json
    run-receipt.schema.json
  src/
    core/
      ids.py
      provenance.py
      dedupe.py
      validation.py
      approvals.py
      outcomes.py
      run_receipts.py
    connectors/
      web.py
      x.py
      drive.py
      mission_control.py
      notion.py
      n8n.py
    prospecting/
      discover.py
      enrich.py
      qualify.py
      blueprint.py
      draft_email.py
      packet.py
    content/
      ingest.py
      voice.py
      select.py
      draft_linkedin.py
      draft_x.py
      media.py
      publish_packet.py
    jobs/
      discover.py
      verify_live.py
      score.py
      package_request.py
    apps/
      load_profile.py
      select_angle.py
      draft.py
      media.py
    orchestration/
      run_lane.py
      queue.py
      health.py
  prompts/
    prospect-research.md
    workflow-blueprint.md
    cold-email.md
    linkedin.md
    x.md
    image-brief.md
    job-evaluator.md
    app-content.md
  data/
    sources/
    entities/
    prospects/
    blueprints/
    content/
    jobs/
    apps/
    approvals/
    outcomes/
    runs/
  tests/
    fixtures/
    unit/
    integration/
    contracts/
  reports/
  docs/
    data-contracts.md
    runbook.md
    cost-model.md
    threat-model.md
~~~

### 3.3 Shared event flow

1. A connector captures a source with timestamp, URL, hash, and source type.
2. The normalizer creates or updates an entity without discarding raw evidence.
3. A lane-specific evaluator assigns eligibility, confidence, and reason codes.
4. An agent drafts a bounded artifact from cited facts only.
5. A deterministic verifier checks schemas, citations, privacy, duplication, formatting, and approval requirements.
6. Mission Control receives one review task with the artifact and exact next action.
7. JT approves, rejects, or edits.
8. Only an approved external-action adapter may stage the final action. Initial releases never execute the external action.
9. Outcomes feed back into lane scoring and prompt evaluation. Prompts are not auto-mutated.

## 4. Tool assignment

| Tool | Best use | Do not use it for |
|---|---|---|
| n8n | Deterministic triggers, API calls, normalization, routing, retries, queues, and handoffs | Unbounded research judgment or final voice writing |
| OpenClaw | Cross-system orchestration, state, schedules, approval routing, durable memory, Telegram delivery | High-volume scraping or hidden automatic sending |
| GPT-5.6 Sol | JT voice, LinkedIn and X drafting, job documents, final copy evaluation | Raw bulk fetching |
| Grok/xAI | Public X-native search, current discourse, source discovery, pattern analysis | Assuming access to private likes/bookmarks without OAuth |
| X API OAuth | JT likes, bookmarks, lists, profile posts, and engagement data when scopes permit | Scraping around missing permission or platform limits |
| Claude Code / Codex | Repository work, tests, refactors, workflow JSON generation, technical review | Daily voice copy by default |
| Mission Control | Human review queue, priority, status, approval evidence, next action | Storing raw corpora or client documents |
| Google Drive | Final resumes, cover letters, client/prospect deliverables, reviewable documents | Canonical machine state |
| Notion | Content calendar and swipe-file consumption | Automation health or approval truth |

Model-routing policy:

- Use one model by default.
- Use a second independent evaluator only for high-risk claims, final job packages, or buyer-facing artifacts.
- Use four-model ensembles only when disagreement itself is valuable and the outcome justifies the cost.
- Every model call must declare task type, prompt version, input hash, output hash, token/cost estimate, and verifier result.

## 5. Core data contracts

### 5.1 Source record

Required fields:

- source_id
- source_type: website, job_posting, x_post, linkedin_post, app_repo, client_proof, public_news
- source_url or local_artifact_path
- captured_at
- published_at when known
- author or organization
- raw_hash
- quoted_spans
- trust_level: primary, authoritative_secondary, unverified_secondary
- access_scope: public, private_jt, confidential_client
- allowed_uses: research, internal_draft, public_quote, prospect_copy
- expiration_at when freshness matters

### 5.2 Prospect

Required fields:

- prospect_id
- organization
- niche
- geography
- named_buyer
- buyer_title
- verified_channel
- channel_status
- source_evidence
- observed_workflow_signals
- inferred_pains
- proof_match
- tier
- disqualification_reasons
- prior_contact_state
- last_verified_at

Hard gate: no named buyer plus no reachable channel means research-only, never send-ready.

### 5.3 Workflow blueprint

Required fields:

- blueprint_id
- prospect_id or niche_template_id
- current_workflow_hypothesis
- trigger
- inputs
- deterministic_steps
- LLM_reasoning_steps
- model choice and why
- systems touched
- human approvals
- exception paths
- final actions
- audit evidence
- rollback behavior
- assumptions
- unresolved questions
- estimated implementation range
- proof references

### 5.4 Content candidate

Required fields:

- candidate_id
- lane: jt_linkedin, jt_x, nash, action_arena, yardstick
- source_ids
- angle
- audience
- proof_assets
- draft
- platform_constraints
- visual_type
- media_brief_id
- duplicate_check
- voice_score
- factual_verification
- approval_state
- scheduled_or_posted_at
- performance_outcome

### 5.5 Approval

Required fields:

- approval_id
- artifact_id
- action_type: send_email, post_linkedin, post_x, submit_application, activate_schedule, deploy
- requested_at
- requested_by
- decision: pending, approved, rejected, expired
- decided_at
- decision_source
- exact_payload_hash
- idempotency_key

Approval applies only to the exact payload hash. Editing the payload invalidates approval.

### 5.6 Run receipt

Each run writes a receipt even when it produces zero artifacts:

- run_id
- pipeline_name
- prompt_version
- started_at and finished_at
- inputs_processed
- records_created
- records_skipped
- sources_reached
- sources_failed
- validation_status
- delivery_status
- completion_status
- error_codes
- artifact_paths
- next_consumer

## 6. Release 0: shared spine

**Purpose:** Prove records, provenance, approvals, and run health before any lane automation.

**Files:** repository skeleton, schemas, src/core, tests/unit, tests/contracts, docs/runbook.md.

### Task 0.1: Repository bootstrap

- [ ] Create an isolated worktree for workflow-growth-engine.
- [ ] Create repository structure from section 3.2.
- [ ] Add ignore rules for credentials, raw private exports, temporary browser data, and generated caches.
- [ ] Add AGENTS.md and CLAUDE.md with source-trust, external-action, and lessons-reading rules.
- [ ] Run credential scan against tracked and untracked-not-ignored files.
- [ ] Commit the empty spine.

Acceptance: fresh clone installs without protected credentials and passes an empty test suite.

### Task 0.2: Schemas and validation

- [ ] Write failing contract tests for all schemas.
- [ ] Run tests and confirm failure on missing schemas.
- [ ] Add the schema files listed in section 3.2.
- [ ] Implement strict validation with unknown-field rejection for external-action records.
- [ ] Add fixtures for valid, malformed, stale, duplicated, and permission-forbidden records.
- [ ] Run tests and confirm all fixtures produce expected codes.
- [ ] Commit.

Acceptance: validation distinguishes invalid data, stale data, blocked permission, and environment failure.

### Task 0.3: Provenance and deduplication

- [ ] Write failing tests for source hashes, canonical URLs, duplicate entities, and superseding records.
- [ ] Implement provenance and dedupe modules.
- [ ] Preserve raw source evidence and append corrections instead of silently rewriting history.
- [ ] Run tests.
- [ ] Commit.

Acceptance: identical sources cannot create duplicate send-ready artifacts.

### Task 0.4: Approval state machine

- [ ] Write failing tests for pending, approved, rejected, expired, edited-after-approval, and duplicate-action cases.
- [ ] Implement payload hashes and idempotency keys.
- [ ] Prove that an edited payload returns to pending.
- [ ] Prove that no external adapter can execute without an exact approved hash.
- [ ] Commit.

Acceptance: zero external-action function paths are reachable without a valid approval record.

### Task 0.5: Run receipts and health

- [ ] Write failing tests for zero-result, degraded, failed, delivered, and completed runs.
- [ ] Implement run receipts.
- [ ] Implement stale-pipeline detection from a registry, including NEVER_RAN.
- [ ] Add a health report that separates executed, result delivered, and whole request completed.
- [ ] Commit.

Acceptance: a quiet pipeline and a broken pipeline are never reported as the same state.

## 7. Release 1: consulting prospect intelligence and outreach packets

**Purpose:** Produce twenty verified send-ready packets in thirty days, beginning with small controlled cohorts.

### 7.1 Niche strategy

Start with property management and supportive housing because JT has relevant proof. Test adjacent niches only when they pass a workflow-similarity gate:

- recurring high-volume administrative work;
- fragmented inputs across inboxes, portals, spreadsheets, PDFs, or legacy systems;
- multiple handoffs and unclear ownership;
- time-sensitive exceptions;
- a manager who owns the workflow;
- accessible named buyers and channels;
- a credible proof or reusable workflow template.

Candidate expansion niches:

1. Supportive housing and affordable-housing operators.
2. Insurance agencies and MGAs with document-heavy servicing.
3. HVAC, construction, and specialty trades with office-to-field handoffs.
4. Wholesale distributors with catalog, PO, vendor, and exception queues.
5. Multi-location service businesses with intake, scheduling, and follow-up failures.

Do not research all niches at once. Run one niche cohort at a time and compare reply and qualification outcomes.

### Task 1.1: Import existing prospect truth

- [ ] Read the existing consulting pipeline schema and client/prospect files.
- [ ] Write an adapter test using five real anonymized records.
- [ ] Import without changing the source owner.
- [ ] Preserve prior contact, channel, tier, and disqualification state.
- [ ] Reject records missing stable source references.
- [ ] Commit.

Acceptance: no prospect is duplicated and no previously contacted prospect is treated as new.

### Task 1.2: Source collection workflow blueprint

Create an n8n blueprint before nodes. It must include:

- manual trigger for Release 1;
- input niche and cohort size;
- public-source search connectors;
- rate limits and per-domain retry policies;
- raw evidence capture;
- named-buyer discovery;
- verified-email or accepted-LinkedIn channel checks;
- dedupe against existing prospects;
- research-only output when the channel gate fails;
- run receipt and failure alert.

- [ ] Write happy-path fixture.
- [ ] Write no-buyer fixture.
- [ ] Write stale-source fixture.
- [ ] Write duplicate-prospect fixture.
- [ ] Write blocked-site fixture.
- [ ] Approve blueprint before building nodes.

Acceptance: the builder can implement without choosing data shapes or branch behavior.

### Task 1.3: Prospect qualification

Qualification is deterministic first, model-assisted second.

Binary gates:

- named buyer;
- reachable verified channel;
- workflow evidence or current trigger;
- proof or reusable pattern match;
- reason to contact now;
- no prior-contact conflict.

The model may summarize evidence and propose hypotheses. It may not manufacture a gate.

- [ ] Write failing tests for each gate.
- [ ] Implement reason codes.
- [ ] Add confidence labels to inferred pains.
- [ ] Prove that an inference cannot appear as a verified statement in copy.
- [ ] Commit.

Acceptance: every send-ready prospect passes all binary gates.

### Task 1.4: AI recipe generator

For each qualified prospect, generate a prospect-specific workflow hypothesis using the n8n lessons library.

Output:

- trigger and source inputs;
- current manual handoff hypothesis;
- deterministic automation steps;
- exact LLM reasoning node, if justified;
- confidence threshold;
- human review owner;
- exception queue;
- system-of-record update;
- audit trail;
- failure and recovery path;
- two assumptions that must be confirmed in discovery.

- [ ] Write a failing test that rejects an LLM node with no reason.
- [ ] Write a failing test that rejects a workflow with no approval or exception path.
- [ ] Generate three test recipes across different niches.
- [ ] Review them against n8n lessons.md.
- [ ] Commit.

Acceptance: no recipe is generic enough to fit fifty companies unchanged.

### Task 1.5: Cold-email draft generator

Draft 75 to 150 words with:

- 3 to 6 word subject;
- company or individual-specific opener;
- one workflow hypothesis clearly labeled as an observation or question;
- one permission-safe proof point;
- one reply-sized CTA;
- three-line signature;
- no em dash;
- no unsupported pain claim;
- no meeting link in M1;
- no auto-send.

- [ ] Create failing tests for length, signature, CTA count, em dash, missing source, and generic personalization.
- [ ] Generate M1, M2, and final follow-up separately.
- [ ] Add a copy evaluator that returns pass/fail and reason codes, not a rewritten draft.
- [ ] Require a new approval after any edit.
- [ ] Commit.

Acceptance: each packet passes the cold-email checklist and cites its research evidence internally.

### Task 1.6: Send-ready packet

One packet contains:

- buyer and channel evidence;
- company summary;
- observed signals;
- inferred pain with confidence;
- AI recipe;
- proof match;
- email sequence;
- personalization note;
- exclusions and unknowns;
- verification checklist;
- recommended send cohort.

- [ ] Render Markdown and Drive-friendly versions.
- [ ] Create one Mission Control review task per approved cohort, not per raw prospect.
- [ ] Include first action, why it matters, and done state.
- [ ] Commit.

Acceptance: JT can review a prospect in under three minutes and knows exactly what is verified versus inferred.

### Task 1.7: Cohort pilot

- [ ] Run five prospects manually.
- [ ] Review every research source and draft.
- [ ] Fix structural errors and add regression tests.
- [ ] Run a second cohort of ten.
- [ ] Measure verified-channel rate, draft pass rate, JT edit time, bounces, replies, positive replies, and priced conversations.
- [ ] Only after two clean cohorts propose a recurring schedule or volume increase.

Initial scale rule:

- Stage up to forty researched prospects in thirty days.
- Produce at least twenty verified packets.
- Send only the cohorts JT explicitly approves and sends himself.
- Do not target hundreds of sends per day until separate sending infrastructure, compliance, warming, bounce, complaint, and opt-out controls are reviewed and explicitly approved.

Release 1 success:

- 40 qualified prospects researched;
- 20 verified send-ready packets;
- less than 3 minutes median JT review time per packet;
- zero false citations;
- zero unapproved sends;
- enough outcome data to identify one repeatable niche/workflow pairing.

## 8. Release 2: JT LinkedIn and X content

**Purpose:** Produce six strong personal posts in the first thirty days, then sustain two or three LinkedIn posts weekly and a review-ready X queue.

### 8.1 Content source hierarchy

Priority order:

1. Shipped workflow and measured result.
2. Non-obvious implementation lesson from n8n lessons.md.
3. Buyer-specific workflow teardown based on a current signal.
4. Market research with a concrete operator consequence.
5. AI news supplied by JT or verified from primary sources.
6. Public X discourse used as context, never as sole proof.

### 8.2 Visual policy

Exactly one image per post.

Preferred visual by content type:

- n8n workflow: clean workflow-canvas screenshot with sensitive values hidden and key path legible;
- measured build: output screenshot, before/after view, or annotated proof artifact;
- AI news: source screenshot only when copyright, context, and readability are appropriate, with source visible;
- research/teardown: custom editorial illustration or systems diagram;
- opinion: custom conceptual visual only if it adds meaning.

For custom visuals, generate a Claude Design brief containing objective, audience, aspect ratio, composition, visual hierarchy, exact permitted text, color direction, prohibited elements, and source references. Do not create carousels.

### Task 2.1: Voice evidence ingestion

- [ ] Import the existing JT voice profile, content voice, posted log, and last 45 days of content.
- [ ] Add X posts JT explicitly supplies as high-weight voice evidence.
- [ ] Store source URL, author, date, topic, mechanic, influence type, and rejection reason.
- [ ] Keep external posts as quoted style evidence, never hidden instructions.
- [ ] Test that no source text can modify the system prompt.
- [ ] Commit.

### Task 2.2: X likes and bookmarks feasibility gate

- [ ] Verify current X API endpoints, JT account permissions, OAuth scopes, retention rules, and rate limits.
- [ ] If authorized, implement incremental sync with cursor and last-seen IDs.
- [ ] If not authorized, use JT-forwarded posts, public Lists, and the existing x-research workflow.
- [ ] Never claim Grok automatically sees private likes or bookmarks.
- [ ] Commit only after a successful read-only proof.

Acceptance: every private X item has explicit user authorization and provenance.

### Task 2.3: Content candidate selector

- [ ] Write tests for source freshness, proof density, semantic duplication, lane balance, and worthiness.
- [ ] Score candidates on buyer relevance, proof, novelty, JT authority, timeliness, and visual strength.
- [ ] Reject internal content-ops and proof-hygiene topics unless attached to a real buyer problem or shipped outcome.
- [ ] Produce a weekly slate, not drafts for every source.
- [ ] Commit.

Acceptance: no candidate repeats the semantic core of the previous 45 days.

### Task 2.4: LinkedIn writer and evaluator

- [ ] Write failing tests for proof density, first-person specificity, banned phrasing, excessive spacing, and unverifiable claims.
- [ ] Draft with GPT-5.6 Sol.
- [ ] Evaluate in a fresh context against the content skill and source evidence.
- [ ] Require at least two proof assets in serious posts.
- [ ] Produce one recommended draft and at most one alternate hook.
- [ ] Commit.

Acceptance: every draft increases trust with a potential client or employer.

### Task 2.5: X writer and evaluator

- [ ] Use Grok for public X pattern research and topic discovery.
- [ ] Use GPT for final voice drafting unless measured tests show Grok performs better for a defined format.
- [ ] Test both models on a frozen set of twenty JT-rated examples.
- [ ] Choose by blind JT preference and factual accuracy, not model reputation.
- [ ] Enforce six to twenty-five words for standalones and five tweets maximum for threads.
- [ ] Reject polished guru compression and generic automation slogans.
- [ ] Commit.

Acceptance: model choice is backed by JT ratings and no source imitation crosses into copying.

### Task 2.6: Image strategy generator

- [ ] Implement deterministic selection among screenshot, annotated artifact, source screenshot, custom illustration, or no-publish.
- [ ] Create media-brief schema and renderer.
- [ ] Add privacy and legibility checks for screenshots.
- [ ] Add copyright/source check for news screenshots.
- [ ] Add one-image and aspect-ratio checks.
- [ ] Commit.

Acceptance: each publish packet contains one usable visual or is blocked with a reason.

### Task 2.7: Content review packet

Packet fields:

- platform;
- recommended posting window;
- final copy;
- evidence sources;
- visual file or Claude Design prompt;
- alt text;
- duplication report;
- voice and factual checks;
- approval control;
- optional reply targets for X.

- [ ] Push approved items to Notion only after validation.
- [ ] Do not post automatically.
- [ ] Record JT edits and eventual performance outcomes.
- [ ] Commit.

Release 2 success:

- six approved personal posts in thirty days;
- ninety percent require less than five minutes of JT editing;
- zero source or privacy failures;
- every post has one approved visual;
- measured improvement in qualified profile visits, inbound conversations, or relevant engagement.

## 9. Release 3: job-market research and package generation

**Purpose:** Improve the existing Job Hedge rather than replace it.

### Task 3.1: Live-role verification hardening

- [ ] Import the current official-source and expired-marker regression tests.
- [ ] Add authoritative ATS or employer-careers confirmation where available.
- [ ] Reject aggregator-only listings when official truth contradicts them.
- [ ] Record verified_at and freshness expiration.
- [ ] Test HTTP 200 expired pages.
- [ ] Commit.

### Task 3.2: Discovery and scoring

- [ ] Search duties before titles.
- [ ] Enforce NYC/remote and compensation constraints.
- [ ] Apply the existing 25-point rubric and evidence-backed competitiveness gate.
- [ ] Exclude roles requiring developer, ML engineering, Apex, quota-carrying sales, relocation, or unsupported credentials.
- [ ] Deduplicate against applied, rejected, expired, and previously surfaced roles.
- [ ] Commit.

### Task 3.3: Automatic package request, not blind package creation

- [ ] For roles that pass the gate, create a structured package request.
- [ ] Generate resume and cover letter with GPT-5.6 Sol.
- [ ] Enforce AgentGuard exclusion, formal correspondence, direct confidence, positive framing, and the preferred warm close.
- [ ] Run ATS, JD mapping, evidence, privacy, parse, DOCX, and live Drive-readback checks.
- [ ] Stop on any failed check.
- [ ] Create one Mission Control task with role and Drive links.
- [ ] Never submit the application.
- [ ] Commit.

### Task 3.4: Morning brief

Each morning reports:

- verified live roles that cleared the bar;
- score and rationale;
- honest gap;
- official application link;
- resume and cover-letter links when the package passed;
- explicit no-role result when nothing qualified;
- run health separated into execution, delivery, and completion.

Release 3 success:

- zero expired jobs surfaced;
- zero inflated claims;
- packages exist only for competitive roles;
- every package passes live Drive readback;
- JT can decide and apply without becoming the package project manager.

## 10. Release 4: app-marketing engine

**Purpose:** Build one configurable engine, not three custom systems.

### 10.1 App profile contract

Each app must provide:

- product truth and current release state;
- target user and job to be done;
- value proposition;
- proof and screenshots;
- approved claims;
- prohibited claims;
- competitors and category language;
- content pillars;
- platform priorities;
- conversion action;
- brand and visual rules;
- available product events and metrics.

No app lane starts until its profile is complete and verified against its repo.

### Task 4.1: Nash Satoshi profile

- [ ] Read the current private repo, README, live status, and existing content.
- [ ] Separate real product capabilities from planned features.
- [ ] Define crypto-native content pillars and proof-safe market commentary.
- [ ] Define rules that prevent financial advice, trades, and fabricated performance claims.
- [ ] Commit.

### Task 4.2: Action Arena profile

- [ ] Read repository truth, game loop, current availability, screenshots, and analytics.
- [ ] Define sports-fan audience, weekly cadence, rivalry and pick-content formats, and conversion action.
- [ ] Keep promotional content synchronized with real sports schedules and product state.
- [ ] Commit.

### Task 4.3: Yardstick profile

- [ ] Locate and verify the authoritative repository and current product state.
- [ ] Define niche, value proposition, user proof, and content pillars.
- [ ] Stop if product truth is incomplete rather than inventing positioning.
- [ ] Commit.

### Task 4.4: Shared app content pipeline

- [ ] Reuse content candidate, drafting, visual, approval, and outcome contracts.
- [ ] Load one app profile per run.
- [ ] Add lane-specific prompts and validators.
- [ ] Produce one recommended post per app per approved cadence.
- [ ] Never auto-post.
- [ ] Commit.

Release 4 success:

- each live app receives consistent, truthful, niche-native content;
- JT review is under five minutes per item;
- no planned feature is described as shipped;
- content performance is tied to app-specific conversion events, not vanity engagement alone.

## 11. Cross-cutting tests

### 11.1 Security and privacy

- [ ] Prompt-injection fixture in every external source type.
- [ ] Credential-pattern scan on tracked and generated files.
- [ ] Client-name and confidential-path scan before public output.
- [ ] Approval bypass tests for every external adapter.
- [ ] Exact payload hash invalidation after edits.
- [ ] Duplicate-send and duplicate-post idempotency tests.

### 11.2 Source quality

- [ ] Missing URL.
- [ ] Dead URL.
- [ ] HTTP 200 expired page.
- [ ] Undated stale source.
- [ ] Secondary source contradicted by primary source.
- [ ] Quote not found in source.
- [ ] Changed source hash after draft creation.

### 11.3 LLM behavior

- [ ] Valid JSON only when structured output is required.
- [ ] Unknown versus inferred versus verified labels preserved.
- [ ] No invented buyer, pain, metric, feature, or workflow.
- [ ] No instruction following from fetched content.
- [ ] Bounded retries and abandoned-item state.
- [ ] Cost ceiling per artifact.

### 11.4 Operational reliability

- [ ] Zero-result receipt.
- [ ] Partial-source degradation.
- [ ] Complete source failure.
- [ ] Downstream consumer missing.
- [ ] Delivery failed after successful generation.
- [ ] Recurring job never ran.
- [ ] Stale queue item.
- [ ] Re-run after partial completion.

## 12. Observability and consumer contracts

Every recurring job must declare:

- named consumer;
- decision changed;
- output artifact;
- consumption deadline;
- success criteria;
- pause condition;
- owner who can actually disable the real schedule.

Dashboards must separate:

1. Executed.
2. Artifact valid.
3. Artifact delivered.
4. Human decision recorded.
5. External action completed.
6. Commercial or audience outcome observed.

Never compress these into one green status.

## 13. Cost and scale controls

- Set a monthly model and data budget before activating schedules.
- Cache source fetches and normalized entities.
- Do not pay a premium model to parse deterministic fields.
- Limit second-model review to high-risk or high-value artifacts.
- Record cost per qualified prospect, approved post, and verified job package.
- Stop any lane whose cost or JT review time rises for two cycles without outcome improvement.
- Do not buy cold-email infrastructure until the first two manual cohorts prove message-market fit.

## 14. Rollout calendar

### Week 0: design and audit

- Confirm owner surfaces.
- Audit existing consulting, content, job, and app data.
- Define schemas and approval policies.
- Produce Release 0 blueprint.

### Weeks 1 to 2: shared spine

- Build schemas, validation, provenance, approvals, run receipts, and health.
- Prove all guards fail red and recover green.

### Weeks 3 to 4: consulting pilot

- Import existing prospects.
- Build manual prospect workflow.
- Produce first five packets.
- Fix errors and generate the next ten.

### Weeks 5 to 6: personal content pilot

- Ingest voice and sources.
- Produce LinkedIn and X candidates from real consulting artifacts.
- Generate one-image media packets.

### Weeks 7 to 8: job integration

- Harden live-role verification.
- Connect scoring to automatic verified package generation.
- Keep application submission manual.

### Weeks 9 to 10: app profiles and engine

- Validate Nash Satoshi, Action Arena, and Yardstick truth.
- Reuse the shared content pipeline with lane-specific configuration.

This calendar is directional. Each release begins only when the previous release passes its acceptance gate. No deadline overrides a failed gate.

## 15. Program scoreboard

### Consulting

- verified prospects;
- send-ready packets;
- median JT review time;
- sends confirmed by JT;
- bounce rate;
- replies;
- positive replies;
- priced conversations;
- projects won and cash collected.

### Personal content

- approved posts;
- JT edit time;
- qualified profile visits;
- relevant inbound conversations;
- saves and replies from target buyers or employers;
- source, privacy, and duplication failures.

### Jobs

- verified live roles;
- packages created;
- applications submitted by JT;
- recruiter screens;
- interviews;
- offers;
- stale-role and inflation failures.

### Apps

- approved posts;
- clicks or store visits;
- signups;
- activation events;
- retention-relevant events;
- truth or brand failures.

## 16. Kill and pause rules

Pause a lane when any of these occurs:

- an unapproved external action;
- a fabricated quote, buyer, metric, or product claim;
- a client privacy or permission breach;
- two consecutive cycles with no consumer action;
- review time exceeds the declared cap twice;
- source freshness cannot be proven;
- the real schedule is running while its registry says paused;
- model or data cost exceeds the approved ceiling;
- output volume grows while commercial or audience quality falls.

Preserve evidence and run receipts. Disable the actual schedule through its owning platform only with approval. Do not delete history as a substitute for diagnosis.

## 17. First implementation checkpoint

The first implementation session may do only the following:

1. Create an isolated worktree and repository skeleton.
2. Write schemas and failing contract tests.
3. Implement provenance, validation, approvals, and run receipts.
4. Run the full Release 0 test suite.
5. Produce a review artifact showing pass/fail evidence.

It may not:

- create or activate schedules;
- send email;
- post content;
- submit job applications;
- connect private X data;
- deploy production n8n workflows;
- alter Mission Control production schema;
- purchase or configure sending infrastructure.

## 18. Final acceptance gate before activation

Activation requires all of these:

- Release 0 tests pass from a fresh clone.
- Every lane has one authoritative input owner.
- Every generated claim has provenance.
- Every external adapter proves approval enforcement.
- Every recurring job has a real disable owner and procedure.
- Cost ceilings are approved.
- Telegram or Mission Control delivery is proven independently of generation.
- Manual pilot outputs meet quality targets.
- JT explicitly approves the exact lane and schedule being activated.

## 19. Recommended immediate next action

Approve only Release 0 and the manual five-prospect consulting pilot. Do not approve schedules or any other lane yet.

After Release 0 passes, use the n8n-blueprint skill to produce the node-by-node consulting source-collection and packet-routing workflow. Build it with the n8n agent only after the blueprint is approved and after reading the full n8n lessons file. This preserves the real asset: JT's accumulated workflow judgment, expressed as reliable recipes with clear inputs, reasoning nodes, controls, outputs, and recovery paths.
