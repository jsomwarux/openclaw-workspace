# Product UX Guide
*v0.2 seed, July 2026. The companion promised in design guide v1.5, now started. Covers what the marketing files exclude: dashboards, product UI, data tables, forms, multi-step flows, onboarding, empty and loading and error states, and UI microcopy. Built the same way the design guide was built: iteratively, prompted by real product problems. This seed covers only what active work needs; expand per problem, and apply the pruning rule from design-core.md. Always pair with design-core.md.*

---

## 1. Scope

Applies to operator-facing product surfaces: construction and property dashboards, client tooling, internal apps, consumer app product UI, and any multi-state flow. Does not cover marketing pages (patterns-web.md, b2b-trust.md) or video (patterns-video.md). Mobile-native gesture and navigation-stack patterns remain out of scope until a real project forces them in.

Default accessibility tier for client work: WCAG AA strict, same checklist as design-core.md non-negotiable 3.

---

## 2. The three operator principles

These came from shipped dashboard work and its failure modes. They outrank aesthetic preferences on every product surface.

**1. Verbatim data, never synthesis.** The ingestion and display layers render exactly what the source of truth says. Every displayed number, name, and status must be traceable to a specific source cell or record. A display layer that synthesizes plausible values instead of reading verbatim is a defect even when the output looks reasonable, because the operator cannot tell the difference. In briefs, state it explicitly: read verbatim from the source rows; if a value is missing, show that it is missing; never infer or fill.

**2. Summarize, don't enumerate.** A view answers the operator's question first: counts, exceptions, deltas, and status rollups at the top; raw rows behind a click or below the fold. Rendering every row as the primary view pushes the thinking work back onto the operator, which is the work the tool exists to remove. The test for any view: can the operator act after reading only the top block.

**3. Plain language in the UI.** No developer vocabulary reaches an operator's screen: no null, undefined, payload, fetch failed, or snake_case labels. "Last checked," not "last_run_ts." Error copy states what happened and what to do next in operator terms. Labels describe operator meaning, not data structure. Run a plain-language pass as an explicit step before any handoff, and check navigation labels against the operator's vocabulary, not the codebase's.

---

## 3. States are designed, not defaulted

Every view specifies four states explicitly in the brief: loading, empty, error, and partial.

1. Loading: skeleton or progress indication that matches the layout it resolves into; no layout shift on resolve.
2. Empty: says why it is empty and what action creates content. An empty table with no explanation reads as broken.
3. Error: what failed in plain language, what the operator can do, and who to contact if nothing works. Never a dead end, never a raw error string.
4. Partial: when some sources loaded and others didn't, show what loaded and mark what didn't. Silent partial data violates principle 1.

---

## 4. State maps for multi-state flows

Anything that isn't a single static screen gets `/interaction-design:map-states` first, and the state map is a required attachment in the Claude Design brief (this is discovery field 0c routing here). One state map per app or flow, maintained as the shared mental model between Claude Design and Claude Code. Multi-state candidates: submit-and-resolve cycles, comparison flows, approval queues, anything with optimistic updates.

---

## 5. Dashboard information hierarchy

1. Exceptions first: what needs action today sits at the top, before status and before charts.
2. Status second: rollups with consistent, boring vocabulary (OK, Needs attention, Overdue). Color reinforces the word, never replaces it.
3. Detail third: drill-downs, raw tables, history.
4. Visual weight scales with money and legal risk, not with recency or data volume.
5. Charts answer one question each; a chart that needs a paragraph to interpret becomes a table or a number.

## 6. Tables

1. Column order equals decision order; the columns the operator acts on come first.
2. Right-align numerics, human-format timestamps with timezone, and keep units visible.
3. Totals and counts visible without scrolling when the decision depends on them.
4. Row-level actions are explicit verbs, not icons alone.

## 7. Forms

1. Validate inline at the field, preserve all input on error, and never clear a form because one field failed.
2. Sensible defaults over blank fields wherever a default is defensible.
3. Destructive actions get a confirmation that states the consequence in plain terms, not "Are you sure?"
4. Multi-step forms show position and allow backward movement without loss.

## 8. Handoff

Same discipline as the marketing side: tokens file per product via `/design-systems:tokenize`, `/design-ops:handoff` at the end of every Claude Design session, and the state map plus states specification attached to what Claude Code receives.

---

## 9. Active-work notes

**Construction progress dashboard expansions (client-A-type work).** The three operator principles above are the standing corrections for this codebase family: ingestion must read sheet rows verbatim, views summarize before they enumerate, and a plain-language and navigation pass runs before delivery. The current build's spec document is the source of truth for tab-level requirements; this file governs how those tabs behave and read.

**Agency engagement UI (client-B-type work, if closed).** Dashboards and AI-insight surfaces for a client-of-clients context add two constraints: per-client isolation must be visible in the UI (the operator should always know which client context they are in), and AI-generated insight is labeled as such with its source and freshness visible, per principle 1.

---

## 10. Motion for product surfaces

Product motion follows different physics than marketing motion. The marketing tiers in patterns-web.md are explanatory and can run slow; an operator dashboard is used hundreds of times a day and cannot. The rules below derive from the emil-design-eng skill (install per design-core.md section 7; run its review-animations companion as a gate before any interactive client handoff).

**1. Frequency decides whether anything animates.** Actions seen 100 or more times a day, and anything keyboard-initiated, get no animation at all. Actions seen tens of times a day get minimal motion. Occasional surfaces (modals, drawers, toasts) get standard motion. Rare or first-time moments (onboarding, empty-state education) can carry delight. Applied to our dashboards: tab switches, filters, row expansion, and keyboard shortcuts stay instant; a first-run walkthrough may animate.

**2. Every animation needs a purpose it can state:** spatial consistency, state indication, feedback, explanation, or preventing a jarring change. "Looks nice" on a daily-use surface is a defect.

**3. Timing budgets.** Press feedback 100-160ms, tooltips 125-200ms, dropdowns 150-250ms, modals and drawers 200-500ms, and everything UI stays under 300ms unless it has a stated reason. Never ease-in on UI; entrances and exits use strong ease-out curves (see the product-grade curves in the patterns-web easing table). Constant motion (spinners, progress) is linear.

**4. Physical correctness.** Pressable elements get scale(0.97) on active with a 160ms ease-out transition. Nothing enters from scale(0); start at scale(0.95) plus opacity. Popovers, dropdowns, and tooltips scale from their trigger via transform-origin; modals stay centered. Once one tooltip is open, adjacent tooltips open instantly.

**5. Interruptibility and performance.** Rapidly triggered elements (toasts, toggles) use CSS transitions, not keyframes, so they retarget instead of restarting. Animate transform and opacity only; animating width, height, margin, or top is a finding. Do not drive child transforms by updating a CSS variable on a parent in hot paths.

**6. Accessibility.** prefers-reduced-motion means gentler, not zero: keep opacity and color cues, drop movement. Hover motion gates behind `@media (hover: hover) and (pointer: fine)` so touch devices don't false-positive. These sit on top of the AA checklist in design-core.md.

**7. Product-UX-safe sourcing.** From sourcing.md: AutoAnimate for list add/remove/reorder in tables and queues (one line, honors reduced motion); Kibo UI for app composites (Gantt, Kanban, calendar, tables); HeroUI when a product wants a full coherent kit; SHSF UI for micro-interaction polish; mapcn for property portfolio and unit maps on MapLibre, directly relevant to property-ops dashboards; Make It Animated as the React Native reference for Expo app work, subject to project gates. Everything else in sourcing.md sections 4, 6, and 7 defaults to banned on operator surfaces.
