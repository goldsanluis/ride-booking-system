"""
Promo/discount code service.
Codes are defined here; extend as needed or load from a JSON file.
"""
import json, os

DATA_DIR   = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROMOS_FILE = os.path.join(DATA_DIR, "promos.json")

# Built-in codes (always available)
BUILTIN_PROMOS = {
    "RIDE10":   {"type": "flat",    "value": 10.0,  "min_fare": 50.0,   "desc": "₱10 off",                "uses": None},
    "RIDE50":   {"type": "flat",    "value": 50.0,  "min_fare": 200.0,  "desc": "₱50 off (min ₱200)",     "uses": None},
    "SAVE20":   {"type": "percent", "value": 20.0,  "min_fare": 100.0,  "desc": "20% off (min ₱100)",     "uses": None},
    "NEWUSER":  {"type": "flat",    "value": 80.0,  "min_fare": 0.0,    "desc": "₱80 welcome discount",   "uses": None},
    "VANRIDE":  {"type": "flat",    "value": 100.0, "min_fare": 300.0,  "desc": "₱100 off Van rides",     "uses": None},
    "PEAKHOUR": {"type": "percent", "value": 10.0,  "min_fare": 0.0,    "desc": "10% surge relief",       "uses": None},
}


def _load_extra_promos():
    if not os.path.exists(PROMOS_FILE):
        return {}
    try:
        with open(PROMOS_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_extra_promos(promos: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROMOS_FILE, "w") as f:
        json.dump(promos, f, indent=2)


def get_all_promos() -> dict:
    """Return merged dict of built-in + admin-added promos."""
    merged = dict(BUILTIN_PROMOS)
    merged.update(_load_extra_promos())
    return merged


def add_promo(code: str, ptype: str, value: float, min_fare: float, desc: str, uses=None):
    """Add or overwrite a promo (admin-only). ptype = 'flat' | 'percent'."""
    extra = _load_extra_promos()
    extra[code.upper()] = {"type": ptype, "value": value, "min_fare": min_fare,
                            "desc": desc, "uses": uses}
    _save_extra_promos(extra)


def delete_promo(code: str):
    """Delete an admin-added promo (cannot delete built-ins)."""
    extra = _load_extra_promos()
    extra.pop(code.upper(), None)
    _save_extra_promos(extra)


def apply_promo(code: str, base_fare: float):
    """
    Returns (discount_amount, description, error_message).
    discount_amount is 0.0 on failure; error_message is None on success.
    """
    code  = code.strip().upper()
    if not code:
        return 0.0, "", "No promo code entered."
    promo = get_all_promos().get(code)
    if not promo:
        return 0.0, "", f"'{code}' is not a valid promo code."
    if base_fare < promo["min_fare"]:
        return 0.0, "", (f"Minimum fare for {code} is ₱{promo['min_fare']:.2f}. "
                         f"Your fare is ₱{base_fare:.2f}.")
    if promo["type"] == "flat":
        discount = min(promo["value"], base_fare)
    else:
        discount = round(base_fare * promo["value"] / 100, 2)
    return discount, promo["desc"], None


def list_promos():
    """Return a human-readable list of all available promos."""
    lines = []
    for code, info in get_all_promos().items():
        min_text = f"  (min ₱{info['min_fare']:.0f})" if info["min_fare"] > 0 else ""
        uses_txt = f"  [{info['uses']} uses left]" if info.get("uses") else ""
        lines.append(f"  {code:<12} — {info['desc']}{min_text}{uses_txt}")
    return "\n".join(lines)
