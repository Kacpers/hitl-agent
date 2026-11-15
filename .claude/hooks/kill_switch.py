"""PreToolUse hook, matcher "*": a STOP file in the project stops every tool of the agent. Exercise 5: uv run pytest -m cw5"""
import json
import os
import pathlib


# EXERCISE 5
def decision(project: pathlib.Path) -> dict | None:
    """Exercise 5. If the project folder has a STOP file, return a deny (permissionDecision "deny")
    with the reason "Kill switch: STOP file present. Doing nothing.". Otherwise return None. Check: uv run pytest -m cw5"""
    return None
# END OF EXERCISE 5


if __name__ == "__main__":
    result = decision(pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")))
    if result:
        print(json.dumps(result, ensure_ascii=False))
