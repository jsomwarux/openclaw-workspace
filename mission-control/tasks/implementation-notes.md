# Mission Control redesign: slice one implementation notes

Status: built and verified locally; fresh-context review in section 9
Date: 2026-10-03
Branch: `claude/mc-redesign-slice-1` (worktree `~/.config/superpowers/worktrees/openclaw-workspace/mc-redesign-slice-1`, cut from `origin/master` at `e5b9943`)
Spec: `docs/design/mission-control-redesign/` (bundle, committed unchanged in `a86d2b7`; overrides recorded in `ea1e8e3`)

**Nothing in this branch is merged or deployed.** No database schema change, no new service, no package installed, no write to the production database. Every test, screenshot and browser check ran against an in-memory fixture backend.

Top three notes:
1. The backend cannot remove `waitingOn` or `snoozedUntil`, so Block has no Undo and Defer Undo writes "now" when there was no earlier snooze (your Phase 0 answer). GAPS item 25 says what an exact Undo needs.
2. Lane packets and outreach reviews are read-only in slice one, so a run that contains one ends with it under "Still needs you" until slice two (or until it is decided in the Work list, which the cockpit then picks up).
3. The P-card Approve confirm copy differs from DECISIONS 5.6, because that copy describes lane-packet hash binding and would be false on a generic card (X4).

---

## 1. Phase 0 findings (read-only, before any code)

Read: the whole bundle (README, DECISIONS, KEYBOARD, GAPS, state map, view model, tokens, prototype HTML and logic, data contract, fixtures, UX guide), `mission-control/CLAUDE.md`, the workspace `AGENTS.md`, `docs/agents/workflow-protocols.md`, and the Mission Control entries in `docs/agents/mistakes-log-recent.md` and `docs/agents/regression-checks.md`. No file named `lessons.md` exists in this repository; those two logs are its lessons files.

Interface code was read only for routing, data fetching and API wiring: `app/layout.tsx`, `components/Sidebar.tsx`, `lib/mission-control/hooks.ts`, `lib/mission-control/routes.ts`, `lib/mission-control/nav-layout.ts`, `app/api/tasks/route.ts`, `lib/mission-control/task-admission.ts`, `lib/mission-control/task-feedback.ts`, `lib/mission-control/work-actions.ts`, `lib/mission-control/adapters.ts` (evidence extraction only), `convex/tasks.ts` (`update`, `appendFeedback`, `listActive`), `convex/schema.ts` (`waitingOn`). No layout, component or styling was copied.

### Backend checked against DECISIONS.md and 01-data-contract.md

| Claim in the bundle | Backend today | Effect on slice one |
|---|---|---|
| `GET /api/tasks` returns all non-archived tasks | True (`tasks.listActive`, `{ tasks }`) | None |
| `PATCH /api/tasks {action:"append-feedback", id, body, author}` appends, body trimmed, 1 to 4,000 characters, append-only | True | None |
| Generic status any to any through `PATCH /api/tasks` | True | None |
| Block writes `waitingOn` and `status`, with an evidence string | True. The evidence and source fields are named `auditEvidence` and `auditSource` on the route | Field names only |
| Defer (override) writes `snoozedUntil` | True (`v.optional(v.number())`) | None |
| Undo after Block clears `waitingOn` (DECISIONS 6.7) | **Not possible.** `tasks.update` declares `waitingOn` and `snoozedUntil` as `v.optional(...)`; `null` is refused and JSON cannot carry `undefined`. No other route or mutation unsets a field | **Asked and answered** (below) |
| Undo after Defer restores the previous `snoozedUntil` (override 1) | Exact only when a previous value existed. All 31 decision cards have none | **Asked and answered** (below) |
| No URL opens one task in the current interface | True: `/work` and `/` open the drawer from click state only | **Asked and answered** (below) |
| A new route can sit alongside the current interface | The root layout renders the old Sidebar (desktop rail, mobile top bar and bottom nav) on every route; no App Router route can opt out without an edit | **Asked and answered** (below) |
| Lane packet and outreach writes are JT-identity routes | True; not exercised in slice one (read-only) | None |
| No ESLint configuration | True: `next lint` has no config and would start an interactive setup | Lint reported as not configured |

### Questions asked and answers (2026-10-03)

1. **Undo gap.** Answer: *No backend change.* Block has no Undo in slice one; its confirm form is the safeguard. Defer Undo writes back the previous `snoozedUntil` when one existed; when there was none it writes the moment of Undo, which is already past, so eligibility is exactly as before. Logged here and in the GAPS addendum.
2. **Old chrome.** Answer: *One-line Sidebar guard.* `components/Sidebar.tsx` renders nothing on `/cockpit`; every other route is unchanged, pinned by a test.
3. **Deep link.** Answer: *Link to /work and name the item.* Lane packets and outreach reviews link to the Work list in a new tab and say which title to open. No change to the current interface.

---

## 2. Plan (test first)

New route: **`/cockpit`** (no collision: no `app/cockpit`, no redirect, no middleware). Logic in `lib/cockpit/`, UI in `components/cockpit/`, route in `app/cockpit/`.

Every step below starts with a failing test, then the minimum code to pass it.

1. **Tokens wired by name.** `tailwind.config.ts` spreads the bundle's `tokens/tailwind.config.ts` extension (colors `mc-*`, font sizes `mc-*`, radii, widths). The bundle's `fontFamily.sans/mono` would restyle the current interface, so they are mapped to new keys `mc-sans` and `mc-mono` (same values, read from the bundle object). `app/cockpit/layout.tsx` imports `tokens/tokens.css` directly from the bundle. Test: the config exposes every bundle color and size key by reference and leaves `fontFamily.mono` and `content` unchanged.
2. **Classification and eligibility** (`classify.ts`, `eligibility.ts`): family (lane packet, outreach review, decision card by `^(?:.*?\s)?(AP|Q|P)(\d{1,3}):`, generic), the seven exclusions of DECISIONS 1.1. Tests against fixtures F01 to F12 plus edge records.
3. **Curated order and tie-break** (`order.ts`): Q, P, AP by number, then other cards by `sortOrder`, missing last, ties by `createdAt` then title A to Z, then id. Tests include numeric (not string) code comparison and shared `sortOrder`.
4. **Urgent exceptions** (`exceptions.ts`): the two triggers, labels, run start placement, mid-run placement after the open item with displacement, and the waiting-nudge non-trigger.
5. **Slot lifting and remaining description** (`slots.ts`, `description.ts`): typed field wins; decision cards lift `First action:`, `Why it matters:`, `Done:`, `Guard:` verbatim; Guard feeds Authority on P and AP only; remaining description parsed into paragraphs, `## ` headings, `- ` bullets, ordered sub-lists and `**Label:**`.
6. **Validity** (`validity.ts`): DECISIONS 9 reasons in plain language.
7. **Action matrix** (`actions.ts`): DECISIONS 5.7 with override 1, every row, plus the slice-one read-only rule for lane packets and outreach reviews.
8. **Answer before Complete** (`answer.ts`): Q and AP show Save answer until an `Answer:` feedback entry by `jt` exists; validation; body building for answers and P decision notes.
9. **Defer limits** (`defer.ts`): tomorrow 8:00 local (default), next week, a date; future only; never past a lane packet's `expiresAt`; hidden on outreach reviews and closed packets; Undo value.
10. **Run state machine** (`run.ts`, `changes.ts`): every transition of 03-state-map Part B (1 to 11), snapshot with a content fingerprint, own writes folded into the snapshot, change summary text, acknowledge re-base, completion, same-day reopen, date rollover.
11. **Keyboard** (`keyboard.ts`): KEYBOARD.md, including the rule that no key, chord or Shift combination opens or confirms Approve or Reject.
12. **Write plans and retry** (`writes.ts`): each action as ordered steps; retry resumes at the failed step; a retried feedback step first re-reads and skips a duplicate.
13. **Controller** (`controller.ts`): framework-free store driving reads, polling state, the run, writes, failures and undo; tested end to end against an in-memory fixture backend (no network, no Convex).
14. **UI** (`components/cockpit/*`): every screen and state in README at desktop and below 760 px; SSR render tests for structure and copy.
15. **Fixture harness** for development and screenshots: active only when `NEXT_PUBLIC_COCKPIT_FIXTURES=1` and the URL carries `?fixture=<scenario>`. It never touches `/api/tasks`.
16. **Verification**: full `bun test`, `tsc --noEmit --incremental false`, isolated `.next-build` build, `git diff --check`, screenshots at 1440x900 and 390x844 compared with the prototype, then a fresh-context review.

---

## 3. Design decisions (where the spec was silent or ambiguous)

**Wiring**
- D1. Route is `/cockpit`. Logic in `lib/cockpit/`, UI in `components/cockpit/`, route files in `app/cockpit/`.
- D2. Old chrome: `hidesLegacyChrome(path)` in `lib/mission-control/nav-layout.ts`; `components/Sidebar.tsx` returns nothing when it is true (Phase 0 answer 2). A render test pins the Sidebar markup for `/work` and checks every existing page path.
- D3. Tokens by reference: `tailwind.config.ts` spreads the bundle's `tokens/tailwind.config.ts` (colors `mc-*`, font sizes `mc-*`, radii, widths). The bundle's `fontFamily.sans/mono` would restyle the current interface, so they are exposed as `mc-sans`/`mc-mono` with the bundle's own values. `app/cockpit/layout.tsx` imports the bundle's `tokens/tokens.css` directly. A test fails if any cockpit file contains a hex, `rgb()` or `oklch()` value.

**Eligibility and order**
- D4. Owner: DECISIONS 1.1 says "owner is jt (owner eve is excluded)" and points at contract 7.1, which excludes only `eve`. `both` is therefore eligible (0 live cards use it).
- D5. Ties after `createdAt`: title compared with `localeCompare(…, "en")`, then the database id, so the order is total. Decision cards with the same number in one series fall back to the id.
- D6. A card that meets both urgent triggers carries the deadline label (its time is earlier, matching the ordering rule). An external deadline less than an hour overdue reads "less than an hour overdue".
- D7. Mid-run exceptions: only cards that existed when the run started (`startIds`) can join as exceptions. Cards created later never join a committed run (rule 1.9), even if urgent; they are reported as "Added to the backlog". A joining exception displaces the last unhandled curated item after the open one; if none can be displaced, the exception stays in the backlog.

**Slots and description**
- D8. Only lines that actually fill a shown slot leave the description. A Q card's `Guard:` line is not lifted (Q shows no Authority block), so it stays visible in the description rather than disappearing. A typed field also leaves its description line in place.
- D9. A labelled line with nothing after the label (for example `Done:`) counts as Missing and stays in the description. The first matching line wins. A trailing `\r` is treated as a line ending.
- D10. Description blocks: a blank line ends a block; a non-bullet line right after a bullet starts a paragraph; indented `1.` lines under a bullet become its ordered sub-list; other `1.` lines form an ordered list. Only `**Label:**` becomes bold; all other Markdown stays literal text.

**Actions**
- D11. Invalid card reasons: owner and priority get separate sentences ("Its owner is not one this app recognizes." / "Its priority …"); outreach snapshot or decision problems read "Its review details are incomplete."
- D12. A generic card in `waiting-external` or `snoozed` acts like "not started" (Start, Complete, Defer, Block). Lane packets (matrix only; read-only in slice one): Approve is hidden once the current hash is approved; Complete shows when internal or approved for the current hash; Start only when not started.
- D13. Defer "next week" is Monday 8:00 local of next week; on a Sunday that would equal tomorrow, so it is the Monday after. "A date" snoozes until 8:00 local that day and must be after today. On a lane packet, options past `expiresAt` show "Not available: this item expires …"; Defer is hidden when even tomorrow 8:00 is past expiry.
- D14. Defer writes `snoozedUntil` with `auditSource: "jt"` and `auditEvidence: "Deferred from Mission Control run"`. `snoozedUntil` is not an audited field, so no audit row is written; the evidence string is harmless and consistent with Block.
- D15. Run effect of Defer (follows from override 1): the item is handled with outcome "deferred", leaves today's run, and appears under "Still needs you" with its snooze time.
- D16. Block has no Undo (Phase 0 answer 1). Undo is offered after Start, Complete and Defer on generic and decision cards only.

**Run state machine**
- D17. Change detection compares a fingerprint of the tracked fields (title, description, status, owner, priority, sortOrder, the seven-field content, evidence, waitingOn, snooze, deadline, packet hash, approval, expiry, proof type, outreach decision). `updatedAt` and feedback are not compared (DECISIONS 11.7, GAPS 9). The operator's own successful writes are folded into the snapshot. Consequence: a feedback entry Eve appends is not reported as a change.
- D18. Transition 2: after a successful write the item stays on screen with its status line, and J moves on (README status lines "Press J for the next item", mobile "Next item →"). The state map's "cursor moves" is read as "moves on Next".
- D19. Next on the last position: if every item is resolved, the summary opens; otherwise the cursor goes to the first unresolved item with "Item n of N still needs you." Moving past an item that cannot be acted on (invalid, expired, or read-only in slice one) marks it left unhandled; it is listed under "Still needs you".
- D20. Items closed by someone else (done, decided, rejected, deleted) count as handled or removed once the change summary is acknowledged, marked "elsewhere".
- D21. Transition 9: a complete, unclosed run that sees a new eligible card shows the change summary; acknowledging appends the new cards (curated order, up to 7) and the denominator grows. A closed run never reopens. (Open question Q2.)
- D22. Transition 10: on load, an earlier day's run that was never closed is closed (`unfinished` when anything was unresolved) and its summary shows first; "Continue" leads to today's start. Nothing is deleted from storage.
- D23. Transition 3: Pause run, a hidden tab and a closed page all pause. Returning to a visible tab with nothing changed goes straight back to the item (transition 4); reloading the page always shows Resume (README). The inactivity timeout is not built because its length is undecided (Q3).
- D24. Writes are retried from the failed step. A retried feedback step first re-reads the card and skips the append if a jt entry with the same body exists from within a minute of the first attempt (GAPS 13 interim). A first attempt never skips.
- D25. After a confirmed write the local copy of the task is updated (and a provisional feedback entry added) until the next read replaces it, so the operator's own write never shows as "changed underneath".

**Screens**
- D26. The remaining description renders in the decision pane under the slots and Authority, with a "Description" label, and the answer box sits where the empty `- **Answer:**` bullet is. If a Q or AP card has no such bullet, the box follows the description. Save answer is the primary button in the action row.
- D27. After an answer is saved the box shows it read-only ("Your answer · Saved"); the cockpit does not offer a second answer, because feedback is append-only.
- D28. Missing Why it matters, Done when and Exact steps show the Missing chip with a short sentence ("Not recorded for this item.", "No steps are recorded for this item."). The Freshness grid's Description row reads "Recorded. Shown with the item." when a description exists.
- D29. Failure panel copy: network and server errors use the designed sentence; a refused (4xx) write says "Nothing was changed. Mission Control refused the change. Check the item, then try again."; a P decision whose note saved but whose Done failed says "Your note was saved, but the item was not marked done. Retry finishes the change." ("Nothing was changed" would be false there.)
- D30. While a write is in flight the action buttons stay rendered but disabled, so nothing jumps.
- D31. Read-only lane packets and outreach reviews show a notice, an "Open the Work list" link (new tab) and the title to open there (Phase 0 answer 3). The expired panel keeps its designed copy.
- D32. Rail statuses: Handled, the live status for the current item and for items passed without handling, Up next, and "Moved up" for an unhandled exception ahead. The exception label also shows under the eyebrow and inside the queue row.
- D33. The queue before a run starts shows the planned run in the run positions. Opening a row outside the run shows "This item is not in today's run. Open it from the Work list in the current interface." (the prototype showed a placeholder).
- D34. Same-day reopen (transition 9) shows the change banner on the summary ("New since the run finished") with "Acknowledge and continue". An earlier day's unfinished run shows "Run summary · <date> · Unfinished" and "Continue to today".
- D35. Loading shows the static skeleton with "Checking…", no run position and no Pause or Queue. If the first read fails, a line says "Mission Control did not answer. Retrying automatically."
- D36. Focus rings use `:focus-visible`, so a mouse click does not leave a ring. Confirm panels move focus to the confirm button; Esc returns focus to the action button that opened the panel; the shortcuts overlay traps Tab and restores focus.
- D37. Local file paths in evidence get a "Copy path" control (README Evidence, GAPS 15). E opens the first web link.
- D38. Spacing utilities (`p-d20`, `gap-d16`, …) come from the README's 4 px scale multiplied by the density token `--mc-d` (`lib/cockpit/density.ts`). The cockpit uses its own class merger (`components/cockpit/cx.ts`) because the shared `cn()` drops `text-mc-11` next to a text color. That bug was caught in the first screenshot.
- D39. `next/font` loads Hanken Grotesk and JetBrains Mono. The cockpit layout also declares `--font-hanken` and `--font-jetbrains` on `:root`, because `tokens.css` resolves `--mc-font-sans/mono` there.
- D40. Fixture mode needs all three: a non-production build, `NEXT_PUBLIC_COCKPIT_FIXTURES=1`, and `?fixture=<scenario>`. Production builds drop the branch and the chunk (verified: 0 files in `.next-build/static` contain fixture code).
- D41. Tuning controls (README "Tweaks") ship as defaults through `tokens.css`; there is no settings screen.

**Added after the fresh-context review (section 9)**
- D42. The confirm buttons for Approve, Reject, Complete and Defer ignore auto-repeated Enter or Space keydowns, and ignore pointer clicks in the first 400 ms after their panel opens (`lib/cockpit/confirm-guard.ts`, `CONFIRM_ARM_MS`). A fresh Enter press still confirms at once, and so does a tap after 400 ms. This closes the held-Enter path (review 1) and the double tap on the mobile sheet, whose confirm button opens under the finger (review 3). The sheet layout itself is unchanged, as designed. Block's panel opens with focus in its empty "Who" field, so a held Enter only shows the required-field errors and cannot park the item.
- D43. Undo is offered and allowed only while writes are: nothing in flight, no failure panel, the data is not stale or still checking, and the item's tracked fields still match the snapshot taken after the operator's own write. If another writer changed the item, the status line stays but Undo is gone (review 2).
- D44. Deciding a lane packet in the Work list archives it, and `GET /api/tasks` leaves archived rows out. When an unhandled run item is missing from a read, the cockpit reads `GET /api/tasks?include=archived` once and uses the archived row to say what happened ("Rejected elsewhere.", "Closed elsewhere."). If that read fails, the item is reported as removed, as before (review 4).
- D45. Whether a finished run can reopen (transition 9) is derived from the items (every item resolved, run not closed), not from the stored phase, so the change text is the same on every poll and after a reload (review 5).
- D46. A background read interrupts the run only when something in the run changed: a run item, an exception joining, or an item displaced. Changes to backlog cards only (a new card that cannot join, a backlog packet expiring) do not stop the next J; they show on the next Resume screen and in the queue (review 6). A read is skipped while the operator's own write is in flight, so that write cannot show as a change (review 7).
- D47. When a joining exception displaces an item, the change summary names it: "Leaves today's run" (change kind `displaced`, review 10).
- D48. The Changed panel shows rows of plain words (`changeRows`): a content hash reads "The version you saw" / "A newer version", and approval, proof type and deadline source use the same words as the rest of the screen. No hash or stored enum name is shown (review 11).
- D49. If the browser refuses to store run progress, the screen says "Progress could not be saved in this browser. The run works until you close this page." Nothing is pruned (review 13; retention is open question Q8).
- D50. A refused write (4xx) re-reads at once, so Changed shows without waiting for the next poll (review 16). E with only file-path evidence says to use Copy path (review 17). "· Changed" also marks Title, Exact steps and the Prompt (review 18). Mobile sheets trap Tab and return focus to the opener (review 19). The summary's Handled list holds handled items only; items passed without handling sit under "Still needs you" (review 20).

## 3a. How the test-first rule was kept, and where it slipped

- Every logic module had its test file written and run red before the module existed, except `run.ts` and `controller.ts`: for those two, the implementation was written before the new test file had been run. Red was then shown by moving the module aside (module not found), and the tests were run against it. Both modules were later checked with mutations (section 8).
- The UI render tests (`components/cockpit/screens.test.tsx`) were written after the components. Mutation checks show they bite (making lane packets writable fails them).
- One test setup was wrong and was corrected, not weakened: in `run.test.ts` the "return after another writer changed things" run first started 27 hours earlier, when F06 was within 24 hours of expiry and so (correctly) an urgent exception. It now starts 49 hours earlier. The assertions did not change.
- The browser interaction script found a real bug: after Esc, focus went to the page body, because the button that opened the panel had been unmounted. It was fixed (D36), and the check now asserts focus. The same script's first version compared `innerText`, which is uppercased by CSS, so two "is absent" checks could never fail. They are case-insensitive now.
- Review fixes (section 9) were test-first: each finding got a failing test in `lib/cockpit/review-fixes.test.ts` or `lib/cockpit/confirm-guard.test.ts`, run red before the fix, and a mutation in section 8. Three existing checks were changed, each because the check itself was wrong or the timing changed, not to make a failure pass:
  - `lib/cockpit/view.test.ts`: the summary test asserted the old Handled list, which included items left unhandled. That was the bug in review 20. The assertion now expects handled items only, and a comment in the test says so.
  - `scripts/cockpit-interactions.mjs`: the phone sheet flows now wait 450 ms before tapping a confirm button, because taps in the first 400 ms are ignored by design (D42). The Review 8 check moves focus off the Back button before pressing Enter, so it tests the key map rather than a native button press.
  - `lib/cockpit/fixtures/fixture-api.ts`: the optional write delay (`writeDelayMs`, used only by the review-7 race test) applies after the write lands, so a poll in the gap sees the new value as a real backend would.

## 4. Deviations

- X1. Answer and note length. DECISIONS 5.1 allows an answer of 1 to 4,000 characters, but the stored body is `Answer: <text>` and the backend caps the whole body at 4,000. The answer limit is therefore 3,992 characters and the P decision note limit 3,980 (`Decision: Approved. ` is 20 characters), so a valid answer can never be refused by the server.
- X2. Defer Undo when there was no earlier snooze writes `snoozedUntil` = the moment of Undo instead of removing the field (Phase 0 answer 1). Eligibility is identical; the record keeps a past timestamp.
- X3. Block has no Undo in slice one (Phase 0 answer 1), unlike DECISIONS 6.7 and 15.
- X4. P-card Approve confirm: title "Approve this item?" and body "Your decision is saved as a note on this item and it leaves today's run. It records your decision; it does not authorize anything else. This cannot be undone." DECISIONS 5.6's "Approval applies to the current content only. If the item is edited, approval returns to pending." describes lane packets and is false for a generic card (GAPS 3). The Reject copy is as designed.
- X5. Expired lane packet: the designed panel and authority show, but there is no Reject button, because lane-packet actions are slice two. A read-only notice links to the Work list.
- X6. Defer confirm and status-line copy follow override 1 ("It is snoozed and leaves today's run…", "Deferred until Sun, Oct 4, 08:00 EDT. It leaves today's run.") instead of the README's priority copy.
- X7. The summary counts line adds "· N rejected" only when N is above 0; the README line shows four counts.
- X8. Two prototype colors were not tokens (the key chip on a primary button, the Authority dashed border). The build uses the nearest bundle tokens (`accent-tint` / `accent-on`, `ink-muted`, which the README names for the Authority border).

## 5. Tradeoffs

- T1. Fixture backend (`lib/cockpit/fixtures/fixture-api.ts`) instead of a development Convex. Production Convex is the only reachable backend on this machine, so every test and screenshot runs against the in-memory fixture backend. It mirrors the refusals the cockpit depends on (outreach immutability, closed packets, generic Done on external packets, snooze past expiry, unknown statuses, `null` for optional fields) so a test cannot pass by writing something the real backend would refuse.
- T2. Pure state-machine functions plus a framework-free controller, rather than logic inside React components, so every transition and action can be tested end to end without a browser.
- T3. The cockpit polls `/api/tasks` every 60 seconds from the client, like the existing data hook, instead of subscribing through Convex React. Writes go through the same HTTP routes the current interface uses, so the backend's validation and refusals apply unchanged.
- T4. Screenshots come from the development server in fixture mode, since production builds exclude fixtures by design. The floating development badge is hidden with injected CSS during capture only.
- T5. Playwright was not installed. The browser checks use an existing Playwright from the npx cache, passed in by `PLAYWRIGHT_MODULE`, and the installed Google Chrome.

## 6. Open questions

- Q1. GAPS addendum for JT: the Undo gap (no way to remove `waitingOn` or `snoozedUntil` through `PATCH /api/tasks`) needs either a narrow unset path or acceptance of X2 and X3 for slice two too.
- Q2. Transition 9 versus DECISIONS 1.9: reopening appends new cards to a finished run (D21). Confirm, or prefer leaving them in the backlog until tomorrow.
- Q3. Inactivity timeout length for transition 3 (not built).
- Q4. A card created after the run started never joins it, even if it is urgent (D7, rule 1.9). Confirm, or allow urgent new cards to join after the open item.
- Q5. `assignee: "both"` is eligible (D4). Confirm, or restrict runs to `jt`.
- Q6. Lane packets in a run cannot be finished in slice one. Should slice one leave them out of the run, or keep them in (as built) so they stay visible?
- Q7. Where `/cockpit` should eventually live (replace `/`, or be added to the nav) is not decided here; it is reachable only by URL.
- Q8. Browser storage retention (review 13). DECISIONS 8 asks to keep the previous day and never clear other keys; it does not say when to prune. One run record is about 47 KB with fixture data, and up to about 220 KB on a heavy day, so years of daily runs would be needed to approach the browser's limit of about 5 MB per site, which the current interface shares. Slice one prunes nothing and reports a failed save (D49). Proposal for slice two: keep the last 14 days of `mission-control:cockpit-run:*` keys and delete older ones on load.
- Q9. P-card Approve confirm copy (X4, review 12) needs JT's sign-off: keep "Approve this item?" with the generic-card body, or use DECISIONS 5.6's "Approve this version?" copy, which describes hash-bound approval that generic cards do not have.

## 7. Running log

- 2026-10-03: baseline in the worktree before any change: `bun test` 461 pass, 0 fail, 59 files; `tsc --noEmit --incremental false` exit 0; `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:9 npm run build` exit 0.
- Commits: `a86d2b7` bundle (unchanged), `ea1e8e3` overrides, `b3e6105` logic, `2641530` route and UI, `fbedcee` notes, screenshots and GAPS addendum, `27b3959` review fixes, then this file and the regenerated screenshots.

## 8. Verification (exact commands and results)

All commands ran in `mission-control/` of the worktree, with `node_modules` symlinked from the primary checkout (the symlink is not committed). `NEXT_PUBLIC_CONVEX_URL` points at an unreachable placeholder, so nothing could reach the production Convex.

| Check | Command | Result |
|---|---|---|
| Full test suite | `bun test` | **647 pass, 0 fail**, 9,376 expect() calls, 75 files (baseline 461 / 59; 627 / 73 before the review fixes) |
| Type check | `npx tsc --noEmit --incremental false` | **exit 0** (includes the bundle's `.ts` files) |
| Lint | `next lint` | **Not configured**: no ESLint config file exists, and `next lint` would start an interactive setup. Not run. |
| Production build | `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:9 npm run build` (writes `.next-build`) | **exit 0**; `/cockpit` 33.7 kB, first load 146 kB |
| No fixture code shipped | `grep -rl -e cockpit-fixture-run -e fx-invalid-card -e 'Sample DC Q1' -e fixtureSession -e FixtureApi .next-build/static \| wc -l` | **0** |
| Whitespace | `git diff --check e5b9943` (whole branch, working tree) | **clean** (exit 0). Commit `2641530` alone had one trailing blank line in `RunScreens.tsx`, fixed in the next commit. |
| Browser interactions | `PLAYWRIGHT_MODULE=… node scripts/cockpit-interactions.mjs` against `NEXT_PUBLIC_COCKPIT_FIXTURES=1 next dev -p 3100` | **25 of 25 pass**: J/K, C+Enter+Undo, D with tomorrow pre-selected, Esc returns focus, Q/Esc/?, E with no evidence, letters and Enter never open Approve, Tab+Enter+Enter approves with no Undo, answer validation and save, Copy prompt copies all 10,533 characters, failure + Retry, changed-underneath pause and acknowledge, stale pause, Enter starts the run, resume, pause, close the run, zero `/api/` requests in fixture mode, three phone sheet flows; added after the review: one held Enter opens Approve but never confirms it (review 1), queue keys on run start (review 8), a phone double tap opens Approve but does not confirm (review 3), 44 px phone targets (review 9) |
| Screenshots | `PLAYWRIGHT_MODULE=… node scripts/cockpit-screenshots.mjs docs/design/mission-control-redesign-slice-1/screenshots` | **39 files**: 20 states desktop, 19 mobile. Compared with the prototype in `docs/design/mission-control-redesign-slice-1/README.md` |
| Mutation checks | a script breaks one guard, runs the tests that should notice, restores the file | **35 of 35 caught**: nudge `>`→`>=`, no displacement, self-set deadline urgent, Complete before an answer, lane packets writable, Defer on outreach, snooze past expiry, a letter confirms Approve, Shift+Enter confirms, lifted slot trimmed, Guard lifted on Q, tie-break without createdAt, codes compared as strings, own writes not folded, updatedAt compared, new cards join a run, retry appends twice, stale not pausing, changed item not pausing, Sidebar guard removed, answer over the cap, Block offering Undo; after the review: held-key repeat not ignored, pointer tap not armed, Undo ignoring another writer, Undo while stale, no archived lookup, reopen keyed on phase, backlog changes interrupting, poll during a write, queue keys after the screen check, displaced item not reported, hash in the Changed panel, silent save failure, no read after a refusal |

The requested tests, by file:

| Requirement | Where |
|---|---|
| Eligibility | `lib/cockpit/eligibility.test.ts` |
| Curated order and the tie-break | `lib/cockpit/eligibility.test.ts` (curated order block) |
| Urgent exceptions | `lib/cockpit/exceptions.test.ts`, mid-run in `lib/cockpit/run.test.ts` |
| Slot lifting | `lib/cockpit/slots.test.ts` |
| Action matrix (DECISIONS 5) | `lib/cockpit/actions.test.ts`, `components/cockpit/screens.test.tsx` |
| Answer before Complete | `lib/cockpit/actions.test.ts`, `lib/cockpit/controller.test.ts` |
| Defer limits | `lib/cockpit/defer.test.ts` |
| Run state transitions (state map Part B, 1 to 11) | `lib/cockpit/run.test.ts`, `lib/cockpit/controller.test.ts` |
| No single key for Approve and Reject | `lib/cockpit/keyboard.test.ts` (every printable key and modifier set), browser checks |

## 9. Fresh-context review

A fresh agent with none of this build's context reviewed the branch against the bundle and the overrides. It was told not to write to the repository and not to contact any backend. It drove the real controller against the fixture backend and the fixture-mode page in Chrome, with every `/api/**` request blocked. Its report is committed unchanged at `docs/design/mission-control-redesign-slice-1/review-1.md` and pasted verbatim in the pull request description.

Verdict: **PASS WITH FINDINGS**, with 2 major findings, 11 minor and 7 nits. All were checked against the code before fixing. Every fix has a test that was seen failing first (section 3a) and a mutation check (section 8). Fixed in `27b3959`:

| # | Severity | Finding | What changed |
|---|---|---|---|
| 1 | Major | One held Enter opened and confirmed Approve or Reject | Confirm buttons ignore auto-repeat keydowns (D42). Browser check "Review 1" |
| 2 | Major | Undo wrote while paused and could overwrite another writer | Undo gated on the same conditions as writes, plus "unchanged since my write" (D43) |
| 3 | Minor | Phone confirm opens under the finger, so a double tap confirms | Taps in the first 400 ms are ignored (D42). Browser check "Review 3" |
| 4 | Minor | A packet decided in the Work list read as "no longer in Mission Control" | Archived lookup for missing run items (D44) |
| 5 | Minor | Same-day reopen text changed between polls | Reopen derived from the items (D45) |
| 6 | Minor | Backlog-only changes interrupted the next J | Only run changes interrupt (D46) |
| 7 | Minor | A poll during the operator's own write showed an empty change screen | Reads are skipped while a write is in flight (D46) |
| 8 | Minor | Queue keys misbehaved on the run start screen | The queue-open rule is checked first on every screen. Browser check "Review 8" |
| 9 | Minor | Phone targets under 44 px | Evidence links, Copy path and Open the Work list are 44 px. Browser check "Review 9" |
| 10 | Minor | The displaced item was not named | `displaced` change kind (D47) |
| 11 | Minor | The Changed panel could show a hash or stored enum names | `changeRows` in plain words (D48) |
| 13 | Minor | Storage grows without limit; failed saves were silent | Failed saves are reported (D49). Retention is open question Q8 |
| 14 | Nit | Hand-typed paddings | Density tokens (`px-d12`, `pt-d10`, …) |
| 16 | Nit | A refused write did not re-read | Re-read at once (D50) |
| 17 | Nit | E's message was misleading when only file paths are stored | File-path message (D50) |
| 18 | Nit | "· Changed" was on only three labels | It also marks Title, Exact steps and Prompt (D50) |
| 19 | Nit | Mobile sheets did not trap or restore focus | `components/cockpit/focus.ts` (D50) |
| 20 | Nit | The Handled list included items left unhandled | Handled items only (D50); `view.test.ts` assertion corrected (section 3a) |

Not changed:
- 12 (Approve confirm copy): this deviation (X4) is deliberate, and the reviewer agrees the reasoning is sound. It needs JT's sign-off (Q9).
- 15 (answer limit 3,992): the reviewer calls the build's limit "the correct resolution" (X1).
- The spec ambiguities the reviewer listed were already recorded: `both` owner (D4, Q5), the Guard line on Q cards (D8), the title regex used verbatim (DECISIONS 1.4), and transition 9 growing the run (D21, Q2).

What the reviewer could not verify, from its report: physical key repeat in Safari and Firefox, screen readers, a pixel comparison of all 39 screenshots, and real network timing for finding 7. None of these was run after the fixes either. The browser checks use Chrome and Playwright's synthetic key repeat.

## 10. Rollback

Everything is additive. To roll back, close the pull request, or revert its commits after a merge. Specifically:
- Delete `app/cockpit/`, `components/cockpit/`, `lib/cockpit/`, `scripts/cockpit-*.mjs` and `docs/design/mission-control-redesign-slice-1/`.
- Revert two small edits in shared files: the `hidesLegacyChrome` helper in `lib/mission-control/nav-layout.ts` with its one-line use in `components/Sidebar.tsx`, and the added keys in `tailwind.config.ts` (new `mc-*` colors and sizes, `mc-sans`/`mc-mono`, `d*` spacing, radii and widths; existing keys are untouched).
- Revert the `/cockpit` paragraph in `CLAUDE.md` and the plan entry in `tasks/todo.md` if wanted.
- No database, schema, Convex function, API route or environment variable changed, so there is nothing to migrate back. The only state the cockpit creates is browser storage under `mission-control:cockpit-run:<date>` on the operator's browser; it is harmless and can be left or cleared.
