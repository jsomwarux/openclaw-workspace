# UX / UI Architecture Guidelines

Use this skill when JT says "design this," "build a new dashboard," "what is our UI aesthetic," or when a sub-agent is tasked with originating a new interface (web app, iOS, or dashboard).

## Core Aesthetic: "Systems Architect"
The guiding design philosophy is cold logic, minimal friction, and premium execution.
*   **Anti-pattern:** Social media feeds, bloated dashboards, redundant labels, gamified engagement metrics (like Letterboxd).
*   **Pattern:** Bloomberg Terminals, Stripe dashboards, minimalist data-tracking.

### 1. Typography & Hierarchy
*   **The Rule:** Content structure > visual decoration.
*   **Font Choices:** Inter, SF Pro, or pure Monospace for data. No decorative serifs.
*   **Sizing:** 
    *   Headers: Bold, highly contrasted size (rarely used).
    *   Data/Numbers: Monospaced or tabular lining.
    *   Labels: Muted (text-zinc-500 or gray), ultra-small context.
*   **Density:** Keep data dense where appropriate, but pad structural borders lavishly.

### 2. Color Palette (Dark Mode Default)
*   **Primary Backgrounds:** Absolute black (`#000000`) or deep zinc (`#09090b`).
*   **Surface / Panels:** Subtle elevation (e.g., `#18181b` for borders, `#27272a` for hover states).
*   **Text:** High contrast white for primary data, `#A1A1AA` for secondary text.
*   **Accents:** Teal (`#14b8a6`) or Indigo (`#6366f1`) for actionable elements only. Never use solid block colors for backgrounds; rely on gradients or subtle borders to indicate hierarchy.

### 3. Spacing & Borders
*   Use a rigid 4pt grid system.
*   Borders should be hairline (1px solid border-white/10).
*   Shadows are obsolete in dark mode; use borders and background lightness to distinguish layers.
*   Padding should be generous around container edges (p-6 or p-8) and tight between actual data rows (gap-2 or gap-3).

### 4. Interactive Elements (Frictionless)
*   No multi-step modals unless legally required. Use sliding side-panels or inline expansion.
*   Inputs should be borderless with subtle bottom strokes, or use ultra-faint borders until focused.
*   Feedback must be immediate but silent (subtle flash or icon change, no popups saying "Successfully saved!").

### Execution Checks
Before submitting a design or triggering a coding agent:
*   [ ] Does this look like a tool built for a professional, or a consumer app built for a teenager?
*   [ ] Can I remove one more divider or label and still have it make sense?
*   [ ] Is the data the focal point of the screen?
