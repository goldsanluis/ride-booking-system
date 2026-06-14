"""
file_handler/file_manager.py
----------------------------
Handles reading and writing of bookings, favourite routes, and vehicle
status snapshots to JSON files in the data/ directory.

This module is the main persistence layer for the booking system —
all Booking objects are serialised to JSON here so that data survives
between application sessions.

author = "Ghani Regina Gold San Luis"
group  = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


from __future__ import annotations

import json
import logging
import os
import shutil
import tempfile
from datetime import datetime
from typing   import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from models.booking import Booking

# ── Logging ───────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Path Constants ────────────────────────────────────────────────────────────
# All paths are resolved relative to this file so the app works from any
# working directory.
_HERE          = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT  = os.path.dirname(_HERE)
DATA_DIR       = os.path.join(_PROJECT_ROOT, "data")

BOOKINGS_FILE        = os.path.join(DATA_DIR, "bookings.json")
FAVORITES_FILE       = os.path.join(DATA_DIR, "favorites.json")
VEHICLE_STATUS_FILE  = os.path.join(DATA_DIR, "vehicle_status.json")

# ── JSON Meta Watermark ───────────────────────────────────────────────────────
_META_RECORD: dict[str, Any] = {
    "_meta": {
        "author":  "Ghani Regina Gold San Luis",
        "group":   "Group 6",
        "course":  "CMPE 103 - Object Oriented Programming",
        "school":  "Polytechnic University of the Philippines",
        "github":  "https://github.com/your-username/ride-booking-system",
    }
}


# ── Helper: Atomic Write ──────────────────────────────────────────────────────

def _atomic_write(filepath: str, data: Any) -> None:
    """
    Write *data* to *filepath* atomically using a temp file + rename.
    This prevents corruption if the process is interrupted mid-write.

    Args:
        filepath (str): Destination JSON file path.
        data     (Any): JSON-serialisable object.

    Raises:
        OSError: If the file cannot be written or renamed.
    """
    dir_name = os.path.dirname(filepath)
    os.makedirs(dir_name, exist_ok=True)

    # Write to a temp file in the same directory so os.replace is atomic
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, filepath)          # Atomic on POSIX & Windows
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ── Helper: Safe JSON Load ────────────────────────────────────────────────────

def _safe_load(filepath: str, default: Any = None) -> Any:
    """
    Load JSON from *filepath*, returning *default* on any error.

    Handles:
        - File does not exist     → returns default
        - File is empty           → returns default
        - File contains bad JSON  → logs a warning, returns default

    Args:
        filepath (str): Path to the JSON file.
        default  (Any): Value returned when the file cannot be read.

    Returns:
        Any: Parsed JSON object or *default*.
    """
    if default is None:
        default = []
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except json.JSONDecodeError as exc:
        logger.warning(
            "Could not decode JSON from '%s': %s. Returning default.",
            filepath, exc,
        )
        return default
    except OSError as exc:
        logger.error("Could not read '%s': %s. Returning default.", filepath, exc)
        return default


# ── FileManager ───────────────────────────────────────────────────────────────

class FileManager:
    """
    Manages JSON persistence for:
        • Bookings           (bookings.json)
        • Favourite routes   (favorites.json)
        • Vehicle status     (vehicle_status.json)

    All write operations are atomic — a crash mid-write will not leave
    the file in a corrupt state.

    Usage
    ─────
        fm = FileManager()
        fm.save_bookings(my_bookings_list)
        raw = fm.load_bookings()          # list[dict]
    """

    def __init__(self, data_dir: str = DATA_DIR):
        """
        Initialise the FileManager and ensure the data directory exists.

        Args:
            data_dir (str): Path to the directory used for JSON files.
                            Defaults to the project-level data/ folder.
        """
        self.data_dir             = data_dir
        self.bookings_file        = os.path.join(data_dir, "bookings.json")
        self.favorites_file       = os.path.join(data_dir, "favorites.json")
        self.vehicle_status_file  = os.path.join(data_dir, "vehicle_status.json")

        os.makedirs(self.data_dir, exist_ok=True)

    # =========================================================================
    # ── Booking ID ────────────────────────────────────────────────────────────
    # =========================================================================

    def get_next_id(self) -> int:
        """
        Determine the next available booking ID.

        Reads all existing records and returns (max booking_id + 1).
        Returns 1 when no valid bookings exist yet.

        Returns:
            int: Next booking ID (always ≥ 1).
        """
        bookings = self.load_bookings()
        ids = [
            b["booking_id"]
            for b in bookings
            if isinstance(b, dict) and isinstance(b.get("booking_id"), int)
        ]
        return (max(ids) + 1) if ids else 1

    # =========================================================================
    # ── Bookings ──────────────────────────────────────────────────────────────
    # =========================================================================

    def load_bookings(self) -> list[dict]:
        """
        Read all booking records from bookings.json.

        Meta watermark records (those with a '_meta' key) are automatically
        filtered out so callers only receive real booking dictionaries.

        Returns:
            list[dict]: List of raw booking dictionaries.
                        Empty list if the file does not exist or cannot be read.
        """
        raw: list = _safe_load(self.bookings_file, default=[])
        # Filter out the meta watermark record
        return [
            record for record in raw
            if isinstance(record, dict) and "_meta" not in record
        ]

    def save_bookings(self, bookings: "list[Booking]") -> bool:
        """
        Serialise a list of Booking objects and persist them to bookings.json.

        The meta watermark is prepended automatically.

        Args:
            bookings (list[Booking]): All current in-memory Booking objects.

        Returns:
            bool: True on success, False if serialisation or I/O fails.
        """
        try:
            records: list[dict] = [_META_RECORD]
            for booking in bookings:
                records.append(self._booking_to_dict(booking))
            _atomic_write(self.bookings_file, records)
            logger.debug("Saved %d bookings to '%s'.", len(bookings), self.bookings_file)
            return True
        except (TypeError, AttributeError) as exc:
            logger.error("Failed to serialise bookings: %s", exc)
            return False
        except OSError as exc:
            logger.error("Failed to write '%s': %s", self.bookings_file, exc)
            return False

    def save_single_booking(self, booking: "Booking") -> bool:
        """
        Append or update a single booking in the JSON file without loading
        all other bookings into memory first.

        If a record with the same booking_id already exists it is replaced;
        otherwise the new record is appended.

        Args:
            booking (Booking): The booking to upsert.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            existing = self.load_bookings()
            new_dict = self._booking_to_dict(booking)

            # Replace existing record with the same ID, or append
            updated = False
            for i, record in enumerate(existing):
                if record.get("booking_id") == booking.booking_id:
                    existing[i] = new_dict
                    updated = True
                    break
            if not updated:
                existing.append(new_dict)

            _atomic_write(self.bookings_file, [_META_RECORD] + existing)
            return True
        except (OSError, TypeError, AttributeError) as exc:
            logger.error("Failed to save single booking #%s: %s", booking.booking_id, exc)
            return False

    def delete_booking(self, booking_id: int) -> bool:
        """
        Permanently remove a booking record by ID.

        Args:
            booking_id (int): The booking ID to delete.

        Returns:
            bool: True if a record was removed, False if not found or on error.
        """
        try:
            existing = self.load_bookings()
            filtered = [b for b in existing if b.get("booking_id") != booking_id]
            if len(filtered) == len(existing):
                logger.warning("Booking #%d not found; nothing deleted.", booking_id)
                return False
            _atomic_write(self.bookings_file, [_META_RECORD] + filtered)
            return True
        except OSError as exc:
            logger.error(
                "Failed to delete booking #%d from '%s': %s",
                booking_id, self.bookings_file, exc,
            )
            return False

    def get_bookings_by_user(self, username: str) -> list[dict]:
        """
        Return all booking records belonging to a specific user.

        Args:
            username (str): The passenger's username.

        Returns:
            list[dict]: Filtered list of raw booking dicts.
        """
        return [b for b in self.load_bookings() if b.get("user") == username]

    def get_bookings_by_status(self, status: str) -> list[dict]:
        """
        Return all booking records that match a given status.

        Args:
            status (str): e.g. 'Active', 'Scheduled', 'Completed', 'Cancelled'.

        Returns:
            list[dict]: Filtered list of raw booking dicts.
        """
        return [b for b in self.load_bookings() if b.get("status") == status]

    # ── Internal Serialisation Helper ─────────────────────────────────────────

    @staticmethod
    def _booking_to_dict(booking: "Booking") -> dict:
        """
        Convert a Booking object to a flat dictionary for JSON storage.

        Prefers calling booking.to_dict() if defined; otherwise builds the
        dict manually so this method degrades gracefully during development.

        Args:
            booking (Booking): The Booking object to serialise.

        Returns:
            dict: Flat dictionary matching the bookings.json schema.
        """
        if hasattr(booking, "to_dict") and callable(booking.to_dict):
            return booking.to_dict()

        # Manual fallback — mirrors the schema produced by Booking.to_dict()
        return {
            "booking_id":     booking.booking_id,
            "user":           booking.user,
            "vehicle_type":   booking.vehicle.name,
            "start_location": booking.start_location,
            "end_location":   booking.end_location,
            "distance":       booking.distance,
            "total_cost":     booking.total_cost,
            "date":           booking.date,
            "status":         booking.status,
            "surge":          booking.surge,
            "rating":         booking.rating,
            "passengers":     getattr(booking, "passengers",     1),
            "notes":          getattr(booking, "notes",          ""),
            "promo_code":     getattr(booking, "promo_code",     None),
            "discount":       getattr(booking, "discount",       0.0),
            "scheduled_time": getattr(booking, "scheduled_time", None),
            "payment_method": getattr(booking, "payment_method", "Cash"),
            "driver_name":    booking.driver.name,
            "driver_plate":   booking.driver.plate,
            "driver_rating":  booking.driver.rating,
            "driver_id":      booking.driver.driver_id,
        }

    # =========================================================================
    # ── Favourites (per-user saved routes) ────────────────────────────────────
    # =========================================================================

    def load_favorites(self, username: str) -> list[dict]:
        """
        Load the saved favourite routes for a specific user.

        Args:
            username (str): The logged-in passenger's username.

        Returns:
            list[dict]: List of route dicts.
                        Each dict has keys: name, start, end, distance, vehicle.
                        Empty list if the user has no saved favourites.
        """
        all_favs: dict = _safe_load(self.favorites_file, default={})
        return all_favs.get(username, [])

    def save_favorite(self, username: str, route: dict) -> tuple[bool, str]:
        """
        Save a new favourite route for the user, rejecting exact duplicates
        (matched on start + end location pair, case-insensitive).

        Args:
            username (str):  The passenger's username.
            route    (dict): Route info with keys: name, start, end, distance, vehicle.

        Returns:
            tuple[bool, str]: (True, success_msg) or (False, reason_msg).
        """
        required_keys = {"start", "end"}
        missing = required_keys - route.keys()
        if missing:
            return False, f"Route dict is missing required keys: {missing}."

        try:
            all_favs: dict = _safe_load(self.favorites_file, default={})
            user_favs: list = all_favs.get(username, [])

            # Reject if an identical start → end already exists (case-insensitive)
            start_lower = route["start"].strip().lower()
            end_lower   = route["end"].strip().lower()
            for existing in user_favs:
                if (
                    existing.get("start", "").strip().lower() == start_lower
                    and existing.get("end",   "").strip().lower() == end_lower
                ):
                    return False, "This route is already saved as a favourite."

            user_favs.append(route)
            all_favs[username] = user_favs
            _atomic_write(self.favorites_file, all_favs)
            return True, f"Route '{route.get('name', 'Untitled')}' saved to favourites."
        except OSError as exc:
            logger.error("Failed to save favourite for '%s': %s", username, exc)
            return False, f"Could not save favourite: {exc}"

    def delete_favorite(self, username: str, index: int) -> tuple[bool, str]:
        """
        Remove a saved favourite route by its zero-based list index.

        Args:
            username (str): The passenger's username.
            index    (int): Zero-based index of the route to remove.

        Returns:
            tuple[bool, str]: (True, success_msg) or (False, reason_msg).
        """
        try:
            all_favs: dict = _safe_load(self.favorites_file, default={})
            user_favs: list = all_favs.get(username, [])

            if not (0 <= index < len(user_favs)):
                return False, f"Index {index} is out of range (0–{len(user_favs) - 1})."

            removed = user_favs.pop(index)
            all_favs[username] = user_favs
            _atomic_write(self.favorites_file, all_favs)
            return True, f"Favourite '{removed.get('name', 'Untitled')}' removed."
        except OSError as exc:
            logger.error("Failed to delete favourite for '%s': %s", username, exc)
            return False, f"Could not delete favourite: {exc}"

    def clear_favorites(self, username: str) -> tuple[bool, str]:
        """
        Remove all favourite routes for a user.

        Args:
            username (str): The passenger's username.

        Returns:
            tuple[bool, str]: (True, success_msg) or (False, reason_msg).
        """
        try:
            all_favs: dict = _safe_load(self.favorites_file, default={})
            all_favs[username] = []
            _atomic_write(self.favorites_file, all_favs)
            return True, f"All favourites cleared for '{username}'."
        except OSError as exc:
            logger.error("Failed to clear favourites for '%s': %s", username, exc)
            return False, f"Could not clear favourites: {exc}"

    # =========================================================================
    # ── Vehicle Status Snapshot ───────────────────────────────────────────────
    # =========================================================================

    def save_vehicle_status(self, vehicles: list) -> bool:
        """
        Persist a snapshot of every vehicle's availability to vehicle_status.json.

        Each vehicle must have at least: vehicle_id, name, is_available.
        If the vehicle has a to_dict() method it is used; otherwise a minimal
        dict is built from the object's attributes.

        Args:
            vehicles (list): List of Vehicle (or subclass) instances.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            snapshot = {
                "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "vehicles": [],
            }
            for v in vehicles:
                if hasattr(v, "to_dict") and callable(v.to_dict):
                    snapshot["vehicles"].append(v.to_dict())
                else:
                    snapshot["vehicles"].append({
                        "vehicle_id":   getattr(v, "vehicle_id",   None),
                        "name":         getattr(v, "name",         "Unknown"),
                        "capacity":     getattr(v, "capacity",     0),
                        "cost_per_km":  getattr(v, "cost_per_km",  0.0),
                        "is_available": getattr(v, "is_available", True),
                    })
            _atomic_write(self.vehicle_status_file, snapshot)
            return True
        except (OSError, TypeError, AttributeError) as exc:
            logger.error("Failed to save vehicle status: %s", exc)
            return False

    def load_vehicle_status(self) -> dict:
        """
        Load the last-saved vehicle status snapshot.

        Returns:
            dict: Keys 'saved_at' (str) and 'vehicles' (list[dict]).
                  Returns {'saved_at': None, 'vehicles': []} if unavailable.
        """
        default = {"saved_at": None, "vehicles": []}
        data = _safe_load(self.vehicle_status_file, default=default)
        if not isinstance(data, dict):
            return default
        return data

    # =========================================================================
    # ── Backup Utility ────────────────────────────────────────────────────────
    # =========================================================================

    def backup(self, backup_dir: Optional[str] = None) -> tuple[bool, str]:
        """
        Copy all data JSON files to a timestamped backup directory.

        Args:
            backup_dir (str | None): Destination directory.
                                     Defaults to data/backups/<timestamp>/.

        Returns:
            tuple[bool, str]: (True, backup_path) or (False, error_message).
        """
        try:
            timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_dir = backup_dir or os.path.join(
                self.data_dir, "backups", timestamp
            )
            os.makedirs(target_dir, exist_ok=True)

            copied: list[str] = []
            for src in (
                self.bookings_file,
                self.favorites_file,
                self.vehicle_status_file,
            ):
                if os.path.exists(src):
                    dst = os.path.join(target_dir, os.path.basename(src))
                    shutil.copy2(src, dst)
                    copied.append(os.path.basename(src))

            msg = (
                f"Backup created at '{target_dir}' "
                f"({', '.join(copied) if copied else 'no files found'})."
            )
            logger.info(msg)
            return True, target_dir
        except OSError as exc:
            logger.error("Backup failed: %s", exc)
            return False, f"Backup failed: {exc}"

    # =========================================================================
    # ── Stats / Reporting ─────────────────────────────────────────────────────
    # =========================================================================

    def get_booking_stats(self) -> dict:
        """
        Compute aggregate statistics across all stored booking records.

        Returns:
            dict: Keys — total, by_status (dict), by_vehicle (dict),
                  total_revenue (float), average_fare (float).
        """
        bookings = self.load_bookings()
        if not bookings:
            return {
                "total":         0,
                "by_status":     {},
                "by_vehicle":    {},
                "total_revenue": 0.0,
                "average_fare":  0.0,
            }

        by_status:  dict[str, int]   = {}
        by_vehicle: dict[str, int]   = {}
        total_cost: float            = 0.0
        completed:  list[float]      = []

        for b in bookings:
            status  = b.get("status",       "Unknown")
            vehicle = b.get("vehicle_type", "Unknown")
            cost    = b.get("total_cost",   0.0)

            by_status[status]   = by_status.get(status, 0)   + 1
            by_vehicle[vehicle] = by_vehicle.get(vehicle, 0) + 1

            if status == "Completed":
                total_cost += cost
                completed.append(cost)

        return {
            "total":         len(bookings),
            "by_status":     by_status,
            "by_vehicle":    by_vehicle,
            "total_revenue": round(total_cost, 2),
            "average_fare":  round(total_cost / len(completed), 2) if completed else 0.0,
        }

    # ── Dunder ────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"FileManager(data_dir={self.data_dir!r})"