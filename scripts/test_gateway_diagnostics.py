#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, os, tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name('gateway-diagnose.py')
spec = importlib.util.spec_from_file_location('gateway_diagnose', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore

def test_missing_dylib_classification_and_alert():
    lines = [
        'dyld[123]: Library not loaded: /opt/homebrew/opt/simdjson/lib/libsimdjson.29.dylib',
        '  Referenced from: /opt/homebrew/Cellar/node@22/22.22.0/bin/node',
        '  Reason: tried: /opt/homebrew/opt/simdjson/lib/libsimdjson.29.dylib (no such file)'
    ]
    category, fix = mod.classify(lines, ['/opt/homebrew/opt/simdjson/lib/libsimdjson.29.dylib'], False)
    assert category == 'dependency/runtime failure'
    assert 'brew reinstall simdjson' in fix
    payload = {
        'category': category,
        'recommended_fix': fix,
        'launchctl': {'last_exit': '78'},
        'gateway_pid': None,
        'port_18789_listening': False,
        'node_path': '/opt/homebrew/opt/node@22/bin/node',
        'node_version': 'dyld failure',
        'missing_dylibs': ['/opt/homebrew/opt/simdjson/lib/libsimdjson.29.dylib'],
        'last_20_stderr_lines': lines,
    }
    alert = mod.format_alert(payload)
    assert 'Library not loaded' in alert
    assert '/opt/homebrew/opt/simdjson/lib/libsimdjson.29.dylib' in alert
    assert 'brew reinstall simdjson' in alert
    assert 'brew reinstall node@22' in alert

def test_alert_redaction():
    s = mod.redact('OPENAI_API_KEY=sk-test123456789SECRET Bearer abc.def.ghi')
    assert 'SECRET' not in s
    assert 'abc.def.ghi' not in s
    assert '[REDACTED]' in s

if __name__ == '__main__':
    test_missing_dylib_classification_and_alert()
    test_alert_redaction()
    print('gateway diagnostics tests passed')
