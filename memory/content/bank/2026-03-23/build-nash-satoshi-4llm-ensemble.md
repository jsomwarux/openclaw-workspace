# build-nash-satoshi-4llm-ensemble
# Pass 3: Build Showcase
# build: Nash Satoshi — 32-node n8n pipeline, 4-LLM ensemble
# platform: X | banked: true | posted: false

single-model rankings have a confidence problem: the model doesn't know what it doesn't know.

Nash Satoshi runs 4 models in parallel on the same coin. GPT, Gemini, Claude, Grok. each scores in isolation.

the verdict is consensus. divergence is flagged as uncertainty, not hidden.

high disagreement between models is itself a signal. built that into the output.

32-node n8n pipeline. end-to-end in under 4 minutes.
