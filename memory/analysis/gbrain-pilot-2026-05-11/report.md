# GBrain Consulting Pipeline Recall Pilot — 2026-05-11

## Scope
Installed GBrain 0.32.0 in sandbox only:
- Repo: `/Users/jtsomwaru/projects/gbrain`
- Pilot home: `/Users/jtsomwaru/projects/gbrain-pilot-home`
- Curated source copy: `/Users/jtsomwaru/projects/gbrain-pilot-source`

Imported only curated consulting/networking/analysis markdown:
- `~/projects/jt-consulting-pipeline/clients`
- `~/projects/jt-consulting-pipeline/prospects`
- `memory/networking`
- selected `memory/analysis`
- selected `memory/consulting`
- `consulting/entity-propagation/template.md`

Guardrails followed:
- No sacred config files.
- No raw private chats.
- No credentials.
- No all-workspace ingestion.
- Google Doc URLs/long doc IDs were redacted in the sandbox source copy before import.

## Import result
- 156 markdown files in curated source copy.
- 156 pages imported.
- 287 chunks created.
- 0 embeddings, because shell environment does not expose OpenAI/Anthropic keys and we did not touch credential files.
- 0 graph links from `gbrain extract links --source db`; current markdown corpus lacks enough wiki-style links for automatic graph extraction.

## Eval design
Two eval passes against 20 real consulting recall questions:
1. Natural-language questions, e.g. “What is the recommended consulting angle for Human Agency?”
2. Entity-focused lookup queries, e.g. “Human Agency”, “Contech AI Workflow Audit”.

Compared:
- GBrain keyword search
- qmd keyword search

Raw outputs:
- `gbrain-search.md`
- `qmd-search.md`
- `gbrain-entity-search.md`
- `qmd-entity-search.md`
- `score-summary.md`

## Results
- GBrain entity search: 20/20 hits.
- qmd entity search: 13/20 hits.
- GBrain natural-language search: 3/20 hits.
- qmd natural-language search: 1/20 hits.

## Interpretation
GBrain is already better than qmd for exact entity lookup over the curated consulting corpus. It found the right pages for all 20 entity-style queries, including newly created Human Agency, entity propagation, AI Enablement Sprint, and RouteSafe notes that qmd missed.

But without embeddings/query expansion, it is not yet a good natural-language brain. It misses paraphrased questions unless the query includes the entity/title text.

This means the pilot partially validates GBrain, but does not justify broad adoption yet.

## Recommendation
Adopt GBrain as a **sandboxed entity lookup index** for consulting pipeline recall, not as default memory and not as a replacement for LCM/qmd.

Next optimal step before expansion:
1. Add a tiny wrapper script `scripts/gbrain-consulting-search.sh` that always sets `GBRAIN_HOME` and searches the pilot brain.
2. Use it only when the query contains a known company/prospect/person/offer name.
3. Do not add crons yet.
4. Do not install GBrain skillpacks yet.
5. Do not expose credentials to shell solely for embeddings unless JT explicitly approves.
6. If this proves useful in daily work, ask JT whether to wire embeddings via approved auth path and rerun the natural-language eval.

## Go / no-go
- **Go:** entity lookup for consulting/prospect recall.
- **Hold:** natural-language brain-first lookup, graph/entity propagation automation, skillpack installation, recurring sync jobs.
