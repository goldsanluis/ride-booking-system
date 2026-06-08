"""
services/booking_service.py
----------------------------
Business logic layer for all booking-related operations.
Acts as the bridge between the GUI and the persistence layer (FileManager).

All booking state lives here in memory during a session;
FileManager handles saving to and loading from disk.
"""

from models.booking import Booking
from models.car     import Car
from models.van     import Van
from models.bike    import Bike
from models.driver  import Driver


class BookingService:
    """
    Central service for creating, retrieving, and modifying bookings.

    Attributes:
        file_manager (FileManager): Handles JSON read/write for bookings.
        bookings     (list[Booking]): In-memory list of all bookings.
        next_id      (int): Next available booking ID.
    """

    VEHICLE_CLASSES = {
        "Car":  Car,
        "Van":  Van,
        "Bike": Bike,
    }

    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.bookings     = []
        self.next_id      = self.file_manager.get_next_id()
        self.load_bookings()  # Restore saved bookings at startup

    # ── Vehicle Factory ───────────────────────────────────────────────────────

    def get_vehicle(self, vehicle_type):
        """
        Instantiate the correct Vehicle subclass for the given type string.
        This is a simple factory pattern.

        Args:
            vehicle_type (str): 'Car', 'Van', or 'Bike'.

        Returns:
            Vehicle | None: A new vehicle instance, or None for unknown types.
        """
        cls = self.VEHICLE_CLASSES.get(vehicle_type)
        return cls(self.next_id) if cls else None

    # ── Persistence ───────────────────────────────────────────────────────────

    def load_bookings(self):
        """
        Deserialise bookings from the JSON file into Booking objects
        and populate the in-memory bookings list.
        Skips any records with unrecognised vehicle types.
        """
        data = self.file_manager.load_bookings()
        for item in data:
            # Skip hidden meta watermark record
            if isinstance(item, dict) and item.get("_meta") is not None:
                continue

            vehicle = self.get_vehicle(item["vehicle_type"])
            if not vehicle:
                continue  # Skip corrupted / unknown vehicle records

            booking = Booking(
                item["booking_id"],
                item["user"],
                vehicle,
                item["start_location"],
                item["end_location"],
                item["distance"],
                passengers    = item.get("passengers",    1),
                notes         = item.get("notes",         ""),
                promo_code    = item.get("promo_code",    None),
                discount      = item.get("discount",      0.0),
                scheduled_time= item.get("scheduled_time",None),
            )

            # Restore saved values that would otherwise be recalculated
            booking.total_cost = item["total_cost"]
            booking.date       = item["date"]
            booking.status     = item["status"]
            booking.surge      = item.get("surge",  1.0)
            booking.rating     = item.get("rating", None)

            booking.driver = Driver(
                item.get("driver_name",   "Unknown"),
                item.get("driver_plate",  "Unknown"),
                item.get("driver_rating", 0.0),
                driver_id=item.get("driver_id")
            )

            self.bookings.append(booking)

    # ── Booking Operations ────────────────────────────────────────────────────

    def book_ride(self, user, vehicle_type, start_location, end_location, distance,
                  passengers=1, notes="", promo_code=None, discount=0.0,
                  scheduled_time=None):
        """
        Create a new booking, add it to the in-memory list, and persist it.

        Args:
            user           (str):         Passenger's username.
            vehicle_type   (str):         'Car', 'Van', or 'Bike'.
            start_location (str):         Pick-up location name.
            end_location   (str):         Drop-off location name.
            distance       (float):       Trip distance in km.
            passengers     (int):         Number of passengers.
            notes          (str):         Optional driver instructions.
            promo_code     (str | None):  Applied promo code.
            discount       (float):       Discount amount in ₱.
            scheduled_time (str | None):  Future ride datetime string.

        Raises:
            ValueError: If vehicle_type is not recognised.

        Returns:
            Booking: The newly created Booking object.
        """
        vehicle = self.get_vehicle(vehicle_type)
        if not vehicle:
            raise ValueError(f"Invalid vehicle type: '{vehicle_type}'. "
                             f"Choose from: {', '.join(self.VEHICLE_CLASSES)}.")

        booking = Booking(
            self.next_id, user, vehicle,
            start_location, end_location, distance,
            passengers    = passengers,
            notes         = notes,
            promo_code    = promo_code,
            discount      = discount,
            scheduled_time= scheduled_time,
        )

        self.bookings.append(booking)
        self.next_id += 1
        self.save_bookings()  # Persist immediately so data survives a restart
        return booking

    def get_all_bookings(self):
        """Return every booking in the system (admin use)."""
        return self.bookings

    def get_user_bookings(self, username):
        """
        Return only the bookings that belong to a specific passenger.

        Args:
            username (str): Passenger's username.

        Returns:
            list[Booking]: Filtered list of bookings.
        """
        return [b for b in self.bookings if b.user == username]

    def get_booking_count(self, username):
        """
        Return the total number of bookings for a passenger.

        Args:
            username (str): Passenger's username.

        Returns:
            int: Total booking count.
        """
        return len(self.get_user_bookings(username))

    def get_total_spent(self, username):
        """
        Return the total amount spent on completed rides.

        Args:
            username (str): Passenger's username.

        Returns:
            float: Sum of total_cost for all completed bookings.
        """
        return sum(
            b.total_cost for b in self.get_user_bookings(username)
            if b.status == "Completed"
        )

    def cancel_booking(self, booking_id, username, refund_policy=100):
        """
        Cancel a booking and return the fare as a refund amount.
        Only the passenger who made the booking can cancel it.

        Args:
            booking_id    (int):   ID of the booking to cancel.
            username      (str):   Username of the requesting passenger.
            refund_policy (float): Percentage of booking.total_cost to refund.

        Returns:
            tuple[str, float]: (message, refund_amount).
                               refund_amount is 0.0 on failure.
        """
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.user != username:
                    return "You can only cancel your own bookings!", 0.0

                try:
                    refund_pct = float(refund_policy)
                except (TypeError, ValueError):
                    refund_pct = 100.0

                refund = booking.total_cost * refund_pct / 100.0
                booking.cancel()
                self.save_bookings()
                return (f"Booking #{booking_id} cancelled. "
                        f"₱{refund:.2f} refund computed ({refund_pct:.0f}%)."), refund
        return "Booking not found!", 0.0

    def complete_booking(self, booking_id, username):
        """
        Mark a booking as completed.

        Args:
            booking_id (int): ID of the booking to complete.
            username   (str): Username of the requesting passenger.

        Returns:
            str: Success or error message.
        """
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.user != username:
                    return "You can only complete your own bookings!"
                booking.complete()
                self.save_bookings()
                return f"Booking #{booking_id} completed!"
        return "Booking not found!"

    def rate_booking(self, booking_id, username, rating):
        """
        Attach a star rating to a completed booking.
        Only completed bookings can be rated.

        Args:
            booking_id (int): ID of the booking to rate.
            username   (str): Must match the booking's owner.
            rating     (int): Star rating 1-5.

        Returns:
            str: Success or error message.
        """
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.user != username:
                    return "You can only rate your own bookings!"
                if booking.status != "Completed":
                    return "You can only rate completed bookings!"
                result = booking.add_rating(rating)
                self.save_bookings()
                return result
        return "Booking not found!"

    def get_active_bookings(self):
        """Return all bookings currently in 'Active' status."""
        return [b for b in self.bookings if b.status == "Active"]

    def save_bookings(self):
        """Persist all in-memory bookings via the underlying FileManager."""
        self.file_manager.save_bookings(self.bookings)

    def activate_booking(self, booking_id, username):
        """Activate a scheduled booking for a specific user."""
        booking = self.find_booking_by_id(booking_id)
        if not booking:
            return "Booking not found."
        if booking.user != username:
            return "You can only activate your own bookings."
        if booking.status != "Scheduled":
            return f"Booking is not Scheduled (current status: {booking.status})."
        booking.activate()
        self.save_bookings()
        return f"Booking #{booking_id} is now Active!"

    def find_booking_by_id(self, booking_id):
        """
        Look up a single booking by its numeric ID.

        Args:
            booking_id (int): The booking ID to search for.

        Returns:
            Booking | None: The matching Booking, or None if not found.
        """
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None

    def search_user_bookings(self, username, keyword):
        """
        Filter a passenger's bookings by a keyword that matches
        the start location, end location, or notes fields.

        Args:
            username (str): Passenger's username.
            keyword  (str): Search term (case-insensitive).

        Returns:
            list[Booking]: Matching bookings.
        """
        keyword = keyword.lower()
        return [
            b for b in self.get_user_bookings(username)
            if keyword in b.start_location.lower()
            or keyword in b.end_location.lower()
            or keyword in (b.notes or "").lower()
        ]

    # ── Stats ─────────────────────────────────────────────────────────────────

    def get_user_stats(self, username):
        """
        Compute a summary of a passenger's booking history.

        Args:
            username (str): Passenger's username.

        Returns:
            dict: Keys: total_bookings, completed, cancelled, active,
                  total_spent, avg_fare, total_distance, by_vehicle,
                  avg_rating_given.
        """
        bookings  = self.get_user_bookings(username)
        completed = [b for b in bookings if b.status == "Completed"]

        total_spent = sum(b.total_cost for b in completed)

        by_vehicle = {}
        for b in completed:
            vname = b.vehicle.name
            by_vehicle[vname] = by_vehicle.get(vname, 0.0) + b.total_cost

        avg_fare       = total_spent / len(completed) if completed else 0.0
        total_distance = sum(b.distance for b in completed)
        ratings_given  = [b.rating for b in completed if b.rating]
        avg_rating     = sum(ratings_given) / len(ratings_given) if ratings_given else None

        return {
            "total_bookings":   len(bookings),
            "completed":        len(completed),
            "cancelled":        len([b for b in bookings if b.status == "Cancelled"]),
            "active":           len([b for b in bookings if b.status in ("Active", "Scheduled")]),
            "total_spent":      total_spent,
            "avg_fare":         avg_fare,
            "total_distance":   total_distance,
            "by_vehicle":       by_vehicle,
            "avg_rating_given": avg_rating,
        }