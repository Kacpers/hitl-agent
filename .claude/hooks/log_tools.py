"""PostToolUse hook, matcher "*": one JSON line per tool call (what, with which input, when)."""
import datetime
import json
import os
import pathlib
import sys

data = json.load(sys.stdin)
project = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
with open(project / "tool_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({"time": datetime.datetime.now().isoformat(timespec="seconds"),
                        "tool": data.get("tool_name"), "input": data.get("tool_input")}, ensure_ascii=False) + "\n")
