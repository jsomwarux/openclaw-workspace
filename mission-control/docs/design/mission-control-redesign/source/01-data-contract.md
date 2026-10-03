# Mission Control — Task Data Contract

Prepared 2026-10-02 for a from-scratch interface redesign. This file describes the data and the rules the backend enforces. It says nothing about the current interface on purpose.

## 0. Sources and how the numbers were made

- **Backend rules** come from the Mission Control app's data layer. File paths are relative to the app root: `convex/` (database schema and server functions), `app/api/` (HTTP routes), `lib/mission-control/` (contracts, adapters, ranking logic), `docs/` (integration contracts), plus `CLAUDE.md`. Every rule below cites its file and line numbers.
- **Not read (blind-design rule):** page components, layouts, navigation, presentational components, styling, and screenshots. When a question can only be answered from interface code (for example, whether a screen reads `sortOrder`), this file says so and leaves it open.
- **Live statistics** were read once, read-only, through `GET /api/tasks` and `GET /api/tasks?include=archived` on the already-running local server at **2026-10-03T00:07Z (2026-10-02 20:07 ET)**. No credential, configuration, or data was changed. Every statistic carries one of these labels:
  - **[current]**: the 85 non-archived tasks (63 todo, 20 done, 2 waiting-external).
  - **[decision-31]**: the 31 Growth OS decision cards (a subset of current).
  - **[archived]**: the 1,337 archived tasks.
  - **[all]**: current + archived = 1,422.
- "Filled" means present and not empty (an empty string, empty list, or missing key counts as unfilled). Lengths are characters.

## 1. Premise check

| Premise | Verdict | Evidence [current] |
|---|---|---|
| 31 Growth OS decision cards exist | **True** | 10 titled Q1–Q10, 12 titled P1–P12, 9 titled AP1–AP9 |
| All 31 are in todo | **True** | 31 of 31 `status: "todo"`, all `assignee: "jt"` |
| Ordered Q1–Q10, P1–P12, AP1–AP9 with sortOrder 201–231 | **True as stored** | Q1–Q10 = 201–210, P1–P12 = 211–222, AP1–AP9 = 223–231, one value per card |
| They sit alongside other operational cards | **True** | 54 other current cards (32 todo, 20 done, 2 waiting-external) |
| The 201–231 band holds only these 31 | **False** | 36 todo cards sit in the band. sortOrder 220 is shared by P10 and 5 other low-priority cards |
| That stored order is the order anything is shown in | **False for every ordering the backend and logic layer define** | See §7. No backend or logic function reads `sortOrder`. Today and the Work list both put the 31 in exactly reverse order (AP9 first, Q1 last) |

Shape of the 31 [decision-31]:
- **Fields.** Each fills only 9 fields: title, description, status, assignee, priority, project, sortOrder, createdAt, updatedAt. None has whyItMatters, exactSteps, pasteReadyPrompt, evidenceLinks, dollars, dueDate, or any scoring input.
- **Priority.** Q and AP cards are high (19). P cards are medium (12).
- **Lengths.** Titles run 40 / 67 / 130 (min / median / max); every title starts with the program name, then the code, then a colon. Descriptions run 643 / 879 / 1,767.
- **Description layout.** Every description has the same skeleton:
  - a `First action:` line;
  - 4–5 bullets that start with a bold label;
  - three closing lines, `Why it matters:`, `Done:` and `Guard:`, which are **identical on all 31 cards**.
- **Bullet labels by family:**
  - Q: question → why → proposed answer → empty `Answer:`.
  - P: change → evidence → reviewer note → (sometimes "where it would be built differently") → recommendation. P cards have no answer slot.
  - AP: draft or patch → status → (sometimes a choose line) → built differently → empty `Answer:`.
- **The answer gap.** 19 cards (all Q and AP) end with an empty `- **Answer:**` bullet for JT to fill. **The backend has no typed field for that answer.** The only ways to record one today are a free-text description edit or an append-only feedback entry.

## 2. Task fields

Type notation follows the schema in `convex/schema.ts:228-308`. "ms" means epoch milliseconds. Every field except title, status, assignee, priority, createdAt and updatedAt is optional.

### 2.1 Core card fields

| Field | Type | What it means to the operator | [current] filled /85 | [decision-31] /31 | [archived] /1,337 | Length [current] min / median / max | Longest [all] |
|---|---|---|---|---|---|---|---|
| title | string | The card's headline | 85 | 31 | 1,337 | 29 / 57 / 130 | 609 |
| description | string | Free-text body. On decision cards it holds the whole decision. 56 current descriptions contain line breaks and 32 use markdown bold. URLs inside it are turned into evidence links (§2.4) | 85 | 31 | 1,315 | 150 / 743 / 1,767 | 4,238 |
| status | enum (§3) | Where the card is in its life | 85 | 31 | 1,337 | todo 63, done 20, waiting-external 2 | |
| assignee | `"jt"` \| `"eve"` \| `"both"` | Who acts: jt = the operator, eve = the operator's AI agent, both = shared | 85 | 31 | 1,337 | jt 79, eve 6, both 0 ([archived]: both 13) | |
| priority | `"high"` \| `"medium"` \| `"low"` | Importance label. Drives the Work list order. **Never affects Today order** | 85 | 31 | 1,337 | high 49, medium 31, low 5 | |
| project | string | Free-text grouping label (8 distinct values) | 84 | 31 | 1,294 | 6 / 21 / 21 | 21 |
| sortOrder | number | A position number the agent writes under its own convention (§7.4). No backend or logic function reads it | 71 | 31 | 1,302 | values 3–302; 7 values shared by more than one card | |
| clientId | id → clients | Links the card to a client record | 5 | 0 | 5 | | |
| createdAt | ms | When the card was created | 85 | 31 | 1,337 | age 0 / 1.4 / 142 days | |
| updatedAt | ms | Last write of any kind, including a feedback append. It is the main tie-breaker in ordering (§7) | 85 | 31 | 1,337 | age 0 / 1.4 / 66 days | |
| _id, _creationTime | system | Database id (32 characters) and insert time | 85 | 31 | 1,337 | | |

### 2.2 Seven-field universal card (all optional; legacy cards omit them)

| Field | Type | Meaning | [current] /85 | [decision-31] | [archived] | Length [current] | Longest [all] |
|---|---|---|---|---|---|---|---|
| firstAction | string | The first concrete step | 23 | 0 | 21 | 52 / 119 / 268 | 268 |
| whyItMatters | string | Why the card deserves attention | 25 | 0 | 31 | 61 / 115 / 220 | 270 |
| exactSteps | string[] | Ordered steps | 10 | 0 | 19 | 3 / 4.5 / 5 steps; each step 30 / 89 / 190; all steps together 240 / 377 / 615 | 6 steps; step 193 |
| pasteReadyPrompt | string | Text meant to be copied verbatim into another tool | 6 | 0 | 12 | 36 / 93 / 161 | **10,533** (an archived card: 108 lines, mostly inside one code fence, 46 bullets, 23 numbered lines, 1 heading) |
| pasteDestination | string | Where that prompt gets pasted. Can exist without a prompt (3 current cards) | 9 | 0 | 12 | 24 / 39 / 69 | 102 |
| doneState | string | What "done" looks like | 25 | 0 | 35 | 53 / 125 / 312 | 312 |
| feedback | entry[] (§2.6) | Append-only notes from the operator or agent | **0** | 0 | **0** | no entry exists in any record | |

### 2.3 Scheduling, waiting, and scoring inputs

| Field | Type | Meaning | [current] /85 | [decision-31] | [archived] | Values [current] |
|---|---|---|---|---|---|---|
| dueDate | ms | Deadline | 14 | 0 | 11 | all 14 are past due: 10.5 to 42 days overdue |
| dueDateSource | `"external"` \| `"self"` | Real external deadline, or self-imposed (counts half) | 9 | 0 | 11 | self 8, external 1. **5 cards have a dueDate with no source, so the scorer ignores their deadline** |
| dollars | number | Cash attached to the card | 4 | 0 | 5 | 1,500–2,250 |
| stageProbability | number 0–1 | Chance the cash lands | 4 | 0 | 5 | 0.35–0.55 |
| cashDirect | boolean | Override: is this direct cash | 0 | 0 | 0 | |
| effortMinutes | number | Effort estimate | 0 | 0 | 1 | |
| lane | string (free text) | Routing lane. The logic layer recognizes only work, revenue, ship, machine, evidence, health; anything else falls back to a keyword guess on project + title | 21 | 0 | 14 | revenue 12, plus 9 cards with unrecognized values ("systems" 7, "jobs" 2) |
| waitingOn | {who, what, since ms, nudgeAfterDays} | Parked on an outside person until a nudge is due | 1 | 0 | 0 | who 14 chars, what 45 chars, waiting 22 days, nudge after 14 days (**nudge overdue**) |
| snoozedUntil | ms | Hidden from Today until this time | 3 | 0 | 4 | all 3 passed 24.5 days ago, so they are visible again |
| proofRequired | boolean | Finishing this should yield a proof asset. Raises rank; **not enforced at completion** | 16 present (8 true) | 0 | 8 | |
| riskContainment | boolean | Prevents a loss. Raises rank | 1 (true) | 0 | 1 | |
| blocks | number | How many other items **this card** blocks (not "is blocked") | 1 (2) | 0 | 2 | |
| blocksAgent | boolean | This card blocks an agent | 0 | 0 | 1 | |
| reasonCodes | string[] | Extra stored reason codes, prepended to the scorer's own | 0 | 0 | 0 | |
| rankScore, rankUpdatedAt | number, ms | Legacy stored rank. Never read by Today | 0 | 0 | 0 | |
| reviewAt | ms | Revisit date | 0 | 0 | 0 | |
| workstream | `"paid-delivery"` \| `"career-hedge"` \| `"compounding-bet"` \| `"administrative"` \| `"other"` | Portfolio bucket | 14 | 0 | 3 | paid-delivery 7, other 4, career-hedge 2, administrative 1 |
| slug | string | Stable short id on pipeline and legacy cards | 10 | 0 | 107 | 7 / 22 / 63 |
| pipelineStage | string | Sales pipeline stage label (5 distinct) | 11 | 0 | 58 | 2 / 19 / 28 |

### 2.4 Evidence and provenance

| Field | Type | Meaning | [current] /85 | [decision-31] | [archived] | Values [current] |
|---|---|---|---|---|---|---|
| evidenceLinks | string[] | Links or local file paths that back the card | 9 | **0** | 10 | 1 / 3 / 4 per card; each 22 / 66 / 97 chars; 13 web links, 13 file paths. **76 of 85 current cards have none** |
| sourceSystem | string | Which producer wrote the card (5 distinct) | 10 | 0 | 10 | 3 / 22 / 22 |
| dedupeKey | string | Producer's idempotency key (§5.4) | 13 | 0 | 26 | 41 / 92 / 142 |

The adapter builds one evidence list per card: every `http(s)` URL found in the description, followed by every evidenceLinks entry (`lib/mission-control/adapters.ts:166-201`). Entries are tagged as a web link, a hosted document, or a local file. 7 current descriptions contain URLs.

### 2.5 Experiment and nightly-validation fields (no current data)

`hypothesis`, `nextTest`, `killDate`, `promotionScore`, `revivalTrigger`, `verdict`, `verifierConfirmed`, `verifiedAt`, `sourceHash`, `evidenceScore`, `distributionScore`, `fatalConstraint`: 0 current. hypothesis, nextTest and revivalTrigger each appear on 1 archived card; none of the others appears anywhere. They belong to "compounding bet" cards and to cards admitted by the nightly validation controller (§5.5).

### 2.6 Nested records

| Record | Shape | Notes |
|---|---|---|
| feedback entry | `{ id: string, body: string, author: "jt" \| "eve", createdAt: ms }` (`convex/schema.ts:89-94`) | id = `"<createdAt>-<n>"`, server-assigned. Body is 1–4,000 characters after trimming |
| waitingOn | `{ who, what, since, nudgeAfterDays }` (`convex/schema.ts:13-18`) | |
| outreachReview | candidateId, cohortId, draftSha256, subject, body, verifierReport, reviewAuthorityId, verifierActorId, gitBindings {evidence, policy, gate, draft, verifier}, optional suppressionBinding, snapshotSha256, reviewCycle 1 \| 2, admittedBy "server", admittedAt (`convex/schema.ts:57-78`) | [current] 6 cards. Subject 17 / 18 / 22, body 31 / 55 / 459, verifier report 34 / 52 / 2,506 chars. The top-level `candidateId`, `cohortId`, `draftSha256` fields mirror it |
| outreachDecision | `{ candidateId, draftSha256, snapshotSha256, decision: "approve" \| "reject", decidedBy: "jt", decidedAt }` (`convex/schema.ts:80-87`) | [current] 4 decided (all reject), 2 awaiting a decision |
| artifactRef | `{ system, id, url?, sha256 }` | Lane packets only |
| doneEvidence | `{ type, ref, recordedAt, recordedBy: "jt" }` | Lane packets only. [all] 0 |
| outcomeRef | `{ system, id, url?, recordedAt }` | Lane packets only. [all] 0 |
| closureReason | `{ kind: "rejected" \| "skipped" \| "expired" \| "no-action", note?, closedAt, closedBy: "jt" \| "eve" \| "server" }` | Lane packets only. [all] 0 |

### 2.7 Lane-packet envelope (Growth OS card envelope v1)

These fields exist only on cards admitted through the lane-packet route. Only the server writes them (`lib/mission-control/lane-packet.ts:164-168`).

| Field | Type | Meaning | [current] |
|---|---|---|---|
| packetSchema | `"lane-packet-v1"` | Marks the card as a lane packet | 1 |
| growthLane | `"linkedin"` \| `"x"` \| `"outreach"` \| `"jobs"` \| `"apps"` \| `"passive-income"` \| `"networking"` \| `"profile-site"` | Which growth lane produced it | 1 (jobs) |
| artifactRef | object | Pointer to the reviewed artifact plus its hash | 1 |
| payloadHash / admittedPayloadHash | 64-hex | Hash of the current card content / content at admission | 1. **They differ: the card was edited after admission** |
| approvalState | `"pending"` \| `"approved"` \| `"rejected"` | JT's approval of the current content | 1 (pending) |
| approvedPayloadHash, approvedAt | 64-hex, ms | Which content version was approved, and when | 0 |
| expiresAt | ms | Last moment the card is actionable | 1 (2.0 days out) |
| estMinutes | integer 1–480 | Estimated minutes | 1 (20) |
| doneEvidenceType | `"post-url"` \| `"message-ref"` \| `"application-ref"` \| `"rsvp-ref"` \| `"profile-edit-ref"` \| `"deploy-ref"` \| `"none"` | Proof JT must record to finish. `none` = internal card | 1 (application-ref) |
| doneEvidence, outcomeRef, closureReason | §2.6 | Completion proof, downstream outcome, typed closure | 0 |

Conflict to note: Mission Control's `CLAUDE.md` describes the one live packet as "exact-payload-approved". Live data shows `approvalState: "pending"`, no approvedPayloadHash, and a payload hash different from the admitted one. That is exactly the state a generic content edit leaves behind (§6.3).

## 3. Statuses

### 3.1 Stored statuses (`convex/schema.ts:4-11`)

| Status | Meaning | [current] | [archived] |
|---|---|---|---|
| `todo` | Open, not started | 63 | — |
| `in-progress` | Being worked | 0 | — |
| `waiting-external` | Waiting on someone outside | 2 | — |
| `snoozed` | Put to sleep (status form) | 0 | — |
| `done` | Finished | 20 | — |
| `archived` | Out of the active list | — | 1,337 |

**There is no `blocked` status, flag, or blocked-by field.** Blocked work is described in title or description prose; 18 current cards mention block, blocked or blocker. `snoozedUntil` (a timestamp on an open card) and the `snoozed` status are separate mechanisms.

### 3.2 Display statuses the adapter derives (not stored)

`lib/mission-control/adapters.ts:156-164` maps stored status one to one, with one exception: `todo` + `assignee: "both"` + `priority: "high"` becomes **awaiting-approval** (0 current cards qualify). The shared status type also names `awaiting-decision`, `blocked`, `failed` and `stale` (`lib/mission-control/types.ts:16-27`), but the task adapter never produces them. Only scheduled jobs (`failed`), agents (`stale`) and proof entries (`failed`) can carry them.

## 4. Status transitions the backend allows

### 4.1 Generic task (includes the 31 decision cards, legacy cards, agent cards)

- **Any status → any status**, in one write, by any caller that can reach the server: `PATCH /api/tasks {id, status}` → `tasks.update` (`app/api/tasks/route.ts:88-133`, `convex/tasks.ts:871-910`). The `tasks.updateStatus` and `tasks.updatePipelineStage` mutations do the same (`convex/tasks.ts:857-869, 1048-1063`). **No transition table exists.** An archived card can be reopened, and a done card can go back to todo.
- **System: done → archived.** A scheduled job runs daily at 03:00 UTC. It archives every `done` card whose `updatedAt` is more than 7 days old and skips outreach review cards (`convex/crons.ts:6-11`, `convex/tasks.ts:1028-1046`).
- Delete is permanent: `DELETE /api/tasks?id=` → `tasks.remove` (`convex/tasks.ts:928-940`).

### 4.2 Outreach review card

- Admission creates it as `todo` (pending JT).
- JT's first decision moves it **todo → done**, with `outreachDecision` approve or reject. A decision is refused unless the card is `todo` (`lib/mission-control/outreach-decision.ts:66-99`).
- Nothing else can change it. Generic update, status, pipeline-stage, upsert and delete all throw (`lib/mission-control/outreach-decision.ts:101-105`, called at `convex/tasks.ts:865, 903, 932, 1059`), and auto-archive skips it.
- An identical retry of the same decision is a no-op. A different decision, or one against a changed snapshot, is refused (409) and needs a new, versioned card.

### 4.3 Lane packet (`lib/mission-control/lane-packet-transitions.ts`)

- **Open statuses:** todo, in-progress, waiting-external, snoozed. Generic writes may move between them (lines 199-224).
- **Terminal:** `done`, or `archived` with a typed closureReason. Once terminal, every generic write and every transition is refused ("closed"). Only a feedback append still works (lines 131, 209).
- **Generic done** is allowed only when `doneEvidenceType` is `none` (line 211). **Generic archive** is always refused (line 214). **Delete** is refused (line 226).
- Typed transitions are in §6.3.

## 5. What the backend permits, by card type

Legend: ✅ allowed · ❌ refused by the backend · 🔒 JT only (identity-checked) · — not applicable

| Action | Generic task (incl. decision-31) | Outreach review card | Lane packet, open | Lane packet, closed |
|---|---|---|---|---|
| Create | ✅ `POST /api/tasks`; no identity required | ✅ only `POST /api/tasks/outreach-review` with the review capability | ✅ only `POST /api/tasks/lane-packet` with the producer capability | — |
| Edit text or scoring fields | ✅ any caller | ❌ immutable | ✅ any caller. A content edit re-hashes and resets approval to pending | ❌ |
| Change status | ✅ any → any | ❌ (only via decision) | ✅ among open statuses; done only if `doneEvidenceType: none`; archive ❌ | ❌ |
| Set priority, defer, snooze | ✅ | ❌ | ✅; snoozedUntil cannot pass expiresAt | ❌ |
| Append feedback | ✅ | ✅ (snapshot untouched) | ✅ (hash untouched) | ✅ |
| Delete | ✅ | ❌ | ❌ | ❌ |
| Approve | — (no approval concept) | 🔒 decision `approve` (while todo) | 🔒 with current payloadHash, before expiry | ❌ |
| Reject | — | 🔒 decision `reject` (while todo) | 🔒 with current payloadHash; also allowed after expiry | ❌ |
| Complete | ✅ by setting status done (no proof needed) | — (approve or reject closes it) | 🔒. External type: needs an approved current hash plus evidence of the declared type. `none` type: no approval or evidence needed. Expiry does not block it | ❌ |
| Skip / close with no action | — | — | ✅ JT or agent (producer capability) | ❌ |
| Expire | — | — | Server only; hidden from Today at read time | — |

Sources: `app/api/tasks/route.ts`, `app/api/tasks/[id]/route.ts`, `app/api/tasks/create-only/route.ts`, `convex/tasks.ts` (create 336-367, upsert 369-416, create-only 420-458, admit 466-506, transition 514-550, update 871-910, feedback 912-926, remove 928-940, decision 942-971), `lib/mission-control/lane-packet-route.ts:42, 144-176`, `lib/mission-control/lane-packet-transitions.ts:41, 121-186`.

### 5.1 Client-side conventions (logic layer, not enforced)

- "Defer" writes `{priority: "low", status: "todo"}` (`lib/mission-control/work-actions.ts:10-12`).
- The Work list offers three statuses, labeled todo, doing and done (`lib/mission-control/work-status.ts`). Every other stored status is shown as todo there.

### 5.2 Nightly validation cards (none live)

A generic card with `sourceSystem: "nightly-validation-controller"` must carry all of the following, or it is refused (`convex/tasks.ts:248-272`, `lib/mission-control/task-admission.ts:79-107`):
- dedupeKey, firstAction, whyItMatters, doneState, workstream, candidateId and sourceHash;
- at least one evidence link;
- promotionScore ≥ 30, evidenceScore ≥ 4, distributionScore ≥ 3;
- verdict `promote`, verifierConfirmed `true`, fatalConstraint `false`;
- verifiedAt within the last 24 hours.

Snake_case aliases are refused. **Side effect:** `tasks.update` re-checks these rules against the merged record (`convex/tasks.ts:904`). Once verifiedAt is more than 24 hours old, any edit through `PATCH /api/tasks`, including a status change, fails on such a card.

## 6. Authority boundaries the backend enforces

### 6.1 Who is who

- Generic task routes have **no identity check**. Mission Control's `CLAUDE.md` says it is "localhost only" behind the private network. Anyone who can reach the server can create, edit, re-status or delete a generic card.
- **JT identity**: a trusted login header added by the private-network proxy must equal a configured login. The server then uses its own decision capability, which producers never hold (`lib/mission-control/lane-packet-route.ts:110-117`). The same pattern guards outreach decisions.
- **Producers** (the agent and other automated systems) hold separate capabilities for admitting lane packets and outreach reviews. If any required capability is missing, blank, or equal to another, the route fails closed with 503 before touching data.

### 6.2 Actions that require JT

| Action | Where enforced |
|---|---|
| Approve, reject, or complete a lane packet | `lib/mission-control/lane-packet-transitions.ts:41, 128-130`; producer callers get 403 (`lane-packet-route.ts:161-163`) |
| Approve or reject an outreach review (first and only decision) | `convex/tasks.ts:942-971`; `decidedBy` is fixed to `"jt"` |
| Record completion evidence on a lane packet (`recordedBy: "jt"`) | `lane-packet-transitions.ts:170-178` |

Everything else, including marking a generic card done, needs no identity.

### 6.3 Proof requirements

| Rule | Where |
|---|---|
| External-action lane packet: completion needs evidence whose type equals `doneEvidenceType`; `post-url` evidence must be an https URL; ref 1–500 chars | `lane-packet-transitions.ts:157-166` |
| ...and the current payload must be approved (`approvedPayloadHash === payloadHash`) | `lane-packet-transitions.ts:167-169` |
| Approval is bound to an exact content hash. A stale hash is refused (409, "payload changed since review") | `lane-packet-transitions.ts:137, 145` |
| Any generic edit to title, description, firstAction, whyItMatters, exactSteps, pasteReadyPrompt, pasteDestination or doneState re-hashes the payload. If the card was approved, it returns to pending | `lane-packet-transitions.ts:219-223`; editable fields `lane-packet.ts:145-154` |
| Nightly validation admission needs evidence links, verification, and scores | §5.2 |
| `proofRequired: true` is **only a ranking input**. Nothing checks for proof when such a card is marked done | `lib/mission-control/score.ts:79` |
| Generic `done` needs no evidence. [current] 0 of 20 done cards carry `doneEvidence` | |

### 6.4 Expiry

- Only lane packets expire. At admission, `expiresAt` must be in the future and at most 90 days out (`lane-packet.ts:134, 318-319`).
- Today hides an open packet at or past `expiresAt`, at read time (`lib/mission-control/lane-capacity.ts:16-18`, `score.ts:215-218`).
- After expiry, **approve** is refused (`lane-packet-transitions.ts:136`). Reject, complete, skip and no-action are not blocked.
- Snoozing past `expiresAt` is refused (`lane-packet-transitions.ts:215-217`).
- The persisted closure (`archived` + `closureReason {kind: "expired", closedBy: "server"}`) is written only by the internal mutation `tasks.expireDueLanePackets` (`convex/tasks.ts:557-571`). **That mutation is not scheduled.** The only scheduled job is auto-archive. [all] 0 expired packets so far.

### 6.5 Deduplication

| Path | Rule |
|---|---|
| `POST /api/tasks` without dedupeKey | Plain insert. **Duplicates are possible** |
| `POST /api/tasks` with dedupeKey (default mode) | **Upsert.** An existing generic card with that key is **overwritten** with the new fields (`lib/mission-control/task-upsert.ts`) |
| `POST /api/tasks?mode=create-only` or `POST /api/tasks/create-only` | Create-if-absent. An existing card is returned untouched (`task-create-only.ts`, `task-write-mode.ts`) |
| Lane packet | Key stored as `lane-packet:v1:<lane>:<producerKey>`. An exact retry returns the existing card, even after closure. A different payload while an earlier version is open → 409. A new version is allowed only once every earlier version is closed. The `lane-packet:` prefix is reserved and refused on generic paths (`lane-packet.ts:213-219, 456-503`) |
| Outreach review | One review cycle per distinct snapshot per candidate + cohort, at most 2. An exact retry is idempotent. A third distinct snapshot → 409 |
| Nightly card | dedupeKey required |

### 6.6 Append-only feedback

- The only writer is `PATCH /api/tasks` with `{action: "append-feedback", id, body, author}` → `tasks.appendFeedback` (`app/api/tasks/route.ts:92-112`, `convex/tasks.ts:912-926`).
- Every other create or update path refuses a `feedback` field: HTTP check at `task-admission.ts:51-53`, and the generic mutation argument lists do not include it.
- Body is trimmed and must be 1–4,000 characters (`task-feedback.ts:3, 13-15`).
- The server sets `id` and `createdAt`. The existing list is copied and the new entry is added at the end, so entries cannot be edited, reordered or removed.
- `author` is whatever the caller declares (`"jt"` or `"eve"`). **It is not identity-checked.**
- Appending bumps `updatedAt`, which changes ordering ties (§7). It works on every card type, including closed lane packets and decided outreach cards.

### 6.7 Change audit trail

A generic update that changes `dollars`, `dueDate`, `waitingOn`, `stageProbability` or `priority` writes a `priorityAudit` row: {taskId, field, oldValue, newValue, evidence, source "eve" \| "jt" \| "model", ts}. Source defaults to "jt" and evidence to "manual edit" (`convex/tasks.ts:275-307`, schema 360-370). **Status, title and description changes are not audited.** Read it with `tasks.listAudit`.

### 6.8 Writer policy (documented, not enforced)

The agent's write contract (workspace `memory/mission-control-write-contract.md`) and task-board rules (workspace `docs/agents/task-board-rules.md`) say:
- the agent never sets priority high;
- every fact update carries an evidence string;
- cash-bearing cards get dollars and stageProbability;
- client cards get clientId;
- cards blocked on a person get waitingOn;
- every card states a first action, why it matters, and what done looks like.

The backend checks none of this outside nightly admission.

## 7. Ordering today

### 7.1 Today queue: `allocateToday` (`lib/mission-control/score.ts:207-248`) is the only owner

This function alone orders Today; the command brief reads its result. **priority, sortOrder and rankScore are never inputs** (lines 190-206, and the lane-packet contract doc).

1. **Exclusions:**
   - agent and proof entries;
   - status done, archived or snoozed;
   - an open lane packet at or past expiry (counted separately as "expired");
   - snoozedUntil in the future;
   - owner `eve`, unless the entry has failed (tasks never do; only scheduled jobs can fail);
   - a card with `waitingOn.who`, until `now − since > nudgeAfterDays` days. Once the nudge is due, the card is admitted with its title rewritten to `Nudge <who>: <what>` and a `nudge-due` reason code.
   - **`waiting-external` status alone does not exclude a JT-owned card.**
2. **Score 0–100.** These factors are added together (`score.ts:6-83`):

| Factor | Points | Input |
|---|---|---|
| Cash | 0 / 15 / 30 / 40 | expected = dollars × stageProbability (missing probability counts as 1). Indirect cash (lane not revenue, unless cashDirect) = 15. Direct: ≥3,000 → 40, ≥1,000 → 30, else 15 |
| Deadline | 0 / 8 / 12 / 15 | Needs both dueDate **and** dueDateSource. Overdue or today 15, ≤3 days 12, ≤7 days 8. Self-set deadlines count half |
| Unblock | 0 / 8 / 15 | blocksAgent or blocks ≥ 2 → 15; blocks = 1 → 8 |
| Proof | 0 / 10 | proofRequired |
| Risk | 0 / 10 | riskContainment |
| Stability | 0 / 10 | lane = health |

   Modifiers (lines 124-141):
   - −15 off-focus: the week's focus row lists projects, the card's project is not among them, and cash < 30.
   - −10 long effort: effortMinutes (or estMinutes) ≥ 60 and cash < 20.
   - Ship cap at 25: ship-lane card with no dollars, while the focus mandate is consulting-cash and collected cash is below the gate.
   - The result is clamped to 0–100. A score ≥ 50 with no reason gets an `unexplained` code.

3. **Sort:** score high → low, then `updatedAt` newest first, then title A → Z.
4. **Lane capacity** (`lane-capacity.ts:31-63`): optional per-lane minute budgets from the week's focus row. They filter lane packets in rank order and never reorder. A packet with an external deadline inside 24 hours always fits but still uses budget. Packets that don't fit are reported as a count per lane ("overflow").
5. **Cut to 7.** Position 1 is the single top item; positions 2–7 follow.

Reason codes the scorer emits: `cash:<amount>`, `deadline:<date>`, `deadline:self:<date>`, `unblocks:<n>`, `unblocks:agent`, `proof`, `risk`, `stability`, `focus-penalty`, `effort-demotion`, `ship-capped`, `nudge-due`, `unexplained`.

Score context (`lib/mission-control/score-context.ts`): the focus row is looked up by the first day of the current week (local time). **No focus row exists for the week of 2026-09-28**, so right now there is no mandate, no off-focus penalty, no ship cap, and no lane budgets.

### 7.2 Work list order (`lib/mission-control/work-priority.ts:41-51`)

priority high → low, then status rank (failed/blocked 5, stale 4, awaiting-decision/approval 3, todo/in-progress 2, waiting-external 1, snoozed/done/archived 0), then `updatedAt` newest first. The derived "blocked" filter (`work-filters.ts:44`) matches blocked/stale status **or any card untouched for 14+ days**.

### 7.3 What those rules do to the live 31 (simulation)

This is a standalone re-implementation of the two functions above, written for this packet, run over the live [current] data at capture time with the real (absent) focus row. Failed scheduled jobs were not loaded, so they are not in it.
- **Today:** 62 cards eligible. 14 score above 0. **All 31 decision cards score 0**: they carry no scoring inputs, so none reaches the top 7. They tie, and the newest-first tie-break places them at positions 15–45 **in exact reverse of their intended order: AP9, AP8 … AP1, P12 … P1, Q10 … Q1**. The top slot is the waiting card whose nudge is overdue (score 63).
- **Work list:** AP9…AP1 then Q10…Q1 (high, positions 6–24), then P12…P1 (medium, positions 34–45). Also reverse within each family.
- Any write to one of these cards, including a feedback append, moves it to the front of its tie group.

### 7.4 sortOrder

- **Who writes it.** The agent, by convention (workspace `docs/agents/task-board-rules.md`): high cards use 10–40 for quick wins, 50–90 for alerts, 100+ for strategic work; medium cards use 10, 20, 30…; speculative cards use 500+.
- **Who reads it.** No backend function, no ranking function, and no adapter (searched across `convex/` and `lib/mission-control/`). The lane-packet contract states outright that it never affects Today, and lane packets cannot set it at admission. **Whether any screen reads it was not checked under the blind-design rule.**
- [current] 71 of 85 have one, and 7 values are shared by more than one card.

## 8. HTTP surface a new interface can call

| Method + path | Purpose | Auth |
|---|---|---|
| `GET /api/tasks` | All non-archived tasks (newest first) | none |
| `GET /api/tasks?include=archived` | Archived tasks | none |
| `POST /api/tasks` | Create. Defaults: status todo, assignee **eve**, priority medium. With dedupeKey it upserts; `?mode=create-only` makes it create-if-absent | none |
| `POST /api/tasks/create-only` | Create-if-absent by dedupeKey | none |
| `PATCH /api/tasks` | Update any generic field. `{action:"append-feedback"}` appends feedback | none |
| `PATCH /api/tasks/[id]` | Update, without the HTTP-level field checks. The database argument check still refuses feedback and envelope fields | none |
| `DELETE /api/tasks?id=` or `/api/tasks/[id]` | Delete (refused for outreach and lane packets) | none |
| `POST /api/tasks/lane-packet` | Admit a lane packet | producer capability |
| `PATCH /api/tasks/lane-packet` | approve / reject / complete (JT), skip / no-action (JT or producer) | JT identity or producer capability |
| `POST /api/tasks/outreach-review`, `GET` same | Admit an immutable review / read the review count | review capability |
| `POST /api/tasks/outreach-decision` | JT's approve/reject | JT identity |
| `GET /api/tasks/outreach-decision?candidateId&draftSha256&snapshotSha256` | Exact decision lookup for pre-send checks | decision capability |
| `GET /api/focus?weekOf=YYYY-MM-DD` | The week's focus row (gate, mandate, lane budgets) | none |
| `GET /api/task-audit?taskId=` | Change audit trail for one task, or the 100 most recent rows without `taskId` | none |

Error behavior: lane-packet errors map to fixed messages and codes (400 invalid, 401, 403, 404, 409 conflict/closed/expired/transition-required, 503 not configured) (`lane-packet-route.ts:44-54`). The generic routes return 400 with a validation message, or 500 for anything else.

## 9. Facts a design must not assume away

1. Decision content on the 31 cards lives in prose. Answers, options and the risk guard are text, not fields.
2. 19 cards expect an answer, and no typed field exists for it.
3. The stored Q1→AP9 order is not the order any defined ranking produces. Today and the Work list both reverse it, and Today does not show any of the 31 in its top 7.
4. `blocked` is not a state. `waiting-external` alone does not hide a JT card from Today. Only `waitingOn` parks one.
5. Only lane packets and outreach reviews have approval, evidence or JT-only actions. Generic cards, including all 31 decision cards, can be completed by anyone with no proof.
6. Feedback is append-only and has never been used. Its author label is unverified.
7. Expiry hides lane packets at read time, but the expired closure is never written today.
8. Long content exists. The longest prompt is 10,533 characters, the longest title 609, the longest description 4,238, and the longest verifier report 2,506.
