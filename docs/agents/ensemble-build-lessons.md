# Ensemble Build Lessons — Python Engine + OpenRouter

Lessons from operational experience building Python FastAPI ensemble ranking pipelines.
Read this before starting any new ensemble ranking build.

## Python Engine (Mac mini, Python 3.9)

**Python 3.9: no `X | None` union type hints at runtime.**
`asyncio.Semaphore | None = None` throws `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`. Mac mini runs Python 3.9 — always use `Optional[X]` from `typing` or plain `object` for nullable variables. The `X | Y` syntax is Python 3.10+ only.

**Use `nohup` + log file for engine persistence during development.**
`nohup python3 -m uvicorn main:app --port 8001 --host 127.0.0.1 > /tmp/glow-engine.log 2>&1 &`
Engine dies if terminal closes otherwise. Always check `/tmp/glow-engine.log` for silent errors — the engine can start successfully but fail on first request with no visible output. Set up a LaunchAgent only after end-to-end flow is confirmed.

**asyncio.Semaphore is the correct pattern for bulk concurrency control.**
Create semaphore at startup in lifespan context manager. Push requests to a FIFO list. Spawn a queue worker task on each `/analyze` call — worker pops from list inside `async with semaphore`. MAX_CONCURRENT = 2 default; only raise to 3 if OpenRouter rate limits aren't being hit.

**Always bind uvicorn to `127.0.0.1`, not `localhost`.**
n8n may resolve `localhost` as `::1` (IPv6) while uvicorn listens on IPv4 only. HTTP Request to `localhost:8001` fails silently; `127.0.0.1:8001` works. Use explicit IP everywhere.

## OpenRouter Model Rules

**Always verify model IDs before building — dot vs hyphen matters.**
OpenRouter uses dots for version separators: `anthropic/claude-sonnet-4.6`, `anthropic/claude-opus-4.6`. NOT hyphens. GPT-5 does not exist on OpenRouter — use `openai/o3`. Always run `curl https://openrouter.ai/api/v1/models | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data'] if 'provider' in m['id']]"` to verify IDs before finalizing config.

**ALL OpenRouter responses use `choices[0].message.content` regardless of model.**
OpenRouter normalizes Anthropic, Google, and xAI responses to OpenAI format. Never use model-native extractors (`content[0].text` for Claude, `candidates[0].content.parts[0].text` for Gemini). One extractor for all.

**Gemini rejects `response_format: {"type": "json_object"}` via OpenRouter.**
Causes `finish_reason: "length"` with content `"OK"` — a silent failure that looks like truncation. Remove `response_format` from all Gemini calls. Only OpenAI models (o3, gpt-*) support this parameter through OpenRouter.

**Model config (confirmed March 2026, ~$0.78/analysis for 13 LLM calls):**
- OpenAI: `openai/o3` ($2/$8 per M) — reasoning model, max intelligence
- Google: `google/gemini-2.5-pro` ($1.25/$10 per M) — confirmed available, cheaper than 3.1-pro-preview
- Anthropic: `anthropic/claude-sonnet-4.6` ($3/$15 per M) — dot separator required
- xAI: `x-ai/grok-4.20-beta` ($2/$6 per M) — cheaper than grok-4, 2M context

## Prompt Architecture

**Port prompts from scratch for each new use case — never copy-paste and search-replace.**
When the Nash Satoshi skincare prompts were audited, crypto-specific language ("exit liquidity," "coordination game," "Category Heat," "lifecycle phase modifiers") had survived a find-replace pass and were still driving scoring. This produced nonsense results: a well-formulated moisturizer lost points for being "at peak phase." Write new prompts from the domain up, not from a crypto prompt down.

**Prompt field names must match validator field names end-to-end.**
If prompts output `base_score`, validators must check `base_score`, stage4 must read `base_score`, and the frontend type must include `base_score`. Any mismatch silently produces `null` or `NaN` — not an error. Audit the full chain (prompt → parse → validate → aggregate → callback → frontend) before the first real run.

**When changing output schema, update every layer simultaneously:**
1. Prompt (what fields the LLM outputs)
2. `validate_score()` in validators.py (which field to check)
3. `stage4_aggregate.py` score extraction + analyses builder
4. Callback payload construction
5. Frontend type definitions + components

Missing any one layer = silent breakage. The system won't error — it'll just show NaN or a blank verdict.

**Derive frontend verdicts from explicit fields, not text scanning.**
When backend passes `consumer_verdict: "BUY_IT"` in each analysis object, the frontend should read that field directly. Scanning reasoning text for verdict keywords is fragile — the exact string may not appear, or may appear in a negation ("not BUY_IT"). Always pass structured verdict fields through the callback payload and read them explicitly.

## Callback + Integration

**A 404 from a secret-protected callback looks identical to a missing route.**
Test with the correct secret before debugging the route. The Replit callback returns 404 intentionally when the secret doesn't match — not because the endpoint is missing.

**n8n jsonBody double-serialization: use `contentType: raw` when passing pre-serialized JSON.**
`specifyBody: "json"` + `jsonBody: "={{ JSON.stringify(...) }}"` causes n8n to double-wrap the string. Fix: switch to `contentType: "raw"`, `rawContentType: "application/json"`, `body` set to the stringify expression. Sends the raw string directly.

**Frontend text-extraction for pros/cons/quick-take is fragile — structured fields are better.**
Extracting pros, cons, quick takes, and dupe recommendations from raw LLM reasoning text using regex patterns works as a fallback, but misses a lot and produces inconsistent results across models. The right architecture: prompt the LLM to output these as explicit structured fields (key_findings: [], red_flags: [], quick_take: "...", best_dupe: "...") and pass them through the callback payload. Then the frontend reads fields, not scraped text. The regex approach should only exist as a fallback for legacy data.

**Never truncate user-facing content at an arbitrary character count.**
Truncating bullet points at 120 chars with "..." is worse than showing the full sentence — it signals incomplete information and destroys trust in a product review context. If a sentence is too long for the layout, let it wrap. Only truncate preview cards (product tiles, search results) where space is physically constrained, and only with a "Read more" affordance.

**UX copy must be accurate to what's actually on the page.**
"Read the breakdown to make sure it fits your skin" promises a breakdown section. If no breakdown section exists, the copy is misleading. Never write subtext that references content that isn't rendered. Audit every piece of helper text against the actual page layout before shipping.
