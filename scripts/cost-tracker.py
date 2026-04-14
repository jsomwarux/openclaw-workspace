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

# ── Paths ────────────────────────────────────────────────────────────────────
OPENCLAW_DIR   = Path.home() / ".openclaw"
SESSIONS_FILE  = OPENCLAW_DIR / "agents/main/sessions/sessions.json"
CRON_RUNS_FILE = OPENCLAW_DIR / "cron/runs/undefined.jsonl"
COSTS_DIR      = Path.home() / ".openclaw/workspace/memory/costs"
TZ_EST         = timezone(timedelta(hours=-5))  # EST (no DST correction needed for storage)

COSTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Pricing (per 1M tokens, USD) ─────────────────────────────────────────────
# NOTE: Anthropic models use OAuth subscription token (sk-ant-oat01-*), NOT an API key.
# All Claude model usage is $0 in real API charges — covered by flat Claude subscription.
# Only OpenRouter and Groq entries below represent real billable costs.
PRICING = {
    # Anthropic — $0 real cost (OAuth subscription token, not API key)
    "claude-sonnet-4-6":    {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "claude-opus-4-6":      {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "claude-haiku-4-5":     {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "claude-sonnet-4-5":    {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    "claude-opus-4-5":      {"input": 0.0, "output": 0.0, "cache_read": 0.0, "cache_write": 0.0},
    # Groq (nearly free)
    "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079, "cache_read": 0.0, "cache_write": 0.0},
    "llama-3.1-70b-versatile": {"input": 0.00059, "output": 0.00079, "cache_read": 0.0, "cache_write": 0.0},
    # OpenRouter — via openrouter/ prefix (no caching, OpenRouter markup included)
    "openrouter/openai/gpt-4o":                    {"input": 2.50,  "output": 10.00, "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/openai/gpt-4o-mini":               {"input": 0.15,  "output": 0.60,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/openai/o3-mini":                   {"input": 1.10,  "output": 4.40,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/x-ai/grok-3":                      {"input": 3.00,  "output": 15.00, "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/x-ai/grok-3-mini":                 {"input": 0.30,  "output": 0.50,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/google/gemini-2.5-flash-preview":  {"input": 0.15,  "output": 0.60,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/google/gemini-2.0-flash-001":      {"input": 0.10,  "output": 0.40,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/google/gemini-2.5-pro-preview":    {"input": 1.25,  "output": 10.00, "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/moonshot/kimi-k2":                 {"input": 0.60,  "output": 2.50,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/deepseek/deepseek-chat":            {"input": 0.27,  "output": 1.10,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/deepseek/deepseek-r1":              {"input": 0.55,  "output": 2.19,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/mistralai/mistral-large":           {"input": 2.00,  "output": 6.00,  "cache_read": 0.0, "cache_write": 0.0},
    "openrouter/mistralai/mistral-small":           {"input": 0.10,  "output": 0.30,  "cache_read": 0.0, "cache_write": 0.0},
}
DEFAULT_PRICING = {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75}  # fallback

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

    snapshot_data = {
        "date":        date_str,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "total_usd":   round(total_cost, 6),
        "sessions":    by_session,
        "by_model":    models_used,
        "alerts_fired": alerts_fired
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
    """Check all alert thresholds. Returns list of alert dicts."""
    today = today_est()
    today_dt = datetime.strptime(today, "%Y-%m-%d")
    alerts = []

    # ── Snapshot current data first ──────────────────────────────────────────
    # Re-read live sessions for real-time check
    sessions = load_sessions()
    live_costs = {}
    for key, session in sessions.items():
        if not isinstance(session, dict):
            continue
        model  = session.get("model", "unknown")
        inp    = session.get("inputTokens", 0) or 0
        out    = session.get("outputTokens", 0) or 0
        cr     = session.get("cacheRead", 0) or 0
        cw     = session.get("cacheWrite", 0) or 0
        label  = session.get("label") or "Main Session"
        cost   = calc_cost(model, inp, out, cr, cw)
        live_costs[key] = {"cost": cost, "label": label, "model": model}

        # Single session alert
        if cost >= ALERT_SESSION_USD:
            alerts.append({
                "type":    "session_high",
                "level":   "warning",
                "message": f"💸 Session '{label}' cost ${cost:.3f} (threshold: ${ALERT_SESSION_USD})",
                "data":    {"session": key, "cost_usd": round(cost, 4), "model": model}
            })

    # ── Daily total (from snapshot + live sessions) ──────────────────────────
    snap = load_snapshot(today)
    daily_total = sum(s["cost_usd"] for s in snap.get("sessions", {}).values()) if snap else 0.0
    # Add any live sessions not yet snapshotted
    if snap:
        snapped_keys = set(snap.get("sessions", {}).keys())
        for key, lc in live_costs.items():
            if key not in snapped_keys:
                daily_total += lc["cost"]
    else:
        daily_total = sum(lc["cost"] for lc in live_costs.values())

    if daily_total >= ALERT_DAILY_USD:
        alerts.append({
            "type":    "daily_high",
            "level":   "critical",
            "message": f"🚨 Daily spend ${daily_total:.2f} exceeded ${ALERT_DAILY_USD} limit!",
            "data":    {"daily_usd": round(daily_total, 4)}
        })

    # ── Monthly pace ─────────────────────────────────────────────────────────
    year, month = today_dt.year, today_dt.month
    month_total = 0.0
    d = today_dt
    while d.month == month:
        snap = load_snapshot(d.strftime("%Y-%m-%d"))
        if snap:
            month_total += snap.get("total_usd", 0)
        d -= timedelta(days=1)

    days_in_month = 28  # conservative
    day_of_month  = today_dt.day
    if day_of_month > 1:
        daily_avg   = month_total / day_of_month
        monthly_pace = daily_avg * days_in_month

        if monthly_pace >= MONTHLY_TARGET:
            level = "critical" if monthly_pace >= ALERT_MONTHLY_PACE else "warning"
            alerts.append({
                "type":    "monthly_pace",
                "level":   level,
                "message": f"📈 Monthly pace ${monthly_pace:.2f} — {'exceeds $75 cap' if monthly_pace >= ALERT_MONTHLY_PACE else f'above ${MONTHLY_TARGET} goal'} (${month_total:.2f} spent so far)",
                "data":    {"month_total": round(month_total, 4), "pace": round(monthly_pace, 4), "target": MONTHLY_TARGET}
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

    # Yesterday's data
    y_snap = load_snapshot(yesterday)
    t_snap = load_snapshot(today)  # might be partial (from nightly snapshot)

    lines = ["💰 *API Cost Summary*"]
    lines.append("_Anthropic/Claude: covered by OAuth subscription ($0 API charge)_")

    if y_snap:
        y_total = y_snap["total_usd"]  # now $0 for Anthropic sessions
        y_sessions = y_snap.get("sessions", 28)

        # Show token volume (useful even at $0 cost)
        y_tokens = sum(
            s.get("total_tokens", 0) for s in y_snap.get("session_details", [])
            if "claude" in s.get("model", "").lower() or "anthropic" in s.get("provider", "").lower()
        )
        sess_count = len(y_snap.get('sessions', {})) if isinstance(y_snap.get('sessions'), dict) else y_snap.get('sessions', '?')
        lines.append(f"Yesterday: Anthropic {sess_count} sessions (subscription-covered)")

        # Only show real costs if non-zero
        if y_total > 0.001:
            lines.append(f"  Real API spend (OpenRouter/Groq): *${y_total:.4f}*")
        else:
            lines.append(f"  Real API spend: *$0.00* ✅")
    else:
        lines.append("Yesterday: no data (first run)")

    # Monthly real spend total
    year, month = today_dt.year, today_dt.month
    month_total = 0.0
    d = today_dt
    while d.month == month:
        snap = load_snapshot(d.strftime("%Y-%m-%d"))
        if snap:
            month_total += snap.get("total_usd", 0)
        d -= timedelta(days=1)

    budget_pct = (month_total / MONTHLY_TARGET) * 100 if MONTHLY_TARGET > 0 else 0
    bar_filled = min(int(budget_pct / 10), 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)
    status = "✅" if budget_pct < 80 else ("⚠️" if budget_pct < 100 else "🚨")
    lines.append(f"Month real API spend: *${month_total:.2f}* / ${MONTHLY_TARGET:.0f} target {status}")
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
