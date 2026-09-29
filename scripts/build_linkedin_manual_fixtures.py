#!/usr/bin/env python3
"""Render and verify one local manual LinkedIn fixture from frozen JSON."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.linkedin_content_os.canonical import canonical_bytes
from scripts.linkedin_content_os.manual_fixtures import build_manual_fixture


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--now", required=True)
    arguments = parser.parse_args()
    source = json.loads(Path(arguments.source).read_text(encoding="utf-8"))
    packet = build_manual_fixture(
        source,
        Path(arguments.artifact_root),
        now=datetime.fromisoformat(arguments.now),
    )
    print(canonical_bytes(packet).decode("utf-8"))


if __name__ == "__main__":
    main()
