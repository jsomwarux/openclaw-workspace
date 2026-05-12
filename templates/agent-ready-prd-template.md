# Agent-Ready PRD Template

Use before handing a software/app/build task to a coding agent, n8n agent, Agentforce agent, or client implementation workflow.

The goal is not a corporate PRD. The goal is to remove ambiguity for an AI builder.

**Recommended save path:** project root `tasks/prd.md`, client/prospect folder `prd.md`, or `memory/drafts/[slug]-prd.md` for early concepts. Link it from `tasks/todo.md` before coding begins.

## 1. Product Overview
- **Project title:**
- **One-sentence summary:**
- **Primary user:**
- **Core job to be done:**
- **Current workflow/problem:**

## 2. Goals
### Business goals
- Goal:
  - Success metric:
  - Baseline:
  - Target:
  - Timeframe:

### User goals
- Goal:
  - Success metric:
  - Baseline:
  - Target:
  - Timeframe:

### Non-goals
- Explicitly out of scope:

## 3. Personas and Access
- **Primary persona:**
- **Secondary persona(s):**
- **Role-based access:** single-role / admin-editor-viewer / owner-member-guest / other
- **Permissions by role:**

## 4. User Stories
Use stable IDs.

- **US-1:** As a [persona], I want to [action] so that [outcome].
- **US-2:**

## 5. Functional Requirements
Every requirement should be testable and map to one or more user stories.

- **FR-1:** [testable requirement] — implements US-[x]
- **FR-2:**

## 6. User Experience
- **Entry point:**
- **First-time flow:**
- **Core flow:**
- **Edge cases:**
- **Empty/error/loading states:**
- **Mobile/responsive needs:**
- **UI style references:**

## 7. Data, Integrations, and Privacy
- **Data sources:**
- **External APIs/tools:**
- **Auth/secrets needed:**
- **Storage:**
- **Sensitive data boundaries:**
- **Audit/logging needs:**

## 8. Technical Considerations
- **Preferred stack:**
- **Known constraints:**
- **Performance targets:**
- **Failure modes:**
- **Security risks:**
- **Manual fallback:**

## 9. Build Phases
Order by dependency, not calendar time.

### Phase 1 — Scaffold / data model / auth
- 

### Phase 2 — Core workflow
- 

### Phase 3 — polish / edge cases / observability
- 

## 10. Agent Handoff
- **Files/repo to inspect first:**
- **Commands to run first:**
- **Definition of done:**
- **Verification gate:** build / test / lint / screenshot / live URL / sample run
- **Do not touch:**
- **Questions/blockers:**

## Consistency Check
Before handing off, verify:
- Each user story maps to at least one FR.
- Each business/user goal has a success metric.
- Each metric has baseline/target/timeframe or is explicitly `_TBD_`.
- Personas match the goals and access model.
- Build phases include the minimum scaffold before UI/polish.
- No fabricated numbers, integrations, schemas, or claims.

## Review Notes
### Weak spots
- 

### Suggested validations
- 
