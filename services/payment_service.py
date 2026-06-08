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
    
    #-----Public methods------
    

   