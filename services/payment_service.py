"""
Multiple payment methods service.
Stores payment methods per user in data/payment_methods.json

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import json, os

class PaymentMethodService:
    PAYMENT_ICONS = {
        "wallet":   "💳",
        "gcash":    "📱",
        "maya":     "💜",
        "card":     "💳",
        "cash":     "💵",
}
    def __init__(self, storage_path: str = None):
            if storage_path is None:
                base_dir = os.path.dirname(os.path.dirname(__file__))
                self.storage_path = os.path.join(base_dir, "data", "payment_methods.json")
            else:
                self.storage_path = storage_path
    
    #-----Private helpers------
    def _load(self) -> dict:
        if not os.path.exists(self.storage_path):
            return {}
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # File exists but is corrupted; return empty dict (or handle error)
            return {}

    def _save(self, data: dict):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def _ensure_wallet(self, methods: list) -> list:
        """Ensures the wallet is always present at index 0."""
        has_wallet = any(m["type"] == "wallet" for m in methods)
        if not has_wallet:
            methods.insert(0, {"type": "wallet", "label": "Ride Wallet", "default": True})
        return methods
    
    #-----Public API------
    def get_methods(self, username: str) -> list:
        data = self._load()
        methods = data.get(username, [])
        return self._ensure_wallet(methods)

    def add_method(self, username: str, mtype: str, label: str) -> tuple:
        if mtype not in self.PAYMENT_ICONS:
            return False, f"Invalid payment type. Allowed: {', '.join(self.PAYMENT_ICONS.keys())}"

        data = self._load()
        methods = self._ensure_wallet(data.get(username, []))

        if any(m["type"] == mtype and m["label"] == label for m in methods):
            return False, "This payment method already exists."

        methods.append({"type": mtype, "label": label, "default": False})
        data[username] = methods
        self._save(data)
        return True, f"{label} added successfully."

    def remove_method(self, username: str, index: int) -> tuple:
        data = self._load()
        methods = self._ensure_wallet(data.get(username, []))

        if index == 0 or methods[index].get("type") == "wallet":
            return False, "Cannot remove the default Ride Wallet."
            
        if 0 <= index < len(methods):
            removed = methods.pop(index)
            # If the removed method was the default, fallback to wallet
            if removed.get("default"):
                methods[0]["default"] = True
            
            data[username] = methods
            self._save(data)
            return True, "Payment method removed."
            
        return False, "Invalid index."

    def set_default(self, username: str, index: int) -> tuple:
        data = self._load()
        methods = self._ensure_wallet(data.get(username, []))

        if not (0 <= index < len(methods)):
            return False, "Invalid index."

        for i, m in enumerate(methods):
            m["default"] = (i == index)
            
        data[username] = methods
        self._save(data)
        return True, "Default payment method updated."

    def get_default(self, username: str) -> dict:
        methods = self.get_methods(username)
        for m in methods:
            if m.get("default"):
                return m
        return methods[0] # Fallback to wallet

   