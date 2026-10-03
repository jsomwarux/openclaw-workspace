# Gaps: what the design needs that the data contract does not support

Each item names what the design needs, what `source/01-data-contract.md` says (section references), and what would be required. "Blocking" means the feature cannot work correctly without it. "Workable" means an interim exists with a stated limit.

Summary

| # | Need | Severity |
|---|---|---|
| 1 | Daily run record | Blocking for multi-device; workable client-only |
| 2 | Typed answer field | Workable via feedback |
| 3 | Approval and identity for decision cards | Blocking for real authority |
| 4 | Decision card marker and typed slots | Workable via parsing |
| 5 | Unique curated order | Workable via title code |
| 6 | Blocker field | Workable for people only |
| 7 | Urgent exception inputs | Partly blocking |
| 8 | Run query that is not the scorer | Blocking |
| 9 | Content change token | Blocking for change detection |
| 10 | Field-level change history | Blocking for "Changed underneath me" detail |
| 11 | Persisted expiry | Workable |
| 12 | Read freshness and connection thresholds | Client-only |
| 13 | Safe retry for feedback | Blocking for retry |
| 14 | Card validation | Workable client-side |
| 15 | Evidence for decision cards; local file paths | Workable |
| 16 | Lane packet proof entry | Blocking for Complete on external packets |
| 17 | Skip and no-action in the action set | Design decision |
| 18 | Identity on generic writes | Blocking for a trusted "only me" |
| 19 | Nudge title | Workable |
| 20 | Undo after closing writes | Constraint |
| 21 | Time zone | Workable |
| 22 | Multi-writer awareness (Eve edits) | See 9 and 10 |
| 23 | Sort order data quality | Data hygiene |
| 24 | Deadline data quality | Data hygiene |

---

## 1. Daily run record

**Design needs:** a committed ordered list for one local date, a cursor, per-item handled state and outcome, a snapshot for change detection, phase (not started, in progress, paused, queue changed, complete), and the position "n of 7".

**Contract says:** "There is no run record, no per-day progress, and no 'handled in this run' marker anywhere in the schema" (`03-state-map.md` Part B header). Skip-for-today is "stored in run state only; no backend write".

**Required:**
- Interim: browser storage keyed by local date (one device; lost if cleared).
- Target: a Convex table, for example `dailyRuns` (`localDate`, `size`, `phase`, `cursor`, `snapshot[]`, `startedAt`, `closedAt`) and `dailyRunItems` (`runId`, `taskId`, `position`, `state`, `outcome`, `deferredOnce`). Mutations: `startRun`, `recordOutcome`, `advance`, `rebaseSnapshot`, `closeRun`. A schema change that is "separately gated" (`03-state-map.md`).

## 2. Typed answer field

**Design needs:** a saved answer on 19 Q and AP cards, shown in the slot where the empty Answer bullet is, required before Complete.

**Contract says:** "The backend has no typed field for that answer. The only ways to record one today are a free-text description edit or an append-only feedback entry" (section 1; section 9, fact 2). Feedback has no `kind`.

**Required:**
- Interim: append feedback with body `Answer: <text>`.
- Target: an optional `answer` field (string, 1 to 4,000) or a feedback `kind` of `answer`, plus a rule that the UI reads the latest `answer`. Without it, finding the answer means parsing a body prefix, and an edited answer cannot be replaced (feedback is append-only).

## 3. Approval and identity for decision cards

**Design needs:** P cards ask approve or decline. Approve and Reject must be an authority only the operator holds.

**Contract says:** generic tasks have "no approval concept" (section 5); generic routes have "no identity check" (section 6.1); `author` on feedback "is not identity-checked" (section 6.6). Only lane packets and outreach reviews have JT-only decisions.

**Required:**
- Interim: Approve and Reject append a feedback entry and set `status: "done"`. They record intent and authorize nothing.
- Target: either (a) admit decision cards as a new family with an `approvalState` and a JT-identity-checked decision route like outreach review, or (b) move them to lane packets. Either needs the producer to emit them differently.

## 4. Decision card marker and typed slots

**Design needs:** know a card is a decision card, and fill First action, Why it matters, Done when and Guard.

**Contract says:** the 31 cards fill only nine fields; there is no `firstAction`, `whyItMatters`, `doneState` or `exactSteps` (section 1). Structure is prose: a `First action:` line, bold-label bullets, and `Why it matters:`, `Done:`, `Guard:` lines identical on all 31. There is no `guard` field anywhere. The marker is the title pattern.

**Required:**
- Interim: regex on the title, line parse on the description (`DECISIONS.md` sections 1 and 4). Unit-test the parser against `source/02-fixtures.json` F01, F02, F03.
- Target: a one-time migration that writes `firstAction`, `whyItMatters`, `doneState` from the lines; a new `guard` string; and a `cardKind: "decision"` plus `series` and `seriesNumber`. Keep the description as the source of the bullets.

## 5. Unique curated order

**Design needs:** a stable position for every item.

**Contract says:** `sortOrder` is written by the agent by convention, "No backend or logic function reads it" (section 7.4); 36 cards sit in the 201 to 231 band; "sortOrder 220 is shared by P10 and 5 other low-priority cards"; 7 values are shared; 14 of 85 current cards have none (section 2.1).

**Required:**
- Interim: decision cards by title number, others by `sortOrder` with the tie-break in `DECISIONS.md` section 1.
- Target: a server function `curatedRun(now)` that applies the eligibility and order rules and returns the ordered ids, covered by tests; or a unique `runRank` the agent must set. Add uniqueness checking on write.

## 6. Blocker field

**Design needs:** a Blocker column in the queue and Block that records a reason.

**Contract says:** "There is no `blocked` status, flag, or blocked-by field" (section 3.1); 18 current cards mention block in prose; `blocks` means the opposite (how many others this card blocks); only `waitingOn` has structure and it requires a person (`who`).

**Required:**
- Interim: Block writes `waitingOn` (a person). The Blocker column shows `waitingOn` or the first description line of a card titled "Blocked".
- Target: an optional `blocker: { text, since }` for blockers that are not a person, with a rule for when it hides the item from the run. Until then, a blocker with no person cannot be recorded.

## 7. Urgent exception inputs

**Design needs:** "approval expires within 24 hours" and "overdue external deadline", with the reason as plain text.

**Contract says:**
- Only lane packets have `expiresAt`. Decision cards and outreach reviews do not expire (section 6.4).
- `dueDateSource === "external"` exists on 1 current card; 5 cards have a `dueDate` and no source, so they never qualify (section 2.3).
- The scorer emits reason codes such as `deadline:<date>`, but none for expiry.

**Required:**
- A server-computed `urgentReason` (`{ kind, text, at }`) on the run query, so the label text is not built in the client.
- A data rule that the agent sets `dueDateSource` whenever it sets `dueDate`; otherwise the second trigger rarely fires.
- A product decision on displacement when an exception falls outside the cut of 7 (`DECISIONS.md` section 3 rule 5).

## 8. A run query that is not the scorer

**Design needs:** a ranked list that puts decision cards first.

**Contract says:** `allocateToday` is "the only owner" of Today; all 31 decision cards score 0 and land at positions 15 to 45 in reverse order (section 7.3); lane capacity filters packets by minutes.

**Required:** a new query that uses the eligibility rules from section 7.1 step 1 and the order rules in this design, and does not call the scorer for order. Decide whether lane capacity budgets also apply (this design ignores them; no focus row exists for the current week).

## 9. Content change token

**Design needs:** know whether an item changed since the snapshot, without counting the operator's own writes.

**Contract says:** `updatedAt` is "the main tie-breaker" and "Appending bumps `updatedAt`" (section 6.6). Feedback append works on every card, so a saved answer would look like an external edit. Lane packets have `payloadHash`; generic cards have no content hash.

**Required:** a `contentRevision` (number incremented on any edit to title, description, steps, prompt, destination, done state, status, priority, `waitingOn`, but not on feedback append), or a content hash for generic cards. The snapshot compares that token.

## 10. Field-level change history

**Design needs:** "Another writer edited this item... The done condition changed", with the previous version and the new one.

**Contract says:** status, title and description changes "are not audited"; only `dollars`, `dueDate`, `waitingOn`, `stageProbability` and `priority` write audit rows (section 6.7). No previous text is stored.

**Required:** the client can keep the text it displayed and diff against the fresh read for fields it showed (interim, works only while the page is open). For the Resume summary after being away, it needs either the snapshot to include a field copy, or a `taskRevisions` table (`taskId`, `field`, `old`, `new`, `at`, `by`). Without it the Resume banner can say that an item changed and which kinds of fields differ from the snapshot copy, but cannot show history it never captured.

## 11. Persisted expiry

**Design needs:** an Expired state that is consistent between devices and the queue.

**Contract says:** expiry hides an open packet from Today "at read time"; the closure is written only by `tasks.expireDueLanePackets`, which "is not scheduled"; 0 expired packets so far (section 6.4). Approve is refused after expiry; Reject, complete, skip and no-action are not.

**Required:** the client derives Expired from `expiresAt < now` on an open packet, and must keep an expired packet in the run snapshot (Today's read will not return it). To close them for real, schedule `expireDueLanePackets`. Decide what that does to a run that holds the packet.

## 12. Read freshness and connection thresholds

**Design needs:** "Out of date", "Connection unreliable", last-checked times.

**Contract says:** the data hook refetches every 60 seconds (`03-state-map.md` A4). No server timestamp for the read and no thresholds are defined.

**Required (client-only):** record `lastGoodReadAt`, count consecutive failures, apply the thresholds in `DECISIONS.md` section 15, and use the server clock or a header to compute ages if the device clock may be wrong. Confirm the thresholds.

## 13. Safe retry for feedback

**Design needs:** Retry after a failed action must not duplicate a saved answer or note.

**Contract says:** `appendFeedback` copies the list and appends; `id` and `createdAt` are server-assigned (section 6.6). There is no idempotency key. Status writes are idempotent; lane packet transitions are bound to a hash; an identical outreach decision is a no-op.

**Required:** add an optional `clientRequestId` to `append-feedback`, stored on the entry; a repeat with the same id returns the existing entry. Without it, a retry after a timeout can append twice. Interim: after a failure, re-read and check whether an entry with the same body from the last minute exists before retrying.

## 14. Card validation

**Design needs:** reasons a card is invalid, in plain language.

**Contract says:** validation exists only for nightly-validation cards, lane packets at admission and outreach reviews (sections 5.2, 2.7). Generic cards carry no such check; Convex schema validators reject unknown enum values on write, but legacy rows can still be odd.

**Required:** a shared `validateCard(task)` returning reasons (`DECISIONS.md` section 9), used by the client and, ideally, by the run query so invalid cards are flagged before they reach the screen. Confirm the rule list.

## 15. Evidence for decision cards; local file paths

**Design needs:** evidence links on every item where they exist, and an Open evidence key.

**Contract says:** 76 of 85 current cards have none; the 31 decision cards have none (section 2.4). 13 of 26 evidence entries are local file paths (`~/...`, `/home/...`). The adapter extracts URLs from the description.

**Required:** the UI shows "Missing" where absent (done). For file paths a browser cannot open them: show a copy-path control, or provide a local-open helper. For decision cards, the producer could add `evidenceLinks`; the design does not require it.

## 16. Lane packet proof entry

**Design needs:** Complete on an external packet records evidence.

**Contract says:** completion needs "an approved current hash plus evidence of the declared type"; `post-url` must be https; ref 1 to 500 characters; `recordedBy: "jt"` (sections 5, 6.3). `doneEvidence` is 0 across all cards.

**Required:** a design for the proof form, per type (`post-url`, `message-ref`, `application-ref`, `rsvp-ref`, `profile-edit-ref`, `deploy-ref`), with inline validation and a retry-safe call to `PATCH /api/tasks/lane-packet`. Not built in the prototype.

## 17. Skip and no-action in the action set

**Design needs:** a way to dismiss an item that needs nothing.

**Contract says:** lane packets support skip and no-action (JT or producer) with a typed closure. The brief's action list (Start, Complete, Approve, Reject, Defer, Block, Previous, Next) does not include them. Generic tasks have no equivalent except Complete.

**Required:** a product decision. Options: add "Close without action" for lane packets mapped to no-action; or leave Reject as the only closing action (this design). Expired packets currently offer only Reject.

## 18. Identity on generic writes

**Design needs:** the premise that only the operator decides.

**Contract says:** generic routes have no identity check and are "localhost only" behind a private network (section 6.1). Anyone who can reach the server can mark a card done or delete it.

**Required:** put the app behind the same trusted-header proxy that lane packet decisions use and check it for every write from this interface, or add identity to generic mutations. Until then, Complete on a generic card is not an authenticated decision.

## 19. Nudge title

**Design needs:** show a nudge-due waiting card.

**Contract says:** Today rewrites the title to `Nudge <who>: <what>` in its own output (section 7.1); the record title is unchanged.

**Required:** decide which to display. This design shows the record title verbatim and a "Waiting" status with the `waitingOn` blocker text. If you want the rewritten title, the run query must return it with the rewrite flagged.

## 20. Undo after closing writes

**Design needs:** Undo on every action.

**Contract says:** a closed lane packet refuses every write except feedback; outreach decisions are one-time; generic status moves are free (sections 4.2, 4.3).

**Required:** none for generic tasks. Do not offer Undo after Reject, Approve, outreach decisions or lane packet Complete. For those, the confirm panel is the only safeguard, and it states the consequence.

## 21. Time zone

**Design needs:** a local date for the run and for rollover.

**Contract says:** the focus row uses "the first day of the current week (local time)" (section 7.1). No operator time zone setting exists. The live capture was taken at 20:07 ET.

**Required:** use the browser time zone, or store a `timeZone` setting for the operator so the run date does not change when travelling. Show timestamps with the zone (the design shows UTC; switch to the operator's zone).

## 22. Multi-writer awareness (Eve edits)

**Design needs:** "Another writer edited this item" and a count of changes while away.

**Contract says:** both the agent and the operator write; `author` on feedback is declared, not checked; the audit trail covers five fields.

**Required:** items 9 and 10. The label "Another writer" is deliberately vague because the record does not say who edited.

## 23. Sort order data quality

**Required:** before relying on `sortOrder` for operational cards, fix duplicates (7 shared values) and fill the 14 missing values, or accept the tie-break rule. See item 5.

## 24. Deadline data quality

**Required:** all 14 current `dueDate` values are past due and only 1 has `dueDateSource: "external"`. The overdue-deadline exception will fire for at most that card until the agent labels deadlines correctly (the writer policy in section 6.8 is documented but not enforced).

---

## Addendum (2026-10-03, found while building slice one)

## 25. Removing an optional field

**Design needs:** Undo after Block clears `waitingOn` (DECISIONS 6.7); Undo after Defer restores the previous `snoozedUntil`, which for most cards means no snooze at all (override 1).

**Contract says:** nothing about removal. In practice `PATCH /api/tasks` and `PATCH /api/tasks/[id]` call `tasks.update`, which declares `waitingOn` and `snoozedUntil` as `v.optional(...)`: `null` is refused by the validator and JSON cannot carry `undefined`. No route or mutation removes either field.

**Slice one (JT, 2026-10-03, no backend change):** Block offers no Undo. Defer Undo writes back the previous `snoozedUntil` when there was one; otherwise it writes the moment of Undo, which is already past, so eligibility is identical but the record keeps a past timestamp.

**Required for exact Undo:** a narrow unset option on `tasks.update` (for example `unset: ["waitingOn", "snoozedUntil"]`) that passes through the same outreach and lane-packet guards and writes the `waitingOn` audit row. No schema change.
