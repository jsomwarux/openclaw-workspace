---
name: product-build-loop
description: "Run JT's product/app build loop for real features, apps, dashboards, and tools: plan, implement, test, quality pass, LARP assessment, production validation, and shipping discipline."
---

# Product Build Loop

Use for non-trivial product work in Vista, Nash Satoshi, Glow Index, jtsomwaru.com, Mission Control, dashboards, and new apps.

## Principle
The output must be real software, not a plausible-looking draft. Every build ends with evidence.

## Workflow
1. Read project `CLAUDE.md`, `AGENTS.md`, and any `tasks/lessons.md` before editing.
2. Create or update `tasks/todo.md` unless the change is a one-liner.
3. Confirm the build has a validation-gate artifact with a `BUILD` decision. If it is a new app/product wedge and no validation-gate artifact exists, stop and run the app-discovery loop first.
4. Freeze the data contract before implementation: entities, fields, event names, API shape, import/export formats, and analytics events. Treat this as the handoff boundary before frontend or backend build work.
5. Plan the smallest useful shipped version.
6. Implement in logical chunks.
7. Run the quality pass:
   - simplify
   - remove dead code and redundant comments
   - delete over-abstracted AI boilerplate
   - check for stubs, fake data, swallowed errors, and mocks of the code under test
8. Verify with real commands: build, typecheck, lint, tests, and UI/browser checks when relevant.
9. For visual shipped work, consider a 30-90s demo MP4/GIF or screenshot walkthrough before calling it content/proof-ready.
10. Update proof/recent-build/content/portfolio routing only when the build is substantive and verified.

## App-Specific Defaults
- Next.js: `npm run build` before any deploy or completion claim.
- Frontend work: use Playwright/screenshot verification for layout and interaction.
- Three.js/canvas: verify nonblank pixels and framing on desktop/mobile.
- React Native/Expo: run typecheck/lint/tests and inspect native constraints.
- Apps shared by Codex and Claude should keep reusable process in skills and project facts in `AGENTS.md`; symlink `CLAUDE.md` only when the repo needs both tools to read the same file.

## Quality Gate
Return:
- what changed
- what got simplified or removed
- what LARP/fake implementation risk was checked
- exact verification commands and results
- demo/proof asset path or explicit no-demo-needed reason
- remaining risks or blockers
