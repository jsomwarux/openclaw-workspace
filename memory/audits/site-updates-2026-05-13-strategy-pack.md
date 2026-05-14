# jtsomwaru.com Strategy Pack Site Updates — 2026-05-13

## Files changed
- `tasks/todo.md` — project task plan for this update.
- `src/app/property-family-office-ai-ops/page.tsx` — new hidden/noindex Property / Family Office AI Operations offer page.
- `src/app/guyana/page.tsx` — updated metadata for Local Content Operations Sprint; remains noindex/nofollow.
- `src/app/guyana/GuyanaContent.tsx` — rewrote hidden Guyana page from broad government AI infrastructure to local-content supplier operations sprint.
- `src/components/Hero.tsx` — sharpened homepage promise around expired/aged/changed/approval-needed workflows and updated anchor labels.
- `src/components/DiagnosticOffer.tsx` — reframed roadmap deliverables around exception inventory, data readiness, human approval, and logging.
- `src/components/ClientOutcomes.tsx` — sharpened anonymized sensitive-ops proof language without naming Altmark.
- `src/components/Services.tsx` — updated service copy around exception layers, local-first workflows, and human approval.
- `src/components/WhoIHelp.tsx` — updated family-office/property-ops copy around approval queues and audit trails.

## Routes added/updated
- Added: `/property-family-office-ai-ops`
  - Hidden from nav.
  - `robots: { index: false, follow: false }`.
  - Not added to sitemap.
  - Uses anonymized property/family-office language only; no Altmark name or public case-study framing.
- Updated: `/guyana`
  - Hidden from nav.
  - `robots: { index: false, follow: false }` preserved.
  - Not added to sitemap.
  - Repositioned as Local Content Operations Sprint for Guyana-connected suppliers.

## Validation
- `npm run lint` — passed.
- `npm run build` — passed.
- Source files touched are under the project-level 250-line source-file cap.

## Follow-up recommendations
- If these hidden pages are shared with warm prospects, consider adding a light lead-capture or Calendly CTA once JT confirms preferred intake path.
- Update `public/llms.txt` only if the hidden offer pages become public/indexable or the homepage positioning is intended as a durable SEO/GEO shift.
- Do not publish Altmark by name until acceptance, proof screenshots, payment/deposit status, and explicit permission are clean.
