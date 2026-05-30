"""
Multiple payment methods service.
Stores payment methods per user in data/payment_methods.json
"""
import json, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PM_FILE  = os.path.join(DATA_DIR, "payment_methods.json")

PAYMENT_ICONS = {
    "wallet":   "💳",
    "gcash":    "📱",
    "maya":     "💜",
    "card":     "💳",
    "cash":     "💵",
}


def _load() -> dict:
    if not os.path.exists(PM_FILE):
        return {}
    try:
        with open(PM_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PM_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_methods(username: str) -> list:
    """Return list of payment method dicts for this user."""
    data = _load()
    methods = data.get(username, [])
    # Wallet is always first and always present
    wallet_entry = {"type": "wallet", "label": "Ride Wallet", "default": True}
    has_wallet = any(m["type"] == "wallet" for m in methods)
    if not has_wallet:
        methods = [wallet_entry] + methods
    return methods


def add_method(username: str, mtype: str, label: str):
    """Add a new payment method. Returns (ok, msg)."""
    data = _load()
    methods = data.get(username, [])
    if any(m["type"] == mtype and m["label"] == label for m in methods):
        return False, "This payment method already exists."
    methods.append({"type": mtype, "label": label, "default": False})
    data[username] = methods
    _save(data)
    return True, f"{label} added successfully."


def remove_method(username: str, index: int):
    """Remove a payment method by index (cannot remove wallet)."""
    data = _load()
    methods = data.get(username, [])
    # Filter out wallet from indexing
    non_wallet = [m for m in methods if m["type"] != "wallet"]
    if 0 <= index < len(non_wallet):
        non_wallet.pop(index)
    data[username] = non_wallet
    _save(data)


def set_default(username: str, index: int):
    """Set method at index as default."""
    data  = _load()
    methods = data.get(username, [])
    for i, m in enumerate(methods):
        m["default"] = (i == index)
    data[username] = methods
    _save(data)


def get_default(username: str) -> dict:
    """Return the default payment method dict."""
    for m in get_methods(username):
        if m.get("default"):
            return m
    return {"type": "wallet", "label": "Ride Wallet"}
