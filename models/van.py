"""
models/van.py
-------------
Van vehicle type — large vehicle for groups of up to 10 passengers.
Inherits from Vehicle and overrides calculate_cost() with a higher base fare.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


from models.vehicle import Vehicle


class Van(Vehicle):
    """
    Large van: seats up to 10 passengers.
    Pricing: ₱80 base fare + ₱20 per km.
    """

    def __init__(self, vehicle_id, capacity=10):
        # Pass van-specific values up to the Vehicle constructor
        super().__init__(vehicle_id, "Van", capacity, cost_per_km=20.0)

    def calculate_cost(self, distance):
        """
        Polymorphic override: Van fare = ₱80 flag-down + ₱20/km.
        Higher rates reflect the larger vehicle size and fuel cost.

        Args:
            distance (float): Trip distance in kilometres.

        Returns:
            float: Total fare in ₱.
        """
        base_fare = 80.0  # Higher flag-down for larger vehicle
        return base_fare + (self.cost_per_km * distance)

    def __str__(self):
        return (f"Van (Capacity: {self.capacity}, "
                f"Base fare: ₱80, "
                f"Cost per km: ₱{self.cost_per_km})")
