"""PreToolUse hook on MCP tools: sending, publishing and deleting is done by a human. Exercise 4: uv run pytest -m cw4

Input: JSON from Claude Code on stdin (tool_name, tool_input). Output: a JSON decision, or nothing (= the usual permission prompt).
"""
import json
import re
import sys

# EXERCISE 4
RULES = [  # (pattern for the tool name after "mcp__server__", reason)
    (r"(^|_)(send|reply|forward)", "Sending is blocked. Prepare a draft with create_draft. A human sends it."),
    (r"(^|_)(delete|trash|remove)", "Deleting is blocked. Tell the human what you propose to delete and why."),
    (r"(^|_)(publish|execute)", "Publishing to a live system is blocked. Leave it to a human."),
]


def decision(tool_name: str) -> dict | None:
    part = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", tool_name.split("__")[-1]).replace("-", "_").lower()
    for pattern, reason in RULES:
        if tool_name.startswith("mcp__") and re.search(pattern, part):
            return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                           "permissionDecision": "deny", "permissionDecisionReason": reason}}
    return None
# END OF EXERCISE 4


if __name__ == "__main__":
    try:
        result = decision(json.load(sys.stdin).get("tool_name", ""))
    except Exception as error:  # unexpected input: block, do not let it through (fail closed)
        result = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"block_send: error ({error.__class__.__name__})"}}
    if result:
        print(json.dumps(result, ensure_ascii=False))
