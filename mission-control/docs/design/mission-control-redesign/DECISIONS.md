# Decisions

Every question asked in this project, the option chosen, and the rule to implement. Read with `state-map/03-state-map.md` (governing) and `source/01-data-contract.md` (what the backend enforces).

Labels used below:

- **Answered**: you chose this in a question form or stated it in the brief.
- **Designed**: you did not answer; the design had to decide to build the screen. Marked **Confirm**.
- **Not decided**: no answer exists. The rule gives an interim behavior and the target.

Terms: "item" is a task record. "Run" is today's committed list. `jt` is the operator, `eve` is the agent.

---

## 0. Overrides (Confirmed 2026-10-03)

These override the rules below wherever they conflict. **Confirmed 2026-10-03.**

1. **Defer is a snooze, not a priority change.** Confirmed 2026-10-03. It asks each time: tomorrow at 8am local, pre-selected so Enter accepts it; next week; or a date. It writes `snoozedUntil`. On a lane packet it may not pass `expiresAt`. It is hidden on outreach reviews and closed packets. Undo restores the previous value. This replaces section 7 and the Defer confirm and status-line copy in the README that mention priority.
2. **Run progress uses the interim browser-storage rule in section 8 for slice one.** Confirmed 2026-10-03. No database change.
3. **Every other item marked Confirm is accepted as designed.** Confirmed 2026-10-03. That covers: section 1 rule 6 (Other cards tie-break), section 3 rule 5 (exception displacement), section 4 rule 7 (Guard fills Authority on P and AP; Q shows none), section 5 rule 2 (the P decision note is optional), section 6 rule 2 (Block also sets `status: "waiting-external"`), section 9 (invalid card rules), and section 15 (other designed rules).

---

## 1. What fills the run, and in what order

**Question:** What fills today's run? **Answered:** "Decision cards (Q, P, AP) in curated order, then operational cards."

**Question:** Where does curated order come from? **Answered:** "Title code: Q1 to Q10, P1 to P12, AP1 to AP9; operational cards by sortOrder."

**Rules**

1. **Eligibility.** An item can enter a run only if it passes the Today exclusions in `01-data-contract.md` section 7.1 step 1, read at run start:
   - not an agent definition or proof entry;
   - status is not `done`, `archived` or `snoozed`;
   - an open lane packet is not at or past `expiresAt`;
   - `snoozedUntil` is not in the future;
   - owner is `jt` (owner `eve` is excluded);
   - a card with `waitingOn.who` is excluded until `now - since > nudgeAfterDays` days. A `waiting-external` status alone does not exclude it;
   - an outreach review card that already has an `outreachDecision` is excluded.
2. **Do not use `allocateToday` or its score to build the run.** It scores all 31 decision cards 0 and orders them AP9 to Q1. Use eligibility only, then the order below.
3. **Group order:** decision cards Q, then P, then AP, then every other eligible item ("Other cards").
4. **Decision card detection.** A decision card is a generic task whose title matches `^(?:.*?\s)?(AP|Q|P)(\d{1,3}):` (case-sensitive). Titles start with the program name, then the code, then a colon. The card has no marker field (see `GAPS.md` item 4).
5. **Within Q, P and AP:** ascending by the number in the code (Q1, Q2, ... Q10; P1 ... P12; AP1 ... AP9). Compare numbers, never strings.
6. **Other cards:** ascending by `sortOrder`. Items with no `sortOrder` come after all that have one. Ties and missing values: `createdAt` ascending, then title A to Z. **Designed, Confirm** (the tie-break is not specified; 7 `sortOrder` values are shared by several cards).
7. **Do not read `priority` or `rankScore` for order.**
8. **Cut** to the run size (rule 2 of section 2) after exceptions are applied (section 3).
9. **The run is committed at start.** Items added later never join it (they appear under "Added to the backlog" in the change summary). Items that become ineligible stay in the run until handled; an expired or invalid one shows its own state (README, States).
10. **Queue screen** lists everything, including items outside the run, grouped Q, P, AP, Other cards, with a divider "Not in today's run" for the backlog part of Other cards. Order inside each group follows rules 5 and 6.

## 2. Run size

**Question:** Run size. **Answered:** "7, same as the Today cut."

**Rules**

1. Run size is **7 items**, fixed. Position reads "n of 7". Do not size by minutes or priority.
2. A run with fewer than 7 eligible items has size equal to the eligible count. A run with 0 shows the Empty run screen.
3. Position denominator never changes during the run, even when an item is deferred or parked.
4. Note: the structural wireframes used "of 12" because the brief's example and the fixture count were twelve. The build uses 7 as answered.

## 3. What may jump ahead as an urgent exception

**Question:** What may jump ahead as a labeled urgent exception? **Answered (selected):** "Approval that expires within 24 hours" and "Overdue external deadline."
**Answered (not selected):** "Waiting card with an overdue nudge" and "Nothing automatic; I promote by hand."

**Rules**

1. Exactly two triggers, evaluated at run start and on every background read:
   - **Approval expires within 24 hours:** a lane packet that is open, `approvalState` is `pending`, and `0 < expiresAt - now <= 24 h`.
   - **Overdue external deadline:** `dueDate < now` and `dueDateSource === 'external'`. A self-set deadline never qualifies. A `dueDate` with no `dueDateSource` never qualifies (the scorer ignores it too).
2. **A waiting card whose nudge is overdue does not jump.** It keeps its curated place (in the prototype fixture F07 is position 4, not 1). This differs from the Today scorer, which ranks it first.
3. There is **no manual promotion**. No control moves an item ahead.
4. Exceptions take the next positions after the item currently open, never before it, and never interrupt an open item. Several exceptions order by earliest `expiresAt` or `dueDate`. At run start they take positions 1 onward.
5. An exception that is outside the cut of 7 displaces the last curated, unhandled item, which returns to the backlog. The run stays 7. **Designed, Confirm.**
6. Every exception carries a label shown in the item eyebrow and on its queue row, stating why it jumped. Header order name stays "Curated order". Text:
   - "Moved up: approval expires in 5 hours (Oct 3, 04:00 UTC)"
   - "Moved up: external deadline passed Sep 21 (12 days overdue)"
7. If an exception appears mid-run, show it through the changed-while-away or changed-underneath banner. Never reorder under an open item.
8. At run start with none: the Run start screen says "Urgent exceptions: None. No approval expires within 24 hours and no external deadline is overdue."

## 4. How slots are filled from description lines

**Question:** Decision cards keep First action, Why it matters, Done and Guard as lines in the description. How do they fill the slots? **Answered:** "Lift those lines verbatim into the slots, labeled 'from description'."

**Rules**

1. A typed field wins. Use `firstAction`, `whyItMatters`, `doneState` when present.
2. When the typed field is absent and the item is a decision card, lift from the description. Match whole lines that start exactly with `First action:`, `Why it matters:`, `Done:` or `Guard:`.
3. The slot value is the text after the label on that line, minus the single space after the colon. Do not trim trailing characters (the dots are data), do not rewrite, do not summarize.
4. Lifted slots carry a chip "From description" (README, First action).
5. If no line matches: the slot shows "Missing". Never fall back to another line.
6. Slot mapping: `First action:` fills First action; `Why it matters:` fills Why it matters; `Done:` fills Done when.
7. `Guard:` fills the Authority block on **P and AP** cards as the authority boundary, verbatim. Q cards show no Authority block. **Designed, Confirm.**
8. The rest of the description must still render, because the decision lives in it. Below the slots, render the description with the four lifted lines removed. Supported formatting: paragraphs, `## ` headings, `- ` bullets, ordered sub-lists, and `**Label:**` rendered as a bold label. Preserve order and line breaks. No other Markdown features. The prompt block is never rendered as Markdown.
9. On Q and AP cards the empty `- **Answer:**` bullet is replaced by the answer box (section 5). The description text itself is never modified.

## 5. How answers and approvals are recorded

**Question:** The 31 cards have no approval or answer field. 19 end with an empty Answer; P cards ask approve or decline. How do I record my decision? **Answered:** "Answer required before Complete on Q and AP; P gets an Approve/Decline note."

**Rules**

1. **Q (10 cards) and AP (9 cards):**
   - Show an answer box (textarea, label "Your answer") in the decision pane where the empty Answer bullet sits.
   - **Complete is not available until an answer is saved.** Until then the primary action is "Save answer".
   - Valid answer: 1 to 4,000 characters after trimming (the feedback limit). Validate inline, keep the text on error.
   - Saving appends a feedback entry: `PATCH /api/tasks { action: "append-feedback", id, body: "Answer: <text>", author: "jt" }`. Then Complete writes `status: "done"`.
   - The saved answer shows in Feedback history.
   - Until a typed answer field exists, feedback is the only append-only channel (`01-data-contract.md` section 1, "The answer gap"). Do not edit the description to store the answer.
2. **P (12 cards):** no Answer slot. Buttons **Approve** and **Reject** (the action names from the brief; your option text said "Decline"). Each opens a confirm panel with an optional note field. Confirming appends one feedback entry `Decision: Approved. <note>` or `Decision: Rejected. <note>` (author `jt`), then writes `status: "done"`. The note is optional. **Designed, Confirm** (optional vs required).
3. **Generic tasks have no approval concept and no identity check** (`01-data-contract.md` section 5). Approve and Reject on a P card record intent only; they authorize nothing downstream (`GAPS.md` item 3).
4. **Lane packet:**
   - Approve and Reject call `PATCH /api/tasks/lane-packet` with the **current** `payloadHash`, JT identity required.
   - Approve is refused after `expiresAt`. Reject is allowed after expiry.
   - A content edit resets approval to pending. Show "Edited after it was added" when `payloadHash !== admittedPayloadHash`. On a 409 "payload changed since review", show the Changed underneath me state and re-read.
   - Approve counts as **handled** in the run (outcome "approved") and the item moves to "Still needs you" in the summary until proof is recorded.
   - Complete: internal packets (`doneEvidenceType: "none"`) need no proof. External packets need an approved current hash plus evidence of the declared type: `post-url` must be an https URL, other types a reference of 1 to 500 characters. The evidence entry form is not built (README, Not built).
5. **Outreach review card:** Approve or Reject once, through the decision route with JT identity. Show subject, body and verifier report in full. A repeat of the same decision is a no-op; a different decision is refused. No other action renders.
6. **Approve and Reject have no single-key shortcut** (section 12). Both open a confirm panel.
   - Approve confirm: title "Approve this version?", body "Approval applies to the current content only. If the item is edited, approval returns to pending." Confirm button is primary.
   - Reject confirm: title "Reject this item?", body "It closes for good and leaves today's run. This cannot be undone." Confirm button is `ink`.
7. **Permitted actions** (only these render; everything else is hidden, not disabled):

| Family and status | Actions |
|---|---|
| Generic task, open, not started | Start, Complete, Defer, Block, Previous, Next |
| Generic task, in progress | Complete, Defer, Block, Previous, Next |
| Decision card Q or AP | Save answer, then Complete; Defer; Block; Previous; Next |
| Decision card P | Approve, Reject; Defer; Block; Previous; Next |
| Lane packet, open, not expired | Approve, Reject, Defer, Block, Start, Previous, Next. Complete only when internal, or after approval and proof |
| Lane packet, open, expired | Reject, Previous, Next |
| Lane packet, closed | Previous, Next |
| Outreach review, pending | Approve, Reject, Previous, Next |
| Outreach review, decided | Previous, Next |
| Any item in a paused state (stale, changed, invalid, loading, failed) | Previous, Next only |

   "Skip" and "no action" exist in the backend for lane packets but are not in the permitted action list from the brief, so the design omits them (`GAPS.md` item 17).

## 6. What Block writes

**Question:** No blocked status exists. What should Block do? **Answered:** "Park it on a person: who, what, nudge after N days; hidden until the nudge."

**Rules**

1. Block opens the "Park this item on a person" form: Who (required text), What (required text), Nudge after (days, whole number 1 to 365, default 14).
2. Confirming writes one update: `waitingOn: { who, what, since: <now ms>, nudgeAfterDays: N }`. Also set `status: "waiting-external"` so the Work list agrees. **Designed, Confirm** (status write).
3. Pass an evidence string with the update, because `waitingOn` changes write a change-audit row: for example "Parked from Mission Control run". Source is `jt`.
4. The item leaves today's run. Run outcome: "parked". It returns to eligibility when `now - since > nudgeAfterDays` days. The scorer then titles it "Nudge <who>: <what>" in its own output; the record title is unchanged. Display the record title verbatim.
5. Block is hidden for outreach review cards and closed lane packets (they refuse edits).
6. Summary shows: "Parked on {who}. Nudge due {date}."
7. Undo clears `waitingOn` and restores the previous status. Offer Undo only for generic tasks and open lane packets.
8. There is no free-text "blocked" status and no blocker without a person. A blocker with no person is not supported (`GAPS.md` item 6).

## 7. What Defer writes

**Superseded by section 0, override 1 (Confirmed 2026-10-03): Defer is a snooze that writes `snoozedUntil`, not a priority change. The rules below are kept for the record only.**

**Not asked directly; follows the contract convention. Designed, Confirm.**

**Rules**

1. Defer writes `{ priority: "low", status: "todo" }` (`01-data-contract.md` section 5.1). Pass an evidence string, because a priority change writes an audit row.
2. Defer opens a confirm panel: "Defer this item?" / "Its priority is set to low and it moves to the end of today's run."
3. Run effect (client): the item moves to the end of the run's unhandled list and counts as handled-for-now. Position denominators do not change. When it comes up again, a second Defer removes it from today's run and the summary counts it as "deferred". **Designed, Confirm** (the prototype's summary shows 0 deferred and does not model the second case).
4. Lane packets: Defer is allowed but a snooze may not pass `expiresAt`. Use priority only. Outreach review and closed packets: Defer is hidden.
5. Undo restores the previous `priority` and `status`. Generic tasks and open lane packets only.

## 8. Where run progress is stored

**Slice one: interim rule below, per section 0, override 2 (Confirmed 2026-10-03). No database change.**

**Not decided.** No question was answered. `03-state-map.md` Part B open question 4 stays open: "client-only, or a new backend table".

**Interim rule (no schema change):** keep the run in browser storage on this device, keyed by local date `YYYY-MM-DD` (time zone: the operator's browser zone). Store the `RunRecord` from `reference/view-model.ts`: ordered item ids, per-item state and outcome, cursor, snapshot, phase. Never clear storage entries you did not write. Clear nothing on date rollover; write a new key and keep the previous one for the summary.

**Target rule (needs your approval; schema change is separately gated):** a Convex table for the run and its items, written by mutations, so progress survives a cleared browser and works across devices. See `GAPS.md` item 1.

Either way the transition rules are the Part B table of `03-state-map.md`, including: snapshot at start; "Queue changed while away" when a fresh read differs materially; acknowledge re-bases the snapshot; date rollover closes the run as unfinished and summarizes it.

## 9. What counts as an invalid card

**Not asked; the design needed it for the Invalid card state. Designed, Confirm.**

A card is invalid, and no write action renders for it, when any of these holds:

1. `title` is missing or empty after trimming.
2. `status` is not one of `todo`, `in-progress`, `waiting-external`, `snoozed`, `done`, `archived`.
3. `assignee` is not `jt`, `eve` or `both`, or `priority` is not `high`, `medium` or `low`.
4. Lane packet (`packetSchema === "lane-packet-v1"`) with a missing `payloadHash`, `expiresAt` or `doneEvidenceType`.
5. Outreach review (`outreachReview` present) with a missing `candidateId`, `draftSha256` or `snapshotSha256`, or a `decision` that is not approve or reject.

Behavior: show the Invalid card state with one plain sentence per failed check ("No title is recorded." "Its status is not one this app recognizes." "Its approval details are incomplete."), "Source:" with the `sourceSystem` or "Missing", and "Check again". Previous and Next work. Prompt copy is disabled. The card still counts as a run position; it is handled only when fixed or skipped by moving on, and then appears under "Still needs you" in the summary.

## 10. Ordering display

**Answered (brief):** "One order at a time. Curated order is the default. An urgent item may move ahead only as a labeled exception that says why it jumped. The header always names the active order."

**Rules:** one active order, named "Curated order" in the header, at the top of the queue, on Run start and on Resume. No sort control exists. An exception carries its own label (section 3).

## 11. Daily run and change handling

**Answered (brief):** "Today's committed run is separate from the backlog and sized by item count. Position reads like '4 of 12'. If the queue changes while I am away, show the change before moving me anywhere."

**Rules**

1. Position format "n of 7".
2. On load, focus or visibility return, compare a fresh read with the snapshot. Material change = any of: a card entered or left scope, `updatedAt` or `payloadHash` changed, status or approval changed, a card passed `expiresAt`, rank order of unhandled cards changed (Part B definition).
3. If material: show Run resume with the change banner, **before** any item. The operator acknowledges to continue. Nothing moves them.
4. While an item is open and a background read (every 60 s) shows that item changed: show Changed underneath me (README, States). Actions stay paused until acknowledged.
5. A refused write (409, closed, expired) does not advance. It shows the Failed action state or Changed underneath me, depending on the response.
6. If a different unhandled item changed while working, show a slim notice at the next item boundary. **Not built.**
7. Do not use `updatedAt` alone to detect a change on cards that receive feedback appends: your own answer would flag itself (`GAPS.md` item 9).

## 12. Keyboard scheme

**Answered (brief and later message):** desktop shortcuts for next, previous, complete, defer, open evidence, queue, with a discoverable help overlay. **Approve and Reject get no single-key shortcut; they need a click or a confirming second key.**

**Rules:** the full map is in `KEYBOARD.md`. Summary: `J` next, `K` previous, `C` complete (opens confirm), `D` defer (opens confirm), `E` open evidence, `Q` queue, `?` overlay, `Esc` cancel or close, `Enter` confirm. Approve and Reject: click, then confirm with a click or `Enter`; or Tab to the button, `Enter` to open the confirm panel, `Enter` to confirm. No letter, chord or Shift combination opens or confirms either. Start and Block have no key.

## 13. Layout and visual direction

**Answered (variations):** "Two to compare" for the current-item screen, differing on "Layout: single reading column vs. two panes (decision left, context right)". The comparison was built as three wireframes (A column with queue sheet, B two panes with queue rail, C position strip with tabs). **You chose the B architecture** ("Using that architecture") after the recommendation.

**Rules:** desktop = queue rail + decision pane + context pane. Mobile = single column, actions at the bottom (tweak: top), queue as a bottom sheet. Queue as a full view on desktop is opened on demand and never replaces the item between items.

**Answered (visual system):** Light. Type: Hanken Grotesk + JetBrains Mono. Density: Compact on desktop. Tone and accent were left to the designer; the design drew **warm** neutrals and a **green** accent (`oklch(0.50 0.12 150)`) by random selection from small sets. Change them only through `tokens/`. No design system and no `design-core.md` were attached; no code source was connected, so the design was made blind to the existing UI.

## 14. Rules inherited from the brief (answered)

- Render every field verbatim from the record. A missing field shows as missing and is never invented.
- No developer vocabulary anywhere on screen.
- Only actions the data contract permits for that item's type and status appear: Start, Complete, Approve, Reject, Defer, Block, Previous, Next.
- No marketing hero, gradients, glow, glass, neon, charts or metrics above the current item, kanban, streaks, badges, confetti or celebratory gamification. No Inter, no Roboto.
- Desktop is primary for depth. Mobile at 390 x 844 is excellent for the one-item flow: actions in thumb reach, queue as a sheet.
- States are designed: loading, empty run, stale data, degraded connection, failed action with retry, changed underneath me, invalid card (plus expired).
- Screens: Current item, Queue, Run start and resume (including what changed), Run summary.

## 15. Other designed rules to confirm

| Rule | Value in the design |
|---|---|
| Stale | Last good read older than 5 minutes (five missed 60 s polls). Banner, actions paused, "Refresh now" |
| Degraded | Two consecutive failed or slow reads (over 10 s). Banner, auto retry every 8 s with backoff, "Retry now". Actions stay available; a failed write shows the failure panel |
| Failed action | Same request retried; the position never advances on failure |
| Undo | Offered after Start, Complete, Defer, Block on generic tasks and open lane packets. **Never** after Reject, Approve, outreach decisions or lane packet Complete (the backend refuses writes on closed packets and decided reviews) |
| Handled items | Previous and Next may open handled items read-only with their status line and, where allowed, Undo |
| Summary outcomes | completed, approved, rejected, parked, deferred. "Still needs you" lists approved-awaiting-proof, parked (with nudge date), deferred and invalid items |
| Age | Time since `createdAt`; hours under 48 h, days otherwise |
| Blocker column | `waitingOn` as "Waiting on {who}: {what}"; else the first line of the description when the title begins "Blocked"; else "None recorded" |
| Date | Local date of the browser; rollover closes the prior run as unfinished and shows its summary |
