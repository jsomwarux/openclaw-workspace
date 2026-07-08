# Eve Standing Directive 5 of 5: Repeat Offender Digest

Effective 2026-07-06. Approved by JT. The same failure twice is a pattern, not bad luck.

1. Every Friday, inside the Friday Scoreboard run and before the scoreboard sends, read every run log from the last 7 days: proofs/*/actions.jsonl, cron run records, docs/agents/mistakes-log.md, all state files, and all claim files with verdicts.
2. Normalize each failure to a signature: fabricated-artifact, pseudo-command, builder-verifier-conflict, redid-logged-work, state-skip, auth-failure, timeout, delivery-failure, unverified-claim, scope-creep, or other with a short name.
3. A repeat offender is any signature appearing 2 or more times in the week, within one job or across jobs. The pattern is the unit, not the job.
4. For each repeat offender record: signature, jobs affected, count, dates, prior fix attempts with links, and exactly one proposed structural fix. A structural fix changes a prompt, a script, a schedule, or kills the job. A re-run is never a fix.
5. Save the digest to memory/audits/repeat-offenders/YYYY-MM-DD.md. The scoreboard SYSTEM line carries one line: offender count, worst signature, and the proposed fix staged as a yellow item for JT's keyword.
6. Three strikes, pre-approved here: a signature appearing in 3 consecutive digests for the same job pauses that job automatically, reported the same day with evidence. Re-enabling is red and requires JT.
7. A zero-failure week reports 0 repeat offenders plus coverage: files read versus files present. Coverage under 100 percent makes the digest UNVERIFIED under Directive 1.
8. The digest reads logs and never rewrites them. Deleting lines, reclassifying old failures, or improving counts is fabrication under Directive 1 with signature fabricated-artifact.
