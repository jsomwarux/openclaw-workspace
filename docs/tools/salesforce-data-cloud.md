# Salesforce Data Cloud — Reference Doc
> Last updated: 2026-04-02 | Sources: Salesforce Engineering Blog, Trailhead, Salesforce Ben, Torrent Consulting, official Salesforce product pages

---

## What It Is (2 sentences max — for quick recall)

Salesforce Data Cloud (officially rebranding as "Data 360" as of late 2025) is a hyperscale customer data platform (CDP) built natively on the Salesforce Platform that ingests, harmonizes, and unifies structured and unstructured data from any source into real-time customer profiles. It is the data backbone that Agentforce depends on to ground AI agents in accurate, current, customer-specific context — without it, Agentforce is working blind.

---

## Core Concepts

- **Data Streams**: The ingestion pipelines that bring external data into Data Cloud. A Data Stream is a connector configuration that pulls data from a source system (e.g., an ERP, a cloud data warehouse like Snowflake, a Salesforce Sales Cloud org, web clickstream events, or a CSV upload) on a scheduled or real-time basis and maps it to a Data Lake Object (DLO) inside Data Cloud. Example: a retailer sets up a Data Stream from their e-commerce platform to pipe purchase events into Data Cloud every 15 minutes, so customer purchase history is always current. Structured Salesforce data (Sales Cloud, Service Cloud, Marketing Cloud Engagement, Commerce Cloud) can now be ingested via Data Streams at no additional credit cost as of the September 2025 pricing update.

- **Data Graphs**: Dynamic, relationship-aware data structures that connect related Data Model Objects (DMOs) into a traversable graph for low-latency retrieval. Rather than running a SQL join at query time, a Data Graph pre-materializes the relationships between objects (e.g., Account → Cases → Products purchased → Entitlements) so an AI agent can pull a fully contextualized customer record in milliseconds. Dynamic Data Graphs are a core part of Agentforce's grounding strategy — when an agent needs a Customer 360 view mid-conversation, it queries the Data Graph, not individual tables. Example: a service agent handling a billing dispute retrieves the customer's account tier, last 5 interactions, current entitlements, and open cases in a single Data Graph lookup.

- **Unified Profiles**: The harmonized, deduplicated customer identity record that Data Cloud builds by matching and merging data from multiple Data Streams into a single Individual (or Account) profile. Data Cloud uses a rules-based identity resolution engine that matches on email, phone, loyalty ID, and other configured keys — collapsing what might be 4 separate records across CRM, e-commerce, and support systems into one authoritative profile. Example: a customer who appears as "Jon Somwaru" in Salesforce CRM, "jsomwaru@gmail.com" in the email platform, and "account #98231" in the ERP is merged into a single Unified Profile with the full interaction history from all three systems. This unified view is what Agentforce draws on when personalizing responses.

- **Grounding (in Agentforce)**: The mechanism by which Data Cloud injects real-time, customer-specific data into Agentforce agent prompts at the moment of inference, so the LLM responds based on actual facts rather than hallucinated or stale information. Grounding is implemented via Retrieval-Augmented Generation (RAG): when an Agentforce agent receives a user query, it triggers a retriever configured in Einstein Studio, which queries a Data Cloud Search Index or Data Graph to fetch relevant chunks (for unstructured data) or field values (for structured DMOs), and injects that retrieved context directly into the prompt template before the LLM generates a response. There are two setup paths: (1) **Agentforce Data Libraries (ADL)** — a simplified, mostly automated setup for unstructured data (PDFs, FAQs, web content); and (2) **Manual RAG setup** — direct configuration of Data Streams → DLOs → DMOs → Search Index → Retriever → Prompt Template, which gives more control over data sources and retrieval logic. Example: a customer asks "What's my current contract tier?" — the agent's retriever queries the Unified Profile DMO, pulls the entitlement data, injects it into the prompt, and the LLM responds with the actual contract details.

---

## How It Integrates with Agentforce

**Pattern 1 — Prompt Grounding via RAG (most common)**
Data Cloud acts as the retrieval layer for Agentforce prompts. Unstructured content (knowledge articles, product manuals, policy PDFs, web pages) is ingested via Data Streams, chunked and vectorized into a Data Cloud Search Index (native vector database), and exposed to the agent via a Retriever configured in Einstein Studio. When an agent needs to answer a knowledge question, the retriever does a hybrid search (vector + keyword) against the index and injects the top chunks into the Prompt Template. This replaces static knowledge base lookups with dynamic, real-time retrieval from any data source. Built with: Data Stream → DLO → DMO → Search Index → Retriever → Prompt Template → Agent Action.

**Pattern 2 — Real-Time Personalization via Unified Profiles**
Structured customer data (CRM records, purchase history, support cases, loyalty status) is unified into a Unified Profile in Data Cloud. Agentforce agent actions can reference Data Model Objects (DMOs) directly in Prompt Templates using merge fields, pulling live profile data into responses without a separate API call. This enables agents to deliver genuinely personalized experiences — e.g., a service agent that knows a customer's premium tier status, last 3 support cases, and NPS score before saying a word. The zero-copy integration with Snowflake, Databricks, and other warehouses via the Zero Copy Partner Network means this data doesn't have to be physically moved into Salesforce.

**Pattern 3 — Segment-Triggered Agent Actions**
Data Cloud can define real-time segments (e.g., "customers who haven't engaged in 60 days" or "accounts showing churn signals") and trigger automated Agentforce actions when a profile enters or exits a segment. A customer crossing a churn risk threshold can automatically kick off an Agentforce-powered outreach sequence — the agent reaches out with a personalized message grounded in that customer's purchase history and last interaction. This is the bridge from passive data analytics to active, autonomous business action.

---

## Business Value (for consulting pitches)

- **Eliminates the context problem that breaks AI agents.** Agentforce without Data Cloud is an agent that doesn't know who it's talking to. Data Cloud gives agents access to the full customer history — across every system, not just Salesforce CRM — so responses are accurate, relevant, and safe to act on. For SMBs already juggling QuickBooks, a website CRM, and email tools, this unification alone solves a problem they feel every day.

- **Reduces manual data prep and integration work by 60–80%.** Rather than building point-to-point integrations between each system and each AI use case, Data Cloud provides a single ingestion and harmonization layer. New AI use cases draw from the same unified data foundation instead of requiring a new integration project. This compounds over time: each Data Stream built pays dividends across every agent, segment, and insight built on top of it.

- **Turns AI from a demo into an auditable, compliant business system.** Data Cloud's Einstein Trust Layer logs every agent decision — what data was retrieved, what prompt was sent, what response was generated. In regulated industries (healthcare, finance, real estate), this audit trail is the difference between a tool you can deploy to customers and one that stays in a sandbox. For NYC clients in property management or finance, this is a real procurement requirement.

---

## Interview Talking Points

1. **"Data Cloud is what makes Agentforce production-ready."** You can explain the architecture clearly: Data Streams bring in external data, identity resolution builds Unified Profiles, Data Graphs pre-join the relationships so agents can query in milliseconds, and RAG via Search Indexes grounds prompt templates in real facts. Interviewers testing conceptual depth will respond well to this sequence.

2. **"I understand the two grounding paths and when to use each."** Agentforce Data Libraries are the fast path — low-code, automated, good for unstructured content. Manual RAG setup (Data Stream → DLO → DMO → Search Index → Retriever → Prompt Template) gives precise control for structured data, multiple sources, and complex retrieval logic. Knowing this distinction signals hands-on understanding, not just surface awareness.

3. **"Zero Copy is the unlock for enterprises with existing data infrastructure."** Data Cloud's Zero Copy Partner Network lets Agentforce operate on data in Snowflake, Databricks, or BigQuery without physically moving it into Salesforce. For enterprise clients who've already invested in a data warehouse, this is the pitch: you don't have to start over, you layer Agentforce on top of what you have.

4. **"Pricing shifted to a consumption-based model in 2025."** You can speak to the Flex Credits system, Data Service Credits, and the fact that Salesforce-to-Salesforce data ingestion (Sales Cloud, Service Cloud, Marketing Cloud) is now free. This shows you track the commercial side, not just the technical — relevant for Solutions Architect roles where you own scope and cost conversations.

5. **Honest framing of learning edge:** "My current hands-on experience with Data Cloud is at the conceptual and architecture-design level — I've worked with the Agentforce side of the integration and understand how grounding and RAG work in practice. I'm actively completing the Trailhead Data Cloud learning path and building toward the Data Cloud Consultant certification as I deepen this area." This is a confident, honest answer that shows direction and self-awareness without overclaiming.

---

## Pricing / Licensing (brief)

Data Cloud uses a **consumption-based model** as of the September 2025 pricing simplification:

- **Data Service Credits**: The single fungible credit unit used across all Data Cloud functions — ingesting data, unifying profiles, running segments, grounding agents, generating insights. Previously split into four separate credit types (including sandbox and segmentation credits); now consolidated into one.
- **Free Salesforce data ingestion**: As of September 2025, structured data from Salesforce Sales Cloud, Service Cloud, Marketing Cloud Engagement, Marketing Cloud Personalization, and Commerce Cloud can be ingested into Data Cloud at zero credit cost. This significantly reduces onboarding friction for existing Salesforce customers.
- **Salesforce Foundations (Enterprise Edition+)**: All Enterprise Edition and above customers receive 100,000 Flex Credits at no charge — providing a free starting point for Agentforce + Data Cloud experimentation.
- **Agentforce Editions bundle**: Full Agentforce editions include 1 million Flex Credits per org annually (for license-to-compute swaps) plus 2.5 million Data Services Credits per year. This is the bundled path for customers deploying at scale.
- **Storage**: Priced separately from credits; you pay only for what you store.
- **Profiles-based pricing**: Historically, Data Cloud was licensed per Unified Profile (a specific number of profiles included per license tier). The shift to credits-based pricing in 2025 was partly to decouple cost from profile count and make it more usage-proportional.
- **Agentforce conversations**: Separately metered at $2 per conversation (the original rate, still available) or via Flex Credits at a rate that varies by edition.

---

## Key Trailhead Modules

1. **"Explore Data Cloud"** (Trail: `trailhead.salesforce.com/content/learn/trails/explore-customer-360-audiences`) — The primary learning trail covering Data Cloud fundamentals: architecture, data streams, identity resolution, unified profiles, segmentation, and activation. Start here for the foundational layer.

2. **"Data Cloud-Powered Agentforce"** (Module: `trailhead.salesforce.com/content/learn/modules/data-cloud-powered-agentforce`) — Covers the specific integration between Data Cloud and Agentforce, including how to enable trusted agents with Data Cloud, configure Data Libraries, and implement RAG grounding. Directly relevant to interview scenarios and client builds.

3. **"Grounding an Agent with Data"** (Module: `trailhead.salesforce.com/content/learn/modules/grounding-an-agent-with-data`) — Explains the four mechanisms for connecting Agentforce to data (Apex, Flows, Prompt Templates, MuleSoft APIs), the role of Data Model Objects as merge fields in prompt templates, and how Agentforce Data Libraries simplify RAG setup for unstructured content. Practical, step-by-step grounding knowledge.

> **Bonus cert path**: "Salesforce Data Cloud Consultant Certification Prep" module (`trailhead.salesforce.com/content/learn/modules/cert-prep-data-cloud-consultant`) covers the six exam sections (Data Cloud Overview, Data Streams, Identity Resolution, Segmentation, Activation, and Insights) — recommended once the above three are complete.

---

*Sources: Salesforce Engineering Blog (May 2025), Salesforce.com/news "How Data Cloud Powers Agentforce" (Jul 2025), Salesforce Blog "Data Cloud Pricing Updates" (Sep 2025), Torrent Consulting "Agentforce and Data Cloud: Do You Need Both?" (Mar 2025), Salesforce Ben "Connecting Agentforce to Data Cloud for Grounding With RAG" (Jan 2026), Trailhead "Grounding an Agent with Data" module, Aquiva Labs "Agentforce Pricing Update Q3 2025."*
