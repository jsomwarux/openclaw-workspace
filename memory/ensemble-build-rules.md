# Ensemble Build Rules (adopted 2026-03-20)
Full spec: docs/agents/ensemble-build-spec.md

## Architecture (mandatory for every new ensemble build)
- n8n = thin trigger only (webhook → HTTP Request to Python engine → write result). Max 5-7 nodes.
- Python FastAPI = all data collection, LLM calls, prompt management, retry/fallback, aggregation
- Never put ensemble logic inside n8n Code nodes

## Pre-Build Checklist (run before writing any pipeline code)
1. Test every API key individually with a live call that returns real data
2. Set up permanent webhook URL (Tailscale Funnel) before writing any webhook logic
3. Store prompts as .txt files in prompts/ — never inline. Assert len(prompt) > 500 before any LLM call.
4. Verify every {variable} in every prompt template has a matching non-empty value at injection time
5. Validate score range after each model (0-100 or whatever the rubric specifies)
6. Validate data collection gate before Stage 2: price/market data, ≥5 social signals, ≥3 search results
7. Minimum 3 models for aggregation — never present 2-model average as consensus
8. Every model appears in final output with score or status (no silent drops)
9. Force-reset endpoint + auto-timeout poller (>5 min processing → mark failed)

## Project Structure (reuse for every new niche)
ensemble-engine/
├── main.py                    # FastAPI /analyze endpoint
├── config.py                  # All config, loaded from .env via python-dotenv
├── collectors/                # Domain-specific data sources (swap per niche)
├── analyzers/                 # Per-model LLM interface (universal)
├── pipeline/                  # stage1_collect, stage2_analyze, stage3_deliberate, stage4_aggregate, validators
└── prompts/                   # Full .txt prompt files (never inline)

## Model-Specific Quirks
- Grok: ALWAYS include a system message or it refuses
- Gemini: May safety-filter some content — detect and retry with adjusted framing
- GPT-4/5: Best for structured JSON output, good anchor model

## For New Niches (Glow Index, movies, etc.)
1. Copy Python engine structure
2. Replace collectors with domain-specific APIs
3. Write new full prompts (scoring rubric + all output fields + format spec)
4. Keep validators, aggregation logic, and n8n wrapper unchanged
