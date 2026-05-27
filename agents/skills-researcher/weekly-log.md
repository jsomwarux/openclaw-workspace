# Weekly Log — Skills & API Researcher

## Week: 2026-W22 (May 25 - May 31, 2026)

[2026-05-25] — reset after synthesis
[2026-05-23] daily scan — no critical findings. KB only: .NET 11 `dotnet new mcpserver` preview signal; Svelte official AI/MCP docs; property-management inspection-data-entry positioning signal; OpenClaw v2026.5.22-beta.1 noted but existing upgrade tasks/backlog cover action.
[2026-05-25] daily scan — 🔴 OpenClaw v2026.5.24-beta.2 runtime/security/perf release noted (KB only; MC skipped because Skills backlog is at cap 15 and existing OpenClaw upgrade tasks cover action). KB only: n8n Microsoft Agent 365 duplicate of existing MC task; Trust3 MCP Security signal; Hawaii Coastal/Roam property-management AI ops assistant signal; Anthropic Claude Platform on AWS / MCP tunnels signal.
## 2026-05-26 - Daily Scan Findings

### 🔴 Critical Security Advisory
- **Name:** OpenClaw/ClawHub RCE Vulnerability (CVE-2026-25253)
- **Description:** One-click Remote Code Execution vulnerability via the Control UI. Reported by The Claw Report and prompted rapid patches from the core team.
- **Action:** JT MUST update to v2026.5.25-beta.1 or newer immediately.
- **Source:** https://www.theclawreport.com/
- **Fit:** OpenClaw Runtime / Security

### 🟠 High - New Stack Capability
- **Name:** n8n Microsoft Agent Node
- **Description:** n8n shipped a native node that grants AI agents a real Microsoft identity (Teams @mentions, Outlook inbox, SharePoint permissions).
- **First Action:** Test the node in an n8n workflow for internal task routing or client SharePoint automation.
- **Why now:** Directly unblocks complex enterprise/SMB workflow integrations where simple webhooks aren't enough.
- **Source:** https://x.com/darshan_gupta17/status/2058797714012536871
- **Fit:** n8n-agent / Consulting Deliverables

### 🟠 High - Security Skill Suite
- **Name:** ClawSec by Prompt Security
- **Description:** A complete security skill suite for OpenClaw featuring drift detection, SOUL.md protection, and skill integrity verification.
- **First Action:** git clone https://github.com/prompt-security/clawsec and audit for integration into JT's local workspace.
- **Why now:** JT is running a high-complexity agent stack; automated drift detection for SOUL.md and settings is a critical governance layer.
- **Source:** https://github.com/prompt-security/clawsec
- **Fit:** Eve (main) / System Auditor

### 🟡 Medium - Ecosystem Intelligence
- **Name:** Anthropic "Dreaming" Managed Agents Memory
- **Description:** Research preview feature for consolidation of persistent agent memory (merging duplicates/removing stale entries).
- **First Action:** Check Anthropic developer console for "Managed Agents" beta/research access.
- **Source:** https://en.wikipedia.org/wiki/Claude_(language_model)
- **Fit:** Eve (main) / Future Memory Layer

### 🟡 Medium - MCP Framework
- **Name:** .NET 11 Preview 4 MCP Template
- **Description:** SDK now includes dotnet new mcpserver template for native MCP server scaffolding.
- **Source:** https://x.com/jfversluis/status/2057370813817311443
- **Fit:** mcp-builder / Developer Experience
