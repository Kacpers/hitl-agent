"""PreToolUse hook on MCP tools: sending, publishing and deleting is done by a human. Exercise 4: uv run pytest -m cw4

Input: JSON from Claude Code on stdin (tool_name, tool_input). Output: a JSON decision, or nothing (= the usual permission prompt).
"""
import json
import re
import sys

# EXERCISE 4
RULES = []  # Exercise 4: (pattern for the tool name after "mcp__server__", reason) for sending, deleting and publishing


def decision(tool_name: str) -> dict | None:
    """Exercise 4. For MCP tools that send (send, reply, forward), delete (delete, trash, remove)
    or publish (publish, execute), return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
    "permissionDecision": "deny", "permissionDecisionReason": reason}}. Return None for anything else.
    Note: untrash_message and unpublish_workflow must pass. Check: uv run pytest -m cw4"""
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
