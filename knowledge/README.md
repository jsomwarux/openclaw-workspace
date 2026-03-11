# Eve's Knowledge Base

SQLite-backed knowledge store with vector embeddings for semantic search.

## Location
- **Database:** `~/.openclaw/workspace/knowledge/kb.sqlite`
- **CLI:** `~/.openclaw/workspace/knowledge/kb.ts`

## Quick Start

```bash
cd ~/.openclaw/workspace/knowledge

# Add something
bun kb.ts add --title "GPT-5 released" \
              --content "OpenAI released GPT-5 with 10x context window..." \
              --category tech \
              --tags "ai,openai,llm"

# Search semantically
bun kb.ts search "new OpenAI language models"

# Search with category filter
bun kb.ts search "bitcoin price trend" --category crypto

# Index your daily notes
bun kb.ts index --dir ~/.openclaw/workspace/memory --source daily-notes

# Index research folder recursively
bun kb.ts index --dir ~/.openclaw/workspace/memory/research --source research --recursive

# List all business items
bun kb.ts list --category business --limit 20

# Full item view
bun kb.ts show 42

# Delete
bun kb.ts delete 42

# Stats
bun kb.ts stats
```

## Categories

| Category    | Use for                                              |
|-------------|------------------------------------------------------|
| `business`  | Consulting clients, market research, competitor intel   |
| `tech`      | AI tools, models, APIs, dev discoveries              |
| `crypto`    | Market analysis, trends, token research              |
| `personal`  | Health, goals, habits, reflections                   |
| `projects`  | Project-specific notes, decisions, progress          |

## Search Modes

- `hybrid` (default) — combines semantic + keyword, re-ranks results
- `semantic` — vector cosine similarity only (meaning-based)
- `keyword` — FTS5 full-text search only (exact terms)

## Embedding Model

First search/add triggers a one-time model download:
- **Model:** `Xenova/all-MiniLM-L6-v2` (384 dims, quantized ~22MB)
- **Cache:** `~/.cache/xenova/`
- **Inference:** Local, no API needed

## Database Schema

```sql
knowledge_items
  id, title, content, summary, category, tags (JSON), source, source_path,
  created_at (unix), updated_at (unix)

embeddings
  item_id, embedding (Float32Array blob), model, dims, embedded_at

knowledge_fts (FTS5 virtual table — auto-synced via triggers)

indexed_files
  path, mtime, indexed_at, item_count  — prevents re-indexing unchanged files
```

## Environment

Set `KB_PATH` to override the database location:
```bash
KB_PATH=/custom/path/kb.sqlite bun kb.ts stats
```

## Auto-Indexing Tips

- Run `bun kb.ts index --dir ~/.openclaw/workspace/memory` periodically to absorb new daily notes
- Use `--recursive` for nested research folders
- The indexer splits files by `##` headings — each section becomes a separate item
- Re-indexing the same unchanged file is safe (skipped automatically by mtime check)
