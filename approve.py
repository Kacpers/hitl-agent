"""A human approves one specific action by its fingerprint. It first shows what is being approved (from the agent log)."""
import getpass
import json
import sys

from policy import APPROVALS, ROOT

fp = sys.argv[1]
entries = [json.loads(line) for line in (ROOT / "log.jsonl").read_text(encoding="utf-8").splitlines()] if (ROOT / "log.jsonl").exists() else []
action = next((e for e in reversed(entries) if e["fingerprint"] == fp), None)
if not action:
    sys.exit(f"Unknown fingerprint {fp}: the agent never asked for this action.")
print(f"approving: {action['tool']} {json.dumps(action['args'], ensure_ascii=False)}")
approvals = json.loads(APPROVALS.read_text()) if APPROVALS.exists() else {}
approvals[fp] = getpass.getuser()
APPROVALS.write_text(json.dumps(approvals, indent=1))
print(f"approved: {fp} by {approvals[fp]}")
