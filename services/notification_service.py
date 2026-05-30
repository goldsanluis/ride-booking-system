"""
Enhanced notification service with categories, persistence, and push-style toasts.
"""
import json, os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
NF_FILE  = os.path.join(DATA_DIR, "notifications.json")

CATEGORIES = {
    "ride":    "🚗",
    "payment": "💰",
    "promo":   "🎟️",
    "system":  "🔔",
    "driver":  "🚕",
    "refund":  "↩️",
}


def _load() -> list:
    if not os.path.exists(NF_FILE):
        return []
    try:
        with open(NF_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def _save(notifs: list):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(NF_FILE, "w") as f:
        json.dump(notifs, f, indent=2)


def push(user: str, message: str, category: str = "system", booking_id=None):
    """Add a notification for `user`."""
    notifs = _load()
    notifs.append({
        "user":       user,
        "message":    message,
        "category":   category,
        "booking_id": booking_id,
        "seen":       False,
        "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    _save(notifs)


def get_for_user(username: str) -> list:
    return [n for n in _load() if n.get("user") == username]


def get_unread_count(username: str) -> int:
    return sum(1 for n in get_for_user(username) if not n.get("seen"))


def mark_all_seen(username: str):
    notifs = _load()
    for n in notifs:
        if n.get("user") == username:
            n["seen"] = True
    _save(notifs)


def delete_notification(username: str, index: int):
    notifs = _load()
    mine = [(i, n) for i, n in enumerate(notifs) if n.get("user") == username]
    if 0 <= index < len(mine):
        notifs.pop(mine[index][0])
    _save(notifs)


def clear_all(username: str):
    notifs = [n for n in _load() if n.get("user") != username]
    _save(notifs)


def broadcast(message: str, category: str = "system"):
    """Send a notification to ALL users (admin use)."""
    from file_handler.account_manager import AccountManager
    try:
        accounts = AccountManager().load_accounts()
        for acc in accounts:
            push(acc["username"], message, category)
    except Exception:
        pass
