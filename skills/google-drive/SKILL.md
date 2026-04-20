# Google Drive Automation Skill
> Unified capability for pushing drafts, resumes, presentations, and client documents to Google Drive.

## Description
This skill leverages OpenClaw's existing Python scripts to directly upload generated text, markdown files, and formatted decks to specific Google Drive directories (using `openclawagenteve14@gmail.com` via service accounts). 

## Usage
`openclaw sessions_spawn --agentId [id] --task "Draft a cold email and upload it to Drive using the google-drive skill"`
For Codex: "Output the final deployment keys directly to Google Drive using the Python scripts mapped in this skill."

## Execution Framework (Python Mapping)
The heavy lifting is handled by Python scripts in the `scripts/` directory. No new auth logic is needed.

**1. The Drafts Engine (`drive_drafts.py`):**
Use this to securely push single files or text blobs.
- Command pattern: `python3 scripts/drive_drafts.py --title "[Title]" --path "[Target/Path/In/Drive]" --file [local_path]`

**2. The Consulting Pipeline Engine (`pipeline_drive_sync.py`):**
Use this to push entire client folders, decks, and outreach templates to the `Consulting/Clients/[Name]` folder.
- Command pattern: `python3 scripts/pipeline_drive_sync.py --slug [client_slug] --client "[Client Name]" --stage [deck|outreach|all]`

## Common Drive Paths
When using `drive_drafts.py`, use these exact `--path` values:
- Cold Outreach DMs: `Consulting/Clients/[Client]/Outreach/LinkedIn`
- X Posts: `Content/X/Bank`
- Resumes: `Job Applications/Resumes`
