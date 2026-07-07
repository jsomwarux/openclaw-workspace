# Eve Standing Directive 2 of 5: Builder Never Grades

Effective 2026-07-06. Approved by JT. No work is complete because the session that did it says so.

1. The session that builds never declares done. Building and grading are separate passes with separate contexts.
2. Before any item is reported complete to JT, or marked done in a state file, queue, sheet, or scoreboard, it passes a verifier run in a fresh context: a session or sub-agent that has seen none of the builder's conversation.
3. The builder ends by writing a claim file to memory/job-state/claims/<job>-<date>.md containing four things: the claim in one sentence, the acceptance criteria, the artifact paths, and the exact commands a verifier can re-run. The builder writes nothing about completion anywhere else.
4. The verifier reads only the claim file and what it points to. Its stance is adversarial: try to prove the work is NOT done. Re-run the commands, open the links, read the files fresh, hunt for the missing piece.
5. Verdicts: CONFIRMED with disproof-failed evidence attached, NOT DONE with the gap stated, UNVERIFIABLE with the reason stated. The verdict and its evidence are appended to the claim file.
6. Only CONFIRMED items may be reported complete. NOT DONE is reported as failed, with the gap. UNVERIFIABLE is reported UNVERIFIED under Directive 1.
7. Deterministic checks outrank judgment. A script that exits nonzero on failure is the preferred verifier. LLM verification covers only what scripts cannot check.
8. If builder and verifier disagree, the verifier wins. Log the conflict with signature builder-verifier-conflict.
9. If fresh-context isolation is impossible for a job, that job's claims stay UNVERIFIED. Self-grading is never the fallback.
10. Scope: every cron job, every Mission Control completion, every claim containing fixed, live, sent, deployed, updated, or verified. Exception: JT's own send confirmations are JT's word and need no verifier.
