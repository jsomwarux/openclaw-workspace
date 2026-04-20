# Notion Database Automation Skill
> Unified capability for programmatically interacting with JT's Notion Content Calendar and Swipe Databases.

## Description
This skill leverages OpenClaw's existing Python scripts to directly inject planned social media text, case study links, and viral research straight into the Notion workspace. Used for scheduling marketing material or logging competitive data.

## Usage
`openclaw sessions_spawn --agentId [id] --task "Scrape recent tweets on [Topic] and save them to Notion using the notion-integration skill"`
For Codex: "When the new app feature is built, draft a launch post and schedule it via the Notion python framework."

## Execution Framework (Python Mapping)
The heavy lifting is handled by Python scripts in the `scripts/` directory. No new auth logic is needed.

**1. The Calendar Engine (`notion-calendar-push.py`):**
Use this to push pending or planned content to the editorial calendar database.
- Command pattern: `python3 scripts/notion-calendar-push.py --platform "[X|LinkedIn]" --date "YYYY-MM-DD" --post "[Message Text]" --type "Planned" --drive-link "[URL]"`

**2. The Swipe File Engine (`notion-swipe-push.py`):**
Use this to save viral hooks, competitive intelligence, or high-performing posts for future reference.
- Command pattern: `python3 scripts/notion-swipe-push.py --text "..." --author "@handle" --url "..." --niche "[Niche]" --format "[Format]" --why "..." --engagement [Count] --hook "[Hook text]"`
