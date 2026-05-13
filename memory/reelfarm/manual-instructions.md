# Manual setup for JT — Social Growth Engineers → ReelFarm Intel

## Option A — simplest now
1. Open the Social Growth Engineers newsletter email.
2. Copy the full email body.
3. Save it as a text/markdown file named `YYYY-MM-DD-social-growth-engineers.md`.
4. Put it in `~/.openclaw/workspace/memory/reelfarm/newsletters/inbox/`.

Eve's daily cron runs at 5:15 PM ET and will process anything new in that inbox.

## Option B — better once Drive OAuth is fixed
Forward the newsletter to a dedicated Gmail label/folder, then Eve can poll with gog/Gmail once credentials are working. This removes manual file drops.

Current recommendation: use Option A for the first week. It is reliable, auditable, and lets us validate output quality before automating ingestion.

## Option C — fully automated Gmail ingestion
Once Google OAuth is connected, Eve's daily ReelFarm cron runs at 5:15 PM ET and will run:
`python3 ~/.openclaw/workspace/scripts/reelfarm_gmail_ingest.py`

It searches Gmail for Social Growth Engineers messages, writes new emails into the newsletter inbox, dedupes processed Gmail message IDs, and never sends/modifies mail.

Manual OAuth setup required once:
1. Open Terminal.
2. Run:
   `gog auth add openclawagenteve14@gmail.com --services gmail --gmail-scope readonly --force-consent`
3. Complete the browser Google consent flow.
4. Verify:
   `gog auth list`
5. Test ingestion:
   `python3 ~/.openclaw/workspace/scripts/reelfarm_gmail_ingest.py`
6. Confirm it prints `GMAIL_INGEST_OK`.
## Gmail unread behavior
The Social Growth Engineers Gmail ingest uses read-only Gmail access and does not mark messages as read, archive them, label them, or otherwise modify Gmail. Unread emails in `openclawagenteve14@gmail.com` can still have been scraped and analyzed. The source of truth is `memory/reelfarm/gmail-state.json` plus files moved into `memory/reelfarm/newsletters/processed/`.
