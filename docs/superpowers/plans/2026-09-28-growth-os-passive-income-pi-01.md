# Growth OS Passive Income Lane — PI-01 End-to-End Implementation Plan

> **Execution rule:** Work through the gates in order. A later phase is not authorized by completion of an earlier phase. External messages, Mission Control writes, checkout/store changes, deployments, schedules, provider calls, credentials, and publication each retain their existing approval boundaries.

**Goal:** Add one governed Passive Income lane to Growth OS and validate the Production-Grade n8n Reliability Kit as its first stream, optimizing net profit per hour of JT attention.

**Architecture:** A local Passive Income domain owner stores stream state and append-only events. Deterministic Governor and Revenue Controller code evaluates lifecycle gates, economics, and WIP. Thin n8n workflows orchestrate those components only after validation. Mission Control remains the single cross-lane human decision queue and receives only bounded exceptions.

**Canonical design:** `docs/superpowers/specs/2026-09-28-growth-os-passive-income-lane-design.md`

---

## Current checkpoint

Completed locally:

- PI-01 created in `validating`.
- Buyer, painful moment, promise, product boundary, validation deadline, and kill gates recorded.
- Twelve-module kit outline derived from the existing n8n lessons corpus.
- Validation scorecard and ten unsent research-message drafts created.
- One bundled JT decision card, a bootstrap-only generic packet fixture, and a specialized live decision-form fixture staged locally; none is admitted to Mission Control.
- n8n control-plane blueprint written; build/deploy/recurrence remain blocked.

Current human gate:

1. Price anchor: recommend **$149 one-time** for the validation probe.
2. Package: recommend **Core Kit only** for V1; membership is offered only after a buyer wants ongoing compatibility coverage.
3. Implementation upsell: recommend **allowed as active consulting, excluded from Passive Income performance**.
4. Passivity threshold: recommend **median support <=30 minutes per sale during the first ten deliveries**.

---

## Phase 1 — Freeze the PI domain contract

### Step 1.1: Add schemas and transition table

Create:

- `scripts/passive_income/storage.py`
- `scripts/passive_income/domain.py`
- `scripts/passive_income/schemas.py`
- `scripts/tests/test_passive_income_domain.py`
- `memory/passive-income/streams/pi-01-reliability-kit/events.v1.jsonl`
- `memory/passive-income/streams/pi-01-reliability-kit/receipts/`

Implement test-first:

- canonical stream/event/receipt parsing;
- legal lifecycle transitions;
- exact event hashing;
- identical replay as no-op;
- conflicting replay refusal;
- SQLite WAL storage with `BEGIN IMMEDIATE`, foreign keys, and unique event/idempotency constraints;
- event and projection commit in one transaction;
- deterministic JSON/JSONL export with revision, cursor, hashes, and receipt;
- genesis import of the current pre-ledger seed;
- crash rollback, `PRAGMA integrity_check`, replay verification, and guarded projection rebuild;
- zero/unknown numeric semantics;
- `kill` terminal behavior;
- pause/resume with a new evidence-bound decision.

Verification:

```bash
python3 -m unittest scripts.tests.test_passive_income_domain -v
python3 -m compileall scripts/passive_income scripts/tests/test_passive_income_domain.py
git diff --check -- scripts/passive_income scripts/tests/test_passive_income_domain.py memory/passive-income/streams/pi-01-reliability-kit
```

Gate: fresh independent review of the immutable local commit. No Mission Control or n8n changes.

### Step 1.2: Add telemetry ingestion

Create:

- `scripts/passive_income/telemetry.py`
- `scripts/tests/test_passive_income_telemetry.py`
- `memory/passive-income/streams/pi-01-reliability-kit/prospects.v1.jsonl`
- `memory/passive-income/streams/pi-01-reliability-kit/evidence/`

Accepted validation events:

- buyer conversation;
- price-bound intent commit;
- presale/design partner;
- repeated market evidence.

Later accepted commerce events:

- payment, delivery, refund, fee, infrastructure cost, affiliate reversal, support time, and JT time.

Tests must prove duplicate suppression, evidence requirements, stale/invalid refusal, and no false advancement from nonresponses, likes, or generic trend evidence.

Verification:

```bash
python3 -m unittest scripts.tests.test_passive_income_telemetry -v
python3 -m compileall scripts/passive_income/telemetry.py scripts/tests/test_passive_income_telemetry.py
git diff --check -- scripts/passive_income/telemetry.py scripts/tests/test_passive_income_telemetry.py
```

### Step 1.3: Implement Governor and scorecard CLI

Create:

- `scripts/passive_income/governor.py`
- `scripts/passive_income/cli.py`
- `scripts/passive_income/schemas/*.json`
- `scripts/tests/test_passive_income_governor.py`
- `scripts/tests/test_passive_income_cli.py`

Implement every input/output schema from `memory/app-discovery/pi-01-reliability-kit/data-contracts.md` as JSON Schema with `additionalProperties: false`.

CLI contract:

```bash
python3 -m scripts.passive_income.cli init-stream --seed memory/passive-income/streams/pi-01-reliability-kit/stream.v1.json
python3 -m scripts.passive_income.cli record-decision --input /absolute/path/decision.json
python3 -m scripts.passive_income.cli record-prospect --input /absolute/path/prospect.json
python3 -m scripts.passive_income.cli record-send --input /absolute/path/send.json
python3 -m scripts.passive_income.cli record-response --input /absolute/path/response.json
python3 -m scripts.passive_income.cli record-commerce-event --input /absolute/path/commerce-event.json
python3 -m scripts.passive_income.cli evaluate --stream PI-01 --as-of 2026-09-29T00:00:00-04:00
python3 -m scripts.passive_income.cli run-governor --request /absolute/path/run-request.json
python3 -m scripts.passive_income.cli run-revenue --request /absolute/path/run-request.json
python3 -m scripts.passive_income.cli record-admission --input /absolute/path/admission-result.json
python3 -m scripts.passive_income.cli ack-decision --input /absolute/path/decision-ack.json
python3 -m scripts.passive_income.cli finalize-run --input /absolute/path/finalize-run.json
python3 -m scripts.passive_income.cli verify-state
python3 -m scripts.passive_income.cli rebuild-projection --input /absolute/path/rebuild-projection.json
python3 -m scripts.passive_income.cli export --stream PI-01
python3 -m scripts.passive_income.cli replay-dead-letter --input /absolute/path/dead-letter-replay.json
```

Each command accepts exactly the arguments shown and returns `pi-command-result-v1`. Exit codes are 0 terminal success/no-action, 2 invalid input, 3 replay conflict, 4 systemic dependency failure, and 5 integrity failure. stdout is canonical JSON; stderr contains fixed diagnostics only.

Tests cover all lifecycle transitions, the two-of-four gate, the October 12 self-deadline, advisory `iterate` before the deadline, incomplete ranking inputs, stable candidate hashes, WIP snapshot staleness, and no automatic state transition.

Verification:

```bash
python3 -m unittest scripts.tests.test_passive_income_governor scripts.tests.test_passive_income_cli -v
python3 -m compileall scripts/passive_income scripts/tests/test_passive_income_governor.py scripts/tests/test_passive_income_cli.py
```

### Step 1.4: Implement Revenue Controller

Create:

- `scripts/passive_income/revenue.py`
- `scripts/tests/test_passive_income_revenue.py`

Implement USD-only cash/delivery recognition, unique-order refund rates, 30-day membership conversion, compensating corrections, cost attribution, overlap-safe time events, support minutes per sale, and raw plus floored net-profit-per-JT-hour outputs exactly as defined in the design.

Verification:

```bash
python3 -m unittest scripts.tests.test_passive_income_revenue -v
python3 -m compileall scripts/passive_income/revenue.py scripts/tests/test_passive_income_revenue.py
```

Gate: one immutable Phase 1 commit plus fresh independent verification. Phase 1 creates no external state.

---

## Phase 2 — Run the 14-day validation manually

### Step 2.1: Approve the one bundled decision

JT reviews `memory/app-discovery/pi-01-reliability-kit/jt-decision-card.md` and answers the four fields. Record the exact values through `record-decision`, binding the event to JT's Telegram message ID and the decision-artifact hash. This bootstrap event authorizes configuration only; it does not authorize a send, build, store, payment, or workflow.

### Step 2.2: Build the buyer list

Select 10–15 reachable n8n freelancers/agencies with one real signal each: published client work, reliability discussion, support complaint, maintenance offer, or production-focused content.

For each prospect record:

- person and role;
- organization;
- public source URL or existing relationship reference;
- exact signal;
- one channel;
- selected message version;
- status and evidence pointer.

No private scraping. No automated send. No same-day email plus LinkedIn.

Write each prospect through:

```bash
python3 -m scripts.passive_income.cli record-prospect --input /absolute/path/prospect.json
```

`prospects.v1.jsonl` is a deterministic export from the domain database, not a separately edited tracker.

### Step 2.3: Finalize and send research messages

Use the drafts in `buyer-validation-messages.md` only after replacing the first line with a specific signal. Each final message must be individually reviewed. JT presses send; the bundled configuration decision does not authorize any message.

After JT confirms a send, record it with `record-send`; record a reply with `record-response`. Preserve the buyer's exact failure language and a source pointer. These commands are PI-specific and do not call the consulting `outreach_update.py` path. Do not pitch the kit before learning the current recovery process.

### Step 2.4: Evaluate the gate daily

Run:

```bash
python3 -m scripts.passive_income.cli evaluate --stream PI-01 --as-of <ISO-8601>
```

It may report:

- `continue_validation`;
- `pilot_eligible`;
- `pause_due_to_deadline`;
- `invalid_evidence`.

It may not change state automatically. `iterate` is advisory and remains `validating` only before the current deadline. At two qualifying signals, stage one exact-payload-bound pilot decision. If the Passive Income Mission Control adapter is not yet deployed, JT's explicit Telegram decision is recorded as a bootstrap event bound to message ID and artifact hash, then imported as the outcome when the adapter is released. At fewer than two on 2026-10-12, stage one pause decision unless JT already approved a versioned deadline extension.

Gate: no product build, storefront, checkout, autonomous publishing, or Stream Owner Agent before `pilot_eligible` is approved.

---

## Phase 3 — Build the kit only after validation passes

### Step 3.1: Convert the module outline into acceptance tests

For every module in `module-list.md`, define:

- failure it prevents;
- input fixture;
- expected behavior;
- terminal receipt;
- replay procedure;
- rollback/dead-letter behavior;
- compatibility assumptions;
- buyer-facing documentation.

The kit is complete only when each promised failure mode has a runnable fixture and expected result.

### Step 3.2: Assemble V1

Recommended V1 structure:

```text
/Users/jtsomwaru/projects/n8n-reliability-kit/
  README.md
  LICENSE.md
  CHANGELOG.md
  compatibility.json
  pyproject.toml
  patterns/
  fixtures/
  contracts/
  monitors/
  playbooks/
  release-checklist/
  scripts/
    verify_manifest.py
    package_release.py
    scan_release.py
  tests/
    test_manifest.py
    test_package_release.py
    test_scan_release.py
  support-policy.md
  update-policy.md
```

Use sanitized examples only. Do not include client data, secrets, or opaque production exports.

Before implementation, capture the installed n8n version with `n8n --version` in the isolated builder environment and pin it in `compatibility.json`; do not infer the version from old exports. Each of the twelve modules receives one numbered pattern file, one fixture directory, one expected receipt, and one focused test. License choice is an explicit JT decision before packaging; until then `LICENSE.md` says `UNLICENSED - validation build`.

### Step 3.3: Product QA

Prove:

- every example imports against the supported n8n version;
- expected fixtures match runtime data shape;
- duplicate/retry/partial-failure tests pass;
- valid-empty executions reach the terminal receipt;
- auth/billing/quota failure does not advance state;
- rollback and dead-letter replay work;
- secret/PII scans are clean;
- documentation matches the files shipped.

Required commands in the kit repository:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m compileall patterns monitors tests
python3 scripts/verify_manifest.py --root . --compatibility compatibility.json
python3 scripts/scan_release.py --root . --reject-secrets --reject-pii --reject-client-identifiers
python3 scripts/package_release.py --dry-run --root .
git diff --check
```

`verify_manifest.py` proves every promised module has a file, fixture, expected receipt, documentation entry, and manifest hash. `package_release.py` writes a deterministic inventory and archive hash in dry-run and real modes. `scan_release.py` uses explicit credential-prefix, private-key, email/phone, and client-identifier fixtures; false positives are allowlisted by exact file/hash, never broad patterns.

Gate: fresh builder/verifier separation and immutable accepted bundle.

---

## Phase 4 — Configure checkout, delivery, and update channel

This phase requires separate approval because it affects external systems and money.

### Step 4.1: Choose the owned system of record

Required capabilities:

- customer export;
- payment/refund webhooks;
- versioned file delivery;
- tax/receipt handling appropriate to the platform;
- webhook signing;
- idempotent fulfillment;
- owned backup of product files and customer entitlements.

The storefront is a rented shelf. Product files, changelog, entitlement ledger, and customer export remain portable.

### Step 4.2: Configure products in order

1. One-time Core Kit at the approved price.
2. Update membership only after demand for updates is observed.
3. Disclosed referral links only for tools used in the kit.
4. Implementation upsell routed to Consulting and excluded from passive-income metrics.

### Step 4.3: Configure deterministic fulfillment

Payment webhook -> signature check -> canonical payment event -> idempotent entitlement -> delivery -> delivery evidence -> receipt.

Required exception:

- payment without delivery creates an urgent JT card;
- delivery without authorized payment stops and creates a reconciliation card;
- duplicate webhook produces zero new delivery writes.

Gate: controlled test transaction, refund-path proof, delivery replay proof, and explicit pilot authorization.

---

## Phase 5 — Integrate Mission Control

### Step 5.1: Build the Passive Income adapter

Map only eligible decisions into the accepted generic lane packet with `lane: passive-income`.

`portfolio_family` is internal taxonomy only and never passes as a Growth OS lane value. The adapter always maps PI-01 to `lane: passive-income`.

Modify test-first:

- `mission-control/lib/mission-control/lane-packet.ts`
- `mission-control/lib/mission-control/lane-packet-route.ts`
- `mission-control/lib/mission-control/lane-packet-transitions.ts`
- `mission-control/convex/tasks.ts`
- `mission-control/convex/schema.ts`
- `mission-control/app/api/tasks/passive-income-decision/route.ts`
- `mission-control/lib/mission-control/passive-income-decision.ts`
- `mission-control/lib/mission-control/passive-income-decision-route.ts`
- `mission-control/components/mission-control/PassiveIncomeDecisionForm.tsx`
- `mission-control/components/mission-control/InspectionDrawer.tsx`
- `mission-control/lib/mission-control/passive-income-decision-form.test.tsx`
- `mission-control/docs/mission-control-lane-packet-contract.md`
- focused tests beside each file;
- add `mission-control/lib/mission-control/passive-income-lane-adapter.ts` and `.test.ts`.

Eligible families:

- pilot/listing approval;
- rights/refund/fulfillment/support exception;
- price/spend/dependency change;
- scale/pause/kill.

Enforce:

- one unresolved card per stream;
- three unresolved Passive Income cards globally;
- expiry and exact-payload approval;
- identical replay creates zero writes;
- typed closure and outcome pointer;
- machine backlog never becomes cards.

`artifactRef.system` is `passive-income-domain`; `artifactRef.id` is the stream ID. Convex resolves exact replay first, then transactionally counts open Passive Income packets and refuses a new insert when the same stream already has one or the lane already has three. For this guard, `open` means `status` is neither `done` nor `archived` and `expiresAt > serverNow`; an expired row does not consume capacity even before the expiry mutation persists closure. The producer's local count is never authoritative.

JT submits the four fields through the specialized authenticated `pi-mc-decision-v1` route. Convex stores the canonical decision and hash but leaves the task open. The PI controller retrieves the immutable decision through the producer-capability GET, commits the exact values to SQLite, then sends `pi-mc-decision-ack-v1` containing the full decision-event envelope. Convex recomputes decision/event hashes and verifies task, admitted/current payload, stored values, and one-time acknowledgment before setting Done and writing `outcomeRef`. Add fixed refusals for missing, stale, duplicate-conflicting, or mismatched submissions; identical reads/acks are no-ops. The producer uses a durable SQLite outbox and stable dedupe key so a crash after remote admission is reconciled by exact replay before the local receipt finalizes.

For live PI decision packets, `InspectionDrawer` renders the four-field specialized form instead of a Telegram paste destination. The existing `jt-decision-packet.v0.json` is explicitly bootstrap-only; `jt-decision-form.v1.json` is the synthetic form/route fixture.

### Step 5.2: Preserve global ranking authority

The PI Governor computes eligibility and a supporting score. It does not create another Today queue. The existing Mission Control allocator maps verified economics, probability, urgency, risk, blockers, and JT minutes and ranks the card alongside all other lanes.

Treat `/passive-income` as a read-only portfolio/evidence surface. Remove decision-language or controls that imply it is a second queue; only admitted lane packets are actionable.

Verification:

```bash
cd /Users/jtsomwaru/.openclaw/workspace/mission-control
bun test lib/mission-control/lane-packet.test.ts lib/mission-control/lane-packet-route.test.ts lib/mission-control/lane-packet-transitions.test.ts lib/mission-control/lane-packet-convex.test.ts lib/mission-control/passive-income-lane-adapter.test.ts
bun test
npx tsc --noEmit
npm run build
```

Crash-boundary tests cover: local outbox before admission; remote insert followed by local failure; returned task ID persisted before receipt failure; exact-replay recovery; stream cap race; lane cap race; and zero-write exact replay.

Gate: local adapter proof, full Mission Control suite, independent verification, then separate approval for exactly one controlled PI-01 card admission and replay.

---

## Phase 6 — Build the thin n8n runtime

This phase begins only after the blueprint and deterministic domain code are independently accepted.

### Step 6.1: Builder handoff

Provide the n8n Builder Agent:

- immutable blueprint SHA;
- immutable domain-code SHA;
- exact target n8n version;
- sanitized runtime fixtures;
- expected receipts;
- deployment and rollback boundary.

The builder must read `/Users/jtsomwaru/projects/n8n-agent/tasks/lessons.md` before changing anything.

### Step 6.2: Build three workflows, not one monolith

Create under the isolated n8n-agent worktree:

- `workflows/passive-income/pi-governor.source.json`
- `workflows/passive-income/pi-revenue-reconciliation.source.json`
- `workflows/passive-income/pi-error-no-run-monitor.source.json`
- `workflows/passive-income/fixtures/*.json`
- `workflows/passive-income/expected/*.receipt.json`
- `scripts/test_passive_income_workflows.py`

1. **PI Governor** — invokes `run-governor`, consumes the durable outbox, admits/reconciles a packet, and finalizes a terminal receipt.
2. **Revenue Reconciliation** — validates signed-event evidence, invokes `record-commerce-event` and `run-revenue`, then uses the same outbox saga for mismatches.
3. **PI Error/No-Run Monitor** — zero-LLM 26-hour freshness check for daily workflows, one alert per fingerprint/24 hours, and one recovery receipt.

Node-by-node interfaces, retries, exit codes, dead-letter schema, and test payloads are canonical in `memory/app-discovery/pi-01-reliability-kit/n8n-blueprint.md`; the builder may not collapse or reorder them without a reviewed blueprint revision.

Distribution remains a separate draft-only workflow after the first paid delivery. Catalog remains dormant until the first paid sale.

### Step 6.3: Prove before deployment

Run every test payload in `n8n-blueprint.md`, source/live normalization, rollback rehearsal, kill switch, and credential/reference scan. Obtain fresh independent acceptance of the immutable bundle.

```bash
python3 scripts/test_passive_income_workflows.py --fixtures workflows/passive-income/fixtures --expected workflows/passive-income/expected
python3 -m compileall scripts/test_passive_income_workflows.py
git diff --check -- workflows/passive-income scripts/test_passive_income_workflows.py
```

Gate: separate approval for inactive deployment. Separate approval again for one controlled pilot. No schedule yet.

---

## Phase 7 — Pilot ten deliveries

### Step 7.1: Controlled pilot

- Manually initiate fulfillment.
- Reconcile every payment and delivery.
- Record support and JT minutes.
- Classify every issue against the failure playbook.
- Keep one unresolved PI-01 card maximum.

### Step 7.2: Evaluate passivity

Track:

- recognized revenue;
- refunds and platform fees;
- infrastructure cost;
- support minutes per sale;
- JT minutes;
- net profit per JT hour;
- delivery failures;
- membership intent/conversion;
- update incidents.

Pause if support load turns the kit into services in disguise. Report the rolling 30-day net profit per JT hour after ten deliveries against the provisional `$250 net/JT-hour` benchmark, but do not pause or kill on that comparison until JT approves the benchmark or a versioned trailing-90-day consulting median.

Gate: ten deliveries, no critical support pile-up, refund rate <=10%, deterministic delivery, and approved support threshold.

---

## Phase 8 — Enable recurrence and distribution

### Step 8.1: Soak the runtime

Run at least three expected opportunities across five weekdays with terminal receipts, no duplicates/lost outcomes, source/live equality, a working kill switch, and no WIP breach.

### Step 8.2: Approve the schedule

JT explicitly approves frequency, cost ceiling, external hosts, alert path, and disable procedure. Only then enable the daily Governor and Revenue Controller recurrence.

### Step 8.3: Activate product-led distribution

Create drafts only from accepted kit IP:

`one problem -> one proof -> one CTA -> active destination`

Autonomous publication remains off until the first ten deliveries show no critical support pile-up and JT separately approves the publication contract. No destination means no post.

---

## Phase 9 — Scale or kill

Scale only when:

- ten or more deliveries exist;
- refunds are <=10%;
- contribution margin is positive;
- membership conversion is >=15% or verified inbound supports a second same-family kit;
- JT cards stayed within WIP for 14 days.

The next product, if earned, must stay in the reliability family: observability, credentials/rotation, or client handoff. Derive one to three digital byproducts only after a paid kit sale.

Kill or pause when:

- the 14-day validation gate fails;
- dependency risk lacks a fallback;
- support makes the product a service in disguise;
- rolling 30-day post-launch net profit per JT hour after ten deliveries is below a JT-approved client-fix benchmark; the current `$250` planning default is advisory only.

---

## Final acceptance checklist

- [ ] PI-01 has an immutable stream/event/receipt contract.
- [ ] Validation evidence passes the two-of-four gate.
- [ ] JT approved price, package, upsell treatment, and support threshold.
- [ ] Every kit promise has a fixture and expected result.
- [ ] Checkout, refund, delivery, and replay are proven.
- [ ] Mission Control admits one card and exact replay creates zero writes.
- [ ] n8n source/live equality, rollback, kill switch, receipts, and no-run detection pass.
- [ ] Ten controlled deliveries complete without critical support pile-up.
- [ ] Five-weekday soak passes.
- [ ] Recurrence receives explicit approval.
- [ ] Scale or kill decision is evidence-bound.
