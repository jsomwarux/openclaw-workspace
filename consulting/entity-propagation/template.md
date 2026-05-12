# Consulting Entity Propagation Template

Use when a client, prospect, contact, job-signal lead, or meeting note changes.

## Trigger
A durable fact changes about a consulting entity: status, contact, pain signal, outreach, meeting, proposal, delivery, objection, or next action.

## Propagate to
1. **Source note**: the file where the fact originated.
2. **Company/prospect page**: `~/projects/jt-consulting-pipeline/[clients|prospects]/[slug]/`.
3. **Contact/person page** if known: `memory/networking/contacts.md` or client contact file.
4. **Pipeline/status file** if present.
5. **Compiled consulting wiki**: update or create relevant page(s) under `consulting/wiki/pages/` and update `consulting/wiki/index.md` + `consulting/wiki/log.md` when the fact is durable/reusable.
6. **Daily note**: `memory/YYYY-MM-DD.md`.
7. **Mission Control** task if a concrete action exists.

## Required fields
- Entity name
- Date
- Source/evidence link or file
- What changed
- Why it matters
- Next action
- Owner: Eve or JT
- Status: active / waiting / sent / passed / stalled / done

## Guardrails
- Never infer a contact relationship that is not sourced.
- Never mark outreach sent unless JT confirms or tool evidence proves it.
- Do not create MC tasks without a specific first action and done state.
- If a source is stale or removed, record it as market intel only.

## Done check
The same fact should not conflict across MEMORY.md, prospect folder, consulting wiki, daily note, and Mission Control.
