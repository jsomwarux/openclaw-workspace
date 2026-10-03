# Handoff: Mission Control (daily decision cockpit)

## Overview

Mission Control is a private daily operating cockpit for one person. Agents prepare work; the operator decides: approvals, sends, posts, purchases, deployments. The interface is a queue worked one item at a time.

The job of the first screen: within ten seconds the operator knows the single item to handle now, why it is first, the exact action, and the context needed, without hunting. After that the operator works through the day's committed run, never returning to a backlog screen between items.

Read in this order:

1. `README.md` (this file): screens, layout, behavior, tokens.
2. `DECISIONS.md`: every question answered in the design process, written as rules to implement.
3. `KEYBOARD.md`: the keyboard map.
4. `GAPS.md`: what the design needs that `source/01-data-contract.md` does not support, and what each would take.
5. `state-map/03-state-map.md`: **the governing state map.** Part A is backend truth. Part B is the daily-run state machine this design adopts; section "State map coverage" below maps each state to a screen.
6. `reference/view-model.ts`: TypeScript view-model types that enforce "verbatim or missing".
7. `tokens/`: CSS variables, Tailwind v3 config, Tailwind v4 theme, JSON.
8. `prototype/`: the HTML design references.
9. `source/`: the data contract, fixtures and UX guide that were binding for the design.

Target stack: Next.js 15 (App Router), TypeScript, Tailwind CSS, Convex.

## About the Design Files

The files in `prototype/` are **design references created in HTML**. They show intended look and behavior. They are not production code. Do not copy them into the app. Recreate the screens in the existing Next.js codebase with its own components, routing and Convex queries and mutations.

`prototype/Mission Control.dc.html` is a single self-contained page that needs `prototype/support.js` next to it. Open it in a browser. A **Prototype** control at the bottom-left (desktop widths only) jumps to every screen and state. It is scaffolding and must not ship. A Tweaks panel exposes eight tuning controls (see "Tuning controls").

`prototype/Current Item Wireframes.dc.html` holds the three structural options compared before the build. Option B (two panes with a queue rail) was chosen. Keep it for the reasoning only.

## Fidelity

**High fidelity** for everything the prototype renders: final colors, type, spacing, states and interactions. Recreate pixel-accurately using Tailwind and the tokens in `tokens/`.

**Specified but not built** (follow the rules in `DECISIONS.md`, use the same components and tokens): see "Not built in the prototype" below. Do not treat the prototype as complete for those.

## Product constraints that shaped every screen

- **Verbatim data, never synthesis.** Render each field exactly as stored. A missing field renders as a "Missing" chip. Nothing is inferred or filled. Use the `Verbatim<T>` type in `reference/view-model.ts` for every displayed field.
- **Plain language.** No developer vocabulary on screen: no "payload", "null", "undefined", "fetch failed", snake_case or camelCase labels. Use the words in this document.
- **One order at a time.** Curated order is the default. The header always names it. An urgent item may jump ahead only as a labeled exception that says why.
- **States are designed.** Loading, empty run, stale data, degraded connection, failed action with retry, changed underneath me, invalid card, expired.
- **Excluded:** marketing hero, gradients, glow, glass, neon styling, charts or metrics above the current item, kanban, streaks, badges, confetti, any celebration. Do not use Inter or Roboto.
- **Motion:** only press feedback (scale 0.97, 160 ms ease-out) on pressable controls. Everything else is instant, including keyboard-initiated actions. Skeletons are static.

## Screens and views

Every screen exists at desktop (primary) and mobile (390 x 844) unless noted. In the prototype, open each through the Prototype control: Screens group (Run start, Resume with queue changed, Current item, Run summary), States group (the eight states), Layout group (Auto, Desktop, Phone).

### 1. Current item (desktop)

**Purpose:** decide and act on one item. Nothing competes above it.

**Layout:** page is a column, `min-width: 1100px`, `height: 100vh`.

1. **Header**, 44 px high, `surface` fill, 1 px `line` bottom border, padding `0 16px`, gap 28 px. Left to right: wordmark "Mission Control" (15/700); label `ORDER` + value "Curated order" (600); label `TODAY'S RUN` + "6 of 7" (600) + "· 5 handled" in `ink-muted`; spacer; freshness text 13 px `ink-muted`; buttons "Pause run", "Queue" with key chip `Q`, "Shortcuts" with key chip `?`. Header buttons: 1 px `line-strong` border, `surface` fill, radius 4, padding `4px 10px`, 13/500, hover `control-hover`. Key chip: mono 11/500, 1 px `line-table` border, radius 3, padding `0 5px`, `ink-muted`.
2. **Status banner** (only for stale and degraded): full width under the header, padding `8px 16px`, `notice` fill, 1 px `line-strong` bottom border, 13 px. Tag chip (mono 11/600 uppercase, tracking .06em, 1 px `ink` border, radius 3), message, one button.
3. **Body row**, fills the remaining height, three columns:
   - **Queue rail**, 248 px, `panel` fill, 1 px `line` right border, scrolls. Rows are grouped under mono 11 uppercase `ink-muted` headers: Q, P, AP, Other cards (padding `12px 12px 4px`). Row: position (mono 12, 16 px wide), title (13 px, one line, ellipsis), status (11 px `ink-muted`). Row min-height = `--mc-qrow - 3px` (31 px), padding `6px 12px`. Current row: `accent-tint` fill, 3 px `accent` left bar, weight 700. Handled rows: `ink-muted`. Hover `panel-hover`. The rail shows only today's run (7 rows).
   - **Decision pane**, width `clamp(380px, 34%, 480px)`, `surface` fill, 1 px `line` right border, scrolls. Inner padding `20px 24px 12px`, gap 16. Order of blocks, top to bottom: state panels (expired, changed, invalid; see States), eyebrow, title, First action, Why it matters, Done when, Authority (approval items only), action row, confirm or failure panel, status line with Undo. A sticky footer holds the notice line and the Previous / position / Next row.
   - **Context pane**, flexible, padding `20px 32px 40px`, gap 24, scrolls. Sections separated by 1 px `line` rules (padding-top 16): Exact steps, Paste-ready prompt, Evidence links, Freshness and source, Feedback history.

**Decision pane components**

| Component | Spec |
|---|---|
| Eyebrow | mono 12/400 `ink-muted`: `6 of 7 · Not started · Owner: jt · Priority: high` |
| Title | Hanken Grotesk 24/1.2, 700, tracking -0.015em, `text-wrap: balance`, `overflow-wrap: anywhere`. Never truncate. |
| First action | Container: 2 px dashed `line-missing` when missing, radius 6, padding `14px 16px`, `page` fill. Label `FIRST ACTION` (mono 11 uppercase `ink-muted`) + chip "Missing". Text 17/600: "This item has no first action recorded." When present: same container with 2 px solid `ink` border and `surface` fill, text 17/600 verbatim. When lifted from a description line, add chip "From description". |
| Why it matters / Done when | Label (mono 11 uppercase `ink-muted`) above body text 14/1.45, `overflow-wrap: anywhere`. |
| Authority | Only when the item needs approval. 1 px dashed `ink-muted` border, radius 6, padding `10px 12px`, `surface` fill. Label `AUTHORITY · NEEDS YOUR APPROVAL`. Body, for example: "Approval pending · Edited after it was added · Expires in 2 days · Proof needed to finish: application reference". |
| Actions | Row, gap 8, wraps. Primary = `accent` fill, `accent-deep` 1 px border, `accent-on` text, radius 4, padding `9px 18px`, 14/600; hover `accent-hover`. Secondary = `surface` fill, 1 px `line-control` border, `ink` text, padding `9px 16px`; hover `control-hover`. Start is primary while status is not started; Complete becomes primary once started. Complete and Defer show key chips C and D. Block has no key. Only actions permitted for the item's family and status render (see `DECISIONS.md`, "Permitted actions"). |
| Confirm panel | 1 px `line-control` border, radius 6, `page` fill, padding `12px 14px`. Title 600, one sentence stating the consequence, buttons (confirm = primary, Cancel = secondary), hint "Enter confirms · Esc cancels". Complete: "Mark this item done?" / "No proof is recorded for this type of item. It leaves today's run." Defer: "Defer this item?" / "Its priority is set to low and it moves to the end of today's run." Reject: "Reject this item?" / "It closes for good and leaves today's run. This cannot be undone." (confirm button is `ink` fill). |
| Block form | Same container. Title "Park this item on a person". Help "It leaves today's run and returns when the nudge is due." Fields: "Who are you waiting on", "What are you waiting for", "Nudge after (days)" (default 14, whole number 1 to 365). Inline errors in `error` 12/500: "Enter who you are waiting on." / "Enter what you are waiting for." / "Enter a whole number of days from 1 to 365." Buttons "Park it" and Cancel. Input: radius 4, 1 px `line-control`, padding `7px 9px`, `surface` fill. Values are preserved on error. |
| Status line | Appears after an action: 13 px, top 1 px `line` rule, text + "Undo" link button (`accent-deep`, underlined). Examples: "Started. Status is now In progress." / "Marked done. Press J for the next item." / "Deferred. Priority is now low and the item moves to the end of today's run." / "Parked on {who}. It returns to today's run if no reply by day {n}." Undo is offered only where the backend allows reversal (see `DECISIONS.md`). |
| Footer | Sticky bottom of the pane, `surface` fill, 1 px `line` top rule, padding `10px 24px`. Notice line 13 px. Row: "← Previous" + chip K, centered mono 12 position, "Next →" + chip J. Buttons padding `7px 12px`, 13/600, 1 px `line-strong` border, radius 4. |

**Context pane components**

| Section | Spec |
|---|---|
| Exact steps · N | Numbered list. Number mono 13 `ink-muted` in a 20 px column, step text 14, gap 6. |
| Paste-ready prompt | Header row: label, meta in mono 12 `ink-muted` ("108 lines · 10,533 characters"), "Show more" / "Collapse" button, "Copy prompt" primary button (min-width 112, label becomes "Copied" for 1.8 s). Under it: "Where to paste" (13/600) + destination text verbatim. Then the prompt in a `<pre>`: mono 12.5/1.55, `white-space: pre-wrap`, `overflow-wrap: anywhere`, `surface` fill, 1 px `line-table` border, radius 6, padding `12px 14px`, height 300 px collapsed and 640 px expanded, scrolls, focusable. The text is never reformatted, never rendered as Markdown, and Copy copies the full original string. If copy fails: inline error "The prompt could not be copied. Select the text below and copy it by hand." When the prompt is missing: meta reads "Missing" and the box, Show more and Copy are not rendered. |
| Evidence links | Label + count, or chip "Missing" with "No links are recorded for this item." Links render as a list (mono 12, wrapped) or as pill chips (1 px `line-strong`, radius 999, padding `3px 10px`, one line, ellipsis). Web links open in a new tab. Local file paths are text, not links. |
| Freshness and source | Definition grid, 150 px label column: Last changed, Created (both "Sep 24, 2026, 00:00 UTC · 9 days ago"), Source (value or Missing chip), Project (value or Missing chip), Description (Missing chip when absent). |
| Feedback history | "None recorded." when empty. Otherwise one entry per row, newest last, each with author (jt or eve), timestamp and the full body. Not built (see below). |

### 2. Current item (mobile, 390 x 844)

Single column; actions in thumb reach at the bottom; queue is a bottom sheet.

- **Header:** padding `8px 8px 8px 16px`, `surface`, 1 px `line` bottom. Left: "6 of 7 · 5 handled" (17/700 + 13/500 muted), under it mono 11 "Order: Curated order · Up to date". Right: "Pause" (min 64 x 44) and "Queue" (min 76 x 44), radius 6, 1 px `line-strong`.
- **Scroll area:** padding `16px 16px 24px`, gap 16. Same blocks in the same order as desktop: state panels, eyebrow, title (22/1.22/700), First action, Why it matters, Done when, Authority, Exact steps, Paste-ready prompt (full-width Copy prompt button, 48 px, `accent-tint` fill, 1 px `accent-deep` border, `accent-ink` text, 15/700; prompt box 240 px collapsed, 480 px expanded; full-width "Show more" 44 px), Evidence links, Freshness and source (108 px label column), Feedback history.
- **Action bar**, pinned at the bottom (tweak: top), `surface`, 1 px `line` top rule, padding `10px 12px calc(10px + env(safe-area-inset-bottom))`, gap 8. Row 1: Start (primary, flex 2, 48 px, 16/700, radius 6) + Complete (secondary, flex 1, 48 px). Row 2: Defer, Block, Previous, Next (flex 1, 44 px, 14 px). After Start, row 1 is Complete (primary, full width). After the item is resolved, row 1 is "Next item →" (primary) and row 2 is Previous only. Expired: row 1 is Reject (outlined `ink`, 48 px). Notice, status line + Undo (44 px target), failure panel and paused message render above the buttons.
- **Sheets** (confirm, Block form, Queue): scrim `ink` at 45 %; sheet radius `12px 12px 0 0`, 1 px `line-strong` top border, padding `20px 16px calc(16px + safe-area)`, title 18/700, buttons 48 px full width stacked (confirm first, Cancel second). Queue sheet: height 88 %, header (title 18/700, mono 11 "Order: Curated order · 6 of 7", mono 11 "Today's run 7 · Outside today's run 5", Close button 44 px), scrolling list.
- All hit targets are at least 44 px. Inputs use 16 px text so the browser does not zoom.

### 3. Queue

**Purpose:** scannable list of everything, grouped by series, with the active order stated.

**Desktop:** a full view that replaces the three-column body (header stays). Opened with the Queue button or Q; closed with Esc, Q, or "← Back to item 6 of 7". Content column max 1120 px, padding `20px 24px 48px`, gap 14.

- Title "Queue" (22/700). Order statement: "**Order: Curated order.** Q, P and AP follow their numbers, then other cards in their saved sequence. No other order is active."
- Counts row (13 px, top and bottom 1 px `line` rules): "**7** in today's run · **5** handled · **1** current · **1** up next · **5** outside today's run".
- Table in a `surface` card (1 px `line-table`, radius 6). Columns: `44px minmax(240px,1.6fr) 140px 56px 56px minmax(220px,1.4fr)` with gap 12: **Pos.** (right-aligned), **Item**, **Status**, **Owner**, **Age** (right-aligned), **Blocker**. Header row: `panel` fill, mono 11 uppercase `ink-muted`. Group header rows: mono 12/600 uppercase, "Q · 1 item", "P · 1 item", "AP · 1 item", "Other cards · 9 items". Inside Other cards, a divider row "Not in today's run" (12/600, dashed top rule, `page` fill) precedes backlog items. Row: min-height `--mc-qrow` (34 px), 3 px left bar (`accent` on the current row), current row `accent-tint`, hover `row-hover`. Title one line with ellipsis and a tooltip with the full title. Items outside the run show "—" for position and are dimmed. Blocker shows the text or "None recorded" dimmed.
- Footnote: "Age counts from when the item was created. A dash means the item is not in today's run."
- Clicking a row opens that item (rows for items not yet built show a notice in the prototype).

**Mobile:** the same data as a bottom sheet (above). Row: min-height `--mc-qrow + 22px` (56 px), two lines: position + title, then `Status · Owner: jt · Age 9d · Blocker or "No blocker recorded"` in 12 px `ink-muted`. Same group headers and "Not in today's run" divider.

**Status values in the queue:** run items show Handled, the live status of the current item, or Up next. Items outside the run show their own state: Not started, Waiting, Done, Expired, Awaiting decision. Age = time since `createdAt` (hours under 48 h, otherwise days). Blocker = `waitingOn` as "Waiting on {who}: {what}", else the first line of the description when the title begins "Blocked", else none.

### 4. Run start

Shown when no run has started today.

- Column max 760 px, padding `40px 32px 56px` (mobile `20px 16px 28px`), gap 20. Header strip: wordmark, "Order: Curated order", Shortcuts button (desktop), "Sat, Oct 3".
- Label `TODAY'S RUN`, h1 28/1.15/700/-0.02em "7 items, ready to start", meta "Saturday, Oct 3 · Curated order · Q 1 · P 1 · AP 1 · Other cards 4".
- **First item card:** 2 px solid `ink`, radius 8, `surface`, padding `16px 18px`. Label `FIRST ITEM · 1 OF 7`, title 20/700, First action (with "From description" chip when lifted), "Why it is first": "Curated order puts Q cards first, in number order."
- "Urgent exceptions": "None. No approval expires within 24 hours and no external deadline is overdue." If any exist, list each with its reason.
- Footnote: "5 other items stay in the backlog and are not part of today's run."
- **Action bar** (pinned, same spec as run screens below): "Start run" (primary), "See the queue" (secondary). Enter starts.

### 5. Run resume (and what changed)

Shown when returning to an unfinished run. **The change summary appears before anything moves the operator.**

- Label `TODAY'S RUN · PAUSED`, h1 "Resume at 6 of 7", meta "5 handled · You left Oct 2, 21:00 UTC (3 hours ago)".
- **Changes banner** (only when something changed): 2 px solid `ink`, radius 8, `notice` fill, padding `16px 18px`. Label `CHANGED WHILE YOU WERE AWAY · 3`, headline 16/600 "None affect item 6 of 7. One affects a later item.", then a list (1 px `line-notice` rules): tag chip (Changed, Added to the backlog, Expired), location mono 12 ("Item 7 of 7" / "Not in today's run"), item title 600, detail sentence. Closing line: "Order and run size are unchanged. Item 6 of 7 is unchanged since you left."
  - Changed: "Edited since you left. Approval is pending for the new version. Expires in 2 days."
  - Added to the backlog: "Created 50 minutes ago." New items never join a committed run.
  - Expired: "Expired Oct 2, 00:00 UTC. Hidden from today."
- No changes: a bordered card: "**Nothing changed while you were away.** Order, run size and every item are as you left them."
- "Where you left": title (18/700), eyebrow, "Next in the run, 7 of 7: {title}".
- **Action bar:** primary "Acknowledge and resume at 6 of 7" (or "Resume at 6 of 7" when nothing changed), secondary "Review the queue first". Acknowledging re-bases the run snapshot (state-map transition 7).

### 6. Run summary

Shown when every item in the run is handled.

- Label `RUN SUMMARY`, h1 "7 of 7 handled", meta "Saturday, Oct 3 · Curated order · 4 completed · 2 approved · 1 parked · 0 deferred". No celebration, no streak, no score.
- **Still needs you** (first, because exceptions come first): 2 px `ink` card listing items that remain open after the run with the next required step and date, for example "Approved. To finish, record an application reference. Expires Oct 5, 01:09 UTC." and "Parked on {who}. Nudge due Oct 17."
- **Handled:** ordered list in a card: position, title, what was done ("Answer recorded, then completed.", "Approved. Note recorded.", "Completed.", "Parked on … Nudge after 14 days.", "Approved. Proof still to record.").
- Line: "Added to the backlog since the run started: 1 item. It is not part of today's run."
- **Action bar:** "Close the run" (primary), "See the queue". After closing the bar shows: "Run closed for today. The next run starts when you open Mission Control tomorrow."

### 7. Shortcuts overlay (desktop)

Opened with `?` or the Shortcuts button, on every desktop screen. Scrim `ink` 45 %. Dialog 500 px (max `100vw - 32px`), `surface`, 1 px `line-strong`, radius 8, padding `20px 24px`, gap 16. Title "Keyboard shortcuts" (17/700) and a "Close · Esc" button. Groups with mono uppercase labels: Move (J Next item, K Previous item, Q Show or hide the queue), Act (C Complete, asks you to confirm; D Defer, asks you to confirm; E Open evidence links), Dialogs (Enter Confirm, Esc Cancel or close), Help (? Show this list). Footer note: "Approve and Reject have no shortcut. Click the button, then confirm with Enter or a click. Reject cannot be undone." See `KEYBOARD.md`.

### 8. Designed states

All eight are reachable through the Prototype control. Plain-language copy is final.

| State | Where it appears | Design |
|---|---|---|
| **Loading** | Current item (desktop and mobile) | Skeleton that matches the layout, no shift on resolve: 7 rail bars (22 px), decision pane blocks (eyebrow 14, title 30 x 2, First action 84, text lines, four button blocks), context blocks (prompt 300). Blocks are `skeleton` fill, radius 4, **static**. Visible text "Loading today's run…". Header freshness reads "Checking…". No actions render. |
| **Empty run** | Run screen | h1 "Nothing is waiting for you". Card: "Today's run has no items." / "No cards are committed to it, and none of your agents' work needs a decision from you right now." "What you can do": "Check again if you expect new work. 5 items are in the backlog. Review them to decide whether any belong in today's run." Buttons "Check again" (shows "Checked just now. Nothing new yet.") and "Review the backlog" (opens the queue). |
| **Stale data** | Banner under the header | Tag "Out of date", "Last checked Oct 2, 23:22 UTC (38 minutes ago). This item may have changed since.", button "Refresh now". Header reads "Out of date · last checked …". Reading and copying still work. **All write actions are replaced by** "Actions are paused until this item refreshes." |
| **Degraded connection** | Banner under the header | Tag "Connection", "The connection is slow or dropping. Showing the copy from Oct 3, 00:00 UTC. Retrying automatically.", button "Retry now". Header reads "Connection unreliable · last checked …". Actions stay available; a failed write produces the failure panel. |
| **Failed action with retry** | Decision pane (desktop), above the buttons (mobile) | 2 px `error` border, `error-bg` fill, radius 6, padding `12px 14px`. Title 700 "Could not {action phrase}." (for example "Could not mark this item done."). Body: "Nothing was changed. The connection dropped while saving. If this keeps happening, check that you are on your private network." Buttons "Retry" (primary) and "Dismiss". The item stays on screen and the position does not advance. Retry repeats the same write; success shows the normal status line. |
| **Changed underneath me** | Top of decision pane / scroll area | Panel: 2 px `ink` border, `notice` fill, radius 8, padding `14px 16px`, tag "Changed while you were looking", headline "Another writer edited this item at Oct 3, 00:00 UTC. The done condition changed.", **Previous version** and **Now** text blocks, button "I have read the new version". The changed field's label gets "· Changed". Actions are replaced by "Actions are paused until you confirm you have read the new version." until acknowledged. |
| **Invalid card** | Top of decision pane / scroll area | Same panel style, tag "Invalid card", "This card cannot be acted on.", list of plain reasons ("No title is recorded." "Its status is not one this app recognizes."), "Fix the card where it was created, then check again. Source: Missing.", button "Check again". Title reads "Title missing". Prompt copy is disabled ("Not available for an invalid card"). Only Previous and Next work. |
| **Expired** | Top of decision pane / scroll area | Panel, tag "Expired", "This item expired on Oct 2, 00:00 UTC (1 day ago).", "Approval is no longer possible. You can still reject it. Moving on leaves it unhandled." Authority block: "Approval pending · Expired · Proof needed to finish: RSVP reference". The only action is **Reject** (outlined) with the note "Approve is no longer available." Header status reads Expired; the rail row shows Expired. |

## Interactions and behavior

- **Run flow:** Run start → Start run → items 1 to 7 → Run summary → Close. Returning mid-run goes to Resume, never straight to an item. "Pause run" returns to Resume.
- **Order:** one order at a time, "Curated order", always in the header and at the top of the queue.
- **Action flow:** Start applies immediately. Complete, Defer, Reject (and Approve) open a confirm panel; Block opens the form. Confirm applies the write; failure shows the failure panel; success shows the status line.
- **Paused states** (stale, changed underneath until acknowledged, invalid, loading, expired for everything except Reject, failed until dismissed or retried): `C`, `D` and all write buttons are inactive.
- **Prompt:** Copy copies the exact stored string with the Clipboard API (fallback `execCommand`). It needs a secure context (HTTPS or localhost).
- **Evidence:** `E` opens the first web link in a new tab; with none it shows "Nothing to open: this item has no evidence links." Local file paths cannot open from a browser; offer a copy-path control (see `GAPS.md`).
- **Queue:** Q toggles the full view (desktop) or sheet (mobile). Esc closes. Choosing the current item returns to it.
- **Responsive switch:** below 760 px wide the mobile layout is used. The prototype's Layout control forces Desktop or Phone.
- **No celebratory or decorative motion.** Press feedback only.

## State management

Client state (React). The run record is described in `DECISIONS.md` ("Where run progress is stored") and `GAPS.md`.

```ts
// See reference/view-model.ts for full types.
type ScreenState = 'normal' | 'loading' | 'emptyRun' | 'stale' | 'degraded' | 'actionFailed'
                 | 'changedUnderneath' | 'invalidCard' | 'expired';
type Screen = 'runStart' | 'runResume' | 'item' | 'runSummary' | 'emptyRun';

interface UiState {
  screen: Screen;
  queueOpen: boolean;          // desktop full view or mobile sheet
  helpOpen: boolean;
  mode: null | 'complete' | 'defer' | 'block' | 'reject' | 'approve';
  promptExpanded: boolean;
  copied: boolean; copyFailed: boolean;
  changedAck: boolean;         // "changed underneath me" acknowledged
  failedAction: null | { label: string; retry: () => void };
  undo: null | { snapshot: unknown };
  notice: string;              // transient, 4 s
  lastGoodReadAt: number;      // for stale and degraded
}
```

Transitions: see the table in `state-map/03-state-map.md` Part B. Derived flags in the prototype (`paused`, `openEff`, `canAct`) are the reference for when write actions are inactive.

## Tuning controls (Tweaks)

Eight controls, all tune the chosen direction without changing layout. Implement them as CSS variables (`tokens/tokens.css`) set from a user setting; ship defaults only unless the user asks for a settings screen.

| Control | Values | Default | Effect |
|---|---|---|---|
| Density | compact, comfortable | compact | `--mc-d` 1 or 1.2 multiplies gaps and paddings |
| Base type size | 13 to 17 px | 14 | `--mc-fs`; every font size is `calc(var(--mc-fs) * ratio)` where ratio = size / 14 |
| Prompt block height | 160 to 520 px, step 20 | 300 | Collapsed height. Expanded = collapsed + 340 (desktop). Mobile = 0.8x collapsed, 1.6x expanded |
| Queue row height | 28 to 48 px, step 2 | 34 | `--mc-qrow`; rail row = value - 3; mobile sheet row = value + 22 |
| Evidence | list, chips | list | See Evidence links |
| Mobile action bar | bottom, top | bottom | Bar moves under the header |
| Accent shade | deep, standard, light | standard | Accent L 0.44 / 0.50 / 0.56 (hover -0.06, deep -0.07) |
| Focus ring | accent, ink, halo | accent | accent: 2 px solid accent, offset 2. ink: 3 px solid ink. halo: 2 px accent plus `0 0 0 5px` accent at 22 % |

Note: Evidence has no visible effect on the prototype's sample items because neither has links. Check it on a card with links (fixture F05 has four).

## Design tokens

Full set in `tokens/`. Light theme only. Fonts: **Hanken Grotesk** (400, 500, 600, 700) for UI and **JetBrains Mono** (400, 500, 600) for labels, numerals, keys, prompts. Load with `next/font/google`; expose as `--font-hanken` and `--font-jetbrains`.

### Colors

| Token | OKLCH | Hex | Use |
|---|---|---|---|
| `page` | oklch(0.975 0.006 85) | #f9f6f2 | App background |
| `surface` | oklch(0.995 0.003 85) | #fefdfb | Decision pane, cards, inputs, header, bars |
| `panel` | oklch(0.955 0.008 85) | #f3f0ea | Queue rail, table header |
| `panel-hover` | oklch(0.92 0.012 85) | #e8e4dc | Rail row hover |
| `row-hover` | oklch(0.94 0.01 85) | #eeebe4 | Table row hover |
| `control-hover` | oklch(0.95 0.008 85) | #f1eee9 | Secondary button hover |
| `skeleton` | oklch(0.92 0.01 85) | #e8e4dd | Loading blocks |
| `line` | oklch(0.89 0.01 85) | #dedad3 | Pane and section dividers |
| `line-soft` | oklch(0.93 0.008 85) | #eae7e2 | Row separators |
| `line-table` | oklch(0.85 0.01 85) | #d1cdc7 | Table, card, prompt box outlines |
| `line-notice` | oklch(0.82 0.015 85) | #c8c4b9 | Dividers inside notice panels |
| `line-strong` | oklch(0.78 0.012 85) | #bbb7af | Header buttons, dialogs, sheets |
| `line-control` | oklch(0.62 0.012 85) | #89867e | Secondary button and input borders |
| `line-missing` | oklch(0.72 0.012 85) | #a8a49c | Dashed outline of a missing slot |
| `ink` | oklch(0.22 0.01 70) | #1e1a16 | Primary text, 2 px emphasis borders |
| `ink-secondary` | oklch(0.35 0.012 70) | #3f3a34 | Supporting copy |
| `ink-muted` | oklch(0.45 0.012 70) | #5a544e | Labels, meta, handled rows |
| `accent` | oklch(0.50 0.12 150) | #21763c | Primary action fill |
| `accent-hover` | oklch(0.44 0.12 150) | #03642b | Primary hover |
| `accent-deep` | oklch(0.43 0.12 150) | #006129 | Primary border, links |
| `accent-ink` | oklch(0.36 0.1 150) | #004b1e | Copy prompt text, mobile |
| `accent-tint` | oklch(0.94 0.03 150) | #def1e1 | Current row, mobile Copy fill |
| `accent-on` | oklch(0.99 0.003 85) | #fdfcf9 | Text on accent |
| `notice` | oklch(0.97 0.025 85) | #fdf4e3 | Banner and notice panel fill |
| `error` | oklch(0.42 0.14 30) | #892218 | Field errors, failed-action border |
| `error-bg` | oklch(0.97 0.02 30) | #fff1ed | Failed-action fill |
| scrim | oklch(0.22 0.01 70 / 0.45) | rgba(30,26,22,.45) | Sheet and dialog scrim |

Accent shades (hex): deep #03642b / hover #00531b / deep-border #005018; standard #21763c / #03642b / #006129; light #36884d / #21763c / #1d7339.

Contrast: `ink` on `page` and `surface` is above 15:1. `ink-muted` on `surface` is above 7:1. `accent-on` on `accent` is about 5.5:1 (standard) and stays above 4.5:1 on the light shade. Color never carries meaning alone: every state has a word.

### Type scale (px at base 14; all scale with `--mc-fs`)

| Role | Size / line / weight |
|---|---|
| Mono label (uppercase, tracking .06em) | 11 / 1.45 / 500, JetBrains Mono, `ink-muted` |
| Mono meta, numerals, keys | 12 to 13 / 1.45 / 400 to 500 |
| Small body, buttons in header | 13 / 1.45 / 500 to 600 |
| Body | 14 / 1.45 / 400 |
| Mobile body | 15 |
| Action text, headlines in panels | 16 / 1.45 / 600 |
| First action | 17 / 1.35 / 600 |
| Sheet and dialog titles | 17 to 18 / 700 |
| Run item title | 20 / 1.25 / 700 |
| Item title desktop / mobile | 24 / 1.2 / 700, tracking -0.015em; 22 / 1.22 |
| Run screen h1 | 28 / 1.15 / 700, tracking -0.02em |
| Prompt text | 12.5 / 1.55 / 400 mono (mobile 12) |

### Spacing, radius, borders, elevation

- Spacing is 4 px based: 4, 6, 8, 10, 12, 14, 16, 20, 24, 32, 40, 48, 56. All gaps and paddings scale by `--mc-d`.
- Radius: 3 (chips, key chips), 4 (desktop buttons, inputs), 6 (cards, prompt box, mobile buttons), 8 (notice panels, dialogs, first-item card), 12 top corners (mobile sheets), 999 (evidence chips).
- Borders: 1 px hairlines; 2 px solid `ink` for emphasis panels; 2 px dashed `line-missing` for a missing First action.
- **No shadows, gradients, blur or glow** anywhere. Separation is by borders and fill only.
- Layout constants: header 44, rail 248, decision pane `clamp(380px, 34%, 480px)`, run column 760, queue column 1120, mobile frame 390 x 844, mobile minimum hit target 44 (primary actions 48).

## Assets

None. No images or icons are used. Arrows are the characters ← and →. Key hints are text chips. Do not add icons or illustrations. Fonts: Hanken Grotesk and JetBrains Mono (Google Fonts, OFL).

## Not built in the prototype

Specified in `DECISIONS.md` and `GAPS.md`; build with the same tokens and components.

1. Pages for the other run items: decision cards (Q, P, AP) with the answer box and the P decision note; approval cards with Approve and Reject; outreach review cards (subject, body, verifier report, decision); lane packet completion with proof entry; nudge-due waiting cards; Eve-owned cards (never in a run).
2. The urgent-exception label on the item header and queue row ("Moved up: ...").
3. Feedback history with entries, including the 4,000-character entry and 12-entry case.
4. Long content: 609-character titles, 4,238-character descriptions, 2,506-character verifier reports.
5. Run reopening when a new eligible item appears after completion (state-map transition 9) and local-date rollover (transition 10).
6. An in-run "changed" banner for a different item than the open one (transition 6 for an unhandled card).
7. Previous and Next between built items. In the prototype they show a notice because only one item is rendered.
8. Persistence of run progress.

## Prototype scaffolding that must not ship

The Prototype control, the notices "opens on a later page of this prototype", the hard-coded run (7 items assembled from fixtures), the hard-coded change list, the hard-coded summary outcomes, the fixed date "Sat, Oct 3" and fixed freshness times, and the demo failure that shows on entering the Action failed state.

## Files

```
design_handoff_mission_control/
  README.md                       this file
  DECISIONS.md                    answered questions as implementation rules
  KEYBOARD.md                     keyboard map
  GAPS.md                         what the data contract does not support
  state-map/03-state-map.md       governing state map
  tokens/tokens.css               CSS variables (OKLCH with hex comments)
  tokens/tailwind.config.ts       Tailwind v3 theme extension
  tokens/theme.v4.css             Tailwind v4 @theme block
  tokens/tokens.json              machine-readable tokens
  reference/view-model.ts         view-model types
  prototype/Mission Control.dc.html          the prototype (needs support.js)
  prototype/Current Item Wireframes.dc.html  structural options
  prototype/support.js
  source/01-data-contract.md      backend rules (binding)
  source/02-fixtures.json         twelve records (binding)
  source/product-ux-guide.md      product UI rules (binding)
```

Fixtures used in the prototype: F04 (longest prompt; the displayed item), F06 (expired), F01, F02, F03, F05, F07, F08, F09, F10, F11, F12 (queue and run). Titles in the queue are verbatim from the fixtures.
