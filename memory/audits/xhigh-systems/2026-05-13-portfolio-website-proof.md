# XHigh Systems Audit — Portfolio / Website / Proof Automation

Date: 2026-05-13
Scope: jtsomwaru.com, portfolio updater queue/state, recent builds/proof sources, hidden Strategy Jobs pages, Mission Control tasks, public proof/anonymization gates.

## Before Grade
B+

The public website itself was mostly strong: current positioning is clear, client outcomes are anonymized, hidden Strategy Jobs pages exist, and the site builds. The automation layer had state drift: portfolio updater still treated the permanently banned B2B Account Service Agent and Glow Index as added public proof even though the current public `projects.ts` has neither slug.

## After Grade
A-

The proof layer is now safer and cleaner. Public site validation passes, hidden pages remain noindex and out of sitemap, stale MC site tasks are closed, and portfolio updater state no longer silently claims banned/missing public proof. Not A+ yet because the remaining Proof + Distribution audit still needs the actual next asset drafted/distributed, and Glow Index needs live-state verification before any portfolio decision.

## Inventory Findings

### Public site / portfolio
- Site project: `/Users/jtsomwaru/projects/jtsomwaru-com`.
- Current public portfolio has 23 project slugs and no duplicate slugs.
- `b2b-account-service-agent` is not present in `src/data/projects.ts`; only an orphan graphic remains in `src/components/project-graphics/index.tsx`, which matches the permanent exclusion note.
- `glow-index` is not present in `src/data/projects.ts` even though portfolio updater state previously marked it added.
- Client outcomes section uses anonymized language for Aya-style and sensitive property/family-office work; no Altmark/Yair/Matt names appear in public source content.
- Public `llms.txt` still names Aya as client proof. That may be intentional historical proof, but it is the most permission-sensitive public citation currently present.

### Hidden Strategy Jobs pages
- `/property-family-office-ai-ops` exists, is hidden from nav, and has `robots: { index: false, follow: false }`.
- `/guyana` exists, is repositioned around Local Content Operations Sprint, and has `robots: { index: false, follow: false }`.
- Neither hidden page is included in `src/app/sitemap.ts`.
- `npm run build` confirms both routes prerender successfully.

### Portfolio updater automation
- `agents/portfolio-updater/AGENT.md` correctly bans `b2b-account-service-agent` permanently.
- State drift existed: `state.json` still included `b2b-account-service-agent` under `addedSlugs` and `demandScoreCache`.
- State drift also existed for `glow-index`: state marked it added, but current public site has no matching slug.
- Queue included stale `added` status for the banned B2B card and unfinalized Glow Index entries.

### Proof/recent-build sources
- `memory/content/recent-builds.md` contains useful site/proof entries: Client Outcomes section, AI Operations Diagnostic reposition, blog library, Systems Overview, StreetEasy metric correction.
- `memory/north-star/proof-distribution-engine.md` correctly says Altmark should not be over-distributed before acceptance and proof capture.
- Remaining active MC task `Run first Proof + Distribution audit` is appropriate and should stay open until a concrete proof asset/post/snippet is drafted.

## Patches Applied

### Portfolio updater state hygiene
- Edited `agents/portfolio-updater/state.json`:
  - Removed `b2b-account-service-agent` from `addedSlugs`.
  - Removed `b2b-account-service-agent` from `demandScoreCache`.
  - Removed stale `glow-index` from `addedSlugs`.
  - Removed stale `glow-index` from `demandScoreCache`.
  - Added audit note dated 2026-05-13.

### Portfolio updater queue hygiene
- Edited `agents/portfolio-updater/queue.jsonl`:
  - Marked B2B Account Service Agent as `excluded_permanent` with final decision that it is permanently excluded and not present on public site.
  - Marked Glow Index entries as `review_needed_public_card_missing` with final decision to hold until current live state is verified.

### Portfolio updater run log
- Appended 2026-05-13 audit-housekeeping entry to `agents/portfolio-updater/update-log.md`.

### Mission Control task cleanup
- Closed stale completed site tasks:
  - `Property/Family Office: publish offer page copy into jtsomwaru.com draft branch` → done.
  - `Guyana: rewrite hidden jtsomwaru.com page around Local Content Ops Sprint` → done.
- Updated remaining high-priority proof task:
  - `Run first Proof + Distribution audit` remains todo/high with pointer to this audit and next first action.

## Validation
- `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md` completed before edits:
  - AGENTS.md: 27863 bytes
  - MEMORY.md: 19161 bytes
  - TOOLS.md: 13581 bytes
  - HEARTBEAT.md: 14330 bytes
- Read `/Users/jtsomwaru/projects/jtsomwaru-com/CLAUDE.md` before site inspection.
- `npm run lint` passed.
- `npm run build` passed.
- Build output included static routes for `/guyana`, `/property-family-office-ai-ops`, `/robots.txt`, `/sitemap.xml`, blog routes, and all `/work/[slug]` pages.
- Sitemap source check: `/guyana` and `/property-family-office-ai-ops` are not in `src/app/sitemap.ts`.
- Source grep check: no public Altmark/Yair/Matt names in site source; `Aya` appears in About/llms proof references.
- Slug check: 23 project slugs, no duplicates, `b2b-account-service-agent` absent from public project data.

## Remaining Blockers / Not A+ Items
1. **Proof asset still needs distribution.** The systems layer is cleaned up, but `Run first Proof + Distribution audit` should produce one proof snippet/post/deck insert. Recommended next proof: property/family-office exception layer snippet, or Altmark case study only after acceptance/permission.
2. **Glow Index public-card decision is unresolved.** Do not re-add automatically until current Replit/live state, metrics, and positioning are verified.
3. **Aya naming in `llms.txt` should be reviewed.** It may be acceptable, but public AI-search citation surface is more sensitive than anonymized homepage cards. If no explicit permission exists, change to anonymized wording.
4. **Portfolio updater still uses stale coding-agent instructions mentioning direct `claude --dangerously-skip-permissions`.** That conflicts with current gateway-freeze policy for main-session exec. It should be modernized in a separate skill/agent maintenance pass.

## Recommended Next Action
Run the remaining Proof + Distribution audit task by drafting one safe proof asset:

- If Altmark acceptance is confirmed: create referral-safe proof package plus LinkedIn case-study draft without confidential data.
- If not confirmed: create a property/family-office exception-layer sales proof snippet from the hidden offer page and public-safe language, explicitly avoiding client names and unverified metrics.

## Files Changed
- `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/state.json`
- `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/queue.jsonl`
- `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/update-log.md`
- Mission Control task records via local API.

## Site / Build Validation
- `npm run lint` passed.
- `npm run build` passed.
- No public deploy or git push performed.
