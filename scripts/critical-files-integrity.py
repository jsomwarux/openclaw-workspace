#!/usr/bin/env python3
"""
Critical Files Integrity Check + Auto-Discovery
Compares critical memory/agent files against git reference.
Restores from git if file has been truncated to <50% of reference size.
Auto-discovers new AGENT.md and SKILL.md files not yet in FILE_REFS.
Run via cron: daily 9AM ET (UUID: ee357abb)
"""
import subprocess, sys, os
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
os.chdir(WORKSPACE)

# Known good git refs per file
FILE_REFS = {
    # Critical memory files
    "memory/content-voice.md": "b89cabd",
    "memory/FEEDBACK-LOG.md": "b89cabd",
    "docs/x-algorithm.md": "b89cabd",
    # Agent files (auto-discovered 2026-04-14)
    "agents/vibe-marketing/AGENT.md": "61d5594",
    "agents/content-scheduler/AGENT.md": "6605054",
    "agents/launch-kit/AGENT.md": "47f3721",
    "agents/autoresearch/AGENT.md": "47f3721",
    "agents/networking/AGENT.md": "47f3721",
    "agents/niche-fitness/AGENT.md": "b89cabdc",
    "agents/portfolio-updater/AGENT.md": "e76cf9f",
    "agents/skills-researcher/AGENT.md": "e76cf9f",
    "agents/content-calendar/AGENT.md": "b89cabdc",
    "agents/critic/AGENT.md": "b89cabdc",
    "agents/passive-income-scout/AGENT.md": "e76cf9f",
    "agents/job-tracker/AGENT.md": "b89cabdc",
    "agents/t3-cold-hook/AGENT.md": "486a1d9",
    "agents/passive-income-strategist/AGENT.md": "e76cf9f",
    "agents/overnight/AGENT.md": "e76cf9f",
    # Skill files (auto-discovered 2026-04-14)
    "skills/runbook/SKILL.md": "5eac0c4",
    "skills/cold-email/SKILL.md": "5eac0c4",
    "skills/job-application/SKILL.md": "b89cabd",
    "skills/positioning-angles/SKILL.md": "486a1d9",
    "skills/ui-clone/SKILL.md": "5b4a2ca",
    "skills/qmd/SKILL.md": "c75c008",
    "skills/x-research/SKILL.md": "e76cf9f",
    "skills/launch-strategy/SKILL.md": "486a1d9",
    "skills/opticfy-ops/SKILL.md": "ad9173c3",
    "skills/agentguard-positioning/SKILL.md": "ff7dd30",
    "skills/prompt-library/SKILL.md": "e76cf9f",
    "skills/content-atomizer/SKILL.md": "486a1d9",
    "skills/post-bridge-social-manager/SKILL.md": "0f652db",
    "skills/portfolio-card/SKILL.md": "b89cabdc",
    "skills/ai-seo/SKILL.md": "486a1d9",
    "skills/webapp-testing/SKILL.md": "3aeb22d",
    "skills/wednesday-linkedin/SKILL.md": "47f3721",
    "skills/opticfy-pipeline/SKILL.md": "ad9173c3",
    "skills/mcp-builder/SKILL.md": "3aeb22d",
    "skills/content-generation/SKILL.md": "691d1f48",
    "skills/system-auditor/SKILL.md": "8042966f",
    "skills/notion-integration/SKILL.md": "8042966f",
    "skills/google-drive/SKILL.md": "8042966f",
    "skills/video-generation/SKILL.md": "8042966f",
    "skills/google-slides/SKILL.md": "b62aeb89",
    "skills/ux-architecture/SKILL.md": "933c2ef8",
    "skills/sports-gm/SKILL.md": "357ca121",
    "skills/workflow-skillify/SKILL.md": "62739dbcdeff58a46a1dd24fcb25889ccf053758",
    "skills/high-stakes-draft-eval/SKILL.md": "62739dbcdeff58a46a1dd24fcb25889ccf053758",
    "agents/mission-control-priority-auditor/AGENT.md": "3e4cc2bf2da3cae470cf6f4737eb9ce9cb0897f4",
    "agents/ai-ops-teardown/AGENT.md": "3e4cc2bf2da3cae470cf6f4737eb9ce9cb0897f4",
    "skills/ai-governance-readiness/SKILL.md": "f245c53eeb57a7a1f1c9601fc8663471bed66b8f",
    "agents/client-proof-engine/AGENT.md": "b8619d18007ffce53fe12daf2a1ca09c8001c2a4",
    "agents/linkedin-corpus/AGENT.md": "b8619d18007ffce53fe12daf2a1ca09c8001c2a4",
    "skills/ai-context-os/SKILL.md": "b8619d18007ffce53fe12daf2a1ca09c8001c2a4",
    "skills/client-proof-capture/SKILL.md": "b8619d18007ffce53fe12daf2a1ca09c8001c2a4",
    "skills/linkedin-corpus/SKILL.md": "b8619d18007ffce53fe12daf2a1ca09c8001c2a4",
    "agents/workflow-strategist/AGENT.md": "46f0d88b71ddaf7ba6931b7408858c9647df4695",
    "agents/product-quality-pass/AGENT.md": "46f0d88b71ddaf7ba6931b7408858c9647df4695",
    "skills/n8n-blueprint/SKILL.md": "46f0d88b71ddaf7ba6931b7408858c9647df4695",
    "skills/product-build-loop/SKILL.md": "46f0d88b71ddaf7ba6931b7408858c9647df4695",
    "skills/proposal-pdf/SKILL.md": "46f0d88b71ddaf7ba6931b7408858c9647df4695",
    "skills/plan-review-pack/SKILL.md": "d0b62d2d9726224259e1d9e6e049bcd3113ff39f",
}

def get_git_lines(file_path, ref):
    try:
        result = subprocess.run(
            ["git", "show", f"{ref}:{file_path}"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return len(result.stdout.splitlines())
    except:
        pass
    return None

def restore_from_git(file_path, ref):
    try:
        content = subprocess.run(
            ["git", "show", f"{ref}:{file_path}"],
            capture_output=True, text=True, timeout=10
        )
        if content.returncode == 0:
            full_path = WORKSPACE / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content.stdout)
            return True
    except:
        pass
    return False

def discover_new_critical_files():
    """Find AGENT.md and SKILL.md files not in FILE_REFS."""
    new_files = []
    workspace = Path(WORKSPACE)
    # Scan agents/
    agents_dir = workspace / "agents"
    if agents_dir.exists():
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                agt_file = agent_dir / "AGENT.md"
                if agt_file.exists():
                    rel = agt_file.relative_to(workspace)
                    if str(rel) not in FILE_REFS:
                        new_files.append(str(rel))
    # Scan skills/
    skills_dir = workspace / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skl_file = skill_dir / "SKILL.md"
                if skl_file.exists():
                    rel = skl_file.relative_to(workspace)
                    if str(rel) not in FILE_REFS:
                        new_files.append(str(rel))
    return new_files

def run_cron_snapshot():
    """Snapshot jobs.json daily through the existing zero-LLM integrity cron."""
    snapshot_script = WORKSPACE / "scripts/cron_snapshot.py"
    if not snapshot_script.exists():
        return False, "CRON_SNAPSHOT_MISSING scripts/cron_snapshot.py"
    result = subprocess.run(
        ["python3", str(snapshot_script)],
        capture_output=True, text=True, timeout=60
    )
    output = (result.stdout or result.stderr).strip()
    return result.returncode == 0, output or f"CRON_SNAPSHOT_EXIT_{result.returncode}"

def main():
    alerts = []
    restored = []
    new_found = []

    # Check FILE_REFS files
    for file_path, ref in FILE_REFS.items():
        full_path = WORKSPACE / file_path
        if not full_path.exists():
            alerts.append(f"  MISSING: {file_path}")
            continue

        current_lines = len(full_path.read_text().splitlines())
        git_lines = get_git_lines(file_path, ref)

        if git_lines is None:
            alerts.append(f"  NO GIT REF: {file_path} (ref={ref} not found)")
            continue

        # Alert if current is <50% of git reference (wipe detected)
        if current_lines < git_lines * 0.5:
            alerts.append(f"  🔴 WIPE DETECTED: {file_path} ({current_lines} lines vs {git_lines} in git ref {ref})")
            if restore_from_git(file_path, ref):
                restored.append(f"  ✅ Restored from git ({ref}): {file_path}")
            else:
                alerts.append(f"  ❌ FAILED TO RESTORE: {file_path}")
        else:
            pct = int(current_lines / git_lines * 100)
            marker = "OK" if pct >= 80 else "⚠️ REDUCED"
            print(f"  {marker}: {file_path} ({current_lines}/{git_lines} lines, {pct}%)")

    # Auto-discovery: find new AGENT.md/SKILL.md not in FILE_REFS
    new_files = discover_new_critical_files()
    if new_files:
        for f in new_files:
            print(f"  🆕 NEW FILE (not in FILE_REFS): {f}")
            new_found.append(f)

    if alerts:
        print("=== Integrity Alerts ===")
        for a in alerts:
            print(a)
    if restored:
        print("=== Restored ===")
        for r in restored:
            print(r)
    if new_found:
        print("=== New Files Found — add to FILE_REFS ===")
        for n in new_found:
            print(f"  {n}")
        print("\nTo add: run 'git log --all --format=\"%H\" -- <file> | head -1' to find the oldest good ref.")

    snapshot_ok, snapshot_output = run_cron_snapshot()
    print(f"=== Cron Snapshot ===\n  {snapshot_output}")
    if not snapshot_ok:
        alerts.append(f"  CRON SNAPSHOT FAILED: {snapshot_output}")

    # Exit codes: 0=all OK, 1=wipe detected or restore failed, 2=new files found
    if alerts:
        sys.exit(1)
    elif new_found:
        sys.exit(2)  # New files found — signal cron to add to FILE_REFS
    else:
        print("All critical files intact. No new files detected.")

if __name__ == "__main__":
    main()
