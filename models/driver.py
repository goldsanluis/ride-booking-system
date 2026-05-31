"""
models/driver.py
----------------
Represents a driver assigned to a booking.
Includes a static roster of available drivers and a helper to pick one at random.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


import random


class Driver:
    """
    A driver with a name, vehicle plate, and passenger rating.

    Class Attribute:
        DRIVERS (list[dict]): Built-in pool of available drivers used
                              when randomly assigning one to a new booking.

    Attributes:
        driver_id (str | None): Persistent ID matching the drivers.json record,
                                or None for in-memory / unassigned drivers.
        name      (str): Driver's full name.
        plate     (str): Vehicle plate number.
        rating    (float): Average star rating out of 5.0.
    """

    # Static pool of available drivers used for random assignment
    DRIVERS = [
        {"name": "Juan dela Cruz", "plate": "ABC 1234", "rating": 4.8},
        {"name": "Maria Santos",   "plate": "XYZ 5678", "rating": 4.9},
        {"name": "Pedro Reyes",    "plate": "DEF 9012", "rating": 4.7},
        {"name": "Ana Garcia",     "plate": "GHI 3456", "rating": 4.6},
        {"name": "Jose Rizal",     "plate": "JKL 7890", "rating": 4.9},
        {"name": "Rosa Mendoza",   "plate": "MNO 2345", "rating": 4.5},
        {"name": "Carlo Ramos",    "plate": "PQR 6789", "rating": 4.8},
        {"name": "Liza Cruz",      "plate": "STU 0123", "rating": 4.7},
    ]

    def __init__(self, name, plate, rating, driver_id=None):
        self.driver_id = driver_id
        self.name      = name
        self.plate     = plate
        self.rating    = rating

    @staticmethod
    def get_random_driver():
        """
        Pick a random driver from the built-in pool and return
        a new Driver instance. Used when auto-assigning a driver
        to an incoming booking.

        Returns:
            Driver: A randomly selected Driver object.
        """
        driver_data = random.choice(Driver.DRIVERS)
        return Driver(
            driver_data["name"],
            driver_data["plate"],
            driver_data["rating"]
        )

    def __str__(self):
        return f"🚗 {self.name} | Plate: {self.plate} | Rating: ⭐{self.rating}"
