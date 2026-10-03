VERDICT: PASS WITH FINDINGS. Commit 27b3959 fixes most of the 20 findings, and the new confirm guard holds. One held Enter or Space, or a double tap under about 400 ms, no longer opens and confirms Approve or Reject. A real fresh Enter, and an `element.click()` with detail 0, still confirm at once. The safety invariants hold, and no regression in the existing tests was found. Three problems remain, and the first should be fixed before merge:
(1) Undo can still overwrite another writer's change once any acknowledge re-bases the snapshot. This is the same data-integrity class as finding 2.
(2) Finding 4 is not fixed after a reload, because the archived lookup skips the first read.
(3) Finding 7 is closed only for polls that start during a write. A read already in flight, or a return to the tab during a write, still reports the operator's own write as a change.

COMMANDS RUN:
- `git status --porcelain=v1` before and after: identical (`?? mission-control/node_modules` only; HEAD 22713c6, unchanged).
- `git show --stat 27b3959`, `git show --stat 22713c6` (docs and screenshots only), `git diff fbedcee 27b3959 -- <each changed file>`.
- `bun test` (mission-control) → "647 pass / 0 fail / 9376 expect() calls / Ran 647 tests across 75 files."
- `npx tsc --noEmit --incremental false` → exit 0, no output.
- `grep` of the existing `.next-build/static` (built 13:34, after the fix commit at 13:31) for cockpit-fixture-run, fx-invalid-card, writeDelayMs, fixtureSession and failReads → 0 files. `include=archived` is present in `app/cockpit/page-*.js`, so this build contains the fix.
- Bun probes in `mc-redesign-slice-1-scratch/review-2/`. The `@/` alias resolved, and they drive the real CockpitController against FixtureApi.
  - probe-controller.test.ts: 13 pass.
  - probe-reload-poll.test.ts: 1 pass.
  - Key outputs are quoted under the findings.
- Playwright with installed Chrome against :3100 in fixture mode (browser-probe.mjs and -2/-3/-4.mjs), with every `/api/**` request aborted → "API request attempts: 0" in every run. I never contacted :3000, :3210, :3211 or Convex.

PRIOR FINDINGS 1-20:
1. Fixed.
   - Browser: focus Approve, `keyboard.down('Enter')` ×6 → the panel opens and nothing is approved. Held Space on Reject: same.
   - Enter-open then an immediate fresh Enter → approved, as intended.
   - Caveat: confirm-guard.test.ts tests only the pure functions. Removing the `ConfirmButton` wiring (Panels.tsx:17-35) would not fail `bun test`; only the browser script, or my probe, catches it.
2. Partly fixed.
   - All four paths the review named are closed, and those tests do fail if the fix is reverted.
   - Any acknowledge brings Undo back over another writer's change (new finding 1).
3. Fixed. Phone double tap with the second tap at 80 ms or 300 ms → not approved. At 420 ms → approved, which is by design (`CONFIRM_ARM_MS` = 400). Same unit-test-only caveat as 1.
4. Partly fixed.
   - Works while the page stays open: a refresh reads "Rejected elsewhere.", and acknowledge records `outcome: rejected`.
   - Broken on load: new finding 2.
   - Other archive reasons are still told wrongly: new finding 4.
5. Fixed. `reopenable` is now derived from the items (run.ts:164 and 272). The test fails with the old phase-based rule.
6. Fixed for the named case: a backlog-only change keeps the run `inProgress`, and the test bites. Small leftover: new finding 6.
7. Partly fixed. Only reads that start while `busy` is set are skipped: new finding 3.
8. Fixed.
   - Browser, run start with the queue open: Enter and j are ignored, ? opens help, the first Esc closes help, the second closes the queue, and the run did not start.
   - Item screen with the queue open: j and c are ignored; q opens and closes the queue.
9. Fixed. Measured at 390 px on item 7: links 358×44, Copy path 72×44, "Open the Work list" 110×44.
10. Fixed. The `displaced` change is shown as "Leaves today's run" (RunScreens.tsx:16), and the test fails without it.
11. Fixed in code: ChangedPanel uses `changeRows` (ItemBlocks.tsx:30). Only `changeRows` is unit-tested, not the panel wiring.
12. Left as documented (X4, Q9). The copy is still "Approve this item?".
13. Partly addressed, as documented. A failed save sets the notice (controller.ts:94-97), and the test bites. Retention is open as Q8. Side effect: new finding 7.
14. Fixed. Computed at density 1: action bar padding 10px bottom, 10px top, 12px left; sheet padding-bottom 16px; run-start bar 10px. So the `calc(…*var(--mc-d,1)+env())` arbitrary values are valid CSS. No test.
15. Left as documented (X1).
16. Fixed. A refused write re-reads once (controller.ts:391), and the test fails if the line is removed.
17. Fixed. `nothingToOpen` (view.ts) is wired in CockpitApp.tsx:258-267. Only the pure function is tested.
18. Fixed by reading: Title label (ItemBlocks.tsx:88), Exact steps, and Prompt including the paste destination. No test, and no fixture changes those fields, so I did not see it in the browser.
19. Fixed (browser).
   - Phone Approve sheet: Tab and Shift+Tab stay inside, and Cancel returns focus to `[data-action=approve]`.
   - Defer sheet: Shift+Tab stays inside.
   - Queue sheet: Close returns focus to the header Queue button.
   - No automated test. See new finding 8.
20. Fixed. view.ts:348. The view.test.ts change is a justified correction: item 7 is still asserted under "Still needs you". Side effect: part of new finding 4.

NEW FINDINGS:
1. Major. Undo comes back after an acknowledge and overwrites the other writer's change.
   - Where: controller.ts:365-373 (`canUndo` compares the live task with `run.snapshot`); run.ts:283-287 (`acknowledge` re-bases the snapshot of every item, handled ones too); controller.ts:311-320 (`ackItemChange` re-bases the open item); run.ts:181 (`detectChanges` skips resolved items).
   - Spec: README paused states; state map Part B transition 7 ("Snapshot re-based"); D43's own rule that Undo is "bound to the state the operator's own write left".
   - Code: `item.undo` is never cleared, so after any re-base `itemChangedKeys` is 0 and Undo writes the value from before the write.
   - Verified with probe P4:
     - Complete item 6, then another writer sets status `in-progress`, then a poll. `canUndo` = false (correct).
     - Then Pause → Acknowledge. The Resume screen listed 0 changes for that item, so the operator was never told.
     - `canUndo` = true. `undo()` → backend status "todo", overwriting `in-progress`.
   - P4b: Start, then another writer sets `done`, then the operator acknowledges the Changed panel. `canUndo` = true, and Undo writes "todo" over `done`. The status line had still read "Started. Status is now In progress."
   - Why it matters: this is the overwrite finding 2 was meant to close. It is reachable through Pause/Resume, a reload, or any run change, and in the first path with no warning on screen.
   - Fix direction: store the post-write fingerprint on the item when the write succeeds, and compare the live task with that, not with the re-basable snapshot. Or clear `item.undo` when a re-base sees a difference.
2. Minor. Finding 4 is unfixed on load.
   - Where: controller.ts:122-124 (`if (!run) return tasks`) and 139-157 (`load()` reads before `state.run` is set; `enterToday` then resumes against those tasks).
   - Spec: DECISIONS 11.2 ("On load … compare a fresh read with the snapshot"); D44.
   - Verified with probes P1 and reload-poll. Packet F05 is rejected in the Work list, then the cockpit is reloaded (new controller, same storage):
     - 0 `listArchived` calls. The Resume screen says "It is no longer in Mission Control. It leaves today's run."
     - Acknowledge → `left: removed, did: "Removed elsewhere."`; the summary says "Still needs you: It is no longer in Mission Control."
     - If no acknowledge happens first, the next 60 s poll changes the same row to "Rejected elsewhere.", the same unstable text finding 5 was about.
3. Minor (timing-dependent). Finding 7 is closed only for polls that start mid-write.
   - Where: controller.ts:167 (busy is checked only before the read) and controller.ts:269-274 (`onVisible` calls `read()` with no busy check).
   - Verified with probes:
     - P2: a GET in flight when Start begins and served after the PATCH lands → phase `queueChanged`; J → `runResume` with 0 changes. This is exactly finding 7.
     - P3: hide then show the page while a Start is in flight → `runResume` lists "Edited since you left: the status changed." (the operator's own write).
     - P2b, a related race already present before this commit: a GET served before the PATCH whose reply lands after the fold → the Changed panel shows the operator's own Start, with status back to "todo".
   - The finding-7 test bites only for the "starts mid-write" case.
   - Fix direction: a write-generation counter that drops any read that started before the latest write finished.
4. Minor. Archived rows found by the lookup are mis-described, and the finding-20 change hides what is known.
   - Where: changes.ts:80-90; run.ts:252-256; view.ts:337.
   - Verified with probes:
     - P5b: a generic card archived in the Work list → the change summary says "Marked done elsewhere." That is false; it was archived. The old text, "no longer in Mission Control", was closer.
     - P5b and P5c (Eve skips a packet): after acknowledge the item is `left: removed, did: "Closed elsewhere."`. The summary now lists it under "Still needs you" as "It is no longer in Mission Control." Its `did` is no longer shown anywhere.
     - So the Resume screen and the summary contradict each other.
5. Nit. The archived lookup reruns on every poll while an unhandled run item is missing.
   - Where: controller.ts:122-133; convex/tasks.ts:1016-1025 (collects every archived row, with no limit).
   - P5: 5 calls in 5 polls for an item that was deleted outright, until acknowledge.
   - The time counts inside the read (`recordRead`), so a large archive could push reads past `SLOW_MS` and mark the connection degraded.
6. Nit. After the open-item change is acknowledged, a backlog-only change still interrupts J.
   - Where: controller.ts:316-318 checks `detectChanges(...).length`, not `.some(inRun)`.
   - P6: phase stays `queueChanged`; J → `runResume` showing only `[addedToBacklog, inRun:false]`. This goes against D46.
7. Nit. When storage fails, the save notice replaces navigation notices.
   - Where: controller.ts:96.
   - P7: at the end of a run with unhandled items, "Item 1 of 7 still needs you." becomes the save-failure text, and this repeats on every `setRun` and poll.
8. Nit. `useRestoreFocus` in `MobileSheet` does nothing for the confirm sheets.
   - Where: Panels.tsx:41 with :23. `autoFocus` moves focus during commit, before the passive effect records `document.activeElement`, so the effect captures the confirm button itself.
   - Restore works only because of the older D36 `focusAction` path (CockpitApp.tsx:206-218). Harmless, but the comment and D50 credit the wrong mechanism.
9. Nit. While a write hangs, reads are skipped.
   - Where: controller.ts:167; api.ts `send()` has no fetch timeout, which predates this commit.
   - A hung PATCH now turns the poll, "Refresh now" and "Retry now" into no-ops until reload. The connection correctly drifts to stale; it never shows falsely fresh.
- Fine (checked):
  - (a) Desktop: the confirm button does not open under the cursor, and a click inside 400 ms is silently ignored (a Nit-level UX cost).
  - (d) Pausing actions on the open item uses `paused()` → `openItemChange()` directly, so the `backgroundCheck` change cannot miss an open-item change.
  - (f) Keyboard: correct.
  - (h) The three test changes are justified. The view.test change matches finding 20. The 450 ms waits are paired with a new double-tap check. `writeDelayMs` is new, and placing it after the write lands is what makes the finding-7 test bite.

SAFETY INVARIANTS:
- No writes to lane packets or outreach reviews: holds. actions.ts and writes.ts are unchanged; the new calls are a read-only GET `?include=archived` and a re-read. `item.undo` exists only for permitted generic writes.
- Approve and Reject have no single-key path: holds. Verified with held Enter, held Space, an immediate Enter, phone double taps at 80 and 300 ms, and the keyboard map, which has no Approve or Reject command.
- No write while paused: holds. `act()` uses `permitted()`; `undo()` now requires `canUndo()`, which mirrors busy, failure, stale/checking and changed. New finding 1 is a write after the pause was acknowledged, not during it, but it still overwrites another writer.
- Feedback append-only: holds. `appendFeedback` is unchanged, and the PATCH route refuses `feedback`.
- Fixture code out of production: holds.
  - The gate at CockpitApp.tsx:77 is unchanged.
  - The fixtures are imported only through the dynamic harness import.
  - The 13:34 production build has no fixture markers.
  - Fixture-mode pages made 0 `/api` attempts.

COULD NOT VERIFY:
- The real backend: no live reads or writes. The archived route and PATCH pass-through were checked by reading route.ts and convex/tasks.ts.
- Physical key repeat, Safari, Firefox, and Linux X11 auto-repeat (where repeat may not be flagged).
- Real screen readers. A synthetic click with detail 1 inside 400 ms is silently dropped (probe B4b). TalkBack and iOS VoiceOver may send detail 1, though rarely within 400 ms.
- "· Changed" on Title, Steps and Prompt in the browser: no fixture edits those fields.
- The builder's scripts/cockpit-*.mjs and its 35 mutation checks: not run, per the rules. I reproduced the key behaviours with my own probes.
- The production build was not re-run; I relied on the existing .next-build from 13:34.
- How often new finding 3 happens under real network timing.
