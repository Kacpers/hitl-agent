import pytest
from conftest import denied, hook

pytestmark = pytest.mark.cw4


@pytest.mark.parametrize("tool", ["mcp__mailbox__send_message", "mcp__claude_ai_Gmail__reply",
                                  "mcp__claude_ai_Google_Calendar__delete_event", "mcp__n8n__publish_workflow"])
def test_send_delete_publish_blocked(tool):
    assert denied(hook("block_send.py", {"tool_name": tool, "tool_input": {}}))


@pytest.mark.parametrize("tool", ["mcp__mailbox__create_draft", "mcp__claude_ai_Gmail__untrash_message",
                                  "mcp__n8n__unpublish_workflow", "Bash"])
def test_draft_and_reverse_actions_pass(tool):
    assert hook("block_send.py", {"tool_name": tool, "tool_input": {}}) is None


def test_garbage_input_blocks():
    assert denied(hook("block_send.py", "this is not JSON"))
