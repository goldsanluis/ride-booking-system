"""
file_handler/file_manager.py
----------------------------
Handles reading and writing of bookings and per-user favourite routes
to JSON files in the data/ directory.

This module is the main persistence layer for the booking system —
all booking objects are serialised to JSON here so that data
survives between application sessions.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


import json
import os

# Resolve data directory relative to this file's location
# so the app works regardless of the working directory
DATA_DIR      = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")
FAVORITES_FILE = os.path.join(DATA_DIR, "favorites.json")


class FileManager:
    """
    Manages JSON persistence for bookings and favourite routes.

    Responsibilities:
        - Loading and saving all Booking objects to bookings.json.
        - Managing per-user saved routes in favorites.json.
        - Generating the next available booking ID.
    """

    def __init__(self):
        # Ensure the data directory exists when the manager is created
        os.makedirs(DATA_DIR, exist_ok=True)

    # ── Booking ID ────────────────────────────────────────────────────────────

    def get_next_id(self):
        """
        Determine the next booking ID by finding the current maximum
        and adding 1. Returns 1 if there are no existing bookings.

        Returns:
            int: Next available booking ID.
        """
        bookings = self.load_bookings()
        if not bookings:
            return 1
        return max(b["booking_id"] for b in bookings) + 1

    # ── Bookings ──────────────────────────────────────────────────────────────

    def load_bookings(self):
        """
        Read all bookings from the JSON file.

        Returns:
            list[dict]: List of raw booking dictionaries,
                        or an empty list if the file doesn't exist.
        """
        if not os.path.exists(BOOKINGS_FILE):
            return []
        with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_bookings(self, bookings):
        """
        Serialise a list of Booking objects to JSON and write to disk.
        Called automatically after every booking, cancellation, or update.

        Args:
            bookings (list[Booking]): All current Booking objects to persist.
        """
        data = []
        for b in bookings:
            # Flatten the Booking object into a plain dictionary
            data.append({
                "booking_id":    b.booking_id,
                "user":          b.user,
                "vehicle_type":  b.vehicle.name,
                "start_location": b.start_location,
                "end_location":  b.end_location,
                "distance":      b.distance,
                "total_cost":    b.total_cost,
                "date":          b.date,
                "status":        b.status,
                "surge":         b.surge,
                "rating":        b.rating,
                # Use getattr with defaults so older records without these
                # fields don't raise AttributeError
                "passengers":    getattr(b, "passengers",  1),
                "notes":         getattr(b, "notes",       ""),
                "promo_code":    getattr(b, "promo_code",  None),
                "discount":      getattr(b, "discount",    0.0),
                "scheduled_time": getattr(b, "scheduled_time", None),
                # Driver details are stored flat (no nested object)
                "driver_name":   b.driver.name,
                "driver_plate":  b.driver.plate,
                "driver_rating": b.driver.rating,
                "driver_id":     b.driver.driver_id,
            })

        # Hidden meta watermark (stored as a special first record in the list)
        # to avoid breaking backward compatibility with existing JSON schema.
        data.insert(0, {
            "_meta": {
                "author": "Ghani Regina Gold San Luis",
                "group": "Group 6",
                "course": "CMPE 103 - Object Oriented Programming",
                "school": "Polytechnic University of the Philippines",
                "github": "https://github.com/your-username/ride-booking-system"
            }
        })

        with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


    # ── Favourites (per-user saved routes) ────────────────────────────────────

    def load_favorites(self, username):
        """
        Load the saved favourite routes for a specific user.

        Args:
            username (str): The logged-in passenger's username.

        Returns:
            list[dict]: List of route dicts, each with keys:
                        name, start, end, distance, vehicle.
        """
        if not os.path.exists(FAVORITES_FILE):
            return []
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            all_favs = json.load(f)
        return all_favs.get(username, [])

    def save_favorite(self, username, route: dict):
        """
        Save a new favourite route for the user, avoiding exact duplicates
        (matched on start + end location pair).

        Args:
            username (str):  The passenger's username.
            route    (dict): Route info: {name, start, end, distance, vehicle}.

        Returns:
            bool: True if saved successfully, False if a duplicate was found.
        """
        # Load the full favourites file to preserve other users' data
        if not os.path.exists(FAVORITES_FILE):
            all_favs = {}
        else:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                all_favs = json.load(f)

        user_favs = all_favs.get(username, [])

        # Reject if this exact start→end route already exists
        for existing in user_favs:
            if existing["start"] == route["start"] and existing["end"] == route["end"]:
                return False

        user_favs.append(route)
        all_favs[username] = user_favs

        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(all_favs, f, indent=2, ensure_ascii=False)
        return True

    def delete_favorite(self, username, index):
        """
        Remove a saved favourite route by its list index.

        Args:
            username (str): The passenger's username.
            index    (int): Zero-based index of the route to remove.
        """
        if not os.path.exists(FAVORITES_FILE):
            return

        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            all_favs = json.load(f)

        user_favs = all_favs.get(username, [])

        # Only remove if index is within bounds
        if 0 <= index < len(user_favs):
            user_favs.pop(index)

        all_favs[username] = user_favs

        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(all_favs, f, indent=2, ensure_ascii=False)
