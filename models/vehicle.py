"""
models/vehicle.py
-----------------
Base class for all vehicle types in the system.
Demonstrates encapsulation by bundling vehicle properties together,
and serves as the parent class for Car, Van, and Bike (inheritance).

author = "Ghani Regina Gold San Luis"
group = "Group 6"
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
        vehicle_id  (int): Unique identifier for this vehicle instance.
        name        (str): Display name of the vehicle type (e.g. 'Car').
        capacity    (int): Maximum number of passengers the vehicle can carry.
        cost_per_km (float): Base rate charged per kilometre travelled.
    """

    def __init__(self, vehicle_id, name, capacity, cost_per_km):
        self.vehicle_id  = vehicle_id
        self.name        = name
        self.capacity    = capacity
        self.cost_per_km = cost_per_km

    def calculate_cost(self, distance):
        """
        Calculate the fare for a given distance.
        Base implementation: flat rate × distance (no base fare).
        Subclasses override this to add their own base fares and rules.

        Args:
            distance (float): Trip distance in kilometres.

        Returns:
            float: Total fare in Philippine Pesos (₱).
        """
        return self.cost_per_km * distance

    def __str__(self):
        return (f"{self.name} "
                f"(Capacity: {self.capacity}, "
                f"Cost per km: ₱{self.cost_per_km})")
