// Approve and Reject need a deliberate second action (DECISIONS 5.6, 12; KEYBOARD "No
// shortcut"). The confirm button takes focus when its panel opens, so without these guards one
// held Enter (auto-repeat) or a double tap on mobile could open and confirm in one gesture.

export const CONFIRM_ARM_MS = 400;

/** Auto-repeated Enter or Space keydowns from a held key never activate a confirm button. */
export function ignoreConfirmKey(event: { key: string; repeat: boolean }): boolean {
  return event.repeat && (event.key === "Enter" || event.key === " ");
}

/** A pointer click (detail > 0) inside the arming window is the tail of the opening tap. */
export function ignoreConfirmClick(event: { detail: number; openedAt: number; now: number }): boolean {
  return event.detail > 0 && event.now - event.openedAt < CONFIRM_ARM_MS;
}
