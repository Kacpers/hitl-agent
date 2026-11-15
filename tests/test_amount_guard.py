from conftest import denied, hook


def draft(body, subject="Reklamacja Z-1042"):
    return {"tool_name": "mcp__mailbox__create_draft", "tool_input": {"to": "[EMAIL_1]", "subject": subject, "body": body}}


def test_amount_above_script_output_denied():
    assert denied(hook("amount_guard.py", draft("Zwrócimy Panu 5 000,00 zł.")))


def test_amount_from_script_output_passes():
    assert hook("amount_guard.py", draft("Zlecamy zwrot 480,00 zł.")) is None


def test_order_in_transit_has_no_refund():
    assert denied(hook("amount_guard.py", draft("Zwrot 89,90 zł", subject="Reklamacja Z-1103")))


def test_other_tools_untouched():
    assert hook("amount_guard.py", {"tool_name": "mcp__mailbox__list", "tool_input": {"body": "5000 zł Z-1042"}}) is None
