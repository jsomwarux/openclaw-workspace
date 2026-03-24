# auto-ranking-app-factory — 2026-03-23
Pillar: autonomous-detection
Source: main-session | build
Rubric: architectural decision with real tradeoffs + non-obvious problem solved

---

ranking apps all have the same bones.

4 LLMs score items. scores aggregate. frontend displays the verdict.

so i stopped building them and built the thing that builds them.

niche config schema. parameterized next.js template. prompt generator. one shell script.

new niche: edit the config, run the script. tested with colleges today. took minutes.

the third app is almost free. the tenth one is free.
