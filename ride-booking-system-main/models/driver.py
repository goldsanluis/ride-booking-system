import random

class Driver:
    DRIVERS = [
        {"name": "Juan dela Cruz", "plate": "ABC 1234", "rating": 4.8},
        {"name": "Maria Santos", "plate": "XYZ 5678", "rating": 4.9},
        {"name": "Pedro Reyes", "plate": "DEF 9012", "rating": 4.7},
        {"name": "Ana Garcia", "plate": "GHI 3456", "rating": 4.6},
        {"name": "Jose Rizal", "plate": "JKL 7890", "rating": 4.9},
        {"name": "Rosa Mendoza", "plate": "MNO 2345", "rating": 4.5},
        {"name": "Carlo Ramos", "plate": "PQR 6789", "rating": 4.8},
        {"name": "Liza Cruz", "plate": "STU 0123", "rating": 4.7},
    ]

    def __init__(self, name, plate, rating, driver_id=None):
        self.driver_id = driver_id
        self.name = name
        self.plate = plate
        self.rating = rating

    @staticmethod
    def get_random_driver():
        driver_data = random.choice(Driver.DRIVERS)
        return Driver(
            driver_data["name"],
            driver_data["plate"],
            driver_data["rating"]
        )

    def __str__(self):
        return f"🚗 {self.name} | Plate: {self.plate} | Rating: ⭐{self.rating}"
