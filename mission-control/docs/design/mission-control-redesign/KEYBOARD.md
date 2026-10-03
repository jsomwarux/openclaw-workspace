# Keyboard map

Desktop only. One window-level `keydown` listener. Keys are matched on `event.key`, lower-cased, except `?`.

## Keys

| Key | Action | Notes |
|---|---|---|
| `J` | Next item | Works while an item is shown, including resolved items |
| `K` | Previous item | |
| `C` | Complete | Opens the Complete confirm panel. `Enter` confirms, `Esc` cancels. Does not complete directly |
| `D` | Defer | Opens the Defer confirm panel. `Enter` confirms, `Esc` cancels |
| `E` | Open evidence | Opens the first web link in a new tab. With none, shows "Nothing to open: this item has no evidence links." |
| `Q` | Queue | Toggles the full queue view. Pressing `Q` inside the queue closes it |
| `?` | Shortcuts overlay | Works on every desktop screen, including run start, resume, summary and empty run |
| `Esc` | Close or cancel | Closes the first of: queue sheet, shortcuts overlay, queue view, open confirm panel or form |
| `Enter` | Confirm | Confirms an open Complete, Defer or Reject panel. On Run start it starts the run. On Run resume it acknowledges and resumes. If a button has focus, `Enter` activates that button natively and the global handler does nothing |

## No shortcut

- **Approve and Reject have no single-key shortcut.** Two ways to act, both deliberate:
  1. Click the button, then confirm in the panel (click the confirm button or press `Enter`).
  2. Tab to the button, press `Enter` to open the confirm panel, press `Enter` again to confirm.
  No letter key, chord or shift-key opens or confirms either action. Reject cannot be undone and its confirm button is `ink`, not accent.
- **Start, Block, Copy prompt, Pause run and Refresh** have no shortcut.

## When keys are ignored

- Any modifier held (`Ctrl`, `Cmd`, `Alt`): ignored.
- Focus in an input, textarea or editable element: all shortcuts ignored except `Esc`.
- Shortcuts overlay open: everything ignored except `Esc` (closes it).
- Queue view open: everything ignored except `Q`, `?` and `Esc`.
- Paused states (stale data, changed underneath me until acknowledged, invalid card, loading, expired, failed action until dismissed or retried): `C` and `D` do nothing. `J`, `K`, `Q`, `E`, `?` still work.
- Item already resolved (done, rejected, parked, deferred): `C` and `D` do nothing.
- Run screens (start, resume, summary, empty run): only `Enter` (where defined), `?` and `Esc` act.
- Recommended addition, not in the prototype: ignore `event.repeat` so holding a key cannot open a panel repeatedly.

## Discoverability

- Key chips on the buttons they trigger: Queue `Q`, Complete `C`, Defer `D`, Previous `K`, Next `J`, Shortcuts `?`. A display setting can hide chips; they are shown by default.
- The overlay lists every key and states the Approve and Reject rule. Its footer: "Approve and Reject have no shortcut. Click the button, then confirm with Enter or a click. Reject cannot be undone."

## Accessibility

- All controls are real buttons with visible focus rings (see "Focus ring" in the README; default 2 px accent, offset 2).
- Confirm panels use `role="alertdialog"` and move focus to the confirm button on open (`autoFocus`). On cancel, return focus to the button that opened them.
- The overlay uses `role="dialog"` with `aria-modal="true"`; trap focus and restore it on close.
- Status lines, notices and failure panels use `role="status"` (polite) or `role="alert"`.
- The current queue row has `aria-current="step"`.
