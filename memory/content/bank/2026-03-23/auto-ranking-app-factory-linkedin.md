# auto-ranking-app-factory-linkedin — 2026-03-23
Pillar: autonomous-detection
Source: main-session | build
Rubric: architectural decision with real tradeoffs + non-obvious problem solved

---

I've built three ranking apps. Nash Satoshi (crypto), Glow Index (skincare), and today I tested colleges.

After the second one, I realized I wasn't building apps. I was building the same app with different prompts.

So I stopped and built the factory instead.

It's a niche config schema, a parameterized Next.js template, a prompt generator, and a shell script that wires it all together. To stand up a new ranking app in any niche: edit the config, run the script. Today's colleges test took minutes from zero to working frontend.

The architecture is the same every time: 4 LLMs scoring items in parallel, consensus aggregation, verdict display. What changes is the scoring criteria, the item schema, and the prompts. All of that is now parameterized.

The business model is obvious once you see it: own the infrastructure, the apps are just configs. The third one is almost free. The tenth one is free.

This is what building at the meta-level looks like. Not solving the problem. Building the machine that solves the problem category.
