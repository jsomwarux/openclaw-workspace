#!/usr/bin/env python3
"""
cost-tracker.py — OpenClaw API cost tracker
Reads sessions.json and cron runs to calculate spend, detect alerts, and generate reports.

Usage:
  python3 cost-tracker.py --snapshot          # Capture today's costs from sessions.json
  python3 cost-tracker.py --report today      # Today's spend summary (JSON)
  python3 cost-tracker.py --report yesterday  # Yesterday's spend summary (JSON)
  python3 cost-tracker.py --report week       # Last 7 days summary (JSON)
  python3 cost-tracker.py --report month      # Current month summary (JSON)
  python3 cost-tracker.py --check-alerts      # Check thresholds, return alerts (JSON)
  python3 cost-tracker.py --brief             # Human-readable morning brief section
  python3 cost-tracker.py --weekly-review     # Weekly optimization review text
  python3 cost-tracker.py --check-runaway     # Check for rapid-fire cron loops
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

# ── Paths ────────────────────────────────────────────────────────────────────
OPENCLAW_DIR   = Path.home() / ".openclaw"
SESSIONS_FILE  = OPENCLAW_DIR / "agents/main/sessions/sessions.json"
CRON_RUNS_FILE = OPENCLAW_DIR / "cron/runs/undefined.jsonl"
COSTS_DIR      = Path.home() / ".openclaw/workspace/memory/costs"
TZ_EST         = ZoneInfo("America/New_York")  # local cost/reporting day, DST-aware

COSTS_DIR.mkdir(parents=True, exist_ok=True)

# ── OpenRouter Billing (source of truth — uses actual API, not estimates) ───
OR_BILLING_FILE = COSTS_DIR / "openrouter-billing.jsonl"

def fetch_openrouter_billing() -> dict:
    """Fetch real total_usage from OpenRouter credits API. Returns dict with total_usage, total_credits."""
    # Load key from global.env (shell env file, not inherited by Python subprocesses)
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        env_file = Path.home() / ".config/env/global.env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not key:
        return {"error": "OPENROUTER_API_KEY not set", "total_usage": 0.0, "total_credits": 0.0}
    try:
        import urllib.request
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/credits",
            headers={"Authorization": f"Bearer {key}"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return {
                "total_usage": float(data.get("data", {}).get("total_usage", 0)),
                "total_credits": float(data.get("data", {}).get("total_credits", 0)),
            }
    except Exception as e:
        return {"error": str(e), "total_usage": 0.0, "total_credits": 0.0}


def load_or_billing_log() -> list:
    """Load all OpenRouter billing log entries."""
    entries = []
    if not OR_BILLING_FILE.exists():
        return entries
    with open(OR_BILLING_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def save_or_billing_entry(total_usage: float, total_credits: float) -> None:
    """Append today's OpenRouter billing snapshot to the log."""
    with open(OR_BILLING_FILE, "a") as f:
        f.write(json.dumps({
            "date": today_est(),
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "total_usage": round(total_usage, 6),
            "total_credits": round(total_credits, 6),
            "balance_remaining": round(total_credits - total_usage, 6),
        }) + "\n")


def get_real_daily_cost() -> dict:
    """Compute real daily costs from OpenRouter billing deltas.
    Returns {date: cost_usd} for available days."""
    log = load_or_billing_log()
    if len(log) < 2:
        return {}
    costs = {}
    for i in range(1, len(log)):
        prev = log[i - 1]
        curr = log[i]
        # Only same-day or consecutive entries count
        delta = curr["total_usage"] - prev["total_usage"]
        if delta >= 0:  # positive means spend increased
            costs[curr["date"]] = round(delta, 6)
    return costs


# ── Pricing (per 1M tokens, USD) ─────────────────────────────────────────────
# NOTE: Anthropic models use OAuth subscription token (sk-ant-oat01-*), NOT an API key.
# All Claude model usage is $0 in real API charges — covered by flat Claude subscription.
# Only OpenRouter and Groq entries below represent real billable costs.
# Prices in USD per million tokens
PRICING = {
    # Anthropic — $0 real cost (OAuth subscription token, not API key)
    "anthropic/claude-sonnet-4-6":  {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "anthropic/claude-opus-4-6":    {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "anthropic/claude-haiku-4-5":   {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "anthropic/claude-sonnet-4-5":  {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "anthropic/claude-opus-4-5":    {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "claude-sonnet-4-6":           {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},  # legacy key
    # Groq (nearly free — actual rate ~$0.59/$0.79/M)
    "llama-3.3-70b-versatile":     {"input": 0.00059, "output": 0.00079, "cache_read": 0.0, "cache_write": 0.0},
    "llama-3.1-70b-versatile":     {"input": 0.00059, "output": 0.00079, "cache_read": 0.0, "cache_write": 0.0},
    "groq/llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079, "cache_read": 0.0, "cache_write": 0.0},
    # OpenRouter direct (no provider prefix in sessions.json for these)
    "minimax/m2.7":                {"input": 0.30,   "output": 1.20,  "cache_read": 0.0, "cache_write": 0.0},  # $0.30/$1.20 per M (API: $0.0000003/$0.0000012 per token)
    "minimax/minimax-m2.7":        {"input": 0.30,   "output": 1.20,  "cache_read": 0.0, "cache_write": 0.0},  # full key as in sessions.json
    "deepseek/deepseek-chat-v3-0324": {"input": 0.20, "output": 0.77,  "cache_read": 0.0, "cache_write": 0.0},  # $0.20/$0.77 per M (API: $0.00000020/$0.00000077 per token)
    "deepseek/deepseek-chat":       {"input": 0.20,  "output": 0.77,  "cache_read": 0.0, "cache_write": 0.0},  # legacy key
    # OpenRouter via openrouter/ prefix
    "openrouter/openai/gpt-4o":                    {"input": 2.50,  "output": 10.00, "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/openai/gpt-4o-mini":               {"input": 0.15,  "output": 0.60,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/openai/o3-mini":                   {"input": 1.10,  "output": 4.40,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/x-ai/grok-3":                      {"input": 3.00,  "output": 15.00, "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/x-ai/grok-3-mini":                 {"input": 0.30,  "output": 0.50,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/google/gemini-2.5-flash-preview":   {"input": 0.15,  "output": 0.60,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/google/gemini-2.0-flash-001":       {"input": 0.10,  "output": 0.40,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/google/gemini-2.5-pro-preview":     {"input": 1.25,  "output": 10.00, "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/moonshot/kimi-k2":                 {"input": 0.60,  "output": 2.50,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/deepseek/deepseek-chat":            {"input": 0.20,  "output": 0.77,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/deepseek/deepseek-r1":              {"input": 0.55,  "output": 2.19,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/mistralai/mistral-large":           {"input": 2.00,  "output": 6.00,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/mistralai/mistral-small":           {"input": 0.10,  "output": 0.30,  "cache_read": 0.0, "cache_write": 0.0},
}
DEFAULT_PRICING = {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75}  # fallback for unknown models

# ── Alert Thresholds ─────────────────────────────────────────────────────────
ALERT_SESSION_USD   = 1.50   # single session cost (was $0.50 — too tight, causing alert spam. Normal cron runs $0.65-$1.41)
ALERT_DAILY_USD     = 15.00  # daily total real API spend (was $2.00 — too tight. Realistic daily is $5-$15 with current crons)
ALERT_MONTHLY_PACE  = 50.00  # projected monthly real API spend (raised from $15 to match MEMORY.md $50/mo goal)
MONTHLY_TARGET      = 50.00  # goal: keep real API costs under $50/mo (Anthropic = subscription, not counted)
RUNAWAY_CALLS       = 10     # API calls in 5 min = runaway
RUNAWAY_WINDOW_SEC  = 300    # 5 minutes


def calc_cost(model: str, input_tokens: int, output_tokens: int,
              cache_read: int = 0, cache_write: int = 0) -> float:
    p = PRICING.get(model, DEFAULT_PRICING)
    return (
        (input_tokens  / 1_000_000) * p["input"] +
        (output_tokens / 1_000_000) * p["output"] +
        (cache_read    / 1_000_000) * p["cache_read"] +
        (cache_write   / 1_000_000) * p["cache_write"]
    )


def ts_to_date(ts_ms: int) -> str:
    """Convert millisecond UTC timestamp to YYYY-MM-DD in EST."""
    dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).astimezone(TZ_EST)
    return dt.strftime("%Y-%m-%d")


def today_est() -> str:
    return datetime.now(tz=TZ_EST).strftime("%Y-%m-%d")


def load_sessions() -> dict:
    if not SESSIONS_FILE.exists():
        return {}
    with open(SESSIONS_FILE) as f:
        return json.load(f)


def snapshot():
    """Capture current sessions.json costs and store in memory/costs/YYYY-MM-DD.json."""
    sessions = load_sessions()
    date_str = today_est()
    out_path = COSTS_DIR / f"{date_str}.json"

    # Load existing snapshot to accumulate (handle sessions updated throughout the day)
    existing = {}
    if out_path.exists():
        with open(out_path) as f:
            existing = json.load(f)

    by_session = existing.get("sessions", {})
    alerts_fired = existing.get("alerts_fired", [])

    for key, session in sessions.items():
        if not isinstance(session, dict):
            continue
        updated_ms = session.get("updatedAt", 0)
        if not updated_ms:
            continue

        sess_date = ts_to_date(updated_ms)
        # Only include sessions last updated today
        if sess_date != date_str:
            continue

        model      = session.get("model", "unknown")
        provider   = session.get("modelProvider", "unknown")
        inp        = session.get("inputTokens", 0) or 0
        out        = session.get("outputTokens", 0) or 0
        cr         = session.get("cacheRead", 0) or 0
        cw         = session.get("cacheWrite", 0) or 0
        total_tok  = session.get("totalTokens", 0) or 0
        label      = session.get("label") or "Main Session"
        cost       = calc_cost(model, inp, out, cr, cw)

        by_session[key] = {
            "label":        label,
            "model":        model,
            "provider":     provider,
            "input_tokens": inp,
            "output_tokens": out,
            "cache_read":   cr,
            "cache_write":  cw,
            "total_tokens": total_tok,
            "cost_usd":     round(cost, 6),
            "updated_at":   updated_ms
        }

    total_cost = sum(s["cost_usd"] for s in by_session.values())
    models_used = {}
    for s in by_session.values():
        m = s["model"]
        if m not in models_used:
            models_used[m] = {"sessions": 0, "input_tokens": 0, "output_tokens": 0,
                               "cache_read": 0, "cache_write": 0, "cost_usd": 0.0}
        models_used[m]["sessions"]      += 1
        models_used[m]["input_tokens"]  += s["input_tokens"]
        models_used[m]["output_tokens"] += s["output_tokens"]
        models_used[m]["cache_read"]    += s["cache_read"]
        models_used[m]["cache_write"]   += s["cache_write"]
        models_used[m]["cost_usd"]      = round(models_used[m]["cost_usd"] + s["cost_usd"], 6)

    # ── OpenRouter real billing (source of truth) ────────────────────────────
    or_billing = fetch_openrouter_billing()
    real_total_usage = or_billing.get("total_usage", 0.0)
    real_balance = (or_billing.get("total_credits", 0) - real_total_usage
                   if "error" not in or_billing else None)

    # Compute today's real spend from delta (if we have a previous entry)
    real_today_cost = 0.0
    if "error" not in or_billing:
        log = load_or_billing_log()
        # Find the most recent entry for a DIFFERENT date
        today_str = today_est()
        for entry in reversed(log):
            if entry["date"] != today_str:
                prev_usage = entry["total_usage"]
                real_today_cost = round(max(0.0, real_total_usage - prev_usage), 6)
                break
        # Save today's entry
        save_or_billing_entry(real_total_usage, or_billing.get("total_credits", 0))

    snapshot_data = {
        "date":           date_str,
        "captured_at":    datetime.now(timezone.utc).isoformat(),
        "total_usd":       round(total_cost, 6),          # estimated from session tokens (deprecated)
        "sessions":        by_session,
        "by_model":        models_used,
        "alerts_fired":    alerts_fired,
        # Real OpenRouter billing (source of truth)
        "openrouter": {
            "total_usage":      round(real_total_usage, 6),
            "balance_remaining": round(real_balance, 6) if real_balance is not None else None,
            "today_cost":       real_today_cost,         # actual spend since last snapshot
            "from_api":          "error" not in or_billing,
        }
    }

    with open(out_path, "w") as f:
        json.dump(snapshot_data, f, indent=2)

    print(json.dumps({"status": "ok", "date": date_str, "total_usd": round(total_cost, 4),
                      "sessions": len(by_session)}, indent=2))


def load_snapshot(date_str: str) -> Optional[dict]:
    p = COSTS_DIR / f"{date_str}.json"
    if not p.exists():
        return None
    with open(p) as f:
        return json.load(f)


def report(period: str) -> dict:
    """Generate cost report for today, yesterday, week, or month."""
    today = today_est()
    today_dt = datetime.strptime(today, "%Y-%m-%d")

    if period == "today":
        dates = [today]
    elif period == "yesterday":
        d = today_dt - timedelta(days=1)
        dates = [d.strftime("%Y-%m-%d")]
    elif period == "week":
        dates = [(today_dt - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    elif period == "month":
        year, month = today_dt.year, today_dt.month
        dates = []
        d = today_dt
        while d.month == month:
            dates.append(d.strftime("%Y-%m-%d"))
            d -= timedelta(days=1)
    else:
        return {"error": f"Unknown period: {period}"}

    total_usd = 0.0
    by_model = {}
    top_sessions = []
    days_with_data = 0

    for date_str in dates:
        snap = load_snapshot(date_str)
        if not snap:
            continue
        days_with_data += 1
        total_usd += snap.get("total_usd", 0)

        for m, stats in snap.get("by_model", {}).items():
            if m not in by_model:
                by_model[m] = {"sessions": 0, "input_tokens": 0, "output_tokens": 0,
                                "cache_read": 0, "cache_write": 0, "cost_usd": 0.0}
            for k in ["sessions", "input_tokens", "output_tokens", "cache_read", "cache_write"]:
                by_model[m][k] += stats.get(k, 0)
            by_model[m]["cost_usd"] = round(by_model[m]["cost_usd"] + stats.get("cost_usd", 0), 6)

        for sid, s in snap.get("sessions", {}).items():
            top_sessions.append({
                "date":       date_str,
                "label":      s["label"],
                "model":      s["model"],
                "cost_usd":   s["cost_usd"],
                "output_tokens": s["output_tokens"]
            })

    top_sessions.sort(key=lambda x: x["cost_usd"], reverse=True)

    return {
        "period":          period,
        "total_usd":       round(total_usd, 4),
        "days_with_data":  days_with_data,
        "by_model":        by_model,
        "top_sessions":    top_sessions[:5],
    }


def check_alerts() -> list:
    """Check all alert thresholds. Returns list of alert dicts.
    Uses real OpenRouter billing API as the source of truth for daily/monthly costs."""
    today = today_est()
    today_dt = datetime.strptime(today, "%Y-%m-%d")
    alerts = []

    # ── Real OpenRouter billing (source of truth) ───────────────────────────
    or_billing = fetch_openrouter_billing()
    real_today_cost = 0.0
    real_month_total = 0.0
    real_balance = None

    if "error" not in or_billing:
        total_credits = or_billing.get("total_credits", 0)
        total_usage   = or_billing.get("total_usage", 0)
        real_balance  = round(total_credits - total_usage, 2)

        # Compute monthly from billing log (sum of daily deltas this month)
        billing_log = load_or_billing_log()
        month_str   = f"{today_dt.year}-{today_dt.month:02d}"
        prev_usage  = None

        for entry in billing_log:
            if entry.get("date", "").startswith(month_str):
                u = entry.get("total_usage", 0)
                if prev_usage is not None:
                    delta = max(0.0, u - prev_usage)
                    real_month_total += delta
                prev_usage = u

        # Today's cost: delta from yesterday's last known usage
        for i in range(len(billing_log) - 1, -1, -1):
            entry = billing_log[i]
            if entry.get("date") != today:
                prev_usage = entry.get("total_usage", 0)
                real_today_cost = round(max(0.0, total_usage - prev_usage), 2)
                break

    # ── Session-level alerts (estimated, for debugging) ──────────────────────
    sessions = load_sessions()
    for key, session in sessions.items():
        if not isinstance(session, dict):
            continue
        model = session.get("model", "unknown")
        inp   = session.get("inputTokens", 0) or 0
        out   = session.get("outputTokens", 0) or 0
        cr    = session.get("cacheRead", 0) or 0
        cw    = session.get("cacheWrite", 0) or 0
        label = session.get("label") or "Main Session"
        cost  = calc_cost(model, inp, out, cr, cw)

        # Only alert on truly expensive sessions (real cost would be much lower now)
        if cost >= 5.00:  # raised threshold since estimates are inflated
            alerts.append({
                "type":    "session_high",
                "level":   "warning",
                "message": f"💸 Session '{label}' estimated ${cost:.3f} (model: {model})",
                "data":    {"session": key, "cost_usd_est": round(cost, 4), "model": model,
                            "note": "estimate — real cost much lower with corrected pricing"}
            })

    # ── Daily total alert (use real OpenRouter billing) ─────────────────────
    if real_today_cost > 0 and real_today_cost >= ALERT_DAILY_USD:
        alerts.append({
            "type":    "daily_high",
            "level":   "critical",
            "message": f"🚨 Daily spend ${real_today_cost:.2f} exceeded ${ALERT_DAILY_USD} limit!",
            "data":    {"daily_usd": round(real_today_cost, 2), "source": "openrouter_api"}
        })

    # ── Monthly pace alert (use real OpenRouter billing) ────────────────────
    days_in_month = 28
    day_of_month  = today_dt.day
    if day_of_month >= 1 and real_month_total > 0:
        daily_avg    = real_month_total / day_of_month
        monthly_pace = daily_avg * days_in_month

        if monthly_pace >= MONTHLY_TARGET:
            level = "critical" if monthly_pace >= ALERT_MONTHLY_PACE else "warning"
            alerts.append({
                "type":    "monthly_pace",
                "level":   level,
                "message": f"📈 Monthly pace ${monthly_pace:.2f} — {'exceeds $50 cap' if monthly_pace >= ALERT_MONTHLY_PACE else f'above ${MONTHLY_TARGET} goal'} (${real_month_total:.2f} real spend this month)",
                "data":    {
                    "month_total":   round(real_month_total, 2),
                    "pace":          round(monthly_pace, 2),
                    "target":        MONTHLY_TARGET,
                    "balance":       real_balance,
                    "source":        "openrouter_api"
                }
            })

    # ── Deduplicate against already-alerted today ────────────────────────────
    dedup_file = COSTS_DIR / "alerts-sent.json"
    today_str = today_est()
    try:
        with open(dedup_file) as f:
            dedup_state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dedup_state = {"_last_date": ""}

    # Reset if new day
    if dedup_state.get("_last_date") != today_str:
        dedup_state = {"_last_date": today_str}

    sent_keys = set(v for k, v in dedup_state.items() if k != "_last_date")

    new_alerts = []
    for alert in alerts:
        key = f"{alert['type']}:{alert['message']}"
        if key not in sent_keys:
            new_alerts.append(alert)
            dedup_state[key] = key  # mark as sent
        # else: skip duplicate

    # Persist updated dedup state
    dedup_state["_last_date"] = today_str
    with open(dedup_file, "w") as f:
        json.dump(dedup_state, f)

    return new_alerts


def check_runaway() -> list:
    """Check for runaway cron loops: >10 runs in 5 minutes."""
    if not CRON_RUNS_FILE.exists():
        return []

    now_ms = datetime.now(timezone.utc).timestamp() * 1000
    window_ms = RUNAWAY_WINDOW_SEC * 1000
    recent_runs = []

    with open(CRON_RUNS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = entry.get("ts", 0)
            if ts and (now_ms - ts) <= window_ms:
                recent_runs.append(entry)

    alerts = []
    if len(recent_runs) >= RUNAWAY_CALLS:
        # Group by summary prefix (task name)
        by_task = {}
        for r in recent_runs:
            task_key = r.get("summary", "")[:60]
            by_task.setdefault(task_key, []).append(r)

        for task, runs in by_task.items():
            if len(runs) >= RUNAWAY_CALLS:
                alerts.append({
                    "type":    "runaway_loop",
                    "level":   "critical",
                    "message": f"🚨 RUNAWAY LOOP: Task fired {len(runs)}x in {RUNAWAY_WINDOW_SEC//60} min! Task: '{task[:50]}...'",
                    "data":    {"run_count": len(runs), "task": task, "window_sec": RUNAWAY_WINDOW_SEC}
                })

    return alerts


def brief() -> str:
    """Human-readable cost section for morning brief."""
    yesterday = (datetime.now(tz=TZ_EST) - timedelta(days=1)).strftime("%Y-%m-%d")
    today = today_est()
    today_dt = datetime.strptime(today, "%Y-%m-%d")

    lines = ["💰 *API Cost Summary*"]
    lines.append("_Anthropic/Claude: covered by OAuth subscription ($0 API charge)_")

    # ── Real OpenRouter billing (source of truth) ─────────────────────────
    or_billing = fetch_openrouter_billing()
    billing_log = load_or_billing_log()
    month_str = f"{today_dt.year}-{today_dt.month:02d}"

    real_month_total = 0.0
    real_yesterday_cost = 0.0
    real_balance = None

    if "error" not in or_billing and billing_log:
        total_credits = or_billing.get("total_credits", 0)
        total_usage   = or_billing.get("total_usage", 0)
        real_balance  = round(total_credits - total_usage, 2)

        # Build dict of date → total_usage for quick lookup
        date_usage = {e["date"]: e["total_usage"] for e in billing_log}

        # Yesterday's cost: if both yesterday and today in log → delta; else latest entry
        all_keys = sorted(date_usage.keys())
        if yesterday in date_usage and today in date_usage:
            # Both days in log: today's total - yesterday's total = yesterday's spend
            real_yesterday_cost = round(max(0.0, date_usage[today] - date_usage[yesterday]), 2)
        elif yesterday in date_usage:
            # Only yesterday in log (today not snapshotted yet)
            if len(all_keys) >= 2 and all_keys[-2] == yesterday:
                real_yesterday_cost = round(max(0.0, date_usage[yesterday] - date_usage[all_keys[-2]], 2))
            else:
                real_yesterday_cost = round(max(0.0, date_usage[yesterday]), 2)

        # Monthly cost = sum of daily deltas this month
        month_keys = sorted(k for k in date_usage if k.startswith(month_str))
        for i, dk in enumerate(month_keys):
            if i > 0:
                real_month_total += round(max(0.0, date_usage[dk] - date_usage[month_keys[i-1]]), 2)

    # Show yesterday's real spend
    lines.append(f"Yesterday: *${real_yesterday_cost:.2f}* (OpenRouter real billing)")

    # Show real balance
    if real_balance is not None:
        bal_color = "✅" if real_balance > 10 else ("⚠️" if real_balance > 3 else "🚨")
        lines.append(f"  Balance: ${real_balance:.2f} remaining {bal_color}")

    budget_pct = (real_month_total / MONTHLY_TARGET) * 100 if MONTHLY_TARGET > 0 and real_month_total > 0 else 0
    bar_filled = min(int(budget_pct / 10), 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)
    status = "✅" if budget_pct < 80 else ("⚠️" if budget_pct < 100 else "🚨")
    lines.append(f"Month real API spend: *${real_month_total:.2f}* / ${MONTHLY_TARGET:.0f} target {status}")
    lines.append(f"  [{bar}] {budget_pct:.0f}%")

    # X API costs
    import json as _json
    from datetime import timedelta as _td
    x_log = os.path.join(COSTS_DIR, "x-api.jsonl")
    x_today = 0.0
    x_week = 0.0
    x_month = 0.0
    X_WEEKLY_TARGET = 10.0
    if os.path.exists(x_log):
        try:
            week_ago = (datetime.now(tz=TZ_EST) - _td(days=7)).strftime("%Y-%m-%d")
            x_month_str = today_dt.strftime("%Y-%m")
            with open(x_log) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = _json.loads(line)
                        d = entry.get("date", "")
                        c = entry.get("cost_usd", 0)
                        if d == today:
                            x_today += c
                        if d >= week_ago:
                            x_week += c
                        if d.startswith(x_month_str):
                            x_month += c
                    except Exception:
                        pass
        except Exception:
            pass
    x_status = "✅" if x_week < X_WEEKLY_TARGET * 0.8 else ("⚠️" if x_week < X_WEEKLY_TARGET else "🚨")
    lines.append(f"𝕏 API (this week): *${x_week:.2f}* / ${X_WEEKLY_TARGET:.0f} target {x_status}  (today: ${x_today:.3f} | month: ${x_month:.2f})")

    return "\n".join(lines)


def weekly_review() -> str:
    """Weekly optimization review for Sunday brief."""
    today = today_est()
    today_dt = datetime.strptime(today, "%Y-%m-%d")

    r = report("week")
    lines = [
        "📊 *Weekly Cost Optimization Review*",
        f"Total 7-day spend: *${r['total_usd']:.3f}*",
        ""
    ]

    # Spend by model
    if r["by_model"]:
        lines.append("*By model tier:*")
        for model, stats in sorted(r["by_model"].items(), key=lambda x: -x[1]["cost_usd"]):
            pct = (stats["cost_usd"] / r["total_usd"] * 100) if r["total_usd"] > 0 else 0
            lines.append(f"  • {model}: ${stats['cost_usd']:.3f} ({pct:.0f}% of total, {stats['sessions']} sessions)")

    # Top sessions
    if r.get("top_sessions"):
        lines.append("")
        lines.append("*Most expensive sessions:*")
        for s in r["top_sessions"][:3]:
            lines.append(f"  • {s['date']} | {s['label']}: ${s['cost_usd']:.3f} ({s['model']})")

    # Routing suggestions
    lines.append("")
    lines.append("*Routing observations:*")
    by_model = r.get("by_model", {})
    expensive_sessions = [s for s in r.get("top_sessions", []) if s["cost_usd"] > 0.10 and "sonnet" in s["model"].lower()]
    if expensive_sessions:
        lines.append(f"  ⚠️ {len(expensive_sessions)} Sonnet sessions over $0.10 — review if Groq could handle them")
    groq_usage = by_model.get("llama-3.3-70b-versatile", {})
    sonnet_usage = by_model.get("claude-sonnet-4-6", {})
    if groq_usage.get("sessions", 0) == 0:
        lines.append("  💡 Groq (Llama) unused this week — check heartbeat/simple cron routing")
    elif groq_usage.get("sessions", 0) < 3:
        lines.append(f"  💡 Groq only used {groq_usage['sessions']}x — more lightweight tasks could route there")

    # Monthly projection
    month_snap_dates = []
    d = today_dt
    month_total = 0.0
    while d.month == today_dt.month:
        snap = load_snapshot(d.strftime("%Y-%m-%d"))
        if snap and snap.get("total_usd", 0) > 0:
            month_total += snap["total_usd"]
            month_snap_dates.append(d.strftime("%Y-%m-%d"))
        d -= timedelta(days=1)

    if len(month_snap_dates) > 0:
        daily_avg = month_total / len(month_snap_dates)
        pace = daily_avg * 28
        lines.append("")
        lines.append(f"Monthly pace: *${pace:.2f}* (target: ${MONTHLY_TARGET:.0f})")
        if pace > MONTHLY_TARGET:
            lines.append(f"  ⚠️ On track to exceed goal by ${pace - MONTHLY_TARGET:.2f}")
        else:
            lines.append(f"  ✅ ${MONTHLY_TARGET - pace:.2f} headroom to goal")

    # OpenRouter efficiency check
    or_check = check_openrouter_efficiency()
    if or_check:
        lines.append("")
        lines.append(or_check)

    return "\n".join(lines)


def log_experiment(model: str, task: str, cost: float, verdict: str = ""):
    """Log a new model experiment to memory/costs/model-experiments.jsonl."""
    experiments_file = COSTS_DIR / "model-experiments.jsonl"
    entry = {
        "date":    today_est(),
        "model":   model,
        "task":    task,
        "cost":    round(cost, 6),
        "verdict": verdict
    }
    with open(experiments_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(json.dumps({"status": "logged", "entry": entry}))


def check_openrouter_efficiency() -> str:
    """Check if any OpenRouter model is used heavily enough to warrant a direct key."""
    today = today_est()
    today_dt = datetime.strptime(today, "%Y-%m-%d")

    # Last 30 days
    or_totals = {}
    d = today_dt
    for _ in range(30):
        snap = load_snapshot(d.strftime("%Y-%m-%d"))
        if snap:
            for model, stats in snap.get("by_model", {}).items():
                if model.startswith("openrouter/"):
                    if model not in or_totals:
                        or_totals[model] = {"sessions": 0, "cost_usd": 0.0}
                    or_totals[model]["sessions"]  += stats.get("sessions", 0)
                    or_totals[model]["cost_usd"]  += stats.get("cost_usd", 0.0)
        d -= timedelta(days=1)

    if not or_totals:
        return ""

    lines = ["*OpenRouter usage (last 30 days):*"]
    flagged = []
    for model, stats in sorted(or_totals.items(), key=lambda x: -x[1]["cost_usd"]):
        lines.append(f"  • {model}: ${stats['cost_usd']:.3f} ({stats['sessions']} sessions)")
        # Flag if monthly cost > $5 on this model (direct key would save ~10%)
        if stats["cost_usd"] > 5.00:
            flagged.append(model)

    if flagged:
        lines.append("")
        lines.append("⚡ *Consider direct API keys for:*")
        for m in flagged:
            provider = m.split("/")[1] if "/" in m else m
            lines.append(f"  • {provider} (>{or_totals[m]['cost_usd']:.2f}/mo — direct key saves ~10%)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw cost tracker")
    parser.add_argument("--snapshot",      action="store_true",  help="Capture today's costs")
    parser.add_argument("--report",        metavar="PERIOD",     help="Report: today|yesterday|week|month")
    parser.add_argument("--check-alerts",  action="store_true",  help="Check thresholds, return JSON alerts")
    parser.add_argument("--brief",         action="store_true",  help="Morning brief cost section (plain text)")
    parser.add_argument("--weekly-review", action="store_true",  help="Weekly review text")
    parser.add_argument("--check-runaway", action="store_true",  help="Check for runaway cron loops")
    args = parser.parse_args()

    if args.snapshot:
        snapshot()
    elif args.report:
        print(json.dumps(report(args.report), indent=2))
    elif args.check_alerts:
        alerts = check_alerts() + check_runaway()
        print(json.dumps(alerts, indent=2))
    elif args.brief:
        print(brief())
    elif args.weekly_review:
        print(weekly_review())
    elif args.check_runaway:
        alerts = check_runaway()
        print(json.dumps(alerts, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
