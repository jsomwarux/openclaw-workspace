# Python AI Patterns — Cheat Sheet for JT Interview Prep
**Purpose:** AI Solutions Architect interview prep — Python as orchestration tool, not ML engineering
**Angle:** "I implement AI workflows and orchestrate LLM calls" — not "I train models"

---

## Section 1: Python Patterns Common in AI SA Roles

### 1. API Calls with `requests` — Standard REST Call to an AI Endpoint
The most fundamental pattern in AI integration work. Every AI service exposes a REST API; this is how you call it.

```python
import requests, os

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={"x-api-key": os.getenv("ANTHROPIC_API_KEY"), "anthropic-version": "2023-06-01"},
    json={"model": "claude-sonnet-4-6", "max_tokens": 1024,
          "messages": [{"role": "user", "content": "Summarize this case."}]}
)
print(response.json()["content"][0]["text"])
```

**Why it matters in SA work:** When a client's system can't use the official SDK, direct HTTP calls are the fallback. Also used in n8n HTTP Request nodes — this is exactly what runs under the hood.

---

### 2. Async with `asyncio` — Parallel LLM Calls
When you need to process 50 customer records simultaneously instead of one at a time.

```python
import asyncio, anthropic

client = anthropic.AsyncAnthropic()

async def classify_case(case_text: str) -> str:
    msg = await client.messages.create(
        model="claude-sonnet-4-6", max_tokens=100,
        messages=[{"role": "user", "content": f"Classify: {case_text}"}]
    )
    return msg.content[0].text

async def main(cases: list[str]):
    results = await asyncio.gather(*[classify_case(c) for c in cases])
    return results
```

**Why it matters:** Batch processing 500 support tickets in parallel instead of sequentially is a 50x speed improvement. This is the pattern behind any AI triage pipeline.

---

### 3. Dataclasses for Structured AI Responses
When you need to guarantee the shape of what comes back from an LLM — critical for downstream systems.

```python
from dataclasses import dataclass
import json

@dataclass
class CaseClassification:
    category: str
    priority: str
    sentiment: str
    recommended_action: str

def parse_llm_response(raw_json: str) -> CaseClassification:
    data = json.loads(raw_json)
    return CaseClassification(**data)
```

**Why it matters:** In real AI pipelines, you can't pass a blob of text to a CRM API. You need structured output. Dataclasses give you type safety without the overhead of full Pydantic schemas.

---

### 4. Error Handling / Retry Pattern for LLM Calls
LLM APIs rate limit, timeout, and fail. Production AI workflows must handle this gracefully.

```python
import time, anthropic
from anthropic import RateLimitError, APITimeoutError

def call_with_retry(prompt: str, max_retries: int = 3) -> str:
    client = anthropic.Anthropic()
    for attempt in range(max_retries):
        try:
            msg = client.messages.create(
                model="claude-sonnet-4-6", max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        except RateLimitError:
            time.sleep(2 ** attempt)  # exponential backoff
        except APITimeoutError:
            time.sleep(5)
    raise RuntimeError("Max retries exceeded")
```

**Why it matters:** A workflow that crashes on the first rate limit error isn't production-ready. This is table stakes for any AI SA who has shipped real integrations.

---

### 5. Environment Variable Management — `dotenv` Pattern
The correct way to handle secrets in AI scripts — never hardcode API keys.

```python
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file in current directory

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
SALESFORCE_TOKEN = os.getenv("SF_ACCESS_TOKEN")

if not ANTHROPIC_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in environment")
```

**Why it matters:** Every AI project has secrets. The dotenv pattern is the standard for local development; production uses actual secret managers (AWS Secrets Manager, Salesforce Named Credentials). Knowing this pattern correctly signals engineering maturity.

---

## Section 2: 5 LLM Integration Code Snippets (Copy-Paste Quality)

### 1. Anthropic SDK — Basic Message Call with System Prompt
```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a Salesforce expert. Be concise and specific.",
    messages=[
        {"role": "user", "content": "What is the difference between a Lead and a Contact in Salesforce?"}
    ]
)

print(message.content[0].text)
```

---

### 2. OpenAI SDK — Chat Completion with JSON Mode
```python
from openai import OpenAI
import json

client = OpenAI()  # reads OPENAI_API_KEY from env

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "Return JSON only. Schema: {category, priority, action}"},
        {"role": "user", "content": "Customer says their order hasn't arrived after 2 weeks."}
    ]
)

result = json.loads(response.choices[0].message.content)
print(result)  # {"category": "shipping", "priority": "high", "action": "escalate"}
```

---

### 3. LangChain — Simple Chain (Prompt → LLM → Output Parser)
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatAnthropic(model="claude-sonnet-4-6")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You summarize customer support tickets in one sentence."),
    ("human", "{ticket_text}")
])
parser = StrOutputParser()

chain = prompt | llm | parser
result = chain.invoke({"ticket_text": "I've been waiting 3 weeks and nobody has responded to my emails..."})
print(result)
```

---

### 4. Requests — Direct API Call to Any LLM Endpoint (Generic Pattern)
```python
import requests, os

def call_llm_api(endpoint: str, api_key: str, prompt: str, model: str) -> str:
    """Generic pattern — works for OpenAI-compatible APIs, Anthropic, custom endpoints."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512
    }
    response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Works for OpenAI, Azure OpenAI, or any OpenAI-compatible endpoint
result = call_llm_api(
    endpoint="https://api.openai.com/v1/chat/completions",
    api_key=os.getenv("OPENAI_API_KEY"),
    prompt="Summarize in 2 sentences: [text]",
    model="gpt-4o"
)
```

---

### 5. Streaming Response — Anthropic Streaming Output Pattern
```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a detailed analysis of AI agent adoption in enterprise."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)  # prints token-by-token as it arrives
    
    final_message = stream.get_final_message()
    print(f"\n\nTotal tokens: {final_message.usage.input_tokens + final_message.usage.output_tokens}")
```

**When to use streaming:** Any user-facing AI interface where you want output to appear immediately instead of waiting for the full response. Critical for demos — nothing kills a demo faster than a 10-second blank wait.

---

## Section 3: How JT Should Frame Python Experience

### The Positioning
JT's angle is **orchestration, not engineering**. He uses Python to wire together AI systems, not to train models or write algorithms. This is exactly what AI SA roles need — someone who can implement workflows, not a research scientist.

### 4 Talking Points (Use Verbatim)

**1. "I implement AI workflows using Python as the orchestration layer."**
"I've built Python scripts that upload content to Google Drive, query SQLite health databases, and run cost tracking against API usage logs. I use Python to glue together the pieces of an AI system — data in, LLM call, structured output, action taken. That's the core loop of any AI workflow, and I've built several of them."

**2. "I've been hitting LLM APIs directly in production — via n8n HTTP nodes calling the Anthropic API."**
"In n8n, I've built workflows where HTTP Request nodes call the Claude API with structured JSON payloads, parse the response, and route it into downstream actions. That's the same pattern as writing a Python requests call — I understand what's happening at the HTTP layer, not just the drag-and-drop level."

**3. "I review and direct AI-generated code rather than writing everything from scratch."**
"In AI SA work, the skill isn't writing 500 lines of Python from memory — it's knowing what to build, reviewing what the AI generates, catching logic errors, and integrating the output into a real system. I use Claude and Copilot to accelerate implementation, but I understand the code well enough to verify it's correct and catch where it'll break."

**4. "I think about Python in terms of the AI integration stack, not scripts."**
"I know when to use the Anthropic SDK directly versus a requests call versus LangChain. I know what async matters for (batch processing), what streaming matters for (user-facing interfaces), and what structured output matters for (feeding data into other systems). Those decisions are what an SA makes — not the syntax."

**5. "My Python experience is operational — cost tracking, data queries, API integrations — which is exactly the Python an AI implementation team uses day-to-day."**
"I've written scripts that query SQLite databases for health tracking, call the Google Drive API to upload documents, and snapshot cost data from API usage logs. That's real, working Python that does something in production — not exercises."

---

## Section 4: What NOT to Say

**Don't say "I know Python but I'm not a developer."**
This frames Python as a weakness before the conversation starts. Say instead: "I use Python for AI workflow implementation and automation" — let them probe depth if they want it.

**Don't lead with "I learned Python from a course."**
Courses signal studying, not doing. Lead with what you've built. If they ask how you learned: "I've learned by implementing — scripts for Drive uploads, cost tracking, API integrations. I learn by building something that runs in production."

**Don't say "I'd need to look that up" for basic patterns.**
For common patterns (how to call an API, what dotenv does, what async is for), you should be able to speak to them directly. Memorize the 5 patterns in Section 1 cold.

**Don't confuse ML engineering with AI implementation.**
If someone asks about PyTorch, scikit-learn, or "training models" — be honest that's not your lane, but immediately pivot: "My expertise is on the implementation and integration side — taking a model that exists and wiring it into a business workflow. That's where the SA work actually lives."

**Don't undersell the n8n HTTP node work.**
"I built HTTP Request nodes in n8n" sounds small. Say: "I've built API integrations that call LLM endpoints with structured payloads, parse the response, and route it into downstream workflows — in n8n and in Python." Same thing, bigger frame.

**Don't over-explain what you don't know.**
If there's a Python concept you genuinely don't know, say "I'd research that before implementing" — not "I don't know that." An AI SA's job isn't to have every syntax memorized; it's to deliver working integrations. Knowing where to find answers is a skill.

---

## Section 5: Quick Reference — Libraries + When to Use Each

| Library | Use When | Avoid When |
|---------|----------|------------|
| `anthropic` (SDK) | Building Anthropic integrations, want typed responses + streaming support, prefer official SDK ergonomics | Need to call multiple LLM providers with the same code |
| `openai` (SDK) | OpenAI or Azure OpenAI integrations; also works with any OpenAI-compatible endpoint | Only using Anthropic — SDK overhead not worth it |
| `requests` | Direct HTTP calls to any API, n8n-equivalent logic in Python, vendor-agnostic LLM calls | High-volume async scenarios (use aiohttp instead) |
| `aiohttp` | Async HTTP calls at scale (hundreds of concurrent API requests) | Simple scripts — adds complexity not worth it for <10 concurrent calls |
| `asyncio` | Parallel LLM calls, batch processing, any I/O-bound operations that need concurrency | CPU-bound tasks (use multiprocessing instead) |
| `langchain` | Orchestrating multi-step agent chains, using retrieval pipelines, prototyping agent architectures | Simple single-turn LLM calls — overkill and adds latency |
| `pydantic` | Structured output validation from LLMs, schema enforcement, type-safe API response parsing | Simple string output where dataclasses are enough |
| `python-dotenv` | Local development secret management, loading .env files | Production environments — use real secret managers (AWS, Vault) |
| `sqlalchemy` | Database-backed AI applications, reading structured data to feed into LLM prompts | Simple SQLite scripts — overkill; use sqlite3 directly |
| `tiktoken` | Counting tokens before sending to OpenAI (avoid exceeding context limits) | Anthropic calls — use their token counting API instead |

---

*Last updated: 2026-03-19 | Maintained by Eve for JT's AI SA interview prep*
