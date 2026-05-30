import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")
FAVORITES_FILE = os.path.join(DATA_DIR, "favorites.json")

class FileManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

    def get_next_id(self):
        bookings = self.load_bookings()
        if not bookings:
            return 1
        return max(b["booking_id"] for b in bookings) + 1

    def load_bookings(self):
        if not os.path.exists(BOOKINGS_FILE):
            return []
        with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_bookings(self, bookings):
        data = []
        for b in bookings:
            data.append({
                "booking_id": b.booking_id,
                "user": b.user,
                "vehicle_type": b.vehicle.name,
                "start_location": b.start_location,
                "end_location": b.end_location,
                "distance": b.distance,
                "total_cost": b.total_cost,
                "date": b.date,
                "status": b.status,
                "surge": b.surge,
                "rating": b.rating,
                "passengers": getattr(b, "passengers", 1),
                "notes": getattr(b, "notes", ""),
                "promo_code": getattr(b, "promo_code", None),
                "discount": getattr(b, "discount", 0.0),
                "scheduled_time": getattr(b, "scheduled_time", None),
                "driver_name": b.driver.name,
                "driver_plate": b.driver.plate,
                "driver_rating": b.driver.rating,
                "driver_id": b.driver.driver_id,
            })
        with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ── Favorites (per-user saved routes) ─────────────────────────────────────
    def load_favorites(self, username):
        if not os.path.exists(FAVORITES_FILE):
            return []
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            all_favs = json.load(f)
        return all_favs.get(username, [])

    def save_favorite(self, username, route: dict):
        """route = {name, start, end, distance, vehicle}"""
        if not os.path.exists(FAVORITES_FILE):
            all_favs = {}
        else:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                all_favs = json.load(f)
        user_favs = all_favs.get(username, [])
        # Avoid exact duplicates by start+end
        for existing in user_favs:
            if existing["start"] == route["start"] and existing["end"] == route["end"]:
                return False  # already saved
        user_favs.append(route)
        all_favs[username] = user_favs
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(all_favs, f, indent=2, ensure_ascii=False)
        return True

    def delete_favorite(self, username, index):
        if not os.path.exists(FAVORITES_FILE):
            return
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            all_favs = json.load(f)
        user_favs = all_favs.get(username, [])
        if 0 <= index < len(user_favs):
            user_favs.pop(index)
        all_favs[username] = user_favs
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(all_favs, f, indent=2, ensure_ascii=False)
