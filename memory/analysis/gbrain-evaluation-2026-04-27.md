# GBrain Evaluation — 2026-04-27

## Summary
GBrain is a Postgres/PGLite-native personal knowledge brain for agents. It is not just markdown search. Its core value is a typed knowledge graph layered on top of markdown pages, chunks, embeddings, keyword search, source attribution, and timeline/compiled-truth pages.

## What it does
- Imports markdown/code/files into a brain DB.
- Stores pages with `compiled_truth` (current synthesis) and `timeline` (append-only evidence).
- Chunks content and supports keyword search + vector search + reciprocal-rank fusion.
- Extracts typed links between pages (people, companies, meetings, ideas, sources, code refs).
- Uses graph traversal/backlinks to improve relational recall.
- Provides MCP/CLI surfaces and a skillpack for agent workflows.
- Includes Minions: durable deterministic background jobs for brain ingestion/sync tasks.
- Includes Skillify/routing eval tooling for skill quality and routing gaps.

## Eval evidence
BrainBench compares GBrain against grep-only, vector-only, and vector+keyword RRF baselines on a fictional 240-page personal corpus.
Reported headline from gbrain-evals:
- GBrain: P@5 ~49.1%, R@5 ~97.9%
- Vector+grep RRF: P@5 ~17.8%, R@5 ~65.1%
- Grep-only: P@5 ~17.1%, R@5 ~62.4%
- Vector-only: P@5 ~10.8%, R@5 ~40.7%

Interpretation: the graph layer matters most for relational queries — “who do I know at X,” “what companies connect to Y,” “what did this person say over time,” etc. It is less obviously superior for simple keyword lookup.

## Best use cases
- Large personal knowledge bases: thousands of markdown notes, meetings, emails, people/company dossiers.
- Relationship memory: people, companies, deals, investors, conversations, source trails.
- Consulting/business development: prospect dossiers, outreach history, client context, meeting notes.
- Original ideas/content: ideas with provenance and evolution over time.
- Codebase knowledge: code chunks, definitions, references, call graph-ish lookup.
- Deterministic ingestion jobs where LLM subagents are wasteful.

## Fit with JT/Eve stack
Current stack already has:
- Lossless-claw for conversation recall.
- MEMORY.md/daily notes for operating memory.
- qmd installed for local BM25/vector search, but currently indexes 0 files.
- Ad hoc knowledge DB and many markdown files.

GBrain would not replace lossless-claw. LCM is for conversation transcript recall. GBrain is better suited to durable world/project knowledge: people, companies, prospects, client history, research docs, content ideas, and source-attributed dossiers.

## Recommendation
Do not full-migrate immediately. Optimal path is staged adoption:
1. Immediate low-risk fix: configure qmd to index workspace/project markdown so local search stops being dead weight.
2. Pilot GBrain on one high-value domain: consulting pipeline + networking/contact notes + client/prospect research.
3. If pilot improves recall materially, expand to content bank and project docs.
4. Do not ingest secrets, credentials, raw private chat logs, or sacred config files.

## Why staged, not full send
- GBrain is powerful but operationally heavier than qmd: database, migrations, embeddings, schema discipline, and new habits.
- Our AGENTS.md is near budget, so adding broad new recall rules there would increase fragility.
- The current urgent gap is not “no graph brain”; it is “our qmd has zero indexed files.”
- GBrain shines once we have entity-rich corpora. Consulting/client/prospect knowledge is the best pilot.

## Candidate implementation plan
- Create a new Mission Control task: “Pilot GBrain for consulting pipeline recall.”
- Install GBrain in a sandbox or isolated workspace first.
- Import only curated markdown: `~/projects/jt-consulting-pipeline/clients`, `memory/networking`, and selected `memory/analysis` docs.
- Run BrainBench smoke or a custom eval against 20 real questions Eve should answer.
- Keep LCM as-is for chat recall.
- Add a small “brain-first lookup” rule only after pilot proves value.
