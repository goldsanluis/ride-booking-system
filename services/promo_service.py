"""
services/promo_service.py
-------------------------
Manages promotional discount codes.

Built-in codes are defined directly in this file and are always available.
Admins can add or remove extra codes at runtime; these are persisted to
data/promos.json so they survive restarts.

Promo types:
    'flat'    — subtracts a fixed ₱ amount from the fare.
    'percent' — subtracts a percentage of the fare.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


import json
import os

DATA_DIR    = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROMOS_FILE = os.path.join(DATA_DIR, "promos.json")

VALID_TYPES = {"flat", "percent"}

# ── Built-in promo codes (always available, cannot be deleted)
# "vehicle type": None means the promo applies to all vehicle types
BUILTIN_PROMOS = {
    "RIDE10":   {"type": "flat",    "value": 10.0,  "min_fare": 50.0,  "desc": "₱10 off",               "uses": None, "vehicle_type": None  },
    "RIDE50":   {"type": "flat",    "value": 50.0,  "min_fare": 200.0, "desc": "₱50 off (min ₱200)",    "uses": None, "vehicle_type": None  },
    "SAVE20":   {"type": "percent", "value": 20.0,  "min_fare": 100.0, "desc": "20% off (min ₱100)",    "uses": None, "vehicle_type": None  },
    "NEWUSER":  {"type": "flat",    "value": 80.0,  "min_fare": 0.0,   "desc": "₱80 welcome discount",  "uses": None, "vehicle_type": None  },
    "VANRIDE":  {"type": "flat",    "value": 100.0, "min_fare": 300.0, "desc": "₱100 off Van rides",    "uses": None, "vehicle_type": None  },
    "PEAKHOUR": {"type": "percent", "value": 10.0,  "min_fare": 0.0,   "desc": "10% surge relief",      "uses": None, "vehicle_type": None  },
}


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load_extra_promos():
    """
    Load admin-created promo codes from disk.

    Returns:
        dict: Extra promos keyed by code string, or {} on missing/corrupt file.
    """
    if not os.path.exists(PROMOS_FILE):
        return {}
    try:
        with open(PROMOS_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_extra_promos(promos: dict):
    """
    Persist admin-created promos to data/promos.json.

    Args:
        promos (dict): The full set of extra promo codes to write.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROMOS_FILE, "w") as f:
        json.dump(promos, f, indent=2)


# ── Public API ────────────────────────────────────────────────────────────────

def get_all_promos() -> dict:
    """
    Return a merged dictionary of all available promo codes
    (built-in codes + any admin-added codes).
    Admin codes override built-ins if the code matches.

    Returns:
        dict: All promos keyed by uppercase code string.
    """
    merged = dict(BUILTIN_PROMOS)       # Start with built-ins
    merged.update(_load_extra_promos()) # Admin codes take precedence
    return merged


def add_promo(code: str, ptype: str, value: float,
              min_fare: float, desc: str, uses=None, vehicle_type: str=None) -> tuple:
    """
    Add or overwrite an admin-created promo code.
    Built-in codes will be shadowed if the same code is used.

    Args:
        code     (str):         Promo code string (stored in uppercase).
        ptype    (str):         'flat' or 'percent'.
        value    (float):       Discount amount or percentage.
        min_fare (float):       Minimum fare required to apply the code.
        desc     (str):         Human-readable description shown to users.
        uses     (int | None):  Max redemptions (None = unlimited).
        vehicle_type (str | None): The type of vehicle the promo applies to (None = all types).
        
    Return: tuple[bool, str]: (success, message)
    """
    if not code or not code.strip():
        return False, "Promo code cannot be empty."
    if ptype not in VALID_TYPES:
        return False, f"Invalid promo type '{ptype}'. Must be 'flat' or 'percent'."
    if value <= 0:
        return False, "Discount value must be greater than zero."
    if min_fare < 0:
        return False, "Minimum fare cannot be negative."
    if uses is not None and uses <= 0:
        return False, "Uses must be a positive number or None for unlimited."
 
    extra = _load_extra_promos()
    extra[code.strip().upper()] = {
        "type": ptype, "value": value,
        "min_fare": min_fare, "desc": desc,
        "uses": uses, "vehicle_type": vehicle_type,
    }
    _save_extra_promos(extra)
    return True, f"Promo '{code.strip().upper()}' saved."


def delete_promo(code: str) -> tuple:
    """
    Delete an admin-created promo code.
    Built-in codes cannot be deleted through this function.

    Args:
        code (str): The promo code to remove (case-insensitive).
        
    Returns: 
        tuple[bool, str]: (success, message)
    """
    code  = code.strip().upper()
    extra = _load_extra_promos()
    
    if code not in extra:
        if code in BUILTIN_PROMOS:
            return False, f"'{code}' is a built-in promo and cannot be deleted."
        return False, f"'{code}' does not exist."
 
    del extra[code]
    _save_extra_promos(extra)
    return True, f"'{code}' deleted."


def apply_promo(code: str, base_fare: float):
    """
    Validate and calculate the discount for a promo code.

    Args:
        code      (str):   The promo code entered by the passenger.
        base_fare (float): The fare before any discount is applied.

    Returns:
        tuple[float, str, str | None]:
            - discount_amount (float): ₱ amount to subtract (0.0 on failure).
            - description     (str):   Human-readable promo description.
            - error_message   (str | None): None on success, error text on failure.
    """
    code  = code.strip().upper()

    if not code:
        return 0.0, "", "No promo code entered."

    promo = get_all_promos().get(code)
    if not promo:
        return 0.0, "", f"'{code}' is not a valid promo code."

    # Check minimum fare requirement
    if base_fare < promo["min_fare"]:
        return 0.0, "", (
            f"Minimum fare for {code} is ₱{promo['min_fare']:.2f}. "
            f"Your fare is ₱{base_fare:.2f}."
        )

    # Calculate discount based on promo type
    if promo["type"] == "flat":
        discount = min(promo["value"], base_fare)  # Cannot discount more than the fare
    else:  # percent
        discount = round(base_fare * promo["value"] / 100, 2)

    return discount, promo["desc"], None


def list_promos():
    """
    Build a human-readable summary of all available promo codes.
    Used to display the promo list inside the booking form.

    Returns:
        str: Multi-line string with one promo per line.
    """
    lines = []
    for code, info in get_all_promos().items():
        min_text  = f"  (min ₱{info['min_fare']:.0f})" if info["min_fare"] > 0 else ""
        uses_text = f"  [{info['uses']} uses left]"     if info.get("uses")   else ""
        lines.append(f"  {code:<12} — {info['desc']}{min_text}{uses_text}")
    return "\n".join(lines)
