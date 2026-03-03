# CLAUDE.md - Optimal Development Instructions

## Session Start

1. **Review lessons first.** Read `tasks/lessons.md` before doing anything. Orient around past mistakes.
2. **Review the task list.** Check `tasks/todo.md` for current state.
3. **Then proceed.**

---

## Critical Rules

### Model & Verification
**Always use Opus 4.5+ with thinking.** Less steering, better tool use, faster overall.

**Always verify your work.** Never mark a task complete without proving it works:
- Run the test suite
- Start the dev server and test functionality
- Use browser automation to verify UI changes
- Diff behavior between main and your changes
- Check logs, demonstrate correctness
- Ask yourself: **"Would a staff engineer approve this?"**

**Self-review before presenting.** Challenge your own work before showing it to the user. Don't wait to be asked.

### When You Make a Mistake
**Update lessons immediately.** End every correction with:
> "Update `tasks/lessons.md` so you don't make that mistake again."

You are eerily good at writing rules for yourself. Do it.

### Minimal Impact
Changes should only touch what's necessary. Don't refactor unrelated files. Don't introduce bugs in code you weren't asked to change. Surgical precision.

---

## Task Management

Every session uses `tasks/todo.md` and `tasks/lessons.md`:

1. **Plan First:** Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan:** Check in with the user before starting implementation
3. **Track Progress:** Mark items complete as you go
4. **Document Results:** Add review section to `tasks/todo.md` when done
5. **Capture Lessons:** Update `tasks/lessons.md` after corrections

```
tasks/
  todo.md       # Current task plan with checkable items
  lessons.md    # Accumulated rules from past mistakes
```

---

## Mistakes / Lessons Log

*Claude: Write rules for yourself in `tasks/lessons.md`. Review at every session start.*

```
# Format: - [Date] Rule learned from mistake
# Example: - [2026-01] Never use TypeScript enums; always use string literal unions
# Example: - [2026-01] Always run typecheck after making changes
```

---

## Parallelism Options

### Option 1: Git Worktrees (Manual)
Run 3-5 worktrees simultaneously, each with its own Claude session.

```bash
# Create worktrees
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
git worktree add ../project-analysis main  # Read-only for logs/queries

# Shell aliases for instant switching
alias za="cd ../project-feature-a && claude"
alias zb="cd ../project-feature-b && claude"
alias zc="cd ../project-analysis && claude"
```

**Best for:** When you want manual control over parallel sessions.

### Option 2: Agent Teams (Automated - Experimental)
Multiple Claude instances coordinated by a lead agent. Teammates work in parallel on shared codebase.

**Enable:**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
# Or add to settings.json
```

**Usage:**
```
Create an agent team for this project:
- One teammate on frontend components
- One teammate on API routes
- One teammate on tests
Each should work independently and coordinate via the task list.
```

**How it works:**
- Lead agent creates shared task list and spawns teammates
- Teammates run in independent context windows (split panes via tmux/iTerm2)
- Teammates communicate via inbox files
- Lead synthesizes findings and manages completion

**Best for:** Complex projects that can be parallelized. Research tasks needing multiple perspectives.

**Limitations:**
- Experimental, token-intensive
- No session resumption
- Requires tmux or iTerm2 for split-pane mode
- Break work so each teammate owns different files (avoid overwrites)

---

## Plan Mode Strategy

### When to Use Plan Mode
Enter plan mode for ANY task with **3+ steps or architectural decisions.** No ambiguity — if it's 3+ steps, plan first.

Press `shift+tab` twice. Pour energy into the plan so Claude can 1-shot the implementation.

### Two-Claude Review Pattern
1. Have one Claude write the plan
2. Spin up a second Claude to review it as a staff engineer
3. Only proceed when the plan passes review

### When Things Go Sideways
**STOP. Re-plan. Don't keep pushing.**

The moment something goes wrong, switch back to plan mode and re-plan. Don't iterate on a bad approach.

### Plan Mode for Verification Too
Use plan mode not just for building, but for verification steps. Plan HOW you will prove the work is correct before doing it.

---

## Development Philosophy

### No Stubs, No Placeholders, No Slop

**CRITICAL:** Always implement fully finished, production-ready code.

- **No stubs or TODOs** - Complete implementations only
- **No try/catch or defensive patterns** unless genuinely necessary
- **No hardcoded values** masquerading as dynamic behavior
- **No mocks of code under test** - Integration tests against real code
- **No verbose comments** restating the obvious
- **No over-abstraction** - Keep it as simple as possible

### Core Principles

- **Simplicity First:** Make every change as simple as possible. Minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Changes should only touch what's necessary. Avoid introducing bugs.

### Before Writing Code

1. **Search the codebase first** - Don't assume not implemented
2. **Clarify the goal** - What exactly needs to be built and why?
3. **Identify constraints** - Dependencies, edge cases, limitations
4. **Use Context7** for up-to-date library documentation

### Demand Elegance (Balanced)

For non-trivial changes, pause and ask: "Is there a more elegant way?"

If a fix feels hacky:
> "Knowing everything you know now, scrap this and implement the elegant solution."

**But skip this for simple, obvious fixes.** Don't over-engineer a one-line bug fix.

---

## Advanced Prompting Techniques

### Make Claude Your Reviewer
```
"Grill me on these changes and don't make a PR until I pass your test."
```

### Prove It Works
```
"Prove to me this works. Diff the behavior between main and this feature branch."
```

### Challenge Mode
```
"Review this as a senior staff engineer. What would you push back on?"
```

### Fresh Start After Learning
```
"Knowing everything you know now, scrap this and implement the elegant solution."
```

### Throw More Compute
```
"[Your request] - use subagents"
```

---

## Bug Fixing - Trust Claude

**Pattern 1: Slack MCP + "Fix"**
```
[paste Slack bug thread]
"Fix this."
```

**Pattern 2: CI Failures**
```
"Go fix the failing CI tests."
```

**Pattern 3: Distributed Systems**
```
"Here are the docker logs. Troubleshoot this."
```

---

## Skills

Skills are reusable instruction packages that teach Claude specific workflows. They load automatically when relevant.

### Built-in Skills
- `xlsx` - Excel spreadsheets with formulas
- `pptx` - PowerPoint presentations
- `docx` - Word documents
- `pdf` - PDF manipulation, form filling

### When to Create Custom Skills
- Workflow you repeat across multiple projects
- Domain-specific conventions (your UI patterns, API structure)
- Team standards that should be consistent
- Complex multi-step processes that need precise execution

### Skill Structure
```
.claude/skills/[skill-name]/
  SKILL.md      # Instructions with YAML frontmatter
  scripts/      # Optional executable scripts
  references/   # Optional reference docs
```

### Example Custom Skill
```markdown
# .claude/skills/dashboard-setup/SKILL.md
---
name: dashboard-setup
description: Use when creating new dashboard projects. Sets up Next.js with standard patterns.
---

## Setup Steps
1. Initialize Next.js with App Router and TypeScript
2. Add Tailwind CSS with custom color palette
3. Create standard component structure
4. Set up API route patterns for Gumloop integration

## Standard Components
- ScoreCard, ConsensusPanel, AnalysisTimeline
- Use shadcn/ui for base components

## File Structure
src/
  app/
    api/         # API routes
    dashboard/   # Dashboard pages
  components/
    ui/          # Base components
    features/    # Feature-specific
```

### Skill Locations
```
~/.claude/skills/           # Personal (all projects)
.claude/skills/             # Project (team shared, commit to git)
```

---

## Slash Commands

### Rule: If You Do It More Than Once a Day, Make It a Command

### Essential Commands

**/techdebt** - Run at end of every session
```markdown
# .claude/commands/techdebt.md
Find and report duplicated code, unused imports, inconsistent patterns,
and potential simplifications. Prioritize by impact.
```

**/context-dump** - Sync recent activity into context
```markdown
# .claude/commands/context-dump.md
Sync the last 7 days of activity from Slack, GDrive, Asana, and GitHub
into a single context summary. Highlight decisions, blockers, and action items.
```

**/commit-push-pr** - Daily inner-loop command
```markdown
# .claude/commands/commit-push-pr.md
$ARGUMENTS: Commit message

1. git status
2. git add -A
3. git commit -m "$ARGUMENTS"
4. git push
5. Create PR with description
```

### Skills vs Commands
- **Skills**: Loaded automatically when relevant, can include scripts, for complex workflows
- **Commands**: Invoked explicitly with `/name`, for quick actions

---

## Subagents

Use subagents to offload tasks and keep main context clean:
- Append **"use subagents"** for compute-heavy tasks
- One task per subagent for focused execution
- Research, exploration, and parallel analysis

### Permission Security Hook
Route permission requests to Opus for intelligent auto-approval:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "type": "command",
        "command": "claude --model opus -p 'Evaluate this permission request for security risks. If safe, respond ALLOW. If suspicious, respond DENY with reason: $PERMISSION_REQUEST'"
      }
    ]
  }
}
```

---

## MCP Servers

### Context7 (Required)
Up-to-date library documentation. Eliminates hallucinated APIs.

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

### Slack MCP (Recommended)
Paste bug threads directly, say "fix."

### Database CLI
Use `bq` CLI for BigQuery, or any database with CLI/MCP/API.

---

## Terminal & Environment

### Voice Dictation
Hit **fn x2** on macOS. 3x faster, more detailed prompts.

### Status Line
```
/statusline
```
Always show context usage and git branch.

### Recommendations
- **Ghostty** or iTerm2 for terminal
- Color-code terminal tabs per worktree
- tmux for session persistence and agent teams

---

## Quality Gates

### Self-Review Checklist
- **Would a staff engineer approve this?**
- Does it actually work (verified with real execution)?
- Did I only touch what was necessary?
- Did I introduce any bugs in unrelated code?
- Is there a simpler way to do this?

### LARP Check - Is This Code Real?
- Stubbed functions returning fake data?
- Hardcoded values pretending to be dynamic?
- Tests mocking the logic being tested?
- Error handling that silently swallows failures?
- Async code that doesn't actually await?

### Slop Removal
- Unnecessary abstractions and wrappers
- Verbose comments restating the obvious
- Defensive code for impossible conditions
- Over-generic solutions for specific problems

---

## Technique Selection

### Quick Decision
```
Vague requirements? → GSD (/gsd:new-project)
Clear specs + want autonomy? → Ralph Wiggum
Complex parallel work? → Agent Teams
Quick bug fix? → Just "fix it"
```

### GSD Commands
```
/gsd:new-project      # Start with deep interview
/gsd:plan-phase N     # Create atomic task plans
/gsd:execute-phase N  # Autonomous execution
```

### Ralph Wiggum
For well-defined specs with clear acceptance criteria:
```bash
./ralph.sh plan 5     # Generate plan from specs
./ralph.sh 30         # Autonomous implementation
```

---

## Hooks

### PostToolUse - Auto-Format
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command", 
            "command": "npm run format || true"
          }
        ]
      }
    ]
  }
}
```

---

## Permissions

Pre-allow safe commands:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build:*)",
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(bq:*)"
    ]
  }
}
```

---

## Project Configuration

### Build & Run
```bash
# Add your project's commands
npm run dev        # Development server
npm run build      # Production build
npm run typecheck  # Type checking
npm run test       # Tests
npm run lint       # Linting
```

### Code Style
```
# Add your conventions
```

### Architecture
```
# Add your project structure
```

---

## Workflow Summary

```
SESSION START:
  Review tasks/lessons.md → Review tasks/todo.md → Orient

PLANNING (3+ steps or architectural decisions):
  Plan mode → Write tasks/todo.md → Verify plan → Proceed

IMPLEMENTATION:
  Follow plan → Complete code only → Track progress

PARALLELISM (complex projects):
  Option A: Git worktrees (manual control)
  Option B: Agent teams (automated coordination)

VERIFICATION:
  Run tests → Diff against main → "Would a staff engineer approve?"

SELF-REVIEW:
  LARP check → Slop removal → Minimal impact audit

COMPLETION:
  Document results → Update lessons.md → Present work

REMEMBER:
  1. Plan first (3+ steps) - pour energy into plan
  2. Write your own rules - update lessons.md after mistakes
  3. Verify everything - prove it works
  4. Self-review before presenting
  5. Minimal impact - only touch what's necessary
  6. Parallel sessions - worktrees or agent teams for complex work
  7. Skills for repeated workflows - codify once, reuse everywhere
  8. Voice dictation - fn x2, 3x faster prompting
```
