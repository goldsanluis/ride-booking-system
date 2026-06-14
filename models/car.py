"""
models/car.py
-------------
Car vehicle type — standard sedan for up to 4 passengers.
Inherits from Vehicle and overrides calculate_cost() to apply a base flag-down
fare and an optional extra-passenger surcharge.

author = "Ghani Regina Gold San Luis"
group  = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


from models.vehicle import Vehicle


class Car(Vehicle):
    """
    Standard sedan: seats up to 4 passengers.

    Pricing (Philippine peso defaults):
        ₱40  flag-down fare  (first 1 km included)
        ₱14  per km thereafter
        ₱5   per extra passenger beyond the first (optional surcharge)
        ₱40  minimum fare floor

    Attributes (in addition to Vehicle):
        extra_passenger_rate (float): Additional charge per passenger beyond 1.
    """

    # ── Class-Level Defaults ──────────────────────────────────────────────────
    DEFAULT_BASE_FARE:           float = 40.0
    DEFAULT_COST_PER_KM:         float = 14.0
    DEFAULT_MIN_FARE:            float = 40.0
    DEFAULT_CAPACITY:            int   = 4
    DEFAULT_EXTRA_PASSENGER_RATE: float = 5.0   # ₱ per pax beyond the first

    def __init__(
        self,
        vehicle_id: int,
        capacity: int = DEFAULT_CAPACITY,
        extra_passenger_rate: float = DEFAULT_EXTRA_PASSENGER_RATE,
    ):
        """
        Initialise a Car with car-specific defaults.

        Args:
            vehicle_id           (int):   Unique identifier for this vehicle.
            capacity             (int):   Maximum passengers (default 4).
            extra_passenger_rate (float): Surcharge per pax beyond the first.
        """
        super().__init__(
            vehicle_id  = vehicle_id,
            name        = "Car",
            capacity    = capacity,
            cost_per_km = self.DEFAULT_COST_PER_KM,
            base_fare   = self.DEFAULT_BASE_FARE,
            min_fare    = self.DEFAULT_MIN_FARE,
        )
        self.extra_passenger_rate = extra_passenger_rate

    # ── Fare Calculation ──────────────────────────────────────────────────────

    def calculate_cost(self, distance: float, passengers: int = 1) -> float:
        """
        Compute the Car fare:
            fare = base_fare + (cost_per_km × distance)
                 + extra_passenger_rate × max(0, passengers − 1)

        The result is clamped to min_fare so it never falls below the flag-down.

        Args:
            distance   (float): Trip distance in kilometres (must be ≥ 0).
            passengers (int):   Number of passengers (default 1).

        Returns:
            float: Total fare in ₱.

        Raises:
            ValueError: If distance < 0 or passengers < 1.
        """
        if distance < 0:
            raise ValueError(f"Distance must be non-negative; got {distance}.")
        if passengers < 1:
            raise ValueError(f"Passenger count must be at least 1; got {passengers}.")

        raw = (
            self.base_fare
            + (self.cost_per_km * distance)
            + (self.extra_passenger_rate * max(0, passengers - 1))
        )
        return max(raw, self.min_fare)

    # ── Serialisation ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Extend the base dict with Car-specific fields."""
        d = super().to_dict()
        d["extra_passenger_rate"] = self.extra_passenger_rate
        return d

    # ── String Representation ─────────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Car "
            f"(Capacity: {self.capacity} pax | "
            f"Base fare: ₱{self.base_fare:.2f} | "
            f"₱{self.cost_per_km:.2f}/km | "
            f"Extra pax: +₱{self.extra_passenger_rate:.2f} each | "
            f"Min fare: ₱{self.min_fare:.2f})"
        )

    def __repr__(self) -> str:
        return (
            f"Car(id={self.vehicle_id!r}, "
            f"capacity={self.capacity!r}, "
            f"cost_per_km={self.cost_per_km!r}, "
            f"extra_passenger_rate={self.extra_passenger_rate!r})"
        )