"""
models/vehicle.py
-----------------
Base class for all vehicle types in the system.
Demonstrates encapsulation by bundling vehicle properties together,
and serves as the parent class for Car, Van, and Bike (inheritance).

author = "Ghani Regina Gold San Luis"
group  = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""



class Vehicle:
    """
    Abstract-style base class representing a generic vehicle.

    Subclasses must override calculate_cost() to implement their own
    pricing logic (polymorphism).

    Attributes:
        vehicle_id    (int):   Unique identifier for this vehicle instance.
        name          (str):   Display name of the vehicle type (e.g. 'Car').
        capacity      (int):   Maximum number of passengers the vehicle can carry.
        cost_per_km   (float): Base rate charged per kilometre travelled.
        is_available  (bool):  Whether the vehicle is free to accept new bookings.
        vehicle_type  (str):   Category string matching JSON records ('Car','Van','Bike').
        min_fare      (float): Minimum possible fare regardless of distance.
        base_fare     (float): Fixed flag-down charge applied before per-km rate.
    """

    # Minimum fare floor (₱) — can be overridden by subclasses
    MIN_FARE: float = 0.0

    def __init__(
        self,
        vehicle_id: int,
        name: str,
        capacity: int,
        cost_per_km: float,
        base_fare: float = 0.0,
        min_fare: float = 0.0,
    ):
        self.vehicle_id   = vehicle_id
        self.name         = name
        self.capacity     = capacity
        self.cost_per_km  = cost_per_km
        self.base_fare    = base_fare
        self.min_fare     = min_fare
        self.is_available = True          # Tracks real-time availability
        self.vehicle_type = name          # Mirrors name; used in serialisation

    # ── Availability ──────────────────────────────────────────────────────────

    def set_available(self, status: bool) -> None:
        """
        Update the vehicle's availability flag.

        Args:
            status (bool): True if the vehicle is free; False if occupied.
        """
        self.is_available = status

    def get_availability_label(self) -> str:
        """Return a human-readable availability string."""
        return "Available" if self.is_available else "Unavailable"

    # ── Capacity Validation ───────────────────────────────────────────────────

    def can_accommodate(self, passenger_count: int) -> bool:
        """
        Check whether the vehicle can carry the requested number of passengers.

        Args:
            passenger_count (int): Number of passengers to check.

        Returns:
            bool: True if passenger_count ≤ capacity, False otherwise.
        """
        return passenger_count <= self.capacity

    # ── Fare Calculation ──────────────────────────────────────────────────────

    def calculate_cost(self, distance: float) -> float:
        """
        Calculate the fare for a given distance.

        Base implementation:
            fare = base_fare + (cost_per_km × distance)
            clamped to min_fare so the fare never falls below the minimum.

        Subclasses may override this to apply additional rules (e.g. time-of-day
        multipliers or luggage surcharges).

        Args:
            distance (float): Trip distance in kilometres. Must be ≥ 0.

        Returns:
            float: Total fare in Philippine Pesos (₱), never below min_fare.

        Raises:
            ValueError: If distance is negative.
        """
        if distance < 0:
            raise ValueError(f"Distance must be non-negative; got {distance}.")
        raw = self.base_fare + (self.cost_per_km * distance)
        return max(raw, self.min_fare)

    # ── Serialisation Helpers ─────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """
        Return a plain dictionary representation of this vehicle.
        Used when storing vehicle metadata alongside booking records.

        Returns:
            dict: Keys — vehicle_id, name, capacity, cost_per_km,
                  base_fare, min_fare, is_available.
        """
        return {
            "vehicle_id":   self.vehicle_id,
            "name":         self.name,
            "capacity":     self.capacity,
            "cost_per_km":  self.cost_per_km,
            "base_fare":    self.base_fare,
            "min_fare":     self.min_fare,
            "is_available": self.is_available,
        }

    # ── String Representations ────────────────────────────────────────────────

    def __str__(self) -> str:
        avail = self.get_availability_label()
        return (
            f"{self.name} "
            f"(Capacity: {self.capacity} pax | "
            f"Base fare: ₱{self.base_fare:.2f} | "
            f"₱{self.cost_per_km:.2f}/km | "
            f"Min fare: ₱{self.min_fare:.2f} | "
            f"{avail})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.vehicle_id!r}, "
            f"capacity={self.capacity!r}, "
            f"cost_per_km={self.cost_per_km!r})"
        )