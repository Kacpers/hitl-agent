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
    """Numbers become strings with two decimals (480 and 480.0 are the same money). Other values stay."""
    if type(value) in (int, float):      # bool stays bool
        return f"{value:.2f}"
    return value


def fingerprint(tool: str, args: dict) -> str:
    """Exercise 3a. Fingerprint of an action: sha256 of [tool, args with canonical() values] (json.dumps with sort_keys=True),
    first 12 chars. One grosz more must give a different fingerprint; 480 and 480.0 must give the same one."""
    raise NotImplementedError("Exercise 3a: write fingerprint()")


def consume_approval(fp: str) -> str | None:
    """Exercise 3b. Approvals live in the APPROVALS file (dict fingerprint -> who). If fp is approved:
    remove it from the file (an approval is single-use) and return who approved it. Otherwise return None.
    Check: uv run pytest -m cw3"""
    raise NotImplementedError("Exercise 3b: write consume_approval()")
# END OF EXERCISE 3
