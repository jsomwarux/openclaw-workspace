---
name: qmd
description: Local BM25 + vector search and indexing CLI for workspace files and knowledge bases. Use when JT says "search my files", "find notes on", "search the workspace for", "index this", "local search", or when a task requires searching previously saved research, daily notes, or knowledge base entries. NOT for: web search (use web_search tool), X/Twitter search (use x-research skill), or searching live databases.
homepage: https://tobi.lutke.com
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["qmd"]},"install":[{"id":"node","kind":"node","package":"https://github.com/tobi/qmd","bins":["qmd"],"label":"Install qmd (node)"}]}}
---

# qmd

Use `qmd` to index local files and search them.

Indexing
- Add collection: `qmd collection add /path --name docs --mask "**/*.md"`
- Update index: `qmd update`
- Status: `qmd status`

Search
- BM25: `qmd search "query"`
- Vector: `qmd vsearch "query"`
- Hybrid: `qmd query "query"`
- Get doc: `qmd get docs/path.md:10 -l 40`

Notes
- Embeddings/rerank use Ollama at `OLLAMA_URL` (default `http://localhost:11434`).
- Index lives under `~/.cache/qmd` by default.
- MCP mode: `qmd mcp`.
