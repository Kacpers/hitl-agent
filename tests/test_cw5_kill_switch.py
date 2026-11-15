import pytest
from conftest import denied, hook

pytestmark = pytest.mark.cw5


def test_stop_file_blocks_everything(tmp_path):
    (tmp_path / "STOP").touch()
    assert denied(hook("kill_switch.py", {"tool_name": "Read", "tool_input": {}}, tmp_path))


def test_no_stop_file_blocks_nothing(tmp_path):
    assert hook("kill_switch.py", {"tool_name": "Read", "tool_input": {}}, tmp_path) is None
