import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
HOOKS = ROOT / ".claude" / "hooks"


def hook(script, payload, project=ROOT):
    """Runs a hook the way Claude Code does: JSON on stdin. Returns the parsed output or None."""
    p = subprocess.run([sys.executable, str(HOOKS / script)], input=payload if isinstance(payload, str) else json.dumps(payload),
                       capture_output=True, text=True, env={**os.environ, "CLAUDE_PROJECT_DIR": str(project)})
    return json.loads(p.stdout) if p.stdout.strip() else None


def denied(result):
    return bool(result) and result["hookSpecificOutput"]["permissionDecision"] == "deny"
