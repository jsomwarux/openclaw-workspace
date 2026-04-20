# System Auditor Skill
> Unified capability for logging proofs, tracking cross-project costs, and verifying system file integrity.

## Description
This skill leverages OpenClaw's existing system-level tracking scripts to ensure autonomous actions, refactors, and cron loops are logged securely, within budget, and without corrupting critical files. Essential for safe multi-file edits.

## Usage
`openclaw sessions_spawn --agentId [id] --task "Check API costs using the system-auditor skill before starting this project"`
For Codex: "Run a cost snapshot before and after this deep refactor, and log the execution proof in the system-auditor framework."

## Execution Framework (Python Mapping)
The heavy lifting is handled by Python scripts in the `scripts/` directory.

**1. The Proof Logger (`log-proof.py`):**
Use this to create an immutable audit trail of actions taken, outcomes, and modified files.
- Command pattern: `python3 scripts/log-proof.py --type "code_refactor" --title "[Task Title]" --description "[Details]" --outcome "[success|failure|partial]" --files "[file1,file2]"`

**2. The Cost Tracker (`cost-tracker.py`):**
Use this to fetch current total session, daily, and monthly API spend against the $50/mo goal.
- Command pattern: `python3 scripts/cost-tracker.py --brief | --snapshot | --check-alerts`

**3. The File Integrity Check (`critical-files-integrity.py`):**
Use this to ensure your changes didn't corrupt the `AGENTS.md` rules, JSON database schemas, or OpenClaw configurations.
- Command pattern: `python3 scripts/critical-files-integrity.py`
