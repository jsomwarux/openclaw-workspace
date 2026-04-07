# Ensemble Ranking Apps — Build Briefing for Claude Desktop
> Comprehensive technical briefing for building LLM-ensemble product ranking apps.
> For JT Somwaru. Based on lessons from Nash Satoshi, Glow Index, and operational experience through April 2026.

---

## What You Are Building

A suite of LLM-ensemble product ranking web apps. Each app:
- Analyzes products in a specific niche using a **4-LLM consensus engine** (2-stage: independent → cross-check)
- Produces a **0–100 consensus score** from domain-specific scoring dimensions
- Displays ranked products with **tier labels** (S+/S/A/B/C), dimension breakdowns, and analysis excerpts
- Has a **public vote page** for users to request new products
- Has a **password-protected admin panel** to trigger analyses and manage content
- Deploys to **Vercel** (frontend) + **Mac mini Python engine** via Tailscale Funnel

**Apps in this suite:** Nash Satoshi (crypto/game theory), Glow Index (skincare), and new niches to be built.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  USER BROWSER                                           │
│  Next.js App (Vercel)                                   │
│  /rankings /vote /admin                                 │
└─────────────────────┬───────────────────────────────────┘
                      │ POST /api/trigger-analysis
                      ▼
┌─────────────────────────────────────────────────────────┐
│  n8n Cloud Workflow (webhook trigger)                    │
│  Stage 1: 4 LLMs analyze independently (parallel)      │
│  Stage 2: 4 LLMs cross-check each other (parallel)     │
│  Then: HTTP POST results to callback URL                │
└────────────┬────────────────────────────────────────────┘
             │
             ▼ (results posted to)
┌─────────────────────────────────────────────────────────┐
│  Next.js API: /api/analysis-callback                    │
│  Saves to Supabase Postgres via Prisma                  │
│  Updates Product.consensusScore + tier                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Python Engine (Mac mini, port 8001)                    │
│  Runs ONCE per niche as a persistent server            │
│  Handles: product data collection, web scraping,       │
│  Brave Search, LLM calls via OpenRouter, scoring       │
└─────────────────────────────────────────────────────────┘
```

**The engine does NOT run in n8n.** n8n calls the Python engine for data collection, then orchestrates the LLM ensemble, then calls back to the Next.js app with results.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 (App Router, TypeScript strict) |
| Styling | Tailwind CSS 3.4+ + shadcn/ui |
| Database | Supabase Postgres via Prisma ORM |
| LLM Orchestration | n8n cloud (webhook → 4-LLM → callback) |
| Python Engine | FastAPI + uvicorn, Python 3.9 |
| Model Routing | OpenRouter API (all models unified) |
| Deployment | Vercel (frontend) + Mac mini (engine) |
| Admin Auth | Env var secret only (no auth library) |

**Do NOT use:** NextAuth/Clerk, Redux, CSS-in-JS, Pages Router.

---

## The 4-LLM Ensemble Pattern

### Stage 1 — Independent Analysis
All 4 LLMs receive the same prompt + product data simultaneously. Each produces:
- 6 domain-specific dimension scores (must sum to 100)
- Written reasoning
- Tier classification
- Structured fields: key_findings, red_flags, verdict, best_dupe

### Stage 2 — Cross-Check Consensus
All 4 Stage 1 responses are fed back to all 4 LLMs simultaneously. Each LLM:
- Reviews all other analyses
- Identifies agreements and disagreements
- Challenges outlier scores (>15pt deviation from median)
- Produces a refined final score

**Consensus score:** average of 4 Stage 2 totals. Weighted toward closest 2 if one is a significant outlier.

### Current Model IDs (OpenRouter — verify before building)
```
openai/o3          — reasoning model, max intelligence
google/gemini-2.5-pro — confirmed available, $1.25/$10 per M
anthropic/claude-sonnet-4.6 — DOT separator, not hyphen
x-ai/grok-4.20-beta — $2/$6 per M, 2M context
```
Always run `curl https://openrouter.ai/api/v1/models | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"` to verify before finalizing config.

### ALL OpenRouter responses use `choices[0].message.content`
OpenRouter normalizes ALL models to OpenAI format. Never use model-native extractors:
- NOT `content[0].text` (Claude native)
- NOT `candidates[0].content.parts[0].text` (Gemini native)
- YES `choices[0].message.content` (works for all)

### Gemini + response_format = silent failure
Gemini rejects `response_format: {"type": "json_object"}` via OpenRouter. It returns `finish_reason: "length"` with content `"OK"`. **Remove response_format from all Gemini calls.** Only OpenAI models support this param through OpenRouter.

---

## The Python Engine (Mac mini)

### Python 3.9 constraint
Mac mini runs Python 3.9. `asyncio.Semaphore | None` throws `TypeError`. Always use `Optional[asyncio.Semaphore]` from `typing`. The `X | Y` union syntax is Python 3.10+ only.

### Persistence
```bash
nohup python3 -m uvicorn main:app --port 8001 --host 127.0.0.1 > /tmp/glow-engine.log 2>&1 &
```
Engine dies if terminal closes. Check `/tmp/glow-engine.log` for silent errors.

### Bind to 127.0.0.1, not localhost
n8n may resolve `localhost` as `::1` (IPv6) while uvicorn listens on IPv4 only. HTTP requests to `localhost:8001` fail silently. Use `127.0.0.1` explicitly.

### Concurrency
```python
# Create at startup in lifespan context manager
semaphore = asyncio.Semaphore(MAX_CONCURRENT)  # default: 2
```
Only raise to 3 if OpenRouter rate limits aren't being hit.

---

## n8n Workflow Structure

```
Webhook Trigger (receives product data)
  → HTTP Request: GET product data from app DB
  → [PARALLEL] OpenAI o3 Stage 1
  → [PARALLEL] Claude Sonnet 4.6 Stage 1
  → [PARALLEL] Gemini 2.5 Pro Stage 1
  → [PARALLEL] Grok 4.20 Stage 1
  → Merge (Wait for All 4)
  → [PARALLEL] OpenAI o3 Stage 2 (includes all Stage 1 results)
  → [PARALLEL] Claude Stage 2
  → [PARALLEL] Gemini Stage 2
  → [PARALLEL] Grok Stage 2
  → Merge (Wait for All 4)
  → Calculate consensus score (Code node)
  → HTTP POST: callback to app API (/api/analysis-callback)
```

### n8n JSON body double-serialization fix
`specifyBody: "json"` + `jsonBody: "={{ JSON.stringify(...) }}"` causes double-wrap.
**Fix:** `contentType: "raw"`, `rawContentType: "application/json"`, `body` = stringify expression. Sends raw string directly.

---

## Callback + Database Layer

### Schema (Prisma/Supabase)
```prisma
model Product {
  id              String    @id @default(cuid())
  name            String
  brand           String
  category        String
  priceUsd        Float
  imageUrl        String?
  consensusScore  Float?
  tier            String?   // "S+", "S", "A", "B", "C"
  lastAnalyzedAt  DateTime?
  analyses        Analysis[]
  votes           Vote[]
  createdAt       DateTime  @default(now())
}

model Analysis {
  id              String    @id @default(cuid())
  productId       String
  product         Product   @relation(fields: [productId], references: [id])
  runId           String    // Groups the 4 LLM analyses in one run
  llmName         String
  stage           Int       // 1 = independent, 2 = consensus
  scores          Json      // {dim1: N, dim2: N, ..., total: N}
  reasoning       String
  consensusScore  Float?    // Only on stage 2
  createdAt       DateTime  @default(now())
}
```

### Every structured field must survive through the callback
The engine produces: `key_findings`, `red_flags`, `verdict`, `best_dupe`, `consensusScore`
**All must survive through the callback into the DB.** Query one analysis record after first run and verify all fields are present. Regex extraction from reasoning text is a fragile fallback only.

### Callback URL on Replit (Glow Index legacy issue)
`request.nextUrl.origin` on Replit returns an internal URL unreachable externally.
**Fix:** `process.env.NEXT_PUBLIC_APP_URL || process.env.SITE_URL || request.nextUrl.origin`
**Required Replit Secret:** `NEXT_PUBLIC_APP_URL=https://[app-name].replit.app`

### Never test callback with real product IDs
Will corrupt the product record (fake score with no real analysis data). Use `productId: "test-product-00"` for verification.

---

## Pre-Batch Checklist (Mandatory for Every Niche)

Before running batch-analyze on ANY new niche:

1. ✅ Verify all API keys work (Brave, OpenRouter, Supabase)
2. ✅ Test Brave queries with the LONGEST product name in catalog — confirm 4+ queries return snippets. **Never use exact-match quotes on product names in Brave queries** — fails for multi-word names. Use `product_name brand site:reddit.com` instead.
3. ✅ Trigger 1 product via `/api/trigger-analysis`
4. ✅ Check n8n execution — confirm callbackUrl is the public Replit/Vercel URL
5. ✅ Wait for score to land in Supabase (< 10 min)
6. ✅ **Load the product detail page and verify:**
   - Quick Take shows human-readable verdict (NOT an enum like `WORTH_IT_WITH_CAVEATS`)
   - Pros are genuinely positive, Cons genuinely negative (LLMs misclassify negative statements as pros)
   - Budget Alternative shows a different product (not the product itself)
   - All 4 models show scores in AI Panel
   - No LLM deliberation meta-text leaking into consumer UI
7. ✅ Only then trigger batch-analyze

**Step 6 is the one that gets skipped. It costs 5 minutes and saves hours.**

---

## Scoring Tier Framework

| Tier | Score | Label |
|------|-------|-------|
| S+ | 85–100 | Best in Class |
| S | 70–84 | Excellent |
| A | 55–69 | Good |
| B | 35–54 | Average |
| C | 0–34 | Skip |

Display the modifier breakdown separately in the UI:
`Base: 68 + Lifecycle: +7 + Category: +3 + Price: +10 = Final: 88 [S]`
This transparency is the key differentiator — users see WHY a product scored what it scored.

---

## Frontend Display Rules (Known Failure Modes)

These pass visual inspection but mislead users with real data:

**Pros/Cons integrity:** Regex extraction must EXCLUDE sentences that:
- Start with "No [ingredient]..." (limitation framing, not a pro)
- Contain "positions X as" or "marketed as" (marketing critique, not a con)
- Contain "rather than", "limiting", "instead of" in negative context

**Quick Take readability:** Must NOT contain LLM meta-commentary ("cross-model consensus", "INCI list", "all four models"). Target 8th grade reading level. If extraction finds only jargon-heavy sentences, return null.

**Budget Alternative guard:** Filter out sentences containing the current product's brand name. A product cannot be its own alternative.

**Score color thresholds:**
- >= 75: green | >= 55: amber | < 55: red
Setting green at 80+ makes fair products look bad and destroys trust.

**Numeric labels:** Every dimension score renders as "57% · Fair" not just "57%".
Labels: Excellent (90+) / Good (75+) / Fair (55+) / Below Avg (35+) / Poor (<35)

**AI Panel spread signal:** All models within 3 pts → "Strong agreement". 10+ pt spread → "Models disagreed significantly".

**Never truncate user-facing content at arbitrary character counts.** Truncating bullet points at 120 chars with "..." signals incomplete information and destroys trust. Let sentences wrap. Only truncate preview cards with a "Read more" affordance.

**UX copy must match actual page content.** "Read the breakdown" is misleading if no breakdown section renders. Audit every helper text against the actual layout.

---

## Build System (Ranking App Agent)

The ranking-app-agent has templates that scaffold most of this automatically:

```
~/projects/ranking-app-agent/
├── template-app/        ← Next.js app template with all pages wired
├── template-engine/     ← Python FastAPI engine template
├── niches/             ← Niche config files (skincare, crypto, etc.)
├── scripts/
│   └── new-niche.sh   ← THE scaffold script — USE THIS
└── shared/            ← Prisma schema, types, scoring utils
```

**To build a new niche:**
```bash
cd ~/projects/ranking-app-agent
./scripts/new-niche.sh niches/[id].config.ts ~/projects/[id]-rankings/
```

This scaffolds: Next.js app + Python engine + Prisma schema + n8n workflow template + seed script + deployment configs.

**Every new niche gets its own domain.** Never add as a tab or sub-path. Each niche is independently sellable.

---

## Deployment

### Frontend (Vercel)
```bash
cd ~/projects/[niche]-rankings
vercel --prod
```
Set environment variables in Vercel dashboard: OPENROUTER_API_KEY, BRAVE_API_KEY, DATABASE_URL (Supabase), ADMIN_KEY, N8N_WEBHOOK_URL, N8N_CALLBACK_SECRET.

**`next.config.ts` — do NOT set `output: 'standalone'`** (that was for Replit). Vercel handles this natively.

### Engine (Mac mini)
Each niche engine runs on a unique port. Use `new-niche.sh` which creates a LaunchAgent.

**Engine URL for n8n:** `http://127.0.0.1:[PORT]` (engine is on Mac mini, n8n calls it directly)

**n8n public webhook URL:** Tailscale Funnel exposes the Mac mini:
`https://jts-mac-mini.tailaf2fd2.ts.net:8443/webhook/[niche]-analysis`

**The Funnel URL (port 8443) is the public URL. The tailnet-only URL (port 8080) is inaccessible from Replit/Vercel.**

### Database (Supabase)
Use the existing paid Supabase account. Create a new database per niche app.

```bash
npx prisma generate
npx prisma db push
npx tsx scripts/seed.ts
```

**Prisma generated/ is gitignored.** Replit build fails without it. Build script must include `prisma generate --schema=prisma/schema.prisma && next build`.

---

## Key Lessons (From Glow Index Build)

### Lesson: Prompt Field Names Must Match Every Layer
If prompts output `base_score`, validators must check `base_score`, stage4 must read `base_score`, frontend type must include `base_score`. Any mismatch silently produces `null` or `NaN` — not an error.

**When changing output schema, update every layer simultaneously:**
1. Prompt (LLM output fields)
2. `validate_score()` in validators.py
3. `stage4_aggregate.py` score extraction + analyses builder
4. Callback payload construction
5. Frontend type definitions + components

### Lesson: Stage 3 Deliberation Text Leaking into Consumer UI
`getSourceAnalyses()` fell back to all analyses when stage 2 filter returned nothing. Stage 3 records contain model self-comparison language ("My original score of 22 was conservative...").

**Fix:** Filter strictly to `stage === 2`. Return null if no stage 2 — never fall back. Add deliberation patterns to the blocklist.

### Lesson: Per-Model Score Blank in AI Panel
`parseTotal()` summed component fields — returns 0/null if any field missing or differently named.

**Fix:** Read `analysis.consensusScore` (stored directly by callback) first. Component sum is fallback only. Always store the total score as a direct field on the record.

### Lesson: Brave Search Exact-Match Quotes Fail
Exact-match quotes on long product names (`"Anthelios Melt-In Sunscreen SPF 60"`) return 0 results.

**Fix:** Remove all quotes from Brave queries. Use `product_name brand site:reddit.com` — brand name provides enough specificity. Test with the longest product name in the catalog before batch.

### Lesson: Verdict Enum Displayed Raw
Frontend showed "WORTH_IT_WITH_CAVEATS" instead of prose.

**Fix:** Frontend mapping table: enum → human sentence. Unknown enums title-cased as fallback. Never display raw enums in consumer UI.

### Lesson: Pro/Con Misclassification
LLMs put negative statements ("undermines consumer trust") in key_findings (Pros).

**Fix:** (1) Prompt validation instruction, (2) Frontend negative-language regex filter that auto-moves matches to Cons. Never trust LLMs to classify sentiment correctly.

### Lesson: Callback URL on Replit Is Internal
`request.nextUrl.origin` returns internal URL. Engine received empty callbackUrl, skipped all callbacks. 66 analyses ran to completion with zero scores landing in the DB.

**Fix:** `process.env.NEXT_PUBLIC_APP_URL || process.env.SITE_URL || request.nextUrl.origin`

### Lesson: Prisma Client Not Generated on Replit
`generated/` is gitignored. Build fails with "Cannot find module" for Prisma models.

**Fix:** `prisma generate` in build script before `next build`.

---

## Design System (Adapt Per Niche)

Each niche gets its own aesthetic — but the tier system and scoring mechanics stay identical.

**Nash Satoshi (dark/crypto):** Dark terminal aesthetic. Emerald green primary. Monospace fonts.

**Glow Index (skincare/beauty):**
- Background: `#FAFAF8` (warm white)
- Primary: `#3D1F2E` (deep burgundy/plum)
- Accent: `#C4956A` (rose gold)
- Typography: Playfair Display (headlines) + Inter (body) + DM Mono (scores)
- Tier colors: S+ rose gold / S soft plum / A sage / B muted gold / C muted rose

**Tier badge system is universal** — same pill-shaped badge pattern, just different colors per niche.

---

## Vibe Marketing Integration (Post-Launch)

After a niche app launches, add it to the vibe marketing system:
1. Update `~/.openclaw/workspace/agents/vibe-marketing/product-registry.json`
2. Add real product photos to `agents/vibe-marketing/real-photos/[niche]/`
3. Update `agents/vibe-marketing/brands/[niche].json` with product info
4. The posting crons will automatically include the new niche

**Sound selection for TikTok slideshows:**
- Trending first, aesthetic as filter — never sacrifice a 100K+ video trend for perfect aesthetic fit
- Crypto niche: "Bounce (i just wanna dance)" by фрози & joyful (8M videos, business-approved), or search TikTok sound library for "crypto" trends
- Movie niche: Charli xcx & John Cale "House" (55K videos), Azealia Banks "212" instrumental, or Coachella/Euphoria audio
- Never use generic lo-fi or Hans Zimmer — they don't trend on TikTok
- When a movie trailer drops, clip the audio and post within 24h — fastest growing movie audio format

---

## Development Standards

- Every page must look polished at 375px (mobile), 768px (tablet), 1280px (desktop)
- No placeholder text — use real product data from seed
- Score display must be calculated programmatically, not hardcoded
- All TypeScript strict — no `any` types
- No `console.log` in production code
- No stubs or TODOs — complete implementations only
- Minimal impact: only touch what's necessary, don't refactor unrelated files

**Verification (non-negotiable):** Run `npm run typecheck` after every change. Prove it works before presenting it done.

**When you make a mistake:** Update `lessons.md` in the same session. Concrete failure + root cause + rule that prevents recurrence. Not a vague note — a usable rule.
