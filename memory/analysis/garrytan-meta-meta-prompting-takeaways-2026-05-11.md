# Garry Tan Meta-Meta-Prompting / GBrain Post — Takeaways for JT/Eve

Date: 2026-05-11  
Source: JT pasted X/article text + live `garrytan/gbrain` README check + prior Eve GBrain eval.

## Main read
The post is directionally correct. The real unlock is not “better prompts.” It is compounding operational memory:

- Thin harness: OpenClaw routes work.
- Fat skills: reusable workflows with triggers, edge cases, quality gates, and model routing.
- Fat data: structured, source-attributed knowledge pages that accumulate over time.
- Eval loop: every bad output creates a permanent skill/rule/check improvement.

This is already how Eve works in miniature: AGENTS.md, skills, MEMORY.md, daily notes, Mission Control, LCM, qmd, and cron workflows. Garry's stack is the more graph-native, entity-propagating version.

## What matters for us
1. **Skillification is the highest-ROI habit.**
   When we repeat a workflow twice, extract it into a skill or checklist. The value is not the first output. The value is that every correction compounds.

2. **Entity propagation is the missing layer.**
   Our daily notes and client files capture facts, but meeting/prospect/client updates do not automatically propagate to person/company/opportunity pages. This is the most useful GBrain-style pattern for consulting.

3. **Cross-model eval should be used selectively.**
   We do not need model councils for every task. Use them for high-stakes artifacts: outreach campaigns, consulting offers, job applications, landing page positioning, and portfolio proof points.

4. **Do not replace lossless-claw.**
   LCM is for conversation recall. GBrain/qmd-style brain is for durable world knowledge: people, companies, client history, source-backed research, content ideas, meeting notes.

5. **The book-mirror concept maps to JT content/strategy.**
   Not a priority to mirror books right now. Better adaptation: “market mirror” and “client/prospect mirror” workflows that map external signals to JT's actual positioning, proof points, and offers.

## What to implement now
### 1. Pilot GBrain only on consulting pipeline recall
Use the existing MC task. Keep scope narrow:
- `~/projects/jt-consulting-pipeline/clients`
- `~/projects/jt-consulting-pipeline/prospects`
- `memory/networking`
- selected `memory/analysis` docs

Success test: answer 20 real questions better than qmd/grep, especially relationship and prospect-history queries.

### 2. Create/upgrade a Skillify-style workflow for Eve
We already have `skill-creator`, but not a standing “turn this repeated workflow into a reusable skill/checklist” process. The optimal implementation is a lightweight `workflow-skillify` skill that:
- detects repeated workflow
- extracts trigger phrases
- writes edge cases
- adds quality gates
- adds regression checks
- registers/autoresearches if recurring

### 3. Add entity propagation for consulting/client work
Whenever a client/prospect note changes:
- update company page
- update contact/person page if known
- update opportunity/pipeline status
- update source note/daily note

This should be a skill or script before it becomes a cron.

### 4. Add a small eval harness for high-stakes drafts
For outreach/positioning, have one critic pass check:
- generic language
- unsupported claims
- wrong ICP
- bad CTA
- missing proof
- stale source

DeepSeek/GPT/Claude model routing is optional. The important part is the fixed rubric.

## What not to do
- Do not ingest secrets, credentials, raw private chats, or sacred config files.
- Do not install every GBrain cron/job blindly.
- Do not add 100 crons. JT's cron cap and reliability matter more.
- Do not overbuild book-mirror before consulting pipeline recall is solved.
- Do not put huge new instructions in AGENTS.md; use focused skills/files.

## Recommendation
Proceed in this order:
1. Tighten existing MC task: Pilot GBrain for consulting pipeline recall.
2. Create a lightweight Skillify-style skill/checklist for repeated Eve workflows.
3. Add a consulting entity-propagation template/script.
4. Add an outreach/positioning eval checklist.

This is the highest-leverage adaptation of Garry's post for JT: not copying the whole stack, but adopting the compounding loops that directly improve consulting acquisition and delivery.
