import pytest
from policy import policy

pytestmark = pytest.mark.cw2


def test_refund_above_order_value_denied():
    assert policy("refund_payment", {"order_id": "Z-1042", "amount": 5000})[0] == "DENY"


def test_refund_within_value_waits_for_human():
    assert policy("refund_payment", {"order_id": "Z-1042", "amount": 480})[0] == "HUMAN"


def test_data_deletion_always_denied():
    assert policy("delete_customer_data", {"customer": "[PERSON_1]"})[0] == "DENY"


def test_read_and_draft_without_human():
    assert policy("check_order", {"order_id": "Z-1042"})[0] == "AUTO"
    assert policy("draft_reply", {"body": "Dzień dobry"})[0] == "AUTO"
