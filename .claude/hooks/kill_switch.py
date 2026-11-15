"""PreToolUse hook, matcher "*": a STOP file in the project stops every tool of the agent. Exercise 5: uv run pytest -m cw5"""
import json
import os
import pathlib


# EXERCISE 5
def decision(project: pathlib.Path) -> dict | None:
    if (project / "STOP").exists():
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": "Kill switch: STOP file present. Doing nothing."}}
    return None
# END OF EXERCISE 5


if __name__ == "__main__":
    result = decision(pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")))
    if result:
        print(json.dumps(result, ensure_ascii=False))
