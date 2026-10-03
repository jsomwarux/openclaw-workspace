"use client";
// Focus handling for modal surfaces (KEYBOARD.md, Accessibility): keep Tab inside while open and
// give focus back to what had it before on close.
import { useEffect } from "react";
import type { KeyboardEvent, RefObject } from "react";

const FOCUSABLE = "button:not([disabled]), [href], input:not([disabled]), textarea:not([disabled]), select, [tabindex]:not([tabindex='-1'])";

/** Restores focus to the element that had it when the dialog opened. */
export function useRestoreFocus() {
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    return () => {
      if (previous && document.contains(previous)) previous.focus();
    };
  }, []);
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
