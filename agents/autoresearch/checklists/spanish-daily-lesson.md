# Spanish Daily Lesson Cron — Autoresearch Checklist

Score each generated lesson/run against these yes/no checks:

1. Does the lesson use `write`/full JSON overwrite for `spanish/state.json`, never brittle exact-text edit?
2. Does it verify `spanish/state.json` parses after update and that `last_lesson_date` equals the lesson date?
3. Does `python3 scripts/spanish_state_check.py --date YYYY-MM-DD --require-today` pass after the run?
4. Does Telegram delivery status show delivered, or does the run fail loudly with enough context to resend?
5. Does the lesson save `spanish/lessons/YYYY-MM-DD.md` with topic/phrases covered?
6. Does the lesson stay within the 10-minute structure: review, 3–4 phrases, mini-practice, real-world challenge, TTS phrase audio?
7. Does it avoid duplicate topics from the prior two lesson files unless explicitly reviewing?
8. Does the 10PM accountability path validate state before nudging, so stale/broken state cannot trigger a false reminder?
