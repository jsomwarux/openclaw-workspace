**Last updated:** Monday, March 30, 2026 — 9:00 AM EST

🔴 **n8n Critical RCE — CVE-2026-33660 + CVE-2026-33696 (CVSS 9.4)** — Two remote code execution vulnerabilities published March 25 affect all self-hosted n8n installations below versions 2.14.1, 2.13.3, or 1.123.27; exploitable by any authenticated user with workflow editing permissions, exposing all stored credentials (AWS, Slack, DB connection strings). Patch immediately or disable Merge + XML nodes via NODES_EXCLUDE env vars as interim mitigation. (https://anonhaven.com/en/news/n8n-rce-alasql-prototype-pollution/)
