# Mission Control redesign, slice one: screenshots

Captured 2026-10-03 from `/cockpit` on a development server in fixture mode (in-memory backend built from the bundle's `source/02-fixtures.json`; no Convex, no `/api/tasks` request). Browser time zone forced to UTC so the times line up with the prototype; the app itself shows the operator's browser zone. Desktop is 1440 x 900; mobile is 390 x 844 at 1x.

Reproduce:

```bash
NEXT_PUBLIC_COCKPIT_FIXTURES=1 NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:9 npx next dev -H 127.0.0.1 -p 3100
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node scripts/cockpit-screenshots.mjs docs/design/mission-control-redesign-slice-1/screenshots
```

## Requested states

| # | State | Files | Prototype counterpart |
|---|---|---|---|
| 01 | First load (run start) | `01-first-load-{desktop,mobile}.png` | Screens → Run start |
| 02 | An active run (6 of 7, 5 handled) | `02-active-run-*` | Screens → Current item |
| 03 | The queue (full view; bottom sheet on mobile) | `03-queue-*` | Queue view / queue sheet |
| 04 | A Q card with its answer box | `04-q-card-answer-box-*` | Not built in the prototype (README "Not built" 1) |
| 05 | A P card's approve confirm | `05-p-card-approve-confirm-*` | Not built in the prototype |
| 06 | A parked item | `06-parked-item-*` | Block form, then status line |
| 07 | A deferred item | `07-deferred-item-*` | Defer (override 1: a snooze) |
| 08 | The empty run | `08-empty-run-*` | States → Empty run |
| 09 | Stale data | `09-stale-data-*` | States → Stale data |
| 10 | A failed action | `10-failed-action-*` | States → Action failed |
| 11 | Changed underneath me | `11-changed-underneath-*` | States → Changed underneath me |
| 12 | An invalid card | `12-invalid-card-*` | States → Invalid card |
| 13 | An expired card | `13-expired-card-*` | States → Expired |
| 14 | The run summary | `14-run-summary-*` | Screens → Run summary |

Extra: `15-resume-change-banner`, `16-degraded-connection`, `17-loading`, `18-defer-choices`, `19-park-form-errors`, `20-shortcuts-overlay` (desktop only).

## Compared with the prototype and README

Matches: layout and measurements of the header, rail, decision and context panes, mobile header, scroll area and action bar; all copy for the designed states; tokens, type scale, radii and borders; the queue table and sheet; run start, resume and summary structure.

Differences, all deliberate:

1. **Defer** (07, 18) shows the confirmed snooze choices (tomorrow 8:00 AM pre-selected, next week, a date) instead of the prototype's "priority is set to low" copy. Override 1.
2. **Approve on a P card** (05) reads "Approve this item?" and says the decision is saved as a note and authorizes nothing else. DECISIONS 5.6's "Approval applies to the current content only. If the item is edited, approval returns to pending" is true only for lane packets, so it would be false here. Deviation X4.
3. **Expired** (13) shows the expired panel and authority facts, but no Reject button: lane-packet actions are slice two. A read-only notice links to the Work list instead.
4. **Item 7 (the lane packet)** is read-only for the same reason, so the summary (14) reads "6 of 7 handled" with the packet under "Still needs you"; the prototype's summary assumed it was approved.
5. **Description** renders under the slots, with the answer box in place of the empty Answer bullet (04). The prototype did not build decision cards.
6. **Queue order outside the run** follows DECISIONS 1.6 (no sortOrder: createdAt, then title), so the outreach review comes before the expired packet. The prototype listed those rows in a different order.
7. **Resume** (15) lists two changes; the fixture run started after F06 had already expired, so no "Expired" row appears.
8. **Invalid card** (12) is a synthetic test card at position 7; the prototype showed the state on item 6.
9. **Token-only colors**: the key chip on a primary button and the Authority border use bundle tokens; the prototype hand-wrote two off-token OKLCH values there.
10. **Missing exact steps** show a Missing chip and a sentence, like evidence. The prototype's sample items always had steps.
