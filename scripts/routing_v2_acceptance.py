#!/usr/bin/env python3
"""Deterministic temporary-ledger acceptance check for Routing V2."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / "scripts/model_capacity_controller.py"
PRODUCTION_LEDGER = ROOT / "memory/capacity/execution-ledger.jsonl"
ATTEMPT_ID = "00000000-0000-4000-8000-000000000001"


def file_signature(path: Path):
    if not path.exists():
        return {"exists": False, "sha256": None, "bytes": 0}
    content = path.read_bytes()
    return {
        "exists": True,
        "sha256": hashlib.sha256(content).hexdigest(),
        "bytes": len(content),
    }


def run_json(args):
    process = subprocess.run(
        [sys.executable, str(CONTROLLER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or process.stdout.strip())
    return json.loads(process.stdout)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--production-ledger", type=Path, default=PRODUCTION_LEDGER)
    args = parser.parse_args(argv)

    report_path = args.report.resolve(strict=False)
    production_ledger = args.production_ledger.resolve(strict=False)
    if report_path == production_ledger:
        parser.error("--report must not resolve to the production ledger")
    if report_path.exists() and production_ledger.exists() and report_path.samefile(production_ledger):
        parser.error("--report must not alias the production ledger")

    before = file_signature(production_ledger)
    captured_at = datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        current = temp_root / "current.json"
        execution = temp_root / "execution.jsonl"
        current.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "providers": {
                        "codex": {
                            "provider": "codex",
                            "remaining_percent": 99.0,
                            "reset_at": None,
                            "captured_at": captured_at,
                            "source": "routing-v2-acceptance",
                        },
                        "claude": {
                            "provider": "claude",
                            "remaining_percent": 99.0,
                            "reset_at": None,
                            "captured_at": captured_at,
                            "source": "routing-v2-acceptance",
                        },
                    },
                },
                sort_keys=True,
            )
        )
        preflight = run_json(
            [
                "--current", str(current),
                "--execution-ledger", str(execution),
                "preflight",
                "--task-id", "acceptance-buyer-copy",
                "--attempt-id", ATTEMPT_ID,
                "--task", "Routing V2 acceptance",
                "--task-kind", "buyer_copy",
                "--size", "medium",
                "--estimated-burn", "8",
                "--estimated-minutes", "12",
                "--batch-items", "25",
            ]
        )
        completion = run_json(
            [
                "--execution-ledger", str(execution),
                "complete",
                "--task-id", "acceptance-buyer-copy",
                "--attempt-id", ATTEMPT_ID,
                "--tool-calls", "8",
                "--provider-delta", "unknown",
                "--avoidable-delay-minutes", "0",
                "--delivered",
            ]
        )
        summary = run_json(
            ["--execution-ledger", str(execution), "summary", "--days", "7"]
        )
        events = [json.loads(line) for line in execution.read_text().splitlines() if line.strip()]

    after = file_signature(production_ledger)
    require(preflight["decision"] == "route", "preflight did not route")
    require(preflight["provider"] == "codex", "preflight did not select codex")
    require(preflight["attempt_id"] == ATTEMPT_ID, "attempt ID changed")
    require(
        [event["event_type"] for event in events] == ["preflight", "complete"],
        "temporary ledger event sequence is invalid",
    )
    require(completion["sla_verdict"] == "on_target", "SLA verdict is not on_target")
    require(completion["provider_delta"] is None, "unknown provider delta was inferred")
    require(summary["completion_count"] == 1, "summary completion count is invalid")
    require(before == after, "production execution ledger changed")

    report = {
        "status": "ok",
        "events": len(events),
        "provider": preflight["provider"],
        "attempt_id": preflight["attempt_id"],
        "sla_verdict": completion["sla_verdict"],
        "provider_delta": completion["provider_delta"],
        "production_ledger_unchanged": True,
        "summary": summary,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("ROUTING_V2_ACCEPTANCE_OK events=2 sla=on_target provider_delta=null")
    return 0


if __name__ == "__main__":
    sys.exit(main())
