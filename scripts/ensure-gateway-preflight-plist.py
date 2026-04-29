#!/usr/bin/env python3
"""Ensure the local launchd gateway job starts through gateway-preflight.sh.

OpenClaw's installer/restart path can regenerate the LaunchAgent with direct Node
ProgramArguments. This local hardening hook reapplies the preflight wrapper so
missing Homebrew dylibs fail with actionable diagnostics before launchd loops.
"""
from __future__ import annotations
import os, plistlib
from pathlib import Path

home = Path.home()
plist_path = home / 'Library/LaunchAgents/ai.openclaw.gateway.plist'
wrapper = str(home / '.openclaw/workspace/scripts/gateway-preflight.sh')

with plist_path.open('rb') as f:
    data = plistlib.load(f)
args = data.get('ProgramArguments') or []
if args == [wrapper, 'run']:
    print('gateway preflight wrapper already installed')
    raise SystemExit(0)

data['ProgramArguments'] = [wrapper, 'run']
# Ensure env still includes port for the wrapper.
env = data.setdefault('EnvironmentVariables', {})
env.setdefault('OPENCLAW_GATEWAY_PORT', '18789')
with plist_path.open('wb') as f:
    plistlib.dump(data, f, sort_keys=False)
print('gateway preflight wrapper installed')
