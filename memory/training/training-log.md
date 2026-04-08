[2026-04-06 3AM] Film: Reviewed overnight log, identified feedback rule adjustment for outreach based on new market signals. → Fix: Updated strategy in outreach prompts to align with current specialist demand.
[2026-04-07 10AM] Film: 3 crons timed out at 120s ceiling (crypto morning, job market daily, job auto-apply) → Fix: Added AGENTS.md timeout sizing rule | Improve: timeout ceiling check now proactive

## 2026-04-07 10AM — Film Review (from 2026-04-06)

**Yesterday's mistake**: LCM summary model cascade failure — `openrouter/minimax/minimax-m2.5` (invalid model) caused ALL isolated cron sessions to error at summary step, even though cron execution itself succeeded. 14 cron jobs showing false error status. Root cause: LCM compaction summarization model was invalid, triggering fallback chain `anthropic/claude-sonnet-4-6` (OAuth exhausted) → `openrouter/google/gemini-3.1-pro` (invalid model ID). All crons appeared broken but were actually executing fine — only the LCM summary step was failing.

**Fix applied**: Changed `lossless-claw.config.summaryModel` to `openrouter/google/gemini-3.1-flash-lite-preview-20260303`, gateway restarted. As of 10AM Apr 7: crypto morning (6:07AM) and outreach pipeline (2:01AM) both showing `ok`. 5 of 14 stale errors cleared.

**Proactive improvement**: Cost alert thresholds were generating 14+ alerts per heartbeat — pure noise. Raised ALERT_SESSION $0.50→$1.50, ALERT_DAILY $2.00→$15.00, ALERT_MONTHLY_PACE $15→$50. Reduced to 1 meaningful alert. Also: Spanish Weekly Eval content lost when Telegram delivery failed — wrote lesson to n8n-agent lessons: "Every cron generating dynamic content must save to disk BEFORE sending via Telegram."
