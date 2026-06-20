# Spanish Daily Lesson Cron — Autoresearch Checklist

Score each generated lesson/run against these yes/no checks:

1. Does the lesson use `write`/full JSON overwrite for `spanish/state.json`, then verify valid JSON and today's `last_lesson_date` with `python3 scripts/spanish_state_check.py --date YYYY-MM-DD --require-today`?
2. Does Telegram delivery status show delivered, or does the run fail loudly with enough context to resend?
3. Does the lesson save `spanish/lessons/YYYY-MM-DD.md` with topic, curriculum week, phrases covered, practice prompts, challenge, and anti-repeat result?
4. Does the lesson stay within the 10-minute structure: review, 3-4 phrases, mini-practice, real-world challenge, and TTS phrase audio?
5. Does it avoid duplicate topics from the prior two lesson files unless explicitly labeling the lesson as review?
6. Does it fail loudly instead of recycling old material when the current curriculum week is missing?
