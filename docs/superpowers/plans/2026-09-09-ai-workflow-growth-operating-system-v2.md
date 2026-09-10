# AI Workflow Growth Operating System v2 Implementation Plan

> **For agentic workers:** REQUIRED: Use `superpowers:subagent-driven-development` if subagents are available or `superpowers:executing-plans` otherwise. Steps use checkbox (`- [ ]`) syntax for tracking. This plan does not authorize purchases, sends, posts, applications, schedules, production deployments, account changes, or external deletions.

**Goal:** Turn JT's workflow-building advantage into one operating system that creates qualified consulting outreach, proof-led personal content, verified job packages, and app marketing packets while keeping JT's daily review burden under 45 minutes.

**Architecture:** Extend `jsomwarux/jt-ops` as the durable shared evidence and run-control spine. Keep specialist execution in the systems that already own it: n8n for deterministic workflows, the existing job-market agent for jobs, app repositories for product truth, and OpenClaw for orchestration, memory, Telegram delivery, and independent verification routing. Mission Control/Convex is the only human queue. No new `workflow-growth-engine` repository and no second Notion task board.

**Tech Stack:** `jt-ops`, n8n, `/Users/jtsomwaru/projects/n8n-agent/tasks/lessons.md`, OpenClaw, Mission Control/Convex, GitHub Actions, Claude Code/Codex/Grok Build, GPT-5.6 Sol, Grok/xAI API, optional Grok Automations and Grok Bot, X API OAuth, Google Drive, Notion Content Calendar, pytest, JSON Schema.

---

## 1. Final decisions

### 1.1 What the three model reviews settled

1. Agents research and draft; JT sends, posts, applies, purchases, and activates.
2. Mission Control is the only daily review surface.
3. Outputs must arrive as complete, child-clear packets, not research fragments.
4. n8n owns deterministic collection, routing, retries, and stateful workflow execution.
5. Models perform bounded judgment; deterministic checks verify their output.
6. Outreach intelligence and outreach delivery are separate systems.
7. Start with manual buyer motion; production automation catches up to proven work.
8. Expand one niche at a time using buyer evidence, not calendar time.
9. Improvement jobs propose diffs with evidence and tests; they never mutate their own instructions.
10. Normal daily review is 30 to 45 minutes. Ninety minutes is an overflow alarm, not the target.

### 1.2 The final forks

| Fork | Decision | Reason |
|---|---|---|
| Shared repository | Extend `jt-ops`; do not create `workflow-growth-engine` | A second generic spine duplicates schemas, receipts, health, and CI. |
| Domain implementations | Keep them in their current owner systems | `jt-ops` indexes and coordinates; it does not absorb the n8n agent, job-market agent, app repos, or private client files. |
| Orchestrator | OpenClaw/Eve routes work, memory, approvals, verification, and Telegram delivery | This capability already exists. Removing it would discard working integrations. |
| Durable run truth | `jt-ops` receipts, artifacts, PRs, and issues | OpenClaw must not be the sole source of execution truth or grade its own work. |
| Human queue | Existing Mission Control/Convex | No Notion or ClickUp duplicate. |
| Manual external motion | Start immediately from a newly requalified cohort | Automation may not delay sends or publishing. The old 57 are not automatically eligible. |
| Sending infrastructure | Prepare two-domain/four-inbox pilot in parallel after packet QA and explicit spend approval | Warmup is a long pole; fleet expansion still waits for message-market evidence. |
| LinkedIn writer | GPT first, Grok challenger | Final routing is decided by blind JT ratings by format. |
| X writer | Grok first, GPT challenger | Grok owns X-native research; final routing is still earned by blind tests. |
| Grok Bot | Optional bounded browser worker | It must prove facts or review-time savings that APIs/public web cannot. |
| Events | Monthly lightweight query | Not a production system. |
| Passive-income lane | Parked | Revisit only when it can mine proprietary pain, workflow, and client-learning data. |

### 1.3 What is not true

- The 57 existing prospect folders are **not** 57 fresh send-ready contacts. The current preflight skips 57 because an M-sequence is already active/pitched or a T3 send flag exists; one prospect is warm-up-only.
- `jt-ops` is not healthy merely because records validate. On 2026-09-09 the harvester validated 653 records and committed 30 new postings, then failed because the staging queue reached 600 bodies while ingestion did not drain it.
- A green agent run, a commit, or a generated packet does not prove task, delivery, or commercial success.
- Grok's general X access does not imply access to JT's private likes/bookmarks. Those require authenticated X API user access.
- Watchdog or an unlaunched delinquency workflow is not the default proof. Use the strongest permission-safe paid or accepted work available.

## 2. System boundary

### 2.1 Three systems and one board

#### System A: Research and Match Engine

Shared primitives serve two production lanes:

- **Prospects:** discover, enrich, verify buyer/channel, identify visible workflow signals, match permission-safe proof, draft an AI recipe and outreach packet.
- **Jobs:** collect, verify the official listing, score against JT's profile, generate a package only when the role clears the competitiveness gate.

Events may reuse collectors and scoring utilities, but remain a monthly query rather than a scheduled production lane.

#### System B: Content Engine

One pipeline with lane configuration for:

- JT LinkedIn;
- JT X;
- Yardstick;
- Nash Satoshi;
- Action Arena.

Shared stages: source evidence, candidate selection, platform-specific drafting, factual/voice checks, one-image selection, review packet, outcome capture.

#### System C: Outreach Delivery

Separate domains, mailboxes, authentication, warmup, sequencer, suppression, reply routing, bounce monitoring, unsubscribe handling, and campaign outcomes. It consumes approved packets; it never decides who is qualified or invents copy.

#### Board: Mission Control

Mission Control is the only Today/Waiting/Done surface. Notion remains the Content Calendar and Swipe File. Telegram is the doorbell and command surface, not a second task database.

### 2.2 Owner surfaces

| Fact | Authoritative owner | `jt-ops` role |
|---|---|---|
| Pipeline schemas, source evidence, packet index, payload hashes/pointers, run receipts | `jt-ops` | Owner |
| n8n implementation lessons | `/Users/jtsomwaru/projects/n8n-agent/tasks/lessons.md` | Read by hash/reference; never copied as a second editable file |
| Prospect/client relationship state | Existing consulting files and Mission Control | Read-only adapter; no client private data copied |
| Job discovery and application state | `/Users/jtsomwaru/projects/job-market-agent` | Read status and package links |
| Resume and cover-letter finals | Google Drive Job Applications | Store links and validation receipt only |
| Product truth | Each app repository | Read verified app profile and source commit |
| Voice and public proof policy | OpenClaw content memory/skills | Read canonical version/hash |
| Human task and approval decisions | Mission Control/Convex | Owner; expose immutable decision ID/time/hash to `jt-ops` |
| External action and outcome state | Owning domain system: sequencer, X, job tracker, or app analytics | Owner; expose immutable status/result pointer to `jt-ops` |
| Long-term decisions and preferences | OpenClaw memory | Not duplicated into operational rows |
| Content calendar | Notion | Receive validated approved drafts only |

### 2.3 OpenClaw/Eve role

OpenClaw remains the orchestrator, but not an unchecked mega-agent.

It may:

- trigger approved workers and read their receipts;
- route complete packets into Mission Control and Telegram;
- write human decisions through the Mission Control adapter and retain pointers only;
- enforce policy and approval boundaries;
- assign a fresh verifier;
- reconcile confirmed external outcomes through the owning domain adapter and retain pointers only.

It may not:

- claim a worker succeeded without reading an artifact or receipt;
- be both builder and final verifier;
- silently send, post, apply, RSVP, purchase, or deploy;
- overwrite domain-owned facts with memory guesses;
- turn Telegram delivery into proof of task completion.

`jt-ops` never becomes a second approval database or CRM. It stores the packet hash, Mission Control decision pointer, external-system outcome pointer, and immutable run evidence needed to reconstruct what happened.

## 3. Mission Control contract

### 3.1 Seven universal fields

Every human-facing card contains:

1. **Title:** a child can understand the action.
2. **Why:** one sentence explaining the outcome.
3. **Exact steps:** one action per numbered step.
4. **Paste-ready prompt:** included only when needed.
5. **Where:** the exact app, URL, document, or interface.
6. **Done condition:** observable evidence, not “reviewed.”
7. **Feedback box:** JT's edit/reject reason and result.

Typed payloads hold lane-specific fields such as source URLs, expiry, buyer evidence, image asset, official job URL, approval hash, or send cohort. Irrelevant fields are omitted rather than filled with fake placeholders.

### 3.2 Required machine fields

- `card_id`
- `lane`
- `artifact_id`
- `artifact_url`
- `source_hashes[]`
- `expires_at`
- `approval_state`
- `payload_hash`
- `next_owner`
- `created_at`
- `completed_at`
- `outcome_ref`

Editing an external payload invalidates its approval.

### 3.3 Daily and weekly loop

**Daily, 30 to 45 minutes:**

1. Open Mission Control Today.
2. Process at most one outreach cohort card.
3. Process at most one personal-content card.
4. Process at most one job card.
5. Process an app card only if time remains after the first three priorities.
6. Reject incomplete packets back to their owner.
7. Stop at 45 minutes; automatically move overflow to the next eligible date.
8. Confirm external actions only after JT actually completes them.

**Friday, 30 minutes:**

1. Review sends, replies, meetings, priced conversations, cash, posts, qualified engagement, applications, and interviews.
2. Review JT edit/reject notes.
3. Approve or reject proposed prompt/skill patches.
4. Promote only changes with source examples and a regression test.
5. Pause lanes whose output is not being consumed.

## 4. Day 0: do not let architecture hide live decisions

### Task 0.1: Resolve the Altmark decision separately

**Owner:** JT. **No agent sends.**

- [ ] Check for any Yair/Adi response newer than the recorded 2026-08-24 update.
- [ ] If a newer response exists, update the client record and follow that reality.
- [ ] If no newer response exists, draft a current decision follow-up about ownership and the two planning questions from verified correspondence.
- [ ] Remove any deadline JT no longer intends to enforce.
- [ ] JT sends or explicitly declines to send it.
- [ ] Record the result separately from the operating-system build.

**Why:** Fable was right that a live commercial decision can outrank infrastructure. It was wrong to embed a potentially stale client message as an unconditional build step.

### Task 0.2: Allow manual work to lead the engine

- [ ] Select one publish-safe proof item for a manual LinkedIn post.
- [ ] Publish only if the post clears the existing content-worthiness and permission checks.
- [ ] Do not wait for the Content Engine.
- [ ] Start a newly requalified five-prospect cohort; do not use “the 57” as a blanket queue.
- [ ] Do not wait for the Research Engine to be productionized.

## 5. Phase 0: repair and narrow `jt-ops` (Days 1–3)

### Task 1: Snapshot current truth

**Files/Surfaces:** GitHub `jsomwarux/jt-ops`, current branches/PRs/issues, `pipelines.json`, `runs/`, `staging/raw-text.jsonl`, Mission Control, current automation inventory.

- [ ] Create a read-only inventory of active pipelines, schedule owner, last artifact, last successful end-to-end completion, current failure, next consumer, and real disable procedure.
- [ ] Record the current main SHA and open `claude/` branches.
- [ ] Record current queue sizes before any repair.
- [ ] Identify receipts and outputs stranded on unmerged branches.
- [ ] Identify every duplicate owner surface proposed by the old plan.
- [ ] Produce `reports/system-inventory-2026-09.md` in the implementation branch.

**Acceptance:** Every active pipeline has one named owner, real schedule, last complete output, and disable path; unknowns are labeled unknown.

**Current evidence to preserve, not hard-code into future logic:** on 2026-09-09, `main@2d1c95d` held 600 staged bodies and 653 schema-valid records; the staging-size guard and one deterministic extraction-flow test failed; `demand-ingest` and `demand-digest` were reported as `NEVER RAN` on `main`. Task 2 must use the count and hash captured by Task 1 at execution time.

### Task 2: Stop backlog growth safely

- [ ] Write a failing test proving a harvester cannot keep growing staging when ingestion has not consumed the prior threshold.
- [ ] Obtain approval to pause the real harvest schedule while the queue is repaired.
- [ ] Preserve a snapshot/hash of the staged bodies counted in Task 1.
- [ ] Do not delete staged evidence to make CI green.
- [ ] Add backpressure: when staging exceeds the approved threshold, harvesting writes a degraded receipt and skips new bodies.
- [ ] Run the test red, implement the guard, and run it green.

**Acceptance:** Queue growth stops without data loss; the real schedule state matches the registry.

### Task 3: Restore extraction and branch visibility

- [ ] Reproduce the current extraction-flow failure from a clean clone.
- [ ] Trace why `demand-ingest` is not draining staging.
- [ ] Fix the smallest root cause.
- [ ] Make every routine open or update a PR when it produces data.
- [ ] Make zero-result and failed runs create a durable issue/comment/receipt visible from `main`.
- [ ] Make verifiers test the PR head explicitly, not a scheduled clone of `main`.
- [ ] Reconcile pipeline names with receipt directory names.
- [ ] Add a test that fails when a registered pipeline writes under another name.
- [ ] Run one complete harvest → ingest → extract → validate → report cycle.

**Acceptance:** Main CI is green, staging falls below threshold, one end-to-end cycle is visible, and `check_pipelines.py` reports reality.

### Task 4: Extend contracts only where missing

Reuse existing schemas and utilities. Add only missing contracts for:

- prospect qualification;
- workflow blueprint;
- content candidate;
- media brief;
- job package reference;
- approval payload hash;
- external outcome.

- [ ] Write failing contract tests before each schema addition.
- [ ] Reference existing source/proof/run schemas rather than cloning them.
- [ ] Reject client names/private data in public or prospect-facing artifacts.
- [ ] Preserve `verified`, `inferred`, and `unknown` labels.
- [ ] Add no passive-income, generic knowledge-ingestion, or automatic prompt-mutation schema.

**Phase 0 gate:** No new scheduled lane until main CI stays green for 24 hours and one full existing pipeline cycle completes.

### Task 4.1: Exact shared contracts

Builders must not invent these boundaries. Reuse the existing `jt-ops` source, proof, outcome, approval-adjacent, and run-receipt fields when equivalent; add the following files only after a field-by-field diff.

| Contract / registry name | Path | Required core fields | Writer | Consumer |
|---|---|---|---|---|
| `prospect-candidate` | `schemas/prospect-candidate.schema.json`; records `data/prospects/YYYY-MM.jsonl` | `prospect_id`, organization, niche, buyer, title, channel state/evidence, source IDs, visible signals, inferred pains/confidence, proof refs, suppression state, qualification reasons, `verified_at` | Prospect qualifier | Recipe generator, packet renderer |
| `workflow-blueprint` | `schemas/workflow-blueprint.schema.json`; records `data/blueprints/YYYY-MM.jsonl` | `blueprint_id`, prospect/niche ref, trigger, inputs, deterministic steps, justified LLM steps, systems, approvals, exceptions, actions, evidence, recovery, assumptions, proof refs | Recipe generator | Packet renderer, n8n builder |
| `content-candidate` | `schemas/content-candidate.schema.json`; records `data/content/candidates/YYYY-MM.jsonl` | `candidate_id`, lane, source IDs, angle, audience, proof refs, draft, duplicate result, voice/fact results, media ref, approval pointer, outcome pointer | Content worker | Content verifier, packet renderer |
| `media-brief` | `schemas/media-brief.schema.json`; records `data/content/media/YYYY-MM.jsonl` | `media_id`, candidate ID, visual type, source refs, ratio, objective, hierarchy, permitted text, prohibited elements, privacy/copyright checks, asset path | Media selector | Claude Design/manual creator, verifier |
| `job-package-ref` | `schemas/job-package-ref.schema.json`; records `data/jobs/packages/YYYY-MM.jsonl` | `job_id`, official URL, verification time/result, score/evidence, Drive links, validator results, Mission Control pointer, application outcome pointer | Job-market adapter | Mission Control packet renderer |
| `approval-ref` | `schemas/approval-ref.schema.json`; records `data/approvals/YYYY-MM.jsonl` | `artifact_id`, action type, payload hash, Mission Control decision ID, decision, decided time, expiry | Mission Control adapter | External adapter gate |
| `external-outcome-ref` | `schemas/external-outcome-ref.schema.json`; records `data/outcomes/YYYY-MM.jsonl` | `artifact_id`, owning system, external record ID/URL, status, observed time, metrics, source pointer | Domain adapter after confirmed action | Scoreboards and learning evaluator |

Registry names are exact: `prospect-qualify`, `recipe-generate`, `packet-render`, `content-select`, `content-draft-linkedin`, `content-draft-x`, `content-media`, `job-package-index`, `mission-control-sync`, and `outcome-sync`. Every pipeline writes receipts under its exact registry name.

Adapter direction is one-way per fact: domain owner → `jt-ops` pointer/index → Mission Control card. Mission Control decision → `jt-ops` approval reference → domain adapter. No reverse write may overwrite the owner's underlying fact.

### Task 4.2: Mission Control compatibility and staged migration

- [ ] Inspect the current Convex task schema, API routes, task creation helpers, and work views.
- [ ] Map every universal and machine card field to an existing field or one typed payload object.
- [ ] Prefer a typed payload over adding top-level columns for lane-specific data.
- [ ] Document the mapping in `jt-ops/docs/mission-control-adapter.md`.
- [ ] Write contract tests for create, readback, update, payload-hash invalidation, dedupe/idempotency, completion, and outcome-pointer behavior.
- [ ] Stage any required Mission Control schema/API migration in a separate branch and review artifact.
- [ ] Do not mutate the production Convex schema during the first implementation checkpoint.
- [ ] Obtain explicit approval before deploying any Mission Control migration.

**Acceptance:** One synthetic card for each lane round-trips without duplicate task state, edits invalidate approval, and completion stores a pointer to the domain-owned outcome rather than copying the outcome into a second owner.

## 6. Parallel Track A: manual consulting motion (Days 1–10)

### Task 5: Requalify the prospect universe

The current outreach preflight scans 58 folders: 57 are skipped and one is warm-up-only. Build a new decision table rather than treating those folders as fresh leads.

- [ ] Classify each record as prior-pitched, prior-sent, active sequence, reactivation-eligible, suppression-blocked, research-only, or new.
- [ ] Verify a named buyer from a primary/public authoritative source.
- [ ] Verify a reachable email or accepted LinkedIn connection.
- [ ] Verify the channel again within seven days of send.
- [ ] Record a current visible workflow signal or a strong reusable niche trigger.
- [ ] Match only permission-safe proof or label the workflow as a hypothesis.
- [ ] Exclude duplicate companies, prior sequences, and conflicts.
- [ ] Select five prospects that pass every gate.

**Acceptance:** Five candidates have a named buyer, current reachable channel, evidence, proof/hypothesis boundary, and no suppression conflict.

### Task 6: Produce cohort one manually

Each packet contains:

1. company, buyer, title, and why this buyer;
2. visible signal with URL/date;
3. inferred pain with confidence;
4. five-to-eight-step AI recipe;
5. systems/tools named only when supportable;
6. human approvals, exception path, and audit evidence;
7. one permission-safe proof point;
8. M1, M2, and final follow-up;
9. unknowns and disqualifiers;
10. verification receipt.

- [ ] Use the n8n `lessons.md` file directly as canonical implementation evidence.
- [ ] Draft M1 at 80–130 words with one fact, one workflow hypothesis, one proof point, and one reply-sized ask.
- [ ] Include no attachment or meeting link in M1.
- [ ] Label inferred workflow pain as a question/hypothesis.
- [ ] Run an independent source/copy verifier.
- [ ] Put one cohort card in Mission Control.
- [ ] JT reviews and sends each message manually.
- [ ] Record send confirmation and outcome.

**Acceptance:** Five messages sent by JT, zero false facts, zero permission leaks, and median review time under three minutes per packet.

### Task 7: Produce cohort two

- [ ] Review cohort-one edit notes and replies.
- [ ] Patch only structural defects with regression tests.
- [ ] Requalify ten additional prospects.
- [ ] Generate and verify ten packets.
- [ ] JT sends the approved messages.
- [ ] Record delivery, bounce, reply, positive reply, buyer-confirmed pain, priced conversation, and opt-out.

**Scale evidence:** The first 15 messages validate process and copy quality. Do not infer stable conversion rates from 15 observations.

## 7. Parallel Track B: outbound infrastructure readiness

This track may run beside the manual cohorts because warmup is slow. It requires separate explicit approval for spend and account changes.

### Task 8: Approve the pilot infrastructure decision

- [ ] Confirm five source-verified cohort-one packets have clean copy/verifier receipts; this is a hard prerequisite.
- [ ] Confirm no suitable dedicated outreach domains/inboxes already exist.
- [ ] Compare Instantly and Smartlead using current official pricing and required features.
- [ ] Define an approved monthly ceiling before purchase.
- [ ] Choose one sequencer, not both.
- [ ] Choose two clearly related but non-deceptive sending domains.
- [ ] Choose four mailboxes total.
- [ ] Record the physical mailing address and unsubscribe process required for commercial email.
- [ ] Define who monitors replies, bounces, abuse reports, and suppression.
- [ ] JT explicitly approves the exact purchase and configuration.

**Infrastructure-readiness gate:** Tasks 8 and 9 are a separately approved external setup track. They may begin after five packets pass QA even if reply data is not yet available. This is the only approved exception to the general recurring-lane activation gate. It authorizes mailbox warmup only, not cold campaigns. Campaign activation remains blocked by Task 10 and Section 18.

### Task 9: Configure and warm safely

- [ ] Purchase the approved domains.
- [ ] Create the approved mailboxes.
- [ ] Configure SPF, DKIM, DMARC, TLS, tracking-domain policy, and forwarding.
- [ ] Add the domains to Postmaster Tools where applicable.
- [ ] Connect the mailboxes to the chosen sequencer.
- [ ] Enable warmup using the selected provider's current documented guidance.
- [ ] Send no cold campaign until authentication and inbox placement checks pass.
- [ ] Keep JT's primary business domain out of cold-volume campaigns.

Google recommends gradual volume increases, authenticating mail, monitoring reputation, keeping reported spam below 0.1%, and preventing it from reaching 0.3% or higher. Recheck the [current Gmail sender guidelines](https://support.google.com/mail/answer/81126) at activation.

### Task 10: Earn scaled sending

The four-inbox pilot does not authorize an eight-to-twelve-inbox fleet.

- [ ] Wait until mailbox warmup and authentication gates pass.
- [ ] Require at least 50 delivered niche-consistent messages before a fleet decision.
- [ ] Hard bounce rate must remain at or below 2%.
- [ ] Spam complaints must stay below 0.1% and never reach 0.3%.
- [ ] Stop immediately on a suppression or unsubscribe failure.
- [ ] Require at least one positive reply or buyer-confirmed pain before increasing volume.
- [ ] If 50 delivered messages produce neither, revise targeting/copy and do not scale.
- [ ] JT explicitly approves each campaign and presses send/activate.

### 7.1 Credential controls for every integration

- [ ] Provision credentials only through masked host-owned or platform credential entry.
- [ ] Never request or paste secrets in Telegram, chat, transcripts, source files, commands, command-line arguments, URLs, logs, or plaintext environment output.
- [ ] Store OAuth tokens in n8n's credential store or the approved protected shared store.
- [ ] Use least-privilege scopes: read-only during research pilots; add write scopes only after separate approval.
- [ ] Allowlist only the exact egress hosts required by the integration.
- [ ] Record credential name/reference, owner, scopes, allowed hosts, created date, and revocation procedure without recording the secret.
- [ ] Rotate/revoke a credential immediately after any suspected exposure.
- [ ] Provide no plaintext fallback when protected injection is unavailable.

## 8. Phase 1: Research and Match Engine (Weeks 1–3)

### Task 11: Build the prospect contracts in `jt-ops` and execution in n8n

**Execution:** n8n handles deterministic collection and routing; GitHub Actions handles unrestricted public fetching where useful; a bounded model worker handles hypotheses and recipes.

**Source/runtime ownership:**

- Blueprint and handoff specification: `/Users/jtsomwaru/projects/n8n-agent/tasks/workflow-growth-prospect-blueprint.md`.
- Versioned workflow JSON and node code: `/Users/jtsomwaru/projects/n8n-agent/workflows/workflow-growth-prospect-research.json` plus focused scripts/tests beside it.
- Canonical implementation lessons: `/Users/jtsomwaru/projects/n8n-agent/tasks/lessons.md`.
- Deployed workflow ID, execution cursor, retry state, and runtime execution history: the deployed n8n instance.
- Input evidence, normalized prospect/blueprint records, packet contracts, payload hashes, and immutable receipt/outcome pointers: `jt-ops`.

**Adapter direction:** `jt-ops` creates a qualified research request and calls an authenticated n8n webhook with only the request ID and source pointers. n8n reads permitted inputs, executes collection/routing, and posts a result manifest plus runtime execution ID to a `jt-ops` intake endpoint or approved GitHub branch/PR. `jt-ops` validates the returned records and writes the durable `prospect-qualify`/`packet-render` receipts. n8n owns its runtime receipt; `jt-ops` stores only its immutable ID/status pointer. Neither system rewrites the other's receipt.

- [ ] Create the node-by-node n8n blueprint before building nodes.
- [ ] Read `/Users/jtsomwaru/projects/n8n-agent/tasks/lessons.md` in full.
- [ ] Add primary-source collection, dedupe, freshness, retry, and source hashing.
- [ ] Add buyer and channel gates before model calls.
- [ ] Add visible signal and suppression gates.
- [ ] Generate an AI recipe only for qualified candidates.
- [ ] Justify every LLM node; reject unnecessary model use.
- [ ] Add human approval, exception queue, final action boundary, audit trail, and recovery path to every recipe.
- [ ] Create a complete Mission Control packet.
- [ ] Keep sending outside this lane.

### Task 12: Tier research by value

- **Tier A:** highest-value accounts receive deep primary-source/browser research and a custom recipe.
- **Tier B:** verified structured personalization from a small set of evidence fields and one approved framework.
- **Research-only:** no buyer/channel or insufficient evidence; never send-ready.

- [ ] Do not use Grok Bot for Tier B volume.
- [ ] Run one Grok Bot browser-research spike on five Tier A accounts only if public APIs/web research leaves material gaps.
- [ ] Compare fact accuracy, source completeness, runtime, cost, and JT review time against the standard method.
- [ ] Keep Bot only if it wins materially.

### Task 13: Choose the next niche

Start with property/supportive housing where proof and buyer access are strongest. Insurance is the first adjacent candidate because JT has paid implementation proof.

- [ ] Score niche candidates on manual-work density, accessible buyer, reachable channels, proof adjacency, average value, privacy/regulatory burden, and visible triggers.
- [ ] Test one adjacent niche at a time.
- [ ] Do not enter healthcare workflows without a separate privacy/compliance design.
- [ ] Unlock the next niche only after either one priced conversation or at least 50 delivered messages plus two independent buyer-confirmed pain signals in the current niche.

## 9. Phase 2: Content Engine (Weeks 2–4)

Manual posts may begin before the engine. The engine is judged by better consistency and lower review time, not by being the prerequisite to publish.

### Task 14: Canonical voice and adapter design

- [ ] Keep one canonical JT voice source.
- [ ] Keep one canonical positioning source: controlled automated workflows around messy operational handoffs.
- [ ] Keep `n8n-agent/tasks/lessons.md` canonical.
- [ ] Generate thin read-only adapters for GPT, Grok, OpenClaw, and coding workers.
- [ ] Record source path, version, and hash in every run.
- [ ] Never paste separate editable copies into each platform.

### Task 15: Personal LinkedIn lane

Use a weekly target, not a forced quota:

- one workflow/project post;
- one company/niche teardown;
- one AI-news take supplied or approved by JT.

If only two are strong, publish two.

- [ ] Select source evidence using this order: shipped result, non-obvious n8n lesson, public-evidence teardown, market finding, primary-source AI news, public X context.
- [ ] Label company-specific teardowns as hypotheses from public evidence.
- [ ] Prefer category-level teardowns when company evidence is thin.
- [ ] Draft with GPT and generate a Grok challenger on frozen briefs during the test period.
- [ ] Blind the model identity.
- [ ] Track JT preference, edit distance, factual defects, and publish decision by format.
- [ ] Route future formats to the measured winner.
- [ ] Produce one recommended draft and at most one materially different alternate hook.

### Task 16: X voice lab and daily candidates

- [ ] Collect 30 admired X posts and at least 20 JT-authored examples.
- [ ] Label JT examples keep/mixed/reject with reasons.
- [ ] Use the Grok app for one-time interactive voice analysis.
- [ ] Separate JT's demonstrated voice from admired external techniques.
- [ ] Require two examples for every voice rule.
- [ ] Save one canonical X voice specification.
- [ ] Test X API OAuth read-only access to JT's likes/bookmarks using `tweet.read`, `users.read`, `like.read`, `bookmark.read`, and `offline.access` as currently documented.
- [ ] If OAuth is not approved or available, use JT-forwarded posts and public sources.
- [ ] Let n8n own cursor, dedupe, hashes, and source state.
- [ ] Let Grok/xAI analyze the evidence and return zero to three candidates.
- [ ] Make `skip_today` a valid successful output.
- [ ] Keep publishing manual during the pilot.

Verified product setup detail lives in `deliverables/xai-x-content-system-guide-2026-09-09.md` and should be rechecked against current [X OAuth documentation](https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code) at implementation.

### Task 17: One-image system

- [ ] Workflow post: use a redacted, legible, annotated n8n canvas screenshot.
- [ ] Measured build: use a redacted output or before/after artifact.
- [ ] AI news: use a source-visible screenshot only when context, copyright, and readability are appropriate.
- [ ] Teardown/research: create one original editorial visual or systems diagram.
- [ ] Generate a Claude Design prompt only when a screenshot/artifact is not stronger.
- [ ] Require objective, audience, 1:1 or 4:5 ratio, hierarchy, permitted text, color direction, sources, and prohibited elements.
- [ ] Reject carousels and tiny-text diagrams.
- [ ] Add alt text to every packet.

### Task 18: Content packet and feedback

Each packet includes final copy, source links, recommended posting window, one visual or image prompt, alt text, duplicate report, voice/fact checks, and approval hash.

- [ ] Push validated approved items to the existing Notion Content Calendar.
- [ ] Never auto-post in the pilot.
- [ ] Capture JT edits as raw feedback.
- [ ] Record the published URL and performance outcome.
- [ ] Let the weekly evaluator propose a patch; never write raw feedback directly into the canonical skill.

## 10. Phase 3: harden the existing Job Hedge (Weeks 3–4)

Do not rebuild the job system or impose a daily package quota.

### Task 19: Discovery and official verification

- [ ] Preserve the existing duty-first search and 25-point rubric.
- [ ] Search NYC/remote roles at JT's compensation floor.
- [ ] Verify the role on an employer or authoritative ATS source before scoring.
- [ ] Reject aggregator-only listings contradicted by official truth.
- [ ] Test HTTP 200 pages with expired/removed banners.
- [ ] Deduplicate applied, rejected, expired, and previously surfaced roles.

### Task 20: Package only competitive roles

- [ ] Generate a package only after the role clears the evidence gate.
- [ ] Use GPT-5.6 Sol for resume and cover letter.
- [ ] Enforce AgentGuard exclusion from Key Projects.
- [ ] Enforce formal correspondence, direct confidence, positive framing, and JT's preferred warm close.
- [ ] Run ATS mapping, JD mapping, evidence, privacy, parsing, DOCX, and live Drive-readback checks.
- [ ] Create one Mission Control card with official role and document links.
- [ ] Never submit the application.

**Daily output:** zero to three verified roles; packages only for qualifying roles. A clean no-role result is success.

## 11. Phase 4: app marketing (Weeks 4–7)

Use one content chassis with separate verified product profiles.

### Task 21: Verify activation order

- [ ] Verify each app's current repository, live surface, conversion action, and product truth.
- [ ] Activate Yardstick first only if it is live and can convert current fantasy-football attention.
- [ ] Keep Action Arena off until the rebuild has a real destination.
- [ ] Keep Nash Satoshi off until a live surface or approved conversion action exists.
- [ ] Recheck this order at implementation; seasonality is not enough without a working destination.

### Task 22: Build app profiles

Each profile contains product truth, release state, audience, job-to-be-done, value proposition, approved/prohibited claims, proof/screenshots, category language, content pillars, conversion action, visual rules, and measurable product events.

- [ ] Read each repository and project `CLAUDE.md`/lessons before drafting.
- [ ] Separate shipped capabilities from planned features.
- [ ] Give each app a niche-native voice addendum.
- [ ] Keep consulting and crypto/game brands separate.
- [ ] Produce zero content when nothing real shipped, ranked, changed, or can convert.

### Task 23: Reuse the Content Engine

- [ ] Load one verified app profile per run.
- [ ] Reuse provenance, candidate, image, approval, and outcome contracts.
- [ ] Produce one recommended post, one visual, and optional reply target.
- [ ] Keep JT review under five minutes.
- [ ] Never auto-post.

## 12. Optional lanes

### 12.1 Events

Once per month, return no more than five NYC events over the next 30 days with relevance, likely audience, exact RSVP link/deadline, and one natural opener. JT decides and RSVPs. No recurring agent is needed unless this manual query repeatedly misses opportunities.

### 12.2 Passive-income discovery

Park until the shared system contains enough proprietary pain, recipes, outcomes, and distribution data. Re-entry requires:

- uses JT's real edge;
- ugly but functional v0 within three days;
- distribution path JT already owns;
- not a generic AI-wrapper/newsletter/dropshipping/print-on-demand idea;
- one small revenue or waitlist test;
- kill on failed demand signal.

## 13. Tool routing

| Tool | Use | Boundary |
|---|---|---|
| n8n + canonical lessons | Deterministic workflows, API calls, retries, queues, packet assembly | Not final judgment or voice |
| GitHub Actions | Public fetching and deterministic CI | Not buyer-facing writing |
| OpenClaw/Eve | Orchestration, memory, approval routing, Telegram, verification routing | Not sole run truth or self-grader |
| Mission Control | Today queue, approval decisions, feedback, outcome review/pointers | Not raw corpora, private client documents, or authoritative external outcomes |
| GPT-5.6 Sol | LinkedIn, job documents, voice-sensitive copy | Not bulk fetching |
| Grok app | Interactive X voice lab | Not workflow state |
| Grok/xAI API | Structured X analysis and candidate drafting | Not private X access without OAuth |
| Grok Automations | Optional public-X/news scout | Not durable cursor or private bookmark collector |
| Grok Bot | Optional bounded browser research | Not posting, sending, purchasing, or system of record |
| Codex/Claude Code/Grok Build | Build and repair code/workflows | Selected by test evidence, not reputation |
| Google Drive | Final human-readable documents | Not operational state |
| Notion | Content calendar/swipe file | Not Mission Control |
| Apollo | Initial contact discovery/enrichment if needed | Verify key facts from primary sources |
| Clay | Add only after a measured enrichment/orchestration gap | Not required in v1 |
| Instantly or Smartlead | Approved volume delivery after warmup | Never research/qualification owner |

## 14. Program schedule

### Days 0–3

- Resolve the current Altmark decision or explicitly defer it.
- Snapshot and repair `jt-ops` backlog/visibility.
- Requalify prospects and create five manual packets.
- Draft one manual LinkedIn post from publish-safe proof.
- Decide whether to approve two-domain/four-inbox readiness in parallel.

### Days 4–10

- JT sends cohort one.
- Complete one green `jt-ops` end-to-end cycle.
- Build only the missing prospect contracts and n8n blueprint.
- Begin approved mailbox warmup if selected.

### Week 2

- Produce and send cohort two of ten.
- Build the prospect lane around the proven manual packet.
- Start the LinkedIn lane from real prospect/build artifacts.

### Week 3

- Review the first 15 outcomes.
- Continue to 50 delivered messages only if source/copy quality is clean.
- Harden Job Hedge official verification and package generation.
- Run the LinkedIn writer blind test.

### Week 4

- Run the X voice lab and private-X OAuth feasibility proof.
- Complete three manual X workflow runs.
- Keep posting manual.

### Weeks 5–6

- Evaluate 50-message scale gate.
- Activate no more than the approved four-inbox pilot if gates pass.
- Verify Yardstick and build its app profile if live.
- Add Grok Bot only if the bounded research spike wins.

### Weeks 7–8

- Add the next proven niche or hold.
- Add Action Arena or Nash only when each has a live conversion surface.
- Review cost, review time, buyer outcomes, content outcomes, and system health.
- Pause unconsumed lanes.

### 14.1 Cost worksheet required before activation

Complete this worksheet with current official prices at the approval date. `TBD` blocks activation; it is not permission to assume zero.

| Lane/item | Fixed monthly | Usage cap | Per-artifact target | Approval owner |
|---|---:|---:|---:|---|
| X API read-only likes/bookmarks | Verify current pay-per-use | $5 pilot cap | Record per processed source | JT |
| xAI API drafting/analysis | Verify current model price | $10 pilot cap | Record per valid X packet | JT |
| GPT drafting/evaluation | Existing plan or measured usage | Set lane cap | Record per approved content/job packet | JT |
| Grok Bot | Verify entitlement/current price | No purchase in core plan | Compare per verified Tier A packet | JT |
| Apollo | Verify current plan | No purchase until coverage gap is shown | Record per verified buyer/channel | JT |
| Clay | Deferred | $0 until measured enrichment gap | N/A | JT |
| Two domains | Obtain registrar quote | One-time approved amount | N/A | JT |
| Four mailboxes | Obtain provider quote | Approved monthly ceiling | Record per active inbox | JT |
| Instantly or Smartlead | Compare current official pricing | Approved monthly ceiling | Record per delivered message/reply | JT |
| Claude/Codex/Grok Build | Existing plan or measured usage | Set implementation cap | Record per accepted task | JT |

The verified X-content guide estimated $2–$15 incremental monthly for the read-only X/xAI pilot as of 2026-09-09, but implementation must refresh the price. No optional paid tool enters the core stack merely because it appears in this table.

## 15. Scoreboards and gates

### Consulting

- qualified prospects;
- verified send-ready packets;
- median JT edit/review time;
- delivered messages;
- hard bounce and spam-complaint rates;
- replies and positive replies;
- buyer-confirmed pain;
- priced conversations;
- projects won and cash collected.

### Content

- approved/published posts;
- JT edit time;
- qualified profile visits;
- relevant inbound conversations;
- saves/replies from target buyers or employers;
- source, privacy, and duplication failures.

### Jobs

- verified live roles;
- competitive packages;
- JT-submitted applications;
- recruiter screens, interviews, offers;
- stale-role and inflation failures.

### Apps

- approved/published posts;
- clicks/store visits;
- signups and activation events;
- retention-relevant events;
- truth or brand failures.

### System health

Track these separately:

1. worker executed;
2. artifact valid;
3. packet delivered;
4. human decision recorded;
5. external action confirmed;
6. commercial/audience outcome observed.

## 16. Kill and pause rules

Pause a lane immediately for:

- unapproved external action;
- fabricated source, buyer, quote, metric, workflow, or product claim;
- privacy, permission, or credential incident;
- source freshness failure;
- unsubscribe/suppression failure;
- the real schedule running while its registry says paused.

Pause and review after two cycles for:

- no human consumption;
- review time above the cap;
- rising cost without better outcomes;
- growing volume with declining quality;
- repeated delivery failure;
- zero positive reply or buyer-confirmed pain after 50 delivered niche-consistent messages.

Preserve artifacts and receipts. Disable the real schedule through its owning platform only after the required approval. Never delete history to make a dashboard look healthy.

## 17. First implementation checkpoint

The first implementation session may:

1. inventory `jt-ops` and its live schedules;
2. create a safe branch/worktree;
3. write failing backlog, branch-visibility, and receipt-name tests;
4. repair current CI and restore one full existing pipeline cycle;
5. requalify five prospects and produce manual review packets;
6. create a review artifact with evidence.

It may not:

- purchase domains, inboxes, or subscriptions;
- change DNS or activate warmup;
- send an email or client message;
- post content;
- submit a job application;
- activate or edit schedules;
- deploy production n8n workflows;
- connect private X data;
- alter production Mission Control schema;
- archive tasks in bulk.

## 18. Final acceptance gate before any recurring activation

- [ ] `jt-ops` main CI is green from a fresh clone.
- [ ] One existing end-to-end pipeline cycle is complete and visible.
- [ ] Every lane reads one canonical owner per fact.
- [ ] Every generated claim has provenance.
- [ ] Every external adapter enforces exact-payload approval.
- [ ] Every recurring job has a real disable owner and procedure.
- [ ] Mission Control and Telegram delivery are proven separately from generation.
- [ ] Manual pilot outputs meet the quality/review-time target.
- [ ] Cost ceilings are approved.
- [ ] JT explicitly approves the exact lane, schedule, and external permissions.

The separately approved mailbox-warmup exception in Task 8 may run before these lane gates only after five packets pass QA. It cannot send cold campaigns, expand the fleet, or grant any model write access.

## 19. Immediate recommendation

Approve one bounded checkpoint, not the entire eight-week program:

1. resolve or consciously defer the current Altmark/Yair decision;
2. repair `jt-ops` staging, ingestion, CI, branch visibility, and receipt naming;
3. requalify five prospects and produce five manual send-ready packets;
4. prepare one proof-led LinkedIn post;
5. return a decision packet for the two-domain/four-inbox pilot, with current price, compliance, and ownership details.

This sequence preserves Fable's strongest insight, manual buyer motion now, without accepting its false premise that the old 57 are fresh or its attempt to demote the existing control plane. It preserves Grok's strongest insight, bounded specialists producing complete packets, without adopting a duplicate Notion board. It preserves the original plan's strongest insight, provenance, approvals, verification, and kill rules, without rebuilding the spine next door.
