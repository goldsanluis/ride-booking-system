"""
models/booking.py
-----------------
Represents a single ride booking made by a passenger.
Handles fare calculation, surge pricing, promo discounts, and status transitions.
"""

from datetime import datetime
from models.driver import Driver


class Booking:
    """
    A ride booking linking a passenger, a vehicle, and a route.

    Fare calculation pipeline:
        1. Vehicle.calculate_cost(distance)  →  base fare
        2. × surge multiplier               →  surged fare
        3. − promo discount                 →  final total

    Status lifecycle:
        New booking  →  'Active' (immediate) or 'Scheduled' (future ride)
        Active       →  'Completed'  (via complete())
        Any          →  'Cancelled'  (via cancel())

    Attributes:
        booking_id     (int):         Unique booking identifier.
        user           (str):         Username of the passenger who booked.
        vehicle        (Vehicle):     Vehicle instance (Car, Van, or Bike).
        start_location (str):         Pick-up location name.
        end_location   (str):         Drop-off location name.
        distance       (float):       Trip distance in kilometres.
        passengers     (int):         Number of passengers (informational).
        notes          (str):         Optional instructions for the driver.
        promo_code     (str | None):  Applied promo code, if any.
        discount       (float):       Discount amount in ₱ from promo.
        scheduled_time (str | None):  ISO-style datetime string for future rides.
        date           (str):         Timestamp when the booking was created.
        status         (str):         Current status ('Active', 'Scheduled',
                                      'Completed', or 'Cancelled').
        driver         (Driver):      Assigned driver (defaults to 'Unassigned').
        rating         (int | None):  Passenger's 1–5 star rating after the ride.
        surge          (float):       Surge multiplier applied to the fare (1.0 or 1.5).
        total_cost     (float):       Final fare after surge and discount.
    """

    def __init__(self, booking_id, user, vehicle, start_location, end_location,
                 distance, passengers=1, notes="", promo_code=None, discount=0.0,
                 scheduled_time=None):

        self.booking_id     = booking_id
        self.user           = user
        self.vehicle        = vehicle
        self.start_location = start_location
        self.end_location   = end_location
        self.distance       = distance
        self.passengers     = passengers
        self.notes          = notes
        self.promo_code     = promo_code
        self.discount       = discount
        self.scheduled_time = scheduled_time

        # Record the exact creation time
        self.date   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Scheduled rides start as 'Scheduled'; immediate rides start as 'Active'
        self.status = "Scheduled" if scheduled_time else "Active"

        # Placeholder driver — replaced when a real driver accepts the ride
        self.driver = Driver("Unassigned", "Unassigned", 0.0, driver_id="unassigned")

        self.rating = None  # Set by the passenger after trip completion

        # Scheduled rides skip surge pricing (fare is locked in at booking time)
        self.surge = 1.0 if scheduled_time else self.check_surge()

        # Calculate the final fare once all fields are set
        self.total_cost = self.calculate_total_cost()

    # ── Surge Pricing ─────────────────────────────────────────────────────────

    def check_surge(self):
        """
        Apply surge pricing during peak commute hours.
        Peak windows: 7–9 AM and 5–8 PM.

        Returns:
            float: 1.5 during peak hours, 1.0 otherwise.
        """
        hour = datetime.now().hour
        if (7 <= hour <= 9) or (17 <= hour <= 20):
            return 1.5  # 50 % surge during rush hour
        return 1.0

    # ── Fare Calculation ──────────────────────────────────────────────────────

    def calculate_total_cost(self):
        """
        Compute the final fare:
            (vehicle base cost × surge multiplier) − promo discount.
        Clamped to ₱0 so the fare never goes negative.

        Returns:
            float: Final fare in ₱.
        """
        base_cost = self.vehicle.calculate_cost(self.distance)
        return max(0.0, (base_cost * self.surge) - self.discount)

    # ── Status Transitions ────────────────────────────────────────────────────

    def cancel(self):
        """Mark this booking as cancelled."""
        self.status = "Cancelled"

    def complete(self):
        """Mark this booking as completed."""
        self.status = "Completed"

    def activate(self):
        """
        Transition a scheduled booking to 'Active' when its time arrives.
        Re-checks surge pricing so the live rate is applied at pickup.
        """
        self.surge      = self.check_surge()
        self.total_cost = self.calculate_total_cost()
        self.status     = "Active"

    # ── Rating ────────────────────────────────────────────────────────────────

    def add_rating(self, rating):
        """
        Attach a passenger star rating to a completed booking.

        Args:
            rating (int): Star rating between 1 and 5 (inclusive).

        Returns:
            str: Success or error message.
        """
        if 1 <= rating <= 5:
            self.rating = rating
            return f"Rating of {rating}⭐ added successfully!"
        return "Rating must be between 1 and 5!"

    # ── String Representation ─────────────────────────────────────────────────

    def __str__(self):
        # Build optional display segments
        surge_text      = f" (Surge: {self.surge}x)" if self.surge > 1.0 else ""
        rating_text     = f"⭐{self.rating}" if self.rating else "Not rated"
        promo_text      = f"\nPromo: {self.promo_code} (-₱{self.discount:.2f})" if self.promo_code else ""
        passengers_text = f"\nPassengers: {self.passengers}" if self.passengers > 1 else ""
        notes_text      = f"\nNotes: {self.notes}" if self.notes else ""
        sched_text      = f"\nScheduled: {self.scheduled_time}" if self.scheduled_time else ""

        return (
            f"Booking ID: {self.booking_id}\n"
            f"User: {self.user}\n"
            f"Vehicle: {self.vehicle}\n"
            f"Driver: {self.driver}\n"
            f"From: {self.start_location} → To: {self.end_location}\n"
            f"Distance: {self.distance} km\n"
            f"Total Cost: ₱{self.total_cost:.2f}{surge_text}{promo_text}\n"
            f"Date: {self.date}\n"
            f"Status: {self.status}\n"
            f"Rating: {rating_text}{passengers_text}{notes_text}{sched_text}"
        )
