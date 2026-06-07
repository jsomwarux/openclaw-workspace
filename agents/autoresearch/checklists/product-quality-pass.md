# Product Quality Pass Autoresearch Checklist

1. Does the pass inspect the recent diff and project instructions before making claims?
2. Does it remove or flag needless abstractions, duplicated logic, unclear names, placeholder code, fake data, and dead routes/buttons?
3. Does it explicitly check for LARP risks where UI appears complete but behavior is unwired or mocked?
4. Does it run the appropriate verification commands for the repo, including build/typecheck/lint/tests and browser/native checks where relevant?
5. Does the report separate fixes made from remaining blockers or risks?
6. Does it avoid declaring success unless the verification output actually passed?
