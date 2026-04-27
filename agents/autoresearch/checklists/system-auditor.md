# Autoresearch Checklist — system-auditor

Score system audit outputs against these yes/no checks:

1. Does it distinguish confirmed failures from warnings or unknowns?
2. Does it include the exact command/log/source that supports each finding?
3. Does it prioritize risks by impact and urgency?
4. Does it recommend a concrete fix or next diagnostic step for each material issue?
5. Does it avoid unsafe changes to sacred files, auth config, or gateway config without approval?
6. Does it verify any applied fix before marking it resolved?
