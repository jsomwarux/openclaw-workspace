# Local Archive Workflows — birdclaw, notcrawl, gog

Purpose: add high-signal local memory sources without increasing OpenClaw bootstrap size or creating privacy-heavy automation.

## Installed now

### birdclaw — X/Twitter local workspace
- Installed: `birdclaw` v0.1.1 via `brew install steipete/tap/birdclaw`
- Local state:
  - `~/.birdclaw/config.json`
  - `~/.birdclaw/birdclaw.sqlite`
  - `~/.birdclaw/media/`
- Safe commands:
  - `birdclaw db stats --json`
  - `birdclaw archive find --json`
  - `birdclaw import archive --json`
- Current mode: local only unless `xurl` is installed/configured.
- Workflow fit:
  - X content mining from JT's archive/bookmarks/likes
  - “Have I already said this?” checks before drafting posts
  - Nash/Dynasty/Vista angle mining from saved X material
  - Future X Lists workflow companion, not replacement

### gog — Google Workspace CLI
- Installed: `gog` v0.13.0 via `brew install steipete/tap/gogcli`
- Config path: `~/Library/Application Support/gogcli/config.json`
- Agent safety defaults:
  - Use `--json --no-input` for scripting.
  - Use `--gmail-no-send` by default.
  - Confirm with JT before Gmail sends or Calendar event creation.
- Workflow fit:
  - Drive search/export verification for deliverables
  - Gmail read/search triage if JT explicitly authorizes
  - Sheets/Docs export/cat/copy for structured artifacts

## Staged, not installed yet

### notcrawl — Notion SQLite/Markdown mirror
- No Homebrew formula found as of 2026-04-26.
- Repo exists: `vincentkoc/notcrawl`.
- Install later from source only after reviewing build steps.
- Workflow fit:
  - Mirror Notion content calendar/swipe file locally
  - Local weekly content review and backup
  - Avoid depending on Notion UI for content memory

## Explicitly skipped for now

### beeper
- Reason: privacy-heavy personal chat history. Only add if JT asks for chat-history search.

### wacrawl
- Reason: WhatsApp is not currently a core business/source channel.

### discrawl/slacrawl
- Reason: useful only if Discord/Slack become high-signal communities for JT.

## Integration rules
1. Read/search/export first; no auto-sending messages or external posts.
2. Do not add personal chat archives to recurring workflows without JT approval.
3. Keep workflow docs here instead of bloating TOOLS.md.
4. If a CLI requires OAuth/auth, create a JT-owned manual auth task; do not attempt account auth silently.
5. Any recurring cron using these tools must include an empty-result guard and cost/runtime expectations.
