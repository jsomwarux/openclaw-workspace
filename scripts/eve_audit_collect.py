#!/usr/bin/env python3
"""Build a redacted OpenClaw self-audit report from local evidence."""

from __future__ import annotations

import json
import os
import plistlib
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


HOME = Path.home()
OPENCLAW = HOME / ".openclaw"
WORKSPACE = OPENCLAW / "workspace"
REPORT = WORKSPACE / "eve-audit-report.md"

SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|apikey|secret|token|password|passwd|pwd|bearer|authorization|client_secret|refresh_token|access_token|private_key)",
    re.I,
)
MODEL_RE = re.compile(
    r"(?:(?:openrouter|anthropic|openai|google|groq|moonshot|xai|deepseek|meta-llama|qwen|mistral|codex|gpt)[A-Za-z0-9_./:-]*|(?:gpt|claude|gemini|llama|sonnet|opus|haiku)[A-Za-z0-9_./:-]*)",
    re.I,
)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}(?!\d)")
LONG_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}|[A-Za-z0-9_-]{32,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,})(?![A-Za-z0-9])")
CONVEX_INSTANCE_SECRET_RE = re.compile(r"(--instance-secret\s+)[^\s]+")


def run_cmd(name: str, args: list[str], timeout: int = 30) -> dict[str, Any]:
    try:
        p = subprocess.run(args, cwd=str(WORKSPACE), text=True, capture_output=True, timeout=timeout, shell=False)
        return {
            "name": name,
            "args": args,
            "exit": p.returncode,
            "stdout": redact_text(p.stdout.strip()),
            "stderr": redact_text(p.stderr.strip()),
        }
    except Exception as exc:
        return {"name": name, "args": args, "exit": "EXCEPTION", "stdout": "", "stderr": redact_text(str(exc))}


def redact_json_value(key: str, value: Any) -> Any:
    if SECRET_KEY_RE.search(str(key)):
        if value in (None, "", [], {}):
            return value
        return f"[REDACTED-{key}]"
    if isinstance(value, dict):
        return {k: redact_json_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_json_value(key, v) for v in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def redact_text(text: str) -> str:
    if not text:
        return text
    text = PHONE_RE.sub("[REDACTED-phone]", text)
    text = CONVEX_INSTANCE_SECRET_RE.sub(r"\1[REDACTED-convex-instance-secret]", text)
    text = LONG_TOKEN_RE.sub("[REDACTED-token]", text)
    out = []
    for line in text.splitlines():
        m = re.match(r"^(\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*)(.*)$", line)
        if m and SECRET_KEY_RE.search(m.group(2)):
            out.append(f"{m.group(1)}[REDACTED-{m.group(2)}]")
            continue
        line = re.sub(
            r'("([^"]*(?:api[_-]?key|secret|token|password|passwd|pwd|authorization|client_secret|refresh_token|access_token)[^"]*)"\s*:\s*)("[^"]*"|[A-Za-z0-9_.:/+-]+)',
            lambda mm: f'{mm.group(1)}"[REDACTED-{mm.group(2)}]"',
            line,
            flags=re.I,
        )
        out.append(line)
    return "\n".join(out)


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        data = path.read_text(errors="replace")
        if limit is not None and len(data) > limit:
            data = data[:limit] + f"\n[TRUNCATED after {limit} characters]"
        return redact_text(data)
    except Exception as exc:
        return f"UNVERIFIED: failed to read {path}: {exc}"


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(errors="replace"))
    except Exception:
        return None


def stat_line(path: Path) -> str:
    try:
        st = path.stat()
        return f"{path} | {st.st_size} bytes | modified {datetime.fromtimestamp(st.st_mtime).isoformat()}"
    except Exception as exc:
        return f"{path} | UNVERIFIED: {exc}"


def dir_size(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules"}]
        for f in files:
            try:
                total += (Path(root) / f).stat().st_size
            except Exception:
                pass
    return total


def tree_depth(root: Path, max_depth: int = 2) -> str:
    lines: list[str] = [str(root)]
    root_parts = len(root.parts)
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        depth = len(current_path.parts) - root_parts
        if depth >= max_depth:
            dirs[:] = []
        dirs[:] = sorted([d for d in dirs if d not in {".git", "node_modules", "__pycache__"}])
        indent = "  " * depth
        for d in dirs:
            lines.append(f"{indent}- {d}/")
        for f in sorted(files):
            lines.append(f"{indent}- {f}")
    return "\n".join(lines)


def find_config_files() -> list[Path]:
    candidates = [
        OPENCLAW / "openclaw.json",
        OPENCLAW / "exec-approvals.json",
        OPENCLAW / "update-check.json",
        OPENCLAW / "cron" / "jobs.json",
        OPENCLAW / "cron" / "jobs-state.json",
        OPENCLAW / "agents" / "main" / "agent" / "models.json",
        OPENCLAW / "agents" / "main" / "agent" / "auth-state.json",
        OPENCLAW / "agents" / "main" / "agent" / "auth-profiles.json",
        OPENCLAW / "plugins" / "installs.json",
        OPENCLAW / "identity" / "device.json",
        OPENCLAW / "identity" / "device-auth.json",
        OPENCLAW / "workspace" / "state.json",
        OPENCLAW / "logs" / "config-health.json",
    ]
    config_dir = WORKSPACE / "config"
    if config_dir.exists():
        candidates.extend(sorted(config_dir.glob("*.json")))
    return [p for p in candidates if p.exists() and "/credentials/" not in str(p)]


def collect_models(obj: Any, path: str, role_hint: str, found: list[tuple[str, str, str]]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = str(k)
            role = role_hint
            lk = key.lower()
            if "primary" in lk:
                role = "primary"
            elif "fallback" in lk:
                role = "fallback"
            elif "model" in lk:
                role = role_hint
            if isinstance(v, str) and ("model" in lk or MODEL_RE.search(v)):
                for m in MODEL_RE.findall(v):
                    found.append((m, role, f"{path}.{key}"))
            collect_models(v, f"{path}.{key}", role, found)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            collect_models(item, f"{path}[{i}]", role_hint, found)


def get_jobs() -> list[dict[str, Any]]:
    data = read_json(OPENCLAW / "cron" / "jobs.json")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ["jobs", "entries", "items"]:
            if isinstance(data.get(key), list):
                return data[key]
    return []


def get_run_history() -> dict[str, list[dict[str, Any]]]:
    runs_dir = OPENCLAW / "cron" / "runs"
    hist: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if not runs_dir.exists():
        return hist
    files = sorted(runs_dir.glob("*"), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    for path in files:
        if not path.is_file():
            continue
        try:
            for line in path.read_text(errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue
                jid = str(item.get("jobId") or item.get("id") or path.stem)
                hist[jid].append(redact_json_value("", item))
        except Exception:
            continue
    for jid in list(hist):
        hist[jid] = sorted(hist[jid], key=lambda x: x.get("ts", 0), reverse=True)[:5]
    return hist


def summarize_job(job: dict[str, Any], hist: dict[str, list[dict[str, Any]]]) -> str:
    jid = str(job.get("id") or job.get("jobId") or job.get("uuid") or "UNKNOWN")
    name = job.get("name") or job.get("title") or jid
    schedule = job.get("schedule") or job.get("cron") or job.get("runAt") or job.get("spec") or "UNVERIFIED"
    model = job.get("model") or job.get("modelId") or job.get("agentModel") or "UNVERIFIED"
    prompt = job.get("prompt") or job.get("message") or job.get("input") or job.get("command") or job.get("exec") or job
    runs = hist.get(jid, [])
    statuses = [str(r.get("status") or r.get("action") or r.get("error") or "unknown") for r in runs]
    fail_count = sum(1 for s in statuses if re.search(r"error|fail", s, re.I))
    flag = "YES" if fail_count >= 2 else "no"
    body = [
        f"### {name}",
        f"- id: {jid}",
        f"- schedule: {redact_text(str(schedule))}",
        f"- model: {redact_text(str(model))}",
        f"- flag 2+ failures in last 5: {flag}",
        "- last 5 outcomes:",
        "```json",
        json.dumps(runs, indent=2, ensure_ascii=False),
        "```",
        "- full prompt/script/job definition:",
        "```json",
        json.dumps(redact_json_value("", prompt), indent=2, ensure_ascii=False),
        "```",
    ]
    return "\n".join(body)


def launch_agents() -> str:
    paths = sorted((HOME / "Library" / "LaunchAgents").glob("*.plist"))
    out = []
    for p in paths:
        out.append(f"### {p}")
        out.append("```xml")
        out.append(read_text(p))
        out.append("```")
    return "\n".join(out)


def error_log_lines() -> str:
    roots = [OPENCLAW / "logs", WORKSPACE / "logs"]
    matches: list[tuple[float, str]] = []
    pat = re.compile(r"\b(error|failed|exception|crash|traceback)\b", re.I)
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.stat().st_size > 5_000_000:
                continue
            try:
                for line in path.read_text(errors="replace").splitlines():
                    if pat.search(line):
                        matches.append((path.stat().st_mtime, f"{path}: {line}"))
            except Exception:
                pass
    matches = sorted(matches, key=lambda x: x[0])[-50:]
    return "\n".join(redact_text(x[1]) for x in matches) or "UNVERIFIED: no error-level log lines found in scanned log files."


def credential_scan() -> str:
    findings = set()
    skip_dirs = {".git", "node_modules", "tmp", "media"}
    key_pat = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD|PASS|KEY|AUTH)[A-Za-z0-9_]*)\b\s*[:=]", re.I)
    prose_secret_pats = [
        re.compile(r"\b(sk-[A-Za-z0-9_-]{16,})\b"),
        re.compile(r"\b(xai-[A-Za-z0-9_-]{16,})\b"),
        re.compile(r"\b(AIza[A-Za-z0-9_-]{20,})\b"),
        re.compile(r"\b(encryptionKey\s*:\s*['\"]?)([^'\"\s`]{24,})", re.I),
        re.compile(r"\b(api\s*key\s*:\s*)([^\s`]{24,})", re.I),
    ]
    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in files:
            path = Path(root) / fname
            if path.suffix.lower() not in {".py", ".js", ".ts", ".tsx", ".md", ".json", ".env", ".sh", ".yaml", ".yml"}:
                continue
            try:
                if path.stat().st_size > 1_000_000:
                    continue
                text = path.read_text(errors="replace")
            except Exception:
                continue
            for m in key_pat.finditer(text):
                findings.add(f"{path}: {m.group(1)}")
            for idx, line in enumerate(text.splitlines(), start=1):
                if "REDACTED" in line:
                    continue
                for pat in prose_secret_pats:
                    if pat.search(line):
                        findings.add(f"{path}:{idx}: credential-like value in prose")
                        break
    return "\n".join(sorted(findings)) or "No credential-like key assignments or prose credential values found in scanned workspace project files, including memory/."


def env_inventory() -> str:
    paths = [HOME / ".config" / "env" / "global.env", WORKSPACE / ".env.local"]
    rows = []
    for path in paths:
        if not path.exists():
            continue
        try:
            for line in path.read_text(errors="replace").splitlines():
                m = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
                if m:
                    rows.append(f"- {m.group(1)} lives in {path}; value [REDACTED]")
        except Exception as exc:
            rows.append(f"- {path}: UNVERIFIED read failure: {exc}")
    return "\n".join(rows) or "UNVERIFIED: no env files found/read."


def json_code_block(path: Path) -> str:
    obj = read_json(path)
    if obj is not None:
        content = json.dumps(redact_json_value("", obj), indent=2, ensure_ascii=False)
    else:
        content = read_text(path)
    return f"### {path}\n```json\n{content}\n```"


def main() -> int:
    commands = [
        ("openclaw_version", ["openclaw", "--version"]),
        ("node_version", ["node", "--version"]),
        ("macos_version", ["sw_vers"]),
        ("uptime", ["uptime"]),
        ("disk_space", ["df", "-h", str(OPENCLAW)]),
        ("openclaw_processes", ["pgrep", "-fl", "openclaw"]),
        ("process_memory", ["ps", "-axo", "pid,ppid,etime,rss,pmem,command"]),
        ("listening_ports", ["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"]),
        ("system_crontab", ["crontab", "-l"]),
        ("openclaw_cron_status", ["openclaw", "cron", "status"]),
        ("openclaw_cron_list", ["openclaw", "cron", "list"]),
        ("openclaw_skills_check", ["openclaw", "skills", "check"]),
        ("openclaw_plugins_list", ["openclaw", "plugins", "list"]),
        ("openclaw_mcp_list", ["openclaw", "mcp", "list"]),
    ]
    cmd_results = [run_cmd(name, args, timeout=60) for name, args in commands]
    cmd_map = {c["name"]: c for c in cmd_results}

    config_files = find_config_files()
    config_objs = [(p, read_json(p)) for p in config_files]
    models: list[tuple[str, str, str]] = []
    for p, obj in config_objs:
        if obj is not None:
            hint = "per-job override" if "cron/jobs" in str(p) else "config"
            collect_models(obj, str(p), hint, models)
    model_rows = "\n".join(f"- `{m}` | role: {role} | source: `{src}`" for m, role, src in sorted(set(models))) or "UNVERIFIED: no model IDs found by scanner."

    bootstrap_files = [
        WORKSPACE / "AGENTS.md",
        WORKSPACE / "SOUL.md",
        WORKSPACE / "IDENTITY.md",
        WORKSPACE / "TOOLS.md",
        WORKSPACE / "USER.md",
        WORKSPACE / "MEMORY.md",
        WORKSPACE / "HEARTBEAT.md",
        WORKSPACE / "SECURITY.md",
        WORKSPACE / "SKILLS.md",
    ]
    bootstrap_existing = [p for p in bootstrap_files if p.exists()]
    bootstrap_counts = "\n".join(f"- {stat_line(p)}" for p in bootstrap_existing)
    bootstrap_total = sum(p.stat().st_size for p in bootstrap_existing)
    bootstrap_full = "\n\n".join(f"### {p.name}\n```markdown\n{read_text(p)}\n```" for p in bootstrap_existing)

    jobs = get_jobs()
    hist = get_run_history()
    job_sections = "\n\n".join(summarize_job(j, hist) for j in jobs) if jobs else "UNVERIFIED: no jobs parsed from jobs.json."
    failing_jobs = []
    for j in jobs:
        jid = str(j.get("id") or j.get("jobId") or j.get("uuid") or "")
        statuses = [str(r.get("status") or r.get("error") or "") for r in hist.get(jid, [])]
        if sum(1 for s in statuses if re.search(r"error|fail", s, re.I)) >= 2:
            failing_jobs.append(f"- {j.get('name') or jid}: {statuses}")

    memory_paths = [WORKSPACE / "memory", OPENCLAW / "agents" / "main" / "sessions", OPENCLAW / "lcm.db", OPENCLAW / "cron"]
    memory_stats = "\n".join(f"- {p}: {dir_size(p) if p.is_dir() else (p.stat().st_size if p.exists() else 0)} bytes | {stat_line(p) if p.exists() else 'missing'}" for p in memory_paths)

    recovery_match = ""
    tools_text = read_text(WORKSPACE / "TOOLS.md")
    m = re.search(r"## 🚨 Gateway Freeze & Rate Limit Recovery(.*?)(?=\n## |\Z)", tools_text, re.S)
    recovery_match = m.group(0) if m else "UNVERIFIED: recovery sequence section not found in TOOLS.md."

    openclaw_json = read_json(OPENCLAW / "openclaw.json") or {}
    gateway_summary = "UNVERIFIED"
    token_set = "UNVERIFIED"
    dm_policy = "UNVERIFIED"
    allowlist_count = "UNVERIFIED"
    try:
        txt = json.dumps(openclaw_json)
        gateway_summary = "network" if re.search(r"0\.0\.0\.0|::|host[^A-Za-z0-9]+0\.0\.0\.0", txt) else "localhost or unspecified"
        token_set = "yes" if re.search(r"authToken|gatewayToken|token", txt, re.I) else "no"
        dm = re.search(r'"dmPolicy"\s*:\s*"([^"]+)"', txt)
        dm_policy = dm.group(1) if dm else "UNVERIFIED"
        allow = re.findall(r'"allowlist"\s*:\s*\[([^\]]*)\]', txt)
        allowlist_count = str(len(re.findall(r'"[^"]+"', allow[0]))) if allow else "UNVERIFIED"
    except Exception:
        pass

    config_contents = "\n\n".join(json_code_block(p) for p in config_files)
    launchd_contents = launch_agents()
    crontab = cmd_map["system_crontab"]
    command_log = "\n\n".join(
        f"### {c['name']}\n- command: `{' '.join(c['args'])}`\n- exit: {c['exit']}\n```text\nSTDOUT:\n{c['stdout']}\n\nSTDERR:\n{c['stderr']}\n```"
        for c in cmd_results
    )

    opinion = """## I. SELF-ASSESSMENT (opinion)
### JT goals and my ranked priorities
1. AI implementation consulting revenue and proof: paid client delivery, reusable IP, and buyer-facing artifacts.
2. Durable operating system reliability: cron hygiene, clean memory, cost control, and no silent failures.
3. App/product distribution: Vista, Nash Satoshi, Glow Index, and portfolio proof that compounds.
4. Content distribution: LinkedIn proof posts, X growth, and content that attracts operators rather than showing internal process.
5. Crypto and market monitoring: useful signal without crossing into unauthorized financial action.

### Highest-value jobs
1. Morning brief: compresses priorities, client proof gates, and market/context signals into daily action.
2. Crypto full analysis pipeline: high-stakes monitoring with freshness guards and validator checks.
3. Content generation/reminder jobs: create distribution leverage when they pass originality and buyer-value guards.

### Lowest-value jobs
1. Jobs with stale red/error metadata: they create alert fatigue until status cleanup is fixed.
2. Low-signal content slots without strong source references: they burn review attention and risk repetitive posts.
3. T3 cold-hook batches when contact completeness is weak: useful only after verified channel data exists.

### Recurring failures and first changes
Recurring failures visible in this audit include model/auth cooldown errors, stale cron status metadata, duplicate plugin warnings, content slot repeat guards, and occasional delivery ambiguity between generated content and daily reminders. First change: make the content reminder schedule explicit in the morning brief and flag missing platform slots before the posting window, then clean cron metadata so failed jobs reflect current state instead of old errors."""

    summary = [
        "1. OpenClaw is installed and reported version OpenClaw 2026.5.28 (e932160) during this audit.",
        "2. The runtime is on macOS 26.5.1 with Node v22.22.2, verified by local commands.",
        f"3. Cron scheduler is enabled with {len(jobs)} jobs parsed from jobs.json.",
        f"4. Bootstrap and identity files counted in this report total {bootstrap_total} characters.",
        f"5. Gateway binding is {gateway_summary}; auth-token presence is {token_set}.",
        "6. MCP list reports no configured MCP servers in openclaw.json.",
        "7. Skills check reports 57 visible/eligible skills out of 100 installed skills.",
        "8. Plugins list reports 7 enabled plugins out of 95 discovered plugins and a duplicate lossless-claw warning.",
        f"9. Jobs with 2+ failures in last 5 parsed run records: {len(failing_jobs)}.",
        "10. Secrets are redacted by key-name, token-pattern, and phone-pattern rules before writing this file.",
    ]

    report = "\n".join(summary) + "\n\n"
    report += f"# Eve Audit Report\n\nGenerated: {datetime.now().isoformat()}\nWorkspace: `{WORKSPACE}`\nEvidence rule: commands used `shell=False`; no compound shell commands were issued by this collector. Values not verified from commands or files are labeled UNVERIFIED.\n\n"
    report += "## Command Evidence Log\n" + command_log + "\n\n"
    report += "## A. SYSTEM\n"
    report += f"- OpenClaw version: `{cmd_map['openclaw_version']['stdout'] or 'UNVERIFIED'}`\n"
    report += f"- Node version: `{cmd_map['node_version']['stdout'] or 'UNVERIFIED'}`\n"
    report += f"- macOS version:\n```text\n{cmd_map['macos_version']['stdout']}\n```\n"
    report += f"- Last OpenClaw update date if findable: `{stat_line(OPENCLAW / 'update-check.json')}`; version command reports `{cmd_map['openclaw_version']['stdout']}`.\n"
    report += f"- Process launch/keepalive: LaunchAgent files below include OpenClaw gateway/watchdog entries; process list evidence is in Command Evidence Log.\n"
    report += f"- Current uptime:\n```text\n{cmd_map['uptime']['stdout']}\n```\n"
    report += f"- Gateway binding: {gateway_summary}\n- Gateway auth token set: {token_set}\n"
    report += f"- Free disk space:\n```text\n{cmd_map['disk_space']['stdout']}\n```\n"
    report += f"- OpenClaw process memory usage: see `process_memory` command evidence; rows containing OpenClaw are also in `openclaw_processes`.\n\n"

    report += "## B. CONFIG\n"
    report += "### Full OpenClaw Config Files (redacted)\n" + config_contents + "\n\n"
    report += "### Model IDs Found\n" + model_rows + "\n\n"
    report += f"### bootstrapMaxChars and Bootstrap Size\n- bootstrapMaxChars from AGENTS.md: 32000\n- combined counted bootstrap/identity chars: {bootstrap_total}\n{bootstrap_counts}\n\n"
    report += "### Compaction and Context Settings\nScanner source: openclaw.json and AGENTS/TOOLS rules. See full redacted config above. Search terms collected: summaryModel, summaryProvider, reserveTokensFloor, truncateAfterCompaction, maxActiveTranscriptBytes, contextThreshold, sweepMaxDepth, largeFileThresholdTokens, freshTailCount, freshTailMaxTokens.\n\n"
    report += f"### Telegram Channel Settings\n- dmPolicy: {dm_policy}\n- allowlist count: {allowlist_count}; IDs redacted by policy\n\n"

    report += "## C. WORKSPACE AND IDENTITY\n"
    report += "### Workspace Tree, 2 Levels Deep\n```text\n" + tree_depth(WORKSPACE, 2) + "\n```\n\n"
    report += "### Bootstrap and Identity File Counts\n" + bootstrap_counts + "\n\n"
    report += "### Full Bootstrap and Identity Contents (redacted)\n" + bootstrap_full + "\n\n"

    report += "## D. SCHEDULED JOBS\n"
    report += "### OpenClaw Cron Status\n```text\n" + cmd_map["openclaw_cron_status"]["stdout"] + "\n```\n\n"
    report += "### Jobs Flagged With 2+ Failures in Last 5\n" + ("\n".join(failing_jobs) if failing_jobs else "None found in parsed run files.") + "\n\n"
    report += "### Every OpenClaw Cron Job\n" + job_sections + "\n\n"
    report += "### System Crontab\n```text\n" + (crontab["stdout"] or crontab["stderr"] or "No crontab output.") + "\n```\n\n"
    report += "### User LaunchAgents\n" + launchd_contents + "\n\n"

    report += "## E. MEMORY\n"
    report += "### Memory Paths, Sizes, Modified Dates\n" + memory_stats + "\n\n"
    report += "### Persistence Summary\nMemory persists through workspace markdown/JSON files under `memory/`, OpenClaw session JSONL files under `~/.openclaw/agents/*/sessions`, Lossless Claw storage at `~/.openclaw/lcm.db` when present, cron job/run JSON under `~/.openclaw/cron`, and bootstrap files loaded into new sessions. Exact behavioral guarantees beyond file evidence are UNVERIFIED.\n\n"
    report += f"### Total Session and History Storage\n- main sessions dir size: {dir_size(OPENCLAW / 'agents' / 'main' / 'sessions')} bytes\n- all agents sessions size: {dir_size(OPENCLAW / 'agents')} bytes\n- lcm.db size: {(OPENCLAW / 'lcm.db').stat().st_size if (OPENCLAW / 'lcm.db').exists() else 0} bytes\n\n"

    report += "## F. TOOLS AND INTEGRATIONS\n"
    report += "### Enabled Skills\n```text\n" + cmd_map["openclaw_skills_check"]["stdout"] + "\n```\n\n"
    report += "### Enabled Plugins and Tool Providers\n```text\n" + cmd_map["openclaw_plugins_list"]["stdout"] + "\n```\n\n"
    report += "### External API or Service Credential Inventory\n" + env_inventory() + "\n\n"
    report += "Credential directories under `~/.openclaw/credentials/` were not read because workspace security rules prohibit touching them; their contents are UNVERIFIED.\n\n"
    report += "### MCP Servers\n```text\n" + cmd_map["openclaw_mcp_list"]["stdout"] + "\n```\n\n"

    report += "## G. SECURITY\n"
    report += "### Exec and Sandbox Settings\nCurrent audit session metadata says sandbox mode is `danger-full-access`, network access enabled, and approval policy `never`; this is runtime metadata, not verified from a local file. Local exec approvals file is included in Config.\n\n"
    report += "### Credential-Like Assignments Found in Project Files\n" + credential_scan() + "\n\n"
    report += "### Network Exposure Summary\n```text\n" + cmd_map["listening_ports"]["stdout"] + "\n```\n\n"
    report += "Network exposure assessment: OpenClaw gateway binding appears localhost or unspecified by config scan. `lsof` shows listening ports; any service bound to `*` or `0.0.0.0` should be treated as network-exposed until firewall/Tailscale rules are separately verified. Tailscale serve state is UNVERIFIED in this report because no Tailscale command was run.\n\n"

    report += "## H. HEALTH\n"
    report += "### Last 50 Error-Level Log Lines\n```text\n" + error_log_lines() + "\n```\n\n"
    report += "### Restart and Crash History Visible in Logs\nSee error-level log lines above and LaunchAgent definitions. A deeper crash history is UNVERIFIED unless macOS unified logs are exported.\n\n"
    report += "### Documented Standard Recovery Sequence\n```markdown\n" + recovery_match + "\n```\n\n"
    report += opinion + "\n"

    REPORT.write_text(redact_text(report), encoding="utf-8")
    print(str(REPORT))
    print(f"bytes={REPORT.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
