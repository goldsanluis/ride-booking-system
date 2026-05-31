"""
models/bike.py
--------------
Bike vehicle type — motorcycle for solo riders, cheapest option.
Inherits from Vehicle and overrides calculate_cost() with the lowest fare structure.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


from models.vehicle import Vehicle


class Bike(Vehicle):
    """
    Motorcycle: seats 1 passenger only.
    Pricing: ₱20 base fare + ₱8 per km.
    """

    def __init__(self, vehicle_id, capacity=1):
        # Pass bike-specific values up to the Vehicle constructor
        super().__init__(vehicle_id, "Bike", capacity, cost_per_km=8.0)

    def calculate_cost(self, distance):
        """
        Polymorphic override: Bike fare = ₱20 flag-down + ₱8/km.
        Lowest rates due to small size and fuel efficiency.

        Args:
            distance (float): Trip distance in kilometres.

        Returns:
            float: Total fare in ₱.
        """
        base_fare = 20.0  # Cheapest flag-down rate
        return base_fare + (self.cost_per_km * distance)

    def __str__(self):
        return (f"Bike (Capacity: {self.capacity}, "
                f"Base fare: ₱20, "
                f"Cost per km: ₱{self.cost_per_km})")
