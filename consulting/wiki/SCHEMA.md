# Consulting Wiki Schema

Purpose: maintain a lightweight LLM-maintained consulting wiki that compounds across sources, prospects, clients, meetings, outreach, and research.

This is inspired by Karpathy's `llm-wiki` pattern, but scoped narrowly to JT's consulting pipeline. It does not replace MEMORY.md, lossless-claw, or the GBrain pilot.

## Layers

### 1. Raw sources
Immutable source files live where they already belong:
- `~/projects/jt-consulting-pipeline/clients/`
- `~/projects/jt-consulting-pipeline/prospects/`
- `memory/networking/`
- `memory/consulting/`
- selected `memory/analysis/`

Do not move or rewrite raw sources just to fit the wiki.

### 2. Compiled wiki
LLM-maintained markdown pages live in `consulting/wiki/pages/`.

Page types:
- `company-[slug].md` — durable facts, signals, pain, offers, contacts, status
- `person-[slug].md` — contact relationship, role, last touch, next action
- `offer-[slug].md` — reusable offer language, fit criteria, proof, objections
- `concept-[slug].md` — cross-client concepts like exception dashboards, judge layers, AI pilot governance
- `comparison-[slug].md` — synthesized analysis across companies/niches/offers

### 3. Navigation
- `consulting/wiki/index.md` catalogs pages with one-line summaries.
- `consulting/wiki/log.md` records ingests, updates, queries, and lint passes.


## Adoption rule
Do not create abstract wiki scaffolding without compiling at least one real entity, offer, or concept page from current consulting work. A wiki is only useful if it changes future recall or delivery.

## Ingest workflow
When a durable consulting source changes:
1. Read the source file.
2. Identify affected entities: company, person, offer, concept, status, objection, next action.
3. Update or create relevant wiki pages.
4. Add cross-links using `[[page-slug]]` style where useful.
5. Update `index.md`.
6. Append a `log.md` entry.
7. Use `consulting/entity-propagation/template.md` to ensure source/prospect/contact/pipeline/daily-note consistency.

## Query workflow
When answering a consulting/prospect recall question:
1. Check `consulting/wiki/index.md` if the topic likely belongs to consulting durable knowledge.
2. Read relevant pages.
3. If exact entity lookup is needed, use `scripts/gbrain-consulting-search.sh "Entity"`.
4. If the answer creates reusable synthesis, save it as a wiki page and log it.

## Lint workflow
Periodically inspect for:
- stale statuses
- conflicting company/contact facts
- orphan pages with no links
- concepts mentioned in several pages but missing their own page
- prospects with no next action
- offers with no proof or objection handling

## Guardrails
- No secrets, credentials, raw private chats, or sacred config files.
- Do not claim outreach was sent unless JT confirmed or tool evidence proves it.
- Do not create a wiki fact without a source path/date.
- Do not replace raw source files with wiki summaries.
- Keep wiki pages short enough to be useful: durable facts, links, contradictions, next actions.
