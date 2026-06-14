"""
models/booking.py
-----------------
Represents a single ride booking made by a passenger.
Handles fare calculation (including surge and promos), vehicle assignment,
status transitions, ratings, and serialisation.

author = "Ghani Regina Gold San Luis"
group  = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


from __future__ import annotations

from datetime import datetime
from typing   import Optional, TYPE_CHECKING

from models.driver import Driver

if TYPE_CHECKING:
    # Only imported for type hints; avoids circular imports at runtime
    from models.vehicle import Vehicle


# ── Valid Status Values ───────────────────────────────────────────────────────

VALID_STATUSES = {"Active", "Scheduled", "Completed", "Cancelled"}

# ── Surge Pricing Windows (24-hour clock) ─────────────────────────────────────
# Each entry is a (start_hour_inclusive, end_hour_inclusive) tuple.
PEAK_WINDOWS = [
    (7,  9),   # Morning rush
    (17, 20),  # Evening rush
]


class Booking:
    """
    A ride booking linking a passenger, a vehicle, and a route.

    Fare Calculation Pipeline
    ─────────────────────────
    1. vehicle.calculate_cost(distance)          →  base_vehicle_fare
    2. base_vehicle_fare × surge_multiplier      →  surged_fare
    3. surged_fare − promo_discount              →  final total_cost  (≥ ₱0)

    Status Lifecycle
    ────────────────
    New booking  →  'Active'    (immediate ride)
                 →  'Scheduled' (future ride)
    Active       →  'Completed' via complete()
    Scheduled    →  'Active'    via activate()
    Any          →  'Cancelled' via cancel()

    Attributes
    ──────────
    booking_id      int             Unique booking identifier.
    user            str             Username of the passenger.
    vehicle         Vehicle         Assigned vehicle instance (Car, Van, Bike…).
    start_location  str             Pick-up point.
    end_location    str             Drop-off point.
    distance        float           Trip distance in kilometres.
    passengers      int             Head count (validated against vehicle capacity).
    notes           str             Optional driver instructions.
    promo_code      str | None      Applied promo code label.
    discount        float           Discount amount in ₱ (from promo).
    scheduled_time  str | None      ISO-format datetime string for future rides.
    date            str             Timestamp when this booking was created.
    status          str             Current lifecycle status.
    driver          Driver          Assigned driver (placeholder until confirmed).
    rating          int | None      Passenger's 1–5 star rating post-ride.
    surge           float           Surge multiplier in effect (1.0 or 1.5).
    total_cost      float           Final fare after surge and discount.
    payment_method  str             How the ride will be paid ('Cash', 'Wallet', …).
    """

    # ── Constructor ───────────────────────────────────────────────────────────

    def __init__(
        self,
        booking_id:     int,
        user:           str,
        vehicle:        "Vehicle",
        start_location: str,
        end_location:   str,
        distance:       float,
        passengers:     int            = 1,
        notes:          str            = "",
        promo_code:     Optional[str]  = None,
        discount:       float          = 0.0,
        scheduled_time: Optional[str]  = None,
        payment_method: str            = "Cash",
    ):
        """
        Create a new Booking and immediately compute the fare.

        Args:
            booking_id      (int):         Unique booking identifier.
            user            (str):         Passenger's username.
            vehicle         (Vehicle):     Instantiated vehicle (Car / Van / Bike).
            start_location  (str):         Pick-up location name.
            end_location    (str):         Drop-off location name.
            distance        (float):       Trip distance in km (must be ≥ 0).
            passengers      (int):         Number of passengers (default 1).
            notes           (str):         Optional driver instructions.
            promo_code      (str | None):  Promo label, e.g. 'SUMMER20'.
            discount        (float):       Flat ₱ discount from promo (default 0).
            scheduled_time  (str | None):  ISO datetime string; None = ride now.
            payment_method  (str):         Payment method label (default 'Cash').

        Raises:
            ValueError: If distance < 0 or passengers < 1.
        """
        if distance < 0:
            raise ValueError(f"Booking distance must be ≥ 0; got {distance}.")
        if passengers < 1:
            raise ValueError(f"Passenger count must be ≥ 1; got {passengers}.")

        self.booking_id     = booking_id
        self.user           = user
        self.vehicle        = vehicle
        self.start_location = start_location
        self.end_location   = end_location
        self.distance       = distance
        self.passengers     = passengers
        self.notes          = notes.strip()
        self.promo_code     = promo_code
        self.discount       = max(0.0, discount)
        self.scheduled_time = scheduled_time
        self.payment_method = payment_method

        # Record when the booking was created
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Initial status depends on whether this is a scheduled or immediate ride
        self.status = "Scheduled" if scheduled_time else "Active"

        # Placeholder driver — replaced when a real driver accepts the booking
        self.driver: Driver = Driver(
            name      = "Unassigned",
            plate     = "Unassigned",
            rating    = 0.0,
            driver_id = "unassigned",
        )

        self.rating: Optional[int] = None   # Set after trip completion

        # Scheduled rides lock in the current (non-surge) rate at booking time
        self.surge: float = 1.0 if scheduled_time else self._check_surge()

        # Compute the final fare using the full pipeline
        self.total_cost: float = self._calculate_total_cost()

    # ── Surge Pricing ─────────────────────────────────────────────────────────

    def _check_surge(self) -> float:
        """
        Determine whether surge pricing applies based on the current time.
        Peak windows are defined in PEAK_WINDOWS at module level.

        Returns:
            float: 1.5 during peak hours, 1.0 otherwise.
        """
        hour = datetime.now().hour
        for start, end in PEAK_WINDOWS:
            if start <= hour <= end:
                return 1.5
        return 1.0

    @property
    def is_surge_active(self) -> bool:
        """True if a surge multiplier greater than 1.0 is currently applied."""
        return self.surge > 1.0

    # ── Fare Calculation ──────────────────────────────────────────────────────

    def _calculate_total_cost(self) -> float:
        """
        Internal fare pipeline:
            1. Ask the vehicle for the base fare (respects vehicle type rules).
            2. Apply the surge multiplier.
            3. Subtract the promo discount.
            4. Clamp to ₱0 so the final amount is never negative.

        Returns:
            float: Final fare in ₱.
        """
        # Pass passengers so vehicles that apply per-pax surcharges (e.g. Car)
        # can use it; vehicles that don't (Van, Bike) accept and ignore it.
        try:
            base = self.vehicle.calculate_cost(self.distance, self.passengers)
        except TypeError:
            # Fallback for vehicle implementations that only accept distance
            base = self.vehicle.calculate_cost(self.distance)

        surged = base * self.surge
        return max(0.0, round(surged - self.discount, 2))

    def recalculate_cost(self) -> None:
        """
        Re-run the fare pipeline and refresh total_cost in-place.
        Call this if the distance, discount, or surge changes after creation.
        """
        self.total_cost = self._calculate_total_cost()

    # ── Driver Assignment ─────────────────────────────────────────────────────

    def assign_driver(self, driver: Driver) -> None:
        """
        Assign a specific driver to this booking, replacing the placeholder.

        Args:
            driver (Driver): The Driver instance to assign.
        """
        self.driver = driver

    def auto_assign_driver(self) -> None:
        """Pick a random driver from the built-in pool and assign them."""
        self.driver = Driver.get_random_driver()

    # ── Status Transitions ────────────────────────────────────────────────────

    def cancel(self) -> str:
        """
        Cancel this booking regardless of its current status.

        Returns:
            str: Confirmation message or error if already cancelled/completed.
        """
        if self.status == "Cancelled":
            return "Booking is already cancelled."
        if self.status == "Completed":
            return "Cannot cancel a completed booking."
        self.status = "Cancelled"
        # Free up the vehicle
        if hasattr(self.vehicle, "set_available"):
            self.vehicle.set_available(True)
        return f"Booking #{self.booking_id} has been cancelled."

    def complete(self) -> str:
        """
        Mark this booking as completed.

        Returns:
            str: Confirmation message or error if the transition is invalid.
        """
        if self.status == "Completed":
            return "Booking is already completed."
        if self.status == "Cancelled":
            return "Cannot complete a cancelled booking."
        self.status = "Completed"
        if hasattr(self.vehicle, "set_available"):
            self.vehicle.set_available(True)
        return f"Booking #{self.booking_id} is now completed."

    def activate(self) -> str:
        """
        Transition a scheduled booking to 'Active' when its time arrives.
        Re-checks surge pricing so the live rate is applied at pick-up.

        Returns:
            str: Confirmation message or error if transition is invalid.
        """
        if self.status != "Scheduled":
            return f"Cannot activate a booking with status '{self.status}'."
        self.surge      = self._check_surge()
        self.total_cost = self._calculate_total_cost()
        self.status     = "Active"
        return f"Booking #{self.booking_id} is now active."

    def update_status(self, new_status: str) -> str:
        """
        Manually set the booking status to any valid value.

        Args:
            new_status (str): One of 'Active', 'Scheduled', 'Completed', 'Cancelled'.

        Returns:
            str: Confirmation message or error for unknown statuses.
        """
        if new_status not in VALID_STATUSES:
            return (
                f"Unknown status '{new_status}'. "
                f"Valid options: {', '.join(sorted(VALID_STATUSES))}."
            )
        self.status = new_status
        return f"Booking #{self.booking_id} status updated to '{new_status}'."

    # ── Rating ────────────────────────────────────────────────────────────────

    def add_rating(self, rating: int) -> str:
        """
        Attach a passenger star rating to a completed booking.

        Args:
            rating (int): Integer between 1 and 5 (inclusive).

        Returns:
            str: Success message or validation error.
        """
        if self.status != "Completed":
            return "You can only rate a completed booking."
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return "Rating must be an integer between 1 and 5."
        self.rating = rating
        return f"Thank you! You gave this ride {rating}⭐."

    # ── Serialisation / Deserialisation ───────────────────────────────────────

    def to_dict(self) -> dict:
        """
        Serialise this Booking to a plain dictionary suitable for JSON storage.

        Returns:
            dict: All booking fields, with driver fields stored flat
                  (no nested object) for backward-compatibility with
                  the existing bookings.json schema.
        """
        return {
            "booking_id":     self.booking_id,
            "user":           self.user,
            "vehicle_type":   self.vehicle.name,
            "start_location": self.start_location,
            "end_location":   self.end_location,
            "distance":       self.distance,
            "total_cost":     self.total_cost,
            "date":           self.date,
            "status":         self.status,
            "surge":          self.surge,
            "rating":         self.rating,
            "passengers":     self.passengers,
            "notes":          self.notes,
            "promo_code":     self.promo_code,
            "discount":       self.discount,
            "scheduled_time": self.scheduled_time,
            "payment_method": self.payment_method,
            # Driver stored flat to match the existing JSON schema
            "driver_name":    self.driver.name,
            "driver_plate":   self.driver.plate,
            "driver_rating":  self.driver.rating,
            "driver_id":      self.driver.driver_id,
        }

    # ── String Representations ────────────────────────────────────────────────

    def __str__(self) -> str:
        surge_label   = f" (Surge ×{self.surge})" if self.is_surge_active else ""
        rating_label  = f"⭐ {self.rating}/5" if self.rating else "Not yet rated"
        promo_label   = (
            f"\nPromo Code : {self.promo_code}  (−₱{self.discount:.2f})"
            if self.promo_code else ""
        )
        sched_label   = (
            f"\nScheduled  : {self.scheduled_time}"
            if self.scheduled_time else ""
        )
        return (
            f"{'─' * 50}\n"
            f"Booking ID   : #{self.booking_id}\n"
            f"Passenger    : {self.user}  |  Pax count: {self.passengers}\n"
            f"Vehicle      : {self.vehicle}\n"
            f"Driver       : {self.driver}\n"
            f"Route        : {self.start_location} → {self.end_location}\n"
            f"Distance     : {self.distance:.1f} km\n"
            f"Total Fare   : ₱{self.total_cost:.2f}{surge_label}"
            f"{promo_label}\n"
            f"Payment      : {self.payment_method}\n"
            f"Booked on    : {self.date}{sched_label}\n"
            f"Status       : {self.status}\n"
            f"Rating       : {rating_label}\n"
            f"Notes        : {self.notes or '(none)'}\n"
            f"{'─' * 50}"
        )

    def __repr__(self) -> str:
        return (
            f"Booking(id={self.booking_id!r}, "
            f"user={self.user!r}, "
            f"vehicle={self.vehicle.name!r}, "
            f"status={self.status!r}, "
            f"total_cost={self.total_cost!r})"
        )