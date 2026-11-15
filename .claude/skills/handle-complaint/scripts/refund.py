"""How much can be refunded for an order: code computes it, not the model."""
import json
import pathlib
import sys

ORDERS = json.loads((pathlib.Path(__file__).resolve().parents[4] / "data" / "orders.json").read_text(encoding="utf-8"))
order_id, requested = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
order = ORDERS.get(order_id)
if not order:
    sys.exit(f"[MISSING] order {order_id} does not exist")
maximum = order["amount"] if order["status"] == "delivered" else 0.0
print(f"order {order_id}: {order['customer']}, value {order['amount']:.2f} PLN, status {order['status']}")
print(f"customer asks for: {requested:.2f} PLN, maximum refund: {maximum:.2f} PLN")
if requested > maximum:
    print(f"NEEDS DECISION: request above the maximum refund by {requested - maximum:.2f} PLN")
if order["status"] != "delivered":
    print("NEEDS DECISION: order in transit, refund only after delivery or return of the parcel")
