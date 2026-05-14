#!/usr/bin/env python3
"""Deterministic preflight guard for bounded Autoresearch sweeps.

This does not read secrets or call model APIs. It enforces the declared sweep budget
before an LLM run begins by checking selected model, max target/test/round limits,
and a conservative cost estimate. If the estimate exceeds the cap, the sweep must
block instead of relying on prompt-level restraint.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
PROMPT = ROOT / "agents" / "autoresearch" / "weekly-sweep-prompt.md"
TARGETS = ROOT / "agents" / "autoresearch" / "targets.md"
STATUS = ROOT / "agents" / "autoresearch" / "cost-guard-status.json"

# Conservative ballpark. The guard is intentionally pessimistic because the
# recurring sweep is supposed to be cheap and bounded.
MODEL_ESTIMATES_PER_1K = {
    "openai-codex/gpt-5.5": 0.010,
    "anthropic/claude-sonnet-4-6": 0.018,
    "moonshot/kimi-k2.6": 0.004,
    "default": 0.015,
}


def parse_limits(text: str) -> dict:
    def find(pattern: str, default: int) -> int:
        m = re.search(pattern, text, re.I)
        return int(m.group(1)) if m else default
    return {
        "max_targets": find(r"Max targets:\s*(\d+)", 1),
        "max_test_inputs": find(r"Max test inputs:\s*(\d+)", 3),
        "max_rounds": find(r"Max rounds:\s*(\d+)", 5),
    }


def estimate_cost(model: str, max_targets: int, max_test_inputs: int, max_rounds: int, tokens_per_eval: int) -> float:
    # Baseline + mutation rounds, each over all test inputs. Add 25% overhead for
    # scoring/logging/registry reads.
    evals = max_targets * max_test_inputs * (1 + max_rounds)
    estimated_tokens = int(evals * tokens_per_eval * 1.25)
    rate = MODEL_ESTIMATES_PER_1K.get(model, MODEL_ESTIMATES_PER_1K["default"])
    return round((estimated_tokens / 1000) * rate, 4)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="openai-codex/gpt-5.5")
    p.add_argument("--cap", type=float, default=0.50)
    p.add_argument("--tokens-per-eval", type=int, default=5000)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if not PROMPT.exists() or not TARGETS.exists():
        result = {"ok": False, "error": "missing_autoresearch_prompt_or_targets", "prompt": str(PROMPT), "targets": str(TARGETS)}
    else:
        text = PROMPT.read_text(errors="ignore")
        limits = parse_limits(text)
        cost = estimate_cost(args.model, **limits, tokens_per_eval=args.tokens_per_eval)
        result = {
            "ok": cost <= args.cap,
            "model": args.model,
            "cap_usd": args.cap,
            "estimated_usd": cost,
            "limits": limits,
            "tokens_per_eval": args.tokens_per_eval,
            "status": "PASS" if cost <= args.cap else "BLOCKED_COST_CAP",
        }

    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(result, indent=2))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"AUTORESEARCH_COST_GUARD_{result.get('status', 'FAIL')}: estimated=${result.get('estimated_usd')} cap=${result.get('cap_usd')}")
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
