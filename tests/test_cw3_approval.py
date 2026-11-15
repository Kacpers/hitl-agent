import json
import pytest
import policy

pytestmark = pytest.mark.cw3


def test_approval_pinned_to_amount():
    a = policy.fingerprint("refund_payment", {"order_id": "Z-1042", "amount": 480})
    b = policy.fingerprint("refund_payment", {"order_id": "Z-1042", "amount": 481})
    assert a != b


def test_same_amount_written_differently_is_the_same_approval():
    a = policy.fingerprint("refund_payment", {"order_id": "Z-1042", "amount": 480})
    b = policy.fingerprint("refund_payment", {"order_id": "Z-1042", "amount": 480.0})
    assert a == b   # found in a real run on 15.11: the human approved 480, the model sent 480.0


def test_approval_is_single_use(tmp_path, monkeypatch):
    monkeypatch.setattr(policy, "APPROVALS", tmp_path / "approvals.json")
    fp = policy.fingerprint("refund_payment", {"order_id": "Z-1042", "amount": 480})
    (tmp_path / "approvals.json").write_text(json.dumps({fp: "kacper"}))
    assert policy.consume_approval(fp) == "kacper"
    assert policy.consume_approval(fp) is None


def test_no_approval(tmp_path, monkeypatch):
    monkeypatch.setattr(policy, "APPROVALS", tmp_path / "approvals.json")
    assert policy.consume_approval("0123456789ab") is None
