# Revenue Signal Lab Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the outdated Grok Bot setup with one canonical, revenue-first Grok Project and weekday Automation guide.

**Architecture:** A standalone setup guide owns all copy-ready Grok configuration. The historical operating-system redesign points to it as the governing source. Drive reuses the existing Agent Operating System document so JT has one current link.

**Tech Stack:** Markdown, Google Drive draft sync, deterministic text checks, independent document review.

---

## Chunk 1: Canonical setup and source reconciliation

### Task 1: Write the canonical setup guide

**Files:**
- Create: `deliverables/revenue-signal-lab-setup-2026-08-25.md`

- [ ] Write the exact Project name, description, instructions, privacy boundary, Automation prompt, schedule, output schema, example, four-week test, handoff, and troubleshooting.
- [ ] Confirm the prompt has Task Context, Detailed Rules, Immediate Task, and Output Formatting.
- [ ] Scan for secrets and private client detail.

### Task 2: Reconcile the historical redesign

**Files:**
- Modify: `deliverables/agent-operating-system-redesign-2026-08-24.md`
- Modify: `plans/agent-operating-system-redesign-2026-08-24.md`
- Modify: `MEMORY.md`
- Modify: `~/.claude/CLAUDE.md`

- [ ] Mark Bot-specific setup as historical and superseded.
- [ ] Point all governing references to the canonical setup guide.
- [ ] Preserve the already-shipped non-Grok architecture.

## Chunk 2: Review, Drive, and proof

### Task 3: Run independent review

- [ ] Have a fresh reviewer check economic focus, privacy, prompt completeness, contradictory instructions, and setup usability.
- [ ] Fix every material issue and repeat review until confirmed.

### Task 4: Update Drive and verify

- [ ] Update the existing `Agent Operating System Redesign — 2026-08-24` Google Doc in `Research/Agent Operating System/` with the reconciled source.
- [ ] Create or update `Revenue Signal Lab — Setup Instructions — 2026-08-25` in the same Drive folder.
- [ ] Read back the live document text and verify canonical Project + Automation language.

### Task 5: Record proof and hand off

- [ ] Update weekly recap and durable memory.
- [ ] Log proof and run the memory/proof guard.
- [ ] Return the canonical Drive link and the first setup action to JT.
