"""
Promo/discount code service.
Codes are defined here; extend as needed or load from a JSON file.
"""

PROMO_CODES = {
    "RIDE10":   {"type": "flat",    "value": 10.0,  "min_fare": 50.0,   "desc": "₱10 off"},
    "RIDE50":   {"type": "flat",    "value": 50.0,  "min_fare": 200.0,  "desc": "₱50 off (min ₱200)"},
    "SAVE20":   {"type": "percent", "value": 20.0,  "min_fare": 100.0,  "desc": "20% off (min ₱100)"},
    "NEWUSER":  {"type": "flat",    "value": 80.0,  "min_fare": 0.0,    "desc": "₱80 welcome discount"},
    "VANRIDE":  {"type": "flat",    "value": 100.0, "min_fare": 300.0,  "desc": "₱100 off Van rides"},
    "PEAKHOUR": {"type": "percent", "value": 10.0,  "min_fare": 0.0,    "desc": "10% surge relief"},
}


def apply_promo(code: str, base_fare: float):
    """
    Returns (discount_amount, description, error_message).
    discount_amount is 0.0 on failure; error_message is None on success.
    """
    code = code.strip().upper()
    if not code:
        return 0.0, "", "No promo code entered."

    promo = PROMO_CODES.get(code)
    if not promo:
        return 0.0, "", f"'{code}' is not a valid promo code."

    if base_fare < promo["min_fare"]:
        return 0.0, "", (f"Minimum fare for {code} is ₱{promo['min_fare']:.2f}. "
                         f"Your fare is ₱{base_fare:.2f}.")

    if promo["type"] == "flat":
        discount = min(promo["value"], base_fare)
    else:  # percent
        discount = round(base_fare * promo["value"] / 100, 2)

    return discount, promo["desc"], None


def list_promos():
    """Return a human-readable list of all available promos."""
    lines = []
    for code, info in PROMO_CODES.items():
        min_text = f"  (min ₱{info['min_fare']:.0f})" if info["min_fare"] > 0 else ""
        lines.append(f"  {code:<10} — {info['desc']}{min_text}")
    return "\n".join(lines)
