# TOOLS.md - Tool Reference
> Check this file before saying "I can't." Full command syntax lives in `docs/tools/TOOLS-full.md`.

## Health System
- DB: `health/health.sqlite`; daily 9PM check-in, Sunday 9AM report.
- Use `health/health.py` for log/report/history and `health/inbound_handler.py` for JT replies.
- Full syntax: `docs/tools/TOOLS-full.md#health-system`.

## Spanish Learning
- State: `spanish/state.json`; lessons: `spanish/lessons/YYYY-MM-DD.md`; cron `babd905a-1098-49dd-8700-772fef14f817`.
- Validate with `scripts/spanish_state_check.py`; delivery truth is the latest cron run deliveryStatus.
- Full syntax: `docs/tools/TOOLS-full.md#spanish-learning`.

## Cost Tracker
- Script: `scripts/cost-tracker.py`; common modes: snapshot, brief, check-alerts, weekly-review, check-runaway.
- `--diagnose` is not supported. Routing guard: `scripts/model_routing_guard.py --include-disabled`.
- Full syntax: `docs/tools/TOOLS-full.md#cost-tracker`.

## Audit Trail
- Proof log: `scripts/log-proof.py`; proof guard: `scripts/memory_recap_proof_guard.py`.
- Daily proof JSONL: `proofs/YYYY-MM-DD/actions.jsonl`.
- Full syntax: `docs/tools/TOOLS-full.md#audit-trail`.

## Restart / Gateway Recovery
- Approved restart path: `scripts/restart-gateway.sh "reason"`; no raw gateway restart unless explicitly approved.
- Gateway freeze/cooldown recovery details moved to full docs. Never raise `bootstrapMaxChars` above 32000.
- Full syntax: `docs/tools/TOOLS-full.md#restart-script` and `docs/tools/TOOLS-full.md#gateway-freeze--rate-limit-recovery`.

## Image / OCR
- OpenClaw image attachments require `sharp` in the OpenClaw node_modules tree.
- OCR fallback: Homebrew `tesseract`; full install/use notes in full docs.
- Full syntax: `docs/tools/TOOLS-full.md#image--ocr-tooling`.

## Diagnostics
- `openclaw doctor`; `openclaw doctor --fix` only when something is broken and root cause is unclear.

## Web / X Research
- Fresh web research: use `scripts/web_search.py` with freshness filters; do not use managed web_search for freshness/date filters.
- X research skill wrapper: `skills/x-research`; cheap default is quick limit 5.
- Full syntax: `docs/tools/TOOLS-full.md#canonical-web-search` and `docs/tools/TOOLS-full.md#x-research-skill`.

## Backups / Session Cleanup / Task Queue
- Backup script: `scripts/backup.sh`; cleanup script: `scripts/cleanup-sessions.py`.
- Task queue: `tasks/pending.jsonl`; every 2h 8AM-10PM ET.
- Full syntax: `docs/tools/TOOLS-full.md#backups`.

## Knowledge Base / Skills Scout
- KB lives in `knowledge/kb.sqlite`; CLI is `knowledge/kb.ts`.
- SkillsMP Scout is pattern intelligence only; never auto-install marketplace skills.
- Full syntax: `docs/tools/TOOLS-full.md#knowledge-base` and `docs/tools/TOOLS-full.md#skillsmp-scout`.

## Mission Control Dashboard
- Next.js: `http://localhost:3000`; Convex: 3210/3211; tailnet: `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n: `/n8n`.
- If unreachable, kickstart Mission Control LaunchAgents immediately; Tailscale serve recovery details are in full docs.
- Task API is primary for priorities; task creation examples live in full docs.
- Full syntax: `docs/tools/TOOLS-full.md#mission-control-dashboard` and `docs/tools/TOOLS-full.md#mission-control--task-push`.

## Claude Code Agent Personas
- Full persona table: `docs/tools/claude-personas.md`.
- Quick map: frontend, AI/Agentforce, backend, rapid POC, review.

## Consulting / Project Agents
- Project roots: `~/projects/research-agent`, `analysis-agent`, `n8n-agent`, `agentforce-agent`, `crypto-agent`, `job-market-agent`, `ranking-app-agent`.
- Crypto full-analysis validator/writer/pipeline commands moved to full docs.
- Consulting pipeline skill: `skills/opticfy-pipeline/SKILL.md`; command details in full docs.
- Full syntax: `docs/tools/TOOLS-full.md#consulting-pipeline-agents-projects`.

## Salesforce Data Cloud
- Real-time CDP/Data 360 grounding path for Agentforce; details: `docs/tools/salesforce-data-cloud.md`.

## Drive Drafts
- Script: `scripts/drive_drafts.py`; account root: `Eve - Drafts`.
- Reusing title/path updates the existing Google Doc. Corrected high-stakes drafts require live doc verification.
- Full syntax: `docs/tools/TOOLS-full.md#drive-drafts`.

## Consulting Pipeline Drive Sync
- Script: `scripts/pipeline_drive_sync.py`; outreach confirmation: `scripts/outreach_update.py`; email pivot: `scripts/outreach_email_pivot.py`.
- Full syntax: `docs/tools/TOOLS-full.md#consulting-pipeline-drive-sync`.

## Notion
- DBs: Viral Post Swipe File `31316aff930580f6a195ca179793eb0e`; Content Calendar `32516aff930581a78659eac869c71ba8`.
- Use env `NOTION_TOKEN`; never paste tokens. Push/fetch/calendar command syntax moved to full docs.
- Cron truth: `Viral Post Swipe File - X Research`, Mon/Wed/Fri 5:45AM ET; model defaults follow cron config, not a standing isolated-sonnet rule.
- Full syntax: `docs/tools/TOOLS-full.md#notion`.

## Apps
- `jtsomwaru.com`: `~/projects/jtsomwaru-com/` -> Vercel.
- Glow Index: Replit / `jsomwarux/skincare-rankings`; fresh build required before redeploy.
- Nash Satoshi: `jsomwarux/Nash-Satoshi` private.
- Full ops details: `docs/tools/TOOLS-full.md#apps`.
