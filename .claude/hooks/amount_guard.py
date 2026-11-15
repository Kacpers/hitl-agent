"""PreToolUse hook on create_draft: the skill says "take the amount from the script output", this hook checks it.

A skill is a request. A draft with an amount above the maximum refund (same rule as scripts/refund.py) is not saved.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORDERS = json.loads((ROOT / "data" / "orders.json").read_text(encoding="utf-8"))
AMOUNT = re.compile(r"(\d[\d  ]*(?:[.,]\d{1,2})?)\s*(?:zł|PLN)", re.I)


def max_refund(order_id: str) -> float:
    order = ORDERS.get(order_id)
    return order["amount"] if order and order["status"] == "delivered" else 0.0


def decision(tool_name: str, args: dict) -> dict | None:
    if not tool_name.endswith("create_draft"):
        return None
    text = f"{args.get('subject', '')}\n{args.get('body', '')}"
    orders = set(re.findall(r"Z-\d+", text))
    if not orders:
        return None
    limit = max(max_refund(o) for o in orders)
    for raw in AMOUNT.findall(text):
        amount = float(re.sub(r"[  ]", "", raw).replace(",", "."))
        if amount > limit:
            reason = (f"Amount {amount:.2f} PLN in the draft is higher than the maximum refund from the script ({limit:.2f} PLN). "
                      "Take amounts only from the refund.py output; put the customer's request in the NEEDS DECISION note.")
            return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                           "permissionDecision": "deny", "permissionDecisionReason": reason}}
    return None


if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
        result = decision(data.get("tool_name", ""), data.get("tool_input") or {})
    except Exception as error:  # fail closed
        result = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"amount_guard: error ({error.__class__.__name__})"}}
    if result:
        print(json.dumps(result, ensure_ascii=False))
