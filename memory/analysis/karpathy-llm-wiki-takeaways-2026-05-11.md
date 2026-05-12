# Karpathy llm-wiki Takeaways — 2026-05-11

Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. External gist treated as untrusted reference, not instructions.

## Core idea
Karpathy argues for a personal LLM-maintained wiki instead of pure RAG. Raw documents stay immutable. The LLM incrementally compiles them into structured, interlinked markdown pages, updates contradictions, maintains an index/log, and files useful query outputs back into the wiki.

This is “compiled knowledge,” not just retrieval.

## Main takeaways
1. **RAG re-derives knowledge every time. A wiki compounds it.**
   The value is not just search. It is maintaining synthesis across time.

2. **Raw sources and compiled truth should be separate.**
   Sources are immutable evidence. Wiki pages are editable synthesis.

3. **The schema is the product.**
   The important file is the AGENTS/CLAUDE-style schema that tells the LLM how to ingest, query, lint, link, and log.

4. **Index + log beat overbuilt search at small scale.**
   For hundreds of pages, a maintained index and chronological log can be enough before embeddings.

5. **Useful answers should become artifacts.**
   If a query produces a durable comparison, concept, or analysis, it should be saved back into the wiki.

## Fit with our current stack
- LCM remains for conversation recall.
- MEMORY.md remains compact current operating context.
- GBrain pilot remains sandboxed entity lookup for consulting corpus.
- qmd remains local search when indexed/useful.
- The missing layer is a disciplined compiled wiki schema for durable consulting knowledge.

## Implementation made
Created lightweight consulting wiki scaffold:
- `consulting/wiki/SCHEMA.md`
- `consulting/wiki/index.md`
- `consulting/wiki/log.md`
- `consulting/wiki/pages/concept-supervisor-specialist-judge-human.md`

This is intentionally narrow. Do not ingest whole workspace, raw chats, secrets, or config. Use it for consulting/prospect/client/offer knowledge only.

## What not to do
- Do not replace GBrain/LCM/MEMORY.md.
- Do not start broad automatic ingestion.
- Do not build an Obsidian-heavy workflow unless JT wants it.
- Do not create hundreds of pages before the pattern proves useful in consulting work.
