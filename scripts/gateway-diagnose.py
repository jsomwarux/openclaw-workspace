#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, plistlib, re, socket, subprocess, sys, time
from pathlib import Path

HOME = Path.home()
LOG_DIR = HOME / '.openclaw' / 'logs'
ERR_LOG = LOG_DIR / 'gateway.err.log'
OUT_LOG = LOG_DIR / 'gateway.log'
PREFLIGHT_LOG = LOG_DIR / 'gateway-preflight.log'
WATCHDOG_STATE = LOG_DIR / 'watchdog-state.json'
PLIST = HOME / 'Library/LaunchAgents/ai.openclaw.gateway.plist'
DEFAULT_NODE = '/opt/homebrew/opt/node@22/bin/node'
PORT = int(os.environ.get('OPENCLAW_GATEWAY_PORT', '18789'))
SECRET_RE = re.compile(r'(sk-[A-Za-z0-9_-]{8})[A-Za-z0-9_-]+|(Bearer\s+)[A-Za-z0-9._-]+|([A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*=)[^\s]+')

def redact(s: str) -> str:
    def repl(m):
        if m.group(1): return m.group(1) + '[REDACTED]'
        if m.group(2): return m.group(2) + '[REDACTED]'
        if m.group(3): return m.group(3) + '[REDACTED]'
        return '[REDACTED]'
    return SECRET_RE.sub(repl, s)

def run(cmd, timeout=8):
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 999, '', str(e)

def tail(path: Path, n=20) -> list[str]:
    try:
        data = path.read_text(errors='replace').splitlines()
        return data[-n:]
    except FileNotFoundError:
        return []

def node_from_plist() -> str:
    try:
        with PLIST.open('rb') as f:
            d = plistlib.load(f)
        args = d.get('ProgramArguments') or []
        first = args[0] if args else DEFAULT_NODE
        # LaunchAgent may point at the preflight wrapper. Diagnostics should still
        # validate/report the real Node binary that dyld loads.
        if first.endswith('gateway-preflight.sh'):
            return os.environ.get('OPENCLAW_NODE_BIN', DEFAULT_NODE)
        return first
    except Exception:
        return DEFAULT_NODE

def port_listening(port=PORT) -> bool:
    s = socket.socket()
    s.settimeout(0.5)
    try:
        return s.connect_ex(('127.0.0.1', port)) == 0
    finally:
        s.close()

def launchctl_state():
    rc, out, err = run(['launchctl', 'print', f'gui/{os.getuid()}/ai.openclaw.gateway'], timeout=5)
    text = out + err
    pid = re.search(r'pid = (\d+)', text)
    last_exit = re.search(r'last exit code = ([^\n]+)', text)
    state = re.search(r'state = ([^\n]+)', text)
    return {'rc': rc, 'pid': pid.group(1) if pid else None, 'state': state.group(1).strip() if state else None, 'last_exit': last_exit.group(1).strip() if last_exit else None, 'raw_tail': '\n'.join(text.splitlines()[-20:])}

def otool_missing(node: str) -> list[str]:
    if not Path(node).exists():
        return [node]
    rc, out, err = run(['otool', '-L', node], timeout=8)
    if rc != 0:
        return [f'otool failed: {err or out}']
    missing=[]
    for line in out.splitlines()[1:]:
        p=line.strip().split(' ',1)[0]
        if p.startswith(('/opt/homebrew/', '/usr/local/')) and not Path(p).exists():
            missing.append(p)
    simd=Path('/opt/homebrew/opt/simdjson/lib')
    if not simd.exists():
        missing.append(str(simd))
    elif not list(simd.glob('libsimdjson.*.dylib')):
        missing.append(str(simd / 'libsimdjson.*.dylib'))
    return missing

def classify(lines: list[str], missing: list[str], port_ok: bool, gateway_pid: str | None = None) -> tuple[str,str]:
    text='\n'.join(lines + missing)
    low=text.lower()
    if port_ok and gateway_pid and not missing and 'library not loaded' not in low and 'dyld' not in low:
        return 'healthy', 'no repair needed'
    if missing or 'library not loaded' in low or 'dyld' in low or 'image not found' in low or 'no such file or directory' in low and 'node' in low:
        return 'dependency/runtime failure', 'brew update && brew reinstall simdjson && brew reinstall node@22'
    if 'eaddrinuse' in low or 'address already in use' in low:
        return 'port conflict', f'lsof -nP -iTCP:{PORT} -sTCP:LISTEN'
    if 'missing' in low and ('api' in low or 'token' in low or 'key' in low) or 'invalid api key' in low or 'unauthorized' in low:
        return 'config/auth failure', 'check ~/.config/env/global.env and auth profiles; do not print secrets'
    if '429' in low or 'rate limit' in low or 'quota' in low or 'insufficient_quota' in low:
        return 'model/API failure', 'wait for quota reset or change model route; do not restart-loop the gateway'
    if port_ok:
        return 'channel failure or non-fatal runtime warning', 'gateway port is alive; inspect channel/plugin logs before restarting'
    if 'uncaught' in low or 'exception' in low or 'error:' in low:
        return 'runtime crash', 'inspect stack trace in gateway.err.log and recent config changes'
    return 'startup crash', 'run openclaw doctor and inspect gateway.err.log / gateway-preflight.log'

def diagnose_json():
    node=node_from_plist()
    lc=launchctl_state()
    err=tail(ERR_LOG,20)
    pre=tail(PREFLIGHT_LOG,20)
    out=tail(OUT_LOG,20)
    missing=otool_missing(node)
    port_ok=port_listening()
    category, fix=classify(pre+err, missing, port_ok, lc.get('pid'))
    rc, nv, ne = run([node, '--version'], timeout=5) if Path(node).exists() else (127,'','missing')
    cfg=HOME/'.openclaw/openclaw.json'
    config_model='unknown'
    try:
        d=json.load(cfg.open())
        config_model=d.get('agents',{}).get('defaults',{}).get('model') or d.get('model') or 'unknown'
    except Exception:
        pass
    payload={
        'category': category,
        'recommended_fix': fix,
        'launchctl': lc,
        'gateway_pid': lc.get('pid'),
        'port_18789_listening': port_ok,
        'node_path': node,
        'node_version': (nv or ne).strip(),
        'missing_dylibs': missing,
        'last_20_stderr_lines': [redact(x) for x in err],
        'last_20_preflight_lines': [redact(x) for x in pre],
        'last_20_stdout_lines': [redact(x) for x in out],
        'model_route': config_model,
    }
    return payload

def format_alert(d):
    missing='\n'.join(f'- {x}' for x in d['missing_dylibs']) or '- none detected by otool'
    stderr='\n'.join(d['last_20_stderr_lines'][-20:]) or '(no stderr lines)'
    healthy = d.get('category') == 'healthy'
    emoji = '✅' if healthy else '🚨'
    label = 'OpenClaw gateway diagnostic' if healthy else 'OpenClaw gateway failure'
    recovery = '' if healthy else f"""
Recommended fix:
{d['recommended_fix']}

Safe manual recovery after fixing deps:
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist"""
    return redact(f"""{emoji} {label}: {d['category']}

Last exit reason: {d['launchctl'].get('last_exit') or 'unknown'}
Gateway PID: {d.get('gateway_pid') or 'not running'}
Port {PORT} listening: {d['port_18789_listening']}
Node: {d['node_path']} ({d['node_version']})

Missing dylibs:
{missing}

Last 20 stderr lines:
{stderr}{recovery}""")

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'text'
    d=diagnose_json()
    if mode=='json':
        print(json.dumps(d, indent=2))
    elif mode=='alert':
        if d.get('category') == 'healthy':
            return
        print(format_alert(d))
    else:
        print(format_alert(d))

if __name__=='__main__':
    main()
