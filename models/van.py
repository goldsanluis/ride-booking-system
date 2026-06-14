"""
models/van.py
-------------
Van vehicle type — large vehicle for groups of up to 10 passengers.
Inherits from Vehicle and overrides calculate_cost() with a higher base fare
and an optional luggage surcharge.

author = "Ghani Regina Gold San Luis"
group  = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


from models.vehicle import Vehicle


class Van(Vehicle):
    """
    Large passenger van: seats up to 10 passengers.

    Pricing (Philippine peso defaults):
        ₱80  flag-down fare  (first 1 km included)
        ₱20  per km thereafter
        ₱50  flat luggage surcharge when large_luggage=True
        ₱80  minimum fare floor

    Attributes (in addition to Vehicle):
        luggage_surcharge (float): Flat fee added when the passenger has
                                   bulky or oversized luggage.
    """

    # ── Class-Level Defaults ──────────────────────────────────────────────────
    DEFAULT_BASE_FARE:       float = 80.0
    DEFAULT_COST_PER_KM:    float = 20.0
    DEFAULT_MIN_FARE:        float = 80.0
    DEFAULT_CAPACITY:        int   = 10
    DEFAULT_LUGGAGE_SURCHARGE: float = 50.0

    def __init__(
        self,
        vehicle_id: int,
        capacity: int = DEFAULT_CAPACITY,
        luggage_surcharge: float = DEFAULT_LUGGAGE_SURCHARGE,
    ):
        """
        Initialise a Van with van-specific defaults.

        Args:
            vehicle_id        (int):   Unique identifier for this vehicle.
            capacity          (int):   Maximum passengers (default 10).
            luggage_surcharge (float): Flat fee for oversized luggage.
        """
        super().__init__(
            vehicle_id  = vehicle_id,
            name        = "Van",
            capacity    = capacity,
            cost_per_km = self.DEFAULT_COST_PER_KM,
            base_fare   = self.DEFAULT_BASE_FARE,
            min_fare    = self.DEFAULT_MIN_FARE,
        )
        self.luggage_surcharge = luggage_surcharge

    # ── Fare Calculation ──────────────────────────────────────────────────────

    def calculate_cost(
        self,
        distance: float,
        passengers: int = 1,
        large_luggage: bool = False,
    ) -> float:
        """
        Compute the Van fare:
            fare = base_fare + (cost_per_km × distance)
                 + (luggage_surcharge if large_luggage else 0)

        Result is clamped to min_fare.

        Args:
            distance      (float): Trip distance in kilometres (must be ≥ 0).
            passengers    (int):   Number of passengers (informational; vans
                                   do not apply a per-pax surcharge, but the
                                   parameter is accepted for API consistency).
            large_luggage (bool):  True to add the flat luggage surcharge.

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
            + (self.luggage_surcharge if large_luggage else 0.0)
        )
        return max(raw, self.min_fare)

    # ── Capacity Check (override for informative message) ─────────────────────

    def can_accommodate(self, passenger_count: int) -> bool:
        """Vans are best for groups; still delegates to the parent check."""
        return super().can_accommodate(passenger_count)

    # ── Serialisation ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Extend the base dict with Van-specific fields."""
        d = super().to_dict()
        d["luggage_surcharge"] = self.luggage_surcharge
        return d

    # ── String Representation ─────────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Van "
            f"(Capacity: {self.capacity} pax | "
            f"Base fare: ₱{self.base_fare:.2f} | "
            f"₱{self.cost_per_km:.2f}/km | "
            f"Luggage surcharge: +₱{self.luggage_surcharge:.2f} | "
            f"Min fare: ₱{self.min_fare:.2f})"
        )

    def __repr__(self) -> str:
        return (
            f"Van(id={self.vehicle_id!r}, "
            f"capacity={self.capacity!r}, "
            f"cost_per_km={self.cost_per_km!r}, "
            f"luggage_surcharge={self.luggage_surcharge!r})"
        )