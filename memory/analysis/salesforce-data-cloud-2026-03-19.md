# Salesforce Data Cloud — Research Note
**Date:** 2026-03-19
**Purpose:** Skills gap fill for AI SA job search + prerequisite for Data Cloud + Agentforce Context Injection Demo build

---

## What Is Data Cloud

Salesforce Data Cloud is Salesforce's native real-time Customer Data Platform (CDP) — a hyperscale data engine built directly into the Salesforce Platform. Unlike third-party CDPs that require separate integration work, Data Cloud lives inside the same platform as Sales Cloud, Service Cloud, and Agentforce, which means customer data is available to agents without ETL pipelines or API middleware hops. It ingests, processes, and harmonizes data from any source — CRM records, web events, mobile activity, data lakes, data warehouses, third-party apps — and resolves all of that into a single Unified Customer Profile per individual.

The architecture is built around the concept of Data Model Objects (DMOs) — a canonical schema layer that maps incoming raw data (from Data Lake Objects, or DLOs) into standardized fields Salesforce recognizes. When a customer's data comes in from multiple sources — say, a Shopify order history, a Zendesk ticket, and a Salesforce CRM record — Data Cloud's Identity Resolution engine matches those records using deterministic (email/phone) and probabilistic matching rules to decide they all belong to the same person. The result is a single Unified Profile that becomes the single source of truth for that customer across all of Salesforce.

Data Cloud also handles unstructured data. It includes a native vector database that converts PDFs, support transcripts, Slack threads, knowledge articles, and images into embeddings — searchable vector representations that an LLM can retrieve from at query time. This is how agents can answer nuanced questions grounded in real documentation, not just structured field lookups. The combination of structured CRM data and vectorized unstructured data is what makes Data Cloud fundamentally more powerful than a basic CRM lookup.

One architectural distinction worth knowing: Data Cloud uses "zero copy" integrations with external data warehouses (Snowflake, BigQuery, Databricks). This means Salesforce can query data where it lives without physically moving or duplicating it. For enterprise SA conversations, this is a key point — it addresses the objection "we can't move our data to Salesforce." With zero copy, they don't have to.

---

## How It Pairs With Agentforce

The integration between Data Cloud and Agentforce is the core value proposition of the entire Salesforce AI strategy — Agentforce without Data Cloud is a general-purpose agent; Agentforce *with* Data Cloud is a personalized, context-aware agent that knows who the customer is before they finish their first sentence.

**The technical pattern is Retrieval-Augmented Generation (RAG), implemented through a Salesforce-native toolchain:**

1. **Data Streams** bring raw data into Data Cloud from source systems.
2. **Identity Resolution** unifies that data into a single Unified Profile per customer.
3. **Data Model Objects (DMOs)** map unified data into structured, queryable objects.
4. **Search Indexes** (vector-based) are built over DMOs or unstructured content chunks.
5. **Retrievers** (configured in Einstein Studio) define what data to pull back and how many results to return for a given query.
6. **Prompt Templates** (built in Prompt Builder) define how retrieved data gets injected into the agent's context window before the LLM generates a response.
7. **Agentforce agents** call these prompt templates as part of their actions — specifically the "Answer Questions with Knowledge" action or custom actions.

At runtime, when a customer messages an Agentforce Service Agent, here's what actually happens: the agent identifies the customer, calls a retriever that queries the Data Cloud search index for relevant chunks based on the conversation context, those chunks are injected into the prompt template, and the LLM generates a response that is *grounded* in actual customer data — not hallucinated. This is what "grounding" means in the Salesforce/Agentforce context: giving the LLM factual context so it doesn't make things up.

Segments from Data Cloud also feed into Agentforce decision logic. An agent can behave differently for a customer who is in the "at-risk churn" segment versus a "high lifetime value" segment — without any custom code, just configuration in the agent's Topics and Actions.

The practical workflow for building this in a Salesforce org:
- Set up a Data Stream (connector to a source)
- Map to a DMO and run Identity Resolution
- Build a Search Index over the relevant DMO
- Create a Retriever in Einstein Studio pointing to that index
- Build or modify a Prompt Template in Prompt Builder using the retriever as a resource
- Wire the prompt template into an Agentforce agent action

---

## Key Concepts to Know (Interview Ready)

- **Unified Customer Profile (UCP)**: The resolved, merged view of a single customer stitched together from all data sources — the core output of Data Cloud
- **Data Streams**: Connectors that ingest data into Data Cloud (batch or real-time) from Salesforce clouds, MuleSoft, or third-party apps
- **Data Lake Objects (DLOs)**: Raw ingested data before transformation — the "landing zone" inside Data Cloud
- **Data Model Objects (DMOs)**: The canonical schema layer; standardized objects that DLO data maps into for use across the platform
- **Identity Resolution (IR)**: The engine that matches records across sources and decides they belong to the same customer using deterministic + probabilistic rules
- **Segments**: Audience groups defined by filter criteria (e.g., "purchased in last 30 days AND opened email this week") — can feed Agentforce behavior or Marketing Cloud activations
- **Data Spaces**: Logical partitions within a single Data Cloud instance for multi-brand or multi-region orgs — separate data governance while sharing infrastructure
- **Retrievers**: Einstein Studio objects that query a Search Index and return relevant data chunks for injection into an LLM prompt
- **Grounding**: The practice of injecting real, factual data into an LLM prompt so its response is based on actual records, not training data alone
- **Zero Copy**: Data Cloud's ability to query data in external warehouses (Snowflake, BigQuery) without physically moving it into Salesforce

---

## What It Costs / Licensing

Data Cloud pricing moved to a consumption-based model in 2025. Key pricing tiers:

- **Flex Credits**: $500 per 100,000 Flex Credits — pay per action (segmentation queries, identity resolution runs, activations). Ingestion is free. Credits can also be applied to Agentforce actions, making them shared currency across the AI platform.
- **Profiles (CDP tier)**: $240 per 1,000 profiles/year — includes 100 segments, 25 data streams, and 1 Identity Resolution ruleset per Data Space. Designed for CDP-first use cases (marketing personalization, segmentation).
- **Enterprise Profiles**: $420 per 1,000 profiles/year — includes 500 segments, 100 data streams, 2 IR rulesets per Data Space, plus Data Masking and Ad Audience add-ons.
- **Data Spaces add-on**: ~$60,000/year for multi-org isolation (multi-brand/multi-region enterprises).

Data Cloud is an **add-on**, not bundled with standard Sales or Service Cloud licenses. However, Salesforce now includes a free provisioning tier (Salesforce Foundations) with limited storage and credits — the new Developer Edition org also includes Data Cloud + Agentforce, which makes it easier to demo and learn.

Important for SA conversations: pricing is negotiated at enterprise deal level. The credit model means cost scales with actual usage, which is a selling point for large orgs worried about overcommitting. The shared Flex Credits between Data Cloud and Agentforce also means a single credit pool serves both the data platform and the AI agents layer.

---

## Interview Talking Points

**1. Lead with the "why Data Cloud" answer, not the feature list.**
Most candidates can list features. The differentiator is explaining *why* Data Cloud exists: because LLMs are trained on general knowledge and have no idea who your specific customer is. Data Cloud is the bridge that makes Agentforce's responses personalized and factually grounded. Without it, Agentforce is a sophisticated chatbot. With it, it's an actual agent that knows the customer's history, segment, and context before the conversation starts.

**2. Know the RAG implementation inside Salesforce.**
The interview question isn't "what is RAG?" — it's "how do you implement grounding in Agentforce?" The answer is: Data Streams → Identity Resolution → DMO → Search Index → Retriever (Einstein Studio) → Prompt Template (Prompt Builder) → Agent Action. Being able to walk through that chain signals architecture-level understanding, not just product knowledge.

**3. Frame it as a data integration problem that Salesforce solves natively.**
Enterprise objections to AI agents almost always come back to data: "our data is in Snowflake," "we have siloed systems," "we don't want to move data to Salesforce." Data Cloud answers all of these: zero-copy for external warehouses, native connectors (Data Streams) for Salesforce + third-party apps, and Data Spaces for governance. Position it as the data architecture answer, not just a marketing CDP.

**4. Connect Data Cloud to revenue outcomes, not just features.**
In an AI SA interview, the question behind the question is always "can this person sell this?" Frame Data Cloud examples with business outcomes: FedEx connected all Salesforce clouds to Data Cloud to improve customer journeys without duplicating data. Retail clients use segment-based agent behavior to deflect low-value cases automatically. The output isn't "unified profiles" — it's "agents that resolve cases faster because they already know the customer."

---

## Sources

- https://www.salesforce.com/news/stories/how-data-cloud-powers-agentforce/ (Salesforce official — Data Cloud + Agentforce deep dive, updated December 2025)
- https://www.salesforce.com/data/pricing/ (Official pricing page — Flex Credits, Profiles, Enterprise Profiles tiers)
- https://www.salesforceben.com/connecting-agentforce-to-data-cloud-for-grounding-with-rag/ (Practical RAG implementation walkthrough — Retriever + Prompt Builder + Agent config)
- https://trailhead.salesforce.com/content/learn/modules/grounding-an-agent-with-data/review-options-to-ground-an-agent-with-data (Trailhead — grounding mechanisms)
- https://trailhead.salesforce.com/content/learn/modules/grounding-an-agent-with-data/learn-the-basics-of-grounding (Trailhead — grounding basics)
- https://salesforcenegotiations.com/salesforce-data-cloud-licensing-negotiation-guide-managing-usage-credits-and-costs/ (Licensing + negotiation guide)
- https://developer.salesforce.com/blogs/2025/03/introducing-the-new-salesforce-developer-edition-now-with-agentforce-and-data-cloud (Dev Edition now includes Data Cloud + Agentforce)
