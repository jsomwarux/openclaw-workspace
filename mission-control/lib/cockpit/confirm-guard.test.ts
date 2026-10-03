import { describe, expect, test } from "bun:test";
import { CONFIRM_ARM_MS, ignoreConfirmClick, ignoreConfirmKey } from "./confirm-guard";

// Review finding 1 and 3: one held Enter, or a double tap, must never open and confirm
// Approve or Reject. These guards sit on the confirm button itself.
describe("confirm buttons need a deliberate second action", () => {
  test("auto-repeated keydowns from a held key never activate the confirm button", () => {
    expect(ignoreConfirmKey({ key: "Enter", repeat: true })).toBe(true);
    expect(ignoreConfirmKey({ key: " ", repeat: true })).toBe(true);
    expect(ignoreConfirmKey({ key: "Enter", repeat: false })).toBe(false);
    expect(ignoreConfirmKey({ key: "j", repeat: true })).toBe(false);
  });

  test("a pointer tap that lands within the arming window after the panel opens is ignored", () => {
    expect(CONFIRM_ARM_MS).toBe(400);
    expect(ignoreConfirmClick({ detail: 1, openedAt: 1000, now: 1000 })).toBe(true);
    expect(ignoreConfirmClick({ detail: 2, openedAt: 1000, now: 1399 })).toBe(true);
    expect(ignoreConfirmClick({ detail: 1, openedAt: 1000, now: 1400 })).toBe(false);
  });

  test("a keyboard activation (click detail 0) is a separate keypress and is never delayed", () => {
    expect(ignoreConfirmClick({ detail: 0, openedAt: 1000, now: 1001 })).toBe(false);
  });
});
