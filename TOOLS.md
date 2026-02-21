# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Firecrawl

- **API Key:** `fc-0d0961fa920a466a869fdd4068b9fe7e`
- **Endpoint:** `https://api.firecrawl.dev`
- **Scrape:** `POST /v1/scrape` with `{"url": "...", "formats": ["markdown"]}`
- **Auth header:** `Authorization: Bearer fc-0d0961fa920a466a869fdd4068b9fe7e`

### Pipeline: Brave → Firecrawl
1. Use `web_search` (Brave) to find relevant URLs
2. Use `web_fetch` or call Firecrawl `/v1/scrape` directly to get full page content as markdown
3. Firecrawl handles JS-heavy pages and bot circumvention that plain `web_fetch` can't

---

Add whatever helps you do your job. This is your cheat sheet.
