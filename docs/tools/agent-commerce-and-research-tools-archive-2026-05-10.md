# Agent Commerce and Research Tools Archive — 2026-05-10

## Cloudflare Browser Rendering — /crawl (preferred for full-site crawls)
- Replaces Firecrawl for full-site ingestion. One API call crawls an entire site.
- Async: POST to start → receive job_id → GET to poll results
- Free during beta for `render: false` (static sites). Headless/JS rendering billed under Workers pricing.
- Supports: HTML, Markdown, JSON output | incremental re-crawls via `modifiedSince` | depth/limit/pattern controls
- **Primary use cases:** H.C. Oswald RAG ingestion (Shopify catalog), prospect full-site crawls in research-agent
- Endpoint: `POST https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl`
- Auth: `Authorization: Bearer <CF_API_TOKEN>` | Credentials in `~/.config/env/global.env` (CF_ACCOUNT_ID, CF_API_TOKEN)
- Quick example (static site, markdown):
  ```
  curl -X POST 'https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl' \
    -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' \
    -d '{"url":"https://example.com","formats":["markdown"],"render":false,"options":{"includePatterns":["https://example.com/products/**"]}}'
  ```
- Structured extraction (JSON + prompt): add `"formats":["json"],"jsonOptions":{"prompt":"Extract services, tech stack, key contacts"}`
- Docs: https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/

## Scrapling
- Library: `pip install "scrapling[ai]"` — adaptive Python web scraping framework
- NOT a native OpenClaw feature — used inside Python scripts exec'd by OpenClaw
- Key classes: `Fetcher` (fast HTTP + TLS fingerprint spoofing), `StealthyFetcher` (Cloudflare bypass), `DynamicFetcher` (Playwright browser automation)
- Adaptive selectors: `page.css('.selector', auto_save=True)` — auto-relocates elements when site structure changes
- MCP server: `scrapling.readthedocs.io/en/latest/ai/mcp-server/` — wire as tool in research-agent for consulting pipeline
- Docs: scrapling.readthedocs.io | GitHub: github.com/D4Vinci/Scrapling
- Use case: StreetEasy scraper resilience (upgrade plan: memory/analysis/scrapling-evaluation-2026-03-02.md)

## OpenRouter
- Status: ✅ Active | Profile: openrouter:default
- Routing: All models → openrouter/provider/model (no direct Anthropic since April 2026 ban)
- **Model Tiering (JT's system):**
  - **Default / everything:** `openrouter/minimax/minimax-m2.7` — $0.07/$0.20 per M input/output, handles most work
  - **Upgrade when needed:** `openrouter/anthropic/claude-sonnet-4-6` — ~$3/$15 per M, for complex reasoning
  - **Precision / complex code:** `openrouter/anthropic/claude-opus-4-6` — ~$15/$75 per M, for n8n workflow generation and complex multi-file Python (quality × no-rework ROI)
  - **Lightweight crons:** `openrouter/deepseek/deepseek-chat-v3-0324` — $0.03/$0.10 per M, for simple data aggregation
  - **Fallback:** `openrouter/deepseek/deepseek-chat-v3-0324`
- Key models available: openrouter/openai/gpt-4o | openrouter/x-ai/grok-3 | openrouter/google/gemini-2.5-pro | openrouter/google/gemini-2.5-flash-preview | openrouter/google/gemini-3.1-flash-lite-preview | openrouter/google/gemini-3-pro-preview | openrouter/moonshot/kimi-k2 | openrouter/deepseek/deepseek-r1
- **Image generation:** `google/gemini-2.5-flash-image` (NB1, GA) | `google/gemini-3.1-flash-image-preview` (NB2, $0.50/$3 per M) — NB2 adds visual grounding (searches web for real locations/species before generating), extreme aspect ratios (1:4, 1:8 for banners), 512px option, thinking mode toggle (off by default). 95% of Pro quality. Cost workflow: Batch API (50% discount) → 5-8 variations at 512px → upscale winner only. Thinking ON only for complex infographics or visual grounding + spatial reasoning.
- Gemini 2.5 Pro: $1.25/$10 per M tokens, 1M context, flat pricing — use for large doc analysis (>100K tokens), RAG ingestion. Gemini 3-pro-preview: $2/$12 (≤200K) or $4/$18 (>200K) — better reasoning but expensive at large context, not worth it for doc ingestion.
- Gemini 3.1 Flash-Lite: $0.25/$1.50 per M tokens, 1M context, 2.5x faster than 2.5 Flash, 45% faster output — use for cheap high-volume tasks: KB reads, content batch gen, summarization, quick lookups. Replaces gemini-2.5-flash-preview for non-reasoning tasks. Verified routing: google/gemini-3.1-flash-lite-preview-20260303.
- Full list: https://openrouter.ai/models | Experiments log: memory/costs/model-experiments.jsonl
