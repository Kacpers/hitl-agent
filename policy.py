"""The agent's boundary: the model proposes, this file decides. Exercises 2 and 3.

Exercise 2: policy()                          ->  uv run pytest -m cw2
Exercise 3: fingerprint() and consume_approval()  ->  uv run pytest -m cw3
"""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ORDERS = json.loads((ROOT / "data" / "orders.json").read_text(encoding="utf-8"))
APPROVALS = ROOT / "approvals.json"          # approvals given by a human: fingerprint -> who (approve.py)


# EXERCISE 2
def policy(tool: str, args: dict) -> tuple[str, str]:
    """Returns (AUTO | HUMAN | DENY, reason). Code decides, not the model."""
    if tool == "delete_customer_data":
        return "DENY", "only a human deletes customer data"
    if tool == "refund_payment":
        order = ORDERS.get(args["order_id"])
        if not order or args["amount"] > order["amount"]:
            return "DENY", "amount is higher than the order value"
        return "HUMAN", "a refund needs a human approval"
    return "AUTO", ""
# END OF EXERCISE 2


# EXERCISE 3
def canonical(value):
    """480, 480.0 and "480.00" are the same money: numbers become strings with two decimals before hashing."""
    if type(value) in (int, float):      # bool stays bool
        return f"{value:.2f}"
    return value


def fingerprint(tool: str, args: dict) -> str:
    """The approval covers this action with these arguments: one grosz more is a different fingerprint."""
    args = {k: canonical(v) for k, v in args.items()}
    return hashlib.sha256(json.dumps([tool, args], sort_keys=True).encode()).hexdigest()[:12]


def consume_approval(fp: str) -> str | None:
    """If a human approved fp: remove the approval (it is single-use) and return who approved it."""
    approvals = json.loads(APPROVALS.read_text()) if APPROVALS.exists() else {}
    who = approvals.pop(fp, None)
    if who:
        APPROVALS.write_text(json.dumps(approvals, indent=1))
    return who
# END OF EXERCISE 3
