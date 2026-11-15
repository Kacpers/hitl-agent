from conftest import ROOT, denied, hook


def test_colleague_script_stopped_at_line_18():
    r = hook("block_network.py", {"tool_name": "Bash", "cwd": str(ROOT),
                                  "tool_input": {"command": "uv run colleague_tools/export-complaints/scripts/export.py log.jsonl"}})
    assert denied(r) and "line 18" in r["hookSpecificOutput"]["permissionDecisionReason"]


def test_refund_script_passes():
    assert hook("block_network.py", {"tool_name": "Bash", "cwd": str(ROOT),
                                     "tool_input": {"command": "uv run .claude/skills/handle-complaint/scripts/refund.py Z-1042 5000"}}) is None
