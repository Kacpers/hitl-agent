"""PreToolUse hook on Bash: a Python script that sends data to a host outside the allowlist does not start.

It does not ask the model whether the script is safe. It parses the script (ast) and looks for network calls.
A seatbelt, not a vault: an encoded or assembled import gets through. The sandbox closes the network.
"""
import ast
import json
import os
import pathlib
import re
import sys

ALLOWED = {"api.nbp.pl"}                        # hosts scripts in the company may talk to
NETWORK_MODULES = {"urllib", "requests", "http", "httpx", "aiohttp", "socket", "smtplib", "ftplib"}


def check_script(path: pathlib.Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imports = [n.lineno for n in ast.walk(tree) if any(
        name.split(".")[0] in NETWORK_MODULES for name in ([a.name for a in n.names] if isinstance(n, ast.Import) else
                                                           [n.module or ""] if isinstance(n, ast.ImportFrom) else []))]
    if not imports:
        return None
    foreign = sorted(set(re.findall(r"https?://([A-Za-z0-9.\-]+)", text)) - ALLOWED)
    if not foreign and re.findall(r"https?://", text):
        return None                                     # network only to allowed hosts
    calls = sorted(n.lineno for n in ast.walk(tree)
                   if isinstance(n, ast.Call) and ast.unparse(n.func).split(".")[0] in NETWORK_MODULES)
    line = calls[0] if calls else imports[0]           # the line where the network call really happens
    return f"{path.name}, line {line}: network call to a host not on the allowlist: {', '.join(foreign) or 'unknown'}"


def decision(command: str, project: pathlib.Path) -> dict | None:
    for script in re.findall(r"[\w./\-]+\.py\b", command):
        path = (project / script) if not os.path.isabs(script) else pathlib.Path(script)
        if path.is_file() and (reason := check_script(path)):
            return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                           "permissionDecisionReason": f"block_network: {reason}. Data does not leave for unknown hosts."}}
    return None


if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
        result = decision(data.get("tool_input", {}).get("command", ""), pathlib.Path(data.get("cwd") or "."))
    except Exception as error:
        result = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"block_network: error ({error.__class__.__name__})"}}
    if result:
        print(json.dumps(result, ensure_ascii=False))
