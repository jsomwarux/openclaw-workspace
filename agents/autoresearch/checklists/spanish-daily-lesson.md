# Spanish Daily Lesson Cron — Autoresearch Checklist

Score each generated lesson/run against these yes/no checks:

1. Does the lesson use `write`/full JSON overwrite for `spanish/state.json`, never brittle exact-text edit?
2. Does it verify `spanish/state.json` parses after update and that `last_lesson_date` equals the lesson date?
3. Does Telegram delivery status show delivered, or does the run fail loudly with enough context to resend?
4. Does the lesson save `spanish/lessons/YYYY-MM-DD.md` with topic/phrases covered?
5. Does the lesson stay within the 10-minute structure: review, 3–4 phrases, mini-practice, real-world challenge, TTS phrase audio?
6. Does it avoid duplicate topics from the prior two lesson files unless explicitly reviewing?
