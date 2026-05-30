"""
models/car.py
-------------
Car vehicle type — standard sedan for up to 4 passengers.
Inherits from Vehicle and overrides calculate_cost() to apply a base flag-down fare.
"""

from models.vehicle import Vehicle


class Car(Vehicle):
    """
    Standard car: seats up to 4 passengers.
    Pricing: ₱40 base fare + ₱14 per km.
    """

    def __init__(self, vehicle_id, capacity=4):
        # Pass car-specific values up to the Vehicle constructor
        super().__init__(vehicle_id, "Car", capacity, cost_per_km=14.0)

    def calculate_cost(self, distance):
        """
        Polymorphic override: Car fare = ₱40 flag-down + ₱14/km.

        Args:
            distance (float): Trip distance in kilometres.

        Returns:
            float: Total fare in ₱.
        """
        base_fare = 40.0  # Flag-down / minimum charge
        return base_fare + (self.cost_per_km * distance)

    def __str__(self):
        return (f"Car (Capacity: {self.capacity}, "
                f"Base fare: ₱40, "
                f"Cost per km: ₱{self.cost_per_km})")
