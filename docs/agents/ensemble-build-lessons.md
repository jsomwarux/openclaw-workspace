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

## 2026-04-05 — Glow Index callback URL bug

**Problem:** All 66+ analyses ran to completion but zero scores landed in the DB. Engine showed `callback_url: NOT SET` for every job.

**Root cause:** `request.nextUrl.origin` on Replit returns an internal URL unreachable from external services. The engine received an empty callbackUrl and skipped all callbacks.

**Fix:** Use `process.env.NEXT_PUBLIC_APP_URL || process.env.SITE_URL || request.nextUrl.origin` in any endpoint that builds a callback URL for an external service to call back into.

**Required Replit Secret:** `NEXT_PUBLIC_APP_URL=https://[app-name].replit.app`

**Pre-flight checklist for any new ensemble niche:**
1. Trigger 1 product via `/api/trigger-analysis`
2. Check engine `/status` — confirm `callback_url` shows the real public URL
3. Wait for score to land in DB
4. Only then trigger full batch

**Never test callback endpoints with real product IDs** — will corrupt the product record in Supabase (fake score with no real analysis data). Use `productId: "test-product-00"` for verification.
echo "✅ ensemble-build-lessons.md updated"
## 2026-04-05 — Glow Index callback URL bug

**Problem:** All 66+ analyses ran to completion but zero scores landed in the DB. Engine showed `callback_url: NOT SET` for every job.

**Root cause:** `request.nextUrl.origin` on Replit returns an internal URL unreachable from external services. The engine received an empty callbackUrl and skipped all callbacks.

**Fix:** Use `process.env.NEXT_PUBLIC_APP_URL || process.env.SITE_URL || request.nextUrl.origin` in any endpoint that builds a callback URL for an external service to call back into.

**Required Replit Secret:** `NEXT_PUBLIC_APP_URL=https://[app-name].replit.app`

**Pre-flight checklist for any new ensemble niche:**
1. Trigger 1 product via `/api/trigger-analysis`
2. Check engine `/status` — confirm `callback_url` shows the real public URL
3. Wait for score to land in DB
4. Only then trigger full batch

**Never test callback endpoints with real product IDs** — will corrupt the product record in Supabase (fake score with no real analysis data). Use `productId: "test-product-00"` for verification.

## 2026-04-05 — Frontend data quality bugs (Glow Index)

### Stage 3 deliberation text leaking into consumer UI
**Problem:** Quick Take and Pros/Cons showed internal deliberation text ("My original score of 22 was conservative relative to Gemini and Grok").
**Root cause:** `getSourceAnalyses()` fell back to all analyses when stage 2 filter returned nothing. Stage 3 records contain model self-comparison language.
**Fix:** Filter strictly to `stage === 2`. Return null if no stage 2 — never fall back. Add deliberation patterns to META_PATTERNS.
**Rule:** Any component reading LLM reasoning for consumer display MUST have an explicit stage filter AND a deliberation-language blocklist.

### Per-model score blank in AI Panel
**Problem:** GPT showed blank score in the LLM panel.
**Root cause:** `parseTotal()` summed component fields — returns 0/null if any field missing or differently named.
**Fix:** Read `analysis.consensusScore` (stored directly by callback) first. Component sum is fallback only.
**Rule:** Always store the total score as a direct field on the record. Never rely solely on component sum for display.

### Pre-batch verification protocol (mandatory for all future niches)
Before running batch-analyze on ANY new niche:
1. Trigger 1 product → confirm callback_url is real URL in engine /status
2. Confirm score lands in DB
3. **Load the product detail page and verify:** all 4 models show scores, Quick Take is consumer language, no meta-text, Pros/Cons are product-specific
4. Only then batch

Step 3 is the one we skipped. It costs 5 min and saves hours.

## Model routing rule (2026-04-05)
Use Claude Opus for any build session — app development, ensemble ranking builds, debugging, architecture decisions. Sonnet is fine for content, crons, and research. Both are $0 on Claude Max subscription, so there's no cost penalty for defaulting to Opus on complex work.

## 2026-04-05 — Full session post-mortem

### Brave Search exact-match bug
**Problem:** 5/6 Brave queries returned 0 snippets → Stage 1 gate failed → analysis aborted.
**Root cause:** Exact-match quotes on long product names (`"Anthelios Melt-In Sunscreen SPF 60"`) return 0 results. Works for short names ("Squalane") but fails for multi-word names.
**Fix:** Remove quotes from all Brave queries. Use `product_name brand site:reddit.com` — brand name provides enough specificity.
**Rule:** Never use exact-match quotes on product names in search queries. Test with the longest product name in the catalog before batch.

### Structured data loss at callback
**Problem:** Engine produces key_findings, red_flags, verdict, best_dupe — callback throws them all away, stores only `scores` and `reasoning`. Frontend regex-extracts from reasoning → wrong results.
**Fix:** Store structured fields inside `scores` JSON with underscore prefix. Frontend reads structured first, regex fallback for legacy products only.
**Rule:** Every structured field the engine produces must survive through the callback into the DB. Check by querying one product's analysis record and verifying all fields are present.

### Verdict enum displayed raw
**Problem:** Quick Take showed "WORTH_IT_WITH_CAVEATS" instead of prose.
**Fix:** Frontend mapping table: enum → human sentence. Unknown enums title-cased as fallback.
**Rule:** Never display raw enums in consumer UI. Every enum field needs a display mapping.

### Pro/Con misclassification
**Problem:** LLMs put negative statements ("undermines consumer trust") in key_findings (Pros).
**Fix:** (1) Prompt validation instruction, (2) Frontend negative-language regex filter that auto-moves matches to Cons.
**Rule:** Never trust LLMs to classify sentiment correctly. Always add a frontend safety filter.

### Prisma client not generated on Replit
**Problem:** `generated/` is gitignored. Replit build fails with "Cannot find module" for Subscription model.
**Fix:** Build script: `prisma generate --schema=prisma/schema.prisma && next build`.
**Rule:** Any gitignored generated code needs a build-time generation step.

### Complete pre-batch checklist (updated — mandatory for all future niches)
1. Verify all API keys work (Brave, OpenRouter, Supabase)
2. Test Brave queries with the LONGEST product name in catalog — confirm 4+ queries return snippets
3. Trigger 1 product via `/api/trigger-analysis`
4. Check n8n execution — confirm callbackUrl is the public Replit URL
5. Wait for score to land in Supabase (< 10 min)
6. **Load the product detail page and verify:**
   - Quick Take shows human-readable verdict (not an enum)
   - Pros are genuinely positive, Cons genuinely negative
   - Budget Alternative shows a specific product name + price
   - All 4 models show scores in AI Panel
   - Best For / Skip If / How To Use appear (if new prompt)
7. Only then trigger batch-analyze



---

## OpenRouter API Key Management (added 2026-04-10)

**Engine reads `OPENROUTER_API_KEY` from LaunchAgent plist environment, NOT from workspace files.**
The plist at `~/Library/LaunchAgents/com.openclaw.glow-index-engine.plist` stores `OPENROUTER_API_KEY` as an environment variable. The engine gets this via `os.environ["OPENROUTER_API_KEY"]`. Workspace files (TOOLS.md, global.env) are NOT read by the engine at runtime.

**When updating the plist: must `launchctl unload` + `load` to pick up changes.**
Just restarting the process (`kill` + start) is insufficient — launchd caches the plist env vars on load. Update sequence:
```bash
plutil -replace EnvironmentVariables.OPENROUTER_API_KEY -string "sk-or-v1-..." ~/Library/LaunchAgents/com.openclaw.glow-index-engine.plist
launchctl unload ~/Library/LaunchAgents/com.openclaw.glow-index-engine.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.glow-index-engine.plist
```

**Engine must have startup API key validation (defensive).**
Engine can start "successfully" (uvicorn binds port, /health returns 200) even with a revoked/invalid OpenRouter key. First real analysis then fails silently with all-401 errors. Fix: on startup, make a minimal test call to OpenRouter (any cheap model, 5 tokens). If 401 → log FATAL error + exit 1 so launchd restarts it. Without this, the engine appears healthy but produces zero results.

**Test the specific key the engine uses, not just global.env.**
`curl` from your shell uses the key in global.env. The engine may use a different key (e.g., stored in plist). Always test: `curl -H "Authorization: Bearer <engine-key>" https://openrouter.ai/api/v1/models`. If 401 → engine key is revoked/wrong.

---

## Glow Index Pipeline Failures — Failure Modes and Fixes (added 2026-04-10)

**Failure mode: Products added via votes flow have `website: null`.**
The `/api/votes/add-product` endpoint hardcodes `website: ""` (empty string, treated as null by engine). Engine's Stage 1 can't scrape ingredients without a website URL. Gate fails with "No valid ingredient data found — ingredients are required." Fix: always provide a real website URL when adding products. For products without websites, use IncideDecoder/CosDNA URL as the website field.

**Failure mode: Engine goes down silently.**
n8n webhook returns 202 immediately (async), so n8n never knows the engine failed. Analysis silently produces no results. Fix: engine `/health` endpoint should do a live API key check. Monitor via watchdog cron: `curl -s http://127.0.0.1:8001/health` → if non-200 or slow (>500ms), restart engine + alert JT.

**Failure mode: Tailscale Funnel port mismatch.**
n8n webhook must be reachable from Replit/Vercel. Correct URL: `https://jts-mac-mini.tailaf2fd2.ts.net:8443/webhook/[path]`. Port 8443 = n8n. Port 443 = Mission Control (Next.js). Test with: `curl -s -o /dev/null -w "%{http_code}" https://jts-mac-mini.tailaf2fd2.ts.net:8443/webhook/[path]` → should return 202.

**Failure mode: Callback 404 means wrong secret, not missing endpoint.**
The Glow Index `/api/analysis-callback` returns 404 for wrong `callbackSecret` (security measure). If engine log shows "Callback attempt N/3 failed: 404" → wrong secret in engine's N8N_CALLBACK_SECRET env var, OR wrong URL. Verify: engine's N8N_CALLBACK_SECRET must match Replit's `N8N_CALLBACK_SECRET` secret.
