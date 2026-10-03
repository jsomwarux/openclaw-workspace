"use client";
// Focus handling for modal surfaces (KEYBOARD.md, Accessibility): keep Tab inside while open and
// give focus back to what had it before on close.
import { useEffect, useState } from "react";
import type { KeyboardEvent, RefObject } from "react";

const FOCUSABLE = "button:not([disabled]), [href], input:not([disabled]), textarea:not([disabled]), select, [tabindex]:not([tabindex='-1'])";

/**
 * Restores focus to the element that had it when the dialog opened. The opener is read during the
 * first render: by the time an effect runs, autoFocus inside the dialog has already moved focus to
 * the dialog's own button (review 2, finding 8).
 */
export function useRestoreFocus() {
  const [opener] = useState(() => (typeof document === "undefined" ? null : (document.activeElement as HTMLElement | null)));
  useEffect(() => () => {
    if (opener && document.contains(opener)) opener.focus();
  }, [opener]);
}

/** onKeyDown handler that keeps Tab and Shift+Tab inside the given container. */
export function trapTab(ref: RefObject<HTMLElement | null>) {
  return (event: KeyboardEvent) => {
    if (event.key !== "Tab") return;
    const focusable = ref.current?.querySelectorAll<HTMLElement>(FOCUSABLE);
    if (!focusable || focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };
}
