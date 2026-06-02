# Agentforce/Data Cloud Proof-Pack Research — 2026-06-01

## Why This Matters Now

The 2026-06-01 skills audit queued `Skills gap: build Agentforce/Data Cloud implementation proof pack`. The market signal supports a narrow proof-pack angle: buyers and hiring managers are asking for Agentforce fluency, but the practical risk is still data readiness, governance, scope, and cost control.

## Fresh Signals

- Thinklytics frames 2026 Data Cloud consulting around focused first-wave deployments, with a useful benchmark of roughly three months for 3-5 source systems, 2-3 activation destinations, and one segmentation pattern. This supports a scoped "first useful slice" proof pack instead of a broad platform transformation.
- Salesforce Admins' May 2026 Agentforce examples emphasize privacy-minimized intake, deterministic business rules, real-time Salesforce data, and explainable ranking. This is a strong proof-pack pattern: show the agent's input limits, retrieval source, ranking rules, and human handoff.
- Recent pricing guides keep pointing at the same buyer anxiety: Agentforce plus Data Cloud can create hidden cost lines through edition upgrades, Data Cloud storage, SI work, and usage/credit consumption. A useful proof pack should include a cost/risk assumptions page, not just architecture.
- Existing local reference `docs/tools/salesforce-data-cloud.md` already has the conceptual spine: Data Streams, Data Graphs, Unified Profiles, grounding/RAG, Data Libraries vs manual RAG, and honest hands-on boundaries.

## Proof-Pack Shape

Use a concise private artifact with five sections:

1. **Fit filter:** Salesforce edition, current clouds, number of source systems, data owner, target workflow, support volume, and whether Data Cloud is already enabled.
2. **Source map:** each data source, owner, freshness, PII/sensitive fields, allowed agent actions, and unresolved data quality risks.
3. **Grounding design:** Agentforce Data Library for unstructured docs when speed matters; manual Data Stream/DLO/DMO/Search Index/Retriever path when structured or multi-source precision matters.
4. **Pilot scope:** one workflow, one audience, one retrieval layer, one human-review route, and explicit "out of scope" rules for Apex-heavy customization.
5. **Proof artifacts:** before/after workflow map, 20-50 prompt/eval cases, fallback examples, hallucination/incorrect-source checks, cost assumptions, and rollback/signoff criteria.

## JT Translation

Best immediate lane: position this as "agent readiness and proof pack" rather than "Salesforce implementation." JT can credibly show architecture, governance, evaluation, and rollout discipline without overclaiming deep Apex or full SI ownership.

For consulting: tie the offer to AI Context OS. The same source-of-truth map, escalation rules, and eval pack already used for property ops can become the pre-Agentforce readiness artifact for Salesforce-heavy companies.

For job-market proof: translate Altmark/Aya/OpenClaw systems into the same categories hiring teams use: discovery, data architecture, guardrails, workflow automation, human review, monitoring, and ROI.

## Sources Checked

- Salesforce Admins, "11 Award-Winning Agentforce Solutions To Inspire Your Next Build", 2026-05-13
- Thinklytics, "Salesforce Data Cloud Consulting in 2026", 2026-05-01
- RizeX Labs, "Agentforce Pricing Licensing Guide 2026", 2026-05-13
- Ekfrazo, "Salesforce Agentforce Pricing 2026", 2026-05-27
- Local reference: `docs/tools/salesforce-data-cloud.md`

