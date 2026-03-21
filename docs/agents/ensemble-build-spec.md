# Ensemble Ranking Workflow Builder — Agent Instructions

## Purpose
These instructions govern how you build multi-LLM ensemble analysis pipelines (like Nash Satoshi Oracle, Glow Index, or any future ranking/scoring app). Follow them exactly. Every failure mode described here has been encountered in production.

---

## Architecture Decision: n8n as Trigger, Python as Engine

**Do NOT build the LLM pipeline inside n8n Code nodes.** n8n is the wrong tool for the compute layer of a multi-LLM ensemble. Use this architecture instead:

```
[Website/Telegram] → [n8n Webhook] → [Python Ensemble Engine] → [n8n Response/Storage]
```

- **n8n handles**: Webhook intake, request validation, dispatching to the Python engine, receiving results, writing to storage (Google Sheets, Supabase, etc.), sending notifications
- **Python handles**: All data collection, all LLM calls, prompt management, variable threading, retry/fallback logic, score aggregation, and final output formatting

**Why**: n8n Code nodes truncate long strings, have unreliable env var access, don't support parallel async natively, and provide no programmatic error recovery. A Python script gives you full control over all of these. The Python engine can run as a Flask/FastAPI endpoint on the same server, called by n8n via HTTP Request node.

---

## Stage 0: Infrastructure Setup (Do This First, Every Time)

Before writing any pipeline logic, verify these are working:

### Credentials & Environment
1. **Never use `$env.VARIABLE_NAME` in n8n Code nodes.** n8n blocks env var access by default. Instead:
   - Store API keys in n8n's built-in Credential Manager (for n8n-native nodes)
   - For the Python engine, use a `.env` file loaded via `python-dotenv`
   - **Verification step**: After wiring any credential, make a test call that returns data. If the response is empty or null, the credential is not connected — do not proceed.

2. **Test every API key individually** before building the pipeline:
   - Brave Search: Run a test query, confirm results array is non-empty
   - Firecrawl / scraping tool: Fetch a known-good URL, confirm content returned
   - X/Twitter API: Fetch tweets for a popular account, confirm data
   - Each LLM provider: Send "respond with the word HELLO" and confirm response

### Webhook & Tunnel Stability
1. **Never use ngrok free tier.** The subdomain changes on every restart. Use one of:
   - Tailscale Funnel (permanent URL, recommended)
   - Cloudflare Tunnel
   - A fixed domain with reverse proxy
2. **Pin webhook paths.** In n8n, set the webhook path explicitly (e.g., `/ensemble/analyze`) rather than relying on auto-generated paths. Never rename webhook nodes after deployment — it changes the registered path.
3. **After setting up the webhook**, make a test POST from the frontend/client and confirm the n8n execution log shows it received the payload before proceeding.

### Error Recovery Endpoint
Always create a `/force-reset` endpoint that:
- Marks any "processing" analysis as "failed"
- Clears any stuck state
- Returns the reset status
Also implement an auto-timeout: if an analysis has been "processing" for more than 5 minutes, automatically mark it as failed.

---

## Stage 1: Data Collection (The Most Critical Stage)

**RULE: Never ask an LLM to "research" a token/product/entity.** LLMs hallucinate data from stale training sets. Every data point must come from a real API call or web scrape.

### Required Data Sources Per Analysis Target
For each token/product/entity being analyzed, collect data from ALL of these source types:

#### For Crypto Tokens (Nash Satoshi pattern):
1. **Price & Market Data** — CoinGecko API or DexScreener API
   - Use the direct contract address endpoint, NOT the search endpoint
   - Example: `https://api.dexscreener.com/latest/dex/tokens/{CONTRACT_ADDRESS}`
   - Fallback: If CoinGecko slug returns 404 (common for micro-caps), fall back to DexScreener by contract address
   - Collect: price, FDV, market cap, 24h volume, 24h change, 7d change, liquidity

2. **On-Chain Data** — Block explorer API (Etherscan/Basescan/Solscan)
   - Use the correct chain-specific explorer — do NOT use Etherscan for Base tokens
   - Collect: holder count, top holder concentration, contract verification status, transaction count

3. **Social Signals** — X/Twitter API
   - Run 3-5 keyword queries (token name, ticker, contract address)
   - Collect 10 tweets per query minimum
   - Extract: engagement metrics, sentiment, notable accounts discussing

4. **Web Research** — Brave Search + Firecrawl/Jina
   - Brave Search: 3 queries (token name, "token_name review", "token_name tokenomics")
   - Scrape top 3-5 results for deeper content
   - Target: project website, docs, Medium articles, audit reports

#### For Other Domains (Skincare/GlowScore, Movies/Vista, etc.):
Adapt the pattern — the principle is the same:
- **Structured data** from a domain-specific API (e.g., product database, TMDB, etc.)
- **Reviews/sentiment** from social or review platforms
- **Expert content** from web search + page scraping
- **Never rely on LLM training data for factual claims**

### Data Collection Validation Gate
After data collection completes, **verify before proceeding**:
```python
def validate_collection(data):
    checks = {
        "price_data": data.get("price") is not None,
        "market_cap": data.get("market_cap") is not None or data.get("fdv") is not None,
        "social_data": len(data.get("tweets", [])) >= 5,
        "web_research": len(data.get("search_results", [])) >= 3,
    }
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise DataCollectionError(f"Missing critical data: {failed}")
    return True
```
If any critical data source returns empty, retry with fallback queries/endpoints before proceeding. Log which sources succeeded and which failed — this metadata goes to the LLMs so they know what data they're working with.

---

## Stage 2: Independent Analysis (Per-Model)

### Prompt Management

**CRITICAL: Never truncate prompts.** This is the single most common failure mode when an AI agent builds these pipelines. The production prompts for ensemble analysis are 1500-3000 words each. They contain:
- The complete scoring rubric (e.g., 100-point system with component weights)
- All output fields (often 50+)
- Output format specification (JSON schema)
- Calibration examples

**How to handle long prompts in the Python engine:**
```python
# Store prompts as separate files, never inline
PROMPT_DIR = Path("prompts/")

def load_prompt(stage: str, model: str) -> str:
    """Load the full prompt from file. Never truncate."""
    prompt_path = PROMPT_DIR / f"{stage}_{model}.txt"
    prompt = prompt_path.read_text()
    # Verification: prompts should be substantial
    assert len(prompt) > 500, f"Prompt suspiciously short ({len(prompt)} chars) — likely truncated or stub"
    return prompt
```

**Prompt stub detection:** If any prompt is under 500 characters, it's almost certainly a placeholder. Stop and flag it. Real analysis prompts are never that short.

### Parallel LLM Execution
Run all models simultaneously with individual timeout and retry logic:

```python
import asyncio

async def run_stage2(collected_data: dict, models: list[str]) -> dict:
    """Run independent analysis across all models in parallel."""
    tasks = {
        model: run_single_model(model, collected_data)
        for model in models
    }
    results = {}
    for model, task in tasks.items():
        try:
            results[model] = await asyncio.wait_for(task, timeout=120)
        except asyncio.TimeoutError:
            results[model] = {"status": "timeout", "response": None}
        except Exception as e:
            results[model] = {"status": "error", "error": str(e), "response": None}
    return results
```

### Model-Specific Handling
Each LLM provider has quirks. Handle them explicitly:
- **Grok**: REQUIRES a system message. Without one, it refuses content. Always include a system prompt framing the analytical task.
- **Claude**: Works reliably with or without system message. Use system message for role framing.
- **Gemini**: May return safety-filtered responses for certain tokens. Detect and retry with adjusted framing.
- **GPT-4**: Most reliable for structured JSON output. Good anchor model.

### Score Range Validation
After each model returns its analysis, validate the score range BEFORE passing to the next stage:
```python
def validate_scores(response: dict, expected_range=(0, 100)):
    score = response.get("game_theory_score")
    if score is None:
        raise ScoreError("No score in response")
    if not (expected_range[0] <= score <= expected_range[1]):
        raise ScoreError(f"Score {score} outside expected range {expected_range}")
    return True
```
A model scoring on a 1-3 scale instead of 0-100 means the prompt was truncated or missing the scoring rubric. Stop and fix the prompt.

---

## Stage 3: Cross-Model Deliberation

### Variable Threading (The Silent Killer)

**This is where the n8n build catastrophically failed.** The deliberation stage requires each model to see:
1. Its own Stage 2 analysis
2. Every other model's Stage 2 analysis (with model names attributed)

**The variable names in the prompt template MUST exactly match the variable names you inject.** Verify this programmatically:

```python
import re

def verify_template_variables(prompt_template: str, available_vars: dict):
    """Ensure every {variable} in the template has a matching value."""
    required_vars = set(re.findall(r'\{(\w+)\}', prompt_template))
    provided_vars = set(available_vars.keys())
    missing = required_vars - provided_vars
    if missing:
        raise TemplateError(f"Prompt expects variables not provided: {missing}")
    # Also check for empty values
    empty = [k for k in required_vars if not available_vars.get(k)]
    if empty:
        raise TemplateError(f"Variables present but empty: {empty}")
    return True
```

**Run this verification before every LLM call.** If a model receives empty context for deliberation, it's debating nothing — the output is worthless.

### Handling Model Dropouts
If a model failed in Stage 2 (timeout, refusal, error), handle it explicitly in Stage 3:
- Remove the failed model from the deliberation context
- Adjust the prompt to reflect how many models are participating: "You are reviewing analyses from 3 models (one model was unavailable)" rather than leaving a blank slot
- Log which models are participating at each stage

---

## Stage 4: Consensus Aggregation

### Minimum Model Threshold
**Never aggregate with fewer than 3 models.** If only 2 models reached Stage 4:
- Retry the failed models once with fresh API calls
- If still only 2, mark the analysis as "LOW CONFIDENCE — insufficient model coverage" in the output
- Never present a 2-model average as if it were full consensus

### Aggregation Logic
```python
def aggregate_scores(stage3_results: dict, min_models: int = 3) -> dict:
    valid_results = {
        model: result for model, result in stage3_results.items()
        if result.get("status") == "success" and result.get("score") is not None
    }

    if len(valid_results) < min_models:
        return {
            "consensus": "LOW",
            "confidence": "INSUFFICIENT",
            "note": f"Only {len(valid_results)}/{len(stage3_results)} models completed analysis",
            "average_score": sum(r["score"] for r in valid_results.values()) / len(valid_results) if valid_results else None,
        }

    scores = [r["score"] for r in valid_results.values()]
    spread = max(scores) - min(scores)

    return {
        "consensus": "HIGH" if spread <= 15 else "MEDIUM" if spread <= 30 else "LOW",
        "confidence": "HIGH" if len(valid_results) >= 4 and spread <= 15 else "MEDIUM" if len(valid_results) >= 3 else "LOW",
        "average_score": round(sum(scores) / len(scores), 2),
        "model_scores": {model: r["score"] for model, r in valid_results.items()},
        "spread": spread,
        "models_reporting": len(valid_results),
        "models_total": len(stage3_results),
    }
```

### Output Validation
Before returning the final result, verify:
1. The Game Theory Score is between 0 and 100
2. All required output fields are present (not null/empty)
3. The consensus label matches the actual model agreement spread
4. The narrative summary is coherent (not template placeholders)

---

## Stage 5: Pipeline-Level Error Handling

### Retry Strategy
```
Level 1 (per-API-call): Retry 2x with exponential backoff (2s, 4s)
Level 2 (per-model): If a model fails all retries, mark as unavailable, continue with remaining models
Level 3 (per-stage): If a stage produces no valid results, abort and return error state
Level 4 (per-pipeline): If the pipeline hangs for >5 min, auto-timeout and mark as failed
```

### Never Silently Drop Models
Every model that was supposed to participate must appear in the final output, either with its score or with a clear status indicator:
```json
{
  "claude_opus": {"score": 72, "status": "success"},
  "gemini_pro": {"score": 68, "status": "success"},
  "gpt4": {"score": 75, "status": "success"},
  "grok": {"score": null, "status": "refused", "reason": "content_filter"}
}
```

---

## Anti-Patterns Checklist (Verify Before Deploying)

Run through this checklist before considering any ensemble pipeline complete:

- [ ] **No fake research**: Every data point comes from a real API call or scrape. No LLM is asked to "research" anything.
- [ ] **No stub prompts**: Every analysis prompt is >500 characters. Scoring rubric is present. Output format is specified.
- [ ] **No truncated prompts**: Load prompts from files, not inline strings. Verify byte length matches source file.
- [ ] **No template mismatches**: Every `{variable}` in every prompt template has a matching, non-empty value injected.
- [ ] **No silent failures**: Every API call has error handling. Every model reports success or failure status.
- [ ] **No env var assumptions**: Every credential is verified working with a test call before pipeline runs.
- [ ] **No dropped models**: Final output shows every model's status. Consensus reflects actual participation count.
- [ ] **No stuck states**: Processing timeout exists. Force-reset endpoint exists.
- [ ] **No unstable URLs**: Webhook URL is permanent (Tailscale/Cloudflare, not ngrok free).
- [ ] **Score range verified**: All scores are on the correct scale (0-100, not 1-3 or 1-10).

---

## Python Engine Project Structure

```
ensemble-engine/
├── main.py                  # FastAPI app with /analyze endpoint
├── config.py                # All configuration, loaded from .env
├── collectors/
│   ├── __init__.py
│   ├── coingecko.py         # Price/market data
│   ├── dexscreener.py       # DEX data (fallback)
│   ├── explorer.py          # On-chain data (chain-aware)
│   ├── twitter.py           # Social signals
│   ├── brave_search.py      # Web search
│   └── scraper.py           # Page content extraction
├── analyzers/
│   ├── __init__.py
│   ├── base.py              # Base model interface
│   ├── claude.py
│   ├── gemini.py
│   ├── gpt4.py
│   └── grok.py
├── pipeline/
│   ├── __init__.py
│   ├── stage1_collect.py    # Data collection + validation
│   ├── stage2_analyze.py    # Independent analysis
│   ├── stage3_deliberate.py # Cross-model deliberation
│   ├── stage4_aggregate.py  # Consensus scoring
│   └── validators.py        # Score range, template, completeness checks
├── prompts/
│   ├── stage2_analysis.txt
│   ├── stage3_deliberation.txt
│   └── stage4_aggregation.txt
└── .env                     # API keys (never commit)
```

---

## n8n Workflow Structure (Thin Orchestration Layer)

The n8n workflow should be minimal:

```
[Webhook: /ensemble/analyze]
  → [Validate Input (Code node: check required fields)]
  → [HTTP Request: POST to Python engine /analyze]
  → [Wait for response (up to 5 min timeout)]
  → [Write results to Google Sheets / Supabase]
  → [Webhook Response: return results to caller]

[Separate workflow: Timeout Poller]
  → [Cron: every 2 minutes]
  → [Check for analyses stuck in "processing" > 5 min]
  → [Mark as failed, notify via Telegram]
```

That's it. All complexity lives in the Python engine where you have full programmatic control.

---

## Adapting for New Domains

When building a new ensemble ranking app (e.g., Glow Index for skincare, Vista for movies):

1. **Copy the Python engine structure** — the pipeline stages (collect → analyze → deliberate → aggregate) are universal
2. **Replace the collectors** — swap crypto APIs for domain-specific APIs (product databases, review platforms, etc.)
3. **Write new prompts** — this is the domain-specific part. Each prompt file gets the full scoring rubric for the new domain.
4. **Keep the validators** — score range validation, template verification, and model dropout handling are domain-agnostic
5. **Keep the n8n wrapper** — same thin orchestration, just pointed at the new Python endpoint
