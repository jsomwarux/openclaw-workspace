# Marketsmith Meeting Notes - 2026-07-02

## Summary
- Meeting with Sam/team felt more like an interview than a standard project meeting.
- JT thought it went well overall.
- They spent time on JT's backend, client work, OpenClaw, and how JT would implement AI for their specific marketing business.
- They could not show dashboard examples because of client confidentiality.
- They said they will talk with leadership and get back on Monday or Tuesday next week, July 6 or July 7, 2026, with a plan to move forward.

## Main Buyer Signals
- Security: protect client access and reduce data leakage risk.
- Scalability: make each build more efficient and repeatable over time.
- Data intake: make sure data is clean, complete, and accurate before insights are generated.

## Points JT Raised
- Security: use a local LLM on a dedicated PC to analyze client data without exposing it externally.
- Scalability: use an agent with a `lessons.md`-style file that updates after each build so delivery gets more efficient.
- Data intake: create a clean-data qualification file and have the workflow check every refresh against it before moving forward.
- Snowflake: all data lives in Snowflake; current Snowflake built-in AI insight generation is probably suboptimal.
- Insight quality: talk with each client directly, understand business needs and priorities, then use separate client-specific prompts for insight generation.
- Marketing AI contribution: automated competitor research and adaptation of the strongest competitor tactics.
- Always-on agent angle: an OpenClaw-like personal agent that continuously researches the business's industry and finds growth opportunities.

## Questions Not Asked / Missing Evidence
- JT did not get to ask many questions because the conversation skewed interview-style.
- No dashboard examples were shown due to confidentiality.
- Need to confirm their dashboard priority order, client-priority discovery process, Snowflake access pattern, data-readiness owner, security constraints, and first 30-day acceptance criteria.

## Proposal Implications
- Lead with governed AI insight operations, not dashboard labor.
- Strongest offer frame: secure data intake + client-specific insight generation + repeatable delivery memory.
- Avoid framing as raw Azure staff augmentation.
- Keep local/dedicated-PC LLM as an option, not a default claim, until security/access constraints are clear.

## Next Step
- Wait for leadership follow-up on July 6 or July 7, 2026.
- If they move forward, prepare a playbook/proposal covering security, scalability, data-readiness gates, Snowflake workflow, client-specific prompt packs, competitor research, and always-on industry research.
