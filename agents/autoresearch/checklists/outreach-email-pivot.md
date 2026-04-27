# Autoresearch Checklist — outreach-email-pivot daily cron
*6 yes/no questions. Run against the last 3 outreach email pivot outputs/runs.*

1. Does the run stop safely when Drive OAuth is missing, creating or referencing exactly one auth recovery item instead of generating duplicate outreach/MC tasks?
2. Does the run correctly identify only prospects where M2 was sent 7+ days ago, M3 has not been sent, and no email pivot already exists?
3. For each generated pivot, does it use a materially different angle from the LinkedIn M1/M2 hook and include the local draft path?
4. Does the run verify the email address when available, or clearly mark inferred/unverified emails before any send/review task is created?
5. Does the run create at most one Mission Control task per company/contact pivot and cite evidence of de-duplication?
6. Does the run exit silently when zero new pivots are created, without sending noisy Telegram updates or failing the cron?
