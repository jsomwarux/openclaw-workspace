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

## 3a. How the test-first rule was kept, and where it slipped

- Every logic module had its test file written and run red before the module existed, except `run.ts` and `controller.ts`: for those two, the implementation was written before the new test file had been run. Red was then shown by moving the module aside (module not found), and the tests were run against it. Both modules were later checked with mutations (section 8).
- The UI render tests (`components/cockpit/screens.test.tsx`) were written after the components. Mutation checks show they bite (making lane packets writable fails them).
- One test setup was wrong and was corrected, not weakened: in `run.test.ts` the "return after another writer changed things" run first started 27 hours earlier, when F06 was within 24 hours of expiry and so (correctly) an urgent exception. It now starts 49 hours earlier. The assertions did not change.
- The browser interaction script found a real bug: after Esc, focus went to the page body, because the button that opened the panel had been unmounted. It was fixed (D36), and the check now asserts focus. The same script's first version compared `innerText`, which is uppercased by CSS, so two "is absent" checks could never fail. They are case-insensitive now.

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

## 7. Running log

- 2026-10-03: baseline in the worktree before any change: `bun test` 461 pass, 0 fail, 59 files; `tsc --noEmit --incremental false` exit 0; `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:9 npm run build` exit 0.
- Commits: `a86d2b7` bundle (unchanged), `ea1e8e3` overrides, `b3e6105` logic, `2641530` route and UI, then docs, screenshots and this file.

## 8. Verification (exact commands and results)

All commands ran in `mission-control/` of the worktree, with `node_modules` symlinked from the primary checkout (the symlink is not committed). `NEXT_PUBLIC_CONVEX_URL` points at an unreachable placeholder, so nothing could reach the production Convex.

| Check | Command | Result |
|---|---|---|
| Full test suite | `bun test` | **627 pass, 0 fail**, 9,324 expect() calls, 73 files (baseline 461 / 59) |
| Type check | `npx tsc --noEmit --incremental false` | **exit 0** (includes the bundle's `.ts` files) |
| Lint | `next lint` | **Not configured**: no ESLint config file exists, and `next lint` would start an interactive setup. Not run. |
| Production build | `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:9 npm run build` (writes `.next-build`) | **exit 0**; `/cockpit` 32.6 kB, first load 145 kB |
| No fixture code shipped | `grep -rl -e cockpit-fixture-run -e fx-invalid-card -e 'Sample DC Q1' -e fixtureSession .next-build/static \| wc -l` | **0** |
| Whitespace | `git diff --check e5b9943` (whole branch, working tree) | **clean** (exit 0). Commit `2641530` alone had one trailing blank line in `RunScreens.tsx`, fixed in the next commit. |
| Browser interactions | `PLAYWRIGHT_MODULE=… node scripts/cockpit-interactions.mjs` against `NEXT_PUBLIC_COCKPIT_FIXTURES=1 next dev -p 3100` | **21 of 21 pass**: J/K, C+Enter+Undo, D with tomorrow pre-selected, Esc returns focus, Q/Esc/?, E with no evidence, letters and Enter never open Approve, Tab+Enter+Enter approves with no Undo, answer validation and save, Copy prompt copies all 10,533 characters, failure + Retry, changed-underneath pause and acknowledge, stale pause, Enter starts the run, resume, pause, close the run, zero `/api/` requests in fixture mode, three phone sheet flows |
| Screenshots | `PLAYWRIGHT_MODULE=… node scripts/cockpit-screenshots.mjs docs/design/mission-control-redesign-slice-1/screenshots` | **39 files**: 20 states desktop, 19 mobile. Compared with the prototype in `docs/design/mission-control-redesign-slice-1/README.md` |
| Mutation checks | a script breaks one guard, runs the tests that should notice, restores the file | **22 of 22 caught**: nudge `>`→`>=`, no displacement, self-set deadline urgent, Complete before an answer, lane packets writable, Defer on outreach, snooze past expiry, a letter confirms Approve, Shift+Enter confirms, lifted slot trimmed, Guard lifted on Q, tie-break without createdAt, codes compared as strings, own writes not folded, updatedAt compared, new cards join a run, retry appends twice, stale not pausing, changed item not pausing, Sidebar guard removed, answer over the cap, Block offering Undo |

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

See the pull request description: the reviewer's findings are pasted there verbatim, and any follow-up is listed under them.

## 10. Rollback

Everything is additive. To roll back, close the pull request, or revert its commits after a merge. Specifically:
- Delete `app/cockpit/`, `components/cockpit/`, `lib/cockpit/`, `scripts/cockpit-*.mjs` and `docs/design/mission-control-redesign-slice-1/`.
- Revert two small edits in shared files: the `hidesLegacyChrome` helper in `lib/mission-control/nav-layout.ts` with its one-line use in `components/Sidebar.tsx`, and the added keys in `tailwind.config.ts` (new `mc-*` colors and sizes, `mc-sans`/`mc-mono`, `d*` spacing, radii and widths; existing keys are untouched).
- Revert the `/cockpit` paragraph in `CLAUDE.md` and the plan entry in `tasks/todo.md` if wanted.
- No database, schema, Convex function, API route or environment variable changed, so there is nothing to migrate back. The only state the cockpit creates is browser storage under `mission-control:cockpit-run:<date>` on the operator's browser; it is harmless and can be left or cleared.
