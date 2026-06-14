"""
models/bike.py
--------------
Bike vehicle type — motorcycle for solo riders; cheapest and fastest option.
Inherits from Vehicle and overrides calculate_cost() with the lowest fare
structure, plus a weather surcharge for rainy conditions.

author = "Ghani Regina Gold San Luis"
group  = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


from models.vehicle import Vehicle


class Bike(Vehicle):
    """
    Motorcycle: seats 1 passenger only (driver + 1 pax, LTFRB-compliant).

    Pricing (Philippine peso defaults):
        ₱20  flag-down fare  (first 1 km included)
        ₱8   per km thereafter
        ₱10  flat weather surcharge when raining=True
        ₱20  minimum fare floor

    Attributes (in addition to Vehicle):
        weather_surcharge (float): Flat fee added during bad weather to
                                   compensate for reduced speed and safety risk.
    """

    # ── Class-Level Defaults ──────────────────────────────────────────────────
    DEFAULT_BASE_FARE:        float = 20.0
    DEFAULT_COST_PER_KM:     float = 8.0
    DEFAULT_MIN_FARE:         float = 20.0
    DEFAULT_CAPACITY:         int   = 1
    DEFAULT_WEATHER_SURCHARGE: float = 10.0

    def __init__(
        self,
        vehicle_id: int,
        capacity: int = DEFAULT_CAPACITY,
        weather_surcharge: float = DEFAULT_WEATHER_SURCHARGE,
    ):
        """
        Initialise a Bike with bike-specific defaults.

        Args:
            vehicle_id        (int):   Unique identifier for this vehicle.
            capacity          (int):   Maximum passengers — always 1 for a bike.
            weather_surcharge (float): Extra flat charge in bad weather.
        """
        # Bikes carry exactly 1 passenger regardless of what is passed in
        super().__init__(
            vehicle_id  = vehicle_id,
            name        = "Bike",
            capacity    = min(capacity, 1),   # Enforce single-pax limit
            cost_per_km = self.DEFAULT_COST_PER_KM,
            base_fare   = self.DEFAULT_BASE_FARE,
            min_fare    = self.DEFAULT_MIN_FARE,
        )
        self.weather_surcharge = weather_surcharge

    # ── Capacity Enforcement ──────────────────────────────────────────────────

    def can_accommodate(self, passenger_count: int) -> bool:
        """
        Bikes accept exactly 1 passenger (aside from the driver).
        Always returns False for passenger_count > 1.
        """
        return passenger_count == 1

    # ── Fare Calculation ──────────────────────────────────────────────────────

    def calculate_cost(
        self,
        distance: float,
        passengers: int = 1,
        raining: bool = False,
    ) -> float:
        """
        Compute the Bike fare:
            fare = base_fare + (cost_per_km × distance)
                 + (weather_surcharge if raining else 0)

        Result is clamped to min_fare.

        Args:
            distance   (float): Trip distance in kilometres (must be ≥ 0).
            passengers (int):   Must be 1 for bikes; raises ValueError otherwise.
            raining    (bool):  True to add the flat weather surcharge.

        Returns:
            float: Total fare in ₱.

        Raises:
            ValueError: If distance < 0 or passengers != 1.
        """
        if distance < 0:
            raise ValueError(f"Distance must be non-negative; got {distance}.")
        if passengers != 1:
            raise ValueError(
                f"Bikes can only carry 1 passenger; got {passengers}. "
                "Please choose a Car or Van for group rides."
            )

        raw = (
            self.base_fare
            + (self.cost_per_km * distance)
            + (self.weather_surcharge if raining else 0.0)
        )
        return max(raw, self.min_fare)

    # ── Serialisation ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Extend the base dict with Bike-specific fields."""
        d = super().to_dict()
        d["weather_surcharge"] = self.weather_surcharge
        return d

    # ── String Representation ─────────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Bike "
            f"(Capacity: {self.capacity} pax | "
            f"Base fare: ₱{self.base_fare:.2f} | "
            f"₱{self.cost_per_km:.2f}/km | "
            f"Weather surcharge: +₱{self.weather_surcharge:.2f} | "
            f"Min fare: ₱{self.min_fare:.2f})"
        )

    def __repr__(self) -> str:
        return (
            f"Bike(id={self.vehicle_id!r}, "
            f"capacity={self.capacity!r}, "
            f"cost_per_km={self.cost_per_km!r}, "
            f"weather_surcharge={self.weather_surcharge!r})"
        )